"""o001_demand_planner - Kaggriculture agent (Claude lineage, 2026-09-14).

Original implementation (no code inherited from the public V37 / c-series routers).

Architecture
------------
1. Market model      : exact replica of the engine price curve + deterministic
                       town consumption; expected value of future shop unlocks.
2. Supply forecast   : projected harvest/production arrivals from BOTH farms
                       (the opponent's farm is public) -> projected inventory path.
3. Portfolio planner : greedy marginal allocation of tiles / animals / land using
                       projected marginal prices (diminishing returns give natural
                       diversification); re-planned twice a day.
4. Task scheduler    : per-turn task list (water/feed/care/harvest/plant/...)
                       assigned to farmer + hands by a value/distance greedy.
5. Market executor   : prompt sales with hold rules, feed/seed/animal purchases,
                       hire sizing, land purchase, endgame liquidation.
"""

import math

# --------------------------------------------------------------------------
# Engine constants (kaggle-environments 1.32.7 kaggriculture)
# --------------------------------------------------------------------------
CROPS = {
    "WHEAT":      {"seed": 10,  "first": 2,  "maxday": 4,  "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT":     {"seed": 20,  "first": 2,  "maxday": 3,  "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO":     {"seed": 50,  "first": 8,  "maxday": 8,  "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first": 10, "maxday": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":      {"seed": 80,  "first": 10, "maxday": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
UNFERT_YIELD = {"WHEAT": 4, "CARROT": 3, "MELON": 6}
ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP",    "first": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
MARKET_PARAMS = {
    "WHEAT":      {"base": 25,  "T": 400, "bf": "sqrt",   "bt": 0.80, "af": "log",    "at": 0.20},
    "CARROT":     {"base": 35,  "T": 450, "bf": "hinge",  "bt": 1.00, "af": "sqrt",   "at": 0.70},
    "TOMATO":     {"base": 60,  "T": 200, "bf": "hinge",  "bt": 0.40, "af": "sqrt",   "at": 0.60},
    "STRAWBERRY": {"base": 120, "T": 100, "bf": "sqrt",   "bt": 0.70, "af": "linear", "at": 1.60},
    "MELON":      {"base": 250, "T": 300, "bf": "log",    "bt": 0.20, "af": "sq",     "at": 3.60},
    "EGG":        {"base": 50,  "T": 332, "bf": "hinge",  "bt": 0.40, "af": "log",    "at": 0.20},
    "MILK":       {"base": 160, "T": 122, "bf": "sqrt",   "bt": 0.60, "af": "linear", "at": 1.60},
    "WOOL":       {"base": 200, "T": 105, "bf": "log",    "bt": 0.20, "af": "sq",     "at": 3.20},
    "FERTILIZER": {"base": 100, "T": 200, "bf": "linear", "bt": 0.40, "af": "linear", "at": 0.40},
}
I0 = 10000
SHOPS = {
    "BAKERY":         ["EGG", "WHEAT"],
    "PIZZA_SHOP":     ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT":    ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE":     ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE":       ["CARROT"],
    "SMOOTHIE_SHOP":  ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
LAND_ORDER = ["NE", "SW", "SE"]
LAND_PRICES = [1000, 2000, 4000]
TURNS = 24
DAYS = 30
LAST_STEP = 718          # last observation on which an action is processed
BOARD = 10
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]
SHED_CAP = 100
MAX_ORDERS = 10

# Expected per-day consumption contributed by one *future unknown* shop unlock.
_EXP_UNLOCK = {}
for _p in PRODUCTS:
    _tot = 0.0
    for _s, _items in SHOPS.items():
        if _p in _items:
            _tot += 6.0 * (2 if len(_items) == 1 else 1)
    _EXP_UNLOCK[_p] = _tot / len(SHOPS)

# --------------------------------------------------------------------------
# Tunables
# --------------------------------------------------------------------------
LABOR_COST = 4.0          # shadow price per unit action
MAX_HANDS = 11
MIN_HANDS_EARLY = 4
ACTIONS_PER_HAND = 14.0
HAND_FLOOR = [4, 4, 6, 6, 6, 6, 8, 8, 9, 9] + [10] * 20   # per-day minimum hands (labor is nearly free)
OPP_MIRROR = 0.5          # fraction of my *new* plans assumed to be mirrored by the opponent
OPP_ANIMAL_EFF = 0.7      # opponent animals assumed to realise this fraction of the max schedule
OPP_CROP_EFF = 0.85
FUTURE_UNLOCK_WEIGHT = 1.0   # expected demand from unknown future shops
ZONE_BONUS = 2.2          # score multiplier for tasks inside a unit's own zone
DELIVER_MIN_VALUE = 700.0 # carried produce worth less than this waits for the free night drop
WHEAT_TILES_PER_ANIMAL = 1.2
RESERVE_WHEAT_DAYS = 1.5
FERT_MIN_VALUE = 25.0
MAX_ANIMALS = 30
HOLD_FLOOR_FRAC = 0.30    # hold stock when marginal price < this fraction of base and demand can absorb it
# Day-0 opening (fixed, cash 3000): 4 hands, 2 cows, 3 sheep, 6 melon + 8 wheat seeds, 5 feed wheat.
OPENING_ORDERS = [["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
                  ["BUY_ANIMAL", "COW", 2], ["BUY_ANIMAL", "SHEEP", 3],
                  ["BUY_SEED", "MELON", 6], ["BUY_PRODUCT", "WHEAT", 8]]
OPENING_ANIMALS = ["SHEEP", "SHEEP", "SHEEP", "COW", "COW"]
OPENING_CROPS = ["MELON"] * 6 + ["WHEAT"] * 8
OPENING_MELON_TARGET = 12
MAX_LAND_PURCHASES = 2    # NE + SW; the SE quadrant (4000) only pays with huge unmet demand


def _shape(func, x, T):
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "hinge":
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def price(item, inv):
    p = MARKET_PARAMS[item]
    base, T = p["base"], p["T"]
    if inv < I0:
        amp = p["bt"] * base / _shape(p["bf"], T, T)
        v = base + amp * _shape(p["bf"], I0 - inv, T)
    else:
        amp = p["at"] * base / _shape(p["af"], T, T)
        v = base - amp * _shape(p["af"], inv - I0, T)
    return max(1, int(round(v)))


def revenue(item, inv, n):
    tot = 0
    for j in range(n):
        tot += price(item, inv + j)
    return tot


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def nearest_shed(pos):
    best, bd = SHED_TILES[0], 99
    for t in SHED_TILES:
        d = dist(pos, t)
        if d < bd:
            best, bd = t, d
    return best, bd


def step_toward(pos, target):
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


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# --------------------------------------------------------------------------
# Crop / animal schedules
# --------------------------------------------------------------------------
def crop_schedule(crop, p, fert=False):
    """Return (sales:[(sale_day, units)], last_day, actions) for planting on day p.

    Only production sellable by day 29 counts. Day 29 has no night tick, so the
    last ongoing production fires at the end of day 28 (sold on day 29)."""
    cd = CROPS[crop]
    if not cd["ongoing"]:
        first, maxday = cd["first"], cd["maxday"]
        ws = (maxday + 1) // 2
        if crop == "MELON":
            h = p + first
        else:
            h = min(p + maxday, DAYS - 1)
        if h < p + first or h > DAYS - 1:
            return None
        if crop == "MELON":
            units = cd["max_yield"]
        else:
            bonus_days = max(0, min(h, p + maxday) - (p + ws) + 1)
            units = min(cd["max_yield"], 1 + (2 if fert else 1) * bonus_days)
        actions = 2 + (h - p + 1) + (1 if fert else 0)
        return [(h, units)], h, actions
    first, interval = cd["first"], cd["interval"]
    sales = []
    last = p
    for k in range(cd["max_yield"]):
        prod_day = p + first - 1 + k * interval      # production fires at END of prod_day
        if prod_day > DAYS - 2:
            break
        sales.append((prod_day + 1, 2 if fert else 1))
        last = prod_day + 1
    if not sales:
        return None
    actions = 1 + (last - p + 1) + len(sales) + (2 if fert else 0)
    return sales, last, actions


def animal_schedule(kind, q):
    """(sale_day, units) list for an animal placed on day q, fed + cared daily."""
    a = ANIMALS[kind]
    sales = []
    d = q + a["first"] - 1
    firstprod = True
    while d <= DAYS - 2:
        if firstprod:
            units = min(a["max_held"], 1 + (d - q + 1))
            firstprod = False
        else:
            units = min(a["max_held"], 1 + a["interval"])
        sales.append((d + 1, units))
        d += a["interval"]
    return sales


# --------------------------------------------------------------------------
# Brain
# --------------------------------------------------------------------------
class Brain:
    def __init__(self, player):
        self.player = player
        self.last_step = -1
        self.plan = {}            # (x,y) -> crop planned for planting
        self.animal_plan = {}     # (x,y) -> animal kind (structure to build / animal to place)
        self.animal_orders = {}   # kind -> count still to buy
        self.pending_animals = {} # kind -> count in shed or carried
        self.plan_day_idx = -1
        self.hands_target = MIN_HANDS_EARLY
        self.land_wanted = False
        self.errors = 0
        self.pass_today = 0
        self.acts_today = 0
        self.idle_frac = 0.3
        self.labor_cost = LABOR_COST
        self.telemetry = {"plants": 0, "errors": 0, "land": [], "animals": {}, "hires": 0, "idle": []}

    # ------------------------------------------------------------------ obs
    def parse(self, obs):
        self.step = int(obs.get("step", 0))
        self.day = self.step // TURNS
        self.hour = self.step % TURNS
        self.me = obs["farms"][self.player]
        self.opp = obs["farms"][1 - self.player]
        priv = obs["private"]
        self.shed = dict(priv.get("shed", {}) or {})
        self.seeds = dict(priv.get("seeds", {}) or {})
        invs = [dict(i or {}) for i in (priv.get("inventories") or [{}])]
        self.market_inv = dict(obs["market"]["inventory"])
        self.prices = dict(obs["market"]["prices"])
        self.shops = list(obs["town"].get("unlocked_shops", []) or [])
        self.money = float(self.me["money"])
        self.tiles = self.me["tiles"]
        self.unlocked = set(self.me.get("unlocked_quadrants", ["NW"]))
        positions = [tuple(self.me["farmer"])] + [tuple(h) for h in self.me.get("hands", [])]
        while len(invs) < len(positions):
            invs.append({})
        self.units = [{"idx": i, "pos": positions[i], "inv": invs[i]} for i in range(len(positions))]
        self.hires_today = int(self.me.get("hires_today", 0))
        self.n_animals = 0
        for _, _, t in self.owned_tiles():
            if isinstance(t, dict) and "animal" in t:
                self.n_animals += 1

    def owned_tiles(self):
        tiles = self.tiles
        for y in range(BOARD):
            row = tiles[y]
            for x in range(BOARD):
                t = row[x]
                if t == "LOCKED":
                    continue
                yield x, y, t

    def tile_at(self, xy):
        return self.tiles[xy[1]][xy[0]]

    def is_weed(self, xy):
        t = self.tile_at(xy)
        return isinstance(t, dict) and t.get("kind") == "WEED"

    # ---------------------------------------------------------------- demand
    def consumption(self, item, from_day):
        known = 0.0 if item == "FERTILIZER" else 1.0
        for s in self.shops:
            items = SHOPS[s]
            if item in items:
                known += 6.0 * (2 if len(items) == 1 else 1)
        cons = [0.0] * DAYS
        n_unlocked = len(self.shops)
        for d in range(from_day, DAYS):
            k_seen = min(8, d // 3)
            extra = max(0, k_seen - n_unlocked)
            cons[d] = known + extra * _EXP_UNLOCK[item] * FUTURE_UNLOCK_WEIGHT
        return cons

    def tile_supply(self, farm, sup, crop_eff=1.0, animal_eff=1.0):
        day = self.day
        for y in range(BOARD):
            row = farm["tiles"][y]
            for x in range(BOARD):
                t = row[x]
                if not isinstance(t, dict):
                    continue
                kind = t.get("kind")
                if kind == "PLANT":
                    crop = t["crop"]
                    p = t["planted_day"]
                    cd = CROPS[crop]
                    if not cd["ongoing"]:
                        h = p + (cd["first"] if crop == "MELON" else cd["maxday"])
                        h = max(h, day)
                        if h <= DAYS - 1:
                            sup[crop][h] += UNFERT_YIELD[crop] * crop_eff
                    else:
                        first, interval = cd["first"], cd["interval"]
                        for k in range(cd["max_yield"]):
                            pd = p + first - 1 + k * interval
                            if pd > DAYS - 2:
                                break
                            sd = pd + 1
                            if sd >= day:
                                sup[crop][sd] += 1.3 * crop_eff
                        if t.get("yield_units", 0) > 0:
                            sup[crop][day] += t["yield_units"]
                elif "animal" in t:
                    kind = t["animal"]
                    prod = ANIMALS[kind]["product"]
                    for sd, u in animal_schedule(kind, t["placed_day"]):
                        if sd >= day:
                            sup[prod][sd] += u * animal_eff
                    if t.get("yield_units", 0) > 0:
                        sup[prod][day] += t["yield_units"]
                    for d in range(day + 1, DAYS):
                        sup["FERTILIZER"][d] += 1.0 * animal_eff

    def build_forecast(self):
        day = self.day
        sup = {p: [0.0] * DAYS for p in PRODUCTS}
        self.tile_supply(self.me, sup)
        self.tile_supply(self.opp, sup, OPP_CROP_EFF, OPP_ANIMAL_EFF)
        for p in PRODUCTS:
            sup[p][day] += self.shed.get(p, 0)
        # committed but not yet placed animals
        q = day if self.hour <= 14 else day + 1
        for kind, n in self.pending_animals.items():
            for _ in range(n):
                for sd, u in animal_schedule(kind, q):
                    sup[ANIMALS[kind]["product"]][sd] += u
        for xy, kind in self.animal_plan.items():
            t = self.tile_at(xy)
            if isinstance(t, dict) and "animal" in t:
                continue
            for sd, u in animal_schedule(kind, q):
                sup[ANIMALS[kind]["product"]][sd] += u * 0.5
        self.supply = sup
        self.cons = {p: self.consumption(p, day) for p in PRODUCTS}
        feed = self.n_animals + sum(self.pending_animals.values())
        for d in range(day, DAYS - 1):
            self.cons["WHEAT"][d] += feed
        path = {}
        for p in PRODUCTS:
            arr = [0.0] * DAYS
            inv = float(self.market_inv[p])
            for d in range(day, DAYS):
                inv += sup[p][d]
                arr[d] = inv
                inv -= self.cons[p][d]
            path[p] = arr
        self.inv_path = path

    def add_planned_supply(self, item, day, units, mirror=True):
        if day >= DAYS:
            return
        u = units * ((1.0 + OPP_MIRROR) if (mirror and self.day <= 2) else 1.0)
        self.supply[item][day] += u
        arr = self.inv_path[item]
        for d in range(day, DAYS):
            arr[d] += u

    def value_of_sales(self, item, sales):
        tot = 0.0
        path = self.inv_path[item]
        for d, u in sales:
            if d >= DAYS:
                continue
            inv = int(path[d])
            n = int(u)
            frac = u - n
            tot += revenue(item, inv, n) + frac * price(item, inv + n)
        return tot

    def fert_value(self):
        return max(FERT_MIN_VALUE, min(self.prices.get("FERTILIZER", 100), 100))

    def wheat_price(self):
        return self.prices.get("WHEAT", 25)

    # ------------------------------------------------------------- valuation
    def crop_option(self, crop, p):
        """Best (rate, value, occupancy, fert, sales) for planting crop on day p, or None."""
        best = None
        for fert in (False, True):
            if fert and crop == "MELON":
                continue
            sch = crop_schedule(crop, p, fert)
            if sch is None:
                continue
            sales, last, actions = sch
            gross = self.value_of_sales(crop, sales)
            cost = CROPS[crop]["seed"] + self.labor_cost * actions
            if fert:
                cost += (2 if CROPS[crop]["ongoing"] else 1) * self.fert_value()
            val = gross - cost
            occ = max(1, last - p + 1)
            rate = val / occ
            if best is None or rate > best[0]:
                best = (rate, val, occ, fert, sales)
        return best

    def best_crop(self, p):
        best, name = None, None
        for crop in CROPS:
            v = self.crop_option(crop, p)
            if v is not None and (best is None or v[0] > best[0]):
                best, name = v, crop
        return name, best

    def animal_option(self, kind, q):
        a = ANIMALS[kind]
        sales = animal_schedule(kind, q)
        if not sales:
            return None
        gross = self.value_of_sales(a["product"], sales)
        days = DAYS - 1 - q
        gross += self.value_of_sales("FERTILIZER", [(d, 1) for d in range(q + 1, DAYS)]) * 0.9
        feed_days = max(0, sales[-1][0] - 1 - q + 1)
        cost = a["cost"] + feed_days * (self.wheat_price() + 1.0) + self.labor_cost * (3.2 * days + 4)
        val = gross - cost
        return (val / max(1, days), val, days, sales)

    # -------------------------------------------------------------- planning
    def plan_day(self):
        day, hour = self.day, self.hour
        if hour == 0 and day > 0:
            # labor saturation from yesterday's idle rate -> shadow price of an action
            if self.acts_today > 0:
                self.idle_frac = self.pass_today / float(self.acts_today)
                self.telemetry["idle"].append(round(self.idle_frac, 2))
            self.pass_today = 0
            self.acts_today = 0
        if self.idle_frac < 0.04:
            self.labor_cost = LABOR_COST * 1.6
        elif self.idle_frac < 0.10:
            self.labor_cost = LABOR_COST * 1.25
        else:
            self.labor_cost = LABOR_COST
        self.build_forecast()
        # keep plans only for tiles that are still empty / weed
        self.plan = {k: v for k, v in self.plan.items() if self.tile_at(k) is None or self.is_weed(k)}
        free = []
        for x, y, t in self.owned_tiles():
            xy = (x, y)
            if xy in self.animal_plan:
                continue
            if t is None or (isinstance(t, dict) and t.get("kind") == "WEED"):
                free.append(xy)
            elif isinstance(t, dict) and t.get("kind") in ("COOP", "PASTURE") and "animal" not in t:
                free.append(xy)
        free.sort(key=lambda xy: (nearest_shed(xy)[1], xy[1], xy[0]))

        reserve = self.cash_reserve()
        budget = self.money - reserve

        if day == 0 and hour == 0:
            # fixed opening template; the planner takes over from the first replan
            self.animal_plan = {}
            self.plan = {}
            tiles = list(free)
            for kind in OPENING_ANIMALS:
                if tiles:
                    self.animal_plan[tiles.pop(0)] = kind
            for crop in OPENING_CROPS:
                if tiles:
                    self.plan[tiles.pop(0)] = crop
            self.animal_orders = {}
            self.land_wanted = False
            self.hands_target = HAND_FLOOR[0]
            self.plan_day_idx = day
            return

        # ---- animals ----
        q = day if hour <= 14 else day + 1
        # every pending (bought, unplaced) animal must have a planned tile
        for kind, n in self.pending_animals.items():
            have = sum(1 for k in self.animal_plan.values() if k == kind)
            while have < n and free:
                tile = None
                for xy in free:
                    t = self.tile_at(xy)
                    if isinstance(t, dict) and t.get("kind") == ANIMALS[kind]["structure"]:
                        tile = xy
                        break
                if tile is None:
                    tile = free[0]
                free.remove(tile)
                self.animal_plan[tile] = kind
                have += 1
        n_committed = self.n_animals + sum(self.pending_animals.values()) + len(self.animal_plan)
        orders = dict(self.animal_orders)
        shed_room = SHED_CAP - sum(self.shed.values())
        feed_price = self.wheat_price() + 3
        # structures already built and empty: prefer filling them
        while free and shed_room > 2 and day <= DAYS - 8:
            best = None
            for kind in ANIMALS:
                v = self.animal_option(kind, q)
                if v is not None and (best is None or v[0] > best[1][0]):
                    best = (kind, v)
            if best is None:
                break
            kind, (rate, val, occ, sales) = best
            _, cb = self.best_crop(day)
            crop_rate = cb[0] if cb else -1e9
            if val <= 0 or rate < crop_rate or ANIMALS[kind]["cost"] + 2 * feed_price > budget:
                break
            if n_committed + sum(orders.values()) >= MAX_ANIMALS:
                break
            budget -= ANIMALS[kind]["cost"] + 2 * feed_price
            shed_room -= 1
            orders[kind] = orders.get(kind, 0) + 1
            # pick the free tile closest to the shed, preferring an existing matching structure
            tile = None
            for xy in free:
                t = self.tile_at(xy)
                if isinstance(t, dict) and t.get("kind") == ANIMALS[kind]["structure"]:
                    tile = xy
                    break
            if tile is None:
                tile = free[0]
            free.remove(tile)
            self.animal_plan[tile] = kind
            for d, u in sales:
                self.add_planned_supply(ANIMALS[kind]["product"], d, u)
            for d in range(q + 1, DAYS):
                self.add_planned_supply("FERTILIZER", d, 1)
        self.animal_orders = orders

        # ---- crops ----
        seed_budget = budget
        new_plan = {}
        # feed self-sufficiency: keep enough wheat tiles for the herd (buying feed
        # drains the shared wheat market in the opponent's favour)
        if 8 <= day <= DAYS - 6:
            animals_total = self.n_animals + sum(self.pending_animals.values()) + sum(max(0, v) for v in self.animal_orders.values())
            have_wheat = sum(1 for _, _, t in self.owned_tiles() if isinstance(t, dict) and t.get("crop") == "WHEAT")
            need_wheat_tiles = int(math.ceil(animals_total * WHEAT_TILES_PER_ANIMAL)) - have_wheat
            wv = self.crop_option("WHEAT", day)
            while need_wheat_tiles > 0 and free and wv is not None and wv[1] > 0 and seed_budget >= CROPS["WHEAT"]["seed"]:
                tile = free.pop(0)
                new_plan[tile] = "WHEAT"
                seed_budget -= CROPS["WHEAT"]["seed"]
                need_wheat_tiles -= 1
                for d, u in wv[4]:
                    self.add_planned_supply("WHEAT", d, u)
        # opening prior: reach the melon target early (first-mover melon market)
        if day <= 3:
            have_melon = sum(1 for _, _, t in self.owned_tiles() if isinstance(t, dict) and t.get("crop") == "MELON")
            have_melon += self.seeds.get("MELON", 0)
            while have_melon < OPENING_MELON_TARGET and free and seed_budget >= CROPS["MELON"]["seed"]:
                v = self.crop_option("MELON", day)
                if v is None or v[1] <= 0:
                    break
                tile = free.pop(0)
                new_plan[tile] = "MELON"
                seed_budget -= CROPS["MELON"]["seed"]
                have_melon += 1
                for d, u in v[4]:
                    self.add_planned_supply("MELON", d, u)
        # use seeds already on hand first (avoid churn between replans)
        onhand = {c: n for c, n in self.seeds.items() if n > 0}
        remaining_free = []
        for tile in free:
            placed = False
            for crop in list(onhand.keys()):
                if onhand[crop] <= 0:
                    continue
                v = self.crop_option(crop, day)
                if v is None or v[1] <= 0:
                    onhand.pop(crop, None)
                    continue
                onhand[crop] -= 1
                new_plan[tile] = crop
                for d, u in v[4]:
                    self.add_planned_supply(crop, d, u)
                placed = True
                break
            if not placed:
                remaining_free.append(tile)
        for tile in remaining_free:
            name, best = self.best_crop(day)
            if best is None or best[1] <= 0:
                continue
            rate, val, occ, fert, sales = best
            if CROPS[name]["seed"] > seed_budget:
                if CROPS["WHEAT"]["seed"] <= seed_budget:
                    wb = self.crop_option("WHEAT", day)
                    if wb is None or wb[1] <= 0:
                        continue
                    name, sales = "WHEAT", wb[4]
                else:
                    continue
            seed_budget -= CROPS[name]["seed"]
            new_plan[tile] = name
            for d, u in sales:
                self.add_planned_supply(name, d, u)
        self.plan = new_plan
        # leftover tiles (no profitable crop): still worth an animal if its value is positive
        leftover = [xy for xy in free if xy not in new_plan]
        while leftover and day <= DAYS - 8 and shed_room > 2:
            best = None
            for kind in ANIMALS:
                v = self.animal_option(kind, q)
                if v is not None and (best is None or v[1] > best[1][1]):
                    best = (kind, v)
            if best is None:
                break
            kind, (rate, val, occ, sales) = best
            if val <= 150 or ANIMALS[kind]["cost"] + 2 * feed_price > budget:
                break
            if self.n_animals + sum(self.pending_animals.values()) + len(self.animal_plan) + sum(orders.values()) >= MAX_ANIMALS:
                break
            budget -= ANIMALS[kind]["cost"] + 2 * feed_price
            shed_room -= 1
            orders[kind] = orders.get(kind, 0) + 1
            tile = leftover.pop(0)
            self.animal_plan[tile] = kind
            for d, u in sales:
                self.add_planned_supply(ANIMALS[kind]["product"], d, u)
            for d in range(q + 1, DAYS):
                self.add_planned_supply("FERTILIZER", d, 1)
        self.animal_orders = orders

        # ---- land ----
        self.land_wanted = False
        n_extra = len(self.unlocked) - 1
        if n_extra < min(len(LAND_ORDER), MAX_LAND_PURCHASES) and day <= 16:
            lp = LAND_PRICES[n_extra]
            extra_val = 0.0
            for _ in range(25):
                name, best = self.best_crop(day + 1)
                if best is None or best[1] <= 0:
                    break
                extra_val += best[1]
                for d, u in best[4]:
                    self.add_planned_supply(name, d, u)
            if extra_val > lp * 1.25 and len(free) - len(new_plan) <= 4:
                self.land_wanted = True

        # ---- hands ----
        work = self.estimate_work()
        target = int(math.ceil(work / ACTIONS_PER_HAND))
        cap = MAX_HANDS
        target = max(HAND_FLOOR[min(day, len(HAND_FLOOR) - 1)], min(cap, target))
        if day <= 5:
            target = HAND_FLOOR[day]
        if day >= DAYS - 1:
            target = min(target, 8)
        self.hands_target = target
        self.plan_day_idx = day

    def estimate_work(self):
        n_plants = harvests = n_animals = 0
        for _, _, t in self.owned_tiles():
            if isinstance(t, dict):
                if t.get("kind") == "PLANT":
                    n_plants += 1
                    harvests += 0.6 if CROPS[t["crop"]]["ongoing"] else 0.3
                elif "animal" in t:
                    n_animals += 1
        n_plan = len(self.plan) + len(self.animal_plan)
        work = n_plants * 1.15 + harvests + n_animals * 3.4 + n_plan * 2.2 + 8
        return work * 1.55

    def cash_reserve(self):
        if self.day <= 6:
            return 30 + self.n_animals * 12
        return 40 + self.n_animals * (self.wheat_price() + 2) * 1.2

    # ---------------------------------------------------------------- tasks
    def build_tasks(self):
        day, hour, step = self.day, self.hour, self.step
        last_day = day >= DAYS - 1
        tasks = []
        pr = self.prices
        unfed = []
        fert_targets = 0
        fv = self.fert_value()
        for x, y, t in self.owned_tiles():
            xy = (x, y)
            if t is None:
                kind = self.animal_plan.get(xy)
                if kind and not last_day:
                    tasks.append({"pos": xy, "op": ["BUILD_" + ANIMALS[kind]["structure"]], "value": 400, "key": "tile", "need": None})
                    continue
                crop = self.plan.get(xy)
                if crop and hour <= 21 and not last_day:
                    v = self.crop_option(crop, day)
                    if v is not None and v[1] > 0:
                        tasks.append({"pos": xy, "op": ["PLANT", crop], "value": 60 + max(0.0, v[0]) * 3, "key": "tile", "need": ("SEED", crop)})
                    else:
                        self.plan.pop(xy, None)
                continue
            if not isinstance(t, dict):
                continue
            kind = t.get("kind")
            if kind == "WEED":
                if xy in self.plan or xy in self.animal_plan:
                    tasks.append({"pos": xy, "op": ["DIG"], "value": 55, "key": "tile", "need": None})
                continue
            if kind == "PLANT":
                crop = t["crop"]
                cd = CROPS[crop]
                age = day - t["planted_day"]
                yu = t.get("yield_units", 0)
                p_unit = pr.get(crop, MARKET_PARAMS[crop]["base"])
                mls = t.get("max_lifespan_step", -1)
                decaying = mls >= 0 and step >= mls
                unw = t.get("consecutive_unwatered", 0)
                fert_until = t.get("fertilized_until_day", -1)
                if not cd["ongoing"]:
                    ws = (cd["maxday"] + 1) // 2
                    target_age = cd["first"] if crop == "MELON" else cd["maxday"]
                    in_window = ws <= age <= cd["maxday"]
                    can_harvest = age >= cd["first"] and yu > 0
                    if can_harvest:
                        do_now = decaying or last_day or age > cd["maxday"] or (
                            age >= target_age and (t["watered_today"] or not in_window or yu >= cd["max_yield"]))
                        if do_now:
                            tasks.append({"pos": xy, "op": ["HARVEST"], "value": 40 + yu * p_unit * (1.4 if decaying else 1.0), "key": "tile", "need": None})
                            continue
                    if last_day:
                        continue
                    if not t["watered_today"]:
                        if in_window and yu < cd["max_yield"]:
                            val = 60 + (2 if fert_until >= day else 1) * p_unit
                        elif unw >= 1:
                            val = 500 + yu * p_unit
                        else:
                            val = 45
                        tasks.append({"pos": xy, "op": ["WATER"], "value": val, "key": "tile", "need": None})
                    if age == ws and fert_until < day and crop in ("WHEAT", "CARROT") and day <= DAYS - 3 and yu < cd["max_yield"]:
                        gain = (2 if crop == "WHEAT" else 1) * p_unit
                        if gain > fv + 10:
                            tasks.append({"pos": xy, "op": ["FERTILIZE"], "value": gain, "key": "tile", "need": ("FERTILIZER", 1)})
                            fert_targets += 1
                    continue
                # ongoing crop
                first, interval = cd["first"], cd["interval"]
                p0 = t["planted_day"]
                remaining = [p0 + first - 1 + k * interval for k in range(cd["max_yield"])
                             if day <= p0 + first - 1 + k * interval <= DAYS - 2]
                prod_tonight = bool(remaining) and remaining[0] == day
                if yu > 0:
                    urgent = yu >= 3 or decaying or last_day or not remaining
                    tasks.append({"pos": xy, "op": ["HARVEST"], "value": 30 + yu * p_unit * (1.5 if urgent else 0.9), "key": "tile", "need": None})
                if decaying or last_day or not remaining:
                    if yu > 0 and unw >= 1 and not last_day and not decaying:
                        tasks.append({"pos": xy, "op": ["WATER"], "value": 30 + yu * p_unit, "key": "tile", "need": None})
                    continue
                if not t["watered_today"]:
                    if unw >= 1:
                        val = 400 + p_unit * 2 * len(remaining)
                    elif prod_tonight and fert_until >= day:
                        val = 60 + p_unit
                    else:
                        val = 45
                    if day == DAYS - 2 and not prod_tonight and unw == 0:
                        val = 0
                    if val > 0:
                        tasks.append({"pos": xy, "op": ["WATER"], "value": val, "key": "tile", "need": None})
                if prod_tonight and fert_until < day:
                    covered = [d for d in remaining if d <= day + 2]
                    gain = len(covered) * p_unit
                    if gain > fv + 10:
                        tasks.append({"pos": xy, "op": ["FERTILIZE"], "value": gain * 1.2, "key": "tile", "need": ("FERTILIZER", 1)})
                        fert_targets += 1
                continue
            if "animal" in t:
                kind = t["animal"]
                a = ANIMALS[kind]
                prod = a["product"]
                p_unit = pr.get(prod, MARKET_PARAMS[prod]["base"])
                yu = t.get("yield_units", 0)
                since = day + 1 - t["placed_day"] - a["first"]
                prod_tonight = since >= 0 and since % a["interval"] == 0
                if last_day:
                    if yu > 0:
                        tasks.append({"pos": xy, "op": ["HARVEST"], "value": 40 + yu * p_unit * 1.5, "key": "tile", "need": None})
                    elif t.get("fertilizer_available"):
                        tasks.append({"pos": xy, "op": ["COLLECT_FERTILIZER"], "value": fv * 0.8, "key": "tile", "need": None})
                    continue
                if not t["fed_today"] and not (day == DAYS - 2 and not prod_tonight):
                    bonus_val = p_unit * (1 + t.get("pending_care_bonus", 0)) if prod_tonight else p_unit
                    v = 350 + bonus_val
                    if t.get("consecutive_unfed", 0) >= 1:
                        v = 3000 + bonus_val
                    tasks.append({"pos": xy, "op": ["FEED"], "value": v, "key": "tile", "need": ("WHEAT", 1)})
                    unfed.append(xy)
                if not t["cared_today"] and (day < DAYS - 2 or prod_tonight):
                    tasks.append({"pos": xy, "op": ["CARE"], "value": 40 + p_unit, "key": "tile", "need": None})
                if t.get("fertilizer_available"):
                    tasks.append({"pos": xy, "op": ["COLLECT_FERTILIZER"], "value": 30 + fv, "key": "tile", "need": None})
                if yu > 0:
                    urgent = prod_tonight and yu + 1 + a["interval"] > a["max_held"]
                    tasks.append({"pos": xy, "op": ["HARVEST"], "value": 25 + yu * p_unit * (1.4 if urgent else 0.8), "key": "tile", "need": None})
                continue
            if kind in ("COOP", "PASTURE"):
                want = self.animal_plan.get(xy)
                if want and ANIMALS[want]["structure"] == kind:
                    if self.pending_animals.get(want, 0) > 0:
                        tasks.append({"pos": xy, "op": ["PLACE", want, 1], "value": 1500, "key": "tile", "need": (want, 1)})
                    continue
                if want and ANIMALS[want]["structure"] != kind:
                    tasks.append({"pos": xy, "op": ["DIG"], "value": 60, "key": "tile", "need": None})
                    continue
                if xy in self.plan:
                    tasks.append({"pos": xy, "op": ["DIG"], "value": 50, "key": "tile", "need": None})
        self.unfed = unfed
        self.fert_targets = fert_targets
        return tasks

    # ------------------------------------------------------------ assignment
    def zones_for(self, tasks, n_units):
        """Workload-balanced pie slices around the shed, one per expected unit.

        Recomputed at hours 0 and 12. Chunk i belongs to unit index i, so a unit
        keeps its zone all day even while hands are still being hired."""
        n_chunks = max(1, self.hands_target + 1)
        key = (self.day, 0 if self.hour < 12 else 12, n_chunks)
        if getattr(self, "_zone_key", None) != key or not getattr(self, "_zones", None):
            weights = {}
            for x, y, t in self.owned_tiles():
                xy = (x, y)
                if isinstance(t, dict):
                    if "animal" in t:
                        weights[xy] = 3.6
                    elif t.get("kind") == "PLANT":
                        weights[xy] = 1.6 if CROPS[t["crop"]]["ongoing"] else 1.3
                    elif t.get("kind") == "WEED":
                        if xy in self.plan or xy in self.animal_plan:
                            weights[xy] = 2.5
                    else:
                        weights[xy] = 2.0 if xy in self.animal_plan else 0.3
                elif xy in self.plan or xy in self.animal_plan:
                    weights[xy] = 2.2
            for t in tasks:
                weights.setdefault(t["pos"], 1.0)
            cx = cy = (BOARD - 1) / 2.0
            order = sorted(weights, key=lambda xy: (math.atan2(xy[1] - cy, xy[0] - cx), dist(xy, (4, 4))))
            total = sum(weights.values())
            per = total / float(n_chunks)
            zones = [set() for _ in range(n_chunks)]
            acc, zi = 0.0, 0
            for xy in order:
                if acc >= per * (zi + 1) and zi < n_chunks - 1:
                    zi += 1
                zones[zi].add(xy)
                acc += weights[xy]
            self._zone_key = key
            self._zones = zones
        zones = self._zones
        return [zones[i] if i < len(zones) else set() for i in range(n_units)]

    def assign(self, tasks):
        """Zone sweep: a unit finishes every task on its tile, then walks to the
        nearest tile of its zone with pending work. Urgent global tasks (placing a
        carried animal, starving animals, morning pickups, valuable deliveries) override."""
        units = self.units
        day, hour = self.day, self.hour
        last_day = day >= DAYS - 1
        actions = {u["idx"]: ["PASS"] for u in units}
        seeds_left = dict(self.seeds)
        zones = self.zones_for(tasks, len(units))
        by_pos = {}
        for t in tasks:
            by_pos.setdefault(t["pos"], []).append(t)
        claimed = set()          # tiles targeted by a moving unit this turn
        done_here = set()        # (pos, op) already taken by a unit standing there
        shed_wheat = self.shed.get("WHEAT", 0)
        shed_fert = self.shed.get("FERTILIZER", 0)
        feed_pos = {t["pos"] for t in tasks if t["op"][0] == "FEED"}
        fert_pos = {t["pos"] for t in tasks if t["op"][0] == "FERTILIZE"}
        animals_pos = set()
        for x, y, t in self.owned_tiles():
            if isinstance(t, dict) and "animal" in t:
                animals_pos.add((x, y))
        max_reach = (TURNS - 1) if not last_day else (TURNS - 3)

        def feasible(u, t):
            need = t["need"]
            if not need:
                return True
            if need[0] == "SEED":
                return seeds_left.get(need[1], 0) > 0
            return u["inv"].get(need[0], 0) >= need[1]

        def do(u, t):
            need = t["need"]
            if need and need[0] == "SEED":
                seeds_left[need[1]] -= 1
                self.telemetry["plants"] += 1
            done_here.add((t["pos"], t["op"][0]))
            actions[u["idx"]] = t["op"]

        def go(u, target):
            claimed.add(target)
            actions[u["idx"]] = step_toward(u["pos"], target)

        # process the farmer first, then hands in index order (engine order)
        for u in units:
            inv = u["inv"]
            up = u["pos"]
            zone = zones[u["idx"]] if u["idx"] < len(zones) else set()
            st, sd = nearest_shed(up)
            here = [t for t in by_pos.get(up, []) if feasible(u, t) and (up, t["op"][0]) not in done_here]
            carried_animal = [k for k in ANIMALS if inv.get(k, 0) > 0]

            # ---- last day: harvest what is on the tile, otherwise deliver to the shed ----
            if last_day:
                if here and hour <= TURNS - 4:
                    do(u, max(here, key=lambda t: t["value"]))
                    continue
                if any(k in PRODUCTS for k in inv) and hour <= TURNS - 2:
                    if sd == 0:
                        actions[u["idx"]] = ["DROP"]
                    else:
                        go(u, st)
                    continue
                # nearest harvest anywhere
                best, bd = None, 99
                for t in tasks:
                    if t["op"][0] not in ("HARVEST", "COLLECT_FERTILIZER"):
                        continue
                    d = dist(up, t["pos"])
                    if t["pos"] in claimed or hour + d + sd + 2 > TURNS - 2:
                        continue
                    if d < bd:
                        best, bd = t, d
                if best is not None:
                    go(u, best["pos"])
                continue

            # ---- carried animal: go place it ----
            if carried_animal:
                kind = carried_animal[0]
                targets = [xy for xy, k in self.animal_plan.items() if k == kind]
                built = [xy for xy in targets if isinstance(self.tile_at(xy), dict) and self.tile_at(xy).get("kind") == ANIMALS[kind]["structure"] and "animal" not in self.tile_at(xy)]
                pool = built or targets
                if pool:
                    tgt = min(pool, key=lambda xy: dist(up, xy))
                    if up == tgt:
                        tt = self.tile_at(tgt)
                        if tt is None:
                            actions[u["idx"]] = ["BUILD_" + ANIMALS[kind]["structure"]]
                        elif isinstance(tt, dict) and tt.get("kind") == "WEED":
                            actions[u["idx"]] = ["DIG"]
                        else:
                            actions[u["idx"]] = ["PLACE", kind, 1]
                    else:
                        go(u, tgt)
                    continue

            # ---- starving animal anywhere (escape tonight) ----
            urgent_feed = [t for t in tasks if t["op"][0] == "FEED" and t["value"] >= 1000 and t["pos"] not in claimed]
            if urgent_feed and inv.get("WHEAT", 0) > 0:
                t = min(urgent_feed, key=lambda t: dist(up, t["pos"]))
                if dist(up, t["pos"]) + hour <= max_reach:
                    if up == t["pos"]:
                        do(u, t)
                    else:
                        go(u, t["pos"])
                    continue

            # ---- morning logistics at the shed: wheat for the zone's animals, fertilizer for targets ----
            if sd == 0 and hour <= 3:
                zone_animals = sum(1 for p in animals_pos if p in zone)
                need_w = zone_animals - inv.get("WHEAT", 0)
                if need_w > 0 and shed_wheat > 0:
                    n = min(need_w, shed_wheat, 8)
                    shed_wheat -= n
                    actions[u["idx"]] = ["PICKUP", "WHEAT", n]
                    continue
                zone_ferts = sum(1 for p in fert_pos if p in zone)
                need_f = zone_ferts - inv.get("FERTILIZER", 0)
                if need_f > 0 and shed_fert > 0:
                    n = min(need_f, shed_fert, 6)
                    shed_fert -= n
                    actions[u["idx"]] = ["PICKUP", "FERTILIZER", n]
                    continue
                for kind, cnt in self.pending_animals.items():
                    if cnt > 0 and self.shed.get(kind, 0) > 0 and any(k == kind for k in self.animal_plan.values()):
                        self.shed[kind] -= 1
                        actions[u["idx"]] = ["PICKUP", kind, 1]
                        break
                if actions[u["idx"]] != ["PASS"]:
                    continue

            # ---- valuable cargo: deliver so it can be sold today ----
            best_item, best_val = None, 0.0
            poor = self.money < 800
            for item, n in inv.items():
                if item not in PRODUCTS or item == "WHEAT":
                    continue
                if item == "FERTILIZER":
                    zone_ferts_here = sum(1 for p in fert_pos if p in zone)
                    if n <= zone_ferts_here or (fert_pos and hour < 14 and not poor):
                        continue
                    v = (n - zone_ferts_here) * self.prices.get(item, 50) * 0.6
                else:
                    v = n * self.prices.get(item, 10)
                if v > best_val:
                    best_item, best_val = item, v
            deliver_min = 40.0 if poor else DELIVER_MIN_VALUE
            if best_item is not None and best_val >= deliver_min and hour + sd <= 19 and not here:
                if sd == 0:
                    actions[u["idx"]] = ["PLACE", best_item, int(inv[best_item])]
                else:
                    go(u, st)
                continue

            # ---- work on the current tile ----
            if here:
                do(u, max(here, key=lambda t: t["value"]))
                continue

            # ---- blocked feed in own zone and no wheat: fetch some ----
            if inv.get("WHEAT", 0) == 0 and hour <= 19:
                blocked = [p for p in feed_pos if p in zone]
                if blocked and shed_wheat > 0 and hour + sd <= 19:
                    if sd == 0:
                        n = min(len(blocked), shed_wheat, 8)
                        shed_wheat -= n
                        actions[u["idx"]] = ["PICKUP", "WHEAT", n]
                    else:
                        go(u, st)
                    continue

            # ---- sweep: nearest zone tile with feasible pending work ----
            best, bd, bv = None, 99, 0.0
            for pos, ts in by_pos.items():
                if pos not in zone or pos in claimed:
                    continue
                fs = [t for t in ts if feasible(u, t) and (pos, t["op"][0]) not in done_here]
                if not fs:
                    continue
                d = dist(up, pos)
                if hour + d > max_reach:
                    continue
                v = max(t["value"] for t in fs)
                if d < bd or (d == bd and v > bv):
                    best, bd, bv = pos, d, v
            if best is not None:
                go(u, best)
                continue

            # ---- nothing in zone: help elsewhere (value / distance) ----
            best, bs = None, 0.0
            for pos, ts in by_pos.items():
                if pos in claimed:
                    continue
                fs = [t for t in ts if feasible(u, t) and (pos, t["op"][0]) not in done_here]
                if not fs:
                    continue
                d = dist(up, pos)
                if hour + d > max_reach:
                    continue
                sc = max(t["value"] for t in fs) / (1.0 + d)
                if sc > bs:
                    best, bs = pos, sc
            if best is not None:
                go(u, best)
                continue
            # idle: pre-position toward the shed late in the day to shorten tomorrow's walk (farmer only)
        n_pass = sum(1 for a in actions.values() if a == ["PASS"])
        self.pass_today += n_pass
        self.acts_today += len(actions)
        return actions

    # --------------------------------------------------------------- market
    def sell_quantity(self, item, have, inv, endgame, shed_total):
        if endgame:
            return have
        base = MARKET_PARAMS[item]["base"]
        cons = self.cons[item][self.day]
        days_left = DAYS - 1 - self.day
        floor = HOLD_FLOOR_FRAC * base
        if shed_total > 80:
            floor = 0.05 * base
        if days_left <= 1 or cons <= 1.5:
            floor = 1
        n = 0
        for j in range(have):
            if price(item, inv + j) >= floor:
                n += 1
            else:
                break
        hold = have - n
        if hold > 0:
            absorb = cons * days_left
            glut = max(0, inv + n - I0)
            if hold + glut > absorb:
                n = have
        return n

    def market_orders(self):
        day, hour, step = self.day, self.hour, self.step
        if day == 0 and hour == 0:
            self.telemetry["hires"] += 4
            return [list(o) for o in OPENING_ORDERS]
        reserve = self.cash_reserve()
        money = self.money
        endgame = step >= LAST_STEP - 1 or day >= DAYS - 1
        shed_total = sum(self.shed.values())

        incoming = sum(self.pending_animals.values()) + sum(max(0, v) for v in self.animal_orders.values())
        animals_total = self.n_animals + incoming
        carried_wheat = sum(u["inv"].get("WHEAT", 0) for u in self.units)
        need_today = max(0, len(self.unfed) - carried_wheat)
        if day >= DAYS - 1:
            wheat_keep = 0
            wheat_reserve = 0
        elif day == DAYS - 2:
            wheat_keep = need_today
            wheat_reserve = need_today
        elif day <= 5:
            # cash-poor opening: buy only today's feed; never sell what the herd eats in a day
            wheat_keep = need_today + (self.n_animals if hour >= 16 else 0)
            wheat_reserve = need_today + self.n_animals
        else:
            wheat_keep = need_today + (animals_total if hour >= 12 else 0) + 2
            wheat_reserve = need_today + animals_total * 2 + 2
        carried_fert = sum(u["inv"].get("FERTILIZER", 0) for u in self.units)
        fert_uncovered = max(0, self.fert_targets - carried_fert) if (day < DAYS - 1 and hour <= 18) else 0
        fert_reserve = min(self.shed.get("FERTILIZER", 0), fert_uncovered)

        sells = []
        for item in PRODUCTS:
            have = self.shed.get(item, 0)
            if item == "WHEAT":
                have -= wheat_reserve
            elif item == "FERTILIZER":
                have -= fert_reserve
            if have <= 0:
                continue
            n = self.sell_quantity(item, have, self.market_inv[item], endgame, shed_total)
            if n > 0:
                sells.append((self.prices.get(item, 1) * n, ["SELL", item, int(n)]))
        sells.sort(key=lambda s: -s[0])
        for v, _ in sells:
            money += v * 0.9

        prio = []   # (priority, order)
        # hires (also on the last day: harvest + drop labor is nearly free)
        n_hands = len(self.units) - 1
        want = self.hands_target - n_hands
        if day >= DAYS - 1:
            want = min(want, 6 - n_hands) if hour <= 8 else 0
        if want > 0 and hour <= 19 and step < LAST_STEP - 2:
            hire_budget = money - 2
            cost_acc, k, nh = 0, self.hires_today, 0
            for _ in range(want):
                c = _fib(k)
                if cost_acc + c > hire_budget or c > (250 if self.idle_frac < 0.05 else 150):
                    break
                cost_acc += c
                k += 1
                nh += 1
            cap = 8 if hour == 0 else 6
            for _ in range(min(nh, cap)):
                prio.append((90, ["HIRE"]))
            money -= cost_acc
            self.telemetry["hires"] += min(nh, cap)
        if not endgame:
            # feed wheat: top up to wheat_keep
            deficit = wheat_keep - self.shed.get("WHEAT", 0)
            if deficit > 0:
                wp = self.wheat_price() + 3
                room = SHED_CAP - shed_total - 1
                n = int(min(deficit, max(0, room), max(0, money) // max(1, wp)))
                if n > 0:
                    prio.append((100, ["BUY_PRODUCT", "WHEAT", n]))
                    money -= n * wp
            # opening: second melon batch as soon as fertilizer cash arrives
            if 1 <= day <= 3:
                have_melon = self.seeds.get("MELON", 0) + sum(1 for _, _, t in self.owned_tiles() if isinstance(t, dict) and t.get("crop") == "MELON")
                have_melon += sum(1 for c in self.plan.values() if c == "MELON" and False)
                short = OPENING_MELON_TARGET - have_melon
                if short > 0:
                    k = int(min(short, max(0, money - 20) // CROPS["MELON"]["seed"]))
                    if k > 0:
                        prio.append((95, ["BUY_SEED", "MELON", k]))
                        money -= k * CROPS["MELON"]["seed"]
            # fertilizer for today's fertilize targets (+2 units of premium crop each)
            fert_short = fert_uncovered - self.shed.get("FERTILIZER", 0)
            fp = self.prices.get("FERTILIZER", 100) + 2
            if fert_short > 0 and hour <= 16 and fp <= 130:
                room = SHED_CAP - shed_total - 1
                n = int(min(fert_short, 8, max(0, room), max(0, money - reserve) // max(1, fp)))
                if n > 0:
                    prio.append((65, ["BUY_PRODUCT", "FERTILIZER", n]))
                    money -= n * fp
            # land
            if self.land_wanted:
                n_extra = len(self.unlocked) - 1
                if n_extra < len(LAND_ORDER) and money - reserve >= LAND_PRICES[n_extra]:
                    prio.append((70, ["BUY_LAND"]))
                    money -= LAND_PRICES[n_extra]
                    self.land_wanted = False
                    self.telemetry["land"].append(day)
            # animals
            for kind, cnt in list(self.animal_orders.items()):
                if cnt <= 0:
                    continue
                cost = ANIMALS[kind]["cost"]
                room = SHED_CAP - shed_total - 2
                n = int(min(cnt, max(0, (money - reserve) // cost), max(0, room)))
                if n > 0:
                    prio.append((60, ["BUY_ANIMAL", kind, n]))
                    money -= n * cost
                    self.animal_orders[kind] = cnt - n
                    self.telemetry["animals"][kind] = self.telemetry["animals"].get(kind, 0) + n
            # seeds for planned plantings on empty tiles
            if hour <= 21:
                need = {}
                for xy, crop in self.plan.items():
                    if self.tile_at(xy) is None or self.is_weed(xy):
                        need[crop] = need.get(crop, 0) + 1
                for crop, n in sorted(need.items(), key=lambda kv: -CROPS[kv[0]]["seed"]):
                    short = n - self.seeds.get(crop, 0)
                    if short <= 0:
                        continue
                    cost = CROPS[crop]["seed"]
                    k = int(min(short, max(0, (money - reserve * 0.5) // cost)))
                    if k > 0:
                        prio.append((50, ["BUY_SEED", crop, k]))
                        money -= k * cost
        # assemble: top sells (by value) get priority 80, others 40
        for i, (v, o) in enumerate(sells):
            prio.append((80 if i < 3 else 40, o))
        prio.sort(key=lambda p: -p[0])
        chosen = [o for _, o in prio[:MAX_ORDERS]]
        # engine processes orders in list order: sells first so proceeds fund buys
        chosen.sort(key=lambda o: 0 if o[0] == "SELL" else 1)
        return chosen

    # ------------------------------------------------------------------ act
    def act(self, obs):
        self.parse(obs)
        self.last_step = self.step
        # pending animals = in shed + carried
        for kind in ANIMALS:
            in_shed = self.shed.get(kind, 0)
            carried = sum(u["inv"].get(kind, 0) for u in self.units)
            self.pending_animals[kind] = in_shed + carried
        # clean animal plans
        for xy in list(self.animal_plan.keys()):
            t = self.tile_at(xy)
            if isinstance(t, dict) and ("animal" in t or t.get("kind") == "PLANT"):
                self.animal_plan.pop(xy, None)
        n_pending = sum(self.pending_animals.values()) + sum(max(0, v) for v in self.animal_orders.values())
        if n_pending == 0:
            self.animal_plan = {}
        else:
            # per kind: keep at most (pending + ordered) plans, preferring built structures
            keep = {}
            for kind in ANIMALS:
                quota = self.pending_animals.get(kind, 0) + max(0, self.animal_orders.get(kind, 0))
                plans = [(xy, k) for xy, k in self.animal_plan.items() if k == kind]
                plans.sort(key=lambda p: 0 if isinstance(self.tile_at(p[0]), dict) else 1)
                for xy, k in plans[:quota]:
                    keep[xy] = k
            self.animal_plan = keep
        n_free = sum(1 for _, _, t in self.owned_tiles() if t is None or (isinstance(t, dict) and t.get("kind") == "WEED"))
        unplanned = sum(1 for x, y, t in self.owned_tiles() if (t is None or (isinstance(t, dict) and t.get("kind") == "WEED")) and (x, y) not in self.plan and (x, y) not in self.animal_plan)
        if (self.hour % 6 == 0 or self.plan_day_idx != self.day or len(self.unlocked) != getattr(self, "_planned_unlocked", 0)
                or unplanned >= 3):
            self.plan_day()
            self._planned_unlocked = len(self.unlocked)
        else:
            self.build_forecast()
        tasks = self.build_tasks()
        actions = self.assign(tasks)
        orders = self.market_orders()
        farmer = actions.get(0, ["PASS"])
        hands = [actions.get(i, ["PASS"]) for i in range(1, len(self.units))]
        return {"farmer": farmer, "hands": hands, "market": orders}


_BRAINS = {}


def agent(obs, config=None):
    player = int(obs["player"])
    step = int(obs.get("step", 0))
    brain = _BRAINS.get(player)
    if brain is None or step == 0 or step < brain.last_step:
        brain = Brain(player)
        _BRAINS[player] = brain
    try:
        return brain.act(obs)
    except Exception as exc:  # never crash: fall back to a safe action
        brain.errors += 1
        brain.telemetry["errors"] = brain.errors
        brain.telemetry["last_error"] = repr(exc)
        n_hands = len(obs["farms"][player].get("hands", []))
        return {"farmer": ["PASS"], "hands": [["PASS"] for _ in range(n_hands)], "market": []}


agent.telemetry = _BRAINS
