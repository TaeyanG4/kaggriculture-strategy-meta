"""Hour-level cash-flow trace of the leader (from an archived replay) against our planner in the same pinned world, for the d0-d9
build: per step cash, market orders (buys/sells/hires with the price at that step), and the day-end farm state. Prints an aligned
table for the hours where either side acted, then the first cash divergences with their causes.
Usage: python o_tools/cash_trace.py --replay o_replays/leader_archive/<id>-replay.json [--team Majkel1337] [--days 9] [--seat 0] [--knobs ...]
       python o_tools/cash_trace.py --replay ... --summary     (per-day purchase/sale summary only)"""
import argparse, collections, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
SEED = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
ANIMAL = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}


def farm_summary(farm):
    c = collections.Counter()
    for row in farm['tiles']:
        for t in row:
            if isinstance(t, dict):
                c[t.get('animal') or t.get('crop') or t.get('kind')] += 1
    an = {k: c[k] for k in ('COW', 'SHEEP', 'GOOSE') if c[k]}; cr = {k: c[k] for k in ('WHEAT', 'MELON', 'STRAWBERRY', 'CARROT', 'TOMATO') if c[k]}
    return an, cr


def fmt_orders(orders, prices):
    out = []
    hires = sum(1 for o in orders if isinstance(o, list) and o and o[0] == 'HIRE')
    for o in orders:
        if not isinstance(o, list) or not o:
            continue
        if o[0] == 'HIRE':
            continue
        if o[0] == 'BUY_LAND':
            out.append('LAND'); continue
        if len(o) >= 3:
            q = int(o[2]); it = o[1]
            if o[0] == 'SELL':
                out.append(f"S:{it[:4]}{q}@{prices.get(it, 0)}")
            elif o[0] == 'BUY_PRODUCT':
                out.append(f"B:{it[:4]}{q}@{prices.get(it, 0)}")
            elif o[0] == 'BUY_SEED':
                out.append(f"seed:{it[:4]}{q}")
            elif o[0] == 'BUY_ANIMAL':
                out.append(f"{it[:3]}x{q}")
    if hires:
        out.append(f"HIRE{hires}")
    return ' '.join(out)


def leader_trace(path, team, days):
    r = json.load(open(path, encoding='utf-8')); names = r['info'].get('TeamNames') or []
    seat = names.index(team); steps = r['steps']
    shops = list(steps[-1][0]['observation']['town']['unlocked_shops'])
    rows = {}
    for k in range(1, min(len(steps), days * 24 + 1)):
        pre = steps[k - 1][0]['observation']; post = steps[k][0]['observation']
        act = steps[k][seat].get('action') or {}
        orders = act.get('market') or [] if isinstance(act, dict) else []
        rows[k - 1] = dict(cash_pre=pre['farms'][seat]['money'], cash_post=post['farms'][seat]['money'], orders=orders, prices=dict(pre['market']['prices']),
                           hands=len(post['farms'][seat].get('hands') or []), farm=farm_summary(post['farms'][seat]), quads=len(post['farms'][seat]['unlocked_quadrants']))
    return shops, rows, r['info'].get('seed'), names[1 - seat]


def our_trace(shops, seed, seat_b, days, a_path, b_path):
    os.environ.setdefault('MPLBACKEND', 'Agg'); os.chdir(ROOT)
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
    rows = {}; pre = {}

    def pre_hook(env, step):
        ob = env.state[0].observation; pre['cash'] = ob['farms'][seat_b]['money']; pre['prices'] = dict(ob['market']['prices'])

    def step_hook(env, step):
        if step >= days * 24:
            return
        ob = env.state[0].observation; act = env.state[seat_b].action or {}
        rows[step] = dict(cash_pre=pre['cash'], cash_post=ob['farms'][seat_b]['money'], orders=act.get('market') or [], prices=pre['prices'],
                          hands=len(ob['farms'][seat_b].get('hands') or []), farm=farm_summary(ob['farms'][seat_b]), quads=len(ob['farms'][seat_b]['unlocked_quadrants']))
    env = make('kaggriculture', configuration={'seed': int(seed or 0) % (2 ** 31)}, debug=False)
    fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, step_hook=step_hook, pre_hook=pre_hook)
    engine._end_of_day = orig
    return rows, [x.reward for x in env.state]


