# Databricks notebook source
# MAGIC %md
# MAGIC # 02. Ordnance Survey open data (OS Data Hub Downloads API, no key needed)
# MAGIC Tables: `os_open_roads_links`, `os_open_roads_nodes`, `os_open_rivers`, `os_open_uprn`,
# MAGIC `os_code_point_open`, `os_boundary_line_*`, `bgs_geocoast`.
# MAGIC
# MAGIC Vector files are GeoPackage (EPSG:27700). We read them in slices with `pyogrio` (raw WKB, no shapely)
# MAGIC and reproject to 4326 in Spark with `ST_Transform`.

# COMMAND ----------
# MAGIC %pip install pyogrio
# MAGIC dbutils.library.restartPython()

# COMMAND ----------
import os, sys, zipfile, glob

sys.path.insert(0, os.getcwd())
import requests
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils, {"products": "OpenRoads,OpenRivers,OpenUPRN,CodePointOpen,BoundaryLine,GeoCoast_Open",
                               "slice_rows": "500000"})
SLICE = int(cfg["slice_rows"])
API = "https://api.os.uk/downloads/v1/products"


def fetch(product, fmt_contains, area="GB"):
    """Download the product zip for the first format whose name contains fmt_contains."""
    opts = requests.get(f"{API}/{product}/downloads", headers=hc.UA, timeout=60).json()
    pick = next(o for o in opts if fmt_contains.lower() in o["format"].lower() and o["area"] == area)
    dest = f"{cfg['vol']}/os/{product}/{product}.zip"
    print(f"{product}: {pick['format']} {pick['size'] / 1e6:.0f} MB")
    # Reuse a complete earlier download (big files are slow and the loader is re-run while debugging).
    if not (os.path.exists(dest) and os.path.getsize(dest) == pick["size"]):
        hc.download(pick["url"], dest)
    out = f"{cfg['vol']}/os/{product}/extracted"
    if not glob.glob(f"{out}/**/*.*", recursive=True):
        with zipfile.ZipFile(dest) as z:
            z.extractall(out)
    return out


def gpkg_to_table(gpkg, layer, table, srid=27700):
    """Vector file -> Delta. pyogrio reads slices to local Arrow, writes Parquet parts to the volume,
    then Spark loads all parts in one pass. (Passing pandas frames of binary geometry through
    spark.createDataFrame ran at ~20 rows/s on serverless, so do not do that.)
    """
    import shutil, time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from pyogrio import read_info
    from pyogrio.raw import read

    # SQLite GeoPackages read through the Volumes FUSE mount are extremely slow for sliced reads. Copy local first.
    if gpkg.startswith("/Volumes"):
        local = f"/local_disk0/tmp/{os.path.basename(gpkg)}"
        if not os.path.exists(local) or os.path.getsize(local) != os.path.getsize(gpkg):
            os.makedirs("/local_disk0/tmp", exist_ok=True)
            print(f"copying {gpkg} to local disk ...", flush=True)
            shutil.copy(gpkg, local)
        gpkg = local

    info = read_info(gpkg, layer=layer)
    total, meta_cols = info["features"], list(info["fields"])
    crs = str(info.get("crs") or "")
    if crs.upper().startswith("EPSG:"):
        srid = int(crs.split(":")[1])  # trust the file over the default (BGS and OS files differ)

    parts = f"{cfg['vol']}/parts/{table}"
    shutil.rmtree(parts, ignore_errors=True)
    os.makedirs(parts, exist_ok=True)
    names = [hc.snake(c) or "col" for c in meta_cols]
    t0 = time.time()
    for n, skip in enumerate(range(0, total, SLICE)):
        t1 = time.time()
        # force_2d: some layers (BGS) carry Z values, which ST_GeomFromWKB rejects.
        _, _, geoms, fields = read(gpkg, layer=layer, skip_features=skip, max_features=SLICE, force_2d=True)
        t2 = time.time()
        cols = {nm: pa.array(fields[i]) for i, nm in enumerate(names)}
        cols["geom_wkb"] = pa.array(list(geoms), type=pa.binary())
        local_part = f"/local_disk0/tmp/{table}_{n:04d}.parquet"
        pq.write_table(pa.table(cols), local_part, compression="zstd")
        shutil.move(local_part, f"{parts}/part-{n:04d}.parquet")
        print(f"{table}: slice {n} {min(skip + SLICE, total):,}/{total:,}  read {t2 - t1:.0f}s  "
              f"write {time.time() - t2:.0f}s  elapsed {time.time() - t0:.0f}s", flush=True)

    t3 = time.time()
    sdf = hc.snake_columns(spark.read.parquet(parts))
    sdf = hc.add_geometry(spark, sdf, "geom_wkb", srid=srid)
    hc.save(sdf, cfg, table)
    print(f"{table}: loaded to Delta in {time.time() - t3:.0f}s", flush=True)


