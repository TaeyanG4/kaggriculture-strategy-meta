"""Kaggriculture baseline v0: compact mixed-crop farm for local benchmarking.

Independent standard-library implementation against the published Kaggriculture
observation/action interface. The goal is a reproducible first rung above the
built-in one-tile starter, not a leaderboard-ready final strategy.
"""

BOARD = 10
HALF = 5
SHED = (4, 4)

CROPS = {
    "WHEAT": {"seed_cost": 10, "first": 2, "max_day": 4, "ongoing": False},
    "CARROT": {"seed_cost": 20, "first": 2, "max_day": 3, "ongoing": False},
    "TOMATO": {"seed_cost": 50, "first": 8, "max_day": 8, "ongoing": True},
}

SEED_TARGET = {"WHEAT": 8, "CARROT": 6, "TOMATO": 4}
PRICE_FLOOR = {"WHEAT": 10, "CARROT": 15, "TOMATO": 25}
SELL_ORDER = ["TOMATO", "CARROT", "WHEAT"]


def _dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _step_toward(pos, target):
    x, y = pos
    tx, ty = target
    if x < tx:
        return ["EAST"]
    if x > tx:
        return ["WEST"]
    if y < ty:
        return ["SOUTH"]
    if y > ty:
        return ["NORTH"]
    return ["PASS"]


def _desired_crop(x, y):
    """Static 50/30/20-ish crop mix for the starting 5x5 quadrant."""
    slot = (y * HALF + x) % 10
    if slot < 5:
        return "WHEAT"
    if slot < 8:
        return "CARROT"
    return "TOMATO"


def _ready(tile, day):
    crop = tile.get("crop")
    info = CROPS.get(crop)
    if info is None or tile.get("yield_units", 0) <= 0:
        return False
    age = day - tile.get("planted_day", day)
    if age < info["first"]:
        return False
    if info["ongoing"]:
        return True
    return age >= info["max_day"]


def _planting_open(crop, day):
    if crop == "TOMATO":
        return day <= 19
    return day <= 25


def _collect_jobs(obs, me, private):
    day = obs.get("day", 0)
    tiles = me["tiles"]
    seeds = dict(private.get("seeds", {}))
    harvest = []
    water = []
    dig = []
    plant = []

    # Existing assets first. Each tile produces at most one job this turn so two
    # workers never waste actions on the same plant simultaneously.
    for y in range(BOARD):
        for x in range(BOARD):
            tile = tiles[y][x]
            if tile == "LOCKED" or tile is None:
                continue
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "WEED":
                dig.append(((x, y), ["DIG"]))
                continue
            if tile.get("kind") != "PLANT":
                continue
            if _ready(tile, day):
                harvest.append(((x, y), ["HARVEST"]))
            elif day < 29 and not tile.get("watered_today", False):
                water.append(((x, y), ["WATER"]))

    # Refill the starting quadrant according to a stable coordinate pattern.
    # Virtual seed accounting avoids scheduling more same-turn PLANT jobs than
    # the observation says are actually available.
    if day <= 25:
        empties = []
        for y in range(HALF):
            for x in range(HALF):
                if tiles[y][x] is None:
                    empties.append((x, y))
        empties.sort(key=lambda pos: (_dist(pos, SHED), pos[1], pos[0]))
        for x, y in empties:
            crop = _desired_crop(x, y)
            if not _planting_open(crop, day) or seeds.get(crop, 0) <= 0:
                continue
            plant.append(((x, y), ["PLANT", crop]))
            seeds[crop] = seeds.get(crop, 0) - 1

    # Harvest before watering: bank mature inventory and free one-time crop tiles.
    # Weed cleanup precedes new planting so the field does not slowly lose capacity.
    return harvest + water + dig + plant


def _assign_units(obs, me, private, jobs):
    positions = [tuple(me["farmer"])] + [tuple(p) for p in me.get("hands", [])]
    inventories = private.get("inventories", [])
    actions = [["PASS"] for _ in positions]
    busy = [False for _ in positions]
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)

    # Harvested goods carried into the final hours have no value unless banked.
    # Also relay a heavily loaded worker late in ordinary days to avoid inventory
    # pressure; wheat is a sale crop in this crop-only baseline, so all load counts.
    for index, pos in enumerate(positions):
        inv = inventories[index] if index < len(inventories) else {}
        load = sum(int(v or 0) for v in inv.values())
        should_drop = (day >= 29 and hour >= 10 and load > 0) or (hour >= 20 and load >= 12)
        if not should_drop:
            continue
        busy[index] = True
        actions[index] = ["DROP"] if pos == SHED else _step_toward(pos, SHED)

    remaining = list(jobs)
    while remaining:
        best = None
        for job_index, (target, op) in enumerate(remaining):
            for unit_index, pos in enumerate(positions):
                if busy[unit_index]:
                    continue
                distance = _dist(pos, target)
                key = (distance, job_index, unit_index)
                if best is None or key < best[0]:
                    best = (key, job_index, unit_index, target, op)
        if best is None:
            break
        _, job_index, unit_index, target, op = best
        del remaining[job_index]
        busy[unit_index] = True
        actions[unit_index] = op if positions[unit_index] == target else _step_toward(positions[unit_index], target)

    return actions


def _market_orders(obs, me, private):
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    money = float(me.get("money", 0))
    shed = private.get("shed", {})
    seeds = private.get("seeds", {})
    prices = (obs.get("market", {}) or {}).get("prices", {})
    orders = []

    shed_load = sum(int(v or 0) for v in shed.values())
    force_sell = shed_load >= 70 or day >= 28
    for item in SELL_ORDER:
        have = int(shed.get(item, 0) or 0)
        if have <= 0:
            continue
        price = float(prices.get(item, 0) or 0)
        if force_sell or price >= PRICE_FLOOR[item]:
            orders.append(["SELL", item, min(have, 30)])
        if len(orders) >= 3:
            break

    # Cheap labour is the main improvement over the official starter. Hire early
    # each day; all four orders still leave room in the ten-order market queue.
    if day < 29 and hour <= 1:
        missing = max(0, 4 - int(me.get("hires_today", 0) or 0))
        for _ in range(min(missing, 4)):
            orders.append(["HIRE"])

    # Keep only a small working seed stock. Orders execute before unit actions but
    # newly bought seed is intentionally not assumed available until the next turn.
    if day <= 25:
        for crop in ("WHEAT", "CARROT", "TOMATO"):
            if not _planting_open(crop, day):
                continue
            have = int(seeds.get(crop, 0) or 0)
            target = SEED_TARGET[crop]
            gap = target - have
            if gap <= 0:
                continue
            buy = min(gap, 6)
            cost = CROPS[crop]["seed_cost"] * buy
            if money >= cost + 100:
                orders.append(["BUY_SEED", crop, buy])
                money -= cost
            if len(orders) >= 10:
                break

    return orders[:10]


def agent(obs):
    farms = obs.get("farms", [])
    player = int(obs.get("player", 0) or 0)
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}

    me = farms[player]
    private = obs.get("private", {}) or {}
    jobs = _collect_jobs(obs, me, private)
    unit_actions = _assign_units(obs, me, private, jobs)
    market = _market_orders(obs, me, private)
    return {
        "farmer": unit_actions[0] if unit_actions else ["PASS"],
        "hands": unit_actions[1:],
        "market": market,
    }
