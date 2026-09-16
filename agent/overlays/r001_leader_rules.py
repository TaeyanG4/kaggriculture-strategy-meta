# SPDX-License-Identifier: Apache-2.0
# r001_leader_rules (reverse-engineering series, 2026-09-15). Appended to agent/o001_demand_planner.py
# (Claude-written operator: parsing, task building, worker assignment, market execution).
"""Level-2 behavioural clone of the #1 team (Majkel1337) as a RULE policy, not a tape.

Why not tape retrieval: r001_leader_clone (per-day nearest-neighbour replay of 337 leader games)
collapsed to ~45k because the leader plays at $1-5 cash margins; a $1 price difference caused by
the opponent's step-0 trade changed 4 hires into 3 and the whole tape cascaded. The leader's
policy is therefore "buy/hire what is affordable toward a target farm", which needs a rule engine.

Targets = the leader's per-day MEDIAN farm from 337 public replays (o_replays/leader*,
state/o_dev/r001/leader_targets.json): counts of COW/SHEEP/GOOSE, MELON/WHEAT/STRAWBERRY/
CARROT, TOMATO conditioned on the number of tomato shops (PIZZA/FARMERS), quadrants (NE ~day 6-7,
SW ~day 9-10, never SE), hires per day. The o001 operator executes toward those targets (plant,
water, feed, care, harvest, deliver, hire, sell). Extra leader rules: never buy FERTILIZER; hold
STRAWBERRY/TOMATO/WOOL on days 26-27 (shed room permitting) and drip them out on day 29.
Recorded facts only shape the targets; every action is produced by our own operator.
"""
import copy as _r1_copy
import math as _r1_math

_R1_T = %(targets)s   # day -> dict(COW,SHEEP,GOOSE,MELON,WHEAT,STRAWBERRY,CARROT,quads,tomato_by_shops{shops:tiles})
_R1_HIRES = %(hires)s
_R1_TOM_SHOPS = ("PIZZA_SHOP", "FARMERS_MARKET")
_R1_HOLD_ITEMS = ("STRAWBERRY", "TOMATO", "WOOL")
_R1_HOLD_DAYS = (26, 28)      # hold on days 26..27
_R1_SHED_ROOM = 85


def _r1_target(day, n_tom_shops):
    t = dict(_R1_T[min(day, 29)])
    tb = t.get("tomato_by_shops") or {}
    key = str(min(3, n_tom_shops))
    t["TOMATO"] = tb.get(key, t.get("TOMATO", 0))
    return t


