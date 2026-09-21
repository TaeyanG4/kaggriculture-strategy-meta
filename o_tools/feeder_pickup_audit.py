"""Feeder wheat-flow audit for two planner candidates on pinned proxy worlds."""
import argparse, importlib.util, json, os, statistics, sys
os.environ['MPLBACKEND'] = 'Agg'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_agent(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return [v for k, v in vars(mod).items() if callable(v) and not k.startswith('__')][-1]

def run(path, opp, seed, seat, shops):
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    cand = load_agent(path, f'cand_{abs(hash(path))}_{seed}_{seat}')
    rival = load_agent(opp, f'opp_{abs(hash(path))}_{seed}_{seat}')
    original = engine._end_of_day
    def pinned(state, env, day):
        original(state, env, day)
        want = shops[:len(state[0].observation.town['unlocked_shops'])]
        if len(want) == len(state[0].observation.town['unlocked_shops']):
            state[0].observation.town['unlocked_shops'][:] = want
    engine._end_of_day = pinned
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        env.run([cand, rival] if seat == 0 else [rival, cand])
    finally:
        engine._end_of_day = original

    pickup_w = feed_cmd = care_cmd = buy_w = sell_w = 0
    for k in range(1, len(env.steps)):
        a = env.steps[k][seat].action or {}
        for cmd in [a.get('farmer')] + (a.get('hands') or []):
            if not cmd: continue
            if cmd[0] == 'PICKUP' and len(cmd) >= 3 and cmd[1] == 'WHEAT': pickup_w += int(cmd[2])
            elif cmd[0] == 'FEED': feed_cmd += 1
            elif cmd[0] == 'CARE': care_cmd += 1
        for order in a.get('market') or []:
            if len(order) >= 3 and order[1] == 'WHEAT':
                if order[0] == 'BUY_PRODUCT': buy_w += int(order[2])
                elif order[0] == 'SELL': sell_w += int(order[2])

    fed = cared = animals = end_inv_w = end_shed_w = 0
    day_rows = []
    for d in range(30):
        idx = min(len(env.steps)-1, d*24+23)
        o = env.steps[idx][seat].observation; f = o['farms'][seat]; p = o['private']
        an = [t for row in f['tiles'] for t in row if isinstance(t, dict) and t.get('animal')]
        fd = sum(1 for t in an if t.get('fed_today')); cr = sum(1 for t in an if t.get('cared_today'))
        iw = sum((iv or {}).get('WHEAT', 0) for iv in (p.get('inventories') or [])); sw = p['shed'].get('WHEAT', 0)
        fed += fd; cared += cr; animals += len(an); end_inv_w += iw; end_shed_w += sw
        day_rows.append((len(an), fd, cr, iw, sw))
    return dict(reward=env.steps[-1][seat].reward, pickup=pickup_w, feed=feed_cmd, care=care_cmd,
                buy=buy_w, sell=sell_w, fed=fed, cared=cared, animals=animals,
                end_inv=end_inv_w, end_shed=end_shed_w, daily=day_rows)

def summarize(name, rows):
    mean = lambda k: statistics.mean(r[k] for r in rows)
    animals = sum(r['animals'] for r in rows)
    print(f"{name}: cash={mean('reward'):.0f} pickupW={mean('pickup'):.1f} feedCmd={mean('feed'):.1f} careCmd={mean('care'):.1f} "
          f"buyW={mean('buy'):.1f} sellW={mean('sell'):.1f} feedCov={sum(r['fed'] for r in rows)/max(1,animals):.3f} "
          f"careCov={sum(r['cared'] for r in rows)/max(1,animals):.3f} h23InvWdaySum={mean('end_inv'):.1f} h23ShedWdaySum={mean('end_shed'):.1f}")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base', required=True); ap.add_argument('--cand', required=True)
    ap.add_argument('--opponent', default='agent/o227_stealth_drop.py'); ap.add_argument('--seeds', default='7000-7003')
    a=ap.parse_args(); lo,hi=map(int,a.seeds.split('-')); shops=json.load(open(os.path.join(ROOT,'o_results','proxy','shop_seq.json')))
    rb=[]; rc=[]
    for seed in range(lo,hi+1):
        for seat in (0,1):
            rb.append(run(a.base,a.opponent,seed,seat,shops[str(seed)])); rc.append(run(a.cand,a.opponent,seed,seat,shops[str(seed)]))
    summarize('BASE',rb); summarize('CAND',rc)
    for key in ('reward','pickup','feed','care','buy','sell','end_inv','end_shed'):
        ds=[c[key]-b[key] for b,c in zip(rb,rc)]; print(f"delta {key:8s} mean={statistics.mean(ds):+.1f} min={min(ds):+.1f} max={max(ds):+.1f}")
    for d in range(30):
        # only print days with a meaningful pickup/inventory coverage difference
        ba=statistics.mean(r['daily'][d][0] for r in rb); ca=statistics.mean(r['daily'][d][0] for r in rc)
        bf=statistics.mean(r['daily'][d][1] for r in rb); cf=statistics.mean(r['daily'][d][1] for r in rc)
        bi=statistics.mean(r['daily'][d][3] for r in rb); ci=statistics.mean(r['daily'][d][3] for r in rc)
        if abs(cf-bf)>=0.25 or abs(ci-bi)>=0.5:
            print(f"d{d:02d} animals {ba:.1f}->{ca:.1f} fed {bf:.1f}->{cf:.1f} invW {bi:.1f}->{ci:.1f}")
if __name__=='__main__': main()
