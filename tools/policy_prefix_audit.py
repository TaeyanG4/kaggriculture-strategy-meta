"""Compare two complete policies before their first observable/action divergence.

This is a diagnostic only.  It reuses the pinned Kaggriculture engine and the
already-verified fastgame loop, records only information visible to the policy,
and never treats a later shop draw or final reward as a decision-time feature.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "o_tools"))

from kaggle_environments import make
from kaggle_environments.agent import build_agent
import fastgame


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.loads(json.dumps(value, sort_keys=True, separators=(",", ":")))


def visible_observation(obs):
    value = canonical(dict(obs))
    value.pop("remainingOverageTime", None)
    return value


def tile_counts(farm):
    counts = {}
    for row in farm["tiles"]:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            key = tile.get("crop") or tile.get("animal") or tile.get("kind")
            counts[key] = counts.get(key, 0) + 1
    return counts


def visible_summary(obs):
    player = int(obs["player"])
    farms = obs["farms"]
    return {
        "step": int(obs["step"]),
        "player": player,
        "shops": list(obs["town"]["unlocked_shops"]),
        "prices": dict(obs["market"]["prices"]),
        "own_money": farms[player]["money"],
        "rival_money": farms[1 - player]["money"],
        "own_tiles": tile_counts(farms[player]),
        "rival_tiles": tile_counts(farms[1 - player]),
        "own_farmer": list(farms[player]["farmer"]),
        "rival_farmer": list(farms[1 - player]["farmer"]),
        "own_hands": [list(p) for p in farms[player]["hands"]],
        "rival_hands": [list(p) for p in farms[1 - player]["hands"]],
        "own_shed": dict(obs["private"]["shed"]),
        "own_seeds": dict(obs["private"]["seeds"]),
    }


def load(path: Path):
    policy, _ = build_agent(str(path), {}, "kaggriculture")
    return policy


def run(path: Path, opponent: Path, seed: int, seat: int, capture_steps: int):
    policy = load(path)
    rival = load(opponent)
    records = []

    def capture(obs, config):
        action = policy(obs, config)
        if int(obs["step"]) < capture_steps:
            records.append({
                "step": int(obs["step"]),
                "observation": visible_observation(obs),
                "summary": visible_summary(obs),
                "action": canonical(action),
            })
        return action

    agents = [None, None]
    agents[seat] = capture
    agents[1 - seat] = rival
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=False)
    fastgame.play(env, agents, deep=True)
    final = [state.reward for state in env.state]
    return {
        "records": records,
        "rewards": final,
        "statuses": [state.status for state in env.state],
        "resolved_seed": env.info.get("seed"),
    }


def compare(a, b, seed, seat):
    ar, br = a["records"], b["records"]
    if len(ar) != len(br):
        raise ValueError("capture length differs")
    first_observation = next((x["step"] for x, y in zip(ar, br)
                              if x["observation"] != y["observation"]), None)
    first_action = next((x["step"] for x, y in zip(ar, br)
                         if x["action"] != y["action"]), None)
    first_shop = next((x["step"] for x in ar if x["summary"]["shops"]), None)
    index = first_action if first_action is not None and first_action < len(ar) else None
    return {
        "seed": seed,
        "seat": seat,
        "first_observation_difference": first_observation,
        "first_action_difference": first_action,
        "first_shop_observed": first_shop,
        "observations_equal_at_action_difference": (
            None if index is None else ar[index]["observation"] == br[index]["observation"]),
        "visible_at_action_difference": None if index is None else ar[index]["summary"],
        "action_a": None if index is None else ar[index]["action"],
        "action_b": None if index is None else br[index]["action"],
        "reward_a": a["rewards"],
        "reward_b": b["rewards"],
        "statuses_a": a["statuses"],
        "statuses_b": b["statuses"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=Path, required=True)
    parser.add_argument("--b", type=Path, required=True)
    parser.add_argument("--opponent", type=Path, required=True)
    parser.add_argument("--seeds", required=True, help="comma-separated integer seeds")
    parser.add_argument("--seats", default="0,1")
    parser.add_argument("--capture-steps", type=int, default=96)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    paths = [p.resolve() for p in (args.a, args.b, args.opponent)]
    for path in paths:
        compile(path.read_bytes(), str(path), "exec")
    rows = []
    for seed in [int(v) for v in args.seeds.split(",")]:
        for seat in [int(v) for v in args.seats.split(",")]:
            left = run(paths[0], paths[2], seed, seat, args.capture_steps)
            right = run(paths[1], paths[2], seed, seat, args.capture_steps)
            rows.append(compare(left, right, seed, seat))
    payload = {
        "schema": 1,
        "diagnostic_only": True,
        "sources": {
            "a": {"path": str(paths[0]), "sha256": digest(paths[0].read_bytes())},
            "b": {"path": str(paths[1]), "sha256": digest(paths[1].read_bytes())},
            "opponent": {"path": str(paths[2]), "sha256": digest(paths[2].read_bytes())},
        },
        "engine": "kaggle-environments 1.32.7 pinned by project environment",
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(args.out),
        "rows": len(rows),
        "first_actions": [row["first_action_difference"] for row in rows],
        "first_shops": [row["first_shop_observed"] for row in rows],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
