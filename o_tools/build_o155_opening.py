"""Build o155_opening_sweep_<variant>.py: c150 (unmodified, imported by path) with the step-0
market action overridden externally (the parent's own step-0 action is discarded and replaced,
same technique c150 itself uses internally for _R42_OPENING, just applied post-hoc instead of
inside the tape). Only step 0 is touched; every other step is passed through unmodified.

This is a cheap, safe parameter-search candidate (backlog W): the opening WHEAT buy/sell amounts
are a free parameter nothing else in the file depends on structurally (verified: the tape's own
step-0 entries are fully overwritten by _R42_OPENING already, so overriding them again post-hoc
cannot conflict with any per-route scripted content).

Usage: .venv/Scripts/python.exe o_tools/build_o155_opening.py --buy1 13 --buy2 10 --sell 30 --out agent/o155_open_13_10_30.py
"""
import argparse
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE = '''"""o155_opening_sweep (Claude/o-series, 2026-09-14). Parent: c150 (unmodified, read-only).

Backlog W (parameter search): c150's own step-0 opening market override (_R42_OPENING) is
BUY_PRODUCT WHEAT {buy1} + BUY_PRODUCT WHEAT {buy2} + SELL WHEAT {sell} (a fixed constant, not
tuned per this variant). This candidate overrides step-0's market action a second time,
externally, with an alternative (buy1={buy1}, buy2={buy2}, sell={sell}) to screen for a better
opening. Every other step is untouched (parent action passed straight through).
"""
import importlib.util
import os as _os

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_C150_PATH = _os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o155_c150_base_{tag}", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of

_OPENING = [["BUY_PRODUCT", "WHEAT", {buy1}], ["BUY_PRODUCT", "WHEAT", {buy2}], ["SELL", "WHEAT", {sell}]]


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
    try:
        if _step_of(observation) == 0:
            action = dict(action)
            action["market"] = [list(o) for o in _OPENING]
    except Exception:
        pass
    return action
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--buy1", type=int, required=True)
    ap.add_argument("--buy2", type=int, required=True)
    ap.add_argument("--sell", type=int, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tag = os.path.basename(a.out).replace(".py", "")
    out = TEMPLATE.format(buy1=a.buy1, buy2=a.buy2, sell=a.sell, tag=tag)
    path = os.path.join(ROOT, a.out)
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    compile(out, tag, "exec")
    print("built", a.out)


if __name__ == "__main__":
    main()
