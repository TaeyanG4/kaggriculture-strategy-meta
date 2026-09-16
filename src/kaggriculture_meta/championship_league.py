"""Championship native league with both-player health qualification.

Each match runs in a fresh, bounded subprocess. Policies use Kaggle's actual
Python source loader. This is a benchmark runner, not a security sandbox.
Native games and fixed-shop/frozen-opponent diagnostics are never pooled.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import random
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = 2
WORKER_MODULE = "src.kaggriculture_meta.championship_league"


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else
                          json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def telemetry_snapshot(value):
    """Preserve nested numeric counters instead of silently dropping them."""
    if isinstance(value, dict):
        return {str(k): telemetry_snapshot(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [telemetry_snapshot(v) for v in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    return "<" + type(value).__name__ + ">"


def positive_error_counters(value, prefix=""):
    found = {}
    if isinstance(value, dict):
        for key, child in value.items():
            path = prefix + "." + str(key) if prefix else str(key)
            found.update(positive_error_counters(child, path))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            found.update(positive_error_counters(child, prefix + f"[{index}]"))
    elif "error" in prefix.lower() and isinstance(value, (int, float)) and value > 0:
        found[prefix] = value
    return found


def health_failures(row):
    reasons = []
    for role in ("candidate", "opponent"):
        counts = positive_error_counters(row.get(role + "_telemetry", {}))
        reasons.extend(role + "_internal_error:" + key for key in sorted(counts))
        if row.get(role + "_timing", {}).get("over_1s", 0):
            reasons.append(role + "_over_one_second")
    return reasons


def require_valid(rows, expected):
    """Promotion rejects a complete winning game if either policy malfunctioned."""
    if len(rows) != expected or any(not r.get("valid") for r in rows):
        raise ValueError("Incomplete or invalid championship evaluation")
    ids = [r["match_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate championship evaluation rows")
    for row in rows:
        if "opponent_telemetry" not in row or "opponent_timing" not in row:
            raise ValueError("Opponent health evidence missing; old harness is not qualified")
        reasons = health_failures(row)
        if reasons:
            raise ValueError("Unhealthy match " + str(row["match_id"]) + ": " + ", ".join(reasons))


def engine_identity():
    dist = importlib.metadata.distribution("kaggle-environments")
    files = ["core.py", "agent.py", "utils.py", "envs/kaggriculture/kaggriculture.py",
             "envs/kaggriculture/kaggriculture.json"]
    return {"version": dist.version, "python": sys.version,
            "files": {p: digest(Path(dist.locate_file("kaggle_environments/" + p)).read_bytes())
                      for p in files}}


def validate_splits(splits):
    if set(splits) != {"train", "selection", "holdout"}:
        raise ValueError("Require train, selection and holdout seed lists")
    seen = set()
    for name, seeds in splits.items():
        if not seeds or any(type(s) is not int or s < 0 for s in seeds):
            raise ValueError(f"Invalid {name} seeds")
        if len(seeds) != len(set(seeds)) or seen.intersection(seeds):
            raise ValueError("Seed leakage or duplicates between splits")
        seen.update(seeds)


def frozen_source(path, out):
    path = Path(path).resolve()
    content = path.read_bytes()
    sha = digest(content)
    target = out / "sources" / (sha + ".py")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_bytes() != content:
        raise ValueError("Source snapshot corruption")
    if not target.exists():
        target.write_bytes(content)
    return {"sha256": sha, "source": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name,
            "path": str(target.resolve())}


def prepare(plan, candidate, stage, out, seed_limit=None):
    validate_splits(plan["splits"])
    if seed_limit is not None and seed_limit <= 0:
        raise ValueError("Seed limit must be positive")
    if seed_limit and stage != "train":
        raise ValueError("Partial seed screens are allowed only in train")
    candidate = frozen_source(candidate, out)
    seen, opponents, aliases = set(), [], []
    for item in plan["opponents"]:
        source = frozen_source(ROOT / item["path"], out)
        if source["sha256"] in seen:
            aliases.append({"name": item["name"], "sha256": source["sha256"]})
            continue
        if source["sha256"] == candidate["sha256"] and not plan.get("allow_mirror", False):
            aliases.append({"name": item["name"], "reason": "identical_to_candidate"})
            continue
        seen.add(source["sha256"])
        opponents.append(dict(source, name=item["name"], family=item["family"]))
    if not opponents:
        raise ValueError("No distinct reacting opponents")
    identity = {"schema": SCHEMA, "engine": engine_identity(), "plan_sha256": digest(plan),
                "harness_sha256": digest(Path(__file__).read_bytes()), "stage": stage,
                "seed_limit": seed_limit, "candidate": candidate, "opponents": opponents,
                "deduplicated": aliases, "mode": "native_reacting",
                "configuration": plan.get("configuration", {"episodeSteps": 720})}
    jobs = []
    for seed in plan["splits"][stage][:seed_limit]:
        for opponent in opponents:
            for seat in (0, 1):
                job = dict(identity, seed=seed, candidate_seat=seat, opponent=opponent)
                job["match_id"] = digest(job)[:24]
                jobs.append(job)
    return identity, jobs


def read_journal(path):
    """Recover only an incomplete final write; reject every other corruption."""
    path = Path(path)
    if not path.exists():
        return []
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    rows, offset, seen = [], 0, set()
    for index, line in enumerate(lines):
        try:
            row = json.loads(line)
        except (ValueError, UnicodeDecodeError):
            if index == len(lines) - 1 and not line.endswith(b"\n"):
                with path.open("r+b") as stream:
                    stream.truncate(offset)
                break
            raise ValueError("Corrupt result journal") from None
        if row["match_id"] in seen:
            raise ValueError("Duplicate match in result journal")
        seen.add(row["match_id"])
        rows.append(row)
        offset += len(line)
    if rows and path.read_bytes() and not path.read_bytes().endswith(b"\n"):
        with path.open("ab") as stream:
            stream.write(b"\n")
    return rows


def aggregate(rows):
    good = [r for r in rows if r.get("valid")]
    outcomes = Counter(r["outcome"] for r in good)
    by_seed = defaultdict(list)
    for r in good:
        by_seed[r["seed"]].append(1.0 if r["margin"] > 0 else .5 if r["margin"] == 0 else 0.0)
    clusters = [statistics.mean(v) for v in by_seed.values()]
    interval = None
    # All wins/ties would otherwise misleadingly return a zero-width interval.
    if len(clusters) >= 2 and len(set(clusters)) > 1:
        rng = random.Random(81023)
        draws = sorted(statistics.mean(rng.choices(clusters, k=len(clusters))) for _ in range(2000))
        interval = [draws[49], draws[1949]]
    return {"games": len(rows), "valid_games": len(good), "failures": len(rows) - len(good),
            "wins": outcomes["win"], "losses": outcomes["loss"], "ties": outcomes["tie"],
            "score_rate_ties_half": statistics.mean(clusters) if clusters else None,
            "seed_clusters": len(clusters), "seed_cluster_bootstrap_95": interval,
            "bootstrap_note": "Unavailable with fewer than two seeds or no between-seed variation; not a guarantee of unseen performance",
            "mean_margin": statistics.mean(r["margin"] for r in good) if good else None,
            "worst_margin": min((r["margin"] for r in good), default=None),
            "max_action_seconds": max((r.get("candidate_timing", {}).get("max", 0) for r in rows), default=0),
            "over_one_second_calls": sum(r.get("candidate_timing", {}).get("over_1s", 0) for r in rows)}


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["mode"]].append(row)
    result = {}
    for mode, matches in groups.items():
        result[mode] = {"overall": aggregate(matches),
            "by_opponent": {name: aggregate([r for r in matches if r["opponent_name"] == name])
                            for name in sorted({r["opponent_name"] for r in matches})},
            "by_family": {name: aggregate([r for r in matches if r["opponent_family"] == name])
                          for name in sorted({r["opponent_family"] for r in matches})},
            "by_seat": {str(s): aggregate([r for r in matches if r["candidate_seat"] == s]) for s in (0, 1)}}
    return result


def timed_policy(source, tag, timings, errors, hashes, telemetry):
    # build_agent is also used by env.run("main.py"); it chooses the LAST callable.
    from kaggle_environments.agent import build_agent
    policy, _ = build_agent(source, {}, "kaggriculture")

    def act(obs, config):
        if config.get("seed") is not None or "seed" in obs or "opponent_private" in obs:
            raise ValueError("Hidden-state boundary violation")
        started = time.perf_counter()
        try:
            action = policy(obs, config)
            hashes.update(json.dumps(action, sort_keys=True, separators=(",", ":")).encode())
            return action
        except Exception as exc:
            errors.append({"step": int(obs["step"]), "type": type(exc).__name__, "message": str(exc)[:300]})
            raise
        finally:
            timings.append(time.perf_counter() - started)
            if int(obs["step"]) == 718:
                # Official lazy loader keeps the exported callable in its closure.
                for cell in policy.__closure__ or ():
                    value = cell.cell_contents
                    if callable(value) and hasattr(value, "telemetry"):
                        telemetry.update(telemetry_snapshot(value.telemetry))
    return act


def timing(values):
    ordered = sorted(values)
    return {"calls": len(values), "max": max(values, default=0),
            "p99": ordered[min(len(ordered) - 1, math.floor(.99 * len(ordered)))] if ordered else 0,
            "total": sum(values), "over_1s": sum(v > 1 for v in values)}


def run_match(job):
    from kaggle_environments import make
    if engine_identity() != job["engine"]:
        raise ValueError("Engine changed after planning")
    for source in (job["candidate"], job["opponent"]):
        if digest(Path(source["path"]).read_bytes()) != source["sha256"]:
            raise ValueError("Policy changed after planning")
    started = time.perf_counter()
    seat = job["candidate_seat"]
    counters = [([], [], hashlib.sha256(), {}) for _ in range(2)]
    agents = [None, None]
    agents[seat] = timed_policy(job["candidate"]["path"], "candidate", *counters[seat])
    agents[1 - seat] = timed_policy(job["opponent"]["path"], "opponent", *counters[1 - seat])
    config = dict(job["configuration"], seed=job["seed"])
    env = make("kaggriculture", configuration=config, debug=False)
    env.run(agents)
    final = env.steps[-1]
    rewards = [s.reward for s in final]
    statuses = [s.status for s in final]
    valid = (statuses == ["DONE", "DONE"] and len(env.steps) == 720
             and all(len(c[0]) == 719 and not c[1] for c in counters)
             and env.info.get("seed") == job["seed"] and all(isinstance(v, (int, float)) for v in rewards))
    margin = rewards[seat] - rewards[1 - seat] if all(isinstance(v, (int, float)) for v in rewards) else None
    checkpoints = []
    for step in [24, 48, 72, 144, 288, 432, 576, 648, 719]:
        if step >= len(env.steps):
            continue
        observation = env.steps[step][seat].observation
        farm = observation.farms[seat]
        counts = Counter(t.get("crop") or t.get("animal") or t.get("kind")
                         for row in farm["tiles"] for t in row if isinstance(t, dict))
        checkpoints.append({"step": step, "cash": farm["money"], "tiles": dict(counts),
                            "shed": dict(observation.private["shed"]),
                            "shops": list(observation.town["unlocked_shops"])})
    result = {"match_id": job["match_id"], "mode": job["mode"], "stage": job["stage"],
            "seed": job["seed"], "resolved_seed": env.info.get("seed"), "candidate_seat": seat,
            "candidate_sha256": job["candidate"]["sha256"], "opponent_sha256": job["opponent"]["sha256"],
            "opponent_name": job["opponent"]["name"], "opponent_family": job["opponent"]["family"],
            "rewards": rewards, "statuses": statuses, "valid": valid, "states": len(env.steps),
            "margin": margin, "outcome": "invalid" if not valid else "win" if margin > 0 else "loss" if margin < 0 else "tie",
            "seconds": time.perf_counter() - started,
            "candidate_timing": timing(counters[seat][0]), "opponent_timing": timing(counters[1 - seat][0]),
            "errors": [c[1] for c in counters], "action_hashes": [c[2].hexdigest() for c in counters],
            "candidate_telemetry": counters[seat][3], "opponent_telemetry": counters[1-seat][3],
            "checkpoints": checkpoints,
            "shops": list(final[0].observation.town["unlocked_shops"])}
    result["health_failures"] = health_failures(result)
    if result["health_failures"]:
        result.update(valid=False, outcome="invalid")
    return result


def run_jobs(identity, jobs, out, workers=4, timeout=90):
    if workers < 1 or workers > 8 or timeout <= 0:
        raise ValueError("Require 1..8 workers and positive timeout")
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / "manifest.json"
    if manifest.exists() and json.loads(manifest.read_text(encoding="utf-8")) != identity:
        raise ValueError("Resume refused: source, engine, harness, stage or plan changed; use a new output directory")
    write_json(manifest, identity)
    rows = read_journal(out / "matches.jsonl")
    ids = {j["match_id"] for j in jobs}
    if any(r["match_id"] not in ids for r in rows):
        raise ValueError("Unexpected match in journal")
    completed = {r["match_id"] for r in rows}
    pending = [j for j in jobs if j["match_id"] not in completed]
    active = []
    last_status = time.monotonic()
    try:
        with (out / "matches.jsonl").open("a", encoding="utf-8") as journal:
            while pending or active:
                while pending and len(active) < workers:
                    job = pending.pop(0)
                    target = out / "jobs" / (job["match_id"] + ".json")
                    write_json(target, job)
                    log = target.with_suffix(".log").open("w", encoding="utf-8")
                    process = subprocess.Popen([sys.executable, "-m", WORKER_MODULE,
                                                "_worker", "--job", str(target.resolve())], cwd=ROOT,
                                               stdout=log, stderr=log)
                    active.append((process, time.monotonic(), job, target, log))
                for entry in list(active):
                    process, launched, job, target, log = entry
                    timed_out = time.monotonic() - launched > timeout
                    if process.poll() is None and not timed_out:
                        continue
                    if process.poll() is None:
                        process.kill()
                    process.wait()
                    log.close()
                    result = target.with_suffix(".result.json")
                    if result.exists() and not timed_out and process.returncode == 0:
                        row = json.loads(result.read_text(encoding="utf-8"))
                    else:
                        row = {"match_id": job["match_id"], "mode": job["mode"], "stage": job["stage"],
                               "seed": job["seed"], "candidate_seat": job["candidate_seat"],
                               "opponent_name": job["opponent"]["name"], "opponent_family": job["opponent"]["family"],
                               "valid": False, "error": "wall_timeout" if timed_out else "worker_failed",
                               "exit_code": process.returncode}
                    journal.write(json.dumps(row, ensure_ascii=False) + "\n")
                    journal.flush()
                    rows.append(row)
                    active.remove(entry)
                    print(f"{len(rows)}/{len(jobs)} {row['opponent_name']} seed={row['seed']} "
                          f"seat={row['candidate_seat']} {row.get('outcome', row.get('error'))} "
                          f"margin={row.get('margin')}", flush=True)
                if time.monotonic() - last_status >= 30:
                    write_json(out / "summary.json", summarize(rows))
                    last_status = time.monotonic()
                if active:
                    time.sleep(.1)
    finally:
        for process, _, _, _, log in active:
            if process.poll() is None:
                process.kill()
            process.wait()
            log.close()
    result = summarize(rows)
    write_json(out / "summary.json", result)
    require_valid(rows, len(jobs))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--plan", type=Path, required=True)
    run.add_argument("--candidate", type=Path, required=True)
    run.add_argument("--stage", choices=("train", "selection", "holdout"), required=True)
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--workers", type=int, default=4, choices=range(1, 9))
    run.add_argument("--timeout", type=float, default=90)
    run.add_argument("--seed-limit", type=int)
    worker = sub.add_parser("_worker")
    worker.add_argument("--job", type=Path, required=True)
    args = ap.parse_args()
    if args.command == "_worker":
        job = json.loads(args.job.read_text(encoding="utf-8"))
        write_json(args.job.with_suffix(".result.json"), run_match(job))
    else:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        identity, jobs = prepare(plan, args.candidate, args.stage, args.out.resolve(), args.seed_limit)
        print(json.dumps(run_jobs(identity, jobs, args.out.resolve(), args.workers, args.timeout), indent=2))


if __name__ == "__main__":
    main()
