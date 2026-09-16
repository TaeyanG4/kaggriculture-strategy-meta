"""Run every agent in a pool against a reference agent with tools/o_arena.py and tabulate.

Usage:
  .venv/Scripts/python.exe tools/o_tournament.py --pool state/o_dev/public_scan/donor_pool.json \
      --ref agent/c129_feed_liquidity.py --seeds 4 --seed-base 5000 --workers 8 --out state/o_dev/tournament/donors_vs_c129
"""
import argparse
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed-base", type=int, default=5000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=None, help="comma-separated subset of pool names")
    a = ap.parse_args()
    pool = json.load(open(a.pool))
    if a.only:
        keep = set(a.only.split(","))
        pool = {k: v for k, v in pool.items() if k in keep}
    os.makedirs(a.out, exist_ok=True)
    rows = []
    t0 = time.time()
    for i, (name, path) in enumerate(pool.items()):
        jf = os.path.join(a.out, name + ".json")
        if not os.path.exists(jf):
            cmd = [sys.executable, os.path.join(ROOT, "tools", "o_arena.py"), path, a.ref, "--seeds", str(a.seeds),
                   "--seed-base", str(a.seed_base), "--workers", str(a.workers), "--json-out", jf]
            env = dict(os.environ, MPLBACKEND="Agg")
            try:
                subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=1800, env=env)
            except subprocess.TimeoutExpired:
                pass
        if not os.path.exists(jf):
            rows.append({"name": name, "error": "no result"})
            print(f"[{i+1}/{len(pool)}] {name}: NO RESULT", flush=True)
            continue
        res = json.load(open(jf))["results"]
        valid = [r for r in res if r["outcome"] in ("win", "loss", "tie")]
        errs = [r for r in res if r["outcome"] == "error"]
        w = sum(1 for r in valid if r["outcome"] == "win")
        l = sum(1 for r in valid if r["outcome"] == "loss")
        mm = sum(r["margin"] for r in valid) / max(1, len(valid))
        ma = sum(r["a"] for r in valid) / max(1, len(valid))
        mx = max((r.get("a_max_s", 0) for r in valid), default=0)
        rows.append({"name": name, "w": w, "l": l, "t": len(valid) - w - l, "errors": len(errs), "mean_margin": mm,
                     "mean_cash": ma, "max_step_s": mx, "err_msg": (errs[0].get("error", "")[:200] if errs else "")})
        print(f"[{i+1}/{len(pool)} {time.time()-t0:.0f}s] {name:55s} W/L/T {w}/{l}/{len(valid)-w-l} err {len(errs)} margin {mm:+8.0f} cash {ma:8.0f} max {mx:.2f}s", flush=True)
    rows.sort(key=lambda r: -r.get("mean_margin", -1e9))
    json.dump(rows, open(os.path.join(a.out, "_summary.json"), "w"), indent=1)
    print("=" * 100)
    for r in rows:
        if "error" in r:
            print(f"{r['name']:55s} {r['error']}")
        else:
            print(f"{r['name']:55s} W/L/T {r['w']}/{r['l']}/{r['t']} err {r['errors']} margin {r['mean_margin']:+8.0f} cash {r['mean_cash']:8.0f}")


if __name__ == "__main__":
    main()
