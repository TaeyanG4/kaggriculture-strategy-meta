# SPDX-License-Identifier: Apache-2.0
# Original project addition, 2026-09-12. Appended to the frozen public V37.
# Reuse its attributed exact unit model; never inspect the evaluator or rival private state.
_C102_PARENT = agent
_C102_REPORT = {}
_C102_ENABLED = True


def _c102_future_feed(tape, step, actor):
    needed = 0
    for t in range(step + 1, min((step // 24 + 1) * 24, 719)):
        a = tape[t]
        commands = [a.get('farmer') or ['PASS']] + list(a.get('hands') or [])
        c = commands[actor] if actor < len(commands) else ['PASS']
        if c[0] == 'DROP' or c[:2] in (['PICKUP', 'WHEAT'], ['PLACE', 'WHEAT']):
            break
        if c[0] == 'FEED':
            needed += 1
    return needed


def _c102_repair(obs, action):
    step = int(obs['step'])
    if step >= 696:
        return action
    player = int(obs['player'])
    day = step // 24
    farm, private = copy.deepcopy((obs['farms'][player], obs['private']))
    commands = [list(action.get('farmer') or ['PASS'])] + [list(c) for c in action.get('hands', [])]
    native = _IMPL.chassis.players[player]
    tape = _IMPL.chassis.routes[native['route']]
    owned_elsewhere = set()
    for states in (_V219_STATES, _V233_STATES, _R51_INPUT_STATES):
        owned_elsewhere.update(states.get(player, {}).get('workers', {}))
    changed = False
    # Sequential actor simulation prevents two workers reserving the same grain.
    apply_unit = _UNIT_NS['_apply_unit_action']
    for actor, command in enumerate(commands[:len(farm['hands']) + 1]):
        before = copy.deepcopy((farm, private))
        apply_unit(farm, private, actor, command, 10, day, 24, 100)
        if (farm, private) != before or actor in owned_elsewhere:
            continue
        pos = farm['farmer'] if actor == 0 else farm['hands'][actor - 1]
        x, y = pos
        inv = private['inventories'][actor]
        tile = farm['tiles'][y][x]
        replacement = None
        if isinstance(tile, dict) and tile.get('animal'):
            if not tile.get('fed_today') and inv.get('WHEAT', 0):
                replacement = ['FEED']
            elif not tile.get('cared_today'):
                replacement = ['CARE']
            elif tile.get('fertilizer_available'):
                replacement = ['COLLECT_FERTILIZER']
        elif isinstance(tile, dict) and tile.get('kind') == 'PLANT' and day < 29:
            if not tile.get('watered_today'):
                replacement = ['WATER']
        if replacement is None and _shed_adjacent(pos, 10):
            needed = _c102_future_feed(tape, step, actor) - inv.get('WHEAT', 0)
            stock = private['shed'].get('WHEAT', 0)
            if needed > 0 and stock > 0:
                replacement = ['PICKUP', 'WHEAT', min(needed, stock)]
            else:
                cargo = [item for item in PRODUCTS if item not in ('WHEAT', 'FERTILIZER') and inv.get(item, 0)]
                if cargo and sum(private['shed'].values()) < 100:
                    item = max(cargo, key=lambda p: inv[p] * obs['market']['prices'].get(p, 0))
                    replacement = ['PLACE', item, inv[item]]
        if replacement is not None:
            apply_unit(farm, private, actor, replacement, 10, day, 24, 100)
            if (farm, private) != before:
                commands[actor] = replacement
                changed = True
                key = 'repair_' + replacement[0].lower()
                _C102_REPORT[key] = _C102_REPORT.get(key, 0) + 1
    if changed:
        action = dict(action, farmer=commands[0], hands=commands[1:])
    return action


def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _C102_REPORT.clear()
        _C102_REPORT['repair_errors'] = 0
    result = _C102_PARENT(observation, configuration)
    if _C102_ENABLED:
        try:
            result = _c102_repair(observation, result)
        except Exception:
            _C102_REPORT['repair_errors'] += 1
    _C102_REPORT.update(getattr(_C102_PARENT, 'telemetry', {}))
    return result


agent.telemetry = _C102_REPORT
agent = globals().pop('agent')
