# SPDX-License-Identifier: Apache-2.0
"""o002 sell governor (Claude lineage, 2026-09-14).

Evidence (79 live losses of c125/c129, exact lockstep price reconstruction):
per game we sold 92 MILK, 59 WOOL and 51 STRAWBERRY units below 25% of base
price; the winners sold fewer such units and realised ~15% higher average
prices on the same products.  Production volumes were equal or higher on our
side, so the deficit is market execution, not farming.

This overlay takes over the SELL orders for glut-sensitive products.  Every
step it decides, per product, how many shed units to sell from:
  * the exact engine price curve and the current market inventory,
  * known town consumption (unlocked shops + town centre) plus the expected
    consumption of shops still to be unlocked,
  * projected future supply from BOTH farms' visible animals and crops.
If the market is structurally oversupplied the stock is released early, before
the opponent can, down to a price floor; otherwise sales are dripped right
after the town consumption tick (step % 4 == 1) at prices near base.  Shed
capacity and the remaining days always bound how much can be held.

WHEAT and FERTILIZER are left to the parent.  Field actions, hires, purchases
and land are never changed.  Only public observations and the parent action
are used.
"""

import math as _o2_math

_O2_PARENT = agent
_O2_STATES = {}
_O2_REPORT = {}
del agent

_O2_GOVERNED = ("MILK", "WOOL", "STRAWBERRY", "MELON", "TOMATO", "EGG", "CARROT")
_O2_I0 = 10000
_O2_PARAMS = {
    "CARROT":     (35,  450, "hinge",  1.00, "sqrt",   0.70),
    "TOMATO":     (60,  200, "hinge",  0.40, "sqrt",   0.60),
    "STRAWBERRY": (120, 100, "sqrt",   0.70, "linear", 1.60),
    "MELON":      (250, 300, "log",    0.20, "sq",     3.60),
    "EGG":        (50,  332, "hinge",  0.40, "log",    0.20),
    "MILK":       (160, 122, "sqrt",   0.60, "linear", 1.60),
    "WOOL":       (200, 105, "log",    0.20, "sq",     3.20),
}
_O2_SHOPS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"), "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_O2_EXP_UNLOCK = {}
for _o2_item in _O2_PARAMS:
    _O2_EXP_UNLOCK[_o2_item] = sum(6.0 * (2 if len(v) == 1 else 1) for v in _O2_SHOPS.values() if _o2_item in v) / 8.0
_O2_ANIMALS = {"GOOSE": ("EGG", 4, 1, 4), "COW": ("MILK", 8, 2, 6), "SHEEP": ("WOOL", 6, 3, 6)}
_O2_CROPS = {"CARROT": (2, 3, 0, 4, False), "TOMATO": (8, 8, 1, 4, True), "STRAWBERRY": (10, 10, 2, 4, True), "MELON": (10, 12, 0, 6, False)}
_O2_HOLD_FRAC = 0.55        # never drip below this fraction of base while holding is still possible
_O2_DUMP_FRAC = 0.30        # in structural oversupply release down to this fraction (first seller wins)
_O2_FUTURE_WEIGHT = 0.8     # weight on expected consumption from shops not yet unlocked
_O2_MIN_ROOM = 34           # shed room to keep for the overnight inventory drop
_O2_FREE_STEP = 690         # from here the parent's terminal logic owns the market
_O2_MAX_HOLD_DAYS = 6.0     # never hold a unit longer than this
_O2_DRIP_MULT = 1.25        # sell this multiple of the per-tick town consumption per tick


def _o2_shape(func, x, T):
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return _o2_math.sqrt(x)
    if func == "log":
        return _o2_math.log(1.0 + x)
    if func == "hinge":
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def _o2_price(item, inv):
    base, T, bf, bt, af, at = _O2_PARAMS[item]
    if inv < _O2_I0:
        v = base + bt * base / _o2_shape(bf, T, T) * _o2_shape(bf, _O2_I0 - inv, T)
    else:
        v = base - at * base / _o2_shape(af, T, T) * _o2_shape(af, inv - _O2_I0, T)
    return max(1, int(round(v)))


