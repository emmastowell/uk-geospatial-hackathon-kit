# Databricks notebook source
# MAGIC %md
# MAGIC # 08. EMODnet marine layers: bathymetry and vessel density
# MAGIC Open European compilations covering UK waters.
# MAGIC
# MAGIC * `emodnet_vessel_density`: AIS-derived vessel traffic density (EMSA), annual averages for 2022 to 2024 (earlier years are listed by the service but not served), all vessel types
# MAGIC   plus a split by type. Gridded (cells about 1.4 to 1.8 km across over UK waters), not per-vessel tracks.
# MAGIC * `emodnet_bathymetry`: EMODnet Digital Terrain Model depth/elevation, block-averaged to about 0.01 degrees (~1 km).
# MAGIC
# MAGIC numpy is pinned to the runtime's version: letting pip upgrade it stops the Spark Connect client importing.
# MAGIC Both come from OGC WCS services as GeoTIFF, are read with rasterio, and loaded through Parquet.

# COMMAND ----------
# MAGIC %pip install "rasterio<1.4" pyproj "numpy==1.23.5"
# MAGIC dbutils.library.restartPython()

# COMMAND ----------
import os, re, sys, time

sys.path.insert(0, os.getcwd())
import numpy as np
import pandas as pd
import requests
from pyproj import Transformer
from rasterio.io import MemoryFile
import hackathon_common as hc
from pyspark.sql import functions as F

cfg = hc.init(spark, dbutils, {"bbox": "-12.0,48.0,4.0,62.0", "bathy_coverage": "emodnet__mean_2022",
                               "years": "2022,2023,2024"})
x0, y0, x1, y1 = [float(v) for v in cfg["bbox"].split(",")]
HDR = {"User-Agent": "two-postcodes-hackathon/1.0"}


def pixel_xy(t, col, row):
    """Affine transform applied by hand: Affine * (array, array) is not supported."""
    return t.a * col + t.b * row + t.c, t.d * col + t.e * row + t.f


def wcs_get(url, params, retries=5):
    for i in range(retries):
        try:
            r = requests.get(url, params=params, headers=HDR, timeout=300)
        except requests.RequestException as ex:  # dropped connections happen on long tile runs
            print(f"WCS attempt {i + 1}/{retries}: {type(ex).__name__}", flush=True)
            time.sleep(10 * (i + 1))
            continue
        if r.ok and r.headers.get("content-type", "").startswith("image"):
            return r.content
        msg = re.findall("ExceptionText>([^<]*)", r.text)[:1]
        print(f"WCS attempt {i + 1}/{retries}: {r.status_code} {msg}", flush=True)
        if msg and "startTime" in msg[0]:
            return None  # that year/time is listed in the capabilities but not served; retrying will not help
        time.sleep(10 * (i + 1))
    return None


def to_parquet_table(pdf, table, parts_name):
    d = f"{cfg['vol']}/gap/{parts_name}"
    os.makedirs(d, exist_ok=True)
    pdf.to_parquet(f"{d}/all.parquet", index=False)
    df = spark.read.parquet(d)
    df = hc.add_h3(df, "lon", "lat", 8)
    if hc.has_native_geometry(spark):
        df = df.withColumn("geom", F.expr("ST_Point(lon, lat, 4326)"))
    hc.save(df, cfg, table)


# COMMAND ----------
# MAGIC %md ## Vessel density (EMSA AIS-derived, via EMODnet Human Activities)
# MAGIC Coverage CRS is EPSG:3857 and has a time axis, so each request needs X/Y in metres plus a time.

