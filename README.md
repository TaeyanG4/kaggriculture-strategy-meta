# Kaggriculture Strategy Meta & Agent Benchmark

Data-driven Kaggriculture competition research focused on interpretable strategy fingerprints, strategy-vs-strategy matchups, meta shifts, and measurable solo-agent improvement.

## Current status

**Latest submission, 2026-09-13:** `agent/c111_opening_rescue.py`, ref56190992,
passed Kaggle server validation and an exact server download check. The dated live
snapshot has53W/3L in56 public games,score2350.6; c110 remains highest-rated
observed baseline at2809.7. See [c111 evidence and limitations](reports/c111-opening-rescue-2026-09-13.ko.md).
Its local41W/7L is training evidence; fresh selection/holdout remain unrun.

**Competition development, 2026-09-12:** the simulation league has been rebuilt
with fresh match processes, official source loading, source/engine fingerprints,
separate train/selection/holdout seeds, and controlled replay diagnostics.
`agent/c110_reserve8.py` is the selected V37 derivative; the old v27 and c101
sources remain intact. Read [the implementation evidence](reports/league-rebuild-2026-09-12.ko.md)
and [the simulation guide](docs/simulation-league.md). Local wins do not establish
first place or a particular Kaggle rating.

The dataset checkpoint below describes the separate dataset workstream.

**Gate: GO — NARROW V1, LOCAL CANDIDATE READY (2026-09-11).** The bounded current-meta build now covers 168 official-CC0 episodes / 336 seats from 2026-09-04 through 2026-09-10. The 48-column one-table `strategy_meta.csv` candidate passes core QA and is 122,674 bytes. The product centers on continuous/interpretable opening, economy, resource, and action fingerprints. The family label remains experimental, the counter matrix is not a core release claim, and public publication is still gated.

## Rights posture

- Competition use: allowed under the current Kaggriculture rules, subject to the no-ingress/egress evaluation rule and external-data accessibility requirements.
- Direct Competition Data redistribution: do not publish or redistribute direct competition files to non-participants.
- Public-source path: Kaggle separately publishes daily Kaggriculture episode datasets under CC0-1.0. Public release work should prefer those separately licensed sources and publish compact derived features, not raw replay duplication.
- Any source with weaker or ambiguous rights remains internal until separately cleared.

See `docs/gate-2026-09-11.md` for the live gate evidence and stop-loss conditions.
See `docs/v1-schema.md` for the public schema candidate and `reports/targeted-validation-findings-2026-09-11.md` for the targeted validation.
See `reports/current-v1-findings-2026-09-11.md` for the bounded V1 QA and first-insight readback.
See `docs/data-dictionary.md` for the 48-column dictionary and `notebooks/01_current_meta_quicklook.py` for the private release-notebook draft.

## Current V1 result

The current V1 uses 24 deterministic manifest-score quantile midpoints per day across seven official Kaggle daily CC0 releases. It processed 168/168 episodes and 336 seats with no failures, all on engine 1.32.7. Replay rewards matched final observed cash for every seat, and the local release candidate passes duplicate-key, required-value, resource-share, encoding, source-license, and identity-exclusion checks.

The raw replays and row-level release candidate remain local and excluded from Git. A paired winner/loser check found no robust early-game predictor after multiple-test correction and seat-direction checks, so the first showcase will emphasize temporal current-meta fingerprints rather than winning-formula claims. Historical backfill and publication remain separately gated.
