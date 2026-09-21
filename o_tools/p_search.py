"""Structure+number search for the planner line (p0xx) with optuna TPE.
Objective = paired proxy-cash gain vs the current baseline (BASE labels) on the pinned selection set (o227 opponent, seeds 7000-7015,
32 games). Every trial runs as one proxy_eval subprocess with PROXY_KNOBS set; results are cached by knob string.
Every CHECK trials the best untested configs are confirmed on the holdout set (7016-7031). Board: o_results/p_search/board.txt
Usage: python o_tools/p_search.py --trials 300 --workers 12 [--agent agent/p000_planner.py] [--resume]"""
import argparse, json, os, statistics, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'o_results', 'p_search'); os.makedirs(OUT, exist_ok=True)
SWITCHES = ['fert_h0', 'melon_harv0', 'melon_water', 'melon_bank', 'behind', 'pr0_share', 'no_wheat_fert', 'fert_batch',
            'collect_here', 'herd_first', 'bank_pm', 'd28_feed', 'hire_res', 'herd_angle', 'herd_block',
            'hire_first', 'pick_own', 'feed_stock', 'vrp', 'egg', 'yarn2', 'carrot2', 'anim3', 'vrp_preload', 'vrp_2opt', 'price_hold', 'melon_rush', 'carrot_hold']   # base defaults on: herd_split, shed_cap, horizon, reserve (not searched); rejected outright: melon_open, rescue, radial, melon_d9, land4, straw_open, carrot, sweep
BASE = {'sel': os.environ.get('P_BASE_SEL', 'base19_sel'), 'hold': os.environ.get('P_BASE_HOLD', 'base19_hold')}
DEFAULT_ON = {'collect_here', 'd28_feed', 'tomato', 'vrp', 'egg', 'carrot2', 'herd_block', 'hire_first', 'feed_stock', 'bank_pm', 'melon_water', 'melon_bank', 'opp_supply', 'melon_rush', 'carrot_hold', 'yarn2'}   # base13 switches
SEEDS = {'sel': os.environ.get('P_SEL_SEEDS', '7000-7015'), 'hold': os.environ.get('P_HOLD_SEEDS', '7016-7031')}


def knob_string(cfg):
    return ','.join(f'{k}={v}' for k, v in sorted(cfg.items()))


OBJECTIVE = os.environ.get('P_OBJECTIVE', 'own')   # own = our cash delta; margin = (our - rival) cash delta (wins are decided by the margin)


def paired(label, side):
    import math
    val = ((lambda r: r['b'] - r['a']) if OBJECTIVE == 'margin' else
           (lambda r: 10000.0 * math.tanh((r['b'] - r['a']) / 4000.0)) if OBJECTIVE == 'softwin' else   # smooth win indicator: games near the win line count, hopeless ones do not
           (lambda r: r['b']))
    base = {(r['seed'], r['seat_b']): val(r) for r in json.load(open(os.path.join(ROOT, 'o_results', 'proxy', f'eval_{BASE[side]}.json')))}
    cand = {(r['seed'], r['seat_b']): val(r) for r in json.load(open(os.path.join(ROOT, 'o_results', 'proxy', f'eval_{label}.json')))}
    d = [cand[k] - base[k] for k in sorted(set(base) & set(cand))]
    return statistics.mean(d), statistics.stdev(d) / len(d) ** 0.5, sum(x < -500 for x in d)


def _run_eval(agent, cfg, side, label, workers, seats):
    env = dict(os.environ, PROXY_KNOBS=knob_string(cfg), PYTHONIOENCODING='utf-8', MPLBACKEND='Agg')
    subprocess.run([sys.executable, os.path.join(ROOT, 'o_tools', 'proxy_eval.py'), '--a', 'agent/o227_stealth_drop.py', '--b', agent,
                    '--seeds', SEEDS[side], '--workers', str(workers), '--label', label, '--seats', seats], env=env, cwd=ROOT, capture_output=True, text=True)


