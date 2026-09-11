# Kaggriculture Strategy Meta & Agent Benchmark

Data-driven Kaggriculture competition research focused on interpretable strategy fingerprints, strategy-vs-strategy matchups, meta shifts, and measurable solo-agent improvement.

## Current status

**Gate: NARROW (2026-09-11).** A 42-episode / 84-seat official-CC0 expanded pilot parsed cleanly, but the current categorical resource family is dominated by `cow+strawberry` and only one real cross-family matchup reached five games. Public V1 should therefore lead with interpretable continuous strategy/opening fingerprints; family and matchup fields remain experimental until better supported.

## Rights posture

- Competition use: allowed under the current Kaggriculture rules, subject to the no-ingress/egress evaluation rule and external-data accessibility requirements.
- Direct Competition Data redistribution: do not publish or redistribute direct competition files to non-participants.
- Public-source path: Kaggle separately publishes daily Kaggriculture episode datasets under CC0-1.0. Public release work should prefer those separately licensed sources and publish compact derived features, not raw replay duplication.
- Any source with weaker or ambiguous rights remains internal until separately cleared.

See `docs/gate-2026-09-11.md` for the live gate evidence and stop-loss conditions.

## Current pilot result

The expanded pilot uses six fixed-quantile episodes per day from seven official Kaggle daily CC0 releases. It processed 42/42 episodes and 84 seats with no failures, all on engine 1.32.7. Replay rewards matched final observed cash for every seat.

The raw pilot is intentionally local and excluded from Git. See `reports/expanded-pilot-findings-2026-09-11.md` for the measured gate update.
