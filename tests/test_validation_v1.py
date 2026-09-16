"""Contract tests with synthetic rows and fake processes; never run Kaggle games."""
import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import validation_v1 as V
import validation_stats_v1 as S

def config():
    return dict(schema=1,workers=2,timeout_seconds=180,engine={'test':1},configuration={'episodeSteps':720},
        models={'a':{'path':'a.py','sha256':'a'*64},'b':{'path':'b.py','sha256':'b'*64}},
        opponents={'x':{'path':'x.py','sha256':'c'*64,'family':'one'},'y':{'path':'y.py','sha256':'d'*64,'family':'two'}},
        comparisons=[dict(candidate='b',parent='a',primary=True)],
        stages={s:{'seeds':[2*i,2*i+1],'alpha':alpha} for i,(s,alpha) in enumerate([('screen',.01),('confirm',.015),('final',.025)])})

def records(p):
    rows=[]
    for c in p['models']:
        for seed in p['stages']['screen']['seeds']:
            for o in p['opponents']:
                for seat in (0,1):
                    margin=10 if c=='b' and seed%2 else 0
                    rewards=[100,100]; rewards[seat]+=margin
                    rows.append(dict(model=c,seed=seed,opponent_name=o,opponent_family=p['opponents'][o]['family'],
                        candidate_seat=seat,margin=margin,rewards=rewards,outcome='win' if margin else 'tie',
                        valid=True,action_hashes=[c,c],candidate_telemetry={}))
    return rows

