"""Rebase the exact Local Best market-operator stack onto the exact V54 policy.

The public Local Best artifact is a deterministic chain of base85+LZMA wrappers.
Only the innermost base payload is replaced.  Every wrapper, operator payload,
configuration value, and attribution line remains byte-for-byte unchanged.
"""
from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import lzma
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_BEST_SHA = "41dd60f718c701666f45b23f94e05922354a48189b931e6c6091134d3426fc25"
V54_SHA = "949e2eed410169f7a651e82bb37f6484a332a833d8c75937122701b90fc7658c"
LOCAL_BEST = ROOT / "state/public_league/sources" / f"{LOCAL_BEST_SHA}.py"
V54 = ROOT / "state/public_league/sources" / f"{V54_SHA}.py"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode(value: str) -> str:
    return lzma.decompress(base64.b85decode(value)).decode("utf-8")


def encode(value: str) -> str:
    # The public builder used preset 9.  Pinning it makes a no-op rebuild
    # byte-identical and turns the source chain into a reproducible contract.
    return base64.b85encode(lzma.compress(value.encode("utf-8"), preset=9)).decode("ascii")


def first_payload(source: str):
    tree = ast.parse(source)
    calls = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "_decode" and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)):
            calls.append(node.args[0])
    return min(calls, key=lambda node: (node.lineno, node.col_offset)) if calls else None


def offsets(source: str, node: ast.Constant) -> tuple[int, int]:
    lines = source.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:node.lineno - 1]) + node.col_offset
    end = sum(len(line) for line in lines[:node.end_lineno - 1]) + node.end_col_offset
    return start, end


def innermost(source: str) -> str:
    node = first_payload(source)
    return source if node is None else innermost(decode(node.value))


def rebase(source: str, base: str) -> str:
    node = first_payload(source)
    if node is None:
        return base
    child = rebase(decode(node.value), base)
    start, end = offsets(source, node)
    return source[:start] + repr(encode(child)) + source[end:]


def replace_outer_base(source: str, base: str) -> str:
    """Keep only the public outer wrapper and replace its embedded base."""
    node = first_payload(source)
    if node is None:
        raise ValueError("outer source has no embedded base payload")
    start, end = offsets(source, node)
    return source[:start] + repr(encode(base)) + source[end:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--audit-reproduction", action="store_true")
    parser.add_argument("--outer-only", action="store_true")
    args = parser.parse_args()

    outer = LOCAL_BEST.read_bytes()
    base = V54.read_bytes()
    if sha(outer) != LOCAL_BEST_SHA:
        raise SystemExit("Local Best source identity drift")
    if sha(base) != V54_SHA:
        raise SystemExit("V54 source identity drift")
    outer_text = outer.decode("utf-8")
    if args.audit_reproduction:
        rebuilt = rebase(outer_text, innermost(outer_text)).encode("utf-8")
        if rebuilt != outer:
            raise SystemExit("Wrapper-chain reproduction failed")

    result_text = (replace_outer_base(outer_text, base.decode("utf-8"))
                   if args.outer_only else
                   rebase(outer_text, base.decode("utf-8")))
    result = result_text.encode("utf-8")
    compile(result, str(args.out), "exec")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(result)
    print(f"{args.out.resolve()} {sha(result)} bytes={len(result)}")


if __name__ == "__main__":
    main()
