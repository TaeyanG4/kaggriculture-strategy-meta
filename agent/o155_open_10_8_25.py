"""o155_opening_sweep (Claude/o-series, 2026-09-14). Parent: c150 (unmodified, read-only).

Backlog W (parameter search): c150's own step-0 opening market override (_R42_OPENING) is
BUY_PRODUCT WHEAT 10 + BUY_PRODUCT WHEAT 8 + SELL WHEAT 25 (a fixed constant, not
tuned per this variant). This candidate overrides step-0's market action a second time,
externally, with an alternative (buy1=10, buy2=8, sell=25) to screen for a better
opening. Every other step is untouched (parent action passed straight through).
"""
import importlib.util
import os as _os

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_C150_PATH = _os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o155_c150_base_o155_open_10_8_25", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of

_OPENING = [["BUY_PRODUCT", "WHEAT", 10], ["BUY_PRODUCT", "WHEAT", 8], ["SELL", "WHEAT", 25]]


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
    try:
        if _step_of(observation) == 0:
            action = dict(action)
            action["market"] = [list(o) for o in _OPENING]
    except Exception:
        pass
    return action
