"""Add a price-gated SE strawberry expansion to frozen o302: in worlds with three or more berry
shops among the first four and a scarce strawberry market at day 12, buy the last quadrant, plant
twelve strawberries with two dedicated hands and sell every delivered unit."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
WRAPPER = r'''

# o304: berry expansion. Live loss ra5anchor (-17.9k): in a six-berry-shop world
# the rival bought SE at d12, planted +20 strawberries and sold +122 units at
# $211 while our tape kept 33 tiles. Berry-heavy worlds (>=3 berry shops by d12)
# are 20% of live games and we win only 20% of them. Gate at d12 h0: >=3 berry
# shops among the first four, STRAWBERRY >= $200, SE still locked, cash for land,
# seeds and a reserve. Then buy SE, 12 strawberry seeds and hire two hands after
# every native hire each day (tape hand indices untouched). Each hand plants,
# waters daily, harvests its six tiles on alternating days, delivers to the shed,
# and every delivered unit is sold on the next market turn.
_O304_ENABLED = __ON__
_O304_PARENT = agent
_O304_REPORT = {}
_O304_STATES = {}
_O304_DECISION_STEP = 288
_O304_MIN_BERRY_SHOPS = 3
_O304_MIN_PRICE = 200
_O304_BERRY_SHOPS = ('BRUNCH_SPOT', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP', 'FARMERS_MARKET')
_O304_TILES = [(6, 5), (7, 5), (5, 6), (6, 6), (7, 6), (5, 7), (6, 7), (7, 7), (8, 5), (8, 6), (5, 8), (6, 8)]
_O304_HANDS = 2
_O304_LAND = 4000
_O304_SEED = 100
_O304_RESERVE = 2500
_O304_MAX_ORDERS = 10
_O304_HIRE_DEADLINE = 6
_O304_LAST_DAY = 29

def _o304_fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def _o304_frames(player, step):
    route = _C358_IMPL.chassis.players[player]['route']
    tape = _C358_IMPL.chassis.routes[route]
    day_end = min(len(tape), (step // 24 + 1) * 24)
    return [tape[t] if isinstance(tape[t], dict) else {} for t in range(step // 24 * 24, day_end)], step % 24

def _o304_walk(pos, target):
    x, y = pos; tx, ty = target
    if x != tx:
        return ['EAST' if x < tx else 'WEST']
    if y != ty:
        return ['SOUTH' if y < ty else 'NORTH']
    return None

def _o304_eligible(observation):
    farm = observation['farms'][int(observation['player'])]
    shops = list(observation['town'].get('unlocked_shops') or [])
    if sum(s in _O304_BERRY_SHOPS for s in shops[:4]) < _O304_MIN_BERRY_SHOPS:
        return 'shops'
    if int(observation['market']['prices'].get('STRAWBERRY', 0)) < _O304_MIN_PRICE:
        return 'price'
    tiles = farm['tiles']; half = len(tiles) // 2
    if any(tiles[y][x] != 'LOCKED' for y in range(half, len(tiles)) for x in range(half, len(tiles))):
        return 'land'
    if float(farm['money']) < _O304_LAND + _O304_SEED * len(_O304_TILES) + _O304_RESERVE:
        return 'cash'
    return None

def _o304_hire(observation, action, state):
    """Append the expansion hires (and the one-time land/seed purchase) after the day's native hires."""
    step = int(observation['step']); hour = step % 24; player = int(observation['player'])
    farm = observation['farms'][player]
    if hour > _O304_HIRE_DEADLINE:
        state['day_hired'] = None; _O304_REPORT['hire_missed_deadline'] += 1
        return action
    frames, offset = _o304_frames(player, step)
    if any(o and o[0] == 'HIRE' for f in frames[offset + 1:] for o in (f.get('market') or [])):
        return action
    expected = max((len(f.get('hands') or []) for f in frames), default=0)
    market = [list(o) for o in (action.get('market') or []) if o]
    parent_hires = sum(1 for o in market if o[0] == 'HIRE')
    if len(farm['hands']) + parent_hires != expected:
        state['day_hired'] = None; _O304_REPORT['hire_skipped_indices'] += 1
        return action
    extra = []
    if not state['committed']:
        extra += [['BUY_LAND'], ['BUY_SEED', 'STRAWBERRY', len(_O304_TILES)]]
    extra += [['HIRE'] for _ in range(_O304_HANDS)]
    if len(market) + len(extra) > _O304_MAX_ORDERS:
        state['day_hired'] = None; _O304_REPORT['hire_skipped_orders'] += 1
        return action
    hires_today = int(farm.get('hires_today', 0)) + parent_hires
    cost = sum(_o304_fib(hires_today + i) for i in range(_O304_HANDS))
    if not state['committed']:
        cost += _O304_LAND + _O304_SEED * len(_O304_TILES)
    if float(farm['money']) < cost + (_O304_RESERVE if not state['committed'] else 500):
        state['day_hired'] = None; _O304_REPORT['hire_skipped_cash'] += 1
        return action
    action = dict(action); action['market'] = market + extra
    state['day_hired'] = True; state['first_actor'] = expected + 1; state['hire_step'] = step
    if not state['committed']:
        state['committed'] = True; _O304_REPORT['commitments'] += 1
    _O304_REPORT['hires'] += _O304_HANDS
    return action

