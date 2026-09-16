"""o153_post_budget_guard_v2 (Claude/o-series, 2026-09-14). Parent: c150 (unmodified, read-only).

o152 (post-hoc re-invocation of c150's own disabled `chassis._budget_guard` on the FINAL,
post-overlay action) LOST to plain c150 by -5k..-10k across the first 10/10 arena games tested
(seed-base 100). Root cause (`o_tests/diag_o152.py` trace on seed 100, seat 0): the guard fired
only twice the whole game, each time selling just 2 FERTILIZER units (~$100-200 total) — but this
tiny sale emptied the shed of FERTILIZER right when a LATER overlay's dynamic fertilizer planner
needed it this turn, turning its FERTILIZE action into a silent no-op and losing much more crop
yield than the guard ever raised. Cause: `chassis._block_requirements` computes `item_need` only
from the STATIC route tape's own scripted FEED/FERTILIZE/PLACE ops — it has zero visibility into
overlay-injected DYNAMIC consumption plans (the fertilizer planner, tomato/carrot investment
programs, feed-forward buffers, etc. all decide FERTILIZE/FEED/PLANT at runtime, not from the
tape). Any external guard built purely on `_block_requirements` will systematically under-protect
exactly the items those overlays manage. See o_experiments.jsonl entry for o152 (REJECTED).

Fix tested here: keep the same post-hoc re-invocation of `_budget_guard`, but never let it sell
FERTILIZER or WHEAT (the two items every overlay in c150 treats as a live working input: feed
stock and fertilizer stock) — restrict its emergency-sell candidate pool to pure finished-goods
outputs (CARROT, TOMATO, STRAWBERRY, MELON, EGG, MILK, WOOL) that nothing else in c150 consumes
as an input. Implemented by monkeypatching a *local* copy of the guard rather than editing
c150.py: we call `_block_requirements` ourselves (read-only) and reimplement just the sell-
selection loop with the exclusion, instead of calling the shared bound method (which has no
parameter to exclude items).
"""
import importlib.util
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_C150_PATH = os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o153_c150_base", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of
_View = _base._View
PRODUCTS = _base.PRODUCTS

_PROTECTED_ALWAYS = {"FERTILIZER", "WHEAT"}  # live working inputs; never emergency-sold here
_DIAG = {"guard_invocations": 0, "guard_extra_sells": 0, "guard_errors": 0, "items_sold": {}}


def _safe_sell_guard(chassis, action, view, route, step):
    """Re-implementation of chassis._budget_guard's sell-selection with FERTILIZER/WHEAT
    excluded from the candidate pool. Everything else (budget/shortfall math, item_need for
    the remaining items, ordering) is identical to the original method."""
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
            _DIAG["items_sold"][item] = _DIAG["items_sold"].get(item, 0) + qty
    if added:
        sells = [o for o in market if o and o[0] == "SELL"]
        others = [o for o in market if not (o and o[0] == "SELL")]
        action["market"] = sells + others


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
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
