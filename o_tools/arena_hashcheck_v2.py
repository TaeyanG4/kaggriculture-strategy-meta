"""Before/after identity record for a canonical campaign (no games): config file hash, every model/opponent = config sha == repo file now
== campaign snapshot, engine identity == config, manifest plan == config, contract and runner support hashes, and how many results exist.
Writes hashcheck-<utc>.json into the campaign dir (run once before -Action Run and once after) and exits 1 on any mismatch.
Usage: python o_tools/arena_hashcheck.py <config.json> <campaign_out_dir>"""
import datetime, hashlib, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'tools'))
from src.kaggriculture_meta import championship_league as L
from validation_v2 import support_hashes


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    cfg_path, out = sys.argv[1], sys.argv[2]
    cfg = json.load(open(cfg_path, encoding='utf-8-sig')); man = json.load(open(os.path.join(out, 'manifest.json'), encoding='utf-8'))
    rec = dict(utc=datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z', config=cfg_path, config_sha256=sha(cfg_path), campaign=out, stage=man['stage'], contract_sha256=man['contract_sha256'], sources=[], problems=[])
    if man['plan'] != cfg:
        rec['problems'].append('manifest plan differs from the config file')
    eng = L.engine_identity()
    rec['engine_ok'] = eng == cfg['engine'] == man['engine']
    if not rec['engine_ok']:
        rec['problems'].append('engine identity differs from config/manifest')
    rec['runner_ok'] = man['support'] == support_hashes()
    if not rec['runner_ok']:
        rec['problems'].append('runner/support files changed since prepare')
    for group in ('models', 'opponents'):
        for name, ref in cfg[group].items():
            repo = os.path.join(ROOT, ref['path']); snap = os.path.join(out, 'sources', ref['sha256'] + '.py')
            row = dict(group=group, name=name, path=ref['path'], config_sha=ref['sha256'], repo_sha=sha(repo) if os.path.exists(repo) else None, snapshot_sha=sha(snap) if os.path.exists(snap) else None)
            row['ok'] = row['repo_sha'] == row['config_sha'] == row['snapshot_sha'] == man[group][name]['sha256']
            if not row['ok']:
                rec['problems'].append(f'{group}/{name}: config {ref["sha256"][:12]} repo {str(row["repo_sha"])[:12]} snapshot {str(row["snapshot_sha"])[:12]}')
            rec['sources'].append(row)
    jobs = os.path.join(out, 'jobs')
    rec['results_present'] = sum(1 for d in (os.listdir(jobs) if os.path.isdir(jobs) else []) if os.path.exists(os.path.join(jobs, d, 'result.json')))
    rec['expected_jobs'] = man['expected_jobs']; rec['results_json'] = os.path.exists(os.path.join(out, 'results.json'))
    path = os.path.join(out, f"hashcheck-{rec['utc'].replace(':', '')}.json"); json.dump(rec, open(path, 'w', encoding='utf-8'), indent=1)
    for r in rec['sources']:
        print(f"{'OK ' if r['ok'] else 'BAD'} {r['group']:9s} {r['name']:28s} {r['config_sha'][:16]} repo {'=' if r['repo_sha'] == r['config_sha'] else 'DIFF'} snapshot {'=' if r['snapshot_sha'] == r['config_sha'] else 'DIFF'}")
    print(f"engine {'OK' if rec['engine_ok'] else 'BAD'} | runner {'OK' if rec['runner_ok'] else 'BAD'} | plan==config {'OK' if man['plan'] == cfg else 'BAD'} | contract {man['contract_sha256'][:12]} | config sha {rec['config_sha256'][:12]} | results {rec['results_present']}/{rec['expected_jobs']} | record {os.path.basename(path)}")
    if rec['problems']:
        print('PROBLEMS:'); [print('  -', p) for p in rec['problems']]; sys.exit(1)
    print('HASHCHECK PASSED')


if __name__ == '__main__':
    main()
