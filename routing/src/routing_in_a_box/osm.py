"""Stream a Geofabrik OpenStreetMap extract into a Unity Catalog volume.

The PBF is written straight to the volume path, so the volume is the only copy. A JSON
sidecar records the HTTP metadata, which the tile manifest reports as the data date.
"""

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

import requests

GEOFABRIK_GREAT_BRITAIN = "https://download.geofabrik.de/europe/great-britain-latest.osm.pbf"
CHUNK_BYTES = 8 * 1024 * 1024
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_USER_AGENT = "routing-in-a-box/0.1"


@dataclass(frozen=True)
class OsmExtract:
    """A source PBF in the volume and where it came from."""

    url: str
    path: str
    size_bytes: int
    last_modified: str
    downloaded_at: str


def geocode_bbox(extent: str, session: requests.Session | None = None) -> dict[str, float] | None:
    """Return west/south/east/north for an extent slug, or None if lookup fails."""

    client = session or requests.Session()
    try:
        response = client.get(
            NOMINATIM_URL,
            params={"q": extent.replace("-", " "), "format": "json", "limit": 1},
            headers={"User-Agent": NOMINATIM_USER_AGENT},
            timeout=30,
        )
        response.raise_for_status()
        results = response.json()
        south, north, west, east = (float(value) for value in results[0]["boundingbox"])
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return None
    return {"west": west, "south": south, "east": east, "north": north}


def sidecar_path(pbf: Path) -> Path:
    """Return the metadata file that sits next to a stored PBF."""

    return pbf.with_name(f"{pbf.name}.json")


class OsmDownloader:
    """Download one extract into the volume, reusing a complete earlier download."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()

    def ensure(self, url: str, destination: Path, refresh: bool = False) -> OsmExtract:
        """Return the stored extract, downloading it first if it is missing or `refresh` is set."""

        sidecar = sidecar_path(destination)
        if destination.exists() and sidecar.exists() and not refresh:
            return OsmExtract(**json.loads(sidecar.read_text()))

        destination.parent.mkdir(parents=True, exist_ok=True)
        partial = destination.with_name(f"{destination.name}.partial")
        with self.session.get(url, stream=True, timeout=(30, 1800)) as response:
            response.raise_for_status()
            expected = int(response.headers.get("Content-Length", "0"))
            written = 0
            with partial.open("wb") as output:
                for chunk in response.iter_content(chunk_size=CHUNK_BYTES):
                    output.write(chunk)
                    written += len(chunk)
            last_modified = response.headers.get("Last-Modified", "")
        if expected and written != expected:
            partial.unlink(missing_ok=True)
            raise RuntimeError(f"{url} ended after {written} of {expected} bytes")
        partial.replace(destination)

        extract = OsmExtract(
            url=url,
            path=str(destination),
            size_bytes=written,
            last_modified=last_modified,
            downloaded_at=datetime.now(UTC).isoformat(timespec="seconds"),
        )
        sidecar.write_text(json.dumps(asdict(extract), indent=2))
        return extract
