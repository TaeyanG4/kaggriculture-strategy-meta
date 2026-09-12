# Handoff

## Repository
- Workspace: current project root
- Intended branch: `main`
- GitHub target: `TaeyanG4/kaggriculture-strategy-meta`
- Visibility during active competition: private until public-code and source-rights gates are satisfied
- Tests: `python -m unittest discover -s tests -v` passes (17 tests)
- Durable project/session context: `AGENTS.md`
- Future sessions should read `AGENTS.md` first and apply the user-supplied `kaggle-dataset-ops` skill for relevant work.

## Current phase
- Phase 0 current state: complete for start gate
- Phase 1 market/duplication validation: complete for start gate
- Phase 2 product hypothesis: preserved
- Phase 3 rights gate: source-scoped decision recorded
- Phase 4 small pilot: first measured pilot complete
- Phase 4 expanded official-CC0 pilot: complete
- Phase 5 bounded current-meta V1 build: complete locally
- Phase 6 first-insight / product-hook validation: complete for V1 checkpoint
- Release package / quicklook preparation: complete locally; nothing published
- Overall decision: `GO — NARROW V1 BUILD`; bounded current-meta collection is authorized, full historical backfill is not

## Pilot checkpoint
- 13/13 episodes parsed; 26 seats; 0 failures
- 404,705,767 source bytes processed
- Engine 1.32.7 across this pilot
- Coarse resource-mix family counts: 18 cow+strawberry, 7 sheep+strawberry, 1 sheep+melon
- Row-level reports and replay payloads remain local/ignored
- Aggregate checkpoint: `reports/pilot_summary.json`
- Interpretation: `reports/pilot-findings-2026-09-11.md`

## Expanded pilot checkpoint
- Official Kaggle daily CC0 sources: 2026-09-04 through 2026-09-10
- Fixed manifest quantile sample: 42 episodes / 84 seats
- 42/42 parsed; 0 failures; 1,361,712,110 replay bytes processed
- Engine 1.32.7 across all 42 episodes
- Replay rewards equal final observed cash for 84/84 seats
- Families: 60 cow+strawberry, 15 sheep+strawberry, 4 sheep+carrot, 5 other
- 50 distinct t24 opening hashes; 54 distinct t48 opening hashes
- 9 family matchup pairs; only one real cross-family pair has >=5 games
- cow+strawberry vs sheep+strawberry: 6 games, cow 2 wins / sheep 4, cow Wilson95 0.097-0.700; both seat orientations represented 3/3
- Overall seat0 win rate 0.643; same-family seat0 win rate 0.741, so future matchup claims must be seat-aware
- Name-level repeat family proxy: 20 repeated agents, 60% perfectly stable, mean majority-family share 83.4%; do not treat names as exact submission identities
- Aggregate checkpoint: `reports/expanded_pilot_summary.json`
- Interpretation: `reports/expanded-pilot-findings-2026-09-11.md`
- Row-level expanded reports and raw replay payloads remain local/ignored

## Targeted validation checkpoint
- Matched deterministic 24-quantile samples on 2026-09-09 and 2026-09-10
- 48/48 episodes parsed; 96 seats; 0 failures; 1,567,299,164 replay bytes
- Engine 1.32.7 for all 48 episodes
- `cow+strawberry`: 38/48 seats (79.2%) on 09-09 vs 37/48 (77.1%) on 09-10; Fisher two-sided p=1.0
- The earlier apparent 09-10 family collapse did not reproduce and is treated as a small-sample artifact
- Continuous resource shifts remain descriptive; notable sample shifts include goose +3.53pp and strawberry -3.05pp
- 0 cross-family matchup pairs reached >=5 games with both seat orientations; counter matrix remains gated out of core V1
- Aggregate checkpoint: `reports/targeted_validation_summary.json`
- Interpretation: `reports/targeted-validation-findings-2026-09-11.md`

## V1 schema checkpoint
- One file: `strategy_meta.csv`
- Grain: one row per `(episode_id, seat)`
- Final current schema: 48 columns including provenance, source score quantile, direct within-episode outcome fields, cash checkpoints, first-event timings, opening/labor features, tile-turn resource shares, broad action totals, opening hashes, and an explicitly experimental family label
- Targeted 96-row candidate QA passes: 0 duplicate keys, 0 core missing values, 0 invalid shares, 0 excluded identity fields, 0 Unicode replacement cells
- Candidate CSV size on targeted validation: 34,567 bytes
- Schema: `docs/v1-schema.md`
- Machine-readable QA: `reports/v1_schema_qa.json`
- Alternative comparison: `reports/v1_schema_comparison.json`

