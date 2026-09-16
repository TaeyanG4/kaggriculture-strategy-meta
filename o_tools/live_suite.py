"""Build a replay suite from ALL our live games (wins and losses) of the given submissions.
Downloads missing replays into o_replays/live_all/, then lays them out as 12 chunks in
o_replays/live_chunks/ for run_batch.ps1 -ChunkDir o_replays\\live_chunks -SuiteDir live_suite.
Usage: python o_tools/live_suite.py --subs 3          (newest N COMPLETE submissions)
       python o_tools/live_suite.py --sub 56241633 --sub 56241248
"""
import argparse, glob, json, os, shutil, subprocess, sys, time
import requests
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST_URL = 'https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
REPLAY_URL = 'https://www.kaggleusercontent.com/episodes/{id}.json'


def submissions(n):
    out = subprocess.run(['kaggle', 'competitions', 'submissions', '-c', 'kaggriculture'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
    return [l.split()[0] for l in out.splitlines() if l.strip() and l.split()[0].isdigit() and 'COMPLETE' in l][:n]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--subs', type=int, default=3); ap.add_argument('--sub', action='append'); ap.add_argument('--chunks', type=int, default=12)
    a = ap.parse_args(); subs = a.sub or submissions(a.subs)
    s = requests.Session(); s.headers['User-Agent'] = 'kaggriculture-strategy-meta live_suite'
    dst = os.path.join(ROOT, 'o_replays', 'live_all'); os.makedirs(dst, exist_ok=True)
    have = {os.path.basename(p).split('-')[0] for p in glob.glob(os.path.join(ROOT, 'o_replays', '*', '*-replay.json'))}
    index = []; got = 0
    for sid in subs:
        d = s.post(LIST_URL, json={'submissionId': int(sid)}, timeout=30).json()
        for e in d.get('episodes', []):
            if e.get('state') != 'COMPLETED':
                continue
            ag = e['agents']; me = [x for x in ag if str(x.get('submissionId')) == str(sid)]; op = [x for x in ag if str(x.get('submissionId')) != str(sid)]
            if not me or not op or me[0].get('reward') is None or op[0].get('reward') is None:
                continue
            eid = str(e['id']); index.append(dict(episode=int(eid), sub=sid, margin=me[0]['reward'] - op[0]['reward'], opp_rating=round(op[0].get('updatedScore') or 0), my_seat=ag.index(me[0])))
            f = os.path.join(dst, f'{eid}-replay.json')
            if eid in have or os.path.exists(f):
                continue
            rr = s.get(REPLAY_URL.format(id=eid), timeout=120)
            if rr.status_code == 200:
                open(f, 'wb').write(rr.content); got += 1; time.sleep(0.5)
    json.dump(index, open(os.path.join(dst, '_index.json'), 'w'), indent=1)
    # chunk layout: every replay of these episodes, wherever it already lives
    want = {str(x['episode']) for x in index}; files = {}
    for p in glob.glob(os.path.join(ROOT, 'o_replays', '*', '*-replay.json')) + glob.glob(os.path.join(ROOT, 'o_replays', '*', '*', '*-replay.json')):
        eid = os.path.basename(p).split('-')[0]
        if eid in want and eid not in files:
            files[eid] = p
    out = os.path.join(ROOT, 'o_replays', 'live_chunks')
    if os.path.exists(out):
        shutil.rmtree(out)
    for i, eid in enumerate(sorted(files)):
        d = os.path.join(out, f'c{i % a.chunks}'); os.makedirs(d, exist_ok=True); shutil.copy2(files[eid], d)
    wins = sum(x['margin'] > 0 for x in index)
    print(f'subs {subs}: {len(index)} games ({wins} W / {len(index)-wins} L), downloaded {got}, chunked {len(files)} into {a.chunks} chunks at {out}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
