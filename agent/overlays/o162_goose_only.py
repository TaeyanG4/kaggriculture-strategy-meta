# SPDX-License-Identifier: Apache-2.0
# o162_goose_only (Claude/o-series, 2026-09-15). Overlay appended to immutable parent agent/o159b_feed_margin06.py.
"""Goose-only harvest arm on top of o159b (feed-margin 0.6 and all its feed conditions unchanged).
COW and SHEEP CARE commands are returned exactly as the parent proposes; only GOOSE tiles at
yield_units >= 3 are switched from CARE to HARVEST.

Behaviour (identical to agent/overlays/o160_goose_harvest.py except the species table and
telemetry prefix): when the parent sends a worker to CARE an animal tile whose yield_units is at
or above the species threshold, that worker's command becomes HARVEST (worker already stands on
the tile). Parent commands that are FEED/HARVEST/PASS/moves and every market order are returned
untouched. No cash, price, opponent, seed or feed conditions are added.

Engine facts: GOOSE max_held 4 with 2 eggs/day when cared+fed, COW/SHEEP max_held 6; production
beyond max_held is silently lost until harvested.

Telemetry (prefix o162_): harvest_swap_requests_<SPECIES>, requested_units_<SPECIES> (units on
the tile at the moment of the request - a REQUEST count, not realised harvest or revenue),
errors. Parent telemetry is preserved.
"""
import copy as _o162_copy

_O162_PARENT = agent
_O162_STATE = {}
_O162_REPORT = {}
_O162_THRESH = {'GOOSE': 3}
del agent


def _o162_new_state():
    st = {'last': -1, 'errors': 0}
    for kind in _O162_THRESH:
        st['harvest_swap_requests_' + kind] = 0
        st['requested_units_' + kind] = 0
    return st


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O162_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O162_STATE[seat] = _o162_new_state()
    st['last'] = step
    parent_action = _O162_PARENT(observation, configuration)   # exactly one parent call per turn
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
            if not isinstance(tile, dict) or tile.get('animal') not in _O162_THRESH:
                continue
            kind = tile['animal']
            units = int(tile.get('yield_units', 0) or 0)
            if units >= _O162_THRESH[kind]:
                swaps.append((actor, kind, units))
        if swaps:
            result = _o162_copy.deepcopy(parent_action)
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
    _O162_REPORT.clear()
    _O162_REPORT.update(getattr(_O162_PARENT, 'telemetry', {}))
    _O162_REPORT.update({'o162_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O162_REPORT
agent = globals().pop('agent')
