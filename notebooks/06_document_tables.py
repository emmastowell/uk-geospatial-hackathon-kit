# Databricks notebook source
# MAGIC %md
# MAGIC # 06. Document tables in Unity Catalog and grant access
# MAGIC Applies table and column comments from `table_docs.py` and makes the schema readable by everyone.
# MAGIC Run last, and re-run after any loader change. Idempotent.
# MAGIC
# MAGIC * Table and column comments come only from the curated dictionary. Nothing is auto-generated.
# MAGIC * Any table or column with no description is listed, and the notebook fails if `strict` is `true`.
# MAGIC * Grants are at schema level, so tables created later are covered automatically.

# COMMAND ----------
import os, sys

sys.path.insert(0, os.getcwd())
import hackathon_common as hc
import table_docs as td

cfg = hc.init(spark, dbutils, {"grantee": "account users", "strict": "true"})
fq, catalog, schema = cfg["fq"], cfg["catalog"], cfg["schema"]
grantee = f"`{cfg['grantee']}`"


def q(text):
    return "'" + str(text).replace("\\", "\\\\").replace("'", "\\'") + "'"


# COMMAND ----------
# MAGIC %md ## Access: all users can query (not write)

# COMMAND ----------
with hc.step(spark, cfg, "grants"):
    spark.sql(f"GRANT USE CATALOG ON CATALOG `{catalog}` TO {grantee}")
    spark.sql(f"GRANT USE SCHEMA, SELECT, READ VOLUME ON SCHEMA {fq} TO {grantee}")
    display(spark.sql(f"SHOW GRANTS ON SCHEMA {fq}"))

# COMMAND ----------
# MAGIC %md ## Comments

# COMMAND ----------
tables = [r.tableName for r in spark.sql(f"SHOW TABLES IN {fq}").collect() if not r.tableName.startswith("_")]
missing_tables, missing_cols, stale = [], {}, {}

for t in sorted(tables):
    doc = td.TABLES.get(t)
    if not doc:
        missing_tables.append(t)
        continue
    spark.sql(f"COMMENT ON TABLE {fq}.`{t}` IS {q(doc['comment'])}")
    cols = [r.col_name for r in spark.sql(f"DESCRIBE TABLE {fq}.`{t}`").collect()
            if r.col_name and not r.col_name.startswith("#")]
    known = {**td.COMMON, **doc["columns"]}
    gaps = [c for c in cols if c not in known]
    if gaps:
        missing_cols[t] = gaps
    unused = [c for c in doc["columns"] if c not in cols]
    if unused:
        stale[t] = unused
    for c in cols:
        if c in known:
            spark.sql(f"ALTER TABLE {fq}.`{t}` ALTER COLUMN `{c}` COMMENT {q(known[c])}")
    print(f"documented {t}: {len(cols) - len(gaps)}/{len(cols)} columns")

# COMMAND ----------
# MAGIC %md ## Coverage report

# COMMAND ----------
print("Tables with no entry in table_docs.TABLES:", missing_tables or "none")
print("Columns with no description:", missing_cols or "none")
print("Described columns that no longer exist (stale):", stale or "none")
hc.log(spark, cfg, "document_tables", "ok" if not (missing_tables or missing_cols) else "INCOMPLETE",
       f"missing_tables={missing_tables} missing_cols={missing_cols}")
if cfg["strict"].lower() == "true" and (missing_tables or missing_cols):
    raise RuntimeError("Undocumented tables or columns remain; see report above.")
