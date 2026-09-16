# SPDX-License-Identifier: Apache-2.0
# c179 (GPT/Codex, 2026-09-15): small early tomato lane while preserving V219.
"""Allow o199c's proven V219 SE investment even after c177 planted early tomato.

For the active c177 lane only, qualification is the frozen V219 predicate with
the three 'already have tomato' exclusions removed.  All land/cash/shop/native
route safety gates remain unchanged.  This tests a small early supply tranche as
an addition to the champion regime rather than replacing the champion regime.
"""

_C179_PARENT = agent
_C179_FROZEN_V219_QUALIFIES = _v219_qualifies
_C179_REPORT = {}
del agent


def _c179_v219_qualifies_with_early_tomato(obs, native):
    farm = obs['farms'][obs['player']]
    if len(farm['tiles']) != 10 or set(farm['unlocked_quadrants']) != {'NW', 'NE', 'SW'}:
        return False
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    if sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in obs['town']['unlocked_shops']) < 3:
        return False
    if any(farm['tiles'][y][x] != 'LOCKED' for y in (5, 6) for x in range(5, 10)):
        return False
    for tape in _IMPL.chassis.routes.values():
        for a in tape[432:719]:
            if any(o and o[0] == 'BUY_LAND' for o in a.get('market', [])):
                return False
            if any(c == ['PLANT', 'TOMATO'] for c in [a.get('farmer')] + a.get('hands', [])):
                return False
    return True


def _v219_qualifies(observation, native):
    seat = int(observation.get('player', 0))
    lane = _C177_STATES.get(seat) or {}
    if lane.get('mode') == 'TOMATO' and int(lane.get('plant_units', 0)) > 0:
        return _c179_v219_qualifies_with_early_tomato(observation, native)
    return _C179_FROZEN_V219_QUALIFIES(observation, native)


def agent(observation, configuration=None):
    result = _C179_PARENT(observation, configuration)
    _C179_REPORT.clear()
    _C179_REPORT.update(getattr(_C179_PARENT, 'telemetry', {}))
    seat = int(observation.get('player', 0))
    v219 = _V219_STATES.get(seat) or {}
    _C179_REPORT['c179_v219_eligible'] = int(bool(v219.get('eligible')))
    _C179_REPORT['c179_v219_committed'] = int(bool(v219.get('committed')))
    return result


agent.telemetry = _C179_REPORT
agent = globals().pop('agent')
