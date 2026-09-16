"""Top-10 archive: how top planners fare against the strongest tape-lineage forks (strength-matched benchmark).
Reads every local replays_*.parquet shard, classifies each player as tape-lineage (>= 80% field-action match with
our route tapes, offset +1) or planner, and reports per (planner, fork) records for forks rated >= --min-rating on the
current leaderboard CSV. Usage: python o_tools/top_vs_forks.py --lb <leaderboard.csv> [--min-rating 2750] [--since 2026-09-08]
"""
import argparse, collections, csv, glob, json, os, sys
import pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'


def load_tapes():
    src = open(os.path.join(ROOT, 'agent', 'o219_o218_c180_tomato2.py'), encoding='utf-8').read()
    ns = {'__name__': 'o219mod'}; exec(compile(src, 'o219', 'exec'), ns)
    field = lambda a: (tuple(a.get('farmer') or ['PASS']), tuple(tuple(h) for h in (a.get('hands') or [])))
    return field, {rid: [field(t) for t in tape] for rid, tape in ns['_IMPL'].chassis.routes.items()}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--lb', required=True); ap.add_argument('--min-rating', type=float, default=2750)
    ap.add_argument('--since', default='2026-09-08'); a = ap.parse_args()
    rating = {}
    with open(a.lb, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            try: rating[row['TeamName']] = float(row['Score'])
            except Exception: pass
    field, tapes = load_tapes()

    def lineage(acts):
        best = 0.0
        for tp in tapes.values():
            ok = tot = 0
            for t in range(24, 144):
                if t + 1 < len(acts): tot += 1; ok += field(acts[t + 1] or {}) == tp[t]
            best = max(best, ok / max(1, tot))
            if best >= 0.8: break
        return best
    idx = pd.read_parquet(os.path.join(ROOT, 'state/o_dev/datasets/top10_archive/episodes.parquet'))
    idx['date'] = idx['date'].astype(str); recent = set(idx[idx['date'] >= a.since]['episode_id'])
    rows = collections.defaultdict(list); cls_cache = {}
    for sh in sorted(glob.glob(os.path.join(ROOT, 'state/o_dev/datasets/top10_archive/replays_*.parquet'))):
        if sh.split('replays_')[1][:10] < a.since: continue
        df = pd.read_parquet(sh)
        for eid, rj in zip(df['episode_id'], df['replay_json']):
            if eid not in recent: continue
            rep = json.loads(rj); names = rep['info']['TeamNames']; st = rep['steps']
            strong = [i for i in (0, 1) if rating.get(names[i], 0) >= a.min_rating]
            if not strong: continue
            for i in strong:
                if names[i] not in cls_cache:
                    cls_cache[names[i]] = lineage([s[i].get('action') or {} for s in st])
                if cls_cache[names[i]] < 0.8: continue     # only tape-lineage strong forks
                o = 1 - i
                rows[(names[o], names[i])].append(st[-1][o]['reward'] - st[-1][i]['reward'])
    print(f'strong tape forks (>= {a.min_rating:.0f}): {sorted({k[1] for k in rows})}')
    agg = collections.defaultdict(list)
    for (team, fork), v in rows.items(): agg[team] += v
    print('\nper opponent team (planner or other) vs strong forks: n / wins / mean margin')
    for team, v in sorted(agg.items(), key=lambda kv: -len(kv[1]))[:25]:
        print(f'  {team[:24]:24s} n={len(v):3d} wins {sum(m > 0 for m in v):3d} ({sum(m > 0 for m in v) / len(v):.0%}) mean {sum(v) / len(v):+7.0f} rating {rating.get(team, 0):.0f}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
