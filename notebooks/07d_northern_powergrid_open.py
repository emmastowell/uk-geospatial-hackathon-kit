# Databricks notebook source
# MAGIC %md
# MAGIC # 07d. Northern Powergrid open data (North East, Yorkshire and northern Lincolnshire)
# MAGIC Grid capacity, connection queue and low-carbon technology counts.
# MAGIC NGED, for the Midlands, South West and Wales, is in 07 and 07b.
# MAGIC Tables: `northern_powergrid_capacity_heatmap`, `northern_powergrid_connection_queue`, `northern_powergrid_gsp_connection_info`, `northern_powergrid_lct_postal_districts`,
# MAGIC `northern_powergrid_historical_peak_demand`.

# COMMAND ----------
import io, os, sys, time

sys.path.insert(0, os.getcwd())
import pandas as pd
import requests
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils)
HDR = {"User-Agent": "two-postcodes-hackathon/1.0"}
BASE = "https://northernpowergrid.opendatasoft.com/api/explore/v2.1/catalog/datasets"


def export(ds, retries=4):
    for i in range(retries):
        try:
            r = requests.get(f"{BASE}/{ds}/exports/csv", params={"delimiter": ",", "list_separator": ";"},
                             headers=HDR, timeout=180)
            r.raise_for_status()
            pdf = pd.read_csv(io.BytesIO(r.content), encoding="utf-8-sig", low_memory=False)
            if len(pdf) == 0:
                raise RuntimeError(f"{ds}: export returned 0 rows (access restricted?)")
            return pdf
        except Exception as e:  # noqa: BLE001
            print(f"export attempt {i + 1}/{retries} failed: {str(e)[:120]}")
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"export failed: {ds}")


def load(pdf, table):
    path = f"{cfg['vol']}/gap/{table}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pdf.to_csv(path, index=False)
    return hc.snake_columns(spark.read.option("header", True).option("multiLine", True).option("escape", '"')
                            .option("inferSchema", True).csv(path))


# COMMAND ----------
with hc.step(spark, cfg, "northern_powergrid_capacity_heatmap"):
    df = load(export("heatmapdatatable"), "northern_powergrid_capacity_heatmap")
    if hc.has_native_geometry(spark):
        df = df.withColumn("geom", F.expr("ST_Transform(ST_Point(CAST(grid_easting AS DOUBLE), CAST(grid_northing AS DOUBLE), 27700), 4326)"))
        df = hc.add_h3(df.withColumn("lon", F.expr("ST_X(geom)")).withColumn("lat", F.expr("ST_Y(geom)")), "lon", "lat", 8)
    hc.save(df, cfg, "northern_powergrid_capacity_heatmap")

for ds, table in (("connection-queue-information", "northern_powergrid_connection_queue"),
                  ("grid-supply-point-connection-information", "northern_powergrid_gsp_connection_info"),
                  ("historical-peak-demand", "northern_powergrid_historical_peak_demand")):
    with hc.step(spark, cfg, table):
        hc.save(load(export(ds), table), cfg, table)

with hc.step(spark, cfg, "northern_powergrid_lct_postal_districts"):
    pdf = export("lct-datasets")
    df = load(pdf, "northern_powergrid_lct_postal_districts")
    ll = F.split(F.col("geo_point_2d"), r"[;,]\s*")
    df = df.withColumn("lat", ll.getItem(0).cast("double")).withColumn("lon", ll.getItem(1).cast("double"))
    df = hc.add_h3(df, "lon", "lat", 8)
    if hc.has_native_geometry(spark):
        df = df.withColumn("geom", F.expr("ST_GeomFromGeoJSON(geo_shape)")).drop("geo_shape")
    hc.save(df, cfg, "northern_powergrid_lct_postal_districts")
