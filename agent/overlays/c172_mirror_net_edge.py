
# c172 (GPT/Codex, 2026-09-15): o199c + high-confidence mirror execution edge.
# Macro policy is untouched.  This layer only permutes an all-SELL queue when
# the rival remains visibly near-identical for a sustained window (or the
# inherited cash-response probe has already confirmed a mirror).  The model
# simulates Kaggriculture's exact per-unit lockstep market and maximizes our
# revenue minus the assumed mirror rival's revenue, with a midgame own-cash
# floor so a tiny denial edge cannot starve later obligations.
_C172_PARENT = agent
_C172_STATES = {}
_C172_REPORT = {}
_C172_ENABLE_REORDER = True
_C172_MIN_STEP = 336
_C172_MAX_STEP = 695
_C172_SCORE_GATE = 0.960
_C172_STREAK_GATE = 12
_C172_CASH_GAP = 1500.0
_C172_BEHIND_SLACK = 750.0
_C172_EDGE_GAIN = 25.0
_C172_OWN_FLOOR = -25.0
_C172_MAX_ASCENT = 10
del agent


def _c172_count_farm(farm):
    counts = {}
    for row in farm.get('tiles', []):
        for tile in row:
            if not isinstance(tile, dict):
                continue
            animal = tile.get('animal')
            crop = tile.get('crop')
            if animal:
                key = 'A:' + str(animal)
                counts[key] = counts.get(key, 0) + 1
            if crop:
                key = 'C:' + str(crop)
                counts[key] = counts.get(key, 0) + 1
    return counts


def _c172_composition_similarity(left, right):
    a = _c172_count_farm(left); b = _c172_count_farm(right)
    keys = set(a) | set(b)
    denom = sum(max(a.get(k, 0), b.get(k, 0)) for k in keys)
    if denom <= 0:
        return 0.0
    diff = sum(abs(a.get(k, 0) - b.get(k, 0)) for k in keys)
    return max(0.0, 1.0 - diff / float(denom))


def _c172_stage_similarity(left, right):
    checks = matches = 0
    ltiles = [t for row in left.get('tiles', []) for t in row]
    rtiles = [t for row in right.get('tiles', []) for t in row]
    for a, b in zip(ltiles, rtiles):
        if not isinstance(a, dict) or not isinstance(b, dict):
            continue
        if (a.get('crop'), a.get('animal')) != (b.get('crop'), b.get('animal')):
            continue
        if not (a.get('crop') or a.get('animal')):
            continue
        for key in ('planted_day', 'placed_day', 'yield_units', 'watered_today',
                    'fed_today', 'cared_today', 'fertilizer_available',
                    'consecutive_unfed', 'fertilized_until_day'):
            if key not in a and key not in b:
                continue
            checks += 1
            matches += int(a.get(key) == b.get(key))
    return matches / float(checks) if checks else 0.0


def _c172_mirror_score(observation):
    player = int(observation['player']); rival = 1 - player
    own = observation['farms'][player]; other = observation['farms'][rival]
    if own.get('unlocked_quadrants') != other.get('unlocked_quadrants'):
        return 0.0
    layout = float(_r37_similarity(observation))
    comp = _c172_composition_similarity(own, other)
    stage = _c172_stage_similarity(own, other)
    workers = 1.0 if len(own.get('hands', [])) == len(other.get('hands', [])) else 0.0
    return 0.55 * layout + 0.25 * comp + 0.15 * stage + 0.05 * workers


def _c172_update_state(observation):
    player = int(observation['player']); step = int(observation.get('step', 0))
    state = _C172_STATES.get(player)
    if state is None or step <= state.get('last', -1):
        state = _C172_STATES[player] = {
            'last': -1, 'streak': 0, 'score': 0.0, 'active': False,
            'probe': False, 'gap': 0.0, 'peak_streak': 0,
        }
    own = observation['farms'][player]; rival = observation['farms'][1-player]
    score = _c172_mirror_score(observation)
    gap = float(own.get('money', 0)) - float(rival.get('money', 0))
    similar = score >= _C172_SCORE_GATE and abs(gap) <= _C172_CASH_GAP
    state['streak'] = state['streak'] + 1 if similar else max(0, state['streak'] - 2)
    state['peak_streak'] = max(state['peak_streak'], state['streak'])
    probe = bool((_R44_PROBES.get(player) or {}).get('matched'))
    confirmed = probe and score >= 0.90 and abs(gap) <= max(2500.0, _C172_CASH_GAP)
    state.update(last=step, score=score, gap=gap, probe=probe,
                 active=bool(confirmed or state['streak'] >= _C172_STREAK_GATE))
    return state


