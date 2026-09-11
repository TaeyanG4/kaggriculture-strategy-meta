# Expanded pilot findings — 2026-09-11

## Decision

**NARROW.** The project remains viable, but the public V1 should no longer lead with a categorical strategy-family counter matrix. The strongest measured product shape is a compact, source-scoped table of interpretable opening, economy, resource-allocation, and outcome fingerprints. `strategy_family_pilot` remains experimental, and matchup claims require stronger seat-aware support.

## Scope and provenance

- Source datasets: official `kaggle/kaggriculture-episodes-YYYY-MM-DD` releases for 2026-09-04 through 2026-09-10.
- License observed through Kaggle CLI for each source download: CC0-1.0.
- Sampling: six episodes per day at fixed 10/20, 45/55, and 80/90 percentiles of each official manifest's `avg_score` ordering.
- Important limitation: these bands are relative to Kaggle's published daily elite slice, not the full competition ladder.
- Raw replay JSON stays local and ignored. Only compact aggregate reports are tracked.

## Measured QA

- 42/42 selected episodes parsed successfully.
- 84 player seats extracted; 0 parsing failures.
- 1,361,712,110 source bytes processed.
- All 42 episodes used engine 1.32.7 and contained 720 turns.
- Replay `rewards` matched the last observed farm cash exactly for 84/84 seats.
- Cached rebuild runtime: 10.469 seconds.
- Derived row-level feature file size: 62,185 bytes.

## Strategy-family result

Current deterministic resource-mix family counts:

| Family | Seats | Share |
|---|---:|---:|
| cow+strawberry | 60 | 71.4% |
| sheep+strawberry | 15 | 17.9% |
| sheep+carrot | 4 | 4.8% |
| goose+strawberry | 2 | 2.4% |
| cow+tomato | 1 | 1.2% |
| cow+carrot | 1 | 1.2% |
| sheep+tomato | 1 | 1.2% |

The family label remains too coarse to carry the product by itself. `cow+strawberry` is 67.9% of both the daily-low and daily-high bands and 78.6% of the daily-mid band, so the current family definition does not separate the official score bands in a useful monotonic way.

Name-level repeat stability is only a proxy because one displayed agent name can span submission changes or adaptive behavior. Among 20 names repeated in the sample, 12 (60%) stayed in one family, while the mean majority-family share was 83.4%. This is not strong enough to present the current categorical family as a stable agent identity.

## Opening fingerprints are richer

- 50 distinct 24-turn opening hashes across 84 seats.
- 54 distinct 48-turn opening hashes across 84 seats.
- Largest 24-turn opening share: 9.5%.
- Largest 48-turn opening share: 8.3%.

This supports preserving exact opening identity separately from interpretable resource features. The product moat is more credible as a feature/fingerprint table than as a small set of family labels.

## Matchup result and seat confounding

- 9 family-pair combinations observed.
- Only 2 pairs reached five games, and one of those is the same-family `cow+strawberry` control.
- The only cross-family pair with at least five games is `cow+strawberry` vs `sheep+strawberry`: 6 games, 2 cow wins vs 4 sheep wins, mean cow-minus-sheep margin -10,366.5.
- Cow win rate in that pair is 33.3%, but the 95% Wilson interval is very wide: 9.7% to 70.0%.
- The six games are balanced across seat orientation: cow appears in seat 0 three times and seat 1 three times.

Across all 42 decided games, seat 0 won 64.3%. In 27 same-family games, seat 0 won 74.1%. That makes seat/orientation a mandatory confounder for any future matchup table. Same-family win rates are controls, not counter evidence.

## Possible temporal shift

The dominant `cow+strawberry` share was 55/72 seats (76.4%) across 2026-09-04 through 2026-09-09, then 5/12 (41.7%) on 2026-09-10. Because the sampling is fixed-quantile rather than a random ladder sample, this is a directional meta-shift hypothesis, not a population estimate. It is worth a targeted latest-day validation before collecting more history.

## Re-score

| Dimension | Score | Weighted |
|---|---:|---:|
| Proven demand / adoption evidence | 5/5 | 15 |
| Distinctiveness / moat | 2/5 | 6 |
| Clear task / first insight | 4/5 | 8 |
| Global or broad audience reach | 2/5 | 4 |
| Time-to-first-insight | 5/5 | 10 |
| Source authority + rights clarity | 5/5 | 10 |
| Freshness / update value | 5/5 | 5 |
| Collection + rebuild efficiency | 4/5 | 4 |
| Download/runtime friction | 5/5 | 5 |
| Portfolio diversification | 5/5 | 5 |
| Notebook/visual hook strength | 4/5 | 8 |
| **Total** |  | **80/100** |

The numeric score reaches the strong-candidate range because the official CC0 source path and tiny derived output are excellent. The hard gate still overrides the score: the advertised categorical strategy-family matchup moat is not validated strongly enough for a full backfill.

## Revised public V1 hypothesis

Primary file: `strategy_meta.csv`.

Core fields should emphasize source/date/engine, seat and outcome, opening timing, cash checkpoints, actual tile-turn resource shares, semantic action counts, and exact opening hashes. `strategy_family_pilot` should be clearly marked experimental rather than treated as ground truth.

`matchups.csv` should stay out of the core V1 unless future bounded sampling produces several cross-family pairs with meaningful counts in both seat orientations. A notebook can still demonstrate exploratory matchup analysis with confidence intervals and explicit sample sizes.

## Next gate

1. Validate the apparent 2026-09-10 diversification with another bounded official-CC0 sample rather than historical backfill.
2. Harden a release-schema candidate around continuous/interpretable fingerprints and compare it directly with the closest existing episode-feature alternative.
3. Keep matchup analysis seat-aware and require both seat orientations before calling a pair a counter signal.
4. Either obtain substantially more cross-family support or remove counter-matrix positioning from the public Dataset card.
