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
