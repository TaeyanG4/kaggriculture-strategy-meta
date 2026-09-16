"""Lightweight local arena for fast agent iteration.

Runs seeded Kaggriculture matches between two agent files (both seats),
in parallel subprocesses, and prints W/L/T, margins and per-step timing.

Usage:
  .venv/Scripts/python.exe tools/o_arena.py agent/o001_demand_planner.py agent/c129_feed_liquidity.py --seeds 8 --workers 8
  .venv/Scripts/python.exe tools/o_arena.py A.py B.py --seed-list 1,2,3 --seat 0
  .venv/Scripts/python.exe tools/o_arena.py A.py B.py --seeds 4 --dump-dir state/o_dev/replays

Notes: this is a development harness, NOT the frozen validation league.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_agent(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("agent_" + os.path.basename(path).replace(".py", "").replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Kaggle picks the last callable defined; use `agent` if present.
    fn = getattr(mod, "agent", None)
    if fn is None:
        cands = [v for v in vars(mod).values() if callable(v)]
        fn = cands[-1]
    return fn, mod


def run_one(a_path, b_path, seed, seat, dump_dir=None):
    """Run a single match in-process. Candidate A at `seat`."""
    from kaggle_environments import make
    a_fn, a_mod = _load_agent(a_path)
    b_fn, b_mod = _load_agent(b_path)
    timings = {0: [], 1: []}

    def wrap(fn, who):
        def inner(obs, cfg=None):
            t0 = time.perf_counter()
            try:
                out = fn(obs, cfg) if cfg is not None else fn(obs)
            except TypeError:
                out = fn(obs)
            timings[who].append(time.perf_counter() - t0)
            return out
        return inner

    agents = [None, None]
    agents[seat] = wrap(a_fn, seat)
    agents[1 - seat] = wrap(b_fn, 1 - seat)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": int(seed)}, debug=False)
    env.run(agents)
    final = env.steps[-1]
    rewards = [s.reward for s in final]
    statuses = [s.status for s in final]
    tel = {}
    try:
        brains = getattr(a_mod, "_BRAINS", {})
        b = brains.get(seat)
        if b is not None:
            tel = dict(b.telemetry)
        # overlay-style agents expose agent.telemetry (scalars only); keep it for policy compilers
        at = getattr(a_fn, "telemetry", None)
        if isinstance(at, dict):
            tel.update({k: v for k, v in at.items() if isinstance(v, (int, float, str, bool))})
    except Exception:
        pass
    if dump_dir:
        os.makedirs(dump_dir, exist_ok=True)
        with open(os.path.join(dump_dir, f"seed{seed}_seat{seat}.json"), "w", encoding="utf-8") as f:
            json.dump(env.toJSON(), f)
    ra = rewards[seat]
    rb = rewards[1 - seat]
    return {
        "seed": seed, "seat": seat, "rewards": rewards, "statuses": statuses,
        "a": ra, "b": rb, "margin": (ra or 0) - (rb or 0),
        "outcome": "win" if (ra or 0) > (rb or 0) else ("loss" if (ra or 0) < (rb or 0) else "tie"),
        "a_max_s": max(timings[seat]) if timings[seat] else 0, "a_mean_s": sum(timings[seat]) / max(1, len(timings[seat])),
        "b_max_s": max(timings[1 - seat]) if timings[1 - seat] else 0,
        "shops": env.steps[-1][0].observation["town"]["unlocked_shops"],
        "telemetry": tel,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed-list", type=str, default=None)
    ap.add_argument("--seed-base", type=int, default=1000)
    ap.add_argument("--seat", type=int, default=None, help="only this seat for A (default both)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dump-dir", type=str, default=None)
    ap.add_argument("--json-out", type=str, default=None)
    ap.add_argument("--_one", type=str, default=None)
    args = ap.parse_args()

    if args._one:
        job = json.loads(args._one)
        try:
            res = run_one(job["a"], job["b"], job["seed"], job["seat"], job.get("dump_dir"))
        except Exception as exc:
            res = {"seed": job["seed"], "seat": job["seat"], "error": repr(exc), "outcome": "error", "margin": 0, "a": None, "b": None}
        print("RESULT " + json.dumps(res))
        return

    seeds = [int(s) for s in args.seed_list.split(",")] if args.seed_list else [args.seed_base + i for i in range(args.seeds)]
    seats = [args.seat] if args.seat is not None else [0, 1]
    jobs = [{"a": args.a, "b": args.b, "seed": s, "seat": st, "dump_dir": args.dump_dir} for s in seeds for st in seats]
    results = []
    t0 = time.time()
    done = 0

    def run_job(job):
        cmd = [sys.executable, os.path.abspath(__file__), job["a"], job["b"], "--_one", json.dumps(job)]
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=900)
        for line in p.stdout.splitlines():
            if line.startswith("RESULT "):
                return json.loads(line[7:])
        return {"seed": job["seed"], "seat": job["seat"], "error": (p.stderr or p.stdout)[-2000:], "outcome": "error", "margin": 0, "a": None, "b": None}

    with ThreadPoolExecutor(max_workers=max(1, min(8, args.workers))) as ex:
        futs = [ex.submit(run_job, j) for j in jobs]
        for f in as_completed(futs):
            r = f.result()
            results.append(r)
            done += 1
            el = time.time() - t0
            eta = el / done * (len(jobs) - done)
            print(f"[{done}/{len(jobs)} {100*done/len(jobs):.0f}% {el:.0f}s eta {eta:.0f}s] seed={r['seed']} seat={r['seat']} {r['outcome']:5s} margin={r.get('margin',0):8.0f} A={r.get('a')} B={r.get('b')} a_max={r.get('a_max_s',0):.3f}s shops={r.get('shops')}", flush=True)
            if r.get("error"):
                print("   ERROR:", str(r["error"])[:600])
            if r.get("telemetry", {}).get("errors"):
                print("   A telemetry errors:", r["telemetry"].get("errors"), r["telemetry"].get("last_error"))

    results.sort(key=lambda r: (r["seed"], r["seat"]))
    wins = sum(1 for r in results if r["outcome"] == "win")
    losses = sum(1 for r in results if r["outcome"] == "loss")
    ties = sum(1 for r in results if r["outcome"] == "tie")
    errs = sum(1 for r in results if r["outcome"] == "error")
    valid = [r for r in results if r["outcome"] in ("win", "loss", "tie")]
    mean_margin = sum(r["margin"] for r in valid) / max(1, len(valid))
    mean_a = sum(r["a"] for r in valid) / max(1, len(valid))
    mean_b = sum(r["b"] for r in valid) / max(1, len(valid))
    print("=" * 80)
    print(f"A={os.path.basename(args.a)}  B={os.path.basename(args.b)}")
    print(f"W/L/T/E = {wins}/{losses}/{ties}/{errs}   mean margin {mean_margin:+.0f}   mean cash A {mean_a:.0f}  B {mean_b:.0f}")
    print(f"worst margin {min((r['margin'] for r in valid), default=0):+.0f}   best {max((r['margin'] for r in valid), default=0):+.0f}   A max step time {max((r.get('a_max_s',0) for r in valid), default=0):.3f}s")
    if args.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"a": args.a, "b": args.b, "results": results}, f, indent=1)


if __name__ == "__main__":
    main()
