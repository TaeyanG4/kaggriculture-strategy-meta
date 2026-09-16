# o174_tet_funding (Claude/o-series, 2026-09-15). Tetsutani-lineage funding/order-sequencing tail (EXP231 r97, r124 funded planting, r127 urgent grain slot, r128 service order) ported verbatim onto o162.
# Source: public notebook tetsutani/market-smart-farming-kaggriculture (2026-09-15 pull), lines 2725-3173; upstream notices retained inside.


# EXP231: protect inputs using funded current orders without unassigned cash padding from observed physical resources.
_R97_PARENT=agent
_R97_REPORT={}
_R97_LAST={}

def _r97_market_stock(shed,orders):
    stock=dict(shed);buys={};sales={}
    for index,order in enumerate(orders):
        if len(order)<3:continue
        op,item,n=order[:3];n=max(0,int(n))
        if op=='SELL':
            q=min(n,max(0,stock.get(item,0)));stock[item]=stock.get(item,0)-q;sales[index]=q
        elif op in ('BUY_PRODUCT','BUY_ANIMAL'):
            q=min(n,max(0,100-sum(stock.values())));stock[item]=stock.get(item,0)+q;buys[index]=q
    return stock,buys,sales

def _r97_delivery(stock,private,night):
    stock=dict(stock);lost={}
    if night:
        for inv in private['inventories']:
            for item,q in inv.items():
                q=max(0,int(q));take=min(q,max(0,100-sum(stock.values())))
                stock[item]=stock.get(item,0)+take
                if q>take:lost[item]=lost.get(item,0)+q-take
    return stock,lost

def _r97_budget(obs,orders):
    farm=obs['farms'][obs['player']];cost=0;hires=int(farm['hires_today'])
    # At most ten 100-unit purchases per opponent turn. The additional 1000
    # own units give an intentionally conservative upper bound on buy quotes.
    prices={p:_r37_market_price(p,obs['market']['inventory'][p]-2000) for p in ('WHEAT','FERTILIZER')}
    for order in orders:
        if not order:continue
        op=order[0]
        if op=='HIRE':cost+=_v219_fib(hires);hires+=1
        elif op=='BUY_LAND':cost+=4000
        elif len(order)>2:
            item=order[1];q=max(0,int(order[2]))
            if op=='BUY_PRODUCT':cost+=q*prices[item]
            elif op=='BUY_ANIMAL':cost+=q*{'GOOSE':300,'COW':400,'SHEEP':500}[item]
            elif op=='BUY_SEED':cost+=q*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[item]
    return cost<=farm['money']  # No current sale proceeds are assumed.

