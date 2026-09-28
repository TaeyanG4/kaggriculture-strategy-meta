"""Reusable observed-support confirmation; canonical v3 games and exact audits.

Plan supplies immutable source identities and probe/trace entry points. No policy
editing, automatic admission or model polling. Prior runners remain immutable.
"""
import argparse,concurrent.futures,contextlib,hashlib,importlib,io,json,msvcrt,os,statistics,subprocess,sys,time,traceback
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tools'),str(ROOT/'o_tools')]
from state.c485.prepare import read,save,sha

def entry(ref):
    module,name=ref.split(':');return getattr(importlib.import_module(module),name)

def check(out):
    assert datetime.now(timezone.utc)<datetime(2026,9,30,23,59,tzinfo=timezone.utc)
    p=read(out/'plan.json');m=read(out/'manifest.json')
    assert sha(out/'plan.json')==m['plan_sha256'] and sha(out/'config-template.json')==m['template_sha256']
    for path,h in read(out/'chain-identity.json').items():assert sha(ROOT/path)==h,path
    for key,path in p['policies'].items():assert sha(path)==p['hashes'][key],key
    return p,m

def run_probe(payload):
    return entry(payload['entry'])(payload['job'])

def batch_prefix(out,p,seeds):
    folder=out/'prefix';folder.mkdir(exist_ok=True);rows={};jobs=[dict(seed=s) for s in seeds]
    for job in jobs:
        dest=folder/(str(job['seed'])+'.json')
        if dest.exists():
            r=read(dest);assert r['job']==job;rows[job['seed']]=r
    with concurrent.futures.ProcessPoolExecutor(max_workers=p['workers'],max_tasks_per_child=1) as pool:
        pending={pool.submit(run_probe,dict(entry=p['probe_entry'],job=j)):j for j in jobs if j['seed'] not in rows}
        for f in concurrent.futures.as_completed(pending):
            j=pending[f];r=f.result();assert r['job']==j;save(folder/(str(j['seed'])+'.json'),r);rows[j['seed']]=r
    return [rows[j['seed']] for j in jobs]

def audit_game(payload):
    out=Path(payload['out']);job=payload['job'];dest=out/(job['label']+'-result.json')
    if dest.exists():
        r=read(dest);assert r['job']==job;return r
    from state.c386 import diagnose_losses as runner
    runner.OUT=out;r=runner.run(job);save(dest,r);return r

def trace_game(payload):return entry(payload['entry'])(payload['row'])

