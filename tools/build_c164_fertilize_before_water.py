"""Build immutable c164 = frozen o182 + certified fertilizer/WATER reorder."""
import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o182_combo_overflow.py"
PARENT_SHA256 = "ef9d2aade50ce2ce400a64791288ffb179eee7a6e60ea0d06085ac12fe02900b"
OVERLAY = ROOT / "agent/overlays/c164_fertilize_before_water.py"
TARGET = ROOT / "agent/c164_fertilize_before_water.py"
MANIFEST = ROOT / "agent/c164_fertilize_before_water.manifest.json"


def frozen_write(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError("Existing immutable c164 artifact differs: " + str(path))
    if not path.exists():
        path.write_bytes(data)


def main():
    parent = PARENT.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA256, "o182 parent drift"
    overlay = OVERLAY.read_bytes().replace(b"\r\n", b"\n")
    header = ("# c164 build (GPT/Codex, 2026-09-15): parent "
              f"agent/o182_combo_overflow.py sha256 {PARENT_SHA256} + "
              "agent/overlays/c164_fertilize_before_water.py. "
              "Apache-2.0; parent notices retained below.\n").encode()
    candidate = header + parent + b"\n\n" + overlay
    compile(candidate, str(TARGET), "exec"); ast.parse(candidate.decode("utf-8"))
    namespace = {"__name__": "c164_build_check"}
    exec(compile(candidate, str(TARGET), "exec"), namespace)
    last = [k for k,v in namespace.items() if callable(v) and not k.startswith("__")][-1]
    assert last == "agent", f"last callable is {last}, not agent"
    frozen_write(TARGET, candidate)
    manifest = {"candidate": "c164", "parent": "agent/o182_combo_overflow.py",
                "parent_sha256": PARENT_SHA256,
                "overlay": "agent/overlays/c164_fertilize_before_water.py",
                "overlay_sha256": hashlib.sha256(overlay).hexdigest(),
                "target": "agent/c164_fertilize_before_water.py",
                "target_sha256": hashlib.sha256(candidate).hexdigest(),
                "bytes": len(candidate), "status": "implemented_unvalidated"}
    frozen_write(MANIFEST, (json.dumps(manifest, indent=2) + "\n").encode())
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
