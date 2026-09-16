# SPDX-License-Identifier: Apache-2.0
# o161_harvest_only (Claude/o-series, 2026-09-15). Overlay appended to immutable parent agent/c150.py.
"""Harvest-only arm of the 2x2 feed/harvest separation (c150 / feed-only o159b / harvest-only o161 / both o160).
No feed-margin overlay is included; the parent's feed, market, movement and hire policies are untouched.

Behaviour (identical to agent/overlays/o160_goose_harvest.py except the species table and
telemetry prefix): when the parent sends a worker to CARE an animal tile whose yield_units is at
or above the species threshold, that worker's command becomes HARVEST (worker already stands on
the tile). Parent commands that are FEED/HARVEST/PASS/moves and every market order are returned
untouched. No cash, price, opponent, seed or feed conditions are added.

Engine facts: GOOSE max_held 4 with 2 eggs/day when cared+fed, COW/SHEEP max_held 6; production
beyond max_held is silently lost until harvested.

Telemetry (prefix o161_): harvest_swap_requests_<SPECIES>, requested_units_<SPECIES> (units on
the tile at the moment of the request - a REQUEST count, not realised harvest or revenue),
errors. Parent telemetry is preserved.
"""
import copy as _o161_copy

_O161_PARENT = agent
_O161_STATE = {}
_O161_REPORT = {}
_O161_THRESH = {'GOOSE': 3, 'COW': 5, 'SHEEP': 5}
del agent


def _o161_new_state():
    st = {'last': -1, 'errors': 0}
    for kind in _O161_THRESH:
        st['harvest_swap_requests_' + kind] = 0
        st['requested_units_' + kind] = 0
    return st


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O161_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O161_STATE[seat] = _o161_new_state()
    st['last'] = step
    parent_action = _O161_PARENT(observation, configuration)   # exactly one parent call per turn
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
            if not isinstance(tile, dict) or tile.get('animal') not in _O161_THRESH:
                continue
            kind = tile['animal']
            units = int(tile.get('yield_units', 0) or 0)
            if units >= _O161_THRESH[kind]:
                swaps.append((actor, kind, units))
        if swaps:
            result = _o161_copy.deepcopy(parent_action)
            for actor, kind, units in swaps:
                if actor == 0:
                    result['farmer'] = ['HARVEST']
                else:
                    result['hands'][actor - 1] = ['HARVEST']
                st['harvest_swap_requests_' + kind] += 1
                st['requested_units_' + kind] += units
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O161_REPORT.clear()
    _O161_REPORT.update(getattr(_O161_PARENT, 'telemetry', {}))
    _O161_REPORT.update({'o161_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O161_REPORT
agent = globals().pop('agent')
