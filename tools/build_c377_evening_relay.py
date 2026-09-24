"""Use covered-fertilizer slack to preserve a watering while returning egg cargo."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
WRAPPER = r'''

# c377: bounded day-25 evening relay, using only our observed state and tape.
# The goose keeper has PASS/FEED/CARE/COLLECT/NORTH/WATER at hours18..23.
# Move FEED+CARE one hour earlier, omit optional manure collection, return
# cargo to the shed. Another existing worker waters the original crop using
# only movement/PASS/already-covered fertilizer slack. No hire or land change.
# Closest prior: o306 found overflow in carried cargo (shed-sale was no-op);
# c330 courier only handles workers with no remaining useful obligations.
_C377_ENABLED = __ON__
_C377_PARENT = agent
_C377_REPORT = {}
_C377_PLANS = {}
_C377_MOVES = {'NORTH':(0,-1), 'SOUTH':(0,1), 'WEST':(-1,0), 'EAST':(1,0)}

def _c377_commands(frame):
    return [frame.get('farmer') or ['PASS'], *(frame.get('hands') or [])]

def _c377_move(pos, cmd):
    dx,dy = _C377_MOVES.get(cmd[0], (0,0))
    return (max(0,min(9,pos[0]+dx)), max(0,min(9,pos[1]+dy)))

def _c377_path(pos, target):
    out=[]
    for axis,positive,negative in ((0,'EAST','WEST'),(1,'SOUTH','NORTH')):
        out += [[positive if target[axis]>pos[axis] else negative]] * abs(target[axis]-pos[axis])
    return out

def _c377_plan(obs, action):
    seat=int(obs['player']);step=int(obs['step']);farm=obs['farms'][seat]
    native=_C358_IMPL.chassis.players[seat]
    if native['pending']:
        return None
    route=_C358_IMPL.chassis.routes[native['route']]
    frames=route[step:step+6]
    if len(frames)!=6 or any(o and o[0]=='HIRE' for f in frames for o in f.get('market',[])):
        return None
    # Dynamic workers have separate obligations; never borrow their slots.
    reserved=set()
    for name in ('_R51_INPUT_STATES','_V219_STATES','_V233_STATES'):
        reserved.update(_C365_CA_NS[name].get(seat,{}).get('workers',{}))
    positions=[farm['farmer'],*farm['hands']];bags=obs['private']['inventories']
    now=_c377_commands(action);future=[_c377_commands(f) for f in frames]
    if any(len(f)<len(positions) for f in future):
        return None
    # Only consider a visibly crowded evening; this is a support gate, not a
    # claim of perfect forecasting. Exact overflow sales are computed at h23.
    if sum(sum(b.values()) for b in bags)<75:
        return None
    pattern=[['PASS'],['FEED'],['CARE'],['COLLECT_FERTILIZER'],['NORTH'],['WATER']]
    for actor in range(1,len(positions)):
        if actor in reserved or [f[actor] for f in future]!=pattern or now[actor]!=['PASS']:
            continue
        pos=tuple(positions[actor]);animal=farm['tiles'][pos[1]][pos[0]]
        if not isinstance(animal,dict) or animal.get('animal')!='GOOSE' or animal.get('fed_today'):
            continue
        if bags[actor].get('WHEAT',0)<1 or bags[actor].get('EGG',0)<1:
            continue
        target=(pos[0],pos[1]-1)
        if target[1]<0:
            continue
        crop=farm['tiles'][target[1]][target[0]]
        if not isinstance(crop,dict) or crop.get('kind')!='PLANT' or crop.get('watered_today'):
            continue
        access=min(((4,4),(5,4),(4,5),(5,5)),key=lambda p:abs(p[0]-pos[0])+abs(p[1]-pos[1]))
        trip=_c377_path(pos,access)
        if len(trip)!=3:
            continue
        for helper in range(1,len(positions)):
            if helper==actor or helper in reserved:
                continue
            hp=tuple(positions[helper])
            for f in future[:3]:
                hp=_c377_move(hp,f[helper])
            start=hp;safe=True
            for f in future[3:]:
                cmd=f[helper];tile=farm['tiles'][hp[1]][hp[0]]
                if cmd[0] not in _C377_MOVES and cmd!=['PASS']:
                    if cmd!=['FERTILIZE'] or not isinstance(tile,dict) or int(tile.get('fertilized_until_day',-1))<27:
                        safe=False;break
                hp=_c377_move(hp,cmd)
            path=_c377_path(start,target)
            if not safe or len(path)>2:
                continue
            _C377_REPORT['relay_plans']+=1
            return dict(day=25,actor=actor,helper=helper,target=target,helper_start=start,
                        actor_commands=[['FEED'],['CARE'],*trip,['DROP']],
                        helper_commands=path+[['WATER']]+[['PASS']]*(2-len(path)))
    return None

def agent(observation, configuration=None):
    step=int(observation['step']);seat=int(observation['player']);hour=step%24
    if step==0:
        _C377_PLANS.clear();_C377_REPORT.clear()
        _C377_REPORT.update(relay_plans=0,relay_steps=0,relay_water=0,relay_deposits=0,overflow_sold=0)
    action=_C377_PARENT(observation,configuration)
    _C377_REPORT.update(_O302_REPORT)
    if not _C377_ENABLED or step//24!=25 or hour<18:
        return action
    if hour==18:
        plan=_c377_plan(observation,action)
        if plan:_C377_PLANS[seat]=plan
    plan=_C377_PLANS.get(seat)
    if not plan:
        return action
    units=_c377_commands(action)
    units[plan['actor']]=list(plan['actor_commands'][hour-18])
    if hour>=21:
        units[plan['helper']]=list(plan['helper_commands'][hour-21])
        if units[plan['helper']]==['WATER']:_C377_REPORT['relay_water']+=1
    action=dict(action,farmer=units[0],hands=units[1:]);_C377_REPORT['relay_steps']+=1
    if hour==23:
        _,private=_C365_CA_NS['_ov_fields'](observation,action)
        market=[list(o) for o in action.get('market',[])]
        if all(not o or o[0]=='SELL' for o in market):
            stock,_,_=_C365_CA_NS['_r97_market_stock'](private['shed'],market)
            overflow=max(0,sum(stock.values())+sum(sum(b.values()) for b in private['inventories'])-100)
            q=min(overflow,max(0,int(stock.get('EGG',0))))
            sell=next((o for o in market if len(o)>=3 and o[:2]==['SELL','EGG']),None)
            if q and (sell is not None or len(market)<10):
                if sell is None:market.append(['SELL','EGG',q])
                else:sell[2]+=q
                action=dict(action,market=market);_C377_REPORT['overflow_sold']+=q
        _C377_REPORT['relay_deposits']+=1
    return action

agent.telemetry=_C377_REPORT
kaggle_submission_agent=agent
c377_submission_agent=agent
'''

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--disabled',action='store_true')
    args=ap.parse_args()
    parent=(ROOT/'agent/o302_farmer_feed_topup.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()==PARENT_SHA
    data=parent.rstrip()+WRAPPER.replace('__ON__',str(not args.disabled)).encode()
    compile(data,str(args.out),'exec')
    if args.out.exists():raise FileExistsError(args.out)
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
