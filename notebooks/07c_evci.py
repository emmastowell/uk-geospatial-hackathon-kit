# Databricks notebook source
# MAGIC %md
# MAGIC # 07c. DfT EV charging infrastructure statistics (area level)
# MAGIC Long format: one row per area, measure and quarter. Charger locations are in `overture_places`.
# MAGIC Tables: `dft_evci_local_authority`, `dft_evci_constituency`.

# COMMAND ----------
# MAGIC %pip install python-calamine
# MAGIC dbutils.library.restartPython()

# COMMAND ----------
import datetime, io, os, re, sys, time

sys.path.insert(0, os.getcwd())
import pandas as pd
import requests
import hackathon_common as hc

cfg = hc.init(spark, dbutils)
HDR = {"User-Agent": "two-postcodes-hackathon/1.0"}


def get(url, retries=4):
    for i in range(retries):
        try:
            r = requests.get(url, headers=HDR, timeout=180)
            r.raise_for_status()
            return r
        except Exception as e:  # noqa: BLE001
            print(f"GET attempt {i + 1}/{retries} failed: {str(e)[:120]}")
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"GET failed: {url}")


def pdf_to_table(pdf, table):
    path = f"{cfg['vol']}/gap/{table}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pdf.to_csv(path, index=False)
    hc.save(hc.snake_columns(spark.read.option("header", True).option("inferSchema", True).csv(path)), cfg, table)


# COMMAND ----------
QMAP = {"january": 1, "april": 4, "july": 7, "october": 10}


def parse_quarter(h):
    m = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", str(h))
    return datetime.date(int(m.group(3)), QMAP.get(m.group(2).lower(), 1), 1).isoformat() if m else None


def evci_long(book, sheet_prefix):
    from python_calamine import CalamineWorkbook
    wb = CalamineWorkbook.from_filelike(io.BytesIO(book))
    out = []
    for sn in wb.sheet_names:
        if not sn.upper().startswith(sheet_prefix.upper()):
            continue
        rows = wb.get_sheet_by_name(sn).to_python()
        hi = next((i for i, r in enumerate(rows) if r and "code" in str(r[0]).lower()), None)
        if hi is None:
            continue  # the closing 'machine-readable format' sheet has no header row; the wide sheets carry the same data
        title = str(rows[0][0]).split(":", 1)[-1].split("[")[0].strip()
        header = rows[hi]
        for r in rows[hi + 1:]:
            if not r or not str(r[0]).strip() or str(r[0]).startswith("["):
                continue
            for j in range(2, len(header)):
                q = parse_quarter(header[j])
                v = r[j]
                if q and isinstance(v, (int, float)):
                    out.append((str(r[0]), str(r[1]), sn, title, q, float(v)))
    return pd.DataFrame(out, columns=["area_code", "area_name", "table_ref", "measure", "quarter_start", "value"])


with hc.step(spark, cfg, "dft_evci"):
    page = get("https://www.gov.uk/government/statistical-data-sets/electric-vehicle-charging-infrastructure-statistics-data-tables-evci").text
    links = {u.rsplit("/", 1)[1]: u for u in set(re.findall(r'https://assets\.publishing\.service\.gov\.uk/[^"\' <\\]+\.ods', page))}
    for prefix, table in (("evci0102", "dft_evci_local_authority"), ("evci0103", "dft_evci_constituency")):
        name = next(n for n in links if n.lower().startswith(prefix))
        print("EVCI file:", name)
        pdf_to_table(evci_long(get(links[name]).content, prefix), table)
