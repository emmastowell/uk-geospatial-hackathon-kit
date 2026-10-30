import json
import time
from pathlib import Path
from typing import Any

import pytest

from routing_app.service import EngineState, RoutingService
from routing_app.settings import Settings
from routing_app.tiles import (
    MANIFEST_NAME,
    InsufficientDiskError,
    LocalTileSource,
    TileCache,
    TileManifest,
)

REPO = Path(__file__).resolve().parents[2]
ISLE_OF_WIGHT = REPO / ".local" / "volume" / "tiles" / "isle-of-wight"


def publish(directory: Path, payload: bytes) -> TileManifest:
    directory.mkdir(parents=True)
    (directory / "valhalla_tiles.tar").write_bytes(payload)
    manifest = TileManifest(
        extent="test",
        tile_extract="valhalla_tiles.tar",
        size_bytes=len(payload),
        built_at="2026-10-22T12:00:00+00:00",
        pyvalhalla_version="3.9.1",
        osm_url="https://example.org/test.osm.pbf",
        osm_last_modified="Tue, 20 Oct 2026 23:32:25 GMT",
    )
    (directory / MANIFEST_NAME).write_text(json.dumps(manifest.to_dict()))
    return manifest


def test_source_reports_nothing_until_a_manifest_is_published(tmp_path: Path) -> None:
    assert LocalTileSource(tmp_path).read_manifest() is None


def test_cache_copies_the_extract_once_and_reports_progress(tmp_path: Path) -> None:
    source = LocalTileSource(tmp_path / "volume")
    manifest = publish(tmp_path / "volume", b"x" * 1000)
    cache = TileCache(tmp_path / "cache")
    progress: list[int] = []

    first = cache.fetch(source, manifest, progress.append)
    second = cache.fetch(source, manifest, progress.append)

    assert first == second
    assert first.read_bytes() == b"x" * 1000
    assert progress == [1000]


def test_cache_refuses_an_extract_bigger_than_the_free_disk(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = publish(tmp_path / "volume", b"x" * 1000)
    cache = TileCache(tmp_path / "cache")
    monkeypatch.setattr(cache, "free_bytes", lambda: 10)

    with pytest.raises(InsufficientDiskError, match="needs"):
        cache.fetch(LocalTileSource(tmp_path / "volume"), manifest, lambda _: None)


class EmptyGraphEngine:
    def __init__(self) -> None:
        self.limits: dict[str, Any] = {}

    def call(self, action: str, request: str) -> str:
        return "{}"

    def graph_status(self) -> dict[str, Any]:
        return {"has_tiles": False}


def test_service_fails_visibly_when_the_extract_holds_no_tiles(tmp_path: Path) -> None:
    publish(tmp_path / "volume", b"not a tar extract")
    settings = Settings(str(tmp_path / "volume"), tmp_path / "cache", 1, 0.01)
    service = RoutingService(
        settings,
        LocalTileSource(tmp_path / "volume"),
        TileCache(tmp_path / "cache"),
        engine_factory=lambda *_: EmptyGraphEngine(),
    )

    service.start().join(timeout=30)

    health = service.health()
    assert health["state"] == EngineState.FAILED
    assert "found no routing tiles" in health["detail"]
    assert service.engine is None


# Valhalla keeps the first extract a process opens, so this is the only test that loads one.
@pytest.mark.skipif(not ISLE_OF_WIGHT.is_dir(), reason="build .local Isle of Wight tiles first")
def test_service_serves_routes_from_real_tiles(tmp_path: Path) -> None:
    settings = Settings(str(ISLE_OF_WIGHT), tmp_path / "cache", 2, 0.01)
    cache = TileCache(tmp_path / "cache")
    service = RoutingService(settings, LocalTileSource(ISLE_OF_WIGHT), cache)

    service.start().join(timeout=60)
    deadline = time.monotonic() + 5
    while service.engine is None and time.monotonic() < deadline:
        time.sleep(0.1)

    health = service.health()
    assert health["state"] == EngineState.READY
    assert health["graph"]["has_tiles"] is True
    assert health["limits"]["costing"]["auto"]["matrix_km"] == 2000
    request = {
        "locations": [{"lat": 50.7006, "lon": -1.2926}, {"lat": 50.7290, "lon": -1.1610}],
        "costing": "auto",
    }
    trip = json.loads(service.engine.call("route", json.dumps(request)))["trip"]
    assert 5 < trip["summary"]["length"] < 20
