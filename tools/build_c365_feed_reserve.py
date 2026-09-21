"""Build c365: c358 with the existing CARROT2 feed reserve set to one day."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = "680a4f713d8d672dce3f13f5429df1f803626f408d76e1690eabe32152779196"
PARENT = ROOT / "agent/c358_localbest_hybrid.py"


WRAPPER = r'''

# c365: preserve c358 and change only the existing CARROT2 controller's
# feed-reserve horizon from two days to one. Public One More Wheat, Metav4,
# V54 and Pipe16 use the same one-day horizon. Integration: Taeyang/Codex, 2026.
_C365_ENABLED = __C365_ENABLED__
_C365_PARENT = agent
_C365_REPORT = {}


def _c365_find_carrot_namespace(namespace):
    seen = set()
    while isinstance(namespace, dict) and id(namespace) not in seen:
        seen.add(id(namespace))
        if "_CA_FEED_DAYS" in namespace and "_CA_REPORT" in namespace:
            return namespace
        namespace = namespace.get("_BASE_NS")
    return None


_C365_CA_NS = _c365_find_carrot_namespace(globals())
if _C365_CA_NS is None:
    raise RuntimeError("c365 could not locate the CARROT2 controller")
_C365_PARENT_FEED_DAYS = _C365_CA_NS["_CA_FEED_DAYS"]
if _C365_PARENT_FEED_DAYS != 2:
    raise RuntimeError("c365 parent feed-reserve contract drift")


def agent(observation, configuration=None):
    _C365_CA_NS["_CA_FEED_DAYS"] = 1 if _C365_ENABLED else _C365_PARENT_FEED_DAYS
    action = _C365_PARENT(observation, configuration)
    report = _C365_CA_NS.get("_CA_REPORT", {})
    _C365_REPORT.clear()
    _C365_REPORT.update(
        enabled=int(_C365_ENABLED),
        feed_days=int(_C365_CA_NS["_CA_FEED_DAYS"]),
        ca_swaps=int(report.get("ca_swaps", 0)),
        ca_feed_block=int(report.get("ca_feed_block", 0)),
        ca_errors=int(report.get("ca_errors", 0)),
    )
    return action


agent.telemetry = _C365_REPORT
kaggle_submission_agent = agent
c365_submission_agent = agent
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--disabled", action="store_true")
    args = parser.parse_args()
    body = PARENT.read_bytes()
    if hashlib.sha256(body).hexdigest() != PARENT_SHA:
        raise SystemExit("c358 parent identity drift")
    suffix = WRAPPER.replace("__C365_ENABLED__", str(not args.disabled)).encode()
    output = args.out.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(body.rstrip() + b"\n" + suffix.lstrip())
    compile(output.read_bytes(), str(output), "exec")
    print(f"{output} {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
