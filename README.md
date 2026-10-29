# UK geospatial hackathon kit

Everything needed to stand up a UK geospatial event on Databricks: open-data loaders, documented Unity Catalog
tables, a challenge guide, a teaching app and workspace setup. It was built for "A Tale of Two Postcodes" (transport,
energy and coastal infrastructure) and works for any event that needs UK open geospatial data in a lakehouse.

| Part | Where | What it gives you |
|---|---|---|
| Data loaders | `notebooks/` | Databricks notebooks that load about 57 open datasets into `hackathon.two_postcodes` |
| Data documentation | `notebooks/table_docs.py`, `docs/DATA_CATALOGUE.md` | Table and column descriptions, applied as Unity Catalog comments |
| Challenge guide | `notebooks/00_challenge_guide.py` | Three challenge briefs with starter SQL, spatial techniques and stretch goals |
| Teaching app | `app/` | "Databricks Geospatial Guide": a static AppKit app that teaches H3 and native spatial SQL with worked examples |
| Workspace setup | `scripts/setup_workspace.sql` | Read-only data grants plus a shared writable `playground` catalog |
| Tooling | `scripts/` | Source reachability check, SQL runner, catalogue generator |

**No data is in this repo.** Loaders download from the original publishers at run time. Check each source's licence
before redistributing anything (see "Before you reuse this").

## Quick start: load the data
1. Import `notebooks/` into a workspace (for example `/Workspace/Shared/two_postcodes/`).
2. Optional: `uv run --with requests python -I scripts/check_sources.py` from a laptop to confirm sources are reachable.
3. Run the notebooks in order on **serverless** compute. Every notebook has `catalog`, `schema` and `volume` widgets
   (defaults `hackathon`, `two_postcodes`, `raw`). `CREATE CATALOG` failures are tolerated if the catalog exists.
4. Notebook 02 installs `pyogrio` with `%pip` (plus `python-calamine` in 07 and 07c, and `rasterio` in 08). If your
   proxy blocks PyPI, vendor the wheels first. Notebook 03 (Overture) needs no installs: Spark reads the public S3
   bucket directly.
5. Run `06_document_tables` last. It writes table and column comments and the read grants, and with `strict=true` it
   fails if any column is undescribed.

Every step logs to `_load_log` and fails soft, so one bad source does not stop the rest:
`SELECT * FROM hackathon.two_postcodes._load_log ORDER BY ts`.

Point tables carry `h3_8` (H3 resolution 8) so teams can join on cells straight away, and a native `GEOMETRY` column
`geom` when the runtime supports it (otherwise a `geom_wkb` BINARY column).

## Notebooks
| Notebook | Tables |
|---|---|
| `00_challenge_guide` | Participant guide; reads the tables loaded by 01 to 08 |
| `01_ons_geography` | `nspl` (2.7M postcodes), `lsoa_2021_boundaries` |
| `02_os_open_data` | OS Open Roads, Open Rivers, Open UPRN, Code-Point Open, Boundary-Line; BGS GeoCoast |
| `03_overture_maps` | Overture segments, connectors, places, division areas, buildings |
| `04_transport` | NaPTAN stops, BODS GTFS, STATS19 collisions, DfT traffic counts (AADF) |
| `05_hazard_energy_marine` | EA flood areas, warnings, stations, RoFRS postcodes; DESNZ REPD; OSM search and rescue |
| `06_document_tables` | Table and column comments, grants |
| `07_assets_energy_rescue` | EA flood defences (with condition), RNLI stations, NGED capacity heatmap |
| `07b_nged_open` | NGED embedded capacity register, connection queue |
| `07c_evci` | DfT EV charging infrastructure statistics (local authority, constituency) |
| `07d_northern_powergrid_open` | Northern Powergrid capacity heatmap, connection queue, GSP info, peak demand, LCT by postal district |
| `08_emodnet_marine` | EMODnet vessel density (2022 to 2024) and bathymetry |

The full table and column reference is in [`docs/DATA_CATALOGUE.md`](docs/DATA_CATALOGUE.md).

## Example challenges
| Challenge area | Core tables |
|---|---|
| Resilience and risk | OS roads and rivers, BGS GeoCoast, EA flood data, DESNZ REPD, EMODnet bathymetry, ONS demographics |
| Access and equity | NaPTAN and GTFS, NSPL and LSOA, DfT EV statistics, RNLI stations, OS Open UPRN |
| Investment and prioritisation | EA flood defences, Northern Powergrid and NGED capacity, vessel density, Overture buildings and segments |

## Shared sandbox and compute
`scripts/setup_workspace.sql` creates `playground.shared` where every workspace user can create tables, and grants
read access to the loaded data. Run it as an admin. For compute, give the `users` group `CAN_USE` on a SQL warehouse
and on the Shared Compute cluster policy, or create a shared cluster with `CAN_ATTACH_TO` for `users`. Serverless
notebooks and jobs need no setup. Anyone with write access to `playground` can modify others' tables, which suits a
hackathon but not production.

