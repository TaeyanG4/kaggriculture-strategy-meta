"""Build o161_harvest_only = immutable parent agent/c150.py + agent/overlays/o161_harvest_only.py (parent SHA pinned, frozen writes).
Usage: python tools/build_o161_harvest_only.py"""
import ast, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/c150.py"
PARENT_SHA = "9713af1538ccc8e4e0e8a7ff72ae8a614ba9e7dcb3eb9d53c3074aabec137d6b"
OVERLAY = ROOT / "agent/overlays/o161_harvest_only.py"
TARGET = ROOT / "agent/o161_harvest_only.py"
NL = b"\n"


def frozen_write(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError("Existing artifact differs: " + str(path))
    path.write_bytes(data)


def main():
    parent = PARENT.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA, "parent drift"
    overlay = OVERLAY.read_bytes().replace(b"\r\n", NL)
    header = ("# o161_harvest_only build: parent agent/c150.py sha256 " + PARENT_SHA + " + agent/overlays/o161_harvest_only.py (2026-09-15). Apache-2.0; parent notices retained below.").encode("utf-8") + NL
    candidate = header + parent + NL + overlay
    compile(candidate, "o161_harvest_only", "exec"); ast.parse(candidate.decode("utf-8"))
    frozen_write(TARGET, candidate)
    print("o161_harvest_only overlay SHA256:  ", hashlib.sha256(overlay).hexdigest())
    print("o161_harvest_only candidate SHA256:", hashlib.sha256(candidate).hexdigest(), TARGET)


if __name__ == "__main__":
    main()
