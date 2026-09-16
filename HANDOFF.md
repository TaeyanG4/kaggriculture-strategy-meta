# Kaggriculture Current Handoff

## Latest: c156~c171 candidates implemented; activation screen prepared (2026-09-15)

- Candidate discovery is closed at c171 by user request. No c172 artifact was created.
  The next action is the prepared 1,344-game screen after every other Kaggriculture
  coordinator/worker tree has exited; do not overlap the currently observed o207 run.
- Frozen local parent is `agent/o182_combo_overflow.py`, SHA-256
  `ef9d2aade50ce2ce400a64791288ffb179eee7a6e60ea0d06085ac12fe02900b`.
- Reacting-screen candidates built directly from that parent: c156 production-cap
  harvest, c160 day-29 persistent harvest, c163 worthless-CARE fertilizer recovery,
  c168 certified FERTILIZE-before-WATER, c170 exact-spawn fertilizer-tour assignment,
  and c171 safe V42 non-YARN production routes.
- c159 is an immutable conservative prototype superseded by c170: a static complete
  search found that post-select safety filtering could reject the global maximum and
  miss a safe improving runner-up. c170 applies every target's parent gain floor
  inside the beam search.
- c167/c169 are immutable intermediate V42 artifacts superseded by c171. c171 fixes
  cold-start step-648 reopening, same-step telemetry reset, incomplete-map fallback,
  and malformed shop types while keeping normal routes and all source hashes.
- Combined contract suite: 78 passed. All dedicated builders reran byte-identically.
  No reacting game or submission was performed; all promotion flags remain false.
- Common v1 activation/health screen is prepared and checked at
  `state/agent_experiments/c156_c171_activation_screen_20260915/`: 1,344 games =
  7 models x 8 independent-family opponents x 12 fresh seeds x both seats, 8 workers.
  Run only its `screen` stage. This is an activity/health filter, not promotion proof.
- Detail and exact user-run command:
  `reports/c156-c171-implementation-and-screen-2026-09-15.ko.md`.

## Latest: c160 day-29 harvest screen prepared (2026-09-15)

- Built `agent/c160_day29_harvest.py` from exact `o182_combo_overflow.py` plus a
  narrow overlay. SHA-256: `c3f5d1749665d173640c29271635de8cf5ea761f6dcc8bb82e0820c5a42776fc`.
- Only at steps 696..711, replace a parent `WATER`/`FERTILIZE` with `HARVEST`
  when that actor is standing on TOMATO/STRAWBERRY with existing yield. Market,
  movement, purchases, hiring, planting, and the step-712 terminal planner stay intact.
- Compile, last-callable, synthetic mechanism tests, reusable-runner 9-test suite,
  frozen manifest check, and `git diff --check` passed. No game result exists yet;
  `promotion=false`.
- Frozen native-reacting screen is prepared at
  `state/agent_experiments/c160_o182_long_screen_20260915/`: 4,096 games,
  128 fresh seeds x 8 distinct-author/family opponents x 2 models x both seats,
  8 workers. Config stages are disjoint and have no overlap with prior validation
  configs. Run only the screen first; confirm/final remain unused.
- Each game uses a fresh subprocess, immutable job/source hashes, and unique temp,
  logs, and results. Parallel workers execute a frozen schedule and cannot adapt to
  or read another worker's partial result. c159 fertilizer-tour work remains separate.

## Latest: c155/o160 screen reviewed (2026-09-15)

- 1152/1152 rows revalidated. W/L/T per 288: c150 157/51/80, c155 175/49/64,
  o159b 243/45/0, o160 256/32/0. o160 is strongest on this panel, not qualified elite champion.
- c155-c150 +3.47pp, approximate 97.5% CI +1.04..+6.60pp, win-to-loss 0.
  o160-c150 +20.49pp but win-to-loss 8; o160-o159b +4.51pp, CI crosses zero,
  win-to-loss 9 and worse loss tail. No promotion/submission.
- Next implementation-only design: o161=c150+harvest-only; o162=o159b+goose-only
  harvest (threshold3 unchanged). Separate feed/harvest interaction and species scope.
- Review: `reports/c155-o160-screen-review-2026-09-15.ko.md`.
  Copyable prompt: `reports/o161-o162-implementation-prompt-2026-09-15.ko.md`.
  No candidates implemented or simulations launched; await user implementation report.

## Latest: reusable validation v1 implemented (2026-09-15)

- All agents must reuse the framework rather than create candidate-specific tooling.
  See AGENTS.md's REUSE FIRST rules; CLAUDE.md points Claude Code to the same rules.

