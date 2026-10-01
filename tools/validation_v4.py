"""Official v3 timing with Mapping telemetry and non-invasive recorder failures.

Historical v2/v3 files remain byte-identical. A recorder failure invalidates the
result through errors, but must never replace a policy's actual action.
"""
from collections.abc import Mapping
from pathlib import Path
import json
import math
import time
import validation_v3 as V3
V = V3.V


def telemetry_snapshot(value):
    if isinstance(value, Mapping):
        return {str(k): telemetry_snapshot(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [telemetry_snapshot(v) for v in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    return '<' + type(value).__name__ + '>'


def timed_policy(source, tag, timings, errors, hashes, telemetry):
    from kaggle_environments.agent import build_agent
    policy, _ = build_agent(source, {}, 'kaggriculture')

    def act(obs, config):
        if config.get('seed') is not None or 'seed' in obs or 'opponent_private' in obs:
            raise ValueError('Hidden-state boundary violation')
        started = time.perf_counter()
        try:
            action = policy(obs, config)
            hashes.update(json.dumps(action, sort_keys=True, separators=(',', ':')).encode())
        except Exception as exc:
            errors.append(dict(step=int(obs['step']), type=type(exc).__name__, message=str(exc)[:300]))
            raise
        finally:
            timings.append(time.perf_counter() - started)
        if int(obs['step']) == 718:
            try:
                for cell in policy.__closure__ or ():
                    value = cell.cell_contents
                    if callable(value) and hasattr(value, 'telemetry'):
                        snapshot = telemetry_snapshot(value.telemetry)
                        if not isinstance(snapshot, dict):
                            raise TypeError('Policy telemetry must be a Mapping')
                        telemetry.update(snapshot)
            except Exception as exc:
                errors.append(dict(step=718, stage='telemetry', type=type(exc).__name__, message=str(exc)[:300]))
        return action
    return act


def install():
    V3.install()
    V3.V.L.telemetry_snapshot = telemetry_snapshot
    V3.V.L.timed_policy = timed_policy
    wrapper = Path(__file__).resolve()
    if wrapper not in V3.V.SUPPORT:
        V3.V.SUPPORT += [wrapper]
    V3.V.__file__ = str(wrapper)


if __name__ == '__main__':
    install()
    V3.V.main()
