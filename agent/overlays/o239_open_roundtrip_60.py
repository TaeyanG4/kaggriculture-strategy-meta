# o238 variant with a 60-unit pair (o239 family, 2026-09-17). Turn-0 market hardening against the public V45 opening arm.
# Our tape opens with [BUY WHEAT 13, BUY WHEAT 10, SELL WHEAT 30] (net 0 wheat, -$7). V45 plays [BUY 70, SELL 70] as one
# pair in the same turn; the per-unit lockstep quoting makes our SECOND buy ~$53 dearer, our strictly funded day-0 plan
# then plants 11 melons instead of 12 (measured: vs V45 22/32 wins, vs V44 30/32). A single buy/sell pair is neutral vs
# the market and vs itself, and inflicts the same shortfall on split-buy openings (our own mirrors included).
# KAGG_O238_UNITS sets the pair size (default 70). Nothing else changes. Telemetry o238_turns, o238_errors.
import os as _o238_os
_O238_PARENT = agent
_O238_UNITS = int(_o238_os.environ.get('KAGG_O238_UNITS', '60') or 60)
_O238_SPLIT = [['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 10], ['SELL', 'WHEAT', 30]]
_O238_REPORT = {'o238_turns': 0, 'o238_errors': 0}
del agent


def agent(observation, configuration=None):
    action = _O238_PARENT(observation, configuration)
    try:
        step = int(observation.get('step', 0))
        if step == 0:
            _O238_REPORT.update(o238_turns=0, o238_errors=0)
            if action.get('market') == _O238_SPLIT:
                action = dict(action, market=[['BUY_PRODUCT', 'WHEAT', _O238_UNITS], ['SELL', 'WHEAT', _O238_UNITS]])
                _O238_REPORT['o238_turns'] += 1
    except Exception:
        _O238_REPORT['o238_errors'] += 1
    _O238_REPORT.update(getattr(_O238_PARENT, 'telemetry', {}))
    return action


agent.telemetry = _O238_REPORT
agent = globals().pop('agent')
