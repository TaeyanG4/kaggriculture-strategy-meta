"""Seal frozen first-run captures without rewriting their plans or job IDs.

The c638+ capture plans bind the bytes of an existing owner contract rather
than inventing a second sorted-JSON contract. Cached jobs retain their original
IDs and wrappers. This read-only adapter supplies the common league importer.
"""
import hashlib,json
from pathlib import Path
from tools.import_validation_league import ROOT,read,require,validate_result
from tools import import_validation_league as bulk

def validate_job(job,contract,engine,pin):
    from src.kaggriculture_meta import public_league as league
    core={k:v for k,v in job.items() if k!='match_id'}
    require(hashlib.sha256(json.dumps(core,sort_keys=True).encode()).hexdigest()[:24]==job['match_id'],'Capture job ID drift')
    require(job['contract_sha256']==contract,'Capture owner contract drift')
    require(job['mode']=='native_reacting' and job['configuration']==league.ENGINE_CONFIG and job['engine']==engine,'Capture engine/configuration drift')
    for role in ('candidate','opponent'):pin(job[role]['path'],job[role]['sha256'])

def validate_replay(replay,row):
    frames=replay['steps'];require(len(frames)==720,'Capture trajectory incomplete')
    require(not any(z['status'] in ('ERROR','INVALID','TIMEOUT') for frame in frames for z in frame),'Capture trajectory error')
    require([z['reward'] for z in frames[-1]]==row['rewards'],'Capture terminal rewards differ')
    hashes=[]
    for seat in (0,1):
        h=hashlib.sha256()
        for frame in frames[1:]:h.update(json.dumps(frame[seat]['action'],sort_keys=True,separators=(',',':')).encode())
        hashes.append(h.hexdigest())
    require(hashes==row['action_hashes'],'Capture callback/replay action mismatch')

