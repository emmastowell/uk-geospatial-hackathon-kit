import json
from collections.abc import Iterator
from pathlib import Path

import pytest

from routing_in_a_box.osm import OsmDownloader, geocode_bbox, sidecar_path


class FakeResponse:
    def __init__(self, body: bytes, headers: dict[str, str]) -> None:
        self.body = body
        self.headers = headers

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return json.loads(self.body)

    def iter_content(self, chunk_size: int) -> Iterator[bytes]:
        for start in range(0, len(self.body), 3):
            yield self.body[start : start + 3]


class FakeSession:
    def __init__(self, body: bytes, content_length: int | None = None) -> None:
        length = len(body) if content_length is None else content_length
        self.response = FakeResponse(
            body, {"Content-Length": str(length), "Last-Modified": "Tue, 20 Oct 2026 23:32:25 GMT"}
        )
        self.calls = 0

    def get(self, url: str, **_: object) -> FakeResponse:
        self.calls += 1
        return self.response


def test_downloads_into_the_volume_and_records_where_it_came_from(tmp_path: Path) -> None:
    destination = tmp_path / "osm" / "great-britain.osm.pbf"
    extract = OsmDownloader(FakeSession(b"pbf-bytes")).ensure("https://example.org/gb", destination)

    assert destination.read_bytes() == b"pbf-bytes"
    assert extract.size_bytes == 9
    assert extract.last_modified == "Tue, 20 Oct 2026 23:32:25 GMT"
    assert json.loads(sidecar_path(destination).read_text())["url"] == "https://example.org/gb"
    assert not destination.with_name("great-britain.osm.pbf.partial").exists()


def test_reuses_a_complete_download_unless_refreshed(tmp_path: Path) -> None:
    destination = tmp_path / "gb.osm.pbf"
    session = FakeSession(b"first")
    downloader = OsmDownloader(session)
    downloader.ensure("https://example.org/gb", destination)

    downloader.ensure("https://example.org/gb", destination)
    assert session.calls == 1

    downloader.ensure("https://example.org/gb", destination, refresh=True)
    assert session.calls == 2


def test_rejects_a_truncated_download(tmp_path: Path) -> None:
    destination = tmp_path / "gb.osm.pbf"
    with pytest.raises(RuntimeError, match="ended after 5 of 10 bytes"):
        OsmDownloader(FakeSession(b"short", content_length=10)).ensure("https://x", destination)
    assert not destination.exists()
    assert not destination.with_name("gb.osm.pbf.partial").exists()


class GeocodeSession:
    def __init__(self, payload: object) -> None:
        self.payload = payload

    def get(self, url: str, **_: object) -> FakeResponse:
        body = json.dumps(self.payload).encode() if not isinstance(self.payload, Exception) else b""
        if isinstance(self.payload, Exception):
            raise self.payload
        return FakeResponse(body, {})


def test_geocode_bbox_reads_nominatims_south_north_west_east_order() -> None:
    session = GeocodeSession([{"boundingbox": ["50.57", "50.77", "-1.62", "-1.04"]}])

    assert geocode_bbox("isle-of-wight", session) == {
        "west": -1.62,
        "south": 50.57,
        "east": -1.04,
        "north": 50.77,
    }


def test_geocode_bbox_returns_nothing_when_nominatim_is_unreachable() -> None:
    import requests

    assert geocode_bbox("isle-of-wight", GeocodeSession(requests.ConnectionError())) is None