def evaluate(agent, cfg, side, label, workers):
    """Two-stage when P_SCREEN=1: seat 0 only first (16 games; Spearman 0.994 with the 32-game paired delta on 826 past trials);
    the other seat is added only if the screen delta clears P_SCREEN_MIN. The per-game cache makes the second stage cost 16 games."""
    path = os.path.join(ROOT, 'o_results', 'proxy', f'eval_{label}.json')
    if os.path.exists(path):
        return paired(label, side)
    if os.environ.get('P_SCREEN') == '1' and side == 'sel':
        _run_eval(agent, cfg, side, label + '_s0', workers, '0')
        m, se, worse = paired(label + '_s0', side)
        if m < float(os.environ.get('P_SCREEN_MIN', '-2000' if OBJECTIVE == 'softwin' else '-1000')):
            return m, se, worse   # screened out on the seat-0 half
    _run_eval(agent, cfg, side, label, workers, '0,1')
    return paired(label, side)


def main():
    import optuna
    ap = argparse.ArgumentParser(); ap.add_argument('--trials', type=int, default=300); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--agent', default='agent/p000_planner.py'); ap.add_argument('--check', type=int, default=25); ap.add_argument('--study', default='p000')
    a = ap.parse_args()
    board = open(os.path.join(OUT, 'board.txt'), 'a', encoding='utf-8')
    storage = f"sqlite:///{os.path.join(OUT, a.study + '.db').replace(os.sep, '/')}"
    study = optuna.create_study(study_name=a.study, storage=storage, direction='maximize', load_if_exists=True,
                                sampler=optuna.samplers.TPESampler(n_startup_trials=30, multivariate=True, seed=1))
    cache = {}; confirmed = set(); t0 = time.time()
    if not study.trials:   # anchors: base7 defaults, each switch alone, a few combos of the 09-18 near-misses
        base = dict(feed=4.5, straw=40, melons=12, land3=9, buf=1, wheat_units=3, melon_pr_age=9, melon_pr_hour=12, sheep_plus=1, room_f=0.4, cap_m23=9, cap_m=6, prw=6,
                    vrp_bal=1.4, vrp_w=2.0, vrp_len=12, vrp_pr=4, opp_f=1.0, tom_per=8, straw_f=0.4, seed_last=26, **({'melons0': 8, 'w0feed': 3, 'straw_early': 8, 'd0_res': 5} if os.environ.get('P_SPACE') == 'joint' else {}), **{'sw_' + sw: (1 if sw in DEFAULT_ON else 0) for sw in SWITCHES})
        study.enqueue_trial(base)
        for sw in SWITCHES:
            study.enqueue_trial(dict(base, **{'sw_' + sw: 1 - base['sw_' + sw]}))
        for kv in (dict(vrp_bal=1.2), dict(vrp_bal=1.7), dict(vrp_bal=2.0), dict(vrp_w=2.0), dict(vrp_w=3.0), dict(vrp_len=8), dict(vrp_len=16), dict(vrp_pr=0), dict(vrp_pr=4), dict(opp_f=0.7), dict(opp_f=1.3), dict(tom_per=10), dict(straw=44), dict(room_f=0.5), dict(sheep_plus=2)):
            study.enqueue_trial(dict(base, **kv))

    def objective(trial):
        cfg = {}
        for sw in SWITCHES:
            cfg['sw_' + sw] = trial.suggest_int('sw_' + sw, 0, 1)
        cfg['feed'] = trial.suggest_categorical('feed', [4.0, 4.5, 5.0])
        cfg['straw'] = trial.suggest_int('straw', 28, 40, step=2)
        cfg['melons'] = trial.suggest_int('melons', 10, 14, step=2)
        cfg['land3'] = trial.suggest_int('land3', 7, 9)
        cfg['buf'] = trial.suggest_int('buf', 1, 4)
        cfg['wheat_units'] = trial.suggest_int('wheat_units', 3, 5)
        cfg['melon_pr_age'] = trial.suggest_categorical('melon_pr_age', [9, 10, 11, 99])
        cfg['melon_pr_hour'] = trial.suggest_categorical('melon_pr_hour', [8, 10, 12, 99])
        cfg['sheep_plus'] = trial.suggest_int('sheep_plus', 0, 3)
        cfg['room_f'] = trial.suggest_categorical('room_f', [0.4, 0.5, 0.6])
        cfg['straw_f'] = trial.suggest_categorical('straw_f', [0.4, 0.5, 0.6, 0.8])   # strawberry share of the market room (herd keeps room_f)
        cfg['cap_m23'] = trial.suggest_categorical('cap_m23', [9, 12])
        cfg['cap_m'] = trial.suggest_categorical('cap_m', [3, 6])
        cfg['prw'] = trial.suggest_categorical('prw', [6, 8])
        cfg['vrp_bal'] = trial.suggest_categorical('vrp_bal', [1.2, 1.4, 1.7, 2.0])
        cfg['vrp_w'] = trial.suggest_categorical('vrp_w', [2.0, 2.5, 3.0])
        cfg['vrp_len'] = trial.suggest_categorical('vrp_len', [8, 12, 16])
        cfg['vrp_pr'] = trial.suggest_categorical('vrp_pr', [0, 2, 4])
        cfg['opp_f'] = trial.suggest_categorical('opp_f', [0.7, 1.0, 1.3])
        cfg['tom_per'] = trial.suggest_categorical('tom_per', [6, 8, 10])
        if os.environ.get('P_SPACE') == 'joint':   # opening knobs searched together with the main knobs
            cfg['melons0'] = trial.suggest_int('melons0', 7, 9); cfg['w0feed'] = trial.suggest_categorical('w0feed', [2, 3, 5])
            cfg['straw_early'] = trial.suggest_categorical('straw_early', [4, 8, 12]); cfg['d0_res'] = trial.suggest_categorical('d0_res', [0, 5, 25])
        cfg = {k: v for k, v in cfg.items() if not (k.startswith('sw_') and v == 0 and k[3:] not in DEFAULT_ON)}   # off switches omitted unless the baseline has them on
        ks = knob_string(cfg)
        if ks in cache:
            return cache[ks]
        label = f"{a.study}_t{trial.number:04d}"
        mean, se, worse = evaluate(a.agent, cfg, 'sel', label, a.workers)
        cache[ks] = mean; trial.set_user_attr('se', se); trial.set_user_attr('worse', worse)
        board.write(f"{time.strftime('%m-%d %H:%M')} [{int((time.time()-t0)/60):4d}m] t{trial.number:04d} sel {mean:+7.0f} (se {se:4.0f}, worse {worse:2d}) | {ks}\n"); board.flush()
        # holdout confirmation for the current top configs every CHECK trials
        if (trial.number + 1) % a.check == 0:
            top = sorted([t for t in study.trials if t.value is not None], key=lambda t: -t.value)[:3]
            for t in top:
                if t.number in confirmed or t.value < 1000:
                    continue
                confirmed.add(t.number)
                cfg_t = {k: v for k, v in t.params.items() if not (k.startswith('sw_') and v == 0 and k[3:] not in DEFAULT_ON)}
                hm, hse, hw = evaluate(a.agent, cfg_t, 'hold', f"{a.study}_t{t.number:04d}_hold", a.workers)
                verdict = 'PASS' if (t.value >= 1500 and hm >= 1500 and hw <= 10) else 'fail'
                board.write(f"{time.strftime('%m-%d %H:%M')} HOLDOUT t{t.number:04d} sel {t.value:+7.0f} hold {hm:+7.0f} (se {hse:4.0f}, worse {hw:2d}) -> {verdict} | {knob_string(cfg_t)}\n"); board.flush()
        return mean

    study.optimize(objective, n_trials=a.trials)
    best = study.best_trial
    board.write(f"DONE best t{best.number:04d} sel {best.value:+.0f} | {knob_string(best.params)}\n"); board.close()


if __name__ == '__main__':
    main()