# COMMAND ----------
with hc.step(spark, cfg, "emodnet_vessel_density"):
    wcs = "https://ows.emodnet-humanactivities.eu/wcs"
    caps = requests.get(wcs, params={"service": "WCS", "request": "GetCapabilities"}, headers=HDR, timeout=120).text
    ids = sorted(set(re.findall(r"<(?:wcs:)?CoverageId>(emodnet__vesseldensity_\w+avg)</", caps)))
    to_m = Transformer.from_crs(4326, 3857, always_xy=True)
    to_deg = Transformer.from_crs(3857, 4326, always_xy=True)
    mx0, my0 = to_m.transform(x0, y0)
    mx1, my1 = to_m.transform(x1, y1)
    frames = []
    for cid in ids:
        d = requests.get(wcs, params={"service": "WCS", "version": "2.0.1", "request": "DescribeCoverage",
                                      "coverageId": cid}, headers=HDR, timeout=120).text
        title = re.findall(r"<gml:name>([^<]*)", d)[0]
        vtype = title.split(" - ")[-1].strip()
        code = cid.replace("emodnet__vesseldensity_", "").replace("avg", "")
        for yr in [int(v) for v in cfg["years"].split(",")]:
            content = wcs_get(wcs, {"service": "WCS", "version": "2.0.1", "request": "GetCoverage", "coverageId": cid,
                                    "subset": [f"X({mx0:.0f},{mx1:.0f})", f"Y({my0:.0f},{my1:.0f})",
                                               f'time("{yr}-01-01T00:00:00.000Z")'],
                                    "format": "image/tiff"})
            if not content:
                continue
            with MemoryFile(content) as mf, mf.open() as src:
                a = src.read(1).astype("float64")
                nodata = src.nodata
                t = src.transform
                rows, cols = np.nonzero(np.isfinite(a) & (a > 0) & ((a != nodata) if nodata is not None else True))
                if len(rows) == 0:
                    continue
                xs, ys = pixel_xy(t, cols + 0.5, rows + 0.5)
                lon, lat = to_deg.transform(np.asarray(xs), np.asarray(ys))
                frames.append(pd.DataFrame({"year": yr, "vessel_type_code": code, "vessel_type": vtype,
                                            "density": a[rows, cols], "lon": lon, "lat": lat}))
        print(f"{cid}: done, {sum(len(f) for f in frames):,} rows so far", flush=True)
    to_parquet_table(pd.concat(frames, ignore_index=True), "emodnet_vessel_density", "emodnet_vessel_density")

# COMMAND ----------
# MAGIC %md ## Bathymetry (EMODnet Digital Terrain Model)
# MAGIC Pulled in 2 degree tiles and block-averaged 6x6 (about 0.0104 degrees, roughly 1 km). Land is kept
# MAGIC (positive elevation) so coastal analysis has a continuous surface; filter `depth_m < 0` for sea.

# COMMAND ----------
with hc.step(spark, cfg, "emodnet_bathymetry"):
    url = "https://ows.emodnet-bathymetry.eu/wcs"
    cid, B, TILE = cfg["bathy_coverage"], 6, 2.0
    cache = f"{cfg['vol']}/gap/emodnet_bathy_tiles/{cid}"
    os.makedirs(cache, exist_ok=True)
    out, missing = [], []
    for ty in np.arange(y0, y1, TILE):
        for tx in np.arange(x0, x1, TILE):
            tile_path = f"{cache}/lat{ty:.0f}_lon{tx:.0f}.tif"
            if os.path.exists(tile_path):  # resume: a re-run only fetches tiles that failed before
                content = open(tile_path, "rb").read()
            else:
                content = wcs_get(url, {"service": "WCS", "version": "2.0.1", "request": "GetCoverage", "coverageId": cid,
                                        "subset": [f"Lat({ty},{min(ty + TILE, y1)})", f"Long({tx},{min(tx + TILE, x1)})"],
                                        "format": "image/tiff"})
                if content:
                    with open(tile_path, "wb") as fh:
                        fh.write(content)
            if not content:
                missing.append((float(ty), float(tx)))
                continue
            with MemoryFile(content) as mf, mf.open() as src:
                a = src.read(1).astype("float64")
                if src.nodata is not None:
                    a[a == src.nodata] = np.nan
                t = src.transform
            h, w = (a.shape[0] // B) * B, (a.shape[1] // B) * B
            if h == 0 or w == 0:
                continue
            with np.errstate(all="ignore"):
                m = np.nanmean(a[:h, :w].reshape(h // B, B, w // B, B), axis=(1, 3))
            rows, cols = np.nonzero(np.isfinite(m))
            if len(rows) == 0:
                continue
            xs, ys = pixel_xy(t, cols * B + B / 2, rows * B + B / 2)
            out.append(pd.DataFrame({"lon": np.asarray(xs), "lat": np.asarray(ys), "depth_m": m[rows, cols]}))
        print(f"lat {ty}: {sum(len(f) for f in out):,} cells, {len(missing)} tiles missing", flush=True)
    pdf = pd.concat(out, ignore_index=True)
    pdf = pdf[(pdf.depth_m > -400) & (pdf.depth_m < 60)]  # shelf and coast; drop deep Atlantic and high land
    to_parquet_table(pdf.round({"lon": 5, "lat": 5, "depth_m": 1}), "emodnet_bathymetry", "emodnet_bathymetry")
    if missing:
        raise RuntimeError(f"Saved with {len(missing)} tile(s) missing (lat, lon): {missing}. Re-run this notebook: "
                           "completed tiles are cached, so only the missing ones are fetched.")
