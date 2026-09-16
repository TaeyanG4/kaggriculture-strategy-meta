# o214_tomato_planner (Claude/o-series, 2026-09-15). Overlay for the o199c stack. Macro-planner candidate A.
"""TOMATO commit-size planner on top of V219 (day-18 tomato program on the SE quadrant).
V219 commits 10 tiles only when >= 3 tomato shops are known; in 1-2 shop worlds it does nothing, and
live losses (ymg_aq, PIZZA x2: tomato -16k) show that is too coarse. This layer re-decides the SIZE at
V219's own decision step (432) from the observed state and reuses V219's verified worker/sale path:
  KEEP   = V219 as is (10 tiles iff >= 3 shops)
  SMALL  = if V219 would not commit and tomato demand >= 1: commit 3 tiles
  MEDIUM = same with 5 tiles
State key (telemetry o214_key): tomato shops known | TOMATO price bucket | cash bucket | wheat reserve ok.
Force: env KAGG_FORCE_TOMATO=KEEP|SMALL|MEDIUM (compiler); table lookup otherwise; unknown key -> KEEP.
Mechanics: _v219_qualifies is wrapped (gate relaxed only for the chosen size), V219's state['targets']
is shrunk to the first N tiles before roles are created, and the BUY_SEED TOMATO 10 order is cut to N.
No future shops are assumed. Telemetry: o214_key, o214_action, o214_fired, o214_size, o214_errors.
"""
import copy as _o214_copy
import os as _o214_os

_O214_PARENT = agent
_O214_STATE = {}
_O214_REPORT = {}
_O214_FORCE = _o214_os.environ.get('KAGG_FORCE_TOMATO', '')
_O214_TABLE = {}   # key -> action, compiled by o_tools/macro_compile.py
_O214_SIZE = {'SMALL': 3, 'MEDIUM': 5}
_O214_MIN_CASH = 8000
_O214_TILES = [(x, y) for y in (5, 6) for x in range(5, 10)]
_o214_orig_qualifies = _v219_qualifies
del agent


def _v219_qualifies(obs, native):
    """V219 calls this by global name at step 432: pass the gate only for a seat whose planner chose a size."""
    st = _O214_STATE.get(int(obs['player']))
    if st and st.get('size') and st.get('gate_step') == int(obs['step']):
        return True
    return _o214_orig_qualifies(obs, native)


def _o214_key(observation, seat):
    shops = observation['town'].get('unlocked_shops', []) or []
    demand = sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in shops)
    p = observation['market']['prices']['TOMATO']; cash = observation['farms'][seat]['money']
    shed_wheat = observation['private']['shed'].get('WHEAT', 0)
    animals = sum(1 for row in observation['farms'][seat]['tiles'] for t in row if isinstance(t, dict) and t.get('animal'))
    pb = 'p<70' if p < 70 else ('p70-120' if p < 120 else 'p>120')
    cb = 'c<12k' if cash < 12000 else ('c12-20k' if cash < 20000 else 'c>20k')
    wb = 'w+' if shed_wheat >= 2 * animals else 'w-'
    return f'tom{min(demand, 3)}|{pb}|{cb}|{wb}'


def _o214_decide(observation, seat, native):
    """Return (action, size). KEEP means leave V219 alone."""
    if _O214_FORCE in ('KEEP', 'SMALL', 'MEDIUM'):
        act = _O214_FORCE
    else:
        act = _O214_TABLE.get(_o214_key(observation, seat), 'KEEP')
    if act == 'KEEP' or _o214_orig_qualifies(observation, native):
        return 'KEEP', 0
    shops = observation['town'].get('unlocked_shops', []) or []
    demand = sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in shops)
    farm = observation['farms'][seat]
    if demand < 1 or farm['money'] < _O214_MIN_CASH or 'SE' in farm['unlocked_quadrants']:
        return 'KEEP', 0
    # the rest of V219's own preconditions, with the shop/money tests relaxed
    padded = dict(observation); padded['town'] = dict(observation['town'], unlocked_shops=list(shops) + ['PIZZA_SHOP'] * 3)
    padded['farms'] = list(observation['farms']); f2 = dict(farm); f2['money'] = max(farm['money'], 12000); padded['farms'][seat] = f2
    if not _o214_orig_qualifies(padded, native):
        return 'KEEP', 0
    return act, _O214_SIZE[act]


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O214_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O214_STATE[seat] = {'last': -1, 'key': '', 'action': '', 'fired': 0, 'size': 0, 'errors': 0, 'gate_step': -1}
    st['last'] = step
    if step == 432:
        try:
            native = _IMPL.chassis.players[seat]
            st['key'] = _o214_key(observation, seat)
            act, size = _o214_decide(observation, seat, native)
            st['action'] = act; st['size'] = size
            if size:
                st['gate_step'] = step   # the wrapped gate above passes for this seat at this step only
                vs = _V219_STATES.get(seat)
                if vs is None or vs.get('last_step', -1) < step:
                    vs = {'last_step': step - 1, 'day': -1, 'workers': {}, 'last_work': {}, 'seen_plants': set(), 'lost': set(), 'targets': list(_O214_TILES)}
                    _V219_STATES[seat] = vs
                vs['targets'] = list(_O214_TILES[:size]); vs['last_step'] = step - 1   # let V219 re-enter its own step-432 path
                st['fired'] = 1
        except Exception:
            st['errors'] += 1
    result = _O214_PARENT(observation, configuration)
    try:
        if st['size'] and 432 <= step <= 440:
            orders = result.get('market') or []
            for i, o in enumerate(orders):
                if o and o[:2] == ['BUY_SEED', 'TOMATO'] and int(o[2]) > st['size']:
                    result = _o214_copy.deepcopy(result); result['market'][i] = ['BUY_SEED', 'TOMATO', st['size']]
                    break
    except Exception:
        st['errors'] += 1
    _O214_REPORT.clear()
    _O214_REPORT.update(getattr(_O214_PARENT, 'telemetry', {}))
    _O214_REPORT.update({'o214_' + k: v for k, v in st.items() if k not in ('last', 'gate_step')})
    return result


agent.telemetry = _O214_REPORT
agent = globals().pop('agent')
