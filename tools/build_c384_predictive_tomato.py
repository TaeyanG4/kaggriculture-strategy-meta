"""Port the pinned public tomato qualification onto c383's existing controller."""
import argparse,ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='7f798f0d1ac3e5224b023c17ccf7555373d2dc67bede7a545238d5c37f218f79'
DONOR_SHA='1cac27653a81208bddc652d7f8437a4eed4ff3bd261c32934a08983484edf214'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    body=(ROOT/'agent/c383_terminal_cargo.py').read_bytes()
    identity=json.loads((ROOT/'state/c384/agent254-identity.json').read_text('utf8'))
    donor=Path(identity['source_path']).read_bytes()
    assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    assert hashlib.sha256(donor).hexdigest()==DONOR_SHA
    source=donor.decode('utf8');lines=source.splitlines(keepends=True);tree=ast.parse(source)
    names=('_cxtb_their_supply','_cxtb_expected_revenue','_cxtb_qualifies','_v219_qualifies')
    selected={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names}
    layer='''
_CXTB_MIN_REVENUE = 9000
_CXTB_THEIR_UNITS = 0.75
_CXTB_DRAIN_SLACK = 2.4
_CXTB_OUR_UNITS = 20
_CXTB_HARVEST_DAYS = (26,27,28,29)
_CXTB_REPORT = dict(cxtb_calls=0,cxtb_opened=0,cxtb_blocked=0,cxtb_errors=0,cxtb_features=[])
_CXTB_BASE_QUALIFIES = _v219_qualifies
'''+ '\n'.join(''.join(lines[selected[n].lineno-1:selected[n].end_lineno]) for n in names)
    overlay='''

# c384: predictive qualification only; existing V219 worker/land/seed program retained.
# Public Apache-2.0 donor: Dmitrii Gluzdov, 7-Turn Rescue Historical LB 2800+.
# https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800
# Donor SHA __SHA__. Original notices retained in source/archive. Constants unchanged.
# Integration Taeyang/Codex 2026-09-23. Forecast is an approximation, not exact simulation.
_C384_ENABLED = __ENABLED__
_C384_PARENT = agent
_C384_REPORT = {}
if _C384_ENABLED:
    if '_CXTB_BASE_QUALIFIES' in _C365_CA_NS:
        raise RuntimeError('c384 predictive tomato layer already present')
    if _C365_CA_NS['_v219_qualifies'].__globals__ is not _C365_CA_NS:
        raise RuntimeError('c384 tomato namespace drift')
    exec(compile(__LAYER__, '<c384-public-tomato-qualification>', 'exec'), _C365_CA_NS)

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _C384_REPORT.clear()
        if _C384_ENABLED:
            stats=_C365_CA_NS['_CXTB_REPORT']
            for key in stats:stats[key]=[] if key=='cxtb_features' else 0
    action=_C384_PARENT(observation,configuration)
    _C384_REPORT.update(_C379_REPORT)
    if _C384_ENABLED:
        _C384_REPORT.update(_C365_CA_NS['_CXTB_REPORT'])
    return action

agent.telemetry=_C384_REPORT
c384_submission_agent=agent
'''.replace('__SHA__',DONOR_SHA).replace('__ENABLED__',str(not a.disabled)).replace('__LAYER__',repr(layer))
    data=body.rstrip()+overlay.encode('utf8');compile(data,str(a.out),'exec')
    assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data)
    print(a.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
