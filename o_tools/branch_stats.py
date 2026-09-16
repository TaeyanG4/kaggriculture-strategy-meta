"""Observational branch statistics from replays: per situation, what each side chose and who won.
Situation = shop world (first 2 / 3 shops); choices = animals bought on days 6-7, 8-9, 10-11
(from market orders), as (COW,SHEEP,GOOSE) counts; outcome = margin > 0.
Prints win rate per (world bucket, my d6 choice), per (bucket, my d6, rival d6) and the same for d10.
Usage: python o_tools/branch_stats.py [--dirs o_replays/live_all o_replays/elite_chunks ...] [--team Taeyang]
"""
import argparse, collections, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
WINDOWS = {'d6': (144, 192), 'd8': (192, 240), 'd10': (240, 288)}


def bucket(shops):
    f2 = shops[:2]
    return 'yarn' if 'YARN_STORE' in f2 else ('goose', 'one_milk', 'two_milk')[sum(s in MILK for s in f2)]


def choices(rep, seat):
    out = {}
    for name, (a, b) in WINDOWS.items():
        c = collections.Counter()
        for st in rep['steps'][a:b]:
            for o in ((st[seat].get('action') or {}).get('market') or []):
                if o and o[0] == 'BUY_ANIMAL':
                    c[o[1]] += int(o[2])
        out[name] = '+'.join(f'{c[k]}{k[0]}' for k in ('COW', 'SHEEP', 'GOOSE') if c[k]) or '0'
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dirs', nargs='*', default=['o_replays/live_all', 'o_replays/elite_chunks', 'o_replays/elite2_chunks', 'o_replays/leader_archive'])
    ap.add_argument('--team', default=None, help='only this team as "me" (default: both seats of every game)'); a = ap.parse_args()
    files = {}
    for d in a.dirs:
        for p in glob.glob(os.path.join(ROOT, d, '**', '*-replay.json'), recursive=True):
            files.setdefault(os.path.basename(p).split('-')[0], p)
    rows = []
    for eid, p in files.items():
        try: rep = json.load(open(p, encoding='utf-8'))
        except Exception: continue
        names = rep['info']['TeamNames']; rw = [s['reward'] for s in rep['steps'][-1]]; shops = rep['steps'][-1][0]['observation']['town']['unlocked_shops']
        ch = [choices(rep, 0), choices(rep, 1)]
        for seat in (0, 1):
            if a.team and names[seat] != a.team:
                continue
            rows.append(dict(eid=eid, me=names[seat], riv=names[1 - seat], win=rw[seat] > rw[1 - seat], margin=rw[seat] - rw[1 - seat],
                             b=bucket(shops), s3='|'.join(sorted(shops[:3])), mine=ch[seat], theirs=ch[1 - seat]))
    print(f'{len(files)} replays, {len(rows)} seat-rows')
    def table(title, keyf, minn=8):
        g = collections.defaultdict(list)
        for r in rows: g[keyf(r)].append(r)
        print(f'\n== {title}')
        for k, v in sorted(g.items(), key=lambda kv: (kv[0][0], -len(kv[1]))):
            if len(v) < minn: continue
            w = sum(r['win'] for r in v); print(f'  {str(k):58s} n={len(v):4d} win {w/len(v):5.0%}  margin {sum(r["margin"] for r in v)/len(v):+7.0f}')
    table('bucket x my d6 choice', lambda r: (r['b'], r['mine']['d6']))
    table('bucket x my d6 x rival d6', lambda r: (r['b'], 'me ' + r['mine']['d6'], 'riv ' + r['theirs']['d6']))
    table('bucket x my d8 choice', lambda r: (r['b'], r['mine']['d8']))
    table('bucket x my d10 choice', lambda r: (r['b'], r['mine']['d10']))
    table('bucket x my d10 x rival d10', lambda r: (r['b'], 'me ' + r['mine']['d10'], 'riv ' + r['theirs']['d10']))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
