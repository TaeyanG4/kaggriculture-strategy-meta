#!/usr/bin/env python
"""Repository-local launcher for the unattended public notebook league."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kaggriculture_meta.public_league import main

if __name__ == "__main__":
    main()
