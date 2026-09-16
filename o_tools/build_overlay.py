"""Build a self-contained agent = parent source + overlay(s) appended (Kaggle needs one file;
replay_lab freezes a copy of the candidate elsewhere so path-relative imports would break).
Usage: python o_tools/build_overlay.py --parent agent/c150.py --overlay agent/overlays/o158_feed_margin.py --out agent/o158_feed_margin.py
Multiple --overlay flags are appended in order. Never modifies the parent."""
import argparse, hashlib, os
ap = argparse.ArgumentParser()
ap.add_argument('--parent', required=True); ap.add_argument('--overlay', action='append', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args()
src = open(a.parent, encoding='utf-8').read()
header = f"# o-series build (Claude, 2026-09-15): parent {a.parent} sha256 {hashlib.sha256(src.encode()).hexdigest()[:16]} + overlays {a.overlay}. Apache-2.0; parent notices retained below.\n"
out = header + src
import re as _re
seen = {}
for ov in a.overlay:   # two overlays sharing a _X_PARENT name recurse forever (late global binding)
    for name in _re.findall(r'^(_[A-Z0-9]+_PARENT)\s*=', open(ov, encoding='utf-8').read(), _re.M):
        assert name not in seen, f'{name} defined by both {seen[name]} and {ov}: rename the overlay prefix'
        seen[name] = ov
for ov in a.overlay:
    out += "\n\n" + open(ov, encoding='utf-8').read()
compile(out, a.out, 'exec')
# Kaggle's build_agent uses the LAST callable in the module namespace: verify it is `agent`.
ns = {'__name__': 'o_build_check'}
exec(compile(out, a.out, 'exec'), ns)
last = [k for k, v in ns.items() if callable(v) and not k.startswith('__')][-1]
assert last == 'agent', f'last callable is {last!r}, not agent - append agent = globals().pop("agent") to the overlay'
open(a.out, 'w', encoding='utf-8').write(out)
print('built', a.out, len(out), 'bytes sha256', hashlib.sha256(out.encode()).hexdigest()[:16])
