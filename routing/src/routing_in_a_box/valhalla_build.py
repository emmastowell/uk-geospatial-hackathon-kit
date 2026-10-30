"""Build a Valhalla tile extract with the pyvalhalla wheel and publish it to a volume.

The task process never imports ``valhalla``. On Databricks the kernel's protobuf runtime and
the exported OpenSSL/FIPS settings break the wheel's bundled natives, so every step runs in
a fresh subprocess with a minimal environment. Valhalla writes tiles with random access, so
it builds on the node's local NVMe disk; the volume receives only the finished tar extract
and its manifest, and the scratch directory is removed afterwards.
"""

import json
import os
import shutil
import subprocess
import sys
from collections import deque
from collections.abc import Sequence
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from routing_in_a_box.osm import OsmExtract

TILE_EXTRACT_NAME = "valhalla_tiles.tar"
MANIFEST_NAME = "manifest.json"
ERROR_TAIL_LINES = 80


@dataclass(frozen=True)
class TileManifest:
    """What the App reads to find, size and describe the published extract."""

    extent: str
    tile_extract: str
    size_bytes: int
    built_at: str
    pyvalhalla_version: str
    osm_url: str
    osm_last_modified: str


def routing_env(python_executable: str) -> dict[str, str]:
    """Return a minimal environment for Valhalla subprocesses.

    Starting from an allowlist keeps Databricks' OpenSSL/FIPS variables away from the
    wheel's bundled OpenSSL. The interpreter's bin directory goes first on PATH because
    ``python -m valhalla`` looks its executables up there.
    """

    path = os.pathsep.join(
        part for part in (str(Path(python_executable).parent), os.environ.get("PATH")) if part
    )
    environment = {"PATH": path}
    if "PYTHONPATH" in os.environ:
        environment["PYTHONPATH"] = os.environ["PYTHONPATH"]
    return environment


class ValhallaCommands:
    """Build pyvalhalla subprocess invocations for one Python interpreter."""

    def __init__(self, python_executable: str = sys.executable) -> None:
        self.python = python_executable

    def config(self, tile_dir: Path) -> list[str]:
        """Print the wheel's default config as JSON; an empty extract skips its existence check."""

        script = (
            "import json,sys,valhalla;"
            "print(json.dumps(valhalla.get_config("
            "tile_dir=sys.argv[1], tile_extract='', verbose=True)))"
        )
        return [self.python, "-c", script, str(tile_dir)]

    def version(self) -> list[str]:
        return [self.python, "-c", "import valhalla; print(valhalla.__version__)"]

    def build_admins(self, config: Path, pbf: Path) -> list[str]:
        return [self.python, "-m", "valhalla", "valhalla_build_admins", "-c", str(config), str(pbf)]

    def build_tiles(self, config: Path, pbf: Path) -> list[str]:
        return [self.python, "-m", "valhalla", "valhalla_build_tiles", "-c", str(config), str(pbf)]

    def build_extract(self, config: Path) -> list[str]:
        """Pack mjolnir.tile_dir into the indexed tar at mjolnir.tile_extract."""

        script = "import sys; from valhalla.valhalla_build_extract import main; sys.exit(main())"
        return [self.python, "-c", script, "-c", str(config), "-v", "--overwrite"]


class SubprocessRunner:
    """Run Valhalla subprocesses in the minimal environment."""

    def __init__(self, python_executable: str = sys.executable) -> None:
        self.environment = routing_env(python_executable)

    def capture(self, command: Sequence[str]) -> str:
        """Run a short command and return its stdout."""

        result = subprocess.run(  # noqa: S603
            list(command), capture_output=True, text=True, env=self.environment
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[-4000:]
            raise RuntimeError(f"{command[0]} {command[1]} exited {result.returncode}: {detail}")
        return result.stdout

    def stream(self, command: Sequence[str]) -> None:
        """Run a long command, echoing its log live and raising with the tail on failure."""

        tail: deque[str] = deque(maxlen=ERROR_TAIL_LINES)
        with subprocess.Popen(  # noqa: S603
            list(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=self.environment,
        ) as process:
            for line in process.stdout or ():
                print(line, end="", flush=True)
                tail.append(line)
        if process.returncode != 0:
            step = next((part for part in command if part.startswith("valhalla_")), command[0])
            raise RuntimeError(f"{step} exited {process.returncode}:\n{''.join(tail)}")


def build_config(
    defaults: dict[str, Any], tile_dir: Path, tile_extract: Path, admin_db: Path
) -> dict[str, Any]:
    """Point the wheel's default config at this build's scratch paths."""

    config = deepcopy(defaults)
    mjolnir = config["mjolnir"]
    mjolnir["tile_dir"] = str(tile_dir)
    mjolnir["tile_extract"] = str(tile_extract)
    mjolnir["admin"] = str(admin_db)
    return config


class ValhallaTileBuilder:
    """Build tiles for one extent on local disk and publish the tar extract to the volume."""

    def __init__(
        self,
        extent: str,
        volume_path: Path,
        scratch_root: Path,
        commands: ValhallaCommands | None = None,
        runner: SubprocessRunner | None = None,
    ) -> None:
        self.extent = extent
        self.volume_path = volume_path
        self.scratch_root = scratch_root
        self.commands = commands or ValhallaCommands()
        self.runner = runner or SubprocessRunner(self.commands.python)

    @property
    def scratch_dir(self) -> Path:
        return self.scratch_root / self.extent

    @property
    def publish_dir(self) -> Path:
        """Return the volume directory the App reads: tiles/<extent>/."""

        return self.volume_path / "tiles" / self.extent

    def build(self, extract: OsmExtract) -> TileManifest:
        """Build admins, tiles and the tar extract from `extract`, then publish them."""

        scratch = self.scratch_dir
        shutil.rmtree(scratch, ignore_errors=True)
        tile_dir = scratch / "tiles"
        tile_dir.mkdir(parents=True)
        local_extract = scratch / TILE_EXTRACT_NAME
        config_path = scratch / "valhalla.json"

        defaults = json.loads(self.runner.capture(self.commands.config(tile_dir)))
        config = build_config(defaults, tile_dir, local_extract, scratch / "admins.sqlite")
        config_path.write_text(json.dumps(config, indent=2))

        pbf = Path(extract.path)
        self.runner.stream(self.commands.build_admins(config_path, pbf))
        self.runner.stream(self.commands.build_tiles(config_path, pbf))
        self.runner.stream(self.commands.build_extract(config_path))
        if not local_extract.is_file():
            raise RuntimeError(f"valhalla_build_extract did not write {local_extract}")

        manifest = TileManifest(
            extent=self.extent,
            tile_extract=TILE_EXTRACT_NAME,
            size_bytes=local_extract.stat().st_size,
            built_at=datetime.now(UTC).isoformat(timespec="seconds"),
            pyvalhalla_version=self.runner.capture(self.commands.version()).strip(),
            osm_url=extract.url,
            osm_last_modified=extract.last_modified,
        )
        self.publish(local_extract, manifest)
        shutil.rmtree(scratch, ignore_errors=True)
        return manifest

    def publish(self, local_extract: Path, manifest: TileManifest) -> None:
        """Copy the extract into the volume, then write the manifest that points at it."""

        self.publish_dir.mkdir(parents=True, exist_ok=True)
        target = self.publish_dir / manifest.tile_extract
        partial = target.with_name(f"{target.name}.partial")
        shutil.copyfile(local_extract, partial)
        partial.replace(target)
        (self.publish_dir / MANIFEST_NAME).write_text(json.dumps(asdict(manifest), indent=2))
