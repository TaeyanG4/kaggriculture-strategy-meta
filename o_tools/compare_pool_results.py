"""Compare two o_tournament.py --out directories (same pool, same seeds, different ref agent) and
report the per-opponent margin delta, to see whether a candidate is a net improvement, a net
regression, or mixed across a diverse opponent pool. This is the primary robustness check per the
project's stated goal (paired win rate across a diverse pool > raw money).

Usage: .venv/Scripts/python.exe o_tools/compare_pool_results.py o_results/diverse_vs_c150 o_results/diverse_vs_o157
"""
import argparse
import glob
import json
import os


def load_dir(d):
    out = {}
    for f in glob.glob(os.path.join(d, "*.json")):
        name = os.path.basename(f)[:-5]
        if name == "_summary":
            continue
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        res = [r for r in data.get("results", []) if r.get("outcome") in ("win", "loss", "tie")]
        if not res:
            continue
        w = sum(1 for r in res if r["outcome"] == "win")
        l = sum(1 for r in res if r["outcome"] == "loss")
        mm = sum(r["margin"] for r in res) / len(res)
        out[name] = {"w": w, "l": l, "t": len(res) - w - l, "mean_margin": mm, "n": len(res)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline_dir")
    ap.add_argument("candidate_dir")
    a = ap.parse_args()
    base = load_dir(a.baseline_dir)
    cand = load_dir(a.candidate_dir)
    common = sorted(set(base) & set(cand))
    print(f"{'opponent':55s} {'base_margin':>12s} {'cand_margin':>12s} {'delta':>10s}  note")
    deltas = []
    regressions = []
    improvements = []
    for name in common:
        b = base[name]["mean_margin"]
        c = cand[name]["mean_margin"]
        # margin here is (opponent - ref), so ref improving means margin becomes MORE negative
        delta_for_ref = -(c - b)  # positive = candidate is better for our side than baseline
        deltas.append(delta_for_ref)
        note = ""
        if c > 0 and b <= 0:
            note = "<-- REGRESSION: opponent now WINS on average (baseline: we won)"
            regressions.append((name, b, c))
        elif delta_for_ref < -50:
            note = "<-- notably worse for us"
            regressions.append((name, b, c))
        elif delta_for_ref > 50:
            improvements.append((name, b, c))
        print(f"{name:55s} {b:12.0f} {c:12.0f} {delta_for_ref:10.0f}  {note}")
    only_base = sorted(set(base) - set(cand))
    only_cand = sorted(set(cand) - set(base))
    if only_base:
        print("only in baseline (missing from candidate run):", only_base)
    if only_cand:
        print("only in candidate (missing from baseline run):", only_cand)
    print("=" * 100)
    print(f"opponents compared: {len(common)}")
    print(f"mean delta-for-ref across all: {sum(deltas)/max(1,len(deltas)):+.1f}  "
          f"(positive = candidate better on average)")
    print(f"opponents where candidate is notably WORSE (delta < -50): {len(regressions)}")
    for name, b, c in regressions:
        print(f"   {name}: baseline_margin={b:+.0f} -> candidate_margin={c:+.0f}")
    print(f"opponents where candidate is notably BETTER (delta > +50): {len(improvements)}")
    for name, b, c in improvements:
        print(f"   {name}: baseline_margin={b:+.0f} -> candidate_margin={c:+.0f}")


if __name__ == "__main__":
    main()
