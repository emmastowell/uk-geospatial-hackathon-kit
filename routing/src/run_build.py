"""Job bootstrap: install the routing wheel, then run the tile build.

Databricks python_wheel_task failed to import the package on this workspace and
returned no pip log. Installing from the uploaded wheel in-process surfaces the
error, and keeps pyvalhalla out of the Spark driver.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> None:
    """Install ``--wheel`` then dispatch remaining arguments to the tile builder."""

    parser = argparse.ArgumentParser(description="Install the routing wheel and build tiles.")
    parser.add_argument("--wheel", required=True)
    args, rest = parser.parse_known_args()
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        args.wheel,
    ]
    print(f"installing {args.wheel}")
    subprocess.run(command, check=True)  # noqa: S603
    sys.argv = [sys.argv[0], *rest]
    from routing_in_a_box.build_tiles import main as build_main

    build_main()


if __name__ == "__main__":
    main()
