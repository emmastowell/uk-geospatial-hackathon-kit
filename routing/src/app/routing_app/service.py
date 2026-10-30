"""Bring the routing engine up in the background and report how far it has got.

The web server starts at once, so the map and /api/health answer while the extract is
copied. Until the build job publishes a manifest the service polls for one. Valhalla is
imported here, off the request path, so a native import failure shows up in /api/health
instead of crashing the App before it can say why.
"""

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from enum import StrEnum
from pathlib import Path
from typing import Any, Protocol

from databricks.sdk.errors import DatabricksError

from routing_app.settings import Settings
from routing_app.tiles import TileCache, TileManifest, TileSource, tile_source_for

# Failures that leave the engine down: SDK calls, disk and copy errors, a malformed manifest,
# Valhalla refusing the extract, and the native wheel failing to import.
PREPARE_ERRORS = (DatabricksError, OSError, ValueError, KeyError, RuntimeError, ImportError)


class Engine(Protocol):
    limits: dict[str, Any]

    def call(self, action: str, request: str) -> str: ...

    def graph_status(self) -> dict[str, Any]: ...


EngineFactory = Callable[[Path, Path, int], Engine]


def load_valhalla(tile_extract: Path, config_path: Path, pool_size: int) -> Engine:
    """Import pyvalhalla only once the tiles are local, and load the Actor pool."""

    from routing_app.engine import ValhallaEngine

    return ValhallaEngine.load(tile_extract, config_path, pool_size)


class EngineState(StrEnum):
    STARTING = "starting"
    WAITING_FOR_TILES = "waiting_for_tiles"
    DOWNLOADING = "downloading"
    LOADING = "loading"
    READY = "ready"
    FAILED = "failed"


@dataclass
class Progress:
    state: EngineState = EngineState.STARTING
    detail: str = ""
    manifest: TileManifest | None = None
    bytes_copied: int = 0
    graph: dict[str, Any] = field(default_factory=dict)
    limits: dict[str, Any] = field(default_factory=dict)


class RoutingService:
    """Own the engine's lifecycle: wait for tiles, copy them, load and check the Actor pool."""

    def __init__(
        self,
        settings: Settings,
        source: TileSource,
        cache: TileCache,
        engine_factory: EngineFactory = load_valhalla,
    ) -> None:
        self.settings = settings
        self.source = source
        self.cache = cache
        self.engine_factory = engine_factory
        self._progress = Progress()
        self._engine: Engine | None = None
        self._lock = threading.Lock()

    @classmethod
    def from_settings(cls, settings: Settings) -> "RoutingService":
        return cls(settings, tile_source_for(settings.tiles_dir), TileCache(settings.cache_dir))

    @property
    def engine(self) -> Engine | None:
        return self._engine

    def start(self) -> threading.Thread:
        thread = threading.Thread(target=self._prepare, name="valhalla-prepare", daemon=True)
        thread.start()
        return thread

    def _update(self, **changes: Any) -> None:
        with self._lock:
            for name, value in changes.items():
                setattr(self._progress, name, value)

    def _wait_for_manifest(self) -> TileManifest:
        while (manifest := self.source.read_manifest()) is None:
            self._update(
                state=EngineState.WAITING_FOR_TILES,
                detail=f"No manifest in {self.source.location} yet; the build job publishes it",
            )
            time.sleep(self.settings.poll_seconds)
        return manifest

    def _prepare(self) -> None:
        try:
            manifest = self._wait_for_manifest()
            self._update(state=EngineState.DOWNLOADING, manifest=manifest, detail="")
            extract = self.cache.fetch(
                self.source, manifest, lambda copied: self._update(bytes_copied=copied)
            )
            self._update(state=EngineState.LOADING, bytes_copied=manifest.size_bytes)
            config_path = self.settings.cache_dir / "valhalla.json"
            engine = self.engine_factory(extract, config_path, self.settings.actor_pool_size)
            graph = engine.graph_status()
            if not graph.get("has_tiles"):
                raise RuntimeError(f"Valhalla found no routing tiles in {extract}")
            self._engine = engine
            self._update(state=EngineState.READY, graph=graph, limits=engine.limits)
        except PREPARE_ERRORS as error:
            self._update(state=EngineState.FAILED, detail=f"{type(error).__name__}: {error}")

    def health(self) -> dict[str, Any]:
        """Return a JSON-ready snapshot of the engine's state."""

        with self._lock:
            progress = replace(self._progress)
        return {
            "state": progress.state.value,
            "detail": progress.detail,
            "manifest": progress.manifest.to_dict() if progress.manifest else None,
            "bytes_copied": progress.bytes_copied,
            "graph": progress.graph,
            "limits": progress.limits,
            "tiles_dir": self.settings.tiles_dir,
            "cache_dir": str(self.settings.cache_dir),
            "cache_free_bytes": self.cache.free_bytes(),
            "actor_pool_size": self.settings.actor_pool_size,
        }
