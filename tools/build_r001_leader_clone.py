"""Build r001_leader_clone: Level-2 behavioural clone of the #1 team (Majkel1337) by
state-conditioned action retrieval over 337 public replays, executed through the public
route-replay Chassis (c150 lineage, Apache-2.0; hand_align/weed_repair/sell_lead/room_guard
repair layers) so recorded actions stay physically valid on our own farm.

Policy = pi(observable state): at every day boundary (and at step 0) the router picks the recorded
leader game whose day-start state is nearest to ours (same day; distance = shop mismatch + tile
layout Hamming + cash + quadrants + hands, small bonus for higher final reward, hysteresis to keep
the current game while it stays close) and replays that game's actions for the day. Days 0-6 are
near-deterministic in the leader's play (267/337 identical layouts at day 6) so retrieval is
exact there; later days rely on similarity. Recorded actions come from public Kaggle episodes
(behavioural reference only; no private code).

Usage: .venv/Scripts/python.exe tools/build_r001_leader_clone.py [--min-reward 0] [--max-games 337]
"""
import argparse, base64, hashlib, json, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/c150.py"
PARENT_SHA = "9713af1538ccc8e4e0e8a7ff72ae8a614ba9e7dcb3eb9d53c3074aabec137d6b"
DATASET = ROOT / "state/o_dev/r001/leader_dataset.b85"
TARGET = ROOT / "agent/r001_leader_clone.py"

HEADER = '''# r001_leader_clone (reverse-engineering series, 2026-09-15). Apache-2.0.
# Chassis: public route-replay chassis from agent/c150.py lineage (thomastschinkel, yhay81,
# tetsutani, aurax7; Apache-2.0 notices retained in c150). Policy data: actions reconstructed from
# public Kaggle episodes of team Majkel1337 (behavioural reference; no private code).
# Level-2 behavioural clone: per-day nearest-neighbour retrieval over recorded observable states.
'''

