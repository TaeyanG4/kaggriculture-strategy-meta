# Kaggriculture Project Operating Context

This checkout is MAIN / Competition Core. Keep this file short; detailed history
belongs in ignored `state/` artifacts and dated reports.

## CURRENT 2026-09-21 — Public Notebook League

- Read `HANDOFF.md` **START HERE** and `docs/public-league.ko.md` before changing collection, matchmaking or live replay work. Public League is the current operating track; older c/o/p experiment sections below are historical context unless the owner explicitly resumes them.
- Service entry points: `src/kaggriculture_meta/public_league.py`, `tools/public_league.py`, `public-league.html`, `public-league.vbs`; state is `state/public_league/`. The current frozen contract is `configs/public_league_v2.json`; keep v1 immutable. Scheduled collection is ON every **3 hours**, including battery operation and catch-up after sleep. Battles use **8 workers** and continue until manually stopped. A 240-game value is an internal BT/rematch batch, not a session stop. v2 preserves every submission sidecar, paginates and size-checks declared datasets before downloading them, uses artifact identity, first-action QA, Docker for Linux `agent.so`, official DONE timing, a 1220-second wall cap, near-rating scheduling, and regularized Bradley–Terry ranking. Compiled C++ identity is the runtime `main.py + agent.so`; build-only source is retained in the notebook archive but excluded from the agent hash. Background-tab heartbeat tolerates 180 seconds; explicit last-tab close shuts down after a 5-second reload grace. Existing agents before the 2026-09-20 NEW baseline are excluded; genuinely later notebook versions show NEW for 12 hours. Notebooks collected without an executable agent appear under `수집됨·대전 불가`, not in the ranking.
- Do not rebuild existing collectors or replay analytics. First inspect `o_tools/live_episodes.py`, `fetch_current_elite.py`, `live_suite.py`, `r_crawl.py`, `rival_source_trace.py`, `elite_profile.py`, `branch_stats.py`, `live_replay_audit.py`, and `src/kaggriculture_meta/replay_accounting.py`. Tool roles and evidence limits are indexed in `docs/research-tools.ko.md`.
- A periodic top-ladder replay monitor is **feasible but not implemented**. Kaggle leaderboard gives team IDs while `EpisodeService/ListEpisodes` needs submission IDs. Resolve them incrementally from the `teams` + `submissions` + agent rows returned by one or more known active submission episode graphs. Do not assume the newest submission is the team's displayed/highest-scoring one. Polling is near-real-time, not push/true real-time.
- Replay classification must report confidence: exact source + 720-step reproduction; opening/action fingerprint lineage; behavioural profile only; unknown private policy. Replays can reveal actions, public state, branching correlations and economic profiles, but cannot prove an internal tape/router/planner architecture. Frozen replay evaluation is diagnostic and not a reacting-policy strength estimate.
- `HANDOFF.md` is the only shared worklog. Do not recreate c-working/c-worklog/o-working.
- Every frozen submission candidate must also have a ready-to-upload `.tar.gz` containing only `main.py`. Read it back, verify the member SHA against the exact candidate source, record the archive SHA, and report the absolute path so the owner can submit it directly.

## OWNER RESET 2026-09-19 — c300 research

- Before every experiment, search HANDOFF and the history index. Record the closest prior attempt, what actually ran and its evidence limits, any concrete code/data/validation defect, and what materially changes to justify retrying. A new name or parent alone is not a retry rationale; distinguish untested, no-op, broken and valid negative results.
- Latest owner instruction supersedes historical architecture/naming/parent restrictions: Codex starts at **c300** and autonomously researches, implements and runs local validation toward #1. Reconsider tape, branches, reactive policies and planners; do not presume old code/data/evaluation correct.
- Historical ratings (including 2800 peaks and V48 copies) are dated observations, not current strength. Opponents change; audit evaluation and source identity before choosing a parent.
- Owner permits plausible retries: prior rejection is scoped to the tested implementation/conditions, not an architecture ban. Include current public Kaggle notebooks/discussions in research; check actual code, provenance, publication date and reproducible evidence before adopting claims. Latest index: `reports/c300-public-research-2026-09-19.ko.md`.
- **Single shared worklog: [HANDOFF.md](HANDOFF.md)** for Codex, Claude and every session. The three former C/O logs are merged into its archive sections and deleted; never recreate separate worklogs. Update current status and append to its latest-work section with timestamp and author.
- Current Codex detail: [docs/c300-research.ko.md](docs/c300-research.ko.md). Preserve frozen historical agents/campaigns; new c300+ files are permitted. Do not spend blind 7240–7255 or alter frozen runner contracts. **Latest owner authorization: when improvement is established by validation, Codex submits immediately for live validation and keeps developing toward #1. This supersedes all historical owner-only submission clauses below.** Preserve exact artifact readback, provenance and submission ID; local gains are not proof of #1.
- Conserve tokens/CPU: targeted reads, existing artifacts, small falsifiable audits before broad campaigns; no overlapping campaigns. Historical pending parent decisions do not block the authorized comparison/research.
- **Token workflow (owner, 2026-09-20):** use [research tools](docs/research-tools.ko.md) and `tools/research_ops.py` for bounded history retrieval, progress, verified compact summaries and model subsets. Reuse canonical runners/crawlers; new experiments should primarily add config. Avoid repeating full logs/JSON/source or rewriting common readout glue. Preserve frozen contracts; summarize decisions in HANDOFF only. Token savings are not yet measured.
- Latest owner worker preference (2026-09-21): default **8 CPU workers** after 12-worker contention produced false `candidate_over_one_second` failures for c358/Local Best. New formal validation and Public League batches use 8 unless an already-frozen contract says otherwise; never alter an in-flight contract. Small diagnostic replays may stay sequential. HANDOFF.md remains the sole worklog. Older 12-default statements below are historical.

## Current c312 update (2026-09-19)

- Development baseline is now public v9/4 `state/c312/public_v9_4.py` (bfee70e9), after two fresh native panels vs V49. Read HANDOFF and `reports/c312-public-v9-frontier-and-elite-losses-2026-09-19.ko.md`. No submission candidate. Older parent/rating conclusions below are historical. c313 begins with prior c177–c180 crop-lane contract audit, not an automatic planner takeover.

## STATUS 2026-09-19 07:30 — read `HANDOFF.md` "START HERE" first

- Before proposing or implementing experiments, read [experiment history and lessons](docs/experiment-history-and-lessons.ko.md).
  Match the closest c/o/p-series attempt, its actual status and failure mechanism; state what changed before retrying.
  Historical C/O results and all new work are in `HANDOFF.md`; search its archive sections by candidate ID.