def _o304_worker(observation, state, actor, tiles, day, hour):
    farm = observation['farms'][int(observation['player'])]
    hands = farm.get('hands') or []
    pos = tuple(hands[actor - 1]); board = len(farm['tiles']); half = board // 2
    inventories = observation['private'].get('inventories') or []
    inv = inventories[actor] if actor < len(inventories) else {}
    seeds = int((observation['private'].get('seeds') or {}).get('STRAWBERRY', 0))
    berries = int(inv.get('STRAWBERRY', 0))
    adjacent = pos[0] in (half - 1, half) and pos[1] in (half - 1, half)
    access = min(((half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)),
                 key=lambda p: abs(pos[0] - p[0]) + abs(pos[1] - p[1]))
    todo = []
    for i, (x, y) in enumerate(tiles):
        tile = farm['tiles'][y][x]
        if tile == 'LOCKED':
            continue
        if tile is None:
            if seeds > 0 and day <= 16:
                todo.append(((x, y), ['PLANT', 'STRAWBERRY'], 0))
            continue
        if not isinstance(tile, dict):
            continue
        if tile.get('kind') == 'WEED':
            todo.append(((x, y), ['DIG'], 1)); continue
        if tile.get('crop') != 'STRAWBERRY':
            continue
        if not tile.get('watered_today') and day < _O304_LAST_DAY:
            todo.append(((x, y), ['WATER'], 0))
        if tile.get('yield_units', 0) > 0 and (i % 2 == day % 2 or day >= _O304_LAST_DAY - 1 or tile.get('yield_units', 0) >= 3):
            todo.append(((x, y), ['HARVEST'], 0))
    dist = abs(pos[0] - access[0]) + abs(pos[1] - access[1])
    # Deliver before the day ends (nightly auto-drop can overflow the shed) or when loaded.
    if berries and (hour >= 23 - dist - 1 or berries >= 6 or not todo):
        return _o304_walk(pos, access) or ['DROP']
    if not todo:
        return ['PASS']
    (tx, ty), command, _ = min(todo, key=lambda t: (t[2], abs(pos[0] - t[0][0]) + abs(pos[1] - t[0][1])))
    return _o304_walk(pos, (tx, ty)) or command

