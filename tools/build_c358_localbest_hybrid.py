"""Build the c358 Local Best + V54 productive-idle opening candidate.

The public Local Best source is kept byte-for-byte as the body.  The appended
wrapper only applies V54's published HybridOpening edits to the body's native
route-0 tape and accounts for the two harvested wheat units at delivery.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_BEST_SHA = "41dd60f718c701666f45b23f94e05922354a48189b931e6c6091134d3426fc25"
LOCAL_BEST = ROOT / "state/public_league/sources" / f"{LOCAL_BEST_SHA}.py"


WRAPPER = r'''

# c358: compose Local Best's public market stack with V54's exact one-tile
# Productive Idle Workers opening.  Both source lineages and notices remain
# above.  This wrapper is original integration code by Taeyang/Codex, 2026.
import copy as _c358_copy

_C358_ENABLED = __C358_ENABLED__
_C358_PARENT = agent
_C358_STATE = {}
_C358_REPORT = {}


def _c358_find_impl(namespace):
    seen = set()
    while isinstance(namespace, dict) and id(namespace) not in seen:
        seen.add(id(namespace))
        impl = namespace.get("_IMPL")
        if impl is not None:
            return impl
        namespace = namespace.get("_BASE_NS")
    return None


_C358_IMPL = _c358_find_impl(globals())
if _C358_ENABLED and _C358_IMPL is None:
    raise RuntimeError("c358 could not locate the native tape chassis")
_C358_RAW = (_c358_copy.deepcopy(_C358_IMPL.chassis.routes[0][:96])
             if _C358_IMPL is not None else None)


def _c358_install():
    tape = _C358_IMPL.chassis.routes[0]
    tape[:96] = _c358_copy.deepcopy(_C358_RAW)
    tape[0]["market"] = list(tape[0]["market"]) + [["BUY_SEED", "WHEAT", 1]]
    for step, command in {
        2: ["WEST"], 3: ["WEST"], 4: ["WEST"],
        5: ["PLANT", "WHEAT"], 6: ["WATER"],
    }.items():
        if tape[step]["hands"][1] != ["PASS"]:
            raise RuntimeError("c358 route-0 day-zero contract drift")
        tape[step]["hands"][1] = command
    if tape[29]["hands"][2] != ["BUILD_PASTURE"]:
        raise RuntimeError("c358 route-0 day-one contract drift")
    tape[29]["hands"][2] = ["WATER"]
    commands = [
        ["WEST"], ["WEST"], ["WEST"], ["WATER"], ["HARVEST"],
        ["BUILD_PASTURE"], ["EAST"], ["EAST"], ["DROP"],
    ]
    for step, command in zip(range(49, 58), commands):
        if tape[step]["hands"][0] != ["PASS"]:
            raise RuntimeError("c358 route-0 day-two contract drift")
        tape[step]["hands"][0] = command
    if max(len(action.get("market", [])) for action in tape[:96]) > 10:
        raise RuntimeError("c358 market order overflow")


def _c358_sell_extra(action, item, quantity):
    if quantity <= 0:
        return action
    orders = [list(order) for order in action.get("market", [])]
    sell = next((order for order in orders
                 if len(order) >= 3 and order[:2] == ["SELL", item]), None)
    if sell is not None:
        sell[2] += quantity
    elif len(orders) < 10:
        orders.append(["SELL", item, quantity])
    else:
        return action
    return dict(action, market=orders)


def agent(observation, configuration=None):
    seat = int(observation["player"])
    step = int(observation["step"])
    state = _C358_STATE.get(seat)
    if state is None or step <= state["step"]:
        if _C358_ENABLED:
            _c358_install()
        state = _C358_STATE[seat] = {"step": -1}
        _C358_REPORT.clear()
        _C358_REPORT.update(
            temporary_crop_seen=0, temporary_crop_harvested=0,
            restored_pasture_seen=0, delivered_extra_wheat=0,
            extension_errors=0,
        )
    action = _C358_PARENT(observation, configuration)
    if _C358_ENABLED:
        try:
            farm = observation["farms"][seat]
            private = observation["private"]
            site = farm["tiles"][4][2]
            if step == 6:
                _C358_REPORT["temporary_crop_seen"] = int(
                    isinstance(site, dict) and site.get("crop") == "WHEAT")
            if step == 54:
                _C358_REPORT["temporary_crop_harvested"] = int(
                    private["inventories"][1].get("WHEAT", 0))
            if step == 55:
                _C358_REPORT["restored_pasture_seen"] = int(
                    isinstance(site, dict) and site.get("kind") == "PASTURE")
            if (step == 57 and len(farm["hands"]) >= 1
                    and tuple(farm["hands"][0]) == (4, 4)
                    and action.get("hands", [[]])[0] == ["DROP"]):
                quantity = int(private["inventories"][1].get("WHEAT", 0))
                action = _c358_sell_extra(action, "WHEAT", quantity)
                _C358_REPORT["delivered_extra_wheat"] = quantity
        except Exception:
            _C358_REPORT["extension_errors"] += 1
    state["step"] = step
    return action


agent.telemetry = _C358_REPORT
kaggle_submission_agent = agent
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--disabled", action="store_true")
    args = parser.parse_args()
    body = LOCAL_BEST.read_bytes()
    if hashlib.sha256(body).hexdigest() != LOCAL_BEST_SHA:
        raise SystemExit("Local Best source identity drift")
    suffix = WRAPPER.replace("__C358_ENABLED__", str(not args.disabled)).encode()
    output = args.out.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(body.rstrip() + b"\n" + suffix.lstrip())
    compile(output.read_bytes(), str(output), "exec")
    print(f"{output} {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
