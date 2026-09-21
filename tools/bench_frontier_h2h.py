"""Frontier H2H Benchmark Tool

Evaluates a candidate agent against canonical frontier baselines:
- V48 (agent/p005_v48_exact.py)
- o239_50 (agent/o239_open_roundtrip_50.py)
- public_v9_4 (state/c312/public_v9_4.py)

Runs seat-paired games on explicit screen/confirm seeds.
"""
import sys
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.kaggriculture_meta import championship_league as L

DEFAULT_SEEDS = [1542303036, 1384849883, 458410889, 1101525775]

def run_h2h(cand_path, opp_path, seeds=None):
    cand_p = Path(cand_path).resolve()
    opp_p = Path(opp_path).resolve()
    if not cand_p.exists():
        raise FileNotFoundError(f"Candidate not found: {cand_p}")
    if not opp_p.exists():
        raise FileNotFoundError(f"Opponent not found: {opp_p}")

    cand_sha = hashlib.sha256(cand_p.read_bytes()).hexdigest()
    opp_sha = hashlib.sha256(opp_p.read_bytes()).hexdigest()
    seeds = seeds or DEFAULT_SEEDS

    print(f"=== Frontier H2H Benchmark ===")
    print(f"Candidate: {cand_p.name} ({cand_sha[:8]}...)")
    print(f"Opponent:  {opp_p.name} ({opp_sha[:8]}...)")
    print(f"Seeds:     {len(seeds)} ({seeds})")
    print(f"{'-'*50}")

    margins = []
    wins, losses, ties = 0, 0, 0

    for seed in seeds:
        pair_margins = []
        for seat in (0, 1):
            job = {
                'schema': 2,
                'engine': L.engine_identity(),
                'mode': 'native_reacting',
                'stage': 'diagnostic',
                'seed': seed,
                'candidate_seat': seat,
                'configuration': {'episodeSteps': 720},
                'candidate': {'path': str(cand_p), 'sha256': cand_sha, 'name': cand_p.stem},
                'opponent': {'path': str(opp_p), 'sha256': opp_sha, 'name': opp_p.stem, 'family': 'frontier'},
                'match_id': f"diag_{seed}_{seat}",
                'contract_sha256': '0' * 64
            }
            res = L.run_match(job)
            m = res['margin']
            rew = res['rewards']
            pair_margins.append(m)
            if m > 0:
                wins += 1
            elif m < 0:
                losses += 1
            else:
                ties += 1
            print(f"Seed {seed} | Seat {seat} | Margin: {m:+8.1f} | Rewards: {rew}", flush=True)
        seed_avg = sum(pair_margins) / len(pair_margins)
        margins.append(seed_avg)
        print(f"  -> Seed {seed} Mean Margin: {seed_avg:+8.1f}", flush=True)

    total_mean = sum(margins) / len(margins)
    win_rate = (wins + 0.5 * ties) / (wins + losses + ties) if (wins + losses + ties) else 0
    print(f"{'-'*50}", flush=True)
    print(f"Summary: {wins}W - {losses}L - {ties}T (Win Rate: {win_rate:.1%})", flush=True)
    print(f"Overall Mean Margin: {total_mean:+8.1f}", flush=True)
    return {
        'candidate': cand_p.name,
        'opponent': opp_p.name,
        'wins': wins,
        'losses': losses,
        'ties': ties,
        'mean_margin': total_mean,
        'seed_margins': margins
    }

if __name__ == '__main__':
    cand = sys.argv[1] if len(sys.argv) > 1 else 'agent/p005_v48_exact.py'
    opp = sys.argv[2] if len(sys.argv) > 2 else 'agent/o239_open_roundtrip_50.py'
    run_h2h(cand, opp)
