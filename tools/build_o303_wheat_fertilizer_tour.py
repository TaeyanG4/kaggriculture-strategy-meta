"""Add a dedicated wheat-fertilizer hand to frozen o302: one extra hire on days where the expected
net (yield gain minus withheld fertilizer sales minus the hire) clears a floor, fertilizing age-1/2 wheat."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
WRAPPER = r'''

# o303: wheat fertilizer tour. Fertilized wheat harvests 5.7-5.8 units against
# 3.4-3.8 unfertilized (own ledgers), the tape leaves 12-19 unfertilized age-1/2
# wheat tiles every day from d14 to d25, and late fertilizer sells for $8-35.
# Each morning: if k = min(8, candidates, shed fertilizer) units withheld from the
# morning fertilizer sales, one extra hand (hired after every native hire so the
# tape's hand indices are untouched) and the wheat price clear a net floor,
# hire that hand, pick up k fertilizer and fertilize the nearest candidates.
# Nothing else in the plan changes; leftovers return to the shed at midnight.
_O303_ENABLED = __ON__
_O303_PARENT = agent
_O303_REPORT = {}
_O303_STATES = {}
_O303_MAX_UNITS = 8
_O303_MIN_UNITS = 3
_O303_MIN_NET = 150.0
_O303_GAIN_PER_UNIT = 2.0
_O303_LAST_HARVEST_DAY = 29
_O303_MAX_ORDERS = 10
_O303_HIRE_DEADLINE = 6

def _o303_fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def _o303_frames(player, step):
    route = _C358_IMPL.chassis.players[player]['route']
    tape = _C358_IMPL.chassis.routes[route]
    day_end = min(len(tape), (step // 24 + 1) * 24)
    return [tape[t] if isinstance(tape[t], dict) else {} for t in range(step // 24 * 24, day_end)], step % 24

def _o303_candidates(farm, day):
    out = []
    for y, row in enumerate(farm['tiles']):
        for x, tile in enumerate(row):
            if not (isinstance(tile, dict) and tile.get('crop') == 'WHEAT'):
                continue
            age = day - int(tile.get('planted_day', day))
            if age in (1, 2) and int(tile.get('fertilized_until_day', -1)) < day and int(tile['planted_day']) + 4 <= _O303_LAST_HARVEST_DAY:
                out.append((x, y))
    return out

def _o303_walk(pos, target):
    x, y = pos; tx, ty = target
    if x != tx:
        return ['EAST' if x < tx else 'WEST']
    if y != ty:
        return ['SOUTH' if y < ty else 'NORTH']
    return None

def _o303_plan(observation, state):
    """Decide the day's tour at h0 from candidates, shed stock, prices and the extra hire's cost."""
    step = int(observation['step']); day = step // 24; player = int(observation['player'])
    farm = observation['farms'][player]; prices = observation['market']['prices']
    frames, _ = _o303_frames(player, step)
    expected = max((len(f.get('hands') or []) for f in frames), default=0)
    candidates = _o303_candidates(farm, day)
    stock = int((observation['private'].get('shed') or {}).get('FERTILIZER', 0))
    units = min(_O303_MAX_UNITS, len(candidates), stock)
    hire_cost = _o303_fib(expected)
    net = units * _O303_GAIN_PER_UNIT * int(prices.get('WHEAT', 0)) - units * int(prices.get('FERTILIZER', 0)) - hire_cost
    state['plan'] = None
    if units < _O303_MIN_UNITS or net < _O303_MIN_NET:
        _O303_REPORT['tour_days_skipped'] += 1
        return
    state['plan'] = {'units': units, 'expected': expected, 'hired': False, 'actor': None, 'picked': False, 'done': 0, 'net': net}
    _O303_REPORT['tour_days_planned'] += 1

def _o303_withhold(observation, action, plan):
    """Keep the planned units out of this step's fertilizer sales until the hand has them."""
    stock = int((observation['private'].get('shed') or {}).get('FERTILIZER', 0))
    allowed = max(0, stock - plan['units'])
    market = [list(o) for o in (action.get('market') or []) if o]
    changed = False
    for o in market:
        if o[0] == 'SELL' and len(o) >= 3 and o[1] == 'FERTILIZER':
            q = max(0, int(o[2])); keep = min(q, allowed); allowed -= keep
            if keep != q:
                _O303_REPORT['withheld_units'] += q - keep; o[2] = keep; changed = True
    if changed:
        action = dict(action); action['market'] = [o for o in market if not (o[0] == 'SELL' and len(o) >= 3 and int(o[2]) <= 0)]
    return action

