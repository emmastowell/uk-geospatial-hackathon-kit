"""Runtime settings, read from the environment that app.yaml sets."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Where the tiles are published, where to cache them and how many requests run at once."""

    tiles_dir: str
    cache_dir: Path
    actor_pool_size: int
    poll_seconds: float

    @classmethod
    def from_env(cls) -> "Settings":
        tiles_dir = os.environ.get("VALHALLA_TILES_DIR", "").rstrip("/")
        if not tiles_dir:
            raise RuntimeError("VALHALLA_TILES_DIR must name the published tiles directory")
        pool_size = int(os.environ.get("VALHALLA_ACTOR_POOL_SIZE", "4"))
        if pool_size < 1:
            raise ValueError("VALHALLA_ACTOR_POOL_SIZE must be at least 1")
        return cls(
            tiles_dir=tiles_dir,
            cache_dir=Path(os.environ.get("VALHALLA_CACHE_DIR", "/tmp/valhalla")),
            actor_pool_size=pool_size,
            poll_seconds=float(os.environ.get("VALHALLA_POLL_SECONDS", "60")),
        )
