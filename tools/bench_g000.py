import sys, time, json, hashlib
from pathlib import Path
ROOT = Path('.').resolve()
sys.path.insert(0, str(ROOT))
from tools.test_mechanisms import create_candidate
from tools.bench_screen import run_panel

def main():
    seeds = [
        1542303036, 1384849883, 458410889, 1101525775,
        287049605, 1869390184, 1822423521, 1626853671,
        1468257305, 931118787, 572378660, 1606616802,
        492309603, 1016436360, 1181567501, 1556571517
    ]

    cand_name = 'g000_apex_v1'
    p, sha = create_candidate(cand_name, frontload=False, advance=True, unblock_racepx=False, herd_relax=True)

    opponents = [
        ('state/c312/public_v9_4.py', 'v9', 'tschinkel_v9'),
        ('state/c300/public_research_20260919/v49/extracted_main.py', 'v49', 'v49'),
        ('state/o_dev/jaxa_k0006.py', 'k0006', 'k0006'),
        ('agent/o240_sale_race.py', 'o240', 'own_tape'),
    ]

    total_wins, total_losses, total_ties = 0, 0, 0
    all_margins = []

    for opp_path, opp_name, opp_family in opponents:
        opp_sha = hashlib.sha256(Path(opp_path).read_bytes()).hexdigest()
        results = run_panel(p, cand_name, sha, opp_path, opp_name, opp_sha, opp_family, seeds, max_workers=12)
        w = sum(1 for r in results if r['margin'] > 0)
        l = sum(1 for r in results if r['margin'] < 0)
        t = sum(1 for r in results if r['margin'] == 0)
        m = sum(r['margin'] for r in results) / len(results)
        total_wins += w
        total_losses += l
        total_ties += t
        all_margins.extend([r['margin'] for r in results])
        print(f"--> {cand_name} vs {opp_name}: {w}W - {l}L - {t}T (Mean margin: {m:+.1f})")

    overall_mean = sum(all_margins) / len(all_margins)
    print(f"\n==========================================")
    print(f"OVERALL {cand_name}: {total_wins}W - {total_losses}L - {total_ties}T | Win rate: {total_wins/len(all_margins)*100:.1f}% | Overall mean margin: {overall_mean:+.1f}")
    print(f"==========================================")

if __name__ == '__main__':
    main()
