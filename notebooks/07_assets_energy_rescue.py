# Databricks notebook source
# MAGIC %md
# MAGIC # 07. Asset condition, grid capacity and rescue stations
# MAGIC Official and operator datasets that complement the Overture and OpenStreetMap layers from notebooks 03 and 05.
# MAGIC
# MAGIC | Table(s) | Source | Notes |
# MAGIC |---|---|---|
# MAGIC | `ea_flood_defences` | EA Spatial Flood Defences (OGC API Features) | flood and coastal defence assets with condition grades |
# MAGIC | `nged_ltds_capacity_heatmap` (+07b, 07d) | NGED and Northern Powergrid open data | distribution network capacity (regional coverage) |
# MAGIC | `rnli_lifeboat_stations` | RNLI Geospatial Team ArcGIS service | RNLI stations only (not HM Coastguard) |
# MAGIC | `dft_evci_*` (see 07c) | DfT EV charging infrastructure statistics data tables | area level counts, not devices |
# MAGIC
# MAGIC Every source goes through a file and Spark's reader. Passing pandas frames through `spark.createDataFrame` is slow on serverless.

# COMMAND ----------
# MAGIC %pip install python-calamine
# MAGIC dbutils.library.restartPython()

# COMMAND ----------
import io, json, os, re, sys, time, datetime

sys.path.insert(0, os.getcwd())
import pandas as pd
import requests
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils)
HDR = {"User-Agent": "two-postcodes-hackathon/1.0"}


def get(url, retries=4, **kw):
    for i in range(retries):
        try:
            r = requests.get(url, headers=HDR, timeout=180, **kw)
            r.raise_for_status()
            return r
        except Exception as e:  # noqa: BLE001
            print(f"GET attempt {i + 1}/{retries} failed: {str(e)[:120]}")
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"GET failed: {url}")


def pdf_to_table(pdf, table, lon=None, lat=None, easting=None, northing=None):
    """Small pandas frame -> CSV on the volume -> Spark table. Adds geometry and H3 where coordinates exist."""
    path = f"{cfg['vol']}/gap/{table}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pdf.to_csv(path, index=False)
    df = hc.snake_columns(spark.read.option("header", True).option("multiLine", True).option("escape", '"')
                          .option("inferSchema", True).csv(path))
    if easting and northing:
        df = (df.withColumn("easting_n", F.col(hc.snake(easting)).cast("double"))
                .withColumn("northing_n", F.col(hc.snake(northing)).cast("double")))
        if hc.has_native_geometry(spark):
            df = df.withColumn("geom", F.expr("ST_Transform(ST_Point(easting_n, northing_n, 27700), 4326)"))
            df = hc.add_h3(df.withColumn("lon", F.expr("ST_X(geom)")).withColumn("lat", F.expr("ST_Y(geom)")), "lon", "lat", 8)
        df = df.drop("easting_n", "northing_n")
    elif lon and lat:
        df = df.withColumn("lon", F.col(hc.snake(lon)).cast("double")).withColumn("lat", F.col(hc.snake(lat)).cast("double"))
        df = hc.add_h3(df.filter("lon IS NOT NULL AND lat IS NOT NULL"), "lon", "lat", 8)
        if hc.has_native_geometry(spark):
            df = df.withColumn("geom", F.expr("ST_Point(lon, lat, 4326)"))
    hc.save(df, cfg, table)


# COMMAND ----------
# MAGIC %md ## 1. EA Spatial Flood Defences (asset inventory with condition)
# MAGIC About 141k assets, 1000 per page.

# COMMAND ----------
with hc.step(spark, cfg, "ea_flood_defences"):
    base = ("https://environment.data.gov.uk/spatialdata/spatial-flood-defences-including-standardised-attributes/"
            "ogc/features/v1/collections/Spatial_Flood_Defences_Including_Standardised_Attributes/items")
    url, rows, page = f"{base}?f=json&limit=1000", [], 0
    while url:
        j = get(url).json()
        for f in j["features"]:
            r = dict(f["properties"])
            r["geojson"] = json.dumps(f["geometry"]) if f.get("geometry") else None
            rows.append(r)
        url = next((l["href"] for l in j["links"] if l.get("rel") == "next"), None)
        page += 1
        if page % 20 == 0:
            print(f"{len(rows):,} assets", flush=True)
    pdf = pd.DataFrame(rows)
    # Keep numeric columns numeric (a column that is entirely numbers or nulls); leave the rest as text.
    for c in pdf.columns:
        if c != "geojson":
            num = pd.to_numeric(pdf[c], errors="coerce")
            if num.notna().sum() == pdf[c].replace("", None).notna().sum() and num.notna().any():
                pdf[c] = num
    part_dir = f"{cfg['vol']}/gap/ea_flood_defences"
    os.makedirs(part_dir, exist_ok=True)
    pdf.to_parquet(f"{part_dir}/all.parquet", index=False)
    df = hc.snake_columns(spark.read.parquet(part_dir))
    if hc.has_native_geometry(spark):
        df = df.withColumn("geom", F.expr("ST_GeomFromGeoJSON(geojson)")).drop("geojson")
    hc.save(df, cfg, "ea_flood_defences")

# COMMAND ----------
# MAGIC %md ## 2. Grid capacity from DNO open data

# COMMAND ----------
# Northern Powergrid's capacity and connection datasets are in 07d_northern_powergrid_open.

# COMMAND ----------
NGED = "https://connecteddata.nationalgrid.co.uk/api/3/action/package_show"


def nged_resources(pkg):
    return get(NGED, params={"id": pkg}).json()["result"]["resources"]


with hc.step(spark, cfg, "nged_ltds_capacity_heatmap"):
    frames = []
    for res in nged_resources("ltds-capacity-heatmap"):
        if res.get("format", "").upper() != "JSON":
            continue
        data = get(res["url"]).json()
        data = data if isinstance(data, list) else data.get("features", data.get("data", [data]))
        part = pd.json_normalize(data)
        part["licence_area"] = os.path.splitext(res["url"].rsplit("/", 1)[-1])[0]
        frames.append(part)
    pdf = pd.concat(frames, ignore_index=True)
    pdf.columns = [c.replace("properties.", "") for c in pdf.columns]
    lat = next((c for c in pdf.columns if c.lower() in ("latitude", "lat")), None)
    lon = next((c for c in pdf.columns if c.lower() in ("longitude", "long", "lon", "lng")), None)
    pdf_to_table(pdf.astype({c: str for c in pdf.columns if pdf[c].map(lambda v: isinstance(v, (list, dict))).any()}),
                 "nged_ltds_capacity_heatmap", lon=lon, lat=lat)

# Further open NGED datasets are in 07b_nged_open.

# COMMAND ----------
# MAGIC %md ## 3. RNLI lifeboat stations (official locations)

# COMMAND ----------
with hc.step(spark, cfg, "rnli_lifeboat_stations"):
    q = ("https://services1.arcgis.com/evM5NkxAYjTi6XPw/arcgis/rest/services/"
         "RNLI_Lifeboat_Station_locations/FeatureServer/0/query")
    feats = get(q, params={"where": "1=1", "outFields": "*", "returnGeometry": "false", "f": "json"}).json()["features"]
    pdf = pd.DataFrame([f["attributes"] for f in feats])
    pdf_to_table(pdf, "rnli_lifeboat_stations", lon="Long", lat="Lat")

# DfT EV charging statistics live in 07c_evci.
