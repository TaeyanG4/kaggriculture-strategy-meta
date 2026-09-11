"""Kaggriculture baseline v2: goose + feed-chain experiment.

Independent standard-library agent. V2 keeps the v1 two-quadrant crop economy but
replaces part of the field with a small cared goose flock. The hypothesis is that
fast, daily egg yield and the deep egg market can cross the livestock reference rung
without depending on saturated milk/wool markets.
"""

BOARD = 10
SHED_TILES = ((4, 4), (5, 4), (4, 5), (5, 5))
PRODUCTS = ("EGG", "CARROT", "WHEAT")

CROPS = {
    "WHEAT": {"seed_cost": 10, "first": 2, "max_day": 4},
    "CARROT": {"seed_cost": 20, "first": 2, "max_day": 3},
}

TARGET_GEESE = 10
TARGET_COOPS = 10
SEED_TARGET = {"WHEAT": 18, "CARROT": 10}
SELL_FLOOR = {"EGG": 35, "CARROT": 15, "WHEAT": 12}


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
    for x, y in SHED_TILES:
        if tiles[y][x] != "LOCKED":
            return (x, y)
    return (4, 4)


def _crop_for(x, y):
    # Feed-heavy field with a smaller cash-crop stripe.
    return "WHEAT" if (x + 2 * y) % 5 < 3 else "CARROT"


def _crop_ready(tile, day):
    crop = tile.get("crop")
    info = CROPS.get(crop)
    if info is None or tile.get("yield_units", 0) <= 0:
        return False
    return day - tile.get("planted_day", day) >= info["max_day"]


def _inventory(private, index):
    invs = private.get("inventories", [])
    return invs[index] if index < len(invs) else {}


def _count_owned_geese(me, private):
    total = int((private.get("shed", {}) or {}).get("GOOSE", 0) or 0)
    total += sum(int(inv.get("GOOSE", 0) or 0) for inv in private.get("inventories", []))
    for row in me["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal") == "GOOSE":
                total += 1
    return total


