"""Config-driven native reacting evaluator v1. Prepare/check/analyze never run games."""
import argparse
from collections import deque
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.kaggriculture_meta import championship_league as L
from validation_stats_v1 import analyze

SUPPORT=[Path(__file__),ROOT/'tools/validation_stats_v1.py',ROOT/'tools/run-validation.ps1',
         ROOT/'src/kaggriculture_meta/championship_league.py']
def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def require(ok,message):
    if not ok: raise ValueError(message)

def validate_config(p):
    require(p.get('schema')==1,'schema must be 1')
    require(type(p.get('workers')) is int and 1<=p['workers']<=8,'workers must be 1..8')
    require(type(p.get('timeout_seconds')) is int and p['timeout_seconds']>0,'positive timeout required')
    require(p.get('configuration')=={'episodeSteps':720},'v1 pins default 720-turn configuration')
    require(set(p['stages'])=={'screen','confirm','final'},'Declare all three disjoint stages')
    seen=set()
    for stage,entry in p['stages'].items():
        seeds=entry['seeds']
        require(isinstance(seeds,list) and len(seeds)>=2 and all(type(s) is int and 0<=s<2**31 for s in seeds),'At least two integer seeds per stage')
        require(len(set(seeds))==len(seeds) and not seen.intersection(seeds),'Seed leakage/duplicates')
        seen.update(seeds)
        require(isinstance(entry['alpha'],(float,int)) and 0<entry['alpha']<.05,'Each stage needs alpha allocation')
    require(sum(v['alpha'] for v in p['stages'].values())<=.050000001,'Total stage alpha must be <= .05')
    for group in ('models','opponents'):
        require(bool(p[group]),'Empty '+group)
        for name,ref in p[group].items():
            require(bool(re.fullmatch(r'[A-Za-z0-9_-]+',name)),'Use simple unique labels')
            require(bool(re.fullmatch(r'[a-f0-9]{64}',ref['sha256'])),'Exact source SHA256 required')
            require(isinstance(ref['path'],str),'Source path required')
            if group=='opponents': require(bool(ref.get('family')),'Opponent family required')
        require(len({r['sha256'] for r in p[group].values()})==len(p[group]),'Duplicate source aliases in '+group)
    pairs=[]
    for c in p['comparisons']:
        require(c['candidate'] in p['models'] and c['parent'] in p['models'] and c['candidate']!=c['parent'],'Bad comparison')
        require(type(c['primary']) is bool,'primary must be Boolean')
        pairs.append((c['candidate'],c['parent']))
    require(len(pairs)==len(set(pairs)) and any(c['primary'] for c in p['comparisons']),'Duplicate/no primary comparisons')

def support_hashes(): return {str(p.relative_to(ROOT)):L.digest(p.read_bytes()) for p in SUPPORT}

def make_jobs(m):
    jobs=[]
    for seed in m['plan']['stages'][m['stage']]['seeds']:
        for opponent,ref in m['opponents'].items():
            for seat in (0,1):
                for model,source in m['models'].items():
                    j=dict(schema=2,engine=m['engine'],mode='native_reacting',stage=m['stage'],seed=seed,
                        candidate_seat=seat,configuration=m['plan']['configuration'],candidate=dict(source,name=model),
                        opponent=dict(ref,name=opponent),contract_sha256=m['contract_sha256'])
                    jobs.append(dict(j,match_id=L.digest(j)[:24]))
    return jobs

