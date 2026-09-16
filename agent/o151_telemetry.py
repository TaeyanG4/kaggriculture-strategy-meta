"""o151_telemetry (Claude/o-series, 2026-09-14).

Behavior-NEUTRAL wrapper around the read-only baseline `agent/c150.py`. Loads c150 as a
module and calls its `agent()` unmodified; the returned action is passed through byte-for-byte
identical (same object, no post-processing). The only side effect is appending one JSON line
per own decision to O151_LOG (default o_results/o151_telemetry.jsonl) recording the state
needed for the o15x experiment backlog (advantage estimate, portfolio mix, triggers, etc.).

c150.py itself is NOT modified (read-only baseline per project instructions). This file is a
pure external wrapper: it imports c150.py by path and reuses its already-defined helpers
(_get, _int, _step_of, _View, _r37_market_price, PRODUCTS, _R37_MARKET_PARAMS) so telemetry
math stays consistent with the engine replica c150 already carries. No third-party code is
copied here; c150.py retains all of its own upstream Apache-2.0 attributions unchanged.

Usage: identical to any other agent file (Kaggle picks the last top-level callable, `agent`).
Env vars: O151_LOG (output path), O151_LOG_DISABLE=1 (skip logging entirely, e.g. in arenas
where I/O contention across parallel workers is undesirable).
"""
import importlib.util
import json
import os
import threading

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_C150_PATH = os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o151_c150_base", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of
_View = _base._View
_r37_market_price = _base._r37_market_price
_R37_MARKET_PARAMS = getattr(_base, "_R37_MARKET_PARAMS", {})
PRODUCTS = _base.PRODUCTS

_LOG_PATH = os.environ.get("O151_LOG", os.path.join(_ROOT, "o_results", "o151_telemetry.jsonl"))
_LOG_DISABLE = os.environ.get("O151_LOG_DISABLE") == "1"
_LOCK = threading.Lock()
_RUN_ID = os.environ.get("O151_RUN_ID", str(os.getpid()))


def _liquidation_value(view):
    """cash + shed inventory + carried (in-hand) inventory, all at current market price."""
    total = float(view.money)
    for item, qty in view.shed.items():
        if item in PRODUCTS and qty > 0:
            total += _r37_market_price(item, view.prices.get(item, 0)) * qty
    for inv in view.invs:
        for item, qty in dict(inv or {}).items():
            if item in PRODUCTS and qty > 0:
                total += _r37_market_price(item, view.prices.get(item, 0)) * qty
    return total


def _harvestable_yield(tiles):
    """Sum of yield_units currently sitting ripe on tiles (crops + animal products)."""
    total = 0
    crop_counts = {}
    animal_counts = {}
    for row in tiles or []:
        for t in row or []:
            if not isinstance(t, dict):
                continue
            yu = _int(t.get("yield_units", 0))
            if t.get("kind") == "PLANT":
                crop_counts[t.get("crop")] = crop_counts.get(t.get("crop"), 0) + 1
                total += yu
            elif t.get("kind") in ("COOP", "PASTURE") and t.get("animal"):
                animal_counts[t.get("animal")] = animal_counts.get(t.get("animal"), 0) + 1
                total += yu
    return total, crop_counts, animal_counts


def _safe(fn, default=None):
    try:
        return fn()
    except Exception:
        return default


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
    if _LOG_DISABLE:
        return action
    try:
        cfg = _base._IMPL.chassis.cfg
        player = _int(_get(observation, "player", 0))
        step = _step_of(observation)
        view = _View(observation, player, cfg)
        rview = _View(observation, 1 - player, cfg)
        own_yield, own_crops, own_animals = _harvestable_yield(view.tiles)
        rival_yield, rival_crops, rival_animals = _harvestable_yield(rview.tiles)
        own_value = _liquidation_value(view)
        # Rival value uses only publicly-visible fields (money + visible harvestable yield at
        # current price); we deliberately do NOT assume knowledge of rival shed/inventory.
        rival_visible_value = rview.money + sum(
            _r37_market_price(
                {"WHEAT": "WHEAT", "CARROT": "CARROT", "TOMATO": "TOMATO", "STRAWBERRY": "STRAWBERRY",
                 "MELON": "MELON"}.get(crop, crop),
                view.prices.get(crop, 0),
            ) * n
            for crop, n in [(c, sum(1 for row in rview.tiles or [] for t in row or []
                                     if isinstance(t, dict) and t.get("crop") == c and _int(t.get("yield_units", 0)) > 0))
                             for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")]
            if crop in PRODUCTS and n
        )
        route = _safe(lambda: _base._IMPL.chassis.players[player].get("route"))
        diagnostics = _safe(lambda: dict(_base._IMPL.chassis.diagnostics), {})
        rec = {
            "run": _RUN_ID, "step": step, "player": player,
            "own_money": view.money, "rival_money": rview.money,
            "money_diff": view.money - rview.money,
            "own_value": own_value, "rival_visible_value": rival_visible_value,
            "advantage": own_value - rival_visible_value,
            "own_workers": len(view.positions), "rival_workers": len(rview.positions),
            "own_quadrants": view.quadrants, "rival_quadrants": rview.quadrants,
            "own_crops": own_crops, "rival_crops": rival_crops,
            "own_animals": own_animals, "rival_animals": rival_animals,
            "own_harvestable_yield": own_yield, "rival_harvestable_yield": rival_yield,
            "shed": view.shed, "seeds": view.seeds,
            "market_prices": view.prices,
            "unlocked_shops": _get(_get(observation, "town", {}), "unlocked_shops", []),
            "route": route,
            "diag_snapshot": {k: v for k, v in diagnostics.items() if isinstance(v, (int, float, str))},
            "action_market": action.get("market") if isinstance(action, dict) else None,
        }
        with _LOCK:
            os.makedirs(os.path.dirname(_LOG_PATH), exist_ok=True)
            with open(_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, default=str) + "\n")
    except Exception as exc:
        # Telemetry must never affect gameplay; swallow and continue with the parent action.
        try:
            with _LOCK:
                os.makedirs(os.path.dirname(_LOG_PATH), exist_ok=True)
                with open(_LOG_PATH + ".errors", "a", encoding="utf-8") as f:
                    f.write(repr(exc) + "\n")
        except Exception:
            pass
    return action
