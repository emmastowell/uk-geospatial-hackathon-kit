# Databricks notebook source
# MAGIC %md
# MAGIC # Valhalla routing quickstart
# MAGIC
# MAGIC The **valhalla-routing** App runs the [Valhalla](https://valhalla.github.io/valhalla/api/) routing engine over the OpenStreetMap road network built by the `build-valhalla-tiles` job in this bundle. Open the App from **Compute > Apps** to try routes and isochrones on a map.
# MAGIC
# MAGIC The examples join routing results to the hackathon tables (`nspl`, `rnli_lifeboat_stations`, `naptan_stops`, `osm_sar_facilities`) that `notebooks/01` to `07` in this kit load. Set the widgets if your App or tables have other names.
# MAGIC
# MAGIC Every Valhalla action is served at `<app url>/api/<action>` and takes Valhalla's own JSON request, so the [Valhalla API reference](https://valhalla.github.io/valhalla/api/) applies as written.
# MAGIC
# MAGIC | Action | Use it for |
# MAGIC | --- | --- |
# MAGIC | `route` | A turn-by-turn route through two or more points |
# MAGIC | `sources_to_targets` | A travel-time and distance matrix, up to 2,500 pairs per request |
# MAGIC | `isochrone` | The area reachable within up to four travel times (up to 120 minutes) |
# MAGIC | `locate` | Snap points to the nearest roads |
# MAGIC | `trace_route` | Match a GPS trace to roads |
# MAGIC
# MAGIC Travel modes (`costing`) include `auto`, `pedestrian`, `bicycle`, `bus` and `truck`. Car matrices span up to 2,000 km and walking matrices up to 200 km; a pair the matrix cannot resolve comes back with a `null` time, so use `route` for it. The App serves four requests at a time, so send one matrix request for many pairs rather than many single routes.
# MAGIC
# MAGIC Road data © OpenStreetMap contributors, available under the Open Database Licence.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Connect to the App
# MAGIC
# MAGIC Databricks Apps accept only OAuth tokens issued for them, so the client swaps this notebook's token for one. The token lasts about an hour: re-run this cell if calls start failing with 401.

# COMMAND ----------

import requests

dbutils.widgets.text("app_name", "valhalla-routing")  # noqa: F821
dbutils.widgets.text("data_catalog", "hackathon")  # noqa: F821
dbutils.widgets.text("data_schema", "two_postcodes")  # noqa: F821
APP_NAME = dbutils.widgets.get("app_name")  # noqa: F821
DATA = f"{dbutils.widgets.get('data_catalog')}.{dbutils.widgets.get('data_schema')}"  # noqa: F821


class RoutingClient:
    """Call the routing App's Valhalla API from a notebook."""

    def __init__(self, app_name: str = APP_NAME) -> None:
        context = dbutils.notebook.entry_point.getDbutils().notebook().getContext()  # noqa: F821
        host = context.apiUrl().get()
        notebook_token = context.apiToken().get()
        app = requests.get(
            f"{host}/api/2.0/apps/{app_name}",
            headers={"Authorization": f"Bearer {notebook_token}"},
            timeout=30,
        )
        app.raise_for_status()
        details = app.json()
        exchange = requests.post(
            f"{host}/oidc/v1/token",
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                "subject_token": notebook_token,
                "subject_token_type": "urn:databricks:params:oauth:token-type:personal-access-token",
                "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "scope": "all-apis",
                "audience": details["oauth2_app_client_id"],
            },
            timeout=30,
        )
        exchange.raise_for_status()
        self.base_url = f"{details['url']}/api"
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {exchange.json()['access_token']}"

    def health(self) -> dict:
        """Report whether the engine has loaded its tiles, and which OpenStreetMap data it uses."""

        return self.session.get(f"{self.base_url}/health", timeout=30).json()

    def call(self, action: str, request: dict) -> dict:
        """Send one Valhalla request and return its JSON response."""

        response = self.session.post(f"{self.base_url}/{action}", json=request, timeout=120)
        if response.status_code >= 400:
            raise ValueError(f"{action} failed ({response.status_code}): {response.text[:500]}")
        return response.json()


routing = RoutingClient()
routing.health()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Route from a postcode to its nearest lifeboat station
# MAGIC
# MAGIC Look the postcode up in the NSPL, pick the closest RNLI station as the crow flies, then ask Valhalla for the drive.

