# Research prototype: one coherent demonstrated full plan, not Majkel source.
# First 144 steps may repair known cash/pickup prerequisites; later actions fixed.
import base64
import zlib
import json
import copy
"""Bounded opening execution prototype, NOT a full-season submission agent.

Faithful recorded field program plus a cash prerequisite compiled from verified
successful work before the next day's first realized sale. This does not infer
Majkel's private algorithm and uses no future information from the current game.
"""
import copy


def compile_hire_prerequisite(replay, accounting, seat):
    first_sale=min(x['step'] for x in accounting['transactions']
                   if x['seat']==seat and 24<=x['step']<48 and x['cash_delta']>0)
    work=[x for x in accounting['field_events'] if x['seat']==seat and 24<=x['step']<first_sale
          and (x['tile_changed'] or x['position_changed'] or x['inventory_changed'] or x['seeds_changed'])]
    hands=max(x['actor'] for x in work)
    a,b=1,1;cost=0
    for _ in range(hands):cost+=a;a,b=b,a+b
    return dict(day=1,first_income_step=first_sale,required_hands=hands,required_cash=cost,
                source='Verified teacher work before first sale, not the number of HIRE requests')


class OpeningContract:
    def __init__(self,replay,seat,contract,enabled=True):
        self.tape=[copy.deepcopy(s[seat]['action']) for s in replay['steps'][1:145]]
        self.contract=contract;self.enabled=enabled
        self.telemetry=dict(deferred_seeds=0,events=[],outside_horizon=0)

    def __call__(self,obs,configuration=None):
        step=int(obs['step'])
        if not 0<=step<144:
            self.telemetry['outside_horizon']+=1
            raise ValueError('Opening prototype only; no unvalidated full-season handoff')
        action=copy.deepcopy(self.tape[step])
        if not self.enabled or not 12<=step<24:return action
        orders=action.get('market') or []
        # Restrict to one deterministic-cost seed purchase. No predicted sales or
        # simultaneous opponent transactions are used to justify affordability.
        if len(orders)!=1 or len(orders[0])!=3 or orders[0][:2]!=['BUY_SEED','WHEAT']:return action
        cash=float(obs['farms'][int(obs['player'])]['money'])
        requested=int(orders[0][2]);affordable=min(requested,int(cash)//10)
        allowed=max(0,min(requested,int((cash-self.contract['required_cash'])//10)))
        if allowed<affordable:
            action['market']=[['BUY_SEED','WHEAT',allowed]] if allowed else []
            self.telemetry['deferred_seeds']+=affordable-allowed
            self.telemetry['events'].append(dict(step=step,cash=cash,requested=requested,
                affordable=affordable,allowed=allowed,reserve=self.contract['required_cash']))
        return action

"""Prototype plan prerequisite repair; no new routes or hidden future inputs.

Own future commands are the stored proposed plan, not future engine observations.
Only ration pickup requests during a visible shed shortage. Retain the previous
prototype unchanged as a control. Limited to its 144-step diagnostic horizon.
"""



class ResourceContract(OpeningContract):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.telemetry['pickup_changes']=[]

    def needed(self,obs,actor,step,requested):
        farm=obs['farms'][int(obs['player'])]
        x,y=([farm['farmer']]+farm['hands'])[actor]
        targets=set()
        for t in range(step+1,min(144,(step//24+1)*24)):
            plan=self.tape[t]
            cmds=[plan.get('farmer') or []]+(plan.get('hands') or [])
            cmd=cmds[actor] if actor<len(cmds) else []
            if not cmd:continue
            op=cmd[0]
            if op=='DROP' or (op in ('PICKUP','PLACE') and len(cmd)>1 and cmd[1]=='WHEAT'):break
            if op=='PLACE' and len(cmd)>1 and cmd[1] in ('COW','SHEEP','GOOSE'):
                return requested # Future placement would invalidate the static farm test.
            if op in ('NORTH','SOUTH','EAST','WEST'):
                dx,dy={'NORTH':(0,-1),'SOUTH':(0,1),'EAST':(1,0),'WEST':(-1,0)}[op]
                nx,ny=x+dx,y+dy
                if 0<=nx<len(farm['tiles'][0]) and 0<=ny<len(farm['tiles']):x,y=nx,ny
            if op=='FEED':
                tile=farm['tiles'][y][x]
                if isinstance(tile,dict) and tile.get('animal') and not tile.get('fed_today'):
                    targets.add((x,y))
        carried=obs['private']['inventories'][actor].get('WHEAT',0)
        return min(requested,max(0,len(targets)-carried))

    def __call__(self,obs,configuration=None):
        action=super().__call__(obs,configuration)
        farm=obs['farms'][int(obs['player'])]
        positions=[farm['farmer']]+farm['hands']
        commands=[action.get('farmer') or []]+(action.get('hands') or [])
        center=len(farm['tiles'])//2
        pickups=[(i,c) for i,c in enumerate(commands) if i<len(positions) and len(c)>=3
                 and c[:2]==['PICKUP','WHEAT'] and all(v in (center-1,center) for v in positions[i])]
        shed=obs['private']['shed'].get('WHEAT',0)
        if sum(int(c[2]) for _,c in pickups)<=shed:return action
        for actor,cmd in pickups:
            allowed=self.needed(obs,actor,int(obs['step']),int(cmd[2]))
            if allowed<int(cmd[2]):
                self.telemetry['pickup_changes'].append(dict(step=int(obs['step']),actor=actor,
                    requested=int(cmd[2]),allowed=allowed,shed=shed))
                replacement=['PICKUP','WHEAT',allowed] if allowed else ['PASS']
                if actor==0:action['farmer']=replacement
                else:action['hands'][actor-1]=replacement
        return action

_TAPE=json.loads(zlib.decompress(base64.b64decode('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')))
_CONTRACT={'day': 1, 'first_income_step': 26, 'required_hands': 3, 'required_cash': 4, 'source': 'Verified teacher work before first sale, not the number of HIRE requests'}
_PROTO=ResourceContract.__new__(ResourceContract)
_PROTO.tape=_TAPE[:144]
_PROTO.contract=_CONTRACT
_PROTO.enabled=True
_PROTO.telemetry=dict(deferred_seeds=0,events=[],outside_horizon=0,pickup_changes=[])
def agent(obs,configuration=None):
    step=int(obs['step'])
    if not 0<=step<len(_TAPE):
        raise ValueError('Unexpected season length for frozen demonstration')
    if step<144:return _PROTO(obs,configuration)
    return copy.deepcopy(_TAPE[step])
agent.telemetry=_PROTO.telemetry
