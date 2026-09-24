"""Remove only CARROT2's coarse yield veto; buy uncovered seeds one turn ahead."""
import argparse, ast, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='28a520730a4f0037c0e9f433e28417db1ba0c95999a55b1751a396b28da08ad2'

HELPER=r'''
_C399_CARROT_REPORT = {}

def _c399_seed_need(obs, action, units, market, st):
    step=int(obs['step']);seat=int(obs['player']);future_step=step+1
    if future_step>=718 or not _CA_FROM <= future_step//24 <= _CA_TO:
        return 0
    # A seed purchased now cannot be planted until the next field phase.
    # Inspect only our own next scheduled wheat plant, without opponent futures.
    farm=obs['farms'][seat];board=len(farm['tiles']);tiles=farm['tiles']
    current_positions=[list(farm['farmer'])]+[list(h) for h in farm['hands']]
    positions=[p[:] for p in current_positions]
    occupied=set()
    for i,pos in enumerate(positions):
        cmd=units[i] if i<len(units) else ['PASS']
        if cmd[0] in _CA_MOVES:
            dx,dy=_CA_MOVES[cmd[0]];nx,ny=pos[0]+dx,pos[1]+dy
            if 0<=nx<board and 0<=ny<board:positions[i]=[nx,ny]
        elif cmd[0] in ('PLANT','BUILD_COOP','BUILD_PASTURE'):
            occupied.add(tuple(pos))
    for _ in range(sum(1 for o in market if o and o[0]=='HIRE')):
        positions.append(_ca_spawn(positions,board))
    if step%24==23:positions=[[board//2-1,board//2-1]]
    future=_ca_tape(seat,future_step)
    cmds=[future.get('farmer') or ['PASS']]+list(future.get('hands') or [])
    if _ca_wheat_total(obs)<_ca_feed_need(seat,future_step,_CA_FEED_DAYS):return 0
    pc=int(obs['market']['prices']['CARROT']);pw=int(obs['market']['prices']['WHEAT'])
    seen=set();required=0
    for i,cmd in enumerate(cmds):
        if cmd[:2]!=['PLANT','WHEAT'] or i>=len(positions):continue
        pos=tuple(positions[i])
        if pos in seen or pos in occupied or tiles[pos[1]][pos[0]] is not None:continue
        seen.add(pos)
        visits=_ca_visits(obs,action,pos,(future_step//24+6)*24,start=future_step+1)
        wu,_,_=_ca_yield_path('WHEAT',future_step//24,visits)
        ch,cr,_=_ca_yield_path('CARROT',future_step//24,visits)
        cu=max(ch,cr if _CA_RESCUE else 0)
        if cu*(pc-_CA_DROP)-20>wu*pw-10+_CA_MARGIN:required+=1
    if not required:return 0
    # Reserve native/current carrot planting before allocating the spare seeds.
    planted=sum(c[:2]==['PLANT','CARROT'] for c in units)
    native_next=sum(c[:2]==['PLANT','CARROT'] for c in cmds)
    have=max(0,int(obs['private']['seeds'].get('CARROT',0))-planted-native_next)
    buying=sum(int(o[2]) for o in market if len(o)>=3 and o[:2]==['BUY_SEED','CARROT'])
    available=max(0,min(st['spare_carrot'],have+buying))
    return max(0,required-available)
'''

EXTRA=r'''
        elif _CA_FROM <= day <= _CA_TO - 1 and not coarse_pays_now and len(market) < 10:
            q = _c399_seed_need(observation, action, units, market, st)
            order = ['BUY_SEED', 'CARROT', q]
            if q > 0 and int(farm.get('money', 0)) >= _CA_CASH + 20*q and _r97_budget(observation, market+[order]):
                market.append(order)
                st['spare_carrot'] += q
                _CA_REPORT['ca_seed_bought'] += q
                _C399_CARROT_REPORT['c399_jit_seeds'] = _C399_CARROT_REPORT.get('c399_jit_seeds', 0) + q
                changed = True
'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');args=ap.parse_args()
    body=(ROOT/'agent/c397_shadow_coverage.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    # Reuse the already decoded exact parent layer; no live notebook execution.
    decoded=(ROOT/'state/c398/embedded-11.py').read_text('utf8');tree=ast.parse(decoded)
    marker=next(n.lineno for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_CA_PARENT' for t in n.targets))
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='agent' and n.lineno>marker)
    layer=ast.get_source_segment(decoded,node)
    line='        pays_now = 3 * (p_c - _CA_DROP) - 20 > 4 * p_w - 10 + _CA_MARGIN'
    assert layer.count(line)==1
    layer=layer.replace('def agent(', 'def _c399_carrot_layer(',1)
    layer=layer.replace(line,line.replace('pays_now =','coarse_pays_now =')+'\n        pays_now = True')
    seed_gate='if _CA_FROM <= day <= _CA_TO - 1 and pays_now and len(market) < 10:'
    assert layer.count(seed_gate)==1;layer=layer.replace(seed_gate,seed_gate.replace('and pays_now','and coarse_pays_now'))
    layer=layer.replace('        # 4. sell credited carrots',EXTRA+'\n        # 4. sell credited carrots')
    payload=HELPER+'\n'+layer
    suffix='\n\n# c399: route-specific carrot value, parent thresholds and feed reserve preserved.\n_C399_ENABLED = '+str(not args.disabled)+'\n'
    suffix+=f'_C399_LAYER_SOURCE = {payload!r}\n'
    suffix+='''
_C399_PARENT = agent
_C399_TELEMETRY = {}
if _C399_ENABLED:
    _c399_targets = {id(v): v for v in _C365_CA_NS.values() if callable(v)
        and hasattr(v, '__code__') and '_CA_PARENT' in v.__code__.co_names
        and '_ca_yield_path' in v.__code__.co_names}
    if len(_c399_targets) != 1:
        raise RuntimeError('c399 exact CARROT2 layer not uniquely located')
    exec(compile(_C399_LAYER_SOURCE, '<c399-carrot-layer>', 'exec'), _C365_CA_NS)
    next(iter(_c399_targets.values())).__code__ = _C365_CA_NS['_c399_carrot_layer'].__code__

def agent(observation, configuration=None):
    if _C399_ENABLED and int(observation['step']) == 0:
        _C365_CA_NS['_C399_CARROT_REPORT'].clear()
    result = _C399_PARENT(observation, configuration)
    _C399_TELEMETRY.clear(); _C399_TELEMETRY.update(_C396_TELEMETRY)
    _C399_TELEMETRY.update({'c399_'+k:v for k,v in _C365_CA_NS['_CA_REPORT'].items()})
    if _C399_ENABLED:
        _C399_TELEMETRY.update(_C365_CA_NS['_C399_CARROT_REPORT'])
    return result

agent.telemetry = _C399_TELEMETRY
c399_submission_agent = agent
'''
    result=body.rstrip()+suffix.encode();compile(result,str(args.out),'exec');assert not args.out.exists()
    args.out.parent.mkdir(exist_ok=True,parents=True);args.out.write_bytes(result)
    print(args.out,hashlib.sha256(result).hexdigest())

if __name__=='__main__':main()
