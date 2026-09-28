"""One saved-policy pass for exact response, immutability and service evidence.

This does not run matches or change frozen campaign code. New campaigns may
attach read-only observers and extract service state after the same 719 calls,
instead of loading and replaying the policy again for each type of evidence.
Actual opponent orders/private data enter scoring only after a proposal is
chosen, as in the preserved c470/c526 audit.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import time
from pathlib import Path
from typing import Callable


def trace(row: dict, *, private_model_key: str = "350",
          prepare: Callable | None = None, on_step: Callable | None = None,
          extract: Callable | None = None) -> dict:
    """Observers inspect this pass; they must not modify the policy or inputs.

    prepare(fn) may install transparent instrumentation before step 0. It must
    preserve return values; every resulting action is still checked exactly.
    on_step(fn, step, observation, action) gets detached observation/action
    copies. extract(fn) runs only after all original checks pass.
    """
    from state.c425.shadow import score

    started = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable

        replay_bytes = Path(row['replay']).read_bytes()
        rp = json.loads(replay_bytes.decode('utf-8-sig'))
        seat = int(row['job']['seat'])
        path = Path(row['job']['paths'][seat])
        source = path.read_bytes()
        source_sha = hashlib.sha256(source).hexdigest()
        expected = row['job'].get('hashes')
        if expected:
            assert expected[seat] == source_sha, 'audit source identity drift'
        assert len(rp['steps']) == 720, 'incomplete saved replay'
        fn = get_last_callable(source.decode('utf-8'), path=str(path))
        assert fn.__name__ == 'agent', 'official final callable is not agent'
        g = fn.__globals__
        original = g['_c396_response']
        offers = []
        model_calls = private_errors = 0

        def capture(obs, action, predicted, cfg):
            before = copy.deepcopy(action)
            chosen = original(obs, action, predicted, cfg)
            assert action == before, 'response mutated input action'
            if chosen != action:
                step = int(obs['step'])
                label = score(g, obs, action, chosen,
                              rp['steps'][step + 1][1-seat]['action'],
                              rp['steps'][step][1-seat]['observation']['private'], cfg)
                assert action.get('farmer') == chosen.get('farmer')
                assert action.get('hands') == chosen.get('hands')
                offers.append(dict(step=step, **label))
            return chosen

        g['_c396_response'] = capture
        if prepare is not None:
            prepare(fn)
        opponent = str(row['job'].get('opponent_id', row['job'].get('opponent', '')))
        check_private = opponent in (private_model_key, 'public' + private_model_key)
        for step in range(719):
            obs = dict(rp['steps'][step][0]['observation'],
                       **rp['steps'][step][seat]['observation'])
            passed = copy.deepcopy(obs)
            action = fn(passed, rp['configuration'])
            assert action == rp['steps'][step+1][seat]['action'], (row['job']['label'], step, 'action')
            assert passed == obs, (row['job']['label'], step, 'observation mutation')
            if check_private and private_model_key in g['_C396_MODELS']:
                model_calls += 1
                private_errors += g['_C396_MODELS'][private_model_key]['private'] != rp['steps'][step+1][1-seat]['observation']['private']
            if on_step is not None:
                on_step(fn, step, copy.deepcopy(obs), copy.deepcopy(action))
        result = dict(label=row['job']['label'], exact=719, offers=offers,
                      adverse=[v for v in offers if v['own_delta'] < 0 or v['margin_delta'] < 0 or not v['execution_preserved']],
                      new_model_calls=model_calls, new_model_private_errors=private_errors,
                      telemetry=dict(fn.telemetry))
        result['exact_actions'] = result['exact']
        result['qualified'] = (result['exact'] == 719 and not result['adverse']
                               and private_errors == 0 and result['telemetry'].get('c396_errors', 0) == 0)
        result['immutable'] = True
        if extract is not None:
            result['service'] = copy.deepcopy(extract(fn))
        result['audit_identity'] = dict(source_sha256=source_sha,
                                       replay_sha256=hashlib.sha256(replay_bytes).hexdigest(),
                                       private_model_key=private_model_key,
                                       policy_calls=719, new_matches=0)
        result['audit_seconds'] = time.perf_counter() - started
        return result
