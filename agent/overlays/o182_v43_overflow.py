# o182_v43_overflow (Claude/o-series, 2026-09-15). ahmedberatozer V43 "Recovering Lost Harvests" r148 block ported verbatim.
# Sells existing stock at hour 23 only when otherwise-destroyed dawn cargo would replace it (complete shed vector unchanged).
# Requires the r97/r127 helpers from the o174 port (stack after o174). Source: public notebook lines 3192-3329; upstream notices retained.


_R148_OVERFLOW=True
_R148_SEEDS=False
# Original targeted contracts, Ahmed Berat Ozer, EXP277.
# Uses only current observations and the agent's own existing raw plan.
_R148_PARENT=agent
_R148_REPORT={}
_R148_PENDING={}


def _r148_same_stock(a,b):
    return all(int(a.get(p,0))==int(b.get(p,0)) for p in set(a)|set(b))


def _r148_overflow(obs,action):
    """Sell only inventory replaced by otherwise destroyed dawn cargo.

    All original orders/field jobs remain in place. The COMPLETE warehouse
    vector after dawn must match the original funded action exactly.
    """
    if int(obs['step'])%24!=23:return action
    orders=action.get('market') or []
    if len(orders)>=10 or not _r97_budget(obs,orders):return action
    _,private=_r127_fields(obs,action)
    stock,_,_=_r97_market_stock(private['shed'],orders)
    original,loss=_r97_delivery(stock,private,True)
    if not loss:return action
    # The deposits are ordered. Recoverable cargo is the discarded suffix in
    # that same order, not an unordered product total or future forecast.
    remaining=max(0,100-sum(stock.values()));tail=[]
    for bag in private['inventories']:
        for item,n in bag.items():
            n=max(0,int(n));take=min(n,remaining);remaining-=take
            if n>take:tail.extend([item]*(n-take))
    released={};best=None
    for item in tail:
        released[item]=released.get(item,0)+1
        if item not in obs['market']['prices'] or released[item]>stock.get(item,0):break
        if len(orders)+len(released)>10:break
        proposed=list(orders)+[['SELL',p,n] for p,n in released.items()]
        after,_,_=_r97_market_stock(private['shed'],proposed)
        final,new_loss=_r97_delivery(after,private,True)
        if _r148_same_stock(original,final):best=(proposed,dict(released),final,new_loss)
    if best is None:return action
    proposed,released,final,new_loss=best
    _R148_REPORT['overflow_turns']+=1
    _R148_REPORT['overflow_units_reclaimed']+=sum(released.values())
    _R148_REPORT['overflow_quote_exposure']+=sum(n*obs['market']['prices'][p] for p,n in released.items())
    _R148_PENDING[int(obs['player'])]=(int(obs['step'])+1,dict(final))
    return dict(action,market=proposed)


def _r148_atomic(obs,action):
    """A shortage must not cancel every otherwise executable same-crop plant."""
    commands=[list(c) for c in [action.get('farmer') or ['PASS'],*(action.get('hands') or [])]]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={p for p,n in demand.items() if n>obs['private']['seeds'].get(p,0)}
    if not blocked:return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    kept=removed=0
    for actor,c in enumerate(commands):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:
            pos=None if actor>=len(private['inventories']) else farm['farmer'] if actor==0 else farm['hands'][actor-1]
            valid=pos is not None and farm['tiles'][pos[1]][pos[0]] is None and private['seeds'].get(c[1],0)>0
            if not valid:commands[actor]=['PASS'];removed+=1
            else:kept+=1
        if actor<len(private['inventories']):
            _PLANNER_NS['_apply_unit_action'](farm,private,actor,commands[actor],10,int(obs['step'])//24,24,100)
    if not removed:return action
    result=dict(action,farmer=commands[0],hands=commands[1:])
    # The inherited final-hour watering contract still governs any rescue.
    result=_r127_last_hour(obs,result)
    _R148_REPORT['atomic_turns']+=1;_R148_REPORT['atomic_kept_requests']+=kept;_R148_REPORT['atomic_removed_requests']+=removed
    return result


def _r148_seed_prefund(obs,action):
    """Fund next-turn valid own-plan planting from already available cash.

    No dawn/shop prediction, displaced purchases, new land or future opponent
    observation. Future geometry is obtained from exact current unit effects.
    """
    step=int(obs['step']);orders=action.get('market') or []
    if step<24 or step>=695 or step%24 in (22,23) or len(orders)>=10:return action
    future=_r128_future(obs)
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    if not any(c and c[0]=='PLANT' for c in commands):return action
    if not _r97_budget(obs,orders):return action
    farm,private=_r127_fields(obs,action)
    # Avoid predicting geometry changed by a land purchase in this callback.
    if any(o and o[0]=='BUY_LAND' for o in orders):return action
    access=((4,4),(5,4),(4,5),(5,5));positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    for order in orders:
        if order and order[0]=='HIRE':
            pos=min(access,key=lambda p:(positions.count(p),access.index(p)))
            positions.append(pos);farm['hands'].append(list(pos));private['inventories'].append({})
        elif len(order)>2 and order[0]=='BUY_SEED':
            private['seeds'][order[1]]=private['seeds'].get(order[1],0)+max(0,int(order[2]))
    available=dict(private['seeds']);intended={}
    # Simulate the known next own commands with virtual seeds, solely to count
    # physically valid births. The current atomic repair drops invalid requests.
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':intended[c[1]]=intended.get(c[1],0)+1
    for item,n in intended.items():private['seeds'][item]=available.get(item,0)+n
    before=dict(private['seeds'])
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,step//24,24,100)
    short={item:max(0,before[item]-private['seeds'].get(item,0)-available.get(item,0)) for item in intended}
    short={item:n for item,n in short.items() if n>0}
    if not short or len(orders)+len(short)>10:return action
    proposed=list(orders)+[['BUY_SEED',item,n] for item,n in sorted(short.items())]
    if not _r97_budget(obs,proposed):return action
    _R148_REPORT['seed_prefund_turns']+=1;_R148_REPORT['seed_prefund_units']+=sum(short.values())
    return dict(action,market=proposed)


def agent(observation,configuration=None):
    action=_R148_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step'])
        if step==0:
            _R148_PENDING.pop(player,None);_R148_REPORT.clear()
            _R148_REPORT.update(overflow_turns=0,overflow_units_reclaimed=0,overflow_quote_exposure=0,overflow_contract_checks=0,overflow_contract_errors=0,atomic_turns=0,atomic_kept_requests=0,atomic_removed_requests=0,seed_prefund_turns=0,seed_prefund_units=0,targeted_errors=0)
        pending=_R148_PENDING.pop(player,None)
        if pending:
            if step!=pending[0] or not _r148_same_stock(observation['private']['shed'],pending[1]):_R148_REPORT['overflow_contract_errors']+=1
            else:_R148_REPORT['overflow_contract_checks']+=1
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard:
            if _R148_SEEDS:action=_r148_seed_prefund(observation,_r148_atomic(observation,action))
            if _R148_OVERFLOW:action=_r148_overflow(observation,action)
    except Exception:_R148_REPORT['targeted_errors']=_R148_REPORT.get('targeted_errors',0)+1
    _R148_REPORT.update(getattr(_R148_PARENT,'telemetry',{}))
    return action
agent.telemetry=_R148_REPORT
agent=globals().pop('agent')
