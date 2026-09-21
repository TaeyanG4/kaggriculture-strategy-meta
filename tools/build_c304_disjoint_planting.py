"""Single allocation change on frozen base19; preserve original sources."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parent = ROOT / 'state/o_dev/p000_base19.py'
raw = parent.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '53d803424d2e9686a1474c04af7827945ec1a08fce5c71df2b6334dcc3f31290'
source = raw.decode('utf-8')
old = '            used[crop] = len(picked)'
assert source.count(old) == 1
new = '''            # c304: represent each crop's funded planting on distinct free tiles.
            if int(_KNOBS.get('sw_c304_disjoint', 1)):
                claimed.update(picked)
            used[crop] = len(picked)'''
source = source.replace(old, new)
out = ROOT / 'agent/c304_disjoint_planting.py'
compile(source, str(out), 'exec')
out.write_text(source, encoding='utf-8')
manifest = {'parent': str(parent.relative_to(ROOT)), 'parent_sha256': hashlib.sha256(raw).hexdigest(), 'candidate': str(out.relative_to(ROOT)), 'candidate_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'status': 'development_only', 'mechanism': 'Disjoint funded crop planting allocation before existing task deduplication', 'development_seeds': [7000, 7001], 'off_knob': 'sw_c304_disjoint=0'}
(ROOT / 'state/c304/manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest))
