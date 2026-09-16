"""Build o162_goose_only = immutable parent agent/o159b_feed_margin06.py + agent/overlays/o162_goose_only.py (parent SHA pinned, frozen writes).
Usage: python tools/build_o162_goose_only.py"""
import ast, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o159b_feed_margin06.py"
PARENT_SHA = "cbcc866ce8f710d62c3f6673c743c714643f6aab32b81beba201b9085f3f887a"
OVERLAY = ROOT / "agent/overlays/o162_goose_only.py"
TARGET = ROOT / "agent/o162_goose_only.py"
NL = b"\n"


def frozen_write(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError("Existing artifact differs: " + str(path))
    path.write_bytes(data)


def main():
    parent = PARENT.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA, "parent drift"
    overlay = OVERLAY.read_bytes().replace(b"\r\n", NL)
    header = ("# o162_goose_only build: parent agent/o159b_feed_margin06.py sha256 " + PARENT_SHA + " + agent/overlays/o162_goose_only.py (2026-09-15). Apache-2.0; parent notices retained below.").encode("utf-8") + NL
    candidate = header + parent + NL + overlay
    compile(candidate, "o162_goose_only", "exec"); ast.parse(candidate.decode("utf-8"))
    frozen_write(TARGET, candidate)
    print("o162_goose_only overlay SHA256:  ", hashlib.sha256(overlay).hexdigest())
    print("o162_goose_only candidate SHA256:", hashlib.sha256(candidate).hexdigest(), TARGET)


if __name__ == "__main__":
    main()