def _o304_drive(observation, action, state):
    step = int(observation['step']); day = step // 24; hour = step % 24; player = int(observation['player'])
    farm = observation['farms'][player]; hands = farm.get('hands') or []
    first = state['first_actor']
    if first - 1 + _O304_HANDS - 1 >= len(hands):
        if step == state.get('hire_step', -1) + 1:
            _O304_REPORT['hire_shortfalls'] += 1
        state['day_hired'] = None
        return action
    commands = [list(action.get('farmer') or ['PASS'])] + [list(c) if c else ['PASS'] for c in (action.get('hands') or [])]
    commands += [['PASS'] for _ in range(len(hands) + 1 - len(commands))]
    per = len(_O304_TILES) // _O304_HANDS
    for k in range(_O304_HANDS):
        actor = first + k
        command = _o304_worker(observation, state, actor, _O304_TILES[k * per:(k + 1) * per], day, hour)
        commands[actor] = command
        name = {'PLANT': 'plant_requests', 'WATER': 'water_requests', 'HARVEST': 'harvest_requests', 'DROP': 'drop_requests', 'DIG': 'dig_requests'}.get(command[0])
        if name:
            _O304_REPORT[name] += 1
        if command == ['DROP']:
            inv = (observation['private'].get('inventories') or [{}] * (actor + 1))
            state['delivered_pending'] += int((inv[actor] if actor < len(inv) else {}).get('STRAWBERRY', 0))
    action = dict(action); action['farmer'], action['hands'] = commands[0], commands[1:]
    return action

def _o304_sell(observation, action, state):
    """Sell the delivered units on this market turn (delivery happens in the farm phase of the same step)."""
    pending = state['delivered_pending']
    if pending <= 0:
        return action
    market = [list(o) for o in (action.get('market') or []) if o]
    sell = next((o for o in market if len(o) >= 3 and o[0] == 'SELL' and o[1] == 'STRAWBERRY'), None)
    if sell is not None:
        sell[2] = int(sell[2]) + pending
    elif len(market) < _O304_MAX_ORDERS:
        market.append(['SELL', 'STRAWBERRY', pending])
    else:
        return action
    _O304_REPORT['sale_units'] += pending; state['delivered_pending'] = 0
    return dict(action, market=market)

def agent(observation, configuration=None):
    action = _O304_PARENT(observation, configuration)
    step = int(observation['step']); day = step // 24; player = int(observation['player'])
    state = _O304_STATES.get(player)
    if step == 0 or state is None or step <= state['last_step']:
        state = {'last_step': step, 'day': -1, 'eligible': None, 'committed': False, 'day_hired': False, 'first_actor': None, 'delivered_pending': 0}
        _O304_STATES[player] = state
        _O304_REPORT.clear()
        _O304_REPORT.update(eligibility='', commitments=0, hires=0, hire_missed_deadline=0, hire_skipped_indices=0, hire_skipped_orders=0,
                            hire_skipped_cash=0, hire_shortfalls=0, plant_requests=0, water_requests=0, harvest_requests=0,
                            drop_requests=0, dig_requests=0, sale_units=0)
    state['last_step'] = step
    _O304_REPORT.update(_O302_REPORT)
    if not _O304_ENABLED:
        return action
    if step == _O304_DECISION_STEP:
        reason = _o304_eligible(observation)
        state['eligible'] = reason is None; _O304_REPORT['eligibility'] = reason or 'eligible'
    if not state['eligible'] or day > _O304_LAST_DAY:
        return action
    if state['day'] != day:
        state['day'] = day; state['day_hired'] = False; state['first_actor'] = None
    if state['day_hired'] is None:
        return _o304_sell(observation, action, state)
    if not state['day_hired']:
        action = _o304_hire(observation, action, state)
        return _o304_sell(observation, action, state)
    action = _o304_drive(observation, action, state)
    return _o304_sell(observation, action, state)

agent.telemetry = _O304_REPORT
kaggle_submission_agent = agent
o304_submission_agent = agent
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    args = ap.parse_args()
    parent = (ROOT / 'agent/o302_farmer_feed_topup.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    data = parent.rstrip() + WRAPPER.replace('__ON__', str(not args.disabled)).encode()
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
