# c210 planner late-feed focus (GPT/c-series, 2026-09-16). c207 baseline plus one narrow scheduler rule: from hour 16,
# while any FEED task remains and wheat is reachable, animal workers stop taking same-tile CARE/collect/harvest detours
# and clear stale assignments so they can finish feeding the herd before day end. Research candidate only.
# planners' macro policy (Majkel1337 stats, o_results/proxy/Majkel1337_policy.json): day-0 melon/wheat + 2 cows/3 sheep,
# strawberries d2-4 and d6, land d6/d9, world-conditional animals at d6/d9, wheat blocks d9-11, hands 4->11,
# daily water/feed/care/collect/fertilize routine with nearest-task dispatch, and small-batch buffered selling.
# Used only as a validation opponent (docs/o-planner-proxy-plan.ko.md). Not a submission candidate.
import os as _os, random
_FLAGS = set((_os.environ.get('PROXY_FLAGS') or '').split(','))
_KNOBS = dict(kv.split('=') for kv in (_os.environ.get('PROXY_KNOBS') or '').split(',') if '=' in kv)   # sweepable knobs (o_tools/proxy_sweep.py)

MOVES = {'NORTH': (0, -1), 'SOUTH': (0, 1), 'EAST': (1, 0), 'WEST': (-1, 0)}
MILK_SHOPS = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
EGG_SHOPS = ('BAKERY', 'BRUNCH_SPOT')
SHED = [(4, 4), (5, 4), (4, 5), (5, 5)]
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
CROP_FIRST = {'WHEAT': 2, 'CARROT': 2, 'TOMATO': 8, 'STRAWBERRY': 10, 'MELON': 10}
CROP_LAST = {'WHEAT': 4, 'CARROT': 3, 'MELON': 12}
ONGOING = {'TOMATO': 1, 'STRAWBERRY': 2}
ANIMAL_STRUCT = {'COW': 'PASTURE', 'SHEEP': 'PASTURE', 'GOOSE': 'COOP'}
ANIMAL_FIRST = {'GOOSE': 4, 'COW': 8, 'SHEEP': 6}; ANIMAL_INT = {'GOOSE': 1, 'COW': 2, 'SHEEP': 3}
BUFFER = {'MILK': int(_KNOBS.get('buf', 4)), 'WOOL': int(_KNOBS.get('buf', 4)), 'STRAWBERRY': 2, 'MELON': 0, 'EGG': 0, 'CARROT': 0, 'TOMATO': 0, 'FERTILIZER': 1, 'WHEAT': 0}
BATCH = {'MILK': 3, 'WOOL': 3, 'STRAWBERRY': 4, 'MELON': 12, 'EGG': 6, 'CARROT': 9, 'TOMATO': 5, 'FERTILIZER': 3, 'WHEAT': 7}
HANDS_BY_DAY = [4, 4, 6, 6, 6, 6, 8, 9, 9, 10, 11, 11] + [11] * 18
_STATE = {}


def quadrant(x, y):
    return ('N' if y < 5 else 'S') + ('W' if x < 5 else 'E')


def world_bucket(shops):
    if 'YARN_STORE' in shops[:2]:
        return 'yarn'
    return 'milk%d' % min(3, sum(s in MILK_SHOPS for s in shops[:3]))


ANIMAL_TOTALS = {'yarn': {'SHEEP': 12, 'COW': 6}, 'milk0': {'GOOSE': 4, 'COW': 6, 'SHEEP': 5}, 'milk1': {'GOOSE': 2, 'COW': 8, 'SHEEP': 4},
                 'milk2': {'GOOSE': 1, 'COW': 10, 'SHEEP': 4}, 'milk3': {'COW': 13, 'SHEEP': 3}}   # dict order = purchase order (geese pay back in days)


def animal_plan(bucket, day, have):
    """Shortfall to Majkel's peak herd by world, bought from day 6 as cash allows (order: the world's main product first)."""
    if day < 6 or day > 18:
        return {}   # herd shortfall is still worth closing until d18 (a d15 cow/sheep repays 2x before d30)
    tot = ANIMAL_TOTALS.get(bucket, ANIMAL_TOTALS['milk1'])
    return {k: v - have.get(k, 0) for k, v in tot.items() if v - have.get(k, 0) > 0}


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def step_toward(pos, target):
    dx, dy = target[0] - pos[0], target[1] - pos[1]
    if dx != 0 and (abs(dx) >= abs(dy) or dy == 0):
        return ['EAST'] if dx > 0 else ['WEST']
    if dy != 0:
        return ['SOUTH'] if dy > 0 else ['NORTH']
    return None


