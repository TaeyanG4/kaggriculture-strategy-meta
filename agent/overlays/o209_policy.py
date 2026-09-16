# o209_policy (Claude/o-series, 2026-09-15). Overlay for the o162+o174+o177+o182+o199c stack.
"""Livestock policy TABLE for the tape's purchase slots (route 0/2), compiled offline by
o_tools/compile_policy.py from engine rollouts on the world bank (approach A-1).
  d6  (step 150, 4 animals: 2 at 150 + day-7 cows)  key = sorted first-2 shops
  d8  (step 196, sheep pair)                          key = sorted first-2 shops
  d10 (step 241, 3 geese)                             key = sorted first-3 shops
Slot machinery (schedules, renames, cash guard) is o201's; the choice is a table lookup with the
hand-found rules as fallback (goose world -> GOOSE d6; 3 milk -> COW d10; two-milk -> COW d8).
Env KAGG_O209_FORCE="d6,d8,d10" (kind or -) forces choices for rollouts.
"""
import os as _o209_os
_O209_TABLE = {"d6":{"BAKERY|BAKERY":"GOOSE","BAKERY|BRUNCH_SPOT":"GOOSE","BAKERY|FARMERS_MARKET":"GOOSE","BAKERY|ICE_CREAM_SHOP":"COW","BAKERY|PET_CAFE":"GOOSE","BAKERY|PIZZA_SHOP":"COW","BAKERY|SMOOTHIE_SHOP":"COW","BRUNCH_SPOT|BRUNCH_SPOT":"GOOSE","BRUNCH_SPOT|FARMERS_MARKET":"GOOSE","BRUNCH_SPOT|ICE_CREAM_SHOP":"COW","BRUNCH_SPOT|PET_CAFE":"GOOSE","BRUNCH_SPOT|PIZZA_SHOP":"COW","BRUNCH_SPOT|SMOOTHIE_SHOP":"COW","FARMERS_MARKET|FARMERS_MARKET":"GOOSE","FARMERS_MARKET|ICE_CREAM_SHOP":"COW","FARMERS_MARKET|PET_CAFE":"GOOSE","FARMERS_MARKET|PIZZA_SHOP":"COW","FARMERS_MARKET|SMOOTHIE_SHOP":"COW","ICE_CREAM_SHOP|ICE_CREAM_SHOP":"COW","ICE_CREAM_SHOP|PET_CAFE":"COW","ICE_CREAM_SHOP|PIZZA_SHOP":"COW","ICE_CREAM_SHOP|SMOOTHIE_SHOP":"COW","PET_CAFE|PET_CAFE":"GOOSE","PET_CAFE|PIZZA_SHOP":"COW","PET_CAFE|SMOOTHIE_SHOP":"COW","PIZZA_SHOP|PIZZA_SHOP":"COW","PIZZA_SHOP|SMOOTHIE_SHOP":"COW","SMOOTHIE_SHOP|SMOOTHIE_SHOP":"COW"},"d8":{"BAKERY|BAKERY":"SHEEP","BAKERY|BRUNCH_SPOT":"SHEEP","BAKERY|FARMERS_MARKET":"SHEEP","BAKERY|ICE_CREAM_SHOP":"SHEEP","BAKERY|PET_CAFE":"SHEEP","BAKERY|PIZZA_SHOP":"SHEEP","BAKERY|SMOOTHIE_SHOP":"SHEEP","BRUNCH_SPOT|BRUNCH_SPOT":"SHEEP","BRUNCH_SPOT|FARMERS_MARKET":"COW","BRUNCH_SPOT|ICE_CREAM_SHOP":"SHEEP","BRUNCH_SPOT|PET_CAFE":"SHEEP","BRUNCH_SPOT|PIZZA_SHOP":"SHEEP","BRUNCH_SPOT|SMOOTHIE_SHOP":"SHEEP","FARMERS_MARKET|FARMERS_MARKET":"SHEEP","FARMERS_MARKET|ICE_CREAM_SHOP":"SHEEP","FARMERS_MARKET|PET_CAFE":"SHEEP","FARMERS_MARKET|PIZZA_SHOP":"SHEEP","FARMERS_MARKET|SMOOTHIE_SHOP":"SHEEP","ICE_CREAM_SHOP|ICE_CREAM_SHOP":"SHEEP","ICE_CREAM_SHOP|PET_CAFE":"SHEEP","ICE_CREAM_SHOP|PIZZA_SHOP":"SHEEP","ICE_CREAM_SHOP|SMOOTHIE_SHOP":"SHEEP","PET_CAFE|PET_CAFE":"SHEEP","PET_CAFE|PIZZA_SHOP":"GOOSE","PET_CAFE|SMOOTHIE_SHOP":"SHEEP","PIZZA_SHOP|PIZZA_SHOP":"SHEEP","PIZZA_SHOP|SMOOTHIE_SHOP":"COW","SMOOTHIE_SHOP|SMOOTHIE_SHOP":"SHEEP"},"d10":{"BAKERY|BAKERY|BAKERY":"GOOSE","BAKERY|BAKERY|BRUNCH_SPOT":"GOOSE","BAKERY|BAKERY|FARMERS_MARKET":"GOOSE","BAKERY|BAKERY|PET_CAFE":"GOOSE","BAKERY|BAKERY|PIZZA_SHOP":"GOOSE","BAKERY|BAKERY|SMOOTHIE_SHOP":"GOOSE","BAKERY|BAKERY|YARN_STORE":"SHEEP","BAKERY|BRUNCH_SPOT|FARMERS_MARKET":"GOOSE","BAKERY|BRUNCH_SPOT|ICE_CREAM_SHOP":"GOOSE","BAKERY|BRUNCH_SPOT|PET_CAFE":"GOOSE","BAKERY|BRUNCH_SPOT|SMOOTHIE_SHOP":"GOOSE","BAKERY|FARMERS_MARKET|ICE_CREAM_SHOP":"COW","BAKERY|FARMERS_MARKET|PET_CAFE":"GOOSE","BAKERY|FARMERS_MARKET|PIZZA_SHOP":"GOOSE","BAKERY|ICE_CREAM_SHOP|ICE_CREAM_SHOP":"GOOSE","BAKERY|ICE_CREAM_SHOP|PET_CAFE":"COW","BAKERY|ICE_CREAM_SHOP|PIZZA_SHOP":"GOOSE","BAKERY|ICE_CREAM_SHOP|SMOOTHIE_SHOP":"COW","BAKERY|ICE_CREAM_SHOP|YARN_STORE":"SHEEP","BAKERY|PET_CAFE|PIZZA_SHOP":"GOOSE","BAKERY|PET_CAFE|SMOOTHIE_SHOP":"SHEEP","BAKERY|SMOOTHIE_SHOP|SMOOTHIE_SHOP":"GOOSE","BRUNCH_SPOT|BRUNCH_SPOT|BRUNCH_SPOT":"GOOSE","BRUNCH_SPOT|BRUNCH_SPOT|FARMERS_MARKET":"GOOSE","BRUNCH_SPOT|BRUNCH_SPOT|ICE_CREAM_SHOP":"COW","BRUNCH_SPOT|BRUNCH_SPOT|PET_CAFE":"GOOSE","BRUNCH_SPOT|BRUNCH_SPOT|SMOOTHIE_SHOP":"COW","BRUNCH_SPOT|FARMERS_MARKET|ICE_CREAM_SHOP":"GOOSE","BRUNCH_SPOT|FARMERS_MARKET|PET_CAFE":"COW","BRUNCH_SPOT|FARMERS_MARKET|SMOOTHIE_SHOP":"SHEEP","BRUNCH_SPOT|FARMERS_MARKET|YARN_STORE":"SHEEP","BRUNCH_SPOT|ICE_CREAM_SHOP|ICE_CREAM_SHOP":"GOOSE","BRUNCH_SPOT|ICE_CREAM_SHOP|PET_CAFE":"GOOSE","BRUNCH_SPOT|ICE_CREAM_SHOP|PIZZA_SHOP":"COW","BRUNCH_SPOT|PET_CAFE|PET_CAFE":"GOOSE","BRUNCH_SPOT|PET_CAFE|PIZZA_SHOP":"GOOSE","BRUNCH_SPOT|PET_CAFE|SMOOTHIE_SHOP":"GOOSE","BRUNCH_SPOT|PET_CAFE|YARN_STORE":"SHEEP","BRUNCH_SPOT|PIZZA_SHOP|PIZZA_SHOP":"GOOSE","BRUNCH_SPOT|PIZZA_SHOP|SMOOTHIE_SHOP":"COW","BRUNCH_SPOT|PIZZA_SHOP|YARN_STORE":"SHEEP","BRUNCH_SPOT|SMOOTHIE_SHOP|SMOOTHIE_SHOP":"GOOSE","BRUNCH_SPOT|SMOOTHIE_SHOP|YARN_STORE":"SHEEP","FARMERS_MARKET|FARMERS_MARKET|FARMERS_MARKET":"GOOSE","FARMERS_MARKET|FARMERS_MARKET|ICE_CREAM_SHOP":"GOOSE","FARMERS_MARKET|FARMERS_MARKET|PET_CAFE":"GOOSE","FARMERS_MARKET|FARMERS_MARKET|PIZZA_SHOP":"GOOSE","FARMERS_MARKET|FARMERS_MARKET|YARN_STORE":"SHEEP","FARMERS_MARKET|ICE_CREAM_SHOP|ICE_CREAM_SHOP":"GOOSE","FARMERS_MARKET|ICE_CREAM_SHOP|PET_CAFE":"GOOSE","FARMERS_MARKET|ICE_CREAM_SHOP|PIZZA_SHOP":"GOOSE","FARMERS_MARKET|ICE_CREAM_SHOP|SMOOTHIE_SHOP":"GOOSE","FARMERS_MARKET|PET_CAFE|PET_CAFE":"GOOSE","FARMERS_MARKET|PET_CAFE|PIZZA_SHOP":"GOOSE","FARMERS_MARKET|PET_CAFE|SMOOTHIE_SHOP":"GOOSE","FARMERS_MARKET|PET_CAFE|YARN_STORE":"SHEEP","FARMERS_MARKET|PIZZA_SHOP|PIZZA_SHOP":"GOOSE","FARMERS_MARKET|PIZZA_SHOP|SMOOTHIE_SHOP":"COW","FARMERS_MARKET|SMOOTHIE_SHOP|SMOOTHIE_SHOP":"GOOSE","ICE_CREAM_SHOP|ICE_CREAM_SHOP|SMOOTHIE_SHOP":"COW","ICE_CREAM_SHOP|PET_CAFE|PET_CAFE":"GOOSE","ICE_CREAM_SHOP|PET_CAFE|PIZZA_SHOP":"GOOSE","ICE_CREAM_SHOP|PIZZA_SHOP|SMOOTHIE_SHOP":"COW","ICE_CREAM_SHOP|SMOOTHIE_SHOP|SMOOTHIE_SHOP":"COW","PET_CAFE|PET_CAFE|PIZZA_SHOP":"COW","PET_CAFE|PIZZA_SHOP|PIZZA_SHOP":"SHEEP","PET_CAFE|PIZZA_SHOP|SMOOTHIE_SHOP":"GOOSE","PIZZA_SHOP|PIZZA_SHOP|PIZZA_SHOP":"COW","PIZZA_SHOP|PIZZA_SHOP|SMOOTHIE_SHOP":"COW","PIZZA_SHOP|SMOOTHIE_SHOP|SMOOTHIE_SHOP":"COW","SMOOTHIE_SHOP|SMOOTHIE_SHOP|YARN_STORE":"COW"}}   # compiled by o_tools/compile_policy.py
_O209_FORCE = dict(zip(('d6', 'd8', 'd10'), (_o209_os.environ.get('KAGG_O209_FORCE', '-,-,-').split(','))))
_O209_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
_O209_SHADOW = _o209_os.environ.get('KAGG_O209_SHADOW') == '1'   # 1: record the table's suggestion but act on the fallback
_O209_SNAP = {}   # seat -> rival animal counts at step 150 (to read the rival's day-6 kind later)


