import importlib.util, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

o152 = load(os.path.join(ROOT, "agent", "o152_post_budget_guard.py"), "_diag_o152")
opp = load(os.path.join(ROOT, "agent", "c150.py"), "_diag_opp")

from kaggle_environments import make
env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 100}, debug=False)

fires = []
orig_guard = o152._base._IMPL.chassis._budget_guard
def traced(action, view, route, step):
    before = list(action.get("market") or [])
    orig_guard(action, view, route, step)
    after = list(action.get("market") or [])
    if len(after) > len(before):
        added = after[:len(after)-len(before)]
        fires.append({"step": step, "money": view.money, "added": added, "shed": dict(view.shed)})
o152._base._IMPL.chassis._budget_guard = traced

env.run([o152.agent, opp.agent])
final = env.steps[-1]
print("final rewards", [s.reward for s in final])
print("guard fired", len(fires), "times")
for f in fires[:15]:
    print(f)