- New experiments use `tools/run-validation.ps1` + `tools/validation_v1.py` +
  `tools/validation_stats_v1.py`; change JSON config and output folder, not runner copies.
- Example: `configs/validation/c155-o160-v1.example.json`. Read
  `docs/reusable-validation.ko.md` for Prepare/Check/Run/Analyze and screen/confirm/final.
- Existing o160 and c155/o160 campaigns remain immutable. The example is not a request
  to rerun them. No games were launched for framework implementation.
- User implements agents; this session designs validation and reviews user-run results.
  Only the common framework implementation was explicitly delegated to this session.
- All automatic outcomes remain promotion=false; statistical signals require review.

## Latest: long-validation isolation contract (2026-09-15)

- The user accepts longer runs to reduce seed luck and allows up to the global cap of
  8 workers. Do not start a second campaign while any Kaggriculture worker tree exists.
- Every match must be a fresh Python subprocess with a unique immutable job JSON, log,
  result file/output directory, explicit seed, candidate seat and frozen source hashes.
  Do not use threaded in-process games or share imported agents, monkeypatches, module
  globals, temporary paths, or RNG state between parallel work.
- Baseline and candidate must use the same seed/opponent in both seats. Development,
  selection, and final seeds stay disjoint. Parallel chunks may execute frozen jobs but
  must not adapt from another chunk's partial results.
- At this checkpoint an `o158` fixed-shop elite suite owns six worker branches under
  `o_results/elite_suite/o158/`. Recheck its coordinator/child tree before preparing or
  starting any new campaign; do not infer activity from lock files alone.

## Latest: c154 maintenance-feed rejected (2026-09-15)

- Read-only audit of the 12 latest c153 losses confirms the inherited c129 gap grows
  mainly before the terminal seven turns. From steps 504..695, ours used 206 more
  feed WHEAT while harvesting +170 MILK/+32 WOOL but -97 WHEAT and using 86 less
  fertilizer. At step 712 the aggregate individually reachable harvest-value gap was
  only -66; both sides ended with zero harvestable yield.
- Built `agent/c154_maintenance_feed.py`, SHA-256
  `c4121ea5ec69cc2d1a90272309711f927566ab2319b08f9a902484eb6a66712b`.
  It retains c124's first low-margin feed skip, restoring only a second consecutive
  c124-confirmed skip to prevent escape. This is distinct from rejected c137, which
  restored every sheep feed.
- Recorded-observation shadow: active in 3/12 latest losses, changing only PASS->FEED
  at steps 603/608/612; c129/server mismatches 0. This proves scope/activity only.
- The six-game fixed-opponent mechanism probe completed healthy but failed its gate.
  Across the three paired episodes, c154 worsened margin by 69, 229 and 279
  (total -577) and own cash by 79, 291 and 153 (total -523). Every episode was
  worse and every candidate row reported `maintenance_feed_ambiguous=1`.
- Reject c154. Do not advance it to reacting validation or tune this maintenance-feed
  rule. The result reinforces that preserving low-value animals can cost more WHEAT
  than it returns, even when only the second consecutive skipped feed is restored.
- Evidence: `state/agent_experiments/c154_maintenance_feed_20260915/results.json`.
  This is fixed-shop/frozen-opponent mechanism evidence, not a broad win-rate estimate.
- Detail: `reports/c154-maintenance-feed-development-2026-09-15.ko.md`.

## Latest: c153 direction audit (2026-09-15)

- c153 live snapshot 2383.3 / 59W12L among 71 scored returned games; c129 2820.3.
  Different opponents/seeds/times prevent a causal rating comparison.
- Downloaded all 12 returned c153 losses. On all 719 observations in every game,
  c129 and c153 actions match each other and the actual submitted action exactly.
  These defeats are inherited behavior, not observed c153-triggered regressions.
- Prior c153 reacting gate was FALSE (0 changed conditions / 896); submitting it
  as an improvement was not justified by generalization evidence. Keep c129 baseline.
- Old c153 mechanism runner has unsafe in-process threaded engine monkeypatching.
  Fresh 8-game subprocess audit reproduced +5947/+2997 in BOTH native/fixed modes,
  all exact shop paths. Retract the old claim that candidate caused shop divergence.
- Direction: evaluate executable late-harvest/cash-recovery bundles, then middle-game
  production/reinvestment choices, with shared resource reservation. Require actual
  activity before large evaluation; tune only after reacting improvement evidence.
- See `reports/c153-regression-and-direction-audit-2026-09-15.ko.md` and
  `state/agent_experiments/c153_direction_audit_20260915/`. No new submission this audit.

## Latest: c153 validated and submitted (2026-09-14 night)

