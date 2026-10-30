from pathlib import Path

import pytest

from routing_in_a_box.build_tiles import parse_arguments


def test_accepts_pushed_down_job_parameters_with_underscores() -> None:
    arguments = parse_arguments(
        [
            "--volume-path=/Volumes/playground/routing/valhalla",
            "--extent=great-britain",
            "--osm_url=https://example.org/gb.osm.pbf",
            "--refresh_osm=true",
        ]
    )

    assert arguments.osm_url == "https://example.org/gb.osm.pbf"
    assert arguments.refresh_osm is True
    volume = Path("/Volumes/playground/routing/valhalla")
    assert arguments.pbf_path == volume / "osm" / "great-britain.osm.pbf"


def test_rejects_an_extent_that_is_not_a_path_slug() -> None:
    with pytest.raises(ValueError, match="lowercase slug"):
        parse_arguments(["--volume-path=/v", "--extent=../elsewhere"])
