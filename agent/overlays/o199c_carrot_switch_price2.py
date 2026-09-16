# o199c_carrot_switch price-only ratio 2.0 (Claude/o-series, 2026-09-15). Overlay for o182.
"""World-conditional WHEAT -> CARROT switch for the tape's wheat cycle.
Evidence: holdout loss -34k in a PET_CAFE x3 world - carrot price 35 -> 229 (hinge), rival planted
102 carrots vs our fixed 31. Carrot (seed 20, 1 + 1 unit per watered day at age 2-3, decays from
age 4) fits the wheat cycle the tape already runs (plant, water, harvest at age 2-4).
Rule (per planting step): switch when carrot demand 6*(2*PET_CAFE + FARMERS_MARKET) >= _O199_DEMAND
or carrot price >= _O199_RATIO * wheat price. Mechanics:
  * market: every BUY_SEED WHEAT n gets a companion BUY_SEED CARROT n (wheat seeds are kept, so a
    failed switch never blocks a planting; unused wheat seeds are worth $10 each);
  * field: PLANT WHEAT -> PLANT CARROT while carrot seeds cover this step's switched plantings;
  * harvest: on a CARROT tile at age 3 any non-HARVEST command by the worker standing there becomes
    HARVEST (the wheat schedule may only come back at age 4, when the carrot is already decaying);
  * sale: projected carrot stock beyond the parent's SELL CARROT orders is appended as one SELL.
Feed wheat is replenished by the existing grain/feed overlays (C126, o177, r97). Never touches the
opening (day < _O199_MIN_DAY) or day >= 27 (a carrot planted then cannot be harvested by day 29).
Telemetry: o199_switches, o199_harvest_swaps, o199_seed_orders, o199_extra_sales, o199_errors.
"""
import copy as _o199_copy

_O199_PARENT = agent
_O199_STATE = {}
_O199_REPORT = {}
_O199_DEMAND = 9999     # b: price-only rule
_O199_RATIO = 2.0
_O199_MIN_DAY = 8
_O199_MAX_DAY = 26
del agent


def _o199_hot(observation):
    shops = observation['town'].get('unlocked_shops', []) or []
    demand = 6 * (2 * shops.count('PET_CAFE') + shops.count('FARMERS_MARKET'))
    prices = observation['market']['prices']
    return demand >= _O199_DEMAND or prices['CARROT'] >= _O199_RATIO * max(1, prices['WHEAT'])


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O199_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O199_STATE[seat] = {'last': -1, 'switches': 0, 'harvest_swaps': 0, 'seed_orders': 0, 'extra_sales': 0, 'errors': 0, 'mine': {}}
    st['last'] = step
    parent_action = _O199_PARENT(observation, configuration)
    result = parent_action
    try:
        day = step // 24
        farm = observation['farms'][seat]
        private = observation['private']
        positions = [farm['farmer'], *farm['hands']]
        cmds = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
        out = None
        hot = _O199_MIN_DAY <= day <= _O199_MAX_DAY and _o199_hot(observation)
        # 1) harvest OUR switched carrots at age 3 (the tape's native carrots keep their own schedule)
        for i, c in enumerate(cmds[:len(positions)]):
            x, y = positions[i]
            tile = farm['tiles'][y][x]
            if (isinstance(tile, dict) and tile.get('kind') == 'PLANT' and tile.get('crop') == 'CARROT'
                    and st['mine'].get((x, y)) == int(tile.get('planted_day', -1))
                    and day - int(tile.get('planted_day', day)) >= 3 and int(tile.get('yield_units', 0)) > 0
                    and c != ['HARVEST']):
                out = out or _o199_copy.deepcopy(parent_action)
                if i == 0:
                    out['farmer'] = ['HARVEST']
                else:
                    out['hands'][i - 1] = ['HARVEST']
                st['harvest_swaps'] += 1
        if hot:
            # 2) PLANT WHEAT -> PLANT CARROT within available carrot seeds
            seeds = int(private['seeds'].get('CARROT', 0) or 0)
            for i, c in enumerate(cmds[:len(positions)]):
                if c == ['PLANT', 'WHEAT'] and seeds > 0:
                    x, y = positions[i]
                    if farm['tiles'][y][x] is not None:
                        continue
                    out = out or _o199_copy.deepcopy(parent_action)
                    if i == 0:
                        out['farmer'] = ['PLANT', 'CARROT']
                    else:
                        out['hands'][i - 1] = ['PLANT', 'CARROT']
                    seeds -= 1; st['switches'] += 1; st['mine'][(x, y)] = day
            # 3) companion carrot seed orders for the wheat seed purchases
            orders = (out or parent_action).get('market') or []
            extra = [['BUY_SEED', 'CARROT', int(o[2])] for o in orders if o and o[0] == 'BUY_SEED' and o[1] == 'WHEAT' and int(o[2]) > 0]
            if extra and len(orders) + len(extra) <= 10:
                out = out or _o199_copy.deepcopy(parent_action)
                out['market'] = list(out.get('market') or []) + extra
                st['seed_orders'] += len(extra)
        # 4) sell carrot stock beyond the parent's carrot sales (only once we have switched)
        if st['switches']:
            act = out or parent_action
            orders = act.get('market') or []
            stock = projected_shed(act, FarmView(observation)).get('CARROT', 0)
            sale = sum(max(0, int(o[2])) for o in orders if o and o[:2] == ['SELL', 'CARROT'])
            if stock > sale and len(orders) < 10:
                out = out or _o199_copy.deepcopy(parent_action)
                out['market'] = list(out.get('market') or []) + [['SELL', 'CARROT', int(stock - sale)]]
                st['extra_sales'] += 1
        if out is not None:
            result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O199_REPORT.clear()
    _O199_REPORT.update(getattr(_O199_PARENT, 'telemetry', {}))
    _O199_REPORT.update({'o199_' + k: v for k, v in st.items() if k not in ('last', 'mine')})
    return result


agent.telemetry = _O199_REPORT
agent = globals().pop('agent')