- Submitted `agent/c153_urgent_feed_exact1.py` once, Kaggle ref `56232526`.
  Server status is `COMPLETE` with initial rating 600.0; do not duplicate-submit it.
- Source SHA-256: `b31bbbe2f7c0f8ab93dd773cfc441e40e65d23caaf30c29e6ae42c44e25ed383`.
  Archive SHA-256: `3e7c482519a95468f271ba09941d3b52077bdec787e34075475cd4ebb418d4ca`.
  Server-downloaded archive and sole `main.py` match the local package exactly.
- Fresh reacting/public panel: 1,792/1,792 healthy games, 896 c129/c153 paired
  conditions, zero action/point/margin/cash changes and zero regressions. The
  mechanism was inactive, so this is non-regression evidence, not improvement.
- Requested public opponents: both c129 and c153 scored 76W/52L against each of
  shop-router-reactive-v5, V41 Review Candidate, and Dynamic Route Agent.
- Fixed-opponent mechanism cases passed: episode 108609267 improved margin +5,947
  and own cash +1,569; episode 108724215 improved margin +2,997 and own cash -305.
  Both confirmed purchase/pickup/feed/survival for three animals with zero contract
  failures. The former used native shops after its strict fixed-shop path diverged.
- Keep c129 as confirmed live champion until c153 accumulates enough Kaggle matches;
  the new-agent initial 600.0 is execution confirmation, not a performance comparison.
  Receipt: `state/submission_artifacts/c153_urgent_feed_exact1_20260914/receipt.json`.
  Detail: `reports/c153-autonomous-validation-submission-2026-09-14.ko.md`.

## Latest: c151 failed; c152 expansion-only probe ready (2026-09-14 evening)

- c151 probe completed 128/128 healthy games. Versus paired c146 baselines:
  point delta -3, margin -4,332, own cash -2,278, action changes 6, gate failed.
  c151 evaluated 1,200 certificates and rejected all; it suppressed c146's profitable
  seed 640603013 conversions. Do not submit or tune c151.
- Built `agent/c152_shop_expansion.py` from hash-guarded c146. SHA-256
  `785529ac46ca6731b8901836bab48a1eb647203e9a1b7c9395495a6f7c6ac2fa`.
  c146's demand>=25 branch is exact; the forecast only expands into lower-demand shops.
  Seven mechanism tests passed, including legacy behavior equality and fail-closed timing.
- Prepared and checked 64 new c152 games against 64 exact frozen c146 outputs:
  `& 'H:\dev\kaggle-data\kaggriculture-strategy-meta\state\agent_experiments\c152_shop_expansion_probe_20260914\run.ps1'`
  Eight workers, progress/ETA/cache/resume/notification, roughly 2-5 minutes.
- When complete, analyze `state/agent_experiments/c152_shop_expansion_probe_20260914/results.json`.
  First require legacy seed 640603013 non-regression, then inspect low-demand expansion
  requests, paired points/cash/margin, related/nagata subgroups and bottom tail.
- Detail: `reports/c151-result-and-c152-expansion-2026-09-14.ko.md`.

## Latest: c151 shop-demand development probe (2026-09-14)

This checkpoint supersedes the older runtime/candidate notes below for the next action.
Python 3.12.6 / kaggle-environments 1.32.7 is restored and exact engine identity verified.
The user runs simulations; none were launched in this implementation turn.

- Implemented `agent/c151_shop_forecast.py`, a c146 derivative, **not c150 + c146**.
  SHA-256 `47c1ee52c03f07d79482ec8e3625abdadb2d542387203946803a1a607cd3cab1`.
- Replaces fixed carrot shop threshold with exact known-shop consumption to harvest,
  public crop supply, stock/commitment deduplication, and wheat scarcity opportunity cost.
  Retains the 18-25 day window and physical purchase/plant/feed/harvest guards.
- 12 mechanism tests + 3 summary tests passed; PowerShell parse and frozen plan check passed.
  No reacting improvement, promotion, or rank-1 claim yet.
- Ready user command: `& 'H:\dev\kaggle-data\kaggriculture-strategy-meta\state\agent_experiments\c151_shop_probe_20260914\run.ps1'`
- 128 games = c146/c151 × 8 reused development seeds × c129/c150/c146/nagata × both seats;
  8 workers, estimated 5-10 minutes, progress/ETA/cache/resume and audible notifications.
  Sources/jobs/support/engine are frozen. Do not edit them; use a new experiment for changes.
- Analyze `state/agent_experiments/c151_shop_probe_20260914/results.json` when user completes.
  First check actual action changes and subgroup/tail regressions; do not tune inactive settings.
