"""Preserve the parent's final DROP while compacting c379 terminal routes."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');args=ap.parse_args()
    parent=(ROOT/'agent/c379_terminal_schedule.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='9cbc9171fc5650f59fcfc44c7453ce15bb64f27d7f2293294ab48317f59e3fce'
    original=(ROOT/'agent/overlays/c379_terminal_schedule.py').read_text('utf8')
    function=original.split('def _c379_plan(obs,action):',1)[1].split('\ndef agent(',1)[0]
    function=function.replace("        frame=action if t==step else tape[t]\n", """        frame=action if t==step else tape[t]
        if t==718:
            # The parent's last action is an observed all-cargo DROP, not the
            # raw tape's product-specific PLACE. Preserve it as a real job.
            terminal=[]
            for actor,pos in enumerate([f['farmer']]+f['hands']):
                adjacent=pos[0] in (4,5) and pos[1] in (4,5)
                terminal.append(['DROP'] if adjacent and any(p['inventories'][actor].values()) else ['PASS'])
            frame=dict(farmer=terminal[0],hands=terminal[1:],market=[])
""")
    overlay='\n# c383: preserve o302 terminal all-cargo deposit in the compacted plan.\n_C383_ENABLED = True\n_C383_PRIOR_PLAN = _c379_plan\n\ndef _c383_complete_plan(obs,action):'+function+'\n\ndef _c379_plan(obs,action):\n    return _c383_complete_plan(obs,action) if _C383_ENABLED else _C383_PRIOR_PLAN(obs,action)\n\nc383_submission_agent=agent\n'
    if args.disabled:overlay=overlay.replace('_C383_ENABLED = True','_C383_ENABLED = False')
    data=parent.rstrip()+b'\n'+overlay.encode('utf8');compile(data,str(args.out),'exec')
    assert not args.out.exists();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
