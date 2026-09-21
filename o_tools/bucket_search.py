"""World-profile router search: tune a knob subset for ONE world bucket (yarn / milk0-3 by the first three shops) with profile-gated
knobs ("#bucket:knob=v", active from the step the third shop is known). Objective = paired softwin (or margin/own via P_OBJECTIVE)
on the bucket's tuning seeds (both seats) vs the base label; the bucket's holdout seeds are scored every CHECK trials.
Usage: P_OBJECTIVE=softwin python o_tools/bucket_search.py --bucket milk1 --trials 80 --workers 12 --base base17_pool
Pool definition: o_results/proxy/pool_seeds.json (built by o_tools/build_pool.py)."""
import argparse, json, os, sys, time, statistics, subprocess, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
OUT = os.path.join(ROOT, 'o_results', 'p_search')
OBJECTIVE = os.environ.get('P_OBJECTIVE', 'softwin')


def val(r):
    if OBJECTIVE == 'margin':
        return r['b'] - r['a']
    if OBJECTIVE == 'softwin':
        return 10000.0 * math.tanh((r['b'] - r['a']) / 4000.0)
    return r['b']


def load(label):
    return {(r['seed'], r['seat_b']): r for r in json.load(open(os.path.join(ROOT, 'o_results', 'proxy', f'eval_{label}.json')))}


def paired(base, label, seeds):
    B = load(base); C = load(label)
    keys = [k for k in sorted(B) if k[0] in seeds and k in C]
    d = [val(C[k]) - val(B[k]) for k in keys]
    m = [(C[k]['b'] - C[k]['a']) - (B[k]['b'] - B[k]['a']) for k in keys]
    o = [C[k]['b'] - B[k]['b'] for k in keys]
    wins = sum(C[k]['b'] > C[k]['a'] for k in keys) - sum(B[k]['b'] > B[k]['a'] for k in keys)
    return statistics.mean(d), (statistics.stdev(d) / len(d) ** 0.5 if len(d) > 1 else 0), sum(x < -500 for x in m), statistics.mean(m), statistics.mean(o), wins, len(keys)


def evaluate(agent, knobs, label, seeds, workers):
    path = os.path.join(ROOT, 'o_results', 'proxy', f'eval_{label}.json')
    if not os.path.exists(path):
        env = dict(os.environ, PROXY_KNOBS=knobs, PYTHONIOENCODING='utf-8', MPLBACKEND='Agg')
        subprocess.run([sys.executable, os.path.join(ROOT, 'o_tools', 'proxy_eval.py'), '--a', 'agent/o227_stealth_drop.py', '--b', agent,
                        '--seed-list', ','.join(str(s) for s in seeds), '--workers', str(workers), '--label', label], env=env, cwd=ROOT, capture_output=True, text=True)


SPACE = {
    'room_f': [0.3, 0.4, 0.5, 0.6], 'straw_f': [0.4, 0.5, 0.6], 'sheep_plus': [0, 1, 2, 3], 'tom_per': [6, 8, 10, 12], 'car_pet': [4, 6, 8],
    'buf': [1, 2, 4], 'wheat_units': [3, 4], 'nwf_d': [9, 20, 99], 'worth_d': [24, 27], 'egg1': [2, 3], 'egg2': [3, 4, 5], 'opp_f': [0.7, 1.0, 1.3],
    'seed_last': [26, 27], 'cap_m23': [9, 12], 'straw': [36, 40, 44], 'sc_plus': [0, 8, 12],
}
BASE = dict(room_f=0.4, straw_f=0.4, sheep_plus=1, tom_per=8, car_pet=6, buf=1, wheat_units=3, nwf_d=20, worth_d=27, egg1=2, egg2=4, opp_f=1.0, seed_last=26, cap_m23=9, straw=40, sc_plus=8)


def main():
    import optuna
    ap = argparse.ArgumentParser(); ap.add_argument('--bucket', required=True); ap.add_argument('--trials', type=int, default=80); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--agent', default='agent/p000_planner.py'); ap.add_argument('--base', default='base17_pool'); ap.add_argument('--check', type=int, default=20); ap.add_argument('--study', default='')
    a = ap.parse_args(); study_name = a.study or f'bk_{a.bucket}'
    pool = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'pool_seeds.json')))
    tune = pool['tune'][a.bucket]; hold = pool['hold'][a.bucket]
    print(f'bucket {a.bucket}: tune seeds {len(tune)} ({2 * len(tune)} games), hold seeds {len(hold)}')
    board = open(os.path.join(OUT, 'board.txt'), 'a', encoding='utf-8')
    storage = f"sqlite:///{os.path.join(OUT, study_name + '.db').replace(os.sep, '/')}"
    study = optuna.create_study(study_name=study_name, storage=storage, direction='maximize', load_if_exists=True,
                                sampler=optuna.samplers.TPESampler(n_startup_trials=20, multivariate=True, seed=5))
    if not study.trials:
        study.enqueue_trial(dict(BASE))
        for k, vals in SPACE.items():
            for v in vals:
                if v != BASE[k]:
                    study.enqueue_trial(dict(BASE, **{k: v}))
    cache = {}; confirmed = set(); t0 = time.time()

    def knob_string(cfg):
        return ','.join(f'#{a.bucket}:{k}={v}' for k, v in sorted(cfg.items()) if v != BASE[k])

    def objective(trial):
        cfg = {k: trial.suggest_categorical(k, vals) for k, vals in SPACE.items()}
        ks = knob_string(cfg)
        if ks in cache:
            return cache[ks]
        label = f"{study_name}_t{trial.number:04d}"
        evaluate(a.agent, ks, label, tune, a.workers)
        mean, se, worse, dm, do, wins, n = paired(a.base, label, tune)
        cache[ks] = mean; trial.set_user_attr('se', se); trial.set_user_attr('worse', worse); trial.set_user_attr('margin', dm); trial.set_user_attr('wins', wins)
        board.write(f"{time.strftime('%m-%d %H:%M')} [{int((time.time()-t0)/60):4d}m] {study_name} t{trial.number:04d} tune {mean:+7.0f} (se {se:4.0f}, worse {worse:2d}, margin {dm:+6.0f}, own {do:+6.0f}, wins {wins:+d}, n {n}) | {ks or 'BASE'}\n"); board.flush()
        if (trial.number + 1) % a.check == 0:
            top = sorted([t for t in study.trials if t.value is not None], key=lambda t: -t.value)[:3]
            for t in top:
                if t.number in confirmed or t.value < 300:
                    continue
                confirmed.add(t.number)
                ks_t = knob_string(dict(t.params)); lab_t = f"{study_name}_t{t.number:04d}_hold"
                evaluate(a.agent, ks_t, lab_t, hold, a.workers)
                hm, hse, hw, hdm, hdo, hwins, hn = paired(a.base, lab_t, hold)
                board.write(f"{time.strftime('%m-%d %H:%M')} HOLDOUT {study_name} t{t.number:04d} tune {t.value:+7.0f} hold {hm:+7.0f} (se {hse:4.0f}, worse {hw:2d}, margin {hdm:+6.0f}, own {hdo:+6.0f}, wins {hwins:+d}, n {hn}) | {ks_t}\n"); board.flush()
        return mean

    study.optimize(objective, n_trials=a.trials)
    best = study.best_trial
    board.write(f"DONE {study_name} best t{best.number:04d} tune {best.value:+.0f} | {knob_string(dict(best.params))}\n"); board.flush()


if __name__ == '__main__':
    main()
