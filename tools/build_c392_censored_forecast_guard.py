"""Restrict only extra forecasts when the last market interval hit the price floor."""
import argparse,ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='2574f60424e319f5cd1df0221c94eb1bf33da57fa32ef0a15a8a7e7f65a2eae7'
DONOR_SHA='83fb106f37fcc10f3c3d9db8a78ded1529da30e9e232976ec0cf46fd6662fed4'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');args=ap.parse_args()
    body=(ROOT/'agent/c387_forecast_frontier.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    identity=json.loads((ROOT/'state/c384/agent258-identity.json').read_text('utf8'))
    donor=Path(identity['source_path']).read_bytes();assert hashlib.sha256(donor).hexdigest()==DONOR_SHA
    source=donor.decode('utf8');lines=source.splitlines(True)
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_v92_predict')
    layer=''.join(lines[node.lineno-1:node.end_lineno])
    old='        if votes < 1:\n            continue\n'
    new='''        if (votes and item in _C392_CENSORED and
                best[0].get((step + 1, i), 0) + best[0].get((step + 2, i), 0) < _V92_P_K):
            _C392_REPORT['c392_extra_forecasts_blocked'] += 1
            votes = 0
        if votes < 1:
            continue
'''
    assert layer.count(old)==1;layer=layer.replace(old,new)
    wrapper='''

# c392: a floor-priced interval censors inferred rival sale quantities.
# Keep the primary forecast and all inherited race/price/observer behavior.
# Only new c387 alternative-path proposals abstain for that item/interval.
_C392_ENABLED = __ENABLED__
_C392_PARENT = agent
_C392_CENSORED = set()
_C392_LAST = {}
_C392_REPORT = {'c392_floor_item_turns': 0, 'c392_extra_forecasts_blocked': 0}
_C392_TELEMETRY = {}
if _C392_ENABLED:
    _C365_CA_NS['_C392_CENSORED'] = _C392_CENSORED
    _C365_CA_NS['_C392_REPORT'] = _C392_REPORT
    exec(compile(__LAYER__, '<c392-censored-extra-forecast>', 'exec'), _C365_CA_NS)

def agent(observation, configuration=None):
    step = int(observation['step']); seat = int(observation['player'])
    if step == 0:
        _C392_LAST.pop(seat, None)
        for key in _C392_REPORT: _C392_REPORT[key] = 0
    _C392_CENSORED.clear()
    previous = _C392_LAST.get(seat)
    if _C392_ENABLED and previous and previous['step'] == step - 1:
        draw = _C365_CA_NS['_v9_town_draw'](previous['shops'], previous['step'])
        market = observation['market']
        for item in _C365_CA_NS['_V92_P_USE']:
            before_draw = market['inventory'][item] + draw.get(item, 0)
            if _C365_CA_NS['_r37_market_price'](item, before_draw, market.get('params')) <= 1:
                _C392_CENSORED.add(item)
        _C392_REPORT['c392_floor_item_turns'] += len(_C392_CENSORED)
    result = _C392_PARENT(observation, configuration)
    _C392_LAST[seat] = {'step': step, 'shops': tuple(observation['town']['unlocked_shops'])}
    _C392_TELEMETRY.clear()
    _C392_TELEMETRY.update(_C387_TELEMETRY)
    _C392_TELEMETRY.update(_C392_REPORT)
    return result

agent.telemetry = _C392_TELEMETRY
c392_submission_agent = agent
'''.replace('__ENABLED__',str(not args.disabled)).replace('__LAYER__',repr(layer))
    data=body.rstrip()+wrapper.encode('utf8');compile(data,str(args.out),'exec');assert not args.out.exists();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
