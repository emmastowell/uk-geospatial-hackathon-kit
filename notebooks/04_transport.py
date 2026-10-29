# Databricks notebook source
# MAGIC %md
# MAGIC # 04. Transport: NaPTAN, BODS GTFS, STATS19, DfT traffic counts
# MAGIC Tracks: Access & equity (stops, timetables), Investment (traffic, casualties).
# MAGIC Tables: `naptan_stops`, `gtfs_{stops,routes,trips,stop_times,calendar}`, `stats19_{collision,vehicle,casualty}`,
# MAGIC `dft_aadf`, `dft_major_roads`.

# COMMAND ----------
import glob, os, sys, zipfile

sys.path.insert(0, os.getcwd())
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils, {"stats19_years": "last-5-years"})

# COMMAND ----------
# MAGIC %md ## NaPTAN: every bus stop, rail station, tram and ferry access node in GB

# COMMAND ----------
with hc.step(spark, cfg, "naptan_stops"):
    f = hc.download("https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv", f"{cfg['vol']}/naptan/naptan.csv")
    df = hc.snake_columns(spark.read.option("header", True).option("multiLine", True).option("escape", '"').csv(f))
    df = (df.withColumn("lon", F.col("longitude").cast("double")).withColumn("lat", F.col("latitude").cast("double")))
    hc.save(hc.add_h3(df, "lon", "lat", 8), cfg, "naptan_stops")

# COMMAND ----------
# MAGIC %md ## BODS GTFS (all GB bus timetables, Bus Open Data Service)
# MAGIC `stop_times` is very large (hundreds of millions of rows). Set widget `gtfs_tables` to skip it if you are short of time.

# COMMAND ----------
with hc.step(spark, cfg, "gtfs_bods"):
    z = hc.download("https://data.bus-data.dft.gov.uk/timetable/download/gtfs-file/all/", f"{cfg['vol']}/gtfs/bods_all.zip")
    out = f"{cfg['vol']}/gtfs/extracted"
    with zipfile.ZipFile(z) as zf:
        zf.extractall(out)
    for name in ("stops", "routes", "trips", "calendar", "agency", "stop_times"):
        p = f"{out}/{name}.txt"
        if not os.path.exists(p):
            continue
        df = hc.snake_columns(spark.read.option("header", True).csv(p))
        if name == "stops":
            df = df.withColumn("lon", F.col("stop_lon").cast("double")).withColumn("lat", F.col("stop_lat").cast("double"))
            df = hc.add_h3(df, "lon", "lat", 8)
        hc.save(df, cfg, f"gtfs_{name}")

# COMMAND ----------
# MAGIC %md ## STATS19 road safety data (DfT): collisions with lat/lon, vehicles, casualties

# COMMAND ----------
with hc.step(spark, cfg, "stats19"):
    yrs = cfg["stats19_years"]
    for kind in ("collision", "vehicle", "casualty"):
        url = f"https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-{kind}-{yrs}.csv"
        f = hc.download(url, f"{cfg['vol']}/stats19/{kind}.csv")
        df = hc.snake_columns(spark.read.option("header", True).csv(f))
        if kind == "collision":
            df = (df.withColumn("lon", F.col("longitude").cast("double")).withColumn("lat", F.col("latitude").cast("double")))
            df = hc.add_h3(df.filter("lon IS NOT NULL AND lat IS NOT NULL"), "lon", "lat", 8)
        hc.save(df, cfg, f"stats19_{kind.replace('-', '_')}")

# COMMAND ----------
# MAGIC %md ## DfT traffic counts: AADF by count point, plus the major roads link network

# COMMAND ----------
with hc.step(spark, cfg, "dft_aadf"):
    z = hc.download("https://storage.googleapis.com/dft-statistics/road-traffic/downloads/data-gov-uk/dft_traffic_counts_aadf.zip",
                    f"{cfg['vol']}/dft_traffic/aadf.zip")
    out = f"{cfg['vol']}/dft_traffic/aadf"
    with zipfile.ZipFile(z) as zf:
        zf.extractall(out)
    f = glob.glob(f"{out}/**/*.csv", recursive=True)[0]
    df = hc.snake_columns(spark.read.option("header", True).csv(f))
    df = df.withColumn("lon", F.col("longitude").cast("double")).withColumn("lat", F.col("latitude").cast("double"))
    hc.save(hc.add_h3(df, "lon", "lat", 8), cfg, "dft_aadf")

with hc.step(spark, cfg, "dft_major_roads"):
    z = hc.download("https://storage.googleapis.com/dft-statistics/road-traffic/mrdb-2024.zip",
                    f"{cfg['vol']}/dft_traffic/mrdb.zip")
    out = f"{cfg['vol']}/dft_traffic/mrdb"
    with zipfile.ZipFile(z) as zf:
        zf.extractall(out)
    print("Major roads database extracted to", out, "(shapefile; load with pyogrio as in notebook 02 if needed)")
