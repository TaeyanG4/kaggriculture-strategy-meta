# c396: public-policy state tracking and same-turn funded execution response.
# Taeyang/Codex, 2026-09-23. Embedded policies keep their original notices.
# Official deterministic transitions: kaggle-environments 1.32.7, Apache-2.0.
# Public hypotheses: our c379; prvsiyan Clone Race Horizon; Dmitrii Gluzdov
# More Wheat, Smarter Sales; prvsiyan The Soil Remembers Rain. Exact SHAs are
# pinned in state/c396/shadow-plan-v2.json. No API, source ID, episode seed,
# opponent private observation or future recorded action is used at runtime.
import copy as _c396_copy
import base64 as _c396_b64
import zlib as _c396_zlib
import itertools as _c396_it
from types import SimpleNamespace as _c396_box
_C396_ENABLED = True
_C396_PARENT = agent
_C396_SOURCES = __SOURCES__
_C396_ENGINE = {}
_C396_TRACK = {}
exec(_c396_zlib.decompress(_c396_b64.b85decode(__ENGINE__)),_C396_ENGINE)
exec(_c396_zlib.decompress(_c396_b64.b85decode(__TRACKER__)),_C396_TRACK)
_C396_MODELS = {}
_C396_REPORT = {}
_C396_TELEMETRY = {}

