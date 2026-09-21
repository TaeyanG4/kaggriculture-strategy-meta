"""Faster pinned-world game loop: identical semantics to env.run (same interpreter, same step order) but the agents are called
directly on a shallow per-agent view of the live state instead of kaggle_environments' per-step deep copy of the whole state
(__get_shared_state), which was ~40% of a game's wall time. Optional deep mode also bypasses env.step's schema/structify pass.
Must stay bit-identical to env.run: o_tools/fastgame_check.py compares rewards and per-day cash on several seeds."""
import os, time
from kaggle_environments.utils import Struct

SHARED = ('farms', 'market', 'town', 'day', 'hour', 'step', 'remainingOverageTime')


def view(state, i):
    """Agent i's observation: shared fields from state[0], own player/private from state[i] (references, no copy)."""
    o0 = state[0].observation; oi = state[i].observation
    d = {}
    for k in SHARED:
        if k in o0:
            d[k] = o0[k]
    for k in oi.keys():
        if k not in d:
            d[k] = oi[k]
    return Struct(**d)


def step_direct(env, actions):
    """env.step without schema validation, structify and log capture: set actions, call the interpreter in place."""
    state = env.state
    for i, a in enumerate(actions):
        st = state[i]
        if isinstance(a, BaseException):
            st.status = 'ERROR'; st.action = None
        else:
            st.action = a
    new_state = env.interpreter(state, env)
    new_state[0].observation.step = len(env.steps)
    for ag in new_state:
        if ag.status in ('ERROR', 'INVALID', 'TIMEOUT'):
            ag.reward = None
    env.state = new_state
    if new_state[0].observation.step >= env.configuration.episodeSteps - 1:
        for st in new_state:
            if st.status in ('ACTIVE', 'INACTIVE'):
                st.status = 'DONE'
    env.steps.append(new_state)   # same objects each step (no snapshots): read day-end cash through the day_hook instead


def play(env, agents, deep=False, day_hook=None, step_hook=None, pre_hook=None):
    """Run a fresh env to the end with agents called directly. deep=True also bypasses env.step (no per-step snapshots);
    day_hook(env, day) is called at the state env.run records as steps[d*24+23] (after the h22 step) for on-the-fly recording. Returns env."""
    if env.state is None or len(env.steps) == 1 or env.done:
        env.reset(len(agents))
    cfg = env.configuration
    arity = [getattr(ag, '__code__', None).co_argcount if getattr(ag, '__code__', None) else 2 for ag in agents]
    while not env.done:
        st = env.state
        actions = []
        for i, ag in enumerate(agents):
            if st[i].status != 'ACTIVE':
                actions.append(None); continue
            v = view(st, i)
            try:
                actions.append(ag(v) if arity[i] == 1 else ag(v, cfg))
            except Exception as e:   # mirror the framework: an erroring agent is treated as ERROR status by env.step
                actions.append(e)
        step_before = env.state[0].observation.step
        if pre_hook is not None:
            pre_hook(env, step_before)   # state the actions were computed on (positions, tile yields)
        if deep:
            step_direct(env, actions)
        else:
            env.step(actions)
        if day_hook is not None and step_before % 24 == 22:
            day_hook(env, step_before // 24)   # same state env.run records at steps[d*24+23] (after 23 steps of the day)
        if step_hook is not None:
            step_hook(env, step_before)   # env.state now equals env.run's steps[step_before + 1]
    return env


def money_by_day(env, seat):
    """Per-day cash of one seat from the recorded steps (env.step still records states)."""
    st = env.steps
    return [st[min(len(st) - 1, d * 24 + 23)][0].observation['farms'][seat]['money'] for d in range(30)]
