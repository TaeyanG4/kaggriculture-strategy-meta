"""o157_combined (Claude/o-series, 2026-09-14). Parent: c150 (unmodified, read-only).

Combination candidate per the spec's ablation methodology (don't just stack independently-good
changes without checking interaction): merges the two components that individually showed a
non-negative effect in isolated testing --

  1. o155's opening-order tweak (BUY_PRODUCT WHEAT 10+8, SELL WHEAT 25 at step 0 instead of the
     default 13+10/30) -- KEEP, 156W/4L/0T (97.5%) vs plain c150 across 160 games, mean margin
     +19..+25, bounded worst-case -118.
  2. o153's post-hoc budget-guard-v2 (re-invokes chassis._budget_guard on the final action, with
     FERTILIZER/WHEAT excluded from the emergency-sell pool to avoid the o152 regression) --
     KEEP-NEUTRAL, 1W/1L/46T vs c150 (effectively 0 average effect in mirror testing) but adds a
     safety margin against overlay-injected cash shortfalls with no observed downside, including
     against non-mirror opponents (moon-counts-melons/best-market-agent/metacounter-r1).

Both touch disjoint, well-isolated parts of the final action (step-0 market list vs. an
end-of-block emergency-sell addition) so no interaction is expected, but this file exists
specifically to VERIFY that empirically per spec item 42 rather than assume it.
"""
import importlib.util
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_C150_PATH = os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o157_c150_base", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of
_View = _base._View
PRODUCTS = _base.PRODUCTS

_OPENING = [["BUY_PRODUCT", "WHEAT", 10], ["BUY_PRODUCT", "WHEAT", 8], ["SELL", "WHEAT", 25]]
_PROTECTED_ALWAYS = {"FERTILIZER", "WHEAT"}
_DIAG = {"guard_invocations": 0, "guard_extra_sells": 0, "guard_errors": 0, "opening_applied": 0}


def _safe_sell_guard(chassis, action, view, route, step):
    cfg = chassis.cfg
    block = cfg["block_turns"]
    if block <= 0 or step % block != 0:
        return
    budget, item_need = chassis._block_requirements(view, route, step, step + block)
    market = action.setdefault("market", [])
    existing = {}
    for o in market:
        if o and o[0] == "SELL" and len(o) >= 3:
            existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
    cash = view.money
    for item in PRODUCTS:
        planned = max(existing.get(item, 0), chassis.future_sells(route, item, step)
                      - chassis.future_sells(route, item, step + block))
        cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
    shortfall = budget - cash
    if shortfall <= 0:
        return
    candidates = []
    for item in PRODUCTS:
        if item in _PROTECTED_ALWAYS:
            continue
        price = view.prices.get(item, 0)
        if price < cfg["min_sell_price"]:
            continue
        protected = max(0, item_need.get(item, 0) - view.in_hands(item))
        avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
        if avail > 0:
            candidates.append((-price, item, avail, price))
    candidates.sort()
    added = False
    for _, item, avail, price in candidates:
        if shortfall <= 0:
            break
        qty = min(avail, -(-int(shortfall) // price))
        if chassis._add_sell(action, item, qty, cfg["max_orders"]):
            shortfall -= qty * price
            added = True
    if added:
        sells = [o for o in market if o and o[0] == "SELL"]
        others = [o for o in market if not (o and o[0] == "SELL")]
        action["market"] = sells + others


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
    try:
        step = _step_of(observation)
        if step == 0:
            action = dict(action)
            action["market"] = [list(o) for o in _OPENING]
            _DIAG["opening_applied"] += 1
    except Exception:
        pass
    try:
        chassis = _base._IMPL.chassis
        player = _int(_get(observation, "player", 0))
        step = _step_of(observation)
        st = chassis.players.get(player)
        route = st["route"] if st else 0
        view = _View(observation, player, chassis.cfg)
        before = len(action.get("market") or [])
        _safe_sell_guard(chassis, action, view, route, step)
        after = len(action.get("market") or [])
        _DIAG["guard_invocations"] += 1
        if after > before:
            _DIAG["guard_extra_sells"] += 1
    except Exception:
        _DIAG["guard_errors"] += 1
    return action


agent.telemetry = _DIAG
