# o201b_livestock_ev margin 1000 (Claude/o-series, 2026-09-15). Overlay for o162 (replaces the o171e/o170c rules).
"""Expected-value livestock choice at the tape's purchase slots (route 0/2 only).
The o170/o171 rules ("no milk shop in the first two -> geese", "YARN seen -> sheep") are replaced by
an explicit EV computed from observations at each slot:
    EV(kind) = units * price_hat - cost - feed - externality
    units     = productions in [placed + first_yield, 28] * (1 + interval)          (full care bonus)
    price_hat = engine price curve at the projected inventory, averaged over the horizon:
                inventory + (own_supply + rival_supply - shop_demand - 1) * days, own_supply including
                the candidate block itself; shops consume 1/4 steps per product (2 for single-product)
    feed      = wheat price * remaining days * feed factor (o159 skips cow/sheep non-production nights)
    externality = rival visible animals' remaining units * (price without our block - price with it)
                ADDED: the score is relative, so depressing a product the rival sells is a gain (o179 lesson)
The best kind replaces the tape's default only if EV_best - EV_default >= _O201_MARGIN.
Slots and rewrite schedules (identical tile mapping to o171/o184/o170):
  day 6  (step 150): 2 COW  -> GOOSE/SHEEP  + day-7 cows (169/176)  [4 animals]
  day 8  (step 196): 2 SHEEP -> GOOSE/COW                            [2 animals]
  day 10 (step 241): 3 GOOSE -> SHEEP/COW                            [3 animals]
Telemetry: o201_d6/o201_d8/o201_d10 (chosen kind), o201_rewrites, o201_mismatch, o201_errors.
"""
import copy as _o201_copy