def _o209_rival_kind(observation, seat):
    rv = observation['farms'][1 - seat]; now = {}
    for row in rv['tiles']:
        for t in row:
            if isinstance(t, dict) and t.get('animal'):
                now[t['animal']] = now.get(t['animal'], 0) + 1
    base = _O209_SNAP.get(seat) or {}
    d = {k: now.get(k, 0) - base.get(k, 0) for k in ('COW', 'SHEEP', 'GOOSE')}
    return max(d, key=d.get) if max(d.values()) > 0 else 'NONE'
import copy as _o209_copy

_O209_PARENT = agent
_O209_STATE = {}
_O209_REPORT = {}
_O209_MARGIN = 300
_O209_FEED = {'GOOSE': 1.0, 'COW': 0.6, 'SHEEP': 0.5}
_O209_COST = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
_O209_SPEC = {'GOOSE': (4, 1, 'EGG', 'COOP'), 'COW': (8, 2, 'MILK', 'PASTURE'), 'SHEEP': (6, 3, 'WOOL', 'PASTURE')}
_O209_SHOPS = {'EGG': ('BAKERY', 'BRUNCH_SPOT'), 'MILK': ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'), 'WOOL': ('YARN_STORE',)}
_O209_SINGLE = {'YARN_STORE', 'PET_CAFE'}
# slot -> (default kind, count, buy signature, schedule of (step, worker, expected cmd, expected pos or None))
_O209_SLOTS = {
    150: ('COW', 4, [['BUY_ANIMAL', 'COW', 2]], [
        (151, 7, ['PICKUP', 'COW'], None), (152, 1, ['PICKUP', 'COW'], None),
        (153, 1, ['BUILD_PASTURE'], (5, 4)), (153, 6, ['BUILD_PASTURE'], (5, 2)),
        (155, 7, ['BUILD_PASTURE'], (5, 3)), (155, 1, ['PLACE', 'COW'], (5, 4)),
        (156, 7, ['PLACE', 'COW'], (5, 3)), (159, 1, ['BUILD_PASTURE'], (6, 4)),
        (169, 'M', ['BUY_ANIMAL', 'COW', 1], None), (170, 3, ['PICKUP', 'COW'], None),
        (176, 'M', ['BUY_ANIMAL', 'COW', 1], None), (177, 3, ['PLACE', 'COW'], (6, 4)),
        (177, 5, ['PICKUP', 'COW'], None), (179, 6, ['PICKUP', 'COW'], None), (182, 6, ['PLACE', 'COW'], (5, 2))]),
    196: ('SHEEP', 4, [['BUY_ANIMAL', 'SHEEP', 2]], [   # day-8 pair + day-9 singles (217, 226): all four day-8/9 sheep
        (160, 7, ['BUILD_PASTURE'], (6, 3)), (161, 1, ['BUILD_PASTURE'], (7, 4)),   # built before the slot: decided at 150 (see below)
        (197, 5, ['PICKUP', 'SHEEP'], None), (198, 6, ['PICKUP', 'SHEEP'], None),
        (201, 6, ['PLACE', 'SHEEP'], (7, 4)), (213, 5, ['PLACE', 'SHEEP'], (6, 3)),
        (217, 'M', ['BUY_ANIMAL', 'SHEEP', 1], None), (222, 3, ['PICKUP', 'SHEEP'], None), (229, 3, ['PLACE', 'SHEEP'], (6, 2)),
        (226, 'M', ['BUY_ANIMAL', 'SHEEP', 1], None), (252, 1, ['PICKUP', 'SHEEP'], None),
        (257, 1, ['BUILD_PASTURE'], (1, 4)), (258, 1, ['PLACE', 'SHEEP'], (1, 4))]),
    241: ('GOOSE', 3, [['BUY_ANIMAL', 'GOOSE', 2]], [
        (253, 3, ['PICKUP', 'GOOSE'], None), (254, 6, ['BUILD_COOP'], None), (254, 11, ['PICKUP', 'GOOSE'], None),
        (255, 2, ['BUILD_COOP'], None), (258, 3, ['BUILD_COOP'], None), (259, 3, ['PLACE', 'GOOSE'], None),
        (259, 11, ['BUILD_COOP'], None), (260, 11, ['PLACE', 'GOOSE'], None),
        (265, 'M', ['BUY_ANIMAL', 'GOOSE', 1], None), (268, 6, ['PICKUP', 'GOOSE'], None), (275, 6, ['PLACE', 'GOOSE'], None)]),
}
del agent


def _o209_units(kind, placed_day):
    first, interval, _, _ = _O209_SPEC[kind]
    n = sum(1 for d in range(placed_day + first, 29) if (d - placed_day - first) % interval == 0)
    return n * (1 + interval)


def _o209_daily(kind):
    first, interval, _, _ = _O209_SPEC[kind]
    return (1 + interval) / interval


def _o209_count(farm, kind):
    return sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal') == kind)


def _o209_ev(observation, seat, kind, count, placed_day, default_kind):
    """EV of buying `count` animals of `kind` now; externality against the rival's visible herd."""
    farm = observation['farms'][seat]; rival = observation['farms'][1 - seat]
    prices = observation['market']['prices']; inv = observation['market']['inventory']
    shops = observation['town'].get('unlocked_shops', []) or []
    product = _O209_SPEC[kind][2]
    days = max(1, 28 - placed_day)
    demand = 1 + sum((2 if s in _O209_SINGLE else 1) * 6 for s in shops if s in _O209_SHOPS[product])
    own = _o209_count(farm, kind)   # the block being decided is not placed yet for any kind
    riv = _o209_count(rival, kind)
    rate = _o209_daily(kind)
    def price_path(extra_animals):
        flow = (own + riv + extra_animals) * rate - demand
        tot = 0.0
        for d in range(1, days + 1):
            tot += _r37_market_price(product, inv[product] + flow * d)
        return tot / days
    p_with = price_path(count); p_without = price_path(0)
    units = _o209_units(kind, placed_day) * count
    feed = prices['WHEAT'] * days * count * _O209_FEED[kind]
    rival_loss = riv * _o209_units(kind, placed_day) * max(0.0, p_without - p_with)
    return units * p_with - _O209_COST[kind] * count - feed + rival_loss


def _o209_fallback(observation, slot):
    shops = observation['town'].get('unlocked_shops', []) or []
    milk2 = sum(s in _O209_MILK for s in shops[:2]); milk3 = sum(s in _O209_MILK for s in shops[:3])
    if slot == 150: return 'GOOSE' if milk2 == 0 else 'COW'
    if slot == 196: return 'SHEEP'
    if slot == 241:
        if 'YARN_STORE' in shops[:3]: return 'SHEEP'
        if milk3 == 3: return 'COW'   # o205 (goose world + 1 milk shop -> cows) rejected: replays 27% vs 51% win
        return 'GOOSE'
    return _O209_SLOTS[slot][0]


def _o209_choose(observation, seat, slot, st=None):
    """Table lookup with rival-aware key first (d8/d10), shop-only key second, hand rules last."""
    name = {150: 'd6', 196: 'd8', 241: 'd10'}[slot]
    forced = _O209_FORCE.get(name, '-')
    if forced in _O209_SPEC:
        return forced, {}
    shops = observation['town'].get('unlocked_shops', []) or []
    base_key = '|'.join(sorted(shops[:2] if slot != 241 else shops[:3]))
    fb = _o209_fallback(observation, slot)
    tab = _O209_TABLE.get(name, {})
    kind = None; used = ''
    if slot != 150:
        rk = base_key + '#r=' + _o209_rival_kind(observation, seat)
        if tab.get(rk) in _O209_SPEC:
            kind, used = tab[rk], rk
    if kind is None and tab.get(base_key) in _O209_SPEC:
        kind, used = tab[base_key], base_key
    suggestion = kind or fb
    if st is not None:   # shadow record: what the table says vs the hand rule
        st['shadow'][name] = (used or '-', suggestion, fb)
        if suggestion != fb:
            st['disagree'] += 1
    return (fb if _O209_SHADOW else suggestion), {}


def _o209_rewrite(cmd, kind, default):
    """Rename a schedule command from the default species to the chosen one."""
    if cmd[0] in ('PICKUP', 'PLACE'):
        return [cmd[0], kind] + list(cmd[2:])
    if cmd[0].startswith('BUILD_'):
        return ['BUILD_' + _O209_SPEC[kind][3]]
    if cmd[0] == 'BUY_ANIMAL':
        return ['BUY_ANIMAL', kind, cmd[2]]
    return cmd


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O209_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O209_STATE[seat] = {'last': -1, 'd6': '', 'd8': '', 'd10': '', 'rewrites': 0, 'mismatch': 0, 'errors': 0, 'plan': {}, 'shadow': {}, 'disagree': 0}
    st['last'] = step
    parent_action = _O209_PARENT(observation, configuration)
    result = parent_action
    try:
        orders = parent_action.get('market') or []
        out = None
        # decisions: day-6 slot also fixes the day-8 pastures (built at 160/161); day-8 kind decided at 150 too
        if step == 150 and all(sig in orders for sig in _O209_SLOTS[150][2]) and 'YARN_STORE' not in (observation['town'].get('unlocked_shops', []) or [])[:2]:
            _O209_SNAP[seat] = {}
            for row in observation['farms'][1 - seat]['tiles']:
                for t in row:
                    if isinstance(t, dict) and t.get('animal'):
                        _O209_SNAP[seat][t['animal']] = _O209_SNAP[seat].get(t['animal'], 0) + 1
            k6, _ = _o209_choose(observation, seat, 150, st); st['d6'] = k6; st['route0'] = True
            for s, w, cmd, pos in _O209_SLOTS[150][3]:
                st['plan'].setdefault(s, []).append((w, cmd, pos, k6, 'COW'))
            if k6 != 'COW':
                out = _o209_copy.deepcopy(parent_action)
                for o in out['market']:
                    if o == ['BUY_ANIMAL', 'COW', 2]:
                        o[1] = k6; st['rewrites'] += 1
        elif step == 160 and st.get('route0'):   # rival's day-6 animals are placed by 155/156: decide the day-8 pair now
            k8, _ = _o209_choose(observation, seat, 196, st); st['d8'] = k8
            for s, w, cmd, pos in _O209_SLOTS[196][3]:
                st['plan'].setdefault(s, []).append((w, cmd, pos, k8, 'SHEEP'))
        if step == 196 and st['d8'] and ['BUY_ANIMAL', 'SHEEP', 2] in orders and st['d8'] != 'SHEEP':
            out = _o209_copy.deepcopy(parent_action)
            for o in out['market']:
                if o == ['BUY_ANIMAL', 'SHEEP', 2]:
                    o[1] = st['d8']; st['rewrites'] += 1
        if step == 241 and all(sig in orders for sig in _O209_SLOTS[241][2]):
            k10, _ = _o209_choose(observation, seat, 241, st); st['d10'] = k10
            need = 2 * _O209_COST[k10] + 350
            if k10 != 'GOOSE' and observation['farms'][seat]['money'] >= need:
                for s, w, cmd, pos in _O209_SLOTS[241][3]:
                    st['plan'].setdefault(s, []).append((w, cmd, pos, k10, 'GOOSE'))
                out = _o209_copy.deepcopy(parent_action)
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
                        out = out or _o209_copy.deepcopy(parent_action)
                        for o in out['market']:
                            if o == cmd:
                                o[1] = kind; st['rewrites'] += 1
                    else:
                        st['mismatch'] += 1
                    continue
                ok = w < len(cmds) and cmds[w] == cmd and (pos is None or (w < len(positions) and tuple(positions[w]) == pos))
                if not ok:
                    st['mismatch'] += 1; continue
                out = out or _o209_copy.deepcopy(parent_action)
                new = _o209_rewrite(cmd, kind, default)
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
    _O209_REPORT.clear()
    _O209_REPORT.update(getattr(_O209_PARENT, 'telemetry', {}))
    _O209_REPORT.update({'o209_' + k: v for k, v in st.items() if k not in ('last', 'plan', 'shadow', 'route0')})
    for nm, (used, sug, fb) in st['shadow'].items():
        _O209_REPORT['o209_shadow_' + nm] = f'{sug}|{fb}|{used}'
    return result


agent.telemetry = _O209_REPORT
agent = globals().pop('agent')