def audit(out,p,conditions,index):
    chosen=[];seen=set();active=[c for c in conditions if c['trigger']]
    def add(c):
        key=(c['seed'],c['opponent'],c['seat'])
        if key not in seen and len(chosen)<6:chosen.append(c);seen.add(key)
    pool=active or conditions
    add(min(pool,key=lambda c:c['own']));add(min(pool,key=lambda c:c['margin']));add(max(pool,key=lambda c:c['margin']))
    for seed in sorted({c['seed'] for c in pool}):add(min((c for c in pool if c['seed']==seed),key=lambda c:c['margin']))
    for c in sorted(pool,key=lambda c:(not c['win_to_loss'],c['margin'],c['seed'],c['opponent'],c['seat'])):add(c)
    jobs=[]
    for c in chosen:
        for model in ('parent',p['candidate']):
            s=c['seat'];names=[model,c['opponent']] if s==0 else [c['opponent'],model];r=index[c['stage'],model,c['opponent'],c['seed'],s]
            jobs.append(dict(label=f"{p['campaign']}-audit-{model}-{c['opponent']}-{c['seed']}-s{s}",model=model,opponent=c['opponent'],seed=c['seed'],seat=s,paths=[p['policies'][n] for n in names],hashes=[p['hashes'][n] for n in names],expected=r['rewards'],expected_action_hashes=r['action_hashes']))
    save(out/'selected-plan.json',dict(rule='Worst own/margin, best margin, every active world worst then win-loss/risk order to6; no new games selected by win only.',jobs=jobs,unaudited_win_losses=[c for c in conditions if c['win_to_loss'] and (c['seed'],c['opponent'],c['seat']) not in seen]))
    with concurrent.futures.ProcessPoolExecutor(max_workers=p['workers'],max_tasks_per_child=1) as ex:rows=list(ex.map(audit_game,[dict(out=str(out),job=j) for j in jobs]))
    save(out/'selected-summary.json',rows)
    from tools import c300_execution_audit as qa
    for r in rows:
        replay=read(r['replay']);actual=[]
        for s in (0,1):
            h=hashlib.sha256()
            for frame in replay['steps'][1:]:h.update(qa.encode(frame[s]['action']))
            actual.append(h.hexdigest())
        assert actual==r['job']['expected_action_hashes']
    with concurrent.futures.ProcessPoolExecutor(max_workers=min(6,p['workers']),max_tasks_per_child=1) as ex:traces=list(ex.map(trace_game,[dict(entry=p['trace_entry'],row=r) for r in rows[1::2]]))
    save(out/'service-traces.json',traces)
    from state.c429.audit_selected import failures,escapes
    from state.c479.chain import shortfalls
    from state.c493.review import stock
    pairs=[];strict=[]
    for a,b in zip(rows[::2],rows[1::2]):
        s=b['job']['seat'];la,lb=read(a['ledger']),read(b['ledger']);ra,rb=read(a['replay']),read(b['replay']);ta,tb=la['totals'][s],lb['totals'][s]
        extra=sorted(failures(lb,s)-failures(la,s));short=shortfalls(lb,rb,s)-shortfalls(la,ra,s);ea,eb=escapes(ra,s),escapes(rb,s)
        checks=dict(exact=la['valid'] and lb['valid'] and la['original_observations_match'] and lb['original_observations_match'],cash=ta['cash_residual']==tb['cash_residual']==0,no_extra_failed_feed=not any(x[2][0]=='FEED' for x in extra),escapes=len(eb)<=len(ea),investment=not short)
        pairs.append(dict(seed=b['job']['seed'],opponent=b['job']['opponent'],seat=s,checks=checks,qualified=all(checks.values()),new_ineffective=extra,new_investment_shortfalls=[dict(key=k,quantity=v) for k,v in short.items()],production=[ta['harvested_and_collected'],tb['harvested_and_collected']],same_shops=ra['steps'][-1][0]['observation']['town']==rb['steps'][-1][0]['observation']['town'],discards=[[d for d in l['day_end_discards'] if d['seat']==s] for l in (la,lb)]))
        strict.append(dict(label=b['job']['label'],no_extra_species=not(Counter(e[3] for e in eb)-Counter(e[3] for e in ea)),no_extra_terminal=not(stock(rb,s)-stock(ra,s))))
    result=dict(qualified=all(r['qualified'] for r in pairs),exact_actions=sum(t['exact_actions'] for t in traces),pairs=pairs,scope='Selected exact execution; all ineffective commands/production changes need manual review.')
    save(out/'selected-accounting.json',result);save(out/'species-terminal-review.json',strict)
    return dict(qualified=result['qualified'] and all(t['qualified'] for t in traces) and all(t['no_extra_species'] and t['no_extra_terminal'] for t in strict),exact_actions=result['exact_actions'])

def stats(cs):
    return dict(conditions=len(cs),**{k:statistics.mean(c[k] for c in cs) for k in ('own','margin','points')},win_to_loss=sum(c['win_to_loss'] for c in cs),loss_to_win=sum(c['points']>0 for c in cs),changed=sum(c['trigger'] for c in cs))

