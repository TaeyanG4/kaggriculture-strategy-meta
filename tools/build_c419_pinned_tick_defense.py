"""Repair c418's slot contract without changing detector, size, or thresholds."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WRAPPER='''

# c419: preserve the two-leg slot contract through the inherited response layer.
# c396 can move a single SELL across BUY_SEED; c418's assumption was too weak.
_C419_ENABLED = __ENABLED__
_C419_RESPONSE = _c396_response
_C419_BLOCKED = 0

def _c419_response(obs, action, predicted, configuration):
    global _C419_BLOCKED
    prev = _C418_STATE.get('prev') or {}
    if prev.get('step') == int(obs['step']) and prev.get('pair') is not None:
        _C419_BLOCKED += 1
        return action
    return _C419_RESPONSE(obs, action, predicted, configuration)

if _C419_ENABLED:
    _c396_response = _c419_response
_C419_ENTRY = agent
_C419_TELEMETRY = {}

def agent(observation, configuration=None):
    global _C419_BLOCKED
    if int(observation['step']) == 0:
        _C419_BLOCKED = 0
    result = _C419_ENTRY(observation, configuration)
    _C419_TELEMETRY.clear()
    _C419_TELEMETRY.update(getattr(_C419_ENTRY, 'telemetry', {}))
    _C419_TELEMETRY['c419_pinned_responses'] = _C419_BLOCKED
    return result

agent.telemetry = _C419_TELEMETRY
c419_submission_agent = agent
'''
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
 body=(ROOT/'agent/c418_tick_trade_defense.py').read_bytes()
 assert hashlib.sha256(body).hexdigest()=='e76b6ee02438f3de11b34cf498402670ef2f9f5596e837c1fd1ec7c91a306c94'
 if a.disabled:
  assert body.count(b'_C418_ENABLED = True')==1
  body=body.replace(b'_C418_ENABLED = True',b'_C418_ENABLED = False')
 data=body.rstrip()+WRAPPER.replace('__ENABLED__',str(not a.disabled)).encode('utf8');compile(data,str(a.out),'exec');assert not a.out.exists()
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data);print(a.out,hashlib.sha256(data).hexdigest())