def _r97_supply(obs,action):
    step=int(obs['step']);player=int(obs['player']);day=step//24
    if not 144<=step<695:return action
    native=_IMPL.chassis.players[player]
    future=_IMPL.chassis.routes[2 if step+1>=648 else native['route']][step+1]
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    following=_IMPL.chassis.routes[2 if step+2>=648 else native['route']][step+2]
    next_orders=future.get('market') or []
    prefund=0
    if len(next_orders)==10 and not any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in next_orders):
        later=[following.get('farmer') or ['PASS'],*(following.get('hands') or [])]
        demand=lambda cs:sum(max(0,int(c[2]) if len(c)>2 else 1) for c in cs if c[:2]==['PICKUP','WHEAT'])
        if demand(later):prefund=demand(commands)+demand(later)
    if not prefund and not any(c[:2]==['PICKUP','WHEAT'] for c in commands):return action
    orders=action.get('market') or []
    if len(orders)>10 or not _r97_budget(obs,orders):
        _R97_REPORT['supply_budget_declines']+=1;return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][player],obs['private'])
    for actor,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])];night=step%24==23
    access=((4,4),(5,4),(4,5),(5,5))
    if night:positions=[(4,4)]
    else:
        for order in orders:
            if order and order[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    need=sum(max(0,int(c[2]) if len(c)>2 else 1) for pos,c in zip(positions,commands) if pos in access and c[:2]==['PICKUP','WHEAT'])
    need=max(need,prefund)
    if not need:return action
    original_stock,original_buys,_=_r97_market_stock(private['shed'],orders)
    original_final,original_loss=_r97_delivery(original_stock,private,night)
    if original_final.get('WHEAT',0)>=need:return action
    result=copy.deepcopy(action);proposed=result['market'];blocked=False
    def project(candidate):
        stock,buys,sales=_r97_market_stock(private['shed'],candidate)
        final,loss=_r97_delivery(stock,private,night)
        safe=all(buys.get(i,0)>=q for i,q in original_buys.items()) and all(q<=original_loss.get(item,0) for item,q in loss.items())
        return final,sales,safe
    # Hold an existing grain sale first. Preserve all order indices and every
    # originally funded buy; no extra overnight overflow may be introduced.
    for index in range(len(proposed)-1,-1,-1):
        if proposed[index][:2]!=['SELL','WHEAT']:continue
        final,sales,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
        if not shortage:break
        sold=sales.get(index,0)
        if not sold:continue
        old=proposed[index][2];proposed[index][2]=max(0,sold-shortage)
        after,_,safe=project(proposed)
        if not safe or after.get('WHEAT',0)<=final.get('WHEAT',0):proposed[index][2]=old
    final,_,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
    if shortage:
        last_sale=max((i for i,o in enumerate(proposed) if o[:2]==['SELL','WHEAT']),default=-1)
        index=next((i for i in range(len(proposed)-1,last_sale,-1) if proposed[i][:2]==['BUY_PRODUCT','WHEAT']),None)
        if index is not None:proposed[index][2]=max(0,int(proposed[index][2]))+shortage
        elif len(proposed)<10:proposed.append(['BUY_PRODUCT','WHEAT',shortage])
        else:_R97_REPORT['supply_slot_declines']+=1;return action
    final,_,safe=project(proposed)
    if not safe or final.get('WHEAT',0)<need:
        _R97_REPORT['supply_capacity_declines']+=1;return action
    if not _r97_budget(obs,proposed):
        _R97_REPORT['supply_budget_declines']+=1;return action
    if prefund:
        _R97_REPORT['supply_prefund_changes']+=1
        _R97_REPORT['supply_prefund_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    if step<288:
        _R97_REPORT['supply_early_changes']+=1
        _R97_REPORT['supply_early_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    _R97_REPORT['supply_guard_changes']+=1
    _R97_REPORT['supply_grain_protected']+=final.get('WHEAT',0)-original_final.get('WHEAT',0)
    _R97_REPORT['supply_buy_units']+=sum(max(0,int(o[2])) for o in proposed if o[:2]==['BUY_PRODUCT','WHEAT'])-sum(max(0,int(o[2])) for o in orders if o[:2]==['BUY_PRODUCT','WHEAT'])
    return result

def agent(observation,configuration=None):
    result=_R97_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step'])
        if player not in _R97_LAST or step<=_R97_LAST[player]:
            _R97_REPORT.update(supply_guard_changes=0,supply_grain_protected=0,supply_buy_units=0,supply_early_changes=0,supply_early_units=0,supply_prefund_changes=0,supply_prefund_units=0,supply_slot_declines=0,supply_capacity_declines=0,supply_budget_declines=0,supply_errors=0)
        _R97_LAST[player]=step
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)]):result=_r97_supply(observation,result)
    except Exception:_R97_REPORT['supply_errors']=_R97_REPORT.get('supply_errors',0)+1
    _R97_REPORT.update(getattr(_R97_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R97_REPORT
agent=globals().pop('agent')

"""Original funded planting and first-dawn labor contract, Ahmed Berat Ozer."""
_R124_PARENT=agent
_R124_STATES={}
_R124_REPORT={}

def _r124_labor_reserve(native):
    n=sum(bool(o) and o[0]=='HIRE' for o in native[24].get('market',[]))
    return sum(_v219_fib(i) for i in range(n)),n

def _r124_seed_budget(obs,action,reserve):
    if not any(o and o[0]=='BUY_SEED' for o in action.get('market',[])):return action
    player=int(obs['player']);budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][player]['money']-=reserve
    if _r97_budget(budget,action.get('market',[])):return action
    result=copy.deepcopy(action)
    for i in range(len(result['market'])-1,-1,-1):
        order=result['market'][i]
        if len(order)<3 or order[0]!='BUY_SEED':continue
        before=max(0,int(order[2]));order[2]=before
        while order[2]>0 and not _r97_budget(budget,result['market']):order[2]-=1
        n=before-order[2]
        if n:
            _R124_REPORT['opening_seed_budget_units']+=n
            _R124_REPORT['opening_seed_budget_cost']+=n*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
        if _r97_budget(budget,result['market']):break
    return result

def _r124_atomic(obs,action,state):
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    if not demand:return action
    available=obs['private']['seeds'];blocked={p for p,n in demand.items() if n>available.get(p,0)}
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    changed=False;kept=[]
    for actor,c in enumerate(commands):
        if len(c)>1 and c[0]=='PLANT':
            pos=None if actor>=len(private['inventories']) else farm['farmer'] if actor==0 else farm['hands'][actor-1]
            valid=pos is not None and farm['tiles'][pos[1]][pos[0]] is None and private['seeds'].get(c[1],0)>0
            if not valid:
                commands[actor]=['PASS'];changed=True;_R124_REPORT['opening_atomic_dropped']+=1
            elif c[1] in blocked:
                kept.append(dict(xy=list(pos),crop=c[1],birth=0));_R124_REPORT['opening_atomic_rescued_requests']+=1
        if actor<len(private['inventories']):_PLANNER_NS['_apply_unit_action'](farm,private,actor,commands[actor],10,0,24,100)
    if kept:state['pending_plants']=kept
    if changed:
        action=dict(action,farmer=commands[0],hands=commands[1:])
    return action

def agent(observation,configuration=None):
    result=_R124_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step']);state=_R124_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R124_STATES[player]={'step':-1,'pending_plants':[]}
            _R124_REPORT.update(opening_seed_budget_units=0,opening_seed_budget_cost=0,opening_atomic_dropped=0,opening_atomic_rescued_requests=0,opening_atomic_rescued_confirmed=0,opening_atomic_plant_errors=0,opening_day1_cash=0,opening_day1_hires_requested=0,opening_day1_hires_confirmed=0,opening_day1_hire_shortfalls=0,opening_contract_errors=0)
        state['step']=step;farm=observation['farms'][player]
        for p in state.pop('pending_plants',[]):
            x,y=p['xy'];t=farm['tiles'][y][x]
            if isinstance(t,dict) and t.get('crop')==p['crop'] and t.get('planted_day')==p['birth']:_R124_REPORT['opening_atomic_rescued_confirmed']+=1
            else:_R124_REPORT['opening_atomic_plant_errors']+=1
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard and 0<=step<24:
            native=_ROUTES[_IMPL.chassis.players[player]['route']];reserve,hires=_r124_labor_reserve(native)
            result=_r124_seed_budget(observation,result,reserve);result=_r124_atomic(observation,result,state)
        if step==24:
            _R124_REPORT['opening_day1_cash']=farm['money'];state['hires']=sum(bool(o) and o[0]=='HIRE' for o in result.get('market',[]));_R124_REPORT['opening_day1_hires_requested']=state['hires']
        if step==25:
            actual=len(farm['hands']);_R124_REPORT['opening_day1_hires_confirmed']=actual;_R124_REPORT['opening_day1_hire_shortfalls']=max(0,state.get('hires',0)-actual)
    except Exception:_R124_REPORT['opening_contract_errors']=_R124_REPORT.get('opening_contract_errors',0)+1
    _R124_REPORT.update(getattr(_R124_PARENT,'telemetry',{}))
    return result
agent.telemetry=_R124_REPORT
agent=globals().pop('agent')

"""Fund urgent grain at the first quote slot; avoid unwatered last-hour plants.
Original safety contracts by Ahmed Berat Ozer, EXP258.
"""
_R127_PARENT=agent
_R127_STATES={}
_R127_REPORT={}

def _r127_fields(obs,action):
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={p for p,n in demand.items() if n>private['seeds'].get(p,0)}
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:continue
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,int(obs['step'])//24,24,100)
    return farm,private

def _r127_last_hour(obs,action):
    if int(obs['step'])%24!=23:return action
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    if not any(c and c[0]=='PLANT' for c in commands):return action
    result=copy.deepcopy(action);changed=False
    # Removing rejected requests can unblock the engine's atomic crop batch.
    # Recompute until every retained request ends the turn with a watered crop.
    for _ in range(len(commands)+1):
        farm,_=_r127_fields(obs,result);original=obs['farms'][obs['player']]
        positions=[original['farmer'],*original['hands']];drop=[]
        for actor,c in enumerate(commands):
            if not c or c[0]!='PLANT':continue
            tile=None
            if actor<len(positions):
                x,y=positions[actor];tile=farm['tiles'][y][x]
            if not (isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('crop')==c[1] and tile.get('planted_day')==int(obs['step'])//24 and tile.get('watered_today')):drop.append(actor)
        if not drop:break
        for actor in drop:commands[actor]=['PASS']
        result['farmer']=commands[0];result['hands']=commands[1:];changed=True
        _R127_REPORT['last_hour_plants_dropped']+=len(drop)
    return result if changed else action

def _r127_prefix_bound(obs,quantity):
    inventory=int(obs['market']['inventory']['WHEAT'])
    # Both players quote one unit before either commits. Before own unit j,
    # at most j-1 own and j-1 opponent wheat purchases have depleted inventory.
    return sum(_r37_market_price('WHEAT',inventory-(2*j-1)) for j in range(1,quantity+1))

def _r127_priority(obs,action,state):
    step=int(obs['step']);player=int(obs['player'])
    if not 144<=step<695:return action
    orders=action.get('market') or []
    if len(orders)>9 or any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in orders):return action
    native=_IMPL.chassis.players[player]
    future=_IMPL.chassis.routes[2 if step+1>=648 else native['route']][step+1]
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    if not any(c[:2]==['PICKUP','WHEAT'] for c in commands):return action
    if not _r97_budget(obs,orders):return action
    farm,private=_r127_fields(obs,action);night=step%24==23
    access=((4,4),(5,4),(4,5),(5,5));positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    if night:positions=[(4,4)]
    else:
        for o in orders:
            if o and o[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    need=sum(max(0,int(c[2]) if len(c)>2 else 1) for pos,c in zip(positions,commands) if pos in access and c[:2]==['PICKUP','WHEAT'])
    stock,buys,_=_r97_market_stock(private['shed'],orders);before,loss=_r97_delivery(stock,private,night)
    shortage=max(0,need-before.get('WHEAT',0))
    if not shortage or shortage>100-sum(private['shed'].values()):return action
    cost=_r127_prefix_bound(obs,shortage)
    budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][player]['money']-=cost
    if not _r97_budget(budget,orders):return action
    proposed=[['BUY_PRODUCT','WHEAT',shortage],*copy.deepcopy(orders)]
    stock,after_buys,_=_r97_market_stock(private['shed'],proposed);after,after_loss=_r97_delivery(stock,private,night)
    if after.get('WHEAT',0)<need or any(after_buys.get(i+1,0)<q for i,q in buys.items()) or any(q>loss.get(p,0) for p,q in after_loss.items()):return action
    state['pending_grain']=(step+1,after.get('WHEAT',0),shortage)
    _R127_REPORT['priority_grain_orders']+=1;_R127_REPORT['priority_grain_units']+=shortage
    return dict(action,market=proposed)

def agent(observation,configuration=None):
    result=_R127_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step']);state=_R127_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R127_STATES[player]={'step':-1}
            _R127_REPORT.update(last_hour_plants_dropped=0,priority_grain_orders=0,priority_grain_units=0,priority_grain_confirmed=0,priority_grain_shortfalls=0,priority_contract_errors=0)
        pending=state.pop('pending_grain',None)
        if pending and step==pending[0]:
            if observation['private']['shed'].get('WHEAT',0)>=pending[1]:_R127_REPORT['priority_grain_confirmed']+=pending[2]
            else:_R127_REPORT['priority_grain_shortfalls']+=1
        state['step']=step
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard:result=_r127_priority(observation,_r127_last_hour(observation,result),state)
    except Exception:_R127_REPORT['priority_contract_errors']=_R127_REPORT.get('priority_contract_errors',0)+1
    _R127_REPORT.update(getattr(_R127_PARENT,'telemetry',{}))
    return result
agent.telemetry=_R127_REPORT
agent=globals().pop('agent')

"""Observed-input service order and guaranteed first-sale funding, Ahmed Berat Ozer."""
_R128_PARENT=agent
_R128_STATES={}
_R128_REPORT={}

def _r128_commands(action):
    return [action.get('farmer') or ['PASS'],*(action.get('hands') or [])]

def _r128_future(obs,offset=1):
    step=int(obs['step'])+offset;native=_IMPL.chassis.players[int(obs['player'])]
    return _IMPL.chassis.routes[2 if step>=648 else native['route']][step]

def _r128_sale_credit(obs,action):
    orders=action.get('market') or []
    if not orders or len(orders[0])<3 or orders[0][0]!='SELL' or orders[0][1]=='WHEAT':return 0
    item=orders[0][1]
    if item not in obs['market']['inventory']:return 0
    _,private=_r127_fields(obs,action)
    q=min(max(0,int(orders[0][2])),max(0,int(private['shed'].get(item,0))))
    inventory=int(obs['market']['inventory'][item])
    return sum(_r37_market_price(item,inventory+2*j) for j in range(q))

def _r128_next_need(obs,farm,orders,advanced):
    step=int(obs['step']);access=((4,4),(5,4),(4,5),(5,5))
    positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    if step%24==23:positions=[(4,4)]
    else:
        for order in orders:
            if order and order[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    return sum(max(0,int(c[2]) if len(c)>2 else 1) for actor,(p,c) in enumerate(zip(positions,_r128_commands(_r128_future(obs)))) if actor not in advanced and p in access and c[:2]==['PICKUP','WHEAT'])

def _r128_field_safe(obs,before,after,advanced):
    orders=before.get('market') or []
    if not _r97_budget(obs,orders):return False,None
    oldfarm,oldprivate=_r127_fields(obs,before);farm,private=_r127_fields(obs,after)
    oldcommands=_r128_commands(before);commands=_r128_commands(after)
    for i,c in enumerate(oldcommands[:len(private['inventories'])]):
        if c and c[0]=='PICKUP' and c==commands[i]:
            item=c[1]
            if private['inventories'][i].get(item,0)<oldprivate['inventories'][i].get(item,0):return False,None
    oldstock,oldbuys,oldsales=_r97_market_stock(oldprivate['shed'],orders)
    stock,buys,sales=_r97_market_stock(private['shed'],orders)
    oldfinal,oldloss=_r97_delivery(oldstock,oldprivate,int(obs['step'])%24==23)
    final,loss=_r97_delivery(stock,private,int(obs['step'])%24==23)
    if any(buys.get(i,0)<q for i,q in oldbuys.items()) or any(sales.get(i,0)<q for i,q in oldsales.items()) or any(q>oldloss.get(p,0) for p,q in loss.items()):return False,None
    need=_r128_next_need(obs,farm,orders,advanced)
    pending=_R127_STATES.get(int(obs['player']),{}).get('pending_grain')
    if pending and pending[0]==int(obs['step'])+1:need=max(need,pending[1])
    if final.get('WHEAT',0)<min(need,oldfinal.get('WHEAT',0)):return False,None
    return True,private

def _r128_food_need(obs,farm,private,actor):
    farm,private=copy.deepcopy(farm),copy.deepcopy(private);missing=0;day=int(obs['step'])//24
    for offset in range(1,min(5,24-int(obs['step'])%24)):
        cs=_r128_commands(_r128_future(obs,offset));c=cs[actor] if actor<len(cs) else ['PASS']
        if c[:2]==['PICKUP','WHEAT']:break
        if c==['FEED']:
            x,y=farm['farmer'] if actor==0 else farm['hands'][actor-1];tile=farm['tiles'][y][x]
            if isinstance(tile,dict) and tile.get('animal') and not tile.get('fed_today') and private['inventories'][actor].get('WHEAT',0)<=0:
                private['inventories'][actor]['WHEAT']=1;missing+=1
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    return missing

def _r128_service(obs,action,state):
    step=int(obs['step']);farm=obs['farms'][obs['player']];private=obs['private'];positions=[farm['farmer'],*farm['hands']]
    for item in state.pop('arrivals',[]):
        if item['step']!=step or item['actor']>=len(private['inventories']) or private['inventories'][item['actor']].get('WHEAT',0)<item['expected']:_R128_REPORT['service_arrival_errors']+=1
        else:_R128_REPORT['service_confirmed_units']+=item['quantity']
    old_pending=state.pop('swaps',{});result=action;cs=_r128_commands(result)
    for actor,pending in old_pending.items():
        if step!=pending['step'] or actor>=len(positions) or list(positions[actor])!=pending['xy'] or cs[actor]!=pending['pickup']:
            _R128_REPORT['service_swap_errors']+=1;continue
        x,y=positions[actor];tile=farm['tiles'][y][x]
        if not isinstance(tile,dict) or tile.get('animal')!=pending['animal'] or tile.get('placed_day')!=pending['birth']:
            _R128_REPORT['service_swap_errors']+=1;continue
        if private['inventories'][actor].get('WHEAT',0)<pending['quantity']+1:
            _R128_REPORT['service_swap_errors']+=1;continue
        cs[actor]=['PASS'] if tile.get('fed_today') else ['FEED']
        _R128_REPORT['service_swaps_completed']+=1
    if old_pending:
        proposed=dict(result,farmer=cs[0],hands=cs[1:]);safe,_=_r128_field_safe(obs,result,proposed,{})
        if safe:result=proposed
        else:_R128_REPORT['service_swap_errors']+=1
    if not 144<=step<647:return result
    cs=_r128_commands(result);future=_r128_commands(_r128_future(obs));proposed=copy.deepcopy(result);commands=_r128_commands(proposed)
    swaps={};arrivals=[];prefetches=0
    projected_farm,projected_private=_r127_fields(obs,result)
    for actor,c in enumerate(cs[:len(private['inventories'])]):
        x,y=positions[actor]
        if (x,y) not in ((4,4),(5,4),(4,5),(5,5)):continue
        held=max(0,int(private['inventories'][actor].get('WHEAT',0)));tile=farm['tiles'][y][x]
        nxt=future[actor] if actor<len(future) else ['PASS']
        if c==['FEED'] and held==0 and step%24<=21 and isinstance(tile,dict) and tile.get('animal') and not tile.get('fed_today') and nxt[:2]==['PICKUP','WHEAT']:
            q=max(0,int(nxt[2]) if len(nxt)>2 else 1)
            if not q:continue
            commands[actor]=['PICKUP','WHEAT',q+1]
            swaps[actor]=dict(step=step+1,xy=[x,y],animal=tile['animal'],birth=tile.get('placed_day'),quantity=q,pickup=copy.deepcopy(nxt))
            arrivals.append(dict(step=step+1,actor=actor,expected=q+1,quantity=q+1))
        elif c==['PASS']:
            q=_r128_food_need(obs,projected_farm,projected_private,actor)
            if q:
                commands[actor]=['PICKUP','WHEAT',q];prefetches+=1
                arrivals.append(dict(step=step+1,actor=actor,expected=held+q,quantity=q))
    if not arrivals:return result
    proposed['farmer']=commands[0];proposed['hands']=commands[1:]
    safe,after=_r128_field_safe(obs,result,proposed,swaps)
    if not safe or any(after['inventories'][p['actor']].get('WHEAT',0)<p['expected'] for p in arrivals):
        _R128_REPORT['service_capacity_declines']+=1;return result
    state['swaps']=swaps;state['arrivals']=arrivals
    _R128_REPORT['service_swaps_started']+=len(swaps);_R128_REPORT['service_idle_preloads']+=prefetches
    _R128_REPORT['service_requested_units']+=sum(p['quantity'] for p in arrivals)
    return proposed

def _r128_credit_supply(obs,action,state):
    step=int(obs['step'])
    if not 144<=step<695 or _r97_budget(obs,action.get('market') or []):return action
    credit=_r128_sale_credit(obs,action)
    if not credit:return action
    budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][obs['player']]['money']+=credit
    if not _r97_budget(budget,action.get('market') or []):return action
    result=_r97_supply(budget,action)
    if result==action:return action
    assert result['market'][0]==action['market'][0]
    _,private=_r127_fields(obs,result);stock,_,_=_r97_market_stock(private['shed'],result['market']);final,_=_r97_delivery(stock,private,step%24==23)
    quantity=lambda a:sum(max(0,int(o[2])) for o in a.get('market',[]) if len(o)>2 and o[:2]==['BUY_PRODUCT','WHEAT'])
    extra=max(0,quantity(result)-quantity(action));state['credit_pending']=(step+1,final.get('WHEAT',0),extra)
    _R128_REPORT['sale_credit_orders']+=1;_R128_REPORT['sale_credit_lower_bound']+=credit;_R128_REPORT['sale_credit_grain_units']+=extra
    return result

def agent(observation,configuration=None):
    result=_R128_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step']);state=_R128_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R128_STATES[player]={'step':-1}
            _R128_REPORT.update(service_requested_units=0,service_confirmed_units=0,service_idle_preloads=0,service_swaps_started=0,service_swaps_completed=0,service_capacity_declines=0,service_arrival_errors=0,service_swap_errors=0,sale_credit_orders=0,sale_credit_lower_bound=0,sale_credit_grain_units=0,sale_credit_confirmed_units=0,sale_credit_errors=0,service_errors=0)
        state['step']=step;pending=state.pop('credit_pending',None)
        if pending:
            if pending[0]!=step or observation['private']['shed'].get('WHEAT',0)<pending[1]:_R128_REPORT['sale_credit_errors']+=1
            else:_R128_REPORT['sale_credit_confirmed_units']+=pending[2]
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard:result=_r128_credit_supply(observation,_r128_service(observation,result,state),state)
    except Exception:_R128_REPORT['service_errors']=_R128_REPORT.get('service_errors',0)+1
    _R128_REPORT.update(getattr(_R128_PARENT,'telemetry',{}));_R128_REPORT.update(_R97_REPORT)
    return result
agent.telemetry=_R128_REPORT

agent = globals().pop('agent')   # keep 'agent' the last callable for Kaggle's loader
