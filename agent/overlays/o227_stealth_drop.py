# o227_stealth_drop (Claude/o-series, 2026-09-16). Stealth pull-forward for the o224 stack.
# V44's race arm escalates (horizon 24 for the rest of the game) the moment it sees us SELL a product at the very turn
# it dropped into the shed while V44 held. Our c115 widening (12 vs the public 8) makes exactly that visible at drop
# turns. Rule: on a turn where our own action PLACEs a race product into the shed (a drop turn, identical for a mirror),
# run the native R36 reservation with horizon 8 (what the public lineage sells too); the 9..12-step pull-forward is
# deferred one turn (still ahead of an 8-horizon mirror) and V44 never observes a lost race. Off outside 288..695.
# Telemetry: o227_stealth_turns.
_O227_ITEMS = ('CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL')
_O227_INNER = _r36_reserve
_O227_NATIVE = _C115_NATIVE_R36_RESERVE
_O227_COUNT = {'turns': 0}
_O227_PARENT = agent
_O227_REPORT = {}
del agent


def _r36_reserve(obs, action):
    step = int(obs['step']); player = int(obs['player'])
    if 288 <= step < 696:
        cmds = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
        if any(len(c) >= 2 and c[0] == 'PLACE' and c[1] in _O227_ITEMS for c in cmds):
            saved = _R37_HORIZONS.get(player); _R37_HORIZONS[player] = 8
            _O227_COUNT['turns'] += 1
            try:
                return _O227_NATIVE(obs, action)
            finally:
                if saved is None: _R37_HORIZONS.pop(player, None)
                else: _R37_HORIZONS[player] = saved
    return _O227_INNER(obs, action)


def agent(observation, configuration=None):
    if int(observation.get('step', 0)) == 0:
        _O227_COUNT['turns'] = 0
    result = _O227_PARENT(observation, configuration)
    _O227_REPORT.clear()
    _O227_REPORT.update(getattr(_O227_PARENT, 'telemetry', {}))
    _O227_REPORT['o227_stealth_turns'] = _O227_COUNT['turns']
    return result


agent.telemetry = _O227_REPORT
agent = globals().pop('agent')
