"""Regenerate docs/DATA_CATALOGUE.md from notebooks/table_docs.py. Run from the repo root."""
import pathlib
import re
import sys

sys.path.insert(0, "notebooks")
import table_docs as t  # noqa: E402

out = ["# Data catalogue", "",
       "Generated from `notebooks/table_docs.py` (the same text applied as Unity Catalog comments by notebook 06). "
       "Do not edit by hand: change `table_docs.py` and rerun `python3 scripts/build_catalogue.py`.", "",
       f"{len(t.TABLES)} tables, {sum(len(v['columns']) for v in t.TABLES.values())} documented columns.", "",
       "| Table | Columns | Summary |", "|---|---|---|"]
for n, v in sorted(t.TABLES.items()):
    first = re.split(r"(?<=[a-z\)])\. ", v["comment"])[0].rstrip(".")
    out.append(f"| [`{n}`](#{n}) | {len(v['columns'])} | {first.replace('|', '/')} |")
for n, v in sorted(t.TABLES.items()):
    out += ["", f"## {n}", "", v["comment"], "", "| Column | Description |", "|---|---|"]
    out += [f"| `{c}` | {d.replace('|', '/')} |" for c, d in v["columns"].items()]
pathlib.Path("docs/DATA_CATALOGUE.md").write_text("\n".join(out) + "\n")