## Bounded current-meta V1 checkpoint
- Official daily source window: 2026-09-04 through 2026-09-10
- Selection: 24 deterministic manifest-score quantile midpoints/day = 168 episodes / 336 seats
- Parse result: 168/168 episodes; 0 failures; 5,456,959,047 replay bytes processed
- Engine 1.32.7 for all selected episodes
- Replay rewards equal final observed cash for 336/336 seats
- Local release candidate: 336 rows x 48 columns, 122,674 bytes
- Builder Git SHA: `4448bda51b5bc623f454c2fc585a1dc086e1e3bb`
- Release SHA-256: `7c4249d0fabbf186e059304ebf8a901471bf80ecf193b7b21125dab556f21744`
- QA: 0 duplicate episode/seat keys; 0 core missing; CC0-1.0 for all 336 rows; 0 invalid shares; 0 excluded identity fields; 0 Unicode replacement cells
- Outcomes: 168 win / 168 loss; outcome/margin sign consistent for 336/336 rows
- Experimental families: 232 cow+strawberry, 88 sheep+strawberry, 16 other; still too concentrated for primary taxonomy
- Opening diversity: 115 distinct t24 hashes; 144 distinct t48 hashes
- `peak_cash` was removed from public V1 after proving exactly equal to `final_reward` for 336/336 rows
- Aggregate QA: `reports/current_v1_qa.json`
- Provenance: `reports/current_v1_provenance.json`
- Daily readback: `reports/current_v1_daily_summary.csv`
- Interpretation: `reports/current-v1-findings-2026-09-11.md`

## First-insight checkpoint
- Paired winner/loser comparison across 168 games and 29 non-outcome features
- Exact paired sign tests + Benjamini-Hochberg correction + seat-direction consistency + |paired standardized effect|>=0.2
- Robust exploratory signals: 0
- Closest early signal: `first_land_turn`, winner-minus-loser mean -5.06 turns, effect -0.202, BH q~0.254, seat-consistent; exploratory only
- Do not position V1 as a validated winner predictor or counter dataset
- First showcase should emphasize temporal opening/resource/economy meta shifts
- Insight summary: `reports/current_v1_insight_summary.json`

## Release preparation checkpoint
- Proposed Dataset: `taeyangg4/kaggriculture-current-meta-fingerprints`
- Proposed title: `Kaggriculture Current Meta Fingerprints`
- Proposed subtitle: `Openings, economy and resource allocation from official daily episodes`
- Local package contains one data file: `strategy_meta.csv`
- Package CSV SHA matches the validated release candidate SHA exactly
- Proposed Dataset slug was not found in live Kaggle CLI search at this checkpoint
- Data dictionary: `docs/data-dictionary.md`
- Private quicklook source: `notebooks/01_current_meta_quicklook.py`
- Proposed private Kernel: `taeyangg4/kaggriculture-current-meta-quicklook`
- Proposed Kernel slug was not found in live Kaggle CLI search at this checkpoint
- Quicklook smoke test passes locally against the 336-row / 48-column candidate
- Kernel metadata prepared locally with Python script type, private=true, internet=false, GPU/TPU=false, and the proposed Dataset source
- No `kaggle datasets create`, Dataset version, or Kernel push has been executed for this project
- Preparation report: `reports/release-prep-2026-09-11.md`

## Competition core benchmark checkpoint
- Local engine: `kaggle-environments==1.32.7`; deterministic 720-step, seed-paired, seat-balanced harness is implemented in `src/kaggriculture_meta/benchmark.py`
- Harness checks completed: starter vs random and starter self-play symmetry
- `baseline_v0`: compact mixed-crop starting-quadrant economy; beat built-in starter 40/40 in the initial baseline run
- `baseline_v0` vs authored tier-2 Rotation Rosa: 20/20 wins, mean margin +3,571
- `baseline_v1`: one extra quadrant with larger labor/seed scale; beat authored tier-3 Homestead Hana 20/20
- `baseline_v1` vs authored tier-4 Melon Mateo: 8/10 on the first five paired seeds, then 20/20 on the next ten paired seeds
- `baseline_v1` vs authored tier-5 Rancher Rita: 0/10, mean margin -20,815.4
- `baseline_v2`: goose/feed-chain experiment; vs Rancher Rita 2/10, mean margin -12,747.4
- `baseline_v2` regression check vs Melon Mateo on ten fresh paired seeds: 16/20, mean margin +2,594.2, seat0/seat1 decided win rates both 0.8
- `baseline_v3`: exact byte-preserving MIT Rancher Rita tier-5 backbone, retained with upstream SPDX attribution; SHA-256 matches the local reference source. A two-seed paired mirror check produced 1 win / 1 loss / 2 ties and mean margin 0, as expected for an identical policy.
- `baseline_v7`: independent animal-first capital sequencing agent derived from the project's own v4 cow economy and the official CC0 high-reward fingerprint evidence. Against Rancher Rita it won 12/12 in the pilot and 32/40 on a fresh 20-seed, seat-balanced confirmation set; mean margin +4,566.1 and seat0/seat1 win rates both 0.80.
- Same-seed comparison on the 40-game confirmation set: `baseline_v4` won 26/40 with mean margin +1,183.6, confirming that v7's opening-capital sequencing materially improved the independent cow baseline on that sample.
- `baseline_v5` and `baseline_v6` scale-up experiments failed their small gates and are archived only as ignored local experiment state; do not promote them without new evidence.
- Tier-4 regression check for v4 was strong (18/20 vs Melon Mateo, mean margin +24,251.1). A fresh v7 tier-4 regression check is still required before submission selection.
- Benchmark-only tiers 6-9 remain a much larger gap: v4 went 0/8 against each tested meta-line opponent, with mean margins roughly -99.6k to -114.8k. Do not copy their ambiguous field trace; use them only as opponents.
- Interpretation: `baseline_v7` is the current independent competition-development champion. The next bottleneck is validating v7 against tier 4 and then closing the tier-6+ production/market-scale gap using rights-clear mechanics and official CC0 evidence.
- Reference-agent code tiers 0-5 are covered by the local MIT notice. Tiers 6-9 contain an explicitly unlicensed/competition-derived shared field-plan component and should be used as benchmark opponents, not copied into the submission code without a separate rights decision.