- Entry points: `HANDOFF.md` (START HERE: state board, rules, pending owner decisions) -> `reports/o-index-2026-09-19.ko.md`
  (which artifacts are current vs superseded) -> `reports/o-policy-compare-results-2026-09-19.ko.md` (current conclusions,
  sections 6-8) -> `docs/o-handoff-2026-09-16.ko.md` (chronological detail) -> the method log below (chronological, oldest first
  inside each bullet; statements dated before 09-19 may be superseded).
- Facts that override older text in this file: base19 (the declared champion) rates **~1400 live** (sub 56319267, 38/37 vs <2000
  opponents); our tape line o239_50 rates ~2660 (peak 2754); exact V46 rates ~2430; the public **V48** file
  (`state/o_dev/v48_clearqueue_public.py` = `state/o_dev/p005_v48_exact.py`) is the **development parent candidate** (head-to-head
  on two seed sets: V47 16-0, V46 16-0, o239_50 12-4, base19 14-2; live copies 2560-2760) but its live level equals our tape line and
  it wins only ~30% vs the 2750+ cluster. **No submission candidate exists**; blind 7240-7255 untouched; p004 (V46) superseded.
- Owner decisions pending: planner line keep/hold/close; parent V48 vs our tape; first concrete-loss target (2750+ cluster).
- Evaluation rule learned on 09-19: the 12-opponent panel saturates above .9; rank top policies with
  `configs/validation/policy_h2h_v2.json`-style head-to-head among live-verified strong sources plus live records
  (`o_tools/live_episodes.py`, `o_tools/rival_source_trace.py --verify`). Local win rate is not live proof.
- Execution: since 2026-09-18 21:12 the owner delegated local campaign execution to Claude (8 workers, one campaign at a time);
  Kaggle submission remains owner-only.

## Project goal and direction (2026-09-17, set by the owner; the METHOD premise below is under owner review since 09-19 — see STATUS)

- **Goal: #1 on the Kaggriculture leaderboard within two weeks (by ~2026-10-01).** Rank
  defense and tape maintenance are no longer objectives; do not spend slots or CPU on them
  unless the owner asks.