## The app: Databricks Geospatial Guide (`app/`)
An AppKit (Node, React, TypeScript) learning guide for H3 and native spatial SQL. It is a static app: it needs no SQL
warehouse, no tables and no data. Each lesson has worked examples with copy-ready SQL, the table shape the query
expects, and the values to change. Paste them into a notebook or the SQL editor and point them at your own tables.

Run locally (AppKit needs Databricks credentials even for a static app; a CLI profile is enough):
```bash
cd app
npm install
npm run build
DATABRICKS_CONFIG_PROFILE=<profile> DATABRICKS_APP_PORT=8000 npm start   # then open http://localhost:8000
```

Deploy:
```bash
databricks apps create geospatial-guide -p <profile>
databricks workspace import-dir app /Workspace/Shared/apps/geospatial-guide -p <profile>
databricks apps deploy geospatial-guide --source-code-path /Workspace/Shared/apps/geospatial-guide -p <profile>
```
Then give the `users` group `CAN_USE` on the app (app permissions API or the Apps UI) so everyone can open it. The app
needs its compute to be `ACTIVE` before the first deploy.

The examples use placeholder tables `your_catalog.your_schema.vessel_positions` and `vessel_current_locations`. To
practise on the loaded data instead, swap in point tables such as `naptan_stops` (use `lon`, `lat` and `h3_8`).

## Coverage and limits
* **Assets:** there is no open national bridge inventory. `overture_segments.is_bridge/is_tunnel` and
  `os_open_roads_links.road_structure` flag structures; `ea_flood_defences` has condition grades for flood and coastal
  assets only (about a quarter have a grade).
* **Vessels:** `emodnet_vessel_density` is a gridded density for 2022 to 2024, not individual vessel tracks.
* **Grid capacity:** NGED (Midlands, South West, Wales) and Northern Powergrid (North East, Yorkshire) only.
* **Search and rescue:** RNLI stations are official; the OpenStreetMap layer is volunteer-mapped.
* **EV charging:** DfT counts are by area. Charger locations come from Overture places and are approximate.
* **Bathymetry:** `emodnet_bathymetry` is a European compilation for regional analysis, not navigation.
* **Floods:** `ea_rofrs_postcodes` gives postcodes at risk, not flood extent polygons.

## Lessons learned
* Create volume **subfolders** with `os.makedirs`; only the volume root cannot be created that way.
* Do not call `df.columns` or `df.schema` on a frame with a `GEOMETRY` column: some Spark Connect clients cannot decode it.
* `spark.createDataFrame(pandas_df_with_binary_geometry)` runs at about 20 rows/s on serverless. Write Parquet with pyarrow
  and let Spark read it (Open Roads went from an estimated 80 hours to about 2 minutes).
* Copy GeoPackages to `/local_disk0` before reading; SQLite over the Volumes mount is very slow.
* Overture is readable straight from `s3a://overturemaps-us-west-2/release/<release>/...` with Spark on serverless, no
  credentials or libraries; filter on the `bbox` columns. Counts change a lot between releases (GB places with confidence
  >= 0.5: 2.93M in 2026-09-23.0, 4.10M in 2026-10-21.0), so pin `release` for repeatable loads.
  Overture places use `taxonomy` and `basic_category`.
* BGS GeoCoast is shapefile only and has Z values: use `force_2d=True`.
* A catalogue listing a dataset does not make it open: some portals return empty exports or file URLs that read
  "redacted" without an account. Always check row counts after loading.
* Do not `%pip install` anything that upgrades `numpy`: the Spark Connect client then fails to import after restart.
* Cache long remote downloads (EMODnet tiles) on the volume so a dropped connection costs one tile, not the run.

## Before you reuse this
* **Personal data.** `nged_embedded_capacity_register` contains customer names, addresses and meter point identifiers.
  It is described as such in Unity Catalog. Mask those columns before sharing with participants.
* **Licences.** Most sources are Open Government Licence v3.0 (ONS, OS Open Data, Environment Agency, DfT, DESNZ, NGED,
  Northern Powergrid). Confirm Overture Maps (mixed per theme), OpenStreetMap (ODbL), BGS, EMODnet and RNLI terms before
  redistributing derived data. Each table's licence is stated in its Unity Catalog comment.
* **Column descriptions.** Some (GeoCoast and Northern Powergrid fields, STATS19 code values) were written from
  documentation recall. Have a domain expert spot-check them.
* **Access testing.** Grants were verified as an admin, not from a non-admin participant account.

## Licence
The code, notebooks, app and documentation in this repo are released under the [MIT licence](LICENSE). The MIT
licence does not cover the datasets: each source keeps its own licence, stated in the table descriptions and in
`docs/DATA_CATALOGUE.md`.

## Repo layout
```
notebooks/   Databricks source-format notebooks, shared helpers (hackathon_common.py), table_docs.py
app/         Databricks Geospatial Guide (AppKit, static)
docs/        DATA_CATALOGUE.md (generated by scripts/build_catalogue.py)
scripts/     check_sources.py, run_sql.py, build_catalogue.py, setup_workspace.sql
```

Credentials: use Databricks CLI profiles. Never put tokens in code, notebooks or this repo.
