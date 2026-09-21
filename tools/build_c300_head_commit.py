"""Build a narrow execution experiment on frozen base19; no new evaluation runner."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'state/o_dev/p000_base19.py'
PARENT_SHA = '53d803424d2e9686a1474c04af7827945ec1a08fce5c71df2b6334dcc3f31290'

def build():
    raw = PARENT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_SHA
    source = raw.decode('utf-8')
    def replace_once(old, new):
        nonlocal source
        assert source.count(old) == 1, old[:100]
        source = source.replace(old, new)

    replace_once("        persist = int(_KNOBS.get('vrp_persist', 0))", """        # c300: preserve only a funded in-flight head, not the old whole route.
        commit_on = int(_KNOBS.get('sw_c300_headcommit', 1)) == 1
        locks = {}
        if commit_on and not any(t[0] < 0 for t in tasks):
            for i, (old_day, old_hour, node) in getattr(self, '_c300_heads', {}).items():
                if old_day != day or old_hour != hour-1 or i >= n or node not in live:
                    continue
                need = live[node][3] or self.NEED.get(node[1])
                if need and (invs[i] or {}).get(need, 0) <= 0:
                    continue
                if dist(positions[i], node[0]) + 1 <= left:
                    locks[i] = node
        persist = int(_KNOBS.get('vrp_persist', 0))""")
    old = "        routes = {i: ([node for node in self.routes.get(i, []) if node in live] if persist else []) for i in range(n)}"
    replace_once(old, old + "\n        for i, node in locks.items():\n            routes[i] = [node]")
    old = "                dc, got_need = step_c(nxt)"
    replace_once(old, "                if not out and i in locks and locks[i] in rest:\n                    nxt = locks[i]\n" + old)
    old = "                for k in range(len(r) + 1):"
    replace_once(old, old + "\n                    if i in locks and k == 0:\n                        continue")
    old = "        return cmds\n\n    def act(self, obs):"
    replace_once(old, """        if commit_on:
            heads = {}
            for i, pos in enumerate(positions):
                route = routes[i]
                if not route or pos == route[0][0]:
                    continue
                node = route[0]
                need = need_of(node)
                if need and (invs[i] or {}).get(need, 0) <= 0:
                    continue
                if cmds[i] == step_toward(pos, node[0]):
                    heads[i] = (day, hour, node)
            self._c300_heads = heads
        return cmds

    def act(self, obs):""")
    result = source.encode('utf-8')
    target = ROOT / 'agent/c300_head_commit.py'
    if target.exists():
        assert target.read_bytes() == result, 'Frozen c300 differs; use a new candidate.'
    else:
        target.write_bytes(result)
    manifest = {'parent': str(PARENT.relative_to(ROOT)), 'parent_sha256': PARENT_SHA,
                'candidate': str(target.relative_to(ROOT)), 'sha256': hashlib.sha256(result).hexdigest(),
                'status': 'development only', 'off_knob': 'sw_c300_headcommit=0',
                'closest_prior': 'vrp_persist: whole-route reservations, historically broken',
                'difference': 'one funded in-flight head; all other work replanned; daily/urgent invalidation',
                'design': 'docs/c300-research.ko.md', 'development_seeds': [7000, 7001]}
    path = ROOT / 'state/c300/c300_head_commit.manifest.json'
    if path.exists():
        assert json.loads(path.read_text()) == manifest
    else:
        path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(manifest['sha256'])

if __name__ == '__main__':
    build()
