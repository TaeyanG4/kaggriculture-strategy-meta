"""Version only concurrency limits/entrypoints, preserving frozen v1 contracts."""
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pairs=[
 ('tools/validation_v1.py','tools/validation_v2.py',[
  ('evaluator v1.', 'evaluator v2 (12-worker capacity; native match semantics unchanged).'),
  ("ROOT/'tools/run-validation.ps1'", "ROOT/'tools/run-validation-v2.ps1'"),
  ("1<=p['workers']<=8,'workers must be 1..8'", "1<=p['workers']<=12,'workers must be 1..12'")]),
 ('tools/run-validation.ps1','tools/run-validation-v2.ps1',[
  ("'validation_v1.py'", "'validation_v2.py'"),
  ('validation_v1\\.py', 'validation_v[12]\\.py')]),
 ('o_tools/arena_hashcheck.py','o_tools/arena_hashcheck_v2.py',[
  ('from validation_v1 import support_hashes', 'from validation_v2 import support_hashes')]),
]
manifest=[]
for old,new,replacements in pairs:
 raw=(ROOT/old).read_bytes(); text=raw.decode('utf-8').replace('\r\n','\n')
 for before,after in replacements:
  assert text.count(before)==1,(old,before,text.count(before))
  text=text.replace(before,after)
 target=ROOT/new
 assert not target.exists(),new
 target.write_text(text,encoding='utf-8')
 manifest.append(dict(source=old,source_sha256=hashlib.sha256(raw).hexdigest(),target=new,target_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),replacements=replacements))
def functions(path):
 return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse((ROOT/path).read_text(encoding='utf-8')).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a=functions('tools/validation_v1.py');b=functions('tools/validation_v2.py')
assert a.keys()==b.keys()
assert [k for k in a if a[k]!=b[k]]==['validate_config']
out=ROOT/'state/c306/runner_v2_provenance.json'
out.write_text(json.dumps(dict(files=manifest,unchanged_runtime_functions=sorted(k for k in a if a[k]==b[k]),scope='Concurrency limit 12 and separate launcher/support identity only; all match/job/check/cache/runtime/statistics functions AST-identical.'),indent=2),encoding='utf-8')
print('Created v2 without modifying v1; native runtime functions AST-identical')
