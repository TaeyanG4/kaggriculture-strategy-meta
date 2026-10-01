"""Read-only, bounded summaries for session handoff and experiment review."""
import argparse
import json
import sqlite3
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / 'state/continuation-20260929/owner-request.json'
MAX_JSON_BYTES = 4 * 1024 * 1024


def read(path):
    path = Path(path)
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError('Use a summary file, not a replay or ledger larger than 4 MiB')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def bounded(value, depth=0):
    if isinstance(value, str):
        return value if len(value) <= 180 else value[:177] + '...'
    if isinstance(value, list):
        return {'items': len(value)}
    if isinstance(value, dict):
        if depth >= 2:
            return {'keys': list(value)[:12], 'key_count': len(value)}
        selected = {k: bounded(v, depth+1) for k, v in list(value.items())[:12]}
        if len(value) > 12:
            selected['_omitted_keys'] = len(value)-12
        return selected
    return value


def select(data, keys):
    return {k: bounded(data[k]) for k in keys if k in data}


def resolve(name):
    path = Path(name)
    if path.is_absolute():
        return path
    return ROOT/path


def stage_summary(name):
    path = resolve('state/'+name) if name.startswith('c') and name[1:].isdigit() else resolve(name)
    report = {'stage': path.name}
    primary = 'completion-ready.json' if (path/'completion-ready.json').exists() else 'development-summary.json'
    for filename in (primary, 'review-decision.json'):
        item = path/filename
        if item.exists():
            data = read(item)
            report[filename] = select(data, ('at', 'decision', 'adopt', 'execution_pass', 'execution_qualified',
                'overall', 'combined', 'exact', 'total', 'new_games', 'cached_games', 'source_sha256', 'error', 'limits'))
    report['original_error_preserved'] = (path/'execution-error.json').exists()
    return report


def local_summary():
    db = sqlite3.connect((ROOT/'state/public_league/league.sqlite3').as_uri()+'?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    try:
        row = db.execute('SELECT id,status,games,wins,losses,ties,rating FROM agents WHERE id=387').fetchone()
        return dict(row) if row else {'missing_agent': 387}
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', help='Stage number such as c997, or its directory')
    parser.add_argument('--file', help='Small JSON file; requires --keys')
    parser.add_argument('--keys', help='Comma-separated top-level keys, maximum eight')
    parser.add_argument('--live', action='store_true', help='One local progress request; never polls or starts jobs')
    args = parser.parse_args()
    if args.file:
        keys = args.keys.split(',') if args.keys else []
        if not 1 <= len(keys) <= 8:
            parser.error('--file requires one to eight comma-separated --keys')
        output = {'file': args.file, **select(read(resolve(args.file)), keys)}
    elif args.stage:
        output = stage_summary(args.stage)
    else:
        data = read(POLICY)
        output = select(data, ('phase', 'baseline', 'current_decision_receipt', 'latest_submission_id',
            'latest_submission_status', 'remaining_submission_allowance', 'next'))
        output['local_agent'] = local_summary()
    if args.live:
        with urllib.request.urlopen('http://127.0.0.1:8791/api/progress', timeout=10) as response:
            data = json.load(response)
        output['live'] = select(data, ('running', 'cycle', 'battle', 'auto_collect_enabled'))
    encoded = json.dumps(output, ensure_ascii=False, separators=(',', ':'))
    if len(encoded) > 5000:
        raise ValueError('Summary exceeds 5000 characters; request fewer keys')
    print(encoded)


if __name__ == '__main__':
    main()
