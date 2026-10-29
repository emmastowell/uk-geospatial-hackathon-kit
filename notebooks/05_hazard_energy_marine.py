# Databricks notebook source
# MAGIC %md
# MAGIC # 05. Hazard, energy and marine (the awkward sources)
# MAGIC Each step fails soft and logs to `_load_log`.
# MAGIC
# MAGIC | Table | Source | Note |
# MAGIC |---|---|---|
# MAGIC | `ea_flood_areas`, `ea_flood_warnings`, `ea_stations` | EA real-time flood-monitoring API | Live snapshot, open, no key |
# MAGIC | `ea_rofrs_postcodes` | EA Risk of Flooding from Rivers and Sea, postcodes at risk | Discovered via data.gov.uk |
# MAGIC | `desnz_repd` | DESNZ Renewable Energy Planning Database | Scraped from gov.uk |
# MAGIC | `osm_sar_facilities` | OpenStreetMap via Overpass | Volunteer-mapped, not an official register |
# MAGIC
# MAGIC DfT EV charging statistics are in 07c. EV point locations come from `overture_places` (notebook 03).

# COMMAND ----------
import csv, glob, io, os, sys, zipfile

sys.path.insert(0, os.getcwd())
import requests
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils)
CKAN = "https://ckan.publishing.service.gov.uk/api/3/action"


def ckan_resources(package):
    return requests.get(f"{CKAN}/package_show", params={"id": package}, headers=hc.UA, timeout=60).json()["result"]["resources"]


def first_float(v):
    """Some EA stations report lat/long as a list (multi-parameter stations). Take the first value."""
    if isinstance(v, list):
        v = v[0] if v else None
    return float(v) if v is not None else None


# COMMAND ----------
# MAGIC %md ## Environment Agency flood monitoring (areas, warnings, stations incl. tidal)

# COMMAND ----------
EA = "https://environment.data.gov.uk/flood-monitoring/id"

with hc.step(spark, cfg, "ea_flood_areas"):
    items = requests.get(f"{EA}/floodAreas", params={"_limit": 10000}, headers=hc.UA, timeout=120).json()["items"]
    rows = [(i.get("notation"), i.get("label"), i.get("description"), i.get("riverOrSea"), i.get("county"),
             float(i.get("lat")) if i.get("lat") else None, float(i.get("long")) if i.get("long") else None,
             i.get("polygon")) for i in items]
    df = spark.createDataFrame(rows, "area_id string, label string, description string, river_or_sea string, "
                                     "county string, lat double, lon double, polygon_url string")
    hc.save(hc.add_h3(df, "lon", "lat", 8), cfg, "ea_flood_areas")

with hc.step(spark, cfg, "ea_flood_warnings"):
    items = requests.get(f"{EA}/floods", headers=hc.UA, timeout=120).json()["items"]
    rows = [(i.get("floodAreaID"), i.get("severity"), i.get("severityLevel"), i.get("message"), i.get("timeRaised"),
             i.get("eaAreaName")) for i in items]
    df = spark.createDataFrame(rows, "area_id string, severity string, severity_level int, message string, "
                                     "time_raised string, ea_area string").withColumn("snapshot_ts", F.current_timestamp())
    hc.save(df, cfg, "ea_flood_warnings")

with hc.step(spark, cfg, "ea_stations"):
    items = requests.get(f"{EA}/stations", params={"_limit": 10000}, headers=hc.UA, timeout=180).json()["items"]
    rows = [(i.get("notation"), i.get("label"), i.get("riverName"), i.get("town"), i.get("catchmentName"),
             i.get("stationType") if isinstance(i.get("stationType"), str) else None,
             first_float(i.get("lat")), first_float(i.get("long")),
             str([m.get("parameter") for m in i["measures"]] if isinstance(i.get("measures"), list) else i.get("measures")))
            for i in items]
    df = spark.createDataFrame(rows, "station_id string, label string, river_name string, town string, catchment string, "
                                     "station_type string, lat double, lon double, measures string")
    hc.save(hc.add_h3(df.filter("lat IS NOT NULL"), "lon", "lat", 8), cfg, "ea_stations")

# COMMAND ----------
# MAGIC %md ## EA Risk of Flooding from Rivers and Sea: postcodes in areas at risk

