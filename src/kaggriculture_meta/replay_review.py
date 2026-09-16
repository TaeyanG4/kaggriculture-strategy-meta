"""Read recorded observations only. Never import or execute an agent/engine."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


def farm_counts(farm):
    return dict(Counter(t.get('crop') or t.get('animal') or t.get('kind')
                        for row in farm['tiles'] for t in row if isinstance(t, dict)))


def review(path, candidate_seat):
    raw = Path(path).read_bytes()
    replay = json.loads(raw)
    steps = replay['steps']
    events, daily, differences = [], [], {'field': [], 'market': []}
    cash_moves = []
    for n in range(1, len(steps)):
        before, after = steps[n - 1], steps[n]
        old, new = before[0]['observation']['farms'], after[0]['observation']['farms']
        actions = [s.get('action') or {} for s in after]
        if [(a.get('farmer'), a.get('hands')) for a in actions][0] != (
                actions[1].get('farmer'), actions[1].get('hands')):
            differences['field'].append(n - 1)
        if actions[0].get('market') != actions[1].get('market'):
            differences['market'].append(n - 1)
        for seat in (0, 1):
            for y, row in enumerate(old[seat]['tiles']):
                for x, tile in enumerate(row):
                    later = new[seat]['tiles'][y][x]
                    if isinstance(tile, dict) and tile.get('animal') and (
                            not isinstance(later, dict) or later.get('animal') != tile['animal']):
                        events.append({'step': n - 1, 'seat': seat, 'event': 'animal_disappeared',
                                       'pos': [x, y], 'animal': tile['animal'], 'before': tile,
                                       'after': later})
            action = actions[seat]
            positions = [old[seat]['farmer'], *old[seat]['hands']]
            inventories = before[seat]['observation']['private']['inventories']
            for actor, command in enumerate([action.get('farmer', []), *action.get('hands', [])]):
                if (actor >= len(positions) or not isinstance(command, list)
                        or len(command) < 2 or command[0] != 'PLACE'
                        or command[1] not in ('COW', 'SHEEP', 'GOOSE')):
                    continue
                x, y = positions[actor]
                tile, later = old[seat]['tiles'][y][x], new[seat]['tiles'][y][x]
                if not isinstance(later, dict) or later.get('animal') != command[1]:
                    events.append({'step': n - 1, 'seat': seat, 'event': 'place_without_animal_on_target',
                                   'actor': actor, 'command': command, 'pos': [x, y],
                                   'carried': inventories[actor] if actor < len(inventories) else {},
                                   'before': tile, 'after': later,
                                   'note': 'Observation fact, may be intentional shed deposit; not automatically an error'})
        old_margin = old[candidate_seat]['money'] - old[1-candidate_seat]['money']
        new_margin = new[candidate_seat]['money'] - new[1-candidate_seat]['money']
        cash_moves.append({'step': n - 1, 'margin_delta': new_margin - old_margin,
                           'margin': new_margin, 'market': [a.get('market', []) for a in actions]})
    for n in sorted(set([0, 2, *range(24, len(steps), 24), len(steps)-1])):
        state = steps[n]
        obs = state[0]['observation']
        daily.append({'step': n, 'cash': [f['money'] for f in obs['farms']],
                      'tiles': [farm_counts(f) for f in obs['farms']],
                      'shed': [s['observation']['private']['shed'] for s in state],
                      'carried': [s['observation']['private']['inventories'] for s in state],
                      'prices': obs['market']['prices'], 'shops': obs['town']['unlocked_shops']})
    return {'episode': replay['info']['EpisodeId'], 'candidate_seat': candidate_seat,
            'source_sha256': hashlib.sha256(raw).hexdigest(), 'states': len(steps),
            'evidence_type': 'recorded_observation_analysis_no_engine_execution',
            'team_names': replay['info']['TeamNames'], 'rewards': [s['reward'] for s in steps[-1]],
            'first_market_orders': [s['action'].get('market', []) for s in steps[1]],
            'differences': {k: {'count': len(v), 'first_steps': v[:20]} for k, v in differences.items()},
            'checkpoints': daily, 'events': events,
            'largest_margin_drops': sorted(cash_moves, key=lambda x: x['margin_delta'])[:12],
            'note': 'Cash timing shifts are not causal lost profit. Transaction attribution requires the user-run instrumented reproduction.'}
