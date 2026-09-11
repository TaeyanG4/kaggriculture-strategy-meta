"""Kaggriculture baseline v7: animal-first capital sequencing experiment.

Independent standard-library agent. V7 keeps the validated v4 cow economy but changes
only the opening capital sequence suggested by the official CC0 high-reward slice:
establish a tiny cared herd before paying for land, then expand the field once that
starter herd exists. The starting quadrant reserves only four pasture tiles so early
crop throughput is not sacrificed to empty structures.
"""

BOARD = 10
SHED_TILES = ((4, 4), (5, 4), (4, 5), (5, 5))
PRODUCTS = ("MILK", "CARROT", "WHEAT")

CROPS = {
    "WHEAT": {"seed_cost": 10, "first": 2, "max_day": 4},
    "CARROT": {"seed_cost": 20, "first": 2, "max_day": 3},
}

TARGET_COWS = 10
TARGET_PASTURES = 10
SEED_TARGET = {"WHEAT": 18, "CARROT": 10}
SELL_FLOOR = {"MILK": 120, "CARROT": 15, "WHEAT": 12}


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


def _count_owned_cows(me, private):
    total = int((private.get("shed", {}) or {}).get("COW", 0) or 0)
    total += sum(int(inv.get("COW", 0) or 0) for inv in private.get("inventories", []))
    for row in me["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal") == "COW":
                total += 1
    return total


def _pasture_target(me):
    return 4 if len(me.get("unlocked_quadrants", [])) < 2 else TARGET_PASTURES


def _collect_jobs(obs, me, private):
    day = obs.get("day", 0)
    tiles = me["tiles"]
    shed = private.get("shed", {}) or {}
    inventories = private.get("inventories", [])
    shed_pos = _shed_tile(tiles)

    feed = []
    harvest_animals = []
    care = []
    empty_pastures = []
    pasture_count = 0
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
            elif kind == "PASTURE":
                pasture_count += 1
                if tile.get("animal") != "COW":
                    empty_pastures.append(pos)
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

    carried_cows = sum(int(inv.get("COW", 0) or 0) for inv in inventories)
    cows_in_shed = int(shed.get("COW", 0) or 0)
    place = [
        {"pos": pos, "op": ["PLACE", "COW"], "need": ("COW", 1)}
        for pos in empty_pastures[: carried_cows + cows_in_shed]
    ]
    pickup_cows = []
    if cows_in_shed > carried_cows and empty_pastures:
        pickup_cows.append(
            {
                "pos": shed_pos,
                "op": ["PICKUP", "COW", min(4, cows_in_shed)],
                "need": None,
                "skip": "COW",
            }
        )

    target_pastures = _pasture_target(me)
    build = []
    if day <= 12 and pasture_count < target_pastures:
        empties = []
        for y in range(BOARD):
            for x in range(BOARD):
                if tiles[y][x] is None:
                    empties.append((x, y))
        empties.sort(key=lambda p: (_dist(p, shed_pos), p[1], p[0]))
        room = min(target_pastures - pasture_count, len(empties))
        build = [{"pos": pos, "op": ["BUILD_PASTURE"], "need": None} for pos in empties[:room]]

    plant = []
    if day <= 25:
        seeds = dict(private.get("seeds", {}) or {})
        empties = []
        for y in range(BOARD):
            for x in range(BOARD):
                if tiles[y][x] is None:
                    empties.append((x, y))
        empties.sort(key=lambda p: (_dist(p, shed_pos), p[1], p[0]))
        # Reserve near-shed empty tiles for still-missing pastures.
        reserve = max(0, target_pastures - pasture_count)
        for x, y in empties[reserve:]:
            crop = _crop_for(x, y)
            if seeds.get(crop, 0) <= 0:
                continue
            plant.append({"pos": (x, y), "op": ["PLANT", crop], "need": None})
            seeds[crop] -= 1

    return pickup_feed + feed + pickup_cows + place + harvest_animals + care + harvest_crops + water + dig + build + plant


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
        product_load = sum(int(inv.get(item, 0) or 0) for item in ("MILK", "CARROT"))
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

    placed_cows = 0
    for row in me["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal") == "COW":
                placed_cows += 1
    owned_cows = _count_owned_cows(me, private)
    carried_wheat = sum(int(inv.get("WHEAT", 0) or 0) for inv in private.get("inventories", []))
    feed_reserve = max(16, owned_cows * 3)

    # Sell products first so proceeds are available to later same-turn purchases.
    force_sell = day >= 28 or sum(int(shed.get(item, 0) or 0) for item in PRODUCTS) >= 60
    for item in ("MILK", "CARROT", "WHEAT"):
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

    target_hands = 8 if day < 4 else 10
    if day < 29 and hour <= 1:
        missing = max(0, target_hands - int(me.get("hires_today", 0) or 0))
        for _ in range(missing):
            if len(orders) >= 10:
                break
            orders.append(["HIRE"])

    # Keep two feed-days available in shed + carriers. Wheat purchases are cheap
    # insurance against starving a flock and are capped when the market spikes.
    wheat_price = float(prices.get("WHEAT", 25) or 25)
    feed_gap = feed_reserve - int(shed.get("WHEAT", 0) or 0) - carried_wheat
    if feed_gap > 0 and wheat_price <= 55 and len(orders) < 10:
        n = min(feed_gap, 20, int(max(0, money - 250) // max(1, wheat_price)))
        if n > 0:
            orders.append(["BUY_PRODUCT", "WHEAT", n])
            money -= wheat_price * n

    # Buy a two-cow starter herd before land. A shorter four-day feed float is used
    # only for this initial pair; subsequent purchases return to the conservative
    # v4 eight-day reserve.
    if day <= 2 and owned_cows == 0 and len(orders) < 10:
        starter = min(2, int(max(0, money - 500 - 2 * wheat_price * 4) // 400))
        if starter > 0:
            orders.append(["BUY_ANIMAL", "COW", starter])
            money -= 400 * starter
            owned_cows += starter

    # Expand only after the starter herd is established. This keeps the experiment
    # focused on investment ordering rather than changing final farm scale.
    if (
        4 <= day <= 8
        and len(me.get("unlocked_quadrants", [])) < 2
        and owned_cows >= 2
        and money >= 1700
        and len(orders) < 10
    ):
        orders.append(["BUY_LAND"])
        money -= 1000

    # Cows take longer to mature than geese, so buy later batches only when the
    # post-purchase balance can carry several days of feed and ordinary crop work.
    if day <= 16 and owned_cows < TARGET_COWS and len(orders) < 10:
        gap = TARGET_COWS - owned_cows
        max_buy = 2
        feed_float = max(0, owned_cows + max_buy) * wheat_price * 8
        n = min(gap, max_buy, int(max(0, money - 700 - feed_float) // 400))
        if n > 0:
            orders.append(["BUY_ANIMAL", "COW", n])
            money -= 400 * n

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
