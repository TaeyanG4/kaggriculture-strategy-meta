"""Generic macro-policy compiler: state key -> candidate actions -> forced rollouts -> robust table.
Decision-agnostic. A decision is described by a small JSON spec:
  {"name": "tomato", "env": "KAGG_FORCE_TOMATO", "actions": ["KEEP","SMALL","MEDIUM"],
   "key_tel": "o214_key", "fired_tel": "o214_fired", "agent": "agent/o214_tomato.py",
   "seeds": "dev", "opps": ["c150","v43","fsv4","msf"]}
The agent must (a) read env[env] and force that action when set, (b) publish the state key of the
event in telemetry[key_tel] and whether it fired in telemetry[fired_tel] (o_arena stores telemetry).
Every table cell stores: support, mean paired margin delta vs KEEP, bootstrap 95% CI, win/loss flips,
win-rate change, per-opponent-family delta, worst family delta, activation frequency.
Selection is robust: override only if support >= min_support, CI lower bound > 0 (or wins up and no
family below -family_tol), else KEEP. Dev seeds (world bank, 7000-8499) and holdout seeds (>= 9000)
are separate; compile uses dev only.
Usage: python o_tools/macro_compile.py spec.json [--workers 12] [--per-key 6] [--min-support 12]
Writes o_results/macro/<name>/table.json and prints the cells that override KEEP.
"""
import argparse, collections, json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
OPP = {'c150': 'agent/c150.py', 'v43': 'state/o_dev/public_pull/kaggriculture-v43-recovering-lost-harvests/extracted_main.py',
       'fsv4': 'state/o_dev/public_pull/farming-score-v4-a-better-shop-20260915/extracted_main.py',
       'msf': 'state/o_dev/public_pull/market-smart-farming-kaggriculture-20260915/extracted_main.py',
       'fsv5': 'state/o_dev/public_pull/farming-score-v5-timing-optimized/extracted_main.py'}
FAMILY = {'c150': 'lineage', 'v43': 'lineage-v43', 'fsv4': 'lineage-fs', 'fsv5': 'lineage-fs', 'msf': 'lineage-msf'}


def dev_seeds(spec):
    if isinstance(spec.get('seeds'), list):
        return spec['seeds']
    bank = json.load(open(os.path.join(ROOT, 'o_tools', 'world_bank.json')))
    buckets = spec.get('buckets') or list(bank)
    return sorted({s for b in buckets for s in bank[b] if s < 9000})


def rollout(spec, action, opp, seeds, workers):
    out = os.path.join(ROOT, 'o_results', 'macro', spec['name'], f'{action}__{opp}.json')
    if os.path.exists(out):
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    env = dict(os.environ, MPLBACKEND='Agg'); env[spec['env']] = action
    print(f"  rollout {spec['name']} action={action} vs {opp} ({len(seeds)} seeds x 2)", flush=True)
    subprocess.run([PY, os.path.join(ROOT, 'tools', 'o_arena.py'), os.path.join(ROOT, spec['agent']), os.path.join(ROOT, OPP[opp]),
                    '--seed-list', ','.join(map(str, seeds)), '--workers', str(workers), '--json-out', out],
                   cwd=ROOT, env=env, capture_output=True, text=True, timeout=14400)
    return out


def ci(d, n_boot=2000):
    if not d: return (0.0, 0.0)
    random.seed(0); n = len(d); ms = sorted(sum(random.choice(d) for _ in range(n)) / n for _ in range(n_boot))
    return ms[int(0.025 * n_boot)], ms[int(0.975 * n_boot) - 1]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--min-support', type=int, default=12); ap.add_argument('--family-tol', type=float, default=-150)
    a = ap.parse_args(); spec = json.load(open(a.spec, encoding='utf-8'))
    seeds = dev_seeds(spec); opps = spec.get('opps', ['c150', 'v43', 'fsv4', 'msf']); actions = spec['actions']
    assert actions[0] == 'KEEP'
    res = {}   # (action, opp, seed, seat) -> record
    for act in actions:
        for opp in opps:
            for r in json.load(open(rollout(spec, act, opp, seeds, a.workers)))['results']:
                if r['outcome'] in ('win', 'loss', 'tie'):
                    res[(act, opp, r['seed'], r['seat'])] = r
    # keys come from the KEEP run's telemetry (state at the event is identical across actions until the override)
    key_of = {(opp, sd, st): res[('KEEP', opp, sd, st)]['telemetry'].get(spec['key_tel'], '') for (act, opp, sd, st) in res if act == 'KEEP'}
    table = {}; report = []
    groups = collections.defaultdict(list)
    for (opp, sd, st), k in key_of.items():
        if k: groups[k].append((opp, sd, st))
    for key, games in sorted(groups.items()):
        cell = {'support': len(games), 'actions': {}}
        best = 'KEEP'
        for act in actions[1:]:
            d = []; fl = [0, 0]; fam = collections.defaultdict(list); fired = 0; wk = wa = 0
            for (opp, sd, st) in games:
                kr = res.get(('KEEP', opp, sd, st)); ar = res.get((act, opp, sd, st))
                if not kr or not ar: continue
                dd = ar['margin'] - kr['margin']; d.append(dd); fam[FAMILY.get(opp, opp)].append(dd)
                fl[0] += kr['margin'] <= 0 < ar['margin']; fl[1] += ar['margin'] <= 0 < kr['margin']
                wk += kr['margin'] > 0; wa += ar['margin'] > 0
                fired += bool(ar['telemetry'].get(spec['fired_tel'], 0))
            if not d: continue
            lo, hi = ci(d); fams = {f: round(sum(v) / len(v)) for f, v in fam.items()}
            stats = dict(n=len(d), delta=round(sum(d) / len(d)), ci=[round(lo), round(hi)], flips_lw=fl[0], flips_wl=fl[1],
                         winrate_keep=round(wk / len(d), 3), winrate=round(wa / len(d), 3), by_family=fams, worst_family=min(fams.values()),
                         activation=round(fired / len(d), 2))
            cell['actions'][act] = stats
        # robust choice: enough support, CI lower > 0, wins not down, no family below tolerance
        ok = [(act, s) for act, s in cell['actions'].items()
              if s['n'] >= a.min_support and s['ci'][0] > 0 and s['winrate'] >= s['winrate_keep'] and s['worst_family'] >= a.family_tol]
        if ok:
            best = max(ok, key=lambda kv: (kv[1]['winrate'] - kv[1]['winrate_keep'], kv[1]['delta']))[0]
        cell['choice'] = best; table[key] = cell
        report.append((key, len(games), best, {k: (v['delta'], v['ci'], f"{v['winrate_keep']:.0%}->{v['winrate']:.0%}", v['worst_family']) for k, v in cell['actions'].items()}))
    out = os.path.join(ROOT, 'o_results', 'macro', spec['name'], 'table.json')
    json.dump({'name': spec['name'], 'actions': actions, 'dev_seeds': seeds, 'opps': opps, 'table': table}, open(out, 'w'), indent=1)
    print(f"{spec['name']}: {len(table)} keys, overrides: {sum(1 for c in table.values() if c['choice'] != 'KEEP')} -> {out}")
    for key, n, best, st in report:
        flag = '*' if best != 'KEEP' else ' '
        print(f" {flag} {key:40s} n={n:3d} -> {best:7s} {st}")


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
