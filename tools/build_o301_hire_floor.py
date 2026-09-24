"""Add an opening hire cash floor (with same-day feed repair) to frozen c373."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '6731b608fa9a94e88f47211b3d3e2feb14681e45e6c918756e5a7e3205923297'
WRAPPER = r'''

# o301: opening hire cash floor. The native d0 plan ends with $1-12 and the d1
# HIRE orders cost fib(1,1,2,...). Live replays show three collapses (1-2 hands
# on d1, cows starve, -4k..-18k) when the d0 wheat round-trip left $1-3. When
# the parent's HIRE orders in the first days cannot all be paid, sell shed
# fertilizer, then wheat, for the shortfall only. A wheat sale can starve one
# morning FEED (the plan picks up every stored unit), so on that day a hand that
# is idle for the rest of its shift re-feeds the animal once the plan has bought
# wheat again. No plan edits, extra hires, purchases or land.
_O301_ENABLED = __ON__
_O301_PARENT = agent
_O301_REPORT = {}
_O301_STATES = {}
_O301_ITEMS = ('FERTILIZER', 'WHEAT', 'EGG', 'CARROT', 'TOMATO', 'MELON', 'WOOL', 'MILK', 'STRAWBERRY')
_O301_MAX_DAY = 2
_O301_MAX_ORDERS = 10
_O301_SEED = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
_O301_ANIMAL = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}

def _o301_fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def _o301_shortfall(observation, market):
    """Largest cash gap before any HIRE while replaying the order list in engine order."""
    farm = observation['farms'][int(observation['player'])]
    prices = observation['market']['prices']
    shed = dict(observation['private'].get('shed') or {})
    money = float(farm['money'])
    hires = int(farm.get('hires_today', 0))
    gap = 0.0
    for order in market:
        if not order:
            continue
        op = order[0]
        if op == 'HIRE':
            cost = _o301_fib(hires)
            gap = max(gap, cost - money)
            money -= cost
            hires += 1
        elif op == 'BUY_LAND':
            money -= 4000
        elif len(order) >= 3:
            item, qty = order[1], max(0, int(order[2]))
            if op == 'BUY_SEED':
                money -= qty * _O301_SEED.get(item, 100)
            elif op == 'BUY_ANIMAL':
                money -= qty * _O301_ANIMAL.get(item, 500)
            elif op == 'BUY_PRODUCT':
                money -= qty * (int(prices.get(item, 100)) + 2)
            elif op == 'SELL':
                units = min(qty, int(shed.get(item, 0)))
                shed[item] = int(shed.get(item, 0)) - units
                money += units * max(1, int(prices.get(item, 1)) - 2)
    return gap

def _o301_floor(observation, action, state):
    market = [list(o) for o in (action.get('market') or []) if o]
    if not any(o[0] == 'HIRE' for o in market) or len(market) >= _O301_MAX_ORDERS:
        return action
    _O301_REPORT['floor_checks'] += 1
    gap = _o301_shortfall(observation, market)
    if gap <= 0:
        return action
    prices = observation['market']['prices']
    shed = observation['private'].get('shed') or {}
    planned = {}
    for o in market:
        if o[0] == 'SELL' and len(o) >= 3:
            planned[o[1]] = planned.get(o[1], 0) + max(0, int(o[2]))
    extra = []
    for item in _O301_ITEMS:
        if gap <= 0:
            break
        free = int(shed.get(item, 0)) - planned.get(item, 0)
        unit = max(1, int(prices.get(item, 1)) - 2)
        if free <= 0 or unit < 3:
            continue
        units = min(free, -(-int(gap) // unit))
        extra.append(['SELL', item, units])
        gap -= units * unit
        if len(market) + len(extra) >= _O301_MAX_ORDERS:
            break
    if not extra:
        _O301_REPORT['floor_unfunded'] += 1
        return action
    if gap > 0:
        _O301_REPORT['floor_unfunded'] += 1
    action = dict(action)
    action['market'] = extra + market
    _O301_REPORT['floor_sales'] += 1
    _O301_REPORT['floor_units'] += sum(o[2] for o in extra)
    if any(o[1] == 'WHEAT' for o in extra):
        state['floor_day'] = int(observation['step']) // 24
    return action

def _o301_commands(action, count):
    commands = [list(action.get('farmer') or ['PASS'])] + [list(c) if c else ['PASS'] for c in (action.get('hands') or [])]
    commands += [['PASS'] for _ in range(count - len(commands))]
    return commands[:count]

def _o301_idle(route, actor, step):
    """True when the tape gives this actor nothing but PASS for the rest of the day."""
    tape = _C358_IMPL.chassis.routes[route]
    for t in range(step + 1, min(len(tape), (step // 24 + 1) * 24)):
        frame = tape[t] if isinstance(tape[t], dict) else {}
        if actor == 0:
            command = frame.get('farmer') or ['PASS']
        else:
            hands = frame.get('hands') or []
            command = hands[actor - 1] if actor - 1 < len(hands) else None
        if command is not None and list(command) != ['PASS']:
            return False
    return True

def _o301_walk(pos, target):
    x, y = pos; tx, ty = target
    if x != tx:
        return ['EAST' if x < tx else 'WEST']
    if y != ty:
        return ['SOUTH' if y < ty else 'NORTH']
    return None

def _o301_repair(observation, action, state):
    step = int(observation['step']); day = step // 24
    player = int(observation['player']); farm = observation['farms'][player]
    tiles = farm['tiles']; board = len(tiles); half = board // 2
    positions = [tuple(farm['farmer'])] + [tuple(p) for p in (farm.get('hands') or [])]
    inventories = list(observation['private'].get('inventories') or [])
    shed = observation['private'].get('shed') or {}
    commands = _o301_commands(action, len(positions))

    def animal_tile(target):
        x, y = target
        tile = tiles[y][x] if 0 <= y < board and 0 <= x < board else None
        return tile if isinstance(tile, dict) and tile.get('animal') else None

    # 1. Record FEED commands that cannot succeed because the worker carries no wheat.
    for actor, command in enumerate(commands):
        if command[0] != 'FEED' or actor >= len(positions):
            continue
        inv = inventories[actor] if actor < len(inventories) else {}
        tile = animal_tile(positions[actor])
        if tile is not None and not tile.get('fed_today') and int(inv.get('WHEAT', 0)) <= 0:
            if positions[actor] not in state['unfed']:
                state['unfed'].append(positions[actor])
                _O301_REPORT['feed_failures'] += 1
    # 2. Drop finished or stale jobs.
    for actor in list(state['jobs']):
        job = state['jobs'][actor]
        tile = animal_tile(job['target'])
        if actor >= len(positions) or tile is None or tile.get('fed_today') or commands[actor] != ['PASS']:
            if tile is not None and tile.get('fed_today'):
                _O301_REPORT['feed_repairs_done'] += 1
            state['jobs'].pop(actor)
    # 3. Assign unassigned targets to actors idle for the rest of the day.
    route = _C358_IMPL.chassis.players[player]['route']
    busy = {job['target'] for job in state['jobs'].values()}
    for target in list(state['unfed']):
        tile = animal_tile(target)
        if tile is None or tile.get('fed_today'):
            state['unfed'].remove(target)
            continue
        if target in busy:
            continue
        for actor in list(range(1, len(positions))) + [0]:
            if actor in state['jobs'] or commands[actor] != ['PASS'] or not _o301_idle(route, actor, step):
                continue
            state['jobs'][actor] = {'target': target}
            busy.add(target)
            _O301_REPORT['feed_repairs_assigned'] += 1
            break
    if not state['jobs']:
        return action
    # 4. Drive the jobs: fetch one wheat from the shed, walk to the animal, feed.
    for actor, job in state['jobs'].items():
        pos = positions[actor]; inv = inventories[actor] if actor < len(inventories) else {}
        target = job['target']
        if int(inv.get('WHEAT', 0)) > 0:
            command = _o301_walk(pos, target) or ['FEED']
        elif int(shed.get('WHEAT', 0)) > 0:
            if pos[0] in (half - 1, half) and pos[1] in (half - 1, half):
                command = ['PICKUP', 'WHEAT', 1]
            else:
                access = min(((half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)),
                             key=lambda p: abs(pos[0] - p[0]) + abs(pos[1] - p[1]))
                command = _o301_walk(pos, access) or ['PASS']
        else:
            command = ['PASS']
        commands[actor] = command
        _O301_REPORT['feed_repair_steps'] += 1
    action = dict(action)
    action['farmer'], action['hands'] = commands[0], commands[1:]
    return action

def agent(observation, configuration=None):
    action = _O301_PARENT(observation, configuration)
    step = int(observation['step']); day = step // 24; player = int(observation['player'])
    state = _O301_STATES.get(player)
    if step == 0 or state is None or step <= state['last_step']:
        state = {'last_step': step, 'floor_day': -1, 'day': -1, 'unfed': [], 'jobs': {}}
        _O301_STATES[player] = state
        _O301_REPORT.clear()
        _O301_REPORT.update(floor_checks=0, floor_sales=0, floor_units=0, floor_unfunded=0, feed_failures=0,
                            feed_repairs_assigned=0, feed_repairs_done=0, feed_repair_steps=0)
    state['last_step'] = step
    if state['day'] != day:
        state['day'] = day; state['unfed'] = []; state['jobs'] = {}
    _O301_REPORT.update(_C373_REPORT)
    if not _O301_ENABLED or day > _O301_MAX_DAY:
        return action
    action = _o301_floor(observation, action, state)
    if state['floor_day'] == day:
        action = _o301_repair(observation, action, state)
    return action

agent.telemetry = _O301_REPORT
kaggle_submission_agent = agent
o301_submission_agent = agent
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    args = ap.parse_args()
    parent = (ROOT / 'agent/c373_structure_retry.py').read_bytes()
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
