# p000_planner (Claude, 2026-09-17). Planner line body = base3 (c206/c207 + c2-000) with every later change behind a
# PROXY_KNOBS switch (sw_<name>=1) so o_tools/p_search.py can search structure and numbers together. All switches off = base3;
# defaults (_SW_DEFAULT_ON + knob defaults) = the current baseline (base11, 2026-09-19). Rejected switches stay available off.
# opp_planner_proxy (Claude/o-series, 2026-09-16). OPPONENT PROXY v0 — a tape-free planner that reproduces the top
# planners' macro policy (Majkel1337 stats, o_results/proxy/Majkel1337_policy.json): day-0 melon/wheat + 2 cows/3 sheep,
# strawberries d2-4 and d6, land d6/d9, world-conditional animals at d6/d9, wheat blocks d9-11, hands 4->11,
# daily water/feed/care/collect/fertilize routine with nearest-task dispatch, and small-batch buffered selling.
# Used only as a validation opponent (docs/o-planner-proxy-plan.ko.md). Not a submission candidate.
import os as _os, random, math as _math
_FLAGS = set((_os.environ.get('PROXY_FLAGS') or '').split(','))
_KNOBS = dict(kv.split('=') for kv in (_os.environ.get('PROXY_KNOBS') or '').split(',') if '=' in kv and not kv.startswith('@'))
_GATED = {}   # day -> {knob: value}: "@9:plus_cow=2" in PROXY_KNOBS applies from day 9 (o_tools/oracle.py branches)
_PROFILE = {}   # bucket -> {knob: value}: "#milk2:room_f=0.5" applies once the first three shops are known and match (world profile router)
for _kv in (_os.environ.get('PROXY_KNOBS') or '').split(','):
    if _kv.startswith('@') and ':' in _kv and '=' in _kv:
        _d, _rest = _kv[1:].split(':', 1); _k, _v = _rest.split('=', 1); _GATED.setdefault(int(_d), {})[_k] = _v
    elif _kv.startswith('#') and ':' in _kv and '=' in _kv:
        _b, _rest = _kv[1:].split(':', 1); _k, _v = _rest.split('=', 1); _PROFILE.setdefault(_b, {})[_k] = _v
_KNOBS = {k: v for k, v in _KNOBS.items() if not k.startswith('#')}
if _KNOBS.get('sw_mirror') == '1':
    # base20 candidate (09-18): o227's opening mirror - d0 h0 [BUY 13, BUY 10, SELL 30] + h1 [SELL 13, BUY 5] on the same order indices as the public
    # 'exact0' fork script ([B13, B30, S30] / [S13, B5]; 21% of live opponents, d0-end cash 0): the lockstep collisions cost it ~$15, its d1 HIRE fails
    # and it collapses (v37 96/96, +32k own); the $60 d0 reserve keeps our own d0 feed money through the round trip (else -7.6k vs o227-like scripts)
    for k_, v_ in (('sw_t0war', '1'), ('t0_q1', '13'), ('t0_q2', '10'), ('w0feed', '-7'), ('t0_s1', 'S13/B5'), ('d0_res', '60')):
        _KNOBS.setdefault(k_, v_)


def profile_bucket(shops):
    """Same buckets as o_tools/proxy_eval.bucket, but only once the first three shops are known (world profile router gate)."""
    if len(shops) < 3:
        return None
    if 'YARN_STORE' in shops[:2]:
        return 'yarn'
    return 'milk%d' % min(3, sum(sh in ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP') for sh in shops[:3]))   # sweepable knobs (o_tools/proxy_sweep.py, o_tools/p_search.py)


def _SW(name, default=0):
    """0/1 structural switch from PROXY_KNOBS (sw_<name>=1); every new behaviour defaults to the base3 behaviour."""
    return int(_KNOBS.get('sw_' + name, 1 if name in _SW_DEFAULT_ON else default)) == 1


_SW_DEFAULT_ON = {'herd_split',   # base4: p000b search winner (sel +3.7k / hold +2.0k / fresh +2.0k)
                  'shed_cap', 'horizon',   # base5 (09-18): sell the day-end shed overflow + skip tasks unreachable before midnight (sel +2.8k / hold +2.6k / fresh +3.4k)
                  'reserve',   # base6 (09-18): a task a worker is already walking to is not re-scored for others (sel +3.0k / hold +2.5k / fresh +3.2k)
                  'collect_here', 'd28_feed',   # base8 (09-18, p000c search t0126 with room_f 0.4, sheep_plus 1, straw 32, land3 8, cap 12/6, prw 8: sel +3.5k / hold +2.8k / fresh +2.0k)
                  'tomato',   # base9 (09-19): tomato hinge with >= 2 tomato shops, 8 plants/shop, hold to d26 (pooled 96 games +1.6k, 6 worse/55 better; 3 shops +3.6k)
                  'vrp', 'egg', 'carrot2', 'herd_block', 'hire_first', 'feed_stock', 'bank_pm', 'melon_water', 'melon_bank',   # base10 (09-19, p000f t0067 minus yarn2: VRP dispatcher + capacity knobs straw 40, buf 4, wheat_units 4, land3 7, cap 9/6, prw 6, melon pr age 9 / hour 12; fert_batch off): sel +4.0k / hold +2.3k / fresh +3.1k vs base9
                  'opp_supply',   # base11 (09-19): herd/strawberry caps net of the rival's measured supply (sel +1.6k / hold +1.9k / fresh +1.5k / blind 7064-79 +2.3k; margin vs o227 ~0)
                  'melon_rush',   # base12 (09-17 재개): d10 melon dawn rush (water->harvest pr -1, one tile per worker, straight to the shed, same-step sale) + vrp_pr 4 / vrp_w 2.0
                                  #   sel +1.8k / hold +2.2k / fresh +1.8k / blind 7080-95 +1.5k, 3/128 worse; margin vs o227 +4.3~4.8k (the tapes' h9 dump now sells into our 36 units)
                  'carrot_hold', 'yarn2',   # base13 (09-17 17:50, bundle): seed_last 26 (wheat seeds through d26) + carrot hinge hold (>=18 carrots/day of shop demand) + yarn2 with 3 yarn stores
                  'car_wf',   # base18 (09-18 09:47, execution throughput from the leader gap decomposition): carrots harvested after the age-3 watering (2.0 -> 2.8 units/harvest;
                              #   Majkel 2.6): own +0.8/+1.5/+1.5k, margin +0.8/+1.7/+1.9k (pooled +1.46k, 8 se, 7/96 worse), wins +6/96; blind 7208-7223 margin +2.2k / own +1.9k, 1/32 worse
                  'vrp_h23'}  # base19 (09-18 09:58): the VRP time budget counted 23-hour steps, so the whole crew idled at h23 (292/299 unit-actions PASS) and every h22 planting
                              #   died unwatered (12.5 wheat + 3 carrots + 0.9 melons + 0.7 strawberries per game); now 24-hour steps and no planting at h23.
                              #   own +2.0/+2.4/+2.0k, margin +2.6/+2.8/+1.9k (pooled +2.46k, 11 se, 9/96 worse), wins +8/96; blind 7224-7239 margin +2.1k / own +2.2k, 4/32 worse, wins 8->11
                                  #   sel +1.19k / hold +0.95k / fresh +1.01k (pooled +1.05k, se .17, 3/96 worse) / blind 7096-7111 +1.59k, 0/32 worse; margin ~ +1.0k
                                  # base14 (09-17 18:45, first margin-first promotion): land3 8 (3rd quadrant a day later, the cash goes to animals/strawberries first)
                                  #   + wheat_units 3 (harvest wheat at 3 units): own +0.05/-0.2/-0.1k, margin vs o227 +2.0/+1.9/+2.5k (pooled +2.1k, 10 se, 8/96 worse),
                                  #   blind 7112-7127 margin +3.3k / own +1.2k; vs V46 margin +1.7k. The p000j margin search converged here (its extra glut knobs add margin but not wins).
                                  # base15 (09-17 19:20, margin-first): no wheat fertilizer dose on d9-19 (early fertilizer sells for $60-90 and every unit
                                  #   shrinks the rival's first-come pie; the d2-8 doses stay - touching them cascades from the knife-edge d2 cash) + sell buffer 1
                                  #   for milk/wool: margin +1.07/+1.26/+1.74k (pooled +1.36k, 9.8 se, 10/96 worse), own -0.07k, blind 7128-7143 margin +1.95k / own +0.2k, vs V46 +1.3k
                                  # base16 (09-18 00:30, opening bundle search open1, margin-first): d0 = 2 cows, 3 sheep, 3 feed wheat, 7 melons (melons0 8, reserve 5)
                                  #   + 6 wheat seeds, 3rd quadrant from d9: margin +1.54/+1.55/+1.60k (pooled +1.56k, 8 se, 9/96 worse), blind 7176-7191 +2.50k (2 worse),
                                  #   own -0.5/-0.6/-1.2/-1.1k (the 7th rush melon is bought with the d0 feed/seed money); single opening deviations were all ~0
                                  # base17 (09-18 04:50, oracle-derived conditional rule): strawberry cap +8 while the known shops have a berry shop and no pizza/yarn
                                  #   shop and at most one smoothie shop (sc_*): margin +0.70/+1.33/+1.29k (pooled +1.11k, 4.5 se, 7/96 worse, 54 games untouched),
                                  #   blind 7192-7207 +1.18k (2 worse), own ~0, wins +5/96


MOVES = {'NORTH': (0, -1), 'SOUTH': (0, 1), 'EAST': (1, 0), 'WEST': (-1, 0)}
MILK_SHOPS = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
EGG_SHOPS = ('BAKERY', 'BRUNCH_SPOT')
SHED = [(4, 4), (5, 4), (4, 5), (5, 5)]
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
SHOP_PRODUCTS = {
    'BAKERY': ('EGG', 'WHEAT'), 'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'),
    'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'), 'YARN_STORE': ('WOOL',),
    'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'), 'PET_CAFE': ('CARROT',),
    'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'), 'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY'),
}
SMALL_FLOOR_X = {'MILK': 76, 'WOOL': 59, 'STRAWBERRY': 62, 'MELON': 158}
BASE_PRICE = {'WHEAT': 25, 'CARROT': 35, 'TOMATO': 60, 'STRAWBERRY': 120, 'MELON': 250, 'EGG': 50, 'MILK': 160, 'WOOL': 200, 'FERTILIZER': 100}
ANIMAL_PRODUCT = {'COW': 'MILK', 'SHEEP': 'WOOL', 'GOOSE': 'EGG'}
CROP_FIRST = {'WHEAT': 2, 'CARROT': 2, 'TOMATO': 8, 'STRAWBERRY': 10, 'MELON': 10}
CROP_LAST = {'WHEAT': 4, 'CARROT': 3, 'MELON': 12}
ONGOING = {'TOMATO': 1, 'STRAWBERRY': 2}
ANIMAL_STRUCT = {'COW': 'PASTURE', 'SHEEP': 'PASTURE', 'GOOSE': 'COOP'}
ANIMAL_FIRST = {'GOOSE': 4, 'COW': 8, 'SHEEP': 6}; ANIMAL_INT = {'GOOSE': 1, 'COW': 2, 'SHEEP': 3}
BUFFER = {'MILK': int(_KNOBS.get('buf', 1)), 'WOOL': int(_KNOBS.get('buf', 1)), 'STRAWBERRY': 2, 'MELON': 0, 'EGG': 0, 'CARROT': 0, 'TOMATO': 0, 'FERTILIZER': 1, 'WHEAT': 0}
BATCH = {'MILK': 3, 'WOOL': 3, 'STRAWBERRY': 4, 'MELON': 12, 'EGG': 6, 'CARROT': 9, 'TOMATO': 5, 'FERTILIZER': 3, 'WHEAT': 7}
HANDS_BY_DAY = [4, 4, 6, 6, 6, 6, 8, 9, 9, 10, 11, 11] + [11] * 18
_STATE = {}


def quadrant(x, y):
    return ('N' if y < 5 else 'S') + ('W' if x < 5 else 'E')


def world_bucket(shops):
    if 'YARN_STORE' in shops[:2]:
        return 'yarn'
    return 'milk%d' % min(3, sum(s in MILK_SHOPS for s in shops[:3]))


def _ticks_left(step, interval):
    first = step + (-step % interval)
    return 0 if first > 718 else (718 - first) // interval + 1


_MP = {'WHEAT': (25, 400, 'sqrt', 0.8, 'log', 0.2), 'CARROT': (35, 450, 'hinge', 1.0, 'sqrt', 0.7), 'TOMATO': (60, 200, 'hinge', 0.4, 'sqrt', 0.6),
       'STRAWBERRY': (120, 100, 'sqrt', 0.7, 'linear', 1.6), 'MELON': (250, 300, 'log', 0.2, 'sq', 3.6), 'EGG': (50, 332, 'hinge', 0.4, 'log', 0.2),
       'MILK': (160, 122, 'sqrt', 0.6, 'linear', 1.6), 'WOOL': (200, 105, 'log', 0.2, 'sq', 3.2), 'FERTILIZER': (100, 200, 'linear', 0.4, 'linear', 0.4)}   # engine MARKET_PARAMS


def _shape(f, x, T):
    x = max(0.0, x)
    if f == 'linear': return x
    if f == 'sq': return x * x
    if f == 'sqrt': return _math.sqrt(x)
    if f == 'log': return _math.log(1.0 + x)
    if f == 'hinge':
        u = x / T; return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def price_at(item, inventory):
    """Engine market price for a hypothetical inventory (exact formula, floor 1)."""
    base, T, bf, bt, af, at = _MP[item]
    if inventory < 10000:
        return max(1, int(round(base + bt * base / _shape(bf, T, T) * _shape(bf, 10000 - inventory, T))))
    return max(1, int(round(base - at * base / _shape(af, T, T) * _shape(af, inventory - 10000, T))))


def market_room(obs, item):
    """Units the currently visible market can absorb before this small market reaches $1."""
    floor_x = SMALL_FLOOR_X[item]
    x = obs['market']['inventory'].get(item, 10000) - 10000
    step = int(obs['step'])
    per_shop_tick = 0
    for shop in obs['town'].get('unlocked_shops', []) or []:
        products = SHOP_PRODUCTS.get(shop, ())
        if item in products:
            per_shop_tick += 2 if len(products) == 1 else 1
    absorb = per_shop_tick * _ticks_left(step, 4)
    if item != 'FERTILIZER':
        absorb += _ticks_left(step, 24)
    if _SW('opp_supply'):
        rate = _OPP_RATE.get(int(obs.get('player', 0)), {}).get(item, 0.0)   # the rival's units/day into this market (sw_opp_supply)
        absorb -= int(max(0.0, rate) * (720 - step) / 24.0 * float(_KNOBS.get('opp_f', 1.0)))
    return max(0, floor_x - x + absorb)


_OPP_RATE = {}   # seat -> {item: rival supply units/day}, maintained by Proxy.track_market
_MX2_HELD = {}   # seat -> {item: units the market executor holds this hour on purpose}: the herd/strawberry room caps must not read them as unsold glut
_TEL = {}   # p002 telemetry (flat counters + p002_log by day); exported as agent.telemetry so the canonical runner records it per game


def feedrot_n(animals, day):
    """sw_feedrot (p003): wheat tiles to keep in rotation for feed while day <= fr_last - ceil(animals / fr_yield) clamped to fr_min..fr_max.
    Own state only (placed + unplaced animals). 0 when the switch is off or past the window."""
    if not _SW('feedrot') or day < int(_KNOBS.get('fr_d0', 3)) or day > int(_KNOBS.get('fr_last', 11)):
        return 0   # fr_d0 3: the d0-d2 opening (melon top-up to 12 on Q1) is untouched; the d0 wheat is harvested on d2 and the rotation starts on d3
    return int(min(int(_KNOBS.get('fr_max', 8)), max(int(_KNOBS.get('fr_min', 4)), _math.ceil(animals / float(_KNOBS.get('fr_yield', 1.2))))))


ANIMAL_TOTALS = {'yarn': {'SHEEP': 12, 'COW': 6}, 'milk0': {'GOOSE': 4, 'COW': 6, 'SHEEP': 5}, 'milk1': {'GOOSE': 2, 'COW': 8, 'SHEEP': 4},
                 'milk2': {'GOOSE': 1, 'COW': 10, 'SHEEP': 4}, 'milk3': {'COW': 13, 'SHEEP': 3}}   # dict order = purchase order (geese pay back in days)


