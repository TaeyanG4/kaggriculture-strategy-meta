"""Build r000_terminal_hold = immutable parent agent/c150.py + agent/overlays/r000_terminal_hold.py (parent SHA pinned, frozen writes).
Usage: python tools/build_r000_terminal_hold.py"""
import ast, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/c150.py"
PARENT_SHA = "9713af1538ccc8e4e0e8a7ff72ae8a614ba9e7dcb3eb9d53c3074aabec137d6b"
OVERLAY = ROOT / "agent/overlays/r000_terminal_hold.py"
TARGET = ROOT / "agent/r000_terminal_hold.py"
NL = b"\n"


def frozen_write(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError("Existing artifact differs: " + str(path))
    path.write_bytes(data)


def main():
    parent = PARENT.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA, "parent drift"
    overlay = OVERLAY.read_bytes().replace(b"\r\n", NL)
    header = ("# r000_terminal_hold build: parent agent/c150.py sha256 " + PARENT_SHA + " + agent/overlays/r000_terminal_hold.py (2026-09-15). Apache-2.0; parent notices retained below.").encode("utf-8") + NL
    candidate = header + parent + NL + overlay
    compile(candidate, "r000_terminal_hold", "exec"); ast.parse(candidate.decode("utf-8"))
    frozen_write(TARGET, candidate)
    print("r000_terminal_hold overlay SHA256:  ", hashlib.sha256(overlay).hexdigest())
    print("r000_terminal_hold candidate SHA256:", hashlib.sha256(candidate).hexdigest(), TARGET)


if __name__ == "__main__":
    main()