- **Method: the planner (state-driven) line, judged by behaviour, not by label (owner, 2026-09-18 night).**
  The old premise "all strong opponents are pure planners" is WITHDRAWN: the public top builds and
  the dominant live builds are TAPE ROUTERS (Tschinkel's Public State Router, yhay81 fieldbook
  derivatives; `reports/o-live-source-trace-2026-09-18.ko.md`) - fixed action streams with
  conditional branches at fixed turns on shops/prices. Classify any policy (ours or a rival's) by
  what it actually does: (1) which information it reacts to, (2) when it changes a decision,
  (3) how stably it executes the repeated daily operations, (4) which opponents it therefore beats.
  A base operating plan combined with conditional branches is a fully valid candidate structure.
  Our own tape lineage (c1xx/o2xx) remains capped at ~2750-2800 with every overlay measured zero or
  negative against reacting opponents, so those files stay opponents/baselines; new work continues
  on the p-series body, which may itself adopt plan+branch structure.
- **Naming:** planner candidates are `p000, p001, ...` (`agent/p0xx_<name>.py`, side copies in
  `state/o_dev/p0xx_*.py`, eval labels `p0xx_sel` / `p0xx_hold`). `c*` (Codex) and `o*`
  (Claude) prefixes remain for tape-era files; do not create new tape candidates.
- **Body to build on (historical, 09-18; superseded pending the owner's 09-19 decision — the planner is ~1400 live, parent candidate is the V48 file):** `agent/p000_planner.py` (base19, 09-18 09:58 = base18 + `vrp_h23`: the VRP time budget is 24-hour steps (the h23 step is real; the old 23-hour
  budget idled the whole crew at h23 and killed every h22 planting) and no planting at h23 - own +2.0/+2.4/+2.0k, margin +2.6/+2.8/+1.9k (pooled +2.46k, 11 se, 9/96 worse),
  wins +8/96, blind 7224-7239 margin +2.1k / own +2.2k; base18, 09-18 09:47 = base17 + `car_wf`: carrots harvested after the age-3 watering (2.0 -> 2.8 units/harvest; from the
  leader gap decomposition `o_tools/leader_gap.py`) - own +0.8/+1.5/+1.5k, margin +0.8/+1.7/+1.9k (pooled +1.46k, 8 se, 7/96 worse), wins +6/96, blind 7208-7223 margin +2.2k / own +1.9k;
  base17, 09-18 04:50 = base16 + oracle-derived conditional rule: strawberry cap +8 while the known shops
  include a berry shop and no pizza/yarn shop and at most one smoothie shop - margin +0.7/+1.3/+1.3k (pooled +1.1k, 4.5 se), blind 7192-7207 +1.2k,
  own ~0, wins +5/96; base16, 09-18 00:30 = base15 + opening bundle from `o_tools/open_search.py`: d0 = 2 cows, 3 sheep,
  3 feed wheat, 7 melons (melons0 8, reserve 5), 6 wheat seeds, 3rd quadrant from d9 - margin +1.5/+1.6/+1.6k (pooled +1.56k, 8 se), blind 7176-7191
  +2.5k, own -0.5..-1.2k (margin-first); base15, 09-17 19:20 = base14 + no wheat fertilizer dose on d9-19 + sell buffer 1 (milk/wool):
  margin +1.07/+1.26/+1.74k (pooled +1.36k, 9.8 se, 10/96 worse), own -0.07k, blind 7128-7143 margin +1.95k / own +0.2k, vs V46 +1.3k;
  base14, 09-17 18:45 = base13 + land3 8 + wheat_units 3, the first **margin-first** promotion:
  own cash neutral (+0.05/-0.2/-0.1k), margin vs o227 +2.0/+1.9/+2.5k (pooled +2.1k, 10 se, 8/96 worse), blind 7112-7127 margin +3.3k /
  own +1.2k, vs V46 margin +1.7k; base13, 09-17 17:50 = base12 + bundle {seed_last 26 (wheat seeds through d26), carrot_hold
  (carrot hinge: hold to d26 where shop demand >= 18/day), yarn2 with 3 yarn stores}: pooled +1.05k (se .17, 3/96 worse), blind 7096-7111 +1.59k
  0/32 worse - a sub-threshold bundle promoted under the bundle clause; base12, 09-17 resume = base11 + **melon dawn rush** `sw_melon_rush` (d10: water->harvest
  pr -1, one melon tile per worker, straight to the shed, same-step sale; with the herd kept in the shed ring our melons sit at distance 2-4 and sell at h6/h9/h10, ahead of most of the tapes' h9-15 dump;
  own +1.8/+2.2/+1.8k, blind 7080-95 +1.5k, margin vs o227 +4.3~4.8k) + vrp_pr 4 / vrp_w 2.0; base11, 09-19 = **VRP dispatcher** `sw_vrp` (per-step cheapest-insertion
  routes for all workers, no zones/feeders) + tomato hinge rule + capacity knobs {straw 40, buf 4, wheat_units 4, room_f 0.4,
  sheep_plus 1, land3 7, cap 9/6, prw 6} + switches egg, carrot2, herd_block, hire_first, feed_stock, bank_pm, melon_water,
  melon_bank, collect_here, d28_feed, shed_cap, horizon, reserve, herd_split, opp_supply = market-room caps net of the
  rival's measured supply via `Proxy.track_market`). Every new behaviour goes behind a `_SW('name')`
  switch (default off; `_SW_DEFAULT_ON` = the baseline) so `o_tools/p_search.py` can search it;
  `agent/opp_planner_proxy.py` is the frozen base3 reference. Diagnostics: `o_tools/income_audit.py`
  (exact per-product ledger + shed discards, both seats), `o_tools/herd_audit.py` (feeding/care rate, layout),
  `o_tools/straw_audit.py`; read `HANDOFF.md` 09-18 entries for the measured gap decomposition
  and the rejected switches (herd_block, melon_d9, melon_open, hire_res, radial, bank_cut, herd_first, herd_angle, land4, straw_open, fert_buy, carrot, sweep).
  **Live audit + current-population pool (09-18 18:50-19:00):** `o_tools/live_replay_audit.py --sub <id> --agent <file> --fetch` replays our own live
  episodes with the rival frozen and diffs every local action against the server record: base19 sub 56319267 = 62/62 games step-identical (no timeout/exception/
  version drift; actTimeout is 1 s). The tapes have NO economic edge over reactive forks in pinned worlds (o227/o239 vs V46 12/32, vs K0006 10/32; base19 14/32, 14/32)
  - their live edge is only the exact0 collapse. `o_replays/live_frozen/live_b19/` (117 rivals from our base17/19 live games; `elite_pool.py --dir o_replays/live_frozen
  --teams live_b19 --us Taeyang`) is the closest thing to a live-weighted arena: rivals are tape-like builds (frozen final 91.7k vs recorded 91.9k), the dominant
  build "B13/S8-S9" (30/117) has d12 = 17 animals/33 strawberries/20 wheat, d24 wheat 37. base19 76/117; MX2 80/117 (own +2.45k, margin +2.04k, 14 se, 5 worse);
  mirror 85/117 (margin +1.4k, bimodal: 14 collapses of +20-29k, 5 games -13..-21k); both 89/117.
  **p001 axis 1 - Adaptive Market Executor V2 `sw_mx2` (09-18 16:30-17:26, off):** per-product (mx2_items STRAWBERRY/MILK/WOOL) hourly plan: rival hour-of-day
  profile (opp_hour EMA in track_market) + symmetric-production prior (our morning stock, afternoon x1.5) -> expected inventory at the post-tick sale hours
  1/5/9/13/17/21 and now; the stock is water-filled over those hours and the current hour's share is sold; h21 / melon-rush day / shed room (100-8) liquidate.
  Measured with `o_tools/mx_eval.py` (V46/K0006/v48 32 games + frozen MG/Majkel 40 each, paired vs base19; our rev / opp rev / margin / flips): wool +0.46/+0.11/+0.36k,
  milk +0.70/+0.27/+0.44k, strawberry +0.67/+0.25/+0.43k, milk+straw +1.32/+0.59/+0.75k, all three +1.93/+0.73/**+1.21k** (11.2 se, K0006 +2.56k, V46 +0.13k, v48 +1.36k,
  MG +0.94k, Majkel +1.16k, flips +2); o227 3 sets own +1.2/+1.3/+1.8k, margin +0.3/+0.2/+0.6k (wins +2/96); $/unit +3-5 for us, +1-3 for the rival. Variants
  (margin weight mx2_w 2, last slot 13, held-stock decoupling from the herd/strawberry caps, cash floor) do not beat it. Total consumption is fixed, so timing
  mostly redistributes: a +1k-class mechanism, below the owner's +3k bar - not promoted.
  **p001_mx2 FROZEN (09-18 19:11):** `agent/p001_mx2.py` = base19 body + `mx2` default-on (sha 448d6115...46331, manifest `state/o_dev/p001_mx2.manifest.json`);
  champion stays base19; evidence `reports/o-p001-mx2-evidence-2026-09-18.ko.md`; arena config `configs/validation/live_weighted_arena_v1_p001mx2.json` (prepared,
  320 games, NOT run) with rules R1-R5 fixed in `reports/o-p001-mx2-arena-plan-2026-09-18.ko.md` and readout `o_tools/arena_report.py`. Any change after the freeze = p002+.
  **Live population source (09-18 19:54, `o_tools/rival_source_trace.py`, `reports/o-live-source-trace-2026-09-18.ko.md`):** the "B13/S8-S9" builds are PUBLIC-NOTEBOOK
  TAPE ROUTERS - Thomas Tschinkel's Public State Router v3.1/v5/v5.5 (router v5 = `state/o_dev/datasets/donor_agents/agents/tschinkel-router-v5.py`, reproduced a live
  game 720/720 steps) and yhay81's ShopForge Fieldbook derivatives (flexonafft, boatlee v29, prvsiyan round-trip variants); they branch only at fixed turns on shops/prices.
  base19 loses to router v5 (3/7), round-trip-N variants (7/17), V4x lineage (2/7). Neither router v5 nor the fieldbook lineage (34% of live games) is in arena v1.
  **Throughput audit (09-18 20:10, `o_tools/throughput_audit.py`, `reports/o-throughput-2026-09-18.ko.md`):** vs the 53 tape-router games our labour is NOT the
  bottleneck (hands re-hired daily at fib cost; idle 1,433 vs 557 unit-hours mostly d1-d9; moves/harvest 6.2 vs 6.8 in our favour; failed actions 5 vs 53). The gap is
  herd scale: cows 8.1 vs 6.3, animals 16.6 vs 13.7 -> milk -6.2k, fertiliser -6.9k, net wheat -5.1k, offset by tomato/carrot/egg +15.7k. land4 -3k = $4,000 land vs
  +92 units. Single proposed next candidate: p002 cash-gated herd ramp (owner decision; F's fixed herd floors lost -9.1k/-5.9k, +1k stop rule applies).
  **p002_cow1 IMPLEMENTED + FROZEN (09-18 20:35, owner-scoped: ONE conditional extra cow):** `sw_cow1` in the body (default off; `Proxy.cow1_offer`:
  window d6-16, paid from the cash left after every planned purchase, gated by cash reserve / no cash-blocked planned purchase / free tile / milk price
  after the herd's + the cow's units net of the rival's measured supply >= 100 / conservative payback >= 200; telemetry via `agent.telemetry`, P002_DEBUG=1).
  Files `agent/p002_cow1.py` (f1ca4735...) and `agent/p002_cow1_mx2.py` (88991c8e..., MX2 also on), manifest `state/o_dev/p002_cow1.manifest.json`.
  Identity: body with cow1 off == base19 snapshot, body + sw_mx2 == p001_mx2 (4/4 games each). Evaluation designed and frozen before any run in
  `reports/o-p002-panel-plan-2026-09-18.ko.md`: four-way separation base19 / +MX2 / +p002 / +MX2+p002 on (a) the live-lineage reacting panel
  `configs/validation/live_lineage_panel_v1.json` (router v5/v3.1, boatlee v29, prvsiyan q45, v48, V46; rules L1-L4; prepared 384 games, none run),
  (b) mx_eval ledgers incl. `router_v5` (`o_tools/p002_report.py`: trigger rate, buy days, block reasons, extra milk/fertiliser income, cow/feed/hire
  cost, displaced production, rival income, flips, bought-vs-not split), (c) the frozen live pool by lineage (`o_tools/lineage_report.py`, fieldbook
  lineage judged only here). `o_tools/arena_hashcheck.py` records candidate/opponent/engine/config hashes before and after each campaign. The owner runs.
  **RESULTS (09-18 21:12-22:20, execution delegated to Claude; `reports/o-final-verdict-2026-09-18.ko.md`):** arena v1b/v1c (execution fixes only:
  dmitrii single-file bundle, o227 telemetry wrapper - behaviour-equal) - MX2 screen PASS, confirm PASS, **final R2 FAIL** (V46 W->L 2/0, shop-router-v5
  2/1, all in world 44142014) while own/margin were positive in every set (final +1,389/+992; B 208 games +1,953/+1,367 W->L 0; lineage panel margin
  +2,085, router_tschinkel +3,240, W->L 0; frozen 117 +2,039). Win rate never moved significantly (point delta +0.006..+0.037, CI incl. 0; V46 0/16 for
  every model). -> **MX2 on hold, no submission recommendation, base19 stays champion; blind 7240-7255 untouched.** p002: B own -1,487 / margin -115 /
  W->L 2 (milk +18u but +$48: herd price 129->117; fertiliser $23/u; other products -534), panel own -2,281 / margin -1,294 / W->L 11, frozen -114 ->
  **discarded**, combo discarded (negative increment on MX2), p003 not started, herd-expansion line closed. Next single target: the V46-type hard
  fork loss mechanism (base19 arena -3.9k, panel 0/16).
  Smoke ledger audit (20:56, `reports/o-p002-smoke-audit-2026-09-18.ko.md`): the BUY succeeds and the +1 cow persists to the end (not an acceleration), but
  the new cow's 22-27 units became only +8 herd units in 7000 (morning feeding/care capacity binds: other cows lose feeds), milk REVENUE did not rise
  (-963 with +8u; +475 for +30u at $16/u in the shallow market), feed spend rose 2-3x the naive estimate; own -1,904/-651, rival -2,135/-2,270, margin
  +231/+1,619 (2 games, not a verdict). Design limits (not bugs): no tile-position/feeding-window check, care bonus ignored (units x3 under), price
  optimistic before the rival's milk history exists, fertiliser counted as all-sold; potential defect: cow1_done is set on order emission (a failed BUY
  would not retry). All fixes go to p003+, the frozen p002 stays.
  **V46 line (09-18 22:20-22:59, `reports/o-p003-hypothesis-2026-09-18.ko.md`, `o_tools/pair_trace.py`):** base19 vs exact V46 (7000-7031 x 2 seats) margin -2,247,
  24/64 wins, bimodal by world (berry/milk worlds lost by -12k: wheat net -230u, milk -37u, fertiliser -133u; pizza/pet/yarn worlds won by +8.7k). Same-date
  cause: our early capital is TILE-bound (Q1 full on d3 = 12 melons + 5 animals + 8 strawberries; Q2 full by d9), V46 skips early strawberries and has 4 cows by
  d3, Q3 d11, 33 strawberries, wheat 24-38, Q4 in 31%. Tested and REJECTED this session: `sw_feedrot` (early feed-wheat rotation d3-11: feed -33% only,
  strawberries displaced, own -195 / margin -3,759 / W->L 4), `land3=10` (own -419 / margin -1,349: the d9 cash sits unused, tiles are the gate),
  `sw_mx2c0` (no effect). MX2's tail loss (world 44142014) = its spread selling restores the rival's wool/berry prices that base19's h1 dump destroys
  (market denial). Verdict: no valid intervention with a new mechanism; base19 stays.
  **V46 decision points (09-19 04:00-04:45, `reports/o-v46-decision-points-2026-09-19.ko.md`):** the only price-gated V46 branches are the d9 cow swap
  (MILK>=WOOL, 9/32 worlds), the d12 six-sheep SE commitment (WOOL>=220 & WHEAT<=45, 2/32), the d18 tomato investment (TOMATO>=70, 9/32), the economic feed
  skip (locally optimal for V46) and the d12-28 input planner (fertiliser price); mirror/clone/similarity/cash-probe gates are identity-bound (diagnostic only);
  tape purchases are price-sensitive only for wheat/fertiliser (flat curves); failed orders are never retried; observation lag 1 step. Reachability from the
  trace (engine price curve vs our stock at the gate): D2 needs 32-68 wool units at d11 h23 vs 12 held, D3 needs 29-155 tomatoes vs 0, D1 8-44 milk vs 6-12
  (2/9 worlds). Layer-ablation upper bounds (same world/seat, diagnostic wrappers `state/o_dev/opponents/v46_ablate_*.py`, NOT opponent models): D2 margin
  +3.9..+9.3k (7030: V46's own investment hurts V46 too and costs us -12..-16k via the wool price), D1 +1.9k (milk price), D3 +0.6k, D5 +0.36k. Verdict:
  no valid intervention executable from observable information; nothing implemented (p004 unused), base19 stays.
  **Whole-policy comparison (09-19 04:50-05:40, `reports/o-policy-compare-{plan,results}-2026-09-19.ko.md`, `configs/validation/policy_compare_v1.json`):**
  base19, exact V46 (`state/o_dev/v46_public.py`) and the live-verified Tschinkel router v5 run VERBATIM in our seat against one fixed reacting panel
  (12 executing opponents / 8 equal-weight families, candidate sources excluded, both seats, new seeds RNG 20260919). Point rates screen/confirm/final:
  base19 .42/.49/.49, V46 .91/.94/.92, router v5 .40/.44/.40. V46 vs base19 family-weighted point delta +0.47/+0.50/+0.42 (all CIs > 0), 8/8 families >= 0,
  L->W 97/92/179 vs W->L 4/5/15, zero margins < -10k (base19 41/27/53), every world flag; router v5 fails every stage. Head-to-head: V46 12-4 vs base19,
  15-1 vs router. Ex-post best-of-3 oracle over V46 alone = +0.021 (no policy router). VERDICT: the alternative parent's superiority holds in the separate
  confirmation -> development parent candidate = the V46 policy FILE (not "tapes are better": router v5 loses). p004 = byte-identical frozen copy
  (`agent/p004_v46_exact.py` = `state/o_dev/p004_v46_exact.py`, manifest `state/o_dev/p004_v46_exact.manifest.json`); base19 stays the official champion
  until the owner decides; blind 7240-7255 untouched; submitting a verbatim public source is the owner's decision. Flags: V46's race/probe detection fires in
  nearly every game vs tape-lineage opponents (its sale pre-emption is part of the measured strength); weakest cells o227-stealth .50-.62 and K0006 .75-1.00.
  Next development (p005+) starts from one concrete loss of this parent, not from grafting features onto base19.
  **Live check + V47/V48 (09-19 05:50-07:10, results report sections 6-8):** the panel does NOT represent the live top band: identical-bytes V46 rates
  ~2430 live (2/23/16 vs newer same-opening versions), base19 ~1400 (38/37 vs <2000 opponents), router v5 ~1440, our tape o239_50 ~2660 (peak 2754).
  p004 is therefore NOT a submission candidate. The author's V47 (public score 2686) and V48 ("clear the queue") were pulled with owner permission
  (`state/o_dev/v47_public.py`, `state/o_dev/v48_clearqueue_public.py`, notebook-pinned digests; 3+6 live copies verified by 720-step replay). The
  12-opponent panel SATURATES above .9 (V46 .906 / V47 .938 / V48 .938, P1 useless); the 5-policy head-to-head on two seed sets orders
  V48 > V47 > o239_50 > V46 > base19 (V48: V47 16-0, V46 16-0, o239_50 12-4). Live V48 copies sit at 2560-2760 and win only ~30% vs 2750+.
  DECISION: development parent candidate = the V48 file (record `state/o_dev/p005_v48_exact.py` + manifest; p004 superseded); not a submission
  candidate; #1 requires beating the 2750+ cluster (private round-trip tape variants / private planners, frozen replays only) - the next concrete
  loss target. Our tape line remains a live-equal alternative parent (owner's choice). Rule learned: rank top policies by head-to-head among
  live-verified strong sources + live copy records, not by the saturated panel.
  **p001 axis 2 - Late Wheat Volume Engine `sw_lwe` (09-18 17:00-17:23, off) REJECTED:** d18-26 empties are 3-5 far corner tiles the nearest-first VRP starves
  (planting them costs 90 steps/cycle; forcing it drops window waterings: wheat 441 -> 398-425 u). Engine fact: base19's age-2 wheat dose (pr 3) lands after the
  tile's must-watering (+1 instead of +2) and the dosed plant is cut at age 3 with 3 units (wheat_units 3), so the ~70 late doses are nearly worthless; dose-before-water
  + no age-3 cut gives 5.0 u/harvest and +59 wheat units, but the fertiliser/labour/tile-days come out of tomatoes (-6 u), carrots (-12 u) and fertiliser sales:
  own -0.4k, margin -0.4k (pr 1.5 dose: no doses executed; guard alone -0.7k; lwe_d0 14 -2.0k). seed_last 27 / nwf_d 18 / seed_ahead+replant +-0.5k; vrp_2opt 0; land4 -3.0k.
  **base20-F (09-18 14:30-15:05, owner's coherent fork-economy design) REJECTED on gate 1:** `sw_fmode` (default off, base19 identity kept; knobs fm_*) = fork
  skeleton (2C2S, 12 d0 melons, wheat on the rest, 5 hands) + early herd + demand-proportional targets + wheat floor + carrot tile cap + wheat doses d10+ + pocket banking.
  F1 (separate `fmode_pri`) own -10.7k on the fork pool; F2/F3 (flags inside the base19 flow) -12.3k -> -4.8k; with base19's own d0 the F rest is -2.8k. Ablation (v37, own/opp):
  12-melon/2-sheep d0 = own +1.4k but rival +6.0k (one sheep less -> rival wool +3.2k, fertiliser +1.4k, milk +1.35k; d9 cash $4 -> 3 hands on the rush day), MG-like herd
  floors (6C5S2G d9 / 7-6-3 d12) own -9.1k vs v37 and -5.9k vs frozen MG/Majkel (their 17 animals already fill milk/wool), carrot cap -0.6k, wheat doses d10-19 own 0
  (fertiliser sale -> rival +1.5k), replant 0, 5 hands 0. Frozen-MG 16-world decomposition (`fkpi2.py`): MG +18k over base19 = late wheat +6.9k (30 tiles at d24, no feed
  buys), herd +10k, 12 melons +2.4k, strawberries ~0 - but these are MG's share when WE are the smaller supplier, not ours to take by supplying more (fixed market
  absorption, first-come). The frozen pool inflates the elite by +10-17k (no reaction); use it only paired.
  Small real findings: `sell_h=9,sell_h_items=STRAWBERRY/MILK/WOOL/EGG` (sell after the h0/h4/h8 consumption ticks: town eats every 4 steps after the market) own
  +1.0-1.5k on every pool, margin +0.7k forks/elite, 0 vs o227, wins unchanged - held as a base20 bundle ingredient; `fm_bank` (pocket >= $1000 of product within 5 tiles
  banks first; the d6 wool otherwise sells d7) +0.3k own.
  **Opening mirror (09-18 15:20-15:48, mechanism found):** `sw_t0war=1,t0_q1=13,t0_q2=10,w0feed=-7,t0_s1=S13/B5,d0_res=60` prepends o227's d0 h0 [B13,B10,S30] + h1
  [S13,B5] to the planner's orders: vs v37 own +32k / margin +46k / **96 of 96 wins** (v37 = the live 'exact0' script [B13,B30,S30]/[S13,B5], 21% of live opponents at
  ~2400 with d0-end cash 0; same-index lockstep buys/sells cost it ~$15 -> $0 at d0 end -> d1 HIRE fails -> collapse); tax: o227 own -0.5k / margin -0.9k (wins -2/96),
  V46 own -0.4k / margin -2.4k, K0006 -0.1k / -1.5k (their +1.5-2.4k comes from the $60 d0 reserve: unfed d0 animals lose a care-bonus unit), frozen MG 0. Without the
  reserve our own d0 feed fails vs o227-like scripts (-7.6k own, 0/32). The live 2650 cluster ([B5,B10,S60]/[S13,B5], 35%, d0 cash 29) is immune. Diverse pool
  (49 public agents x 8 games, `$TEMP/dpool.sh`): own +5.8k, margin +8.3k, wins 276->320/392, no flip against us. Convenience switch `sw_mirror=1` (off).
  **base20 candidate = base19 + sw_mirror; promotion is the owner's call** (fragile to the dollar; blind 7240-7255 unused).
  Rejected on base19 (09-18 afternoon, owner's 5-axis brief): Majkel d0 split (w0seed 9-11 with melons0 6 / w0feed 0-1 / straw_early 4 / nwf_lo 0: margin -0.7..-3.2k; the
  25-tile NW quadrant makes a d0 wheat tile cost a dawn-rush melon or a first-come strawberry), feed_alt (0), place_pr -1 (-0.75k), vrp_persist (-18k, broken), bank_am
  morning berry banking (-0.4..-2.2k), melon_water10 0 (-0.5k), rush_all (3 sets +0.3k), rush_ring 2/3 +- place_pr (-2.7..-12.8k: far herd -> d1-2 feeding misses -> escapes),
  t0war (-0.8k), dump0, adaptive dump/pace policy (perfect-information oracle value 0: dumping beats pacing against both o227 and the pacer model). Tools from this round:
  o_tools/cash_trace.py (hourly leader-vs-us cash/orders, --agg), o_tools/cash_shadow.py (+$X at day:hour -> final deltas; d2-4 x6-8, d9 x9, d0-1 ~0, d10+ x1),
  o_tools/sell_hist.py (per-unit sales by product/hour via the engine commit hook).
  Rejected on base19 (09-18 midday, sel screens unless noted): EC2 crop controller `sw_ec2` (3 sets -0.8k/-0.2k), land4 d12/14/16 (-2.3..-3.9k: 25 tiles gave +70 wheat units,
  half the quadrant stayed empty; +2 hands did not help), hands_cap 9/10/12/13 (-6.1/-1.1/-0.4/-3.0k), herd +N of any kind (room_f 0.5 -2.2k, herd_min 12 -4.3k, anim3 -1.1k,
  cow5 -2.7k, geese +1/+2 margin -0.2/-1.5k), tape-like 12 d0 melons with 2 sheep (-9.5k: the rush handles ~7 melons and the missing sheep's wool/fertilizer lifts the tape),
  wheat6 (own +1.5k, margin -0.7k), nwf_d 10/14, fert_buy, wheat_units 4 (-1.7k), seed_last 27 + last-day harvest (0), carrot rotation -2 (0), tom_sell 27/28 (+0.3k own, 0 margin),
  dump0 (h0 dumping, -0.4k), vrp_len 20 (+0.4k), vrp_bal 2.0 / vrp_min 10 (-3.4/-3.9k), opening re-search open3 (best sel +1.2k failed hold). Kept as off switches with small
  consistent own gains (margin n.s.): `hire0` (+0.5k own), `seed_ahead` + `replant` (+0.7k own, empty tiles to leader level), `tom_f6`; bundle of the four: own +0.95k, margin +0.4k.
  Rejected on base12 (09-17, sets vs o227 with margins): cow5 (early cows, -2.2k), hands_cap 12/13 (-1.8k/-5.6k), land4 (-4.3k),
  rush_ring (herd behind the melon ring), rush_all, melon_open/cows0 1, fert_zero(+buy-back), wsell, price_hold (own +0.4k, rival +2.2k),
  egg0/egg1-3 up, straw_f 0.6-1.0 (strawberry glut: own -1.5..-4k, margin +2.5k only in 2-strawberry-shop worlds, -10k in tomato worlds),
  yarn2 with 2 stores (7030 -17k). carrot_hold and yarn2 (3 stores) went into the base13 bundle with seed_last 26; fert_h0 (+160 sel, not additive on hold),
  tom_sell 25/27, term_d 29, hands_d29, straw_last 16/18 stay off.
- **Judgement rule:** pinned-world evaluation vs `agent/o227_stealth_drop.py`,
  selection seeds 7000-7015 and holdout 7016-7031, 32 games each, paired via
  `o_tools/proxy_pair.py --side b base19_sel|base19_hold|base19_fresh <label>` and `o_tools/margin_pair.py --base base19 --cand <label>` (fresh = seeds 7032-7047); pass = all
  three sets >= +1,500 (>= 2 se), <= 10/32 worse, no bucket collapse. Selection-set winners of a search were
  pure noise until confirmed (09-18): never merge on one set. Never judge on mirror (proxy-vs-proxy) cash,
  on a single seed, or on the unpinned 32-seed pool (shop draws change with any behaviour
  change). **Seed roles (09-19 amendment):** 7000-7015 = selection (search objective), 7016-7031 = second selection
  (the search's automatic confirmations query it repeatedly, so it is not a clean holdout), 7032-7047 = third tuning set
  (already queried 30+ times). A promotion therefore also needs a **blind block, looked at exactly once after the candidate
  is frozen**: 7048-7063 for base10 (passed: +3.4k, se .8, 6 worse/23 better vs base9), 7064-7079 for base11 (passed +2.3k), 7080-7095 for base12 (passed +1.5k, 0/32 worse), 7096-7111 for base13 (passed +1.6k, 0/32 worse), 7112-7127 for base14 (margin +3.3k), 7128-7143 for base15 (margin +1.9k), 7144-7175 used for the day total, 7176-7191 for base16 (margin +2.5k), 7192-7207 for base17 (margin +1.2k), 7208-7223 for base18 (margin +2.2k), 7224-7239 for base19 (margin +2.1k), then 7240-7255, ... one
  fresh block per promotion; if the candidate is modified after the blind look, verify again on the next block. The
  search board's PASS lines are intermediate only. **Conditional (world-adaptive) rules** are judged with `o_tools/cond_pair.py` on the pooled 96 games:
  untouched worlds must be bit-identical, pooled gain >= +1,500 with >= 4 se, every set >= +500, <= 10% worse
  games, and the gain monotone in the triggering shop feature (09-19 amendment; base9 = tomato rule passed this way).
  **Margin-first rule (09-17 18:00, owner goal = #1, i.e. wins; announced in the 17:00/18:00 reports, not yet explicitly confirmed):** a
  candidate may also be promoted on the paired margin (own minus o227 cash, `o_tools/margin_pair.py`): pooled 96-game margin >= +1,500
  with >= 4 se, each set >= +500, <= 10% worse games, own cash >= -1,000 on every set, blind block margin >= +1,000 with <= 4 worse,
  and no loss of wins vs V46/K0006. Rationale: the ladder scores wins, and against the tape lineage every unit we add to a shared market
  costs the rival more than us (base14 = land3 8 + wheat_units 3). Glut knobs (straw_f 0.5, sheep_plus 2, buf 2) add margin (+1-2k) but
  not wins and cost own cash with high variance - kept off. Day total (09-17, fresh seeds 7144-7175, 64 games, base11 -> base15):
  own +3.35k (se .47), o227 -5.64k, margin +8.99k (se .54, 0 worse), wins 0 -> 6/64. (Seeds 7144-7175 are therefore used; the
  next unused blind block is 7176-7191.) **Macro Oracle (09-17 night, `o_tools/oracle.py`):** ex-post best of 5 strategy branches at
  d6/9/12/15/18 = +2.8k margin vs +2.2k for 5 matched meaningless perturbations -> strategic slack ~+0.6k (n.s.), 1-2-day selectors
  recover < 0 -> no runtime Macro-MPC (p001) and no d6+ branch router; remaining structural room = the d0-d12 opening bundle
  (`o_tools/open_search.py`, opening knobs cows0/sheep0/melons0/w0seed/w0feed/d0_res/melons_late/straw_early/cows5/straw_d6/d79/d1012).
- **Milestones:** M1 vs o227 >= 85k -> M2 >= 100k -> M3 win rate >= 60% vs o227 and V44/V45
  (first planner submission) -> daily live loop. Current (base19): 100.2k / 96.0k / 96.8k (sel/hold/fresh; **M1 reached**, wins vs o227 14/12/10 of 32; o227 102-104k;
  mean margin -0.9k / -5.1k / -6.5k; unbiased 64-world block 7300-7363: base17 -9.85k / 14 of 128 wins -> base19 -6.2k (se 0.7) / 25 of 128; vs V46 sel +0.3k (14/32), vs K0006 -1.6k (14/32); on the once-used 64-game block 7144-7175 base16 is -11.2k with 8/64 wins, so M3 is far). Knife-edge warning: the d0-d8 cash is so tight that removing one d2 action
  changed a d2 melon purchase and cost 12k in one world (7042) - keep early-game changes off unless they are the point. From base12 the paired report must also show the margin (own minus o227 cash) and a
  candidate whose margin falls is not promoted even if own cash passes (base11's caps lifted o227 almost as much as us).
  (remaining gap by product at base11, 4 worlds: fertilizer -7.9k (not a collection gap: we collect ~308/game like o227 but
  spend 134 on FERTILIZE; o227 sells early and buys back on demand - the engine quotes buys at the post-buy price, so the
  round-trip is free), melon -6.5k (base12 rush recovers ~4k of it; melons in the ring would sell at h2-h7 but every herd relocation tried (rush_ring, rush_arm) lost more on the d6-d8 build chain than the earlier sale gained, so the herd placement stays), milk -5.8k (cows 3-5
  days later than o227's d2/d3 cows), strawberry -3.7k). A game takes ~15 s: a 16-seed set is 50 s, a 3-set 2.5 min - screen
  variants on sets, not on single games.) Sub-threshold items may be judged as a bundle (base7 = straw 30 +
  feed 4.5; base8 = the p000c search bundle). Lesson (09-19): switches rejected on the old dispatcher (egg, carrot2, herd_block, feed_stock, hire_first, melon_*) all pass on top of the VRP dispatcher's spare labour; re-judge upper-layer rules whenever the executor changes. yarn2 (+6 sheep with 2 yarn stores) overloads feeding: rejected.
- **Documents, in reading order:**
  1. `docs/o-handoff-2026-09-16.ko.md` — consolidated state, gates, confirmed engine facts.
  2. `docs/o-planner-proxy-plan.ko.md` — planner design (5.1 controller), fidelity metrics,
     sections 9-13 progress log; the p000 plan-search design is appended there.
  3. `docs/o-planner-candidate-roadmap.ko.md` — quantitative targets (Majkel curves), work
     order, gates.
  4. `docs/o-planner-parallel-briefs.ko.md` — work packages, common rules, **rejected list
     (do not retry)**, 2.5 market-capacity table.
  5. `HANDOFF.md` — chronological 1-2 line log; append your own entries there.
- **Do not:** submit to Kaggle (the owner submits), edit `agent/c*.py`/`agent/o2*.py`, run
  `git reset --hard`, or run more than one 8-worker evaluation at a time (16 cores; parallel
  sessions starve each other).

## Start of task

1. Read this file, the current top section of `HANDOFF.md` (first ~70 lines), and the relevant entries in `docs/experiment-history-and-lessons.ko.md` before proposing experiments. Search HANDOFF archive sections by candidate ID; do not dump the full merged history every turn.
2. Run `git status --short --branch`, recent log, and remotes before edits.
3. Inspect relevant `state/parallel-handoffs/` reports before duplicating work.
4. Prefer current repository and live evidence over chat memory.

## Repository safety

- MAIN is intentionally dirty with many competition artifacts. Preserve all
  unrelated changes and frozen results.
- Never reset, clean, stash, rebase, mass-stage, overwrite, or delete user work.
- Do not recreate sibling worktrees unless a new parallel task explicitly needs
  isolation. Discover any worktrees with `git worktree list`.
- Local colleague handoffs under `state/parallel-handoffs/` are ignored coordination
  state and must not be committed.
- Keep source parents, manifests, job lists, engine hashes, observed failures, and
  rejected results immutable. Create a new candidate/experiment folder for changes.

## Competition workflow

- REUSE FIRST (all Codex/Claude/other agents): before writing validation or helper
  tools, read `docs/reusable-validation.ko.md` and search existing `tools/` and
  `src/kaggriculture_meta/` capabilities. Do not rebuild or copy a per-candidate runner,
  analyzer, process guard, progress bar, cache, or notification implementation.
- Canonical validation: `tools/run-validation.ps1`, `tools/validation_v1.py`, and
  `tools/validation_stats_v1.py`. New evaluations normally add only a JSON config under
  `configs/validation/` and a separate output directory. Use Prepare/Check/Run/Analyze
  and screen/confirm/final; never silently restart an existing campaign.
- If a required capability is missing, document the concrete gap and reuse search,
  then implement the smallest reusable extension or separate mechanism diagnostic.
  Do not duplicate the evaluation framework. Preserve frozen runner/support hashes;
  behavior-changing framework updates require a new version and paired contract.
- Implementation-only assignments end with code/artifact handoff. (Historical execution rule:
  the user ran the commands. Since 2026-09-18 21:12 the owner delegated local campaign execution
  to Claude — prepare, hash-check, run, report — one campaign at a time; Kaggle submission stays owner-only.)

- The project-specific Kaggle skill was removed at the user's request on 2026-09-14.
  Do not require or recreate it.
- Current execution preference (owner, 2026-09-18 21:12): Claude runs local simulations and
  campaigns itself and reports results; judgement rules are fixed before running. The owner
  still decides promotions, blind use and submissions.
- Worker counts (owner, 2026-09-18 19:45): any task that is even slightly long runs with
  **8 workers by default**; genuinely long jobs (full validation stages, 100+ game pools)
  use **12 workers**. Never exceed 12 and never start overlapping campaigns (16 CPUs;
  leave headroom for the owner's own runs). Note: the canonical runner still validates
  `workers` as 1..8 (`tools/validation_v1.py`, schema check) and its contract hash covers
  the runner source, so arena configs stay at 8 until the owner approves raising that cap;
  the o_tools evaluators (`proxy_eval`, `mx_eval`, `elite_pool`, `live_replay_audit`) take
  `--workers 12` directly.
- Long validation may use 8 (default) or 12 (long) workers, but each match must run in a fresh Python
  subprocess with its own immutable job file, log, and result path. Never evaluate
  multiple games in threads or reuse imported policies, engine monkeypatches, module
  globals, temporary directories, or RNG state across matches.
- Compare baseline and candidate on the same explicit seed, reacting opponent, and
  both seats. Keep development, selection, and final seed sets disjoint, and never let
  parallel chunks read or derive decisions from another chunk's partial results.
- Every user-facing run command must show a progress bar, completed/total, percent,
  elapsed time, throughput-based ETA, cached count, and success/failure desktop
  notification with sound.
- Verify coordinator PID and owned worker tree before claiming a campaign is active
  or stopping it. A lock file alone is insufficient.
- Preserve exact engine/runtime identity. Do not weaken source, replay, job, timing,
  or engine hash checks to make old and new results compare.
- Recorded-action/fixed-shop diagnostics test a mechanism only. They are not reacting
  elite games or evidence of general win rate.
- Promote only after paired seeds, both seats, diverse reacting families, health
  gates, subgroup non-regression, tail checks, and unused final conditions.
- A Kaggle submission requires a validated artifact, exact package/source readback,
  and user authorization already applicable to that submission.

## Collaboration

- Consult existing colleague requests and reports first. MAIN owns integration.
- When colleague work is useful, give a bounded question, evidence paths, completion
  criteria, and write scope. Distinguish prepared, sent, accepted, completed, and
  reviewed states.
- Do not let colleagues mutate shared frozen artifacts or independently spend the
  global simulation budget.

## Current checkpoint (c-series, 2026-09-15 — HISTORICAL; the live state is in STATUS above and HANDOFF.md START HERE)

- 2026-09-15 audit supersedes the c153 promotion narrative below: c153 2383.3,
  c129 2820.3; all 12 downloaded c153 losses had exact c129/c153/server action
  equality. Prior reacting gate was false/inactive, so improvement was not proved.
  Old c153 mechanism threading was unsafe; new per-game subprocess audit confirms
  both mechanisms with exact shops in both modes. Use HANDOFF.md's latest audit.
- Evaluation submission: `agent/c153_urgent_feed_exact1.py`, Kaggle ref `56232526`,
  status `COMPLETE` with initial rating 600.0, SHA-256
  `b31bbbe2f7c0f8ab93dd773cfc441e40e65d23caaf30c29e6ae42c44e25ed383`.
  Its 1,792-game fresh panel was exactly equal to c129 because the repair was
  inactive; two fixed-opponent loss mechanisms improved +5,947/+2,997 margin.
  Keep c129 as live champion until c153 has enough live matches.
- Submitted champion: `agent/c129_feed_liquidity.py`, Kaggle ref `56209242`, SHA-256
  `e9973586cbe2c0bbb034243f3d3e4c9fdcac4fcac432c0de32b0ba0e61f7ca61`.
- Latest local live snapshot has 79 losses: c125 43 and c129 36. See
  `state/agent_experiments/structural_loss_audit79_20260914/summary.json`.
- Strongest unsubmitted diagnostic candidate: `agent/c146_carrot_sched3.py`; 47-tape
  result is 4 improved, 43 same, 0 worse, margin +6352, own cash +1569. It lacks
  reacting generalization evidence and is not champion.
- `agent/c147_feed_commitment.py` is an unvalidated isolated first-feed repair.
  Runtime restoration is required before its frozen campaign can be generated.
- Read `HANDOFF.md` for the current blocker, tuning space, and exact next actions.

## Durable pointers

- Validation contract: `docs/agent-validation-protocol.ko.md`
- Current concise state: `HANDOFF.md` (START HERE section) and `reports/o-index-2026-09-19.ko.md`
- Current conclusions: `reports/o-policy-compare-results-2026-09-19.ko.md`; chronological detail: `docs/o-handoff-2026-09-16.ko.md`; log: `HANDOFF.md`
- Full pre-compaction context: `state/context-archive/20260914-121406/`
- Latest loss audit: `state/agent_experiments/structural_loss_audit79_20260914/`
- Colleague evidence: `state/parallel-handoffs/collaboration-20260914/`
- o/r-series (Claude) validation process, reference only, not mandatory for c-series: `docs/o-validation-process.ko.md`
