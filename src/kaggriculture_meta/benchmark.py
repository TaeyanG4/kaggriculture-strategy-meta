from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import time
from pathlib import Path


def wilson_interval(wins: float, games: int, z: float = 1.96) -> tuple[float | None, float | None]:
    if games <= 0:
        return None, None
    p = wins / games
    denominator = 1 + z * z / games
    center = (p + z * z / (2 * games)) / denominator
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * games)) / games) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def summarize_matches(rows: list[dict], candidate: str, opponent: str) -> dict:
    decided = [r for r in rows if r["outcome"] in {"win", "loss"}]
    wins = sum(r["outcome"] == "win" for r in decided)
    losses = sum(r["outcome"] == "loss" for r in decided)
    ties = sum(r["outcome"] == "tie" for r in rows)
    low, high = wilson_interval(wins, len(decided))
    margins = [float(r["reward_margin"]) for r in rows]
    seat0 = [r for r in rows if int(r["candidate_seat"]) == 0]
    seat1 = [r for r in rows if int(r["candidate_seat"]) == 1]

    def seat_rate(members: list[dict]) -> float | None:
        d = [r for r in members if r["outcome"] in {"win", "loss"}]
        return sum(r["outcome"] == "win" for r in d) / len(d) if d else None

    return {
        "candidate": candidate,
        "opponent": opponent,
        "games": len(rows),
        "decided_games": len(decided),
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "win_rate_decided": round(wins / len(decided), 4) if decided else None,
        "wilson95_low": round(low, 4) if low is not None else None,
        "wilson95_high": round(high, 4) if high is not None else None,
        "mean_reward": round(statistics.fmean(float(r["candidate_reward"]) for r in rows), 3),
        "mean_opponent_reward": round(statistics.fmean(float(r["opponent_reward"]) for r in rows), 3),
        "mean_margin": round(statistics.fmean(margins), 3),
        "median_margin": round(statistics.median(margins), 3),
        "candidate_seat0_games": len(seat0),
        "candidate_seat1_games": len(seat1),
        "seat0_win_rate_decided": round(seat_rate(seat0), 4) if seat_rate(seat0) is not None else None,
        "seat1_win_rate_decided": round(seat_rate(seat1), 4) if seat_rate(seat1) is not None else None,
        "all_status_done": all(r["candidate_status"] == "DONE" and r["opponent_status"] == "DONE" for r in rows),
        "mean_runtime_seconds": round(statistics.fmean(float(r["runtime_seconds"]) for r in rows), 4),
    }


def run_match(candidate: str, opponent: str, seed: int, candidate_seat: int, debug: bool = False) -> dict:
    from kaggle_environments import make

    agents = [None, None]
    agents[candidate_seat] = candidate
    agents[1 - candidate_seat] = opponent
    started = time.perf_counter()
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=debug)
    env.run(agents)
    runtime = time.perf_counter() - started
    final = env.steps[-1]
    candidate_state = final[candidate_seat]
    opponent_state = final[1 - candidate_seat]
    candidate_reward = float(candidate_state.reward)
    opponent_reward = float(opponent_state.reward)
    margin = candidate_reward - opponent_reward
    outcome = "win" if margin > 0 else "loss" if margin < 0 else "tie"
    return {
        "candidate": candidate,
        "opponent": opponent,
        "seed": seed,
        "candidate_seat": candidate_seat,
        "candidate_reward": candidate_reward,
        "opponent_reward": opponent_reward,
        "reward_margin": margin,
        "outcome": outcome,
        "candidate_status": candidate_state.status,
        "opponent_status": opponent_state.status,
        "runtime_seconds": round(runtime, 6),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True, help="Built-in agent name or path to .py agent")
    ap.add_argument("--opponent", required=True, help="Built-in agent name or path to .py agent")
    ap.add_argument("--seed-start", type=int, default=1000)
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--out-dir", type=Path, default=Path("state/agent_benchmark"))
    ap.add_argument("--label", default="benchmark")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    rows = []
    seeds = list(range(args.seed_start, args.seed_start + args.seeds))
    for index, seed in enumerate(seeds, 1):
        for candidate_seat in (0, 1):
            row = run_match(args.candidate, args.opponent, seed, candidate_seat, args.debug)
            rows.append(row)
            print(
                f"{index}/{len(seeds)} seed={seed} seat={candidate_seat} "
                f"outcome={row['outcome']} margin={row['reward_margin']:.0f}",
                flush=True,
            )

    summary = summarize_matches(rows, args.candidate, args.opponent)
    summary["seed_start"] = args.seed_start
    summary["seed_count"] = args.seeds
    summary["paired_seat_design"] = True
    summary["engine_configuration"] = {"episodeSteps": 720, "seed": "varied by match pair"}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / f"{args.label}_matches.csv", rows)
    (args.out_dir / f"{args.label}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