def prepare(config,stage,out):
    p=read(config); validate_config(p)
    if (out/'manifest.json').exists():
        m=check(out); require(m['plan']==p and m['stage']==stage,'Frozen plan differs; use a new output'); return m
    require(not out.exists() or not any(out.iterdir()),'New campaign output must be empty')
    engine=L.engine_identity()
    require(engine==p['engine'],'Engine does not match configuration')
    # Check every source before creating the new experiment.
    for ref in list(p['models'].values())+list(p['opponents'].values()):
        data=(ROOT/ref['path']).read_bytes()
        require(L.digest(data)==ref['sha256'],'Source hash mismatch: '+ref['path'])
        compile(data,ref['path'],'exec')
    m=dict(schema=1,plan=p,stage=stage,engine=engine,support=support_hashes(),
           output=str(out),models={},opponents={})
    for group in ('models','opponents'):
        for label,ref in p[group].items():
            m[group][label]=L.frozen_source(ROOT/ref['path'],out)
            if group=='opponents': m[group][label]['family']=ref['family']
    m['contract_sha256']=L.digest(m)
    m['jobs']=make_jobs(m); m['expected_jobs']=len(m['jobs'])
    L.write_json(out/'manifest.json',m)
    check(out)
    print('PREPARED '+str(m['expected_jobs'])+' games; none executed.',flush=True)
    return m

def check(out):
    m=read(out/'manifest.json'); validate_config(m['plan'])
    core={k:v for k,v in m.items() if k not in ('contract_sha256','jobs','expected_jobs')}
    require(L.digest(core)==m['contract_sha256'],'Manifest contract drift')
    require(str(out)==m['output'],'Output path drift')
    require(m['support']==support_hashes(),'Runner changed; retain versioned code or create new paired campaign')
    require(m['engine']==L.engine_identity()==m['plan']['engine'],'Engine drift')
    require(m['jobs']==make_jobs(m) and len(m['jobs'])==m['expected_jobs'],'Job coverage drift')
    for group in ('models','opponents'):
        for label,ref in m[group].items():
            path=Path(ref['path'])
            require(path==out/'sources'/(ref['sha256']+'.py'),'Snapshot path escaped campaign')
            require(ref['sha256']==m['plan'][group][label]['sha256'] and L.digest(path.read_bytes())==ref['sha256'],'Snapshot drift')
    return m

def validate_row(j,r):
    require(r.get('job_sha256')==L.digest(j),'Cache job hash mismatch')
    L.require_valid([r],1)
    fields=dict(match_id=j['match_id'],seed=j['seed'],resolved_seed=j['seed'],candidate_seat=j['candidate_seat'],
        candidate_sha256=j['candidate']['sha256'],opponent_sha256=j['opponent']['sha256'],
        opponent_name=j['opponent']['name'],opponent_family=j['opponent']['family'],model=j['candidate']['name'],
        mode='native_reacting',stage=j['stage'],states=720,statuses=['DONE','DONE'],errors=[[],[]])
    for key,value in fields.items(): require(r.get(key)==value,'Row identity mismatch: '+key)
    require(all(r[role+'_timing']['calls']==719 for role in ('candidate','opponent')),'Incomplete decision count')
    seat=j['candidate_seat']; margin=r['rewards'][seat]-r['rewards'][1-seat]
    require(r['margin']==margin and r['outcome']==('win' if margin>0 else 'loss' if margin<0 else 'tie'),'Outcome mismatch')

def load_rows(out,m):
    rows=[]
    for j in m['jobs']:
        p=out/'jobs'/j['match_id']/'result.json'
        if p.exists():
            r=read(p); validate_row(j,r); rows.append(r)
    return rows

def report(out,m,rows,cached=0):
    result=analyze(m['plan'],m['stage'],rows)
    result.update(contract_sha256=m['contract_sha256'],cached=cached)
    L.write_json(out/'results.json',result)
    print('DONE: '+str(out/'results.json'),flush=True)
    return result

def child_environment(folder):
    env=os.environ.copy(); env['PYTHONHASHSEED']='0'; env['PYTHONDONTWRITEBYTECODE']='1'
    for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR','NUMBA_CACHE_DIR'):
        p=folder/key.lower(); p.mkdir(exist_ok=True); env[key]=str(p)
    return env

def stop_owned(process):
    if process.poll() is not None: return
    if os.name=='nt':
        result=subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True)
        require(result.returncode==0 or process.poll() is not None,'Failed to stop owned worker tree')
    else: process.kill()
    process.wait(timeout=15)

