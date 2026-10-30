"""Find the published Valhalla extract and copy it to local disk for memory-mapping.

The build job publishes ``manifest.json`` and the tar extract to
``/Volumes/<catalog>/<schema>/valhalla/tiles/<extent>/``. Valhalla can only memory-map a
local file, so the App copies the extract once per container start. The volume stays the
source of truth and the copy disappears with the container.
"""

import json
import shutil
from collections.abc import Callable
from contextlib import closing
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import BinaryIO, Protocol

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

MANIFEST_NAME = "manifest.json"
CHUNK_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class TileManifest:
    """The build job's description of a published extract."""

    extent: str
    tile_extract: str
    size_bytes: int
    built_at: str
    pyvalhalla_version: str
    osm_url: str
    osm_last_modified: str

    @classmethod
    def from_json(cls, text: str) -> "TileManifest":
        data = json.loads(text)
        return cls(**{field.name: data[field.name] for field in fields(cls)})

    def to_dict(self) -> dict[str, str | int]:
        return asdict(self)


class InsufficientDiskError(OSError):
    """The cache directory cannot hold the extract."""


class TileSource(Protocol):
    """Somewhere a published extract can be read from."""

    location: str

    def read_manifest(self) -> TileManifest | None:
        """Return the manifest, or None while nothing is published yet."""

    def open_extract(self, manifest: TileManifest) -> BinaryIO:
        """Open the extract the manifest names for streaming."""


class VolumeTileSource:
    """Read a published extract from a Unity Catalog volume through the Files API."""

    def __init__(self, directory: str, client: WorkspaceClient | None = None) -> None:
        self.location = directory
        self.client = client or WorkspaceClient()

    def read_manifest(self) -> TileManifest | None:
        try:
            response = self.client.files.download(f"{self.location}/{MANIFEST_NAME}")
        except NotFound:
            return None
        with closing(response.contents) as stream:
            return TileManifest.from_json(stream.read().decode())

    def open_extract(self, manifest: TileManifest) -> BinaryIO:
        return self.client.files.download(f"{self.location}/{manifest.tile_extract}").contents


class LocalTileSource:
    """Read a published extract from a local or FUSE-mounted directory."""

    def __init__(self, directory: Path) -> None:
        self.location = str(directory)
        self.directory = directory

    def read_manifest(self) -> TileManifest | None:
        path = self.directory / MANIFEST_NAME
        return TileManifest.from_json(path.read_text()) if path.is_file() else None

    def open_extract(self, manifest: TileManifest) -> BinaryIO:
        return (self.directory / manifest.tile_extract).open("rb")


def tile_source_for(directory: str) -> TileSource:
    """Read the directory directly when this machine can see it, else through the Files API."""

    local = Path(directory)
    return LocalTileSource(local) if local.is_dir() else VolumeTileSource(directory)


class TileCache:
    """Copy the extract a manifest names onto local disk."""

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir

    def free_bytes(self) -> int:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        return shutil.disk_usage(self.cache_dir).free

    def fetch(
        self, source: TileSource, manifest: TileManifest, on_progress: Callable[[int], None]
    ) -> Path:
        """Return the local extract, streaming it from `source` unless an exact copy exists."""

        target = self.cache_dir / manifest.tile_extract
        if target.is_file() and target.stat().st_size == manifest.size_bytes:
            return target
        free = self.free_bytes()
        if free < manifest.size_bytes:
            raise InsufficientDiskError(
                f"{self.cache_dir} has {free / 1e9:.1f} GB free; "
                f"the extract needs {manifest.size_bytes / 1e9:.1f} GB"
            )
        partial = target.with_name(f"{target.name}.partial")
        copied = 0
        with closing(source.open_extract(manifest)) as stream, partial.open("wb") as output:
            while chunk := stream.read(CHUNK_BYTES):
                output.write(chunk)
                copied += len(chunk)
                on_progress(copied)
        if copied != manifest.size_bytes:
            raise OSError(f"copied {copied} of {manifest.size_bytes} bytes from {source.location}")
        partial.replace(target)
        return target
