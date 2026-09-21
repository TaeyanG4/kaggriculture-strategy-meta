"""State-trajectory profile of a team from replays (or of our planner played in the same worlds), one schema for everyone:
checkpoints d0,1,3,5,6,9,12,15,18,24,27,29 (cash, hands at h12, land, herd, crop tiles, empty tiles) and three phases
d0-9 / d10-18 / d19-29 (wheat bought/sold, fertilizer collected/used/sold, per-product actual sell units + mean hour + realised
price, op counts incl. PASS, harvest units per crop, animal buy->place lag). Actual sales = min(order, shed + units placed that step).
Usage: python o_tools/elite_profile.py --team Unknown_Mother-Goose [--dir o_replays/elite_current] [--ours] [--workers 16] [--limit N]
  --ours also plays base19 (agent/p000_planner.py) vs o227 in the same worlds (both seats) and profiles it.
Output: o_results/elite_profile/<team>.json (+ <team>__ours.json) and a compact table."""
import argparse, collections, glob, json, os, statistics, sys
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
CROPS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON')
ANIMALS = ('COW', 'SHEEP', 'GOOSE')
OPS = ('PLANT', 'WATER', 'HARVEST', 'FEED', 'CARE', 'COLLECT_FERTILIZER', 'FERTILIZE', 'PASS', 'MOVE', 'PICKUP', 'PLACE')
CHECK = (0, 1, 3, 5, 6, 9, 12, 15, 18, 24, 27, 29)
PHASES = ((0, 9), (10, 18), (19, 29))


def phase_of(day):
    return 0 if day <= 9 else (1 if day <= 18 else 2)


