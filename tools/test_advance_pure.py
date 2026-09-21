import sys, hashlib
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
    opp_path = 'state/c312/public_v9_4.py'
    opp_sha = hashlib.sha256(Path(opp_path).read_bytes()).hexdigest()

    # Create candidate with only advance (cur = cur + extra), NO herd relax
    p, sha = create_candidate('proto_advance_only', frontload=False, advance=True, unblock_racepx=False, herd_relax=False)
    code = Path(p).read_text(encoding='utf-8')
    code = code.replace('cur = extra + cur', 'cur = cur + extra')
    Path(p).write_text(code, encoding='utf-8')
    sha = hashlib.sha256(Path(p).read_bytes()).hexdigest()

    print("Testing proto_advance_only (append) vs v9:")
    run_panel(p, 'proto_advance_only', sha, opp_path, 'v9', opp_sha, 'tschinkel_v9', seeds, max_workers=12)

if __name__ == '__main__':
    main()
