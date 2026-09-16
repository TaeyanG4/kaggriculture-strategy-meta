"""Local recorded-action diagnostics; never interpret these as live elite win rates.

The exact original game is reproduced before every counterfactual. Only the
evaluator can access recorded future shops; the policy receives normal observations.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from .league import ROOT, digest, engine_identity, frozen_source, timed_policy, timing, write_json


def tape_policy(replay, seat):
    def act(observation, configuration):
        return copy.deepcopy(replay['steps'][int(observation['step']) + 1][seat]['action'])
    return act


def verify_replay(make, replay):
    config = dict(replay['configuration'], seed=replay['info']['seed'])
    env = make('kaggriculture', configuration=config, debug=False)
    env.run([tape_policy(replay, 0), tape_policy(replay, 1)])
    expected = [s['reward'] for s in replay['steps'][-1]]
    actual = [s.reward for s in env.steps[-1]]
    if expected != actual or len(env.steps) != len(replay['steps']):
        raise ValueError(f'Replay reproduction failed: {expected} != {actual}')
    for observed, recorded in zip(env.steps, replay['steps']):
        if observed[0].observation.town['unlocked_shops'] != recorded[0]['observation']['town']['unlocked_shops']:
            raise ValueError('Recorded shop sequence did not reproduce')
    return actual


def evaluate(job):
    from kaggle_environments import make
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    source = job['candidate']
    if digest(Path(source['path']).read_bytes()) != source['sha256'] or engine_identity() != job['engine']:
        raise ValueError('Evaluation source drift')
    replay_bytes = Path(job['replay']).read_bytes()
    if digest(replay_bytes) != job['replay_sha256']:
        raise ValueError('Replay changed after planning')
    replay = json.loads(replay_bytes)
    # Optional reproduction cache (o-series batches set KAGG_VERIFY_CACHE): the original game is
    # deterministic given replay sha + engine identity, so re-verifying it per candidate only costs time.
    cache = os.environ.get('KAGG_VERIFY_CACHE')
    cache_file = Path(cache) / (job['replay_sha256'] + '.json') if cache else None
    expected = None
    if cache_file and cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding='utf-8'))
        if cached.get('engine') == job['engine']:
            expected = cached['rewards']
    if expected is None:
        expected = verify_replay(make, replay)
        if cache_file:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            tmp = cache_file.with_suffix('.tmp%d' % os.getpid())
            tmp.write_text(json.dumps({'engine': job['engine'], 'rewards': expected}), encoding='utf-8')
            os.replace(tmp, cache_file)
    seat = job['candidate_seat']
    times, errors, hashes, telemetry = [], [], hashlib.sha256(), {}
    candidate = timed_policy(source['path'], 'candidate', times, errors, hashes, telemetry)
    agents = [tape_policy(replay, 0), tape_policy(replay, 1)]
    agents[seat] = candidate
    original = engine._end_of_day
    if job['mode'] in ('fixed_shops_frozen_opponent', 'fixed_shops_frozen_opponent_weeds'):
        sync_weeds = job['mode'] == 'fixed_shops_frozen_opponent_weeds'
        def controlled_refresh(state, env, day):
            original(state, env, day)
            step = min(719, (day + 1) * 24)
            shops = replay['steps'][step][0]['observation']['town']['unlocked_shops']
            state[0].observation.town['unlocked_shops'][:] = shops
            if sync_weeds:
                # The per-day RNG is shared by both farms' weed draws, so a different candidate farm shifts the frozen
                # opponent's weeds; restore the opponent's recorded weed outcome (spawned weeds and weeds that did not spawn).
                o = 1 - seat
                target = replay['steps'][step][0]['observation']['farms'][o]['tiles']
                tiles = state[0].observation.farms[o]['tiles']
                for y, row in enumerate(tiles):
                    for x, cur in enumerate(row):
                        tgt = target[y][x]
                        cur_weed = isinstance(cur, dict) and cur.get('kind') == 'WEED'
                        tgt_weed = isinstance(tgt, dict) and tgt.get('kind') == 'WEED'
                        if tgt_weed and not cur_weed:
                            row[x] = {'kind': 'WEED'}
                        elif cur_weed and not tgt_weed:
                            row[x] = copy.deepcopy(tgt)
        engine._end_of_day = controlled_refresh
    started = time.perf_counter()
    try:
        env = make('kaggriculture', configuration=dict(replay['configuration'], seed=replay['info']['seed']), debug=False)
        env.run(agents)
    finally:
        engine._end_of_day = original
    final = env.steps[-1]
    statuses = [s.status for s in final]
    rewards = [s.reward for s in final]
    same_shops = (len(env.steps) == len(replay['steps']) and all(
        s[0].observation.town['unlocked_shops'] == r[0]['observation']['town']['unlocked_shops']
        for s, r in zip(env.steps, replay['steps'])))
    if job['mode'] == 'fixed_shops_frozen_opponent' and not same_shops:
        raise ValueError('Controlled shop path did not match')
    return dict(job, original_rewards=expected, original_reproduced=True, rewards=rewards,
                statuses=statuses, states=len(env.steps), candidate_timing=timing(times),
                candidate_telemetry=telemetry, errors=errors, action_sha256=hashes.hexdigest(),
                valid=statuses == ['DONE', 'DONE'] and len(env.steps) == 720 and len(times) == 719 and not errors,
                margin=rewards[seat] - rewards[1-seat], same_shop_sequence=same_shops,
                seconds=time.perf_counter()-started,
                shops=list(final[0].observation.town['unlocked_shops']))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--candidate', type=Path)
    ap.add_argument('--replays', type=Path)
    ap.add_argument('--out', type=Path)
    ap.add_argument('--mode', choices=['fixed_shops_frozen_opponent', 'fixed_shops_frozen_opponent_weeds', 'native_frozen_opponent'], default='fixed_shops_frozen_opponent')
    ap.add_argument('--candidate-team', default='Taeyang')
    ap.add_argument('--elite-team', default='Majkel1337')
    ap.add_argument('--job', type=Path)
    args = ap.parse_args()
    if args.job:
        write_json(args.job.with_suffix('.result.json'), evaluate(json.loads(args.job.read_text(encoding='utf-8'))))
        return
    if not all([args.candidate, args.replays, args.out]):
        ap.error('Require --candidate --replays --out')
    out = args.out.resolve()
    source = frozen_source(args.candidate, out)
    manifest = {'candidate': source, 'engine': engine_identity(), 'mode': args.mode,
                'harness_sha256': digest(Path(__file__).read_bytes()),
                'league_sha256': digest((ROOT/'src/kaggriculture_meta/league.py').read_bytes())}
    old = out / 'manifest.json'
    if old.exists() and json.loads(old.read_text(encoding='utf-8')) != manifest:
        raise ValueError('Use a new output directory after changes')
    write_json(old, manifest)
    results = []
    for path in sorted(args.replays.glob('*-replay.json')):
        replay = json.loads(path.read_text(encoding='utf-8'))
        names = replay['info']['TeamNames']
        if args.candidate_team in names:
            seat = names.index(args.candidate_team)
        elif args.elite_team in names:
            seat = 1 - names.index(args.elite_team)
        else:
            raise ValueError(f'Explicit candidate seat needed for {path.name}')
        job = dict(manifest, replay=str(path.resolve()), replay_sha256=digest(path.read_bytes()),
                   episode=replay['info']['EpisodeId'], candidate_seat=seat,
                   opponent_name=names[1-seat], evidence_type='recorded_diagnostic_not_reacting_policy')
        jobpath = out/'jobs'/(digest(job)[:24]+'.json')
        resultpath = jobpath.with_suffix('.result.json')
        write_json(jobpath, job)
        if not resultpath.exists():
            with jobpath.with_suffix('.log').open('w', encoding='utf-8') as log:
                subprocess.run([sys.executable, '-m', 'src.kaggriculture_meta.replay_lab', '--job', str(jobpath)],
                               cwd=ROOT, stdout=log, stderr=log, check=True, timeout=90)
        result = json.loads(resultpath.read_text(encoding='utf-8'))
        results.append(result)
        write_json(out/'results.json', results)
        print(f"{len(results)} episode={job['episode']} margin={result['margin']} valid={result['valid']}", flush=True)


if __name__ == '__main__':
    main()
