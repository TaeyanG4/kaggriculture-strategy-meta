# One early wheat replant becomes a strawberry lane. Keep the parent opening,
# routes and normal crop work; harvest ready yield on its final production day.
_C331_PARENT = agent
_C331_ON = True
_C331_STATE = {}
_C331_REPORT = dict(seed_orders=0, seed_confirmed=0, plant_orders=0,
                   plant_confirmed=0, terminal_harvests=0, cleanup_orders=0)
del agent

def agent(observation, configuration=None):
    step=int(observation['step']);seat=int(observation['player'])
    if step==0:
        _C331_STATE[seat]={}
        for key in _C331_REPORT:_C331_REPORT[key]=0
    action=_C331_PARENT(observation,configuration)
    if not _C331_ON:return action
    st=_C331_STATE.setdefault(seat,{})
    farm=observation['farms'][seat];private=observation['private']
    tile=farm['tiles'][1][0]
    if step==60:
        # The parent buys the seed one step before its earliest NW replant.
        orders=[list(o) for o in action.get('market') or []]
        index=next((i for i,o in enumerate(orders[:10]) if len(o)>=3 and o[:2]==['BUY_SEED','WHEAT'] and int(o[2])==1),None)
        if index is not None and farm['money']>=100 and isinstance(tile,dict) and tile.get('crop')=='WHEAT':
            st['prior_seed']=int(private['seeds'].get('STRAWBERRY',0));st['seed_attempt']=True
            orders[index]=['BUY_SEED','STRAWBERRY',1];action=dict(action);action['market']=orders
            _C331_REPORT['seed_orders']+=1
    if step==61 and st.get('seed_attempt'):
        if int(private['seeds'].get('STRAWBERRY',0))>st['prior_seed']:
            st['seed_confirmed']=True;_C331_REPORT['seed_confirmed']+=1
        positions=[farm['farmer']]+list(farm['hands'])
        cs=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands') or []]
        for actor,pos in enumerate(positions):
            if list(pos)==[0,1] and actor<len(cs) and cs[actor]==['PLANT','WHEAT'] and tile is None and st.get('seed_confirmed'):
                cs[actor]=['PLANT','STRAWBERRY'];st['plant_attempt']=True;_C331_REPORT['plant_orders']+=1
                action=dict(action);action['farmer']=cs[0];action['hands']=cs[1:];break
    if step==62 and st.get('plant_attempt') and isinstance(tile,dict) and tile.get('crop')=='STRAWBERRY' and tile.get('planted_day')==2:
        st['active']=True;_C331_REPORT['plant_confirmed']+=1
    if st.get('active'):
        positions=[farm['farmer']]+list(farm['hands'])
        cs=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands') or []]
        for actor,pos in enumerate(positions):
            if list(pos)!=[0,1] or actor>=len(cs) or cs[actor][0] not in ('PASS','PLANT','WATER','FERTILIZE','HARVEST','DIG'):continue
            if isinstance(tile,dict) and tile.get('crop')=='STRAWBERRY':
                expiry=int(tile.get('max_lifespan_step',-1))
                if expiry>0 and step//24>=(expiry-1)//24 and tile.get('yield_units',0)>0 and cs[actor]!=['HARVEST']:
                    cs[actor]=['HARVEST'];_C331_REPORT['terminal_harvests']+=1
                else:continue
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':
                cs[actor]=['DIG'];_C331_REPORT['cleanup_orders']+=1;st['active']=False
            else:
                st['active']=False;continue
            action=dict(action);action['farmer']=cs[0];action['hands']=cs[1:];break
    return action

agent.telemetry=_C331_REPORT
agent=globals().pop('agent')
