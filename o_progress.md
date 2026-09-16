# o-series long-run autonomous campaign — progress log

Baseline: `agent/c150.py` (READ-ONLY, never modified). SHA256 `9713af15...b7d6` at campaign start
(2026-09-14 21:xx). All `c*.py` files are owned by a parallel Codex session — never edited/deleted.
New candidates use `o151`, `o152`, ... numbering, never reused. Kaggle submission explicitly
authorized by the user ("할만큼 진행하면 알아서 캐글에 제출도 해줘", 2026-09-14) once a strong,
validated candidate exists — still gated on passing the arena bar below, not automatic on any change.

## Current O champion — FINAL DECISION: keep submitting plain `c150.py` (no change)

**No o15x candidate this session beat c150 by a validated, robust margin across a diverse
opponent pool.** The full campaign is summarized here; see `o_experiments.jsonl` for every
experiment's raw numbers.

- **o155_open_10_8_25 / o157_combined: REJECTED (do not use, do not submit).** Looked like a clean,
  near-risk-free +20/game win in same-lineage mirror testing (156W/4L/0T over 160 games vs c150;
  also flips the exact c129/c146 ties into reliable wins). A full 46-agent diverse-pool re-check
  (matched seeds against the existing c150 baseline) found this was **catastrophically wrong**:
  10/44 opponents showed a 50,000-88,000 point swing in the opponent's favor, and one
  (`ahmedberatozer-v40-plans-that-fit-the-shops`) flipped from c150 winning by -54216 to the
  *opponent* winning by +1962. Root-caused (see `o155_regression_root_cause` in the ledger): the
  engine's shared-market **lockstep unit-by-unit order interleaving** means even a same-net-quantity
  change to our own step-0 trade composition changes the *opponent's* realized cash by a few
  dollars purely as a side effect of price-curve interleaving — and because most public-lineage
  agents (per the c150 audit) are full of exact/near-exact money-threshold branches, that few-dollar
  difference can flip the opponent onto a completely different 720-step trajectory. **This is the
  single most important lesson of the session**: no isolated, "structurally free" tweak can be
  trusted from mirror-match testing alone in this game; everything must clear the full diverse pool.
- **o153_post_budget_guard_v2: KEEP-NEUTRAL, safe but unproven.** Confirmed byte-for-byte identical
  outcomes to plain c150 across the ENTIRE 44-agent diverse pool (every single opponent's mean
  margin matches to the exact integer) plus all earlier mirror/non-mirror testing (~1,300+ games
  total, zero observed differences). Mathematically risk-free to adopt, but never actually fired in
  any tested game, so it has no demonstrated real-world benefit either — it is unactivated insurance
  against a scenario (overlay-injected purchases exceeding what the route tape itself budgeted) that
  simply didn't occur in this session's testing.
- **o151_telemetry / o156_opponent_classifier**: KEEP as analysis tooling, not strategy candidates
  (both proven behavior-neutral).
