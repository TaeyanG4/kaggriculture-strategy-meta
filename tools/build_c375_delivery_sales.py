"""Preserve planned sale quantities until the engine sees final unit deliveries."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '6731b608fa9a94e88f47211b3d3e2feb14681e45e6c918756e5a7e3205923297'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--disabled',action='store_true')
    args=ap.parse_args()
    parent=(ROOT/'agent/c373_structure_retry.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()==PARENT_SHA
    suffix='''

# c375: native clamp_sells runs before later courier/terminal unit rewrites.
# It can zero a planned SELL before the final DROP delivers its stock.
# Match public Clone Race Horizon's clamp_sells=False for this layer only;
# engine execution clamps actual inventory, preserving every market slot.
# Native risk gates, prices, quotes and later operators remain unchanged.
_C375_ENABLED = __ON__
_C375_PARENT = agent
_C375_REPORT = {}
if _C358_IMPL.chassis.cfg['clamp_sells'] is not True:
    raise RuntimeError('c375 parent clamp contract drift')
_C358_IMPL.chassis.cfg['clamp_sells'] = not _C375_ENABLED

def agent(observation, configuration=None):
    action = _C375_PARENT(observation, configuration)
    _C375_REPORT.clear()
    _C375_REPORT.update(_C373_REPORT)
    _C375_REPORT['early_clamp_disabled'] = int(_C375_ENABLED)
    return action

agent.telemetry = _C375_REPORT
kaggle_submission_agent = agent
c375_submission_agent = agent
'''.replace('__ON__',str(not args.disabled))
    data=parent.rstrip()+suffix.encode()
    compile(data,str(args.out),'exec')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    if args.out.exists():raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
