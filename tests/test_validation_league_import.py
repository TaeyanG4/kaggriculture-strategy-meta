import copy
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from src.kaggriculture_meta import public_league as league
from tools import import_validation_league as bulk


def add_fixture_alias(store, ident):
    store.db.execute('''INSERT INTO notebooks(id,ref,title,author,slug,url,origin,first_seen,last_seen)
        VALUES(?,?,?,'fixture',?,'','local','2026-09-27','2026-09-27')''',
        (ident,f'fixture/{ident}',f'fixture{ident}',str(ident)))
    store.db.execute('''INSERT INTO notebook_versions(id,notebook_id,version_key,metadata_json,first_seen)
        VALUES(?,?,'fixture','{}','2026-09-27')''',(ident,ident))
    store.db.execute('''INSERT INTO aliases(agent_id,version_id,notebook_title,notebook_url,author,ref,discovered_at)
        VALUES(?,?,'fixture','','fixture',?,'2026-09-27')''',(ident,ident,f'fixture/{ident}'))


class ValidationImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = league.Store(self.root / 'league')
        self.agents = []
        for i in range(2):
            source = self.root / f'agent{i}.py'
            source.write_bytes(f'# fixture {i}\ndef agent(obs): return {{}}\n'.encode())
            sha = bulk.digest(source)
            self.store.db.execute('''INSERT INTO agents(id,sha256,source_sha256,source_path,artifact_files_json,
                execution_platform,qa_status,created_at) VALUES(?,?,?,?,?,'host','pass','2026-09-27')''',
                (i+1, sha, sha, str(source), '["main.py"]'))
            add_fixture_alias(self.store,i+1)
            self.agents.append(dict(self.store.db.execute('SELECT * FROM agents WHERE id=?', (i+1,)).fetchone()))
        self.store.db.commit()
        self.campaign = self.root / 'campaign'
        self.campaign.mkdir()
        self.manifest = dict(stage='confirm', contract_sha256='f'*64, expected_jobs=2,
            plan=dict(workers=8,models={'c':self.ref(0)},opponents={'o':self.ref(1)}), jobs=[])
        self.rows = []
        for seat in (0,1):
            name = f'm{seat}'
            self.manifest['jobs'].append(dict(match_id=name, candidate=dict(self.ref(0),name='c'),opponent=dict(self.ref(1),name='o')))
            row = dict(match_id=name, mode='native_reacting', stage='confirm', seed=99, resolved_seed=99,
                candidate_seat=seat,candidate_sha256=self.ref(0)['sha256'],opponent_sha256=self.ref(1)['sha256'],
                valid=True,statuses=['DONE','DONE'],states=720,errors=[[],[]],health_failures=[],
                rewards=[12,8] if seat==0 else [8,12],margin=4,outcome='win',seconds=1.5,
                candidate_timing=dict(calls=719,max=2),opponent_timing=dict(calls=719,max=.2),
                candidate_telemetry=dict(who='c'),opponent_telemetry=dict(who='o'),
                action_hashes=[hashlib.sha256(f'{seat}|{p}'.encode()).hexdigest() for p in (0,1)],
                checkpoints=[dict(step=24)],shops=['BAKERY'])
            self.rows.append(row)
            dest = self.campaign/'jobs'/name/'result.json'
            dest.parent.mkdir(parents=True)
            dest.write_text(json.dumps(row), 'utf8')
        (self.campaign/'manifest.json').write_text(json.dumps(self.manifest), 'utf8')
        (self.campaign/'results.json').write_text(json.dumps(dict(status='complete')), 'utf8')
        self.receipt = self.root/'receipt.json'

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def ref(self, index):
        a = self.agents[index]
        return dict(path=a['source_path'],sha256=a['source_sha256'])

    def prepare(self):
        with patch.object(league, 'engine_sha', return_value='e'*64):
            return bulk.prepare(self.store.db,[self.campaign],loader=lambda _: (self.manifest,self.rows))

    def test_canonical_swap_keeps_seat_rewards_and_action_hashes(self):
        high, low = sorted(self.agents,key=lambda a:a['sha256'],reverse=True)
        row = copy.deepcopy(self.rows[1])
        row.update(candidate_sha256=high['source_sha256'],opponent_sha256=low['source_sha256'],
                   public_league_warnings=['candidate_over_one_second'])
        p = bulk.converted(row,high,low,'e'*64,{})
        self.assertEqual(p['a'],low['id'])
        self.assertEqual(p['seat_a'],0)
        self.assertEqual(p['score'],0)
        self.assertEqual(p['result']['action_hashes'],row['action_hashes'])
        self.assertEqual(p['result']['candidate_telemetry'],dict(who='o'))
        self.assertEqual(p['result']['public_league_warnings'],['opponent_over_one_second'])
        self.assertEqual(p['result']['import_provenance']['original_candidate_checkpoints'],row['checkpoints'])

    def test_bulk_idempotency_ratings_and_retired_status(self):
        self.store.set_meta('retired_local_agents',{'1':dict(reason='fixture')})
        planned, summary = self.prepare()
        with patch.object(league,'update_rankings',wraps=league.update_rankings) as ranking:
            bulk.apply_batch(self.store,planned,summary,self.receipt)
            planned, summary = self.prepare()
            self.assertEqual(summary['already_present'],2)
            bulk.apply_batch(self.store,planned,summary,self.receipt)
            self.assertEqual(ranking.call_count,1)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM matches').fetchone()[0],2)
        a = dict(self.store.db.execute('SELECT * FROM agents WHERE id=1').fetchone())
        self.assertEqual((a['games'],a['wins'],a['status']),(2,2,'retired'))
        self.assertGreater(a['rating'],1500)

    def test_restart_after_rows_commit_before_rating(self):
        planned, summary = self.prepare()
        with patch.object(league,'update_rankings',side_effect=RuntimeError('interrupted')):
            with self.assertRaises(RuntimeError):bulk.apply_batch(self.store,planned,summary,self.receipt)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM matches').fetchone()[0],2)
        planned, summary = self.prepare()
        self.assertEqual(summary['new_games'],0)
        bulk.apply_batch(self.store,planned,summary,self.receipt)
        self.assertEqual(self.store.db.execute('SELECT games FROM agents WHERE id=1').fetchone()[0],2)

    def test_wrapper_update_does_not_duplicate_historical_import(self):
        planned, summary = self.prepare()
        bulk.apply_batch(self.store,planned,summary,self.receipt)
        with patch.object(league, 'engine_sha', return_value='d'*64):
            planned, summary = bulk.prepare(self.store.db,[self.campaign],loader=lambda _: (self.manifest,self.rows))
        self.assertEqual((summary['already_present'],summary['new_games']),(2,0))
        bulk.apply_batch(self.store,planned,summary,self.receipt)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM matches').fetchone()[0],2)

    def test_unregistered_source_blocks_all_writes(self):
        self.store.db.execute('DELETE FROM aliases WHERE agent_id=2')
        self.store.db.execute('DELETE FROM agents WHERE id=2');self.store.db.commit()
        planned, summary = self.prepare()
        self.assertFalse(summary['ready'])
        with self.assertRaises(bulk.ImportRejected):bulk.apply_batch(self.store,planned,summary,self.receipt)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM matches').fetchone()[0],0)

    def test_cli_rejection_does_not_open_writable_store(self):
        with patch.object(bulk.sys,'argv',['import','apply',str(self.campaign),'--state',str(self.store.state)]),\
             patch.object(bulk,'prepare_readonly',return_value=([],{'ready':False})),\
             patch.object(league,'Store') as writable:
            with self.assertRaises(bulk.ImportRejected):bulk.main()
            writable.assert_not_called()

    def test_conflicting_duplicate_is_rejected(self):
        planned, summary = self.prepare();bulk.apply_batch(self.store,planned,summary,self.receipt)
        self.rows[0]['action_hashes'][0] = 'a'*64
        with self.assertRaisesRegex(bulk.ImportRejected,'Existing result conflict'):self.prepare()

    def test_nonrating_games_cannot_pass(self):
        for change in [dict(mode='frozen_replay'),dict(states=719),dict(rewards=[float('nan'),8]),
                       dict(errors=[['exception'],[]]),dict(health_failures=['candidate_timeout']),dict(resolved_seed=100)]:
            with self.subTest(change=change),self.assertRaises(bulk.ImportRejected):
                bulk.validate_result(dict(self.rows[0],**change))

    def test_runtime_sidecar_rejected(self):
        self.store.db.execute('UPDATE agents SET artifact_files_json=? WHERE id=2', ('["main.py","data.json"]',))
        with self.assertRaisesRegex(bulk.ImportRejected,'Runtime sidecars'):self.prepare()

    def crlf_validation_copy(self, extra=b''):
        raw = Path(self.agents[0]['source_path']).read_bytes().replace(b'\n', b'\r\n') + extra
        path = self.root / 'validated-crlf.py'; path.write_bytes(raw)
        ref = dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest())
        self.manifest['plan']['models']['c'] = ref
        for job, row in zip(self.manifest['jobs'], self.rows):
            job['candidate'].update(ref); row['candidate_sha256'] = ref['sha256']
        return ref

    def test_upload_newline_normalization_is_proven_and_idempotent(self):
        ref = self.crlf_validation_copy()
        planned, summary = self.prepare()
        self.assertTrue(summary['ready'])
        proof = planned[0]['result']['import_provenance']['source_identity_transforms']['candidate']
        self.assertEqual(proof['validation_sha256'], ref['sha256'])
        self.assertEqual(proof['league_sha256'], self.agents[0]['source_sha256'])
        self.assertTrue(proof['compiled_code_equal'])
        bulk.apply_batch(self.store, planned, summary, self.receipt)
        _, again = self.prepare()
        self.assertEqual((again['new_games'], again['already_present']), (0, 2))

    def test_newline_fallback_does_not_merge_other_edits(self):
        self.crlf_validation_copy(extra=b'# an additional source edit\r\n')
        _, summary = self.prepare()
        self.assertFalse(summary['ready'])
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM matches').fetchone()[0], 0)

    def test_newline_fallback_rejects_registered_source_drift(self):
        self.crlf_validation_copy()
        Path(self.agents[0]['source_path']).write_bytes(b'# changed after registration\n')
        with self.assertRaisesRegex(bulk.ImportRejected, 'source drift'):self.prepare()

    def test_incomplete_campaign_stops_before_loading_outcomes(self):
        (self.campaign/'results.json').write_text('{"status":"running"}', 'utf8')
        with self.assertRaisesRegex(bulk.ImportRejected,'unfinished'):bulk.checked_campaign(self.campaign)

    def test_self_games_do_not_count_twice(self):
        self.manifest['plan']['opponents']['o'] = self.ref(0)
        for job,row in zip(self.manifest['jobs'],self.rows):
            job['opponent'] = dict(self.ref(0),name='o');row['opponent_sha256'] = self.ref(0)['sha256']
        planned,summary=self.prepare()
        self.assertEqual((len(planned),summary['self_games_excluded']),(0,2))

    def test_512_plus_1024_batch_updates_ratings_once(self):
        manifests={}
        for stage,count,start in [('screen',512,1000),('confirm',1024,2000)]:
            path=self.root/stage;path.mkdir()
            manifest=copy.deepcopy(self.manifest)
            manifest.update(stage=stage,expected_jobs=count,contract_sha256=hashlib.sha256(stage.encode()).hexdigest(),jobs=[])
            rows=[]
            for i in range(count):
                name=f'{stage}{i}';job=copy.deepcopy(self.manifest['jobs'][i%2]);job['match_id']=name
                row=copy.deepcopy(self.rows[i%2]);row.update(match_id=name,stage=stage,seed=start+i//2,resolved_seed=start+i//2)
                manifest['jobs'].append(job);rows.append(row)
                dest=path/'jobs'/name/'result.json';dest.parent.mkdir(parents=True)
                dest.write_text(json.dumps(row),'utf8')
            (path/'manifest.json').write_text(json.dumps(manifest),'utf8')
            (path/'results.json').write_text('{"status":"complete"}','utf8')
            manifests[path.resolve()]=(manifest,rows)
        with patch.object(league,'engine_sha',return_value='e'*64),patch.object(league,'update_rankings',wraps=league.update_rankings) as fit:
            planned,summary=bulk.prepare(self.store.db,list(manifests),loader=manifests.__getitem__)
            self.assertEqual((summary['input_games'],summary['new_games']),(1536,1536))
            bulk.apply_batch(self.store,planned,summary,self.receipt)
            planned,summary=bulk.prepare(self.store.db,list(manifests),loader=manifests.__getitem__)
            bulk.apply_batch(self.store,planned,summary,self.receipt)
            self.assertEqual((fit.call_count,summary['already_present'],summary['new_games']),(1,1536,0))
        self.assertEqual(self.store.db.execute('SELECT games FROM agents WHERE id=1').fetchone()[0],1536)


@unittest.skipUnless(os.getenv('VALIDATION_IMPORT_INTEGRATION_CAMPAIGN'), 'Optional real-cache integration')
class RealCampaignImportTests(unittest.TestCase):
    def test_completed_cache_into_isolated_database(self):
        """No games or live writes; unregistered candidates are test fixtures only."""
        campaign = Path(os.environ['VALIDATION_IMPORT_INTEGRATION_CAMPAIGN']).resolve()
        manifest, rows = bulk.checked_campaign(campaign)
        refs = {r['sha256']:r for group in ('models','opponents') for r in manifest['plan'][group].values()}
        live = sqlite3.connect((league.DEFAULT_STATE/'league.sqlite3').resolve().as_uri()+'?mode=ro',uri=True)
        live.row_factory = sqlite3.Row
        with tempfile.TemporaryDirectory() as temporary:
            store = league.Store(Path(temporary)/'league')
            try:
                for sha,ref in refs.items():
                    matches = [dict(r) for r in live.execute('SELECT * FROM agents WHERE source_sha256=?',(sha,))]
                    exact = [r for r in matches if bulk.path_key(r['source_path'])==bulk.path_key(ref['path'])]
                    if exact:matches=exact
                    self.assertLessEqual(len(matches),1)
                    a = matches[0] if matches else dict(source_path=str(bulk.ROOT/ref['path']),source_sha256=sha,
                        sha256=league.artifact_digest({'main.py':(bulk.ROOT/ref['path']).read_bytes()}),
                        artifact_files_json='["main.py"]',execution_platform='host')
                    ident=store.db.execute('''INSERT INTO agents(sha256,source_sha256,source_path,artifact_files_json,
                        execution_platform,qa_status,created_at) VALUES(?,?,?,?,?,'pass','fixture')''',
                        tuple(a[k] for k in ('sha256','source_sha256','source_path','artifact_files_json','execution_platform'))).lastrowid
                    add_fixture_alias(store,ident)
                store.db.commit()
                planned,summary=bulk.prepare(store.db,[campaign])
                self.assertTrue(summary['ready'])
                self.assertEqual(summary['input_games'],len(rows))
                receipt=Path(temporary)/'receipt.json'
                with patch.object(league,'update_rankings',wraps=league.update_rankings) as fit:
                    first=bulk.apply_batch(store,planned,summary,receipt)
                    planned,again=bulk.prepare(store.db,[campaign])
                    second=bulk.apply_batch(store,planned,again,receipt)
                    self.assertEqual((fit.call_count,second['imported_new']),(1,0))
                from tools.league_agent_audit import audit
                audits=[]
                for ident in first['agents']:
                    result=audit(store.db_path,int(ident),expected=first['agents'][ident]['games'])
                    self.assertTrue(result['valid_integrity'],result['problems'])
                    audits.append(dict(agent=int(ident),games=result['games'],integrity=True))
                report=dict(live_database_modified=False,engine_games_run=0,fixture_registration_only=True,
                    input_games=len(rows),imported_games=first['imported_new'],
                    self_games_excluded=summary['self_games_excluded'],retry_imported=second['imported_new'],
                    rating_passes=1,audits=audits)
                if os.getenv('VALIDATION_IMPORT_REPORT'):
                    bulk.atomic_json(os.environ['VALIDATION_IMPORT_REPORT'],report)
                print(json.dumps({k:v for k,v in report.items() if k!='audits'}))
            finally:
                store.close();live.close()


if __name__ == '__main__':
    unittest.main()
