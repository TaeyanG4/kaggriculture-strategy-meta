"""Repair final-day planned sales clipped before the final worker deliveries."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
WRAPPER = r'''

# c376: retain o302, including the early inventory clamp. On the final day,
# restore only the lost part of an already-planned sale when later unit
# rewrites deliver additional stock. No new product, order slot, worker,
# purchase or sale horizon; the final action's physical projection bounds it.
# v2 may append a deleted zero-stock SELL after the surviving sales, within
# the official order cap. It never moves an existing order to another slot.
# Unlike rejected c375, the clamp remains active throughout every layer.
_C376_ENABLED = __ON__
_C376_RESTORE_REMOVED = __RESTORE__
_C376_PARENT = agent
_C376_REPORT = {}
_C376_CLIPPED = {}
_C376_CAPTURE = False
_C376_CLAMP = _C365_CA_NS['Chassis']._clamp_sells

def _c376_clamp(action, projected):
    before = [list(o) for o in action.get('market', [])]
    _C376_CLAMP(action, projected)
    if _C376_CAPTURE:
        for old, new in zip(before, action.get('market', [])):
            if len(old) >= 3 and old[0] == 'SELL' and len(new) >= 3:
                lost = int(old[2]) - int(new[2])
                if lost > 0:
                    item = old[1]
                    _C376_CLIPPED[item] = (_C376_CLIPPED.get(item, (0, int(projected.get(item, 0))))[0] + lost,
                                            int(projected.get(item, 0)))

if _C376_ENABLED:
    _C365_CA_NS['Chassis']._clamp_sells = staticmethod(_c376_clamp)

def agent(observation, configuration=None):
    global _C376_CAPTURE
    step = int(observation['step'])
    if step == 0:
        _C376_REPORT.clear()
        _C376_REPORT.update(delivery_turns=0, delivery_units=0)
    _C376_CLIPPED.clear()
    _C376_CAPTURE = _C376_ENABLED and step // 24 == 29
    action = _C376_PARENT(observation, configuration)
    _C376_REPORT.update(_O302_REPORT)
    if not _C376_CAPTURE or not _C376_CLIPPED:
        return action
    market = [list(o) for o in action.get('market', [])]
    # Preserve washes/input reserves, purchases and all intermediate gates.
    if any(o and o[0].startswith('BUY_') for o in market):
        return action
    _, private = _C365_CA_NS['_ov_fields'](observation, action)
    changed = False
    for item, (lost, early_stock) in _C376_CLIPPED.items():
        if item in ('WHEAT', 'FERTILIZER'):
            continue
        indices = [i for i, o in enumerate(market) if len(o) >= 3 and o[:2] == ['SELL', item]]
        if not indices and (not _C376_RESTORE_REMOVED or len(market) >= 10 or
                            any(not o or o[0] != 'SELL' for o in market)):
            continue
        requested = sum(max(0, int(market[i][2])) for i in indices)
        physical = int(private['shed'].get(item, 0))
        extra = min(lost, physical - early_stock, physical - requested)
        if extra > 0:
            if indices:
                market[indices[0]][2] += extra
            else:
                market.append(['SELL', item, extra])
            _C376_REPORT['delivery_units'] += extra
            changed = True
    if changed:
        _C376_REPORT['delivery_turns'] += 1
        return dict(action, market=market)
    return action

agent.telemetry = _C376_REPORT
kaggle_submission_agent = agent
c376_submission_agent = agent
'''

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--disabled', action='store_true')
    ap.add_argument('--restore-removed', action='store_true')
    args = ap.parse_args()
    parent = (ROOT / 'agent/o302_farmer_feed_topup.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    data = parent.rstrip() + WRAPPER.replace('__ON__', str(not args.disabled)).replace('__RESTORE__', str(args.restore_removed)).encode()
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    main()
