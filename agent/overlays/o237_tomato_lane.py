# o237_tomato_lane (Claude/o-series, 2026-09-16). Late tomato lane for PIZZA/FARMERS_MARKET worlds on the o227 stack.
# Frozen-Majkel diagnosis (YARN,PET,PIZZA,PIZZA): Majkel grows 10-11 tomatoes from ~day 16 and earns 6.9k from them in
# d24-30; our stack only runs the V219 program (>= 3 tomato shops, SE land). Rule: from day 16 to 22, while >= 2
# tomato shops are unlocked, turn up to 8 of the tape's PLANT WHEAT commands into PLANT TOMATO (companion BUY_SEED
# TOMATO orders cover them). The tape keeps watering the tile and its periodic HARVEST on that tile collects the tomato
# units (ongoing crop, max_held 4); extra SELL TOMATO covers stock the parent does not sell. Telemetry o237_*.
import copy as _o237_copy

_O237_PARENT = agent
_O237_STATE = {}
_O237_REPORT = {}
_O237_MAX_SITES = 8
_O237_DAY0, _O237_DAY1 = 16, 22
del agent


def _o237_demand(observation):
    shops = observation['town'].get('unlocked_shops', []) or []
    return sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in shops)


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0)); day = step // 24
    st = _O237_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O237_STATE[seat] = {'last': -1, 'sites': 0, 'swaps': 0, 'seed_orders': 0, 'extra_sales': 0, 'errors': 0}
    st['last'] = step
    parent = _O237_PARENT(observation, configuration)
    result = parent
    try:
        hot = _O237_DAY0 <= day <= _O237_DAY1 and _o237_demand(observation) >= 2 and st['sites'] < _O237_MAX_SITES
        out = None
        if hot:
            farm = observation['farms'][seat]; private = observation['private']
            positions = [farm['farmer'], *farm['hands']]
            cmds = [parent.get('farmer') or ['PASS'], *(parent.get('hands') or [])]
            seeds = int(private['seeds'].get('TOMATO', 0) or 0)
            for i, c in enumerate(cmds[:len(positions)]):
                if c == ['PLANT', 'WHEAT'] and seeds > 0 and st['sites'] < _O237_MAX_SITES:
                    x, y = positions[i]
                    if farm['tiles'][y][x] is not None:
                        continue
                    out = out or _o237_copy.deepcopy(parent)
                    if i == 0:
                        out['farmer'] = ['PLANT', 'TOMATO']
                    else:
                        out['hands'][i - 1] = ['PLANT', 'TOMATO']
                    seeds -= 1; st['sites'] += 1; st['swaps'] += 1
            orders = (out or parent).get('market') or []
            need = _O237_MAX_SITES - st['sites'] - int(private['seeds'].get('TOMATO', 0) or 0)
            if need > 0 and any(o and o[0] == 'BUY_SEED' and o[1] == 'WHEAT' for o in orders) and len(orders) < 10:
                out = out or _o237_copy.deepcopy(parent)
                out['market'] = list(out.get('market') or []) + [['BUY_SEED', 'TOMATO', int(min(need, 4))]]
                st['seed_orders'] += 1
        if st['sites'] and day >= _O237_DAY0 + 8:
            act = out or parent
            orders = act.get('market') or []
            stock = projected_shed(act, FarmView(observation)).get('TOMATO', 0)
            sale = sum(max(0, int(o[2])) for o in orders if o and o[:2] == ['SELL', 'TOMATO'])
            if stock > sale and len(orders) < 10 and observation['market']['prices'].get('TOMATO', 0) > 1:
                out = out or _o237_copy.deepcopy(parent)
                out['market'] = list(out.get('market') or []) + [['SELL', 'TOMATO', int(stock - sale)]]
                st['extra_sales'] += 1
        if out is not None:
            result = out
    except Exception:
        st['errors'] += 1
        result = parent
    _O237_REPORT.clear()
    _O237_REPORT.update(getattr(_O237_PARENT, 'telemetry', {}))
    _O237_REPORT.update({'o237_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O237_REPORT
agent = globals().pop('agent')
