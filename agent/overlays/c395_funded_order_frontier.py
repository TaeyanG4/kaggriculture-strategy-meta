# c395, Taeyang/Codex, 2026-09-23. Mixed funded queues only.
# Public unit-lockstep helpers from prvsiyan/The Soil Remembers Rain, Apache-2.0
# source 178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a.
# Related designs: ahmedberatozer V57 funding order invariant;
# tetsutani Demand-Preserving Turn Sale Timing (multiple rival queue hypotheses).
# Hypotheses are not knowledge of the rival's hidden stock or next action.
import itertools as _c395_it
_C395_ENABLED = True
_C395_PARENT = agent
_C395_REPORT = {}
_C395_TELEMETRY = {}
_C395_NS = dict(_r37_market_price=_C365_CA_NS['_r37_market_price'],
               _R37_MARKET_PARAMS=_C365_CA_NS['_R37_MARKET_PARAMS'])
exec(compile(__LAYER__, '<c395-public-unit-prices>', 'exec'), _C395_NS)

def _c395_scores(opp, inv, stock, params):
    schedules={}
    for i,o in enumerate(opp):
        if o and o[0]=='SELL':schedules.setdefault(o[1],[]).append((i,o[2]))
    cache={}
    def value(candidate):
        mine={}
        for i,o in enumerate(candidate):
            if o and o[0]=='SELL':mine.setdefault(o[1],[]).append((i,o[2]))
        own=margin=0.0
        for item in set(mine)|set(schedules):
            signature=tuple(mine.get(item,[]));key=(item,signature)
            if key not in cache:
                x=[[] for _ in candidate];y=[[] for _ in opp]
                for i,q in signature:x[i]=['SELL',item,q]
                for i,q in schedules.get(item,[]):y[i]=['SELL',item,q]
                aa,bb=_C395_NS['_v44y_lockstep'](x,y,{item:inv[item]},
                    {item:stock.get(item,0)},{item:stock.get(item,0)},{item:params[item]})
                cache[key]=(aa,aa-bb)
            aa,mm=cache[key];own+=aa;margin+=mm
        return own,margin
    return value

def _c395_reorder(obs,action):
    orders=action.get('market') or []
    if not 2<=len(orders)<=10:return action
    slots=[];sales=[];fixed=[];fixed_positions=[]
    for i,o in enumerate(orders):
        if not o:continue  # Empty absolute slots stay fixed.
        if o[0]=='SELL' and len(o)==3 and type(o[2]) is int and o[2]>0:
            sales.append(o);slots.append(i)
        elif (o==['HIRE'] or (len(o)==3 and o[0]=='BUY_SEED' and
                o[1] in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON') and type(o[2]) is int and o[2]>0)):
            fixed.append(o);fixed_positions.append(i);slots.append(i)
        else:return action
    if not sales or not fixed or len(sales)>4:return action
    if len({o[1] for o in sales})!=len(sales):return action
    _C395_REPORT['c395_offers']+=1
    # All spending must be funded before this turn's sales. Seed orders consume
    # no shed space; HIRE order/indices stay in the same order and same step.
    if not _C365_CA_NS['_r97_budget'](obs,orders):
        _C395_REPORT['c395_unfunded']+=1;return action
    stock=_C365_CA_NS['_ov_fields'](obs,action)[1]['shed']
    if any(stock.get(o[1],0)<o[2] for o in sales):
        _C395_REPORT['c395_stock_declined']+=1;return action
    models=[orders]
    for sequence in (sales+fixed,fixed+sales,list(reversed(sales))+fixed):
        model=list(orders)
        for i,o in zip(slots,sequence):model[i]=o
        if model not in models:models.append(model)
    params=_C395_NS['_v44y_params'](obs);inv=obs['market']['inventory']
    scores=[_c395_scores(model,inv,stock,params) for model in models]
    bases=[f(orders) for f in scores];best=(0.0,0.0);chosen=None;examined=0
    for positions in _c395_it.permutations(slots,len(sales)):
        remaining=[i for i in slots if i not in positions]
        if any(new<old for new,old in zip(remaining,fixed_positions)):continue
        candidate=list(orders)
        for i,o in zip(positions,sales):candidate[i]=o
        for i,o in zip(remaining,fixed):candidate[i]=o
        if candidate==orders:continue
        examined+=1
        if examined>800:break
        deltas=[tuple(v-b for v,b in zip(f(candidate),base)) for f,base in zip(scores,bases)]
        if any(own<0 or margin<0 for own,margin in deltas):continue
        quality=(min(mm for _,mm in deltas),sum(mm for _,mm in deltas))
        if quality>best:best=quality;chosen=candidate
    _C395_REPORT['c395_evaluations']+=min(examined,800)
    if chosen is None:return action
    _C395_REPORT['c395_turns']+=1
    _C395_REPORT['c395_min_modeled_margin']+=best[0]
    return dict(action,market=chosen)

def agent(observation,configuration=None):
    step=int(observation['step'])
    if step==0:
        _C395_REPORT.clear();_C395_REPORT.update(c395_offers=0,c395_unfunded=0,
            c395_stock_declined=0,c395_evaluations=0,c395_turns=0,c395_min_modeled_margin=0,c395_errors=0)
    action=_C395_PARENT(observation,configuration)
    standard=configuration is None or all(configuration.get(k,v)==v for k,v in
        [('episodeSteps',720),('turnsPerDay',24),('boardSize',10),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
    if _C395_ENABLED and standard and 216<=step<700:
        try:action=_c395_reorder(observation,action)
        except Exception:
            _C395_REPORT['c395_errors']+=1;raise
    _C395_TELEMETRY.clear();_C395_TELEMETRY.update(_C387_TELEMETRY);_C395_TELEMETRY.update(_C395_REPORT)
    return action
agent.telemetry=_C395_TELEMETRY
c395_submission_agent=agent
