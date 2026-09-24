"""Add a midnight overflow reclaim to frozen o302: at hour 23, sell the cheapest shed units that the
nightly inventory drop would otherwise push past the shed capacity (destroyed units)."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
WRAPPER = r'''

# o306: midnight overflow reclaim. Engine-hooked ledgers of six local games show
# the nightly auto-drop destroying ~$250 of cargo per game (eggs, fertilizer,
# carrots, wheat; mostly days 25 and 27) once the shed holds 100 units; rivals of
# the same lineage lose the same. At hour 23, after the parent's orders, project
# the shed after this step's drops and sales plus the inventories that will be
# auto-dropped; if that exceeds the capacity, sell the cheapest sellable shed
# units for the excess so the incoming cargo is kept instead of destroyed.
_O306_ENABLED = __ON__
_O306_PARENT = agent
_O306_REPORT = {}
_O306_CAPACITY = 100
_O306_MAX_ORDERS = 10
_O306_PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')

def _o306_reclaim(observation, action):
    farm = observation['farms'][int(observation['player'])]
    private = observation['private']
    shed = dict(private.get('shed') or {})
    inventories = list(private.get('inventories') or [])
    commands = [action.get('farmer') or ['PASS']] + list(action.get('hands') or [])
    incoming = 0
    for actor, inv in enumerate(inventories):
        units = sum(int(v) for k, v in inv.items() if v)
        command = commands[actor] if actor < len(commands) else ['PASS']
        if command and command[0] == 'DROP':
            for k, v in inv.items():
                shed[k] = int(shed.get(k, 0)) + int(v)
            continue
        if command and command[0] == 'PLACE' and len(command) >= 2 and command[1] in _O306_PRODUCTS:
            qty = min(int(inv.get(command[1], 0)), max(1, int(command[2])) if len(command) >= 3 else 1)
            shed[command[1]] = int(shed.get(command[1], 0)) + qty
            units -= qty
        incoming += units
    market = [list(o) for o in (action.get('market') or []) if o]
    planned = {}
    for o in market:
        if o[0] == 'SELL' and len(o) >= 3:
            planned[o[1]] = planned.get(o[1], 0) + max(0, int(o[2]))
    for item, qty in planned.items():
        shed[item] = max(0, int(shed.get(item, 0)) - qty)
    excess = sum(int(v) for v in shed.values()) + incoming - _O306_CAPACITY
    _O306_REPORT['reclaim_checks'] += 1
    if excess <= 0:
        return action
    prices = observation['market']['prices']
    extra = {}
    for item in sorted(_O306_PRODUCTS, key=lambda i: int(prices.get(i, 0))):
        if excess <= 0:
            break
        free = int(shed.get(item, 0))
        if free <= 0:
            continue
        take = min(free, excess)
        extra[item] = take; excess -= take
    if not extra:
        _O306_REPORT['reclaim_blocked'] += 1
        return action
    for item, qty in extra.items():
        merged = False
        for o in market:
            if o[0] == 'SELL' and len(o) >= 3 and o[1] == item:
                o[2] = int(o[2]) + qty; merged = True
                break
        if not merged:
            if len(market) >= _O306_MAX_ORDERS:
                _O306_REPORT['reclaim_blocked'] += 1
                continue
            market.append(['SELL', item, qty])
        _O306_REPORT['reclaim_units'] += qty
    if excess > 0:
        _O306_REPORT['reclaim_partial'] += 1
    _O306_REPORT['reclaims'] += 1
    return dict(action, market=market)

def agent(observation, configuration=None):
    action = _O306_PARENT(observation, configuration)
    step = int(observation['step'])
    if step == 0:
        _O306_REPORT.clear()
        _O306_REPORT.update(reclaim_checks=0, reclaims=0, reclaim_units=0, reclaim_blocked=0, reclaim_partial=0)
    _O306_REPORT.update(_O302_REPORT)
    if not _O306_ENABLED or step % 24 != 23 or step >= 719:
        return action
    return _o306_reclaim(observation, action)

agent.telemetry = _O306_REPORT
kaggle_submission_agent = agent
o306_submission_agent = agent
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    args = ap.parse_args()
    parent = (ROOT / 'agent/o302_farmer_feed_topup.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    data = parent.rstrip() + WRAPPER.replace('__ON__', str(not args.disabled)).encode()
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
