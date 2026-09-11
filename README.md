# Kaggriculture Strategy Meta & Agent Benchmark

Data-driven Kaggriculture competition research focused on interpretable strategy fingerprints, strategy-vs-strategy matchups, meta shifts, and measurable solo-agent improvement.

## Current status

**Gate: GO — NARROW V1 BUILD (2026-09-11).** A matched 24-quantile validation on 2026-09-09 and 2026-09-10 showed that the earlier apparent abrupt family shift was a small-sample artifact, while the 46-column one-table fingerprint schema passed core QA. The authorized product is a compact current-meta `strategy_meta.csv` centered on continuous/interpretable opening, economy, resource, and action fingerprints. The family label remains experimental and the counter matrix is not a core release claim.

## Rights posture

- Competition use: allowed under the current Kaggriculture rules, subject to the no-ingress/egress evaluation rule and external-data accessibility requirements.
- Direct Competition Data redistribution: do not publish or redistribute direct competition files to non-participants.
- Public-source path: Kaggle separately publishes daily Kaggriculture episode datasets under CC0-1.0. Public release work should prefer those separately licensed sources and publish compact derived features, not raw replay duplication.
- Any source with weaker or ambiguous rights remains internal until separately cleared.

See `docs/gate-2026-09-11.md` for the live gate evidence and stop-loss conditions.
See `docs/v1-schema.md` for the public schema candidate and `reports/targeted-validation-findings-2026-09-11.md` for the targeted validation.

## Current pilot result

The expanded pilot uses six fixed-quantile episodes per day from seven official Kaggle daily CC0 releases. It processed 42/42 episodes and 84 seats with no failures, all on engine 1.32.7. Replay rewards matched final observed cash for every seat.

The raw pilot is intentionally local and excluded from Git. The next authorized build is a bounded 24-quantile-per-day current-meta V1 for 2026-09-04 through 2026-09-10; historical backfill and publication remain separately gated.
