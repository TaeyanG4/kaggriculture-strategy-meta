"""Per-product realized revenue / cost breakdown for both players from a local replay JSON
(env.toJSON() with private observations, as dumped by tools/o_arena.py --dump-dir).

Sold quantities are derived exactly from shed/inventory deltas; prices are
reconstructed with the engine price curve in per-unit lockstep.

Usage: .venv/Scripts/python.exe tools/o_revenue.py state/o_dev/replays/seed1002_seat0.json
"""
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent"))
from o001_demand_planner import price, PRODUCTS, CROPS, ANIMALS, LAND_PRICES  # noqa: E402

FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]


def analyze(path):
    r = json.load(open(path, encoding="utf-8"))
    steps = r["steps"]
    rev = [defaultdict(float), defaultdict(float)]
    qty = [Counter(), Counter()]
    cost = [defaultdict(float), defaultdict(float)]
    daily = [defaultdict(Counter), defaultdict(Counter)]
    for t in range(1, len(steps)):
        ob_prev = [steps[t - 1][p]["observation"] for p in range(2)]
        ob_now = [steps[t][p]["observation"] for p in range(2)]
        inv = dict(ob_prev[0]["market"]["inventory"])
        farms = ob_prev[0]["farms"]
        hires = [farms[0]["hires_today"], farms[1]["hires_today"]]
        lands = [len(farms[0]["unlocked_quadrants"]) - 1, len(farms[1]["unlocked_quadrants"]) - 1]
        day = (t - 1) // 24
        new_day = (t % 24 == 0)
        sold = [Counter(), Counter()]
        queues = []
        for p in range(2):
            a = steps[t][p].get("action") or {}
            q = list(a.get("market", []) or [])[:10]
            queues.append(q)
            priv_b = ob_prev[p].get("private") or {}
            priv_a = ob_now[p].get("private") or {}
            shed_b = priv_b.get("shed") or {}
            shed_a = priv_a.get("shed") or {}
            invs_b = priv_b.get("inventories") or []
            invs_a = priv_a.get("inventories") or []
            bought = Counter()
            for o in q:
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    bought[o[1]] += int(o[2])   # upper bound; corrected below by delta
            for item in PRODUCTS:
                drops = 0
                pickups = 0
                if new_day:
                    drops = sum(iv.get(item, 0) for iv in invs_b)
                else:
                    n = min(len(invs_b), len(invs_a))
                    for i in range(n):
                        d = invs_b[i].get(item, 0) - invs_a[i].get(item, 0)
                        if d > 0:
                            drops += d
                        elif d < 0:
                            pickups += -d
                # consumed in the field (FEED/FERTILIZE) also reduce unit inventory; treat as drops only if shed rose
                delta = shed_a.get(item, 0) - shed_b.get(item, 0)
                # sold = shed_b + drops - pickups + bought - shed_a  (bought only for WHEAT/FERTILIZER)
                b = bought.get(item, 0) if item in ("WHEAT", "FERTILIZER") else 0
                s = shed_b.get(item, 0) + drops - pickups + b - shed_a.get(item, 0)
                # field consumption (feed/fertilize) was counted as drops; clamp using SELL orders
                sell_req = sum(int(o[2]) for o in q if o and o[0] == "SELL" and len(o) >= 3 and o[1] == item)
                s = max(0, min(s, sell_req))
                sold[p][item] = s
        # lockstep price reconstruction in order slots
        maxlen = max(len(q) for q in queues) if queues else 0
        remaining = [dict(sold[0]), dict(sold[1])]
        step_rev = [defaultdict(float), defaultdict(float)]
        step_cost = [0.0, 0.0]
        money_before = [farms[0]["money"], farms[1]["money"]]
        for i in range(maxlen):
            st = [None, None]
            for p in range(2):
                if i < len(queues[p]):
                    o = queues[p][i]
                    if not o:
                        continue
                    if o[0] == "HIRE":
                        if hires[p] < len(FIB):
                            cost[p]["HIRE"] += FIB[hires[p]]
                            step_cost[p] += FIB[hires[p]]
                        hires[p] += 1
                    elif o[0] == "BUY_LAND":
                        if lands[p] < 3:
                            cost[p]["LAND"] += LAND_PRICES[lands[p]]
                            step_cost[p] += LAND_PRICES[lands[p]]
                            lands[p] += 1
                    elif o[0] in ("SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL") and len(o) >= 3:
                        n = int(o[2])
                        if o[0] == "SELL":
                            n = min(n, remaining[p].get(o[1], 0))
                            remaining[p][o[1]] = remaining[p].get(o[1], 0) - n
                        st[p] = [o[0], o[1], n]
            while any(s and s[2] > 0 for s in st):
                for p in range(2):
                    s = st[p]
                    if not s or s[2] <= 0:
                        continue
                    op, item, n = s
                    if op == "SELL" and item in PRODUCTS:
                        pr = price(item, inv[item])
                        rev[p][item] += pr
                        step_rev[p][item] += pr
                        qty[p][item] += 1
                        daily[p][day][item] += pr
                        if pr > 1:
                            inv[item] += 1
                    elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                        pr = price(item, inv[item] - 1)
                        cost[p]["BUY_" + item] += pr
                        step_cost[p] += pr
                        inv[item] -= 1
                    elif op == "BUY_SEED" and item in CROPS:
                        cost[p]["SEED_" + item] += CROPS[item]["seed"]
                        step_cost[p] += CROPS[item]["seed"]
                    elif op == "BUY_ANIMAL" and item in ANIMALS:
                        cost[p]["ANIMAL_" + item] += ANIMALS[item]["cost"]
                        step_cost[p] += ANIMALS[item]["cost"]
                    s[2] -= 1
        # reconcile with the true money delta: attribute any unexplained revenue to the
        # SELL orders of that step (same-step drop+sell is invisible in shed deltas)
        for p in range(2):
            true_rev = ob_now[p]["farms"][p]["money"] - money_before[p] + step_cost[p]
            est = sum(step_rev[p].values())
            gap = true_rev - est
            if gap > 1.0:
                weights = {}
                for o in queues[p]:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                        weights[o[1]] = weights.get(o[1], 0.0) + int(o[2]) * ob_prev[0]["market"]["prices"][o[1]]
                tot = sum(weights.values())
                if tot > 0:
                    for item, w in weights.items():
                        share = gap * w / tot
                        rev[p][item] += share
                        daily[p][day][item] += share
                        qty[p][item] += int(round(share / max(1, ob_prev[0]["market"]["prices"][item])))
    names = r.get("info", {}).get("TeamNames") or ["P0", "P1"]
    final = [s["reward"] for s in steps[-1]]
    out = {}
    for p in range(2):
        recon = 3000 + sum(rev[p].values()) - sum(cost[p].values())
        print(f"=== player {p} {names[p]} final={final[p]}  (recon {recon:.0f})")
        print("  revenue:", {k: (int(v), qty[p][k], int(v / max(1, qty[p][k]))) for k, v in sorted(rev[p].items(), key=lambda kv: -kv[1])})
        print("  costs  :", {k: int(v) for k, v in sorted(cost[p].items(), key=lambda kv: -kv[1])})
        out[p] = {"revenue": dict(rev[p]), "qty": dict(qty[p]), "cost": dict(cost[p]), "final": final[p]}
    return out


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print("#", path)
        analyze(path)
