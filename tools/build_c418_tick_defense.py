"""Build the fixed c418 hypothesis or its OFF control from a frozen c416."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
 parent=(ROOT/'agent/c416_current_policy_coverage.py').read_bytes()
 assert hashlib.sha256(parent).hexdigest()=='4880a8522c31573e65d315edbe11c7c46085e708695f35e9d95b0b6bfec2e558'
 layer=(ROOT/'state/c418/layer.py').read_text('utf8')
 if a.disabled:layer=layer.replace('_C418_ENABLED = True','_C418_ENABLED = False')
 data=parent.rstrip()+b'\n\n'+layer.encode('utf8');compile(data,str(a.out),'exec');assert not a.out.exists()
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data);print(a.out,hashlib.sha256(data).hexdigest())