def day_summary(rows, d):
    buys = collections.Counter(); sells = collections.Counter(); spend = 0.0; income = 0.0
    for k in range(d * 24, d * 24 + 24):
        r = rows.get(k)
        if not r:
            continue
        for o in r['orders']:
            if not isinstance(o, list) or not o:
                continue
            if o[0] == 'HIRE':
                buys['hire'] += 1
            elif o[0] == 'BUY_LAND':
                buys['land'] += 1
            elif len(o) >= 3:
                q = int(o[2])
                if o[0] == 'SELL':
                    sells[o[1][:4]] += q
                elif o[0] == 'BUY_PRODUCT':
                    buys['P:' + o[1][:4]] += q
                elif o[0] == 'BUY_SEED':
                    buys['s:' + o[1][:4]] += q
                elif o[0] == 'BUY_ANIMAL':
                    buys[o[1][:3]] += q
        dc = r['cash_post'] - r['cash_pre']
        if dc > 0:
            income += dc
        else:
            spend -= dc
    return buys, sells, income, spend


def sales_buys(rows, d, prices_by_step=None):
    """Per-day revenue and spend by category from the order stream, valued at the pre-step price (units x price; hires by fib)."""
    rev = collections.Counter(); spend = collections.Counter(); hires = 0
    for k in range(d * 24, d * 24 + 24):
        r = rows.get(k)
        if not r:
            continue
        for o in r['orders']:
            if not isinstance(o, list) or not o:
                continue
            if o[0] == 'HIRE':
                spend['hire'] += FIB[min(hires, 13)]; hires += 1
            elif o[0] == 'BUY_LAND':
                spend['land'] += 1000
            elif len(o) >= 3:
                q = int(o[2]); it = o[1]
                if o[0] == 'SELL':
                    rev[it[:4]] += q * r['prices'].get(it, 0)
                elif o[0] == 'BUY_PRODUCT':
                    spend['P:' + it[:4]] += q * r['prices'].get(it, 0)
                elif o[0] == 'BUY_SEED':
                    spend['s:' + it[:4]] += q * SEED.get(it, 0)
                elif o[0] == 'BUY_ANIMAL':
                    spend[it[:3]] += q * ANIMAL.get(it, 0)
    return rev, spend


def aggregate(files, team, days, seat, a_path, b_path, workers):
    """Mean per-day revenue/spend by category and day-end state, leader vs ours, over many worlds."""
    from concurrent.futures import ProcessPoolExecutor
    Ls = []; args = []
    for f in files:
        try:
            shops, L, seed, opp = leader_trace(f, team, days)
        except Exception:
            continue
        Ls.append(L); args.append((shops, seed, seat, days, a_path, b_path))
    with ProcessPoolExecutor(workers) as ex:
        Os = [o for o, _ in ex.map(_our_trace_star, args)]
    n = len(Ls)
    print(f'{n} worlds; per-day means (leader | ours): revenue by product, spend by category, day-end cash / hands / animals / strawberries / wheat tiles')
    for d in range(days + 1):
        R = [collections.Counter(), collections.Counter()]; S = [collections.Counter(), collections.Counter()]; cash = [0.0, 0.0]; an = [0.0, 0.0]; st = [0.0, 0.0]; wh = [0.0, 0.0]; ml = [0.0, 0.0]
        for i, rowsets in enumerate((Ls, Os)):
            for rows in rowsets:
                rev, sp = sales_buys(rows, d); R[i].update(rev); S[i].update(sp)
                e = rows.get(d * 24 + 23)
                if e:
                    cash[i] += e['cash_post']; an[i] += sum(e['farm'][0].values()); st[i] += e['farm'][1].get('STRAWBERRY', 0); wh[i] += e['farm'][1].get('WHEAT', 0); ml[i] += e['farm'][1].get('MELON', 0)
        fmt = lambda c: ' '.join(f"{k}{v / n:.0f}" for k, v in sorted(c.items(), key=lambda kv: -kv[1]) if v / n >= 5)
        print(f"d{d} rev  L [{fmt(R[0])}] = {sum(R[0].values()) / n:.0f} | O [{fmt(R[1])}] = {sum(R[1].values()) / n:.0f}")
        print(f"d{d} buy  L [{fmt(S[0])}] = {sum(S[0].values()) / n:.0f} | O [{fmt(S[1])}] = {sum(S[1].values()) / n:.0f}")
        print(f"d{d} end  cash {cash[0] / n:.0f}|{cash[1] / n:.0f} animals {an[0] / n:.1f}|{an[1] / n:.1f} straw {st[0] / n:.1f}|{st[1] / n:.1f} wheat {wh[0] / n:.1f}|{wh[1] / n:.1f} melon {ml[0] / n:.1f}|{ml[1] / n:.1f}")


