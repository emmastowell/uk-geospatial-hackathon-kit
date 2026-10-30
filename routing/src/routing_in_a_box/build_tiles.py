"""Job entry point: stage the OSM extract, build Valhalla tiles and publish them."""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from routing_in_a_box.osm import GEOFABRIK_GREAT_BRITAIN, OsmDownloader
from routing_in_a_box.valhalla_build import (
    SubprocessRunner,
    ValhallaCommands,
    ValhallaTileBuilder,
    install_valhalla,
)

DEFAULT_SCRATCH_ROOT = Path("/local_disk0/valhalla")
EXTENT_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True)
class BuildArguments:
    """Inputs for one tile build."""

    extent: str
    osm_url: str
    volume_path: Path
    scratch_root: Path
    refresh_osm: bool

    @property
    def pbf_path(self) -> Path:
        return self.volume_path / "osm" / f"{self.extent}.osm.pbf"


def add_option(parser: argparse.ArgumentParser, name: str, **kwargs: Any) -> None:
    """Register ``--name`` and its underscored spelling, which pushed-down job parameters use."""

    flags = [f"--{name}"]
    if "-" in name:
        flags.append(f"--{name.replace('-', '_')}")
    parser.add_argument(*flags, dest=name.replace("-", "_"), **kwargs)


def parse_arguments(argv: list[str] | None = None) -> BuildArguments:
    """Parse and validate the task's named parameters and the job parameters pushed down to it."""

    parser = argparse.ArgumentParser(description="Build and publish Valhalla routing tiles.")
    add_option(parser, "extent", default="great-britain")
    add_option(parser, "osm-url", default=GEOFABRIK_GREAT_BRITAIN)
    add_option(parser, "volume-path", required=True)
    add_option(parser, "scratch-root", default=str(DEFAULT_SCRATCH_ROOT))
    add_option(parser, "refresh-osm", choices=("true", "false"), default="false")
    parsed = parser.parse_args(argv)
    if EXTENT_PATTERN.fullmatch(parsed.extent) is None:
        raise ValueError(f"extent must be a lowercase slug, got {parsed.extent!r}")
    return BuildArguments(
        extent=parsed.extent,
        osm_url=parsed.osm_url,
        volume_path=Path(parsed.volume_path),
        scratch_root=Path(parsed.scratch_root),
        refresh_osm=parsed.refresh_osm == "true",
    )


def main() -> None:
    """Download (or reuse) the PBF in the volume, build the tiles and publish the extract."""

    arguments = parse_arguments()
    extract = OsmDownloader().ensure(arguments.osm_url, arguments.pbf_path, arguments.refresh_osm)
    print(f"OSM {extract.path}: {extract.size_bytes / 1e9:.2f} GB from {extract.last_modified}")
    site_dir = install_valhalla(arguments.scratch_root)
    builder = ValhallaTileBuilder(
        arguments.extent,
        arguments.volume_path,
        arguments.scratch_root,
        commands=ValhallaCommands(),
        runner=SubprocessRunner(site_dir=site_dir),
    )
    manifest = builder.build(extract)
    published = builder.publish_dir / manifest.tile_extract
    print(f"published {published}: {manifest.size_bytes / 1e9:.2f} GB")


if __name__ == "__main__":
    main()
