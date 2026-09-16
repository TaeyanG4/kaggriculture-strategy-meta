# SPDX-License-Identifier: Apache-2.0
"""o003 tomato program (Claude lineage, 2026-09-14).

Evidence: in 14 of the 79 recorded live losses the TOMATO price peaked above
$180 (hinge scarcity from PIZZA_SHOP / FARMERS_MARKET demand) and in 12 of
them neither player sold a single tomato.  The parent's own tomato investment
(V219) only fires on day 18 with three tomato shops and 12,000 cash, so this
demand is almost always left unserved.

This overlay runs an earlier, demand-sized tomato program on the idle SE
quadrant: when at least two tomato-consuming shops are open by day 10-14, it
buys the SE land, hires dedicated hands, plants a demand-sized block of
tomatoes, waters daily, fertilizes ahead of the production days (doubling
yield), harvests, delivers and sells.  Field commands of the parent's own
hands are never touched; only the extra hands it requests are controlled.
Only public observations, the parent action and its own route are used.
"""

import copy as _o3_copy

_O3_PARENT = agent
_O3_STATES = {}
_O3_REPORT = {}
del agent

_O3_TOMATO_SHOPS = ("PIZZA_SHOP", "FARMERS_MARKET")
_O3_SE_TILES = [(x, y) for y in (5, 6, 7, 8, 9) for x in range(5, 10)]
_O3_HOME = ((4, 4), (5, 4), (4, 5), (5, 5))
_O3_MIN_DAY = 10          # after the parent's own land purchases (steps 150 / ~220)
_O3_MAX_DAY = 16          # planting later cannot finish four productions before day 29
_O3_MIN_SHOPS = 2
_O3_RESERVE = 3000
_O3_SEED = 50
_O3_LAND = 4000
_O3_MAX_TILES = 20
_O3_MIN_TILES = 8
_O3_TILES_PER_PLANTER = 6


def _o3_fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _o3_walk(pos, target):
    x, y = pos
    tx, ty = target
    if x != tx:
        return ["EAST" if x < tx else "WEST"]
    if y != ty:
        return ["SOUTH" if y < ty else "NORTH"]
    return None


def _o3_home(pos):
    return min(_O3_HOME, key=lambda p: abs(pos[0] - p[0]) + abs(pos[1] - p[1]))


