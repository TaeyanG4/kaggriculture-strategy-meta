"""Build c155 = provisional parent c150 + agent/overlays/c155_milk_externality_gate.py.

Parent choice: c150 is used provisionally (HANDOFF still names c129 the live baseline; c150 and
c129 tie exactly in every local mirror game measured so far and c150 is the baseline of the
existing 88-game elite suite). Neither parent nor overlay is modified; outputs are frozen (an
existing differing artifact aborts the build).

Usage:
  python tools/build_c155_milk_externality.py            # apply-mode candidate (submission default)
  python tools/build_c155_milk_externality.py --observe  # observe-only twin (_C155_APPLY = False)
"""
import argparse
import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/c150.py"
PARENT_SHA = "9713af1538ccc8e4e0e8a7ff72ae8a614ba9e7dcb3eb9d53c3074aabec137d6b"
OVERLAY = ROOT / "agent/overlays/c155_milk_externality_gate.py"
TARGET = ROOT / "agent/c155_milk_externality.py"
TARGET_OBSERVE = ROOT / "agent/c155_milk_externality_observe.py"


def frozen_write(path: Path, data: bytes):
    if path.exists() and path.read_bytes() != data:
        raise ValueError("Existing c155 artifact differs: " + str(path))
    path.write_bytes(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--observe", action="store_true", help="also build the observe-only twin")
    args = ap.parse_args()
    parent = PARENT.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA, "c150 parent drift"
    overlay = OVERLAY.read_bytes().decode("utf-8").replace("\r\n", "\n")
    assert overlay.count("_C155_APPLY = True\n") == 1
    header = (b"# c155 build: parent agent/c150.py sha256 " + PARENT_SHA.encode() +
              b" + agent/overlays/c155_milk_externality_gate.py (2026-09-15). Apache-2.0; parent notices retained below.\n")
    candidate = header + parent + b"\n" + overlay.encode("utf-8")
    compile(candidate, "c155", "exec"); ast.parse(candidate.decode("utf-8"))
    frozen_write(TARGET, candidate)
    print("c155 overlay SHA256:  ", hashlib.sha256(overlay.encode("utf-8")).hexdigest())
    print("c155 candidate SHA256:", hashlib.sha256(candidate).hexdigest(), TARGET)
    if args.observe:
        obs = overlay.replace("_C155_APPLY = True\n", "_C155_APPLY = False\n")
        cand_obs = header.replace(b"c155 build:", b"c155 OBSERVE-ONLY build:") + parent + b"\n" + obs.encode("utf-8")
        compile(cand_obs, "c155_observe", "exec")
        frozen_write(TARGET_OBSERVE, cand_obs)
        print("c155 observe-only SHA256:", hashlib.sha256(cand_obs).hexdigest(), TARGET_OBSERVE)


if __name__ == "__main__":
    main()
