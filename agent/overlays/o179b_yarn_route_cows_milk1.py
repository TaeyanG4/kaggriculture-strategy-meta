# o179b_yarn_route_cows milk>=1 (Claude/o-series, 2026-09-15). Overlay on o162.
"""Late SHEEP purchases -> COW on the sheep-heavy yarn routes when milk demand shows up.
Yarn routes (YARN_STORE among the first two shops) buy 5-6 more SHEEP on days 9-11 regardless of
later shops; the two worst elite losses are (YARN, SMOOTHIE) worlds that end with 5-6 milk shops.
From step _O179_FROM (3 shops known) if milk shops among known shops >= _O179_MILK_MIN, every later
BUY_ANIMAL SHEEP becomes COW (same PASTURE structure, cheaper). PICKUP/PLACE are renamed only when
the shed / worker actually holds a COW, so sheep already bought are still placed.
Telemetry: o179_mode, o179_buys, o179_renames, o179_errors.
"""
import copy as _o179_copy

_O179_PARENT = agent
_O179_STATE = {}
_O179_REPORT = {}
_O179_FROM = 216
_O179_TO = 300
_O179_MILK_MIN = 1
_O179_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O179_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O179_STATE[seat] = {'last': -1, 'mode': '', 'buys': 0, 'renames': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O179_PARENT(observation, configuration)
    result = parent_action
    try:
        shops = list(observation['town'].get('unlocked_shops', []))
        if step == _O179_FROM and 'YARN_STORE' in shops[:2] and sum(s in _O179_MILK for s in shops) >= _O179_MILK_MIN:
            st['mode'] = 'COW'
        if st['mode'] and _O179_FROM <= step < _O179_TO:
            out = None
            for o in parent_action.get('market') or []:
                if o and o[0] == 'BUY_ANIMAL' and o[1] == 'SHEEP':
                    out = out or _o179_copy.deepcopy(parent_action)
                    for oo in out['market']:
                        if oo and oo[0] == 'BUY_ANIMAL' and oo[1] == 'SHEEP':
                            oo[1] = 'COW'; st['buys'] += int(oo[2])
                    break
            shed = observation['private']['shed']
            invs = observation['private']['inventories']
            cmds = [parent_action.get('farmer')] + list(parent_action.get('hands') or [])
            for i, c in enumerate(cmds):
                if not c or len(c) < 2 or c[1] != 'SHEEP' or c[0] not in ('PICKUP', 'PLACE'):
                    continue
                if c[0] == 'PICKUP':
                    ok = int(shed.get('COW', 0)) > 0 and int(shed.get('SHEEP', 0)) == 0
                else:
                    inv = invs[i] if i < len(invs) else {}
                    ok = int(inv.get('COW', 0)) > 0 and int(inv.get('SHEEP', 0)) == 0
                if ok:
                    out = out or _o179_copy.deepcopy(parent_action)
                    new = [c[0], 'COW'] + list(c[2:])
                    if i == 0:
                        out['farmer'] = new
                    else:
                        out['hands'][i - 1] = new
                    st['renames'] += 1
            if out is not None:
                result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O179_REPORT.clear()
    _O179_REPORT.update(getattr(_O179_PARENT, 'telemetry', {}))
    _O179_REPORT.update({'o179_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O179_REPORT
agent = globals().pop('agent')
