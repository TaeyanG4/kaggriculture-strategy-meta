"""Build immutable c156 = frozen o182 + c156 production-cap harvest overlay."""
import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o182_combo_overflow.py"
PARENT_SHA256 = "ef9d2aade50ce2ce400a64791288ffb179eee7a6e60ea0d06085ac12fe02900b"
OVERLAY = ROOT / "agent/overlays/c156_production_cap_harvest.py"
TARGET = ROOT / "agent/c156_production_cap_harvest.py"
MANIFEST = ROOT / "agent/c156_production_cap_harvest.manifest.json"


def frozen_write(path, payload):
    if path.exists() and path.read_bytes() != payload:
        raise ValueError("Existing immutable c156 artifact differs: " + str(path))
    if not path.exists():
        path.write_bytes(payload)


def main():
    parent = PARENT.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA256, "o182 parent drift"
    overlay = OVERLAY.read_bytes().replace(b"\r\n", b"\n")
    overlay_sha = hashlib.sha256(overlay).hexdigest()
    header = ("# c156 build (GPT/Codex, 2026-09-15): parent "
              f"agent/o182_combo_overflow.py sha256 {PARENT_SHA256} + "
              "agent/overlays/c156_production_cap_harvest.py. "
              "Apache-2.0; parent notices retained below.\n").encode()
    candidate = header + parent + b"\n\n" + overlay
    compile(candidate, str(TARGET), "exec")
    ast.parse(candidate.decode("utf-8"))
    namespace = {"__name__": "c156_build_check"}
    exec(compile(candidate, str(TARGET), "exec"), namespace)
    last_callable = [key for key, value in namespace.items()
                     if callable(value) and not key.startswith("__")][-1]
    assert last_callable == "agent", f"last callable is {last_callable}, not agent"
    frozen_write(TARGET, candidate)
    manifest = {
        "candidate": "c156",
        "parent": str(PARENT.relative_to(ROOT)).replace("\\", "/"),
        "parent_sha256": PARENT_SHA256,
        "overlay": str(OVERLAY.relative_to(ROOT)).replace("\\", "/"),
        "overlay_sha256": overlay_sha,
        "target": str(TARGET.relative_to(ROOT)).replace("\\", "/"),
        "target_sha256": hashlib.sha256(candidate).hexdigest(),
        "bytes": len(candidate),
        "status": "implemented_unvalidated",
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
    frozen_write(MANIFEST, manifest_bytes)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