def _our_trace_star(a):
    return our_trace(*a)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--replay', default=''); ap.add_argument('--team', default='Majkel1337'); ap.add_argument('--days', type=int, default=9)
    ap.add_argument('--agg', type=int, default=0, help='aggregate over the first N archive worlds instead of one replay'); ap.add_argument('--dir', default='o_replays/leader_archive'); ap.add_argument('--workers', type=int, default=16)
    ap.add_argument('--seat', type=int, default=0); ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py')
    ap.add_argument('--summary', action='store_true'); ap.add_argument('--thresh', type=float, default=60.0)
    a = ap.parse_args()
    if a.agg:
        import glob
        files = [f for f in sorted(glob.glob(os.path.join(ROOT, a.dir, '*-replay.json'))) if a.team in (json.load(open(f, encoding='utf-8')).get('info', {}).get('TeamNames') or [])][:a.agg]
        aggregate(files, a.team, a.days, a.seat, a.a, a.b, a.workers); return
    shops, L, seed, opp = leader_trace(a.replay, a.team, a.days)
    O, finals = our_trace(shops, seed, a.seat, a.days, a.a, a.b)
    print(f"world {os.path.basename(a.replay)} shops {shops[:5]} leader opp {opp}; our finals {finals}")
    print('day | leader buys / sells / income / spend | ours buys / sells / income / spend | day-end cash L|O, hands L|O, animals L|O, crops L|O')
    for d in range(a.days + 1):
        lb, ls, li, lsp = day_summary(L, d); ob, os_, oi, osp = day_summary(O, d)
        le = L.get(d * 24 + 23) or L.get(max(k for k in L if k < (d + 1) * 24)) if L else None; oe = O.get(d * 24 + 23)
        if le is None or oe is None:
            continue
        print(f"d{d} | {dict(lb)} / {dict(ls)} / +{li:.0f} / -{lsp:.0f} | {dict(ob)} / {dict(os_)} / +{oi:.0f} / -{osp:.0f} | {le['cash_post']:.0f}|{oe['cash_post']:.0f}, {le['hands']}|{oe['hands']}, {le['farm'][0]}|{oe['farm'][0]}, {le['farm'][1]}|{oe['farm'][1]}")
    if a.summary:
        return
    print('\nstep  d h | L cash pre->post  orders                      | O cash pre->post  orders')
    first = None
    for k in sorted(set(L) | set(O)):
        l = L.get(k); o = O.get(k)
        if l is None or o is None:
            continue
        lo = fmt_orders(l['orders'], l['prices']); oo = fmt_orders(o['orders'], o['prices'])
        gap = o['cash_post'] - l['cash_post']
        if lo or oo or k % 24 == 23:
            print(f"{k:4d} {k // 24:2d} {k % 24:2d} | {l['cash_pre']:6.0f}->{l['cash_post']:6.0f} {lo[:42]:42s} | {o['cash_pre']:6.0f}->{o['cash_post']:6.0f} {oo[:42]:42s} | gap {gap:+6.0f}")
        if first is None and abs(gap) >= a.thresh:
            first = k
    if first is not None:
        print(f"\nfirst cash gap >= {a.thresh:.0f} at step {first} (d{first // 24} h{first % 24}): leader {L[first]['cash_post']:.0f} vs ours {O[first]['cash_post']:.0f}")


if __name__ == '__main__':
    main()