def main(out):
    p,m=check(out);cfg=read(out/'config-template.json');candidate=p['candidate']
    os.environ.update(PYTHONHASHSEED='0',KAGGRICULTURE_VALIDATION_GUARDED='1',KAGGRICULTURE_RESEARCH_OWNER_PID=str(os.getpid()))
    with (ROOT/'state/agent_experiments/.kaggriculture-global-launch.lock').open('a+b') as lock:
        lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        from state.c447.formal.league_priority import stop_if_running,start_guard,get
        save(out/'league-before.json',stop_if_running());start_guard()
        while get()['battle']['phase']!='stopped':time.sleep(3)
        save(out/'process.json',dict(pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),workers=p['workers'],model_workers=0))
        selected=[];probes=[]
        for offset in range(0,len(p['probe_seeds']),p['workers']):
            if len(selected)>=p['wanted']:break
            rows=batch_prefix(out,p,p['probe_seeds'][offset:offset+p['workers']]);probes+=rows
            for r in rows:
                if r['supported'] and len(selected)<p['wanted']:selected.append(r['job']['seed'])
        save(out/'coverage.json',dict(qualified=len(selected)==p['wanted'],selected=selected,prefixes=len(probes),results=probes,selection=p['selection']))
        if len(selected)<p['wanted']:
            save(out/'completion-ready.json',dict(at=datetime.now(timezone.utc).isoformat(),status='support insufficient; full games0',fresh_games=0,registered=False,submitted=False));return
        assert len(selected)==4
        cfg['stages']={k:dict(seeds=s,alpha=a) for k,s,a in [('screen',selected[:2],.02),('confirm',selected[2:],.02),('final',p['reserved_final'],.009)]}
        config=Path(m['config'])
        if config.exists():assert read(config)==cfg
        else:save(config,cfg)
        save(out/'formal-identity.json',dict(config_sha256=sha(config),seeds=selected,frozen_before_full_games=True,source_unchanged=True))
        raw={};warnings=[]
        for stage in ('screen','confirm'):
            check(out);dest=Path(p['formal_paths'][stage])
            for args in (['prepare','--config',str(config),'--stage',stage,'--out',str(dest)],['run','--out',str(dest)]):
                with (out/'validation.log').open('a',encoding='utf8') as f:subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/validation_v3.py'),*args],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
            summary=read(dest/'results.json');assert summary['status']=='complete' and summary['completed_jobs']==read(dest/'manifest.json')['expected_jobs']==64
            for path in (dest/'jobs').glob('*/result.json'):
                r=read(path);assert r['valid'] and not r.get('health_failures'),(path,r.get('health_failures'))
                assert r['candidate_sha256']==p['hashes'][r['model']] and r['opponent_sha256']==p['hashes'][r['opponent_name']]
                raw[stage,r['model'],r['opponent_name'],r['seed'],r['candidate_seat']]=r
                if r.get('timing_warnings'):warnings.append(dict(match_id=r['match_id'],warnings=r['timing_warnings']))
        assert len(raw)==128
        cs=[]
        for stage in ('screen','confirm'):
            for seed in cfg['stages'][stage]['seeds']:
                for op in p['opponents']:
                    for s in (0,1):
                        a,b=[raw[stage,n,op,seed,s] for n in ('parent',candidate)];am=a['rewards'][s]-a['rewards'][1-s];bm=b['rewards'][s]-b['rewards'][1-s]
                        point=lambda x:float(x>0)+.5*(x==0)
                        cs.append(dict(stage=stage,seed=seed,opponent=op,seat=s,shops=b['shops'],trigger=a['action_hashes']!=b['action_hashes'],own=b['rewards'][s]-a['rewards'][s],margin=bm-am,points=point(bm)-point(am),parent_margin=am,candidate_margin=bm,win_to_loss=am>0 and bm<0))
        total=stats(cs);public=stats([c for c in cs if c['opponent'] not in p['colleague_opponents']]);worlds={str(s):stats([c for c in cs if c['seed']==s]) for s in selected}
        checks=dict(own=total['own']>=0,margin=total['margin']>0,points=total['points']>=0,public_own=public['own']>=0,public_margin=public['margin']>=0,public_points=public['points']>=0,two_positive_worlds=sum(x['margin']>0 for x in worlds.values())>=2)
        save(out/'independent-review-metrics.json',dict(qualified=all(checks.values()),checks=checks,overall=total,public=public,worlds=worlds,opponents={op:stats([c for c in cs if c['opponent']==op]) for op in p['opponents']},stages={st:stats([c for c in cs if c['stage']==st]) for st in ('screen','confirm')},conditions=cs,timing_warnings=warnings,scope=p['scope']))
        account=audit(out,p,cs,raw);check(out);assert sha(config)==read(out/'formal-identity.json')['config_sha256']
        save(out/'completion-ready.json',dict(at=datetime.now(timezone.utc).isoformat(),status='fresh conditional128 and exact accounting complete; manual review',fresh_games=128,strength_qualified=all(checks.values()),accounting_qualified=account['qualified'],exact_actions=account['exact_actions'],source_sha256=p['hashes'][candidate],registered=False,submitted=False,scope=p['scope']))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args();out=Path(args.out).resolve()
    try:main(out)
    except Exception:save(out/'execution-error.json',dict(at=datetime.now(timezone.utc).isoformat(),error=traceback.format_exc()));raise
