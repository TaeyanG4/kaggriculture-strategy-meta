"""Transfer only More Wheat's supported forecast frontier, preserving our cadence."""
import argparse,ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='4322b098ed0c1478135f34de3492c16b4c186d570156f2596cdc7fb1854e57c9'
DONOR_SHA='83fb106f37fcc10f3c3d9db8a78ded1529da30e9e232976ec0cf46fd6662fed4'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    body=(ROOT/'agent/c386_tomato_opportunity_union.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    identity=json.loads((ROOT/'state/c384/agent258-identity.json').read_text('utf8'));donor=Path(identity['source_path']).read_bytes();assert hashlib.sha256(donor).hexdigest()==DONOR_SHA
    source=donor.decode('utf8');lines=source.splitlines(True);names=('_v92_p_forecast','_v92_predict')
    nodes={n.name:n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in names}
    layer='\n'.join(''.join(lines[nodes[k].lineno-1:nodes[k].end_lineno]) for k in names)
    overlay='''

# c387: public More Wheat, Smarter Sales (Dmitrii Gluzdov, Apache-2.0).
# https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales
# Exact donor __SHA__; retain notices. Integration Taeyang/Codex 2026-09-23.
# Only near-best forecast trajectories plus diagnostic counters are transferred.
# Keep the inherited cadence, stock limits, products, library and physical plan.
_C387_ENABLED = __ENABLED__
_C387_PARENT = agent
_C387_TELEMETRY = {}
if _C387_ENABLED:
    if _C365_CA_NS['_v92_p_forecast'].__globals__ is not _C365_CA_NS:
        raise RuntimeError('c387 forecast namespace drift')
    exec(compile(__LAYER__, '<c387-public-forecast-frontier>', 'exec'), _C365_CA_NS)

def agent(observation, configuration=None):
    if int(observation['step']) == 0 and _C387_ENABLED:
        for key in _C365_CA_NS['_V92_P_REPORT']:
            _C365_CA_NS['_V92_P_REPORT'][key] = 0
    action = _C387_PARENT(observation, configuration)
    _C387_TELEMETRY.clear()
    _C387_TELEMETRY.update(_C386_TELEMETRY)
    if _C387_ENABLED:
        _C387_TELEMETRY.update({'c387_'+k:v for k,v in _C365_CA_NS['_V92_P_REPORT'].items()})
    return action

agent.telemetry = _C387_TELEMETRY
c387_submission_agent = agent
'''.replace('__SHA__',DONOR_SHA).replace('__ENABLED__',str(not a.disabled)).replace('__LAYER__',repr(layer))
    data=body.rstrip()+overlay.encode('utf8');compile(data,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data);print(a.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
