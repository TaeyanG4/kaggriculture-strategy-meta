"""Shadow-planner counterfactuals on real replays (frozen rival, fixed shops).
A hypothesis = (slot, kind, state predicate). For every replay of ours whose state at the slot matches,
replay it with the o209 stack forced to `kind` at that slot (others on fallback) and with no force,
via replay_lab; report paired margin delta, win flips and the rival's money change (externality).
Usage: python o_tools/shadow_cf.py <name> <slot d6|d8|d10> <kind> "<python predicate over row r>" [--dirs ...]
  e.g. shadow_cf.py H2 d10 COW "r['milk']>=2 and r['wool']==0 and not r['yarn_route']"
Rows come from o_results/shadow/dataset.jsonl (only our seat: team == Taeyang).
"""
import argparse, glob, json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
AGENT = os.path.join(ROOT, 'agent', 'o209_policy.py')
SLOT_IDX = {'d6': 0, 'd8': 1, 'd10': 2}


def run_variant(name, force, chunk):
    out = os.path.join(ROOT, 'o_results', 'shadow', name, force.replace(',', '_'))
    if glob.glob(os.path.join(out, 'results.json')):
        return out
    env = dict(os.environ, MPLBACKEND='Agg', KAGG_O209_FORCE=force, KAGG_VERIFY_CACHE=os.path.join(ROOT, 'o_results', '_verify_cache'))
    subprocess.run([PY, '-m', 'src.kaggriculture_meta.replay_lab', '--candidate', AGENT, '--replays', chunk, '--out', out, '--mode', 'fixed_shops_frozen_opponent'],
                   cwd=ROOT, env=env, capture_output=True, text=True, timeout=7200)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('name'); ap.add_argument('slot'); ap.add_argument('kind'); ap.add_argument('pred')
    ap.add_argument('--team', default='Taeyang'); ap.add_argument('--max', type=int, default=60); a = ap.parse_args()
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'o_results', 'shadow', 'dataset.jsonl'), encoding='utf-8')]
    sel = [r for r in rows if r['slot'] == a.slot and r['team'] == a.team and eval(a.pred, {}, {'r': r})][:a.max]
    eids = {str(r['eid']) for r in sel}
    files = {}
    for p in glob.glob(os.path.join(ROOT, 'o_replays', '*', '*-replay.json')) + glob.glob(os.path.join(ROOT, 'o_replays', '*', '*', '*-replay.json')):
        e = os.path.basename(p).split('-')[0]
        if e in eids and e not in files: files[e] = p
    chunk = os.path.join(ROOT, 'o_replays', 'shadow_chunks', a.name)
    if os.path.exists(chunk): shutil.rmtree(chunk)
    os.makedirs(chunk)
    for e, p in files.items(): shutil.copy2(p, chunk)
    print(f'{a.name}: {len(sel)} matching states, {len(files)} replays -> {chunk}', flush=True)
    force = ','.join(a.kind if i == SLOT_IDX[a.slot] else '-' for i in range(3))
    base = run_variant(a.name, '-,-,-', chunk); cf = run_variant(a.name, force, chunk)
    B = {r['episode']: r for r in json.load(open(os.path.join(base, 'results.json'), encoding='utf-8'))}
    C = {r['episode']: r for r in json.load(open(os.path.join(cf, 'results.json'), encoding='utf-8'))}
    d = []; riv = []; flips = [0, 0]
    for e in B:
        if e not in C: continue
        s = B[e]['candidate_seat']; d.append(C[e]['margin'] - B[e]['margin']); riv.append(C[e]['rewards'][1 - s] - B[e]['rewards'][1 - s])
        flips[0] += B[e]['margin'] <= 0 < C[e]['margin']; flips[1] += C[e]['margin'] <= 0 < B[e]['margin']
    n = len(d)
    if not n: print('no paired results'); return
    import random; random.seed(0); ms = sorted(sum(random.choice(d) for _ in range(n)) / n for _ in range(2000))
    print(f'{a.name} force {force}: n={n} mean delta {sum(d)/n:+.0f} CI[{ms[50]:+.0f},{ms[1949]:+.0f}] | flips L->W {flips[0]} W->L {flips[1]} | wins {sum(C[e]["margin"]>0 for e in C)}/{n} (base {sum(B[e]["margin"]>0 for e in B)}) | rival money delta {sum(riv)/n:+.0f}')
    print('  per game (delta, rival delta, shops[:3]):', sorted((round(C[e]['margin'] - B[e]['margin']), round(C[e]['rewards'][1 - B[e]['candidate_seat']] - B[e]['rewards'][1 - B[e]['candidate_seat']]), tuple(B[e]['shops'][:3])) for e in B if e in C)[:12])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
