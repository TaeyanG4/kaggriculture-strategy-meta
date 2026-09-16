import os,sys,importlib.util,json
os.environ['MPLBACKEND']='Agg'
from kaggle_environments import make
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,os.path.abspath(path)); m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m
pm=load('agent/opp_planner_proxy.py','proxymod'); cm=load('agent/c150.py','c150mod')
def proxy(obs,cfg=None):
    seat=int(obs['player']); step=int(obs['step']); st=pm._STATE.get(seat)
    if st is None or step<=st.last_step: st=pm._STATE[seat]=pm.Proxy(seat)
    st.last_step=step; return st.act(obs)
c150=[v for k,v in vars(cm).items() if callable(v) and not k.startswith('__')][-1]
env=make('kaggriculture',configuration={'seed':7000},debug=False); env.run([proxy,c150]); st=env.steps
d=16
o=st[d*24][0].observation; f=o['farms'][0]
animals=[(x,y,t['animal']) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('animal')]
print('animals at day start:',animals)
for k in range(d*24,d*24+24):
    o=st[k][0].observation; f=o['farms'][0]; act=st[k][0].action or {}; pr=o['private']
    pos=[tuple(f['farmer'])]+[tuple(p) for p in f['hands']]; cmds=[act.get('farmer')]+(act.get('hands') or []); invs=pr.get('inventories',[])
    fed=sum(1 for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('animal') and t.get('fed_today'))
    n=min(3,len(pos),len(cmds))
    tile_at=lambda p: (f['tiles'][p[1]][p[0]].get('animal') or f['tiles'][p[1]][p[0]].get('crop') or f['tiles'][p[1]][p[0]].get('kind')) if isinstance(f['tiles'][p[1]][p[0]],dict) else f['tiles'][p[1]][p[0]]
    print(f"h{k%24:2d} shedW {pr['shed'].get('WHEAT',0):2d} fed {fed:2d} | "+' | '.join(f"{i}:{pos[i]}[{str(tile_at(pos[i]))[:5]}]{(cmds[i][0] if cmds[i] else '-')[:6]}{'' if not cmds[i] or len(cmds[i])<2 else ' '+str(cmds[i][1])[:4]} w{(invs[i] or {}).get('WHEAT',0) if i<len(invs) else '?'}" for i in range(n)))
