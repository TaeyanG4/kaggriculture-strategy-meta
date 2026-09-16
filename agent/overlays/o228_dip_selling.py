# o228_dip_selling (Claude/o-series, 2026-09-16). Sell-into-shortage tail holding for the o227 stack.
# Majkel (#2) keeps small shed buffers (milk ~6, strawberry ~11, wool ~7) and sells when market inventory is low; at
# our SELL steps the market sits above the price target T, so the tail of every batch earns near-floor prices. Rule:
# when we sell product X and the market inventory offset (inv - I0) exceeds T, cap the sale to the headroom (min 2
# units) and hold the tail in the shed; release held units when the inventory dips to <= 0.5*T (a shop-consumption
# dip), or after 24 steps, or when the shed is >= 80 units, or from step 672 (terminal). Never inject a sale on a turn
# where we PLACE a race product (keeps o227's stealth) and never touch WHEAT. Telemetry o228_*.
_O228_PARENT = agent
_O228_T = {'CARROT': 450, 'TOMATO': 200, 'STRAWBERRY': 100, 'MELON': 300, 'EGG': 332, 'MILK': 122, 'WOOL': 105, 'FERTILIZER': 200}
_O228_I0 = 10000
_O228_DEADLINE = 24
_O228_DIP = 0.5
_O228_STATE = {}
_O228_REPORT = {}
del agent


def _o228_apply(observation, action, st):
    step = int(observation['step'])
    shed = observation['private']['shed']; inv = observation['market']['inventory']; prices = observation['market']['prices']
    total = sum(int(v) for v in shed.values())
    cmds = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    drop = {c[1] for c in cmds if len(c) >= 2 and c[0] == 'PLACE'}
    market = list(action.get('market') or [])
    selling = {o[1] for o in market if o and o[0] == 'SELL'}
    terminal = step >= 672 or total >= 80
    out = []; changed = False
    for o in market:
        if o and o[0] == 'SELL' and o[1] in _O228_T and len(o) >= 3 and not terminal:
            item = o[1]; qty = int(o[2]); off = int(inv[item]) - _O228_I0
            avail = int(shed.get(item, 0))
            if prices.get(item, 0) > 1 and off > _O228_T[item] and avail > 2:
                cap = max(2, _O228_T[item] - off)
                if qty > cap:
                    held = min(avail, qty) - cap
                    if held > 0:
                        h = st['held'].setdefault(item, [0, step]); h[0] += held; h[1] = min(h[1], step) if h[0] > held else step
                        o = [o[0], item, int(cap)]; changed = True
                        _O228_REPORT['o228_capped'] = _O228_REPORT.get('o228_capped', 0) + 1
                        _O228_REPORT['o228_held_units'] = _O228_REPORT.get('o228_held_units', 0) + held
        out.append(o)
    # release held units into dips / at deadline / terminal
    for item, (units, since) in list(st['held'].items()):
        stock = int(shed.get(item, 0))
        units = min(units, stock)
        if units <= 0:
            st['held'].pop(item, None); continue
        if item in selling or item in drop or len(out) >= 10:
            continue
        off = int(inv[item]) - _O228_I0
        dip = off <= _O228_DIP * _O228_T[item]
        if terminal or dip or step - since >= _O228_DEADLINE:
            q = units if (terminal or step - since >= _O228_DEADLINE) else max(1, min(units, _O228_T[item] - off))
            out.append(['SELL', item, int(q)]); changed = True
            st['held'].pop(item, None)
            if units - q > 0:
                st['held'][item] = [units - q, since]
            key = 'o228_released_dip' if dip and not terminal else 'o228_released_deadline'
            _O228_REPORT[key] = _O228_REPORT.get(key, 0) + q
    if not changed:
        return action
    action = dict(action); action['market'] = out
    return action


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    st = _O228_STATE.get(seat)
    if st is None or step <= st['step']:
        st = _O228_STATE[seat] = {'step': -1, 'held': {}}
        _O228_REPORT.update(o228_capped=0, o228_held_units=0, o228_released_dip=0, o228_released_deadline=0, o228_errors=0)
    st['step'] = step
    action = _O228_PARENT(observation, configuration)
    try:
        if 216 <= step < 696:
            action = _o228_apply(observation, action, st)
    except Exception:
        _O228_REPORT['o228_errors'] = _O228_REPORT.get('o228_errors', 0) + 1
    _O228_REPORT.update(getattr(_O228_PARENT, 'telemetry', {}))
    return action


agent.telemetry = _O228_REPORT
agent = globals().pop('agent')
