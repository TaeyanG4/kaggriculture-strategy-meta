"""Reusable paired statistics. No engine imports or simulation side effects."""
from collections import Counter, defaultdict
import math
import random
import statistics as st

def outcomes(rows):
    counts = Counter(r['outcome'] for r in rows)
    margins = sorted(r['margin'] for r in rows)
    return dict(games=len(rows), wins=counts['win'], losses=counts['loss'], ties=counts['tie'],
                point_rate=(counts['win'] + .5*counts['tie'])/len(rows),
                mean_margin=st.mean(margins), worst_margin=margins[0],
                bottom_10pct_mean=st.mean(margins[:max(1, math.ceil(len(rows)*.1))]))

def paired_summary(details):
    return dict(conditions=len(details), mean_point_delta=st.mean(d['point_delta'] for d in details),
                mean_margin_delta=st.mean(d['margin_delta'] for d in details),
                mean_own_cash_delta=st.mean(d['own_cash_delta'] for d in details),
                win_to_loss=sum(d['win_to_loss'] for d in details),
                tie_to_loss=sum(d['tie_to_loss'] for d in details),
                changed_conditions=sum(d['changed'] for d in details))

def interval(values, alpha, draws=10000):
    # Constant observations do not justify a zero-width population interval.
    if len(values)<2 or len(set(values))<2:
        return None
    rng=random.Random(20260915)
    samples=sorted(st.mean(rng.choices(values,k=len(values))) for _ in range(draws))
    return [samples[max(0,int(draws*alpha/2)-1)],samples[min(draws-1,int(draws*(1-alpha/2))-1)]]

def analyze(plan, stage, rows):
    seeds=plan['stages'][stage]['seeds']
    expected={(c,s,o,t) for c in plan['models'] for s in seeds for o in plan['opponents'] for t in (0,1)}
    indexed={}
    for r in rows:
        key=(r['model'],r['seed'],r['opponent_name'],r['candidate_seat'])
        if key in indexed: raise ValueError('Duplicate condition')
        if not r['valid']: raise ValueError('Invalid row')
        indexed[key]=r
    if set(indexed)!=expected: raise ValueError('Incomplete or unexpected paired coverage')
    models={}
    for name in plan['models']:
        subset=[r for r in rows if r['model']==name]
        groups={}
        for field in ('opponent_name','opponent_family','candidate_seat'):
            groups[field]={str(v):outcomes([r for r in subset if r[field]==v]) for v in sorted({r[field] for r in subset})}
        telemetry=Counter()
        for r in subset:
            telemetry.update({k:v for k,v in r.get('candidate_telemetry',{}).items()
                              if isinstance(v,(int,float)) and math.isfinite(v)})
        models[name]=dict(outcomes(subset), subgroups=groups, telemetry=dict(telemetry))
    primary_count=sum(c['primary'] for c in plan['comparisons'])
    alpha=plan['stages'][stage]['alpha']/primary_count
    comparisons={}
    point={'win':1,'tie':.5,'loss':0}
    for comp in plan['comparisons']:
        candidate,parent=comp['candidate'],comp['parent']
        details=[]
        for seed in seeds:
            for opponent in plan['opponents']:
                for seat in (0,1):
                    a,b=[indexed[c,seed,opponent,seat] for c in (parent,candidate)]
                    details.append(dict(seed=seed,opponent=opponent,family=b['opponent_family'],seat=seat,
                        point_delta=point[b['outcome']]-point[a['outcome']],margin_delta=b['margin']-a['margin'],
                        own_cash_delta=b['rewards'][seat]-a['rewards'][seat],
                        win_to_loss=a['outcome']=='win' and b['outcome']=='loss',
                        tie_to_loss=a['outcome']=='tie' and b['outcome']=='loss',
                        changed=a['action_hashes'][seat]!=b['action_hashes'][seat]))
        # Equal family weight prevents related aliases from dominating the target metric.
        clusters=[]
        for seed in seeds:
            families=defaultdict(list)
            for d in details:
                if d['seed']==seed: families[d['family']].append(d['point_delta'])
            clusters.append(st.mean(st.mean(v) for v in families.values()))
        ci=interval(clusters,alpha) if comp['primary'] else None
        signal='positive' if ci and ci[0]>0 else 'negative' if ci and ci[1]<0 else 'inconclusive'
        subgroups={field:{str(v):paired_summary([d for d in details if d[field]==v])
                         for v in sorted({d[field] for d in details})} for field in ('opponent','family','seat')}
        comparisons[candidate+'_vs_'+parent]=dict(paired_summary(details),primary=comp['primary'],
            family_weighted_point_delta=st.mean(clusters),seed_clusters=len(clusters),
            adjusted_confidence=1-alpha if comp['primary'] else None, approximate_bootstrap_ci=ci,
            signal=signal if comp['primary'] else 'descriptive_only',subgroups=subgroups,conditions=details)
    return dict(status='complete',completed_jobs=len(rows),stage=stage,by_candidate=models,comparisons=comparisons,
                promotion=False, evidence_boundary='Fixed-sample reacting panel; approximate seed-cluster intervals, not live ladder proof. Secondary/subgroup results are descriptive. Inconclusive is not equivalence.')
