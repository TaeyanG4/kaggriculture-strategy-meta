import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tests import test_validation_league_import as fixtures
from tools import bounded_validation_import as bounded
from tools import import_validation_league as bulk
from src.kaggriculture_meta import championship_league as native
from src.kaggriculture_meta import public_league as league


class BoundedImportTests(unittest.TestCase):
    ref = fixtures.ValidationImportTests.ref

    def setUp(self):
        fixtures.ValidationImportTests.setUp(self)
        self.engine = dict(version='fixture', files={})
        self.engine_patch = patch.object(native, 'engine_identity', return_value=self.engine)
        self.engine_patch.start()
        self.contract = dict(scope='fixed explicit fixtures')
        contract_sha = hashlib.sha256(json.dumps(self.contract, sort_keys=True).encode()).hexdigest()
        self.jobs = []
        for index, old in enumerate(self.rows):
            job = dict(schema=2, engine=self.engine, mode='native_reacting', stage='bounded',
                seed=99, candidate_seat=index, configuration=league.ENGINE_CONFIG,
                candidate=dict(self.ref(0), name='c'), opponent=dict(self.ref(1), name='o', family='fixture'),
                contract_sha256=contract_sha)
            job['match_id'] = hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()[:24]
            row = dict(old, match_id=job['match_id'], stage='bounded', model='c',
                       opponent_name='o', opponent_family='fixture', job_sha256=native.digest(job))
            audit = dict(valid=True, rewards=row['rewards'], job=dict(seed=99, seat=index,
                hashes=[self.ref(index)['sha256'], self.ref(1-index)['sha256']]))
            self.write(self.campaign/'official'/(job['match_id']+'.json'), row)
            self.write(self.campaign/'games'/(job['match_id']+'.json'), dict(job=job, official=row, row=audit))
            self.jobs.append(job)
        self.plan = dict(workers=8, contract=self.contract, jobs=self.jobs, cached={})
        self.write(self.campaign/'completion-ready.json', dict(games=2, cached=0, new_games=2))
        self.freeze_plan()

    def tearDown(self):
        self.engine_patch.stop()
        fixtures.ValidationImportTests.tearDown(self)

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), 'utf8')

    def freeze_plan(self):
        file = self.campaign/'plan.json'
        self.write(file, self.plan)
        self.write(self.campaign/'identity.json', {str(file): bulk.digest(file)})

    def make_cache(self):
        from validation_v2 import make_jobs
        scheduled = self.jobs[1]
        original = self.root/'original'
        manifest = dict(stage='screen', engine=self.engine,
            models={'c':dict(self.ref(0))}, opponents={'o':dict(self.ref(1), family='fixture')},
            plan=dict(configuration=league.ENGINE_CONFIG, stages=dict(screen=dict(seeds=[99]))))
        manifest['contract_sha256'] = native.digest(manifest)
        manifest['jobs'] = make_jobs(manifest)
        manifest['expected_jobs'] = len(manifest['jobs'])
        job = manifest['jobs'][1]
        self.write(original/'manifest.json', manifest)
        wrapper_path = self.campaign/'games'/(scheduled['match_id']+'.json')
        wrapper = bulk.read(wrapper_path)
        row = dict(wrapper['official'], match_id=job['match_id'], stage='screen', job_sha256=native.digest(job))
        result_path = original/'jobs'/job['match_id']/'result.json'
        self.write(result_path, row)
        wrapper['official'] = row
        wrapper['row']['job']['expected_action_hashes'] = row['action_hashes']
        wrapper.update(cached_from=str(result_path), original_match_id=job['match_id'])
        self.write(wrapper_path, wrapper)
        self.plan['cached'][scheduled['match_id']] = dict(official=str(result_path), row=wrapper['row'],
            hashes={str(result_path): bulk.digest(result_path)})
        self.freeze_plan()
        self.write(self.campaign/'completion-ready.json', dict(games=2, cached=1, new_games=1))
        return result_path, job

    def test_complete_batch_import_and_retry(self):
        bounded.seal_bounded(self.campaign)
        with patch.object(league, 'engine_sha', return_value='e'*64):
            planned, summary = bulk.prepare(self.store.db, [self.campaign])
            self.assertEqual(summary['new_games'], 2)
            bulk.apply_batch(self.store, planned, summary, self.receipt)
            _, again = bulk.prepare(self.store.db, [self.campaign])
            self.assertEqual((again['already_present'], again['new_games']), (2, 0))

    def make_formal_capture(self):
        from validation_v2 import make_jobs
        manifest = dict(stage='screen', engine=self.engine,
            models={'c':dict(self.ref(0))}, opponents={'o':dict(self.ref(1), family='fixture')},
            plan=dict(configuration=league.ENGINE_CONFIG, stages=dict(screen=dict(seeds=[99]))))
        manifest['contract_sha256'] = native.digest(manifest)
        manifest['jobs'] = make_jobs(manifest)
        manifest['expected_jobs'] = len(manifest['jobs'])
        path = self.root/'prepared-formal'/'manifest.json'
        self.write(path, manifest)
        self.write(self.campaign/'import-formal-provenance.json',
                   dict(manifest=str(path), sha256=bulk.digest(path)))
        for index, job in enumerate(manifest['jobs']):
            row = dict(self.rows[index], match_id=job['match_id'], stage='screen', model='c',
                       opponent_name='o', opponent_family='fixture', job_sha256=native.digest(job))
            audit = dict(valid=True, rewards=row['rewards'], job=dict(seed=99, seat=index,
                hashes=[self.ref(index)['sha256'], self.ref(1-index)['sha256']]))
            self.write(self.campaign/'official'/(job['match_id']+'.json'), row)
            self.write(self.campaign/'games'/(job['match_id']+'.json'), dict(job=job, official=row, row=audit))
        self.plan = dict(workers=8, contract_sha256=manifest['contract_sha256'],
                         jobs=manifest['jobs'], cached={})
        self.freeze_plan()
        return path

    def test_captured_formal_schedule_imports_without_rewriting_plan(self):
        self.make_formal_capture()
        plan_bytes = (self.campaign/'plan.json').read_bytes()
        bounded.seal_bounded(self.campaign)
        self.assertEqual((self.campaign/'plan.json').read_bytes(), plan_bytes)
        with patch.object(league, 'engine_sha', return_value='e'*64):
            planned, summary = bulk.prepare(self.store.db, [self.campaign])
            self.assertEqual(summary['new_games'], 2)
            bulk.apply_batch(self.store, planned, summary, self.receipt)
            _, again = bulk.prepare(self.store.db, [self.campaign])
            self.assertEqual((again['already_present'], again['new_games']), (2, 0))

    def test_captured_formal_schedule_cannot_filter_a_loss(self):
        self.make_formal_capture()
        self.plan['jobs'] = self.plan['jobs'][:1]
        self.freeze_plan()
        self.write(self.campaign/'completion-ready.json', dict(games=1, cached=0, new_games=1))
        with self.assertRaisesRegex(bulk.ImportRejected, 'Captured formal schedule drift'):
            bounded.seal_bounded(self.campaign)

    def test_captured_formal_manifest_drift_rejected(self):
        path = self.make_formal_capture()
        manifest = bulk.read(path)
        manifest['plan']['stages']['screen']['seeds'] = [100]
        self.write(path, manifest)
        with self.assertRaisesRegex(bulk.ImportRejected, 'Frozen file drift'):
            bounded.seal_bounded(self.campaign)

    def test_cached_original_identity_and_import_ref_preserved(self):
        result_path, job = self.make_cache()
        bounded.seal_bounded(self.campaign)
        with patch.object(league, 'engine_sha', return_value='e'*64):
            planned, summary = bulk.prepare(self.store.db, [self.campaign])
            cached = next(x for x in planned if x['result']['import_provenance']['exact_cached_result'])
            self.assertEqual(cached['refs'][0]['contract'], job['contract_sha256'])
            self.assertEqual(cached['refs'][0]['match_id'], job['match_id'])
            self.assertEqual(cached['refs'][0]['result_sha256'], bulk.digest(result_path))
            bulk.apply_batch(self.store, planned, summary, self.receipt)
            _, again = bulk.prepare(self.store.db, [self.campaign])
            self.assertEqual(again['already_present'], 2)

    def test_missing_job_rejected_before_any_import(self):
        (self.campaign/'games'/(self.jobs[1]['match_id']+'.json')).unlink()
        with self.assertRaises(FileNotFoundError):
            bounded.seal_bounded(self.campaign)

    def test_loss_cannot_be_filtered_by_shortened_plan(self):
        self.plan['jobs'] = self.plan['jobs'][:1]
        self.freeze_plan()
        with self.assertRaisesRegex(bulk.ImportRejected, 'Incomplete'):
            bounded.seal_bounded(self.campaign)

    def test_source_and_frozen_plan_drift_rejected(self):
        bounded.seal_bounded(self.campaign)
        self.plan['workers'] = 4
        self.write(self.campaign/'plan.json', self.plan)
        with self.assertRaisesRegex(bulk.ImportRejected, 'Frozen file drift'):
            bounded.checked_bounded(self.campaign)

    def test_cache_wrong_condition_rejected_even_if_wrapper_is_updated(self):
        _, _ = self.make_cache()
        # Original cache is intact, but a schedule for a different seat cannot borrow it.
        job = self.jobs[1]
        job['candidate_seat'] = 0
        self.freeze_plan()
        with self.assertRaisesRegex(bulk.ImportRejected, 'Job ID drift'):
            bounded.seal_bounded(self.campaign)

    def test_result_drift_rejected_after_seal(self):
        bounded.seal_bounded(self.campaign)
        dest = self.campaign/'official'/(self.jobs[0]['match_id']+'.json')
        row = bulk.read(dest)
        row['action_hashes'][0] = 'a'*64
        self.write(dest, row)
        with self.assertRaisesRegex(bulk.ImportRejected, 'Official result/wrapper drift'):
            bounded.checked_bounded(self.campaign)

    def derive_from_bounded(self):
        bounded.seal_bounded(self.campaign)
        original_path = self.campaign
        original_jobs = copy.deepcopy(self.jobs)
        self.campaign = self.root/'derived'
        contract = dict(followup='explicit schedule')
        contract_sha = hashlib.sha256(json.dumps(contract, sort_keys=True).encode()).hexdigest()
        jobs, cached = [], {}
        for index, prior in enumerate(original_jobs):
            result_path = original_path/'official'/(prior['match_id']+'.json')
            wrapper = bulk.read(original_path/'games'/(prior['match_id']+'.json'))
            job = dict(prior, contract_sha256=contract_sha, stage='derived')
            del job['match_id']
            job['match_id'] = hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()[:24]
            if index == 0:
                wrapper['row']['job']['expected_action_hashes'] = wrapper['official']['action_hashes']
                cached[job['match_id']] = dict(official=str(result_path), row=copy.deepcopy(wrapper['row']),
                    hashes={str(result_path): bulk.digest(result_path)})
                wrapper.update(cached_from=str(result_path), original_match_id=prior['match_id'])
            else:
                wrapper['official'].update(match_id=job['match_id'], stage='derived', job_sha256=native.digest(job))
                self.write(self.campaign/'official'/(job['match_id']+'.json'), wrapper['official'])
            wrapper['job'] = job
            self.write(self.campaign/'games'/(job['match_id']+'.json'), wrapper)
            jobs.append(job)
        self.plan = dict(workers=8, contract=contract, jobs=jobs, cached=cached)
        self.freeze_plan()
        self.write(self.campaign/'completion-ready.json', dict(games=2, cached=1, new_games=1))
        return original_path, original_jobs

    def test_bounded_parent_cache_preserves_its_original_contract(self):
        original_path, original_jobs = self.derive_from_bounded()
        bounded.seal_bounded(self.campaign)
        manifest, rows = bounded.checked_bounded(self.campaign)
        original_id = original_jobs[0]['match_id']
        provenance = manifest['_row_provenance'][original_id]
        self.assertEqual(provenance['contract_sha256'], original_jobs[0]['contract_sha256'])
        self.assertEqual(Path(provenance['original_result_path']), original_path/'official'/(original_id+'.json'))
        with patch.object(league, 'engine_sha', return_value='e'*64):
            planned, summary = bulk.prepare(self.store.db, [original_path])
            bulk.apply_batch(self.store, planned, summary, self.receipt)
            _, derived = bulk.prepare(self.store.db, [self.campaign])
            self.assertEqual((derived['already_present'], derived['new_games']), (2, 0))

    def test_bounded_parent_drift_and_cycles_are_rejected(self):
        original_path, _ = self.derive_from_bounded()
        with self.assertRaisesRegex(bulk.ImportRejected, 'Cyclic'):
            bounded.collect(self.campaign, ancestors=(self.campaign.resolve(),))
        seal_path = original_path/'bounded-import.json'
        seal = bulk.read(seal_path)
        seal['games'] = 1
        self.write(seal_path, seal)
        with self.assertRaisesRegex(bulk.ImportRejected, 'Bounded seal drift'):
            bounded.seal_bounded(self.campaign)


if __name__ == '__main__':
    unittest.main()
