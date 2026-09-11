# Kaggriculture Strategy Meta & Agent Benchmark

Data-driven Kaggriculture competition research focused on interpretable strategy fingerprints, strategy-vs-strategy matchups, meta shifts, and measurable solo-agent improvement.

## Current status

**Gate: GO — NARROW V1, LOCAL CANDIDATE READY (2026-09-11).** The bounded current-meta build now covers 168 official-CC0 episodes / 336 seats from 2026-09-04 through 2026-09-10. The 48-column one-table `strategy_meta.csv` candidate passes core QA and is 122,674 bytes. The product centers on continuous/interpretable opening, economy, resource, and action fingerprints. The family label remains experimental, the counter matrix is not a core release claim, and public publication is still gated.

## Rights posture

- Competition use: allowed under the current Kaggriculture rules, subject to the no-ingress/egress evaluation rule and external-data accessibility requirements.
- Direct Competition Data redistribution: do not publish or redistribute direct competition files to non-participants.
- Public-source path: Kaggle separately publishes daily Kaggriculture episode datasets under CC0-1.0. Public release work should prefer those separately licensed sources and publish compact derived features, not raw replay duplication.
- Any source with weaker or ambiguous rights remains internal until separately cleared.

See `docs/gate-2026-09-11.md` for the live gate evidence and stop-loss conditions.
See `docs/v1-schema.md` for the public schema candidate and `reports/targeted-validation-findings-2026-09-11.md` for the targeted validation.
See `reports/current-v1-findings-2026-09-11.md` for the bounded V1 QA and first-insight readback.

## Current V1 result

The current V1 uses 24 deterministic manifest-score quantile midpoints per day across seven official Kaggle daily CC0 releases. It processed 168/168 episodes and 336 seats with no failures, all on engine 1.32.7. Replay rewards matched final observed cash for every seat, and the local release candidate passes duplicate-key, required-value, resource-share, encoding, source-license, and identity-exclusion checks.

The raw replays and row-level release candidate remain local and excluded from Git. A paired winner/loser check found no robust early-game predictor after multiple-test correction and seat-direction checks, so the first showcase will emphasize temporal current-meta fingerprints rather than winning-formula claims. Historical backfill and publication remain separately gated.
