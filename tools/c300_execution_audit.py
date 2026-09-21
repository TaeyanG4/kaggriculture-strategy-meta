"""Independent, uncached differential QA of native and historical fast execution.

Not a strength evaluation. One process per game; frozen agents are read only.
Run with the repository .venv Python. Outputs are immutable per invocation.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import contextlib
import hashlib
import io
import json
import multiprocessing
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
POLICIES = {
    "base19": "state/o_dev/p000_base19.py",
    "v48": "state/o_dev/v48_clearqueue_public.py",
    "o239": "agent/o239_open_roundtrip_50.py",
}


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()


def observation(obs):
    # Wall-clock accounting is expected to differ. All game information remains.
    return {k: v for k, v in obs.items() if k != "remainingOverageTime"}


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def game(job):
    os.chdir(ROOT)
    sys.path[:0] = [str(ROOT), str(ROOT / "o_tools")]
    for key in list(os.environ):
        if key.startswith(("PROXY_", "P002_", "KAGG_O")):
            os.environ.pop(key)
    os.environ["MPLBACKEND"] = "Agg"
    started = time.perf_counter()
    log = io.StringIO()
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        from kaggle_environments import make
        from kaggle_environments.agent import build_agent
        from src.kaggriculture_meta.championship_league import engine_identity
        from proxy_eval import load_agent
        import fastgame

        records = [[], []]
        errors = [[], []]
        mutation_steps = [[], []]
        max_seconds = [0.0, 0.0]
        action_streams = [hashlib.sha256(), hashlib.sha256()]
        paths = [str(ROOT / POLICIES[name]) for name in job["players"]]
        policies = []
        for seat, path in enumerate(paths):
            if job["mode"] == "fast_legacy":
                policy = load_agent(path, f"c300_seat_{seat}")
                arity = policy.__code__.co_argcount
            else:
                policy, _ = build_agent(path, {}, "kaggriculture")
                arity = 2

            def wrap(obs, cfg, seat=seat, policy=policy, arity=arity):
                step = int(obs["step"])
                before = digest(observation(obs))
                began = time.perf_counter()
                try:
                    action = policy(obs) if arity == 1 else policy(obs, cfg)
                except Exception as exc:
                    errors[seat].append({"step": step, "error": repr(exc)})
                    raise
                finally:
                    max_seconds[seat] = max(max_seconds[seat], time.perf_counter() - began)
                after = digest(observation(obs))
                if before != after:
                    mutation_steps[seat].append(step)
                action_streams[seat].update(encode(action))
                records[seat].append({"step": step, "observation": before, "action": digest(action)})
                return action

            # fastgame uses co_argcount; a factory avoids exposing closure defaults.
            def make_two_args(fn):
                def act(obs, cfg):
                    return fn(obs, cfg)
                return act
            policies.append(make_two_args(wrap))

        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": job["seed"]}, debug=False)
        if job["mode"] == "native":
            env.run(policies)
        else:
            fastgame.play(env, policies, deep=True)
        final = [{"reward": s.reward, "status": s.status,
                  "observation": observation(s.observation)} for s in env.state]
        result = dict(job=job, engine=engine_identity(),
                      source_hashes=[hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths],
                      rewards=[s.reward for s in env.state], statuses=[s.status for s in env.state],
                      resolved_seed=env.info.get("seed"), states=len(env.steps),
                      action_hashes=[h.hexdigest() for h in action_streams],
                      final_state_hash=digest(final), records=records, errors=errors,
                      observation_mutations=mutation_steps, max_action_seconds=max_seconds,
                      seconds=time.perf_counter() - started)
        result["valid"] = (result["statuses"] == ["DONE", "DONE"] and result["states"] == 720
                           and all(len(r) == 719 for r in records) and not any(errors)
                           and result["resolved_seed"] == job["seed"])
        result["diagnostic_log_tail"] = log.getvalue()[-2000:]
        return result


def compare(native, other):
    first = []
    for seat in (0, 1):
        mismatch = next(({"seat": seat, "native": a, "other": b}
                         for a, b in zip(native["records"][seat], other["records"][seat]) if a != b), None)
        if mismatch:
            first.append(mismatch)
    same = all(native[k] == other[k] for k in
               ("source_hashes", "engine", "rewards", "statuses", "states", "records", "final_state_hash"))
    return dict(case=native["job"]["case"], mode=other["job"]["mode"],
                identical=same and native["valid"] and other["valid"],
                native_rewards=native["rewards"], other_rewards=other["rewards"],
                first_differences=first,
                mutation_counts=[len(x) for x in other["observation_mutations"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=8, choices=range(1, 9))
    args = ap.parse_args()
    out = args.out.resolve()
    if out.exists():
        raise SystemExit("Use a new output directory; prior evidence is immutable")
    # Shared with the canonical launcher: an open audit handle prevents its
    # exclusive FileShare.None open; byte locking also excludes other audits.
    lock_path = ROOT / "state/agent_experiments/.kaggriculture-global-launch.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock:
        if os.name == "nt":
            import msvcrt
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        out.mkdir(parents=True)
        cases = [("base19", "o239", 7000), ("v48", "o239", 7001), ("base19", "v48", 7001)]
        jobs = []
        for left, right, seed in cases:
            for reverse in (False, True):
                players = [right, left] if reverse else [left, right]
                case = f"{players[0]}_{players[1]}_{seed}"
                for mode in ("native", "fast_official", "fast_legacy"):
                    jobs.append(dict(case=case, players=players, seed=seed, mode=mode))
        support = [Path(__file__), ROOT / "o_tools/fastgame.py", ROOT / "o_tools/proxy_eval.py"]
        write(out / "manifest.json", dict(purpose="QA only; not promotion evidence", workers=args.workers,
              jobs=jobs, support={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in support},
              sources={name: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for name, p in POLICIES.items()}))
        os.environ["PYTHONHASHSEED"] = "0"
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
        results = {}
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn"),
                                 max_tasks_per_child=1) as pool:
            pending = {pool.submit(game, j): j for j in jobs}
            for future in as_completed(pending):
                j = pending[future]
                r = future.result()
                write(out / f"{j['case']}_{j['mode']}.json", r)
                results[j["case"], j["mode"]] = r
                print(json.dumps(dict(done=len(results), total=len(jobs), case=j["case"], mode=j["mode"],
                                      valid=r["valid"], rewards=r["rewards"])), flush=True)
        comparisons = [compare(results[c, "native"], results[c, mode])
                       for c in sorted({j["case"] for j in jobs}) for mode in ("fast_official", "fast_legacy")]
        summary = dict(games=len(results), identical=sum(c["identical"] for c in comparisons),
                       comparisons=comparisons, cpu_proxy_game_seconds=sum(r["seconds"] for r in results.values()),
                       scope="Six native development cases only; no pinned-world or live equivalence claim")
        write(out / "summary.json", summary)
        print(json.dumps({k: v for k, v in summary.items() if k != "comparisons"}), flush=True)


if __name__ == "__main__":
    main()