class ValidationTests(unittest.TestCase):
    def test_stage_leakage_and_alias_rejected(self):
        p=config(); V.validate_config(p)
        p['stages']['final']['seeds']=[0,8]
        with self.assertRaises(ValueError): V.validate_config(p)
        p=config(); p['opponents']['y']['sha256']=p['opponents']['x']['sha256']
        with self.assertRaises(ValueError): V.validate_config(p)

    def test_paired_coverage_and_constant_uncertainty(self):
        p=config(); rows=records(p); result=S.analyze(p,'screen',rows)
        r=result['comparisons']['b_vs_a']
        self.assertEqual(r['family_weighted_point_delta'],.25)
        self.assertEqual(r['seed_clusters'],2)
        self.assertFalse(result['promotion'])
        with self.assertRaises(ValueError): S.analyze(p,'screen',rows[:-1])
        with self.assertRaises(ValueError): S.analyze(p,'screen',rows+[rows[0]])
        self.assertIsNone(S.interval([0]*48,.025))

    def test_family_weighting_resists_alias_count(self):
        p=config(); rows=records(p)
        # Duplicate one family using a distinct hypothetical implementation.
        p['opponents']['z']={'path':'z.py','sha256':'e'*64,'family':'one'}
        rows += [dict(r,opponent_name='z') for r in rows if r['opponent_name']=='x']
        a=S.analyze(p,'screen',rows)['comparisons']['b_vs_a']
        self.assertEqual(a['family_weighted_point_delta'],.25)

    def test_cache_identity(self):
        j={'match_id':'id','seed':3,'candidate_seat':0,'stage':'screen',
           'candidate':{'name':'a','sha256':'a'},'opponent':{'name':'x','family':'f','sha256':'b'}}
        r=dict(job_sha256=V.L.digest(j),match_id='id',seed=3,resolved_seed=3,candidate_seat=0,
            candidate_sha256='a',opponent_sha256='b',opponent_name='x',opponent_family='f',model='a',
            mode='native_reacting',stage='screen',states=720,statuses=['DONE','DONE'],errors=[[],[]],
            rewards=[1,0],margin=1,outcome='win',valid=True,candidate_timing={'calls':719},
            opponent_timing={'calls':719},candidate_telemetry={},opponent_telemetry={})
        V.validate_row(j,r)
        for key,val in [('resolved_seed',4),('margin',2),('job_sha256','bad')]:
            bad=dict(r); bad[key]=val
            with self.assertRaises(ValueError): V.validate_row(j,bad)

    def test_temp_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=Path(tmp)/'a'; b=Path(tmp)/'b'; a.mkdir(); b.mkdir()
            x,y=V.child_environment(a),V.child_environment(b)
            self.assertNotEqual(x['TEMP'],y['TEMP'])
            self.assertEqual(x['PYTHONHASHSEED'],y['PYTHONHASHSEED'])

    def test_cached_run_does_not_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            m={'jobs':[{'match_id':'a'}],'expected_jobs':1,'plan':{'workers':2}}
            with patch.object(V,'check',return_value=m),patch.object(V,'load_rows',return_value=[{'match_id':'a'}]),patch.object(V,'report',return_value='ok'),patch.object(V.subprocess,'Popen') as launch,patch.dict(V.os.environ,{'KAGGRICULTURE_VALIDATION_GUARDED':'1'}):
                self.assertEqual(V.run(Path(tmp)),'ok'); launch.assert_not_called()

    def test_each_job_gets_new_process(self):
        class Fake:
            returncode=0
            def poll(self): return 0
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            jobs=[{'match_id':str(i)} for i in range(5)]
            m={'jobs':jobs,'expected_jobs':5,'plan':{'workers':2,'timeout_seconds':180}}
            def launch(command,**kwargs):
                jp=Path(command[-1]); j=V.read(jp)
                V.L.write_json(jp.parent/'result.json',{'match_id':j['match_id']})
                return Fake()
            with patch.object(V,'check',return_value=m),patch.object(V,'load_rows',return_value=[]),patch.object(V,'validate_row'),patch.object(V,'report',return_value='ok'),patch.object(V.subprocess,'Popen',side_effect=launch) as spawn,patch.dict(V.os.environ,{'KAGGRICULTURE_VALIDATION_GUARDED':'1'}):
                self.assertEqual(V.run(out),'ok')
                self.assertEqual(spawn.call_count,5)
                self.assertEqual(len({str(c.kwargs['cwd']) for c in spawn.call_args_list}),5)

    def test_failure_cleans_owned_workers(self):
        class Fake:
            returncode=1
            def __init__(self,finished): self.finished=finished
            def poll(self): return 1 if self.finished else None
        with tempfile.TemporaryDirectory() as tmp:
            m={'jobs':[{'match_id':'a'},{'match_id':'b'}],'expected_jobs':2,'plan':{'workers':2,'timeout_seconds':180}}
            running=Fake(False)
            with patch.object(V,'check',return_value=m),patch.object(V,'load_rows',return_value=[]),patch.object(V.subprocess,'Popen',side_effect=[Fake(True),running]),patch.object(V,'stop_owned') as stop,patch.dict(V.os.environ,{'KAGGRICULTURE_VALIDATION_GUARDED':'1'}):
                with self.assertRaises(ValueError): V.run(Path(tmp))
                stop.assert_called_once_with(running)

    def test_manifest_drift(self):
        # Exercise real prepare/check in an isolated workspace with fake engine identity.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); p=config()
            for group in ('models','opponents'):
                for name,ref in p[group].items():
                    file=root/ref['path']; file.write_text('value='+repr(name)+'\n')
                    ref['sha256']=V.L.digest(file.read_bytes())
            support=root/'support.py'; support.write_text('# runner v1\n')
            cfg=root/'config.json'; V.L.write_json(cfg,p); out=root/'out'
            with patch.object(V,'ROOT',root),patch.object(V.L,'ROOT',root),patch.object(V,'SUPPORT',[support]),patch.object(V.L,'engine_identity',return_value=p['engine']):
                m=V.prepare(cfg,'screen',out); self.assertEqual(m['expected_jobs'],16)
                V.check(out)
                frozen=Path(m['models']['a']['path']); frozen.write_text('tampered')
                with self.assertRaises(ValueError): V.check(out)

if __name__=='__main__': unittest.main()