def _collect_jobs(obs, me, private):
    day = obs.get("day", 0)
    tiles = me["tiles"]
    shed = private.get("shed", {}) or {}
    inventories = private.get("inventories", [])
    shed_pos = _shed_tile(tiles)

    feed = []
    harvest_animals = []
    care = []
    empty_coops = []
    coop_count = 0
    harvest_crops = []
    water = []
    dig = []

    for y in range(BOARD):
        for x in range(BOARD):
            tile = tiles[y][x]
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            pos = (x, y)
            if kind == "WEED":
                dig.append({"pos": pos, "op": ["DIG"], "need": None})
            elif kind == "PLANT":
                if _crop_ready(tile, day):
                    harvest_crops.append({"pos": pos, "op": ["HARVEST"], "need": None})
                elif day < 29 and not tile.get("watered_today", False):
                    water.append({"pos": pos, "op": ["WATER"], "need": None})
            elif kind == "COOP":
                coop_count += 1
                if tile.get("animal") != "GOOSE":
                    empty_coops.append(pos)
                    continue
                if not tile.get("fed_today", False):
                    feed.append({"pos": pos, "op": ["FEED"], "need": ("WHEAT", 1)})
                if tile.get("yield_units", 0) > 0:
                    harvest_animals.append({"pos": pos, "op": ["HARVEST"], "need": None})
                if not tile.get("cared_today", False):
                    care.append({"pos": pos, "op": ["CARE"], "need": None})

    carried_wheat = sum(int(inv.get("WHEAT", 0) or 0) for inv in inventories)
    feed_shortfall = max(0, len(feed) - carried_wheat)
    pickup_feed = []
    feed_available = int(shed.get("WHEAT", 0) or 0)
    if feed_shortfall > 0 and feed_available > 0:
        carrier_count = max(1, min(4, len(me.get("hands", [])) // 2 + 1))
        trips = min(carrier_count, max(1, (feed_shortfall + 3) // 4))
        for _ in range(trips):
            qty = min(4, feed_available)
            if qty <= 0:
                break
            pickup_feed.append({"pos": shed_pos, "op": ["PICKUP", "WHEAT", qty], "need": None, "skip": "WHEAT"})
            feed_available -= qty

    carried_geese = sum(int(inv.get("GOOSE", 0) or 0) for inv in inventories)
    geese_in_shed = int(shed.get("GOOSE", 0) or 0)
    place = [
        {"pos": pos, "op": ["PLACE", "GOOSE"], "need": ("GOOSE", 1)}
        for pos in empty_coops[: carried_geese + geese_in_shed]
    ]
    pickup_geese = []
    if geese_in_shed > carried_geese and empty_coops:
        pickup_geese.append(
            {
                "pos": shed_pos,
                "op": ["PICKUP", "GOOSE", min(4, geese_in_shed)],
                "need": None,
                "skip": "GOOSE",
            }
        )

    build = []
    if day <= 12 and coop_count < TARGET_COOPS:
        empties = []
        for y in range(BOARD):
            for x in range(BOARD):
                if tiles[y][x] is None:
                    empties.append((x, y))
        empties.sort(key=lambda p: (_dist(p, shed_pos), p[1], p[0]))
        room = min(TARGET_COOPS - coop_count, len(empties))
        build = [{"pos": pos, "op": ["BUILD_COOP"], "need": None} for pos in empties[:room]]

    plant = []
    if day <= 25:
        seeds = dict(private.get("seeds", {}) or {})
        empties = []
        for y in range(BOARD):
            for x in range(BOARD):
                if tiles[y][x] is None:
                    empties.append((x, y))
        empties.sort(key=lambda p: (_dist(p, shed_pos), p[1], p[0]))
        # Reserve near-shed empty tiles for still-missing coops.
        reserve = max(0, TARGET_COOPS - coop_count)
        for x, y in empties[reserve:]:
            crop = _crop_for(x, y)
            if seeds.get(crop, 0) <= 0:
                continue
            plant.append({"pos": (x, y), "op": ["PLANT", crop], "need": None})
            seeds[crop] -= 1

    return pickup_feed + feed + pickup_geese + place + harvest_animals + care + harvest_crops + water + dig + build + plant


def _assign(obs, me, private, jobs):
    tiles = me["tiles"]
    shed_pos = _shed_tile(tiles)
    positions = [tuple(me["farmer"])] + [tuple(p) for p in me.get("hands", [])]
    inventories = private.get("inventories", [])
    actions = [["PASS"] for _ in positions]
    busy = [False for _ in positions]
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)

    # Bank harvested products early enough to sell again the same day.
    for i, pos in enumerate(positions):
        inv = _inventory(private, i)
        product_load = sum(int(inv.get(item, 0) or 0) for item in ("EGG", "CARROT"))
        if product_load <= 0:
            continue
        if not (hour >= 12 or product_load >= 6 or day >= 29):
            continue
        busy[i] = True
        actions[i] = ["DROP"] if pos == shed_pos else _step_toward(pos, shed_pos)

    remaining = list(jobs)
    while remaining:
        best = None
        for j, job in enumerate(remaining):
            need = job.get("need")
            skip = job.get("skip")
            for i, pos in enumerate(positions):
                if busy[i]:
                    continue
                inv = _inventory(private, i)
                if need and int(inv.get(need[0], 0) or 0) < need[1]:
                    continue
                if skip and int(inv.get(skip, 0) or 0) > 0:
                    continue
                key = (_dist(pos, job["pos"]), j, i)
                if best is None or key < best[0]:
                    best = (key, j, i, job)
        if best is None:
            break
        _, j, i, job = best
        del remaining[j]
        busy[i] = True
        actions[i] = job["op"] if positions[i] == job["pos"] else _step_toward(positions[i], job["pos"])
    return actions


def _market(obs, me, private):
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    money = float(me.get("money", 0) or 0)
    shed = private.get("shed", {}) or {}
    seeds = private.get("seeds", {}) or {}
    prices = (obs.get("market", {}) or {}).get("prices", {})
    orders = []

    placed_geese = 0
    for row in me["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal") == "GOOSE":
                placed_geese += 1
    owned_geese = _count_owned_geese(me, private)
    carried_wheat = sum(int(inv.get("WHEAT", 0) or 0) for inv in private.get("inventories", []))
    feed_reserve = max(12, owned_geese * 2)

    # Sell products first so proceeds are available to later same-turn purchases.
    force_sell = day >= 28 or sum(int(shed.get(item, 0) or 0) for item in PRODUCTS) >= 60
    for item in ("EGG", "CARROT", "WHEAT"):
        have = int(shed.get(item, 0) or 0)
        if item == "WHEAT":
            have = max(0, have - feed_reserve)
        price = float(prices.get(item, 0) or 0)
        if have > 0 and (force_sell or price >= SELL_FLOOR[item]):
            n = min(have, 40)
            orders.append(["SELL", item, n])
            money += price * n * 0.75
        if len(orders) >= 3:
            break

    target_hands = 7 if day < 4 else 9
    if day < 29 and hour <= 1:
        missing = max(0, target_hands - int(me.get("hires_today", 0) or 0))
        for _ in range(missing):
            if len(orders) >= 10:
                break
            orders.append(["HIRE"])

    # One expansion at the start, as in v1; delay any further land until the
    # goose experiment proves itself instead of spending capital blindly.
    if day <= 8 and len(me.get("unlocked_quadrants", [])) < 2 and money >= 1700 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        money -= 1000

    # Keep two feed-days available in shed + carriers. Wheat purchases are cheap
    # insurance against starving a flock and are capped when the market spikes.
    wheat_price = float(prices.get("WHEAT", 25) or 25)
    feed_gap = feed_reserve - int(shed.get("WHEAT", 0) or 0) - carried_wheat
    if feed_gap > 0 and wheat_price <= 55 and len(orders) < 10:
        n = min(feed_gap, 20, int(max(0, money - 250) // max(1, wheat_price)))
        if n > 0:
            orders.append(["BUY_PRODUCT", "WHEAT", n])
            money -= wheat_price * n

    # Grow the flock gradually. This avoids the all-in day-0 bankruptcy mode while
    # still starting early enough for geese to pay back their four-day delay.
    if day <= 18 and owned_geese < TARGET_GEESE and len(orders) < 10:
        gap = TARGET_GEESE - owned_geese
        max_buy = 3 if day <= 3 else 2
        n = min(gap, max_buy, int(max(0, money - 500 - feed_reserve * wheat_price) // 300))
        if n > 0:
            orders.append(["BUY_ANIMAL", "GOOSE", n])
            money -= 300 * n

    if day <= 25:
        for crop in ("WHEAT", "CARROT"):
            if len(orders) >= 10:
                break
            have = int(seeds.get(crop, 0) or 0)
            gap = SEED_TARGET[crop] - have
            if gap <= 0:
                continue
            n = min(gap, 8)
            cost = CROPS[crop]["seed_cost"] * n
            if money >= cost + 200:
                orders.append(["BUY_SEED", crop, n])
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
    actions = _assign(obs, me, private, jobs)
    return {
        "farmer": actions[0] if actions else ["PASS"],
        "hands": actions[1:],
        "market": _market(obs, me, private),
    }
