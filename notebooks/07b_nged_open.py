# Databricks notebook source
# MAGIC %md
# MAGIC # 07b. NGED open data: embedded capacity register and connection queue
# MAGIC National Grid Electricity Distribution (Midlands, South West and Wales). Only datasets that can be downloaded
# MAGIC without a portal login are loaded.
# MAGIC * `nged_embedded_capacity_register`: generators and storage connected to the distribution network
# MAGIC * `nged_connection_queue`: pending connection requests by supply point (45 area files combined)

# COMMAND ----------
import io, os, sys

sys.path.insert(0, os.getcwd())
import pandas as pd
import requests
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils)
HDR = {"User-Agent": "two-postcodes-hackathon/1.0"}
NGED = "https://connecteddata.nationalgrid.co.uk/api/3/action/package_show"


def resources(pkg):
    return [r for r in requests.get(NGED, params={"id": pkg}, headers=HDR, timeout=60).json()["result"]["resources"]
            if str(r["url"]).startswith("http") and r.get("format", "").upper() == "CSV"]


def csv_get(url):
    r = requests.get(url, headers=HDR, timeout=180)
    r.raise_for_status()
    return pd.read_csv(io.BytesIO(r.content), encoding="utf-8-sig", low_memory=False)


def write(pdf, table):
    path = f"{cfg['vol']}/gap/{table}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pdf.to_csv(path, index=False)
    df = hc.snake_columns(spark.read.option("header", True).option("multiLine", True).option("escape", '"')
                          .option("inferSchema", True).csv(path))
    return df


# COMMAND ----------
with hc.step(spark, cfg, "nged_embedded_capacity_register"):
    pdf = csv_get(resources("embedded-capacity-register")[0]["url"])
    df = write(pdf, "nged_embedded_capacity_register")
    e = next((c for c in df.columns if "easting" in c), None)
    n = next((c for c in df.columns if "northing" in c), None)
    if e and n and hc.has_native_geometry(spark):
        df = df.withColumn("geom", F.expr(f"ST_Transform(ST_Point(try_cast(`{e}` AS DOUBLE), try_cast(`{n}` AS DOUBLE), 27700), 4326)"))
        # NGED masks some coordinates with the text "--REDACTED--"; try_cast turns those into NULL geometries.
        df = hc.add_h3(df.withColumn("lon", F.expr("ST_X(geom)")).withColumn("lat", F.expr("ST_Y(geom)")), "lon", "lat", 8)
    hc.save(df, cfg, "nged_embedded_capacity_register")

with hc.step(spark, cfg, "nged_connection_queue"):
    frames = []
    for r in resources("connection-queue"):
        part = csv_get(r["url"])
        part["source_file"] = r["url"].rsplit("/", 1)[-1]
        frames.append(part)
    pdf = pd.concat(frames, ignore_index=True)
    hc.save(write(pdf.astype(str).replace("nan", None), "nged_connection_queue"), cfg, "nged_connection_queue")