# COMMAND ----------

POSTCODE = "TR18 4AA"  # Penzance

origin = spark.sql(  # noqa: F821
    f"SELECT lat, long AS lon FROM {DATA}.nspl WHERE pcds = :postcode",
    args={"postcode": POSTCODE},
).first()

station = spark.sql(  # noqa: F821
    f"""
    SELECT station, lat, lon
    FROM {DATA}.rnli_lifeboat_stations
    ORDER BY pow(lat - :lat, 2) + pow((lon - :lon) * cos(radians(:lat)), 2)
    LIMIT 1
    """,
    args={"lat": origin.lat, "lon": origin.lon},
).first()

trip = routing.call(
    "route",
    {
        "locations": [
            {"lat": origin.lat, "lon": origin.lon},
            {"lat": station.lat, "lon": station.lon},
        ],
        "costing": "auto",
        "directions_options": {"units": "kilometers", "language": "en-GB"},
    },
)["trip"]

summary = trip["summary"]
print(f"{POSTCODE} to {station.station} lifeboat station: {summary['length']:.1f} km, {summary['time'] / 60:.0f} min by car")
for maneuver in trip["legs"][0]["maneuvers"]:
    print(f"  {maneuver['instruction']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## What lies within a 10-minute walk
# MAGIC
# MAGIC Isochrones come back as GeoJSON polygons. `h3_coverash3` lists the H3 resolution 8 cells (the hackathon's join key) that the polygon touches, which narrows the search, and `st_contains` keeps only what is inside the polygon: here, NaPTAN bus stops. The `st_` functions need serverless compute, as do the GEOMETRY columns in the hackathon tables.

# COMMAND ----------

import json

isochrone = routing.call(
    "isochrone",
    {
        "locations": [{"lat": origin.lat, "lon": origin.lon}],
        "costing": "pedestrian",
        "contours": [{"time": 10}],
        "polygons": True,
    },
)
walk_area = json.dumps(isochrone["features"][0]["geometry"])

display(  # noqa: F821
    spark.sql(  # noqa: F821
        f"""
        SELECT count(*) AS bus_stops_within_10_min_walk
        FROM {DATA}.naptan_stops
        WHERE stoptype = 'BCT'
          AND h3_8 IN (SELECT explode(h3_coverash3(:area, 8)))
          AND st_contains(st_geomfromgeojson(:area), st_point(lon, lat, 4326))
        """,
        args={"area": walk_area},
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Travel-time matrix: postcodes to search and rescue facilities
# MAGIC
# MAGIC One `sources_to_targets` request returns the drive time from every source to every target. Keep sources × targets at 2,500 or fewer per request and split bigger jobs into batches.

# COMMAND ----------

import pandas as pd

postcodes = spark.sql(  # noqa: F821
    f"""
    SELECT pcds, lat, long AS lon
    FROM {DATA}.nspl
    WHERE pcds LIKE 'TR18 %' AND doterm IS NULL
    LIMIT 20
    """
).toPandas()

facilities = spark.sql(  # noqa: F821
    f"""
    SELECT coalesce(name, facility_type) AS facility, lat, lon
    FROM {DATA}.osm_sar_facilities
    WHERE lat BETWEEN :lat - 0.5 AND :lat + 0.5 AND lon BETWEEN :lon - 0.8 AND :lon + 0.8
    """,
    args={"lat": origin.lat, "lon": origin.lon},
).toPandas()

matrix = routing.call(
    "sources_to_targets",
    {
        "sources": postcodes[["lat", "lon"]].to_dict("records"),
        "targets": facilities[["lat", "lon"]].to_dict("records"),
        "costing": "auto",
    },
)

rows = []
for postcode, row in zip(postcodes.pcds, matrix["sources_to_targets"]):
    reachable = [cell for cell in row if cell["time"] is not None]
    best = min(reachable, key=lambda cell: cell["time"]) if reachable else None
    rows.append(
        {
            "postcode": postcode,
            "nearest_facility": facilities.facility[best["to_index"]] if best else None,
            "drive_minutes": round(best["time"] / 60, 1) if best else None,
            "drive_km": best["distance"] if best else None,
        }
    )
display(pd.DataFrame(rows).sort_values("drive_minutes"))  # noqa: F821
