import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'agent' / 'o199c_carrot_price2.py'
OVERLAYS = [
    ROOT / 'agent' / 'overlays' / 'c177_tomato_strawberry_lane.py',
    ROOT / 'agent' / 'overlays' / 'c179_early_tomato_plus_v219.py',
    ROOT / 'agent' / 'overlays' / 'c180_guarded_early_tomato2.py',
]
OUTPUT = ROOT / 'agent' / 'c180_guarded_early_tomato2.py'
MANIFEST = ROOT / 'agent' / 'c180_guarded_early_tomato2.manifest.json'
PARENT_SHA = '1429673c3c1057c07f0a644124a4fd497b111b1646451bac1de852e5c035a41d'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(PARENT) == PARENT_SHA
    payload = PARENT.read_text(encoding='utf-8') + '\n'
    for overlay in OVERLAYS:
        payload += overlay.read_text(encoding='utf-8') + '\n'
    compile(payload, str(OUTPUT), 'exec')
    OUTPUT.write_text(payload, encoding='utf-8', newline='\n')
    manifest = {
        'schema': 1,
        'candidate': 'c180_guarded_early_tomato2',
        'status': 'implemented_unvalidated',
        'parent': {'path': 'agent/o199c_carrot_price2.py', 'sha256': PARENT_SHA},
        'overlays': [{'path': str(p.relative_to(ROOT)).replace('\\','/'), 'sha256': sha(p)} for p in OVERLAYS],
        'policy': 'At native day11 strawberry tranche: 2 tiles STRAWBERRY->TOMATO only if tomato-demand shops >=2, strawberry-demand shops <=1, TOMATO price>=60; preserve V219 if its own day18 gates qualify.',
        'evidence_origin': 'c179 cheap panel: negative seeds 7078/7082 both had strawberry-demand=2; positive four had 0..1.',
        'promotion': False,
        'output': {'path': 'agent/c180_guarded_early_tomato2.py', 'sha256': sha(OUTPUT), 'bytes': OUTPUT.stat().st_size},
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
