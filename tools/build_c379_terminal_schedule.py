"""Build immutable terminal schedule compaction on o302."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
 parent=(ROOT/'agent/o302_farmer_feed_topup.py').read_bytes()
 assert hashlib.sha256(parent).hexdigest()=='2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
 overlay=(ROOT/'agent/overlays/c379_terminal_schedule.py').read_text('utf8')
 if a.disabled:overlay=overlay.replace('_C379_ENABLED = True','_C379_ENABLED = False')
 data=parent.rstrip()+b'\n\n'+overlay.encode();compile(data,str(a.out),'exec')
 if a.out.exists():raise FileExistsError(a.out)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data);print(a.out,hashlib.sha256(data).hexdigest())
if __name__=='__main__':main()
