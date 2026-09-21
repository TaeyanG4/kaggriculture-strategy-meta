"""Current Elite Pool evaluation: our candidate plays against FROZEN elite opponents (their recorded actions replayed step by step)
in their own recent worlds (same seed -> same shops). Frozen opponents do not react, so absolute numbers are not live win rates;
use it PAIRED (candidate vs base) per (team, episode). Also keeps o227 as the dumper stress test via proxy_eval.
Usage: python o_tools/elite_pool.py --label <name> [--knobs ...] [--teams Unknown_Mother-Goose,Majkel1337,Boey,SpaTaro,DSM] [--per-team 40] [--workers 16]
       python o_tools/elite_pool.py --compare base19 <label>      (paired table per team + aggregate)
Output: o_results/elite_pool/eval_<label>.json = [{team, episode, our_cash, their_cash, recorded_their_cash}]"""
import argparse, copy, glob, json, os, statistics, sys
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
OUT = os.path.join(ROOT, 'o_results', 'elite_pool')
TEAMS = ['Unknown_Mother-Goose', 'Majkel1337', 'Boey', 'SpaTaro', 'DSM']


def play(args):
    path, team, knobs, b_path = args[:4]; us = args[4] if len(args) > 4 else None
    os.environ['PROXY_KNOBS'] = knobs; os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    r = json.load(open(path, encoding='utf-8')); names = r['info']['TeamNames']; tn = team.replace('_', ' ')
    seat = (1 - names.index(us)) if us else (names.index(tn) if tn in names else names.index(team)); steps = r['steps']   # --us: freeze whoever played against us in our own live replays
    shops = list(steps[-1][0]['observation']['town']['unlocked_shops'])
    B = load_agent(b_path, 'agB')

    def frozen(observation, configuration=None):
        k = int(observation['step']) + 1
        return copy.deepcopy(steps[k][seat]['action']) if k < len(steps) else {}
    orig = engine._end_of_day

    def pinned(state, env, day):
        orig(state, env, day); town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want
    engine._end_of_day = pinned
    env = make('kaggriculture', configuration={'seed': int(r['info'].get('seed') or 0) % (2 ** 31)}, debug=False)
    agents = [frozen, B] if seat == 0 else [B, frozen]
    fastgame.play(env, agents, deep=True)
    engine._end_of_day = orig
    ours = float(env.state[1 - seat].reward or 0); theirs = float(env.state[seat].reward or 0)
    return dict(team=team, episode=os.path.basename(path).split('-')[0], our_cash=ours, their_cash=theirs, recorded_their_cash=float(steps[-1][seat].get('reward') or 0), recorded_opp_cash=float(steps[-1][1 - seat].get('reward') or 0))


def compare(base, cand):
    B = {(x['team'], x['episode']): x for x in json.load(open(os.path.join(OUT, f'eval_{base}.json')))}
    C = {(x['team'], x['episode']): x for x in json.load(open(os.path.join(OUT, f'eval_{cand}.json')))}
    keys = sorted(k for k in B if k in C)
    print(f'{cand} vs {base} against frozen elite opponents (paired, n={len(keys)})')
    print('team                    n | own delta (se) | margin delta (se) | worse/better(>500) | wins base->cand | base own/their')
    allm = []; allo = []; wb = wc = 0
    for team in TEAMS + sorted({k[0] for k in keys} - set(TEAMS)):
        ks = [k for k in keys if k[0] == team]
        if not ks:
            continue
        do = [C[k]['our_cash'] - B[k]['our_cash'] for k in ks]; dm = [(C[k]['our_cash'] - C[k]['their_cash']) - (B[k]['our_cash'] - B[k]['their_cash']) for k in ks]
        w0 = sum(B[k]['our_cash'] > B[k]['their_cash'] for k in ks); w1 = sum(C[k]['our_cash'] > C[k]['their_cash'] for k in ks)
        se = lambda v: statistics.stdev(v) / len(v) ** 0.5 if len(v) > 1 else 0.0
        print(f"{team:23s} {len(ks):2d} | {statistics.mean(do):+6.0f} ({se(do):4.0f}) | {statistics.mean(dm):+6.0f} ({se(dm):4.0f}) | {sum(x < -500 for x in dm):2d}/{sum(x > 500 for x in dm):2d} | {w0:2d}->{w1:2d} | {statistics.mean(B[k]['our_cash'] for k in ks):.0f}/{statistics.mean(B[k]['their_cash'] for k in ks):.0f}")
        allm += dm; allo += do; wb += w0; wc += w1
    se = statistics.stdev(allm) / len(allm) ** 0.5 if len(allm) > 1 else 0.0
    print(f"POOL n={len(allm)} own {statistics.mean(allo):+.0f} margin {statistics.mean(allm):+.0f} (se {se:.0f}, {statistics.mean(allm) / max(1e-9, se):.1f} se) worse {sum(x < -500 for x in allm)} wins {wb}->{wc}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--label', default=''); ap.add_argument('--knobs', default=''); ap.add_argument('--teams', default=','.join(TEAMS))
    ap.add_argument('--per-team', type=int, default=40); ap.add_argument('--workers', type=int, default=16); ap.add_argument('--b', default='agent/p000_planner.py'); ap.add_argument('--dir', default='o_replays/elite_current')
    ap.add_argument('--compare', nargs=2, metavar=('BASE', 'CAND')); ap.add_argument('--us', default='', help='freeze the rival of this team name (our own live replays); teams = replay dir names')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.compare:
        compare(*a.compare); return
    jobs = []
    for team in a.teams.split(','):
        files = sorted(glob.glob(os.path.join(ROOT, a.dir, team, '*-replay.json')) or glob.glob(os.path.join(ROOT, a.dir, '*-replay.json')) if team == '.' else glob.glob(os.path.join(ROOT, a.dir, team, '*-replay.json')))[:a.per_team]
        jobs += [(f, team, a.knobs, a.b, a.us or None) for f in files]
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(play, jobs, chunksize=2))
    json.dump(res, open(os.path.join(OUT, f'eval_{a.label}.json'), 'w'), indent=0)
    for team in a.teams.split(','):
        rs = [x for x in res if x['team'] == team]
        if rs:
            print(f"{team:23s} n={len(rs):2d} ours {statistics.mean(x['our_cash'] for x in rs):7.0f} frozen {statistics.mean(x['their_cash'] for x in rs):7.0f} (recorded {statistics.mean(x['recorded_their_cash'] for x in rs):7.0f}) margin {statistics.mean(x['our_cash'] - x['their_cash'] for x in rs):+6.0f} wins {sum(x['our_cash'] > x['their_cash'] for x in rs)}/{len(rs)}")


if __name__ == '__main__':
    main()
