# Handoff

## Repository
- Workspace: current project root
- Intended branch: `main`
- GitHub target: `TaeyanG4/kaggriculture-strategy-meta`
- Visibility during active competition: private until public-code and source-rights gates are satisfied
- Tests: `python -m unittest discover -s tests -v` passes (4 tests)

## Current phase
- Phase 0 current state: complete for start gate
- Phase 1 market/duplication validation: complete for start gate
- Phase 2 product hypothesis: preserved
- Phase 3 rights gate: source-scoped decision recorded
- Phase 4 small pilot: first measured pilot complete
- Phase 4 expanded official-CC0 pilot: complete
- Overall decision: `NARROW`; full historical backfill is not authorized by the gate

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
Run a targeted bounded validation of the apparent 2026-09-10 strategy diversification, then harden a public-V1 schema centered on continuous opening/economy/resource fingerprints. Keep `strategy_family_pilot` experimental and do not promote a counter matrix until several cross-family pairs have adequate seat-balanced support.
