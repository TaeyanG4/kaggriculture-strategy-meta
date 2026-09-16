"""Build o005_majkel_router: the public route-replay chassis (from c129, Apache-2.0
lineage thomastschinkel/yhay81/tetsutani/aurax7) driving action tapes recorded
from Majkel1337's public episodes, routed by the first unlocked shops.

Usage: .venv/Scripts/python.exe tools/build_o005.py --out agent/o005_majkel_router.py
"""
import argparse
import base64
import hashlib
import json
import zlib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEADER = '''# o005_majkel_router (Claude lineage, 2026-09-14). Apache-2.0.
# Route-replay chassis: c129 lineage (thomastschinkel, yhay81, tetsutani, aurax7; notices retained in c129).
# Action tapes: reconstructed from public Kaggle episodes of team Majkel1337 (public replay data,
# used as behavioural reference; no private code). Routing: first two unlocked shops.
'''

TAIL = '''

import base64 as _o5_b64
import json as _o5_json
import zlib as _o5_zlib
_O5_PAYLOAD = _o5_json.loads(_o5_zlib.decompress(_o5_b64.b85decode(%(payload)r)))
_O5_ROUTES = {int(k): v for k, v in _O5_PAYLOAD["routes"].items()}
_O5_BY_PAIR = {tuple(k.split("|")): int(v) for k, v in _O5_PAYLOAD["by_pair"].items()}
_O5_BY_FIRST = {k: int(v) for k, v in _O5_PAYLOAD["by_first"].items()}
_O5_DEFAULT = int(_O5_PAYLOAD["default"])
_O5_HANDS = {int(k): v for k, v in _O5_PAYLOAD["hands"].items()}
del _O5_PAYLOAD
_O5_SETTINGS = %(settings)r


def _o5_router(observation, step, state):
    shops = _get(_get(observation, "town", {}), "unlocked_shops", []) or []
    if step >= 72 and not state.get("day3") and len(shops) >= 1:
        state["route"] = _O5_BY_FIRST.get(shops[0], _O5_DEFAULT)
        state["day3"] = True
    if step >= 144 and not state.get("day6") and len(shops) >= 2:
        pair = (shops[0], shops[1])
        if pair in _O5_BY_PAIR:
            state["route"] = _O5_BY_PAIR[pair]
        state["day6"] = True
    return state.get("route", _O5_DEFAULT)


_O5_IMPL = make_agent(_O5_ROUTES, router=_o5_router, **_O5_SETTINGS)
_O5_REPORT = {}


_O5_PRIORITY = {"SELL": 0, "HIRE": 1, "BUY_PRODUCT": 2, "BUY_ANIMAL": 3, "BUY_LAND": 4, "BUY_SEED": 5}
_O5_SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
_O5_OPENING_RESERVE = %(reserve)d


def _o5_market_fix(observation, action):
    """Strip same-step wheat buy/sell washes, order SELL > HIRE > buys so proceeds
    fund hires first, and keep a small cash reserve on day 0 so day-1 hires succeed."""
    market = [list(o) for o in (action.get("market") or []) if o]
    sells = sum(int(o[2]) for o in market if o[0] == "SELL" and len(o) == 3 and o[1] == "WHEAT")
    buys = sum(int(o[2]) for o in market if o[0] == "BUY_PRODUCT" and len(o) == 3 and o[1] == "WHEAT")
    wash = min(sells, buys)
    if wash > 0:
        out = []
        for o in market:
            if len(o) == 3 and o[1] == "WHEAT" and o[0] in ("SELL", "BUY_PRODUCT") and wash > 0:
                cut = min(int(o[2]), wash)
                if o[0] == "SELL":
                    o[2] = int(o[2]) - cut
                    sells -= cut
                else:
                    o[2] = int(o[2]) - cut
                    buys -= cut
                wash = min(sells, buys)
            if len(o) == 3 and int(o[2]) <= 0:
                continue
            out.append(o)
        market = out
    step = int(observation.get("step", 0))
    # cap HIREs at the hand count the source game actually reached that day
    try:
        route = _O5_IMPL.chassis.players[int(observation["player"])]["route"]
        expected = _O5_HANDS[route][min(29, step // 24)]
        have = len(observation["farms"][int(observation["player"])].get("hands") or [])
        allow = max(0, expected - have)
        out = []
        for o in market:
            if o[0] == "HIRE":
                if allow <= 0:
                    continue
                allow -= 1
            out.append(o)
        market = out
    except Exception:
        pass
    if step < 24 and _O5_OPENING_RESERVE > 0:
        money = float(observation["farms"][int(observation["player"])]["money"])
        kept = []
        for o in market:
            if o[0] == "BUY_SEED" and len(o) == 3:
                cost = _O5_SEED_COST.get(o[1], 0) * int(o[2])
                if money - cost < _O5_OPENING_RESERVE:
                    continue
                money -= cost
            kept.append(o)
        market = kept
    action["market"] = market[:10]
    return action


def agent(observation, configuration=None):
    action = _O5_IMPL(observation, configuration)
    try:
        action = _o5_market_fix(observation, action)
    except Exception:
        pass
    _O5_REPORT.clear()
    _O5_REPORT.update(_O5_IMPL.chassis.diagnostics)
    try:
        _O5_REPORT["route"] = _O5_IMPL.chassis.players[int(observation["player"])]["route"]
    except Exception:
        pass
    return action


agent.telemetry = _O5_REPORT
agent = globals().pop("agent")
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default="state/o_dev/majkel_tapes/games.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--block", type=int, default=24)
    ap.add_argument("--min-reward", type=float, default=0.0)
    ap.add_argument("--reserve", type=int, default=12)
    ap.add_argument("--no-guard", action="store_true")
    ap.add_argument("--prefix-consistent", action="store_true")
    ap.add_argument("--layout-consistent", action="store_true")
    a = ap.parse_args()
    src = (ROOT / "agent/c129_feed_liquidity.py").read_text(encoding="utf-8")
    start = src.index('"""Kaggriculture route-replay chassis')
    end = src.index("    agent.chassis = chassis\n    return agent\n") + len("    agent.chassis = chassis\n    return agent\n")
    chassis = src[start:end]
    games = json.load(open(ROOT / a.games, encoding="utf-8"))
    games = [g for g in games if g["reward"] >= a.min_reward]
    # modal opening cluster (steps 0-24) -> default route from the largest cluster
    def h(t, b):
        return hashlib.sha256(json.dumps(t[:b], sort_keys=True).encode()).hexdigest()
    clusters = Counter(h(g["tape"], 24) for g in games)
    modal = clusters.most_common(1)[0][0]
    routes = {}
    hands = {}
    by_pair = {}
    by_first = {}
    # choose best-reward game per pair; per first shop; default
    best_pair = {}
    for g in games:
        k = tuple(g["pair"])
        if k not in best_pair or g["reward"] > best_pair[k]["reward"]:
            best_pair[k] = g
    best_first = {}
    for g in games:
        k = g["pair"][0]
        if k not in best_first or g["reward"] > best_first[k]["reward"]:
            best_first[k] = g
    if a.layout_consistent:
        # splice between tapes whose farms are identical at the switch step (hands respawn at dawn)
        c72 = Counter(g["layout72"] for g in games); m72 = c72.most_common(1)[0][0]
        c144 = Counter(g["layout144"] for g in games); m144 = c144.most_common(1)[0][0]
        pool72 = [g for g in games if g["layout72"] == m72]
        pool144 = [g for g in games if g["layout144"] == m144 and g["layout72"] == m72]
        default = max(pool144, key=lambda g: g["reward"])
        best_first = {}
        for g in pool144:
            k = g["pair"][0]
            if k not in best_first or g["reward"] > best_first[k]["reward"]:
                best_first[k] = g
        best_pair = {}
        for g in pool144:
            k = tuple(g["pair"])
            if k not in best_pair or g["reward"] > best_pair[k]["reward"]:
                best_pair[k] = g
        print("layout-consistent: pool72", len(pool72), "pool144", len(pool144), "first", len(best_first), "pairs", len(best_pair))
    elif a.prefix_consistent:
        # only splice between tapes that share the exact action prefix up to the switch step
        c72 = Counter(h(g["tape"], 72) for g in games)
        modal72 = c72.most_common(1)[0][0]
        pool72 = [g for g in games if h(g["tape"], 72) == modal72]
        default = max(pool72, key=lambda g: g["reward"])
        best_first = {}
        for g in pool72:
            k = g["pair"][0]
            if k not in best_first or g["reward"] > best_first[k]["reward"]:
                best_first[k] = g
        best_pair = {}
        for g in games:
            if h(g["tape"], 144) != h(best_first.get(g["pair"][0], default)["tape"], 144):
                continue
            k = tuple(g["pair"])
            if k not in best_pair or g["reward"] > best_pair[k]["reward"]:
                best_pair[k] = g
        print("prefix-consistent: pool72", len(pool72), "first", len(best_first), "pairs", len(best_pair))
    else:
        default = max((g for g in games if h(g["tape"], 24) == modal), key=lambda g: g["reward"])
    ids = {}
    def rid(g):
        key = g["episode"]
        if key not in ids:
            ids[key] = len(ids)
            routes[ids[key]] = g["tape"]
            hands[ids[key]] = g["hands_per_day"]
        return ids[key]
    default_id = rid(default)
    for k, g in best_pair.items():
        by_pair["|".join(k)] = rid(g)
    for k, g in best_first.items():
        by_first[k] = rid(g)
    payload = base64.b85encode(zlib.compress(json.dumps({"routes": routes, "hands": hands, "by_pair": by_pair, "by_first": by_first, "default": default_id}, separators=(",", ":")).encode(), 9)).decode()
    settings = {"hand_align": True, "weed_repair": True, "sell_lead": True, "budget_guard": not a.no_guard, "room_guard": True,
                "clamp_sells": True, "dead_stock": True, "terminal_liquidation": True, "front_run": False, "block_turns": a.block}
    out = HEADER + chassis + TAIL % {"payload": payload, "settings": settings, "reserve": a.reserve}
    compile(out, "o005", "exec")
    (ROOT / a.out).write_text(out, encoding="utf-8")
    print("built", a.out, len(out), "routes", len(routes), "pairs", len(by_pair), "first", len(by_first), "default episode", default["episode"], default["reward"])


if __name__ == "__main__":
    main()
