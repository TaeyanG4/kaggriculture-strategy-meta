# o196b_no_demand_abandon_d15 (Claude/o-series, 2026-09-15). Overlay for o181.
"""Stop feeding COW/SHEEP whose product has no shop demand: measured in no-milk worlds the six
remaining cows sell milk at $2-14 (68/71 units under half base) while feed costs ~$40/day each.
o159 only abandons after all 8 shops are known and day >= 20; this fires once _O196_KNOWN shops
are known (day _O196_DAY) with zero shops for the product and spot price <= _O196_PRICE. Every
FEED on such a tile becomes PASS (animal escapes after two unfed nights; structure remains).
GOOSE never (egg price never collapses). Telemetry o196_skips/o196_tiles/o196_errors.
"""
import copy as _o196_copy

_O196_PARENT = agent
_O196_STATE = {}
_O196_REPORT = {}
_O196_KNOWN = 5      # shops known -> day 15
_O196_DAY = 15
_O196_PRICE = 8
_O196_SHOPS = {'COW': ('PIZZA_SHOP', 'SMOOTHIE_SHOP', 'ICE_CREAM_SHOP'), 'SHEEP': ('YARN_STORE',)}
_O196_PRODUCT = {'COW': 'MILK', 'SHEEP': 'WOOL'}
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O196_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O196_STATE[seat] = {'last': -1, 'skips': 0, 'tiles': set(), 'errors': 0}
    st['last'] = step
    parent_action = _O196_PARENT(observation, configuration)
    result = parent_action
    try:
        day = step // 24
        shops = list(observation['town'].get('unlocked_shops', []))
        if day >= _O196_DAY and len(shops) >= _O196_KNOWN and day < 29:
            prices = observation['market']['prices']
            dead = {k for k, ss in _O196_SHOPS.items() if not any(s in shops for s in ss) and prices.get(_O196_PRODUCT[k], 0) <= _O196_PRICE}
            if dead:
                farm = observation['farms'][seat]
                positions = [farm['farmer'], *farm['hands']]
                cmds = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
                out = None
                for i, c in enumerate(cmds[:len(positions)]):
                    if c != ['FEED']:
                        continue
                    x, y = positions[i]
                    tile = farm['tiles'][y][x]
                    if isinstance(tile, dict) and tile.get('animal') in dead:
                        out = out or _o196_copy.deepcopy(parent_action)
                        if i == 0:
                            out['farmer'] = ['PASS']
                        else:
                            out['hands'][i - 1] = ['PASS']
                        st['skips'] += 1; st['tiles'].add((x, y))
                if out is not None:
                    result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O196_REPORT.clear()
    _O196_REPORT.update(getattr(_O196_PARENT, 'telemetry', {}))
    _O196_REPORT.update({'o196_skips': st['skips'], 'o196_tiles': len(st['tiles']), 'o196_errors': st['errors']})
    return result


agent.telemetry = _O196_REPORT
agent = globals().pop('agent')
