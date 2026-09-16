# o180_c155_gate (Claude/o-series, 2026-09-15). c155's milk-externality feed-skip gate stacked on o162.
# o159 already skips low-value feeds (never when consecutive_unfed == 1); c155 adds cow non-production-night
# skips priced with the rival's milk exposure. Test: do the two skip rules compound or conflict?
# SPDX-License-Identifier: Apache-2.0
"""c155: c132-style non-production-night cow feed skip, gated by a public milk-price externality.

Scope (unchanged from c132): only FEED actions the parent already proposes, on a mature COW
(age >= 0 where age = day + 1 - placed_day - 8), on a NON-production night (age % 2 == 1), not
fed today, consecutive_unfed == 0, and the acting worker actually carries WHEAT. Immature cows,
production nights, cows already one day unfed, other animals, purchases, hires, movement, crops
and sales are never touched. Allowed FEEDs become PASS; nothing is added.

Engine semantics (kaggle_environments 1.32.7, _daily_refresh_animals): a cow produces every
2nd night whether or not it was fed; feeding only (a) resets consecutive_unfed (escape at >= 2)
and (b) lets the care bonus accrue (cared AND fed -> pending_care_bonus + 1) and be consumed
(fed on a production night -> yield += 1 + pending). Skipping one non-production-night feed
therefore forgoes at most ONE future MILK unit (the pending bonus that day's care would have
banked), provided the tape feeds the cow on the following production night (it must, and the
consecutive_unfed == 0 gate guarantees the animal cannot escape from this single skip). c155
charges OWN_LOSS_UNITS = 2 as c132 did: a deliberately conservative over-estimate.

Externality (the new part, after state/parallel-handoffs/collaboration-20260915/
c132-market-externality/report.md): our skip lowers future MILK supply by SHOCK_UNITS, which
raises the public MILK price by delta_p = price(inv - SHOCK) - price(inv) on the engine curve
(local shock only; NO cumulative cross-turn subtraction and NO 4-day shop-demand stress, unlike
c135 - the current inventory already reflects every earlier realized skip). The rival can
monetize that rise only on milk it visibly holds: rival_exposure = (yield_units on rival COW
tiles) + RIVAL_DUE_UNITS * (rival cows producing tonight, from public placed_day). Nothing
private (rival shed, inventories, future actions) is assumed. Only ATTRIBUTION (50%) of the
nominal exposure gain is charged to this skip, plus a BUFFER of 5 cash.

    wheat_saved_value      = WHEAT_REALIZATION * wheat_price          (c132: 0.8 * wheat)
    own_production_loss    = OWN_LOSS_UNITS * max MILK price of the last 24 steps (c132 rule)
    opponent_price_gain    = ATTRIBUTION * rival_exposure * delta_p
    estimated_relative_gain = wheat_saved_value - own_production_loss - opponent_price_gain - BUFFER
    allow_skip             = estimated_relative_gain >= 0

Within one turn, an earlier allowed skip's supply reduction is carried in committed_skips so the
next candidate is priced at inventory - SHOCK_UNITS * committed_skips (no double use of the
same market headroom). All coefficients are development values from the report; they are NOT
validated optima and this whole estimate is an approximation, not a profit guarantee. Only
counters are kept in memory (no per-turn logs); detailed diagnostics belong to the separate
shadow tool tools/c155_shadow.py.

Modes: _C155_APPLY = True (submission default) changes allowed FEEDs; False (observe-only)
evaluates and counts identically but always returns the parent action unchanged. Use
_c155_set_mode('observe'|'apply') or the build script's --observe variant.
"""
import copy as _c155_copy

_C155_PARENT = agent
_C155_STATES = {}
_C155_REPORT = {}
_C155_APPLY = True
_C155_WINDOW = (336, 672)          # c132 window: skips considered for 336 <= step < 672
_C155_WHEAT_REALIZATION = 0.8      # saved wheat credited at 80% of the current WHEAT price (c132)
_C155_OWN_LOSS_UNITS = 2           # MILK units charged per skip (engine-exact <= 1; conservative)
_C155_SHOCK_UNITS = 2              # supply reduction used for the local price-shock estimate
_C155_RIVAL_DUE_UNITS = 2          # units credited per rival cow producing tonight (base 1 + bonus 1)
_C155_ATTRIBUTION = 0.5            # share of the nominal rival exposure gain charged to this skip
_C155_BUFFER = 5.0                 # cash-equivalent uncertainty buffer per skip
_C155_REQUIRED_CONFIG = (('boardSize', 10), ('turnsPerDay', 24), ('townShopSellInterval', 4),
                         ('townCenterSellInterval', 24))
