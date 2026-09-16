"""Build r001_leader_rules = agent/o001_demand_planner.py (operator) + overlays/r001_leader_rules.py
with the leader's median trajectory (state/o_dev/r001/leader_targets.json) embedded."""
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o001_demand_planner.py"; OVERLAY = ROOT / "agent/overlays/r001_leader_rules.py"
TARGET = ROOT / "agent/r001_leader_rules.py"
rows = json.load(open(ROOT / "state/o_dev/r001/leader_targets.json"))
targets = {}
for r in rows:
    targets[r["day"]] = {k: r[k] for k in ("COW", "SHEEP", "GOOSE", "MELON", "WHEAT", "STRAWBERRY", "TOMATO", "CARROT", "quads")}
    targets[r["day"]]["tomato_by_shops"] = {str(k): v[0] for k, v in r["tomato_by_shops"].items()}
hires = [4, 8, 6, 6, 6, 6, 8, 9, 9, 10] + [11] * 18 + [10, 10]
parent = PARENT.read_text(encoding="utf-8"); overlay = OVERLAY.read_text(encoding="utf-8")
body = overlay.replace("%(targets)s", repr(targets)).replace("%(hires)s", repr(hires))
out = parent + "\n\n" + body
compile(out, "r001", "exec"); TARGET.write_text(out, encoding="utf-8")
print("built", TARGET, len(out), "bytes sha256", hashlib.sha256(out.encode()).hexdigest()[:16], "parent sha", hashlib.sha256(parent.encode()).hexdigest()[:16])
