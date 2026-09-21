"""Quantity-based gap decomposition against a leader's archived games. For every replay of the team, the world's shop sequence
is pinned and our planner plays it against the tape (both seats); the leader's own numbers come from the replay. Compared per
world: units sold by product and 5-day window, herd / crop-tile / hand / cash trajectories, fertilize-water-harvest counts.
Quantities are opponent-independent (prices are not: the leader's opponents differ), so the gap is read in units and tiles.
Usage: python o_tools/leader_gap.py [--team Majkel1337] [--dir o_replays/leader_archive] [--workers 16] [--limit N] [--knobs ...]
Output: o_results/leader_gap/<team>.json and a table (overall + per bucket)."""
import argparse, collections, glob, json, os, sys
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
CROPS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON')
ANIMALS = ('COW', 'SHEEP', 'GOOSE')
OPS = ('FERTILIZE', 'WATER', 'HARVEST', 'FEED', 'CARE', 'COLLECT_FERTILIZER', 'PLANT', 'PASS')
MILK = {'PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'}
DAYS = (5, 9, 12, 15, 18, 21, 24, 27, 29)


def bucket(shops):
    return 'yarn' if 'YARN_STORE' in shops[:2] else 'milk%d' % min(3, sum(s in MILK for s in shops[:3]))


def new_stats():
    return {'units': {p: [0.0] * 6 for p in PRODUCTS}, 'rev': {p: [0.0] * 6 for p in PRODUCTS}, 'ops': {o: [0] * 6 for o in OPS},
            'buy_wheat': [0.0] * 6, 'hires': 0, 'cash': {}, 'animals': {}, 'crops': {}, 'hands': {}, 'quads': {}, 'final': 0.0,
            'plant': {c: 0.0 for c in CROPS}, 'harv': {c: 0.0 for c in CROPS}, 'harv_u': {c: 0.0 for c in CROPS}, 'water': {c: 0.0 for c in CROPS}, 'fert': {c: 0.0 for c in CROPS},
            'wheat_age': [0.0] * 8, 'regap': [0.0] * 8, 'empty_tiles': {}}   # wheat harvest age histogram; hours between a harvest and the next PLANT on that tile (0-7+ x 24h bins); empty crop tiles by day


def farm_day(st, farm, day):
    an = collections.Counter(); cr = collections.Counter()
    for row in farm['tiles']:
        for t in row:
            if isinstance(t, dict):
                if t.get('animal'):
                    an[t['animal']] += 1
                elif t.get('crop'):
                    cr[t['crop']] += 1
    st['cash'][day] = farm['money']; st['animals'][day] = dict(an); st['crops'][day] = dict(cr)
    st['empty_tiles'][day] = sum(1 for row in farm['tiles'] for t in row if t is None)
    st['hands'][day] = len(farm.get('hands', []) or []); st['quads'][day] = len(farm['unlocked_quadrants'])