def _o3_tomato_demand(shops, day):
    known = 1.0
    for s in shops:
        if s in _O3_TOMATO_SHOPS:
            known += 6.0
    k_seen = min(8, day // 3)
    extra = max(0, k_seen - len(shops))
    return known + extra * 1.5 * 0.8


def _o3_price(deficit):
    """Tomato price at a market deficit (hinge below, sqrt above)."""
    if deficit >= 0:
        u = deficit / 200.0
        return max(1, int(round(60 + 0.4 * 60 * (u + 8.0 * max(0.0, u - 1.0) ** 2))))
    x = -deficit
    return max(1, int(round(60 - 0.6 * 60 / (200 ** 0.5) * (x ** 0.5))))


def _o3_plan_size(obs, day):
    """Number of tiles worth planting, from projected demand at harvest time."""
    shops = list(obs["town"].get("unlocked_shops") or [])
    cons = _o3_tomato_demand(shops, day)
    opp = obs["farms"][1 - int(obs["player"])]
    me = obs["farms"][int(obs["player"])]
    rival_tiles = sum(1 for row in opp["tiles"] for t in row if isinstance(t, dict) and t.get("crop") == "TOMATO")
    own_tiles = sum(1 for row in me["tiles"] for t in row if isinstance(t, dict) and t.get("crop") == "TOMATO")
    inv = int(obs["market"]["inventory"]["TOMATO"])
    deficit_now = 10000 - inv
    # deficit at first harvest: eight more days of consumption minus the rival's visible supply
    deficit_h = deficit_now + cons * 8 - rival_tiles * 4 - own_tiles * 4
    price_h = _o3_price(deficit_h)
    # size the block so that four fertilised production days do not glut the market:
    # daily supply from the block (2 units/tile/day) should stay near the daily demand
    tiles = int(round(cons * 0.6))
    tiles = max(_O3_MIN_TILES, min(_O3_MAX_TILES, tiles))
    # value gate: 6 units/tile at the harvest-time price minus seed, fertilizer share and labor
    fert_price = min(120, int(obs["market"]["prices"]["FERTILIZER"]) + 10)
    value = 6.0 * min(price_h, 400) - _O3_SEED - 2 * fert_price - 90.0
    return tiles, value, price_h, cons


def _o3_qualifies(obs, state, day):
    farm = obs["farms"][int(obs["player"])]
    shops = list(obs["town"].get("unlocked_shops") or [])
    if sum(1 for s in shops if s in _O3_TOMATO_SHOPS) < _O3_MIN_SHOPS:
        return None
    if len(farm["tiles"]) != 10:
        return None
    if "SE" in farm["unlocked_quadrants"]:
        return None
    if any(farm["tiles"][y][x] != "LOCKED" for x, y in _O3_SE_TILES):
        return None
    tiles, value, price_h, cons = _o3_plan_size(obs, day)
    if value <= 150:
        state["value_declines"] += 1
        return None
    return tiles, value, price_h


def _o3_request_hires(obs, action, state, count):
    """Append `count` HIRE orders if the parent's day plan will not hire again today."""
    step = int(obs["step"])
    day = step // 24
    offset = step % 24
    farm = obs["farms"][int(obs["player"])]
    native = _IMPL.chassis.players[int(obs["player"])]
    tape = _IMPL.chassis.routes[native["route"]]
    planned = tape[day * 24:min((day + 1) * 24, 719)]
    remaining = planned[offset + 1:]
    if any(o and o[0] == "HIRE" for a in remaining for o in a.get("market", [])):
        return None
    parent_hires = sum(bool(o) and o[0] == "HIRE" for o in action["market"])
    expected = max(len(a.get("hands", [])) for a in planned) if planned else len(farm["hands"])
    if len(farm["hands"]) + parent_hires != expected:
        return None
    if len(action["market"]) + count > 10:
        return None
    cost = sum(_o3_fib(n) for n in range(farm["hires_today"] + parent_hires, farm["hires_today"] + parent_hires + count))
    return expected + 1, cost


def _o3_budget(obs, action):
    total = 0
    for order in action["market"]:
        if not order:
            continue
        if order[0] == "BUY_PRODUCT":
            total += int(order[2]) * (int(obs["market"]["prices"][order[1]]) + 10)
        elif order[0] == "BUY_ANIMAL":
            total += int(order[2]) * {"COW": 400, "SHEEP": 500, "GOOSE": 300}[order[1]]
        elif order[0] == "BUY_SEED":
            total += int(order[2]) * {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}[order[1]]
        elif order[0] == "BUY_LAND":
            total += 4000
    return total


def _o3_worker(obs, state, actor, role):
    step = int(obs["step"])
    day = step // 24
    farm = obs["farms"][int(obs["player"])]
    priv = obs["private"]
    positions = [farm["farmer"]] + [list(h) for h in farm["hands"]]
    if actor >= len(positions):
        return ["PASS"]
    pos = tuple(positions[actor])
    invs = priv.get("inventories") or []
    inv = invs[actor] if actor < len(invs) else {}
    tiles = farm["tiles"]
    # fertilizer loading at the shed
    if role.get("needs_fertilizer") and not role.get("loaded"):
        home = _o3_home(pos)
        walk = _o3_walk(pos, home)
        if walk:
            return walk
        want = role.get("fert_qty", len(role["targets"]))
        if inv.get("FERTILIZER", 0) >= want or role.get("pickup_requested"):
            role["loaded"] = True
        elif priv["shed"].get("FERTILIZER", 0) > 0:
            role["pickup_requested"] = True
            return ["PICKUP", "FERTILIZER", min(want, priv["shed"].get("FERTILIZER", 0))]
        else:
            role["loaded"] = True
    todo = []
    for target in role["targets"]:
        x, y = target
        tile = tiles[y][x]
        tomato = isinstance(tile, dict) and tile.get("crop") == "TOMATO"
        command = None
        if tomato:
            if target not in state["seen_plants"]:
                state["seen_plants"].add(target)
                state["confirmed_plants"] += 1
            decaying = tile.get("max_lifespan_step", -1) >= 0 and step >= tile["max_lifespan_step"]
            if tile.get("yield_units", 0) > 0 and (tile.get("yield_units", 0) >= 2 or decaying or day >= 28 or tile.get("watered_today")):
                command = ["HARVEST"]
            elif day < 29 and not tile.get("watered_today") and not decaying:
                command = ["WATER"]
            elif role.get("needs_fertilizer") and inv.get("FERTILIZER", 0) > 0 and tile.get("fertilized_until_day", -1) < day and not decaying:
                command = ["FERTILIZE"]
            elif tile.get("yield_units", 0) > 0:
                command = ["HARVEST"]
        elif state["phase"] == "plant":
            if tile is None and priv["seeds"].get("TOMATO", 0) > 0:
                command = ["PLANT", "TOMATO"]
            elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                command = ["DIG"]
        elif target in state["seen_plants"] and isinstance(tile, dict) and tile.get("kind") == "WEED":
            command = ["DIG"]
        if command:
            todo.append((target, command))
    home = _o3_home(pos)
    distance = abs(pos[0] - home[0]) + abs(pos[1] - home[1])
    if step >= 718 - distance and inv.get("TOMATO", 0):
        return _o3_walk(pos, home) or ["PLACE", "TOMATO", int(inv["TOMATO"])]
    # deliver a full cargo mid-day so it can be sold today
    if inv.get("TOMATO", 0) >= 8 and step % 24 <= 20:
        return _o3_walk(pos, home) or ["PLACE", "TOMATO", int(inv["TOMATO"])]
    if todo:
        # watering/harvest sweep in target order from the current position
        target, command = min(todo, key=lambda v: (abs(pos[0] - v[0][0]) + abs(pos[1] - v[0][1]), role["targets"].index(v[0])))
        # water must not be skipped: plants unwatered two days running die overnight
        return _o3_walk(pos, target) or command
    if inv.get("TOMATO", 0):
        return _o3_walk(pos, home) or ["PLACE", "TOMATO", int(inv["TOMATO"])]
    if any(v for k, v in inv.items() if k != "FERTILIZER"):
        return _o3_walk(pos, home) or ["DROP"]
    return ["PASS"]


def _o3_step(obs, action, state):
    step = int(obs["step"])
    day = step // 24
    offset = step % 24
    player = int(obs["player"])
    farm = obs["farms"][player]
    priv = obs["private"]
    if state["day"] != day:
        state["day"] = day
        state["workers"] = {}
        state["requested_day"] = -1
    # ---- commitment ----
    if not state["committed"]:
        if day < _O3_MIN_DAY or day > _O3_MAX_DAY or offset > 4:
            return action
        q = _o3_qualifies(obs, state, day)
        if q is None:
            return action
        tiles, value, price_h = q
        planters = max(1, min(4, (tiles + _O3_TILES_PER_PLANTER - 1) // _O3_TILES_PER_PLANTER))
        hires = _o3_request_hires(obs, action, state, planters)
        if hires is None:
            state["hire_blocked"] += 1
            return action
        first_actor, hire_cost = hires
        need = _O3_LAND + tiles * _O3_SEED + hire_cost + _o3_budget(obs, action) + _O3_RESERVE
        if farm["money"] < need:
            state["budget_declines"] += 1
            return action
        state["committed"] = True
        state["plant_day"] = day
        state["tiles"] = tiles
        state["targets"] = _O3_SE_TILES[:tiles]
        state["phase"] = "plant"
        state["value_estimate"] = value
        state["price_estimate"] = price_h
        state["pending"] = {"first_actor": first_actor, "count": planters}
        changed = _o3_copy.deepcopy(action)
        changed["market"] += [["BUY_LAND"], ["BUY_SEED", "TOMATO", tiles]] + [["HIRE"] for _ in range(planters)]
        state["requested_day"] = day
        return changed
    # ---- daily hire request (hour 0..3) ----
    plant_day = state["plant_day"]
    age = day - plant_day
    if state["requested_day"] != day and offset <= 3 and day <= 29:
        harvest_days = age >= 7
        fert_day = age in (7, 10)
        if state["phase"] == "plant" and age >= 1:
            state["phase"] = "grow"
        count = 2 if not harvest_days else 3
        if state["tiles"] >= 16:
            count += 1
        if day == 29:
            count = 3
        hires = _o3_request_hires(obs, action, state, count)
        if hires is None:
            state["hire_blocked"] += 1
        else:
            first_actor, hire_cost = hires
            extra = [["HIRE"] for _ in range(count)]
            fert_needed = 0
            if fert_day:
                fert_needed = max(0, state["tiles"] - priv["shed"].get("FERTILIZER", 0))
                fp = int(obs["market"]["prices"]["FERTILIZER"])
                if fert_needed > 0 and fp <= 140 and len(action["market"]) + len(extra) < 10:
                    extra.append(["BUY_PRODUCT", "FERTILIZER", fert_needed])
                else:
                    fert_needed = 0
            need = hire_cost + _o3_budget(obs, action) + fert_needed * (int(obs["market"]["prices"]["FERTILIZER"]) + 10) + 300
            if farm["money"] >= need and len(action["market"]) + len(extra) <= 10:
                state["pending"] = {"first_actor": first_actor, "count": count, "fertilizer": fert_day}
                state["requested_day"] = day
                changed = _o3_copy.deepcopy(action)
                changed["market"] += extra
                action = changed
            else:
                state["budget_declines"] += 1
    # ---- confirm hires -> assign roles ----
    pending = state.pop("pending", None)
    if pending:
        if len(farm["hands"]) + 1 >= pending["first_actor"] + pending["count"] and "SE" in farm["unlocked_quadrants"]:
            targets = state["targets"]
            n = pending["count"]
            per = (len(targets) + n - 1) // n
            for i in range(n):
                part = targets[i * per:(i + 1) * per]
                if not part:
                    continue
                state["workers"][pending["first_actor"] + i] = {
                    "targets": part, "needs_fertilizer": bool(pending.get("fertilizer")), "fert_qty": len(part)}
            state["confirmed_workers"] += n
        else:
            state["hire_shortfalls"] += 1
    # ---- drive workers ----
    if state["workers"]:
        commands = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        commands += [["PASS"] for _ in range(len(farm["hands"]) + 1 - len(commands))]
        for actor, role in state["workers"].items():
            if actor >= len(commands):
                continue
            command = _o3_worker(obs, state, actor, role)
            commands[actor] = command
            key = {"PLANT": "plant_requests", "WATER": "water_requests", "FERTILIZE": "fertilize_requests",
                   "HARVEST": "harvest_requests"}.get(command[0])
            if key:
                state[key] += 1
        action = _o3_copy.deepcopy(action)
        action["farmer"], action["hands"] = commands[0], commands[1:len(farm["hands"]) + 1]
    # ---- sell tomatoes that are (or will be, after this step's field actions) in the shed ----
    if len(action["market"]) < 10 and not any(o and o[:2] == ["SELL", "TOMATO"] for o in action["market"]):
        try:
            quantity = int(projected_shed(action, FarmView(obs)).get("TOMATO", 0))
        except Exception:
            quantity = int(priv["shed"].get("TOMATO", 0))
        if quantity > 0:
            action = _o3_copy.deepcopy(action)
            action["market"].insert(0, ["SELL", "TOMATO", quantity])
            state["sale_units"] += quantity
    return action


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _O3_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _O3_STATES[seat] = {
            "last": -1, "day": -1, "committed": False, "workers": {}, "seen_plants": set(), "targets": [],
            "tiles": 0, "phase": "", "plant_day": -1, "requested_day": -1, "value_declines": 0,
            "budget_declines": 0, "hire_blocked": 0, "hire_shortfalls": 0, "confirmed_workers": 0,
            "confirmed_plants": 0, "plant_requests": 0, "water_requests": 0, "fertilize_requests": 0,
            "harvest_requests": 0, "sale_units": 0, "errors": 0, "value_estimate": 0, "price_estimate": 0}
    state["last"] = step
    parent = _O3_PARENT(observation, configuration)
    result = parent
    try:
        supported = configuration is None or all(configuration.get(key, value) == value for key, value in (
            ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100), ("maxMarketOrdersPerTurn", 10)))
        if supported and isinstance(parent, dict):
            result = _o3_step(observation, parent, state)
    except Exception:
        state["errors"] += 1
        result = parent
    _O3_REPORT.clear()
    _O3_REPORT.update(getattr(_O3_PARENT, "telemetry", {}) or {})
    _O3_REPORT.update({"o3_" + k: v for k, v in state.items() if isinstance(v, (int, float)) and k not in ("last", "day")})
    _O3_REPORT["o3_committed"] = state["committed"]
    return result


agent.telemetry = _O3_REPORT
agent = globals().pop("agent")
