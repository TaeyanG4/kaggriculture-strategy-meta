# SPDX-License-Identifier: Apache-2.0
# c176 (GPT/Codex, 2026-09-15): structural tomato-tail regime for frozen o199c.
"""Replace a bounded part of o199c's late WHEAT cycle with a coherent TOMATO tail.

This is intentionally different from o214.  o214 changed V219's commit size while
keeping V219's $4,000 southeast-land investment.  c176 never buys land.  Instead,
at the day-18 macro boundary it may enter one committed regime:

  * buy the tomato seed pool up front;
  * replace up to 8/10 *actual* WHEAT planting requests on already-unlocked empty
    tiles during days 18-20 with TOMATO;
  * hire dedicated observed workers to water/harvest/deliver those exact plants;
  * keep a short-horizon WHEAT reserve for the parent's already-known pickup/feed
    obligations after the crop substitution;
  * sell only physically projected TOMATO stock, then re-apply the parent's sale
    ordering helpers.

The parent remains the execution fallback.  No opponent identity, replay id, seed,
future shop, hidden inventory, new land, livestock substitution, or opening action
is used.  AUTO activates only with >=2 currently-open tomato-demand shops and a
non-hot carrot regime.  KAGG_C176_FORCE=KEEP|REALLOC is provided for paired local
screens; KAGG_C176_SIZE=1..10 can isolate commit size.  Force mode bypasses only
the economic AUTO gate, never the physical/cash/land safety checks.

This file is an unvalidated research overlay.  It does not promote or submit the
candidate and is designed to be screened against the immutable o199c parent.
"""

import copy as _c176_copy
import os as _c176_os


_C176_PARENT = agent
_C176_ORIGINAL_V219_QUALIFIES = _v219_qualifies
_C176_STATES = {}
_C176_REPORT = {}
_C176_FORCE = (_c176_os.environ.get('KAGG_C176_FORCE', '') or '').strip().upper()
try:
    _C176_SIZE_OVERRIDE = int(_c176_os.environ.get('KAGG_C176_SIZE', '0') or 0)
except Exception:
    _C176_SIZE_OVERRIDE = 0

_C176_MIN_CASH = 7000
_C176_CASH_RESERVE = 3000
_C176_MIN_TOMATO_PRICE = 70
_C176_FIRST_DAY = 18
_C176_LAST_PLANT_DAY = 20
_C176_LAST_SERVICE_DAY = 29
_C176_WHEAT_LOOKAHEAD = 48
_C176_MAX_WHEAT_TOPUP = 12

del agent


