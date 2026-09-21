# SPDX-License-Identifier: Apache-2.0
"""c334: d11 tomato lanes with funded age7 fertilizer / age8 water tours.

Uses current observation and own selected program only. Imported c170 helper
functions implement spawn-aware assignment; source helpers are embedded by build.
"""
import copy as _c334_copy
_C334_PARENT = agent
_C334_ON = True
_C334_STATES = {}
_C334_REPORT = {}
del agent

def _c334_gain(target, arrival, day):
    return 1

def _c334_new():
    return dict(last=-1, day=-1, workers={}, pending=None, requested=[], counts={})

def _c334_count(st,key,n=1):
    st['counts'][key]=st['counts'].get(key,0)+n

def _c334_reserve(obs):
    seat=int(obs['player']);day=int(obs['step'])//24
    native=_IMPL.chassis.players.get(seat) or {}
    maximum=0
    for route in {native.get('route',0),2}:
        for a in _IMPL.chassis.routes[route][day*24:(day+1)*24]:
            for i,c in enumerate(a.get('hands') or []):
                if c and c!=['PASS']:maximum=max(maximum,i+1)
    return maximum

def _c334_apply(obs,action,st):
    step=int(obs['step']);day=step//24;seat=int(obs['player']);farm=obs['farms'][seat];private=obs['private']
    if st['day']!=day:
        if st['workers']:
            _c334_count(st,'unfinished_targets',sum(len(p['path']) for p in st['workers'].values()))
        st.update(day=day,workers={},pending=None,requested=[])
    for xy,op in st['requested']:
        t=farm['tiles'][xy[1]][xy[0]]
        ok=isinstance(t,dict) and t.get('crop')=='TOMATO' and (t.get('fertilized_until_day',-1)>=day+2 if op=='FERTILIZE' else t.get('watered_today',False))
        _c334_count(st,'confirmed_'+op.lower() if ok else 'service_failures')
    st['requested']=[]
    if st['pending']:
        plans=st.pop('pending');st['pending']=None
        if len(farm['hands'])!=max(plans):
            _c334_count(st,'hire_failures',len(plans))
        else:
            for actor,plan in plans.items():
                if tuple(farm['hands'][actor-1])!=tuple(plan['spawn']):
                    _c334_count(st,'spawn_failures');continue
                st['workers'][actor]=plan;_c334_count(st,'confirmed_hires')
    if day<18 or day>22 or not ((_C177_STATES.get(seat) or {}).get('sites') or st['workers']):
        return action
    result=_c334_copy.deepcopy(action)
    cmds=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
    cmds += [['PASS'] for _ in range(len(farm['hands'])+1-len(cmds))]
    sites=(_C177_STATES.get(seat) or {}).get('sites',set())
    positions=[farm['farmer'],*farm['hands']];claimed=set()
    for actor,(pos,cmd) in enumerate(zip(positions,cmds)):
        xy=tuple(pos)
        if xy not in sites or xy in claimed or cmd[0] not in ('FERTILIZE','WATER'):continue
        t=farm['tiles'][pos[1]][pos[0]]
        if not isinstance(t,dict) or t.get('crop')!='TOMATO' or t.get('planted_day')!=11 or t.get('yield_units',0)<=0:continue
        if cmd[0]=='FERTILIZE' or day>=22:
            cmds[actor]=['HARVEST'];claimed.add(xy);_c334_count(st,'harvest_replacements')
    result['farmer'],result['hands']=cmds[0],cmds[1:]
    available=int(projected_shed(result,FarmView(obs)).get('FERTILIZER',0))
    for actor,plan in st['workers'].items():
        if actor>len(farm['hands']):
            _c334_count(st,'missing_actor');continue
        if cmds[actor]!=['PASS']:
            _c334_count(st,'parent_actor_conflicts');continue
        pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
        if not plan['loaded']:
            q=len(plan['path'])
            if available<q or pos not in _C334_ACCESS:
                _c334_count(st,'load_waits');continue
            cmds[actor]=['PICKUP','FERTILIZER',q];available-=q;plan['loaded']=True
            _c334_count(st,'pickup_units',q);continue
        while plan['path']:
            x,y,crop,birth=plan['path'][0];t=farm['tiles'][y][x]
            if not isinstance(t,dict) or t.get('crop')!=crop or t.get('planted_day')!=birth:
                _c334_count(st,'lost_targets');plan['path'].pop(0);continue
            done=t.get('fertilized_until_day',-1)>=day+2 if plan['op']=='FERTILIZE' else t.get('watered_today',False)
            if done:plan['path'].pop(0);_c334_count(st,'already_served');continue
            if plan['op']=='FERTILIZE' and inv.get('FERTILIZER',0)<=0:
                _c334_count(st,'input_shortfalls');break
            cmd=_v219_walk(pos,(x,y)) or [plan['op']];cmds[actor]=cmd
            if cmd[0]==plan['op']:
                st['requested'].append(((x,y),plan['op']));plan['path'].pop(0);_c334_count(st,'requested_'+plan['op'].lower())
            break
    result['farmer'],result['hands']=cmds[0],cmds[1:]
    if step%24!=4 or day not in (18,19) or not sites:return result
    if any(o and o[0]=='HIRE' for o in result.get('market',[])) or len(farm['hands'])<_c334_reserve(obs):
        _c334_count(st,'reservation_declines');return result
    for name in ('_V219_STATES','_V231_STATES','_V233_STATES','_R51_INPUT_STATES'):
        state=(globals().get(name,{}) or {}).get(seat) or {}
        if state.get('pending'):
            _c334_count(st,'pending_declines');return result
    op='FERTILIZE' if day==18 else 'WATER'
    rows=[]
    for x,y in sorted(sites):
        t=farm['tiles'][y][x]
        if not isinstance(t,dict) or t.get('crop')!='TOMATO' or t.get('planted_day')!=11:continue
        done=t.get('fertilized_until_day',-1)>=day+2 if op=='FERTILIZE' else t.get('watered_today',False)
        if not done:rows.append((x,y,'TOMATO',11))
    if not rows:return result
    selected=None
    for count in (1,2):
        if count>len(rows):continue
        proposed=_c334_copy.deepcopy(result);proposed['market']=list(result.get('market') or [])+([['BUY_PRODUCT','FERTILIZER',len(rows)]] if op=='FERTILIZE' else [])+[['HIRE']]*count
        if len(proposed['market'])>10:continue
        starts=_c334_spawn_starts(obs,proposed,count)
        if op=='WATER':starts=[(t-1,p) for t,p in starts]
        quotas=[len(rows)] if count==1 else [(len(rows)+1)//2,len(rows)//2]
        paths,expanded=_c334_search(rows,quotas,starts,{r:None for r in rows},{'TOMATO':1},day,{r:1 for r in rows})
        _c334_count(st,'search_expansions',expanded)
        if paths is not None:selected=(proposed,count,starts,paths);break
    if selected is None:
        _c334_count(st,'route_declines');return result
    proposed,count,starts,paths=selected
    q=len(rows) if op=='FERTILIZE' else 0
    stock=projected_shed(result,FarmView(obs));buys=sum(int(o[2]) for o in result.get('market',[]) if len(o)>2 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    if q and sum(stock.values())+buys+q>95:
        _c334_count(st,'capacity_declines');return result
    quote=max(1,_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-q))
    cost=q*(quote+5)+sum(_v219_fib(int(farm['hires_today'])+i) for i in range(count))
    if farm['money']<cost+3000:
        _c334_count(st,'cash_declines');return result
    first=len(farm['hands'])+1
    st['pending']={first+i:dict(path=list(paths[i]),spawn=list(starts[i][1]),op=op,loaded=op!='FERTILIZE') for i in range(count)}
    _c334_count(st,'requested_hires',count);_c334_count(st,'fert_purchase_units',q);_c334_count(st,'tour_days')
    return proposed

def agent(observation,configuration=None):
    result=_C334_PARENT(observation,configuration)
    if not _C334_ON:return result
    seat=int(observation['player']);step=int(observation['step']);st=_C334_STATES.get(seat)
    if st is None or step<=st['last']:st=_C334_STATES[seat]=_c334_new()
    st['last']=step
    try:result=_c334_apply(observation,result,st)
    except Exception:
        _c334_count(st,'errors');raise
    _C334_REPORT.clear();_C334_REPORT.update({'c334_'+k:v for k,v in st['counts'].items()})
    return result

agent.telemetry=_C334_REPORT
agent=globals().pop('agent')
