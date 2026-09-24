# c379 terminal dependency-preserving compaction, Taeyang/Codex, 2026-09-22.
# Parent's native final-day harvest/water/delivery order is kept per actor and
# shared tile. Only ineffective service and travel detours are removed.
from collections import deque as _c379_deque
_C379_PARENT = agent
_C379_ENABLED = True
_C379_STATE = {}
_C379_REPORT = {}
_C379_PRODUCTS = ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')

def _c379_paths(grid):
    n=len(grid);paths={}
    for y,row in enumerate(grid):
        for x,tile in enumerate(row):
            if tile=='LOCKED':continue
            start=(x,y);paths[start]={start:[]};q=_c379_deque([start])
            while q:
                pos=q.popleft()
                for cmd,dx,dy in [('NORTH',0,-1),('WEST',-1,0),('SOUTH',0,1),('EAST',1,0)]:
                    nxt=(pos[0]+dx,pos[1]+dy)
                    if 0<=nxt[0]<n and 0<=nxt[1]<n and grid[nxt[1]][nxt[0]]!='LOCKED' and nxt not in paths[start]:
                        paths[start][nxt]=paths[start][pos]+[[cmd]];q.append(nxt)
    return paths

def _c379_plan(obs,action):
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat]
    ns=_C365_CA_NS['_PLANNER_NS'];f,p=ns['_clone_state'](farm,obs['private'])
    tape=_C358_IMPL.chassis.routes[2];starts=[tuple(farm['farmer'])]+list(map(tuple,farm['hands']))
    count=min(len(starts),1+max(len(a.get('hands',[])) for a in tape[step:719]))
    # Controllers beyond the native crew retain their parent commands.
    dynamic=set(_C365_CA_NS.get('_R51_INPUT_STATES',{}).get(seat,{}).get('workers',{}))
    if any(i<count for i in dynamic):return None
    jobs=[]
    for t in range(step,719):
        frame=action if t==step else tape[t]
        units=[frame.get('farmer') or ['PASS']]+list(frame.get('hands') or [])
        for i in range(count):
            cmd=units[i] if i<len(units) else ['PASS'];pos=tuple(([f['farmer']]+f['hands'])[i])
            tile=f['tiles'][pos[1]][pos[0]]
            before=dict(p['inventories'][i]);before_shed=dict(p['shed'])
            old_yield=tile.get('yield_units',0) if isinstance(tile,dict) else 0
            ns['_apply_unit_action'](f,p,i,cmd,10,29,24,100)
            after=p['inventories'][i]
            tile_after=f['tiles'][pos[1]][pos[0]]
            new_yield=tile_after.get('yield_units',0) if isinstance(tile_after,dict) else 0
            useful=(cmd[0]=='HARVEST' and any(after.get(k,0)>before.get(k,0) for k in _C379_PRODUCTS))
            useful|=(cmd[0]=='WATER' and new_yield>old_yield)
            useful|=(cmd[0]=='COLLECT_FERTILIZER' and after.get('FERTILIZER',0)>before.get('FERTILIZER',0))
            useful|=(cmd[0] in ('DROP','PLACE') and p['shed']!=before_shed)
            if useful:jobs.append(dict(t=t,i=i,pos=pos,cmd=cmd[:],cargo=sum(before.get(k,0) for k in _C379_PRODUCTS) if cmd[0]=='DROP' else 0))
        # Original sale timing is not needed for physical demand; no purchases.
        p['shed']={k:0 for k in p['shed']}
    paths=_c379_paths(farm['tiles']);out={i:{} for i in range(count)}
    current=starts[:];ready=[step]*count;tile_ready={};drop_load={};advance=0
    for job in jobs:
        i=job['i'];target=job['pos'];route=paths[current[i]][target]
        service=job['cmd'][0] in ('WATER','HARVEST','COLLECT_FERTILIZER')
        dependency=tile_ready.get(target,(step,-1)) if service else (step,-1)
        at=max(ready[i]+len(route),dependency[0]+int(i<=dependency[1]))
        if job['cargo']:
            while drop_load.get(at,0)+job['cargo']>100:at+=1
        if at>job['t'] or at>718:
            _C379_REPORT['support_declined']+=1;return None
        for j,c in enumerate(route):out[i][ready[i]+j]=c
        out[i][at]=job['cmd'];ready[i]=at+1;current[i]=target
        # All useful service on a tile retains the original joint ordering.
        if service:tile_ready[target]=(at,i)
        advance+=job['t']-at
        if job['cargo']:drop_load[at]=drop_load.get(at,0)+job['cargo']
    _C379_REPORT.update(plans=1,jobs=len(jobs),native_actors=count,advance=advance)
    return out

def agent(observation,configuration=None):
    step=int(observation['step']);seat=int(observation['player'])
    if step==0:
        _C379_STATE.clear();_C379_REPORT.clear();_C379_REPORT.update(plans=0,jobs=0,support_declined=0,changed_turns=0)
    action=_C379_PARENT(observation,configuration)
    if not _C379_ENABLED or not 700<=step<=718:return action
    if configuration is not None and any(configuration.get(k,v)!=v for k,v in [('episodeSteps',720),('turnsPerDay',24),('boardSize',10)]):return action
    if seat not in _C379_STATE:_C379_STATE[seat]=_c379_plan(observation,action)
    plan=_C379_STATE[seat]
    if plan is None:return action
    farm=observation['farms'][seat]
    units=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
    while len(units)<len(farm['hands'])+1:units.append(['PASS'])
    for i,route in plan.items():units[i]=route.get(step,['PASS'])
    f,p=_C365_CA_NS['_PLANNER_NS']['_clone_state'](farm,observation['private'])
    for i,c in enumerate(units):_C365_CA_NS['_PLANNER_NS']['_apply_unit_action'](f,p,i,c,10,29,24,100)
    prices=observation['market']['prices'];products=sorted(_C379_PRODUCTS,key=lambda k:(-prices[k],k))
    result=dict(action,farmer=units[0],hands=units[1:],market=[['SELL',k,int(p['shed'].get(k,0))] for k in products if p['shed'].get(k,0)>0])
    _C379_REPORT['changed_turns']+=int(result!=action)
    return result
agent.telemetry=_C379_REPORT
kaggle_submission_agent=agent
c379_submission_agent=agent