_O201_PARENT = agent
_O201_STATE = {}
_O201_REPORT = {}
_O201_MARGIN = 1000
_O201_FEED = {'GOOSE': 1.0, 'COW': 0.6, 'SHEEP': 0.5}
_O201_COST = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
_O201_SPEC = {'GOOSE': (4, 1, 'EGG', 'COOP'), 'COW': (8, 2, 'MILK', 'PASTURE'), 'SHEEP': (6, 3, 'WOOL', 'PASTURE')}
_O201_SHOPS = {'EGG': ('BAKERY', 'BRUNCH_SPOT'), 'MILK': ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'), 'WOOL': ('YARN_STORE',)}
_O201_SINGLE = {'YARN_STORE', 'PET_CAFE'}
# slot -> (default kind, count, buy signature, schedule of (step, worker, expected cmd, expected pos or None))
_O201_SLOTS = {
    150: ('COW', 4, [['BUY_ANIMAL', 'COW', 2]], [
        (151, 7, ['PICKUP', 'COW'], None), (152, 1, ['PICKUP', 'COW'], None),
        (153, 1, ['BUILD_PASTURE'], (5, 4)), (153, 6, ['BUILD_PASTURE'], (5, 2)),
        (155, 7, ['BUILD_PASTURE'], (5, 3)), (155, 1, ['PLACE', 'COW'], (5, 4)),
        (156, 7, ['PLACE', 'COW'], (5, 3)), (159, 1, ['BUILD_PASTURE'], (6, 4)),
        (169, 'M', ['BUY_ANIMAL', 'COW', 1], None), (170, 3, ['PICKUP', 'COW'], None),
        (176, 'M', ['BUY_ANIMAL', 'COW', 1], None), (177, 3, ['PLACE', 'COW'], (6, 4)),
        (177, 5, ['PICKUP', 'COW'], None), (179, 6, ['PICKUP', 'COW'], None), (182, 6, ['PLACE', 'COW'], (5, 2))]),
    196: ('SHEEP', 2, [['BUY_ANIMAL', 'SHEEP', 2]], [
        (160, 7, ['BUILD_PASTURE'], (6, 3)), (161, 1, ['BUILD_PASTURE'], (7, 4)),   # built before the slot: decided at 150 (see below)
        (197, 5, ['PICKUP', 'SHEEP'], None), (198, 6, ['PICKUP', 'SHEEP'], None),
        (201, 6, ['PLACE', 'SHEEP'], (7, 4)), (213, 5, ['PLACE', 'SHEEP'], (6, 3))]),
    241: ('GOOSE', 3, [['BUY_ANIMAL', 'GOOSE', 2]], [
        (253, 3, ['PICKUP', 'GOOSE'], None), (254, 6, ['BUILD_COOP'], None), (254, 11, ['PICKUP', 'GOOSE'], None),
        (255, 2, ['BUILD_COOP'], None), (258, 3, ['BUILD_COOP'], None), (259, 3, ['PLACE', 'GOOSE'], None),
        (259, 11, ['BUILD_COOP'], None), (260, 11, ['PLACE', 'GOOSE'], None),
        (265, 'M', ['BUY_ANIMAL', 'GOOSE', 1], None), (268, 6, ['PICKUP', 'GOOSE'], None), (275, 6, ['PLACE', 'GOOSE'], None)]),
}
del agent


def _o201_units(kind, placed_day):
    first, interval, _, _ = _O201_SPEC[kind]
    n = sum(1 for d in range(placed_day + first, 29) if (d - placed_day - first) % interval == 0)
    return n * (1 + interval)


def _o201_daily(kind):
    first, interval, _, _ = _O201_SPEC[kind]
    return (1 + interval) / interval


def _o201_count(farm, kind):
    return sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') == kind)


def _o201_ev(observation, seat, kind, count, placed_day, default_kind):
    """EV of buying `count` animals of `kind` now; externality against the rival's visible herd."""
    farm = observation['farms'][seat]; rival = observation['farms'][1 - seat]
    prices = observation['market']['prices']; inv = observation['market']['inventory']
    shops = observation['town'].get('unlocked_shops', []) or []
    product = _O201_SPEC[kind][2]
    days = max(1, 28 - placed_day)
    demand = 1 + sum((2 if s in _O201_SINGLE else 1) * 6 for s in shops if s in _O201_SHOPS[product])
    own = _o201_count(farm, kind)   # the block being decided is not placed yet for any kind
    riv = _o201_count(rival, kind)
    rate = _o201_daily(kind)
    def price_path(extra_animals):
        flow = (own + riv + extra_animals) * rate - demand
        tot = 0.0
        for d in range(1, days + 1):
            tot += _r37_market_price(product, inv[product] + flow * d)
        return tot / days
    p_with = price_path(count); p_without = price_path(0)
    units = _o201_units(kind, placed_day) * count
    feed = prices['WHEAT'] * days * count * _O201_FEED[kind]
    rival_loss = riv * _o201_units(kind, placed_day) * max(0.0, p_without - p_with)
    return units * p_with - _O201_COST[kind] * count - feed + rival_loss


def _o201_choose(observation, seat, slot):
    default, count, _, _ = _O201_SLOTS[slot]
    placed = slot // 24 + 1
    evs = {k: _o201_ev(observation, seat, k, count, placed, default) for k in _O201_SPEC}
    best = max(evs, key=evs.get)
    if best != default and evs[best] - evs[default] >= _O201_MARGIN:
        return best, evs
    return default, evs


def _o201_rewrite(cmd, kind, default):
    """Rename a schedule command from the default species to the chosen one."""
    if cmd[0] in ('PICKUP', 'PLACE'):
        return [cmd[0], kind] + list(cmd[2:])
    if cmd[0].startswith('BUILD_'):
        return ['BUILD_' + _O201_SPEC[kind][3]]
    if cmd[0] == 'BUY_ANIMAL':
        return ['BUY_ANIMAL', kind, cmd[2]]
    return cmd


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O201_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O201_STATE[seat] = {'last': -1, 'd6': '', 'd8': '', 'd10': '', 'rewrites': 0, 'mismatch': 0, 'errors': 0, 'plan': {}}
    st['last'] = step
    parent_action = _O201_PARENT(observation, configuration)
    result = parent_action
    try:
        orders = parent_action.get('market') or []
        out = None
        # decisions: day-6 slot also fixes the day-8 pastures (built at 160/161); day-8 kind decided at 150 too
        if step == 150 and all(sig in orders for sig in _O201_SLOTS[150][2]) and 'YARN_STORE' not in (observation['town'].get('unlocked_shops', []) or [])[:2]:
            k6, _ = _o201_choose(observation, seat, 150); st['d6'] = k6
            k8, _ = _o201_choose(observation, seat, 196); st['d8'] = k8
            for s, w, cmd, pos in _O201_SLOTS[150][3]:
                st['plan'].setdefault(s, []).append((w, cmd, pos, k6, 'COW'))
            for s, w, cmd, pos in _O201_SLOTS[196][3]:
                st['plan'].setdefault(s, []).append((w, cmd, pos, k8, 'SHEEP'))
            if k6 != 'COW':
                out = _o201_copy.deepcopy(parent_action)
                for o in out['market']:
                    if o == ['BUY_ANIMAL', 'COW', 2]:
                        o[1] = k6; st['rewrites'] += 1
        elif step == 196 and st['d8'] and ['BUY_ANIMAL', 'SHEEP', 2] in orders and st['d8'] != 'SHEEP':
            out = _o201_copy.deepcopy(parent_action)
            for o in out['market']:
                if o == ['BUY_ANIMAL', 'SHEEP', 2]:
                    o[1] = st['d8']; st['rewrites'] += 1
        elif step == 241 and all(sig in orders for sig in _O201_SLOTS[241][2]):
            k10, _ = _o201_choose(observation, seat, 241); st['d10'] = k10
            need = 2 * _O201_COST[k10] + 350
            if k10 != 'GOOSE' and observation['farms'][seat]['money'] >= need:
                for s, w, cmd, pos in _O201_SLOTS[241][3]:
                    st['plan'].setdefault(s, []).append((w, cmd, pos, k10, 'GOOSE'))
                out = _o201_copy.deepcopy(parent_action)
                for o in out['market']:
                    if o == ['BUY_ANIMAL', 'GOOSE', 2]:
                        o[1] = k10; st['rewrites'] += 1
            else:
                st['d10'] = 'GOOSE'
        # scheduled rewrites
        if step in st['plan']:
            farm = observation['farms'][seat]
            positions = [farm['farmer'], *farm['hands']]
            cmds = [parent_action.get('farmer')] + list(parent_action.get('hands') or [])
            for w, cmd, pos, kind, default in st['plan'][step]:
                if kind == default:
                    continue
                if w == 'M':
                    if cmd in (out or parent_action)['market']:
                        out = out or _o201_copy.deepcopy(parent_action)
                        for o in out['market']:
                            if o == cmd:
                                o[1] = kind; st['rewrites'] += 1
                    else:
                        st['mismatch'] += 1
                    continue
                ok = w < len(cmds) and cmds[w] == cmd and (pos is None or (w < len(positions) and tuple(positions[w]) == pos))
                if not ok:
                    st['mismatch'] += 1; continue
                out = out or _o201_copy.deepcopy(parent_action)
                new = _o201_rewrite(cmd, kind, default)
                if w == 0:
                    out['farmer'] = new
                else:
                    out['hands'][w - 1] = new
                st['rewrites'] += 1
        if out is not None:
            result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O201_REPORT.clear()
    _O201_REPORT.update(getattr(_O201_PARENT, 'telemetry', {}))
    _O201_REPORT.update({'o201_' + k: v for k, v in st.items() if k not in ('last', 'plan')})
    return result


agent.telemetry = _O201_REPORT
agent = globals().pop('agent')
