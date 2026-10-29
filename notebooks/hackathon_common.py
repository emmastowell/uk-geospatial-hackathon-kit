"""Shared helpers for the "A Tale of Two Postcodes" data loaders.

Imported by every notebook in this folder. Keep it dependency-light: only
requests + pyspark, both present on serverless.
"""
import os
import re
import time
import traceback
from contextlib import contextmanager

import requests

UA = {"User-Agent": "Mozilla/5.0 (two-postcodes-hackathon loader)"}


# ---------------------------------------------------------------- params
def init(spark, dbutils, extra_widgets=None):
    """Create standard widgets, ensure catalog/schema/volume exist, return a config dict."""
    dbutils.widgets.text("catalog", "hackathon")
    dbutils.widgets.text("schema", "two_postcodes")
    dbutils.widgets.text("volume", "raw")
    for name, default in (extra_widgets or {}).items():
        dbutils.widgets.text(name, default)
    cfg = {k: dbutils.widgets.get(k) for k in ("catalog", "schema", "volume")}
    cfg.update({k: dbutils.widgets.get(k) for k in (extra_widgets or {})})
    fq = f"`{cfg['catalog']}`.`{cfg['schema']}`"
    # Lab workspaces often pre-create the catalog and forbid CREATE CATALOG, so try and carry on.
    try:
        spark.sql(f"CREATE CATALOG IF NOT EXISTS `{cfg['catalog']}`")
    except Exception as e:
        print(f"CREATE CATALOG skipped: {str(e)[:120]}")
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {fq}")
    spark.sql(f"CREATE VOLUME IF NOT EXISTS {fq}.`{cfg['volume']}`")
    cfg["fq"] = fq
    cfg["vol"] = f"/Volumes/{cfg['catalog']}/{cfg['schema']}/{cfg['volume']}"
    spark.sql(
        f"CREATE TABLE IF NOT EXISTS {fq}._load_log "
        "(ts TIMESTAMP, step STRING, status STRING, detail STRING)"
    )
    return cfg


def log(spark, cfg, step, status, detail=""):
    detail = str(detail).replace("'", "''")[:2000]
    spark.sql(
        f"INSERT INTO {cfg['fq']}._load_log VALUES (current_timestamp(), '{step}', '{status}', '{detail}')"
    )
    print(f"[{status}] {step} {detail[:200]}")


@contextmanager
def step(spark, cfg, name):
    """One failing dataset must not sink the whole notebook. Log and move on."""
    t0 = time.time()
    try:
        yield
        log(spark, cfg, name, "ok", f"{time.time() - t0:.0f}s")
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        log(spark, cfg, name, "FAILED", f"{type(e).__name__}: {e}")


# ---------------------------------------------------------------- download
def download(url, dest, retries=4, chunk=8 * 1024 * 1024):
    """Stream to a UC volume path. Follows redirects (gov.uk and OS both redirect)."""
    # Subfolders inside a volume must be created explicitly. (Creating the volume root itself is what fails.)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(1, retries + 1):
        try:
            with requests.get(url, headers=UA, stream=True, allow_redirects=True, timeout=120) as r:
                r.raise_for_status()
                with open(dest, "wb") as f:
                    for b in r.iter_content(chunk):
                        f.write(b)
            return dest
        except Exception as e:  # noqa: BLE001
            print(f"download attempt {attempt}/{retries} failed: {e}")
            time.sleep(5 * attempt)
    raise RuntimeError(f"download failed: {url}")


def scrape_links(page_url, pattern):
    """Find current asset links on a landing page. gov.uk asset URLs drift, never hard-code them."""
    html = requests.get(page_url, headers=UA, timeout=60).text
    return sorted(set(re.findall(pattern, html)))


def snake(name):
    """Delta rejects ' ,;{}()\\n\\t=' in column names. Normalise everything."""
    return re.sub(r"[^A-Za-z0-9]+", "_", str(name)).strip("_").lower()


def snake_columns(df):
    seen = {}
    out = df
    for c in df.columns:
        n = snake(c) or "col"
        if n in seen:
            seen[n] += 1
            n = f"{n}_{seen[n]}"
        else:
            seen[n] = 1
        if n != c:
            out = out.withColumnRenamed(c, n)
    return out


# ---------------------------------------------------------------- geometry
def has_native_geometry(spark):
    """True if this workspace supports the native GEOMETRY type and ST_ functions."""
    try:
        spark.sql("SELECT ST_AsText(ST_GeomFromWKT('POINT(0 0)'))").collect()
        return True
    except Exception:  # noqa: BLE001
        return False


def add_geometry(spark, df, wkb_col="geom_wkb", srid=4326, out_col="geom"):
    """WKB -> GEOMETRY in EPSG:4326 (reprojecting from `srid` if needed).

    Falls back to leaving the WKB column alone on runtimes without native spatial SQL.
    """
    if not has_native_geometry(spark):
        return df
    from pyspark.sql import functions as F

    expr = f"ST_GeomFromWKB({wkb_col}, {srid})"
    if srid != 4326:
        expr = f"ST_Transform({expr}, 4326)"
    # Never call df.columns / df.schema after this: the Spark Connect client on some runtimes cannot decode GEOMETRY.
    return df.withColumn(out_col, F.expr(expr)).drop(wkb_col)


def add_h3(df, lon="lon", lat="lat", res=8):
    """H3 cell id (bigint) at the given resolution. Native function, no library."""
    from pyspark.sql import functions as F

    return df.withColumn(f"h3_{res}", F.expr(f"h3_longlatash3({lon}, {lat}, {res})"))


def save(df, cfg, table, mode="overwrite"):
    fq_table = f"{cfg['fq']}.`{table}`"
    (
        df.write.mode(mode)
        .option("overwriteSchema", "true" if mode == "overwrite" else "false")
        .saveAsTable(fq_table)
    )
    n = df.sparkSession.table(fq_table).count()
    print(f"{fq_table}: {n:,} rows")
    return n
