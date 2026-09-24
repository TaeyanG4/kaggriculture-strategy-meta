"""Official overage validity must not revive execution/identity failures."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import validation_v3 as V3

def row():
    return dict(statuses=['DONE','DONE'],states=720,errors=[[],[]],seed=17,resolved_seed=17,
      candidate_timing=dict(calls=719,over_1s=1),opponent_timing=dict(calls=719,over_1s=0),
      candidate_telemetry={},opponent_telemetry={})

class TimingTests(unittest.TestCase):
    def test_done_overage_is_warning_for_either_seat(self):
        for role in ('candidate','opponent'):
            r=row();r['candidate_timing']['over_1s']=0;r[role+'_timing']['over_1s']=1
            assert V3.official_health(r)==[]
            assert r['timing_warnings']==[role+'_over_one_second']

    def test_real_failure_or_incomplete_identity_keeps_rejection(self):
        for key,value in [('statuses',['TIMEOUT','DONE']),('states',719),('errors',[[{'step':0}],[]]),('resolved_seed',18)]:
            r=row();r[key]=value;assert V3.official_health(r)==['candidate_over_one_second']
        r=row();r['candidate_timing']['calls']=718;assert V3.official_health(r)

    def test_hidden_code_error_stays_fatal_despite_done(self):
        r=row();r['opponent_telemetry']={'controller':{'errors':1}}
        assert V3.official_health(r)==['opponent_internal_error:controller.errors']

    def test_old_health_contract_stays_strict_without_install(self):
        assert V3.ORIGINAL_HEALTH(row())==['candidate_over_one_second']


if __name__=="__main__":unittest.main()
