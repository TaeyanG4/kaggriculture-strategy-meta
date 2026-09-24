"""Keep c373's structure repair and suppress unused last-day fertilizer buys."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '6731b608fa9a94e88f47211b3d3e2feb14681e45e6c918756e5a7e3205923297'
WRAPPER = r'''

# c374: last-day fertilizer has no remaining input use on this pinned parent.
# Public reference: Frontier agent ecbc06f5... (_33_KO, days29). Unlike its
# list deletion, retain empty slots to preserve other order positions.
# Integration Taeyang/Codex; upstream attribution retained above.
_C374_ENABLED = __ON__
_C374_PARENT = agent
_C374_REPORT = {}
_C374_RAW_TAIL = _C358_IMPL.chassis.routes[2][696:719]
if any(c and (c[0] == 'FERTILIZE' or c[:2] == ['PICKUP', 'FERTILIZER'])
       for a in _C374_RAW_TAIL
       for c in [a.get('farmer') or ['PASS'], *(a.get('hands') or [])]):
    raise RuntimeError('c374 terminal input contract drift')

def agent(observation, configuration=None):
    step = int(observation['step'])
    if step == 0:
        _C374_REPORT.clear()
        _C374_REPORT.update(cut_units=0, changed_turns=0, guarded_turns=0)
    action = _C374_PARENT(observation, configuration)
    _C374_REPORT.update({'structure_'+k:v for k,v in _C373_REPORT.items()})
    if not _C374_ENABLED or step < 696 or step > 718:
        return action
    if configuration is not None and any(configuration.get(k,v) != v for k,v
        in [('episodeSteps',720),('turnsPerDay',24),('boardSize',10)]):
        return action
    market = action.get('market') or []
    if not any(len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER'] and int(o[2])>0 for o in market):
        return action
    seat = int(observation['player'])
    pending = _C358_IMPL.chassis.players[seat]['pending']
    units = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    commands = units + [c for q in pending.values() for _,c in q]
    if any(c and (c[0]=='FERTILIZE' or c[:2]==['PICKUP','FERTILIZER']) for c in commands):
        _C374_REPORT['guarded_turns'] += 1
        return action
    out = []
    for order in market:
        if len(order)>=3 and order[:2]==['BUY_PRODUCT','FERTILIZER']:
            _C374_REPORT['cut_units'] += max(0,int(order[2]))
            out.append([])
        else:
            out.append(order)
    _C374_REPORT['changed_turns'] += 1
    return dict(action, market=out)

agent.telemetry = _C374_REPORT
kaggle_submission_agent = agent
c374_submission_agent = agent
'''

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--disabled',action='store_true')
    args=ap.parse_args()
    parent=(ROOT/'agent/c373_structure_retry.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()==PARENT_SHA
    data=parent.rstrip()+WRAPPER.replace('__ON__',str(not args.disabled)).encode()
    compile(data,str(args.out),'exec')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    if args.out.exists():raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
