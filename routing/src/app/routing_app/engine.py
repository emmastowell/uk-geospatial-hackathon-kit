"""A pool of Valhalla Actors behind one call interface.

pyvalhalla releases the GIL for every action, but one Actor must not serve two requests at
once, so each request leases its own Actor. Actors memory-map the same tar extract, so the
pool shares one copy of the graph in the page cache.
"""

import json
import queue
from collections.abc import Iterator
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any

from valhalla import Actor, ValhallaError, get_config

from routing_app.errors import RoutingError

# Valhalla's HTTP action names mapped to Actor methods; the matrix action is
# sources_to_targets over HTTP.
ACTIONS: dict[str, str] = {
    "route": "route",
    "optimized_route": "optimized_route",
    "sources_to_targets": "matrix",
    "matrix": "matrix",
    "isochrone": "isochrone",
    "locate": "locate",
    "trace_route": "trace_route",
    "trace_attributes": "trace_attributes",
    "expansion": "expansion",
    "centroid": "centroid",
    "status": "status",
}


GRAPH_STATUS_KEYS = ("has_tiles", "has_admins", "tileset_last_modified", "osm_changeset")
# Valhalla rejects car matrices spanning more than 400 km by default, and its matrix search
# stops at a cost derived from this distance: at 1,000 km London to Edinburgh came back
# empty. 2,000 km resolves nearly every pair in Great Britain with no slowdown locally.
AUTO_MAX_MATRIX_METRES = 2_000_000
# The travel modes the guide documents limits for.
LIMIT_COSTINGS = ("auto", "pedestrian", "bicycle", "bus", "truck")


def build_config(tile_extract: Path) -> dict[str, Any]:
    """Return the wheel's default service config, pointed at the local extract.

    get_config() shares nested dicts with the wheel's defaults, so copy before editing.
    Verbose status reports whether the extract holds tiles at all.
    """

    config = deepcopy(get_config(tile_extract=str(tile_extract), tile_dir=""))
    config["service_limits"]["status"]["allow_verbose"] = True
    config["service_limits"]["auto"]["max_matrix_distance"] = AUTO_MAX_MATRIX_METRES
    return config


def summarise_limits(service_limits: dict[str, Any]) -> dict[str, Any]:
    """Return the request limits callers most often hit, in counts, minutes and kilometres."""

    def costing_limits(limits: dict[str, Any]) -> dict[str, float]:
        return {
            "route_locations": limits["max_locations"],
            "route_km": limits["max_distance"] / 1000,
            "matrix_pairs": limits["max_matrix_location_pairs"],
            "matrix_km": limits["max_matrix_distance"] / 1000,
        }

    isochrone, trace = service_limits["isochrone"], service_limits["trace"]
    return {
        "costing": {name: costing_limits(service_limits[name]) for name in LIMIT_COSTINGS},
        "isochrone": {
            "contours": isochrone["max_contours"],
            "minutes": isochrone["max_time_contour"],
            "km": isochrone["max_distance_contour"],
        },
        "trace": {"points": trace["max_shape"], "km": trace["max_distance"] / 1000},
    }


class ValhallaEngine:
    """Serve Valhalla actions from a fixed pool of Actors.

    Valhalla memory-maps the first extract a process opens and reuses it for every later
    Actor, so one process serves one extract.
    """

    def __init__(self, config_path: Path, pool_size: int, limits: dict[str, Any]) -> None:
        self.limits = limits
        self._actors: queue.Queue[Any] = queue.Queue()
        for _ in range(pool_size):
            self._actors.put(Actor(str(config_path)))

    @classmethod
    def load(cls, tile_extract: Path, config_path: Path, pool_size: int) -> "ValhallaEngine":
        config = build_config(tile_extract)
        config_path.write_text(json.dumps(config))
        return cls(config_path, pool_size, summarise_limits(config["service_limits"]))

    def graph_status(self) -> dict[str, Any]:
        """Return what Valhalla reports about the loaded graph, including has_tiles."""

        status = json.loads(self.call("status", '{"verbose":true}'))
        return {key: status.get(key) for key in GRAPH_STATUS_KEYS}

    @contextmanager
    def _lease(self) -> Iterator[Any]:
        actor = self._actors.get()
        try:
            yield actor
        finally:
            self._actors.put(actor)

    def call(self, action: str, request: str) -> str:
        """Run one action on a JSON request string and return Valhalla's JSON response."""

        method = ACTIONS[action]
        with self._lease() as actor:
            try:
                return getattr(actor, method)(request)
            except ValhallaError as error:
                raise RoutingError(
                    error.http_code, error.code, error.message, error.http_message
                ) from error