## Parallel worktree consolidation checkpoint
- `mechanics-research`, `meta-refresh/daily-2026-09-11`, and `agent-search/optimizer-2026-09-11` have been consolidated back into `main`.
- The meta-refresh branch contributed `src/kaggriculture_meta/meta_refresh.py`.
- The agent-search branch contributed `src/kaggriculture_meta/optimizer.py`, `tests/test_optimizer.py`, and `agent/rancher_rita_land14.py`.
- The mechanics branch was already an ancestor of `main`, so no additional merge content was needed.
- Former sibling worktree directories were removed with Git worktree commands after confirming they were clean.
- Cross-agent handoffs now live in ignored local state at `state/parallel-handoffs/`; check this directory before duplicating research or experiments.

## Kaggle
- Competition: `kaggriculture`
- Deadline observed: 2026-09-30 23:59
- Team count observed: 8,602
- Joined: yes
- Kaggle CLI: 2.2.4
- Local `kaggle-environments`: 1.32.7 installed in the project `.venv`
- No Kaggle Dataset has been created for this project
- No competition submission has been made by this project yet

## Rights / release invariants
- Direct Competition Data is not for redistribution to non-participants.
- Official Kaggle daily episode datasets with CC0-1.0 metadata are the preferred public source path.
- Raw replays never belong in the public release or Git history.
- Eventual V1 should remain compact and source-scoped.
- No credentials, tokens, authorization headers, cookies, or local secret paths may enter Git.

## Authentication constraints
- Kaggle CLI is already usable for current read/download operations.
- `KAGGLE_MCP_TOKEN_FILE` was not set when checked.
- Kaggle MCP has not been needed or initialized.
- If MCP later becomes necessary and a user-authorized token file is available, use raw-token-file -> child environment -> `Authorization: Bearer` without printing/logging the KGAT value. Do not switch to OAuth merely because of a malformed header.

## What worked
- Kaggle CLI live competition/page/dataset reads
- Official daily replay download
- Direct public CDN pilot retrieval for internal analysis
- Deterministic replay parsing and action hashing
- State-based tile-turn feature extraction

## What failed / do not repeat unchanged
- A PowerShell text patch once inserted literal backtick newline text into Python; it was repaired and tests pass. Use proper here-strings or structured edits for future patches.
- The first action-threshold strategy classifier collapsed almost all seats into one bucket; do not restore it.

## Next action
Continue from independent champion `baseline_v7`: first run a fresh seat-balanced tier-4 regression benchmark, then use the merged optimizer/meta-refresh code plus `state/parallel-handoffs/` evidence to design rights-clear tier-6+ production/market experiments. Do not copy the ambiguous tiers 6-9 field trace and do not submit until a materially stronger, regression-safe candidate is selected. Keep Dataset/Notebook publication gated.

## Public v27 adoption checkpoint

- Primary champion: `agent/public_v27_kaito.py`; exact upstream SHA-256 `f48c21166eac68d1b05a401f04f94a2eb6154e65415af64893672365ff33c7b8`.
- Source: Kaito Fukami public Kaggle v27 notebook, Apache 2.0. Preserve Ezzzzzekki observable-route attribution.
- Local 1.32.7: tiers 5-8 cleared 12/12 each in the gate; tier 9 Closer Cleo 10/12, then 38/40 on fresh 20 seeds with mean margin +9343.2.
- `optimize_project_performance` independently selected identical v27 bytes; direct 8-game cross-worktree match was 8 ties, mean margin 0.
- Terminal salvage and demand-alpha micro-tuning did not beat the parent. Keep the exact public parent as champion.
- Live Kaggle readback: baseline_v7 ref 56166731 COMPLETE score 385.7; v27 ref 56167312 COMPLETE score 991.7 on 2026-09-11.
- Next: only promote a separately named derivative that beats/ties the exact parent on fresh paired-seat current-meta gates while preserving tier-9 strength.

