"""o152_post_budget_guard (Claude/o-series, 2026-09-14). Parent: c150 (unmodified, read-only).

Hypothesis (backlog item C, "General Liquidity / Commitment Guard", flagged high priority):
c150's chassis ships a generic `_budget_guard` (six_day_budget_guard.hpp port: at every
block-turns boundary, make sure cash + already-planned sells cover the block's own tape-scheduled
purchases/hires, else add extra SELLs of unprotected stock). c150 disables it
(`_SETTINGS['budget_guard'] = False`) — presumably because the route tape is self-funding by
construction and the check is redundant/conflicting with later overlays' own ad-hoc reserves.
BUT ~25 later overlays (tomato/carrot/livestock investment programs, extra HIREs, etc.) inject
*additional* BUY_SEED/BUY_ANIMAL/BUY_LAND/HIRE orders that `_budget_guard` never sees, because it
normally only runs once, mid-chassis, before those overlays execute.

This candidate does NOT edit c150.py. It calls the SAME already-existing, already-tested
`chassis._budget_guard(action, view, route, step)` method a second time, externally, on the FINAL
action after all ~25 overlays have run — so it can catch (and top up with extra SELLs) any
shortfall the overlays introduced that the base tape did not budget for. This is a direct
re-use/re-invocation experiment, not new financial logic: if `_budget_guard`'s own reasoning is
sound, applying it post-overlay should only ever ADD safety, never remove capability (it only
appends SELL orders, never removes existing orders, per its implementation at c150.py ~L754-790).

Reused attribution: `chassis._budget_guard`/`_block_requirements` are c150.py's own code
(ported from a `six_day_budget_guard.hpp` reference per its docstring), already covered by
c150.py's own upstream Apache-2.0 notices. This file adds no new third-party code, only an
external call site.
"""
import importlib.util
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_C150_PATH = os.path.join(_ROOT, "agent", "c150.py")

_spec = importlib.util.spec_from_file_location("_o152_c150_base", _C150_PATH)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

_PARENT_AGENT = _base.agent
_get = _base._get
_int = _base._int
_step_of = _base._step_of
_View = _base._View

_DIAG = {"guard_invocations": 0, "guard_extra_sells": 0, "guard_errors": 0}


def agent(observation, configuration=None):
    action = _PARENT_AGENT(observation, configuration)
    try:
        chassis = _base._IMPL.chassis
        player = _int(_get(observation, "player", 0))
        step = _step_of(observation)
        st = chassis.players.get(player)
        route = st["route"] if st else 0
        view = _View(observation, player, chassis.cfg)
        before = len(action.get("market") or [])
        chassis._budget_guard(action, view, route, step)
        after = len(action.get("market") or [])
        _DIAG["guard_invocations"] += 1
        if after > before:
            _DIAG["guard_extra_sells"] += 1
    except Exception:
        _DIAG["guard_errors"] += 1
    return action


agent.telemetry = _DIAG
