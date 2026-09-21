"""Compose the published Local Best update with c358's productive opening."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from build_c358_localbest_hybrid import WRAPPER


ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = "89a50e928ea14281220413f73cc9fa16b7ad47f2bf930ba7279a75d125a21859"
PARENT = ROOT / "state/public_league/sources" / f"{PARENT_SHA}.py"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--disabled", action="store_true")
    args = parser.parse_args()
    body = PARENT.read_bytes()
    if hashlib.sha256(body).hexdigest() != PARENT_SHA:
        raise SystemExit("updated Local Best source identity drift")
    suffix = WRAPPER.replace("__C358_ENABLED__", str(not args.disabled)).encode()
    output = args.out.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(body.rstrip() + b"\n" + suffix.lstrip())
    compile(output.read_bytes(), str(output), "exec")
    print(f"{output} {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