- Detail: `reports/c151-shop-forecast-development-2026-09-14.ko.md`.

## Older context (some snapshot and blocker notes below are historical)

Updated 2026-09-14 KST. This is a current-state index, not a chronological log.
Full pre-compaction files are preserved under
`state/context-archive/20260914-121406/`.

## Champion and live evidence

- Submitted champion: `agent/c129_feed_liquidity.py`.
- Kaggle submission ref: `56209242`; prior readback was COMPLETE with empty error and
  server archive/source match.
- SHA-256: `e9973586cbe2c0bbb034243f3d3e4c9fdcac4fcac432c0de32b0ba0e61f7ca61`.
- Its final pre-submission 64-seed/1024-game paired confirmation improved direct
  points 50% to 53.125% with no common win-to-loss. This was a small tested-pool
  gain, not proof of rank 1.
- Latest downloaded snapshot is
  `state/agent_experiments/c125_followup_20260913/snapshots/20260914T015403531994Z/`:
  c125 score 2833.6, 97W/43L/1T in 141 games; c129 score 2810.8,
  83W/36L in 119 games. Panels and times differ, so scores are not a paired model
  comparison.

## Loss evidence: 79 recorded defeats

The latest snapshot adds 32 losses to the earlier 47: c125 adds 17 and c129 adds
15. All 79 replay files exist locally. The read-only audit is:

- `state/agent_experiments/structural_loss_audit79_20260914/analyze_recorded.py`
- `state/agent_experiments/structural_loss_audit79_20260914/summary.json`
- `state/agent_experiments/structural_loss_audit79_20260914/results.json`

The script imports neither an agent nor the engine. It verifies 720 states and the
snapshot/replay margin, then records action/state transitions. Results are diagnostic,
not causal counterfactuals.

Key all-79 observations:

- Severity: 11 losses under 500, 55 from 500 to 4,999, and 13 at 5,000 or worse.
- 32 games were ahead at step 504 and still lost; 34 lost at least 2,000 cash from
  step 504 to the end. Aggregate late swing was -248,105.
- Opponent used less feed in 64/79 and more fertilizer in 60/79. Opponent recorded
  more successful harvested units in 34/79.
- Our traces contain 765 failed FEED transitions, 23 failed wheat pickups,
  6 failed animal placements, and 184 animal disappearances. These counts include
  repeated scheduled attempts and do not individually prove avoidable lost profit.
- New 32 are consistent with the inherited weakness: 15 late reversals, 15 late
  decays of at least 2,000, opponent less feed in 25, more fertilizer in 22, and
  our failed wheat pickups 16 versus rival 3.
- Repeated opponent submissions form useful clusters; see `repeated_opponent_submissions`
  in the summary. Do not count their games as independent families.

Current diagnosis: c125 and c129 share a production-allocation and execution-chain
weakness. The recurring path is market choice plus `HIRE -> BUILD -> PLACE -> FEED ->
HARVEST/SELL`, with wheat, feed, fertilizer, and late conversion competing for the
same labor and cash. Small timing losses and large structural losses require separate
objectives.

## Candidate state

### c145

`agent/c145_carrot_min3.py` passed the old 47 fixed-tape development gate:
3 improved, 44 same, 0 worse; margin +4,130 and own cash +932. Its 192 reacting
games were all inactive and identical to c129. It showed no broad effect and is not
a promotion candidate.

### c146 — strongest current diagnostic improvement

- Source: `agent/c146_carrot_sched3.py`
- SHA-256: `5e51caad786dac00f98639e8eb8ef911a169904f86cff3d2fe777853cd89a928`
- Result: `state/agent_experiments/c146_carrot_sched3_20260914/results.json`
- Old 47 tapes: 4 improved, 43 same, 0 worse; total margin +6,352; own cash
  +1,569; 11 conversions and 11 confirmed plants.
- This is the largest clean improvement among current unsubmitted fixed-tape
  candidates. It has no reacting qualification and is not champion.
- A 12-game realized-economics trace was prepared at
  `state/agent_experiments/c146_realized_trace_20260914/`, but its runner must use
  the exact restored runtime before execution.

### c147 — isolated feed commitment repair

- Source: `agent/c147_feed_commitment.py`
- SHA-256: `d055f46ce8340ed1e309b14d28f30521c424368c720cd45911952e7fbb89d3ea`
- It only buys a bounded wheat shortfall when the parent is already picking up a
  demanded cow/sheep and the route proves next-turn wheat pickup, placement, and
  first feed. Episode 108609267 should request exactly 2 wheat for 2 sheep.
- Static candidate build passed. No simulation result exists and no promotion claim
  is allowed.

