"""Gate 1+2 check for o151_telemetry: importable, callable, and byte-identical actions to c150
across a handful of seeded steps (telemetry must not change behavior).

Usage: .venv/Scripts/python.exe o_tests/test_o151_neutral.py
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def main():
    os.environ["O151_LOG"] = os.path.join(ROOT, "o_tests", "_scratch_o151.jsonl")
    if os.path.exists(os.environ["O151_LOG"]):
        os.remove(os.environ["O151_LOG"])
    c150 = load(os.path.join(ROOT, "agent", "c150.py"), "_gate_c150")
    o151 = load(os.path.join(ROOT, "agent", "o151_telemetry.py"), "_gate_o151")

    from kaggle_environments import make
    mismatches = 0
    total = 0
    for seed in (1, 2, 3):
        env = make("kaggriculture", configuration={"episodeSteps": 40, "seed": seed}, debug=False)
        # Run c150 vs c150 to get real trajectories, then re-derive: instead, run o151 as seat0
        # vs a fixed simple opponent and separately c150 vs the same opponent with the same seed,
        # comparing seat-0 actions turn by turn (env state should match since seat0 policy call
        # order is deterministic given identical opponent and seed).
        opp_path = os.path.join(ROOT, "agent", "c150.py")
        opp = load(opp_path, f"_gate_opp_{seed}")

        def run(agent_fn):
            e = make("kaggriculture", configuration={"episodeSteps": 40, "seed": seed}, debug=False)
            actions = []
            captured = {}

            def wrapped(obs, cfg=None):
                out = agent_fn(obs, cfg) if cfg is not None else agent_fn(obs)
                actions.append(json.loads(json.dumps(out, default=str)))
                return out
            e.run([wrapped, opp])
            return actions

        a_c150 = run(c150)
        a_o151 = run(o151)
        total += len(a_c150)
        for i, (x, y) in enumerate(zip(a_c150, a_o151)):
            if x != y:
                mismatches += 1
                print(f"MISMATCH seed={seed} step={i}: c150={x} o151={y}")
    print(f"compared {total} decisions, mismatches={mismatches}")
    if mismatches == 0:
        print("PASS: o151_telemetry is behavior-neutral over tested seeds/steps")
    else:
        print("FAIL: telemetry wrapper changed behavior")
        sys.exit(1)


if __name__ == "__main__":
    main()