def _c176_standard(configuration):
    return configuration is None or all(configuration.get(key, value) == value for key, value in (
        ('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100),
        ('maxMarketOrdersPerTurn', 10), ('farmHandCostMult', 1),
    ))


def _c176_new_state():
    return {
        'last': -1,
        'day': -1,
        'decided': False,
        'active': False,
        'regime': 'KEEP',
        'target_count': 0,
        'seed_ordered': False,
        'seed_order_step': -1,
        'targets': {},          # (x,y) -> {'birth', 'confirmed'}
        'pending_plants': {},   # (x,y) -> birth day
        'workers': [],          # actor ids hired for this day
        'pending_hires': None,
        'hire_day': -1,
        'wheat_topup_day': -1,
        'counts': {
            'decisions': 0,
            'activations': 0,
            'v219_suppressed': 0,
            'seed_orders': 0,
            'seed_units': 0,
            'plant_swaps': 0,
            'plants_confirmed': 0,
            'plant_failures': 0,
            'hire_requests': 0,
            'hires_confirmed': 0,
            'hire_shortfalls': 0,
            'hire_declines': 0,
            'water_requests': 0,
            'harvest_requests': 0,
            'drop_requests': 0,
            'wheat_topup_turns': 0,
            'wheat_topup_units': 0,
            'wheat_topup_declines': 0,
            'tomato_sale_turns': 0,
            'tomato_sale_units': 0,
            'lost_targets': 0,
            'errors': 0,
        },
    }


def _c176_tomato_demand(observation):
    shops = observation['town'].get('unlocked_shops', []) or []
    return sum(shop in ('PIZZA_SHOP', 'FARMERS_MARKET') for shop in shops)


def _c176_physical_gate(observation, state):
    """Physical/cash gate that force mode is not allowed to bypass."""
    seat = int(observation['player'])
    farm = observation['farms'][seat]
    if int(observation['step']) != _C176_FIRST_DAY * 24:
        return False
    if len(farm.get('tiles', [])) != 10:
        return False
    if set(farm.get('unlocked_quadrants', [])) != {'NW', 'NE', 'SW'}:
        return False
    if farm.get('money', 0) < _C176_MIN_CASH:
        return False
    # This regime deliberately replaces the SE V219 investment rather than
    # stacking on top of a pre-existing southeast commitment.
    if 'SE' in farm.get('unlocked_quadrants', []):
        return False
    if (_V219_STATES.get(seat) or {}).get('committed'):
        return False
    return True


def _c176_decide(observation, state):
    state['counts']['decisions'] += 1
    if not _c176_physical_gate(observation, state):
        return
    demand = _c176_tomato_demand(observation)
    prices = observation['market']['prices']
    carrot_hot = False
    try:
        carrot_hot = bool(_o199_hot(observation))
    except Exception:
        carrot_hot = False

    forced = _C176_FORCE == 'REALLOC'
    if _C176_FORCE == 'KEEP':
        return
    if not forced:
        if demand < 2 or int(prices.get('TOMATO', 0)) < _C176_MIN_TOMATO_PRICE or carrot_hot:
            return

    target = _C176_SIZE_OVERRIDE if 1 <= _C176_SIZE_OVERRIDE <= 10 else (10 if demand >= 3 else 8)
    state['active'] = True
    state['regime'] = 'REALLOC'
    state['target_count'] = target
    state['counts']['activations'] += 1


def _v219_qualifies(observation, native):
    """Suppress only V219's SE investment when c176 has committed at step 432."""
    seat = int(observation['player'])
    state = _C176_STATES.get(seat)
    if (state and state.get('active') and int(observation.get('step', -1)) == _C176_FIRST_DAY * 24):
        state['counts']['v219_suppressed'] += 1
        return False
    return _C176_ORIGINAL_V219_QUALIFIES(observation, native)


def _c176_set_command(action, actor, command):
    if actor == 0:
        action['farmer'] = list(command)
    else:
        hands = action.setdefault('hands', [])
        while len(hands) < actor:
            hands.append(['PASS'])
        hands[actor - 1] = list(command)


def _c176_confirm_plants(observation, state):
    if not state['pending_plants']:
        return
    farm = observation['farms'][int(observation['player'])]
    for xy, birth in list(state['pending_plants'].items()):
        x, y = xy
        tile = farm['tiles'][y][x]
        if (isinstance(tile, dict) and tile.get('crop') == 'TOMATO'
                and int(tile.get('planted_day', -1)) == int(birth)):
            meta = state['targets'].get(xy)
            if meta is not None:
                meta['confirmed'] = True
            state['counts']['plants_confirmed'] += 1
        else:
            state['targets'].pop(xy, None)
            state['counts']['plant_failures'] += 1
        state['pending_plants'].pop(xy, None)


def _c176_convert_plants(observation, action, state):
    step = int(observation['step']); day = step // 24
    if not (_C176_FIRST_DAY <= day <= _C176_LAST_PLANT_DAY):
        return action
    if len(state['targets']) >= state['target_count']:
        return action
    private = observation['private']
    available = max(0, int(private['seeds'].get('TOMATO', 0)))
    if available <= 0:
        return action
    farm = observation['farms'][int(observation['player'])]
    positions = [farm['farmer'], *farm['hands']]
    commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    result = None
    for actor, command in enumerate(commands[:len(positions)]):
        if len(state['targets']) >= state['target_count'] or available <= 0:
            break
        if command != ['PLANT', 'WHEAT']:
            continue
        x, y = map(int, positions[actor])
        if farm['tiles'][y][x] is not None or (x, y) in state['targets']:
            continue
        if result is None:
            result = _c176_copy.deepcopy(action)
        _c176_set_command(result, actor, ['PLANT', 'TOMATO'])
        state['targets'][(x, y)] = {'birth': day, 'confirmed': False}
        state['pending_plants'][(x, y)] = day
        state['counts']['plant_swaps'] += 1
        available -= 1
    return result if result is not None else action


def _c176_seed_pool(observation, action, state):
    if state['seed_ordered']:
        return action
    step = int(observation['step'])
    if not (_C176_FIRST_DAY * 24 <= step <= _C176_FIRST_DAY * 24 + 4):
        return action
    private = observation['private']; farm = observation['farms'][int(observation['player'])]
    have = max(0, int(private['seeds'].get('TOMATO', 0)))
    quantity = max(0, int(state['target_count']) - have)
    if quantity <= 0:
        state['seed_ordered'] = True
        return action
    orders = action.get('market') or []
    if len(orders) >= 10:
        return action
    seed_cost = quantity * 50
    if float(farm.get('money', 0)) < seed_cost + _C176_CASH_RESERVE:
        return action
    result = _c176_copy.deepcopy(action)
    result['market'] = list(result.get('market') or []) + [['BUY_SEED', 'TOMATO', quantity]]
    state['seed_ordered'] = True
    state['seed_order_step'] = step
    state['counts']['seed_orders'] += 1
    state['counts']['seed_units'] += quantity
    return result


def _c176_confirm_hires(observation, state):
    pending = state.get('pending_hires')
    if not pending:
        return
    step = int(observation['step'])
    if step != pending['step'] + 1:
        if step > pending['step'] + 1:
            state['counts']['hire_shortfalls'] += pending['count']
            state['pending_hires'] = None
        return
    hands = len(observation['farms'][int(observation['player'])]['hands'])
    last_actor = pending['first_actor'] + pending['count'] - 1
    if hands >= last_actor:
        state['workers'] = list(range(pending['first_actor'], last_actor + 1))
        state['counts']['hires_confirmed'] += pending['count']
    else:
        state['counts']['hire_shortfalls'] += pending['count']
        state['workers'] = []
    state['pending_hires'] = None


def _c176_request_workers(observation, action, state):
    step = int(observation['step']); day = step // 24; hour = step % 24
    if not (_C176_FIRST_DAY <= day <= 28) or hour > 3 or state['hire_day'] == day:
        return action
    # Start one maintenance worker on day18 even before the first conversion.
    # Scattered existing-land targets use two once the committed set grows.
    confirmed_or_pending = len(state['targets'])
    desired = 1 if confirmed_or_pending <= 4 else 2
    farm = observation['farms'][int(observation['player'])]
    orders = action.get('market') or []
    parent_hires = sum(bool(order) and order[0] == 'HIRE' for order in orders)
    if len(orders) + desired > 10:
        state['counts']['hire_declines'] += 1
        return action
    first_actor = len(farm.get('hands', [])) + parent_hires + 1
    hire_cost = sum(_v219_fib(int(farm.get('hires_today', 0)) + parent_hires + i) for i in range(desired))
    if float(farm.get('money', 0)) < hire_cost + _C176_CASH_RESERVE:
        state['counts']['hire_declines'] += 1
        return action
    result = _c176_copy.deepcopy(action)
    result['market'] = list(result.get('market') or []) + [['HIRE'] for _ in range(desired)]
    state['pending_hires'] = {'step': step, 'first_actor': first_actor, 'count': desired}
    state['hire_day'] = day
    state['counts']['hire_requests'] += desired
    return result


def _c176_worker(observation, state, actor):
    seat = int(observation['player']); step = int(observation['step'])
    farm = observation['farms'][seat]; private = observation['private']
    positions = [farm['farmer'], *farm['hands']]
    if actor >= len(positions) or actor >= len(private['inventories']):
        return ['PASS']
    pos = tuple(positions[actor]); inv = private['inventories'][actor]
    worker_ids = list(state.get('workers') or [actor])
    try:
        rank = worker_ids.index(actor)
    except ValueError:
        rank = 0
    live = []
    for xy, meta in sorted(state['targets'].items(), key=lambda item: (item[0][1], item[0][0])):
        x, y = xy; tile = farm['tiles'][y][x]
        if isinstance(tile, dict) and tile.get('crop') == 'TOMATO':
            live.append(xy)
        elif meta.get('confirmed'):
            # Release a failed slot.  During the bounded day18-20 planting
            # window a later native WHEAT planting may refill it; afterwards
            # the slot simply remains lost and is visible in telemetry.
            state['targets'].pop(xy, None)
            state['counts']['lost_targets'] += 1
    assigned = live[rank::max(1, len(worker_ids))]
    todo = []
    for xy in assigned:
        x, y = xy; tile = farm['tiles'][y][x]
        command = None
        if not tile.get('watered_today'):
            command = ['WATER']
        elif int(tile.get('yield_units', 0)) > 0:
            command = ['HARVEST']
        if command is not None:
            todo.append((abs(pos[0]-x) + abs(pos[1]-y), xy, command))

    home = _v219_home(pos)
    distance_home = abs(pos[0]-home[0]) + abs(pos[1]-home[1])
    # Preserve end-of-day delivery even if one distant target remains.
    if step % 24 >= 23 - distance_home and inv.get('TOMATO', 0):
        return _v219_walk(pos, home) or ['PLACE', 'TOMATO', int(inv.get('TOMATO', 0))]
    if todo:
        _, target, command = min(todo, key=lambda row: (row[0], row[1]))
        return _v219_walk(pos, target) or command
    if inv.get('TOMATO', 0):
        return _v219_walk(pos, home) or ['PLACE', 'TOMATO', int(inv.get('TOMATO', 0))]
    if any(int(value) > 0 for value in inv.values()):
        return _v219_walk(pos, home) or ['DROP']
    return ['PASS']


def _c176_apply_workers(observation, action, state):
    if not state.get('workers'):
        return action
    farm = observation['farms'][int(observation['player'])]
    result = _c176_copy.deepcopy(action)
    commands = [result.get('farmer') or ['PASS'], *(result.get('hands') or [])]
    commands += [['PASS'] for _ in range(len(farm.get('hands', [])) + 1 - len(commands))]
    for actor in list(state['workers']):
        if actor >= len(commands):
            continue
        command = _c176_worker(observation, state, actor)
        commands[actor] = command
        if command == ['WATER']:
            state['counts']['water_requests'] += 1
        elif command == ['HARVEST']:
            state['counts']['harvest_requests'] += 1
        elif command and command[0] in ('PLACE', 'DROP'):
            state['counts']['drop_requests'] += 1
    result['farmer'], result['hands'] = commands[0], commands[1:]
    return result


def _c176_future_wheat_pickups(observation):
    step = int(observation['step']); seat = int(observation['player'])
    native = _IMPL.chassis.players.get(seat) or {}
    route = native.get('route', 0)
    demand = 2  # small physical slack, not a six-units-per-tile opportunity-cost fiction
    stop = min(719, step + 1 + _C176_WHEAT_LOOKAHEAD)
    for future_step in range(step + 1, stop):
        tape = _IMPL.chassis.routes[2 if future_step >= 648 else route]
        future = tape[future_step]
        for command in [future.get('farmer') or ['PASS'], *(future.get('hands') or [])]:
            if len(command) > 1 and command[:2] == ['PICKUP', 'WHEAT']:
                demand += max(0, int(command[2]) if len(command) > 2 else 1)
    return demand


def _c176_wheat_topup(observation, action, state):
    step = int(observation['step']); day = step // 24
    if not state['targets'] or state['wheat_topup_day'] == day or step % 24 > 5:
        return action
    farm = observation['farms'][int(observation['player'])]
    stock = projected_shed(action, FarmView(observation))
    need = max(0, _c176_future_wheat_pickups(observation) - int(stock.get('WHEAT', 0)))
    quantity = min(_C176_MAX_WHEAT_TOPUP, need)
    if quantity <= 0:
        state['wheat_topup_day'] = day
        return action
    orders = action.get('market') or []
    capacity = sum(max(0, int(value)) for value in stock.values())
    quote = max(1, int(observation['market']['prices'].get('WHEAT', 1)))
    if (len(orders) >= 10 or capacity + quantity > 95
            or float(farm.get('money', 0)) < quantity * (quote + 10) + _C176_CASH_RESERVE):
        state['counts']['wheat_topup_declines'] += 1
        return action
    result = _c176_copy.deepcopy(action)
    result['market'] = list(result.get('market') or []) + [['BUY_PRODUCT', 'WHEAT', quantity]]
    state['wheat_topup_day'] = day
    state['counts']['wheat_topup_turns'] += 1
    state['counts']['wheat_topup_units'] += quantity
    return result


def _c176_sell_tomato(observation, action, state):
    if not state['targets']:
        return action
    orders = action.get('market') or []
    if len(orders) >= 10:
        return action
    stock = max(0, int(projected_shed(action, FarmView(observation)).get('TOMATO', 0)))
    planned = sum(max(0, int(order[2])) for order in orders
                  if len(order) >= 3 and order[:2] == ['SELL', 'TOMATO'])
    extra = max(0, stock - planned)
    if extra <= 0:
        return action
    result = _c176_copy.deepcopy(action)
    result['market'] = list(result.get('market') or []) + [['SELL', 'TOMATO', extra]]
    # Preserve the parent's market-order contracts after adding a new product.
    try:
        result = _v224_sales_first(result)
        result = _r37_reorder_sales(observation, result)
    except Exception:
        pass
    state['counts']['tomato_sale_turns'] += 1
    state['counts']['tomato_sale_units'] += extra
    return result


def _c176_control(observation, parent_action, state):
    step = int(observation['step']); day = step // 24
    if state['day'] != day:
        state['day'] = day
        state['workers'] = []
        state['hire_day'] = -1
        state['wheat_topup_day'] = -1
    _c176_confirm_plants(observation, state)
    _c176_confirm_hires(observation, state)

    result = parent_action
    result = _c176_seed_pool(observation, result, state)
    result = _c176_convert_plants(observation, result, state)
    result = _c176_request_workers(observation, result, state)
    result = _c176_apply_workers(observation, result, state)
    result = _c176_wheat_topup(observation, result, state)
    result = _c176_sell_tomato(observation, result, state)
    return result


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    state = _C176_STATES.get(seat)
    if state is None or step <= state.get('last', -1):
        state = _C176_STATES[seat] = _c176_new_state()
    state['last'] = step

    # Decide before invoking the parent so V219's global qualification hook can
    # see the committed regime on the same step-432 callback.
    if step == _C176_FIRST_DAY * 24 and not state['decided']:
        state['decided'] = True
        try:
            if _c176_standard(configuration):
                _c176_decide(observation, state)
        except Exception:
            state['counts']['errors'] += 1

    parent_action = _C176_PARENT(observation, configuration)
    result = parent_action
    try:
        if state.get('active') and _c176_standard(configuration):
            result = _c176_control(observation, parent_action, state)
    except Exception:
        state['counts']['errors'] += 1
        result = parent_action

    _C176_REPORT.clear()
    _C176_REPORT.update(getattr(_C176_PARENT, 'telemetry', {}))
    _C176_REPORT.update({'c176_' + key: value for key, value in state['counts'].items()})
    _C176_REPORT.update({
        'c176_regime': state.get('regime', 'KEEP'),
        'c176_active': int(bool(state.get('active'))),
        'c176_target_count': int(state.get('target_count', 0)),
        'c176_live_targets': len(state.get('targets', {})),
        'c176_confirmed_targets': sum(int(bool(meta.get('confirmed'))) for meta in state.get('targets', {}).values()),
    })
    return result


agent.telemetry = _C176_REPORT
agent = globals().pop('agent')
