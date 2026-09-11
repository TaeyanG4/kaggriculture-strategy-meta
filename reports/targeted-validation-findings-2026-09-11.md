# Targeted validation findings — 2026-09-11

## Decision

**GO — NARROW V1 BUILD.** The narrowed one-table fingerprint product passed a targeted temporal check and release-schema QA. This authorizes a bounded current-meta V1 build from official CC0 daily sources. It does not authorize a full historical replay backfill, and it does not restore the strategy-family counter matrix as a core product claim.

## Targeted temporal validation

The earlier six-point pilot suggested a sharp drop in `cow+strawberry` on 2026-09-10. That hypothesis was retested with the same deterministic 24-quantile grid on both 2026-09-09 and 2026-09-10.

- 48/48 episodes parsed successfully.
- 96 player seats extracted.
- 1,567,299,164 replay bytes processed.
- All 48 episodes used engine 1.32.7.
- All sources were official daily Kaggle datasets reporting CC0-1.0.

### The apparent abrupt family shift did not reproduce

| Date | cow+strawberry | Seats | Share |
|---|---:|---:|---:|
| 2026-09-09 | 38 | 48 | 79.2% |
| 2026-09-10 | 37 | 48 | 77.1% |

The difference is -2.1 percentage points and Fisher's two-sided exact p-value is 1.0. The earlier 41.7% latest-day estimate is therefore treated as a small-sample artifact, not evidence of an abrupt meta regime change.

This result is limited to the official daily published slice; it is not a random estimate of the entire competition ladder.

### Continuous fingerprints still move

Mean resource-share changes from 2026-09-09 to 2026-09-10 include goose +3.53pp, strawberry crop -3.05pp, sheep -2.14pp, tomato crop +1.70pp, and cow -1.38pp. These are descriptive sample shifts, not causal or population claims. They support retaining continuous resource fingerprints even when the coarse family label is stable.

### Opening diversity remains high

- 2026-09-09: 24 distinct t24 hashes and 24 distinct t48 hashes across 48 seats.
- 2026-09-10: 23 distinct t24 hashes and 26 distinct t48 hashes across 48 seats.

Exact opening identity remains substantially richer than the current categorical family label.

## Matchup gate remains closed

The targeted validation produced 10 family-pair combinations, but zero cross-family pairs reached both five games and both seat orientations. Seat 0 won 29.2% of the 24 games sampled on 2026-09-09 and 50.0% on 2026-09-10.

Therefore `matchups.csv` stays outside core V1 and no counter claim should appear in the Dataset title, subtitle, or primary card positioning.

## V1 schema result

The candidate `strategy_meta.csv` schema contains 46 columns. It is one row per `(episode_id, seat)` and excludes `team_id`, `submission_id`, `agent_name`, and `rating_after`.

The targeted 96-row candidate passed machine-readable QA:

- duplicate `(episode_id, seat)` keys: 0
- core required missing values: 0
- source license: CC0-1.0 for 96/96 rows
- invalid resource-share values: 0
- maximum crop-share sum error: 0.0001
- maximum animal-share sum error: 0.0001
- excluded identity fields present: 0
- Unicode replacement-character cells: 0
- candidate CSV size: 34,567 bytes

The schema includes `source_score_quantile` so users can see the deterministic sampling position within each official daily manifest score ordering.

## Closest-alternative comparison

The closest broad alternative, `georgymamarin/kaggriculture-episodes`, already provides a 32-column `episode_features.csv` with final money, crew/hires, first-land day, crop counts, and market-price ranges. It also publishes action-stream hashes separately.

Against that `episode_features.csv`, the 46-column V1 candidate has three exact-name overlaps (`episode_id`, `seat`, `engine_version`) and three explicitly mapped semantic overlaps (`final_reward`, `total_hires_actual`, `first_land_turn`). The candidate has 31 timing/economy/resource/action/fingerprint columns in its main fingerprint group.

Hashes are not claimed as novel. The candidate differentiator is the compact single-row combination of official-source provenance, sampling position, cash trajectory checkpoints, turn-level first-event timing, observed tile-turn resource shares, semantic behavior totals, and opening fingerprints.

## Re-score of the narrowed product

| Dimension | Score | Weighted |
|---|---:|---:|
| Proven demand / adoption evidence | 5/5 | 15 |
| Distinctiveness / moat | 2/5 | 6 |
| Clear task / first insight | 5/5 | 10 |
| Global or broad audience reach | 2/5 | 4 |
| Time-to-first-insight | 5/5 | 10 |
| Source authority + rights clarity | 5/5 | 10 |
| Freshness / update value | 5/5 | 5 |
| Collection + rebuild efficiency | 4/5 | 4 |
| Download/runtime friction | 5/5 | 5 |
| Portfolio diversification | 5/5 | 5 |
| Notebook/visual hook strength | 5/5 | 10 |
| **Total** |  | **84/100** |

The score applies to the narrow fingerprint product, not the rejected family-counter positioning. The hard veto is removed because V1 no longer depends on stable categorical strategy identities or a well-supported counter matrix.

## Authorized next step

Build a bounded current-meta V1 for 2026-09-04 through 2026-09-10 using the same deterministic 24-quantile-per-day selection rule. Keep raw replay JSON and row-level development tables local. Produce one local release candidate plus aggregate QA and provenance. Do not publish a Kaggle Dataset or make the GitHub repository public yet.