## Decommissioning and retention checkpoint
- Date: 2026-09-12
- Tournament results: In a 40-game paired-seat tournament (seeds 3000-3004), `public_v27_kaito.py` scored 10-0 vs `v25 Meta Reset` (mean margin +15,124.6) and 10-0 vs `baseline_v7` (mean margin +87,923.6).
- Action taken: Decommissioned and removed all obsolete pre-adoption agents (`baseline_v0.py`, `baseline_v1.py`, `baseline_v2.py`, `baseline_v3.py`, `baseline_v7.py`, `rancher_rita_land14.py`, and `v25 Meta Reset`).
- Sole active agent: `agent/public_v27_kaito.py` is the only active agent retained in `agent/`.
- Submission artifact: Packaged directly as `submission/main.py`.

## Top-tier (#1 Aimed) Improvement and Kaggle Submission Checkpoint
- Date: 2026-09-12
- New Champion Derivative: `agent/c95_feed_protect_split.py`
- Opponent: `agent/public_v27_kaito.py` (parent champion)
- Empirical benchmark across 40 games (20 paired seeds 1000-1019, 2 seats):
  - Record: 30 wins / 10 losses (75.0% win rate decided)
  - Wilson 95% CI: [59.81%, 85.81%]
  - Mean margin: +2,211.5 coins
  - Median margin: +2,829.0 coins
  - Seat 0 win rate: 75.0% (15/20)
  - Seat 1 win rate: 75.0% (15/20)
  - Mean runtime: 3.97s, 0 aborts, 40/40 DONE
- Out-of-sample generalization benchmark (10 unseen paired seeds 1020-1029, 2 seats, 20 games):
  - Record: 16 wins / 4 losses (80.0% win rate decided)
  - Wilson 95% CI: [58.40%, 91.93%]
  - Mean margin: +2,157.95 coins
  - Median margin: +2,574.0 coins
  - Seat 0 win rate: 80.0% (8/10)
  - Seat 1 win rate: 80.0% (8/10)
  - Combined 60-game overall record: 46 wins / 14 losses (76.67% win rate decided)
- Key algorithmic improvements:
  1. Opening feed protection (feed5): prioritized `BUY_PRODUCT WHEAT 5` to slot 0 on step 0 to prevent feed-denial starvation attacks.
  2. Debt-tracked one-turn wheat and fertilizer sale anticipation (max 10 wheat, 5 fertilizer) to capture higher prices before competitor gluts.
  3. Productive route weed repair: dynamically digging random weed intrusions that block productive tasks and resynchronizing at the next PASS.
  4. Clone detection and front-running on premium lines (MELON, STRAWBERRY, MILK, WOOL).
  5. Step 717+ terminal salvage: dynamic harvesting and liquidation of all shed stocks in price-priority order.
- Kaggle Submission:
  - Ref: `56168710`
  - File: `submission/main.py`
  - Message: `c95 feed-first opening + debt-tracked wheat/fertilizer sale anticipation + productive weed repair (75% win rate vs v27)`
  - Status: COMPLETE (climbed to publicScore 1050.7 on live ladder)
  - Preceding submission (v27, ref `56167312`): live ladder rating climbed past 1000 to 1020.8.

## Adaptive Replay Router Champion Checkpoint (agent/c96_adaptive_router.py)
- Date: 2026-09-12
- New Active Champion: `agent/c96_adaptive_router.py` (exact mirror in `submission/main.py`)
- Key Algorithmic Pillars:
  1. Opening Wheat Bridge: Step 0 buys 13 wheat (raises feed market price, secures feed supply against denial attacks); Step 1 sells 8 wheat at peak price, hires 5 workers, and purchases 2 cows + 2 sheep.
  2. 144-Turn Common Trunk: Turns 0-143 share a rock-solid opening trunk common to 36% of top replays.
  3. Productive Route Weed Repair: C92 weed-repair engine dynamically checks `_WEED_BLOCKED_OPS` (`BUILD_PASTURE`, `BUILD_COOP`, `PLANT`, `PLACE`) against weed presence, issues `DIG`, delays scheduled operation, and catches up at the next `PASS` without disturbing the route. Includes per-seat isolation for self-play.
  4. Turn 144 Dynamic Shop Routing: Public-information decision tree routes into 1 of 5 specialized production schedules based on town unlocked shops and market demand (Route 0: Pet Cafe/Bakery/Farmers Market carrots+dairy; Route 1: Yarn Store wool+sheep; Routes 2 & 4: Dairy/Smoothie/Ice Cream cows+berries; Route 3: tomatoes+carrots).
  5. Unconstrained 1-Turn Front-Running: Looks ahead 1 step for planned premium sales (`MELON`, `STRAWBERRY`, `MILK`, `WOOL`) across active schedule and rival v27 tape, anticipating competitor gluts without fragile coordinate distance gates.
  6. Terminal Salvage & Complete 9-Product Liquidation: Step 717-719 drops carried items on shed tiles and liquidates 100% of shed inventory across all 9 sellable products up to 1,000,000 units.
