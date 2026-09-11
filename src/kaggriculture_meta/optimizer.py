from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import pprint
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from src.kaggriculture_meta.benchmark import summarize_matches


BASE_VARIANT = "base_rita"


def candidate_specs() -> dict[str, dict]:
    """Small epsilon search over the highest-leverage Rancher Rita policy knobs."""
    return {
        BASE_VARIANT: {},
        "hands_7": {"hands": 7},
        "hands_9": {"hands": 9},
        "land_after_6": {"land_after_animals": 6},
        "land_after_14": {"land_after_animals": 14},
        "mix_12cow_4sheep": {"animal_mix": {"COW": 12, "SHEEP": 4}},
        "mix_8cow_8sheep": {"animal_mix": {"COW": 8, "SHEEP": 8}},
        "feed_float_12": {"feed_float_days": 12},
        "feed_float_20": {"feed_float_days": 20},
        "animal_buffer_200": {"animal_buffer": 200},
        "animal_buffer_600": {"animal_buffer": 600},
        "max_wheat_45": {"max_wheat_price": 45},
        "max_wheat_65": {"max_wheat_price": 65},
        "carry_6": {"carry": 6},
        "carry_10": {"carry": 10},
        "sell_chunk_12": {"sell_chunk": 12},
        "sell_chunk_30": {"sell_chunk": 30},
        "shed_pressure_60": {"shed_pressure": 60},
        "shed_pressure_90": {"shed_pressure": 90},
        "liquidate_27": {"liquidate_from_day": 27},
        "liquidate_29": {"liquidate_from_day": 29},
    }


def _load_policy(template: Path) -> dict:
    spec = importlib.util.spec_from_file_location("optimizer_template_agent", template)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load template: {template}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return copy.deepcopy(module.POLICY)


def apply_changes(base_policy: dict, changes: dict) -> dict:
    policy = copy.deepcopy(base_policy)
    for key, value in changes.items():
        if key == "animal_mix":
            policy["animal_target"] = copy.deepcopy(value)
            if policy.get("build"):
                policy["build"][0]["target"] = sum(int(v) for v in value.values())
        else:
            policy[key] = copy.deepcopy(value)
    return policy


def render_agent_source(template_source: str, policy: dict) -> str:
    start = template_source.index("POLICY =")
    marker = "\n\n\n# ---------------------------------------------------------------------------"
    end = template_source.index(marker, start)
    rendered = "POLICY = " + pprint.pformat(policy, width=100, sort_dicts=False)
    return template_source[:start] + rendered + template_source[end:]


