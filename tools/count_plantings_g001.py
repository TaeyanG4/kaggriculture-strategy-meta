from kaggle_environments.agent import build_agent
from kaggle_environments import make

a_g001, _ = build_agent('agent/g001_dynamic_liquidation.py', {}, 'kaggriculture')
a_v9, _ = build_agent('state/c312/public_v9_4.py', {}, 'kaggriculture')

env = make('kaggriculture', configuration={'seed': 416733134, 'episodeSteps': 720})
env.reset()

plantings = {}
for step in range(720):
    obs0 = env.state[0]['observation']
    obs0['step'] = step
    act0 = a_g001(obs0, {})
    day = step // 24
    if day >= 20:
        for c in [act0.get('farmer')] + list(act0.get('hands') or []):
            if c and len(c) >= 2 and c[0] == 'PLANT':
                crop = c[1]
                plantings[crop] = plantings.get(crop, 0) + 1
    
    env.step([act0, [{'farmer': ['PASS']}]])
    if env.done:
        break

print("g001 plantings after Day 20 on seed 416733134:")
for crop, count in sorted(plantings.items()):
    print(f"  {crop}: {count}")
