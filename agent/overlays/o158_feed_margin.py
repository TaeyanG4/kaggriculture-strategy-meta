# SPDX-License-Identifier: Apache-2.0
# o158_feed_margin (Claude/o-series, 2026-09-15). Overlay appended to c150 (parent untouched).
"""Marginal-value FEED gate.

Engine facts (kaggriculture 1.32.7, _daily_refresh_animals): animals PRODUCE on schedule whether
or not they were fed; feeding only (a) resets consecutive_unfed (escape at >=2) and (b) lets the
care bonus accrue (cared AND fed -> pending+1) and be consumed (fed on a production day ->
yield += 1 + pending; unfed on a production day zeroes pending). Production at the end of day 29
can never be sold. Hence each FEED is worth roughly ONE unit of the animal's product (the bonus
it enables), plus survival insurance when consecutive_unfed == 1. The parent tape feeds every
animal every day at ~$42 wheat even when MILK/WOOL trade below $20 (live elite-loss audit:
we make ~24 more cow feeds per game with MILK < $20 than the 2750+ cluster does).

Rule: replace a scheduled FEED by PASS when the feed's marginal value < WHEAT price, subject to
  - never skip when consecutive_unfed == 1 unless the animal is worthless for the rest of the game
    (all remaining sellable production + yield on tile < one wheat) -> deliberate abandonment;
  - never skip the same tile two days in a row (bounds escape risk if the tape stops feeding);
  - day 29: every FEED is worthless (skip); day 28 handled by the general value model (LAST=28).
Only removes FEED actions (turns them into PASS); never adds actions, orders, or moves.
"""
import copy as _o158_copy

_O158_PARENT = agent
_O158_STATE = {}
_O158_REPORT = {}
_O158_SPEC = {'GOOSE': (4, 1), 'COW': (8, 2), 'SHEEP': (6, 3)}       # first_yield_day, interval
_O158_PRODUCT = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}
_O158_LAST_SELLABLE_DAY = 28
_O158_MARGIN = 1.0          # skip iff value < MARGIN * wheat price
_O158_MIN_DAY = 8           # never touch the opening (tape is fragile there)
del agent


def _o158_is_prod(kind, placed, day):
    first, interval = _O158_SPEC[kind]
    ds = (day + 1) - placed - first
    return ds >= 0 and ds % interval == 0


def _o158_value(tile, kind, day, prices):
    """Expected sellable product value (in $) that THIS feed protects/enables."""
    price = prices.get(_O158_PRODUCT[kind], 0)
    placed = int(tile.get('placed_day', 0))
    pending = int(tile.get('pending_care_bonus', 0) or 0)
    unfed = int(tile.get('consecutive_unfed', 0) or 0)
    held = int(tile.get('yield_units', 0) or 0)
    if day > _O158_LAST_SELLABLE_DAY:
        return 0.0, 0.0
    remaining = [d for d in range(day, _O158_LAST_SELLABLE_DAY + 1) if _o158_is_prod(kind, placed, d)]
    interval = _O158_SPEC[kind][1]
    # value if the animal survives the rest of the game (daily care assumed): base 1 + bonus per cycle
    future = sum(1 + (min(pending, interval) if i == 0 else min(interval, 3)) for i, _ in enumerate(remaining))
    abandon_value = price * (held + future)
    if unfed >= 1:
        return abandon_value, abandon_value
    if _o158_is_prod(kind, placed, day):
        return price * pending, abandon_value
    return (price * 1.0 if remaining else 0.0), abandon_value


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    day = step // 24
    st = _O158_STATE.get(seat)
    if st is None or step <= st['last']:
        st = {'last': -1, 'skipped_day': {}, 'skips': 0, 'abandons': 0, 'kept_survival': 0, 'errors': 0, 'day29_skips': 0}
        _O158_STATE[seat] = st
    st['last'] = step
    parent_action = _O158_PARENT(observation, configuration)
    result = parent_action
    try:
        if day >= _O158_MIN_DAY:
            prices = observation['market']['prices']
            wheat = float(prices.get('WHEAT', 0))
            farm = observation['farms'][seat]
            positions = [farm['farmer'], *farm['hands']]
            commands = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
            replacements = []
            for actor, command in enumerate(commands[:len(positions)]):
                if command != ['FEED']:
                    continue
                x, y = positions[actor]
                tile = farm['tiles'][y][x]
                if not isinstance(tile, dict) or tile.get('animal') not in _O158_SPEC or tile.get('fed_today'):
                    continue
                kind = tile['animal']
                key = (x, y)
                if day >= 29:
                    replacements.append((actor, key, 'day29')); continue
                value, abandon_value = _o158_value(tile, kind, day, prices)
                unfed = int(tile.get('consecutive_unfed', 0) or 0)
                if unfed >= 1:
                    if abandon_value < _O158_MARGIN * wheat:
                        replacements.append((actor, key, 'abandon'))
                    else:
                        st['kept_survival'] += 1
                    continue
                if st['skipped_day'].get(key) == day - 1:
                    continue  # never two consecutive skips on one tile
                if value < _O158_MARGIN * wheat:
                    replacements.append((actor, key, 'skip'))
            if replacements:
                result = _o158_copy.deepcopy(parent_action)
                for actor, key, why in replacements:
                    if actor == 0:
                        result['farmer'] = ['PASS']
                    else:
                        result['hands'][actor - 1] = ['PASS']
                    if why == 'skip':
                        st['skipped_day'][key] = day; st['skips'] += 1
                    elif why == 'abandon':
                        st['abandons'] += 1
                    else:
                        st['day29_skips'] += 1
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O158_REPORT.clear()
    _O158_REPORT.update(getattr(_O158_PARENT, 'telemetry', {}))
    _O158_REPORT.update({'o158_' + k: v for k, v in st.items() if k not in ('last', 'skipped_day')})
    return result


agent.telemetry = _O158_REPORT
agent = globals().pop('agent')