products = [p.strip() for p in cfg["products"].split(",")]

# COMMAND ----------
# MAGIC %md ## OS Open Roads (road links + nodes, with functional class / form of way)
# MAGIC Core network for all three tracks. ~3.6M links nationally.

# COMMAND ----------
if "OpenRoads" in products:
    with hc.step(spark, cfg, "os_open_roads"):
        d = fetch("OpenRoads", "GeoPackage")
        gpkg = glob.glob(f"{d}/**/*.gpkg", recursive=True)[0]
        gpkg_to_table(gpkg, "road_link", "os_open_roads_links")
        gpkg_to_table(gpkg, "road_node", "os_open_roads_nodes")

# COMMAND ----------
if "OpenRivers" in products:
    with hc.step(spark, cfg, "os_open_rivers"):
        d = fetch("OpenRivers", "GeoPackage")
        gpkg = glob.glob(f"{d}/**/*.gpkg", recursive=True)[0]
        gpkg_to_table(gpkg, "watercourse_link", "os_open_rivers")

# COMMAND ----------
# MAGIC %md ## OS Open UPRN (~41M addresses as points) and Code-Point Open (postcode centroids)
# MAGIC CSV products. Spark reads straight from the volume (never pandas, see data-loading gotchas).

# COMMAND ----------
if "OpenUPRN" in products:
    with hc.step(spark, cfg, "os_open_uprn"):
        d = fetch("OpenUPRN", "CSV")
        f = glob.glob(f"{d}/**/*.csv", recursive=True)[0]
        df = hc.snake_columns(spark.read.option("header", True).csv(f))
        df = (df.withColumn("uprn", F.col("uprn").cast("long"))
                .withColumn("lon", F.col("longitude").cast("double"))
                .withColumn("lat", F.col("latitude").cast("double")))
        hc.save(hc.add_h3(df, "lon", "lat", 8), cfg, "os_open_uprn")

if "CodePointOpen" in products:
    with hc.step(spark, cfg, "os_code_point_open"):
        d = fetch("CodePointOpen", "CSV")
        files = glob.glob(f"{d}/**/Data/CSV/*.csv", recursive=True)
        cols = ["postcode", "positional_quality_indicator", "eastings", "northings", "country_code",
                "nhs_regional_ha_code", "nhs_ha_code", "admin_county_code", "admin_district_code", "admin_ward_code"]
        df = spark.read.csv(files).toDF(*cols)
        df = (df.withColumn("eastings", F.col("eastings").cast("double"))
                .withColumn("northings", F.col("northings").cast("double")))
        if hc.has_native_geometry(spark):
            df = df.withColumn("geom", F.expr("ST_Transform(ST_Point(eastings, northings, 27700), 4326)"))
            df = (df.withColumn("lon", F.expr("ST_X(geom)")).withColumn("lat", F.expr("ST_Y(geom)")))
            df = hc.add_h3(df, "lon", "lat", 8)
        hc.save(df, cfg, "os_code_point_open")

# COMMAND ----------
# MAGIC %md ## Boundary-Line and BGS GeoCoast (coastal hazard)

# COMMAND ----------
if "BoundaryLine" in products:
    with hc.step(spark, cfg, "os_boundary_line"):
        d = fetch("BoundaryLine", "GeoPackage")
        gpkg = glob.glob(f"{d}/**/*.gpkg", recursive=True)[0]
        from pyogrio import list_layers
        for name, _ in list_layers(gpkg):
            if name in ("district_borough_unitary", "county_region", "westminster_const", "english_region"):
                gpkg_to_table(gpkg, name, f"os_boundary_line_{name}")

if "GeoCoast_Open" in products:
    with hc.step(spark, cfg, "bgs_geocoast"):
        d = fetch("GeoCoast_Open", "Shapefile")  # GeoCoast is only published as shapefiles
        for shp in glob.glob(f"{d}/**/*.shp", recursive=True):
            gpkg_to_table(shp, None, f"bgs_geocoast_{hc.snake(os.path.splitext(os.path.basename(shp))[0])}")
