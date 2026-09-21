"""Reuse c146's audited route contract on V48 without importing old policy layers."""
import ast
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
parent = ROOT / 'state/o_dev/v48_clearqueue_public.py'
module = ROOT / 'agent/overlays/c146_carrot_sched3.py'
helper = ROOT / 'agent/overlays/championship_placement.py'
assert hashlib.sha256(parent.read_bytes()).hexdigest() == '4b5402888feeb4170dce38f34bebe56788b62ca287139fce7db72df8eb89bb96'
source = helper.read_text(encoding='utf-8')
tree = ast.parse(source)
pieces = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_CP0_MOVES' for t in node.targets):
        pieces.append(ast.get_source_segment(source, node))
    elif isinstance(node, ast.FunctionDef) and node.name == '_cp0_command':
        pieces.append(ast.get_source_segment(source, node))
assert len(pieces) == 2
out = ROOT / 'state/c305'
out.mkdir(exist_ok=True)
(out / 'adapter.py').write_text('# SPDX-License-Identifier: Apache-2.0\n# c305: reuse two original championship_placement helpers; no policy layer.\n' + '\n\n'.join(pieces) + '\nagent = _e335_agent\nagent = globals().pop("agent")\n', encoding='utf-8')
(out / 'entry.py').write_text('''# c305: same frozen file supports an off identity audit through the loader.
_C305_ON = True
_C305_ACTIVE = agent
_TEL = _C146_REPORT
def agent(observation, configuration=None):
    if not _C305_ON:
        return _C146_PARENT(observation, configuration)
    return _C305_ACTIVE(observation, configuration)
agent.telemetry = _TEL
agent = globals().pop('agent')
''', encoding='utf-8')
manifest = dict(parent=str(parent.relative_to(ROOT)), parent_sha256=hashlib.sha256(parent.read_bytes()).hexdigest(), module=str(module.relative_to(ROOT)), module_sha256=hashlib.sha256(module.read_bytes()).hexdigest(), helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(), design='c146 route-certified late carrot rotation; unchanged thresholds; no o199c forced harvest', status='development_only', off='_C305_ON=False set by diagnostic loader')
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print('Prepared adapter and off wrapper; build with existing o_tools/build_overlay.py')
