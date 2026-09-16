# o185b_yarn_day10_geese_noegg (Claude/o-series, 2026-09-15). Overlay for o181.
"""Yarn routes (YARN_STORE in the first two shops) buy a 3-SHEEP block on days 10-11 (steps 241-270,
pastures built 254-259). When the known shops show only that one YARN_STORE (yarn among first
_O185_KNOWN shops == 1) and an egg shop is present, the block becomes GOOSE: BUY/PICKUP/PLACE renamed
and BUILD_PASTURE -> BUILD_COOP inside the window. PICKUP/PLACE are renamed only when the shed /
worker actually holds a GOOSE. Variant _O185_NEED_EGG_SHOP. Telemetry o185_mode/o185_rewrites/o185_errors.
"""
import copy as _o185_copy

_O185_PARENT = agent
_O185_STATE = {}
_O185_REPORT = {}
_O185_WINDOW = (241, 275)
_O185_KNOWN = 3
_O185_NEED_EGG_SHOP = False
_O185_EGG = ('BAKERY', 'BRUNCH_SPOT')
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O185_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O185_STATE[seat] = {'last': -1, 'mode': '', 'rewrites': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O185_PARENT(observation, configuration)
    result = parent_action
    try:
        if step == _O185_WINDOW[0]:
            shops = list(observation['town'].get('unlocked_shops', []))
            orders = parent_action.get('market') or []
            if ('YARN_STORE' in shops[:2] and shops[:_O185_KNOWN].count('YARN_STORE') == 1
                    and (not _O185_NEED_EGG_SHOP or any(s in _O185_EGG for s in shops))
                    and any(o and o[0] == 'BUY_ANIMAL' and o[1] == 'SHEEP' for o in orders)):
                st['mode'] = 'GOOSE'
        if st['mode'] and _O185_WINDOW[0] <= step < _O185_WINDOW[1]:
            out = None
            for o in parent_action.get('market') or []:
                if o and o[0] == 'BUY_ANIMAL' and o[1] == 'SHEEP':
                    out = out or _o185_copy.deepcopy(parent_action)
                    for oo in out['market']:
                        if oo and oo[0] == 'BUY_ANIMAL' and oo[1] == 'SHEEP':
                            oo[1] = 'GOOSE'; st['rewrites'] += 1
                    break
            shed = observation['private']['shed']; invs = observation['private']['inventories']
            cmds = [parent_action.get('farmer')] + list(parent_action.get('hands') or [])
            for i, c in enumerate(cmds):
                if not c:
                    continue
                new = None
                if c[0] == 'BUILD_PASTURE':
                    new = ['BUILD_COOP']
                elif c[0] == 'PICKUP' and len(c) > 1 and c[1] == 'SHEEP' and int(shed.get('GOOSE', 0)) > 0 and int(shed.get('SHEEP', 0)) == 0:
                    new = ['PICKUP', 'GOOSE'] + list(c[2:])
                elif c[0] == 'PLACE' and len(c) > 1 and c[1] == 'SHEEP':
                    inv = invs[i] if i < len(invs) else {}
                    if int(inv.get('GOOSE', 0)) > 0 and int(inv.get('SHEEP', 0)) == 0:
                        new = ['PLACE', 'GOOSE']
                if new is not None:
                    out = out or _o185_copy.deepcopy(parent_action)
                    if i == 0:
                        out['farmer'] = new
                    else:
                        out['hands'][i - 1] = new
                    st['rewrites'] += 1
            if out is not None:
                result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O185_REPORT.clear()
    _O185_REPORT.update(getattr(_O185_PARENT, 'telemetry', {}))
    _O185_REPORT.update({'o185_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O185_REPORT
agent = globals().pop('agent')