def collect(path,authority_file):
    from src.kaggriculture_meta import championship_league as native
    path=Path(path).resolve();files={}
    def pin(f,expected=None):
        f=Path(f).resolve();h=bulk.digest(f);require(expected is None or h==expected,'Capture frozen file drift: '+str(f));files[str(f)]=h;return f
    plan=read(pin(path/'plan.json'));identity=read(pin(path/'identity.json'));completion=read(pin(path/'completion-ready.json'))
    require(any((ROOT/f).resolve()==path/'plan.json' for f in identity),'Capture plan was not frozen')
    for f,h in identity.items():pin(ROOT/f,h)
    authority=pin(authority_file);contract=bulk.digest(authority);jobs=plan['jobs'];cached=plan.get('cached',{})
    require(completion['total']==len(jobs) and completion['cached_games']==len(cached) and completion['new_games']==len(jobs)-len(cached),'Capture completion coverage differs')
    require(len({j['match_id'] for j in jobs})==len(jobs) and set(cached)<={j['match_id'] for j in jobs},'Capture duplicate/missing jobs')
    require(completion['execution_pass'] and 1<=plan['workers']<=12,'Capture execution not qualified')
    engine=native.engine_identity();rows=[];models={};opponents={};result_files={};provenance={}
    for j in jobs:
        mid=j['match_id'];cache=cached.get(mid)
        # A reused original job can predate a later owner-record update. Its
        # frozen original plan below binds that historical contract field.
        # New jobs must match the current contract bytes; never relabel either.
        validate_job(j,j['contract_sha256'] if cache else contract,engine,pin)
        wp=pin(cache['path'],cache['sha256']) if cache else pin(path/'games'/(mid+'.json'))
        wrapper=read(wp);require(wrapper['job']==j,'Capture wrapper/schedule mismatch');origin=wp.parent.parent
        if cache:
            origin_plan=origin/('probe-plan.json' if (origin/'probe-plan.json').exists() else 'plan.json')
            origin_identity=origin/('probe-identity.json' if (origin/'probe-identity.json').exists() else 'identity.json')
            oi=read(pin(origin_identity));op=read(pin(origin_plan));require(j in op['jobs'],'Original cached capture was not scheduled')
            require(any((ROOT/f).resolve()==origin_plan and bulk.digest(origin_plan)==h for f,h in oi.items()),'Original capture plan not frozen')
            pin(wrapper['row']['replay'],cache['replay_sha256']);pin(wrapper['row']['ledger'],cache['ledger_sha256'])
        result_path=pin(origin/'official'/(mid+'.json'));r=read(result_path);validate_result(r)
        require(wrapper['official']==r and r['job_sha256']==native.digest(j),'Capture official job hash mismatch')
        fields=dict(match_id=mid,seed=j['seed'],candidate_seat=j['candidate_seat'],candidate_sha256=j['candidate']['sha256'],opponent_sha256=j['opponent']['sha256'],opponent_name=j['opponent']['name'],opponent_family=j['opponent']['family'],model=j['candidate']['name'],stage=j['stage'])
        require(all(r.get(k)==v for k,v in fields.items()),'Capture official identity mismatch')
        a=wrapper['row'];require(a['valid'] and a['rewards']==r['rewards'] and a['job']['seed']==j['seed'] and a['job']['seat']==j['candidate_seat'],'Capture audit identity mismatch')
        s=j['candidate_seat'];require(a['job']['hashes'][s]==j['candidate']['sha256'] and a['job']['hashes'][1-s]==j['opponent']['sha256'],'Capture audit source mismatch')
        validate_replay(read(pin(a['replay'])),r);ledger=read(pin(a['ledger']))
        require(ledger['valid'] and ledger['original_observations_match'] and all(t['cash_residual']==0 for t in ledger['totals']),'Capture wholefarm accounting failure')
        for role,dest in [('candidate',models),('opponent',opponents)]:
            ref=j[role];require(ref['name'] not in dest or dest[ref['name']]['sha256']==ref['sha256'],'Capture ambiguous source name');dest[ref['name']]=ref
        rows.append(r);result_files[mid]=str(result_path);provenance[mid]=dict(source='native_captured_validation',original_result_path=str(result_path),original_wrapper_path=str(wp),exact_cached_result=bool(cache),contract_sha256=j['contract_sha256'],scheduled_authority_sha256=contract,authority_file=str(authority),historical_contract_bound_by_original_frozen_plan=bool(cache),selection='All valid scheduled results, including losses; fixed validation panel, not random matchmaking')
    manifest=dict(stage='bounded_development',contract_sha256=contract,jobs=jobs,expected_jobs=len(jobs),plan=dict(workers=plan['workers'],models=models,opponents=opponents),_manifest_file='captured-import.json',_results_file='completion-ready.json',_result_files=result_files,_row_provenance=provenance)
    return manifest,rows,files

def seal(path,authority_file):
    path=Path(path).resolve();manifest,rows,files=collect(path,authority_file)
    record=dict(schema=1,kind='frozen_native_capture_schedule',manifest=manifest,files=files,games=len(rows),replay_action_hashes_verified=True,wholefarm_verified=True,original_plans_unchanged=True,adapter_sha256=bulk.digest(__file__))
    dest=path/'captured-import.json'
    if dest.exists():require(read(dest)==record,'Capture seal already differs')
    else:bulk.atomic_json(dest,record)
    return record

def checked_capture(path):
    path=Path(path).resolve();seal=read(path/'captured-import.json');require(seal['schema']==1 and seal['kind']=='frozen_native_capture_schedule','Unknown capture seal')
    require(seal['adapter_sha256']==bulk.digest(__file__),'Capture adapter drift')
    for f,h in seal['files'].items():require(bulk.digest(f)==h,'Sealed capture drift: '+f)
    m=seal['manifest'];rows=[read(m['_result_files'][j['match_id']]) for j in m['jobs']]
    require(len(rows)==seal['games']==m['expected_jobs'],'Sealed capture coverage drift')
    for r in rows:validate_result(r)
    return m,rows
