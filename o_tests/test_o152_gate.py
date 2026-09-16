"""Gate 1+2 for o152_post_budget_guard: importable/callable; identical to c150 off block
boundaries; only differs (by adding SELL orders, never removing/reordering non-SELL orders) on
step % 72 == 0.

Usage: .venv/Scripts/python.exe o_tests/test_o152_gate.py
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def main():
    c150 = load(os.path.join(ROOT, "agent", "c150.py"), "_g2_c150")
    o152 = load(os.path.join(ROOT, "agent", "o152_post_budget_guard.py"), "_g2_o152")
    opp = load(os.path.join(ROOT, "agent", "c150.py"), "_g2_opp")

    from kaggle_environments import make
    off_boundary_mismatches = 0
    boundary_hits = 0
    non_sell_diffs = 0
    for seed in (1, 2, 3, 4):
        def run(fn):
            e = make("kaggriculture", configuration={"episodeSteps": 100, "seed": seed}, debug=False)
            out = []

            def wrapped(obs, cfg=None):
                a = fn(obs, cfg) if cfg is not None else fn(obs)
                out.append((obs.step if hasattr(obs, "step") else obs.get("step"),
                             json.loads(json.dumps(a, default=str))))
                return a
            e.run([wrapped, opp])
            return out

        base = run(c150)
        cand = run(o152)
        for (s1, a1), (s2, a2) in zip(base, cand):
            assert s1 == s2
            step = s1
            if step % 72 != 0:
                if a1 != a2:
                    off_boundary_mismatches += 1
                    print(f"OFF-BOUNDARY MISMATCH seed={seed} step={step}: c150={a1} o152={a2}")
            else:
                boundary_hits += 1
                m1 = [o for o in (a1.get("market") or []) if o[0] != "SELL"]
                m2 = [o for o in (a2.get("market") or []) if o[0] != "SELL"]
                if m1 != m2 or a1.get("farmer") != a2.get("farmer") or a1.get("hands") != a2.get("hands"):
                    non_sell_diffs += 1
                    print(f"BOUNDARY NON-SELL DIFF seed={seed} step={step}: c150={a1} o152={a2}")
    print(f"off_boundary_mismatches={off_boundary_mismatches} boundary_steps_seen={boundary_hits} non_sell_diffs={non_sell_diffs}")
    if off_boundary_mismatches or non_sell_diffs:
        print("FAIL")
        sys.exit(1)
    print("PASS: o152 only ever adds SELL orders, only at block boundaries")


if __name__ == "__main__":
    main()
