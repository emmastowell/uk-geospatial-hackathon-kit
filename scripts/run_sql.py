"""Run one SQL statement on a SQL warehouse through the Statement Execution API.

Usage: python scripts/run_sql.py "<statement>"
Config: DATABRICKS_PROFILE (CLI profile name) and DATABRICKS_WAREHOUSE_ID environment variables.
Auth comes from the Databricks CLI profile. Never put a token in this file.
"""
import json
import os
import subprocess
import sys
import tempfile

profile = os.environ["DATABRICKS_PROFILE"]
warehouse = os.environ["DATABRICKS_WAREHOUSE_ID"]
body = {"warehouse_id": warehouse, "wait_timeout": "30s", "statement": sys.argv[1]}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
    json.dump(body, fh)
out = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "-p", profile, "--json", f"@{fh.name}"],
                     capture_output=True, text=True).stdout
os.unlink(fh.name)
d = json.loads(out[out.index("{"):])
print(d["status"]["state"], d["status"].get("error", {}).get("message", "")[:300])
for row in d.get("result", {}).get("data_array", []):
    print(row)
