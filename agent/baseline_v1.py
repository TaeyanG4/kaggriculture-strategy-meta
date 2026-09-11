"""Kaggriculture baseline v1: two-quadrant mixed-crop farm.

Independent standard-library agent. Compared with baseline_v0, this version tests
one specific hypothesis: does buying the first extra quadrant early and scaling
cheap labor clear the authored tier-3 reference rung?
"""

BOARD = 10
HALF = 5
SHED_TILES = ((4, 4), (5, 4), (4, 5), (5, 5))

CROPS = {
    "WHEAT": {"seed_cost": 10, "first": 2, "max_day": 4, "ongoing": False},
    "CARROT": {"seed_cost": 20, "first": 2, "max_day": 3, "ongoing": False},
    "TOMATO": {"seed_cost": 50, "first": 8, "max_day": 8, "ongoing": True},
}

SEED_TARGET = {"WHEAT": 16, "CARROT": 10, "TOMATO": 6}
PRICE_FLOOR = {"WHEAT": 10, "CARROT": 15, "TOMATO": 25}
SELL_ORDER = ("TOMATO", "CARROT", "WHEAT")


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


def _shed_tile(tiles):
    for pos in SHED_TILES:
        x, y = pos
        if tiles[y][x] != "LOCKED":
            return pos
    return (4, 4)


def _desired_crop(x, y):
    # 50/30/20 coordinate cycle, stable across both northern quadrants.
    slot = (y * BOARD + x) % 10
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
    return day <= (19 if crop == "TOMATO" else 25)


def _collect_jobs(obs, me, private):
    day = obs.get("day", 0)
    tiles = me["tiles"]
    seeds = dict(private.get("seeds", {}))
    harvest = []
    water = []
    dig = []
    plant = []

    for y in range(BOARD):
        for x in range(BOARD):
            tile = tiles[y][x]
            if tile == "LOCKED" or tile is None or not isinstance(tile, dict):
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

    if day <= 25:
        shed_pos = _shed_tile(tiles)
        empties = []
        for y in range(BOARD):
            for x in range(BOARD):
                if tiles[y][x] is None:
                    empties.append((x, y))
        empties.sort(key=lambda pos: (_dist(pos, shed_pos), pos[1], pos[0]))
        for x, y in empties:
            crop = _desired_crop(x, y)
            if not _planting_open(crop, day) or seeds.get(crop, 0) <= 0:
                continue
            plant.append(((x, y), ["PLANT", crop]))
            seeds[crop] = seeds.get(crop, 0) - 1

    return harvest + water + dig + plant


def _assign_units(obs, me, private, jobs):
    tiles = me["tiles"]
    shed_pos = _shed_tile(tiles)
    positions = [tuple(me["farmer"])] + [tuple(p) for p in me.get("hands", [])]
    inventories = private.get("inventories", [])
    actions = [["PASS"] for _ in positions]
    busy = [False for _ in positions]
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)

    for index, pos in enumerate(positions):
        inv = inventories[index] if index < len(inventories) else {}
        load = sum(int(v or 0) for v in inv.values())
        should_drop = (day >= 29 and hour >= 8 and load > 0) or (hour >= 19 and load >= 10)
        if not should_drop:
            continue
        busy[index] = True
        actions[index] = ["DROP"] if pos == shed_pos else _step_toward(pos, shed_pos)

    remaining = list(jobs)
    while remaining:
        best = None
        for job_index, (target, op) in enumerate(remaining):
            for unit_index, pos in enumerate(positions):
                if busy[unit_index]:
                    continue
                key = (_dist(pos, target), job_index, unit_index)
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
    force_sell = shed_load >= 65 or day >= 28
    for item in SELL_ORDER:
        have = int(shed.get(item, 0) or 0)
        price = float(prices.get(item, 0) or 0)
        if have > 0 and (force_sell or price >= PRICE_FLOOR[item]):
            orders.append(["SELL", item, min(have, 35)])
        if len(orders) >= 3:
            break

    # Six hands from day 0, then eight once the second quadrant is established.
    target_hands = 6 if day < 4 else 8
    if day < 29 and hour <= 1:
        missing = max(0, target_hands - int(me.get("hires_today", 0) or 0))
        for _ in range(min(missing, target_hands)):
            if len(orders) >= 10:
                break
            orders.append(["HIRE"])

    # Buy exactly one extra quadrant while capital is abundant enough to seed it.
    if day <= 8 and len(me.get("unlocked_quadrants", [])) < 2 and money >= 1600 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        money -= 1000

    if day <= 25:
        for crop in ("WHEAT", "CARROT", "TOMATO"):
            if len(orders) >= 10 or not _planting_open(crop, day):
                continue
            have = int(seeds.get(crop, 0) or 0)
            gap = SEED_TARGET[crop] - have
            if gap <= 0:
                continue
            buy = min(gap, 8)
            cost = CROPS[crop]["seed_cost"] * buy
            if money >= cost + 150:
                orders.append(["BUY_SEED", crop, buy])
                money -= cost
    return orders[:10]


def agent(obs):
    farms = obs.get("farms", [])
    player = int(obs.get("player", 0) or 0)
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    me = farms[player]
    private = obs.get("private", {}) or {}
    jobs = _collect_jobs(obs, me, private)
    actions = _assign_units(obs, me, private, jobs)
    return {
        "farmer": actions[0] if actions else ["PASS"],
        "hands": actions[1:],
        "market": _market_orders(obs, me, private),
    }
