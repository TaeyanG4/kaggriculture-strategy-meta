import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'agent' / 'o199c_carrot_price2.py'
LANE = ROOT / 'agent' / 'overlays' / 'c177_tomato_strawberry_lane.py'
OVERLAY = ROOT / 'agent' / 'overlays' / 'c178_tomato_lane_no_se.py'
OUTPUT = ROOT / 'agent' / 'c178_tomato_lane_no_se.py'
MANIFEST = ROOT / 'agent' / 'c178_tomato_lane_no_se.manifest.json'
PARENT_SHA = '1429673c3c1057c07f0a644124a4fd497b111b1646451bac1de852e5c035a41d'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(PARENT) == PARENT_SHA
    payload = (PARENT.read_text(encoding='utf-8') + '\n'
               + LANE.read_text(encoding='utf-8') + '\n'
               + OVERLAY.read_text(encoding='utf-8') + '\n')
    compile(payload, str(OUTPUT), 'exec')
    OUTPUT.write_text(payload, encoding='utf-8', newline='\n')
    manifest = {
        'schema': 1,
        'candidate': 'c178_tomato_lane_no_se',
        'status': 'implemented_unvalidated',
        'parent': {'path': 'agent/o199c_carrot_price2.py', 'sha256': PARENT_SHA},
        'overlays': [
            {'path': 'agent/overlays/c177_tomato_strawberry_lane.py', 'sha256': sha(LANE)},
            {'path': 'agent/overlays/c178_tomato_lane_no_se.py', 'sha256': sha(OVERLAY)},
        ],
        'hypothesis': 'Use o199c native strawberry labor slots for tomato and treat them as a replacement for, not an addition to, V219 southeast-land tomato.',
        'contracts': {'adds_buy_land': False, 'adds_hire': False, 'promotion': False, 'submission': False},
        'output': {'path': 'agent/c178_tomato_lane_no_se.py', 'sha256': sha(OUTPUT), 'bytes': OUTPUT.stat().st_size},
        'promotion': False,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
