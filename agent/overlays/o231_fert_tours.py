# o231_fert_tours (Claude/o-series, 2026-09-16). Re-priced R51 fertilizer tours on the o227 stack.
# R51 (EXP182) hires a hand to fertilize wheat/carrot tiles in their yield window but priced every fertilizer unit at
# the market quote and demanded value >= 1.5*cost+50, so it never fired (0/128 games): live data show our late
# fertilizer is dumped at $7-15/unit while a fertilized watering adds +1 crop unit (~$38). Changes: own shed
# fertilizer beyond the native pickups is priced at _O231_OWN_VALUE (its late dump value) and only the shortfall is
# bought; ratio 1.5 -> 1.2 (+25). Everything else (targets, paths, hires, pickups, telemetry) is the original R51.
_O231_OWN_VALUE=12
_O231_RATIO=1.2
def _r51_input_control(obs,action,state):
    step=int(obs['step']);day=step//24;hour=step%24;player=int(obs['player']);farm=obs['farms'][player];private=obs['private']
    native=_IMPL.chassis.players[player]
    if state.get('day')!=day:state.update(day=day,workers={},pending=None,placed=[])
    for x,y in state['placed']:
        tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('fertilized_until_day',-1)>=day+2:_R51_INPUT_REPORT['input_confirmed_applications']+=1
        else:_R51_INPUT_REPORT['input_application_errors']+=1
    state['placed']=[]
    if state.get('pending'):
        pending=state.pop('pending')
        for actor,plan in pending.items():
            if len(farm['hands'])>=actor:state['workers'][actor]=plan;_R51_INPUT_REPORT['input_confirmed_hires']+=1
            else:_R51_INPUT_REPORT['input_hire_errors']+=1
    if state['workers']:
        changed=copy.deepcopy(action)
        for actor,plan in state['workers'].items():
            inv=private['inventories'][actor];pos=tuple(farm['hands'][actor-1]);cmd=['PASS']
            if not plan['loaded']:
                stock=projected_shed(changed,FarmView(obs));q=min(plan['quantity'],max(0,stock.get('FERTILIZER',0)))
                if q and _shed_adjacent(pos,10):
                    cmd=['PICKUP','FERTILIZER',q];plan['loaded']=True;_R51_INPUT_REPORT['input_loaded_units']+=q
                    if q<plan['quantity']:_R51_INPUT_REPORT['input_stock_shortfalls']+=plan['quantity']-q
            elif inv.get('FERTILIZER',0):
                while plan['path']:
                    x,y,crop,birth=plan['path'][0];tile=farm['tiles'][y][x]
                    if not isinstance(tile,dict) or tile.get('crop')!=crop or tile.get('planted_day')!=birth or tile.get('fertilized_until_day',-1)>=day+2:
                        plan['path'].pop(0);continue
                    cmd=_v219_walk(pos,(x,y)) or ['FERTILIZE']
                    if cmd==['FERTILIZE']:state['placed'].append((x,y));plan['path'].pop(0);_R51_INPUT_REPORT['input_application_requests']+=1
                    break
            changed['hands'][actor-1]=cmd
        return changed
    if hour not in (1,2,3) or not 12<=day<=28:return action
    planned=_v219_native_day(native,day);expected=max(len(a.get('hands',[])) for a in planned)
    if any(o and o[0]=='HIRE' for a in planned[hour:] for o in a.get('market',[])) or native['pending']:return action
    parents=[_V219_STATES.get(player,{}),_V233_STATES.get(player,{})]
    # A parent may retry after a full market queue; its headcount must remain native.
    if day in (12,18) or any(p.get('committed') and p.get('requested_day')!=day for p in parents):return action
    if any(p.get('pending') for p in parents) or any(o and o[0]=='HIRE' for o in action.get('market',[])):return action
    owned=set(range(1,expected+1))
    for p in parents:
        actors=set(p.get('workers',{}))
        if owned&actors:return action
        owned|=actors
    if owned!=set(range(1,len(farm['hands'])+1)):return action
    targets=_r51_input_forecast(obs,native['route'],expected);plans=[];total_q=0;total_cost=0;all_units={'WHEAT':0,'CARROT':0}
    stock=projected_shed(action,FarmView(obs));purchases=sum(max(0,int(o[2])) for o in action.get('market',[]) if len(o)>2 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    # Units act before market orders. Preserve the native next-turn pickup,
    # after the current parent's actual sales/purchases, before buying tour inputs.
    available=max(0,stock.get('FERTILIZER',0))
    for o in action.get('market',[]):
        if len(o)>=3 and o[:2]==['SELL','FERTILIZER']:available=max(0,available-max(0,int(o[2])))
        elif len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER']:available+=max(0,int(o[2]))
    next_native=planned[hour+1];native_pickups=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [next_native.get('farmer') or ['PASS'],*(next_native.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    topup=max(0,native_pickups-available)
    spare=max(0,available-native_pickups);total_own=0
    for i in range(_R51_INPUT_MAX_WORKERS):
        path,units=_r51_input_path(obs,targets);q=len(path)
        if q<3 or len(action.get('market',[]))+2+i>10 or sum(stock.values())+purchases+total_q+q+topup>95:break
        quote=_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-total_q-q-topup)
        own=min(q,max(0,spare-total_own));cost=(q-own+(topup if i==0 else 0))*(quote+2)+own*_O231_OWN_VALUE+_v219_fib(int(farm['hires_today'])+i)
        value=sum(n*max(1,_r37_market_price(item,obs['market']['inventory'][item]+all_units[item]+n)-2) for item,n in units.items())
        if value<_O231_RATIO*cost+25 or farm['money']<total_cost+cost+3000:break
        plans.append({'path':path,'quantity':q,'loaded':False});total_q+=q;total_cost+=cost;total_own+=own
        for item,n in units.items():all_units[item]+=n
        for x,y,_,_ in path:targets.pop((x,y),None)
    if not plans:return action
    state['pending']={len(farm['hands'])+1+i:plan for i,plan in enumerate(plans)}
    _R51_INPUT_REPORT['input_hire_requests']+=len(plans);_R51_INPUT_REPORT['input_purchase_requests']+=total_q+topup
    _R51_INPUT_REPORT['input_forecast_wheat']+=all_units['WHEAT'];_R51_INPUT_REPORT['input_forecast_carrot']+=all_units['CARROT']
    changed=copy.deepcopy(action);buy=max(0,total_q-total_own+topup)
    if buy:changed['market'] += [['BUY_PRODUCT','FERTILIZER',buy]]
    changed['market'] += [['HIRE'] for _ in plans];_R51_INPUT_REPORT['o231_own_units']=_R51_INPUT_REPORT.get('o231_own_units',0)+total_own;return changed


agent = globals().pop('agent')