### Rejected or limited directions

- c137 blanket late-sheep rescue worsened 14 of 15 activations; do not revive it.
- c139 improved synthetic opening stress but was inactive on the broad reacting
  panel and had a shared-seed regression cluster; do not promote it.
- c140/c141/c142 opening variants gained points in related pools but had major margin
  tails or win-to-loss regressions; keep as stress evidence.
- c143/c144 improved only one old tape while reducing own cash; their gates failed.

## Runtime blocker

The project `.venv` points to removed Python 3.12.6:
`C:/Users/Taeyang/AppData/Local/Programs/Python/Python312/python.exe`.
Bundled Python 3.12.14 can import `kaggle-environments==1.32.7` through the old
site-packages, but strict `engine_identity()` correctly rejects the Python version
change. Do not relax this check.

An attempt to install Python 3.12.6 inside `state/runtime/python` with `uv` could not
download under the restricted network. The escalated retry was unavailable because
automatic approval review had no active account. No runtime was changed.

Preferred recovery: install exact 3.12.6 into the project-local runtime and point
the wrappers at it, preserving existing identity. Alternative: freeze a new 3.12.14
engine contract and rerun every parent/candidate baseline on identical jobs; never
mix those results with 3.12.6 rows.

## Practical tuning space

The strongest current base for tuning is c146, while c147 must first pass its isolated
mechanism preflight.

Ten useful c146 knobs are: active day window, market-hour cutoff, conversion cap,
demand threshold, visible/competing carrot supply buffer, wheat shadow-inventory
shift, grain quote premium, value cushion, cash reserve, and shed-capacity headroom.
With three values each, a full grid is `3^10 = 59,049` configurations.

Seven useful c147 knobs are: active window, market-hour cutoff, wheat price ceiling,
benefit/cost ratio, route lookahead, maximum funded deficit, and combined cash/capacity
reserve policy. With three values each, this is `3^7 = 2,187`. A naive joint grid is
`3^17 = 129,140,163` configurations. Dormant c146 feed-topup thresholds are excluded
because that mechanism activated zero times in the old tape set.

Recommended search budget after runtime recovery:

1. One-factor screen for c146: baseline plus low/high alternatives for ten knobs =
   21 configurations on discovery conditions.
2. Keep the four knobs with stable subgroup effects; run their 3-level interaction
   grid = 81 configurations.
3. Advance at most six configurations to paired reacting development; reject any
   subgroup point regression, common win-to-loss, or worse loss tail.
4. Test c147 separately. Combine it with c146 only if its physical purchase/pickup/
   placement/feed contract and reacting gates pass.
5. Use untouched final seeds once for the last one or two candidates.

This is 102 discovery configurations before reacting qualification instead of 59,049
or 129 million. Do not tune directly for total margin over the observed 79 losses.
Use separate close-loss, structural-loss, late-reversal, and opponent-family slices.

## Execution rules and next actions

- The user currently runs simulations; do not launch a new campaign autonomously.
- Maximum 8 total workers, with no overlapping Kaggriculture campaign.
- Commands require progress bar, completed/total, percent, elapsed, cached-aware ETA,
  desktop notification, and sound.
- First recover exact Python 3.12.6 or deliberately establish a wholly new paired
  engine contract.
- Then run c147's three sequential preflights and the c146 realized trace.
- Expand the loss diagnostic contract from old 47 to all 79 before using the new
  32 as evidence for a candidate.
- Only after mechanism gates pass, run both seats against independent reacting
  opponents plus related regression controls. Preserve unused final conditions.
- No new submission or simulation was made during this handoff update.

## Current evidence index

- `reports/c145-resume-and-top2-review-2026-09-14.ko.md`
- `state/parallel-handoffs/collaboration-20260914/loss-forensics-47/report.md`
- `state/parallel-handoffs/collaboration-20260914/c146-trace/report.md`
- `state/parallel-handoffs/collaboration-20260914/validation-audit/report.md`
- `state/parallel-handoffs/collaboration-20260914/public-opponents/report.md`
- `docs/agent-validation-protocol.ko.md`

## o-series handoff (Claude, 2026-09-16)
Read `docs/o-handoff-2026-09-16.ko.md` first: current best agent (o227, submission 56264950), the six validation gates (incl. the weed-synced frozen-Majkel proxy and the pinned-world A/B harness), today's confirmed facts (market absorption, mirror externality, top cluster = planners, V44 race arm and the stealth response), the rejected-candidate table (o220–o237), the planner-proxy project status, data assets and the prioritized next steps. Ledger: `o_experiments.jsonl`; chronological log: `reports/o-worklog.md`.
