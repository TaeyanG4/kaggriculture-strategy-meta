"""D1 of the planner-proxy plan: extract a top planner's macro policy from archived replays, per world bucket.
Outputs o_results/proxy/<team>_policy.json with, per bucket: animal purchases by day and kind, land-buy days,
hands per day, plantings per day by crop, fertilize targets by (crop, age), feed rate on production days,
sale batch sizes and shed buffers by product, late-game animal counts, hires and final cash.
Usage: python o_tools/proxy_policy_stats.py [--team Majkel1337] [--dirs o_replays/leader_archive ...]"""
import argparse, collections, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MILK = {'PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'}
FIRST = {'GOOSE': 4, 'COW': 8, 'SHEEP': 6}; INT = {'GOOSE': 1, 'COW': 2, 'SHEEP': 3}
ITEMS = ('MILK', 'WOOL', 'STRAWBERRY', 'EGG', 'WHEAT', 'CARROT', 'FERTILIZER', 'MELON', 'TOMATO')


def bucket(shops):
    return 'yarn' if 'YARN_STORE' in shops[:2] else 'milk%d' % min(3, sum(s in MILK for s in shops[:3]))


def animals(farm):
    c = collections.Counter()
    for row in farm['tiles']:
        for t in row:
            if isinstance(t, dict) and t.get('animal'):
                c[t['animal']] += 1
    return c


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--team', default='Majkel1337')
    ap.add_argument('--dirs', nargs='*', default=['o_replays/leader_archive']); a = ap.parse_args()
    B = collections.defaultdict(lambda: collections.defaultdict(list))
    n_games = collections.Counter()
    for d in a.dirs:
        for p in glob.glob(os.path.join(ROOT, d, '**', '*-replay.json'), recursive=True):
            rep = json.load(open(p, encoding='utf-8')); names = rep['info']['TeamNames']
            if a.team not in names:
                continue
            s = names.index(a.team); st = rep['steps']; b = bucket(st[-1][0]['observation']['town']['unlocked_shops'])
            n_games[b] += 1; R = B[b]
            R['final_cash'].append(st[-1][s]['reward'])
            buys = collections.Counter(); land = []; plants = collections.Counter(); fert = collections.Counter(); hires = collections.Counter()
            sells = collections.defaultdict(list)
            for k in range(719):
                day = k // 24; act = st[k][s].get('action') or {}; o = st[k][0]['observation']; farm = o['farms'][s]
                pos = [farm.get('farmer')] + farm.get('hands', []); cmds = [act.get('farmer')] + (act.get('hands') or [])
                for m in (act.get('market') or []):
                    if not m: continue
                    if m[0] == 'BUY_ANIMAL': buys[(day, m[1])] += int(m[2])
                    elif m[0] == 'BUY_LAND': land.append(day)
                    elif m[0] == 'HIRE': hires[day] += 1
                    elif m[0] == 'SELL' and m[1] in ITEMS: sells[m[1]].append(min(int(m[2]), 100))
                for i, c in enumerate(cmds):
                    if not c or i >= len(pos): continue
                    if c[0] == 'PLANT': plants[(day, c[1])] += 1
                    if c[0] == 'FERTILIZE':
                        x, y = pos[i]; t = farm['tiles'][y][x]
                        if isinstance(t, dict) and t.get('crop'):
                            fert[(t['crop'], min(6, day - int(t.get('planted_day', day))))] += 1
            R['animal_buys'].append({f'{d}:{k}': v for (d, k), v in buys.items()})
            R['land_days'].append(sorted(set(land)))
            R['hands_by_day'].append([len(st[min(719, d * 24 + 12)][0]['observation']['farms'][s]['hands']) for d in range(30)])
            R['plants'].append({f'{d}:{c}': v for (d, c), v in plants.items()})
            R['fertilize'].append({f'{c}@{ag}': v for (c, ag), v in fert.items()})
            R['animals_by_day'].append([dict(animals(st[min(719, d * 24 + 12)][0]['observation']['farms'][s])) for d in range(0, 30, 3)])
            for it, q in sells.items():
                R['sell_batches_' + it] += q
            for d in range(0, 30, 3):
                shed = st[min(719, d * 24 + 12)][s]['observation']['private']['shed']
                for it in ITEMS: R['shed_' + it].append(shed.get(it, 0))
            # feeding on production days
            pf = pu = 0
            for d in range(3, 29):
                for row in st[d * 24 + 23][0]['observation']['farms'][s]['tiles']:
                    for t in row:
                        if isinstance(t, dict) and t.get('animal'):
                            dsf = (d + 1) - int(t['placed_day']) - FIRST[t['animal']]
                            if dsf >= 0 and dsf % INT[t['animal']] == 0:
                                pf += bool(t.get('fed_today')); pu += not t.get('fed_today')
            R['prod_day_feed_rate'].append(pf / max(1, pf + pu))
    out = {}
    for b, R in B.items():
        n = n_games[b]
        ab = collections.Counter()
        for g in R['animal_buys']:
            for k, v in g.items(): ab[k] += v
        pl = collections.Counter()
        for g in R['plants']:
            for k, v in g.items(): pl[k] += v
        fz = collections.Counter()
        for g in R['fertilize']:
            for k, v in g.items(): fz[k] += v
        hands = [sum(h[d] for h in R['hands_by_day']) / n for d in range(30)]
        out[b] = dict(games=n, final_cash=sum(R['final_cash']) / n,
                      animal_buys_per_game={k: round(v / n, 2) for k, v in sorted(ab.items(), key=lambda kv: (int(kv[0].split(':')[0]), kv[0]))},
                      land_day_hist=dict(collections.Counter(d for g in R['land_days'] for d in g)),
                      hands_by_day=[round(h, 1) for h in hands],
                      plants_per_game={k: round(v / n, 1) for k, v in sorted(pl.items(), key=lambda kv: (int(kv[0].split(':')[0]), kv[0])) if v / n >= 0.3},
                      fertilize_per_game={k: round(v / n, 1) for k, v in fz.most_common(12)},
                      animals_by_day=[{k: round(sum(g[i].get(k, 0) for g in R['animals_by_day']) / n, 1) for k in ('COW', 'SHEEP', 'GOOSE')} for i in range(10)],
                      prod_day_feed_rate=round(sum(R['prod_day_feed_rate']) / n, 3),
                      sell_batch_mean={it: round(sum(R['sell_batches_' + it]) / max(1, len(R['sell_batches_' + it])), 2) for it in ITEMS if R['sell_batches_' + it]},
                      shed_mean={it: round(sum(R['shed_' + it]) / max(1, len(R['shed_' + it])), 1) for it in ITEMS})
    os.makedirs(os.path.join(ROOT, 'o_results', 'proxy'), exist_ok=True)
    path = os.path.join(ROOT, 'o_results', 'proxy', f'{a.team.split()[0]}_policy.json')
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('wrote', path)
    for b, v in out.items():
        print(f"\n== {b} (n={v['games']}, cash {v['final_cash']:.0f}) feed-on-prod {v['prod_day_feed_rate']:.0%} hands d3/6/9/12 {v['hands_by_day'][3]}/{v['hands_by_day'][6]}/{v['hands_by_day'][9]}/{v['hands_by_day'][12]}")
        print('  animals by 3-day:', v['animals_by_day'])
        print('  animal buys/game:', v['animal_buys_per_game'])
        print('  land days:', v['land_day_hist'], '| sell batch:', v['sell_batch_mean'], '| shed:', v['shed_mean'])
        print('  fertilize:', v['fertilize_per_game'])
        print('  plants (>=0.3/game):', dict(list(v['plants_per_game'].items())[:24]))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
