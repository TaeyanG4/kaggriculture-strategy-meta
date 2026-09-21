"""Find the first counterfactual action divergence on the parent's live path.

Both policies receive separate deep copies of the same public observation.  The
parent action is executed until they differ, so no future information enters the
reported decision point.  Games stop at that point and are diagnostic only.
"""
from __future__ import annotations

import argparse
import concurrent.futures
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


def canon(value):
    return json.loads(json.dumps(value, sort_keys=True, separators=(",", ":")))


def load(path):
    return build_agent(str(path), {}, "kaggriculture")[0]


def one(job):
    a_path, b_path, opponent_path, opponent_name, seed, seat, limit = job
    a, b, rival = load(a_path), load(b_path), load(opponent_path)
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=False)
    env.reset(2)
    cfg = env.configuration
    while not env.done and int(env.state[0].observation.step) < limit:
        step = int(env.state[0].observation.step)
        view = fastgame.view(env.state, seat)
        av = a(copy.deepcopy(view), cfg)
        bv = b(copy.deepcopy(view), cfg)
        if canon(av) != canon(bv):
            obs = canon(dict(view))
            obs.pop("remainingOverageTime", None)
            return {"opponent": opponent_name, "seed": seed, "seat": seat,
                    "step": step, "shops": list(view.town["unlocked_shops"]),
                    "own_money": view.farms[seat]["money"],
                    "rival_money": view.farms[1-seat]["money"],
                    "action_a": canon(av), "action_b": canon(bv),
                    "observation_sha256": hashlib.sha256(json.dumps(
                        obs, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}
        rival_view = fastgame.view(env.state, 1-seat)
        rv = rival(copy.deepcopy(rival_view), cfg)
        actions = [None, None]
        actions[seat] = bv
        actions[1-seat] = rv
        fastgame.step_direct(env, actions)
    return {"opponent": opponent_name, "seed": seed, "seat": seat, "step": None}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--a", type=Path, required=True)
    p.add_argument("--b", type=Path, required=True)
    p.add_argument("--opponents", type=Path, required=True,
                   help="JSON object label -> source path")
    p.add_argument("--seeds", required=True)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--limit", type=int, default=719)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    opponents = json.loads(args.opponents.read_text(encoding="utf-8"))
    seeds = [int(v) for v in args.seeds.split(",")]
    jobs = [(str(args.a.resolve()), str(args.b.resolve()), str(Path(path).resolve()), name,
             seed, seat, args.limit)
            for name, path in opponents.items() for seed in seeds for seat in (0, 1)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(one, jobs))
    payload = {"schema": 1, "diagnostic_only": True, "rows": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    by = {}
    for name in opponents:
        by[name] = [r["step"] for r in rows if r["opponent"] == name]
    print(json.dumps({"out": str(args.out), "rows": len(rows), "steps": by}, ensure_ascii=False))


if __name__ == "__main__":
    main()
