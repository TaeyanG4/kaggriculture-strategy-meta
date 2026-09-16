# o226_adaptive_supply (Claude/o-series, 2026-09-16). Rival-adaptive sale throttle for the o224 stack.
# Market price is a function of inventory vs target T; units beyond T earn ~nothing. Against a dumping mirror the
# equilibrium is to dump too (unilateral restraint gifts the rival: o179), but against a restraining rival (top cluster
# style: small batches, buffers) our dumping craters our own prices (+6..17k available: restrainer proxy tests).
# Rule: estimate the rival's sold units per product each step from market inventory deltas (minus town consumption
# and our own exact sales); if over the last 48 steps the rival sold < 40% of what we sold (>= 12 units of evidence),
# cap each of our SELL orders to the remaining headroom to T (min 2 units), keeping the rest in the shed for later
# steps. Never throttle: WHEAT, products the rival sold in the last 8 steps, price <= 1, shed stock >= 30 of the item
# or total shed >= 85 (overflow guard), steps < 216 or >= 696 (terminal liquidation). Telemetry o226_*.
_O226_PARENT = agent
_O226_T = {'CARROT': 450, 'TOMATO': 200, 'STRAWBERRY': 100, 'MELON': 300, 'EGG': 332, 'MILK': 122, 'WOOL': 105, 'FERTILIZER': 200}
_O226_SHOPS = {'BAKERY': ('EGG', 'WHEAT'), 'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'), 'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'), 'YARN_STORE': ('WOOL',),
               'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'), 'PET_CAFE': ('CARROT',), 'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'), 'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY')}
_O226_I0 = 10000
_O226_WINDOW = 48
_O226_STATE = {}
_O226_REPORT = {}
del agent


def _o226_consumption(step, shops):
    out = {}
    if step % 4 == 0:
        for shop in shops:
            items = _O226_SHOPS.get(shop, ())
            for item in items:
                out[item] = out.get(item, 0) + (2 if len(items) == 1 else 1)
    if step % 24 == 0:
        for item in _O226_T:
            out[item] = out.get(item, 0) + 1
    return out


def _o226_update(observation, st):
    """Book the rival's sales at the previous step from public inventory, our exact sales and town consumption."""
    step = int(observation['step'])
    prev = st.get('prev')
    shed = observation['private']['shed']; inv = observation['market']['inventory']
    if prev is not None and step == prev['step'] + 1:
        cons = _o226_consumption(prev['step'], prev['shops'])
        for item in _O226_T:
            if prev['prices'].get(item, 0) <= 1:
                continue
            ours = max(0, int(prev['shed'].get(item, 0) + prev['placed'].get(item, 0) - shed.get(item, 0)))
            rival = max(0, int(inv[item]) - int(prev['inv'][item]) + cons.get(item, 0) - ours)
            st['log'].append((prev['step'], item, ours, rival))
            if rival > 0:
                st['rival_last'][item] = prev['step']
        st['log'] = [x for x in st['log'] if x[0] >= step - _O226_WINDOW]
    st['prev'] = None   # filled after the parent acts (needs our PLACE quantities)


def _o226_snapshot(observation, action, st):
    placed = {}
    for cmd in [action.get('farmer')] + (action.get('hands') or []):
        if cmd and len(cmd) >= 3 and cmd[0] == 'PLACE' and cmd[1] in _O226_T:
            placed[cmd[1]] = placed.get(cmd[1], 0) + int(cmd[2])
    st['prev'] = dict(step=int(observation['step']), shed=dict(observation['private']['shed']), inv=dict(observation['market']['inventory']),
                      prices=dict(observation['market']['prices']), shops=list(observation['town'].get('unlocked_shops', [])), placed=placed)


def _o226_restrain(st):
    ours = sum(x[2] for x in st['log']); rival = sum(x[3] for x in st['log'])
    return ours >= 12 and rival < 0.4 * ours


def _o226_throttle(observation, action, st):
    step = int(observation['step'])
    if not (216 <= step < 696) or not _o226_restrain(st):
        return action
    shed = observation['private']['shed']; inv = observation['market']['inventory']; prices = observation['market']['prices']
    total = sum(int(v) for v in shed.values())
    out = []; changed = False
    for o in action.get('market') or []:
        if o and o[0] == 'SELL' and o[1] in _O226_T and len(o) >= 3:
            item = o[1]; qty = int(o[2])
            if (prices.get(item, 0) <= 1 or int(shed.get(item, 0)) >= 30 or total >= 85
                    or step - st['rival_last'].get(item, -999) <= 8):
                out.append(o); continue
            cap = max(2, _O226_T[item] - (int(inv[item]) - _O226_I0))
            if qty > cap:
                o = [o[0], item, int(cap)]; changed = True
                _O226_REPORT['o226_capped_orders'] = _O226_REPORT.get('o226_capped_orders', 0) + 1
                _O226_REPORT['o226_held_units'] = _O226_REPORT.get('o226_held_units', 0) + (qty - cap)
        out.append(o)
    if not changed:
        return action
    action = dict(action); action['market'] = out
    return action


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    st = _O226_STATE.get(seat)
    if st is None or step <= st['step']:
        st = _O226_STATE[seat] = {'step': -1, 'prev': None, 'log': [], 'rival_last': {}, 'restrain_turns': 0}
        _O226_REPORT.update(o226_capped_orders=0, o226_held_units=0, o226_restrain_turns=0, o226_errors=0)
    st['step'] = step
    try:
        _o226_update(observation, st)
    except Exception:
        _O226_REPORT['o226_errors'] = _O226_REPORT.get('o226_errors', 0) + 1
    action = _O226_PARENT(observation, configuration)
    try:
        if 216 <= step < 696 and _o226_restrain(st):
            st['restrain_turns'] += 1
        action = _o226_throttle(observation, action, st)
        _o226_snapshot(observation, action, st)
    except Exception:
        _O226_REPORT['o226_errors'] = _O226_REPORT.get('o226_errors', 0) + 1
    _O226_REPORT.update(getattr(_O226_PARENT, 'telemetry', {}))
    _O226_REPORT['o226_restrain_turns'] = st['restrain_turns']
    return action


agent.telemetry = _O226_REPORT
agent = globals().pop('agent')
