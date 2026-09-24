"""Opponent filters preserve source aliases and the local measurement target."""
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from tests import test_public_league as fixtures
from src.kaggriculture_meta import public_league as league


class PublicOnlyTests(unittest.TestCase):
    setUp = fixtures.PublicLeagueTests.setUp
    tearDown = fixtures.PublicLeagueTests.tearDown
    add_version = fixtures.PublicLeagueTests.add_version
    notebook = fixtures.PublicLeagueTests.notebook

    def add(self, name, public=False, source=None):
        source = source or fixtures.AGENT + '\n# ' + name + '\n'
        with patch.object(league, 'qa_source', return_value={'ok': True, 'entrypoint': 'agent'}):
            if not public:
                return league.register_local_upload(self.store, name + '.py', source.encode())['agent_id']
            folder = self.root / name
            self.notebook(folder, source)
            version = self.add_version('author/' + name, name, folder)
            with patch.object(league, 'ensure_notebook_outputs', return_value={'downloaded': [], 'failed': []}):
                league.extract(self.store)
            return self.store.db.execute('SELECT agent_id FROM aliases WHERE version_id=?', (version,)).fetchone()[0]

    def test_filters_target_alias_and_default(self):
        target, local = self.add('target'), self.add('local')
        public = self.add('public', public=True)
        alias = self.add('alias', public=True, source=fixtures.AGENT + '\n# local\n')
        self.assertEqual(alias, local)
        private = self.add('private')
        with patch.object(league, 'engine_sha', return_value='engine'):
            ordinary = league.schedule_matches(self.store, max_matches=16, public_only=True)
            self.assertTrue(ordinary)
            self.assertEqual({j[k] for j in ordinary for k in ('agent_a','agent_b')}, {public, alias})
            focused = league.schedule_matches(self.store, max_matches=12, focus_agent_id=target, public_only=True)
            self.assertEqual({j[k] for j in focused for k in ('agent_a','agent_b')}, {target, public, alias})
            self.assertTrue(all(target in (j['agent_a'], j['agent_b']) for j in focused))
            default = league.schedule_matches(self.store, max_matches=16)
            self.assertIn(private, {j[k] for j in default for k in ('agent_a','agent_b')})
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM matches').fetchone()[0], 0)

    def test_settings_independent_persist_and_validate(self):
        with patch.object(league.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as run:
            settings = league.update_runtime_settings(self.store, 3, 8, True, False)
            self.assertTrue(settings['battle_public_only'])
            self.assertFalse(settings['focus_public_only'])
            settings = league.update_runtime_settings(self.store, 3, 8, focus_public_only=True)
            self.assertTrue(settings['battle_public_only'])
            self.assertTrue(settings['focus_public_only'])
            with self.assertRaises(ValueError):
                league.update_runtime_settings(self.store, 3, 8, 'false')
            self.assertEqual(run.call_count, 2)
        reopened = league.Store(self.store.state)
        try:
            self.assertEqual(league.runtime_settings(reopened), settings)
        finally:
            reopened.close()

    def test_mode_specific_setting_reaches_runner(self):
        self.store.set_meta('runtime_settings', {'battle_public_only': True, 'focus_public_only': False})
        with patch.object(league, '_run_league_unlocked', return_value={}) as run:
            league.run_league(self.store)
            self.assertTrue(run.call_args.args[-1])
            league.run_league(self.store, focus_agent_id=99)
            self.assertFalse(run.call_args.args[-1])

    def test_no_public_opponents_produces_no_games(self):
        target = self.add('only-local')
        self.assertEqual(league.schedule_matches(self.store, focus_agent_id=target, public_only=True), [])
        self.assertEqual(league.schedule_matches(self.store, public_only=True), [])


if __name__ == '__main__':
    unittest.main()
