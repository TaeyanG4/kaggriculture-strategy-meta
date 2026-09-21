import importlib.util
from pathlib import Path
from kaggle_environments import make

spec = importlib.util.spec_from_file_location("mod", "agent/g000_apex_frontier.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

env = make('kaggriculture', configuration={'seed': 416733134, 'episodeSteps': 720})
env.reset()

for step in range(720):
    obs = env.state[0]['observation']
    obs['step'] = step
    act = mod.agent(obs, {})
    m = act.get('market', [])
    for o in m:
        if len(o) > 2 and o[0] == 'SELL' and o[1] in ('STRAWBERRY', 'WOOL', 'EGG', 'MILK', 'MELON', 'CARROT', 'TOMATO'):
            # check if this was an advance
            pass
    env.step([act, []])
