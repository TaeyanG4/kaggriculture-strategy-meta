"""Versioned capture reader for explicit spaced/compact sorted-JSON job IDs.

Original schedules, IDs, wrappers, results, source and trajectory files remain
unchanged. Reuse every v1 identity/execution/accounting check; only recognize
the second deterministic ID encoding used by the new capture generators.
The original v1 adapter and historical seals are never modified.
"""
import hashlib,json,types
from pathlib import Path
from tools import captured_validation_import as base
from tools.import_validation_league import read,require,validate_result
from tools import import_validation_league as bulk

def id_encoding(job):
    core={k:v for k,v in job.items() if k!='match_id'}
    for name,kwargs in [('sorted_spaced_v1',{}),('sorted_compact_v1',dict(separators=(',',':')))]:
        expected=hashlib.sha256(json.dumps(core,sort_keys=True,**kwargs).encode()).hexdigest()[:24]
        if expected==job['match_id']:return name
    raise bulk.ImportRejected('Capture job ID drift in both explicit encodings')

def validate_job(job,contract,engine,pin):
    from src.kaggriculture_meta import public_league as league
    id_encoding(job)
    require(job['contract_sha256']==contract,'Capture owner contract drift')
    require(job['mode']=='native_reacting' and job['configuration']==league.ENGINE_CONFIG and job['engine']==engine,'Capture engine/configuration drift')
    for role in ('candidate','opponent'):pin(job[role]['path'],job[role]['sha256'])

def collect(path,authority_file):
    namespace=dict(base.collect.__globals__,validate_job=validate_job)
    unchanged_checks=types.FunctionType(base.collect.__code__,namespace,base.collect.__name__)
    manifest,rows,files=unchanged_checks(path,authority_file)
    for job in manifest['jobs']:
        manifest['_row_provenance'][job['match_id']].update(job_id_encoding=id_encoding(job),capture_adapter_version=2)
    for f in [__file__,base.__file__]:files[str(Path(f).resolve())]=bulk.digest(f)
    return manifest,rows,files

def seal(path,authority_file):
    path=Path(path).resolve();manifest,rows,files=collect(path,authority_file)
    record=dict(schema=2,kind='frozen_native_capture_schedule_v2',manifest=manifest,files=files,games=len(rows),replay_action_hashes_verified=True,wholefarm_verified=True,original_plans_unchanged=True,original_job_ids_unchanged=True,adapter_sha256=bulk.digest(__file__),base_adapter_sha256=bulk.digest(base.__file__))
    dest=path/'captured-import.json'
    if dest.exists():require(read(dest)==record,'Capture seal already differs')
    else:bulk.atomic_json(dest,record)
    return record

def checked_capture(path):
    path=Path(path).resolve();record=read(path/'captured-import.json')
    if record.get('schema')==1:return base.checked_capture(path)
    require(record['schema']==2 and record['kind']=='frozen_native_capture_schedule_v2','Unknown v2 capture seal')
    require(record['adapter_sha256']==bulk.digest(__file__) and record['base_adapter_sha256']==bulk.digest(base.__file__),'Capture adapter drift')
    for f,h in record['files'].items():require(bulk.digest(f)==h,'Sealed capture drift: '+f)
    manifest=record['manifest'];rows=[read(manifest['_result_files'][j['match_id']]) for j in manifest['jobs']]
    require(len(rows)==record['games']==manifest['expected_jobs'],'Sealed capture coverage drift')
    for j,r in zip(manifest['jobs'],rows):id_encoding(j);validate_result(r)
    return manifest,rows
