import sys, hashlib
from pathlib import Path
ROOT = Path('.').resolve()
sys.path.insert(0, str(ROOT))
from tools.bench_screen import run_panel

def main():
    code = Path('agent/proto_advance.py').read_text(encoding='utf-8')
    # Test only STRAWBERRY, MILK, WOOL, MELON
    code_mod = code.replace(
        "_G000_PREMIUM = ('STRAWBERRY', 'WOOL', 'EGG', 'MILK', 'MELON', 'CARROT', 'TOMATO')",
        "_G000_PREMIUM = ('STRAWBERRY', 'MILK', 'WOOL', 'MELON')"
    )
    p = Path('agent/proto_adv_prem.py')
    p.write_text(code_mod, encoding='utf-8', newline='\n')
    sha = hashlib.sha256(p.read_bytes()).hexdigest()

    opp_path = 'state/c312/public_v9_4.py'
    opp_sha = hashlib.sha256(Path(opp_path).read_bytes()).hexdigest()

    seeds = [
        1542303036, 1384849883, 458410889, 1101525775,
        287049605, 1869390184, 1822423521, 1626853671,
        1468257305, 931118787, 572378660, 1606616802,
        492309603, 1016436360, 1181567501, 1556571517
    ]

    print("Testing proto_adv_prem vs v9...")
    run_panel(str(p), 'proto_adv_prem', sha, opp_path, 'v9', opp_sha, 'tschinkel_v9', seeds, max_workers=12)

if __name__ == '__main__':
    main()
