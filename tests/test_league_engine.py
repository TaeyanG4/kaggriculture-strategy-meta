"""Explicit integration gate: set LEAGUE_ENGINE_TESTS=1; uses the pinned local engine."""
import json
import os
from pathlib import Path
import tempfile
import unittest

from src.kaggriculture_meta.league import prepare, run_jobs


@unittest.skipUnless(os.environ.get('LEAGUE_ENGINE_TESTS') == '1', 'explicit engine integration gate')
class LeagueEngineTests(unittest.TestCase):
    def test_official_loader_private_observations_isolated_globals_and_resume(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            root = Path(tmp)
            source = root / 'policy.py'
            source.write_text('''calls=0
def agent(obs,config):
    global calls
    assert config.get('seed') is None and 'seed' not in obs
    assert calls == obs['step']
    assert all('private' not in farm for farm in obs['farms'])
    calls += 1
    player=obs['player']
    if calls == 2:
        assert obs['private']['seeds']['CARROT'] == player+1
    return {'farmer':['PASS'],'hands':[], 'market':[['BUY_SEED','CARROT',player+1]] if calls==1 else []}
''', encoding='utf-8')
            plan = {'splits': {'train': [71923], 'selection': [71924], 'holdout': [71925]},
                    'allow_mirror': True, 'opponents': [{'name': 'self', 'path': str(source), 'family': 'fixture'}]}
            identity, jobs = prepare(plan, source, 'train', root/'run')
            result = run_jobs(identity, jobs, root/'run', workers=2)
            self.assertEqual(result['native_reacting']['overall']['valid_games'], 2)
            self.assertEqual(run_jobs(identity, jobs, root/'run', workers=2), result)
            rows = (root/'run/matches.jsonl').read_text(encoding='utf-8').splitlines()
            self.assertEqual(len(rows), 2)
            for text in rows:
                row = json.loads(text)
                self.assertEqual(row['candidate_timing']['calls'], 719)
                self.assertEqual(row['resolved_seed'], 71923)
            source.write_text(source.read_text(encoding='utf-8')+'\n# changed\n', encoding='utf-8')
            new_identity, new_jobs = prepare(plan, source, 'train', root/'run')
            with self.assertRaisesRegex(ValueError, 'Resume refused'):
                run_jobs(new_identity, new_jobs, root/'run')

    def test_infinite_policy_is_killed_and_is_not_a_win(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            root = Path(tmp)
            source = root/'infinite.py'
            source.write_text('def agent(obs,config):\n    while True: pass\n', encoding='utf-8')
            plan = {'splits': {'train': [1], 'selection': [2], 'holdout': [3]},
                    'allow_mirror': True, 'opponents': [{'name': 'infinite', 'path': str(source), 'family': 'fixture'}]}
            identity, jobs = prepare(plan, source, 'train', root/'run')
            result = run_jobs(identity, jobs[:1], root/'run', workers=1, timeout=5)
            self.assertEqual(result['native_reacting']['overall']['failures'], 1)
            self.assertEqual(result['native_reacting']['overall']['wins'], 0)
            row=json.loads((root/'run/matches.jsonl').read_text(encoding='utf-8'))
            self.assertEqual(row['error'], 'wall_timeout')


if __name__ == '__main__':
    unittest.main()