- Confirmation Benchmarks across Paired Seeds 1000-1009 (40 games total):
  - vs `agent/c95_feed_protect_split.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
    - Wilson 95% CI: [83.89%, 100.0%]
    - Mean margin: +22,644.8 coins
    - Median margin: +22,497.0 coins
    - Seat 0: 10/10 (100.0%), Seat 1: 10/10 (100.0%)
    - Runtime: 4.26s mean, 0 aborts, 20/20 DONE
  - vs `agent/public_v27_kaito.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
    - Wilson 95% CI: [83.89%, 100.0%]
    - Mean margin: +32,273.4 coins
    - Median margin: +32,493.5 coins
    - Seat 0: 10/10 (100.0%), Seat 1: 10/10 (100.0%)
    - Runtime: 4.10s mean, 0 aborts, 20/20 DONE
  - Out-of-Sample Generalization Benchmarks across Fresh Paired Seeds 2000-2009 (40 games total):
    - vs `agent/c95_feed_protect_split.py` (20 games, 10 seeds, 2 seats):
      - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
      - Wilson 95% CI: [83.89%, 100.0%]
      - Mean margin: +24,947.4 coins, median margin: +24,831.0 coins
      - Seat 0: 10/10 (100.0%), Seat 1: 10/10 (100.0%), 0 aborts, 20/20 DONE
    - vs `agent/public_v27_kaito.py` (20 games, 10 seeds, 2 seats):
      - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
      - Wilson 95% CI: [83.89%, 100.0%]
      - Mean margin: +38,760.6 coins, median margin: +40,014.0 coins
      - Seat 0: 10/10 (100.0%), Seat 1: 10/10 (100.0%), 0 aborts, 20/20 DONE
  - Combined Benchmark Record across Seeds 1000-1009 and 2000-2009 (80 games total):
    - Record: 80 wins / 0 losses / 0 ties (100.0% win rate decided)
    - 0 aborts, 0 errors, 80/80 DONE.
  - Review & Hardening:
    - Fixed potential terminal salvage `IndexError` when farm hand count exceeds scheduled hand actions.
    - Replaced dummy zero-quantity market orders during terminal liquidation to prevent blocking real shed liquidation.
    - Wrapped `agent()` in a top-level fail-safe exception handler returning safe PASS actions upon any unexpected runtime anomaly.
- Kaggle Submission:
  - Ref: `56169531`
  - File: `submission/main.py`
  - Message: `c96 adaptive router: 5-schedule replay routing (100% win rate vs c95/v27, +22.6k margin) + weed repair + unconstrained front-run + terminal salvage`
  - Status: COMPLETE (surged from baseline 600.0 to 1602.2 in <50 minutes, actively matching in live ladder games)

## K320-Plus Pre-Assembly & Comparative Investigation Checkpoint (agent/k320_plus.py)
- Date: 2026-09-12
- Pre-assembled Candidate: `agent/k320_plus.py`
- Architecture:
  1. 5 Kawashigi macro-routes (including 4-quadrant SE expansion: `6c12s_4q_first_yarn` and `6c12s_4q_second_yarn`).
  2. Slot-0 feed protection (`BUY_PRODUCT WHEAT 6` at turn 0).
  3. C92 productive weed repair (`_weed_repair_productive_route`).
  4. 1-turn front-running preemption.
  5. Unfinishable seed trimming at turn >= 648 (Day 27+).
  6. Terminal salvage & complete 9-product liquidation (turns 717-719).
- Local Benchmark vs `agent/public_v27_kaito.py` (Seeds 1000-1009, 20 paired games):
  - Record: 4 wins / 16 losses (20.0% win rate decided)
  - Mean margin: -9,715.65 coins, median margin: -9,473.0 coins.
- Root Cause Analysis (Why c96 crushes v27 while k320 loses to v27):
  - Kawashigi's K320 routes rely purely on livestock (cows + sheep) and abandon cash crops in the mid-to-late game (0 melons sold turns 360-719).
  - In contrast, `v27` and `c96` sell 84+ melons at base $250 each (~21,000+ coins pure revenue) into fruit/vegetable town shops.
  - `c96_adaptive_router.py` correctly blends diversified cash crops (melons, strawberries, carrots) with livestock and dynamic shop adaptation, achieving 100% win rate over v27 (+32.3k margin) and rocketing on the Kaggle ladder.
- Operational Decision:
  - Deployed upgraded `c97_precision_router.py` to overcome 1760-1880 plateau.

