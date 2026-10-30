import json
from pathlib import Path

import pytest

from routing_in_a_box.valhalla_build import (
    MANIFEST_NAME,
    TileManifest,
    ValhallaCommands,
    ValhallaTileBuilder,
    build_config,
    routing_env,
)


def test_routing_env_keeps_only_path_and_pythonpath(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PATH", "/usr/bin")
    monkeypatch.setenv("PYTHONPATH", "/opt/lib")
    monkeypatch.setenv("OPENSSL_CONF", "/etc/fips.cnf")
    monkeypatch.setenv("OPENSSL_FORCE_FIPS_MODE", "1")

    environment = routing_env("/env/bin/python")

    assert environment == {"PATH": "/env/bin:/usr/bin", "PYTHONPATH": "/opt/lib"}


def test_build_config_points_at_scratch_without_changing_the_defaults() -> None:
    defaults = {"mjolnir": {"tile_dir": "", "tile_extract": "", "admin": "/data/admin.sqlite"}}

    scratch = Path("/s")
    config = build_config(
        defaults, scratch / "tiles", scratch / "tiles.tar", scratch / "admins.sqlite"
    )

    assert config["mjolnir"] == {
        "tile_dir": "/s/tiles",
        "tile_extract": "/s/tiles.tar",
        "admin": "/s/admins.sqlite",
    }
    assert defaults["mjolnir"]["admin"] == "/data/admin.sqlite"


def test_commands_run_the_bundled_executables_through_one_interpreter() -> None:
    commands = ValhallaCommands("/env/bin/python")
    config, pbf = Path("/s/valhalla.json"), Path("/v/osm/gb.osm.pbf")

    assert commands.build_admins(config, pbf) == [
        "/env/bin/python",
        "-m",
        "valhalla",
        "valhalla_build_admins",
        "-c",
        str(config),
        str(pbf),
    ]
    assert commands.build_tiles(config, pbf)[3] == "valhalla_build_tiles"
    assert commands.build_extract(config)[-4:] == ["-c", str(config), "-v", "--overwrite"]


def test_publish_writes_the_extract_before_the_manifest_that_names_it(tmp_path: Path) -> None:
    local_extract = tmp_path / "scratch" / "valhalla_tiles.tar"
    local_extract.parent.mkdir()
    local_extract.write_bytes(b"tiles")
    builder = ValhallaTileBuilder("great-britain", tmp_path / "volume", tmp_path / "scratch")
    manifest = TileManifest(
        extent="great-britain",
        tile_extract="valhalla_tiles.tar",
        size_bytes=5,
        built_at="2026-10-22T12:00:00+00:00",
        pyvalhalla_version="3.9.1",
        osm_url="https://example.org/gb",
        osm_last_modified="Tue, 20 Oct 2026 23:32:25 GMT",
    )

    builder.publish(local_extract, manifest)

    published = tmp_path / "volume" / "tiles" / "great-britain"
    assert (published / "valhalla_tiles.tar").read_bytes() == b"tiles"
    assert json.loads((published / MANIFEST_NAME).read_text())["size_bytes"] == 5
    assert not (published / "valhalla_tiles.tar.partial").exists()
