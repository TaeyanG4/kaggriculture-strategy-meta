"""Build immutable c170 = frozen o182 + gain-constrained fertilizer assignment."""
import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o182_combo_overflow.py"
PARENT_SHA256 = "ef9d2aade50ce2ce400a64791288ffb179eee7a6e60ea0d06085ac12fe02900b"
OVERLAY = ROOT / "agent/overlays/c170_fertilizer_tour_assignment.py"
TARGET = ROOT / "agent/c170_fertilizer_tour_assignment.py"
MANIFEST = ROOT / "agent/c170_fertilizer_tour_assignment.manifest.json"


def frozen_write(path, payload):
    if path.exists() and path.read_bytes() != payload:
        raise ValueError("Existing immutable c170 artifact differs: " + str(path))
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def main():
    parent = PARENT.read_bytes()
    if hashlib.sha256(parent).hexdigest() != PARENT_SHA256:
        raise ValueError("o182 parent drift")
    overlay = OVERLAY.read_bytes().replace(b"\r\n", b"\n")
    header = (
        "# c170 build (GPT/Codex, 2026-09-15): parent "
        f"agent/o182_combo_overflow.py sha256 {PARENT_SHA256} + "
        "agent/overlays/c170_fertilizer_tour_assignment.py. "
        "Apache-2.0; parent notices retained below.\n"
    ).encode()
    candidate = header + parent + b"\n\n" + overlay
    compile(candidate, str(TARGET), "exec")
    ast.parse(candidate.decode("utf-8"), str(TARGET))
    namespace = {"__name__": "c170_build_check"}
    exec(compile(candidate, str(TARGET), "exec"), namespace)
    callables = [name for name, value in namespace.items()
                 if callable(value) and not name.startswith("__")]
    if not callables or callables[-1] != "agent":
        raise ValueError("last callable is not agent")
    frozen_write(TARGET, candidate)
    manifest = {
        "schema": 1,
        "candidate": "c170_fertilizer_tour_assignment",
        "supersedes": {
            "candidate": "c159_fertilizer_tour_assignment",
            "reason": "select only among target-level non-regressing beam states",
        },
        "status": "implemented_unvalidated",
        "parent": {"path": "agent/o182_combo_overflow.py", "sha256": PARENT_SHA256},
        "overlay": {"path": "agent/overlays/c170_fertilizer_tour_assignment.py",
                    "sha256": hashlib.sha256(overlay).hexdigest()},
        "output": {"path": "agent/c170_fertilizer_tour_assignment.py",
                   "sha256": hashlib.sha256(candidate).hexdigest(),
                   "bytes": len(candidate)},
        "contract": {
            "parent_action_unchanged": True,
            "target_multiset_unchanged": True,
            "worker_count_unchanged": True,
            "worker_quantities_unchanged": True,
            "fertilizer_purchase_unchanged": True,
            "exact_spawn_after_current_moves": True,
            "first_route_action_step_offset": 2,
            "per_target_gain_non_regression": True,
            "per_target_gain_floor_applied_during_search": True,
            "strict_gain_required": True,
            "beam_width": 128,
        },
        "promotion": False,
    }
    frozen_write(MANIFEST, (json.dumps(manifest, indent=2) + "\n").encode())
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
