"""Report for o_tools/oracle.py output: full-info oracle gain, matched-null gain, full - null, 1-/2-day selector recovery,
choice frequencies, share of worlds with >= 3k/5k gain, and choice consistency by world type.
Usage: python o_tools/oracle_report.py o_results/oracle/orc_sel.json"""
import json, sys, statistics, collections


def margin(br):
    return br['b'] - br['a']


def bucket(shops):
    s = shops[:3]; m = sum(x in ('ICE_CREAM_SHOP', 'SMOOTHIE_SHOP', 'PIZZA_SHOP') for x in s); y = sum(x == 'YARN_STORE' for x in s)
    return 'yarn' if y >= 2 else f'milk{m}'


def main(path):
    res = json.load(open(path))
    fam = {'strat': {}, 'null': {}}
    for ch in res:
        fam[ch['family']][(ch['seed'], ch['seat_b'])] = ch
    keys = sorted(set(fam['strat']) & set(fam['null']))
    gains = {}
    for f in ('strat', 'null'):
        gains[f] = {k: margin(fam[f][k]['stages'][-1]['branches'][[b['name'] for b in fam[f][k]['stages'][-1]['branches']].index(fam[f][k]['stages'][-1]['best'])]) - (fam[f][k]['base']['b'] - fam[f][k]['base']['a']) for k in keys}
    own = {f: {k: fam[f][k]['stages'][-1]['branches'][[b['name'] for b in fam[f][k]['stages'][-1]['branches']].index(fam[f][k]['stages'][-1]['best'])]['b'] - fam[f][k]['base']['b'] for k in keys} for f in ('strat', 'null')}
    n = len(keys)
    def ms(v): return f"{statistics.mean(v):+6.0f} (se {statistics.stdev(v) / len(v) ** 0.5:4.0f})" if len(v) > 1 else f"{v[0]:+6.0f}"
    print(f"worlds (seed,seat) n={n}")
    print(f"full-info oracle margin gain   {ms(list(gains['strat'].values()))} | own {ms(list(own['strat'].values()))}")
    print(f"matched-null oracle margin gain {ms(list(gains['null'].values()))} | own {ms(list(own['null'].values()))}")
    diff = [gains['strat'][k] - gains['null'][k] for k in keys]
    print(f"full - null (pure strategy)     {ms(diff)}")
    for thr in (3000, 5000):
        print(f"  worlds with strat gain >= {thr}: {sum(1 for k in keys if gains['strat'][k] >= thr)}/{n} | strat-null >= {thr}: {sum(1 for x in diff if x >= thr)}/{n}")
    # selector recovery per stage node: pick by 1-/2-day margin (money at day D+h end) vs ex-post best
    rec = {1: [], 2: []}; avail = 0; nodes = 0
    for k in keys:
        for stg in fam['strat'][k]['stages']:
            D = stg['day']; brs = stg['branches']; keep = [b for b in brs if b['name'] == 'KEEP'][0]
            best = max(brs, key=margin)
            gain = margin(best) - margin(keep); nodes += 1
            if gain <= 0:
                continue
            avail += gain
            for h in (1, 2):
                d2 = min(29, D + h)
                pick = max(brs, key=lambda b: (b['money_b'][d2] - b['money_a'][d2]))
                rec[h].append((margin(pick) - margin(keep)) / gain)
    print(f"stage nodes {nodes}, nodes with available gain {len(rec[1])}, total available margin {avail:+.0f} ({avail / n:+.0f}/world)")
    for h in (1, 2):
        if rec[h]:
            print(f"  {h}-day selector recovery: mean {statistics.mean(rec[h]):+.2f} of the node gain, picks the ex-post best in {sum(1 for x in rec[h] if x >= 0.999)}/{len(rec[h])} nodes, negative in {sum(1 for x in rec[h] if x < 0)}")
    # choice frequencies and consistency by bucket
    print("choice frequency by stage (strat):")
    for i, D in enumerate([6, 9, 12, 15, 18]):
        c = collections.Counter(fam['strat'][k]['stages'][i]['best'] for k in keys)
        by = collections.defaultdict(collections.Counter)
        for k in keys:
            stg = fam['strat'][k]['stages'][i]; keep = [b for b in stg['branches'] if b['name'] == 'KEEP'][0]
            by[bucket(keep['feats']['shops'])][stg['best']] += 1
        cons = ' '.join(f"{bk}:{cnt.most_common(1)[0][0]}({cnt.most_common(1)[0][1]}/{sum(cnt.values())})" for bk, cnt in sorted(by.items()))
        print(f"  d{D:2d} " + ' '.join(f"{nm}:{v}" for nm, v in c.most_common()) + f" | by bucket: {cons}")
    # per-world table
    print("per world: strat gain / null gain / strat-null (seat-averaged)")
    seeds = sorted({k[0] for k in keys})
    for s in seeds:
        ks = [k for k in keys if k[0] == s]
        sg = statistics.mean(gains['strat'][k] for k in ks); ng = statistics.mean(gains['null'][k] for k in ks)
        sh = fam['strat'][ks[0]]['stages'][0]['branches'][0]['feats']['shops']
        print(f"  {s} {sg:+7.0f} {ng:+7.0f} {sg - ng:+7.0f}  " + ' '.join(x[:5] for x in sh[:5]))


if __name__ == '__main__':
    main(sys.argv[1])