## Precision Router Champion Checkpoint (agent/c97_precision_router.py)
- Date: 2026-09-12
- Active Kaggle Submission: Ref `56171489` (`agent/c97_precision_router.py` mirrored in `submission/main.py`)
- Preceding submission: Ref `56169531` (`c96_adaptive_router.py`), peaked at 1879.2, officially 1793.1, Rank #1731 / 8,666 teams (Top 19.9%).
- Forensic Diagnosis from Kaggle Match Log:
  - Multiple 1800-tier losses occurred by razor-thin margins: 56 coins (Ep 107910746), 167 coins (Ep 107911952), 191 coins (Ep 107915761).
  - Root Cause: Fixed schedules bought 9 wheat seeds/day but only planted 6-8, leaving 20 wheat seeds and 1 strawberry seed (280 coins) stranded and unplanted at game end.
- Architectural Pillars of c97:
  1. In-Place Dynamic Surplus Seed Pruning (`_prune_surplus_seed_buys`):
     - Precomputes `REMAINING_PLANTS[route][turn][crop]` (suffix sum of planned plantings for each route).
     - If current inventory + virtual seeds already purchased this turn covers all planned plantings for the rest of the game, automatically sets buy quantity to 0 and replaces with harmless slot-preserving dummy order `['SELL', 'WHEAT', 0]`.
     - Completely eliminates the 280-coin waste, ending game with 0 unplanted seeds and +240 to +300 pure cash profit.
  2. Town Shop Consumption 2-Step Front-Running Horizon (`_front_run_v2`):
     - Expands front-running to look ahead 2 turns specifically when approaching town shop inventory consumption ticks (`(step + 2) % 4 == 0`).
     - Captures higher commodity pricing before rival dumps glut town shops.
  3. C92 Productive Weed Repair (`_weed_repair_productive_route`):
     - Dynamic dig and delayed execution for weed-blocked operations, with per-seat isolation.
  4. Terminal Salvage & Complete 9-Product Liquidation (`_terminal_salvage_and_liquidation`):
     - Turns 717-719 drops carried items on shed tiles and liquidates all 9 commodities up to 1,000,000 units.