def animal_plan(bucket, day, have, obs=None):
    """Shortfall to Majkel's peak herd by world, bought from day 6 as cash allows (order: the world's main product first)."""
    if day < 6 or day > 18 or day >= int(_KNOBS.get('herd_stop', 99)):
        return {}   # herd shortfall is still worth closing until d18 (a d15 cow/sheep repays 2x before d30); herd_stop: oracle branch (no more animals from this day)
    tot = dict(ANIMAL_TOTALS.get(bucket, ANIMAL_TOTALS['milk1']))
    tot['SHEEP'] = tot.get('SHEEP', 0) + int(_KNOBS.get('sheep_plus', 1))   # o227 keeps 5-6 sheep in every world (wool ~150 units/game)
    if obs is not None:
        # world-adaptive portfolio (09-19): size the herd by the shops actually unlocked, not only by the first three
        shops = obs['town'].get('unlocked_shops', []) or []
        if _SW('egg'):
            n_egg = sum(sh in EGG_SHOPS for sh in shops)   # BAKERY/BRUNCH eat 6 eggs/day each; a goose lays 2/day fed+cared for $300
            if n_egg >= 1 or int(_KNOBS.get('egg0', 0)) > 0:
                tot['GOOSE'] = max(tot.get('GOOSE', 0), int(_KNOBS.get('egg%d' % min(3, n_egg), {0: 0, 1: 2, 2: 4, 3: 6}[min(3, n_egg)])))   # egg0: geese without an egg shop (log-priced eggs + 1 fertilizer/day)
                if 'GOOSE' in tot:
                    tot = dict([('GOOSE', tot['GOOSE'])] + [(k, v) for k, v in tot.items() if k != 'GOOSE'])   # geese first: they pay back in days
        if _SW('yarn2') and sum(sh == 'YARN_STORE' for sh in shops) >= int(_KNOBS.get('yarn2_min', 3)):
            tot['SHEEP'] = tot.get('SHEEP', 0) + int(_KNOBS.get('yarn2_plus', 6))   # 3 yarn stores = 36 wool/day: 18+ sheep fit (7008: +15k own, +2 wins); with 2 stores the rival's 380 wool already saturates it (7030: -13k)
    if obs is not None:
        # Keep herd/feed/labour at or below the baseline; freed tiles fall through to wheat.
        for kind in ('COW', 'SHEEP'):
            item = ANIMAL_PRODUCT[kind]
            stock = obs['private']['shed'].get(item, 0) + sum((inv or {}).get(item, 0) for inv in (obs['private'].get('inventories') or [])) - _MX2_HELD.get(int(obs.get('player', 0)), {}).get(item, 0)
            rf = float(_KNOBS.get('room_f', 0.4))
            if float(_KNOBS.get('rf_deep', 0)) > 0 and sum(sh in MILK_SHOPS for sh in shops) >= int(_KNOBS.get('rf_deep_n', 2)):
                rf = float(_KNOBS.get('rf_deep', 0))   # deep milk market (2+ milk shops known): larger herd share
            room = max(0, int(rf * market_room(obs, item)) - stock)
            units_per_new = max(6, 30 - day - ANIMAL_FIRST[kind])
            cap = max(have.get(kind, 0), room // units_per_new)
            old = tot.get(kind, 0)
            tot[kind] = min(old, cap)
        hm = int(_KNOBS.get('herd_min', 0))   # herd_min: a floor on cows+sheep whatever the product markets say (every animal is also 1 fertilizer/day = $55-90 early, out of the rival's first-come pie)
        if hm and tot.get('COW', 0) + tot.get('SHEEP', 0) < hm:
            tot['COW'] = hm - tot.get('SHEEP', 0)
        if int(_KNOBS.get('late_cows', 0)) and day >= int(_KNOBS.get('late_d', 13)):
            tot['COW'] = tot.get('COW', 0) + int(_KNOBS.get('late_cows', 0))   # late_cows: extra cows once cash is abundant (fertilizer + 4 milk productions on a wheat tile's opportunity cost)
        for k_, kind_ in (('plus_cow', 'COW'), ('plus_sheep', 'SHEEP'), ('plus_goose', 'GOOSE')):
            if int(_KNOBS.get(k_, 0)):
                tot[kind_] = tot.get(kind_, 0) + int(_KNOBS.get(k_, 0))   # oracle branch: +N animals of this kind beyond the plan (day-gated via @D:)
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
        self.am_sold = {}
        self.seat = seat; self.last_step = -1; self.day_plan = {}; self.claims = {}; self.pending_sell = {}
        self.bought = {}; self.assign = {}; self.assign_day = -1; self.zone_of = {}; self.zone_key = None; self.owner = {}; self.strips = {}; self.cursor = {}; self.fert_demand = 0; self.reserved = set(); self.last_sells = {}; self.opp_day = {}; self.opp_hist = {}; self.opp_hour = {}; self.mx2_est = {}; self.empty_since = {}
        self.cow1_done = False; self.cow1_log = {}; self.tel = _TEL
        if _SW('cow1'):
            _TEL.clear(); _TEL['p002_log'] = self.cow1_log   # p002: fresh telemetry per game (one seat per process in the canonical runner)

    # ---------------- daily macro ----------------
    def free_tiles(self, farm, prefer=None):
        out = []
        for y, row in enumerate(farm['tiles']):
            for x, t in enumerate(row):
                if t is None and (x, y) not in self.reserved:
                    out.append((x, y))
        if prefer:
            out.sort(key=lambda p: (quadrant(*p) != prefer, dist(p, (4, 4))))
        else:
            out.sort(key=lambda p: dist(p, (4, 4)))
        return out

    def herd_reserve(self, obs, farm, day, bucket):
        """sw_herd_block: keep a few free tiles next to the herd out of the crop rotation while animals are still being
        bought (knob herd_hold, default 2), so a new cow/sheep never lands in a far corner (feeder walking, escapes)."""
        if not _SW('herd_block') or day > 18:
            return set()
        shed = obs['private']['shed']; invs = obs['private'].get('inventories', []) or []
        have = {}; unplaced = 0; empties = 0; anchors = []
        for y, row in enumerate(farm['tiles']):
            for x, t in enumerate(row):
                if isinstance(t, dict) and t.get('animal'):
                    have[t['animal']] = have.get(t['animal'], 0) + 1; anchors.append((x, y))
                elif isinstance(t, dict) and t.get('kind') in ('PASTURE', 'COOP'):
                    empties += 1; anchors.append((x, y))
        for k in ANIMAL_STRUCT:
            n = shed.get(k, 0) + sum((inv or {}).get(k, 0) for inv in invs)
            have[k] = have.get(k, 0) + n; unplaced += n
        if _SW('cow1') and self.cow1_done:
            have['COW'] = max(0, have.get('COW', 0) - 1)   # p002: see market_orders
        if day >= 6:
            future = min(sum(animal_plan(bucket, day, have, obs).values()), int(_KNOBS.get('herd_hold', 2)))
        else:
            future = max(0, 5 - sum(have.values()))
        need = max(0, unplaced - empties) + future
        if need <= 0:
            return set()
        anchors = anchors or [(4, 4)]
        free = [(x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row) if t is None]
        free.sort(key=lambda q: (min(dist(q, a) for a in anchors), dist(q, (4, 4)), q[1], q[0]))
        if _SW('melon_rush') and day <= 1 and int(_KNOBS.get('rush_ring', 0)) > 0:
            ring = int(_KNOBS.get('rush_ring', 0))   # 0 = herd placement unchanged (a d0 herd behind the ring delayed the d6 wool by a day: -1.3k)
            free.sort(key=lambda q: (dist(q, (4, 4)) < ring, dist(q, (4, 4 - ring)), dist(q, (4, 4)), q[1], q[0]))   # d0 herd as a block north of the melon ring: the d10 rush must reach the shed before the tapes' h9 dump
        if _SW('melon_rush') and day <= 1 and int(_KNOBS.get('rush_44', 0)):
            free = [q for q in free if q != (4, 4)]   # rush_44: the farmer's spawn tile grows a melon (h0 water, h1 harvest, h2 sale), the 5th d0 animal goes one tile further
        if False:
            pass
        elif _SW('melon_rush') and day <= 1 and int(_KNOBS.get('rush_arm', 0)):
            arm = lambda q: q[0] == 4 or (q[0] == 3 and q[1] <= 2)   # d0 herd on the north arm (x=4 column + (3,<=2)) so (4,4),(3,4),(3,3),(2,4) stay free for melons
            free.sort(key=lambda q: (not arm(q), dist(q, (4, 4)), q[1], q[0]))
        return set(free[:need])

    def rush_today(self, farm, day):
        """sw_melon_rush: day 10 (the d0 melons), or with rush_all any day on which a melon tile reaches its first harvest."""
        if not _SW('melon_rush'):
            return False
        if day == int(_KNOBS.get('melon_day', 10)):
            return True
        if not int(_KNOBS.get('rush_all', 0)):
            return False
        return any(isinstance(t, dict) and t.get('crop') == 'MELON' and day - t['planted_day'] == CROP_FIRST['MELON'] for row in farm['tiles'] for t in row)

    def ec2_targets(self, obs, farm, day, hour):
        """Economic controller v2 (crops only): allocates the crop-tile budget (unlocked tiles minus the herd and the carrot rotation)
        between strawberry, tomato and the wheat filler by projected MARGINAL REVENUE per tile-day: the strawberry value of one more
        tile is the change of our total projected berry revenue (own cohort schedule sold unit by unit down the exact price curve,
        rival supply prior from d16, town consumption), so the price impact on the inframarginal units is charged; the tomato value is
        the hinge price of the residual deficit at the sell day. Targets are recomputed every ec2_every hours; every call returns the
        seeds worth buying now (target minus tiles and seeds in hand, bounded by tiles that free within a day). Livestock untouched."""
        inv = obs['market']['inventory']; prices = obs['market']['prices']; shops = obs['town'].get('unlocked_shops', []) or []
        opp = _OPP_RATE.get(int(obs.get('player', 0)), {}); seeds = obs['private']['seeds']
        crops = [t for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop')]
        S = [t for t in crops if t['crop'] == 'STRAWBERRY']; T = [t for t in crops if t['crop'] == 'TOMATO']
        free = len(self.free_tiles(farm)); sS = int(seeds.get('STRAWBERRY', 0)); sT = int(seeds.get('TOMATO', 0))
        pS = sum(1 for t in S if int(t.get('planted_day', -1)) >= day); pT = sum(1 for t in T if int(t.get('planted_day', -1)) >= day)
        cache = getattr(self, 'ec2_cache', None)
        if cache is None or cache[0] != day or hour - cache[1] >= int(_KNOBS.get('ec2_every', 6)):
            def cons(item):   # units/day the town removes (single-product shop 12, multi 6, town centre 1)
                return sum((12 if len(SHOP_PRODUCTS.get(sh, ())) == 1 else 6) for sh in shops if item in SHOP_PRODUCTS.get(sh, ())) + 1
            cap = free + len(crops)
            lam = float(_KNOBS.get('ec2_lam', 6.0)) if getattr(self, 'idle_yday', 40) < int(_KNOBS.get('ec2_idle', 15)) else 0.0   # $/worker-step when the crew was busy yesterday
            su = float(_KNOBS.get('ec2_su', 1.8)); tu = float(_KNOBS.get('ec2_tu', 7.3)); prior_f = float(_KNOBS.get('ec2_prior', 0.75))
            cs, ct, cw = cons('STRAWBERRY'), cons('TOMATO'), cons('WHEAT')
            rs_obs = max(opp.get('STRAWBERRY', 0.0), 0.0); rs = max(rs_obs, prior_f * (cs - 1)); rt = max(opp.get('TOMATO', 0.0), 0.0); rw = max(opp.get('WHEAT', 0.0), 0.0)
            rs_d0 = int(_KNOBS.get('ec2_rs_d0', 16))   # the rival's first strawberry cohort lands ~d16: before that only what is measured, after it at least the prior
            wheat_day = (4 * price_at('WHEAT', inv.get('WHEAT', 10000) + (rw - cw + 2.0) * 4) - 10 - lam * 6) / 5.0   # filler value per tile-day = the floor
            own = [0.0] * 50   # our sellable strawberry units per day from the cohorts on the farm (+ seeds in hand, planted today)

            def add_straw(p, sign=1):
                for j in range(4):
                    own[p + 10 + 2 * j] += sign * su
            for t in S:
                add_straw(int(t.get('planted_day', day)))
            for _ in range(sS):
                add_straw(day)
            inv_s = inv.get('STRAWBERRY', 10000)

            w_riv = float(_KNOBS.get('ec2_riv', 1.0))   # weight of the rival's revenue in the value (1 = paired margin, 0 = own cash)

            def rev_path(d0, I):   # projected margin value of the berry market from day d0: our batches sold down the curve (Simpson) minus w_riv x the rival's units at the price after our batch
                R = 0.0
                for dd in range(d0, 30):
                    q = own[dd]; r = rs if dd >= rs_d0 else rs_obs
                    if q > 0:
                        R += q / 6.0 * (price_at('STRAWBERRY', I) + 4 * price_at('STRAWBERRY', I + q / 2) + price_at('STRAWBERRY', I + q))
                    if r > 0 and w_riv:
                        R -= w_riv * r * price_at('STRAWBERRY', I + q)
                    I += q + r - cs
                return R
            first = min(29, day + 10); I0 = inv_s
            for dd in range(day, first):
                I0 += own[dd] + (rs if dd >= rs_d0 else rs_obs) - cs   # unchanged by a tile planted today
            R0 = rev_path(first, I0)

            def straw_value():   # marginal revenue of one more tile planted today minus seed, two fertilizer doses and labour
                if day + 12 > 29:
                    return -1e9, 1
                add_straw(day); R1 = rev_path(first, I0); add_straw(day, -1)
                return R1 - R0 - 100 - 2 * min(60, max(20, prices.get('FERTILIZER', 50))) - lam * 16, min(29, day + 17) - day
            sell_d = int(_KNOBS.get('tom_sell', 26)); D = (10000 - inv.get('TOMATO', 10000)) + (ct - rt) * max(0, sell_d - day)
            tom_dem = sum(sh in ('PIZZA_SHOP', 'FARMERS_MARKET') for sh in shops)
            sold = tu * (len(T) + sT)

            riv_tom = (70 if tom_dem >= 3 else (45 if tom_dem == 2 else 0)) * w_riv   # the tape's tomato tranche (v219 10 seeds at 3+ shops, c177 8 at 2) sells into the same dump

            def tom_value():   # one more tomato tile: its units sell last in the sell-day dump at the residual hinge deficit; the rival's units sell after ours
                v = -50 - lam * 12
                for u in range(int(tu)):
                    v += price_at('TOMATO', 10000 - (D - sold - u))
                v += riv_tom * (price_at('TOMATO', 10000 - (D - sold)) - price_at('TOMATO', 10000 - (D - sold - tu)))
                return v, max(1, min(29, day + 12) - day)
            tom_ok = tom_dem >= int(_KNOBS.get('tom_min', 2)) and day <= int(_KNOBS.get('tom_d1', 18))
            straw_ok = 6 <= day <= int(_KNOBS.get('ec2_straw_last', 20))
            pets = sum(sh == 'PET_CAFE' for sh in shops); cdem = sum(sh in ('PET_CAFE', 'FARMERS_MARKET') for sh in shops)
            rot = (8 + int(_KNOBS.get('car_pet', 6)) * pets + int(_KNOBS.get('car_fm2', 0)) * (cdem - pets) + int(_KNOBS.get('car_plus', 0))) if (cdem and day <= 26) else 0
            budget = cap - rot - len(S) - len(T) - sS - sT   # crop tiles minus the carrot rotation the existing rule claims, minus what is committed
            n_s = n_t = 0; last = [0.0, 0.0]
            while budget > 0:
                best = None
                if straw_ok:
                    v, occ = straw_value(); best = ('S', v / occ)
                if tom_ok:
                    v, occ = tom_value(); r = v / occ
                    if best is None or r > best[1]:
                        best = ('T', r)
                if best is None or best[1] <= wheat_day:
                    break
                if best[0] == 'S':
                    n_s += 1; add_straw(day); R0 = rev_path(first, I0); last[0] = best[1]
                else:
                    n_t += 1; sold += tu; last[1] = best[1]
                budget -= 1
            self.ec2_cache = (day, hour, pS + sS + n_s, pT + sT + n_t)   # today's planting target: tiles planted today + seeds in hand + allocation (deaths of old plants do not refill it)
            if _os.environ.get('EC2_DEBUG'):
                print(f"EC2 d{day} h{hour} S={len(S)}+{sS} T={len(T)}+{sT} cap={cap} free={free} rot={rot} budget_left={budget} wheat/day={wheat_day:.1f} new_S={n_s} new_T={n_t} last_r={last[0]:.0f}/{last[1]:.0f} lam={lam} cs={cs} rs={rs_obs:.1f}/{rs:.1f} ct={ct} D={D:.0f} inv_s={inv_s} p_s={prices.get('STRAWBERRY')} p_w={prices.get('WHEAT')} idle={getattr(self, 'idle_yday', None)}", flush=True)
        _, _, tgt_s, tgt_t = self.ec2_cache
        soon = free + sum(1 for t in crops if t['crop'] in ('WHEAT', 'CARROT') and day - int(t.get('planted_day', day)) >= 3) - sS - sT
        n_s = max(0, min(tgt_s - pS - sS, soon)); n_t = max(0, min(tgt_t - pT - sT, soon - n_s))   # seeds beyond the tiles that free within a day only tie up cash
        return n_s, n_t

    def mx2_sell(self, obs, item, avail, day, hour, cap_left):
        """sw_mx2 (p001 market executor v2): units of `item` to sell this hour. The town eats a fixed amount right after every 4th
        market (hours 0/4/8/.. -> the markets at 1/5/9/13/17/21 open with fresh headroom) while the rival's units push the price back;
        the rival's hour-of-day profile (opp_hour EMA over days) gives the expected inventory at every remaining sale hour of the day,
        the stock is water-filled over the remaining sale hours (each unit to the hour with the lowest expected inventory including the
        units already planned there), and whatever the plan puts on the current hour is sold now. Capacity risk or the last slot (h21) liquidates; nothing is carried into tomorrow
        on purpose (cross-day holds lose against dumpers)."""
        K = _KNOBS.get
        if avail <= 0:
            return 0
        if hour >= 21 or self.rush_today(obs['farms'][self.seat], day):
            return avail   # last slot of the day, or the melon rush day (the shed must take 72 melons at dawn)
        farm_ = obs['farms'][self.seat]
        if day <= int(K('mx2_cash_d', 18)) and farm_['money'] < int(K('mx2_cash', 0)):
            return avail   # the herd/land programme still needs today's cash: never delay it for a few dollars of price
        must = max(0, int(K('mx2_capm', 8)) - cap_left)   # keep shed room for the feed purchases and the workers' deposits (a full shed refuses BUY_PRODUCT and PLACE)
        inv_now = obs['market']['inventory'].get(item, 10000); shops = obs['town'].get('unlocked_shops', []) or []
        c = sum((2 if len(SHOP_PRODUCTS.get(sh, ())) == 1 else 1) for sh in shops if item in SHOP_PRODUCTS.get(sh, ()))
        if _SW('mx2c0') and c == 0:
            # p004: no shop consumes this item (e.g. wool without a yarn store) -> the market does not recover between MX2's slots, so spreading
            # is pure delay: our units still sell at the same depressed curve while the rival (who dumps) sells first into the higher quotes
            # (arena world 44142014: base19's h1 wool dump left V46's 22 units at $3; MX2's spread gave V46 $79/u, W->L). Sell all now.
            self.tel['mx2c0_dumps'] = self.tel.get('mx2c0_dumps', 0) + 1; self.tel['mx2c0_units'] = self.tel.get('mx2c0_units', 0) + int(avail)
            return avail
        if hour <= 1 or item not in self.mx2_est:
            self.mx2_est[item] = max(self.mx2_est.get(item, 0.0) * 0.5, float(avail))   # our own morning stock = yesterday's production: the rival is assumed at least as productive
        prior = max(_OPP_RATE.get(self.seat, {}).get(item, 0.0), float(K('mx2_sym', 1.0)) * self.mx2_est[item], 24 * float(K('mx2_prior_min', 0.1))) / 24.0   # rival units/hour
        am, pm, blend = float(K('mx2_am', 0.5)), float(K('mx2_pm', 1.5)), float(K('mx2_blend', 0.3))   # back-loaded prior: rivals sell what they harvested during the day in the afternoon; ours comes from the day-end drop
        slots = [h for h in (1, 5, 9, 13, 17, 21) if hour < h <= int(K('mx2_last', 21))]   # mx2_last: latest planned sale hour (the h21 slot still liquidates)
        cands = [hour] + slots

        def riv_at(u):
            pr = prior * (am if u < 12 else pm)
            return pr if (item, u) not in self.opp_hour else (1 - blend) * self.opp_hour[(item, u)] + blend * pr

        w_r = float(K('mx2_w', 1.0)); sw_ = float(K('mx2_same', 0.5))   # mx2_w 2 = paired-margin weight (a rival unit ahead of ours costs us m and spares them m); mx2_same: same-hour rival units interleave

        def exp_inv(h2):   # expected market inventory when the market of hour h2 opens (before our own units), rival units weighted
            riv = sum(riv_at(u) for u in range(hour, h2)) + sw_ * riv_at(h2)
            ticks = sum(1 for u in range(hour, h2) if u % 4 == 0) + (int(K('mx2_tc', 1)) if hour == 0 and h2 > 0 else 0)   # the h0 tick also takes the town-centre unit
            return inv_now + w_r * riv - c * ticks
        base_inv = {h2: exp_inv(h2) for h2 in cands}; plan = {h2: 0 for h2 in cands}
        for _ in range(int(avail)):   # water-filling: every unit goes to the hour with the lowest expected inventory once the units already planned there are counted
            h2 = min(cands, key=lambda h_: (base_inv[h_] + plan[h_], h_))
            plan[h2] += 1
        plan[hour] = min(avail, max(plan[hour], must))
        _MX2_HELD.setdefault(self.seat, {})[item] = (avail - plan[hour]) if int(K('mx2_decouple', 0)) else 0
        if _os.environ.get('MX2_DEBUG') and day == int(_os.environ.get('MX2_DEBUG')) and item == _os.environ.get('MX2_ITEM', 'STRAWBERRY'):
            print(f"MX2 d{day} h{hour:2d} {item} avail={avail} inv={inv_now} c={c} prior={prior:.2f} prof={[round(self.opp_hour.get((item, u), -1), 1) for u in range(24)]} exp={[(h_, round(base_inv[h_])) for h_ in cands]} plan={ {h_: n for h_, n in plan.items() if n} }", flush=True)
        return plan[hour]

    def market_orders(self, obs, farm, day, hour, bucket):
        """Cash-flow driven just-in-time buying (Majkel style): sales first, then the day's priority list, buying
        as many units as the current money allows; unfilled targets are retried every hour."""
        orders = []
        money = farm['money']; shed = obs['private']['shed']; seeds = obs['private']['seeds']; prices = obs['market']['prices']
        if _SW('t0war') and day == 0 and hour == 0:
            # turn-0 wheat round trip in the public forks' own pattern (buy 13, buy 10, sell 30): a round trip nets ~0 against anyone else, but the
            # forks run a budget-exact "buy 43 / sell 30" gambit and our interleaved units cost them ~$45 -> their d0 plan derails (no hands on d1,
            # cows starve by d2): o227 +53k / 32 of 32 vs public v37 where the planner had +2k. The kept units replace the d0 feed purchase.
            keep = int(_KNOBS.get('w0feed', 3)); q1 = int(_KNOBS.get('t0_q1', 13)); q2 = int(_KNOBS.get('t0_q2', 10))
            orders += [['BUY_PRODUCT', 'WHEAT', q] for q in (q1, q2) if q > 0] + ([['SELL', 'WHEAT', q1 + q2 - keep]] if q1 + q2 - keep > 0 else [])
        if _SW('t0war') and day == 0 and hour == 1 and _KNOBS.get('t0_s1'):
            for tok in _KNOBS.get('t0_s1').split('/'):   # t0_s1: step-1 part of the tape's opening stream, e.g. S13/B5 = SELL 13 then BUY 5
                orders.append(['SELL' if tok[0] == 'S' else 'BUY_PRODUCT', 'WHEAT', int(tok[1:])])
        placed = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal'))
        invs = obs['private'].get('inventories', []) or []
        unplaced = sum(shed.get(k, 0) for k in ANIMAL_STRUCT) + sum((inv or {}).get(k, 0) for inv in invs for k in ANIMAL_STRUCT)
        animals = placed + unplaced
        inv_wheat = sum((inv or {}).get('WHEAT', 0) for inv in invs)
        free = len(self.free_tiles(farm))
        ahead = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') in ('WHEAT', 'CARROT') and day - t.get('planted_day', day) >= CROP_LAST[t['crop']]) if ((_SW('seed_ahead') or (_SW('fmode') and int(_KNOBS.get('fm_replant', 1)))) and hour < 22) else 0   # seed_ahead: tiles harvested today get their seed bought now (same-hour replant; Majkel 100% same-day vs our 87%)
        terminal = day >= int(_KNOBS.get('term_d', 28))   # term_d: first day of the sell-everything endgame
        # --- sales (generate cash first) ---
        if _SW('fert_h0') and (hour <= 1 or (_SW('fert_h23') and hour >= 22)) and 6 <= day <= 27 and shed.get('FERTILIZER', 0) > self.fert_demand + 2:   # fert_h23: the evening surplus sells before the tape's h0 dump (first-come market)
            orders.append(['SELL', 'FERTILIZER', min(40, shed.get('FERTILIZER', 0) - self.fert_demand - 2)])   # surplus never sat in planter pockets again
        rush_day = self.rush_today(farm, day) and hour < 16
        for item in PRODUCTS:
            stock = shed.get(item, 0)
            if item == 'MELON' and rush_day:
                units = [tuple(farm['farmer'])] + [tuple(h) for h in farm['hands']]
                stock += sum((inv or {}).get('MELON', 0) for pos, inv in zip(units, invs) if pos in SHED)   # placed this step, sold this step (actions run before the market)
            if item == 'WHEAT':
                early_dump = ('wsell' in _FLAGS or _SW('wsell')) and day <= int(_KNOBS.get('wsell_d', 5))   # sell the d0 wheat crop above the feed need: early cash compounds (Majkel funds a 7-animal d6 with it)
                reserve = 0 if day >= 29 else (animals if early_dump else (animals * 3 + 2 if day <= 9 else (min(animals + 4, 20) if day <= 10 else min(int(animals * float(_KNOBS.get('wres_m', 1)) + int(_KNOBS.get('wres_a', 2))), int(_KNOBS.get('wres_cap', 16))))))   # wres_*: late wheat reserve kept in the shed (feed comes from our harvest instead of the market)
                extra = stock - reserve
                if extra > 0 and (hour >= 14 or early_dump) and (terminal or early_dump or extra >= BATCH['WHEAT']):
                    orders.append(['SELL', 'WHEAT', extra if (terminal or day >= 12) else BATCH['WHEAT']])
                continue
            if _SW('term_pockets') and day >= 29:
                positions_ = [tuple(farm['farmer'])] + [tuple(p) for p in farm['hands']]
                stock += sum((invs[i] or {}).get(item, 0) for i, p in enumerate(positions_) if i < len(invs) and p in SHED)   # a worker standing at the shed deposits this step: those units sell in this same market (actions run before it)
            if stock <= 0:
                continue
            n_tshop = sum(sh in ('PIZZA_SHOP', 'FARMERS_MARKET') for sh in (obs['town'].get('unlocked_shops', []) or []))
            if item == 'TOMATO' and _SW('tomato') and n_tshop >= int(_KNOBS.get('tom_min', 2)):
                if day < int(_KNOBS.get('tom_sell', 26)):
                    continue   # hold: the deficit (and the hinge price) keeps growing until the sale days
                if not terminal:
                    orders.append(['SELL', 'TOMATO', min(stock, max(2, int(round(float(_KNOBS.get('tom_rate', 1.5)) * n_tshop))))]); continue   # sell at the shops' consumption rate so the deficit (price) holds
            if item == 'CARROT' and _SW('carrot_hold'):
                shops_ = obs['town'].get('unlocked_shops', []) or []
                car_dem = 12 * sum(sh == 'PET_CAFE' for sh in shops_) + 6 * sum(sh == 'FARMERS_MARKET' for sh in shops_)   # units/day nobody else grows
                if car_dem >= int(_KNOBS.get('car_hold_min', 18)) and stock <= int(_KNOBS.get('car_hold_max', 50)) and day < int(_KNOBS.get('car_sell', 26)):
                    continue   # carrot hinge (T 450): let the deficit run to the sale days like tomatoes; the shed keeps up to car_hold_max
                if car_dem >= int(_KNOBS.get('car_hold_min', 18)) and not terminal and day >= int(_KNOBS.get('car_sell', 26)):
                    orders.append(['SELL', 'CARROT', min(stock, max(2, int(round(float(_KNOBS.get('car_rate', 1.0)) * car_dem / 24.0 * 4))))]); continue   # ~ the shops' hourly draw x4
            buf = BUFFER[item] if (farm['money'] >= 3000 and day < 27) else 0   # buffers only once cash flow allows
            if day <= 9 and len(farm['unlocked_quadrants']) < 3 and item != 'FERTILIZER':
                orders.append(['SELL', item, stock]); continue   # land/herd build-up phase: liquidate at once (Majkel sells the first wool/milk in one batch)
            if item == 'FERTILIZER' and 6 <= day <= 26:
                buf = min(16, 2 + self.fert_demand)
                if _SW('fert_batch'):
                    buf = min(8, 1 + self.fert_demand)   # smaller reserve: sell surplus every hour   # reserve today's FERTILIZE demand (planters draw from the shed), sell the rest
                if _SW('fert_zero'):
                    buf = int(_KNOBS.get('fert_buf', 1))   # VRP workers fertilize from their own pockets (collect -> fertilize), so the shed reserve only delays the sale (Majkel's shed holds 0.2 on average)
            if int(_KNOBS.get('sell_h', 0)) and not terminal and day < 29 and hour < int(_KNOBS.get('sell_h', 0)) and item in tuple(_KNOBS.get('sell_h_items', 'STRAWBERRY').split('/')):
                am = int(_KNOBS.get('sell_am_n', 0)) - self.am_sold.get((day, item), 0)   # sell_am_n: a small morning tranche keeps the rival's morning price down
                if am <= 0:
                    continue   # sell_h: the day's harvest sells after the morning consumption ticks (the town eats every 4 steps; a berry sold at h9 sees 2 more ticks than at h1)
                n_am = min(am, stock - buf)
                if n_am > 0:
                    orders.append(['SELL', item, n_am]); self.am_sold[(day, item)] = self.am_sold.get((day, item), 0) + n_am
                continue
            if _SW('mx2') and not terminal and int(_KNOBS.get('mx2_d0', 10)) <= day < 29 and item in tuple(_KNOBS.get('mx2_items', 'STRAWBERRY/MILK/WOOL').split('/')):
                cap_left = 100 - sum(shed.values())
                q = self.mx2_sell(obs, item, stock - buf, day, hour, cap_left)
                if q > 0:
                    orders.append(['SELL', item, q])
                continue
            if (_SW('pace') and not terminal and day < int(_KNOBS.get('pace_last', 27)) and item in ('STRAWBERRY', 'WOOL', 'MILK')
                    and obs['market']['inventory'].get(item, 10000) >= 10000 - int(_KNOBS.get('pace_slack', 0)) and stock < int(_KNOBS.get('pace_max', 60))):
                continue   # pace: never sell into a saturated small market (inventory at/above 10000 = price below base); the town's consumption reopens it within 1-2 days (Majkel sells 64 berries in d25-29 at $172)
            if (_SW('price_hold') and not terminal and day < int(_KNOBS.get('hold_last', 27)) and item in ('MILK', 'WOOL', 'STRAWBERRY', 'EGG')
                    and prices.get(item, 0) < float(_KNOBS.get('hold_f', 0.75)) * BASE_PRICE[item] and stock < int(_KNOBS.get('hold_max', 40))):
                continue   # the rival just dumped: shop consumption restores this small market within 1-2 days, so hold instead of selling into the dip
            if terminal or (item == 'MELON' and (_SW('melon_d9') or _SW('melon_rush')) and day >= int(_KNOBS.get('melon_day', 10))):
                orders.append(['SELL', item, stock])
            elif stock > buf:
                b = BATCH[item]
                if _SW('bank_am') and item in ('STRAWBERRY', 'MILK', 'WOOL') and day >= 12 and hour <= int(_KNOBS.get('bank_h', 12)) + 1:
                    b = max(b, int(_KNOBS.get('bank_batch', 12)))   # the banked morning batch must clear before the tape's afternoon dump
                if _SW('dump0') and hour == 0 and item in ('MILK', 'WOOL', 'EGG', 'STRAWBERRY'):
                    b = max(b, int(_KNOBS.get('dump0_n', 12)))   # dump0: the tape dumps at h0; units sold in the same step interleave with its dump instead of following it
                orders.append(['SELL', item, min(b, stock - buf)])
        if _SW('shed_cap') and hour >= int(_KNOBS.get('cap_h', 22)) and day < 29:
            # the day-end drop discards whatever does not fit in the 100-unit shed (base loses ~55 units/game, mostly wheat):
            # sell the overflow at the last two markets, cheapest reserve first (wheat beyond tomorrow's feed, fertilizer, then products)
            planned = {}
            for o in orders:
                if o[0] == 'SELL':
                    planned[o[1]] = planned.get(o[1], 0) + int(o[2])
            deficit = sum(shed.values()) + sum(sum((inv or {}).values()) for inv in invs) - sum(planned.values()) - int(_KNOBS.get('cap_target', 100)) + (int(_KNOBS.get('cap_m23', 9)) if hour == 23 else int(_KNOBS.get('cap_m', 6)))   # margin for the last harvests; cap_target < 100 leaves room for the h0 wheat top-up
            if deficit > 0:
                order = ['WHEAT', 'FERTILIZER'] + sorted((i for i in PRODUCTS if i not in ('WHEAT', 'FERTILIZER')), key=lambda i: prices.get(i, 0))
                for item in order:
                    if deficit <= 0:
                        break
                    keep = max(0, animals + 2 - inv_wheat) if item == 'WHEAT' else (1 if item == 'FERTILIZER' else 0)
                    extra = min(deficit, shed.get(item, 0) - planned.get(item, 0) - keep)
                    if extra <= 0:
                        continue
                    for o in orders:
                        if o[0] == 'SELL' and o[1] == item:
                            o[2] += extra; break
                    else:
                        orders.append(['SELL', item, extra])
                    deficit -= extra
        # --- purchase priorities for today ---
        want_hands = min(HANDS_BY_DAY[min(day, 29)] + (max(0, int(_KNOBS.get('hands_cap', 11)) - 11) if day >= int(_KNOBS.get('hands_xd', 10)) else 0), int(_KNOBS.get('hands_cap', 11)), int(_KNOBS.get('hands_d29', 11)) if day >= 29 else 99)
        if _SW('fmode') and day <= 1:
            want_hands = max(want_hands, int(_KNOBS.get('fm_hands0', 5)))   # hands_d29: smaller crew on the last day   # hands_cap > 11: extra hands from day hands_xd   # the 10th/11th hand cost 55+89 a day ($3.3k/game): worth it only if they are not idle
        if _SW('hire_first') and hour <= 3 and len(farm['hands']) < want_hands:
            # the market takes 10 orders per step and one HIRE per order: with 6-8 sale orders first, the crew arrived over h0-h2
            # (7% of the day's labour, feeder shares re-split every hour). Sales wait an hour; the smallest sales are dropped first.
            room = max(int(_KNOBS.get('hire_keep', 0)), 10 - min(9, want_hands - len(farm['hands']) + 1))   # keep the top sales: their cash/stock also drive the h0-3 purchases
            if len(orders) > room:
                orders.sort(key=lambda o: -(int(o[2]) * prices.get(o[1], 0)) if o[0] == 'SELL' and len(o) >= 3 else 0)
                orders = orders[:max(0, room)]
        pri = []
        if len(farm['hands']) < want_hands and hour <= 3 and money >= 1:
            pri.append(('HIRE', None, want_hands - len(farm['hands'])))
        melons_have = seeds.get('MELON', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'MELON')
        cows_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') == 'COW') + shed.get('COW', 0) + sum((inv or {}).get('COW', 0) for inv in invs)
        fm = _SW('fmode')   # base20-F: fork skeleton + early herd + late wheat program on top of base19's crop economy (see fm_* knobs)
        if fm and day == 0:
            pri += [('ANIMAL', 'COW', int(_KNOBS.get('fm_cows0', 2))), ('ANIMAL', 'SHEEP', int(_KNOBS.get('fm_sheep0', 2))), ('SEED', 'MELON', int(_KNOBS.get('fm_melons0', 12))),
                    ('SEED', 'WHEAT', max(0, free - sum(int(v) for v in seeds.values())))]   # MG d0: 12 melons (all sold in the d10 rush at the top price), 7 wheat cycling as feed, cash 25
        elif fm and day <= 5 and int(_KNOBS.get('fm_d15', 1)):
            straw_have = seeds.get('STRAWBERRY', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY')
            geese_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') == 'GOOSE') + shed.get('GOOSE', 0) + sum((inv or {}).get('GOOSE', 0) for inv in invs)
            pri.append(('ANIMAL', 'COW', max(0, int(_KNOBS.get('fm_cows5', 2)) - cows_have)))   # MG: 3 cows at d3, 4.4 at d6 (milk +4.3k in d10-18 from the earlier productions)
            if day >= int(_KNOBS.get('fm_goose_d', 4)):
                pri.append(('ANIMAL', 'GOOSE', max(0, int(_KNOBS.get('fm_geese5', 0)) - geese_have)))
            if day >= int(_KNOBS.get('fm_straw_d0', 2)):
                crop_n = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop'))
                room_s = free + crop_n - straw_have - melons_have - int(_KNOBS.get('fm_wheat_min0', 0))   # strawberries take wheat tiles down to fm_wheat_min0 (MG d5: 3 wheat / 4 strawberries)
                pri.append(('SEED', 'STRAWBERRY', max(0, min(int(_KNOBS.get('fm_straw5', 8)) - straw_have, room_s))))
            if straw_have >= int(_KNOBS.get('fm_straw5', 8)) or day < int(_KNOBS.get('fm_straw_d0', 2)):
                pri.append(('SEED', 'WHEAT', max(0, free + ahead - sum(int(v) for v in seeds.values()))))   # wheat only once the early strawberries have their tiles (a wheat on a d2-5 tile delays the first-come berries)
        elif day == 0 and _SW('straw_open'):
            # strawberry opening: no melons (the d10 melon dump is a race the tapes win); 12 strawberries from d0 produce d9/11/13/15 into a fresh market
            pri += [('ANIMAL', 'COW', 2), ('ANIMAL', 'SHEEP', 3), ('PRODUCT', 'WHEAT', 5), ('SEED', 'STRAWBERRY', int(_KNOBS.get('straw0', 6))), ('SEED', 'WHEAT', 11)]
        elif day <= 5 and _SW('straw_open'):
            straw_have = seeds.get('STRAWBERRY', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY')
            pri += [('SEED', 'STRAWBERRY', max(0, int(_KNOBS.get('straw5', 14)) - straw_have)), ('ANIMAL', 'COW', max(0, 2 - cows_have))]
            if straw_have >= int(_KNOBS.get('straw5', 14)):
                pri.append(('SEED', 'WHEAT', max(0, min(10, free) - seeds.get('WHEAT', 0))))
        elif day == 0:
            # melons first: the first dozen melons sold at day 10 fetch ~$800 each (first-mover on a log-priced product)
            if _SW('melon_open'):
                pri += [('ANIMAL', 'COW', 2), ('ANIMAL', 'SHEEP', 2), ('PRODUCT', 'WHEAT', 5), ('SEED', 'MELON', int(_KNOBS.get('melons', 12))), ('ANIMAL', 'SHEEP', 1), ('SEED', 'WHEAT', 11)]   # melons before the third sheep
            else:
                pri += [('ANIMAL', 'COW', int(_KNOBS.get('cows0', 2))), ('ANIMAL', 'SHEEP', int(_KNOBS.get('sheep0', 3)))] + ([] if (_SW('t0war') and hour == 0 and not int(_KNOBS.get('t0_feed', 0))) else [('PRODUCT', 'WHEAT', int(_KNOBS.get('t0_feed', 0)) or int(_KNOBS.get('w0feed', 3)))]) + [('SEED', 'MELON', int(_KNOBS.get('melons0', 8))), ('SEED', 'WHEAT', int(_KNOBS.get('w0seed', 6)))]   # Majkel plants 8 melons at d0 (+2 = +12 units at the d10 price); t0war keeps the feed from the round trip
        elif day <= 5:
            straw_have = seeds.get('STRAWBERRY', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY')
            sheep_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') == 'SHEEP') + shed.get('SHEEP', 0) + sum((inv or {}).get('SHEEP', 0) for inv in invs)
            if _SW('melon_open'):
                pri += [('ANIMAL', 'SHEEP', max(0, 3 - sheep_have)), ('ANIMAL', 'COW', max(0, 2 - cows_have)), ('SEED', 'MELON', max(0, int(_KNOBS.get('melons', 12)) - melons_have) if day <= 2 else 0)]   # the 3rd sheep before anything cheap (else $100 seeds starve the $500 sheep for days)
            else:
                pri += [('SEED', 'MELON', max(0, min(int(_KNOBS.get('melons_late', 12)), 10 if day == 1 else 12) - melons_have) if day <= 2 else 0), ('ANIMAL', 'COW', max(0, int(_KNOBS.get('cows0', 2)) - cows_have)), ('ANIMAL', 'SHEEP', max(0, int(_KNOBS.get('sheep0', 3)) - sheep_have))]   # melons_late: d1-2 top-up target (these ripen d11-12, after the rush)
            if _SW('cow5') and day >= 2:
                pri.append(('ANIMAL', 'COW', max(0, int(_KNOBS.get('cows5', 4)) - cows_have)))   # o227 has 6 animals by d4: a d4 cow gives 9 productions (27 milk) + 25 fertilizer, more than 4 early strawberries
            if _SW('anim3') and day >= 3:
                shops3 = obs['town'].get('unlocked_shops', []) or [None]; first = shops3[0]   # the d3 shop tells the world type 3 days before the bucket does
                if first == 'YARN_STORE' or (int(_KNOBS.get('anim3_y2', 0)) and 'YARN_STORE' in shops3[:2]):   # anim3_y2: a yarn store among the first two shops (the tape commits its sheep program on this)
                    pri.append(('ANIMAL', 'SHEEP', max(0, 3 + int(_KNOBS.get('anim3_n', 2)) - sheep_have)))
                elif first in MILK_SHOPS and int(_KNOBS.get('anim3_cows', 1)):
                    pri.append(('ANIMAL', 'COW', max(0, 2 + int(_KNOBS.get('anim3_n', 2)) - cows_have)))
            if day >= 2:
                pri.append(('SEED', 'STRAWBERRY', max(0, int(_KNOBS.get('straw_early', 8)) - straw_have)))   # d2-5 strawberry target (opening bundle knob)
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
            land_item = [('LAND', None, 1)]
            hf = _SW('herd_first') and day <= int(_KNOBS.get('herd_first_d', 8))
            if not hf or len(farm['unlocked_quadrants']) < 2:
                pri += land_item; land_item = []   # base: land before animals (the d7-8 saving for the 3rd quadrant blocks every other purchase); the 2nd quadrant always first (no tiles for animals before it)
            straw_have = seeds.get('STRAWBERRY', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY')
            straw_stock = shed.get('STRAWBERRY', 0) + sum((inv or {}).get('STRAWBERRY', 0) for inv in invs) - _MX2_HELD.get(self.seat, {}).get('STRAWBERRY', 0)
            berry_dem = 6 * sum(sh in ('ICE_CREAM_SHOP', 'BRUNCH_SPOT', 'SMOOTHIE_SHOP', 'FARMERS_MARKET') for sh in (obs['town'].get('unlocked_shops', []) or []))
            sf = float(_KNOBS.get('straw_f_hi', 0)) if (berry_dem >= int(_KNOBS.get('straw_hi_dem', 24)) and float(_KNOBS.get('straw_f_hi', 0)) > 0) else float(_KNOBS.get('straw_f', _KNOBS.get('room_f', 0.4)))
            if float(_KNOBS.get('sf_deep', 0)) > 0 and berry_dem >= 6 * int(_KNOBS.get('sf_deep_n', 2)):
                sf = float(_KNOBS.get('sf_deep', 0))   # deep berry market (2+ berry shops known at planting time): larger strawberry share
            straw_room = max(0, int(sf * market_room(obs, 'STRAWBERRY')) - straw_stock)   # straw_f: strawberry share of the room (herd keeps room_f); straw_f_hi where >= straw_hi_dem berries/day of shop demand
            straw_cap = max(8, min(int(_KNOBS.get('straw', 40)), straw_room // 6)) + int(_KNOBS.get('straw_plus', 0))   # straw_plus: oracle branch
            if int(_KNOBS.get('sc_plus', 8)):
                shops_ = obs['town'].get('unlocked_shops', []) or []
                n_berry = sum(sh in ('ICE_CREAM_SHOP', 'BRUNCH_SPOT', 'SMOOTHIE_SHOP', 'FARMERS_MARKET') for sh in shops_); n_pizza = sum(sh == 'PIZZA_SHOP' for sh in shops_)
                n_yarn = sum(sh == 'YARN_STORE' for sh in shops_); n_smoot = sum(sh == 'SMOOTHIE_SHOP' for sh in shops_)
                if n_berry >= int(_KNOBS.get('sc_min_berry', 1)) and n_pizza <= int(_KNOBS.get('sc_max_pizza', 0)) and n_yarn <= int(_KNOBS.get('sc_max_yarn', 0)) and n_smoot <= int(_KNOBS.get('sc_max_smoot', 1)):
                    straw_cap += int(_KNOBS.get('sc_plus', 8))   # oracle d6 finding: +8 strawberries pays where berry shops lead and no pizza shop competes for the tiles
            straw_item = [('SEED', 'STRAWBERRY', max(0, min(straw_cap - straw_have, int(_KNOBS.get('straw_d6', 11)) if day == 6 else (int(_KNOBS.get('straw_d79', 4)) if day <= 9 else int(_KNOBS.get('straw_d1012', 3))))))] if day <= 12 else []
            self.straw_dbg = (straw_cap, straw_room, straw_stock, market_room(obs, 'STRAWBERRY'), _OPP_RATE.get(int(obs.get('player', 0)), {}).get('STRAWBERRY', 0.0))
            if _SW('ec2'):
                s_new, _ = self.ec2_targets(obs, farm, day, hour)
                straw_item = [('SEED', 'STRAWBERRY', max(0, min(s_new, int(_KNOBS.get('ec2_batch', 11)))))]   # controller: extra tiles worth more than the wheat filler (net of seeds in hand)
            if _SW('cow1') and self.cow1_done:
                have['COW'] = max(0, have.get('COW', 0) - 1)   # p002: the extra cow is not part of animal_plan's herd (the plan keeps buying its own target)
            anim_items = [('ANIMAL', k, n) for k, n in animal_plan(bucket, day, have, obs).items()]
            if fm:
                # F herd floors (MG mean by checkpoint: cows 4.4/5.9/7.1 and sheep 2.4/5.6/7.1 at d6/d9/d12, geese 1.0/1.4/3.4): the demand caps
                # of animal_plan still add above the floors; below them every animal is also a fertiliser a day and feed comes from the wheat engine
                fl = {'COW': [int(v) for v in _KNOBS.get('fm_cow_fl', '2/2/2').split('/')], 'SHEEP': [int(v) for v in _KNOBS.get('fm_sheep_fl', '2/2/2').split('/')], 'GOOSE': [int(v) for v in _KNOBS.get('fm_goose_fl', '0/0/0').split('/')]}
                stage = 0 if day <= 8 else (1 if day <= 11 else 2)
                plan = dict((k, n) for _, k, n in anim_items)
                for k in ('GOOSE', 'COW', 'SHEEP'):
                    need = max(plan.get(k, 0), fl[k][stage] - have.get(k, 0))
                    if need > 0:
                        plan[k] = need
                anim_items = [('ANIMAL', k, plan[k]) for k in ('GOOSE', 'COW', 'SHEEP') if plan.get(k, 0) > 0]   # base19 order kept: land, strawberries, then the herd (MG d6: +7.5 strawberries, +2 animals)
            if int(_KNOBS.get('d6_geese', 0)) and len(farm['unlocked_quadrants']) < 2:
                anim_items = [it for it in anim_items if it[1] == 'GOOSE']   # d6_geese: before the 2nd quadrant only geese - cows/sheep wait for the land (a same-evening land+herd+berry splurge starves d7-8)
            pri += (anim_items + land_item + straw_item) if (hf or ('anim6' in _FLAGS and day <= 8)) else (straw_item + anim_items)   # herd_first: animals, then (3rd) land, then strawberries
            if fm and day < 9 and int(_KNOBS.get('fm_fill68', 0)):
                res = max(int(_KNOBS.get('fm_tile_res', 4)), straw_cap - straw_have) + sum(n for _, _, n in anim_items)   # d6-8: the filler leaves the tiles of the remaining strawberry program and the herd plan (a d6 wheat is not harvestable before d9; in a 6-berry world base19 fills quadrant 2 with 31 strawberries by d9)
                pri += [('SEED', 'WHEAT', max(0, free + ahead - sum(int(v) for v in seeds.values()) - res))]
            elif day >= 9:
                pri += [('SEED', 'WHEAT', max(0, free + ahead - sum(int(v) for v in seeds.values())))]
            elif _SW('wheat6') and day >= int(_KNOBS.get('wheat_d', 6)) and len(farm['unlocked_quadrants']) >= 2:
                pri += [('SEED', 'WHEAT', max(0, min(int(_KNOBS.get('wheat6_max', 10)), free - sum(int(v) for v in seeds.values()))))]   # d6-8: idle crew + empty tiles; survives the land-3 saving below (cheap)
        elif day <= int(_KNOBS.get('seed_last', 26)):   # seed_last: last day with seed purchases (a d26 wheat still gives 2-3 units on d28-29)
            if day <= 20:
                pri.append(('LAND', None, 1))
            shops = obs['town'].get('unlocked_shops', []) or []
            carrot_demand = sum(sh in ('PET_CAFE', 'FARMERS_MARKET') for sh in shops)
            if _SW('carrot') and carrot_demand and day <= 26:
                # PET_CAFE eats 12 carrots/day (FARMERS_MARKET 6) and nobody grows them: keep ~1 tile per 3 units/day of demand in rotation (3-day crop)
                pets = sum(sh == 'PET_CAFE' for sh in shops)
                carrots_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'CARROT')
                want = min(int(_KNOBS.get('car_max', 16)), int(_KNOBS.get('car_pet', 4)) * pets + int(_KNOBS.get('car_fm', 2)) * (carrot_demand - pets))
                pri.append(('SEED', 'CARROT', max(0, want - seeds.get('CARROT', 0) - carrots_have)))
            elif (carrot_demand or _SW('carrot_all')) and int(_KNOBS.get('car_d0', 15)) <= day <= 26:   # car_d0: first carrot planting day (later = the crop lands straight in the hinge window)
                pets = sum(sh == 'PET_CAFE' for sh in shops)
                if fm and int(_KNOBS.get('fm_carcap', 1)):
                    # F: a carrot TILE target inside the wheat floor (base19's rotation re-seeds every free tile and starved the late wheat: d18 wheat 11 / carrots 11)
                    crop_n = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop')); car_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'CARROT')
                    other = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') in ('STRAWBERRY', 'TOMATO', 'MELON')) + seeds.get('TOMATO', 0)
                    wheat_min = int(_KNOBS.get('fm_wheat_min3', 22)) if day >= int(_KNOBS.get('fm_wheat_d3', 18)) else int(_KNOBS.get('fm_wheat_min', 12))
                    car_t = int(_KNOBS.get('fm_car0', 6)) + int(_KNOBS.get('fm_car_pet', 5)) * pets + int(_KNOBS.get('fm_car_fm', 2)) * (carrot_demand - pets)
                    car_t = min(car_t, max(0, free + crop_n - wheat_min - other - car_have)) if day < 27 else 0
                    pri.append(('SEED', 'CARROT', max(0, min(car_t - car_have - seeds.get('CARROT', 0), free))))
                elif _SW('carrot2') and pets:
                    rot = 8 + int(_KNOBS.get('car_pet', 6)) * pets + int(_KNOBS.get('car_fm2', 0)) * (carrot_demand - pets) + int(_KNOBS.get('car_plus', 0))   # carrot2 (+car_fm2 tiles per FARMERS_MARKET, +car_plus oracle branch): PET_CAFE eats 12/day; base's 8-seed rotation (capped at free//2) undersupplies (rivals sell 90-130 vs our 60)
                    pri.append(('SEED', 'CARROT', max(0, min(rot, free) - seeds.get('CARROT', 0))))
                else:
                    pri.append(('SEED', 'CARROT', max(0, min(8 + int(_KNOBS.get('car_plus', 0)), free // 2) - seeds.get('CARROT', 0))))
            tomato_demand = sum(sh in ('PIZZA_SHOP', 'FARMERS_MARKET') for sh in shops)
            tomatoes_have = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'TOMATO')
            if _SW('tomato') and tomato_demand >= int(_KNOBS.get('tom_min', 2)) and int(_KNOBS.get('tom_d0', 13)) <= day <= int(_KNOBS.get('tom_d1', 18)):
                # tomato hinge: every tomato shop leaves a 6/day deficit nobody fills, so the late price runs to $100-300 (2-3 shops);
                # a d15 tomato yields 1-2/day from d23 -> plant per shop, hold the crop, sell in the last days
                want = min(int(_KNOBS.get('tom_per', 8)) * tomato_demand, int(_KNOBS.get('tom_max', 24)))   # seeds may wait for the next freed wheat tile (tomatoes plant first)
                if _SW('ec2'):
                    _, t_new = self.ec2_targets(obs, farm, day, hour)
                    want = tomatoes_have + seeds.get('TOMATO', 0) + t_new   # controller: tiles whose hinge value beats the wheat alternative
                pri.append(('SEED', 'TOMATO', max(0, want - seeds.get('TOMATO', 0) - tomatoes_have)))
            elif tomato_demand and 15 <= day <= 19:
                pri.append(('SEED', 'TOMATO', max(0, min(8, free // 2) - seeds.get('TOMATO', 0) - tomatoes_have)))
            pri += [('SEED', 'WHEAT', max(0, min(int(_KNOBS.get('wheat_day_cap', 99)), free + ahead - seeds.get('WHEAT', 0) - seeds.get('CARROT', 0) - seeds.get('TOMATO', 0))))]   # wheat_day_cap: seeds per hour cap (with a 4th quadrant, do not swamp the crew)
            if _SW('ec2') and day <= int(_KNOBS.get('ec2_straw_last', 20)):
                s_new, _ = self.ec2_targets(obs, farm, day, hour)
                if s_new > 0:
                    pri.insert(0, ('SEED', 'STRAWBERRY', max(0, min(s_new, int(_KNOBS.get('ec2_batch', 11))))))   # controller: late strawberries only when the projected price still beats wheat
            if int(_KNOBS.get('straw2_n', 0)) and int(_KNOBS.get('straw2_d0', 19)) <= day <= int(_KNOBS.get('straw2_d1', 21)):
                # second strawberry cycle: the d6-12 plants die around d23-29; a d19-21 plant still yields 2 productions (d28-29) on a tile that would grow one wheat cycle
                s2 = seeds.get('STRAWBERRY', 0) + sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY' and t.get('planted_day', 0) >= int(_KNOBS.get('straw2_d0', 19)))
                pri.append(('SEED', 'STRAWBERRY', max(0, int(_KNOBS.get('straw2_n', 0)) - s2)))
            berry_dem = 6 * sum(sh in ('ICE_CREAM_SHOP', 'BRUNCH_SPOT', 'SMOOTHIE_SHOP', 'FARMERS_MARKET') for sh in shops)
            deep = berry_dem >= int(_KNOBS.get('straw_hi_dem', 24)) and int(_KNOBS.get('straw_last_hi', 0)) > 0   # deep berry market (4+ shops): keep planting (a d16 plant still yields 3 productions at $150-200)
            if day <= (int(_KNOBS.get('straw_last_hi', 14)) if deep else int(_KNOBS.get('straw_last', 14))):
                pri.append(('SEED', 'STRAWBERRY', int(_KNOBS.get('straw_late_hi_n', 4)) if deep else int(_KNOBS.get('straw_late_n', 2))))   # a d14 strawberry still produces d23/25/27/29
        rot_n = feedrot_n(animals, day)
        if rot_n:
            # p003 feed rotation: keep rot_n wheat tiles (planted + seeds in hand) so the herd eats own harvests instead of $44 market feed
            # bought every morning in d2-d9 (base19: $2.3k of the d0-d9 cash, wheat tiles 0 on d2-d8 while the herd/land purchases waited)
            wheat_tiles = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('crop') == 'WHEAT')
            rot_need = rot_n - wheat_tiles - seeds.get('WHEAT', 0)
            T = self.tel; T['feedrot_checks'] = T.get('feedrot_checks', 0) + 1; T['feedrot_max_n'] = max(T.get('feedrot_max_n', 0), rot_n)
            if rot_need > 0:
                # leftover tiles only: the entry goes right after the day's strawberry/melon seed entries, so the berry program keeps its
                # tiles and the rotation fills what would otherwise stay empty (base19: 2-4 free tiles on d3-d5, 10-18 on d6-d8, wheat 0)
                k = max([i_ for i_, x in enumerate(pri) if x[0] == 'SEED' and x[1] in ('STRAWBERRY', 'MELON')] + [-1]) + 1
                pri.insert(k, ('SEED', 'WHEAT', rot_need)); T['feedrot_seed_requests'] = T.get('feedrot_seed_requests', 0) + rot_need
                if hour == 0:
                    T['feedrot_short_days'] = T.get('feedrot_short_days', 0) + 1   # mornings on which the rotation was below target
        if _SW('feed_stock') and placed and day < 29:
            # base counted every worker's pocket wheat (planters' harvest, unusable until the day-end drop) -> the shed ran dry mid-day
            # while 50k sat in the bank: buy for the animals still unfed today, netting only the shed and the feeders' pockets
            unfed = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') and not t.get('fed_today'))
            n_f = max(1, sum(1 for z in self.zone_of.values() if z == 'ANIMALS'))
            feeder_wheat = sum(min((invs[w] or {}).get('WHEAT', 0), -(-unfed // n_f) + 1) for w, z in self.zone_of.items() if z == 'ANIMALS' and w < len(invs))   # a pocket counts only up to that feeder's share
            if _SW('feed_stock2') and getattr(self, 'routes', None):
                # VRP: pocket wheat of a worker with FEED nodes is committed feed (up to the node count); the rest of the pockets is harvest that banks tonight
                feeder_wheat = sum(min((invs[i] or {}).get('WHEAT', 0), sum(1 for m in r if m[1] == 'FEED')) for i, r in self.routes.items() if i < len(invs))
            short = unfed + (0 if (_SW('fmode') and day == 0 and int(_KNOBS.get('fm_feed0m', 1))) else int(_KNOBS.get('feed_margin', 2))) - shed.get('WHEAT', 0) - feeder_wheat
            if short > 0 and hour < 22:
                pri.insert(0, ('PRODUCT', 'WHEAT', short))
        elif placed and day < 29 and shed.get('WHEAT', 0) + inv_wheat < placed:
            pri.insert(0, ('PRODUCT', 'WHEAT', placed - shed.get('WHEAT', 0) - inv_wheat))
        if _SW('fert_buy') and 9 <= day <= 26 and hour <= 12 and prices.get('FERTILIZER', 100) <= int(_KNOBS.get('fert_buy_max', 60)):
            fert_have = shed.get('FERTILIZER', 0) + sum((inv or {}).get('FERTILIZER', 0) for inv in invs)
            if self.fert_demand > fert_have:
                pri.append(('PRODUCT', 'FERTILIZER', self.fert_demand - fert_have))   # a $30-60 unit returns +3 wheat ($120) or +2 strawberries ($200); base never buys
        bought = self.bought.setdefault(day, {})
        # keep a little cash for tomorrow's first hires (fib 1,1,2,3) and feed emergencies
        money -= int(_KNOBS.get('d0_res', 5)) if day == 0 else (12 if day < 8 else 0)   # d0 reserve 25 leaves 545 after the herd: 6 melons; tomorrow's 4 hires cost 7, so 8 leaves room for the 7th melon
        if _SW('hire_res') and day < 28 and hour >= int(_KNOBS.get('hire_h', 8)) and (day in [int(v) for v in _KNOBS.get('hire_days', '9').split('/')] or _KNOBS.get('hire_days') == 'all'):
            fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
            money = min(money, farm['money'] - sum(fib[:min(HANDS_BY_DAY[min(day + 1, 29)], int(_KNOBS.get('hands_cap', 11)))]))   # tomorrow's whole crew at h0 (a hand hired at h3 loses 1/8 of its day)
        seed_price = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
        animal_price = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
        land_price = [1000, 2000, 4000][min(2, len(farm['unlocked_quadrants']) - 1)]
        free_left = free + ahead - sum(int(v) for v in seeds.values()) - unplaced   # tiles still open for new seeds/animals
        saving = False
        for kind, item, target in pri:
            if len(orders) >= 10:
                break
            key = (kind, item)
            if kind in ('ANIMAL', 'SEED', 'LAND') and day == int(_KNOBS.get('save_day', -1)):
                continue   # oracle SAVE branch: no herd/seed/land purchase on this day (feed and hires still go through)
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
                land4 = _SW('land4') and q == 3 and int(_KNOBS.get('land4', 10)) <= day <= int(_KNOBS.get('land4_last', 16))   # 4th quadrant ($4000): 25 more wheat tiles for the second half
                if (q >= 3 and not land4) or not (land4 or (q == 1 and day >= int(_KNOBS.get('land2', 6))) or (q == 2 and day >= int(_KNOBS.get('fm_land3' if _SW('fmode') else 'land3', 9)))):
                    continue   # Majkel: quadrant 2 on day 6 and quadrant 3 on day 9 in every archived game
                if money >= land_price:
                    orders.append(['BUY_LAND']); money -= land_price; bought[key] = done + 1; free_left += 25
                elif day <= 12 and not land4:
                    if (_SW('fmode') and (q == 1 or int(_KNOBS.get('fm_save3', 1)))) or (_SW('wheat6') and day <= 8):
                        saving = True; continue   # keep saving, but let the $10 wheat seeds through (see the SEED branch)
                    if _SW('fmode') and not int(_KNOBS.get('fm_save3', 1)):
                        continue   # F (fm_save3=0): the 3rd quadrant waits for the d10 melon money; d6-9 cash goes to strawberries and the herd (MG: land3 d10-12)
                    break   # save the day's cash for the land instead of buying seeds/animals that have no tile
            elif kind == 'ANIMAL':
                if int(_KNOBS.get('land_cool', 0)) and day <= 9 and bought.get(('LAND', None), 0):
                    continue   # land_cool: no herd purchase on a land day (d6-9): the same-evening land+herd+berry splurge left d7-8 with nothing
                if saving:
                    continue
                n = min(left, int(money // animal_price[item]), max(0, free_left + len(self.reserved)))
                if n > 0:
                    orders.append(['BUY_ANIMAL', item, n]); money -= n * animal_price[item]; bought[key] = done + n; free_left -= n
                elif _SW('fmode') and money < animal_price[item] and day <= int(_KNOBS.get('fm_herd_save', 9)) and free_left + len(self.reserved) > 0:
                    saving = True; continue   # F: the herd deficit before $100 seeds (wheat seeds and feed still pass)
                elif day <= 5 and (_SW('melon_open') or (_SW('cow5') and day >= 2) or (_SW('anim3') and day >= 3)) and money < animal_price[item] and free_left > 0:
                    break   # save for the missing d0 herd animal instead of trickling the cash into $100 seeds
            elif kind == 'SEED':
                if saving and (item != 'WHEAT' or (money < int(_KNOBS.get('wheat6_keep', 100)) and not _SW('fmode'))):
                    continue   # land-3 saving: only wheat, and only from cash above the keep level
                n = min(left, int(money // seed_price[item]), max(0, free_left))
                if n > 0:
                    orders.append(['BUY_SEED', item, n]); money -= n * seed_price[item]; bought[key] = done + n; free_left -= n
            elif kind == 'PRODUCT':
                unit = prices.get(item, 25) + 2
                n = min(left, int(money // unit))
                if n > 0:
                    orders.append(['BUY_PRODUCT', item, n]); money -= n * unit
        if _SW('cow1') and not self.cow1_done and day < 29:
            orders, money, free_left = self.cow1_offer(obs, farm, day, hour, orders, money, free_left, pri, bought, shed, invs, prices, placed, unplaced)
        if _os.environ.get('MO_DEBUG') and day == int(_os.environ.get('MO_DEBUG')) and hour < 6:
            print(f"MO d{day} h{hour} money={farm['money']:.0f} free={free} free_left={free_left} seeds={dict(seeds)} straw(cap,room,stock,mroom,opp)={getattr(self, 'straw_dbg', None)} pri={[(k, i, t) for k, i, t in pri]} orders={orders}", flush=True)
        if _SW('hire0') and hour == 0 and len(orders) > 10:
            orders = [o for o in orders if o[0] == 'HIRE'] + [o for o in orders if o[0] != 'HIRE']   # the 10-order cap must not push hires to h1 (a hand hired at h1 appears at h2)
        return orders[:10]

    def cow1_offer(self, obs, farm, day, hour, orders, money, free_left, pri, bought, shed, invs, prices, placed, unplaced):
        """sw_cow1 (p002): at most ONE cow beyond animal_plan, paid from the cash left after every planned purchase of this step, inside
        the day window c1_d0..c1_d1, and only when (1) the near-term committed spend stays covered (tomorrow's crew at h0, feed for the
        whole herd incl. the new cow for c1_feed_days, a c1_res margin), (2) no planned seed/animal/land target of this step is still
        unfilled (the cow never jumps the planner's own queue), (3) a tile is free for the pasture, (4) the milk market net of the rival's
        measured supply still prices the herd's + the cow's remaining units at >= c1_price, (5) a conservative payback (milk at that price
        + a fertiliser a day - feed at market price - c1_labour a day - $400) clears c1_margin. Every evaluation is counted in the
        telemetry with its first failing condition; P002_DEBUG=1 prints them."""
        K = _KNOBS.get
        if not (int(K('c1_d0', 6)) <= day <= int(K('c1_d1', 16))) or hour > int(K('c1_h', 21)) or len(orders) >= 10:
            return orders, money, free_left
        T = self.tel; T['p002_checks'] = T.get('p002_checks', 0) + 1

        def block(reason, **info):
            T['p002_block_' + reason] = T.get('p002_block_' + reason, 0) + 1
            if day not in self.cow1_log:
                self.cow1_log[day] = dict(reason=reason, hour=hour, **info)   # the day's first evaluation
            if _os.environ.get('P002_DEBUG') and hour in (0, 12):
                print(f"P002 d{day} h{hour} block {reason} {info} money={int(money)}", flush=True)
            return orders, money, free_left
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        crew = sum(fib[:min(HANDS_BY_DAY[min(day + 1, 29)], int(K('hands_cap', 11)))])
        herd = placed + unplaced + 1
        wheat_have = shed.get('WHEAT', 0) + sum((inv or {}).get('WHEAT', 0) for inv in invs)
        feed_cost = max(0, herd * int(K('c1_feed_days', 2)) - wheat_have) * (prices.get('WHEAT', 25) + 2)
        need = 400 + crew + feed_cost + int(K('c1_res', 200))
        if money < need:
            return block('cash', money=int(money), need=int(need))
        q = len(farm['unlocked_quadrants'])
        land_ok = (q == 1 and day >= int(K('land2', 6))) or (q == 2 and day >= int(K('land3', 9))) or (_SW('land4') and q == 3 and int(K('land4', 10)) <= day <= int(K('land4_last', 16)))
        unfilled = [(k, i) for k, i, t in pri if t - bought.get((k, i), 0) > 0 and i != 'WHEAT'
                    and ((k == 'LAND' and land_ok) or (k == 'SEED' and free_left > 0) or (k == 'ANIMAL' and free_left + len(self.reserved) > 0))]   # planned purchases still open for want of cash (not for want of a tile or a land rule)
        if unfilled:
            return block('queue', unfilled=str(unfilled[:3]))
        if free_left + len(self.reserved) < 1:
            return block('tile')
        cows = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') == 'COW') + shed.get('COW', 0) + sum((inv or {}).get('COW', 0) for inv in invs)
        left_days = 29 - day
        new_units = max(0, (left_days - ANIMAL_FIRST['COW']) // 2 + 1) if left_days > ANIMAL_FIRST['COW'] else 0   # a cow placed today milks from day+8 every 2 days
        herd_units = cows * left_days // 2
        stock = shed.get('MILK', 0) + sum((inv or {}).get('MILK', 0) for inv in invs)
        room = market_room(obs, 'MILK')   # units this market absorbs before $1, net of the rival's measured supply (sw_opp_supply)
        p_final = price_at('MILK', 10000 + SMALL_FLOOR_X['MILK'] - (room - stock - herd_units - new_units))   # price once everything the herd + the cow will make has landed
        if new_units <= 0 or p_final < int(K('c1_price', 100)):
            return block('room', p_final=int(p_final), room=int(room), herd_units=int(herd_units), new_units=int(new_units))
        p_fert = min(prices.get('FERTILIZER', 50), int(K('c1_fert_cap', 60)))
        value = new_units * p_final + left_days * p_fert - left_days * (prices.get('WHEAT', 25) + 2) - left_days * int(K('c1_labour', 5)) - 400
        if value < int(K('c1_margin', 200)):
            return block('payback', value=int(value), p_final=int(p_final), new_units=int(new_units))
        orders.append(['BUY_ANIMAL', 'COW', 1]); money -= 400; free_left -= 1; self.cow1_done = True
        T.update(p002_bought=1, p002_buy_day=day, p002_buy_hour=hour, p002_value=int(value), p002_p_final=int(p_final), p002_new_units=int(new_units), p002_cash_after=int(money))
        self.cow1_log[day] = dict(reason='BUY', hour=hour, value=int(value), p_final=int(p_final), cows_before=int(cows))
        if _os.environ.get('P002_DEBUG'):
            print(f"P002 d{day} h{hour} BUY cow value={int(value)} p_final={int(p_final)} new_units={new_units} cows={cows} cash_after={int(money)}", flush=True)
        return orders, money, free_left

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
                    last = (age >= CROP_LAST.get(crop, 99) or (_SW('last_harv') and day >= 29 and crop in ('WHEAT', 'CARROT') and age >= 2)) and (t.get('watered_today') or hour >= 20 or crop not in (('WHEAT', 'MELON', 'CARROT') if _SW('car_wf') else ('WHEAT', 'MELON')))   # water first on the last window day (car_wf: carrots too - the age-3 watering is the 3rd unit; Majkel 2.6 u/harvest vs our 2.0); last_harv: on d29 a d27 wheat is worth its 2 units
                    md = int(_KNOBS.get('melon_day', 10)) if (_SW('melon_d9') or _SW('melon_rush')) else -1   # melon rush: harvest at first light of the first harvestable day and sell before the tapes' h09-15 dump (one-shot sq market)
                    tile_md = (day if (crop == 'MELON' and int(_KNOBS.get('rush_all', 0)) and age == CROP_FIRST['MELON'] and _SW('melon_rush')) else md)   # rush_all: every melon's first ripe day
                    if tile_md > 0 and crop == 'MELON' and day == tile_md and t.get('yield_units', 0) >= 3 and age >= CROP_FIRST['MELON'] and (t.get('watered_today') or hour >= int(_KNOBS.get('melon_hcut', 8)) or not int(_KNOBS.get('melon_water10', 1))):
                        out.append((-1, (x, y), ['HARVEST'], None))
                    elif _SW('melon_harv0') and crop == 'MELON' and t.get('yield_units', 0) >= 6:
                        out.append((0, (x, y), ['HARVEST'], None))
                    elif mature and t.get('yield_units', 0) > 0 and not (_SW('lwe') and int(_KNOBS.get('lwe_h4', 1)) and crop == 'WHEAT' and age == 3 and t.get('fertilized_until_day', -1) >= day + 1 and day + 1 <= 29) and (crop in ONGOING or last or (int(_KNOBS.get('term_harv', 0)) and day >= int(_KNOBS.get('term_harv_d', 29))) or t['yield_units'] >= ((int(_KNOBS.get('wheat_units', 3)) if age >= 3 else 5) if crop == 'WHEAT' else 6)   # fertilized wheat: 5 units at age 3 (1.25/day) beats 6 at age 4
                                                                  or (crop == 'WHEAT' and day <= 8 and (feed_short or seeds_waiting) and t['yield_units'] >= 2)):
                        out.append((0 if (_SW('bank_am') and crop == 'STRAWBERRY' and hour <= int(_KNOBS.get('bank_h', 12)) and day >= 12) else 1, (x, y), ['HARVEST'], None))   # bank_am: berries picked in the morning, banked and sold before the tape's afternoon dump
                    if not t.get('watered_today'):
                        # Majkel's watering economy: water on planting day, on yield-window days, and whenever a skipped day
                        # would become a weed (2 unwatered days); every other day is skipped (e.g. wheat age 1, strawberry off-days)
                        must = age == 0 or t.get('consecutive_unwatered', 0) >= 1
                        window = ((crop == 'WHEAT' and 2 <= age <= 4) or (crop == 'CARROT' and 2 <= age <= 3) or (crop == 'MELON' and 6 <= age <= 12)
                                  or (crop == 'STRAWBERRY' and age >= 9 and (age - 9) % 2 == 0) or (crop == 'TOMATO' and age >= 7))
                        if must or window:
                            hot = crop == 'MELON' and 6 <= age <= 12   # each missed melon watering day = 1 unit x ~$200 per tile and a later first sale
                            pr_w = (0 if hour >= 16 else 1) if must else (2 if hour >= 12 else 3)
                            if hot and tile_md > 0 and day == tile_md and int(_KNOBS.get('melon_water10', 1)):
                                pr_w = -1   # rush day: the window watering adds a unit at the top price and the harvest waits for it
                            elif hot and _SW('melon_water'):
                                pr_w = 0 if (age >= int(_KNOBS.get('melon_pr_age', 9)) or hour >= int(_KNOBS.get('melon_pr_hour', 12))) else 1   # ripening day/afternoons shared by all planters
                            elif hot and md > 0 and day <= md:
                                pr_w = -1 if (day == md and int(_KNOBS.get('melon_water10', 1))) else 1   # every window watering before the sale is a unit at the top price
                            out.append((pr_w, (x, y), ['WATER'], None))
                    fert_ok = t.get('fertilized_until_day', -1) < day
                    lead = 2 if (crop == 'TOMATO' and _SW('tom_f6')) else 1   # tom_f6: dose at age 6 so the first production (end of age 7) is already doubled (the age-7 dose often lands after it)
                    if fert_ok and crop in ONGOING and age >= CROP_FIRST[crop] - lead and (age - (CROP_FIRST[crop] - lead)) % ONGOING[crop] == 0:
                        out.append((0 if crop == 'STRAWBERRY' else (1 if _SW('tomato') else 2), (x, y), ['FERTILIZE'], 'FERTILIZER'))   # strawberries first (c207): the age-9/13 dose must land before the production watering; a tomato dose = +3 units over 3 days
                    elif _SW('lwe') and int(_KNOBS.get('lwe_dose', 1)) and fert_ok and crop == 'WHEAT' and age == int(_KNOBS.get('lwe_dose_age', 2)) and day >= int(_KNOBS.get('lwe_d0', 18)) and day + 2 <= 29:
                        out.append((float(_KNOBS.get('lwe_dose_pr', 1.5)), (x, y), ['FERTILIZE'], 'FERTILIZER'))   # sw_lwe: dose behind the strawberry (0) / tomato (1) doses; with the age-3 cut skipped a dosed wheat gives 5 units at age 4 (pr 0 = before the watering = 6 units, but it starved the tomato doses: -6 tomatoes/game)
                    elif _SW('fmode') and fert_ok and crop == 'WHEAT' and age == 2:
                        if day >= int(_KNOBS.get('fm_wf_d', 10)):
                            out.append((2, (x, y), ['FERTILIZE'], 'FERTILIZER'))
                    elif fert_ok and crop == 'WHEAT' and age == 2 and not _SW('no_wheat_fert') and not (int(_KNOBS.get('nwf_lo', 9)) <= day < int(_KNOBS.get('nwf_d', 20))):   # nwf_d: no wheat dose before this day (early fertilizer sells for $60-90 and every unit lowers the rival's pie)   # o227 fertilizes ~24 wheat/game and sells the rest ($40-70)
                        out.append((3, (x, y), ['FERTILIZE'], 'FERTILIZER'))   # age 2 covers all three window waterings (3 -> 6 units)
                elif t.get('animal'):
                    yu = t.get('yield_units', 0)
                    if yu >= 2 or (yu >= 1 and day >= 27):
                        out.append(((0 if (int(_KNOBS.get('harv_pr0', 0)) and day <= int(_KNOBS.get('harv_pr0_d', 9)) and yu >= 4) else 1) if yu >= 4 else 2, (x, y), ['HARVEST'], None))   # harv_pr0: early animal products first (the d6 wool funds the same-day purchases)
                    prod_price = obs['market']['prices'].get({'COW': 'MILK', 'SHEEP': 'WOOL', 'GOOSE': 'EGG'}[t['animal']], 0)
                    worth = day < int(_KNOBS.get('worth_d', 27)) or 'nofeedskip' in _FLAGS or prod_price >= obs['market']['prices'].get('WHEAT', 25) * float(_KNOBS.get('worth_f', 1.0))   # worth_d/worth_f: from this day feed only animals whose product beats the feed price (late milk/wool can be $1-40)
                    skip_feed = False
                    if _SW('feed_alt') and not t.get('fed_today') and t.get('consecutive_unfed', 0) == 0 and day <= int(_KNOBS.get('feed_alt_last', 7)):
                        # pre-production days: an unfed animal still produces, only the care bonus (+1 per fed&cared day, consumed at the first
                        # production, capped by max_held) needs the feed - so skip every other feeding while the remaining days can still fill the cap
                        a_ = t['animal']; age_ = day - int(t.get('placed_day', day)); left_ = ANIMAL_FIRST[a_] - 1 - age_   # fed&cared days that still count (the production day's own care is added after the production), today included
                        need_ = {'COW': 6, 'SHEEP': 6, 'GOOSE': 4}[a_] - 1 - int(t.get('pending_care_bonus', 0))
                        skip_feed = left_ >= 1 and left_ - 1 >= need_
                    if not t.get('fed_today') and day < 29 and worth and not skip_feed:
                        out.append((-1 if (_SW('rescue') and t.get('consecutive_unfed', 0) >= 1) else 0, (x, y), ['FEED'], 'WHEAT'))   # -1 = escapes tonight: every worker may feed it
                    if not t.get('cared_today') and day < 28 and not skip_feed:
                        out.append((1, (x, y), ['CARE'], None))
                    if t.get('fertilizer_available'):
                        out.append((2, (x, y), ['COLLECT_FERTILIZER'], None))
                elif t.get('kind') == 'WEED':
                    out.append((2, (x, y), ['DIG'], None))
        return out

    def plan_placements(self, obs, farm, day, harvest_tiles=()):
        """Animals waiting in the shed -> build + place; seeds -> plant on free tiles (NW first, then new land).
        sw_replant: tiles being harvested today also get a PLANT node (same tile, so the VRP chains harvest -> plant in one visit
        instead of a second trip hours or a day later; far tiles lost a day per cycle)."""
        shed = obs['private']['shed']; seeds = obs['private']['seeds']; out = []; claimed = set()
        invs = obs['private'].get('inventories', []) or []
        for kind in ('COW', 'SHEEP', 'GOOSE'):
            n = shed.get(kind, 0) + sum((inv or {}).get(kind, 0) for inv in invs)
            if n <= 0:
                continue
            struct = ANIMAL_STRUCT[kind]
            empties = [(x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row) if isinstance(t, dict) and t.get('kind') == struct and 'animal' not in t]
            for p in empties[:n]:
                out.append((int(_KNOBS.get('place_pr', 0)), p, ['PLACE', kind], kind))   # place_pr -1: a bought animal is placed before anything else (a next-day placement costs a production day)
            missing = n - len(empties)
            if missing > 0:
                herd = [(x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row) if isinstance(t, dict) and t.get('kind') in ('PASTURE', 'COOP')]
                anchors = herd or [(4, 4)]
                cands = self.free_tiles(farm, 'NW' if day < 6 else None)
                cands.sort(key=lambda q: (min(dist(q, a) for a in anchors), dist(q, (4, 4))))
                if _SW('melon_near') and day <= 1:
                    cands.sort(key=lambda q: (dist(q, (4, 4)) < int(_KNOBS.get('melon_ring', 3)), min(dist(q, a) for a in anchors), dist(q, (4, 4))))   # d0 herd behind the melon ring: the d10 melon rush must reach the shed by h6
                cands = sorted(self.reserved, key=lambda q: (min(dist(q, a) for a in anchors), dist(q, (4, 4)))) + cands   # held tiles first
                for q in cands[:missing]:
                    out.append((int(_KNOBS.get('place_pr', 0)), q, ['BUILD_' + struct], None)); claimed.add(q)
        if not _SW('herd_block'):
            claimed = set()   # base: crops may take the build tile first (the structure then drifts to whatever stays free)
        car_first = _SW('carrot') or (_SW('carrot2') and any(sh == 'PET_CAFE' for sh in (obs['town'].get('unlocked_shops', []) or [])))
        order = ['MELON', 'STRAWBERRY'] + (['TOMATO'] if _SW('tomato') else []) + (['CARROT'] if car_first else []) + ['WHEAT'] + ([] if car_first else ['CARROT']) + ([] if _SW('tomato') else ['TOMATO'])
        if _SW('vrp_h23') and obs.get('hour', 0) >= 23:
            return out   # a plant at h23 cannot be watered on its planting day and is a weed by midnight
        used = {}
        for crop in order:
            n = seeds.get(crop, 0)
            if n <= 0:
                continue
            cand = [q for q in self.free_tiles(farm, 'NW' if day < 6 else None) if q not in claimed]
            if _SW('lwe') and int(_KNOBS.get('lwe_sort', 0)) and day >= int(_KNOBS.get('lwe_d0', 18)) and obs.get('hour', 0) <= int(_KNOBS.get('lwe_h1', 16)):
                step_ = int(obs['step']); stale = int(_KNOBS.get('lwe_stale', 6))
                cand.sort(key=lambda q: (step_ - self.empty_since.get(q, step_) < stale, -(step_ - self.empty_since.get(q, step_)) if step_ - self.empty_since.get(q, step_) >= stale else 0, dist(q, (4, 4))))   # lwe_sort: tiles that waited >= lwe_stale hours first (oldest first), then nearest
            picked = cand[:n]
            for p in picked:
                pr_ = 1
                if _SW('lwe') and day >= int(_KNOBS.get('lwe_d0', 18)) and obs.get('hour', 0) <= int(_KNOBS.get('lwe_h1', 16)) and int(obs['step']) - self.empty_since.get(p, int(obs['step'])) >= int(_KNOBS.get('lwe_stale', 6)):
                    pr_ = float(_KNOBS.get('lwe_pr', 1))   # lwe_pr < 1: a stale far tile is planted before the day's harvests (tested 0/0.5: displaced waterings, wheat -16u)
                out.append((pr_, p, ['PLANT', crop], None))
            used[crop] = len(picked)
        if (_SW('replant') or (_SW('fmode') and int(_KNOBS.get('fm_replant', 1)))) and harvest_tiles and obs.get('hour', 0) <= 20:
            spare = {c: seeds.get(c, 0) - used.get(c, 0) for c in order if seeds.get(c, 0) - used.get(c, 0) > 0}   # seeds beyond the free tiles (seed_ahead buys them)
            for p in harvest_tiles:
                crop = next((c for c in order if spare.get(c, 0) > 0), None)
                if crop is None:
                    break
                spare[crop] -= 1; out.append((1.5, p, ['PLANT', crop], None))   # follows the HARVEST node on the same tile (distance 0; 1.5 = after the harvest in ties)
        return out

    def track_market(self, obs, step):
        """Estimate the rival's supply per product from the market inventory: d(inv) = our sales + rival sales - shop/town consumption.
        Feeds market_room so herd/strawberry caps respect what the rival is already dumping (shared small markets)."""
        inv = obs['market']['inventory']; shops = obs['town'].get('unlocked_shops', []) or []
        prev = getattr(self, 'mkt_prev', None); day = step // 24
        if prev is not None and step > 0:
            for item in PRODUCTS:
                cons = 0
                if (step - 1) % 4 == 0:   # the town consumed right after the previous step's market
                    for sh in shops:
                        pr = SHOP_PRODUCTS.get(sh, ())
                        if item in pr:
                            cons += 2 if len(pr) == 1 else 1
                if step % 24 == 0 and item != 'FERTILIZER':
                    cons += 1
                rival = inv.get(item, 10000) - prev.get(item, 10000) - self.last_sells.get(item, 0) + cons
                self.opp_day[item] = self.opp_day.get(item, 0.0) + rival
                if _SW('mx2'):
                    a_ = float(_KNOBS.get('mx2_alpha', 0.5)); k_ = (item, (step - 1) % 24)   # the change happened in the previous step's market
                    self.opp_hour[k_] = (1 - a_) * self.opp_hour.get(k_, max(0.0, rival)) + a_ * max(0.0, rival)   # rival units by hour of day (EMA over days: the tapes repeat their schedule)
            if step % 24 == 0:
                for item in PRODUCTS:
                    self.opp_hist.setdefault(item, []).append(self.opp_day.get(item, 0.0))
                    hist = self.opp_hist[item][-int(_KNOBS.get('opp_days', 3)):]
                    _OPP_RATE.setdefault(self.seat, {})[item] = sum(hist) / len(hist)
                self.opp_day = {}
        self.mkt_prev = dict(inv)

    # ---------------- sw_vrp: persistent per-worker routes with cheapest insertion ----------------
    NEED = {'FEED': 'WHEAT', 'FERTILIZE': 'FERTILIZER'}

    def dispatch_vrp(self, obs, farm, day, hour, positions, invs, tasks):
        """Daily dispatch as a vehicle-routing heuristic: every task is inserted into the route of the worker where it adds
        the fewest steps (detour via the shed when the item is missing), highest priority first, within the steps left
        today. Routes persist across steps (no re-targeting), so no zones/strips/feeder split is needed."""
        priv = obs['private']; shed = priv['shed']; n = len(positions); left = (24 if _SW('vrp_h23') else 23) - hour   # vrp_h23: the h23 step is a real step (actions run before the day-end pass): 23-hour left the whole crew idle at h23 and killed every h22 planting (unwatered on its planting day)
        rush_run = self.rush_today(farm, day); rush = rush_run and hour < 12   # melon rush morning: pr<0 nodes lead, one per worker
        if getattr(self, 'routes_day', -1) != day:
            self.routes = {}; self.routes_day = day
        live = {(t[1], t[2][0]): t for t in tasks}
        persist = int(_KNOBS.get('vrp_persist', 0))
        routes = {i: ([node for node in self.routes.get(i, []) if node in live] if persist else []) for i in range(n)}
        cap = min(left, max(int(_KNOBS.get('vrp_min', 6)), int(float(_KNOBS.get('vrp_bal', 1.4)) * float(_KNOBS.get('vrp_w', 2.0)) * len(tasks) / max(1, n))))   # balanced load: cheapest insertion below this cap keeps locality without piling on one worker
        need_of = lambda node: (live[node][3] if live[node][3] else self.NEED.get(node[1]))
        shed_near = lambda p: nearest_shed(p)

        def leg_cost(i, r, k, node, seen=None):
            """Extra steps if `node` is inserted at position k of worker i's route (move + act + shed detour when the item is missing).
            seen: whether the needed item is already fetched earlier in the route (None = compute here)."""
            prev = positions[i] if k == 0 else r[k - 1][0]
            nxt = r[k][0] if k < len(r) else None
            tile = node[0]; need = need_of(node)
            detour = 0
            if need and (invs[i] or {}).get(need, 0) <= 0 and not (any(need_of(m) == need for m in r[:k]) if seen is None else seen):
                if shed.get(need, 0) <= 0:
                    return None
                sh = shed_near(prev); detour = abs(prev[0] - sh[0]) + abs(prev[1] - sh[1]) + abs(sh[0] - tile[0]) + abs(sh[1] - tile[1]) - abs(prev[0] - tile[0]) - abs(prev[1] - tile[1]) + 1
            add = abs(prev[0] - tile[0]) + abs(prev[1] - tile[1]) + 1 + detour
            if nxt is not None:
                add += abs(tile[0] - nxt[0]) + abs(tile[1] - nxt[1]) - abs(prev[0] - nxt[0]) - abs(prev[1] - nxt[1])
            return add

        def route_cost(i, r):
            pos = positions[i]; c = 0; got = set()
            for node in r:
                need = need_of(node)
                if need and (invs[i] or {}).get(need, 0) <= 0 and need not in got:
                    sh = shed_near(pos); c += abs(pos[0] - sh[0]) + abs(pos[1] - sh[1]) + 1; pos = sh; got.add(need)
                c += abs(pos[0] - node[0][0]) + abs(pos[1] - node[0][1]) + 1; pos = node[0]
            return c

        def nn_order(i, r):
            """Re-order a route greedily from the worker's position (shed detour counted when the item is missing); trim what no longer fits today."""
            pos = positions[i]; got = set(); out = []; rest = list(r); c = 0
            while rest:
                def step_c(node):
                    need = need_of(node)
                    if need and (invs[i] or {}).get(need, 0) <= 0 and need not in got:
                        sh = shed_near(pos); return abs(pos[0] - sh[0]) + abs(pos[1] - sh[1]) + 1 + abs(sh[0] - node[0][0]) + abs(sh[1] - node[0][1]) + 1, need
                    return abs(pos[0] - node[0][0]) + abs(pos[1] - node[0][1]) + 1, None
                nxt = min(rest, key=lambda m: (step_c(m)[0] - (100 if (rush and live[m][0] < 0) else (int(_KNOBS.get('vrp_pr', 4)) if live[m][0] <= 0 else 0)), live[m][0]))   # urgent (pr<=0) nodes pull forward; rush nodes lead
                dc, got_need = step_c(nxt)
                if c + dc > left:
                    break
                c += dc; pos = nxt[0]; out.append(nxt); rest.remove(nxt)
                if got_need:
                    got.add(got_need)
            return out
        for i in range(n):
            routes[i] = nn_order(i, routes[i])
        assigned = {node for r in routes.values() for node in r}
        cost = {i: route_cost(i, routes[i]) for i in range(n)}
        todo = [t for t in tasks if (t[1], t[2][0]) not in assigned]
        vpr = lambda t: (3 if t[2][0] == 'COLLECT_FERTILIZER' else (2 if (t[2][0] == 'WATER' and t[0] >= 3) else t[0]))   # a window watering (+1 wheat) outranks a fertilizer pickup once the day is full
        todo.sort(key=lambda t: (vpr(t), min(dist(p, t[1]) for p in positions)))
        for pr, tile, op, need in todo:
            node = (tile, op[0]); best = None
            solo = rush and pr < 0 and any(not any(live[m][0] < 0 for m in routes[i]) for i in range(n))   # rush: one melon tile per worker while workers are free
            vlen = int(_KNOBS.get('vrp_len', 12)); nd = need_of(node)
            for i in range(n):
                r = routes[i]
                if pr >= 2 and len(r) >= vlen:
                    continue
                if solo and any(live[m][0] < 0 for m in r):
                    continue
                ci = cost[i]
                if ci + 1 > left or (best is not None and (ci + 1 > cap, 1, ci) >= best[0]):
                    continue   # exact pruning: every insertion adds >= 1 step, so no position of this route can beat the current best key
                seen = False
                for k in range(len(r) + 1):
                    if k > 0 and nd and need_of(r[k - 1]) == nd:
                        seen = True
                    add = leg_cost(i, r, k, node, seen)
                    if add is None:
                        break
                    fin = ci + add
                    if fin > left:
                        continue
                    over = fin > cap   # beyond the balanced share: allowed only when nobody has room
                    key = (over, add, ci)
                    if best is None or key < best[0]:
                        best = (key, i, k)
            if best is not None:
                routes[best[1]].insert(best[2], node); cost[best[1]] = route_cost(best[1], routes[best[1]])
        for i in range(n):
            routes[i] = nn_order(i, routes[i])   # final order = greedy nearest from the worker, urgent first
            if _SW('vrp_2opt') and len(routes[i]) >= 4:
                r = routes[i]; improved = True; guard = 0
                while improved and guard < 20:
                    improved = False; guard += 1
                    for a in range(len(r) - 2):
                        for b in range(a + 2, len(r)):
                            pa = positions[i] if a == 0 else r[a - 1][0]
                            before = dist(pa, r[a][0]) + (dist(r[b][0], r[b + 1][0]) if b + 1 < len(r) else 0)
                            after = dist(pa, r[b][0]) + (dist(r[a][0], r[b + 1][0]) if b + 1 < len(r) else 0)
                            if after + 1e-9 < before and live[r[a]][0] > 0 and live[r[b]][0] > 0:   # never move an urgent node later
                                r[a:b + 1] = r[a:b + 1][::-1]; improved = True
                routes[i] = r
        self.routes = routes
        # ---- emit one command per worker ----
        cmds = []
        for i, pos in enumerate(positions):
            inv = invs[i] or {}; r = routes[i]
            needs = {need_of(m) for m in r if need_of(m)}
            carried = {k: v for k, v in inv.items() if k in PRODUCTS and k not in needs}
            if day >= 29 and hour >= 18 and sum(carried.values()) >= 1:
                if pos in SHED:
                    item = max(carried, key=carried.get); cmds.append(['PLACE', item, carried[item]])
                else:
                    cmds.append(step_toward(pos, shed_near(pos)) or ['PASS'])
                continue
            if rush_run and inv.get('MELON', 0) >= 1 and hour < 16:
                if pos in SHED:
                    cmds.append(['PLACE', 'MELON', inv['MELON']]); continue
                cmds.append(step_toward(pos, shed_near(pos)) or ['PASS']); continue   # rush: every melon reaches the market before the tapes' h9 dump
            if _SW('fmode') and hour <= int(_KNOBS.get('fm_bank_h', 20)) and day < 29 and not any(live[m][0] < 0 for m in r):
                prices = obs['market']['prices']; val = sum(inv.get(k, 0) * prices.get(k, 0) for k in ('STRAWBERRY', 'MILK', 'WOOL', 'EGG', 'MELON', 'TOMATO'))
                if val >= float(_KNOBS.get('fm_bank_v', 400)) and dist(pos, shed_near(pos)) <= int(_KNOBS.get('fm_bank_d', 5)):
                    if pos in SHED:
                        item = max(('STRAWBERRY', 'MILK', 'WOOL', 'EGG', 'MELON', 'TOMATO'), key=lambda k: inv.get(k, 0) * prices.get(k, 0)); cmds.append(['PLACE', item, inv[item]]); continue
                    cmds.append(step_toward(pos, shed_near(pos)) or ['PASS']); continue   # F: $400+ of product sells today instead of after the day-end drop
            if _SW('bank_am') and hour <= int(_KNOBS.get('bank_h', 12)) and day >= 12 and not any(live[m][0] < 0 for m in r):
                # bank_am: the tape sells its berry harvest the same afternoon (h13-23) while ours rode in pockets until the day-end drop and sold next
                # morning behind it; a carrier with a berry batch banks it before noon so it sells ahead of the tape's dump (same units, earlier)
                bk = sum(inv.get(k, 0) for k in ('STRAWBERRY', 'MILK', 'WOOL'))
                if bk >= int(_KNOBS.get('bank_n', 4)) and dist(pos, shed_near(pos)) <= int(_KNOBS.get('bank_d', 4)):
                    if pos in SHED:
                        item = max(('STRAWBERRY', 'MILK', 'WOOL'), key=lambda k: inv.get(k, 0)); cmds.append(['PLACE', item, inv[item]]); continue
                    cmds.append(step_toward(pos, shed_near(pos)) or ['PASS']); continue
            if pos in SHED and sum(carried.values()) >= (3 if r else 1):
                item = max(carried, key=carried.get); cmds.append(['PLACE', item, carried[item]]); continue
            if not r:
                if carried and dist(pos, shed_near(pos)) <= 22 - hour:
                    cmds.append(step_toward(pos, shed_near(pos)) or ['PASS'])   # idle: bank whatever is carried so it sells today (the early fertilizer cash loop)
                else:
                    cmds.append(['PASS'])
                continue
            while r and need_of(r[0]) and inv.get(need_of(r[0]), 0) <= 0 and shed.get(need_of(r[0]), 0) <= 0:
                r.pop(0)   # the item is nowhere to be had right now: skip the node instead of waiting at the shed all day
            if not r:
                cmds.append(['PASS']); continue
            if _SW('vrp_preload') and pos in SHED:
                short = [(m, need_of(m)) for m in r if need_of(m) and shed.get(need_of(m), 0) > 0]
                lack = {}
                for m, nd in short:
                    lack[nd] = lack.get(nd, 0) + 1
                lack = {nd: k - inv.get(nd, 0) for nd, k in lack.items() if k - inv.get(nd, 0) > 0}
                if lack:
                    nd = max(lack, key=lack.get)
                    cmds.append(['PICKUP', nd, max(1, min(8, lack[nd], shed.get(nd, 0)))]); continue   # leaving the shed: take what the whole route needs, not only the first node
            tile, opname = r[0]; op = live[r[0]][2]; need = need_of(r[0])
            if need and inv.get(need, 0) <= 0:
                if pos in SHED:
                    qty = min(8, sum(1 for m in r if need_of(m) == need), shed.get(need, 0))
                    cmds.append(['PICKUP', need, max(1, qty)])
                else:
                    cmds.append(step_toward(pos, shed_near(pos)) or ['PASS'])
                continue
            if pos == tile:
                cmds.append(op)
                if not need:
                    pass
            else:
                cmds.append(step_toward(pos, tile) or ['PASS'])
        return cmds

    def act(self, obs):
        step = int(obs['step']); day = step // 24; hour = step % 24
        if getattr(self, 'cur_day', -1) != day:
            self.idle_yday = getattr(self, 'pass_today', 40); self.pass_today = 0; self.cur_day = day   # yesterday's idle worker-steps (ec2 labour shadow price)
        farm = obs['farms'][self.seat]; priv = obs['private']
        positions = [tuple(farm['farmer'])] + [tuple(p) for p in farm['hands']]
        invs = priv.get('inventories', []) or []
        invs = invs + [{}] * (len(positions) - len(invs))
        bucket = world_bucket(obs['town'].get('unlocked_shops', []))
        if _SW('opp_supply'):
            self.track_market(obs, step)
        if _SW('lwe'):
            now_empty = {(x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row) if t is None}
            self.empty_since = {q: self.empty_since.get(q, step) for q in now_empty}   # sw_lwe: how long each free tile has waited (far corners waited days)
        self.reserved = self.herd_reserve(obs, farm, day, bucket)
        crop_tasks = self.tasks(obs, farm, day, hour)
        harvest_tiles = [t[1] for t in crop_tasks if t[2][0] == 'HARVEST' and isinstance(farm['tiles'][t[1][1]][t[1][0]], dict) and farm['tiles'][t[1][1]][t[1][0]].get('crop') in ('WHEAT', 'MELON')] if (_SW('replant') or (_SW('fmode') and int(_KNOBS.get('fm_replant', 1)))) else ()   # carrot tiles wait for carrot seeds (the rotation), so only wheat/melon tiles chain into wheat
        tasks = self.plan_placements(obs, farm, day, harvest_tiles) + crop_tasks
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
        if _SW('vrp'):
            cmds = self.dispatch_vrp(obs, farm, day, hour, positions, invs, tasks)
            self.last_sells = {}
            for o in orders:
                if o[0] == 'SELL':
                    self.last_sells[o[1]] = self.last_sells.get(o[1], 0) + min(int(o[2]), priv['shed'].get(o[1], 0))
            self.pass_today = getattr(self, 'pass_today', 0) + sum(1 for c in cmds[:len(positions)] if c == ['PASS'])
            if int(_KNOBS.get('h0_harv', 0)) and hour == 0 and cmds:
                t0 = farm['tiles'][positions[0][1]][positions[0][0]]
                if isinstance(t0, dict) and t0.get('animal') and t0.get('yield_units', 0) >= 2:
                    cmds[0] = ['HARVEST']   # h0_harv: the farmer is the only worker awake at h0 - take the product under his feet before the morning pickups
            return {'farmer': cmds[0] if cmds else ['PASS'], 'hands': cmds[1:len(positions)], 'market': orders}
        cmds = []
        taken = set()
        task_index = {(t[1], t[2][0]): t for t in tasks}
        # zones: worker 0 (farmer) + 1 feeder per 5 animals take animal duty; the rest split plant quadrants by load
        n_workers = len(positions)
        animal_tiles = {t[1] for t in tasks if t[2][0] in ('FEED', 'CARE', 'COLLECT_FERTILIZER') or (t[2][0] == 'HARVEST' and isinstance(farm['tiles'][t[1][1]][t[1][0]], dict) and farm['tiles'][t[1][1]][t[1][0]].get('animal'))}
        n_animals = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal'))
        n_animals += sum(priv['shed'].get(k, 0) for k in ANIMAL_STRUCT) + sum((inv or {}).get(k, 0) for inv in invs for k in ANIMAL_STRUCT)
        feed_ratio = float(_KNOBS.get('feed', 4.5))   # base7 (09-18): 4.5 in every world (c206 table 6.0/6.0/5.0/4.5/5.0 left feeders 1 short from d12; with straw 30: sel +2.0k / hold +2.3k / fresh +2.8k)
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
                if _SW('radial'):
                    tiles_q.sort(key=lambda p: (_math.atan2(p[1] - 4.5, p[0] - 4.5), abs(p[0] - 4.5) + abs(p[1] - 4.5)))   # wedges from the shed outwards: the walk out of the shed is the sweep
                else:
                    tiles_q.sort(key=lambda p: (p[1], p[0] if p[1] % 2 == 0 else -p[0]))
                for idx, tile in enumerate(tiles_q):
                    w = ws[idx * len(ws) // max(1, len(tiles_q))]
                    owner[tile] = w; strips.setdefault(w, []).append(tile)
            self.owner = owner; self.strips = strips; self.cursor = {}
            self.zone_of, self.zone_key = zone_of, zone_key
        owner = self.owner
        feeders = [w for w, z in zone_of.items() if z == 'ANIMALS']
        herd_key = (lambda q: (_math.atan2(q[1] - 4.5, q[0] - 4.5), dist(q, (4, 4)))) if _SW('herd_angle') else (lambda q: (q[1], q[0] if q[1] % 2 == 0 else -q[0]))   # herd_angle: wedges around the shed instead of row snakes (no cross-farm detours)
        herd = sorted(((x, y) for y, row in enumerate(farm['tiles']) for x, t in enumerate(row) if isinstance(t, dict) and t.get('animal')), key=herd_key)   # stable split over the whole herd
        animal_owner = {q: feeders[idx * len(feeders) // max(1, len(herd))] for idx, q in enumerate(herd)} if (feeders and _SW('herd_split')) else {}
        feed_tiles = [t[1] for t in tasks if t[2][0] == 'FEED']

        def wheat_need(w):
            """Wheat a feeder should carry: base = every FEED task (each feeder grabbed 8 -> the last feeder found an empty shed);
            sw_pick_own = its own share's unfed animals + 1; before the crew is complete (h0-2) the share is the expected one."""
            if _SW('pick_own') and animal_owner:
                exp_feeders = min(max(1, HANDS_BY_DAY[min(day, 29)] + 1 - 3), max(1, int(round(n_animals / feed_ratio)))) if n_animals else 1
                if hour <= 2 and exp_feeders > len(feeders):
                    return -(-len(feed_tiles) // exp_feeders) + 1
                return sum(1 for q in feed_tiles if animal_owner.get(q, w) == w) + 1
            return len(feed_tiles)
        if day != self.assign_day:
            self.assign = {}; self.assign_day = day
        prw = float(_KNOBS.get('prw_am', 6)) if hour < int(_KNOBS.get('prw_h', 14)) else float(_KNOBS.get('prw', 6))   # priority weight vs distance: low = nearest-first sweep
        horizon = _SW('horizon') and day < 29
        overflow = _SW('bank_pm') and day < 29 and sum(priv['shed'].values()) + sum(sum((inv or {}).values()) for inv in invs) > int(_KNOBS.get('bank_pm_at', 85))   # idle carriers bank before the h23 market when the day-end drop would overflow
        held = {}
        if _SW('reserve'):
            for w, prev_t in self.assign.items():
                if prev_t in task_index and w < len(positions):
                    held.setdefault(prev_t, w)   # a task someone is already walking to is not re-scored for others (kills late-day flapping)
        for i, pos in enumerate(positions):
            inv = invs[i] or {}
            # deposit harvested goods when standing next to the shed and carrying a lot
            is_feeder = zone_of.get(i) == 'ANIMALS'
            keep = () if day >= (29 if _SW('d28_feed') else 28) else (('WHEAT',) if is_feeder else (('FERTILIZER',) if day >= 9 else ()))   # feeders bank fertilizer; planters keep it for FERTILIZE from d9; d28 without the keep = feeders re-deposit their feed wheat every step
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
            if _SW('melon_d9') and day == int(_KNOBS.get('melon_day', 10)) and inv.get('MELON', 0) >= 1:
                if pos in SHED:
                    cmds.append(['PLACE', 'MELON', inv['MELON']]); continue
                cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS']); continue   # straight to the shed: the h23 market is the last one before the dump
            if _SW('melon_bank') and day <= 14 and (inv.get('MELON', 0) >= 12 or (inv.get('MELON', 0) >= 4 and (hour >= 12 or not any(t[2][0] == 'HARVEST' and (t[1], 'HARVEST') not in taken and isinstance(farm['tiles'][t[1][1]][t[1][0]], dict) and farm['tiles'][t[1][1]][t[1][0]].get('crop') == 'MELON' and dist(pos, t[1]) <= 2 for t in tasks)))):
                if pos in SHED:
                    cmds.append(['PLACE', 'MELON', inv['MELON']]); continue
                cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS']); continue
            if (is_feeder and day <= 9 and sum(inv.get(k, 0) for k in ('WOOL', 'MILK', 'EGG')) >= 3
                    and not any(t[1] == pos and t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks)):
                if pos in SHED:
                    item = max(('WOOL', 'MILK', 'EGG'), key=lambda k: inv.get(k, 0)); cmds.append(['PLACE', item, inv[item]]); continue
                cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS']); continue   # bank the first wool/milk at once: it funds land and herd
            if (zone0 == 'ANIMALS' and inv.get('WHEAT', 0) == 0 and priv['shed'].get('WHEAT', 0) > 0
                    and any(t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks)):
                if pos in SHED:
                    qty = max(1, min(8, wheat_need(i)))
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
            here = [t for t in tasks if t[1] == pos and (t[1], t[2][0]) not in taken and (not t[3] or inv.get(t[3], 0) > 0)
                    and not (zone0 == 'ANIMALS' and hour < 18 and pos in animal_owner and animal_owner[pos] != i)]
            if _SW('melon_d9') and day == int(_KNOBS.get('melon_day', 10)) and zone0 != 'ANIMALS' and hour < 12 and any(t[0] < 0 and (t[1], t[2][0]) not in taken for t in tasks):
                here = [t for t in here if t[0] < 0]   # melon rush morning: planters skip incidental work at their feet
            if zone0 == 'ANIMALS' and any(t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks):
                feed_left = sum(1 for t in tasks if t[2][0] == 'FEED' and (t[1], 'FEED') not in taken)
                tile_here = farm['tiles'][pos[1]][pos[0]]
                ripe = isinstance(tile_here, dict) and tile_here.get('yield_units', 0) >= 4   # about to hit the cap -> collect now (1 step)
                behind = _SW('behind') and feed_left > max(1, n_feeders) * (24 - hour) / 2.0   # feed backlog exceeds ~half the feeders' remaining steps
                allowed = ('FEED', 'CARE') if behind else ('FEED', 'CARE') + (('HARVEST',) if ripe else ()) + (('COLLECT_FERTILIZER',) if (hour < 6 or feed_left <= n_feeders or _SW('collect_here')) else ())   # collect_here: 1 step now beats a return trip
                if 'nofinish' in _FLAGS:
                    allowed = ('FEED', 'CARE')
                here = [t for t in here if t[2][0] in allowed]
            if here:
                pr, tile, op, need = min(here, key=lambda t: t[0])
                best = (-2, pr, tile, op, need)
            prev = self.assign.get(i)
            if zone0 == 'ANIMALS' and inv.get('WHEAT', 0) > 0 and any(t[2][0] == 'FEED' and (t[1], 'FEED') not in taken for t in tasks):
                prev = None   # feed first; a stale planting assignment must not pull a feeder away
            if prev in task_index and prev not in taken:
                pr, tile, op, need = task_index[prev]
                if (not need or inv.get(need, 0) > 0 or priv['shed'].get(need, 0) > 0) and not (horizon and dist(pos, tile) > 23 - hour):
                    best = (-1, pr, tile, op, need)
            zone = zone_of.get(i)
            sweep = 0.0   # sw_sweep: when the strip's remaining work fits in the day, take tiles nearest-first (one pass) instead of priority-first (two passes)
            if _SW('sweep') and best is None and zone not in (None, 'ANIMALS') and own_tiles:
                pend = {}
                for pr_, tile_, op_, need_ in tasks:
                    if tile_ in own_tiles and (tile_, op_[0]) not in taken and held.get((tile_, op_[0]), i) == i and not (need_ and inv.get(need_, 0) <= 0 and priv['shed'].get(need_, 0) <= 0):
                        pend[tile_] = pend.get(tile_, 0) + 1
                if pend:
                    cur = pos; cost = 0; left = dict(pend)
                    while left:
                        nxt = min(left, key=lambda q: dist(cur, q)); cost += dist(cur, nxt) + left.pop(nxt); cur = nxt
                    if cost <= (23 - hour) * float(_KNOBS.get('sweep_f', 0.8)):
                        sweep = 1.0
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
                if (tile, op[0]) in taken or held.get((tile, op[0]), i) != i:
                    continue
                if zone == 'ANIMALS' and tile in animal_owner and animal_owner[tile] != i and hour < 18:
                    continue   # another feeder's animal (until the evening sweep)
                if op[0] == 'COLLECT_FERTILIZER' and zone != 'ANIMALS' and (day <= 8 or hour < 12):
                    continue
                in_zone = (tile in animal_tiles) if zone == 'ANIMALS' else (tile not in animal_tiles and quadrant(*tile) == zone)
                if pr < 0 and (hour >= 8 or (zone != 'ANIMALS' and op[0] != 'FEED')):
                    in_zone = True   # rescue feed (unfed yesterday) after the morning: whoever is closest; melon rush: every planter
                if zone is not None and not in_zone and op[0] not in ('BUILD_PASTURE', 'BUILD_COOP', 'PLACE', 'DIG') and not (_SW('pr0_share') and pr == 0 and zone != 'ANIMALS' and tile not in animal_tiles):
                    continue   # priority-0 field work (ripe melons) is shared by all planters
                if zone != 'ANIMALS' and tile in owner and owner[tile] != i and pr > 0:
                    continue
                if need and inv.get(need, 0) <= 0 and priv['shed'].get(need, 0) <= 0:
                    continue
                d = dist(pos, tile)
                if need and inv.get(need, 0) <= 0:
                    d += dist(pos, nearest_shed(pos)) + dist(nearest_shed(pos), tile) + 1
                if horizon and d > 23 - hour:
                    continue   # cannot arrive and act before the day ends (base wastes ~24 moves/day walking into midnight)
                score = (pr * prw + d) if not (sweep and tile in own_tiles and pr >= 0) else (d + min(pr, 0) * prw)
                if best is None or score < best[0]:
                    best = (score, pr, tile, op, need)
            if best is None and zone is not None:
                for pr, tile, op, need in tasks:
                    if (tile, op[0]) in taken or held.get((tile, op[0]), i) != i or (op[0] == 'FEED' and zone != 'ANIMALS' and pr >= 0):
                        continue
                    if op[0] == 'COLLECT_FERTILIZER' and zone != 'ANIMALS' and (day <= 8 or hour < 12):
                        continue
                    if need and inv.get(need, 0) <= 0 and priv['shed'].get(need, 0) <= 0:
                        continue
                    d = dist(pos, tile)
                    if need and inv.get(need, 0) <= 0:
                        d += dist(pos, nearest_shed(pos)) + dist(nearest_shed(pos), tile) + 1
                    if horizon and d > 23 - hour:
                        continue
                    score = pr * prw + d
                    if best is None or score < best[0]:
                        best = (score, pr, tile, op, need)
            if best is None:
                # nothing to do: drop off goods (idle workers only) or wait; inventories auto-drop at day end
                if carried and pos in SHED:
                    item = max(carried, key=carried.get); cmds.append(['PLACE', item, carried[item]])
                elif carried and dist(pos, nearest_shed(pos)) <= 6 and (day >= 28 or carried.get('WHEAT', 0) >= 3 or (day <= 8 and carried.get('FERTILIZER', 0) >= 1)
                                                                        or (overflow and hour >= 16 and sum(carried.values()) >= 4 and dist(pos, nearest_shed(pos)) <= 22 - hour)) and not (_SW('bank_cut') and dist(pos, nearest_shed(pos)) > 22 - hour):
                    cmds.append(step_toward(pos, nearest_shed(pos)) or ['PASS'])   # after h22 the day-end drop does the banking for free
                else:
                    cmds.append(['PASS'])
                continue
            _, pr, tile, op, need = best
            taken.add((tile, op[0])); self.assign[i] = (tile, op[0])
            if need and inv.get(need, 0) <= 0:
                if pos in SHED:
                    if need == 'WHEAT':
                        qty = max(1, min(8, wheat_need(i)))
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
        self.last_sells = {}
        for o in orders:
            if o[0] == 'SELL':
                self.last_sells[o[1]] = self.last_sells.get(o[1], 0) + min(int(o[2]), priv['shed'].get(o[1], 0))
        return {'farmer': farmer_cmd, 'hands': cmds[1:len(positions)], 'market': orders}


def agent(observation, configuration=None):
    seat = int(observation.get('player', 0)); step = int(observation.get('step', 0))
    for _d in sorted(_GATED):
        if _d <= step // 24:
            _KNOBS.update(_GATED[_d])
    if _PROFILE:
        _b = profile_bucket(list(observation['town'].get('unlocked_shops', []) or []))
        if _b and _b in _PROFILE:
            _KNOBS.update(_PROFILE[_b])
    st = _STATE.get(seat)
    if st is None or step <= st.last_step:
        st = _STATE[seat] = Proxy(seat)
    st.last_step = step
    try:
        out = st.act(observation)
        nulls = [x.split(':') for x in _KNOBS.get('null_days', '').split('/') if x]   # "6:3/9:1:2" = day:hour[:worker]; one worker idles one step (matched-null branches)
        for nd in nulls:
            if int(nd[0]) == step // 24 and int(nd[1]) == step % 24:
                w = int(nd[2]) if len(nd) > 2 else 0
                if w == 0:
                    out['farmer'] = ['PASS']
                elif w - 1 < len(out['hands']):
                    out['hands'][w - 1] = ['PASS']
        return out
    except Exception:
        return {'farmer': ['PASS'], 'hands': [['PASS'] for _ in observation['farms'][seat].get('hands', [])], 'market': []}


agent.telemetry = _TEL   # read by the canonical runner (championship_league.timed_policy) at step 718
