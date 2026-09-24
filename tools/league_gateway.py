#!/usr/bin/env python
"""Repository-local launcher for the team league login gateway."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kaggriculture_meta.league_gateway import main

if __name__ == "__main__":
    raise SystemExit(main())
