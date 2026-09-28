"""Build c421's two-constant SHEDROOM experiment from exact frozen c419."""
import argparse
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'agent/c419_pinned_tick_defense.py'
PARENT_SHA='a4890e33741768bc5a5a1ec3c23386ddf7186fafb08edba629f267da67b3bb55'
WRAPPER='''

# c421 N1-02: widen the inherited SHEDROOM decision window and margin only.
_C421_ENABLED = __ENABLED__
_C421_NS = _C365_CA_NS
if tuple(_C421_NS['_SR_HOURS']) != (22, 23) or _C421_NS['_SR_MARGIN'] != 4:
    raise RuntimeError('c421 SHEDROOM parent constants changed')
if _C421_ENABLED:
    _C421_NS['_SR_HOURS'] = (18, 19, 20, 21, 22, 23)
    _C421_NS['_SR_MARGIN'] = 8

_C421_ENTRY = agent
_C421_TELEMETRY = {}

def agent(observation, configuration=None):
    result = _C421_ENTRY(observation, configuration)
    _C421_TELEMETRY.clear()
    _C421_TELEMETRY.update(getattr(_C421_ENTRY, 'telemetry', {}))
    _C421_TELEMETRY.update({'c421_' + k: v for k, v in _C421_NS['_SR_REPORT'].items()})
    return result

agent.telemetry = _C421_TELEMETRY
c421_submission_agent = agent
'''

def build(out,enabled):
    parent=PARENT.read_bytes()
    assert hashlib.sha256(parent).hexdigest()==PARENT_SHA,'frozen c419 changed'
    data=parent+WRAPPER.replace('__ENABLED__',str(enabled)).encode('utf8')
    compile(data,str(out),'exec')
    assert not out.exists(),f'refusing overwrite: {out}'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(data)
    print(out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--disabled',action='store_true')
    args=ap.parse_args()
    build(args.out,not args.disabled)
