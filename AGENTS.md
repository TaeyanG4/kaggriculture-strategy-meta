# Kaggriculture Project Operating Context

This checkout is MAIN / Competition Core. Keep this file short; detailed history
belongs in ignored `state/` artifacts and dated reports.

## Start of task

1. Read this file and `HANDOFF.md`.
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
- Implementation-only assignments end with code/artifact handoff. Do not launch
  simulations: validation design/commands follow implementation review, the user runs
  the commands, and completed results are reviewed afterward.

- The project-specific Kaggle skill was removed at the user's request on 2026-09-14.
  Do not require or recreate it.
- Current execution preference: the user runs simulations. Prepare commands rather
  than launching a new campaign unless the user explicitly changes this preference.
- Global Kaggriculture simulation cap is 8 workers across all active campaigns.
  Never start overlapping campaigns.
- Long validation may use all 8 workers, but each match must run in a fresh Python
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

## Current checkpoint

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
- Current concise state: `HANDOFF.md`
- Full pre-compaction context: `state/context-archive/20260914-121406/`
- Latest loss audit: `state/agent_experiments/structural_loss_audit79_20260914/`
- Colleague evidence: `state/parallel-handoffs/collaboration-20260914/`
- o/r-series (Claude) validation process, reference only, not mandatory for c-series: `docs/o-validation-process.ko.md`
