"""Build o004 = c129 tape opening + o001 adaptive planner from a switch step.

Usage: .venv/Scripts/python.exe tools/build_o004.py --switch 288 --out agent/o004_hybrid_288.py
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TAIL = '''

# ---------------------------------------------------------------------------
# o004 hybrid (Claude lineage): the c129 tape plays the opening, the o001
# demand planner takes over every unit and the market from step _O4_SWITCH.
# ---------------------------------------------------------------------------
_O4_TAPE_PARENT = agent
del agent
_O4_SWITCH = %(switch)d
_O4_PLANNER_SRC = %(src)r
_O4_NS = {"__name__": "o001_planner"}
exec(_O4_PLANNER_SRC, _O4_NS)
_O4_PLANNER = _O4_NS["agent"]
_O4_REPORT = {}


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    if step < _O4_SWITCH:
        result = _O4_TAPE_PARENT(observation, configuration)
    else:
        result = _O4_PLANNER(observation, configuration)
    _O4_REPORT.clear()
    _O4_REPORT.update({"o4_switch": _O4_SWITCH})
    return result


agent.telemetry = _O4_REPORT
agent = globals().pop("agent")
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--switch", type=int, default=288)
    ap.add_argument("--parent", default="agent/c129_feed_liquidity.py")
    ap.add_argument("--planner", default="agent/o001_demand_planner.py")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    parent = (ROOT / a.parent).read_text(encoding="utf-8")
    planner = (ROOT / a.planner).read_text(encoding="utf-8")
    out = parent + TAIL % {"switch": a.switch, "src": planner}
    compile(out, "o004", "exec")
    (ROOT / a.out).write_text(out, encoding="utf-8")
    print("built", a.out, len(out))


if __name__ == "__main__":
    main()