TAIL = r'''

import base64 as _r1_b64, json as _r1_json, zlib as _r1_zlib
_R1 = _r1_json.loads(_r1_zlib.decompress(_r1_b64.b85decode(%(payload)r)))
_R1_ROUTES = {int(k): v for k, v in _R1["routes"].items()}          # id -> 719 actions
_R1_DAYS = {int(k): v for k, v in _R1["days"].items()}              # id -> [30 day-start feature dicts]
_R1_REWARD = {int(k): v for k, v in _R1["reward"].items()}
del _R1
_R1_HYSTERESIS = 3.0
_R1_REWARD_BONUS = 1.0 / 20000.0   # distance units per $ of final reward
_R1_DIAG = {"switches": 0, "dist_sum": 0.0, "picks": 0, "errors": 0}


def _r1_layout(farm):
    out = set()
    for y, row in enumerate(_get(farm, "tiles", []) or []):
        for x, tl in enumerate(row or []):
            if isinstance(tl, dict):
                out.add((x, y, tl.get("crop") or tl.get("animal") or tl.get("kind")))
    return out


def _r1_distance(obs_feat, rec):
    shops = obs_feat["shops"]; rs = rec["shops"]
    d = 0.0
    n = max(len(shops), len(rs))
    d += 3.0 * sum(1 for i in range(n) if (shops[i] if i < len(shops) else None) != (rs[i] if i < len(rs) else None))
    lay = obs_feat["layout"]; rl = set((t[0], t[1], t[2]) for t in rec["layout"])
    d += 0.5 * len(lay ^ rl)
    d += abs(obs_feat["cash"] - rec["cash"]) / 500.0
    d += 5.0 * abs(obs_feat["quads"] - rec["quads"])
    d += 0.5 * abs(obs_feat["hands"] - rec["hands"])
    return d


def _r1_router(observation, step, state):
    day = step // 24
    if state.get("day") == day and state.get("route") in _R1_ROUTES:
        return state["route"]
    try:
        player = _int(_get(observation, "player", 0))
        farm = (_get(observation, "farms", []) or [])[player]
        feat = dict(shops=list(_get(_get(observation, "town", {}), "unlocked_shops", []) or []),
                    layout=_r1_layout(farm), cash=float(_get(farm, "money", 0) or 0),
                    quads=len(list(_get(farm, "unlocked_quadrants", []) or [])), hands=len(list(_get(farm, "hands", []) or [])))
        best, best_d = None, None
        for rid, days in _R1_DAYS.items():
            if day >= len(days):
                continue
            d = _r1_distance(feat, days[day]) - _R1_REWARD_BONUS * _R1_REWARD.get(rid, 0)
            if best_d is None or d < best_d:
                best, best_d = rid, d
        cur = state.get("route")
        if cur in _R1_ROUTES and day < len(_R1_DAYS[cur]):
            cur_d = _r1_distance(feat, _R1_DAYS[cur][day]) - _R1_REWARD_BONUS * _R1_REWARD.get(cur, 0)
            if cur_d <= best_d + _R1_HYSTERESIS:
                best, best_d = cur, cur_d
        if best != cur:
            _R1_DIAG["switches"] += 1
        _R1_DIAG["picks"] += 1; _R1_DIAG["dist_sum"] += float(best_d)
        state["route"] = best; state["day"] = day
        return best
    except Exception:
        _R1_DIAG["errors"] += 1
        return state.get("route", next(iter(_R1_ROUTES)))


_R1_SETTINGS = {"hand_align": True, "weed_repair": True, "sell_lead": True, "budget_guard": False, "room_guard": True,
                "clamp_sells": True, "dead_stock": False, "terminal_liquidation": True, "front_run": False, "block_turns": 24}
_R1_IMPL = make_agent(_R1_ROUTES, router=_r1_router, **_R1_SETTINGS)
_R1_REPORT = {}


def agent(observation, configuration=None):
    action = _R1_IMPL(observation, configuration)
    try:
        _R1_REPORT.clear(); _R1_REPORT.update(_R1_IMPL.chassis.diagnostics)
        _R1_REPORT.update({"r001_" + k: v for k, v in _R1_DIAG.items()})
        _R1_REPORT["r001_route"] = _R1_IMPL.chassis.players[int(observation["player"])]["route"]
    except Exception:
        pass
    return action


agent.telemetry = _R1_REPORT
agent = globals().pop("agent")
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-reward", type=float, default=0.0)
    ap.add_argument("--max-games", type=int, default=400)
    ap.add_argument("--out", default=str(TARGET))
    a = ap.parse_args()
    src = PARENT.read_text(encoding="utf-8")
    assert hashlib.sha256(src.encode("utf-8")).hexdigest() == PARENT_SHA, "c150 parent drift"
    start = src.index('"""Kaggriculture route-replay chassis')
    end = src.index("    agent.chassis = chassis\n    return agent\n") + len("    agent.chassis = chassis\n    return agent\n")
    chassis = src[start:end]
    games = json.loads(zlib.decompress(base64.b85decode(DATASET.read_text())))
    games = sorted((g for g in games.values() if g["reward"] >= a.min_reward), key=lambda g: -g["reward"])[: a.max_games]
    routes, days, reward = {}, {}, {}
    for i, g in enumerate(games):
        routes[i] = g["tape"]; reward[i] = g["reward"]
        days[i] = [dict(shops=d["shops"], layout=d["layout"], cash=d["cash"], quads=d["quads"], hands=d["hands"]) for d in g["days"]]
    payload = base64.b85encode(zlib.compress(json.dumps({"routes": routes, "days": days, "reward": reward}, separators=(",", ":")).encode(), 9)).decode()
    out = HEADER + chassis + TAIL % {"payload": payload}
    compile(out, "r001", "exec")
    Path(a.out).write_text(out, encoding="utf-8")
    print("built", a.out, len(out), "bytes; games", len(games), "sha256", hashlib.sha256(out.encode("utf-8")).hexdigest()[:16])


if __name__ == "__main__":
    main()
