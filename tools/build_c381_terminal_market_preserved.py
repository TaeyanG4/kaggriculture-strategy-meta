"""Separate c379's route change from its blanket terminal liquidation.

c379 remains frozen. Reuse its route/dependency implementation, preserving
the actual parent market orders through step717 and liquidating only at718.
"""
import argparse, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--disabled',action='store_true')
    args=ap.parse_args()
    parent=(ROOT/'agent/o302_farmer_feed_topup.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
    overlay=(ROOT/'agent/overlays/c379_terminal_schedule.py').read_text('utf8')
    original="result=dict(action,farmer=units[0],hands=units[1:],market=[['SELL',k,int(p['shed'].get(k,0))] for k in products if p['shed'].get(k,0)>0])"
    replacement="""market=action.get('market') or []
    if step==718:
        market=[['SELL',k,int(p['shed'].get(k,0))] for k in products if p['shed'].get(k,0)>0]
    result=dict(action,farmer=units[0],hands=units[1:],market=market)"""
    assert overlay.count(original)==1
    overlay=overlay.replace(original,replacement).replace('c379','c381').replace('C379','C381')
    overlay=overlay.replace('# c381 terminal dependency-preserving compaction,', '# c381 terminal compaction with parent market requests preserved,')
    if args.disabled:overlay=overlay.replace('_C381_ENABLED = True','_C381_ENABLED = False')
    data=parent.rstrip()+b'\n\n'+overlay.encode('utf8')
    compile(data,str(args.out),'exec')
    if args.out.exists():raise FileExistsError(args.out)
    args.out.parent.mkdir(exist_ok=True,parents=True);args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
