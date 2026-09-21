"""Trace live rivals to public sources: fingerprint the first K market turns of candidate agent files (seat 0 vs a PASS rival,
fixed seed) and of every rival in a replay directory, group the rivals by fingerprint, and optionally VERIFY a match by
replaying the live episode with the candidate in the rival's seat and our recorded actions frozen (live_replay_audit.play).
Usage: python o_tools/rival_source_trace.py --dir o_replays/live_frozen/live_b19 --us Taeyang --cands a.py b.py ... [--k 6] [--verify 2]
Output: o_results/rival_source_trace.json (fingerprints, groups, verification rows)."""
import argparse, glob, hashlib, io, contextlib, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))


def sig(a):
    if not isinstance(a, dict):
        return '-'
    m = a.get('market') or []
    return ','.join(f"{o[0][0]}{str(o[1])[:3]}{o[2]}" if isinstance(o, list) and len(o) >= 3 else str(o) for o in m) or '.'


def fingerprint(path, k, seed=7000):
    """First k market turns of the agent in seat 0 against a PASS rival (deterministic opening)."""
    from proxy_eval import load_agent
    from kaggle_environments import make
    cwd = os.getcwd()
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            A = load_agent(os.path.abspath(path), 'cand_' + hashlib.md5(path.encode()).hexdigest()[:8])
            env = make('kaggriculture', configuration={'seed': seed}, debug=False); env.reset(2); out = []
            for _ in range(k):
                obs = env.state[0].observation
                try:
                    a = A(obs, env.configuration)
                except TypeError:
                    a = A(obs)
                out.append(sig(a)); env.step([a, {'farmer': ['PASS'], 'hands': [], 'market': []}])
        return tuple(out)
    except BaseException as e:
        return ('ERR', repr(e)[:80])
    finally:
        os.chdir(cwd)


def rival_prints(rdir, us, k):
    rows = []
    for p in sorted(glob.glob(os.path.join(rdir, '*-replay.json'))):
        r = json.load(open(p, encoding='utf-8')); names = r['info']['TeamNames']; op = 1 - names.index(us); steps = r['steps']
        rows.append(dict(path=p, episode=os.path.basename(p).split('-')[0], rival=names[op], fp=tuple(sig(steps[j][op].get('action')) for j in range(1, k + 1) if j < len(steps))))
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dir', required=True); ap.add_argument('--us', default='Taeyang'); ap.add_argument('--cands', nargs='+', required=True)
    ap.add_argument('--k', type=int, default=6); ap.add_argument('--verify', type=int, default=0, help='replay-verify up to N games per matched candidate'); ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args(); os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    cands = {}
    for c in a.cands:
        fp = fingerprint(c, a.k); cands[c] = dict(sha=hashlib.sha256(open(c, 'rb').read()).hexdigest(), fp=fp)
        print(f"cand {c}  sha {cands[c]['sha'][:16]}  fp {' || '.join(fp)}")
    rivals = rival_prints(a.dir, a.us, a.k)
    by = {}
    for r in rivals:
        by.setdefault(r['fp'], []).append(r)
    print(f"\n{len(rivals)} rival games, {len(by)} distinct {a.k}-turn fingerprints")
    matches = {}
    for c, info in cands.items():
        hit = by.get(info['fp'], [])
        matches[c] = [r['episode'] for r in hit]
        print(f"  {os.path.basename(c):50s} matches {len(hit):3d} games: {[r['rival'][:14] for r in hit][:8]}")
    unmatched = [(fp, v) for fp, v in by.items() if fp not in {i['fp'] for i in cands.values()}]
    unmatched.sort(key=lambda kv: -len(kv[1]))
    print('\nunmatched fingerprints (>=2 games):')
    for fp, v in unmatched:
        if len(v) >= 2:
            print(f"  {len(v):3d}  {' || '.join(fp)}   e.g. {[r['rival'][:14] for r in v[:4]]}")
    ver = []
    if a.verify:
        from concurrent.futures import ProcessPoolExecutor
        from live_replay_audit import play
        jobs = []
        for c, eps in matches.items():
            for e in eps[:a.verify]:
                r = next(x for x in rivals if x['episode'] == e); jobs.append((r['path'], r['rival'], c))
        with ProcessPoolExecutor(a.workers) as ex:
            for (p, team, c), res in zip(jobs, ex.map(play, jobs)):
                f = res['first']
                ver.append(dict(cand=c, episode=res['episode'], rival=team, identical=f is None, first=f, n_div=res['n_div'], rec_rival=res['rec_ours'], sim_rival=res['sim_ours']))
                print(f"verify {os.path.basename(c):45s} ep {res['episode']} rival {team[:16]:16s} " + ('IDENTICAL 720 steps' if f is None else f"first div d{f['day']} h{f['hour']} [{f['cat']}] divs {res['n_div']} local {f['local'][:60]} live {f['live'][:60]}") + f"  rival cash rec {res['rec_ours']:.0f} sim {res['sim_ours']:.0f}")
    json.dump(dict(k=a.k, cands={c: dict(sha=i['sha'], fp=list(i['fp']), matches=matches[c]) for c, i in cands.items()},
                   rivals=[dict(episode=r['episode'], rival=r['rival'], fp=list(r['fp'])) for r in rivals], verify=ver),
              open(os.path.join(ROOT, 'o_results', 'rival_source_trace.json'), 'w'), indent=0)


if __name__ == '__main__':
    main()