del agent


def _c155_set_mode(mode):
    """'apply' changes allowed feeds; 'observe' only evaluates/counts."""
    global _C155_APPLY
    if mode not in ('apply', 'observe'):
        raise ValueError(mode)
    _C155_APPLY = (mode == 'apply')
    return _C155_APPLY


def _c155_supported(configuration):
    if configuration is None:
        return True
    try:
        return all(configuration.get(key, value) == value for key, value in _C155_REQUIRED_CONFIG)
    except Exception:
        return False


def _c155_cow_age(tile, day):
    """Nights since first production; production nights have age % 2 == 0."""
    return day + 1 - int(tile.get('placed_day', 0)) - 8


def _c155_candidates(observation, parent_action):
    """Actors whose parent FEED is a c132-scope cow feed. Returns [(actor, x, y)]."""
    seat = int(observation['player'])
    day = int(observation['step']) // 24
    farm = observation['farms'][seat]
    inventories = observation['private']['inventories']
    positions = [farm['farmer'], *farm['hands']]
    commands = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
    out = []
    for actor, (pos, cmd) in enumerate(zip(positions, commands)):
        if cmd != ['FEED'] or actor >= len(inventories) or int(inventories[actor].get('WHEAT', 0)) < 1:
            continue
        x, y = pos
        tile = farm['tiles'][y][x]
        if not isinstance(tile, dict) or tile.get('animal') != 'COW' or tile.get('fed_today'):
            continue
        if int(tile.get('consecutive_unfed', 0) or 0) != 0:
            continue
        age = _c155_cow_age(tile, day)
        if age < 0 or age % 2 == 0:
            continue
        out.append((actor, x, y))
    return out


def _c155_rival_exposure(observation):
    """Publicly visible rival milk that a price rise could benefit: held yield + tonight's due."""
    seat = int(observation['player'])
    day = int(observation['step']) // 24
    rival = observation['farms'][1 - seat]
    ready = 0
    due = 0
    for row in rival.get('tiles', []) or []:
        for tile in row or []:
            if not isinstance(tile, dict) or tile.get('animal') != 'COW':
                continue
            ready += int(tile.get('yield_units', 0) or 0)
            age = _c155_cow_age(tile, day)
            if age >= 0 and age % 2 == 0:
                due += 1
    return ready, due, ready + _C155_RIVAL_DUE_UNITS * due


def _c155_market_params(observation):
    """Engine price parameters with any per-item patches published in the observation (as
    c150's _r37_quote_priority does); falls back to the frozen table."""
    params = {key: dict(value) for key, value in _R37_MARKET_PARAMS.items()}
    try:
        for key, patch in (observation['market'].get('params') or {}).items():
            if key in params and isinstance(patch, dict):
                params[key].update(patch)
    except Exception:
        pass
    return params


def evaluate_feed_skip(observation, actor, committed_skips, recent_max_milk=None):
    """Economic judgement for skipping the parent's FEED of `actor` (a c132-scope cow feed).

    committed_skips: skips already allowed earlier in this same turn; their supply reduction is
    applied before pricing this one. recent_max_milk: max MILK price of the last 24 steps
    (None -> cannot evaluate, keep the feed). Returns a dict; approximation, not a guarantee.
    """
    prices = observation['market']['prices']
    wheat = float(prices['WHEAT'])
    result = dict(allow_skip=False, reason='', wheat_saved_value=0.0, own_production_loss=0.0,
                  opponent_price_gain=0.0, uncertainty_buffer=_C155_BUFFER, estimated_relative_gain=0.0,
                  delta_p=0.0, rival_ready=0, rival_due=0)
    if recent_max_milk is None:
        result['reason'] = 'price_history'
        return result
    wheat_saved = _C155_WHEAT_REALIZATION * wheat
    own_loss = _C155_OWN_LOSS_UNITS * float(recent_max_milk)
    result.update(wheat_saved_value=wheat_saved, own_production_loss=own_loss)
    if wheat_saved - own_loss <= 0:
        result['reason'] = 'gross_edge'
        result['estimated_relative_gain'] = wheat_saved - own_loss - _C155_BUFFER
        return result
    inventory = int(observation['market']['inventory']['MILK']) - _C155_SHOCK_UNITS * int(committed_skips)
    params = _c155_market_params(observation)
    p_now = _r37_market_price('MILK', inventory, params)
    p_shock = _r37_market_price('MILK', inventory - _C155_SHOCK_UNITS, params)
    delta_p = max(0.0, float(p_shock - p_now))
    ready, due, exposure = _c155_rival_exposure(observation)
    opp_gain = _C155_ATTRIBUTION * exposure * delta_p
    gain = wheat_saved - own_loss - opp_gain - _C155_BUFFER
    result.update(opponent_price_gain=opp_gain, estimated_relative_gain=gain, delta_p=delta_p,
                  rival_ready=ready, rival_due=due)
    if gain >= 0:
        result.update(allow_skip=True, reason='allow')
    else:
        result['reason'] = 'externality'
    return result


