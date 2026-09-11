# Handoff

## Repository
- Workspace: current project root
- Intended branch: `main`
- GitHub target: `TaeyanG4/kaggriculture-strategy-meta`
- Visibility during active competition: private until public-code and source-rights gates are satisfied
- Tests: `python -m unittest discover -s tests -v` passes (10 tests)

## Current phase
- Phase 0 current state: complete for start gate
- Phase 1 market/duplication validation: complete for start gate
- Phase 2 product hypothesis: preserved
- Phase 3 rights gate: source-scoped decision recorded
- Phase 4 small pilot: first measured pilot complete
- Phase 4 expanded official-CC0 pilot: complete
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
- 46 columns including provenance, source score quantile, outcome, cash checkpoints, first-event timings, opening/labor features, tile-turn resource shares, broad action totals, opening hashes, and an explicitly experimental family label
- Targeted 96-row candidate QA passes: 0 duplicate keys, 0 core missing values, 0 invalid shares, 0 excluded identity fields, 0 Unicode replacement cells
- Candidate CSV size on targeted validation: 34,567 bytes
- Schema: `docs/v1-schema.md`
- Machine-readable QA: `reports/v1_schema_qa.json`
- Alternative comparison: `reports/v1_schema_comparison.json`

## Kaggle
- Competition: `kaggriculture`
- Deadline observed: 2026-09-30 23:59
- Team count observed: 8,602
- Joined: yes
- Kaggle CLI: 2.2.4
- Local `kaggle-environments`: not installed at this checkpoint
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
Build the bounded current-meta V1 for 2026-09-04 through 2026-09-10 at 24 deterministic manifest quantiles per day. Keep raw/row-level artifacts local, generate one local `strategy_meta.csv` candidate plus aggregate QA/provenance, and do not publish yet. The scheduled 2026-09-11 official daily source can be appended when it becomes available.
