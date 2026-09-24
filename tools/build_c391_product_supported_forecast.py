"""Keep c387's primary forecast; require item-specific support for extra paths."""
import argparse,ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='2574f60424e319f5cd1df0221c94eb1bf33da57fa32ef0a15a8a7e7f65a2eae7'
DONOR_SHA='83fb106f37fcc10f3c3d9db8a78ded1529da30e9e232976ec0cf46fd6662fed4'
HELPER='''
def _c391_supported(best, st, step):
    # Same 240-turn / +/-1 event score as the inherited forecast selector.
    # A second path must improve the evidence for the item it will sell.
    # The primary path is never suppressed, even when its local fit is poor.
    result = {i: [best[0]] for i in range(len(_V92_P_ITEMS))}
    if len(best) <= 1:
        return result
    lo = step - 240
    seen = st['obs']
    def fit(ev, item):
        matched = failed = 0
        for (turn, index) in ev:
            if index == item and lo <= turn < step - 1:
                if any((turn + offset, item) in seen for offset in (-1, 0, 1)):
                    matched += 1
                else:
                    failed += 1
        missed = sum(1 for turn, index in seen if index == item and turn >= lo
                     and not any((turn + offset, item) in ev for offset in (-1, 0, 1)))
        return 2 * matched - failed - missed
    for i, item in enumerate(_V92_P_ITEMS):
        if item not in _V92_P_USE:
            continue
        primary = fit(best[0], i)
        for ev in best[1:]:
            if fit(ev, i) > primary:
                result[i].append(ev)
            elif ev.get((step + 1, i), 0) + ev.get((step + 2, i), 0) >= _V92_P_K:
                _C391_REPORT['c391_unsupported_event_paths'] += 1
    return result
'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');args=ap.parse_args()
    body=(ROOT/'agent/c387_forecast_frontier.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    identity=json.loads((ROOT/'state/c384/agent258-identity.json').read_text('utf8'))
    donor=Path(identity['source_path']).read_bytes();assert hashlib.sha256(donor).hexdigest()==DONOR_SHA
    text=donor.decode('utf8');lines=text.splitlines(True)
    node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='_v92_predict')
    layer=''.join(lines[node.lineno-1:node.end_lineno])
    old='votes = sum(1 for ev in best if ev.get((step + 1, i), 0) + ev.get((step + 2, i), 0) >= _V92_P_K)'
    assert layer.count(old)==1 and layer.count('    changed = False\n')==1
    layer=layer.replace('    changed = False\n','    supported = _c391_supported(best, st, step)\n    changed = False\n').replace(old,old.replace('in best if','in supported[i] if'))
    wrapper='''

# c391: product-specific support for c387's additional forecast paths.
# The inherited More Wheat forecast retains its original public attribution.
_C391_ENABLED = __ENABLED__
_C391_PARENT = agent
_C391_REPORT = {'c391_unsupported_event_paths': 0}
_C391_TELEMETRY = {}
if _C391_ENABLED:
    _C365_CA_NS['_C391_REPORT'] = _C391_REPORT
    exec(compile(__LAYER__, '<c391-item-forecast-support>', 'exec'), _C365_CA_NS)

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _C391_REPORT['c391_unsupported_event_paths'] = 0
    result = _C391_PARENT(observation, configuration)
    _C391_TELEMETRY.clear()
    _C391_TELEMETRY.update(_C387_TELEMETRY)
    _C391_TELEMETRY.update(_C391_REPORT)
    return result

agent.telemetry = _C391_TELEMETRY
c391_submission_agent = agent
'''.replace('__ENABLED__',str(not args.disabled)).replace('__LAYER__',repr(HELPER+'\n'+layer))
    data=body.rstrip()+wrapper.encode('utf8');compile(data,str(args.out),'exec');assert not args.out.exists();args.out.parent.mkdir(exist_ok=True,parents=True);args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
