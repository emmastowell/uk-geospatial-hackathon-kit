"""Lock both projects through a PyPI mirror, then point the locks at public PyPI.

Use this when your laptop reaches PyPI only through a mirror (for example the Databricks
PyPI proxy) but Databricks Apps install from public PyPI. The mirror must serve
byte-identical files under the same paths, so swapping hosts keeps every hash valid.
With direct PyPI access, plain ``uv lock`` and ``uv lock --project src/app`` are enough.

Usage: PYPI_MIRROR=https://pypi-proxy.example.com uv run python scripts/lock_app.py
"""

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = (ROOT, ROOT / "src" / "app")
DEFAULT_MIRROR = "https://pypi-proxy.cloud.databricks.com"


def publicise(lock_text: str, mirror: str) -> str:
    """Return the lock with every mirror URL replaced by its public PyPI equivalent."""

    replacements = (
        (f"{mirror}/simple/", "https://pypi.org/simple"),
        (f"{mirror}/packages/", "https://files.pythonhosted.org/packages/"),
    )
    for mirror_url, public_url in replacements:
        lock_text = lock_text.replace(mirror_url, public_url)
    if mirror in lock_text:
        raise ValueError(f"uv.lock still references {mirror} after rewriting")
    return lock_text


def main() -> None:
    """Resolve each project through the mirror and rewrite its uv.lock for public PyPI."""

    mirror = os.environ.get("PYPI_MIRROR", DEFAULT_MIRROR).rstrip("/")
    environment = {**os.environ, "UV_DEFAULT_INDEX": f"{mirror}/simple/"}
    for project in PROJECTS:
        subprocess.run(["uv", "lock", "--project", str(project)], check=True, env=environment)  # noqa: S603, S607
        lock_path = project / "uv.lock"
        lock_path.write_text(publicise(lock_path.read_text(), mirror))
        print(f"rewrote {lock_path} for public PyPI")


if __name__ == "__main__":
    main()
