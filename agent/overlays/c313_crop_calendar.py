# SPDX-License-Identifier: Apache-2.0
"""Recover remaining tomato yield after its final production, on c177 sites only.

No future replay information, extra movement, labor, fertilizer or field slots.
Existing c177 handles seed choice, carrying and sales; this changes one command.
"""
import copy as _c313_copy

_C313_PARENT = agent
_C313_REPORT = {}
_C313_LAST = {}
del agent


def agent(observation, configuration=None):
    action = _C313_PARENT(observation, configuration)
    seat = int(observation['player'])
    step = int(observation['step'])
    if step <= _C313_LAST.get(seat, -1):
        _C313_REPORT.clear()
    _C313_LAST[seat] = step
    _C313_REPORT.setdefault('c313_harvest_replacements', 0)
    _C313_REPORT.setdefault('c313_requested_units', 0)
    _C313_REPORT.setdefault('c313_errors', 0)
    try:
        state = _C177_STATES.get(seat) or {}
        sites = state.get('sites', set())
        farm = observation['farms'][seat]
        positions = [farm['farmer'], *farm.get('hands', [])]
        commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
        changed = []
        claimed = set()
        for actor, (pos, cmd) in enumerate(zip(positions, commands)):
            xy = tuple(pos)
            if xy not in sites or xy in claimed or cmd[0] not in ('WATER', 'FERTILIZE'):
                continue
            tile = farm['tiles'][pos[1]][pos[0]]
            if not isinstance(tile, dict) or tile.get('crop') != 'TOMATO':
                continue
            # Engine 1.32.7: first at age8; four daily production events, last age11.
            if step // 24 - int(tile['planted_day']) < 11 or tile.get('yield_units', 0) <= 0:
                continue
            claimed.add(xy)
            changed.append(actor)
            _C313_REPORT['c313_requested_units'] += int(tile['yield_units'])
        if changed:
            action = _c313_copy.deepcopy(action)
            for actor in changed:
                if actor == 0:
                    action['farmer'] = ['HARVEST']
                else:
                    action['hands'][actor - 1] = ['HARVEST']
            _C313_REPORT['c313_harvest_replacements'] += len(changed)
    except Exception:
        _C313_REPORT['c313_errors'] += 1
        raise
    _C313_REPORT.update(getattr(_C313_PARENT, 'telemetry', {}))
    return action


agent.telemetry = _C313_REPORT
agent = globals().pop('agent')