def _c396_fields(obs,opp_private,actions):
    farms=_c396_copy.deepcopy(obs['farms']);privates=[None,None];own=int(obs['player'])
    privates[own]=_c396_copy.deepcopy(obs['private']);privates[1-own]=_c396_copy.deepcopy(opp_private)
    for i in (0,1):
        units=[actions[i].get('farmer',['PASS'])]+list(actions[i].get('hands') or []);demand={}
        for a in units:
            if isinstance(a,list) and len(a)>=2 and a[0]=='PLANT':demand[a[1]]=demand.get(a[1],0)+1
        blocked={k for k,n in demand.items() if n>privates[i]['seeds'].get(k,0)}
        for actor,a in enumerate(units):
            if isinstance(a,list) and len(a)>=2 and a[0]=='PLANT' and a[1] in blocked:a=['PASS']
            _C396_ENGINE['_apply_unit_action'](farms[i],privates[i],actor,a,10,int(obs['step'])//24,24,100)
    return farms,privates

def _c396_market(farms,privates,market,orders,configuration,own):
    f=_c396_copy.deepcopy(farms);p=_c396_copy.deepcopy(privates);m=_c396_copy.deepcopy(market)
    state=[_c396_box(observation=_c396_box(farms=f,market=m,private=p[i]),action=dict(market=orders[i])) for i in (0,1)]
    _C396_ENGINE['_process_market'](state,_c396_box(configuration=configuration))
    cash=[x['money'] for x in f]
    own_farm=dict(f[own]);own_farm.pop('money')
    return cash[own],cash[own]-cash[1-own],p[own],own_farm

def _c396_response(obs,action,predicted,configuration):
    orders=action.get('market') or [];own=int(obs['player']);slots=[];sales=[];fixed=[];old_fixed=[]
    if not 2<=len(orders)<=10:return action
    for i,o in enumerate(orders):
        if not o:continue
        if o[0]=='SELL' and len(o)==3 and type(o[2]) is int and o[2]>0:
            slots.append(i);sales.append(o)
        elif o==['HIRE'] or (len(o)==3 and o[0]=='BUY_SEED' and type(o[2]) is int and o[2]>0):
            slots.append(i);fixed.append(o);old_fixed.append(i)
        # All other commands, including variable-price purchases, keep slots.
    if not sales or len(sales)>4 or len(slots)<2:return action
    if len({o[1] for o in sales})!=len(sales):return action
    contexts=[]
    for key,opponent_action in predicted.items():
        actions=[None,None];actions[own]=action;actions[1-own]=opponent_action
        f,p=_c396_fields(obs,_C396_MODELS[key]['private'],actions)
        queues=[None,None];queues[own]=orders;queues[1-own]=opponent_action.get('market') or []
        base=_c396_market(f,p,obs['market'],queues,configuration,own)
        contexts.append((f,p,queues,base))
    best=(0,0);chosen=None;scored=0
    for positions in _c396_it.permutations(slots,len(sales)):
        rest=[i for i in slots if i not in positions]
        if any(new<old for new,old in zip(rest,old_fixed)):continue
        candidate=list(orders)
        for i,o in zip(positions,sales):candidate[i]=o
        for i,o in zip(rest,fixed):candidate[i]=o
        if candidate==orders:continue
        scored+=1
        if scored>64:break
        deltas=[]
        for f,p,queues,base in contexts:
            qs=list(queues);qs[own]=candidate
            result=_c396_market(f,p,obs['market'],qs,configuration,own)
            # Preserve exact completed own purchases, seeds, cargo, hires and
            # field state. Improve own cash and margin for every surviving model.
            if result[2:]!=base[2:] or result[0]<base[0] or result[1]<base[1]:break
            deltas.append(result[1]-base[1])
        if len(deltas)!=len(contexts):continue
        quality=(min(deltas),sum(deltas))
        if quality>best:best=quality;chosen=candidate
    _C396_REPORT['c396_scored']+=min(scored,64)
    if chosen is None:return action
    _C396_REPORT['c396_turns']+=1;_C396_REPORT['c396_predicted_margin']+=best[0]
    return dict(action,market=chosen)

def agent(observation,configuration=None):
    action=_C396_PARENT(observation,configuration);step=int(observation['step']);own=int(observation['player'])
    if step==0:
        _C396_MODELS.clear();_C396_REPORT.clear()
        _C396_REPORT.update(c396_alive=0,c396_rejected=0,c396_verified=0,c396_turns=0,c396_scored=0,c396_predicted_margin=0,c396_errors=0)
    cfg=dict(configuration or {})
    standard=all(cfg.get(k,v)==v for k,v in [('episodeSteps',720),('turnsPerDay',24),('boardSize',10),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
    if _C396_ENABLED and standard:
        try:
            # No hidden seed is provided even if a nonstandard caller supplies it.
            cfg.pop('seed',None)
            if step==0:
                for key,packed in _C396_SOURCES.items():
                    scope={};exec(_c396_zlib.decompress(_c396_b64.b85decode(packed)),scope)
                    policy=[v for v in scope.values() if callable(v)][-1]
                    _C396_MODELS[key]=dict(policy=policy,private=_C396_ENGINE['_new_private'](),prediction=None)
            predicted={}
            for key,m in list(_C396_MODELS.items()):
                if m['prediction'] is not None:
                    if not _C396_TRACK['matches'](m['prediction'],observation):
                        del _C396_MODELS[key];_C396_REPORT['c396_rejected']+=1;continue
                    _C396_REPORT['c396_verified']+=1
                fake=_c396_copy.deepcopy(observation);fake['player']=1-own;fake['private']=_c396_copy.deepcopy(m['private'])
                predicted[key]=m['policy'](fake,cfg)
            if step>=216 and predicted:action=_c396_response(observation,action,predicted,cfg)
            for key,a in predicted.items():
                m=_C396_MODELS[key];actions=[None,None];actions[own]=action;actions[1-own]=a
                result=_C396_TRACK['projected'](_C396_ENGINE,observation,m['private'],actions,cfg)
                m['private']=result['privates'][1-own];m['prediction']=result
            _C396_REPORT['c396_alive']=len(_C396_MODELS)
        except Exception:
            _C396_REPORT['c396_errors']+=1;raise
    _C396_TELEMETRY.clear();_C396_TELEMETRY.update(_C387_TELEMETRY);_C396_TELEMETRY.update(_C396_REPORT)
    return action
agent.telemetry=_C396_TELEMETRY
c396_submission_agent=agent
