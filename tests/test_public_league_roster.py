"""Owner roster changes preserve evidence while preventing future matches."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tests import test_public_league as fixtures
from src.kaggriculture_meta import public_league as league


class RosterTests(unittest.TestCase):
    setUp = fixtures.PublicLeagueTests.setUp
    tearDown = fixtures.PublicLeagueTests.tearDown

    def upload(self, name):
        source = (fixtures.AGENT + '\n# ' + name).encode()
        with patch.object(league, 'qa_source', return_value={'ok': True, 'entrypoint': 'agent'}):
            return league.register_local_upload(self.store, name + '.py', source), source

    def test_retirement_preserves_evidence_and_survives_rerank_and_upload(self):
        uploads = [self.upload(n) for n in ('a', 'b', 'c')]
        a, b, c = [u[0]['agent_id'] for u in uploads]
        now = league.utcnow()
        with self.store.db:
            for i in range(8):
                self.store.db.execute('''INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,outcome_a,created_at,completed_at)
                  VALUES(?,?,?,?,?,0,'complete',1,?,?)''', (str(i), 'e', a, b, i, now, now))
        league.update_rankings(self.store, top_k=1)
        before = [dict(r) for r in self.store.db.execute('SELECT * FROM agents ORDER BY id')]
        matches = [dict(r) for r in self.store.db.execute('SELECT * FROM matches ORDER BY id')]
        league.retire_local_agents(self.store, [a], 'Owner cleanup')
        league.update_rankings(self.store, top_k=1)
        after = [dict(r) for r in self.store.db.execute('SELECT * FROM agents ORDER BY id')]
        for old, new in zip(before, after):
            for field in ('sha256', 'source_path', 'qa_status', 'games', 'wins', 'losses', 'ties', 'rating'):
                self.assertEqual(old[field], new[field], field)
            self.assertTrue(Path(new['source_path']).exists())
        self.assertEqual(after[0]['status'], 'retired')
        self.assertEqual(after[1]['status'], 'active')
        self.assertEqual(matches, [dict(r) for r in self.store.db.execute('SELECT * FROM matches ORDER BY id')])
        repeat = league.register_local_upload(self.store, 'a.py', uploads[0][1])
        self.assertEqual((repeat['agent_id'], repeat['status'], repeat['games']), (a, 'retired', 8))
        with patch.object(league, 'engine_sha', return_value='engine'):
            jobs = league.schedule_matches(self.store, max_matches=4)
            self.assertTrue(jobs)
            self.assertNotIn(a, {j[k] for j in jobs for k in ('agent_a', 'agent_b')})
            with self.assertRaisesRegex(ValueError, 'not eligible'):
                league.schedule_matches(self.store, focus_agent_id=a)
        controller = league.BattleController(self.store.state)
        with self.assertRaises(ValueError):
            controller.focus(a)
        self.assertIsNone(controller.thread)
        snapshot = league.dashboard_snapshot(self.store)
        self.assertEqual(snapshot['summary']['retired'], 1)
        self.assertEqual(snapshot['summary']['active_capacity'], 120)
        with self.store.db:
            for i in range(2):
                self.store.db.execute('''INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,result_json,created_at)
                  VALUES(?,?,?,?,?,0,'invalid',?,?)''',
                  ('old-failure' + str(i), 'e', a, b, i,
                   json.dumps({'errors': [[{'type': 'RuntimeError'}], []]}), now))
        self.assertEqual(league.quarantine_runtime_failures(self.store)['quarantined'], 0)
        self.assertEqual(self.store.db.execute('SELECT status FROM agents WHERE id=?', (a,)).fetchone()[0], 'retired')

    def test_invalid_id_does_not_partially_retire(self):
        row, _ = self.upload('a')
        with self.assertRaises(ValueError):
            league.retire_local_agents(self.store, [row['agent_id'], 9999], 'Owner cleanup')
        self.assertEqual(self.store.get_meta('retired_local_agents', {}), {})
        self.assertEqual(self.store.db.execute('SELECT status FROM agents').fetchone()[0], 'candidate')


if __name__ == '__main__':
    unittest.main()
