"""Build c420 from the exact frozen c419 source; never overwrite an artifact."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'agent/c419_pinned_tick_defense.py'
PARENT_SHA = 'a4890e33741768bc5a5a1ec3c23386ddf7186fafb08edba629f267da67b3bb55'
WRAPPER = '''

# c420 N3-08: bank a held animal product when today's CARE cannot pay by d29.
_C420_ENABLED = __ENABLED__
_C420_PARENT = _C396_PARENT
_C420_REPORT = dict(fires=0, units=0, errors=0)

def _c420_no_care_payout(day, placed, first, interval):
    # End of d refresh first produces for d+1, pays the old pending bonus,
    # and only then banks today's care.  Today's care needs production d+2..29.
    return all(not (d - placed >= first and
                    (d - placed - first) % interval == 0)
               for d in range(day + 2, 30))

def _c420_offer(obs, action):
    step = int(obs['step']); day = step // 24
    if not 26 <= day <= 28:
        return action, 0, 0
    seat = int(obs['player']); farm = obs['farms'][seat]
    private = obs['private']
    positions = [tuple(farm['farmer'])] + [tuple(p) for p in farm['hands']]
    units = [action.get('farmer') or ['PASS']] + list(action.get('hands') or [])
    if len(units) < len(positions) or len(private['inventories']) < len(positions):
        return action, 0, 0
    if not any(c == ['CARE'] for c in units[:len(positions)]):
        return action, 0, 0
    # Conservative capacity: every item in the shed and every carried item
    # competes with early deposits.  Reserve same-turn original harvests too.
    occupied = sum(max(0, int(v)) for v in private['shed'].values())
    occupied += sum(max(0, int(v)) for inv in private['inventories']
                    for v in inv.values())
    for i, cmd in enumerate(units[:len(positions)]):
        if cmd == ['HARVEST']:
            x, y = positions[i]; tile = farm['tiles'][y][x]
            if isinstance(tile, dict):
                occupied += max(0, int(tile.get('yield_units', 0)))
    visits = _C365_CA_NS['_ch_visits_today'](obs, action)
    changed = 0; gained = 0; proposed = list(units)
    for i, cmd in enumerate(units[:len(positions)]):
        if cmd != ['CARE']:
            continue
        pos = positions[i]; x, y = pos
        tile = farm['tiles'][y][x]
        if not isinstance(tile, dict):
            continue
        animal = tile.get('animal')
        if animal not in ('COW', 'SHEEP') or tile.get('cared_today'):
            continue
        qty = int(tile.get('yield_units', 0))
        if qty < 2 or occupied + qty >= 90:
            continue
        first, interval = (8, 2) if animal == 'COW' else (6, 3)
        if not _c420_no_care_payout(day, int(tile['placed_day']), first, interval):
            continue
        # The existing future tape must not already harvest this tile today.
        if any(op == 'HARVEST' for _, op in visits.get(pos, ())):
            continue
        # Unit actions execute in actor order.  Avoid both earlier mutation
        # and a later action aimed at this same tile.
        if any(j != i and positions[j] == pos and units[j] and
               units[j][0] not in ('PASS','NORTH','SOUTH','EAST','WEST')
               for j in range(len(positions))):
            continue
        proposed[i] = ['HARVEST']; occupied += qty
        changed += 1; gained += qty
    if not changed:
        return action, 0, 0
    result = dict(action)
    result['farmer'] = proposed[0]
    result['hands'] = proposed[1:]
    return result, changed, gained

def _c420_parent(observation, configuration=None):
    action = _C420_PARENT(observation, configuration)
    if int(observation['step']) == 0:
        _C420_REPORT.update(fires=0, units=0, errors=0)
    try:
        result, fires, units = _c420_offer(observation, action)
    except Exception:
        _C420_REPORT['errors'] += 1
        raise
    _C420_REPORT['fires'] += fires
    _C420_REPORT['units'] += units
    return result

if _C420_ENABLED:
    _C396_PARENT = _c420_parent

_C420_ENTRY = agent
_C420_TELEMETRY = {}

def agent(observation, configuration=None):
    result = _C420_ENTRY(observation, configuration)
    _C420_TELEMETRY.clear()
    _C420_TELEMETRY.update(getattr(_C420_ENTRY, 'telemetry', {}))
    _C420_TELEMETRY.update({'c420_' + k: v for k, v in _C420_REPORT.items()})
    return result

agent.telemetry = _C420_TELEMETRY
c420_submission_agent = agent
'''

def build(out, enabled):
    body = PARENT.read_bytes()
    assert hashlib.sha256(body).hexdigest() == PARENT_SHA, 'frozen c419 changed'
    data = body + WRAPPER.replace('__ENABLED__', str(enabled)).encode('utf8')
    compile(data, str(out), 'exec')
    assert not out.exists(), f'refusing overwrite: {out}'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(out, hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    args = ap.parse_args()
    build(args.out, not args.disabled)