def nearest_shed(pos):
    return min(SHED, key=lambda s: dist(pos, s))


class Proxy:
    def __init__(self, seat):
        self.seat = seat; self.last_step = -1; self.day_plan = {}; self.claims = {}; self.pending_sell = {}
        self.bought = {}; self.assign = {}; self.assign_day = -1; self.zone_of = {}; self.zone_key = None; self.owner = {}; self.strips = {}; self.cursor = {}; self.fert_demand = 0

    # ---------------- daily macro ----------------
    def free_tiles(self, farm, prefer=None):
        out = []
        for y, row in enumerate(farm['tiles']):
            for x, t in enumerate(row):
                if t is None:
                    out.append((x, y))
        if prefer:
            out.sort(key=lambda p: (quadrant(*p) != prefer, dist(p, (4, 4))))
        else:
            out.sort(key=lambda p: dist(p, (4, 4)))
        return out

    def market_orders(self, obs, farm, day, hour, bucket):
        """Cash-flow driven just-in-time buying (Majkel style): sales first, then the day's priority list, buying
        as many units as the current money allows; unfilled targets are retried every hour."""
        orders = []
        money = farm['money']; shed = obs['private']['shed']; seeds = obs['private']['seeds']; prices = obs['market']['prices']
        placed = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal'))
        invs = obs['private'].get('inventories', []) or []
        unplaced = sum(shed.get(k, 0) for k in ANIMAL_STRUCT) + sum((inv or {}).get(k, 0) for inv in invs for k in ANIMAL_STRUCT)
        animals = placed + unplaced
        inv_wheat = sum((inv or {}).get('WHEAT', 0) for inv in invs)
        free = len(self.free_tiles(farm))
        terminal = day >= 28
        # --- sales (generate cash first) ---
        for item in PRODUCTS:
            stock = shed.get(item, 0)
            if item == 'WHEAT':
                early_dump = 'wsell' in _FLAGS and day <= 5
                reserve = 0 if day >= 29 else (animals if early_dump else (animals * 3 + 2 if day <= 9 else (min(animals + 4, 20) if day <= 10 else min(animals + 2, 16))))
                extra = stock - reserve
                if extra > 0 and (hour >= 14 or early_dump) and (terminal or early_dump or extra >= BATCH['WHEAT']):
                    orders.append(['SELL', 'WHEAT', extra if (terminal or day >= 12) else BATCH['WHEAT']])
                continue
            if stock <= 0:
                continue
            buf = BUFFER[item] if (farm['money'] >= 3000 and day < 27) else 0   # buffers only once cash flow allows
            if day <= 9 and len(farm['unlocked_quadrants']) < 3 and item != 'FERTILIZER':
                orders.append(['SELL', item, stock]); continue   # land/herd build-up phase: liquidate at once (Majkel sells the first wool/milk in one batch)
            if item == 'FERTILIZER' and 6 <= day <= 26:
                buf = min(16, 2 + self.fert_demand)   # reserve today's FERTILIZE demand (planters draw from the shed), sell the rest
            if terminal:
                orders.append(['SELL', item, stock])
            elif stock > buf:
                orders.append(['SELL', item, min(BATCH[item], stock - buf)])
        # --- purchase priorities for today ---
        want_hands = HANDS_BY_DAY[min(day, 29)]
        pri = []
        if len(farm['hands']) < want_hands and hour <= 3 and money >= 1:
            pri.append(('HIRE', None, want_hands - len(farm['hands'])))
        melons_have = seeds.get('MELON', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'MELON')
        cows_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') == 'COW') + shed.get('COW', 0) + sum((inv or {}).get('COW', 0) for inv in invs)
        if day == 0:
            # melons first: the first dozen melons sold at day 10 fetch ~$800 each (first-mover on a log-priced product)
            pri += [('ANIMAL', 'COW', 2), ('ANIMAL', 'SHEEP', 3), ('PRODUCT', 'WHEAT', 5), ('SEED', 'MELON', 6), ('SEED', 'WHEAT', 11)]
        elif day <= 5:
            straw_have = seeds.get('STRAWBERRY', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY')
            pri += [('SEED', 'MELON', max(0, (10 if day == 1 else 12) - melons_have) if day <= 2 else 0), ('ANIMAL', 'COW', max(0, 2 - cows_have))]
            if day >= 2:
                pri.append(('SEED', 'STRAWBERRY', max(0, 8 - straw_have)))
            if melons_have >= 12 and straw_have >= (8 if day >= 2 else 0):
                pri.append(('SEED', 'WHEAT', max(0, min(10, free) - seeds.get('WHEAT', 0))))
        elif 6 <= day <= 14:
            have = {}
            for row in farm['tiles']:
                for t in row:
                    if isinstance(t, dict) and t.get('animal'):
                        have[t['animal']] = have.get(t['animal'], 0) + 1
            for k in ANIMAL_STRUCT:
                have[k] = have.get(k, 0) + shed.get(k, 0) + sum((inv or {}).get(k, 0) for inv in invs)
            pri += [('LAND', None, 1)]
            straw_have = seeds.get('STRAWBERRY', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY')
            straw_item = [('SEED', 'STRAWBERRY', max(0, min(int(_KNOBS.get('straw', 26)) - straw_have, 11 if day == 6 else (4 if day <= 9 else 3))))] if day <= 12 else []
            anim_items = [('ANIMAL', k, n) for k, n in animal_plan(bucket, day, have).items()]
            pri += (anim_items + straw_item) if ('anim6' in _FLAGS and day <= 8) else (straw_item + anim_items)
            if day >= 9:
                pri += [('SEED', 'WHEAT', max(0, free - sum(int(v) for v in seeds.values())))]
        elif day <= 25:
            if day <= 20:
                pri.append(('LAND', None, 1))
            shops = obs['town'].get('unlocked_shops', []) or []
            carrot_demand = sum(sh in ('PET_CAFE', 'FARMERS_MARKET') for sh in shops)
            if carrot_demand and day <= 26:
                pri.append(('SEED', 'CARROT', max(0, min(8, free // 2) - seeds.get('CARROT', 0))))
            tomato_demand = sum(sh in ('PIZZA_SHOP', 'FARMERS_MARKET') for sh in shops)
            tomatoes_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'TOMATO')
            if tomato_demand and 15 <= day <= 19:
                pri.append(('SEED', 'TOMATO', max(0, min(8, free // 2) - seeds.get('TOMATO', 0) - tomatoes_have)))
            pri += [('SEED', 'WHEAT', max(0, free - seeds.get('WHEAT', 0) - seeds.get('CARROT', 0) - seeds.get('TOMATO', 0)))]
            if day <= 14:
                pri.append(('SEED', 'STRAWBERRY', 2))
        if placed and day < 29 and shed.get('WHEAT', 0) + inv_wheat < placed:
            pri.insert(0, ('PRODUCT', 'WHEAT', placed - shed.get('WHEAT', 0) - inv_wheat))
        bought = self.bought.setdefault(day, {})
        # keep a little cash for tomorrow's first hires (fib 1,1,2,3) and feed emergencies
        money -= 25 if day == 0 else (12 if day < 8 else 0)
        seed_price = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
        animal_price = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
        land_price = [1000, 2000, 4000][min(2, len(farm['unlocked_quadrants']) - 1)]
        free_left = free - sum(int(v) for v in seeds.values()) - unplaced   # tiles still open for new seeds/animals
        for kind, item, target in pri:
            if len(orders) >= 10:
                break
            key = (kind, item)
            if kind == 'PRODUCT':
                done = 0   # feed top-up is re-evaluated from the shed every hour
            else:
                done = bought.get(key, 0)
            left = target - done
            if left <= 0:
                continue
            if kind == 'HIRE':
                n = 0; h = int(farm.get('hires_today', 0)); cash = farm['money']
                fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
                while n < left and cash >= fib[min(h + n, 13)]:
                    cash -= fib[min(h + n, 13)]; n += 1
                money -= farm['money'] - cash
                for _ in range(n):
                    orders.append(['HIRE'])
            elif kind == 'LAND':
                q = len(farm['unlocked_quadrants'])
                if q >= 3 or not ((q == 1 and day >= 6) or (q == 2 and day >= int(_KNOBS.get('land3', 7)))):
                    continue   # Majkel: quadrant 2 on day 6 and quadrant 3 on day 9 in every archived game
                if money >= land_price:
                    orders.append(['BUY_LAND']); money -= land_price; bought[key] = done + 1; free_left += 25
                elif day <= 12:
                    break   # save the day's cash for the land instead of buying seeds/animals that have no tile
            elif kind == 'ANIMAL':
                n = min(left, int(money // animal_price[item]), max(0, free_left))
                if n > 0:
                    orders.append(['BUY_ANIMAL', item, n]); money -= n * animal_price[item]; bought[key] = done + n; free_left -= n
            elif kind == 'SEED':
                n = min(left, int(money // seed_price[item]), max(0, free_left))
                if n > 0:
                    orders.append(['BUY_SEED', item, n]); money -= n * seed_price[item]; bought[key] = done + n; free_left -= n
            elif kind == 'PRODUCT':
                unit = prices.get(item, 25) + 2
                n = min(left, int(money // unit))
                if n > 0:
                    orders.append(['BUY_PRODUCT', item, n]); money -= n * unit
        return orders[:10]

    # ---------------- step scheduler ----------------
    def tasks(self, obs, farm, day, hour):
        """Return the list of (priority, (x,y), op, needs) for today."""
        out = []
        shops = obs['town'].get('unlocked_shops', [])
        n_anim = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal'))
        feed_short = obs['private']['shed'].get('WHEAT', 0) + sum((inv or {}).get('WHEAT', 0) for inv in (obs['private'].get('inventories') or [])) < n_anim + 2
        seeds_waiting = sum(int(v) for v in obs['private']['seeds'].values()) > sum(1 for row in farm['tiles'] for t in row if t is None)
        for y, row in enumerate(farm['tiles']):
            for x, t in enumerate(row):
                if not isinstance(t, dict):
                    continue
                if t.get('kind') == 'PLANT':
                    crop = t['crop']; age = day - t['planted_day']
                    mature = age >= CROP_FIRST[crop]
                    last = age >= CROP_LAST.get(crop, 99) and (t.get('watered_today') or hour >= 20 or crop not in ('WHEAT', 'MELON'))   # water first on the last window day
                    if mature and t.get('yield_units', 0) > 0 and (crop in ONGOING or last or t['yield_units'] >= ((int(_KNOBS.get('wheat_units', 5)) if age >= 3 else 5) if crop == 'WHEAT' else 6)   # fertilized wheat: 5 units at age 3 (1.25/day) beats 6 at age 4
                                                                  or (crop == 'WHEAT' and day <= 8 and (feed_short or seeds_waiting) and t['yield_units'] >= 2)):
                        out.append((1, (x, y), ['HARVEST'], None))
                    if not t.get('watered_today'):
                        # Majkel's watering economy: water on planting day, on yield-window days, and whenever a skipped day
                        # would become a weed (2 unwatered days); every other day is skipped (e.g. wheat age 1, strawberry off-days)
                        must = age == 0 or t.get('consecutive_unwatered', 0) >= 1
                        window = ((crop == 'WHEAT' and 2 <= age <= 4) or (crop == 'CARROT' and 2 <= age <= 3) or (crop == 'MELON' and 6 <= age <= 12)
                                  or (crop == 'STRAWBERRY' and age >= 9 and (age - 9) % 2 == 0) or (crop == 'TOMATO' and age >= 7))
                        if must or window:
                            out.append(((0 if hour >= 16 else 1) if must else (2 if hour >= 12 else 3), (x, y), ['WATER'], None))
                    fert_ok = t.get('fertilized_until_day', -1) < day
                    if fert_ok and crop in ONGOING and age >= CROP_FIRST[crop] - 1 and (age - (CROP_FIRST[crop] - 1)) % ONGOING[crop] == 0:
                        out.append((0 if crop == 'STRAWBERRY' else 2, (x, y), ['FERTILIZE'], 'FERTILIZER'))   # strawberries first (c207): the age-9/13 dose must land before the production watering
                    elif fert_ok and crop == 'WHEAT' and age == 2:
                        out.append((3, (x, y), ['FERTILIZE'], 'FERTILIZER'))   # age 2 covers all three window waterings (3 -> 6 units)
                elif t.get('animal'):
                    yu = t.get('yield_units', 0)
                    if yu >= 2 or (yu >= 1 and day >= 27):
                        out.append((1 if yu >= 4 else 2, (x, y), ['HARVEST'], None))
                    prod_price = obs['market']['prices'].get({'COW': 'MILK', 'SHEEP': 'WOOL', 'GOOSE': 'EGG'}[t['animal']], 0)
                    worth = day < 27 or 'nofeedskip' in _FLAGS or prod_price >= obs['market']['prices'].get('WHEAT', 25)
                    if not t.get('fed_today') and day < 29 and worth:
                        out.append((0, (x, y), ['FEED'], 'WHEAT'))
                    if not t.get('cared_today') and day < 28:
                        out.append((1, (x, y), ['CARE'], None))
                    if t.get('fertilizer_available'):
                        out.append((2, (x, y), ['COLLECT_FERTILIZER'], None))
                elif t.get('kind') == 'WEED':
                    out.append((2, (x, y), ['DIG'], None))
        return out

    def plan_placements(self, obs, farm, day):
        """Animals waiting in the shed -> build + place; seeds -> plant on free tiles (NW first, then new land)."""
        shed = obs['private']['shed']; seeds = obs['private']['seeds']; out = []
        invs = obs['private'].get('inventories', []) or []
        for kind in ('COW', 'SHEEP', 'GOOSE'):
            n = shed.get(kind, 0) + sum((inv or {}).get(kind, 0) for inv in invs)
            if n <= 0:
                continue
            struct = ANIMAL_STRUCT[kind]
            empties = [(x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row) if isinstance(t, dict) and t.get('kind') == struct and 'animal' not in t]
            for p in empties[:n]:
                out.append((0, p, ['PLACE', kind], kind))
            missing = n - len(empties)
            if missing > 0:
                herd = [(x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row) if isinstance(t, dict) and t.get('kind') in ('PASTURE', 'COOP')]
                anchors = herd or [(4, 4)]
                cands = self.free_tiles(farm, 'NW' if day < 6 else None)
                cands.sort(key=lambda q: (min(dist(q, a) for a in anchors), dist(q, (4, 4))))
                for q in cands[:missing]:
                    out.append((0, q, ['BUILD_' + struct], None))
        for crop in ('MELON', 'STRAWBERRY', 'WHEAT', 'CARROT', 'TOMATO'):
            n = seeds.get(crop, 0)
            if n <= 0:
                continue
            for p in self.free_tiles(farm, 'NW' if day < 6 else None)[:n]:
                out.append((1, p, ['PLANT', crop], None))
        return out

    def act(self, obs):
        step = int(obs['step']); day = step // 24; hour = step % 24
        farm = obs['farms'][self.seat]; priv = obs['private']
        positions = [tuple(farm['farmer'])] + [tuple(p) for p in farm['hands']]
        invs = priv.get('inventories', []) or []
        invs = invs + [{}] * (len(positions) - len(invs))
        bucket = world_bucket(obs['town'].get('unlocked_shops', []))
        tasks = self.plan_placements(obs, farm, day) + self.tasks(obs, farm, day, hour)
        self.fert_demand = sum(1 for t in tasks if t[2][0] == 'FERTILIZE')
        orders = self.market_orders(obs, farm, day, hour, bucket)
        # placement tasks for free tiles must not collide: take unique tiles in order
        seen = set(); uniq = []
        for t in sorted(tasks, key=lambda t: t[0]):
            key = (t[1], t[2][0])
            if key in seen:
                continue
            seen.add(key); uniq.append(t)
        tasks = uniq
        cmds = []
        taken = set()
        task_index = {(t[1], t[2][0]): t for t in tasks}
        # zones: worker 0 (farmer) + 1 feeder per 5 animals take animal duty; the rest split plant quadrants by load
        n_workers = len(positions)
        animal_tiles = {t[1] for t in tasks if t[2][0] in ('FEED', 'CARE', 'COLLECT_FERTILIZER') or (t[2][0] == 'HARVEST' and isinstance(farm['tiles'][t[1][1]][t[1][0]], dict) and farm['tiles'][t[1][1]][t[1][0]].get('animal'))}
        n_animals = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal'))
        n_animals += sum(priv['shed'].get(k, 0) for k in ANIMAL_STRUCT) + sum((inv or {}).get(k, 0) for inv in invs for k in ANIMAL_STRUCT)
        feed_ratio = float(_KNOBS.get('feed', {'milk0': 6.0, 'milk1': 6.0, 'milk2': 5.0, 'milk3': 4.5, 'yarn': 5.0}.get(bucket, 5.0)))   # world table from c206 (holdout +2.4k)
        n_feeders = min(max(1, n_workers - 3), max(1, int(round(n_animals / feed_ratio)))) if n_animals else 0
        quads = {}
        for y, row in enumerate(farm['tiles']):
            for x, t in enumerate(row):
                if t is None or (isinstance(t, dict) and t.get('kind') in ('PLANT', 'WEED')):
                    q = quadrant(x, y); quads[q] = quads.get(q, 0) + 1
        zone_key = (day, n_workers, n_feeders)
        if self.zone_key == zone_key:
            zone_of = self.zone_of
        else:
            zone_of = {}
        plant_workers = list(range(n_feeders, n_workers))
        if not zone_of and plant_workers and quads:
            total = sum(quads.values()); order = sorted(quads, key=lambda q: -quads[q]); k = 0
            for q in order:
                share = max(1, round(len(plant_workers) * quads[q] / total))
                for _ in range(share):
                    if k < len(plant_workers):
                        zone_of[plant_workers[k]] = q; k += 1
            while k < len(plant_workers):
                zone_of[plant_workers[k]] = order[k % len(order)]; k += 1
        if self.zone_key != zone_key:
            for i in range(n_feeders):
                zone_of[i] = 'ANIMALS'
            # strips: split each zone's work tiles (plants + free tiles) among its workers in snake order
            owner = {}; strips = {}
            for q in set(zone_of.values()):
                if q == 'ANIMALS':
                    continue
                ws = [w for w, z in zone_of.items() if z == q]
                tiles_q = [(x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row)
                           if quadrant(x, y) == q and (t is None or (isinstance(t, dict) and t.get('kind') in ('PLANT', 'WEED')))]
                tiles_q.sort(key=lambda p: (p[1], p[0] if p[1] % 2 == 0 else -p[0]))
                for idx, tile in enumerate(tiles_q):
                    w = ws[idx * len(ws) // max(1, len(tiles_q))]
                    owner[tile] = w; strips.setdefault(w, []).append(tile)
            self.owner = owner; self.strips = strips; self.cursor = {}
            self.zone_of, self.zone_key = zone_of, zone_key
        owner = self.owner
        if day != self.assign_day:
            self.assign = {}; self.assign_day = day
        for i, pos in enumerate(positions):
            inv = invs[i] or {}
            # deposit harvested goods when standing next to the shed and carrying a lot
            is_feeder = zone_of.get(i) == 'ANIMALS'
            keep = () if day >= 28 else (('WHEAT',) if is_feeder else (('FERTILIZER',) if day >= 9 else ()))   # feeders bank fertilizer; planters keep it for FERTILIZE from d9
            carried = {k: v for k, v in inv.items() if k in PRODUCTS and k not in keep}
            if day >= 29 and hour >= 18 and sum(carried.values()) >= 1:
                if pos in SHED:
                    item = max(carried, key=carried.get); cmds.append(['PLACE', item, carried[item]])
                else:
                    cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS'])
                continue   # inventories vanish after the final step: bank everything on the last evening
            if (pos in SHED and sum(carried.values()) >= (1 if (is_feeder and day <= 7) else 3)) or sum(carried.values()) >= 14 and pos in SHED:
                item = max(carried, key=carried.get)
                cmds.append(['PLACE', item, carried[item]]); continue
            best = None
            zone0 = zone_of.get(i)
            if (is_feeder and day <= 9 and sum(inv.get(k, 0) for k in ('WOOL', 'MILK', 'EGG')) >= 3
                    and not any(t[1] == pos and t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks)):
                if pos in SHED:
                    item = max(('WOOL', 'MILK', 'EGG'), key=lambda k: inv.get(k, 0)); cmds.append(['PLACE', item, inv[item]]); continue
                cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS']); continue   # bank the first wool/milk at once: it funds land and herd
            if (zone0 == 'ANIMALS' and inv.get('WHEAT', 0) == 0 and priv['shed'].get('WHEAT', 0) > 0
                    and any(t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks)):
                if pos in SHED:
                    qty = max(1, min(8, sum(1 for t in tasks if t[2][0] == 'FEED')))
                    cmds.append(['PICKUP', 'WHEAT', min(qty, priv['shed'].get('WHEAT', 0))])
                else:
                    cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS'])
                continue
            own_tiles = set(self.strips.get(i, ()))
            own_fert = sum(1 for t in tasks if t[2][0] == 'FERTILIZE' and t[1] in own_tiles and (t[1], 'FERTILIZE') not in taken)
            if zone0 not in (None, 'ANIMALS') and pos in SHED and inv.get('FERTILIZER', 0) > own_fert + 1 and day < 28:
                cmds.append(['PLACE', 'FERTILIZER', inv['FERTILIZER'] - own_fert - 1]); continue   # hand surplus back so the strip owners can draw it
            if (zone0 not in (None, 'ANIMALS') and inv.get('FERTILIZER', 0) < 1 and own_fert > 0 and priv['shed'].get('FERTILIZER', 0) > 0 and pos in SHED
                    and 9 <= day <= 26 and 'nostock' not in _FLAGS and not any(True for t in tasks if t[1] == pos and t[2][0] != 'FERTILIZE')):
                cmds.append(['PICKUP', 'FERTILIZER', min(own_fert, 6, priv['shed'].get('FERTILIZER', 0))]); continue
            here = [t for t in tasks if t[1] == pos and (t[1], t[2][0]) not in taken and (not t[3] or inv.get(t[3], 0) > 0)]
            if zone0 == 'ANIMALS' and any(t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks):
                feed_left = sum(1 for t in tasks if t[2][0] == 'FEED' and (t[1], 'FEED') not in taken)
                urgent_feed = hour >= 16 and feed_left > 0 and (inv.get('WHEAT', 0) > 0 or priv['shed'].get('WHEAT', 0) > 0)
                tile_here = farm['tiles'][pos[1]][pos[0]]
                ripe = isinstance(tile_here, dict) and tile_here.get('yield_units', 0) >= 4   # about to hit the cap -> collect now (1 step)
                allowed = ('FEED',) if urgent_feed else (('FEED', 'CARE') + (('HARVEST',) if ripe else ()) + (('COLLECT_FERTILIZER',) if (hour < 6 or feed_left <= n_feeders) else ()))
                if 'nofinish' in _FLAGS:
                    allowed = ('FEED', 'CARE')
                here = [t for t in here if t[2][0] in allowed]
            if here:
                pr, tile, op, need = min(here, key=lambda t: t[0])
                best = (-2, pr, tile, op, need)
            prev = self.assign.get(i)
            if (zone0 == 'ANIMALS' and hour >= 16
                    and any(t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks)
                    and (inv.get('WHEAT', 0) > 0 or priv['shed'].get('WHEAT', 0) > 0)):
                prev = None
            if zone0 == 'ANIMALS' and inv.get('WHEAT', 0) > 0 and any(t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks):
                prev = None   # feed first; a stale planting assignment must not pull a feeder away
            if prev in task_index and prev not in taken:
                pr, tile, op, need = task_index[prev]
                if not need or inv.get(need, 0) > 0 or priv['shed'].get(need, 0) > 0:
                    best = (-1, pr, tile, op, need)
            zone = zone_of.get(i)
            if best is None and zone not in (None, 'ANIMALS') and 'circuit' in _FLAGS and self.strips.get(i):
                strip = self.strips[i]; start = self.cursor.get(i, 0)
                for off in range(len(strip)):
                    tile = strip[(start + off) % len(strip)]
                    cand = [t for t in tasks if t[1] == tile and (t[1], t[2][0]) not in taken and t[2][0] != 'FEED'
                            and (not t[3] or inv.get(t[3], 0) > 0 or priv['shed'].get(t[3], 0) > 0)]
                    if cand:
                        pr, tile, op, need = min(cand, key=lambda t: t[0])
                        best = (-1, pr, tile, op, need); self.cursor[i] = (start + off) % len(strip)
                        break
            for pr, tile, op, need in (tasks if best is None else []):
                if (tile, op[0]) in taken:
                    continue
                if op[0] == 'COLLECT_FERTILIZER' and zone != 'ANIMALS' and (day <= 8 or hour < 12):
                    continue
                in_zone = (tile in animal_tiles) if zone == 'ANIMALS' else (tile not in animal_tiles and quadrant(*tile) == zone)
                if zone is not None and not in_zone and op[0] not in ('BUILD_PASTURE', 'BUILD_COOP', 'PLACE', 'DIG'):
                    continue
                if zone != 'ANIMALS' and tile in owner and owner[tile] != i and pr > 0:
                    continue
                if need and inv.get(need, 0) <= 0 and priv['shed'].get(need, 0) <= 0:
                    continue
                d = dist(pos, tile)
                if need and inv.get(need, 0) <= 0:
                    d += dist(pos, nearest_shed(pos)) + dist(nearest_shed(pos), tile) + 1
                score = pr * 6 + d
                if best is None or score < best[0]:
                    best = (score, pr, tile, op, need)
            if best is None and zone is not None:
                for pr, tile, op, need in tasks:
                    if (tile, op[0]) in taken or (op[0] == 'FEED' and zone != 'ANIMALS'):
                        continue
                    if op[0] == 'COLLECT_FERTILIZER' and zone != 'ANIMALS' and (day <= 8 or hour < 12):
                        continue
                    if need and inv.get(need, 0) <= 0 and priv['shed'].get(need, 0) <= 0:
                        continue
                    d = dist(pos, tile)
                    if need and inv.get(need, 0) <= 0:
                        d += dist(pos, nearest_shed(pos)) + dist(nearest_shed(pos), tile) + 1
                    score = pr * 6 + d
                    if best is None or score < best[0]:
                        best = (score, pr, tile, op, need)
            if best is None:
                # nothing to do: drop off goods (idle workers only) or wait; inventories auto-drop at day end
                if carried and pos in SHED:
                    item = max(carried, key=carried.get); cmds.append(['PLACE', item, carried[item]])
                elif carried and dist(pos, nearest_shed(pos)) <= 6 and (day >= 28 or carried.get('WHEAT', 0) >= 3 or (day <= 8 and carried.get('FERTILIZER', 0) >= 1)):
                    cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS'])
                else:
                    cmds.append(['PASS'])
                continue
            _, pr, tile, op, need = best
            taken.add((tile, op[0])); self.assign[i] = (tile, op[0])
            if need and inv.get(need, 0) <= 0:
                if pos in SHED:
                    if need == 'WHEAT':
                        qty = max(1, min(8, sum(1 for t in tasks if t[2][0] == 'FEED')))
                    elif need == 'FERTILIZER':
                        qty = max(1, min(6, sum(1 for t in tasks if t[2][0] == 'FERTILIZE' and (zone0 == 'ANIMALS' or t[1] in set(self.strips.get(i, ()))))))
                    else:
                        qty = 1
                    cmds.append(['PICKUP', need, min(qty, priv['shed'].get(need, 0))])
                else:
                    cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS'])
                continue
            if pos == tile:
                cmds.append(op)
            else:
                cmds.append(step_toward(pos, tile) or ['PASS'])
        farmer_cmd = cmds[0] if cmds else ['PASS']
        return {'farmer': farmer_cmd, 'hands': cmds[1:len(positions)], 'market': orders}


def agent(observation, configuration=None):
    seat = int(observation.get('player', 0)); step = int(observation.get('step', 0))
    st = _STATE.get(seat)
    if st is None or step <= st.last_step:
        st = _STATE[seat] = Proxy(seat)
    st.last_step = step
    try:
        return st.act(observation)
    except Exception:
        return {'farmer': ['PASS'], 'hands': [['PASS'] for _ in observation['farms'][seat].get('hands', [])], 'market': []}
