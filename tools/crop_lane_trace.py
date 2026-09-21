"""Trace executed crop actions and crop-controller telemetry for two policies.

This is a diagnostic wrapper around the project's pinned native fastgame loop.
It does not alter actions, shops, or the engine.  Use fresh non-blind seeds and
both seats; the output records exact successful unit actions and selected
``*_REPORT`` dictionaries, including reports nested in packaged public agents.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import types


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "o_tools"))


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _crop(tile):
    return tile.get("crop") if isinstance(tile, dict) else None


def _reports(module, wanted=("_CA_REPORT", "_V9_CARROT_REPORT")):
    """Find selected report dictionaries through nested source-packaging NSes."""
    found, seen = {}, set()

    def walk(obj, prefix, depth):
        if depth > 16 or id(obj) in seen:
            return
        seen.add(id(obj))
        if isinstance(obj, dict):
            items = obj.items()
        elif isinstance(obj, types.SimpleNamespace):
            items = vars(obj).items()
        else:
            return
        for key, value in items:
            here = f"{prefix}.{key}" if prefix else key
            if key in wanted and isinstance(value, dict):
                found[here] = {
                    k: v for k, v in value.items()
                    if isinstance(v, (int, float, str, bool))
                }
            if isinstance(value, (dict, types.SimpleNamespace)) and (
                key.endswith("_NS") or key.startswith(("_BASE", "_PARENT", "_OP"))
            ):
                walk(value, here, depth + 1)

    walk(vars(module), "", 0)
    return found


def _load(path: str, name: str):
    from proxy_eval import load_agent
    return load_agent(path, name)


def play(job):
    a_path, b_path, seed, seat_b = job
    os.environ["MPLBACKEND"] = "Agg"
    os.chdir(ROOT)
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as eng

    a_agent = _load(a_path, "crop_trace_a")
    b_agent = _load(b_path, "crop_trace_b")
    modules = {"a": sys.modules["crop_trace_a"], "b": sys.modules["crop_trace_b"]}
    owner, current = {}, {"step": 0}
    events = {0: [], 1: []}
    decisions = {"a": [], "b": []}
    original = eng._apply_unit_action

    def capture(label, policy):
        def wrapped(observation, configuration=None):
            action = policy(observation, configuration)
            step = int(observation["step"])
            units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
            market = list(action.get("market") or [])
            crop_plant = any(cmd[:2] in (["PLANT", "WHEAT"], ["PLANT", "CARROT"])
                             for cmd in units if isinstance(cmd, list))
            wheat_market = any(len(order) >= 2 and order[1] == "WHEAT"
                               for order in market if isinstance(order, list))
            if step >= 18 * 24 and (crop_plant or wheat_market):
                private = observation["private"]
                decisions[label].append({
                    "step": step, "day": step // 24, "hour": step % 24,
                    "wheat_total": int(private["shed"].get("WHEAT", 0)) + sum(
                        int(inv.get("WHEAT", 0)) for inv in private["inventories"]),
                    "wheat_shed": int(private["shed"].get("WHEAT", 0)),
                    "wheat_inventories": [int(inv.get("WHEAT", 0))
                                           for inv in private["inventories"]],
                    "wheat_price": int(observation["market"]["prices"].get("WHEAT", 0)),
                    "carrot_price": int(observation["market"]["prices"].get("CARROT", 0)),
                    "units": copy.deepcopy(units),
                    "market": copy.deepcopy(market),
                })
            return action
        return wrapped

    def unit(farm, private, idx, action, board_size, day, turns_per_day,
             shed_capacity=100):
        player = owner[id(farm)]
        pos0 = eng._farmer_position(farm, idx)
        pos0 = tuple(pos0) if pos0 is not None else None
        inv0 = copy.deepcopy(eng._farmer_inventory(private, idx)) if pos0 is not None else {}
        tile0 = copy.deepcopy(farm["tiles"][pos0[1]][pos0[0]]) if pos0 is not None else None
        original(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
        if not (isinstance(action, list) and action and action[0] in
                {"PLANT", "HARVEST", "WATER", "FERTILIZE", "DIG"}):
            return
        pos1 = eng._farmer_position(farm, idx)
        pos1 = tuple(pos1) if pos1 is not None else None
        tile1 = copy.deepcopy(farm["tiles"][pos0[1]][pos0[0]]) if pos0 is not None else None
        inv1 = copy.deepcopy(eng._farmer_inventory(private, idx)) if pos0 is not None else {}
        success = tile0 != tile1 or inv0 != inv1 or pos0 != pos1
        events[player].append({
            "step": current["step"], "day": day, "hour": current["step"] % 24,
            "actor": idx, "pos": pos0, "action": list(action), "success": success,
            "crop_before": _crop(tile0), "crop_after": _crop(tile1),
            "yield_before": tile0.get("yield_units") if isinstance(tile0, dict) else None,
            "yield_after": tile1.get("yield_units") if isinstance(tile1, dict) else None,
        })

    def pre(env, step):
        current["step"] = step
        for player, farm in enumerate(env.state[0].observation.farms):
            owner[id(farm)] = player

    eng._apply_unit_action = unit
    try:
        env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=False)
        agents = [None, None]
        agents[seat_b] = capture("b", b_agent)
        agents[1 - seat_b] = capture("a", a_agent)
        with contextlib.redirect_stdout(io.StringIO()):
            fastgame.play(env, agents, deep=True, pre_hook=pre)
    finally:
        eng._apply_unit_action = original

    rewards = [float(state.reward or 0) for state in env.state]
    labels = {seat_b: "b", 1 - seat_b: "a"}
    return {
        "seed": seed,
        "seat_b": seat_b,
        "shops": list(env.state[0].observation.town["unlocked_shops"]),
        "final": rewards,
        "events": {labels[player]: values for player, values in events.items()},
        "decisions": decisions,
        "reports": {label: _reports(module) for label, module in modules.items()},
    }


def _seeds(value: str):
    if "," in value:
        return [int(v) for v in value.split(",")]
    if "-" in value:
        lo, hi = map(int, value.split("-", 1))
        return list(range(lo, hi + 1))
    return [int(value)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=Path, required=True)
    parser.add_argument("--b", type=Path, required=True)
    parser.add_argument("--seeds", required=True)
    parser.add_argument("--seats", default="0,1")
    parser.add_argument("--workers", type=int, default=8, choices=range(1, 9))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    a_path, b_path = args.a.resolve(), args.b.resolve()
    for path in (a_path, b_path):
        compile(path.read_bytes(), str(path), "exec")
    jobs = [(str(a_path), str(b_path), seed, seat)
            for seed in _seeds(args.seeds)
            for seat in [int(v) for v in args.seats.split(",")]]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(play, jobs))
    payload = {
        "schema": 1,
        "diagnostic_only": True,
        "sources": {
            "a": {"path": str(a_path), "sha256": _digest(a_path)},
            "b": {"path": str(b_path), "sha256": _digest(b_path)},
        },
        "workers": args.workers,
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    margins = [row["final"][row["seat_b"]] - row["final"][1-row["seat_b"]]
               for row in rows]
    print(json.dumps({
        "out": str(args.out), "games": len(rows),
        "b_wins": sum(value > 0 for value in margins),
        "mean_b_margin": sum(margins) / len(margins),
        "workers": args.workers,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