def generate_variants(template: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    source = template.read_text(encoding="utf-8")
    base_policy = _load_policy(template)
    paths: dict[str, Path] = {}
    for name, changes in candidate_specs().items():
        policy = apply_changes(base_policy, changes)
        path = output_dir / f"{name}.py"
        path.write_text(render_agent_source(source, policy), encoding="utf-8")
        paths[name] = path.resolve()
    return paths


def _play_task(task: tuple[str, str, int, int]) -> dict:
    candidate, opponent, seed, seat = task
    started = time.perf_counter()
    try:
        from src.kaggriculture_meta.benchmark import run_match

        return run_match(candidate, opponent, seed, seat, False)
    except Exception as exc:  # pragma: no cover - exercised only on engine failures
        return {
            "candidate": candidate,
            "opponent": opponent,
            "seed": seed,
            "candidate_seat": seat,
            "candidate_reward": -1_000_000_000.0,
            "opponent_reward": 0.0,
            "reward_margin": -1_000_000_000.0,
            "outcome": "loss",
            "candidate_status": "ERROR",
            "opponent_status": "UNKNOWN",
            "runtime_seconds": round(time.perf_counter() - started, 6),
            "error": f"{type(exc).__name__}: {exc}",
        }


def _row_key(row: dict) -> tuple[str, str, int, int]:
    return (
        str(row["candidate"]),
        str(row["opponent"]),
        int(row["seed"]),
        int(row["candidate_seat"]),
    )


def run_tasks(tasks: list[tuple[str, str, int, int]], jsonl_path: Path, workers: int) -> list[dict]:
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    done: set[tuple[str, str, int, int]] = set()
    if jsonl_path.exists():
        for line in jsonl_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            rows.append(row)
            done.add(_row_key(row))

    pending = [task for task in tasks if task not in done]
    if not pending:
        return rows

    with jsonl_path.open("a", encoding="utf-8") as f:
        with ProcessPoolExecutor(max_workers=max(1, workers)) as pool:
            future_map = {pool.submit(_play_task, task): task for task in pending}
            completed = 0
            total = len(pending)
            for future in as_completed(future_map):
                row = future.result()
                rows.append(row)
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                completed += 1
                if completed == 1 or completed % 20 == 0 or completed == total:
                    errors = sum(r.get("candidate_status") != "DONE" for r in rows)
                    print(f"progress {completed}/{total} new matches; persisted={len(rows)} errors={errors}", flush=True)
    return rows


def summarize_pool(rows: list[dict], candidate_path: Path, opponent_paths: dict[str, Path]) -> dict:
    selected = [r for r in rows if Path(str(r["candidate"])).resolve() == candidate_path.resolve()]
    if not selected:
        raise ValueError(f"no rows for {candidate_path}")

    overall = summarize_matches(selected, candidate_path.name, "pool")
    by_opponent = {}
    for name, path in opponent_paths.items():
        members = [r for r in selected if Path(str(r["opponent"])).resolve() == path.resolve()]
        if members:
            by_opponent[name] = summarize_matches(members, candidate_path.name, name)

    rates = [v["win_rate_decided"] for v in by_opponent.values() if v["win_rate_decided"] is not None]
    overall["worst_opponent_win_rate"] = min(rates) if rates else None
    overall["worst_matchup"] = (
        min(by_opponent, key=lambda name: (by_opponent[name]["win_rate_decided"], by_opponent[name]["mean_margin"]))
        if by_opponent
        else None
    )
    overall["error_games"] = sum(
        r.get("candidate_status") != "DONE" or r.get("opponent_status") != "DONE" for r in selected
    )
    overall["error_rate"] = round(overall["error_games"] / len(selected), 6)
    overall["by_opponent"] = by_opponent
    return overall


def rank_summaries(summaries: dict[str, dict]) -> list[str]:
    def key(name: str) -> tuple:
        s = summaries[name]
        return (
            -float(s["error_rate"]),
            float(s["win_rate_decided"] or 0.0),
            float(s["worst_opponent_win_rate"] or 0.0),
            float(s["mean_margin"]),
            float(s["median_margin"]),
        )

    return sorted(summaries, key=key, reverse=True)


def _tasks_for(candidates: dict[str, Path], opponents: dict[str, Path], seeds: list[int]) -> list[tuple[str, str, int, int]]:
    return [
        (str(candidate), str(opponent), seed, seat)
        for candidate in candidates.values()
        for opponent in opponents.values()
        for seed in seeds
        for seat in (0, 1)
    ]


def evaluate_stage(
    name: str,
    candidates: dict[str, Path],
    opponents: dict[str, Path],
    seeds: list[int],
    work_dir: Path,
    workers: int,
) -> tuple[dict[str, dict], list[str]]:
    stage_dir = work_dir / name
    rows = run_tasks(_tasks_for(candidates, opponents, seeds), stage_dir / "matches.jsonl", workers)
    summaries = {candidate: summarize_pool(rows, path, opponents) for candidate, path in candidates.items()}
    ranking = rank_summaries(summaries)
    payload = {
        "stage": name,
        "seeds": seeds,
        "opponents": list(opponents),
        "ranking": ranking,
        "summaries": summaries,
    }
    (stage_dir / "summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"{name} ranking: {ranking}", flush=True)
    return summaries, ranking


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", type=Path, required=True)
    ap.add_argument("--opponent-root", type=Path, required=True)
    ap.add_argument("--core-agent", type=Path, required=True)
    ap.add_argument("--work-dir", type=Path, default=Path("state/agent_benchmark/optimizer"))
    ap.add_argument("--workers", type=int, default=max(1, min(8, os.cpu_count() or 1)))
    args = ap.parse_args()

    template = args.template.resolve()
    root = args.opponent_root.resolve()
    core = args.core_agent.resolve()
    work_dir = args.work_dir.resolve()
    variants = generate_variants(template, work_dir / "candidates")

    ref = {
        "rancher_rita": root / "rancher_rita.py",
        "melon_mateo": root / "melon_mateo.py",
        "broker_bea": root / "broker_bea.py",
        "ledger_lena": root / "ledger_lena.py",
        "slotter_silas": root / "slotter_silas.py",
        "closer_cleo": root / "closer_cleo.py",
    }
    for path in [template, core, *ref.values()]:
        if not path.exists():
            raise FileNotFoundError(path)

    _, ranking1 = evaluate_stage(
        "round1",
        variants,
        {k: ref[k] for k in ("rancher_rita", "melon_mateo", "closer_cleo")},
        [20261000, 20261001],
        work_dir,
        args.workers,
    )
    round2_candidates = {name: variants[name] for name in ranking1[:6]}
    _, ranking2 = evaluate_stage(
        "round2",
        round2_candidates,
        ref,
        list(range(20261100, 20261104)),
        work_dir,
        args.workers,
    )
    finalists = ranking2[:3]
    final_candidates = {name: variants[name] for name in dict.fromkeys([BASE_VARIANT, *finalists])}
    final_opponents = {**ref, "core_baseline_v2": core}
    final_summaries, final_ranking = evaluate_stage(
        "round3_final",
        final_candidates,
        final_opponents,
        list(range(20261200, 20261212)),
        work_dir,
        args.workers,
    )

    core_summaries, core_ranking = evaluate_stage(
        "core_check",
        final_candidates,
        {"core_baseline_v2": core},
        list(range(20261300, 20261332)),
        work_dir,
        args.workers,
    )

    best_candidate = final_ranking[0]
    result = {
        "base_variant": BASE_VARIANT,
        "best_candidate": best_candidate,
        "candidate_changes": candidate_specs()[best_candidate],
        "round1_survivors": ranking1[:6],
        "round2_finalists": finalists,
        "final_ranking": final_ranking,
        "core_check_ranking": core_ranking,
        "baseline_final": final_summaries[BASE_VARIANT],
        "candidate_final": final_summaries[best_candidate],
        "baseline_core_check": core_summaries[BASE_VARIANT],
        "candidate_core_check": core_summaries[best_candidate],
    }
    (work_dir / "optimizer_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
