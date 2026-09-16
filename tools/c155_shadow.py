"""c155 shadow diagnostics over RECORDED replays (no engine, no game execution).

Loads the built candidate module (so its evaluate_feed_skip and the parent's price replica are
the real ones), then replays each recorded observation/action pair of a chosen seat through
_c155_evaluate_turn, printing every gate decision with its economic terms. The recorded action
is treated as the parent's proposal (valid when the recorded agent is c129/c150-behaviour).

Usage:
  python tools/c155_shadow.py --candidate agent/c155_milk_externality.py --replay <replay.json> --team Taeyang
  python tools/c155_shadow.py --candidate agent/c155_milk_externality.py --replay-dir o_replays/elite_losses --team Taeyang --summary
"""
import argparse
import collections
import glob
import importlib.util
import json
import os
import sys


def load_module(path):
    spec = importlib.util.spec_from_file_location("c155_shadow_candidate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shadow_one(mod, replay, seat, verbose):
    steps = replay["steps"]
    prices = []
    counts = collections.Counter()
    sums = collections.Counter()
    for t in range(0, len(steps) - 1):
        obs = steps[t][seat]["observation"]
        obs = dict(obs); obs["player"] = seat
        if "step" not in obs:
            obs["step"] = t
        step = int(obs["step"])
        prices.append((step, obs["market"]["prices"]["MILK"]))
        prices = [r for r in prices if r[0] >= step - 23]
        if not (mod._C155_WINDOW[0] <= step < mod._C155_WINDOW[1]):
            continue
        parent_action = steps[t + 1][seat].get("action") or {}
        recent = max(p for _, p in prices) if len(prices) == 24 else None
        decisions, committed = mod._c155_evaluate_turn(obs, parent_action, recent)
        for ev in decisions:
            counts["reviewed"] += 1
            counts["allow" if ev["allow_skip"] else "blocked:" + ev["reason"]] += 1
            if ev["allow_skip"]:
                sums["wheat_saved"] += ev["wheat_saved_value"]; sums["own_loss"] += ev["own_production_loss"]; sums["opp_gain"] += ev["opponent_price_gain"]
            if verbose:
                print(f"  step {step:3d} actor {ev['actor']:2d} tile ({ev['x']},{ev['y']}) {'ALLOW' if ev['allow_skip'] else 'block/' + ev['reason']:22s} "
                      f"gain {ev['estimated_relative_gain']:+6.1f} = wheat {ev['wheat_saved_value']:.1f} - loss {ev['own_production_loss']:.1f} "
                      f"- opp {ev['opponent_price_gain']:.1f} (dp {ev['delta_p']:.0f} x ready {ev['rival_ready']} due {ev['rival_due']}) - buf {ev['uncertainty_buffer']:.0f}")
        counts["max_committed_turn"] = max(counts["max_committed_turn"], committed)
    return counts, sums


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--replay")
    ap.add_argument("--replay-dir")
    ap.add_argument("--team", default="Taeyang")
    ap.add_argument("--seat", type=int)
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    mod = load_module(a.candidate)
    paths = [a.replay] if a.replay else sorted(glob.glob(os.path.join(a.replay_dir, "*.json")))
    total = collections.Counter(); tsum = collections.Counter(); n = 0
    for p in paths:
        try:
            replay = json.load(open(p, encoding="utf-8"))
            names = replay["info"]["TeamNames"]
        except Exception:
            continue
        seat = a.seat if a.seat is not None else (names.index(a.team) if a.team in names else None)
        if seat is None:
            continue
        n += 1
        if not a.summary:
            print(f"== {os.path.basename(p)} seat {seat} ({names[seat]} vs {names[1-seat]})")
        counts, sums = shadow_one(mod, replay, seat, verbose=not a.summary)
        total.update(counts); tsum.update(sums)
        if not a.summary:
            print("   ", dict(counts), {k: round(v, 1) for k, v in sums.items()})
    print(f"replays {n}: {dict(total)} sums {dict((k, round(v, 1)) for k, v in tsum.items())}")


if __name__ == "__main__":
    main()
