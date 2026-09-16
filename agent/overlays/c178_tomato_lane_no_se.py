# SPDX-License-Identifier: Apache-2.0
# c178 (GPT/Codex, 2026-09-15): c177 lane plus V219-SE replacement.
"""If the native strawberry lane was converted to TOMATO, do not also buy SE.

This turns the experiment into the intended portfolio substitution:
existing-land STRAWBERRY -> TOMATO replaces V219's later $4,000 SE+TOMATO
investment rather than stacking with it.
"""

_C178_PARENT = agent
_C178_ORIGINAL_V219_QUALIFIES = _v219_qualifies
_C178_REPORT = {}
del agent


def _v219_qualifies(observation, native):
    seat = int(observation.get('player', 0))
    lane = _C177_STATES.get(seat) or {}
    if lane.get('mode') == 'TOMATO' and int(lane.get('plant_units', 0)) > 0:
        return False
    return _C178_ORIGINAL_V219_QUALIFIES(observation, native)


def agent(observation, configuration=None):
    result = _C178_PARENT(observation, configuration)
    _C178_REPORT.clear()
    _C178_REPORT.update(getattr(_C178_PARENT, 'telemetry', {}))
    seat = int(observation.get('player', 0))
    lane = _C177_STATES.get(seat) or {}
    v219 = _V219_STATES.get(seat) or {}
    _C178_REPORT['c178_lane_tomato'] = int(lane.get('mode') == 'TOMATO')
    _C178_REPORT['c178_v219_committed'] = int(bool(v219.get('committed')))
    return result


agent.telemetry = _C178_REPORT
agent = globals().pop('agent')
