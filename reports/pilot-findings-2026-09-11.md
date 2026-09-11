# Pilot findings — 2026-09-11

## Gate after first measured pilot

**PILOT remains in force. Do not backfill the full corpus yet.**

The first pilot proved that recent replays can be transformed into compact, reproducible seat-level features, but it did not yet establish enough matchup sample support or strategy-family stability for a full collection/public release.

## Measured pilot

- Selected episodes: 13
- Player seats: 26
- Parse success: 13/13 episodes; 0 failures
- Source bytes processed: 404,705,767
- Derived feature CSV: 18,031 bytes
- Engine versions observed: 1.32.7 only
- Rating span represented: about 1,286 to 2,759, plus one official CC0 sentinel replay
- Initial uncached end-to-end pilot run: 62.119 seconds
- Cached extraction rerun: 3.539 seconds

Raw replay payloads stay local and are excluded from Git.

## What changed after looking at real data

The first action-threshold classifier was rejected: it collapsed 23/26 seats into `labor_crop` and only 3/26 into `animal_first`. That was not a defensible strategy taxonomy.

The revised pilot family uses **actual board-state tile-turn occupancy**, not merely submitted orders. Wheat is nearly universal in this small sample, so the coarse family combines:

1. dominant livestock species by observed animal tile-turn share; and
2. dominant non-wheat crop by observed crop tile-turn share.

This produces three current pilot families:

- `cow+strawberry`: 18 seats
- `sheep+strawberry`: 7 seats
- `sheep+melon`: 1 seat

This is still only a coarse resource-mix label. Exact opening identity remains separately represented by deterministic action-stream hashes at turns 24 and 48; final public strategy labels must not simply rename arbitrary hashes as strategies.

## Evidence of a real meta signal

The small sample already shows strong convergence. Many mid/high-rating seats occupy a very similar resource template, roughly centered on carrot/strawberry/wheat with a cow/sheep mix, while a few strong seats use sheep-heavy, tomato-diversified, or strawberry-heavy allocations.

The current matchup table is deliberately caveated:

| Family A | Family B | Games | A wins | B wins | Mean A margin | Interpretation |
|---|---|---:|---:|---:|---:|---|
| cow+strawberry | cow+strawberry | 7 | 5 | 2 | +9,022.14 | small sample; same-family result is not a counter claim |
| cow+strawberry | sheep+strawberry | 4 | 0 | 4 | -5,437.25 | pilot-only directional signal; not publishable evidence |
| sheep+melon | sheep+strawberry | 1 | 0 | 0 | n/a | insufficient |
| sheep+strawberry | sheep+strawberry | 1 | 1 | 0 | +29,228 | insufficient |

No causal or counter-strategy claim should be made from these counts.

## Market scorecard after live validation

The project scores **79/100 — PILOT FIRST** under the Kaggle Dataset Ops scorecard.

| Dimension | Score | Weighted points | Reason |
|---|---:|---:|---|
| Proven demand / adoption | 5/5 | 15 | Multiple Kaggriculture datasets and notebooks have substantial downloads/votes |
| Distinctiveness / moat | 2/5 | 6 | Existing replay, fingerprint, benchmark, and ladder-meta products overlap heavily |
| Clear task / first insight | 5/5 | 10 | Counter/matchup question is immediately understandable |
| Broad audience reach | 2/5 | 4 | Active-competition audience is valuable but narrow |
| Time-to-first-insight | 5/5 | 10 | Intended V1 is one compact table |
| Source authority + rights clarity | 3/5 | 6 | Official CC0 daily episode path exists, but direct Competition Data redistribution is prohibited |
| Freshness / update value | 5/5 | 5 | Live competition meta changes quickly |
| Collection + rebuild efficiency | 3/5 | 3 | Replays are large; derived output is tiny and caching works |
| Download/runtime friction | 5/5 | 5 | Proposed public derivative is compact |
| Portfolio diversification | 5/5 | 5 | Adds a competition-painkiller/game-strategy product |
| Notebook/visual hook | 5/5 | 10 | Strategy matchup matrix and meta shifts have a strong visual story |

A numeric score does not override the stop-loss: strategy labels and matchup evidence still need a larger representative pilot.

## Rights interpretation to preserve

- **Competition use:** allowed under current rules, including research/development, subject to external-data accessibility and no-ingress/egress during evaluation.
- **Direct Competition Data redistribution:** not allowed to non-participants under the current Data Security rule.
- **Public derivative source:** prefer Kaggle's separately published official daily episode datasets carrying CC0-1.0 metadata. Regenerate any eventual public rows from that reviewed source path rather than treating the public episode CDN alone as redistribution permission.
- Do not publish raw replay dumps in this project.

## Next measured action

Expand only the pilot, using a recent **official CC0 daily-dataset sample** with enough games to test:

- family prevalence and stability by rating tier;
- semantic opening features vs exact hash identity;
- minimum matchup sample thresholds;
- same-family vs cross-family outcome uncertainty;
- whether the strategy representation adds information beyond existing `episode_features.csv` and stream hashes.

If the family taxonomy remains dominated by one coarse bucket or matchup cells remain too thin, narrow the Dataset side and continue the competition-agent side independently.