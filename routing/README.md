# Routing in a box

A self-contained [Valhalla](https://valhalla.github.io/valhalla/) routing engine for Databricks, deployed with one
Declarative Automation Bundle. It turns an OpenStreetMap extract into a routing graph and serves routes, isochrones,
travel-time matrices and map matching from a Databricks App, with a map for people and a Valhalla-compatible HTTP API
for notebooks and services.

This is the routing App demonstrated at the "A Tale of Two Postcodes" hackathon, packaged so that anyone can deploy it
to their own workspace and run it end to end.

## What gets deployed

| Resource | Name | Purpose |
|---|---|---|
| Schema | `<catalog>.routing` | Holds the volume |
| Volume | `<catalog>.routing.valhalla` | The OpenStreetMap extract (`osm/`) and the published tiles (`tiles/<extent>/`) |
| Job | `build-valhalla-tiles` | Downloads the extract, builds Valhalla tiles on one classic node and publishes them to the volume |
| App | `valhalla-routing` | FastAPI and Valhalla: the map at `/`, the API at `/api/<action>`, a guide at `/#guide` |
| Notebook | `notebooks/valhalla_quickstart.py` | Calls the App from a notebook and joins the results to the hackathon tables |

```
OpenStreetMap extract ──► build-valhalla-tiles job ──► UC volume ──► valhalla-routing App ──► browser, notebook, service
   (Geofabrik)             (classic single node)       tiles + manifest   (copies tiles at start-up)
```

The volume sits between the job and the App, so tiles can be rebuilt without redeploying the App. The App starts at
once, polls the volume until a manifest appears, copies the tiles to local disk (Valhalla memory-maps a local file) and
reports progress at `/api/health`. The App's service principal has `READ VOLUME` on the volume and nothing else.

## Before you start

* A recent Databricks CLI (built with v1.21) with a profile for the workspace, and [uv](https://docs.astral.sh/uv/).
* An existing catalog where you can create a schema. The default is `playground`, which
  [`scripts/setup_workspace.sql`](../scripts/setup_workspace.sql) creates; pass `--var catalog=<name>` to use another.
* Permission to run classic compute. The tile build needs one node with plenty of memory and a local NVMe disk, so it
  cannot run on serverless compute or Databricks Free Edition.
* Outbound internet access from the build cluster (to download the extract and the `pyvalhalla` wheel) and from the
  App (it installs its dependencies from public PyPI).

## Deploy and run end to end

Run these from this `routing/` directory. Pick the target for your cloud: `aws` (the default, `i3.4xlarge`) or
`azure` (`Standard_L16s_v3`). The Azure target has not been tested end to end yet.

```bash
# 1. Deploy the schema, volume, job and App
databricks bundle deploy -t aws -p <profile>

# 2. Build the Great Britain tiles (about 20 minutes, including cluster start-up)
databricks bundle run build_valhalla_tiles -t aws -p <profile>

# 3. Start the App and deploy its code
databricks bundle run valhalla_routing -t aws -p <profile>
```

Open the App from **Compute > Apps**. The status at the top of the page moves from "Copying tiles" to "Ready" in about
a minute. Steps 2 and 3 can run in either order: an App started before the build waits for the tiles.

For a quick trial, build a small area instead. The extent is a slug used in volume paths and shown in the App:

```bash
databricks bundle deploy -t aws -p <profile> \
  --var extent=isle-of-wight \
  --var osm_url=https://download.geofabrik.de/europe/united-kingdom/england/isle-of-wight-latest.osm.pbf
```

Then run steps 2 and 3 with the same `--var` values. Any [Geofabrik](https://download.geofabrik.de/) extract works,
as does any other OpenStreetMap PBF URL.

### Bundle variables

| Variable | Default | Notes |
|---|---|---|
| `catalog` | `playground` | Must exist already |
| `schema` | `routing` | Created by the bundle |
| `extent` | `great-britain` | Lowercase slug |
| `osm_url` | Geofabrik Great Britain | About 2.2 GB |
| `build_node_type_id` | `i3.4xlarge` (`Standard_L16s_v3` on Azure) | 16 cores and NVMe; smaller nodes suit smaller extents |
| `app_name` | `valhalla-routing` | 26 characters at most |

## Use it

* **Map.** Click to plan car, walking and cycling routes and isochrones. The **API** tab shows the request behind
  each result.
* **Guide.** `/#guide` explains the architecture, Valhalla's concepts, every API action, the limits and errors, and
  has a console for trying requests.
* **API.** Every Valhalla action keeps its name and JSON body at `<app url>/api/<action>`: `route`,
  `optimized_route`, `sources_to_targets`, `isochrone`, `locate`, `trace_route`, `trace_attributes`, `expansion`,
  `centroid` and `status`. The [Valhalla API reference](https://valhalla.github.io/valhalla/api/) applies as written.
* **Notebooks.** Databricks Apps accept only OAuth tokens issued for the App. `notebooks/valhalla_quickstart.py`
  swaps the notebook's token for one and shows a route, an isochrone joined to bus stops with `h3_coverash3` and
  `st_contains`, and a travel-time matrix. It reads the hackathon tables; set the `data_catalog` and `data_schema`
  widgets if yours live elsewhere.
* **Laptop or service.** Get a token with `databricks auth token -p <profile>` and send it as a bearer token.

Give other users `CAN_USE` on the App to share it. The bundle already grants this to the `users` group, along with
`CAN_VIEW` on the job.

## Refresh the data

Run the job with `refresh_osm=true` to download a fresh extract, then restart the App:

```bash
databricks bundle run build_valhalla_tiles -t aws -p <profile> --params refresh_osm=true
databricks apps stop valhalla-routing -p <profile> && databricks apps start valhalla-routing -p <profile>
```

## Cost and sizing

* The build runs on demand only; there is no schedule. A Great Britain build takes about 20 minutes on one
  `i3.4xlarge`, on demand rather than spot because losing the only node loses the run.
* The App uses `LARGE` compute with four Valhalla workers, which keeps the 2.7 GB Great Britain graph in memory and
  serves four requests at a time. Stop the App when you are not using it. For a small extent, set `compute_size` to
  `MEDIUM` and `VALHALLA_ACTOR_POOL_SIZE` to `2` in `resources/valhalla_routing.app.yml`.

## Limits

* Times assume free-flowing traffic. There is no live or historical traffic and no public transport timetable data.
* The Databricks Apps proxy ends a request after 120 seconds, so split very large matrices into batches.
* One App process serves one extent. Deploy the bundle again with another `app_name` and `extent` for a second area.

## Develop

```bash
uv run pytest                                                                  # job package
uv run --project src/app --frozen --with pytest --with httpx pytest tests/app  # App
uv run ruff check . && uv run ruff format --check .
```

To run the App locally, point it at a directory that holds a `manifest.json` and tile extract:

```bash
cd src/app
VALHALLA_TILES_DIR=/path/to/tiles/isle-of-wight VALHALLA_ACTOR_POOL_SIZE=2 \
  uv run --frozen uvicorn --factory routing_app.main:build_app --port 8000
```

The test that loads real tiles looks for them in `.local/volume/tiles/isle-of-wight/` and is skipped otherwise. If
you can reach PyPI only through a mirror, refresh both lock files with `scripts/lock_app.py`.

## Layout

```
databricks.yml               Bundle, variables and per-cloud targets
resources/                   Schema, volume, build job and App
src/routing_in_a_box/        Job wheel: download the extract, build and publish tiles
src/app/                     The App: FastAPI service (routing_app/) and the map and guide (routing_app/static/)
notebooks/                   Quickstart notebook
tests/job, tests/app         Tests for the job package and the App
scripts/lock_app.py          Lock both projects through a PyPI mirror
```

## Licences

The code is under the repository's [MIT licence](../LICENSE). Valhalla is MIT-licensed. Road data is
© OpenStreetMap contributors under the [Open Database Licence](https://www.openstreetmap.org/copyright): credit
OpenStreetMap when you publish maps or results built on it. The basemap is [OpenFreeMap](https://openfreemap.org/).