def _c155_evaluate_turn(observation, parent_action, recent_max_milk):
    """Run the gate over every candidate in turn order; returns (decisions, committed)."""
    decisions = []
    committed = 0
    for actor, x, y in _c155_candidates(observation, parent_action):
        ev = evaluate_feed_skip(observation, actor, committed, recent_max_milk)
        ev.update(actor=actor, x=x, y=y)
        if ev['allow_skip']:
            committed += 1
        decisions.append(ev)
    return decisions, committed


def _c155_new_state():
    return {'last': -1, 'prices': [], 'reviewed': 0, 'allowed': 0, 'blocked': 0,
            'blocked_reasons': {}, 'wheat_saved_sum': 0.0, 'own_loss_sum': 0.0, 'opp_gain_sum': 0.0,
            'max_committed_turn': 0, 'unsupported': 0, 'errors': 0, 'applied': 0}


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    state = _C155_STATES.get(seat)
    if state is None or step <= state['last']:
        state = _C155_STATES[seat] = _c155_new_state()
    state['last'] = step
    try:
        milk_now = observation['market']['prices']['MILK']
        state['prices'].append((step, milk_now))
        state['prices'] = [row for row in state['prices'] if row[0] >= step - 23]
    except Exception:
        state['errors'] += 1
    parent = _C155_PARENT(observation, configuration)
    result = parent
    try:
        if not _c155_supported(configuration):
            state['unsupported'] += 1
        elif _C155_WINDOW[0] <= step < _C155_WINDOW[1]:
            recent = max(p for _, p in state['prices']) if len(state['prices']) == 24 else None
            decisions, committed = _c155_evaluate_turn(observation, parent, recent)
            state['max_committed_turn'] = max(state['max_committed_turn'], committed)
            for ev in decisions:
                state['reviewed'] += 1
                if ev['allow_skip']:
                    state['allowed'] += 1
                    state['wheat_saved_sum'] += ev['wheat_saved_value']
                    state['own_loss_sum'] += ev['own_production_loss']
                    state['opp_gain_sum'] += ev['opponent_price_gain']
                else:
                    state['blocked'] += 1
                    state['blocked_reasons'][ev['reason']] = state['blocked_reasons'].get(ev['reason'], 0) + 1
            if _C155_APPLY and committed:
                result = _c155_copy.deepcopy(parent)
                for ev in decisions:
                    if not ev['allow_skip']:
                        continue
                    if ev['actor'] == 0:
                        result['farmer'] = ['PASS']
                    else:
                        result['hands'][ev['actor'] - 1] = ['PASS']
                    state['applied'] += 1
    except Exception:
        state['errors'] += 1
        result = parent
    _C155_REPORT.clear()
    _C155_REPORT.update(getattr(_C155_PARENT, 'telemetry', {}))
    _C155_REPORT.update({
        'milk_externality_mode': 'apply' if _C155_APPLY else 'observe',
        'milk_externality_reviewed': state['reviewed'],
        'milk_externality_allowed': state['allowed'],
        'milk_externality_applied': state['applied'],
        'milk_externality_blocked': state['blocked'],
        'milk_externality_blocked_gross_edge': state['blocked_reasons'].get('gross_edge', 0),
        'milk_externality_blocked_externality': state['blocked_reasons'].get('externality', 0),
        'milk_externality_blocked_price_history': state['blocked_reasons'].get('price_history', 0),
        'milk_externality_wheat_saved_sum': round(state['wheat_saved_sum'], 1),
        'milk_externality_own_loss_sum': round(state['own_loss_sum'], 1),
        'milk_externality_opp_gain_sum': round(state['opp_gain_sum'], 1),
        'milk_externality_max_committed_turn': state['max_committed_turn'],
        'milk_externality_unsupported': state['unsupported'],
        'milk_externality_errors': state['errors'],
    })
    return result


agent.telemetry = _C155_REPORT
agent = globals().pop('agent')
