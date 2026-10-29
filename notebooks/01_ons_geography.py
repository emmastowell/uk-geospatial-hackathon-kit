# Databricks notebook source
# MAGIC %md
# MAGIC # 01. ONS geography: NSPL postcodes + LSOA boundaries
# MAGIC Tracks: Access & equity (postcode scoring), Resilience (demographics).
# MAGIC Tables: `nspl`, `lsoa_2021_boundaries`.

# COMMAND ----------
import json, os, sys, zipfile

sys.path.insert(0, os.getcwd())
import requests
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils)

# COMMAND ----------
# MAGIC %md ## NSPL (National Statistics Postcode Lookup)
# MAGIC Latest release discovered from the ONS Open Geography portal (item search), so it does not rot.

# COMMAND ----------
with hc.step(spark, cfg, "nspl"):
    hits = requests.get(
        "https://www.arcgis.com/sharing/rest/search",
        params={"q": 'title:"National Statistics Postcode Lookup" owner:ONSGeography_data type:"CSV Collection"',
                "sortField": "modified", "sortOrder": "desc", "num": 5, "f": "json"},
        headers=hc.UA, timeout=60).json()["results"]
    hits = [h for h in hits if "User Guide" not in h["title"] and h["name"].lower().endswith(".zip")]
    item = hits[0]
    print("NSPL item:", item["title"], item["id"])

    zpath = hc.download(f"https://www.arcgis.com/sharing/rest/content/items/{item['id']}/data",
                        f"{cfg['vol']}/nspl/nspl.zip")
    out = f"{cfg['vol']}/nspl/extracted"
    with zipfile.ZipFile(zpath) as z:
        # The Data/ folder holds the national file plus one per postcode area; take the national one.
        names = [n for n in z.namelist() if n.lower().endswith(".csv") and n.lower().startswith("data/")
                 and "multi_csv" not in n.lower()]
        print(names[:5])
        z.extractall(out, members=names)
    national = [n for n in names if os.path.basename(n).upper().startswith("NSPL_")][0]
    df = hc.snake_columns(spark.read.option("header", True).csv(f"{out}/{national}"))
    df = (df.withColumn("lat", F.col("lat").cast("double")).withColumn("long", F.col("long").cast("double"))
            .filter("lat < 99"))  # NSPL uses 99.999999 for postcodes without a grid reference
    df = df.withColumn("lon", F.col("long"))
    df = hc.add_h3(df, "lon", "lat", 8)
    hc.save(df, cfg, "nspl")

# COMMAND ----------
# MAGIC %md ## LSOA 2021 boundaries (England & Wales, generalised clipped)
# MAGIC Paged out of the ONS ArcGIS FeatureServer as GeoJSON (2000 per page, ~35k polygons).

# COMMAND ----------
with hc.step(spark, cfg, "lsoa_2021_boundaries"):
    base = ("https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
            "Lower_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V5/FeatureServer/0")
    total = requests.get(f"{base}/query", params={"where": "1=1", "returnCountOnly": "true", "f": "json"},
                         headers=hc.UA, timeout=60).json()["count"]
    rows, offset = [], 0
    while offset < total:
        r = requests.get(f"{base}/query", params={
            "where": "1=1", "outFields": "LSOA21CD,LSOA21NM", "outSR": 4326, "f": "geojson",
            "resultOffset": offset, "resultRecordCount": 1000, "orderByFields": "LSOA21CD"},
            headers=hc.UA, timeout=180).json()
        feats = r["features"]
        if not feats:
            break
        rows += [(f["properties"]["LSOA21CD"], f["properties"]["LSOA21NM"], json.dumps(f["geometry"])) for f in feats]
        offset += len(feats)
        print(f"{offset}/{total}", end="\r")
    sdf = spark.createDataFrame(rows, "lsoa21cd string, lsoa21nm string, geojson string")
    if hc.has_native_geometry(spark):
        sdf = sdf.withColumn("geom", F.expr("ST_GeomFromGeoJSON(geojson)")).drop("geojson")
    hc.save(sdf, cfg, "lsoa_2021_boundaries")