def _o303_hire(observation, action, plan):
    step = int(observation['step']); hour = step % 24; player = int(observation['player'])
    farm = observation['farms'][player]
    if hour > _O303_HIRE_DEADLINE:
        plan['hired'] = None; _O303_REPORT['hire_missed_deadline'] += 1
        return action
    frames, offset = _o303_frames(player, step)
    if any(o and o[0] == 'HIRE' for f in frames[offset + 1:] for o in (f.get('market') or [])):
        return action
    market = [list(o) for o in (action.get('market') or []) if o]
    parent_hires = sum(1 for o in market if o[0] == 'HIRE')
    if len(farm['hands']) + parent_hires != plan['expected'] or len(market) >= _O303_MAX_ORDERS:
        plan['hired'] = None; _O303_REPORT['hire_skipped_indices'] += 1
        return action
    cost = _o303_fib(int(farm.get('hires_today', 0)) + parent_hires)
    if float(farm['money']) < cost + 1000:
        plan['hired'] = None; _O303_REPORT['hire_skipped_cash'] += 1
        return action
    action = dict(action); action['market'] = market + [['HIRE']]
    plan['hired'] = True; plan['actor'] = plan['expected'] + 1; plan['hire_step'] = step
    _O303_REPORT['tour_hires'] += 1
    return action

def _o303_tour(observation, action, plan):
    step = int(observation['step']); day = step // 24; player = int(observation['player'])
    farm = observation['farms'][player]; actor = plan['actor']
    hands = farm.get('hands') or []
    if actor - 1 >= len(hands):
        if step == plan.get('hire_step', -1) + 1:
            plan['hired'] = None; _O303_REPORT['hire_shortfalls'] += 1
        return action
    pos = tuple(hands[actor - 1]); board = len(farm['tiles']); half = board // 2
    inventories = observation['private'].get('inventories') or []
    inv = inventories[actor] if actor < len(inventories) else {}
    carried = int(inv.get('FERTILIZER', 0))
    shed = int((observation['private'].get('shed') or {}).get('FERTILIZER', 0))
    adjacent = pos[0] in (half - 1, half) and pos[1] in (half - 1, half)
    command = ['PASS']
    if not plan['picked']:
        if adjacent:
            units = min(plan['units'], shed)
            if units > 0:
                command = ['PICKUP', 'FERTILIZER', units]; plan['picked'] = True; _O303_REPORT['picked_units'] += units
            else:
                plan['picked'] = True; _O303_REPORT['pickup_empty'] += 1
        else:
            access = min(((half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)),
                         key=lambda p: abs(pos[0] - p[0]) + abs(pos[1] - p[1]))
            command = _o303_walk(pos, access) or ['PASS']
    elif carried > 0:
        targets = _o303_candidates(farm, day)
        if targets:
            target = min(targets, key=lambda p: (abs(pos[0] - p[0]) + abs(pos[1] - p[1]), p))
            command = _o303_walk(pos, target) or ['FERTILIZE']
            if command == ['FERTILIZE']:
                plan['done'] += 1; _O303_REPORT['fertilizations'] += 1
        else:
            _O303_REPORT['idle_steps'] += 1
    else:
        _O303_REPORT['idle_steps'] += 1
    commands = [list(action.get('farmer') or ['PASS'])] + [list(c) if c else ['PASS'] for c in (action.get('hands') or [])]
    commands += [['PASS'] for _ in range(len(hands) + 1 - len(commands))]
    commands[actor] = command
    action = dict(action); action['farmer'], action['hands'] = commands[0], commands[1:]
    return action

def agent(observation, configuration=None):
    action = _O303_PARENT(observation, configuration)
    step = int(observation['step']); day = step // 24; player = int(observation['player'])
    state = _O303_STATES.get(player)
    if step == 0 or state is None or step <= state['last_step']:
        state = {'last_step': step, 'day': -1, 'plan': None}
        _O303_STATES[player] = state
        _O303_REPORT.clear()
        _O303_REPORT.update(tour_days_planned=0, tour_days_skipped=0, tour_hires=0, hire_missed_deadline=0, hire_skipped_indices=0,
                            hire_skipped_cash=0, hire_shortfalls=0, withheld_units=0, picked_units=0, pickup_empty=0,
                            fertilizations=0, idle_steps=0)
    state['last_step'] = step
    _O303_REPORT.update(_O302_REPORT)
    if not _O303_ENABLED:
        return action
    if state['day'] != day:
        state['day'] = day
        _o303_plan(observation, state)
    plan = state['plan']
    if not plan or plan['hired'] is None:
        return action
    if not plan['picked']:
        action = _o303_withhold(observation, action, plan)
    if not plan['hired']:
        return _o303_hire(observation, action, plan)
    return _o303_tour(observation, action, plan)

agent.telemetry = _O303_REPORT
kaggle_submission_agent = agent
o303_submission_agent = agent
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
