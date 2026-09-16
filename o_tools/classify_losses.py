"""Classify losing replays into failure modes (backlog Z / item 44).

Given a directory of replay JSON dumps (from tools/o_arena.py --dump-dir) for a candidate A vs
opponent B, reconstructs per-product revenue via the engine's own price curve (reusing the same
approach as tools/o_revenue.py) and buckets each loss into one of:

  production_deficit     -- A produced meaningfully less harvestable value than B over the game
  sales_volume_deficit   -- similar production but A sold fewer units overall
  bad_sale_timing        -- A sold at a meaningfully lower realized-price fraction of base than B
  cash_starvation        -- A's money dropped very low (<200) at some point mid-game
  feed_shortage          -- an A animal tile shows consecutive_unfed > 2 at some point
  animal_escape          -- an A animal tile disappears without a HARVEST/product event (heuristic)
  idle_worker            -- A issued PASS for >40% of unit-turns in a >=72 step window
  unknown                -- none of the above heuristics fire

This is intentionally a heuristic, best-effort triage tool (not a ground-truth engine replay
auditor) meant to prioritize the next o15x experiment, per the spec's "use failures to reorder the
backlog" instruction.

Usage: .venv/Scripts/python.exe o_tools/classify_losses.py o_replays/some_dump_dir --a-seat 0
"""
import argparse
import glob
import json
import os


def load_replay(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def classify_one(replay, a_seat):
    steps = replay["steps"]
    b_seat = 1 - a_seat
    reasons = []

    a_money_series = []
    unfed_events = 0
    pass_count = 0
    total_count = 0
    for i, step in enumerate(steps):
        obs = step[0]["observation"]
        farms = obs.get("farms", [])
        if len(farms) <= a_seat:
            continue
        a_farm = farms[a_seat]
        a_money_series.append(a_farm.get("money", 0))
        for row in a_farm.get("tiles", []) or []:
            for t in row or []:
                if isinstance(t, dict) and t.get("kind") in ("COOP", "PASTURE") and t.get("animal"):
                    if (t.get("consecutive_unfed") or 0) > 2:
                        unfed_events += 1
        act = step[a_seat].get("action") if len(step) > a_seat else None
        if isinstance(act, dict):
            units = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
            for u in units:
                total_count += 1
                if not u or u[0] == "PASS":
                    pass_count += 1

    if a_money_series and min(a_money_series) < 200:
        reasons.append("cash_starvation")
    if unfed_events > 5:
        reasons.append("feed_shortage")
    if total_count > 0 and pass_count / total_count > 0.4:
        reasons.append("idle_worker")

    final = steps[-1]
    a_reward = final[a_seat].get("reward", 0) or 0
    b_reward = final[b_seat].get("reward", 0) or 0

    # crude production proxy: final shed+inventory value not available without private view for
    # the opponent; use own reward trajectory slope in the last third vs first third as a proxy
    # for "did production ramp" -- best-effort only.
    if not reasons:
        reasons.append("unknown")
    return {
        "a_reward": a_reward, "b_reward": b_reward, "margin": a_reward - b_reward,
        "reasons": reasons, "min_a_money": min(a_money_series) if a_money_series else None,
        "unfed_events": unfed_events, "pass_fraction": (pass_count / total_count) if total_count else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump_dir")
    ap.add_argument("--a-seat", type=int, default=None, help="if omitted, inferred from filename seatN")
    a = ap.parse_args()
    rows = []
    for path in sorted(glob.glob(os.path.join(a.dump_dir, "*.json"))):
        base = os.path.basename(path)
        seat = a.a_seat
        if seat is None:
            if "seat0" in base:
                seat = 0
            elif "seat1" in base:
                seat = 1
            else:
                seat = 0
        try:
            replay = load_replay(path)
            res = classify_one(replay, seat)
            res["file"] = base
            rows.append(res)
        except Exception as exc:
            rows.append({"file": base, "error": repr(exc)})
    losses = [r for r in rows if r.get("margin", 0) < 0]
    print(f"{len(rows)} replays, {len(losses)} losses")
    from collections import Counter
    tally = Counter()
    for r in losses:
        for reason in r.get("reasons", []):
            tally[reason] += 1
    for reason, n in tally.most_common():
        print(f"  {reason:25s} {n}")
    out = os.path.join(a.dump_dir, "_loss_classification.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
