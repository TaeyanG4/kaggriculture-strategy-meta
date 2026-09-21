"""Single ablation of c305's collateral sale of pre-existing carrot stock."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
parent = ROOT / 'agent/c305_v48_certified_rotation.py'
raw = parent.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'e6144537246b31fc7855780ebf7d9504bbc3fa03ebf1c07c9e63719529f7f604'
source = raw.decode('utf-8').replace('\r\n', '\n')
start = source.index('    # Sell only physically projected carrot stock. Existing native orders retain priority.')
end = source.index('    if not 18 <= day <= 25', start)
removed = source[start:end]
assert "if state['conversions']:" in removed and "['SELL', 'CARROT', stock - sale]" in removed
source = source[:start] + '    # c306: native policy owns all carrot sales, including any added production.\n' + source[end:]
source = source.replace('_C305_', '_C306_')
out = ROOT / 'agent/c306_v48_native_sale_rotation.py'
assert not out.exists()
out.write_text(source, encoding='utf-8')
state = ROOT / 'state/c306'
state.mkdir(exist_ok=True)
manifest = dict(parent='state/o_dev/v48_clearqueue_public.py', parent_sha256='4b5402888feeb4170dce38f34bebe56788b62ca287139fce7db72df8eb89bb96', derivative_source=str(parent.relative_to(ROOT)), derivative_sha256=hashlib.sha256(raw).hexdigest(), candidate=str(out.relative_to(ROOT)), candidate_sha256=hashlib.sha256(out.read_bytes()).hexdigest(), only_behavior_change='Remove c146 supplemental carrot SELL block; native sale logic retained', status='development_only', off='_C306_ON=False')
(state/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest))
