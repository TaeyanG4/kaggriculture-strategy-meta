from kaggle_environments.agent import build_agent
from kaggle_environments import make

a_proto, _ = build_agent('agent/proto_g002.py', {}, 'kaggriculture')
a_g001, _ = build_agent('agent/g001_dynamic_liquidation.py', {}, 'kaggriculture')
a_v9, _ = build_agent('state/c312/public_v9_4.py', {}, 'kaggriculture')

def run_one(agent_under_test, name):
    env = make('kaggriculture', configuration={'seed': 416733134, 'episodeSteps': 720})
    env.reset()
    history = []
    for step in range(720):
        obs0 = env.state[0]['observation']
        obs1 = env.state[1]['observation']
        obs0['step'] = step
        obs1['step'] = step
        act0 = agent_under_test(obs0, {})
        act1 = a_v9(obs1, {})
        
        # log telemetry or actions
        history.append({
            'step': step,
            'act0': act0,
            'act1': act1,
            'money0': obs0['farms'][0]['money'],
            'money1': obs1['farms'][1]['money'],
            'shed0': dict(obs0['private']['shed']),
            'tiles0': [[t.get('crop') if isinstance(t, dict) else None for t in row] for row in obs0['farms'][0]['tiles']],
        })
        env.step([act0, act1])
        if env.done:
            break
    rew0 = env.state[0]['reward']
    rew1 = env.state[1]['reward']
    print(f"{name} final reward: {rew0} vs opp: {rew1}, margin: {rew0 - rew1}")
    return history

h_g001 = run_one(a_g001, "g001")
h_proto = run_one(a_proto, "proto_g002")

for step in range(720):
    g = h_g001[step]
    p = h_proto[step]
    g_units = [g['act0'].get('farmer')] + list(g['act0'].get('hands') or [])
    p_units = [p['act0'].get('farmer')] + list(p['act0'].get('hands') or [])
    if g_units != p_units:
        day = step // 24
        hour = step % 24
        print(f"\nFirst UNIT action diff at step {step} (d{day} h{hour}):")
        print(f"g001 units : {g_units}")
        print(f"proto units: {p_units}")
        print(f"g001 money: {g['money0']} vs proto money: {p['money0']}")
        print(f"g001 shed: {g['shed0']}")
        print(f"proto shed: {p['shed0']}")
        for s in range(step, min(step + 15, 720)):
            gs = h_g001[s]
            ps = h_proto[s]
            g_u = [gs['act0'].get('farmer')] + list(gs['act0'].get('hands') or [])
            p_u = [ps['act0'].get('farmer')] + list(ps['act0'].get('hands') or [])
            if g_u != p_u:
                print(f"  s{s} (d{s//24} h{s%24}): g001={g_u}\n              proto={p_u}")
        break
