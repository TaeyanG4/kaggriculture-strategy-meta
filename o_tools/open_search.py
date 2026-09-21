"""Opening bundle search (d0-d12 purchase schedule) for the planner: optuna TPE over the opening knobs only, objective = paired
margin (own - rival) vs the base label on the selection set, holdout confirmation every CHECK trials. Reuses p_search's evaluate/paired.
Usage: P_OBJECTIVE=margin python o_tools/open_search.py --study open1 --trials 150 --workers 12"""
import argparse, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
import p_search as ps


def main():
    import optuna
    ap = argparse.ArgumentParser(); ap.add_argument('--trials', type=int, default=150); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--agent', default='agent/p000_planner.py'); ap.add_argument('--check', type=int, default=20); ap.add_argument('--study', default='open1')
    a = ap.parse_args()
    board = open(os.path.join(ps.OUT, 'board.txt'), 'a', encoding='utf-8')
    storage = f"sqlite:///{os.path.join(ps.OUT, a.study + '.db').replace(os.sep, '/')}"
    study = optuna.create_study(study_name=a.study, storage=storage, direction='maximize', load_if_exists=True,
                                sampler=optuna.samplers.TPESampler(n_startup_trials=25, multivariate=True, seed=3))
    wide = os.environ.get('OPEN_SPACE') == 'wide'
    base = dict(cows0=2, sheep0=3, melons0=8, w0seed=6, w0feed=3, d0_res=5, melons_late=12, straw_early=8, cows5=2, straw_d6=11, straw_d79=4, straw_d1012=3, land3=9)
    if wide:
        base['land2'] = 6
    if not study.trials:
        study.enqueue_trial(base)
        probes = [dict(cows0=1), dict(cows0=3), dict(sheep0=2), dict(sheep0=4), dict(melons0=7), dict(w0seed=0), dict(w0feed=5), dict(d0_res=25), dict(melons_late=10),
                  dict(straw_early=4), dict(straw_early=12), dict(cows5=3), dict(cows5=4), dict(straw_d6=8), dict(straw_d6=14), dict(straw_d79=2), dict(straw_d79=6), dict(straw_d1012=0), dict(land3=8)]
        if wide:
            probes += [dict(melons0=10), dict(w0feed=2), dict(d0_res=0), dict(melons_late=8), dict(straw_early=16), dict(straw_d1012=5), dict(land3=10), dict(land2=7)]
        for kv in probes:
            study.enqueue_trial(dict(base, **kv))
    cache = {}; confirmed = set(); t0 = time.time()

    def objective(trial):
        wide = os.environ.get('OPEN_SPACE') == 'wide'
        cfg = dict(cows0=trial.suggest_int('cows0', 1, 3), sheep0=trial.suggest_int('sheep0', 2, 4), melons0=trial.suggest_int('melons0', 5, 10 if wide else 8),
                   w0seed=trial.suggest_categorical('w0seed', [0, 6, 11]), w0feed=trial.suggest_categorical('w0feed', [2, 3, 5] if wide else [3, 5, 8]), d0_res=trial.suggest_categorical('d0_res', [0, 5, 25] if wide else [5, 25]),
                   melons_late=trial.suggest_categorical('melons_late', [8, 10, 12] if wide else [10, 12]), straw_early=trial.suggest_categorical('straw_early', [4, 8, 12, 16] if wide else [4, 8, 12]),
                   cows5=trial.suggest_int('cows5', 2, 4), straw_d6=trial.suggest_categorical('straw_d6', [8, 11, 14]), straw_d79=trial.suggest_categorical('straw_d79', [2, 4, 6]),
                   straw_d1012=trial.suggest_categorical('straw_d1012', [0, 3, 5] if wide else [0, 3]), land3=trial.suggest_int('land3', 8, 10 if wide else 9))
        if wide:
            cfg['land2'] = trial.suggest_int('land2', 6, 7)
        if cfg['cows5'] > 2:
            cfg['sw_cow5'] = 1   # early cows d2-5 up to cows5
        ks = ps.knob_string(cfg)
        if ks in cache:
            return cache[ks]
        label = f"{a.study}_t{trial.number:04d}"
        mean, se, worse = ps.evaluate(a.agent, cfg, 'sel', label, a.workers)
        cache[ks] = mean; trial.set_user_attr('se', se); trial.set_user_attr('worse', worse)
        board.write(f"{time.strftime('%m-%d %H:%M')} [{int((time.time()-t0)/60):4d}m] {a.study} t{trial.number:04d} sel {mean:+7.0f} (se {se:4.0f}, worse {worse:2d}) | {ks}\n"); board.flush()
        if (trial.number + 1) % a.check == 0:
            top = sorted([t for t in study.trials if t.value is not None], key=lambda t: -t.value)[:3]
            for t in top:
                if t.number in confirmed or t.value < 800:
                    continue
                confirmed.add(t.number)
                cfg_t = dict(t.params)
                if cfg_t.get('cows5', 2) > 2:
                    cfg_t['sw_cow5'] = 1
                hm, hse, hw = ps.evaluate(a.agent, cfg_t, 'hold', f"{a.study}_t{t.number:04d}_hold", a.workers)
                verdict = 'PASS' if (hm >= 800 and hw <= 8) else 'fail'
                board.write(f"{time.strftime('%m-%d %H:%M')} HOLDOUT {a.study} t{t.number:04d} sel {t.value:+7.0f} hold {hm:+7.0f} (se {hse:4.0f}, worse {hw:2d}) -> {verdict} | {ps.knob_string(cfg_t)}\n"); board.flush()
        return mean

    study.optimize(objective, n_trials=a.trials)
    best = study.best_trial
    board.write(f"DONE {a.study} best t{best.number:04d} sel {best.value:+.0f} | {ps.knob_string(best.params)}\n"); board.flush()


if __name__ == '__main__':
    main()
