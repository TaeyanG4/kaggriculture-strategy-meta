"""Live-vs-local consistency audit: replay our live episodes with the rival's recorded actions frozen and our local agent file
acting, and report the first step where the local action differs from the action the live agent actually sent. Zero divergence
= the submitted code behaves exactly like the local file in that world (no timeout / exception / version drift); an early
divergence pins the live-only behaviour to a step.
Usage: python o_tools/live_replay_audit.py --sub 56319267 --agent state/o_dev/p000_base19.py [--dir o_replays/live_planner] [--fetch] [--workers 8] [--team Taeyang]
Output: one line per game + summary; JSON in o_results/live_audit_<sub>.json"""
import argparse, copy, glob, json, os, sys, time
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
REPLAY_URL = 'https://www.kaggleusercontent.com/episodes/{id}.json'


def norm(a):
    """Comparable form of an action dict (market list, farmer, hands)."""
    if not isinstance(a, dict):
        return ('none',)
    m = [list(o) for o in (a.get('market') or [])]
    f = list(a.get('farmer') or ['PASS'])
    h = [list(x) if isinstance(x, list) else x for x in (a.get('hands') or [])]
    return (json.dumps(m), json.dumps(f), json.dumps(h))


def play(args):
    path, team, agent_path = args
    os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    r = json.load(open(path, encoding='utf-8')); names = r['info']['TeamNames']; seat = names.index(team); opp = 1 - seat; steps = r['steps']
    shops = list(steps[-1][0]['observation']['town']['unlocked_shops'])
    B0 = load_agent(agent_path, 'agB')
    rec = {'first': None, 'n_div': 0, 'cats': {}}

    def ours(observation, configuration=None):
        a = B0(observation)
        k = int(observation['step']) + 1
        if k < len(steps):
            live = steps[k][seat].get('action')
            la, lb = norm(a), norm(live)
            if la != lb:
                cat = 'market' if la[0] != lb[0] else ('farmer' if la[1] != lb[1] else 'hands')
                rec['n_div'] += 1; rec['cats'][cat] = rec['cats'].get(cat, 0) + 1
                if rec['first'] is None:
                    rec['first'] = dict(step=k - 1, day=(k - 1) // 24, hour=(k - 1) % 24, cat=cat, local=(la[0] if cat == 'market' else (la[1] if cat == 'farmer' else la[2]))[:300], live=(lb[0] if cat == 'market' else (lb[1] if cat == 'farmer' else lb[2]))[:300])
        return a

    def frozen(observation, configuration=None):
        k = int(observation['step']) + 1
        return copy.deepcopy(steps[k][opp]['action']) if k < len(steps) else {}
    orig = engine._end_of_day

    def pinned(state, env, day):
        orig(state, env, day); town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want
    engine._end_of_day = pinned
    env = make('kaggriculture', configuration={'seed': int(r['info'].get('seed') or 0) % (2 ** 31)}, debug=False)
    fastgame.play(env, [ours, frozen] if seat == 0 else [frozen, ours], deep=True)
    engine._end_of_day = orig
    return dict(episode=os.path.basename(path).split('-')[0], seat=seat, opp=names[opp], rec_ours=float(steps[-1][seat].get('reward') or 0), rec_theirs=float(steps[-1][opp].get('reward') or 0),
                sim_ours=float(env.state[seat].reward or 0), sim_theirs=float(env.state[opp].reward or 0), first=rec['first'], n_div=rec['n_div'], cats=rec['cats'], shops=shops[:8])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--sub', required=True); ap.add_argument('--agent', required=True); ap.add_argument('--dir', default='o_replays/live_planner')
    ap.add_argument('--team', default='Taeyang'); ap.add_argument('--fetch', action='store_true'); ap.add_argument('--workers', type=int, default=8); ap.add_argument('--max', type=int, default=200)
    a = ap.parse_args()
    d = json.load(open(os.path.join(ROOT, 'o_results', f'live_episodes_{a.sub}.json'), encoding='utf-8'))
    eps = [e for e in d['episodes'] if e.get('state') == 'COMPLETED']; ids = [int(e['id']) for e in eps]
    os.makedirs(os.path.join(ROOT, a.dir), exist_ok=True)
    if a.fetch:
        import requests
        s = requests.Session(); s.headers['User-Agent'] = 'kaggriculture-strategy-meta live_replay_audit'; got = 0
        for eid in ids:
            p = os.path.join(ROOT, a.dir, f'{eid}-replay.json')
            if os.path.exists(p):
                continue
            rr = s.get(REPLAY_URL.format(id=eid), timeout=120)
            if rr.status_code == 200:
                open(p, 'wb').write(rr.content); got += 1; time.sleep(0.7)
            else:
                print(f'replay {eid} http {rr.status_code}')
        print(f'fetched {got} new replays')
    files = [os.path.join(ROOT, a.dir, f'{eid}-replay.json') for eid in ids if os.path.exists(os.path.join(ROOT, a.dir, f'{eid}-replay.json'))][:a.max]
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(play, [(f, a.team, a.agent) for f in files]))
    json.dump(res, open(os.path.join(ROOT, 'o_results', f'live_audit_{a.sub}.json'), 'w'), indent=0)
    clean = 0
    for x in sorted(res, key=lambda x: (x['first'] or {}).get('step', 10 ** 6)):
        f = x['first']
        if f is None:
            clean += 1
            print(f"{x['episode']} seat{x['seat']} vs {x['opp'][:18]:18s} IDENTICAL (ours {x['rec_ours']:.0f}={x['sim_ours']:.0f}, theirs {x['rec_theirs']:.0f}={x['sim_theirs']:.0f})")
        else:
            print(f"{x['episode']} seat{x['seat']} vs {x['opp'][:18]:18s} first div d{f['day']} h{f['hour']} [{f['cat']}] divs {x['n_div']} | rec ours {x['rec_ours']:.0f} sim {x['sim_ours']:.0f} | local {f['local'][:120]} | live {f['live'][:120]}")
    print(f"SUMMARY sub {a.sub}: {clean}/{len(res)} games identical; divergent first steps: {sorted((x['first'] or {}).get('step', -1) for x in res if x['first'])[:20]}")


if __name__ == '__main__':
    main()
