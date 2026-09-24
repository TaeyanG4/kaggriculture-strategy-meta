"""Build a final-day joint harvest/return planner over the frozen o302 body."""
import argparse, ast, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
WRAPPER=r'''

# c378 final-day joint routes, Taeyang/Codex, 2026-09-22.
# Cheapest-insertion routing follows the existing p000 dispatch_vrp approach;
# this terminal-only variant enforces return/drop and has no new purchases.
# Native planner physical transition helpers and all upstream notices retained.
from collections import deque as _c378_deque
_C378_ENABLED=__ON__
_C378_PARENT=agent
_C378_STATE={}
_C378_REPORT={}
_C378_PRODUCTS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')
_C378_CROPS=__CROPS__

def _c378_plan(obs):
    farm=obs['farms'][obs['player']];grid=farm['tiles'];n=len(grid)
    homes=[(n//2-1,n//2-1),(n//2,n//2-1),(n//2-1,n//2),(n//2,n//2)]
    homes=[p for p in homes if grid[p[1]][p[0]]!='LOCKED']
    cells=[(x,y) for y,row in enumerate(grid) for x,t in enumerate(row) if t!='LOCKED']
    paths={}
    for start in cells:
        paths[start]={start:[]};q=_c378_deque([start])
        while q:
            pos=q.popleft()
            for cmd,dx,dy in [('NORTH',0,-1),('WEST',-1,0),('SOUTH',0,1),('EAST',1,0)]:
                nxt=(pos[0]+dx,pos[1]+dy)
                if 0<=nxt[0]<n and 0<=nxt[1]<n and grid[nxt[1]][nxt[0]]!='LOCKED' and nxt not in paths[start]:
                    paths[start][nxt]=paths[start][pos]+[[cmd]];q.append(nxt)
    step=int(obs['step']);day=step//24;left=719-step
    prices=obs['market']['prices'];jobs=[]
    for xy in cells:
        tile=grid[xy[1]][xy[0]]
        if not isinstance(tile,dict):continue
        actions=[];value=0;item=None;quantity=0
        if tile.get('animal'):
            item={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}[tile['animal']]
            quantity=int(tile.get('yield_units',0))
            if quantity:actions.append(['HARVEST']);value+=quantity*prices[item]
            if tile.get('fertilizer_available'):
                actions.append(['COLLECT_FERTILIZER']);value+=prices['FERTILIZER']
        elif tile.get('crop') in _C378_CROPS:
            item=tile['crop'];first,maxday,maxyield=_C378_CROPS[item];age=day-int(tile['planted_day'])
            quantity=int(tile.get('yield_units',0))
            if age<first or quantity<=0:continue
            if maxday and not tile.get('watered_today') and (maxday+1)//2<=age<=maxday and quantity<maxyield:
                actions.append(['WATER']);quantity=min(maxyield,quantity+(2 if tile.get('fertilized_until_day',-1)>=day else 1))
            actions.append(['HARVEST']);value=quantity*prices[item]
        if actions and value>0:jobs.append(dict(xy=xy,actions=actions,value=value))
    starts=[tuple(farm['farmer'])]+list(map(tuple,farm['hands']))
    routes=[[] for p in starts]
    def cost(i,route):
        pos=starts[i];t=0
        for j in route:
            target=jobs[j]['xy'];t+=len(paths[pos][target])+len(jobs[j]['actions']);pos=target
        return t+min(len(paths[pos][home]) for home in homes)+1
    remaining=set(range(len(jobs)))
    while remaining:
        best=None
        for j in sorted(remaining):
            for i,route in enumerate(routes):
                old=cost(i,route)
                for k in range(len(route)+1):
                    trial=route[:k]+[j]+route[k:];c=cost(i,trial)
                    if c>left:continue
                    gain=jobs[j]['value']/max(1,c-old)
                    key=(gain,jobs[j]['value'],-c,-j,-i,-k)
                    if best is None or key>best[0]:best=(key,i,j,trial)
        if best is None:break
        _,i,j,trial=best;routes[i]=trial;remaining.remove(j)
    commands={}
    for i,route in enumerate(routes):
        pos=starts[i];out=[]
        for j in route:
            target=jobs[j]['xy'];out+=paths[pos][target]+jobs[j]['actions'];pos=target
        home=min(homes,key=lambda h:(len(paths[pos][h]),h))
        out+=paths[pos][home]+[['DROP']]
        commands[i]=out
    _C378_REPORT.update(plans=1,planned_jobs=sum(map(len,routes)),unassigned_jobs=len(remaining),planned_value=sum(jobs[j]['value'] for r in routes for j in r))
    return dict(start=step,commands=commands)

def agent(observation,configuration=None):
    step=int(observation['step'])
    if step==0:
        _C378_STATE.clear();_C378_REPORT.clear();_C378_REPORT.update(plans=0,changed_turns=0)
    action=_C378_PARENT(observation,configuration)
    if not _C378_ENABLED or not 700<=step<=718:return action
    if configuration is not None and any(configuration.get(k,v)!=v for k,v in [('episodeSteps',720),('boardSize',10),('turnsPerDay',24)]):return action
    seat=int(observation['player'])
    if seat not in _C378_STATE:_C378_STATE[seat]=_c378_plan(observation)
    state=_C378_STATE[seat];offset=step-state['start'];farm=observation['farms'][seat]
    units=[]
    for i in range(len(farm['hands'])+1):
        route=state['commands'].get(i,[]);units.append(route[offset] if offset<len(route) else ['PASS'])
    result=dict(action,farmer=units[0],hands=units[1:],market=[])
    # Simulate physical unit actions in official order using the existing pinned helper.
    f,p=_C365_CA_NS['_PLANNER_NS']['_clone_state'](farm,observation['private'])
    for i,c in enumerate(units):_C365_CA_NS['_PLANNER_NS']['_apply_unit_action'](f,p,i,c,10,29,24,100)
    prices=observation['market']['prices']
    products=sorted(_C378_PRODUCTS,key=lambda k:(-prices[k],k))
    result['market']=[['SELL',k,int(p['shed'].get(k,0))] for k in products if p['shed'].get(k,0)>0]
    _C378_REPORT['changed_turns']+=int(result!=action)
    return result
agent.telemetry=_C378_REPORT
kaggle_submission_agent=agent
c378_submission_agent=agent
'''
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
 parent=(ROOT/'agent/o302_farmer_feed_topup.py').read_bytes();assert hashlib.sha256(parent).hexdigest()==PARENT_SHA
 engine=ROOT/'.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py'
 tree=ast.parse(engine.read_text('utf8'))
 crops=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CROPS' for t in n.targets))
 constants={k:(v['first_yield_day'],0 if v['ongoing'] else v['max_yield_day'],v['max_yield']) for k,v in crops.items()}
 data=parent.rstrip()+WRAPPER.replace('__ON__',str(not a.disabled)).replace('__CROPS__',repr(constants)).encode();compile(data,str(a.out),'exec')
 if a.out.exists():raise FileExistsError(a.out)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data);print(a.out,hashlib.sha256(data).hexdigest())
if __name__=='__main__':main()
