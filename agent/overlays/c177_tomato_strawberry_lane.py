# SPDX-License-Identifier: Apache-2.0
# c177 (GPT/Codex, 2026-09-15): tomato substitution on o199c's native strawberry lane.
"""Use an already-funded ongoing-crop lane instead of adding land/labor.

The parent already buys, plants, waters, fertilizes, harvests and carries a final
day-11 STRAWBERRY tranche.  c177 may change only a bounded number of units in
that tranche to TOMATO, preserving the same worker geometry and later field
commands.  Unlike c176 it adds no HIRE, BUY_LAND or WHEAT replacement program.

KAGG_C177_FORCE=KEEP|TOMATO and KAGG_C177_SIZE=1..13 are local-screen hooks.
Force bypasses the economic gate only; it still waits for the certified native
strawberry seed/plant lane.
"""

import copy as _c177_copy
import os as _c177_os

_C177_PARENT = agent
_C177_STATES = {}
_C177_REPORT = {}
_C177_FORCE = (_c177_os.environ.get('KAGG_C177_FORCE', '') or '').strip().upper()
try:
    _C177_SIZE_OVERRIDE = int(_c177_os.environ.get('KAGG_C177_SIZE', '0') or 0)
except Exception:
    _C177_SIZE_OVERRIDE = 0

_C177_DECISION_START = 11 * 24
_C177_DECISION_END = 12 * 24
_C177_MAX_TRANCHE = 13
_C177_MIN_PRICE = 60
_C177_CASH_RESERVE = 2500

del agent


def _c177_new_state():
    return {
        'last': -1,
        'mode': None,
        'target': 0,
        'seed_units': 0,
        'plant_units': 0,
        'sites': set(),
        'pending': [],
        'counts': {
            'decisions': 0,
            'activations': 0,
            'seed_units_rewritten': 0,
            'plant_requests_rewritten': 0,
            'plants_confirmed': 0,
            'plant_failures': 0,
            'deposit_rewrites': 0,
            'sale_turns': 0,
            'sale_units': 0,
            'full_queue_declines': 0,
            'cash_declines': 0,
            'errors': 0,
        },
    }