def _c172_market_revenues(observation, own_orders, rival_orders, own_stock, rival_stock):
    inventory = dict(observation['market']['inventory'])
    params = {item: dict(values) for item, values in _R37_MARKET_PARAMS.items()}
    for item, patch in observation['market'].get('params', {}).items():
        if item in params:
            params[item].update(patch)
    stocks = [dict(own_stock), dict(rival_stock)]
    revenues = [0.0, 0.0]
    max_len = max(len(own_orders), len(rival_orders))
    for index in range(max_len):
        rows = []
        for orders in (own_orders, rival_orders):
            if index >= len(orders):
                rows.append(None); continue
            order = orders[index]
            if (not order or len(order) < 3 or order[0] != 'SELL' or
                    order[1] not in PRODUCTS):
                rows.append(None); continue
            rows.append([order[1], max(0, int(order[2]))])
        while any(row is not None and row[1] > 0 for row in rows):
            quoted = [None, None]
            for side, row in enumerate(rows):
                if row is None or row[1] <= 0:
                    continue
                item = row[0]
                if int(stocks[side].get(item, 0)) <= 0:
                    row[1] = 0; continue
                quoted[side] = (item, _r37_market_price(item, inventory[item], params))
            if quoted == [None, None]:
                break
            for side, quote in enumerate(quoted):
                if quote is None:
                    continue
                item, price = quote
                revenues[side] += price
                stocks[side][item] = max(0, int(stocks[side].get(item, 0)) - 1)
                rows[side][1] -= 1
                if price > 1:
                    inventory[item] = int(inventory.get(item, 0)) + 1
    return revenues[0], revenues[1]


def _c172_reorder(observation, action, state):
    if not _C172_ENABLE_REORDER or not state.get('active'):
        return action
    step = int(observation.get('step', 0))
    if not (_C172_MIN_STEP <= step <= _C172_MAX_STEP):
        return action
    player = int(observation['player']); rival = 1 - player
    own_money = float(observation['farms'][player].get('money', 0))
    rival_money = float(observation['farms'][rival].get('money', 0))
    if own_money > rival_money + _C172_BEHIND_SLACK:
        _C172_REPORT['c172_ahead_declines'] += 1
        return action
    orders = [list(order) for order in (action.get('market') or [])]
    if (len(orders) < 2 or len({o[1] for o in orders if len(o) >= 3}) < 2 or
            any(not o or len(o) < 3 or o[0] != 'SELL' or o[1] not in PRODUCTS or
                type(o[2]) is not int or o[2] <= 0 for o in orders)):
        return action
    stock = projected_shed(action, FarmView(observation))
    if not any(int(stock.get(o[1], 0)) > 0 for o in orders):
        return action
    rival_orders = [list(o) for o in orders]
    rival_stock = dict(stock)  # only under confirmed/high-confidence mirror mode
    base_own, base_rival = _c172_market_revenues(
        observation, orders, rival_orders, stock, rival_stock)
    base_edge = base_own - base_rival
    current = [list(o) for o in orders]
    best_own, best_rival, best_edge = base_own, base_rival, base_edge
    for _ in range(_C172_MAX_ASCENT):
        choice = None
        for left in range(len(current)):
            for right in range(left + 1, len(current)):
                if current[left] == current[right]:
                    continue
                trial = [list(o) for o in current]
                trial[left], trial[right] = trial[right], trial[left]
                own_rev, rival_rev = _c172_market_revenues(
                    observation, trial, rival_orders, stock, rival_stock)
                edge = own_rev - rival_rev
                rank = (edge, own_rev)
                if rank > (best_edge, best_own):
                    choice = (trial, own_rev, rival_rev, edge)
                    best_own, best_rival, best_edge = own_rev, rival_rev, edge
        if choice is None:
            break
        current, best_own, best_rival, best_edge = choice
    edge_gain = best_edge - base_edge
    own_delta = best_own - base_own
    if (edge_gain < _C172_EDGE_GAIN or own_delta < _C172_OWN_FLOOR or current == orders):
        if edge_gain > 0:
            _C172_REPORT['c172_gain_declines'] += 1
        return action
    result = copy.deepcopy(action)
    result['market'] = current
    _C172_REPORT['c172_reorders'] += 1
    _C172_REPORT['c172_modeled_edge_gain'] += edge_gain
    _C172_REPORT['c172_modeled_own_delta'] += own_delta
    return result


def agent(observation, configuration=None):
    state = _c172_update_state(observation)
    result = _C172_PARENT(observation, configuration)
    try:
        step = int(observation.get('step', 0))
        if step == 0:
            _C172_REPORT.update(
                c172_reorders=0, c172_modeled_edge_gain=0.0,
                c172_modeled_own_delta=0.0, c172_ahead_declines=0,
                c172_gain_declines=0, c172_errors=0,
            )
        standard = configuration is None or all(configuration.get(k, v) == v for k, v in (
            ('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100),
            ('maxMarketOrdersPerTurn', 10), ('farmHandCostMult', 1)))
        if standard:
            result = _c172_reorder(observation, result, state)
    except Exception:
        _C172_REPORT['c172_errors'] = _C172_REPORT.get('c172_errors', 0) + 1
        result = result
    _C172_REPORT.update(getattr(_C172_PARENT, 'telemetry', {}))
    _C172_REPORT.update({
        'c172_mirror_score': round(float(state.get('score', 0.0)), 6),
        'c172_mirror_streak': int(state.get('streak', 0)),
        'c172_mirror_peak_streak': int(state.get('peak_streak', 0)),
        'c172_mirror_active': int(bool(state.get('active'))),
        'c172_probe_confirmed': int(bool(state.get('probe'))),
        'c172_cash_gap': float(state.get('gap', 0.0)),
    })
    return result


agent.telemetry = _C172_REPORT
agent = globals().pop('agent')