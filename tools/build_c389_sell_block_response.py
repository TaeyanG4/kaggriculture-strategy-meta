"""Transfer exact public SELL permutation search on purchase-free final output."""
import argparse,ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='05b8d6eedb266fcc131ec74b8b87659e15ed077707d91489a423ad4d1a567144'
DONOR_SHA='178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);parser.add_argument('--disabled',action='store_true');args=parser.parse_args()
    body=(ROOT/'agent/c384_predictive_tomato.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    donor=next(a for a in json.loads((ROOT/'state/c386/league-start.json').read_text('utf8'))['agents'] if a['id']==261)
    source=Path(donor['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==donor['source_sha256']==DONOR_SHA
    text=source.decode('utf8');lines=text.splitlines(True)
    names=('_v44y_price','_v44y_params','_v44y_lockstep','_v44y_factor_margin','_v44y_reorder')
    nodes={n.name:n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name in names}
    layer='\n'.join(''.join(lines[nodes[k].lineno-1:nodes[k].end_lineno]) for k in names)
    wrapper=r'''

# c389, Taeyang/Codex, 2026-09-23. Public prvsiyan SELL-block solver, Apache-2.0.
# https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-soil-remembers-rain
# Donor source __DONOR_SHA__; preserve all inherited notices above.
# c362 used generic sell-impact priority; this factors exact unit-lockstep quotes
# against the unchanged parent queue as a hypothetical rival. It does NOT reveal
# the rival's private stock or guarantee gains against its real next action.
# Only pure SELL queues are supported: no unbounded-cash/purchase assumptions.
import itertools as _c389_it
_C389_ENABLED = __ENABLED__
_C389_PARENT = agent
_C389_REPORT = dict(c389_offers=0,c389_turns=0,c389_errors=0)
_C389_TELEMETRY = {}
_C389_MODEL_REPORT = dict(v44y_reorder_turns=0,v44y_reorder_gain=0.0,v44y_errors=0)
_C389_NS = dict(_v44y_it=_c389_it,_r37_market_price=_C365_CA_NS['_r37_market_price'],
    _R37_MARKET_PARAMS=_C365_CA_NS['_R37_MARKET_PARAMS'],_V44Y_REPORT=_C389_MODEL_REPORT,
    FarmView=lambda obs:obs,
    projected_shed=lambda action,obs:_C365_CA_NS['_ov_fields'](obs,action)[1]['shed'])
exec(compile(__LAYER__, '<c389-public-sell-block>', 'exec'), _C389_NS)


def agent(observation, configuration=None):
    step=int(observation['step'])
    if step==0:
        for key in _C389_REPORT:_C389_REPORT[key]=0
        for key in _C389_MODEL_REPORT:_C389_MODEL_REPORT[key]=0
    action=_C389_PARENT(observation,configuration)
    if _C389_ENABLED and step>=216:
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in
            [('episodeSteps',720),('turnsPerDay',24),('boardSize',10),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
        market=action.get('market') or []
        supported=(2<=len(market)<=6 and all(isinstance(o,list) and len(o)==3 and o[0]=='SELL' and type(o[2]) is int and o[2]>0 for o in market))
        if standard and supported and len({o[1] for o in market})==len(market):
            _C389_REPORT['c389_offers']+=1
            try:
                revised=_C389_NS['_v44y_reorder'](observation,action)
                _C389_REPORT['c389_turns']+=int(revised!=action)
                action=revised
            except Exception:
                _C389_REPORT['c389_errors']+=1
                raise
    _C389_TELEMETRY.clear();_C389_TELEMETRY.update(_C384_REPORT);_C389_TELEMETRY.update(_C389_REPORT)
    _C389_TELEMETRY['c389_hypothetical_gain']=_C389_MODEL_REPORT['v44y_reorder_gain']
    return action


agent.telemetry=_C389_TELEMETRY
c389_submission_agent=agent
'''.replace('__DONOR_SHA__',donor['source_sha256']).replace('__ENABLED__',str(not args.disabled)).replace('__LAYER__',repr(layer))
    data=body.rstrip()+wrapper.encode('utf8');compile(data,str(args.out),'exec');assert not args.out.exists();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest(),'donor',donor['source_sha256'])


if __name__=='__main__':main()
