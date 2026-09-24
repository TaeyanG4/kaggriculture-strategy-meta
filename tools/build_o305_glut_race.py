"""Add a late-game glut race to frozen o302: from a given day, let the chassis lead-sell planned lots
one turn early even when the book is glutted (the v9 RACEPX layer blocks that lead below base price)."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '2cdb9e5d14f72043631eb4b9c287fe2e5fb58a6375aeab90e3a8a36a7df87b34'
WRAPPER = r'''

# o305: late-game glut race. Exact ledgers of eight deterministic local losses
# against V54-family tapes show identical production and identical units sold;
# the whole margin (-371..-2026) is realised price on late lots (d22-28) where the
# rival sells the same lot one turn before ours (d28 strawberries: rival h14 at
# $70, ours h15 at $32). The v9 RACEPX layer blocks the one-turn lead sale while
# a book is below base price, so glutted late lots keep the tape's later slot.
# From __DAY__ on, lift that block (RACEPX margin -> very negative) so the
# chassis' own sell_lead runs on glutted books too; nothing else changes.
_O305_ENABLED = __ON__
_O305_PARENT = agent
_O305_FROM_DAY = __DAY__
_O305_NS = _C365_CA_NS
_O305_ORIGINAL_MARGIN = _O305_NS['V9_RACEPX_MARGIN']
_O305_REPORT = {}

def agent(observation, configuration=None):
    step = int(observation['step']); day = step // 24
    if step == 0:
        _O305_REPORT.clear(); _O305_REPORT.update(glut_race_days=0)
        _O305_NS['V9_RACEPX_MARGIN'] = _O305_ORIGINAL_MARGIN
    if _O305_ENABLED and day >= _O305_FROM_DAY:
        if _O305_NS['V9_RACEPX_MARGIN'] == _O305_ORIGINAL_MARGIN:
            _O305_REPORT['glut_race_days'] += 1
        _O305_NS['V9_RACEPX_MARGIN'] = -10 ** 6
    else:
        _O305_NS['V9_RACEPX_MARGIN'] = _O305_ORIGINAL_MARGIN
    action = _O305_PARENT(observation, configuration)
    _O305_REPORT.update(_O302_REPORT)
    return action

agent.telemetry = _O305_REPORT
kaggle_submission_agent = agent
o305_submission_agent = agent
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    ap.add_argument('--from-day', type=int, default=20)
    args = ap.parse_args()
    parent = (ROOT / 'agent/o302_farmer_feed_topup.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    data = parent.rstrip() + WRAPPER.replace('__ON__', str(not args.disabled)).replace('__DAY__', str(args.from_day)).encode()
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