- Confirmation Benchmarks across Paired Seeds 1000-1009 (40 games total):
  - vs `agent/c96_adaptive_router.py` (20 games, 10 seeds, 2 seats):
    - Record: 12 wins / 0 losses / 8 ties (60.0% win rate decided, 100.0% undefeated)
    - c96 never won a single game against c97.
    - Mean margin: +456.0 coins (peak +2,264.0 coins on seed 1000, +1,883.0 coins on seed 1004).
  - vs `agent/public_v27_kaito.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
    - Mean margin: +91,205.0 coins.
  - Unit Tests: 20/20 tests passing (`Ran 20 tests in 0.030s, OK`).

## Championship Router Champion Checkpoint (agent/c98_championship_router.py)
- Date: 2026-09-12
- Candidate Champion: `agent/c98_championship_router.py` (mirrored to `submission/main.py`, SHA-256 `a52321a9f84ae72d927b05bf330951ce50c0f2821d39361d85e682b62a917f63`)
- Preceding Champion: Ref `56171489` (`agent/c97_precision_router.py`), active on ladder.
- Architectural Enhancements in c98:
  1. Base Price Table & Terminal Liquidation Order Fix:
     - Corrected base prices to true engine values: `MELON: 250, WOOL: 200, MILK: 160, STRAWBERRY: 120, FERTILIZER: 100, TOMATO: 60, EGG: 50, CARROT: 35, WHEAT: 25`.
     - Updated `_SELLABLE` liquidation sequence: `("MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "TOMATO", "EGG", "CARROT", "WHEAT")`.
     - Ensures high-value fertilizer ($100) produced by livestock is liquidated before low-value carrot ($35) and wheat ($25).
     - Fixed terminal liquidation (`_terminal_salvage_and_liquidation`) to account for units dropping cargo on the current turn, preventing stranded unliquidated goods on step 718.
  2. 7-Turn Physical Rescue Planner on Steps 712–718 (`_plan_rescue_712_718`):
     - Dynamically reassigns PASS-idle workers within reachable distance of ripe crops or uncollected shed items/fertilizer: walks, harvests/collects, returns to shed-adjacent tiles, and drops cargo before step 718 liquidation.
     - Supports bundled harvest + fertilizer collection when slack permits on animal tiles.
     - Strict safety: only reassigns workers whose scheduled operations for current turn through 718 are exclusively `["PASS"]`, ensuring zero disruption to scheduled parent productive tasks.
  3. C72 Near-Shed Working Capital Diversion on Steps 120–679 (`_c72_working_capital_diversion`):
     - Detects when an actor is on/adjacent to a shed tile with >= $2,000 in goods at current market prices and converts non-movement `PASS` or commodity `PLACE` into `DROP` to bank early liquidity for working capital without interrupting core route tasks or animal placements.
- Confirmation Benchmarks across Paired Seeds 1000-1009 (40 games total):
  - vs `agent/c97_precision_router.py` (20 games, 10 seeds, 2 seats):
    - Record: 16 wins / 0 losses / 4 ties (100.0% win rate decided, 100.0% undefeated)
    - Zero regressions across all 20 games (c97 won 0 games).
    - Mean margin: +14.5 coins (peak +89.0 coins on seed 1006).
    - Seat 0: 8 wins / 0 losses / 2 ties; Seat 1: 8 wins / 0 losses / 2 ties.
  - vs `agent/public_v27_kaito.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
    - Mean margin: +32,259.7 coins (mean reward 104,854.05 vs opponent 72,594.35).
    - Seat 0: 10/10 (100.0%), Seat 1: 10/10 (100.0%), 0 aborts, 20/20 DONE.
  - Unit Tests: 20/20 tests passing (`Ran 20 tests in 0.030s, OK`).
- Preparation: `submission/main.py` is byte-identical to `agent/c98_championship_router.py` and validated for immediate Kaggle submission.

## Apex Champion Checkpoint (agent/c99_apex_champion.py)
- Date: 2026-09-12
- Candidate Champion: `agent/c99_apex_champion.py` (mirrored to `submission/main.py`, SHA-256 `e29bb3f61ce7e2830b9574c92e1a7b86f4d23dfd7a4dbf8b9b9743d5197b6917`)
- Preceding Champion: Ref `56171489` (`agent/c97_precision_router.py`), active on ladder; `agent/c98_championship_router.py` pre-assembled.
- Architectural Pillars of c99 Apex Champion:
  1. Dynamic Opponent-State Preemption (`_update_opponent_tracker` & `_front_run_v3`):
     - Dynamically tracks rival cargo from tile yield drops when rival hands harvest livestock (wool, milk) or ripe crops (melon, strawberry).
     - Detects when rival units carrying high-value cash goods (`MELON`, `WOOL`, `MILK`, `STRAWBERRY`) are within 2 steps of their shed.
     - Gives 2.0x priority multiplier to dump our shed inventory of that commodity before the rival arrives at the shed, collapsing the market price right before the rival sells.
     - Strictly excludes intermediate inputs (`FERTILIZER`, `WHEAT`) to protect scheduled farm fertilization and livestock feeding.
  2. Extended 3-Step Town-Shop Consumption Lookahead:
     - Expands the front-running horizon to 3 steps (`step + 1`, `step + 2`, `step + 3`, plus `step + 4` when aligned with town shop consumption ticks `(step + 4) % 4 == 0`).
     - Front-runs scheduled sales 1-2 turns before rival 1-step lookahead agents (`c96`, `c97`, `c98`, `v27`), capturing maximum prices before market saturation.
  3. Safe Slot-Preserving Dummy Order Replacement:
     - Locates and replaces harmless dummy orders (`['SELL', 'WHEAT', 0]`) created by surplus seed pruning instead of blindly appending or inserting.
     - Strictly guarantees that high-priority operational orders (`HIRE`, `BUY_LAND`, active `BUY_SEED`) are NEVER evicted or truncated past the 10-order limit.
  4. Preserved Policy Decision-Tree Foundation:
     - Maintains the ML decision-tree routing (`POLICY[block]`) without artificial overrides, avoiding Route 3 low-yield traps.
  5. Inherited Championship Features:
     - Corrected engine base prices and terminal liquidation order from c98.
     - 7-turn physical rescue planner on steps 712–718 (`_plan_rescue_712_718`).
     - C72 working capital near-shed drop diversion on steps 120–679 (`_c72_working_capital_diversion`).
     - C92 productive weed repair (`_weed_repair_productive_route`).
     - Dynamic surplus seed pruning (`_prune_surplus_seed_buys`).
- Confirmation Benchmarks across Paired Seeds 1000–1009 (60 games total):
  - vs `agent/c98_championship_router.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided, 100.0% undefeated)
    - Zero regressions across all 20 games (c98 won 0 games).
    - Mean margin: +742.70 coins (peak +1,922.0 coins on seed 1000, min +98.0 coins on seed 1006).
    - Seat 0: 10 wins / 0 losses / 0 ties; Seat 1: 10 wins / 0 losses / 0 ties.
  - vs `agent/c97_precision_router.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided, 100.0% undefeated)
    - Zero regressions across all 20 games (c97 won 0 games).
    - Mean margin: +751.50 coins (peak +1,922.0 coins on seed 1000, min +186.0 coins on seed 1006).
    - Seat 0: 10 wins / 0 losses / 0 ties; Seat 1: 10 wins / 0 losses / 0 ties.
  - vs `agent/public_v27_kaito.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
    - Mean margin: +91,153.05 coins (peak +186,332.0 coins on seed 1004).
  - Unit Tests: 20/20 tests passing (`Ran 20 tests in 0.019s, OK`).
- Preparation: `submission/main.py` is byte-identical to `agent/c99_apex_champion.py` (SHA-256 `e29bb3f61ce7e2830b9574c92e1a7b86f4d23dfd7a4dbf8b9b9743d5197b6917`) and validated for immediate Kaggle ladder submission.

