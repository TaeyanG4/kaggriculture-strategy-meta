"""Shadow-planner dataset: state at the livestock decision steps -> the macro each side actually chose.
For every replay and both seats, at d6 (step 150), d8 (196), d10 (241): shops known, demand counts,
prices/inventory, own cash, own & rival animal counts, days left -> label = dominant kind bought in the
following window (COW/SHEEP/GOOSE, or NONE), plus the game outcome and the player's identity/rating.
Output: o_results/shadow/dataset.jsonl (one row per game x seat x slot) and a boundary report.
Usage: python o_tools/shadow_dataset.py [--dirs ...] [--min-rating 2750]
"""
import argparse, collections, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'); EGG = ('BAKERY', 'BRUNCH_SPOT'); WOOL = ('YARN_STORE',)
SLOTS = {'d6': (150, 144, 192), 'd8': (196, 192, 240), 'd10': (241, 240, 288)}   # decision step, buy window


def animals(farm):
    c = collections.Counter()
    for row in farm['tiles']:
        for t in row:
            if isinstance(t, dict) and t.get('animal'):
                c[t['animal']] += 1
    return c


def bought(rep, seat, a, b):
    c = collections.Counter()
    for st in rep['steps'][a:b]:
        for o in ((st[seat].get('action') or {}).get('market') or []):
            if o and o[0] == 'BUY_ANIMAL':
                c[o[1]] += int(o[2])
    return c


def rows_for(path, ratings):
    rep = json.load(open(path, encoding='utf-8')); names = rep['info']['TeamNames']; rw = [s['reward'] for s in rep['steps'][-1]]
    out = []
    for seat in (0, 1):
        for slot, (t, a, b) in SLOTS.items():
            st = rep['steps'][t]; obs = st[seat]['observation']; shared = st[0]['observation']
            shops = shared['town']['unlocked_shops']; pr = shared['market']['prices']; inv = shared['market']['inventory']
            me = animals(shared['farms'][seat]); rv = animals(shared['farms'][1 - seat]); buy = bought(rep, seat, a, b)
            label = max(buy, key=buy.get) if buy else 'NONE'
            out.append(dict(eid=rep['info']['EpisodeId'], seat=seat, team=names[seat], rival=names[1 - seat], slot=slot,
                            rating=ratings.get(names[seat]), win=rw[seat] > rw[1 - seat], margin=rw[seat] - rw[1 - seat],
                            shops=shops[:4], n_shops=len(shops), milk=sum(s in MILK for s in shops), egg=sum(s in EGG for s in shops), wool=sum(s in WOOL for s in shops),
                            yarn_route='YARN_STORE' in shops[:2],
                            p_milk=pr['MILK'], p_wool=pr['WOOL'], p_egg=pr['EGG'], p_wheat=pr['WHEAT'], inv_milk=inv['MILK'], inv_wool=inv['WOOL'], inv_egg=inv['EGG'],
                            cash=shared['farms'][seat]['money'], me_cow=me['COW'], me_sheep=me['SHEEP'], me_goose=me['GOOSE'],
                            rv_cow=rv['COW'], rv_sheep=rv['SHEEP'], rv_goose=rv['GOOSE'], days_left=29 - t // 24,
                            buy=dict(buy), label=label))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dirs', nargs='*', default=['o_replays/live_all', 'o_replays/elite_chunks', 'o_replays/elite2_chunks', 'o_replays/leader_archive'])
    ap.add_argument('--min-rating', type=float, default=2750); a = ap.parse_args()
    ratings = {}
    for f in ('o_replays/elite_losses/_index.json', 'o_replays/elite_losses_new/_index.json'):
        try:
            for x in json.load(open(os.path.join(ROOT, f))):
                if x.get('opp_rating'): ratings[str(x.get('opp_team'))] = x['opp_rating']
        except Exception: pass
    files = {}
    for d in a.dirs:
        for p in glob.glob(os.path.join(ROOT, d, '**', '*-replay.json'), recursive=True):
            files.setdefault(os.path.basename(p).split('-')[0], p)
    os.makedirs(os.path.join(ROOT, 'o_results', 'shadow'), exist_ok=True)
    rows = []
    for p in files.values():
        try: rows += rows_for(p, ratings)
        except Exception: continue
    with open(os.path.join(ROOT, 'o_results', 'shadow', 'dataset.jsonl'), 'w', encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'{len(files)} replays -> {len(rows)} rows')
    # boundary report: strong players (winners of the game, or Majkel) by slot and demand state
    strong = [r for r in rows if r['win'] or r['team'] == 'Majkel1337']
    for slot in SLOTS:
        g = collections.defaultdict(collections.Counter)
        for r in strong:
            if r['slot'] != slot or r['yarn_route']: continue
            key = (f"milk{min(r['milk'],3)}", f"egg{min(r['egg'],2)}", f"wool{min(r['wool'],1)}")
            g[key][r['label']] += 1
        print(f'\n== {slot}: winners\' choice by (milk, egg, wool shop counts known at the slot), n>=6')
        for key, c in sorted(g.items(), key=lambda kv: -sum(kv[1].values())):
            n = sum(c.values())
            if n < 6: continue
            print('  ', ' '.join(key), f'n={n:3d}', {k: f'{v/n:.0%}' for k, v in c.most_common(3)})


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