def record_action(st, action, prices, day, farm=None, step=None):
    if not isinstance(action, dict):
        return
    w = min(5, day // 5)
    if farm is not None:   # per-crop plant / harvest (units on the tile) / water / fertilize, from the unit positions before the step
        pos = [farm.get('farmer')] + list(farm.get('hands') or [])
        emptied = st.setdefault('_emptied', {})
        for i, cmd in enumerate([action.get('farmer')] + list(action.get('hands') or [])):
            if not (isinstance(cmd, (list, tuple)) and cmd) or i >= len(pos) or pos[i] is None:
                continue
            if cmd[0] == 'PLANT' and len(cmd) > 1 and cmd[1] in st['plant']:
                st['plant'][cmd[1]] += 1
                key = (int(pos[i][0]), int(pos[i][1]))
                if step is not None and key in emptied and farm['tiles'][key[1]][key[0]] is None:
                    st['regap'][min(7, (step - emptied.pop(key)) // 24)] += 1
                continue
            if cmd[0] not in ('HARVEST', 'WATER', 'FERTILIZE'):
                continue
            x, y = int(pos[i][0]), int(pos[i][1]); t = farm['tiles'][y][x] if 0 <= y < len(farm['tiles']) and 0 <= x < len(farm['tiles'][y]) else None
            if cmd[0] == 'HARVEST' and isinstance(t, dict) and t.get('crop') == 'WHEAT':
                st['wheat_age'][min(7, day - int(t.get('planted_day', day)))] += 1
                if step is not None:
                    emptied[(x, y)] = step
            if isinstance(t, dict) and t.get('crop') in st['plant']:
                if cmd[0] == 'HARVEST':
                    if not t.get('watered_today') and 'WATER' in [c[0] for c in [action.get('farmer')] + list(action.get('hands') or []) if isinstance(c, (list, tuple)) and c]:
                        pass
                    st['harv'][t['crop']] += 1; st['harv_u'][t['crop']] += t.get('yield_units', 0)
                elif cmd[0] == 'WATER':
                    st['water'][t['crop']] += 1
                else:
                    st['fert'][t['crop']] += 1
    for o in action.get('market') or []:
        if not isinstance(o, (list, tuple)) or len(o) < 2:
            continue
        if o[0] == 'SELL' and o[1] in PRODUCTS and len(o) >= 3:
            st['units'][o[1]][w] += float(o[2]); st['rev'][o[1]][w] += float(o[2]) * prices.get(o[1], 0)
        elif o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT' and len(o) >= 3:
            st['buy_wheat'][w] += float(o[2])
        elif o[0] == 'HIRE':
            st['hires'] += 1
    for cmd in [action.get('farmer')] + list(action.get('hands') or []):
        if isinstance(cmd, (list, tuple)) and cmd and cmd[0] in st['ops']:
            st['ops'][cmd[0]][w] += 1


def leader_from_replay(path, team):
    r = json.load(open(path, encoding='utf-8'))
    names = r.get('info', {}).get('TeamNames') or []
    if team not in names:
        return None
    seat = names.index(team); steps = r['steps']
    shops = list(steps[-1][0]['observation']['town']['unlocked_shops'])
    st = new_stats()
    for k, s in enumerate(steps):
        ob = s[0]['observation']; day = k // 24
        if k > 0:   # steps[k].action produced state k: it answers the observation of step k-1
            pre = steps[k - 1][0]['observation']
            record_action(st, s[seat].get('action'), pre['market']['prices'], (k - 1) // 24, pre['farms'][seat], k - 1)
        if k % 24 == 23:
            farm_day(st, ob['farms'][seat], day)
    st['final'] = float(steps[-1][seat].get('reward') or 0.0); opp = float(steps[-1][1 - seat].get('reward') or 0.0)
    return dict(id=os.path.basename(path).split('-')[0], seat=seat, shops=shops, seed=r.get('info', {}).get('seed'), opp=names[1 - seat], opp_final=opp, stats=st)


def play_world(args):
    """Our planner (seat_b) vs the tape in the pinned world; returns our stats."""
    shops, seed, seat_b, knobs, a_path, b_path = args
    os.environ['PROXY_KNOBS'] = knobs; os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    orig = engine._end_of_day

    def pinned(state, env, day):
        orig(state, env, day); town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want
    engine._end_of_day = pinned
    st = new_stats()

    def step_hook(env, step):
        record_action(st, env.state[seat_b].action, pre['prices'], step // 24, pre['farm'], step)

    pre = {'farm': None, 'prices': None}

    def pre_hook(env, step):   # state before the step: unit positions / tile yields the actions refer to, pre-sale prices
        ob = env.state[0].observation
        pre['farm'] = json.loads(json.dumps(ob['farms'][seat_b])); pre['prices'] = dict(ob['market']['prices'])

    def day_hook(env, day):
        farm_day(st, env.state[0].observation['farms'][seat_b], day)
    env = make('kaggriculture', configuration={'seed': int(seed or 0) % (2 ** 31)}, debug=False)
    fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, day_hook=day_hook, step_hook=step_hook, pre_hook=pre_hook)
    engine._end_of_day = orig
    st['final'] = float(env.state[seat_b].reward or 0.0); st['opp_final'] = float(env.state[1 - seat_b].reward or 0.0)
    return st


def mean_stats(lst):
    """Element-wise mean of a list of stats dicts (per-day dicts averaged over the games that have the day)."""
    out = new_stats(); n = len(lst)
    for p in PRODUCTS:
        for w in range(6):
            out['units'][p][w] = sum(s['units'][p][w] for s in lst) / n; out['rev'][p][w] = sum(s['rev'][p][w] for s in lst) / n
    for o in OPS:
        for w in range(6):
            out['ops'][o][w] = sum(s['ops'][o][w] for s in lst) / n
    out['buy_wheat'] = [sum(s['buy_wheat'][w] for s in lst) / n for w in range(6)]
    out['hires'] = sum(s['hires'] for s in lst) / n; out['final'] = sum(s['final'] for s in lst) / n
    for key in ('plant', 'harv', 'harv_u', 'water', 'fert'):
        out[key] = {c: sum(s.get(key, {}).get(c, 0.0) for s in lst) / n for c in CROPS}
    out['opp_final'] = sum(s.get('opp_final', 0.0) for s in lst) / n
    for key in ('wheat_age', 'regap'):
        out[key] = [sum(s.get(key, [0] * 8)[i] for s in lst) / n for i in range(8)]
    for key in ('cash', 'hands', 'quads', 'empty_tiles'):
        out[key] = {d: sum(s[key].get(d, s[key].get(str(d), 0)) for s in lst) / n for d in DAYS}
    for key, names in (('animals', ANIMALS), ('crops', CROPS)):
        out[key] = {d: {k: sum((s[key].get(d) or s[key].get(str(d)) or {}).get(k, 0) for s in lst) / n for k in names} for d in DAYS}
    return out


def table(L, O, title):
    print(f"\n=== {title}: leader final {L['final']:.0f} (opp {L['opp_final']:.0f}) | ours {O['final']:.0f} (tape {O['opp_final']:.0f}) | gap {O['final'] - L['final']:+.0f}")
    print('units sold by 5-day window (leader | ours):')
    for p in PRODUCTS:
        lu = L['units'][p]; ou = O['units'][p]
        print(f"  {p:11s} L " + ' '.join(f"{x:5.0f}" for x in lu) + f" = {sum(lu):5.0f} | O " + ' '.join(f"{x:5.0f}" for x in ou) + f" = {sum(ou):5.0f}  d {sum(ou) - sum(lu):+6.0f}"
              + f"  (L rev {sum(L['rev'][p]):6.0f} @{(sum(L['rev'][p]) / max(1, sum(lu))):4.0f} | O rev {sum(O['rev'][p]):6.0f} @{(sum(O['rev'][p]) / max(1, sum(ou))):4.0f})")
    print('ops per window (leader | ours): ' + '; '.join(f"{o} {sum(L['ops'][o]):.0f}|{sum(O['ops'][o]):.0f}" for o in OPS) + f"; wheat bought {sum(L['buy_wheat']):.0f}|{sum(O['buy_wheat']):.0f}; hires {L['hires']:.1f}|{O['hires']:.1f}")
    print('per crop (leader | ours): ' + '; '.join(f"{c[:5]} plant {L['plant'][c]:.0f}|{O['plant'][c]:.0f} harv {L['harv'][c]:.0f}|{O['harv'][c]:.0f} u/h {L['harv_u'][c] / max(1, L['harv'][c]):.2f}|{O['harv_u'][c] / max(1, O['harv'][c]):.2f} water {L['water'][c]:.0f}|{O['water'][c]:.0f} fert {L['fert'][c]:.0f}|{O['fert'][c]:.0f}" for c in CROPS))
    print('wheat harvest age hist (L|O): ' + ' '.join(f"a{i}:{L['wheat_age'][i]:.0f}|{O['wheat_age'][i]:.0f}" for i in range(8)) + ' ; replant gap days after a wheat harvest (L|O): ' + ' '.join(f"{i}:{L['regap'][i]:.0f}|{O['regap'][i]:.0f}" for i in range(8)))
    print('day    ' + ' '.join(f"{d:>26d}" for d in DAYS))
    print('empty  ' + ' '.join(f"{L['empty_tiles'][d]:>12.1f}|{O['empty_tiles'][d]:<12.1f}" for d in DAYS))
    print('cash   ' + ' '.join(f"{L['cash'][d]:>12.0f}|{O['cash'][d]:<12.0f}" for d in DAYS))
    print('hands  ' + ' '.join(f"{L['hands'][d]:>12.1f}|{O['hands'][d]:<12.1f}" for d in DAYS))
    for k in ANIMALS:
        print(f"{k:6s} " + ' '.join(f"{L['animals'][d][k]:>12.1f}|{O['animals'][d][k]:<12.1f}" for d in DAYS))
    for k in CROPS:
        print(f"{k[:6]:6s} " + ' '.join(f"{L['crops'][d][k]:>12.1f}|{O['crops'][d][k]:<12.1f}" for d in DAYS))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--team', default='Majkel1337'); ap.add_argument('--dir', default='o_replays/leader_archive')
    ap.add_argument('--workers', type=int, default=16); ap.add_argument('--limit', type=int, default=0); ap.add_argument('--knobs', default='')
    ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py'); ap.add_argument('--tag', default='')
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, a.dir, '*-replay.json')))
    leaders = [x for x in (leader_from_replay(f, a.team) for f in files) if x]
    if a.limit:
        leaders = leaders[:a.limit]
    print(f'{len(leaders)} {a.team} games parsed; running our planner on the same worlds ({2 * len(leaders)} games, {a.workers} workers)', flush=True)
    jobs = [(g['shops'], g['seed'], seat, a.knobs, a.a, a.b) for g in leaders for seat in (0, 1)]
    with ProcessPoolExecutor(a.workers) as ex:
        ours = list(ex.map(play_world, jobs, chunksize=2))
    per_game = []
    for i, g in enumerate(leaders):
        o = mean_stats(ours[2 * i:2 * i + 2]); o['finals'] = [ours[2 * i]['final'], ours[2 * i + 1]['final']]
        per_game.append(dict(id=g['id'], shops=g['shops'], bucket=bucket(g['shops']), opp=g['opp'], leader=g['stats'], leader_opp_final=g['opp_final'], ours=o))
    os.makedirs(os.path.join(ROOT, 'o_results', 'leader_gap'), exist_ok=True)
    out = os.path.join(ROOT, 'o_results', 'leader_gap', f"{a.team}{a.tag}.json")
    for g in per_game:
        g['leader'].pop('_emptied', None); g['ours'].pop('_emptied', None)
    json.dump(per_game, open(out, 'w'), indent=0)
    for g in per_game:
        g['leader']['opp_final'] = g['leader_opp_final']
    table(mean_stats([g['leader'] for g in per_game]), mean_stats([g['ours'] for g in per_game]), f'ALL ({len(per_game)} worlds)')
    for b in sorted({g['bucket'] for g in per_game}):
        gs = [g for g in per_game if g['bucket'] == b]
        table(mean_stats([g['leader'] for g in gs]), mean_stats([g['ours'] for g in gs]), f'{b} ({len(gs)} worlds)')
    print('saved', out)


if __name__ == '__main__':
    main()
