"""Run with the App's environment, which has FastAPI and pyvalhalla:

uv run --project src/app --frozen --with pytest --with httpx pytest tests/app
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "app"))
