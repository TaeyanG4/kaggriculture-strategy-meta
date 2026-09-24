"""v2 evaluator with official DONE/overage timing; frozen v2 files stay unchanged.

Only local >1s timing counters become warnings after complete native execution.
Internal exception counters, source/seed identity, states/calls and engine timeouts
remain fatal. Candidate and opponent receive the same rule before results exist.
"""
from pathlib import Path
import sys
import validation_v2 as V

ORIGINAL_HEALTH = V.L.health_failures

def official_health(row):
    reasons = ORIGINAL_HEALTH(row)
    complete = (row.get('statuses') == ['DONE', 'DONE']
                and row.get('states') == 720 and row.get('errors') == [[], []]
                and row.get('seed') == row.get('resolved_seed')
                and all(row.get(role+'_timing', {}).get('calls') == 719
                        for role in ('candidate', 'opponent')))
    warnings = [r for r in reasons if complete and r in
                ('candidate_over_one_second', 'opponent_over_one_second')]
    if warnings:
        row['timing_warnings'] = warnings
    return [r for r in reasons if r not in warnings]

def install():
    # v2's orchestration, hashing, row checks and paired statistics are reused.
    # Worker subprocesses must enter this file to install the identical policy.
    V.L.health_failures = official_health
    wrapper = Path(__file__).resolve()
    if wrapper not in V.SUPPORT:
        V.SUPPORT += [wrapper, wrapper.with_name('run-validation-v3.ps1')]
    V.__file__ = str(wrapper)

if __name__ == '__main__':
    install()
    V.main()
