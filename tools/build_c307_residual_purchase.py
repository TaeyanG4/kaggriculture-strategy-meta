"""Correct one audited deficit/quota contract on frozen base19."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parent = ROOT/'state/o_dev/p000_base19.py'
raw = parent.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='53d803424d2e9686a1474c04af7827945ec1a08fce5c71df2b6334dcc3f31290'
source = raw.decode('utf-8')
old = '            left = target - done\n'
assert source.count(old)==1
new = '''            # c307: these targets already subtract placed + owned inventory.
            # Day-zero totals and later seed daily/batch ceilings keep parent logic.
            residual_contract = day >= 1 and (kind == 'ANIMAL' or
                (kind == 'SEED' and item in ('MELON', 'STRAWBERRY') and day <= 5))
            use_residual = bool(int(_KNOBS.get('sw_c307_residual', 1))) and residual_contract
            left = target if use_residual else target - done
            if use_residual and done > 0 and target > 0:
                _C307_TEL['c307_residual_checks'] += 1
'''
source = source.replace(old,new)
old = '        st = _STATE[seat] = Proxy(seat)\n'
assert source.count(old)==1
source = source.replace(old, old+"        _C307_TEL.update(c307_residual_checks=0, c307_internal_errors=0)\n")
old = '    except Exception:\n        return {\'farmer\': [\'PASS\']'
assert source.count(old)==1
source = source.replace(old, "    except Exception:\n        _C307_TEL['c307_internal_errors'] += 1\n        return {'farmer': ['PASS']")
source += "\n_C307_TEL = dict(c307_residual_checks=0, c307_internal_errors=0)\nagent.telemetry = _C307_TEL\n"
output = ROOT/'agent/c307_residual_purchase.py'
assert not output.exists()
compile(source,str(output),'exec')
output.write_text(source,encoding='utf-8')
manifest = dict(parent=str(parent.relative_to(ROOT)),parent_sha256=hashlib.sha256(raw).hexdigest(),
    candidate=str(output.relative_to(ROOT)),candidate_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
    status='development_only',off_knob='sw_c307_residual=0',
    mechanism='For d1+ animal residuals and d1-5 MELON/STRAWBERRY shortfalls only, do not subtract daily order count twice. Original targets, priorities, routing and sales remain.',
    evidence='state/c307/purchase_audit/summary.json: four action-identical diagnostics show funded/space-feasible suppression, not realized loss.',
    closest_prior='H02 seed cash reservation; p002 added cow; F herd targets. This changes residual accounting, not target numbers. Later seed mixed quota/residual semantics intentionally outside scope.',
    development_conditions='V48 pinned 7000/7001 both seats already observed; not independent confirmation.',
    gate='Off action/cash identity; no internal exceptions; pooled own and margin positive. Otherwise stop broad strength testing. Report all world/seat outcomes, realized purchases and production; no parameter search.',
    known_limitations='Daily order counters still count emitted orders, not all engine transactions. This correction is not a general fill/retry protocol. Purchase target changes across future states may change final herd.')
(ROOT/'state/c307/manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest))
