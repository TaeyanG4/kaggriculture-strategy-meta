"""c398: settle a fully funded, adjacent wheat round-trip in its purchase turn."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT='28a520730a4f0037c0e9f433e28417db1ba0c95999a55b1751a396b28da08ad2'
OVERLAY=r'''

# c398, Taeyang/Codex. Only our own adjacent planned wheat trade is inspected.
# No opponent ID, replay, seed or future opponent observation is used.
_C398_ENABLED = __FLAG__
_C398_PARENT = _C396_PARENT
_C398_ROUTE_ACTION = _C365_CA_NS['Chassis']._route_action
_C398_DEBTS = {}
_C398_REPORT = {}
_C398_SEAT = 0

def _c398_route_action(self, route, step):
    action = _C398_ROUTE_ACTION(self, route, step)
    due = _C398_DEBTS.get((_C398_SEAT, step, route))
    if _C398_ENABLED and due:
        index, quantity = due
        orders = action.get('market') or []
        if index < len(orders) and orders[index] == ['SELL', 'WHEAT', quantity]:
            action = _c396_copy.deepcopy(action)
            action['market'][index] = ['SELL', 'WHEAT', 0]
            _C398_REPORT['c398_settled'] += 1
        else:
            raise RuntimeError('c398 scheduled sale identity mismatch')
    return action

def _c398_parent(observation, configuration=None):
    global _C398_SEAT
    t = int(observation['step']); seat = int(observation['player']); _C398_SEAT = seat
    if t == 0:
        _C398_DEBTS.clear(); _C398_REPORT.clear()
        _C398_REPORT.update(c398_changes=0, c398_units=0, c398_settled=0,
                            c398_budget_declines=0, c398_capacity_declines=0)
    action = _C398_PARENT(observation, configuration)
    for key in list(_C398_DEBTS):
        if key[0] == seat and key[1] <= t:
            del _C398_DEBTS[key]
    if not _C398_ENABLED or not 144 <= t < 647 or t % 24 == 23:
        return action
    cfg = dict(configuration or {})
    if any(cfg.get(k, v) != v for k, v in [('boardSize',10),('turnsPerDay',24),
            ('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
        return action
    orders = action.get('market') or []
    wheat = [(i,o) for i,o in enumerate(orders) if len(o)>=3 and o[1]=='WHEAT'
             and o[0] in ('BUY_PRODUCT','SELL')]
    if len(wheat)!=1 or wheat[0][1][0]!='BUY_PRODUCT' or len(orders)>=10:
        return action
    index, buy = wheat[0]; quantity = int(buy[2])
    if quantity <= 0:
        return action
    native = _C358_IMPL.chassis; route = native.players[seat]['route']
    future = native.routes[route][t+1]
    legs = [(i,o) for i,o in enumerate(future.get('market') or [])
            if len(o)>=3 and o[1]=='WHEAT' and o[0] in ('BUY_PRODUCT','SELL')]
    if len(legs)!=1 or legs[0][1]!=['SELL','WHEAT',quantity]:
        return action
    # Never accelerate a purchase needed by a scheduled field pickup.
    for frame in (action, future):
        if any(c[:2]==['PICKUP','WHEAT'] for c in [frame.get('farmer') or ['PASS']]
               + list(frame.get('hands') or [])):
            return action
    # Existing conservative budget bounds all ten rival market orders. Do not
    # borrow against this turn's sale proceeds or sell existing feed reserves.
    if not _C365_CA_NS['_r97_budget'](observation, orders):
        _C398_REPORT['c398_budget_declines'] += 1
        return action
    projected = projected_shed(action, FarmView(observation))
    if sum(max(0,int(q)) for q in projected.values()) + sum(
            max(0,int(o[2])) for o in orders if len(o)>=3 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL')) > 100:
        _C398_REPORT['c398_capacity_declines'] += 1
        return action
    result = _c396_copy.deepcopy(action)
    result['market'].insert(index+1, ['SELL','WHEAT',quantity])
    _C398_DEBTS[(seat,t+1,route)] = (legs[0][0],quantity)
    _C398_REPORT['c398_changes'] += 1; _C398_REPORT['c398_units'] += quantity
    return result

if _C398_ENABLED:
    _C365_CA_NS['Chassis']._route_action = _c398_route_action
_C396_PARENT = _c398_parent
_C398_ENTRY = agent
_C398_TELEMETRY = {}

def agent(observation, configuration=None):
    action = _C398_ENTRY(observation, configuration)
    _C398_TELEMETRY.clear(); _C398_TELEMETRY.update(_C396_TELEMETRY)
    _C398_TELEMETRY.update(_C398_REPORT)
    return action

agent.telemetry = _C398_TELEMETRY
c398_submission_agent = agent
'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--disabled',action='store_true');args=p.parse_args()
    raw=(ROOT/'agent/c397_shadow_coverage.py').read_bytes();assert hashlib.sha256(raw).hexdigest()==PARENT
    payload=raw.rstrip()+OVERLAY.replace('__FLAG__',str(not args.disabled)).encode()
    compile(payload,str(args.out),'exec');assert not args.out.exists();args.out.write_bytes(payload)
    print(args.out,hashlib.sha256(payload).hexdigest())
if __name__=='__main__':main()
