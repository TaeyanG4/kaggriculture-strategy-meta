# Bounded current-meta V1 findings — 2026-09-11

## Decision

**LOCAL RELEASE CANDIDATE READY; PUBLICATION STILL GATED.**

The bounded current-meta build for 2026-09-04 through 2026-09-10 completed successfully from official Kaggle daily episode datasets reporting CC0-1.0. The local candidate is small, deterministic, provenance-tracked, and passes core QA. It is ready for release-package and notebook preparation, but it has not been published to Kaggle and the GitHub repository remains private.

## Build readback

- Source days: 2026-09-04 through 2026-09-10
- Sampling rule: 24 equally spaced manifest-score quantile midpoints per day
- Selected / parsed episodes: 168 / 168
- Player-seat rows: 336
- Replay bytes processed: 5,456,959,047
- Parse failures: 0
- Engine version: 1.32.7 for all 168 episodes
- Replay reward equals final observed cash: 336 / 336 seats
- Builder Git SHA: `4448bda51b5bc623f454c2fc585a1dc086e1e3bb`
- Local `strategy_meta.csv`: 336 rows x 48 columns
- Candidate bytes: 122,674
- Candidate SHA-256: `7c4249d0fabbf186e059304ebf8a901471bf80ecf193b7b21125dab556f21744`

The source slice is not a random sample of the full competition ladder. Every day is sampled deterministically from the official daily manifest ordered by `avg_score`, and `source_score_quantile` is included in the release candidate so the sampling position is visible to users.

## QA result

Core release QA passes:

- duplicate `(episode_id, seat)` keys: 0
- core required missing values: 0
- license values: CC0-1.0 for 336 / 336 rows
- engine version values: 1.32.7 for 336 / 336 rows
- invalid resource-share values: 0
- maximum crop-share sum absolute error: 0.0002
- maximum animal-share sum absolute error: 0.0001
- excluded identity fields present: 0
- Unicode replacement-character cells: 0
- outcome rows: 168 win / 168 loss / 0 tie
- outcome/margin sign consistency: 336 / 336

`team_id`, `submission_id`, `agent_name`, and `rating_after` are deliberately excluded from the public schema.

## Duplicate-field cleanup

An intermediate V1 included `peak_cash`. QA showed `peak_cash == final_reward` for 336 / 336 rows with correlation 1.0. It was removed because it added no information and would make the public table look wider without increasing utility.

The direct outcome fields retained are:

- `final_reward`
- `opponent_final_reward`
- `reward_margin_vs_opponent`
- `outcome`

This lets a user perform winner/loser analysis immediately without self-joining the two seat rows.

## Current-meta descriptive signal

The coarse experimental family remains dominated by `cow+strawberry` (232 / 336 seats, 69.0%), so it is still unsuitable as the main product taxonomy. Continuous fingerprints are more informative.

Across the seven daily samples:

| Date | cow+strawberry share | distinct t24 openings | distinct t48 openings | mean cash t168 | strawberry share | goose share | sheep share |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-09-04 | 62.5% | 19 | 22 | 545.0 | 44.0% | 6.2% | 41.9% |
| 2026-09-05 | 66.7% | 15 | 18 | 691.3 | 44.0% | 4.6% | 44.0% |
| 2026-09-06 | 60.4% | 21 | 25 | 574.3 | 38.9% | 6.7% | 42.5% |
| 2026-09-07 | 70.8% | 26 | 37 | 589.9 | 40.8% | 9.3% | 38.6% |
| 2026-09-08 | 66.7% | 28 | 30 | 777.3 | 39.6% | 9.0% | 39.8% |
| 2026-09-09 | 79.2% | 24 | 24 | 1,044.2 | 41.9% | 12.2% | 37.7% |
| 2026-09-10 | 77.1% | 23 | 26 | 976.6 | 38.9% | 15.7% | 35.6% |

The strongest simple visual hook is therefore temporal: opening diversity and continuous crop/animal allocation change across recent official daily slices even when the coarse family label remains concentrated.

## Winner-vs-loser exploratory check

The release candidate was tested using within-episode winner-minus-loser differences for 29 non-outcome features. Exact paired sign tests were corrected with Benjamini-Hochberg, and a feature was only flagged if it also had paired standardized effect magnitude at least 0.2 and the mean direction agreed when the winner occupied seat 0 and seat 1.

**No feature passed all robustness conditions.**

The closest early signal was `first_land_turn`: winners unlocked land about 5.06 turns earlier on average, with paired standardized effect -0.202 and seat-consistent direction, but BH-adjusted q was approximately 0.254. That is exploratory only and is not evidence for a winning rule.

This result changes the intended first notebook positioning: lead with **current meta over time**, not “features that predict winning.”

## Product boundary after Phase 6

Core V1 remains one file: `strategy_meta.csv`.

Do not add a public `matchups.csv` yet. Do not advertise counter strategies, stable categorical strategy identities, or a validated early-game winning formula. The useful five-minute task is to load one table and compare:

1. how opening fingerprints vary by source day and score quantile,
2. how crop and animal tile-turn allocation shifts over time,
3. how cash trajectories differ across daily samples,
4. winner/loser differences as clearly labeled exploratory analysis.

## Next action

Prepare, but do not publish, the Kaggle release package and the first current-meta quicklook notebook. Append the 2026-09-11 official daily slice through the same deterministic rule when that source becomes public, then repeat core QA and decide whether publication is ready.
