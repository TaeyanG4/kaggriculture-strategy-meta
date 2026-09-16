# SPDX-License-Identifier: Apache-2.0
# c180 (GPT/Codex, 2026-09-15): guarded two-tile early tomato addition.
"""Production selector learned from the first paired falsification panel.

Use exactly two native late-strawberry slots for early TOMATO only when current
observed tomato demand is present and the same observation does not already have
two or more strawberry-consuming shops.  The latter state was the consistent
negative slice in c179; KEEP remains exact o199c there.
"""

_C180_ORIGINAL_C177_DECIDE = _c177_decide
if _C177_SIZE_OVERRIDE == 0:
    _C177_SIZE_OVERRIDE = 2


def _c180_strawberry_demand(observation):
    shops = observation.get('town', {}).get('unlocked_shops', []) or []
    return sum(shop in ('BRUNCH_SPOT', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP', 'FARMERS_MARKET') for shop in shops)


def _c177_decide(observation, action, state):
    # Explicit force remains a local experiment hook and bypasses this learned
    # economic guard.  Production/AUTO never sees it.
    if (state.get('mode') is None and _C177_FORCE != 'TOMATO'
            and _C177_DECISION_START <= int(observation.get('step', 0)) < _C177_DECISION_END
            and _c177_has_strawberry_seed(action)
            and _c180_strawberry_demand(observation) >= 2):
        state['counts']['decisions'] += 1
        state['mode'] = 'KEEP'
        return
    return _C180_ORIGINAL_C177_DECIDE(observation, action, state)


_C180_PARENT = agent
_C180_REPORT = {}
del agent


def agent(observation, configuration=None):
    result = _C180_PARENT(observation, configuration)
    _C180_REPORT.clear()
    _C180_REPORT.update(getattr(_C180_PARENT, 'telemetry', {}))
    seat = int(observation.get('player', 0))
    state = _C177_STATES.get(seat) or {}
    _C180_REPORT['c180_strawberry_guard'] = int(state.get('mode') == 'KEEP' and _c180_strawberry_demand(observation) >= 2)
    return result


agent.telemetry = _C180_REPORT
agent = globals().pop('agent')
