"""Live loss typology for our recent submissions (all losses, not only 2750+).
Fetches the public episode list per submission, downloads every loss replay once into
o_replays/live_recent/, and prints one line per loss: margin, rival rating, world bucket, whether
the rival farm is a lineage mirror, revenue gap by product, first purchase divergence.
Usage: python o_tools/live_losses.py [--subs N] [--sub 56241633 ...]
"""
import argparse, collections, json, os, subprocess, sys, time
import requests
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST_URL = 'https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
REPLAY_URL = 'https://www.kaggleusercontent.com/episodes/{id}.json'
MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
BASE = {'WHEAT': 25, 'CARROT': 35, 'TOMATO': 60, 'STRAWBERRY': 120, 'MELON': 250, 'EGG': 50, 'MILK': 160, 'WOOL': 200, 'FERTILIZER': 100}


def submissions(n):
    out = subprocess.run(['kaggle', 'competitions', 'submissions', '-c', 'kaggriculture'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
    return [l.split()[0] for l in out.splitlines() if l.strip() and l.split()[0].isdigit() and 'COMPLETE' in l][:n]


def world(shops):
    f2 = shops[:2]
    return 'yarn' if 'YARN_STORE' in f2 else ('goose', 'one_milk', 'two_milk')[sum(s in MILK for s in f2)]


def comp(farm):
    c = collections.Counter()
    for row in farm['tiles']:
        for x in row:
            if isinstance(x, dict) and (x.get('animal') or x.get('crop')):
                c[x.get('animal') or x.get('crop')] += 1
    return c


def revenue(rep, p):
    inc = collections.Counter()
    for t, st in enumerate(rep['steps'][:-1]):
        sh = st[p]['observation']['private']['shed']; nsh = rep['steps'][t + 1][p]['observation']['private']['shed']
        pr = st[0]['observation']['market']['prices']; a = st[p].get('action') or {}
        picked = {c[1] for c in [a.get('farmer')] + list(a.get('hands') or []) if c and c[0] == 'PICKUP' and len(c) > 1}
        for k in BASE:
            d = sh.get(k, 0) - nsh.get(k, 0)
            if d > 0 and k not in picked and t >= 24:
                inc[k] += d * pr[k]
    return inc


def analyse(rep, seat):
    riv = 1 - seat; shops = rep['steps'][-1][0]['observation']['town']['unlocked_shops']
    f = rep['steps'][480][0]['observation']['farms']; cm, cr = comp(f[seat]), comp(f[riv])
    mirror = all(cm[k] == cr[k] for k in ('COW', 'SHEEP', 'GOOSE', 'WHEAT', 'STRAWBERRY'))
    rm, rr = revenue(rep, seat), revenue(rep, riv)
    gap = {k: int(rm[k] - rr[k]) for k in BASE if abs(rm[k] - rr[k]) > 400}
    div = None
    for t, st in enumerate(rep['steps']):
        ba = [[o for o in ((st[p].get('action') or {}).get('market') or []) if o and o[0] in ('BUY_ANIMAL', 'BUY_LAND')] for p in (0, 1)]
        if ba[seat] != ba[riv]:
            div = (t // 24, ba[seat], ba[riv]); break
    an = lambda c: {k: c[k] for k in ('COW', 'SHEEP', 'GOOSE') if c[k]}
    return dict(world=world(shops), shops=shops[:4], mirror=mirror, me=an(cm), riv=an(cr), gap=gap, div=div, rival=rep['info']['TeamNames'][riv])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--subs', type=int, default=2); ap.add_argument('--sub', action='append')
    a = ap.parse_args(); subs = a.sub or submissions(a.subs)
    s = requests.Session(); s.headers['User-Agent'] = 'kaggriculture-strategy-meta live_losses'
    os.makedirs(os.path.join(ROOT, 'o_replays', 'live_recent'), exist_ok=True)
    for sid in subs:
        r = s.post(LIST_URL, json={'submissionId': int(sid)}, timeout=30); d = r.json()
        json.dump(d, open(os.path.join(ROOT, 'o_results', f'live_episodes_{sid}.json'), 'w', encoding='utf-8'))
        games = []; types = collections.Counter(); buckets = collections.defaultdict(lambda: [0, 0])
        eps = [e for e in d.get('episodes', []) if e.get('state') == 'COMPLETED']; t0 = time.time()
        print(f"submission {sid}: {len(eps)} completed episodes; scanning (replays are downloaded only for new losses)", flush=True)
        for n, e in enumerate(eps, 1):
            if n % 10 == 0 or n == len(eps):
                print(f"  {n}/{len(eps)} scanned, {len(games)} losses so far, {time.time()-t0:.0f}s", flush=True)
            ag = e['agents']; me = [x for x in ag if str(x.get('submissionId')) == str(sid)]; op = [x for x in ag if str(x.get('submissionId')) != str(sid)]
            if not me or not op or me[0].get('reward') is None or op[0].get('reward') is None:
                continue
            me, op = me[0], op[0]; rt = op.get('updatedScore') or 0
            b = '<2400' if rt < 2400 else ('2400-2749' if rt < 2750 else '2750+'); buckets[b][1] += 1; buckets[b][0] += me['reward'] > op['reward']
            if me['reward'] >= op['reward']:
                continue
            f = os.path.join(ROOT, 'o_replays', 'live_recent', f"{e['id']}-replay.json")
            if not os.path.exists(f):
                print(f"  downloading loss replay {e['id']} (vs {op.get('submissionId')}, r{round(rt)})", flush=True)
                rr = s.get(REPLAY_URL.format(id=e['id']), timeout=120)
                if rr.status_code != 200:
                    continue
                open(f, 'wb').write(rr.content); time.sleep(0.6)
            rep = json.load(open(f, encoding='utf-8')); info = analyse(rep, ag.index(me))
            games.append((int(me['reward'] - op['reward']), round(rt), e['id'], info))
        print(f"\n=== submission {sid}: {sum(v[1] for v in buckets.values())} games, {len(games)} losses | " + ', '.join(f'{k} {v[0]}/{v[1]}' for k, v in sorted(buckets.items())))
        for m, rt, eid, i in sorted(games):
            kind = 'mirror-noise' if i['mirror'] else ('bet-' + i['world'])
            types[kind] += 1
            print(f"{m:+6d} r{rt} {eid} {i['world']:8s} {i['shops']} | {'mirror' if i['mirror'] else 'me'+str(i['me'])+' riv'+str(i['riv'])} | gap {i['gap']} | 1st buy div {i['div']} | {i['rival'][:14]}")
        print('  types:', dict(types))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
