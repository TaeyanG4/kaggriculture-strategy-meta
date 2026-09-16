import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'agent' / 'o199c_carrot_price2.py'
OVERLAY = ROOT / 'agent' / 'overlays' / 'c177_tomato_strawberry_lane.py'
OUTPUT = ROOT / 'agent' / 'c177_tomato_strawberry_lane.py'
MANIFEST = ROOT / 'agent' / 'c177_tomato_strawberry_lane.manifest.json'
PARENT_SHA = '1429673c3c1057c07f0a644124a4fd497b111b1646451bac1de852e5c035a41d'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(PARENT) == PARENT_SHA
    payload = PARENT.read_text(encoding='utf-8') + '\n' + OVERLAY.read_text(encoding='utf-8') + '\n'
    compile(payload, str(OUTPUT), 'exec')
    OUTPUT.write_text(payload, encoding='utf-8', newline='\n')
    manifest = {
        'schema': 1,
        'candidate': 'c177_tomato_strawberry_lane',
        'status': 'implemented_unvalidated',
        'parent': {'path': 'agent/o199c_carrot_price2.py', 'sha256': PARENT_SHA},
        'overlay': {'path': 'agent/overlays/c177_tomato_strawberry_lane.py', 'sha256': sha(OVERLAY)},
        'hypothesis': 'Replace only part of o199c day-11 STRAWBERRY lane with TOMATO while reusing its already-funded ongoing-crop worker geometry.',
        'contracts': {
            'adds_buy_land': False,
            'adds_hire': False,
            'adds_wheat_topup': False,
            'force_env': 'KAGG_C177_FORCE=KEEP|TOMATO; KAGG_C177_SIZE=1..13',
            'promotion': False,
            'submission': False,
        },
        'output': {'path': 'agent/c177_tomato_strawberry_lane.py', 'sha256': sha(OUTPUT), 'bytes': OUTPUT.stat().st_size},
        'promotion': False,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