def run(out):
    require(os.environ.get('KAGGRICULTURE_VALIDATION_GUARDED')=='1','Use tools/run-validation.ps1')
    m=check(out); rows=load_rows(out,m); cached=len(rows); done={r['match_id'] for r in rows}
    pending=deque(j for j in m['jobs'] if j['match_id'] not in done)
    active=[]; started=time.monotonic(); last=0; failed=0
    def progress():
        elapsed=time.monotonic()-started; rate=(len(rows)-cached)/max(elapsed,.001)
        print('PROGRESS|'+json.dumps(dict(done=len(rows),total=m['expected_jobs'],percent=100*len(rows)/m['expected_jobs'],
            cached=cached,failed=failed,active=len(active),elapsed=elapsed,rate=rate,
            eta=(m['expected_jobs']-len(rows))/rate if rate else None)),flush=True)
    progress()
    try:
        while pending or active:
            while pending and len(active)<m['plan']['workers']:
                j=pending.popleft(); folder=out/'jobs'/j['match_id']; folder.mkdir(parents=True,exist_ok=True)
                jp=folder/'job.json'
                if jp.exists(): require(read(jp)==j,'Stored job drift')
                else: L.write_json(jp,j)
                attempt=time.time_ns(); log=(folder/f'worker-{attempt}.log').open('x',encoding='utf-8')
                try:
                    p=subprocess.Popen([sys.executable,'-X','utf8',str(Path(__file__)),'worker','--out',str(out),'--job',str(jp)],
                        cwd=folder,env=child_environment(folder),stdout=log,stderr=log)
                except BaseException: log.close(); raise
                active.append((p,j,folder,log,time.monotonic()))
            for item in active[:]:
                p,j,folder,log,begun=item
                if p.poll() is None:
                    if time.monotonic()-begun>m['plan']['timeout_seconds']: raise RuntimeError('Timeout: '+str(folder))
                    continue
                log.close(); active.remove(item)
                require(p.returncode==0,'Worker failed; inspect '+str(folder))
                r=read(folder/'result.json'); validate_row(j,r); rows.append(r)
            if time.monotonic()-last>=5: progress(); last=time.monotonic()
            if active: time.sleep(.25)
        progress(); return report(out,m,rows,cached)
    except BaseException as exc:
        failed+=1; progress()
        L.write_json(out/f'failure-{time.time_ns()}.json',dict(error=repr(exc),completed=len(rows)))
        raise
    finally:
        cleanup=[]
        for p,j,folder,log,begun in active:
            try: stop_owned(p)
            except Exception as exc: cleanup.append(str(exc))
            finally: log.close()
        if cleanup: raise RuntimeError('Worker cleanup failed: '+'; '.join(cleanup))

def worker(out,jp):
    # Full contract readback also prevents loading a later changed runner mid-campaign.
    m=check(out); j=read(jp)
    require(j in m['jobs'] and jp==out/'jobs'/j['match_id']/'job.json','Unexpected worker job/path')
    r=L.run_match(j); r.update(job_sha256=L.digest(j),model=j['candidate']['name'])
    L.write_json(jp.parent/'result.json',r)  # Preserve even a failed game's evidence.
    validate_row(j,r)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('action',choices=['prepare','check','run','analyze','worker'])
    ap.add_argument('--config',type=Path); ap.add_argument('--stage',choices=['screen','confirm','final'],default='screen')
    ap.add_argument('--out',type=Path,required=True); ap.add_argument('--job',type=Path)
    args=ap.parse_args(); out=args.out.resolve()
    if args.action=='prepare': prepare(args.config,args.stage,out)
    elif args.action=='check': m=check(out); print('CHECK PASSED: '+str(m['expected_jobs']))
    elif args.action=='run': run(out)
    elif args.action=='analyze': m=check(out); report(out,m,load_rows(out,m))
    elif args.action=='worker': worker(out,args.job.resolve())

if __name__=='__main__': main()
