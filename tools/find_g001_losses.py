import json
from pathlib import Path

p = Path('state/agent_experiments/g001_dynamic_confirm/results.json')
data = json.loads(p.read_text(encoding='utf-8'))

print("Total results:", len(data.get('results', [])))
losses_and_ties = []
for r in data.get('results', []):
    if r.get('outcome') in ('loss', 'tie'):
        losses_and_ties.append(r)

print(f"Losses and ties count: {len(losses_and_ties)}")
for r in losses_and_ties:
    print(f"Seed {r.get('seed')}, Seat {r.get('candidate_seat')}, Opp {r.get('opponent_name')}, Outcome {r.get('outcome')}, Margin {r.get('margin')}, Rewards {r.get('rewards')}")
