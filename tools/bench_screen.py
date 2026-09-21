import sys, time, json, argparse
from pathlib import Path
ROOT = Path('.').resolve()
sys.path.insert(0, str(ROOT))
from src.kaggriculture_meta import championship_league as L
import concurrent.futures

def run_panel(candidate_path, candidate_name, candidate_sha, opponent_path, opponent_name, opponent_sha, opponent_family, seeds, max_workers=12):
    jobs = []
    for seed in seeds:
        for seat in (0, 1):
            jobs.append({
                'schema': 2,
                'engine': L.engine_identity(),
                'mode': 'native_reacting',
                'stage': 'screen',
                'seed': seed,
                'candidate_seat': seat,
                'configuration': {'episodeSteps': 720},
                'candidate': {'path': candidate_path, 'sha256': candidate_sha, 'name': candidate_name},
                'opponent': {'path': opponent_path, 'sha256': opponent_sha, 'name': opponent_name, 'family': opponent_family},
                'match_id': f'{candidate_name}_{opponent_name}_{seed}_{seat}',
                'contract_sha256': '0' * 64
            })

    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(L.run_match, jobs))
    elapsed = time.time() - start

    wins = sum(1 for r in results if r['margin'] > 0)
    losses = sum(1 for r in results if r['margin'] < 0)
    ties = sum(1 for r in results if r['margin'] == 0)
    margins = [r['margin'] for r in results]
    mean_margin = sum(margins) / len(margins) if margins else 0
    print(f"{candidate_name} vs {opponent_name} ({len(results)} games in {elapsed:.1f}s): {wins}W - {losses}L - {ties}T | Mean margin: {mean_margin:+.1f}")
    for r in results:
        if r['margin'] < 0:
            print(f"  LOSS: seed={r['seed']}, seat={r['candidate_seat']}, margin={r['margin']}, rew={r['rewards']}")
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--candidate', default='state/c312/public_v9_4.py')
    ap.add_argument('--candidate-name', default='v9')
    ap.add_argument('--opponent', default='all')
    ap.add_argument('--workers', type=int, default=12)
    args = ap.parse_args()

    seeds = [
        1542303036, 1384849883, 458410889, 1101525775,
        287049605, 1869390184, 1822423521, 1626853671,
        1468257305, 931118787, 572378660, 1606616802,
        492309603, 1016436360, 1181567501, 1556571517
    ]

    import hashlib
    cand_sha = hashlib.sha256(Path(args.candidate).read_bytes()).hexdigest()

    opponents = {
        'v49': ('state/c300/public_research_20260919/v49/extracted_main.py', 'v49', 'v49'),
        'k0006': ('state/o_dev/jaxa_k0006.py', 'k0006', 'k0006'),
        'o240': ('agent/o240_sale_race.py', 'o240', 'own_tape'),
        'v9': ('state/c312/public_v9_4.py', 'v9', 'tschinkel_v9')
    }

    if args.opponent in opponents:
        target_opps = [args.opponent]
    else:
        target_opps = ['v49', 'k0006', 'o240', 'v9']

    for opp_name in target_opps:
        p, name, family = opponents[opp_name]
        opp_sha = hashlib.sha256(Path(p).read_bytes()).hexdigest()
        run_panel(args.candidate, args.candidate_name, cand_sha, p, name, opp_sha, family, seeds, max_workers=args.workers)

if __name__ == '__main__':
    main()
