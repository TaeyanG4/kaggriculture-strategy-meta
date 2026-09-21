# SPDX-License-Identifier: Apache-2.0
"""One carrot crop after exhausted c177 tomatoes, using stationary visits only.

No future replay, opponent identity, new movement, land or hiring. Existing
market execution retains carrot sales (c305/c306 collateral-sale lesson).
"""
import copy as _c320_copy

_C320_PARENT=agent
_C320_ON=True
_C320_STATE={}
_C320_REPORT={}
del agent

def _c320_command(tile,cmd,day,seeds):
    if not cmd or cmd[0] not in ('PASS','WATER','FERTILIZE','HARVEST','DIG'):
        return cmd
    if tile is None:
        return ['PLANT','CARROT'] if seeds>0 and day<=26 else cmd
    if not isinstance(tile,dict):return cmd
    if tile.get('kind')=='WEED':return ['DIG'] if day<=25 else cmd
    if tile.get('crop')=='TOMATO':
        if day-int(tile['planted_day'])>=11 and int(tile.get('yield_units',0))==0:
            return ['DIG'] if day<=25 else cmd
        return cmd
    if tile.get('crop')=='CARROT':
        age=day-int(tile['planted_day'])
        if age>=2 and tile.get('yield_units',0)>0:
            if cmd[0]=='HARVEST' or age>=4 or (age==3 and tile.get('watered_today')):
                return ['HARVEST']
            if age<=3 and not tile.get('watered_today'):return ['WATER']
        if cmd[0]=='HARVEST' and age<2:return ['WATER']
    return cmd

def agent(observation,configuration=None):
    action=_C320_PARENT(observation,configuration)
    if not _C320_ON:return action
    seat=int(observation['player']);step=int(observation['step']);day=step//24
    st=_C320_STATE.get(seat)
    if st is None or step<=st['last']:
        st=_C320_STATE[seat]=dict(last=-1,bought=False,pending=None,planted=set(),requested=0)
        _C320_REPORT.clear()
        _C320_REPORT.update(c320_errors=0,c320_buy_requested=0,c320_buy_confirmed=0,c320_seed_spend=0,c320_plant_requests=0,c320_harvest_requests=0,c320_harvest_units=0,c320_dig_requests=0)
    st['last']=step
    try:
        farm=observation['farms'][seat];private=observation['private']
        seed_count=int(private['seeds'].get('CARROT',0))
        if st['pending'] is not None:
            before,n=st['pending']
            if seed_count>=before+n:
                st['bought']=True
                _C320_REPORT['c320_buy_confirmed']+=n
                _C320_REPORT['c320_seed_spend']+=20*n
            st['pending']=None
        sites=(_C177_STATES.get(seat) or {}).get('sites',set())
        if not sites or day<22:return action
        result=_c320_copy.deepcopy(action)
        positions=[farm['farmer'],*farm.get('hands',[])]
        cmds=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
        market=result.get('market') or []
        # Fund the complete tail tranche once, on a sale-only market step.
        # No parent carrot seed planting occurs during the confirmation interval.
        if not st['bought'] and day<=23 and len(market)<10 and all(o and o[0]=='SELL' for o in market) and not any(c[:2]==['PLANT','CARROT'] for c in cmds):
            n=len(sites)
            if farm['money']>=3000+20*n:
                market.append(['BUY_SEED','CARROT',n]);st['pending']=(seed_count,n)
                _C320_REPORT['c320_buy_requested']+=n
        left=max(0,seed_count-sum(c[:2]==['PLANT','CARROT'] for c in cmds))
        claimed=set()
        for actor,(pos,cmd) in enumerate(zip(positions,cmds)):
            xy=tuple(pos)
            if xy not in sites or xy in claimed:continue
            tile=farm['tiles'][pos[1]][pos[0]]
            # Only our confirmed extra seed budget; never dig a later parent crop.
            if not st['bought']:continue
            if isinstance(tile,dict) and tile.get('crop') not in (None,'TOMATO','CARROT'):continue
            if isinstance(tile,dict) and tile.get('crop')=='CARROT' and xy not in st['planted']:continue
            if xy in st['planted'] and (not isinstance(tile,dict) or tile.get('crop')!='CARROT'):continue
            chosen=_c320_command(tile,cmd,day,left if xy not in st['planted'] else 0)
            if chosen[:2]==['PLANT','CARROT'] and chosen!=cmd:
                st['planted'].add(xy);left-=1;_C320_REPORT['c320_plant_requests']+=1
            if chosen==['HARVEST'] and isinstance(tile,dict) and tile.get('crop')=='CARROT':
                _C320_REPORT['c320_harvest_requests']+=1
                _C320_REPORT['c320_harvest_units']+=int(tile.get('yield_units',0))
            if chosen==['DIG'] and chosen!=cmd:_C320_REPORT['c320_dig_requests']+=1
            if chosen!=cmd:
                cmds[actor]=chosen;claimed.add(xy)
        result['farmer'],result['hands'],result['market']=cmds[0],cmds[1:],market
        return result
    except Exception:
        _C320_REPORT['c320_errors']+=1
        raise
    finally:
        _C320_REPORT.update(getattr(_C320_PARENT,'telemetry',{}))

agent.telemetry=_C320_REPORT
agent=globals().pop('agent')