def _o2_daily_consumption(item, shops, day):
    known = 1.0
    for s in shops:
        items = _O2_SHOPS.get(s, ())
        if item in items:
            known += 6.0 * (2 if len(items) == 1 else 1)
    k_seen = min(8, max(0, day) // 3)
    extra = max(0, k_seen - len(shops))
    return known, extra * _O2_EXP_UNLOCK[item] * _O2_FUTURE_WEIGHT


def _o2_future_supply(farm, item, day, eff):
    """Units of `item` this farm's visible tiles will still produce by day 28 (sale by 29)."""
    total = 0.0
    tiles = farm.get("tiles") or []
    for row in tiles:
        for t in row:
            if not isinstance(t, dict):
                continue
            if "animal" in t:
                prod, first, interval, max_held = _O2_ANIMALS[t["animal"]]
                if prod != item:
                    continue
                d = t["placed_day"] + first - 1
                units = 0.0
                firstprod = True
                while d <= 28:
                    if d >= day:
                        units += min(max_held, 1 + (d - t["placed_day"] + 1)) if firstprod else min(max_held, 1 + interval)
                    firstprod = False
                    d += interval
                total += units * eff + t.get("yield_units", 0)
            elif t.get("kind") == "PLANT" and t.get("crop") == item:
                first, maxday, interval, max_yield, ongoing = _O2_CROPS[item]
                p = t["planted_day"]
                if ongoing:
                    for k in range(max_yield):
                        pd = p + first - 1 + k * interval
                        if pd > 28:
                            break
                        if pd >= day - 1:
                            total += 1.3 * eff
                    total += t.get("yield_units", 0)
                else:
                    h = p + (first if item == "MELON" else maxday)
                    if h >= day - 1 and h <= 29:
                        total += (6 if item == "MELON" else 3) * eff
    return total


def _o2_incoming(obs, action, seat):
    """Units placed/dropped into the shed by this step's field actions (sellable this step)."""
    farm = obs["farms"][seat]
    priv = obs["private"]
    invs = priv.get("inventories") or []
    positions = [farm["farmer"]] + [list(h) for h in farm.get("hands", [])]
    cmds = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
    inc = {}
    shed_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
    for i, pos in enumerate(positions):
        if i >= len(cmds) or tuple(pos) not in shed_tiles:
            continue
        c = cmds[i]
        inv = invs[i] if i < len(invs) else {}
        if not c:
            continue
        if c[0] == "DROP":
            for k, v in inv.items():
                inc[k] = inc.get(k, 0) + v
        elif c[0] == "PLACE" and len(c) >= 2 and c[1] in inv and c[1] not in _O2_ANIMALS:
            n = int(c[2]) if len(c) >= 3 else 1
            inc[c[1]] = inc.get(c[1], 0) + min(n, inv.get(c[1], 0))
    return inc


def _o2_best_future(item, inv, cons_day, opp_day, days_left):
    """Best expected unit price over the next holdable days, assuming the town keeps
    consuming and the opponent keeps supplying at its projected daily rate."""
    best_p, best_h = _o2_price(item, inv), 0
    horizon = int(min(_O2_MAX_HOLD_DAYS, days_left))
    for h in range(1, horizon + 1):
        proj = inv - cons_day * h + opp_day * h
        pr = _o2_price(item, int(round(proj)))
        if pr > best_p:
            best_p, best_h = pr, h
    return best_p, best_h


def _o2_govern(obs, parent, state):
    step = int(obs["step"])
    if step >= _O2_FREE_STEP:
        return parent
    seat = int(obs["player"])
    day = step // 24
    farm = obs["farms"][seat]
    opp = obs["farms"][1 - seat]
    shed = dict(obs["private"].get("shed") or {})
    market_inv = obs["market"]["inventory"]
    shops = list(obs["town"].get("unlocked_shops") or [])
    orders = list(parent.get("market") or [])
    incoming = _o2_incoming(obs, parent, seat)
    days_left = max(0.0, (696 - step) / 24.0)
    shed_total = sum(shed.values()) + sum(incoming.values())

    kept = []
    parent_req = {}
    for o in orders:
        if isinstance(o, list) and len(o) == 3 and o[0] == "SELL" and o[1] in _O2_GOVERNED:
            parent_req[o[1]] = parent_req.get(o[1], 0) + int(o[2])
        else:
            kept.append(o)

    decisions = []   # (hold_gain_per_unit, item, avail, n_sell, price_now)
    ticks_left = max(1.0, (696 - step) / 4.0)
    for item in _O2_GOVERNED:
        avail = shed.get(item, 0) + incoming.get(item, 0)
        if avail <= 0:
            state["held_since"].pop(item, None)
            continue
        base = _O2_PARAMS[item][0]
        inv = int(market_inv[item])
        glut = inv - _O2_I0
        known, future = _o2_daily_consumption(item, shops, day)
        cons_day = known + future
        mine = _o2_future_supply(farm, item, day, 1.0)
        theirs = _o2_future_supply(opp, item, day, 0.8)
        opp_day = theirs / max(1.0, days_left)
        held_since = state["held_since"].setdefault(item, step)
        held_days = (step - held_since) / 24.0
        p_now = _o2_price(item, inv)
        best_p, best_h = _o2_best_future(item, inv + avail, cons_day, opp_day, days_left - held_days)
        gain = best_p - p_now
        # drip rate: at least the town's per-tick consumption, and fast enough to clear
        # everything we hold or will still produce before the final day
        cons_tick = cons_day / 6.0
        clear_rate = (avail + mine) / ticks_left
        rate = _o2_math.ceil(max(cons_tick * _O2_DRIP_MULT, clear_rate, 1.0))
        at_tick = (step % 4 == 1)
        if days_left <= 1.0 or held_days >= _O2_MAX_HOLD_DAYS:
            n = avail
        elif glut <= 0 and gain <= max(8.0, 0.12 * base):
            n = min(avail, rate) if at_tick else 0
        elif at_tick:
            n = min(avail, rate)
        else:
            n = 0
        # in scarcity never sell below the recovery target minus a margin
        if n > 0 and gain > max(8.0, 0.12 * base):
            floor = max(_O2_HOLD_FRAC * base, best_p - max(8.0, 0.12 * base))
            k = 0
            while k < n and _o2_price(item, inv + k) >= floor:
                k += 1
            n = k
        decisions.append([gain, item, avail, int(n), p_now])

    # shed room: release the least promising stock until the overnight inflow fits
    room = 100 - shed_total + sum(d[3] for d in decisions)
    if room < _O2_MIN_ROOM:
        for d in sorted(decisions, key=lambda d: d[0]):
            if room >= _O2_MIN_ROOM:
                break
            extra = min(d[2] - d[3], _O2_MIN_ROOM - room)
            if extra > 0:
                d[3] += extra
                room += extra
                state["room_forced"] += extra

    new_sells = []
    for gain, item, avail, n, p_now in decisions:
        if n > 0:
            new_sells.append([p_now * n, ["SELL", item, n]])
            state["units"][item] = state["units"].get(item, 0) + n
            if n >= avail:
                state["held_since"].pop(item, None)
        else:
            state["held"] += 1
        req = parent_req.get(item, 0)
        if req > n:
            state["cut_units"] += req - n
        elif req < n:
            state["added_units"] += n - req
    new_sells.sort(key=lambda x: -x[0])
    free = max(0, 10 - len(kept))
    chosen = new_sells[:free]
    for _, o in new_sells[free:]:
        state["deferred_no_slot"] += 1
        state["units"][o[1]] = state["units"].get(o[1], 0) - o[2]
        state["held_since"].setdefault(o[1], step)
    result = dict(parent)
    result["market"] = ([o for _, o in chosen] + kept)[:10]
    return result


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _O2_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _O2_STATES[seat] = {"last": -1, "held_since": {}, "units": {}, "gov_orders": 0, "held": 0,
                                    "cut_units": 0, "added_units": 0, "deferred_no_slot": 0, "room_forced": 0, "errors": 0}
    state["last"] = step
    parent = _O2_PARENT(observation, configuration)
    result = parent
    try:
        supported = configuration is None or all(configuration.get(key, value) == value for key, value in (
            ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100), ("maxMarketOrdersPerTurn", 10)))
        if supported and isinstance(parent, dict):
            result = _o2_govern(observation, parent, state)
    except Exception:
        state["errors"] += 1
        result = parent
    _O2_REPORT.clear()
    _O2_REPORT.update(getattr(_O2_PARENT, "telemetry", {}) or {})
    _O2_REPORT.update({"o2_" + k: v for k, v in state.items() if isinstance(v, int) and k != "last"})
    _O2_REPORT["o2_units"] = dict(state["units"])
    return result


agent.telemetry = _O2_REPORT
agent = globals().pop("agent")