# COMMAND ----------
with hc.step(spark, cfg, "ea_rofrs_postcodes"):
    res = [r for r in ckan_resources("risk-of-flooding-from-rivers-and-sea-postcodes-in-areas-at-risk2")
           if r["url"].lower().endswith((".csv", ".zip", ".xlsx"))]
    print([r["url"] for r in res])
    url = res[0]["url"]
    f = hc.download(url, f"{cfg['vol']}/ea/rofrs_postcodes{os.path.splitext(url)[1]}")
    if f.endswith(".zip"):
        out = f"{cfg['vol']}/ea/rofrs_postcodes"
        with zipfile.ZipFile(f) as z:
            z.extractall(out)
        f = glob.glob(f"{out}/**/*.csv", recursive=True)[0]
    hc.save(hc.snake_columns(spark.read.option("header", True).csv(f)), cfg, "ea_rofrs_postcodes")

# COMMAND ----------
# MAGIC %md ## DESNZ Renewable Energy Planning Database (energy asset locations)

# COMMAND ----------
with hc.step(spark, cfg, "desnz_repd"):
    page = "https://www.gov.uk/government/publications/renewable-energy-planning-database-monthly-extract"
    links = hc.scrape_links(page, r"https://assets\.publishing\.service\.gov\.uk/[^\"']+\.csv")
    if not links:
        raise RuntimeError(f"no CSV link found on {page}; download manually and place in {cfg['vol']}/desnz/repd.csv")
    f = hc.download(links[0], f"{cfg['vol']}/desnz/repd.csv")
    df = hc.snake_columns(spark.read.option("header", True).option("multiLine", True).option("escape", '"')
                          .option("encoding", "latin1").csv(f))
    # REPD gives OSGB easting/northing, not lon/lat
    e = next(c for c in df.columns if c.startswith("x_coordinate"))
    n = next(c for c in df.columns if c.startswith("y_coordinate"))
    df = df.withColumn("easting", F.regexp_replace(e, "[^0-9.]", "").cast("double")).withColumn("northing", F.regexp_replace(n, "[^0-9.]", "").cast("double"))
    if hc.has_native_geometry(spark):
        df = df.withColumn("geom", F.expr("ST_Transform(ST_Point(easting, northing, 27700), 4326)"))
        df = hc.add_h3(df.withColumn("lon", F.expr("ST_X(geom)")).withColumn("lat", F.expr("ST_Y(geom)")), "lon", "lat", 8)
    hc.save(df, cfg, "desnz_repd")

# COMMAND ----------
# MAGIC %md ## Marine: OSM search and rescue facilities

# COMMAND ----------
with hc.step(spark, cfg, "osm_sar_facilities"):
    q = """[out:json][timeout:120];
    area["ISO3166-1"="GB"][admin_level=2]->.gb;
    (nwr["emergency"="lifeboat_station"](area.gb);
     nwr["amenity"="coast_guard"](area.gb);
     nwr["emergency"="coast_guard"](area.gb);
     nwr["seamark:type"="rescue_station"](area.gb););
    out center tags;"""
    # Overpass rejects browser-style UAs with 406 and is flaky under load (504), so use a plain UA and retry.
    import time
    for attempt in range(4):
        r = requests.post("https://overpass-api.de/api/interpreter", data={"data": q}, timeout=180,
                          headers={"User-Agent": "two-postcodes-hackathon/1.0", "Accept": "*/*"})
        if r.status_code == 200:
            break
        print(f"overpass {r.status_code}, retry {attempt + 1}")
        time.sleep(15 * (attempt + 1))
    r.raise_for_status()
    els = r.json()["elements"]
    rows = [(e["type"] + str(e["id"]), e.get("tags", {}).get("name"),
             e.get("tags", {}).get("emergency") or e.get("tags", {}).get("amenity") or e.get("tags", {}).get("seamark:type"),
             e.get("lat") or e.get("center", {}).get("lat"), e.get("lon") or e.get("center", {}).get("lon"),
             e.get("tags", {}).get("operator")) for e in els]
    df = spark.createDataFrame(rows, "osm_id string, name string, facility_type string, lat double, lon double, operator string")
    hc.save(hc.add_h3(df.filter("lat IS NOT NULL"), "lon", "lat", 8), cfg, "osm_sar_facilities")
