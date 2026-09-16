"""o154_hinge_sell (Claude/o-series, 2026-09-14). Parent: c150 (unmodified, read-only).

Hypothesis (from the prior c129-era 79-loss forensics, memory `kaggriculture-negative-results`):
CARROT and TOMATO both use a "hinge" scarcity price curve (`_R37_MARKET_PARAMS`: CARROT base=35
T=450 below_target=1.0, TOMATO base=60 T=200 below_target=0.4) that spikes sharply when the shared
market inventory runs low — TOMATO hinge spikes (>=$180, i.e. 3x base) were observed in 18% of a
79-loss sample, and 12/14 of those saw NEITHER player sell a single unit. The c150 audit
(o_progress.md) confirms V219 already runs a full labor-reallocated TOMATO *planting* investment
program, but nothing in c150 reacts to an in-progress price spike by selling ALREADY-HELD CARROT/
TOMATO stock faster — R36's reservation system only pulls forward sales the tape already scheduled
for a *future* step, and R37's reorder only changes sell ORDER, not sell QUANTITY.

This candidate is deliberately narrow and low-risk (sell-side only, no field/worker/land changes):
if CARROT or TOMATO's current market price is >= 3x its base price (a hinge spike), and the shed
holds more of that item than the final action already plans to sell, add one extra SELL order for
the unsold surplus. Both items are pure finished-goods outputs in c150 (CARROT/TOMATO product is
never itself consumed by any overlay — EXP182's R51 only *fertilizes growing plants*, it doesn't
consume harvested product), so this cannot break another overlay's reserve the way o152 did.
"""
import importlib.util
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_C150_PATH = os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o154_c150_base", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of
_View = _base._View
_R37_MARKET_PARAMS = _base._R37_MARKET_PARAMS

_HINGE_ITEMS = ("CARROT", "TOMATO")
_HINGE_MULT = 3.0
_MAX_ORDERS = 10
_DIAG = {"triggers": 0, "units_sold": 0, "errors": 0}


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
    try:
        chassis = _base._IMPL.chassis
        player = _int(_get(observation, "player", 0))
        view = _View(observation, player, chassis.cfg)
        market = action.get("market") or []
        already = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                already[o[1]] = already.get(o[1], 0) + max(0, _int(o[2]))
        extra = []
        for item in _HINGE_ITEMS:
            base_price = _R37_MARKET_PARAMS.get(item, {}).get("base", 0)
            price = view.prices.get(item, 0)
            if base_price <= 0 or price < _HINGE_MULT * base_price:
                continue
            surplus = view.shed.get(item, 0) - already.get(item, 0)
            if surplus > 0:
                extra.append(["SELL", item, surplus])
        if extra and len(market) < _MAX_ORDERS:
            room = _MAX_ORDERS - len(market)
            extra = extra[:room]
            action = dict(action)
            action["market"] = market + extra
            _DIAG["triggers"] += 1
            _DIAG["units_sold"] += sum(o[2] for o in extra)
    except Exception:
        _DIAG["errors"] += 1
    return action


agent.telemetry = _DIAG
