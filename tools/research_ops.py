"""Compact research entry points. Never runs games or changes frozen artifacts."""
import argparse
from collections import deque
import copy
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def output(value, destination=None):
    payload = json.dumps(value, ensure_ascii=False, indent=2)
    if destination:
        p = Path(destination)
        # Derived outputs never overwrite a manifest, contract, or prior report.
        with p.open('x', encoding='utf-8') as stream:
            stream.write(payload + '\n')
    print(payload)


def history(query, limit):
    """Bounded, exact line references into the sole log and lesson index."""
    terms = query.casefold().split()
    found = []
    for name in ('docs/experiment-history-and-lessons.ko.md', 'HANDOFF.md'):
        for number, line in enumerate((ROOT/name).read_text(encoding='utf-8').splitlines(), 1):
            if all(t in line.casefold() for t in terms):
                found.append(dict(file=name, line=number, text=line[:900], truncated=len(line)>900))
    return dict(matches=len(found), shown=found[:limit], limits='Text retrieval only; historical claims still require source/code audit.')


def progress(campaign):
    # No row/outcome inspection while a campaign is running.
    logs = sorted(campaign.glob('console-*.log'), key=lambda p:p.stat().st_mtime)
    if not logs:
        return dict(status='no_console_log', campaign=str(campaign))
    with logs[-1].open(encoding='utf-8-sig') as stream:
        tail = list(deque(stream, maxlen=12))
    events = [json.loads(line.split('|',1)[1]) for line in tail if line.startswith('PROGRESS|')]
    return dict(log=str(logs[-1]), progress=events[-1] if events else None,
                runner_reported_done=any(line.startswith('DONE:') for line in tail),
                limits='Progress only; done is not a hash/health/performance verdict.')


def summarize(campaign):
    import validation_v2 as V
    m = V.check(campaign)
    rows = V.load_rows(campaign, m)
    if len(rows) != m['expected_jobs']:
        raise ValueError(f'Incomplete campaign {len(rows)}/{m["expected_jobs"]}; use progress, not partial performance.')
    fresh = V.analyze(m['plan'], m['stage'], rows)
    saved = read(campaign/'results.json')
    for key in ('status','completed_jobs','stage','by_candidate','comparisons'):
        if saved[key] != fresh[key]:
            raise ValueError('Stored aggregate differs from validated rows: '+key)
    if saved['contract_sha256'] != m['contract_sha256']:
        raise ValueError('Result contract drift')
    comparisons = {}
    for name, c in fresh['comparisons'].items():
        keys = ('family_weighted_point_delta','approximate_bootstrap_ci','adjusted_confidence',
                'mean_margin_delta','mean_own_cash_delta','win_to_loss','tie_to_loss','signal','changed_conditions')
        comparisons[name] = {k:c[k] for k in keys}
        comparisons[name]['by_opponent'] = {op:{k:d[k] for k in ('mean_point_delta','mean_margin_delta','win_to_loss','tie_to_loss')}
                                             for op,d in c['subgroups']['opponent'].items()}
        parent = next(x['parent'] for x in m['plan']['comparisons'] if x['candidate']+'_vs_'+x['parent']==name)
        other = [d for d in c['conditions'] if d['opponent']!=parent]
        if other:
            comparisons[name]['excluding_named_parent_descriptive'] = dict(
                n=len(other), point_delta=statistics.mean(d['point_delta'] for d in other),
                margin_delta=statistics.mean(d['margin_delta'] for d in other))
    counts = {name:{k:r[k] for k in ('games','wins','losses','ties','worst_margin','bottom_10pct_mean')}
              for name,r in fresh['by_candidate'].items()}
    return dict(campaign=str(campaign), stage=m['stage'], games=len(rows), hashes_pass=True,
                health_failures=0, max_seconds=max(r[role+'_timing']['max'] for r in rows for role in ('candidate','opponent')),
                counts=counts, comparisons=comparisons,
                decision='Apply the preregistered experiment gate; this tool does not invent a promotion rule.')


def subset(config, models):
    """Prepare a new execution subset, preserving each primary's alpha."""
    import validation_v2 as V
    original = read(config); V.validate_config(original)
    keep = set(models.split(','))
    if not keep or not keep.issubset(original['models']):
        raise ValueError('Unknown/empty model subset')
    p = copy.deepcopy(original)
    p['models'] = {k:v for k,v in p['models'].items() if k in keep}
    p['comparisons'] = [c for c in p['comparisons'] if c['candidate'] in keep and c['parent'] in keep]
    old_n = sum(c['primary'] for c in original['comparisons'])
    new_n = sum(c['primary'] for c in p['comparisons'])
    if not new_n:
        raise ValueError('Subset must retain a primary comparison and its parent')
    for stage in p['stages']:
        p['stages'][stage]['alpha'] *= new_n/old_n
    p.setdefault('arena_meta',{})['execution_subset'] = dict(source=str(config),source_sha256=V.L.digest(Path(config).read_bytes()),
        retained_models=sorted(keep), note='No source/seed/gate change; per-primary alpha retained. Use a new campaign directory.')
    V.validate_config(p)
    return p


def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='command',required=True)
    h=sub.add_parser('history');h.add_argument('query');h.add_argument('--limit',type=int,default=4)
    for name in ('progress','summary'):
        s=sub.add_parser(name);s.add_argument('campaign',type=Path)
        if name=='summary':s.add_argument('--save',type=Path)
    s=sub.add_parser('subset');s.add_argument('config',type=Path);s.add_argument('--models',required=True);s.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    if a.command=='history':output(history(a.query,a.limit))
    elif a.command=='progress':output(progress(a.campaign.resolve()))
    elif a.command=='summary':output(summarize(a.campaign.resolve()),a.save)
    elif a.command=='subset':output(subset(a.config.resolve(),a.models),a.out)


if __name__=='__main__':
    main()