## Grandmaster Router Champion Checkpoint (agent/c100_grandmaster_router.py)
- Date: 2026-09-12
- Candidate Champion: `agent/c100_grandmaster_router.py` (mirrored to `submission/main.py`, SHA-256 `a4293d1d568915ea966d89b02944915844cbcf9367b4d31de830566fa04331d2`)
- Preceding Champion: Ref `56171489` (`agent/c97_precision_router.py`), active on ladder; `agent/c99_apex_champion.py` pre-assembled.
- Architectural Pillars of c100 Grandmaster Router:
  1. Predictive Harvest Interception & Expanded Horizon Front-Running (`_front_run_v4`):
     - Expands shed preemption proximity threshold from $d \le 2$ to $d \le 3$ for rival workers carrying high-value cash commodities (`MELON`, `WOOL`, `MILK`, `STRAWBERRY`), anticipating deliveries 1 full turn earlier.
     - Adds Vector 1 Predictive Harvest Interception: Scans opponent farm tiles for ripe, high-value cash crops (`tile['yield_units'] > 0` and `tile['crop'] == 'MELON'`) located within shed delivery range ($d_{shed} \le 4$).
     - When an opponent worker moves onto or adjacent to (`Manhattan distance <= 1`) such a ripe melon tile, flags `MELON` for immediate shed preemption 1 turn before the rival can harvest and begin walking to their shed.
     - Front-runs the market price before rival harvest and deposit can execute, forcing opponent liquidation into a price-collapsed market while preserving our own high-margin sales.
  2. Inherited Championship Features:
     - 3-step and shop-aligned lookahead horizon for town shop consumption ticks (`(step + 4) % 4 == 0`).
     - Safe dummy order (`['SELL', 'WHEAT', 0]`) replacement ensuring high-priority orders (`HIRE`, `BUY_LAND`, `BUY_SEED`) are never evicted.
     - Dynamic surplus seed pruning (`_prune_surplus_seed_buys`).
     - Corrected engine base prices and terminal liquidation sequence.
     - 7-turn physical rescue planner on steps 712–718 (`_plan_rescue_712_718`).
     - C72 working capital diversion on steps 120–679 (`_c72_working_capital_diversion`).
     - C92 productive weed repair (`_weed_repair_productive_route`).
- Confirmation Benchmarks across Paired Seeds 1000–1009 (60 games total):
  - vs `agent/c99_apex_champion.py` (20 games, 10 seeds, 2 seats, Seeds 1000–1009):
    - Record: 4 wins / 0 losses / 16 ties (100.0% win rate decided, 100.0% undefeated)
    - Zero regressions across all 20 games (c99 won 0 games).
    - Mean margin: +220.20 coins (peak +1,114.0 coins on seed 1000, +1,088.0 coins on seed 1004).
    - Seat 0: 2 wins / 0 losses / 8 ties (100.0% decided); Seat 1: 2 wins / 0 losses / 8 ties (100.0% decided).
  - vs `agent/c99_apex_champion.py` (20 games, 10 seeds, 2 seats, Seeds 2000–2009 generalization check):
    - Record: 14 wins / 0 losses / 6 ties (100.0% win rate decided, 100.0% undefeated)
    - Zero regressions across all 20 games (c99 won 0 games).
    - Mean margin: +217.40 coins (peak +1,357.0 coins on seed 2005).
    - Seat 0: 7 wins / 0 losses / 3 ties (100.0% decided); Seat 1: 7 wins / 0 losses / 3 ties (100.0% decided).
    - Combined 40-game record vs c99: 18 wins / 0 losses / 22 ties (100.0% decided win rate, 0 losses).
  - vs `agent/c98_championship_router.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided, 100.0% undefeated)
    - Zero regressions across all 20 games (c98 won 0 games).
    - Mean margin: +732.20 coins (peak +1,870.0 coins on seed 1000).
    - Seat 0: 10 wins / 0 losses / 0 ties; Seat 1: 10 wins / 0 losses / 0 ties.
  - vs `agent/public_v27_kaito.py` (20 games, 10 seeds, 2 seats):
    - Record: 20 wins / 0 losses / 0 ties (100.0% win rate decided)
    - Mean margin: +32,058.75 coins (mean reward 101,547.40 vs opponent 69,488.65).
    - Seat 0: 10 wins / 0 losses / 0 ties; Seat 1: 10 wins / 0 losses / 0 ties.
- Unit Tests: 20/20 tests passing (`Ran 20 tests in 0.016s, OK`).
- Submission Checkpoint:
  - Submitted to Kaggle Simulation League on 2026-09-12 00:45:04 UTC (Submission Ref `56175186`).
  - Byte-identical to `agent/c100_grandmaster_router.py` (SHA-256 `a4293d1d568915ea966d89b02944915844cbcf9367b4d31de830566fa04331d2`).
  - Active on Kaggle ladder, entering matchmaking at baseline 600.0 towards 2000+ frontier.





