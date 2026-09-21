from kaggle_environments.agent import build_agent
from kaggle_environments import make

a_g001, _ = build_agent('agent/g001_dynamic_liquidation.py', {}, 'kaggriculture')
env = make('kaggriculture', configuration={'seed': 163122924, 'episodeSteps': 720})
env.reset()

for step in range(720):
    obs0 = env.state[0]['observation']
    obs0['step'] = step
    act0 = a_g001(obs0, {})
    if 570 <= step <= 590:
        prices = obs0['market']['prices']
        inv = obs0['market']['inventory']
        shed = obs0['private']['shed']
        mkt = act0.get('market', [])
        print(f"Step {step} (d{step//24} h{step%24}): straw_px={prices.get('STRAWBERRY')} straw_inv={inv.get('STRAWBERRY')} shed_straw={shed.get('STRAWBERRY')} mkt={mkt}")
    env.step([act0, [{'farmer': ['PASS']}]])
    if env.done:
        break