class LeaderBrain(Brain):
    def plan_day(self):
        day, hour = self.day, self.hour
        if hour == 0 and day > 0:
            if self.acts_today > 0:
                self.idle_frac = self.pass_today / float(self.acts_today)
                self.telemetry["idle"].append(round(self.idle_frac, 2))
            self.pass_today = 0
            self.acts_today = 0
        self.build_forecast()
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
        if day == 0 and hour == 0:
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
            self.hands_target = _R1_HIRES[0]
            self.plan_day_idx = day
            return
        n_tom = sum(1 for s in self.shops if s in _R1_TOM_SHOPS)
        T = _r1_target(day + (1 if hour >= 12 else 0), n_tom)
        reserve = self.cash_reserve()
        budget = self.money - reserve
        feed_price = self.wheat_price() + 3
        shed_room = SHED_CAP - sum(self.shed.values())
        # ---- animals toward target counts ----
        have = {}
        for _, _, t in self.owned_tiles():
            if isinstance(t, dict) and "animal" in t:
                have[t["animal"]] = have.get(t["animal"], 0) + 1
        for kind, n in self.pending_animals.items():
            planned = sum(1 for k in self.animal_plan.values() if k == kind)
            while planned < n and free:
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
                planned += 1
        orders = {}
        if day <= DAYS - 8:
            for kind in ("COW", "SHEEP", "GOOSE"):
                want = int(T.get(kind, 0)) - have.get(kind, 0) - self.pending_animals.get(kind, 0) - sum(1 for k in self.animal_plan.values() if k == kind)
                while want > 0 and free and shed_room > 2 and ANIMALS[kind]["cost"] + 2 * feed_price <= budget:
                    budget -= ANIMALS[kind]["cost"] + 2 * feed_price
                    shed_room -= 1
                    orders[kind] = orders.get(kind, 0) + 1
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
                    want -= 1
        self.animal_orders = orders
        # ---- crops toward target counts (priority order) ----
        seed_budget = budget
        have_crop = {}
        for _, _, t in self.owned_tiles():
            if isinstance(t, dict) and t.get("kind") == "PLANT":
                have_crop[t["crop"]] = have_crop.get(t["crop"], 0) + 1
        for c in list(self.plan.values()):
            have_crop[c] = have_crop.get(c, 0) + 1
        new_plan = dict(self.plan)
        free = [xy for xy in free if xy not in new_plan]
        order = ["MELON", "STRAWBERRY", "TOMATO", "WHEAT", "CARROT"] if day <= 8 else ["TOMATO", "STRAWBERRY", "WHEAT", "CARROT", "MELON"]
        if day >= 23:
            order = ["TOMATO", "CARROT", "WHEAT", "STRAWBERRY", "MELON"]
        for crop in order:
            if crop == "MELON" and day > 3:
                continue
            if crop == "STRAWBERRY" and day > 13:
                continue
            if crop == "TOMATO" and day > 21:
                continue
            if crop == "CARROT" and day < 22:
                continue
            # target minus growing tiles minus tiles already planned; seeds on hand cover the
            # first plans for free, further plans need seed budget. Never exceed the target.
            want = int(T.get(crop, 0)) - have_crop.get(crop, 0)
            onhand = self.seeds.get(crop, 0)
            while free and want > 0:
                if onhand > 0:
                    onhand -= 1
                elif CROPS[crop]["seed"] <= seed_budget:
                    seed_budget -= CROPS[crop]["seed"]
                else:
                    break
                tile = free.pop(0)
                new_plan[tile] = crop
                want -= 1
        # remaining free land: wheat if affordable (the leader keeps 22-32 wheat tiles)
        for tile in list(free):
            if day > DAYS - 6 or CROPS["WHEAT"]["seed"] > seed_budget:
                break
            seed_budget -= CROPS["WHEAT"]["seed"]
            new_plan[tile] = "WHEAT"
            free.remove(tile)
        self.plan = new_plan
        # ---- land: NE from day 6, SW from day 9, never SE ----
        self.land_wanted = False
        n_extra = len(self.unlocked) - 1
        if n_extra < 2 and day >= (6 if n_extra == 0 else 9) and self.money >= LAND_PRICES[n_extra] + reserve:
            self.land_wanted = True
        # ---- hands: leader's daily hire count ----
        target = _R1_HIRES[min(day, 29)]
        if day >= DAYS - 1:
            target = min(target, 8)
        self.hands_target = target
        self.plan_day_idx = day

    def market_orders(self):
        orders = Brain.market_orders(self)
        day, hour = self.day, self.hour
        out = []
        held = sum(self.shed.values()) + sum(sum(u["inv"].values()) for u in self.units)
        for o in orders:
            if o and o[0] == "BUY_PRODUCT" and len(o) >= 2 and o[1] == "FERTILIZER":
                continue
            if _R1_HOLD_DAYS[0] <= day < _R1_HOLD_DAYS[1] and o and o[0] == "SELL" and len(o) >= 3 and o[1] in _R1_HOLD_ITEMS and held <= _R1_SHED_ROOM:
                self.telemetry["r001_held"] = self.telemetry.get("r001_held", 0) + int(o[2])
                continue
            out.append(o)
        if day >= 29 and self.step < LAST_STEP - 1:
            selling = {o[1] for o in out if o and o[0] == "SELL" and len(o) >= 3}
            for item in _R1_HOLD_ITEMS:
                q = int(self.shed.get(item, 0))
                if q > 0 and item not in selling and len(out) < MAX_ORDERS:
                    out.append(["SELL", item, max(1, int(_r1_math.ceil(q / 6.0)))])
        return out[:MAX_ORDERS]


def agent(obs, config=None):
    player = int(obs["player"])
    step = int(obs.get("step", 0))
    brain = _BRAINS.get(player)
    if brain is None or step == 0 or step < brain.last_step or not isinstance(brain, LeaderBrain):
        brain = LeaderBrain(player)
        _BRAINS[player] = brain
    try:
        return brain.act(obs)
    except Exception as exc:
        brain.errors += 1
        brain.telemetry["errors"] = brain.errors
        brain.telemetry["last_error"] = repr(exc)
        n_hands = len(obs["farms"][player].get("hands", []))
        return {"farmer": ["PASS"], "hands": [["PASS"] for _ in range(n_hands)], "market": []}


agent.telemetry = _BRAINS
