"""Re-run ONE elite episode with candidate(s) via replay_lab's evaluate logic and dump per-day
animal counts / escapes / money / feed-skips for diagnosis. Usage: python o_tools/suite_diag.py <episode> agent/c150.py agent/o158_feed_margin.py"""
import sys, os, json, copy, importlib
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.getcwd())
from src.kaggriculture_meta.replay_lab import tape_policy
from kaggle_environments import make
eid=sys.argv[1]; replay=json.load(open(f"o_replays/elite_losses/{eid}-replay.json",encoding="utf-8"))
names=replay["info"]["TeamNames"]; seat=names.index("Taeyang")
engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
def run(cand_path):
    import importlib.util
    spec=importlib.util.spec_from_file_location("cand_"+os.path.basename(cand_path).replace('.','_'),cand_path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    agents=[tape_policy(replay,0),tape_policy(replay,1)]; agents[seat]=m.agent
    original=engine._end_of_day
    def controlled(state,env,day):
        original(state,env,day); step=min(719,(day+1)*24)
        state[0].observation.town['unlocked_shops'][:]=replay['steps'][step][0]['observation']['town']['unlocked_shops']
    engine._end_of_day=controlled
    try:
        env=make('kaggriculture',configuration=dict(replay['configuration'],seed=replay['info']['seed']),debug=False); env.run(agents)
    finally: engine._end_of_day=original
    return env, getattr(m.agent,'telemetry',{})
def animals(farm): return sorted((x,y,t["animal"],t.get("yield_units",0),t.get("consecutive_unfed",0)) for y,row in enumerate(farm["tiles"]) for x,t in enumerate(row) if isinstance(t,dict) and t.get("animal"))
runs={}
for p in sys.argv[2:]:
    env,tel=run(p); runs[p]=env
    print(f"== {p}: rewards {[s.reward for s in env.steps[-1]]} tel {{k:v for k,v in tel.items() if str(k).startswith('o1')}}")
paths=list(runs)
print("day | money(cand) per agent ... | animals | escapes since prev day | shed WHEAT")
for day in range(8,30):
    t=min(719,day*24)
    line=f"{day:2d} |"
    for p in paths:
        st=runs[p].steps; f=st[t][0].observation.farms[seat]; prev=st[max(0,t-24)][0].observation.farms[seat]
        a=animals(f); pa=animals(prev); esc=len([x for x in pa if (x[0],x[1]) not in {(q[0],q[1]) for q in a}])
        shed=st[t][seat].observation.private['shed'].get('WHEAT',0)
        line+=f" {int(f['money']):7d} n={len(a):2d} esc={esc} w={shed:3d} |"
    print(line)
# per-day FEED counts comparison
print("FEED/day:", end=" ")
for p in paths:
    st=runs[p].steps; c=[sum(1 for t in range(d*24+1,min(720,(d+1)*24+1)) for cmd in ([st[t][seat].action.get('farmer') or ['PASS']]+list(st[t][seat].action.get('hands') or [])) if cmd and cmd[0]=='FEED') for d in range(8,30)]
    print(os.path.basename(p), c)
