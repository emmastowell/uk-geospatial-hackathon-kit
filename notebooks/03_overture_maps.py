# Databricks notebook source
# MAGIC %md
# MAGIC # 03. Overture Maps (GeoParquet on public S3, no credentials)
# MAGIC Themes: transportation (segment, connector), places, divisions, buildings (filtered).
# MAGIC Useful extras:
# MAGIC * **bridges / tunnels**: `overture_segments.is_bridge` / `is_tunnel`
# MAGIC * **EV charging points**: `overture_places` with taxonomy category `ev_charging_station`
# MAGIC * **coastguard / lifeboat / port facilities**: `overture_places` maritime categories
# MAGIC
# MAGIC Spark reads the public bucket directly (`s3a://`, anonymous) and filters on the `bbox` columns, which Parquet
# MAGIC statistics turn into file and row-group skipping. No extra libraries, runs on serverless.

# COMMAND ----------
import os, re, sys

sys.path.insert(0, os.getcwd())
import requests
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils, {
    "release": "latest",
    "gb_bbox": "-8.7,49.8,1.9,60.9",            # xmin,ymin,xmax,ymax covering GB + NI
    "buildings_bbox": "-2.75,53.30,-2.00,53.70",  # Greater Manchester. Buildings nationally are ~30M rows; widen if you want.
    "themes": "segment,connector,place,division,building",
})
S3 = "https://overturemaps-us-west-2.s3.amazonaws.com"


def latest_release():
    xml = requests.get(f"{S3}/?list-type=2&prefix=release/&delimiter=/", headers=hc.UA, timeout=60).text
    rels = sorted(re.findall(r"release/([0-9-]+\.[0-9]+)/", xml))
    return rels[-1]


release = latest_release() if cfg["release"] == "latest" else cfg["release"]
print("Overture release:", release)


def bbox_where(bbox):
    x0, y0, x1, y1 = [float(v) for v in bbox.split(",")]
    return f"bbox.xmin BETWEEN {x0} AND {x1} AND bbox.ymin BETWEEN {y0} AND {y1}"


def flag_bridges(df):
    """road_flags is array<struct<values: array<string>, between: array<double>>>."""
    for flag in ("is_bridge", "is_tunnel"):
        df = df.withColumn(flag, F.expr(f"exists(coalesce(road_flags, array()), x -> array_contains(x.values, '{flag}'))"))
    return df


def wkb_expr(path):
    """Overture geometry is WKB in the Parquet file. Some runtimes surface it as GEOMETRY, others as BINARY."""
    probe = spark.read.parquet(path).limit(1)
    for expr in ("geometry", "ST_AsBinary(geometry)"):
        try:
            probe.select(F.expr(expr).alias("g")).collect()
            return expr
        except Exception:  # noqa: BLE001
            continue
    raise RuntimeError("Cannot read the geometry column as WKB")


def export(theme, typ, select, bbox, table, extra_where="1=1", post=None):
    path = f"s3a://overturemaps-us-west-2/release/{release}/theme={theme}/type={typ}/"
    # Write a Parquet slice on the volume first (the same pattern as the other loaders), then load it with Spark.
    dest = f"{cfg['vol']}/overture/{typ}"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    (spark.read.parquet(path).where(f"{bbox_where(bbox)} AND {extra_where}")
          .selectExpr(*[c.strip() for c in re.split(r",\s*(?![^()\[\]]*[)\]])", select) if c.strip() != "geometry"],
                      f"{wkb_expr(path)} AS geom_wkb")
          .write.mode("overwrite").parquet(dest))
    df = spark.read.parquet(dest)
    if post:
        df = post(df)
    df = hc.add_geometry(spark, df, "geom_wkb", 4326)
    hc.save(df, cfg, table)


themes = cfg["themes"].split(",")

# COMMAND ----------
if "segment" in themes:
    with hc.step(spark, cfg, "overture_segments"):
        export("transportation", "segment",
               "id, subtype, class, subclass, names.primary AS name, geometry, "
               "road_surface, speed_limits, road_flags",
               cfg["gb_bbox"], "overture_segments", post=flag_bridges)

if "connector" in themes:
    with hc.step(spark, cfg, "overture_connectors"):
        export("transportation", "connector", "id, geometry", cfg["gb_bbox"], "overture_connectors")

# COMMAND ----------
if "place" in themes:
    with hc.step(spark, cfg, "overture_places"):
        export("places", "place",
               "id, names.primary AS name, taxonomy.primary AS category, basic_category, taxonomy.hierarchy AS category_hierarchy, "
               "confidence, geometry, element_at(addresses, 1).postcode AS postcode, element_at(addresses, 1).locality AS locality",
               cfg["gb_bbox"], "overture_places", "confidence >= 0.5")

if "division" in themes:
    with hc.step(spark, cfg, "overture_divisions"):
        export("divisions", "division_area", "id, subtype, class, names.primary AS name, country, region, geometry",
               cfg["gb_bbox"], "overture_division_areas", "country IN ('GB','IE')")

if "building" in themes:
    with hc.step(spark, cfg, "overture_buildings"):
        export("buildings", "building", "id, subtype, class, height, num_floors, names.primary AS name, geometry",
               cfg["buildings_bbox"], "overture_buildings")

# COMMAND ----------
# MAGIC %md
# MAGIC Add H3 index columns (res 8) for the point/line tables so teams can join on cells immediately:
# MAGIC ```sql
# MAGIC SELECT h3_longlatash3(ST_X(geom), ST_Y(geom), 8) FROM overture_places
# MAGIC ```