def _c177_standard(configuration):
    return configuration is None or all(configuration.get(key, value) == value for key, value in (
        ('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100),
        ('maxMarketOrdersPerTurn', 10), ('farmHandCostMult', 1),
    ))


def _c177_tomato_demand(observation):
    shops = observation.get('town', {}).get('unlocked_shops', []) or []
    return sum(shop in ('PIZZA_SHOP', 'FARMERS_MARKET') for shop in shops)


def _c177_has_strawberry_seed(action):
    return any(len(order) >= 3 and order[:2] == ['BUY_SEED', 'STRAWBERRY']
               and int(order[2]) > 0 for order in (action.get('market') or []))


def _c177_decide(observation, action, state):
    if state['mode'] is not None:
        return
    step = int(observation['step'])
    if not (_C177_DECISION_START <= step < _C177_DECISION_END) or not _c177_has_strawberry_seed(action):
        return
    state['counts']['decisions'] += 1
    demand = _c177_tomato_demand(observation)
    price = int(observation['market']['prices'].get('TOMATO', 0))
    farm = observation['farms'][int(observation['player'])]
    forced = _C177_FORCE == 'TOMATO'
    if _C177_FORCE == 'KEEP':
        state['mode'] = 'KEEP'
        return
    if not forced and (demand < 2 or price < _C177_MIN_PRICE):
        state['mode'] = 'KEEP'
        return
    if float(farm.get('money', 0)) < _C177_CASH_RESERVE:
        state['counts']['cash_declines'] += 1
        state['mode'] = 'KEEP'
        return
    if 1 <= _C177_SIZE_OVERRIDE <= _C177_MAX_TRANCHE:
        target = _C177_SIZE_OVERRIDE
    else:
        target = 10 if demand >= 3 else (8 if demand >= 2 else 4)
    state['mode'] = 'TOMATO'
    state['target'] = target
    state['counts']['activations'] += 1


def _c177_rewrite_seed_orders(action, state):
    remaining = state['target'] - state['seed_units']
    if remaining <= 0:
        return action
    market = action.get('market') or []
    changed = _c177_copy.deepcopy(action)
    rewritten = []
    used = 0
    for order in changed.get('market', []):
        if not (len(order) >= 3 and order[:2] == ['BUY_SEED', 'STRAWBERRY']):
            rewritten.append(order)
            continue
        quantity = max(0, int(order[2]))
        take = min(quantity, remaining - used)
        if take <= 0:
            rewritten.append(order)
            continue
        leftover = quantity - take
        # Route 12 has a single 23-unit order in a full queue: only the known
        # 13-unit complete tranche can be safely compacted (10 units are surplus).
        if leftover and len(market) >= 10:
            if not (state['seed_units'] == 0 and quantity == 23 and take == 13):
                state['counts']['full_queue_declines'] += 1
                return action
            leftover = 0
        rewritten.append(['BUY_SEED', 'TOMATO', take])
        if leftover:
            rewritten.append(['BUY_SEED', 'STRAWBERRY', leftover])
        used += take
    if used <= 0 or len(rewritten) > 10:
        return action
    changed['market'] = rewritten
    state['seed_units'] += used
    state['counts']['seed_units_rewritten'] += used
    return changed


def _c177_confirm(observation, state):
    step = int(observation['step'])
    if not state['pending']:
        return
    farm = observation['farms'][int(observation['player'])]
    keep = []
    for request in state['pending']:
        if request['step'] >= step:
            keep.append(request)
            continue
        x, y = request['xy']
        tile = farm['tiles'][y][x]
        if (isinstance(tile, dict) and tile.get('crop') == 'TOMATO'
                and int(tile.get('planted_day', -1)) == request['step'] // 24):
            state['counts']['plants_confirmed'] += 1
        else:
            state['sites'].discard((x, y))
            state['counts']['plant_failures'] += 1
    state['pending'] = keep


def _c177_rewrite_field(observation, action, state):
    if state['plant_units'] >= state['target']:
        # Deposits may still need rewriting after all plants were created.
        remaining_plants = False
    else:
        remaining_plants = True
    result = _c177_copy.deepcopy(action)
    commands = [result.get('farmer') or ['PASS'], *(result.get('hands') or [])]
    farm = observation['farms'][int(observation['player'])]
    positions = [farm.get('farmer'), *farm.get('hands', [])]
    inventories = observation.get('private', {}).get('inventories', [])
    seeds = max(0, int(observation.get('private', {}).get('seeds', {}).get('TOMATO', 0)))
    changed = False
    position_counts = {}
    for pos in positions:
        key = tuple(pos)
        position_counts[key] = position_counts.get(key, 0) + 1
    for actor in range(min(len(commands), len(positions))):
        command = commands[actor]
        pos = tuple(positions[actor])
        x, y = pos
        if (remaining_plants and seeds > 0 and state['plant_units'] < state['target']
                and command == ['PLANT', 'STRAWBERRY']
                and position_counts.get(pos) == 1 and farm['tiles'][y][x] is None):
            commands[actor] = ['PLANT', 'TOMATO']
            state['sites'].add(pos)
            state['pending'].append({'step': int(observation['step']), 'xy': pos})
            state['plant_units'] += 1
            state['counts']['plant_requests_rewritten'] += 1
            seeds -= 1
            changed = True
        elif (len(command) >= 2 and command[:2] == ['PLACE', 'STRAWBERRY']
              and actor < len(inventories)):
            inv = inventories[actor] or {}
            if int(inv.get('STRAWBERRY', 0)) <= 0 and int(inv.get('TOMATO', 0)) > 0:
                commands[actor] = ['PLACE', 'TOMATO', int(inv.get('TOMATO', 0))]
                state['counts']['deposit_rewrites'] += 1
                changed = True
    if not changed:
        return action
    result['farmer'], result['hands'] = commands[0], commands[1:]
    return result


def _c177_add_sale(observation, action, state):
    step = int(observation['step'])
    if step < 19 * 24 or step % 4 != 1:
        return action
    market = action.get('market') or []
    if len(market) >= 10 or any(len(order) >= 3 and order[:2] == ['SELL', 'TOMATO'] for order in market):
        return action
    price = int(observation['market']['prices'].get('TOMATO', 0))
    if price < _C177_MIN_PRICE:
        return action
    stock = max(0, int(projected_shed(action, FarmView(observation)).get('TOMATO', 0)))
    if stock <= 0:
        return action
    # One shop consumes one unit per shop tick.  Match visible absorption rather
    # than dumping the whole shed into a hinge market.
    quantity = min(stock, max(1, min(4, _c177_tomato_demand(observation))))
    result = _c177_copy.deepcopy(action)
    result['market'] = list(result.get('market') or []) + [['SELL', 'TOMATO', quantity]]
    try:
        result = _v224_sales_first(result)
        result = _r37_reorder_sales(observation, result)
    except Exception:
        pass
    state['counts']['sale_turns'] += 1
    state['counts']['sale_units'] += quantity
    return result


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    state = _C177_STATES.get(seat)
    if state is None or step <= state.get('last', -1):
        state = _C177_STATES[seat] = _c177_new_state()
    state['last'] = step
    _c177_confirm(observation, state)
    parent = _C177_PARENT(observation, configuration)
    result = parent
    try:
        if _c177_standard(configuration):
            _c177_decide(observation, parent, state)
            if state.get('mode') == 'TOMATO':
                result = _c177_rewrite_seed_orders(result, state)
                result = _c177_rewrite_field(observation, result, state)
                result = _c177_add_sale(observation, result, state)
    except Exception:
        state['counts']['errors'] += 1
        result = parent
    _C177_REPORT.clear()
    _C177_REPORT.update(getattr(_C177_PARENT, 'telemetry', {}))
    _C177_REPORT.update({'c177_' + key: value for key, value in state['counts'].items()})
    _C177_REPORT.update({
        'c177_mode': state.get('mode') or 'UNDECIDED',
        'c177_target': int(state.get('target', 0)),
        'c177_sites': len(state.get('sites', ())),
    })
    return result


agent.telemetry = _C177_REPORT
agent = globals().pop('agent')
