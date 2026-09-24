"""One pre-existing public carrot value margin; preserve all execution/feed rules."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='2574f60424e319f5cd1df0221c94eb1bf33da57fa32ef0a15a8a7e7f65a2eae7'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    body=(ROOT/'agent/c387_forecast_frontier.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    layer='''

# c394: public Herd-Safe Sale Window's original CARROT2 value margin.
# https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-herd-safe-sale-window-lb-2700
# This transfers -15, not the later ca20=-20 variant. Feed reserve stays one day.
# No new routes, crop calendars, markets, forecasting data or fitted thresholds.
_C394_ENABLED = __ENABLED__
_C394_PARENT = agent
_C394_TELEMETRY = {}
if _C365_CA_NS['_CA_MARGIN'] != -5.0:
    raise RuntimeError('c394 parent carrot margin drift')
if _C394_ENABLED:
    _C365_CA_NS['_CA_MARGIN'] = -15.0

def agent(observation, configuration=None):
    action = _C394_PARENT(observation, configuration)
    _C394_TELEMETRY.clear()
    _C394_TELEMETRY.update(_C387_TELEMETRY)
    _C394_TELEMETRY.update({'c394_'+k:v for k,v in _C365_CA_NS['_CA_REPORT'].items()})
    return action

agent.telemetry = _C394_TELEMETRY
c394_submission_agent = agent
'''.replace('__ENABLED__',str(not a.disabled))
    data=body.rstrip()+layer.encode();compile(data,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data)
    print(a.out,hashlib.sha256(data).hexdigest())
if __name__=='__main__':main()