- **o152_post_budget_guard / o154_hinge_sell**: REJECTED (see ledger for each's specific root cause).

### Why plain c150 is the right submission right now
Per the user's own explicit criterion ("submit once significantly improved"), nothing this session
cleared that bar. Just as importantly, the c150 **baseline itself was rigorously stress-tested and
held up very well**: undefeated (0 real losses on net margin) against all 44 resolvable, behaviorally
distinct local agents (`o_results/diverse_vs_c150/`, deduplicated from the 52-agent donor dataset
down to genuinely distinct policies via `donors.csv`'s `behaviour_family` clustering), plus the 3
Kaggle-named reference agents (shop-router-reactive-v5, v41-review-candidate, dynamic-route-agent —
all confirmed same-lineage near-mirrors, margin noise only) and the previous local champions
c129/c146 (exact ties). No genuine exploiter was found anywhere in the available local pool. That is
itself a strong, validated result worth reporting even though it isn't a code change.

**Recommendation: do not submit any o15x file to Kaggle this session.** If the user wants to use a
submission slot on a strictly-safe (never worse, unproven-better) hardening, `o153_post_budget_guard_v2.py`
is the only defensible candidate, clearly labeled as "no measured difference from c150, kept as
insurance" rather than "an improvement."

## Baseline arena (c150 vs opponents, 16 seeds x 2 seats = 32 games each, seed-base 9000)
| Opponent | W/L/T (opp perspective) | Margin (opp - c150) |
|---|---|---|
| shop-router-reactive-v5 | 17/15/0 | +432 (near-mirror, noise) |
| v41-review-candidate | 17/15/0 | +420 (near-mirror, noise) |
| dynamic-route-agent | 17/15/0 | +420 (near-mirror, noise) |
| c129 (old c-champion) | 0/0/32 | 0 (exact tie every game — same-family mirror) |
| c146 (old c-champion) | 0/0/32 | 0 (exact tie every game) |
| metacounter-r1 | 0/32/0 | -50746 (c150 crushes) |
| best-market-agent-high-strategy | pending | |
| moon-counts-melons | pending | |

Confirms prior finding: c150/c129/c146/shop-router-v5/v41/dynamic-route are all the same
"route-replay chassis" lineage — mirror matches are noise-level (+/-450 out of ~90k bank).
Full results: `o_results/baseline_c150/_summary.json`.

## c150 structural audit (COMPLETE, 2026-09-14, full-file subagent read of all 3337 lines)

**Architecture**: same chassis+overlay family as c129 but far more heavily stacked — **~24 sequential
`agent = wrapper(agent)` reassignments** (vs c129's handful). Chassis itself (L409-909) is nearly
identical to c129. Everything from ~L940 on diverges.

**Key finding**: Chassis's own native safety layers (`budget_guard, room_guard, clamp_sells,
dead_stock, terminal_liquidation, front_run`) are **ALL disabled** in `_SETTINGS` (L954: only
`hand_align, weed_repair, sell_lead` = True). c150's real safety net is ~20 independent,
individually-try/excepted module-level overlays re-deriving their own view of state, several of
which monkeypatch each other (Python late-binding) rather than using explicit params:

1. `_IMPL` entry guard (L973-979) 2. shop terminal rescue step>=718 (L981-998) 3. physical terminal
planner steps 712-718 (L1009-1104, uses `_PLANNER_NS` E182 planner, engine-extract pinned to
`ENGINE_VERSION="1.32.7"`/`SOURCE_SHA256`) 4. room-guard-v2 hour23 overflow sell (L1109-1136)
5. v28 hard-PASS guard (L1205-1214) 6. **V219 tomato investment** (L1227-1443) 7-8. sales-first
reorder, dead+active variants (L1457-1500) 9. v31 guard (L1502-1515) 10. **V231 cattle<->sheep
substitution** (L1519-1628) 11. **R36 physically-funded sale reservation** (L1633-1714, monkeypatches
`Chassis._sell_lead`/`_apply_suppression`) 12. **R37 mirror-similarity/horizon/quote-reorder**
(L1857-1899) 13. release guard (L1902-1924) 14. **V233 sheep investment** (L1928-2111, monkeypatches
`_shadow_terminal` to abstain if committed) 15. **EXP182 fertilizer/input planner** (L2114-2258,
WHEAT/CARROT only) 16. warehouse-overflow close guard (L2261-2323) 17. labor-assignment telemetry
merge (L2357-2366) 18. LOCAL opening-rescue (L2376-2600) 19. CP0 weed-blocked structure repair
(L2610-2760) 20. **C115** sustained-mirror 12-turn reservation widening (L2772-2877, redefines
`_r36_reserve`) 21. **C116** hardcoded COW->SHEEP anti-mirror route rewrite for one specific
recorded loss signature (L2891-3114) 22. terminal-planner `_proposals`/`dominates`/`plan_terminal`
patches relaxing strict physical dominance to net-positive-value dominance (L3118-3156) 23. **C124**
endgame low-margin FEED abstention (L3167-3230) 24. **C126 feed-buffer pre-funding** (final exported
`agent`, L3337).

**Route table**: `_ROUTES` = 13 routes (id 0-12): one 719-step base tape + 12 diff-patches, all
packed in one base85+zlib blob (L944-953). `_R42_OPENING` (L966-969) overwrites step-0 market to
`[BUY_PRODUCT WHEAT 13, BUY_PRODUCT WHEAT 10, SELL WHEAT 30]` on every route.

**Router** (L956-964): switches ONCE at step>=144 keyed on the first-two-unlocked-shops pair
(15-entry lookup, default route 0), and unconditionally forces route 2 at step>=648. No other
runtime route-switching exists except two *narrow, single-purpose* route-content rewrites:
V231 (COW-for-scheduled-SHEEP swap, steps 216-227) and C116 (COW-for-SHEEP swap, steps 150-157,
gated on an exact recorded-loss action-signature match, NOT gated on the general mirror-similarity
signal).

**Sale reservation**: `_r36_reserve`/`_r36_suppress` (R36, redefined again by C115) pulls forward a
future scheduled SELL to "now" if physically available, tracked as a "debt" against the tape's own
later SELL. Horizon: default 2, ->3/4 under a mirror-similarity streak, ->8 unconditionally for
steps [288,696), ->12 temporarily under C115's stronger mirror-streak condition. **This IS backlog
item H (adaptive sale timing) already implemented**, just gated on mirror-similarity, not on a
general rival-advantage/supply-risk signal.

**Market order priority**: (1) `_v224_sales_first` bubbles SELLs earlier (L1472-1488, active
step>=144); (2) `_r37_reorder_sales`/`_r37_quote_priority` (L1775-1820) re-sorts SELL blocks by
"revenue exposed to a plausible rival dump batch" using the exact engine price replica
`_r37_market_price`/`_R37_MARKET_PARAMS` (L1742-1756) — **this IS a working, partial version of
backlog item A (advantage/scarcity estimator) already in production**, batch-sized from the rival's
*visible* standing ripe yield only (no shed assumption), clamped to [8,24] units.

**Opponent read sites — CONFIRMED SPARSE** (audit item 10, important gap): only 3 functions ever
read rival data in the whole 3337-line file: `_r37_similarity` (tile-by-tile crop/animal match
ratio, mirror-only), `_r37_quote_priority` (rival visible ripe yield for scarcity pricing), and
`_r44_before`/`_r44_after` (rival money, mirror money-parity probe). **`_View.rival` (L387) is
captured every step but never read anywhere else — confirmed dead field.** There is NO general
opponent-classifier, NO general economic-advantage estimator, and NO DEFEND/NEUTRAL/CHASE mode
anywhere in c150 — backlog items A, B, and F are all **genuinely unimplemented gaps**, not
redundant with existing code, unlike H/most of C (see below).

**Crop/livestock investment (backlog K/M) — already substantially implemented, contrary to prior
c129-era assumptions**: V219 (tomato, L1227-1443) and V233 (sheep, L1928-2111) both use
`_r53_labor_assignment` to size worker counts (**labor reallocation, NOT blind extra-hire** — this
is exactly the fix the 2026-09-14 negative-results memory recommended after o003's extra-hire
tomato program lost -29k against c129). V231 (L1519-1628) substitutes COW for a scheduled SHEEP
buy under milk-favorable conditions. **Gap found**: there is no equivalent dedicated CARROT hinge-
demand investment program (EXP182's WHEAT/CARROT logic is only a *fertilizer* planner for tiles
already planted, not a new-planting investment like V219/V233) — CARROT hinge scarcity (documented
in the 79-loss forensics as one of the two largest untapped levers, alongside TOMATO which V219 now
covers) remains a real gap. **-> queued as o155/o156 candidate.**

**Liquidity/commitment guard (backlog C)**: native `_block_requirements`/`_budget_guard` exist but
are disabled; V219/V233 each have their own ad-hoc "budget + 3000 reserve" checks scoped only to
their own commitment. **Tested as o152/o153 below — found to be low-value/redundant with existing
room-guard-v2 and warehouse-close-guard reimplementations**, see Completed experiments.

**Terminal planner (backlog V)**: already very sophisticated — physical-dominance search relaxed to
net-positive-value dominance via a late patch (L3125-3155), strict engine-version/config pinning,
V219/V233 abstention hooks. Per spec's own warning ("don't remove the physical dominance safety
net"), this is now LOW priority to touch further without very strong evidence.

**Dead/inert code found (bug-audit lane, backlog Z)**: `front_run`/`opponent_plan` hook is fully
wired in the Chassis class but never activated (`front_run: False`, `make_agent(...)` called with no
`opponent_plan` argument) — an entire unused capability. `_View.rival` dead field (above). C116's
anti-mirror rewrite is a one-off signature match, not connected to the general `_r37_similarity`
signal that the rest of the file already computes — inconsistent design, possibly a missed
opportunity to generalize a narrow fix.

Full subagent report (line-by-line, all 20 audit questions + call-order diagram) is preserved in
this session's task transcript; summary above captures everything actionable for the backlog.

## Completed experiments (11 total, all built and empirically tested — see `o_experiments.jsonl`)
1. **o151_telemetry**: KEEP (tooling). Behavior-neutral (0/117 mismatches vs c150).
2. **o152_post_budget_guard**: REJECTED. Re-invoking c150's own disabled `chassis._budget_guard`
   post-overlay LOST 10/10 early games (-5k to -10k). Root cause: emptied 2 FERTILIZER units the
   dynamic EXP182 fertilizer planner needed that same turn, turning its FERTILIZE into a no-op.
   **Lesson**: any liquidity guard must exclude live working-input items (FERTILIZER, WHEAT) or
   check overlay-level reservations first.
3. **o153_post_budget_guard_v2**: KEEP-NEUTRAL, fully validated. Same as o152 with FERTILIZER/WHEAT
   excluded. Confirmed byte-for-byte identical to c150 across ~1,300+ games (mirror + all 44 diverse
   opponents) — mathematically risk-free, but never fired in any tested game so no proven upside.
4. **o154_hinge_sell**: REJECTED (no measurable effect). Hypothesis (unserved TOMATO/CARROT hinge
   spikes) turned out to already be solved by V219's unconditional 100%-shed-TOMATO dump once
   committed; trigger fired 0/10 times in testing.
5. **o155_open_10_8_25** (+ 4 sibling grid variants): **REJECTED after a serious near-miss** — see
   below, this is the session's single most important finding.
6. **o156_opponent_classifier**: KEEP (tooling). Behavior-neutral rule-based archetype labeler
   (MIRROR/WOOL_HEAVY/.../UNKNOWN), validated to actually discriminate on a real distinct opponent.
7. **o157_combined** (o155+o153): REJECTED, inherits o155's regression in full (confirmed the guard
   component contributes nothing to the regression — isolated via a direct o155-alone re-test).
8. Structural c150 audit (see above) — not a candidate, but the single highest-value non-code
   deliverable: mapped all ~24 overlays, confirmed the R36/R37 sale-reservation and V219/V233
   investment systems already implement 3 of the spec's ~20 backlog items, and found the specific
   remaining gaps (CARROT-equivalent-of-V219, general advantage/opponent estimation).
9. Full 46-agent diverse-pool baseline of plain c150 (`o_results/diverse_vs_c150/`) — c150 undefeated
   on net margin against all 44 resolvable, behaviorally-distinct local agents.
10. Full 46-agent diverse-pool re-run of o157 (`o_results/diverse_vs_o157/`) — the check that caught
    the regression (see below).
11. Full 46-agent diverse-pool re-run of o153 alone (`o_results/diverse_vs_o153/`) — confirmed clean.

## THE KEY FINDING: why o155/o157 were rejected despite looking like free money
`o155_open_10_8_25` changed only the game's very first (step-0) market order — a smaller WHEAT
buy/sell than c150's default, same net quantity traded. In 160 mirror-match games vs plain c150 it
won 156, lost 4, mean margin +19 to +25/game, and turned c150's exact 0-margin ties against c129/
c146 into reliable wins. This is exactly the kind of "structurally isolated, near-zero-risk" tweak
the spec's parameter-search backlog item (W) describes.

**A full 46-agent diverse-pool re-check (matched seeds against the existing c150 baseline) proved
this conclusion completely wrong.** 10 of 44 tested opponents showed a 50,000-88,000 point swing
*against us* (e.g. `ahmedberatozer-v35`: -57865 -> -5192; `yhay81-shop-router-0911-simple`: -98228
-> -9835), and one opponent (`ahmedberatozer-v40-plans-that-fit-the-shops`) flipped from us winning
by -54216 to the *opponent* winning by +1962. Root cause (traced with a step-by-step money/price
diff, `o_experiments.jsonl` entry `o155_regression_root_cause`): Kaggriculture's shared market
resolves both players' same-turn orders via **unit-by-unit lockstep interleaving**, so changing only
the *composition* (not net quantity) of our own step-0 trade changes the *opponent's* realized cash
by a few dollars as a pure side effect of price-curve interleaving — nothing to do with our own
value. Because most public-lineage agents (confirmed by the c150 audit) are full of exact or
near-exact money-threshold branches, that few-dollar difference can flip an opponent onto a
completely different 720-step trajectory, for better or (mostly, empirically) worse.

**Actionable rule for all future work on this project**: no isolated tweak — however small, however
"structurally free" it looks in code, however cleanly it wins in mirror-match testing — can be
trusted without a full diverse-pool validation. Mirror-match testing (or testing against only 2-3
opponents) is not just insufficient, it is actively misleading here, because the failure mode is a
chaotic threshold-flip in the *opponent's* logic, which a small, homogeneous opponent sample will
almost never surface. This generalizes the Halite IV research lesson
([past-competition-strategies-2026-09-14.ko.md](reports/past-competition-strategies-2026-09-14.ko.md))
from "nice to have" to "load-bearing for this specific engine."

## Rejected ideas
1. **o155/o157's opening-order tweak** — see above. Do not revisit "optimize the step-0 trade" via
   mirror-match testing alone; if retried, it must clear the full `o_tools/diverse_pool.json` set
   with matched seeds against the current champion before being trusted at all.
2. **Generic post-hoc budget/liquidity guard without item-type exclusions** (o152) — actively
   harmful; see o153 for the fix (exclude FERTILIZER/WHEAT).
3. **Hinge-triggered extra-SELL overlay** (o154) — premise already covered by V219; no signal found.
4. Do **not** attempt to relax/replace the terminal planner's physical-dominance safety net — c150's
   own L3125-3155 patch already relaxes it carefully; further loosening without very strong evidence
   risks the terminal-planner's correctness guarantees.

## Promising ideas (not yet built — deprioritized this session in favor of validation rigor)
1. **CARROT hinge-demand investment program** modeled on V219 — still a confirmed structural gap
   (no CARROT-equivalent of V219/V233 exists), but building it means adding NEW BUY_LAND/PLANT/HIRE
   logic, which is exactly the kind of change the o155 lesson says needs full diverse-pool
   validation before trusting any positive mirror-match result. Budget accordingly if attempted.
2. **State/advantage + opponent classifier -> DEFEND/CHASE mode (Backlog A/B/F)**: o156's classifier
   and o151's advantage telemetry are ready; actually gating behavior on them (e.g. relaxing V219/
   V233 thresholds) is exactly the kind of monkeypatch-heavy, deeply-coupled change flagged as high
   implementation risk during this session's audit (R37/R36/C115 all read/write shared module-level
   dicts with Python late-binding) — attempt only with generous validation budget.
3. Expand `o_tools/diverse_pool.json` further and/or build genuine "exploiter" opponents (backlog X)
   — not needed this session since no local agent beat c150, but worth revisiting if new public
   agents appear.
4. Generalize C116's one-off COW->SHEEP anti-mirror rewrite to the general `_r37_similarity` signal.
5. Wire up the already-built-but-inert `front_run`/`opponent_plan` hook (currently `False`/unused).

## Current known weaknesses of c150 (still true, unresolved)
1. No CARROT hinge-demand capture mechanism (TOMATO is covered by V219, CARROT is not).
2. No general economic-advantage estimation or opponent-behavior classification beyond narrow mirror
   detection.
3. **NEW, higher-priority than either of the above**: c150's behavior is demonstrably chaotically
   sensitive to tiny perturbations in shared-market order composition against a meaningful fraction
   (~20%) of real opponent policies, via threshold-branch flips triggered through the lockstep market
   mechanism. This is a property of the ENGINE + the wider public-agent ecosystem's coding style
   (heavy use of exact money/price thresholds), not something c150 itself did wrong, but it means
   c150's true margin against the live Kaggle field could be more variable/fragile than the extremely
   dominant local diverse-pool results suggest, if the live field contains agents with brittle
   threshold logic reacting to whatever tiny cash differences arise from normal head-to-head play.

## Next queue (for a future session)
1. If attempting the CARROT investment overlay or any DEFEND/CHASE work: budget for a full
   `o_tools/diverse_pool.json` validation pass (~15-20 min) per candidate, not just a mirror-match
   screen — non-negotiable given the o155 finding.
2. Consider whether c150's OWN vulnerability to the lockstep-interleaving effect (item 3 above) can
   be defensively hardened (e.g., does varying our OWN market order composition slightly, turn to
   turn, make us harder for a threshold-based opponent to exploit, or does it just add our own risk
   back in? Untested, genuinely unclear which direction is safer).
3. Expand `o_tools/diverse_pool.json` if new public notebooks appear; re-run the baseline audit.

## Important discoveries
- c150 vs c129 vs c146 tie EXACTLY (margin 0 every single game, 32/32) — c150's net behavior in a
  mirror match is indistinguishable from the older c129/c146 champions despite newer EXP-157..173
  changes; likely those overlays cancel out in symmetric mirrors or only activate off-lineage.
- All three Kaggle-named reference agents (shop-router-reactive-v5, v41-review-candidate,
  dynamic-route-agent) are same-lineage mirrors of c150 (margin ~+420-432/32 games, i.e. noise).
- **c150 is undefeated on net margin against all 44 resolvable, behaviorally-distinct local donor
  agents** (deduplicated via `donors.csv`'s `behaviour_family` clustering from the raw 52-agent
  dataset) — a genuinely rigorous, broad robustness result, not just "beats the top 10 by votes."
- **The lockstep-market chaos-sensitivity finding** (see above) — the most important structural
  discovery of the session, applicable to any future change to this or any sibling c-series agent.

## Live Kaggle audit (2026-09-15, `o_tools/live_episodes.py`, `o_tools/live_loss_probe.py`)
Per-submission live results (read-only episode API; `o_results/live_episodes_<sid>.json`):

| sub | episodes | W/L/T | vs <2400 | vs 2400-2749 | vs 2750+ | headline score |
|---|---|---|---|---|---|---|
| c129 (56209242) | 121 | 85/36/0 | 21/21 | 33/38 (87%) | **31/62 (50%)** | 2820 |
| c146 (56219458) | 114 | 76/38/0 | 22/22 | 26/36 (72%) | 28/56 (50%) | 2788 |
| c147 (56219450) | 106 | 71/35/0 | 22/22 | 38/54 (70%) | 11/30 (37%) | 2756 |
| c152 (56231047) | 81 | 52/29/0 | 19/19 | 31/50 (62%) | **2/12 (17%)** | 2703 |
| c153 (56232526) | 71 | 59/12/0 | 56/66 | 3/5 | (none yet) | 2383 (4h old, fresh-vs-fresh pairings, mean opp 2052 — NOT comparable yet) |

Findings:
1. **Ties are 0% live** for every submission — the "exact tie" problem only exists in local
   self-play/mirror tests; it is not a leaderboard problem.
2. **The rating ceiling (~2820) is set entirely by the 2750+ cluster, where we are a coin flip
   (50%)**; we win 100% below 2400 and 70-87% in between. The #1 team (3199) must be beating that
   cluster consistently. Nothing from c129 -> c153 moved the 2750+ win rate; c147/c152 look worse
   there (small samples for c152).
3. c153's headline 2383 is a rating-age artifact (4h, paired with other fresh submissions), not
   evidence of regression — it was locally proven byte-identical to c129 in 896 paired games. But
   that also means it could not have improved anything; it only spent a submission slot and reset
   the rating clock. Its 5 anomalous losses to low-rated opponents were checked replay-by-replay:
   no errors/timeouts (all DONE, 0 non-active steps), just genuine small-margin losses to fresh
   opponents of unknown true strength.
4. **Root process problem**: the local validation loop (donor pool, public trio, mirror pairs) has
   zero discriminating power at the top — c150 is 44-0 against the entire local pool, so "no
   regression in 896 paired games" is uninformative about the only games that decide the rating.
   The 79-live-loss ledger (`structural_loss_audit79_20260914`) already characterizes what the
   2750+ cluster does differently: `opponent_less_feed` 64/79, `opponent_more_fertilizer` 60/79,
   our feed failures 765 vs rival 195, our animal disappearances 184 vs 70, late reversal after
   step 504 in 32/79 (late cash swing total -248k). The c13x-c153 line patched feed narrowly
   (exact-one buffers) but the portfolio (livestock-heavy, feed-hungry, fertilizer-light) is what
   loses to the top cluster.
