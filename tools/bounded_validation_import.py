"""Read-only adapter for complete, frozen explicit-job reacting campaigns.

The seal records provenance after completion; it is not a new validation
contract. Original schedules, results and cached-job identities are retained.
No mirrors are synthesized and no games or registrations are performed.
"""
from pathlib import Path
import hashlib
import json


def collect(path, ancestors=()):
    from tools.import_validation_league import ROOT, read, digest, require, validate_result
    from src.kaggriculture_meta import championship_league as native
    from src.kaggriculture_meta import public_league as league

    path = Path(path).resolve()
    require(path not in ancestors, 'Cyclic bounded cache provenance')
    plan = read(path/'plan.json')
    identity = read(path/'identity.json')
    completion = read(path/'completion-ready.json')
    files = {}

    def pin(file, expected=None):
        file = Path(file).resolve()
        actual = digest(file)
        require(expected is None or actual == expected, 'Frozen file drift: '+str(file))
        files[str(file)] = actual
        return file

    plan_path = path/'plan.json'
    require(any((ROOT/f).resolve() == plan_path for f in identity), 'Plan not frozen by identity')
    for f, sha in identity.items():
        pin(ROOT/f, sha)
    pin(path/'identity.json')
    pin(path/'completion-ready.json')
    jobs = plan['jobs']
    require(jobs and len(jobs) == completion['games'], 'Incomplete bounded campaign')
    require(len({j['match_id'] for j in jobs}) == len(jobs), 'Duplicate scheduled job')
    # Explicit-job plans use sorted JSON with its default whitespace. Native
    # job hashes separately use championship_league.digest's compact encoding.
    formal_schedule = 'contract' not in plan
    if formal_schedule:
        # Some first-run captures retain the exact schedule from a prepared
        # v2/v3 manifest instead of creating a second explicit-job contract.
        # Verify that original manifest and every job; never synthesize a
        # replacement contract or edit the frozen capture plan.
        provenance = read(pin(path/'import-formal-provenance.json'))
        formal = read(pin(ROOT/provenance['manifest'], provenance['sha256']))
        core = {k:v for k,v in formal.items()
                if k not in ('contract_sha256', 'jobs', 'expected_jobs')}
        contract = native.digest(core)
        require(contract == formal['contract_sha256'] == plan['contract_sha256'],
                'Captured formal contract drift')
        from validation_v2 import make_jobs
        require(formal['jobs'] == make_jobs(formal) == jobs,
                'Captured formal schedule drift')
        require(formal['expected_jobs'] == len(jobs), 'Incomplete formal schedule')
    else:
        contract = hashlib.sha256(json.dumps(plan['contract'], sort_keys=True).encode()).hexdigest()
    require(all(j['contract_sha256'] == contract for j in jobs), 'Bounded contract drift')
    require(1 <= plan['workers'] <= 12, 'Invalid worker count')
    cached = plan.get('cached', {})
    require(set(cached) <= {j['match_id'] for j in jobs}, 'Unscheduled cache entry')
    require(completion['cached'] == len(cached) and completion['new_games'] == len(jobs)-len(cached),
            'Completion/cache coverage differs')
    rows, original_jobs, result_files, provenance = [], [], {}, {}
    models, opponents = {}, {}
    expected_engine = native.engine_identity()

    def check_job(job, formal=False):
        core = {k:v for k,v in job.items() if k != 'match_id'}
        job_id = (native.digest(core) if formal else
                  hashlib.sha256(json.dumps(core, sort_keys=True).encode()).hexdigest())[:24]
        require(job['match_id'] == job_id,
                'Job ID drift')
        require(job['mode'] == 'native_reacting' and job['configuration'] == league.ENGINE_CONFIG,
                'Non-native or incompatible job')
        require(job['engine'] == expected_engine, 'Engine drift')
        for role in ('candidate', 'opponent'):
            pin(ROOT/job[role]['path'], job[role]['sha256'])

    def check_row(job, row):
        validate_result(row)
        require(row['job_sha256'] == native.digest(job), 'Original result job hash mismatch')
        fields = dict(match_id=job['match_id'], seed=job['seed'], candidate_seat=job['candidate_seat'],
            candidate_sha256=job['candidate']['sha256'], opponent_sha256=job['opponent']['sha256'],
            opponent_name=job['opponent']['name'], opponent_family=job['opponent']['family'],
            model=job['candidate']['name'], stage=job['stage'])
        for k, v in fields.items():
            require(row.get(k) == v, 'Original result identity differs: '+k)

    for scheduled in jobs:
        check_job(scheduled, formal=formal_schedule)
        mid = scheduled['match_id']
        wrapper = read(pin(path/'games'/(mid+'.json')))
        require(wrapper['job'] == scheduled, 'Wrapper schedule drift')
        original = scheduled
        if mid in cached:
            cache = cached[mid]
            for f, sha in cache['hashes'].items():
                pin(f, sha)
            result_path = Path(cache['official']).resolve()
            require(str(result_path) in files, 'Unpinned cached result')
            # A cached first-run capture may itself come from a sealed bounded
            # schedule. Revalidate its complete provenance; do not re-label it
            # as a new formal/mirrored job or invent a second rating record.
            bounded_path = result_path.parent.parent
            if result_path.parent.name == 'official' and (bounded_path/'bounded-import.json').exists():
                original_manifest, original_rows = checked_bounded(bounded_path, ancestors=(*ancestors,path))
                prior_seal = read(pin(bounded_path/'bounded-import.json'))
                for f, sha in prior_seal['files'].items():pin(f, sha)
                matches = [j for j in original_manifest['jobs'] if j['match_id'] == result_path.stem]
                require(len(matches) == 1, 'Cached original bounded job missing')
                original = matches[0]
                require(Path(original_manifest['_result_files'][original['match_id']]).resolve() == result_path,
                        'Cached original bounded result path differs')
            else:
                # The original formal manifest is a v2/v3 result's authority.
                original_manifest = read(pin(result_path.parents[2]/'manifest.json'))
                core = {k:v for k,v in original_manifest.items() if k not in ('contract_sha256','jobs','expected_jobs')}
                require(native.digest(core) == original_manifest['contract_sha256'], 'Cached manifest drift')
                from validation_v2 import make_jobs
                require(original_manifest['jobs'] == make_jobs(original_manifest), 'Cached schedule drift')
                matches = [j for j in original_manifest['jobs'] if j['match_id'] == result_path.parent.name]
                require(len(matches) == 1, 'Cached original job missing')
                original = matches[0]
                check_job(original, formal=True)
            for key in ('seed','candidate_seat','configuration','engine','mode'):
                require(original[key] == scheduled[key], 'Cached condition differs: '+key)
            for role in ('candidate','opponent'):
                require(original[role]['sha256'] == scheduled[role]['sha256'], 'Cached source differs')
            require(wrapper['cached_from'] == cache['official'] and wrapper['row'] == cache['row'],
                    'Cache wrapper provenance drift')
            require(wrapper['original_match_id'] == original['match_id'], 'Cached match ID drift')
        else:
            result_path = pin(path/'official'/(mid+'.json'))
            require('cached_from' not in wrapper, 'Undeclared cache')
        row = read(result_path)
        require(wrapper['official'] == row, 'Official result/wrapper drift')
        check_row(original, row)
        audit = wrapper['row']
        require(audit['valid'] and audit['rewards'] == row['rewards'], 'Audit reward mismatch')
        require(audit['job']['seed'] == row['seed'] and audit['job']['seat'] == row['candidate_seat'],
                'Audit condition mismatch')
        seat = row['candidate_seat']
        require(audit['job']['hashes'][seat] == row['candidate_sha256'] and
                audit['job']['hashes'][1-seat] == row['opponent_sha256'], 'Audit source mismatch')
        if mid in cached:
            require(audit['job']['expected_action_hashes'] == row['action_hashes'], 'Cache action mismatch')
        for role, group in (('candidate', models), ('opponent', opponents)):
            ref = original[role]
            require(ref['name'] not in group or
                    group[ref['name']]['sha256'] == ref['sha256'], 'Ambiguous model name')
            group[ref['name']] = ref
        oid = original['match_id']
        require(oid not in result_files, 'Repeated original job in schedule')
        result_files[oid] = str(result_path)
        provenance[oid] = dict(contract_sha256=original['contract_sha256'],
            scheduled_contract_sha256=contract, scheduled_match_id=mid,
            original_result_path=str(result_path), exact_cached_result=mid in cached,
            source='native_bounded_validation', scope=plan.get('scope', 'Explicit frozen schedule'))
        rows.append(row)
        original_jobs.append(original)
    manifest = dict(stage='bounded_development', contract_sha256=contract, jobs=original_jobs,
        expected_jobs=len(jobs), plan=dict(workers=plan['workers'], models=models, opponents=opponents),
        _manifest_file='bounded-import.json', _results_file='completion-ready.json',
        _result_files=result_files, _row_provenance=provenance)
    return manifest, rows, files


def seal_bounded(path):
    from tools.import_validation_league import read, atomic_json, require
    path = Path(path).resolve()
    manifest, rows, files = collect(path)
    seal = dict(schema=1, kind='complete_explicit_native_schedule',
                contract_sha256=manifest['contract_sha256'], games=len(rows), files=files)
    dest = path/'bounded-import.json'
    if dest.exists():
        require(read(dest) == seal, 'Existing bounded seal differs; preserve evidence')
    else:
        atomic_json(dest, seal)
    return dict(sealed=str(dest), games=len(rows), contract_sha256=manifest['contract_sha256'])


def checked_bounded(path, ancestors=()):
    from tools.import_validation_league import read, require
    path = Path(path).resolve()
    seal = read(path/'bounded-import.json')
    manifest, rows, files = collect(path, ancestors=ancestors)
    require(seal == dict(schema=1, kind='complete_explicit_native_schedule',
        contract_sha256=manifest['contract_sha256'], games=len(rows), files=files), 'Bounded seal drift')
    return manifest, rows
