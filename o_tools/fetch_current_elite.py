"""Fetch the latest public episodes of the current leaderboard elite (by their public-leaderboard submission ids) and store
the replays under o_replays/elite_current/<team>/<episode>-replay.json with a per-team _index.json (opponent, margin, ratings).
Usage: python o_tools/fetch_current_elite.py --subs "Unknown Mother-Goose:56266758,Majkel1337:56216119,..." [--max 60] [--min-rating 2900]
The episode list endpoint is public (submissionId); replays come from kaggleusercontent. Incremental: existing files are kept."""
import argparse, json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
REPLAY_URL = "https://www.kaggleusercontent.com/episodes/{id}.json"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--subs', required=True); ap.add_argument('--max', type=int, default=60); ap.add_argument('--min-rating', type=float, default=0.0)
    ap.add_argument('--out', default='o_replays/elite_current')
    a = ap.parse_args()
    import requests
    s = requests.Session(); s.headers['User-Agent'] = 'kaggriculture-strategy-meta fetch_current_elite'
    for spec in a.subs.split(','):
        team, sid = spec.rsplit(':', 1); sid = int(sid)
        d = os.path.join(ROOT, a.out, team.replace('/', '_').replace(' ', '_')); os.makedirs(d, exist_ok=True)
        r = None
        for attempt in range(4):
            r = s.post(LIST_URL, json={'submissionId': sid}, timeout=60)
            if r.status_code == 429:
                time.sleep(10); continue
            break
        if r is None or r.status_code != 200:
            print(f'{team}: list http {r.status_code if r else None}'); continue
        data = r.json(); json.dump(data, open(os.path.join(d, f'_episodes_{sid}.json'), 'w'))
        eps = [e for e in data.get('episodes', []) if e.get('state') == 'COMPLETED']
        eps.sort(key=lambda e: e.get('createTime', ''), reverse=True)
        teams = {t['id']: t.get('teamName') for t in data.get('teams', [])}
        idxp = os.path.join(d, '_index.json'); idx = json.load(open(idxp)) if os.path.exists(idxp) else []
        have = {x['episode'] for x in idx}
        got = 0; ratings = []
        for e in eps:
            ag = e.get('agents', [])
            me = next((x for x in ag if x.get('submissionId') == sid), None); op = next((x for x in ag if x.get('submissionId') != sid), None)
            if not me or not op or me.get('reward') is None or op.get('reward') is None:
                continue
            opr = op.get('updatedScore') or 0
            if opr < a.min_rating:
                continue
            eid = int(e['id'])
            if eid in have:
                continue
            if got >= a.max:
                break
            rr = s.get(REPLAY_URL.format(id=eid), timeout=120)
            if rr.status_code != 200:
                print(f'{team}: replay {eid} http {rr.status_code}'); time.sleep(3); continue
            open(os.path.join(d, f'{eid}-replay.json'), 'wb').write(rr.content)
            idx.append(dict(episode=eid, sub=sid, created=e.get('createTime'), my_seat=ag.index(me), margin=me['reward'] - op['reward'], bank=me['reward'], opp_team=teams.get(op.get('teamId'), str(op.get('teamId'))), opp_rating=opr, my_rating=me.get('updatedScore')))
            have.add(eid); got += 1; ratings.append(me.get('updatedScore') or 0)
            time.sleep(0.8)
        json.dump(idx, open(idxp, 'w'), indent=0)
        print(f"{team} sub {sid}: {len(eps)} completed episodes listed ({eps[-1]['createTime'][:10] if eps else '-'} .. {eps[0]['createTime'][:10] if eps else '-'}), downloaded {got} new (index {len(idx)}), rating now {max(ratings) if ratings else '-'}")
        time.sleep(2)


if __name__ == '__main__':
    main()
