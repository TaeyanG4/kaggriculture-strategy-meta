
# c173 (GPT/Codex, 2026-09-15): o199c + high-confidence 16-turn physical sale reservation.
# This reuses the c172 visible mirror score but does not require c172's queue
# permutation to be enabled.  It changes only the already-screened R36 sale lead
# horizon, and only when the mirror signal is stronger than the normal c115 gate.
_C173_PARENT = agent
_C173_STATES = {}
_C173_REPORT = {}
_C173_EXISTING_R36 = _r36_reserve
_C173_NATIVE_R36 = globals().get('_C115_NATIVE_R36_RESERVE', _C173_EXISTING_R36)
_C173_SCORE_GATE = 0.970
_C173_STREAK_GATE = 18
_C173_CASH_GAP = 1000.0
_C173_BEHIND_SLACK = 500.0
_C173_HORIZON = 16
del agent


def _c173_update(observation):
    player = int(observation['player']); step = int(observation.get('step', 0))
    state = _C173_STATES.get(player)
    if state is None or step <= state.get('last', -1):
        state = _C173_STATES[player] = {'last': -1, 'streak': 0, 'active': False, 'score': 0.0}
    score = _c172_mirror_score(observation)
    own = float(observation['farms'][player].get('money', 0))
    rival = float(observation['farms'][1-player].get('money', 0))
    gap = own - rival
    similar = score >= _C173_SCORE_GATE and abs(gap) <= _C173_CASH_GAP
    state['streak'] = state['streak'] + 1 if similar else max(0, state['streak'] - 2)
    probe = bool((_R44_PROBES.get(player) or {}).get('matched'))
    state.update(last=step, score=score, gap=gap,
                 active=bool((probe and score >= 0.92 and gap <= _C173_BEHIND_SLACK) or
                             (state['streak'] >= _C173_STREAK_GATE and gap <= _C173_BEHIND_SLACK)))
    return state


def _r36_reserve(observation, action):
    player = int(observation['player']); step = int(observation.get('step', 0))
    state = _C173_STATES.get(player) or {}
    native_horizon = int(_R37_HORIZONS.get(player, 0))
    if not (state.get('active') and 288 <= step < 696 and native_horizon == 8):
        return _C173_EXISTING_R36(observation, action)
    before = {}
    for order in action.get('market', []) or []:
        if len(order) >= 3 and order[0] == 'SELL':
            before[order[1]] = before.get(order[1], 0) + max(0, int(order[2]))
    _R37_HORIZONS[player] = _C173_HORIZON
    try:
        result = _C173_NATIVE_R36(observation, action)
    finally:
        _R37_HORIZONS[player] = native_horizon
    after = {}
    for order in result.get('market', []) or []:
        if len(order) >= 3 and order[0] == 'SELL':
            after[order[1]] = after.get(order[1], 0) + max(0, int(order[2]))
    added = sum(max(0, after.get(item, 0) - before.get(item, 0)) for item in set(before) | set(after))
    _C173_REPORT['c173_horizon16_calls'] += 1
    _C173_REPORT['c173_horizon16_added_units'] += added
    return result


def agent(observation, configuration=None):
    state = _c173_update(observation)
    step = int(observation.get('step', 0))
    if step == 0:
        _C173_REPORT.update(c173_horizon16_calls=0, c173_horizon16_added_units=0, c173_errors=0)
    try:
        result = _C173_PARENT(observation, configuration)
    except Exception:
        _C173_REPORT['c173_errors'] = _C173_REPORT.get('c173_errors', 0) + 1
        raise
    _C173_REPORT.update(getattr(_C173_PARENT, 'telemetry', {}))
    _C173_REPORT.update({
        'c173_mirror_score': round(float(state.get('score', 0.0)), 6),
        'c173_mirror_streak': int(state.get('streak', 0)),
        'c173_mirror_active': int(bool(state.get('active'))),
    })
    return result


agent.telemetry = _C173_REPORT
agent = globals().pop('agent')