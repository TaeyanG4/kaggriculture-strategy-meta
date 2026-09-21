"""Build c359: c358 with the public One More Wheat maturation schedule.

The parent is the submitted c358 source.  This wrapper keeps the same one-tile,
idle-worker opening, leaves its day-two watering in place, and delays harvest,
pasture restoration, and delivery until day three so the wheat matures once
more.  It does not add land, workers, or replace another crop.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = "680a4f713d8d672dce3f13f5429df1f803626f408d76e1690eabe32152779196"
PARENT = ROOT / "agent/c358_localbest_hybrid.py"


WRAPPER = r'''

# c359: mature c358's temporary wheat one extra day using the public
# One More Wheat schedule by Dmitrii Gluzdov (Apache-2.0 notice retained in
# its source). Integration and contract checks: Taeyang/Codex, 2026.
_C359_PARENT = agent
_C359_STATE = {}
_C359_REPORT = {}


def _c359_install():
    tape = _C358_IMPL.chassis.routes[0]
    # c358 walks west and waters at 49..52. Remove its immediate harvest,
    # pasture restoration, and return to the shed.
    for step in range(53, 58):
        tape[step]["hands"][0] = ["PASS"]
    commands = [
        ["EAST"], ["EAST"], ["WATER"], ["HARVEST"],
        ["BUILD_PASTURE"], ["EAST"], ["EAST"], ["DROP"],
    ]
    for step, command in zip(range(84, 92), commands):
        existing = tape[step]["hands"][0]
        if existing not in (["PASS"], command):
            raise RuntimeError("c359 day-three idle route contract drift")
        tape[step]["hands"][0] = command


def agent(observation, configuration=None):
    seat = int(observation["player"])
    step = int(observation["step"])
    state = _C359_STATE.get(seat)
    reset = state is None or step <= state["step"]
    action = _C359_PARENT(observation, configuration)
    if reset:
        # The parent reinstalls c358 at step zero; patch after that reset.
        _c359_install()
        state = _C359_STATE[seat] = {"step": -1}
        _C359_REPORT.clear()
        _C359_REPORT.update(
            mature_harvested=0, restored_pasture_seen=0,
            delivered_extra_wheat=0, extension_errors=0,
        )
    try:
        farm = observation["farms"][seat]
        private = observation["private"]
        if step == 88:
            _C359_REPORT["mature_harvested"] = int(
                private["inventories"][1].get("WHEAT", 0))
        if step == 89:
            tile = farm["tiles"][4][2]
            _C359_REPORT["restored_pasture_seen"] = int(
                isinstance(tile, dict) and tile.get("kind") == "PASTURE")
        if (step == 91 and farm["hands"]
                and tuple(farm["hands"][0]) == (4, 4)
                and action.get("hands", [[]])[0] == ["DROP"]):
            amount = int(private["inventories"][1].get("WHEAT", 0))
            action = _c358_sell_extra(action, "WHEAT", amount)
            _C359_REPORT["delivered_extra_wheat"] = amount
    except Exception:
        _C359_REPORT["extension_errors"] += 1
    state["step"] = step
    return action


agent.telemetry = _C359_REPORT
kaggle_submission_agent = agent
# The parent already created ``kaggle_submission_agent``. Reassigning an
# existing dict key does not move it to the end, while Kaggle selects the last
# callable by namespace insertion order. This fresh export must remain last.
c359_submission_agent = agent
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    body = PARENT.read_bytes()
    if hashlib.sha256(body).hexdigest() != PARENT_SHA:
        raise SystemExit("c358 parent identity drift")
    output = args.out.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(body.rstrip() + b"\n" + WRAPPER.lstrip().encode())
    compile(output.read_bytes(), str(output), "exec")
    print(f"{output} {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
