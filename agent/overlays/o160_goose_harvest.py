# SPDX-License-Identifier: Apache-2.0
# o160_goose_harvest (Claude/o-series, 2026-09-15). Overlay appended after o159 (parent untouched).
"""Cap-loss rescue for animals: GOOSE max_held is 4 and a cared+fed goose produces 2 eggs/day, so
a goose not harvested every ~2 days silently wastes production. Live audit: our tape leaves geese
at the cap 7.7 goose-days/game (leader: 0.1), ~15 eggs (~$750) lost per game.

Rule: when the tape sends a worker to CARE an animal tile whose yield_units >= threshold
(GOOSE 3, COW/SHEEP 5), replace CARE with HARVEST (worker is already standing on the tile; CARE's
value is +1 pending unit later, HARVEST rescues 3-6 units now). Harvested units ride in the
worker's inventory and reach the shed through the tape's own DROP / end-of-day drop.
Never touches FEED, moves, or market orders.
"""
import copy as _o160_copy

_O160_PARENT = agent
_O160_STATE = {}
_O160_REPORT = {}
_O160_THRESH = {'GOOSE': 3, 'COW': 5, 'SHEEP': 5}
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O160_STATE.get(seat)
    if st is None or step <= st['last']:
        st = {'last': -1, 'harvest_swaps': 0, 'units': 0, 'errors': 0}
        _O160_STATE[seat] = st
    st['last'] = step
    parent_action = _O160_PARENT(observation, configuration)
    result = parent_action
    try:
        farm = observation['farms'][seat]
        positions = [farm['farmer'], *farm['hands']]
        commands = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
        swaps = []
        for actor, command in enumerate(commands[:len(positions)]):
            if command != ['CARE']:
                continue
            x, y = positions[actor]
            tile = farm['tiles'][y][x]
            if not isinstance(tile, dict) or tile.get('animal') not in _O160_THRESH:
                continue
            units = int(tile.get('yield_units', 0) or 0)
            if units >= _O160_THRESH[tile['animal']]:
                swaps.append((actor, units))
        if swaps:
            result = _o160_copy.deepcopy(parent_action)
            for actor, units in swaps:
                if actor == 0:
                    result['farmer'] = ['HARVEST']
                else:
                    result['hands'][actor - 1] = ['HARVEST']
                st['harvest_swaps'] += 1; st['units'] += units
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O160_REPORT.clear()
    _O160_REPORT.update(getattr(_O160_PARENT, 'telemetry', {}))
    _O160_REPORT.update({'o160_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O160_REPORT
agent = globals().pop('agent')