class Recorder:
    def __init__(self):
        self.ck = {}   # day -> dict
        self.hands_mid = {}
        self.ph = [dict(buy_wheat=0.0, sell=collections.Counter(), sell_rev=collections.Counter(), sell_hour=collections.Counter(), ops=collections.Counter(),
                        harv_u=collections.Counter(), harv_n=collections.Counter(), plant=collections.Counter(), buy_seed=collections.Counter(), buy_animal=collections.Counter(), hires=0, land=0)
                   for _ in PHASES]
        self.buys = []; self.lags = []; self.prev_placed = None; self.escapes = 0; self.prev_animals = None

    def step(self, k, pre_farm, pre_priv, pre_prices, action, post_farm):
        """k = step index of the action (0-based), pre_* = state the action was computed on, post_farm = state after."""
        day = k // 24; hour = k % 24; P = self.ph[phase_of(day)]
        if not isinstance(action, dict):
            action = {}
        shed = dict(pre_priv.get('shed', {}) or {})
        cmds = [action.get('farmer')] + list(action.get('hands') or [])
        pos = [pre_farm.get('farmer')] + list(pre_farm.get('hands') or [])
        placed_now = collections.Counter()
        for i, c in enumerate(cmds):
            if not (isinstance(c, (list, tuple)) and c):
                continue
            op = c[0]
            if op in ('NORTH', 'SOUTH', 'EAST', 'WEST'):
                P['ops']['MOVE'] += 1; continue
            if op in P['ops'] or op in OPS:
                P['ops'][op] += 1
            if op == 'PLACE' and len(c) >= 3 and c[1] in PRODUCTS:
                placed_now[c[1]] += int(c[2])
            if op == 'PLANT' and len(c) > 1:
                P['plant'][c[1]] += 1
            if op == 'HARVEST' and i < len(pos) and pos[i] is not None:
                x, y = int(pos[i][0]), int(pos[i][1])
                try:
                    t = pre_farm['tiles'][y][x]
                except Exception:
                    t = None
                if isinstance(t, dict) and t.get('crop'):
                    P['harv_n'][t['crop']] += 1; P['harv_u'][t['crop']] += t.get('yield_units', 0)
        for o in action.get('market') or []:
            if not isinstance(o, (list, tuple)) or not o:
                continue
            if o[0] == 'HIRE':
                P['hires'] += 1
            elif o[0] == 'BUY_LAND':
                P['land'] += 1
            elif len(o) >= 3:
                q = int(o[2]); it = o[1]
                if o[0] == 'SELL' and it in PRODUCTS:
                    avail = shed.get(it, 0) + placed_now.get(it, 0)
                    u = max(0, min(q, avail)); shed[it] = avail - u
                    P['sell'][it] += u; P['sell_rev'][it] += u * pre_prices.get(it, 0); P['sell_hour'][it] += u * hour
                elif o[0] == 'BUY_PRODUCT' and it == 'WHEAT':
                    P['buy_wheat'] += min(q, 60)
                elif o[0] == 'BUY_SEED':
                    P['buy_seed'][it] += q
                elif o[0] == 'BUY_ANIMAL':
                    P['buy_animal'][it] += q
                    for _ in range(q):
                        self.buys.append(k)
        # placement lag / escapes from the herd count
        placed = sum(1 for row in post_farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal'))
        if self.prev_placed is not None:
            for _ in range(max(0, placed - self.prev_placed)):
                if self.buys:
                    b = self.buys.pop(0); self.lags.append((k - b, k // 24 - b // 24))
            if placed < self.prev_placed and hour == 23:
                self.escapes += self.prev_placed - placed
        self.prev_placed = placed
        if hour == 12:
            self.hands_mid[day] = len(post_farm.get('hands') or [])
        if hour == 23 and day in CHECK:
            an = collections.Counter(); cr = collections.Counter(); empty = 0
            for row in post_farm['tiles']:
                for t in row:
                    if t is None:
                        empty += 1
                    elif isinstance(t, dict):
                        if t.get('animal'):
                            an[t['animal']] += 1
                        elif t.get('crop'):
                            cr[t['crop']] += 1
            self.ck[day] = dict(cash=post_farm['money'], quads=len(post_farm['unlocked_quadrants']), hands=self.hands_mid.get(day, 0), empty=empty,
                                **{a: an[a] for a in ANIMALS}, **{c: cr[c] for c in CROPS})

    def result(self, final, opp_final, opp=''):
        return dict(ck=self.ck, ph=[{k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in p.items()} for p in self.ph],
                    lag_mean=statistics.mean(l[0] for l in self.lags) if self.lags else 0.0, lag_nextday=(sum(1 for l in self.lags if l[1] >= 1) / len(self.lags)) if self.lags else 0.0,
                    n_animals=len(self.lags), escapes=self.escapes, final=final, opp_final=opp_final, opp=opp)


def profile_replay(path, team):
    r = json.load(open(path, encoding='utf-8')); names = r['info'].get('TeamNames') or []
    tn = team.replace('_', ' ')
    if tn not in names and team not in names:
        return None
    seat = names.index(tn) if tn in names else names.index(team); steps = r['steps']
    rec = Recorder()
    for k in range(1, len(steps)):
        pre = steps[k - 1]; post = steps[k]
        rec.step(k - 1, pre[0]['observation']['farms'][seat], pre[seat]['observation'].get('private', {}), pre[0]['observation']['market']['prices'], post[seat].get('action'), post[0]['observation']['farms'][seat])
    fin = [s.get('reward') or 0 for s in steps[-1]]
    res = rec.result(fin[seat], fin[1 - seat], names[1 - seat]); res['shops'] = list(steps[-1][0]['observation']['town']['unlocked_shops']); res['seed'] = r['info'].get('seed'); res['id'] = os.path.basename(path).split('-')[0]
    return res


def play_ours(args):
    shops, seed, seat_b, a_path, b_path = args
    os.environ['PROXY_KNOBS'] = os.environ.get('PROXY_KNOBS', ''); os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
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
    rec = Recorder(); pre = {}

    def pre_hook(env, step):
        ob = env.state[0].observation
        pre['farm'] = json.loads(json.dumps(ob['farms'][seat_b])); pre['priv'] = json.loads(json.dumps(env.state[seat_b].observation['private'])); pre['prices'] = dict(ob['market']['prices'])

    def step_hook(env, step):
        rec.step(step, pre['farm'], pre['priv'], pre['prices'], env.state[seat_b].action, env.state[0].observation['farms'][seat_b])
    env = make('kaggriculture', configuration={'seed': int(seed or 0) % (2 ** 31)}, debug=False)
    fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, pre_hook=pre_hook, step_hook=step_hook)
    engine._end_of_day = orig
    return rec.result(float(env.state[seat_b].reward or 0), float(env.state[1 - seat_b].reward or 0), 'o227')


def mean_profiles(ps):
    n = len(ps); out = {'n': n, 'ck': {}, 'ph': []}
    for d in CHECK:
        rows = [p['ck'][str(d)] if str(d) in p['ck'] else p['ck'].get(d) for p in ps]; rows = [r for r in rows if r]
        if rows:
            out['ck'][d] = {k: statistics.mean(r.get(k, 0) for r in rows) for k in rows[0]}
    for i in range(3):
        agg = {}
        for key in ('sell', 'sell_rev', 'sell_hour', 'ops', 'harv_u', 'harv_n', 'plant', 'buy_seed', 'buy_animal'):
            c = collections.Counter()
            for p in ps:
                c.update(p['ph'][i].get(key, {}))
            agg[key] = {k: v / n for k, v in c.items()}
        for key in ('buy_wheat', 'hires', 'land'):
            agg[key] = statistics.mean(p['ph'][i].get(key, 0) for p in ps)
        out['ph'].append(agg)
    out['final'] = statistics.mean(p['final'] for p in ps); out['opp_final'] = statistics.mean(p['opp_final'] for p in ps)
    out['wins'] = sum(p['final'] > p['opp_final'] for p in ps) / n
    out['lag_mean'] = statistics.mean(p['lag_mean'] for p in ps); out['lag_nextday'] = statistics.mean(p['lag_nextday'] for p in ps); out['escapes'] = statistics.mean(p['escapes'] for p in ps)
    return out


def table(name, m):
    print(f"\n=== {name}: n={m['n']} final {m['final']:.0f} vs opp {m['opp_final']:.0f} (margin {m['final'] - m['opp_final']:+.0f}, wins {m['wins']:.0%}); animal buy->place lag {m['lag_mean']:.1f} steps, next-day {m['lag_nextday']:.0%}, escapes {m['escapes']:.2f}/game")
    print('day   cash  hands quad empty | cow shp gse | wheat straw tom car mel')
    for d in CHECK:
        c = m['ck'].get(d)
        if not c:
            continue
        print(f"d{d:2d} {c['cash']:7.0f} {c['hands']:5.1f} {c['quads']:4.1f} {c['empty']:5.1f} | {c['COW']:3.1f} {c['SHEEP']:3.1f} {c['GOOSE']:3.1f} | {c['WHEAT']:5.1f} {c['STRAWBERRY']:5.1f} {c['TOMATO']:3.1f} {c['CARROT']:3.1f} {c['MELON']:3.1f}")
    for i, (a, b) in enumerate(PHASES):
        p = m['ph'][i]
        sells = ' '.join(f"{k[:4]}{v:.0f}@{p['sell_rev'][k] / max(1e-9, v):.0f}/h{p['sell_hour'][k] / max(1e-9, v):.0f}" for k, v in sorted(p['sell'].items(), key=lambda kv: -kv[1]) if v >= 1)
        ops = ' '.join(f"{k[:4]}{v:.0f}" for k, v in sorted(p['ops'].items()) if v >= 1)
        harv = ' '.join(f"{k[:4]}{p['harv_u'][k] / max(1e-9, p['harv_n'][k]):.1f}x{p['harv_n'][k]:.0f}" for k in CROPS if p['harv_n'].get(k, 0) >= 1)
        print(f"d{a}-{b}: wheat bought {p['buy_wheat']:.0f} | sold units@price/hour: {sells}")
        print(f"        ops: {ops} | harvest u/tile x n: {harv} | plants {dict((k[:4], round(v)) for k, v in p['plant'].items())} | animals bought {dict((k, round(v, 1)) for k, v in p['buy_animal'].items())} land {p['land']:.1f}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--team', required=True); ap.add_argument('--dir', default='o_replays/elite_current'); ap.add_argument('--ours', action='store_true')
    ap.add_argument('--workers', type=int, default=16); ap.add_argument('--limit', type=int, default=0); ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, a.dir, a.team, '*-replay.json')))
    if a.limit:
        files = files[:a.limit]
    ps = [p for p in (profile_replay(f, a.team) for f in files) if p]
    os.makedirs(os.path.join(ROOT, 'o_results', 'elite_profile'), exist_ok=True)
    json.dump(ps, open(os.path.join(ROOT, 'o_results', 'elite_profile', f'{a.team}{a.tag}.json'), 'w'))
    m = mean_profiles(ps); table(a.team, m)
    if a.ours:
        jobs = [(p['shops'], p['seed'], seat, a.a, a.b) for p in ps for seat in (0, 1)]
        with ProcessPoolExecutor(a.workers) as ex:
            ours = list(ex.map(play_ours, jobs, chunksize=2))
        json.dump(ours, open(os.path.join(ROOT, 'o_results', 'elite_profile', f'{a.team}{a.tag}__ours.json'), 'w'))
        table(f'base19 in {a.team} worlds (vs o227)', mean_profiles(ours))


if __name__ == '__main__':
    main()
