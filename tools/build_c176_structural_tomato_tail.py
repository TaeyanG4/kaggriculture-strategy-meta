"""Build c176 as frozen o199c plus the structural tomato-tail overlay."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o199c_carrot_price2.py"
OVERLAY = ROOT / "agent/overlays/c176_structural_tomato_tail.py"
OUTPUT = ROOT / "agent/c176_structural_tomato_tail.py"
MANIFEST = ROOT / "agent/c176_structural_tomato_tail.manifest.json"
PARENT_SHA256 = "1429673c3c1057c07f0a644124a4fd497b111b1646451bac1de852e5c035a41d"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build() -> dict:
    parent = PARENT.read_bytes()
    if sha256(parent) != PARENT_SHA256:
        raise RuntimeError("o199c parent changed; refusing to build c176")
    overlay = OVERLAY.read_bytes()
    payload = parent.rstrip(b"\r\n") + b"\n\n" + overlay.rstrip(b"\r\n") + b"\n"
    compile(payload, str(OUTPUT), "exec")
    OUTPUT.write_bytes(payload)
    manifest = {
        "schema": 1,
        "candidate": "c176_structural_tomato_tail",
        "status": "implemented_unvalidated",
        "parent": {"path": "agent/o199c_carrot_price2.py", "sha256": PARENT_SHA256},
        "overlay": {
            "path": "agent/overlays/c176_structural_tomato_tail.py",
            "sha256": sha256(overlay),
        },
        "hypothesis": (
            "At the day-18 boundary, replace a bounded set of already-unlocked late WHEAT "
            "plantings with a coherent TOMATO suffix (seed, maintenance labor, near-term "
            "wheat reserve, harvest, delivery, sale) instead of V219's southeast-land buy."
        ),
        "contracts": {
            "immutable_parent": True,
            "adds_buy_land": False,
            "default_auto_gate": "day18; >=2 PIZZA_SHOP/FARMERS_MARKET; TOMATO>=70; carrot not hot",
            "auto_size": "8 tiles for 2 tomato-demand shops; 10 for >=3",
            "force_env": "KAGG_C176_FORCE=KEEP|REALLOC; KAGG_C176_SIZE=1..10",
            "plant_window": "days18-20 actual parent PLANT WHEAT on empty unlocked tiles",
            "feed_contract": "48-step native WHEAT pickup reserve, max 12-unit top-up/day",
            "promotion": False,
            "submission": False,
        },
        "output": {"path": "agent/c176_structural_tomato_tail.py", "sha256": sha256(payload), "bytes": len(payload)},
        "promotion": False,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
