"""o156_opponent_classifier (Claude/o-series, 2026-09-14). Parent: c150 (unmodified, read-only).

Behavior-NEUTRAL (same guarantee as o151): calls c150.agent() unmodified and returns its action
byte-for-byte. Adds a rule-based opponent-archetype label to telemetry (backlog F) using ONLY
publicly-visible fields (rival farm tiles/animals/money/quadrants) -- the same fields the c150
audit found are already read in 3 places (`_r37_similarity`, `_r37_quote_priority`, `_r44_before`)
for narrow mirror-detection, generalized here into a broader label set for analysis. This label is
NOT yet wired into any behavior change -- it is a research/telemetry tool to validate whether
opponent archetype correlates with outcome before building any DEFEND/CHASE-style reaction (the
audit found c150 has no existing general opponent-classifier or advantage-based mode, so this is
new capability, not a duplicate of anything already in the file).

Labels (first matching rule wins, checked in this order):
  MIRROR            -- tile-signature match ratio (c150's own _r37_similarity) >= 0.90
  WOOL_HEAVY        -- rival SHEEP count > own SHEEP count + 1, and >= 2 SHEEP total
  MILK_HEAVY        -- rival COW count > own COW count + 1, and >= 2 COW total
  EGG_HEAVY         -- rival GOOSE count > own GOOSE count + 1, and >= 2 GOOSE total
  CARROT_HEAVY      -- rival CARROT tile count > 1.5x own CARROT tile count, and >= 4 rival tiles
  HIGH_VALUE_CROP   -- rival TOMATO+STRAWBERRY+MELON tile count > 1.5x own, and >= 4 rival tiles
  EARLY_EXPANDER    -- rival unlocked_quadrants > own unlocked_quadrants (step < 288, i.e. day<12)
  LATE_EXPANDER     -- own unlocked_quadrants > rival unlocked_quadrants (step < 288)
  HIGH_WORKER       -- rival hand count > own hand count + 2
  LOW_WORKER        -- own hand count > rival hand count + 2
  UNKNOWN           -- none of the above (most common case, especially early game)

Env vars: O156_LOG (default o_results/o156_opponent_labels.jsonl), O156_LOG_DISABLE=1.
"""
import importlib.util
import json
import os
import threading

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_C150_PATH = os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o156_c150_base", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of
_View = _base._View
_r37_similarity = getattr(_base, "_r37_similarity", None)

_LOG_PATH = os.environ.get("O156_LOG", os.path.join(_ROOT, "o_results", "o156_opponent_labels.jsonl"))
_LOG_DISABLE = os.environ.get("O156_LOG_DISABLE") == "1"
_LOCK = threading.Lock()
_RUN_ID = os.environ.get("O156_RUN_ID", str(os.getpid()))


def _tile_counts(tiles):
    crops, animals = {}, {}
    for row in tiles or []:
        for t in row or []:
            if not isinstance(t, dict):
                continue
            if t.get("kind") == "PLANT" and t.get("crop"):
                crops[t["crop"]] = crops.get(t["crop"], 0) + 1
            elif t.get("kind") in ("COOP", "PASTURE") and t.get("animal"):
                animals[t["animal"]] = animals.get(t["animal"], 0) + 1
    return crops, animals


def classify(observation, view, rview, step):
    own_crops, own_animals = _tile_counts(view.tiles)
    rival_crops, rival_animals = _tile_counts(rview.tiles)
    try:
        sim = _r37_similarity(observation) if _r37_similarity else 0.0
    except Exception:
        sim = 0.0
    if sim >= 0.90:
        return "MIRROR", sim
    if rival_animals.get("SHEEP", 0) >= 2 and rival_animals.get("SHEEP", 0) > own_animals.get("SHEEP", 0) + 1:
        return "WOOL_HEAVY", sim
    if rival_animals.get("COW", 0) >= 2 and rival_animals.get("COW", 0) > own_animals.get("COW", 0) + 1:
        return "MILK_HEAVY", sim
    if rival_animals.get("GOOSE", 0) >= 2 and rival_animals.get("GOOSE", 0) > own_animals.get("GOOSE", 0) + 1:
        return "EGG_HEAVY", sim
    rival_carrot = rival_crops.get("CARROT", 0)
    own_carrot = own_crops.get("CARROT", 0)
    if rival_carrot >= 4 and rival_carrot > 1.5 * max(1, own_carrot):
        return "CARROT_HEAVY", sim
    rival_hv = sum(rival_crops.get(c, 0) for c in ("TOMATO", "STRAWBERRY", "MELON"))
    own_hv = sum(own_crops.get(c, 0) for c in ("TOMATO", "STRAWBERRY", "MELON"))
    if rival_hv >= 4 and rival_hv > 1.5 * max(1, own_hv):
        return "HIGH_VALUE_CROP", sim
    if step < 288:
        if rview.quadrants > view.quadrants:
            return "EARLY_EXPANDER", sim
        if view.quadrants > rview.quadrants:
            return "LATE_EXPANDER", sim
    if len(rview.positions) > len(view.positions) + 2:
        return "HIGH_WORKER", sim
    if len(view.positions) > len(rview.positions) + 2:
        return "LOW_WORKER", sim
    return "UNKNOWN", sim


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
    if _LOG_DISABLE:
        return action
    try:
        cfg = _base._IMPL.chassis.cfg
        player = _int(_get(observation, "player", 0))
        step = _step_of(observation)
        view = _View(observation, player, cfg)
        rview = _View(observation, 1 - player, cfg)
        label, sim = classify(observation, view, rview, step)
        rec = {"run": _RUN_ID, "step": step, "player": player, "label": label, "similarity": sim,
               "own_money": view.money, "rival_money": rview.money}
        with _LOCK:
            os.makedirs(os.path.dirname(_LOG_PATH), exist_ok=True)
            with open(_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, default=str) + "\n")
    except Exception:
        pass
    return action
