import os,sys,importlib.util,collections
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
env=make('kaggriculture',configuration={'seed':int(os.environ.get('PSEED','7000'))},debug=False); env.run([proxy,c150]); st=env.steps
print('day | $ | hands | plants watered/total | animals fed/total | weeds | moves acts pass | shed')
for d in range(0,30,2):
    k=min(719,d*24+23); o=st[k][0].observation; f=o['farms'][0]
    tiles=[t for row in f['tiles'] for t in row]
    pl=[t for t in tiles if isinstance(t,dict) and t.get('kind')=='PLANT']; an=[t for t in tiles if isinstance(t,dict) and t.get('animal')]
    weeds=sum(1 for t in tiles if isinstance(t,dict) and t.get('kind')=='WEED')
    mv=ac=ps=0
    for kk in range(d*24,min(720,d*24+24)):
        a=st[kk][0].action or {}
        for c in [a.get('farmer')]+(a.get('hands') or []):
            if not c or c[0]=='PASS': ps+=1
            elif c[0] in ('NORTH','SOUTH','EAST','WEST'): mv+=1
            else: ac+=1
    shed={k2:v for k2,v in o['private']['shed'].items() if v}
    print(f"d{d:2d} | {f['money']:6.0f} | {len(f['hands']):2d} | {sum(1 for t in pl if t.get('watered_today')):2d}/{len(pl):2d} | {sum(1 for t in an if t.get('fed_today')):2d}/{len(an):2d} | {weeds:2d} | {mv:3d} {ac:3d} {ps:3d} | {shed}")
print('final',[s.reward for s in st[-1]])
