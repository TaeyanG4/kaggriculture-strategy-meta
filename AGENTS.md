# Kaggriculture Project Operating Context

This file is the durable, project-scoped context for future ChatGPT sessions working in this repository.

## Main project

- This repository checkout is MAIN / Competition Core.

## Parallel work

- Former mechanics, meta-refresh, and agent-search worktrees have been merged back into MAIN.
- Do not recreate sibling worktrees unless a new parallel task explicitly needs isolation.
- If new worktrees are created, discover concrete paths with `git worktree list`; do not persist machine-specific absolute paths in tracked files.

## Shared handoff root

- Local parallel-agent handoffs live under `state/parallel-handoffs/`.
- Role directories may include `strategy-scout`, `mechanics`, `meta-refresh`, `agent-search`, `submission-qa`, and `integration`.
- Treat this tree as ignored local coordination state: read it when resuming work, but do not commit its contents.

## Mandatory skill rule

For every task in this project, apply the `kaggle-dataset-ops` skill when relevant, and use it as the default operating framework for Kaggle dataset/release/meta work.

The canonical skill content for this project was supplied by the user on 2026-09-11. Treat that supplied skill as authoritative for workflow rules including repository reconstruction, rights gates, deterministic collection, QA, Kaggle CLI/live readback, release hygiene, progress reporting, and end-of-session handoff.

If a future session cannot access the original uploaded skill file, it must still follow these project-local requirements and ask the project/tooling layer to load the installed `kaggle-dataset-ops` skill before performing Kaggle dataset operations.

## Session start rule

At the start of a new task in this project:

1. Read this `AGENTS.md`.
2. Read `HANDOFF.md`.
3. Reconstruct repository state with `git status --short --branch`, recent log, and remotes before edits.
4. Check `state/parallel-handoffs/` for relevant cross-agent evidence before duplicating research or experiments.
5. Respect ownership boundaries if new sibling worktrees are later created.
6. Do not treat chat memory as authoritative when repository/live state can be checked.

## Scope

These instructions apply only to this Kaggriculture project and its explicitly configured sibling worktrees/handoffs.

## Current competition champion

- Primary champion: `agent/public_v27_kaito.py`, byte-identical to Kaito Fukami's Apache-2.0 public v27 artifact.
- Exact SHA-256: `f48c21166eac68d1b05a401f04f94a2eb6154e65415af64893672365ff33c7b8`.
- Read `docs/public-v27-adoption.md` before agent optimization. Keep the parent immutable and create separately named derivatives.
- Superseded pre-adoption baselines (`baseline_v0` through `baseline_v7`, `rancher_rita_land14`, and inferior `v25 Meta Reset`) have been decommissioned and removed from `agent/`.
- `agent/public_v27_kaito.py` is the sole retained champion agent in `agent/`, mirrored into `submission/main.py` for direct Kaggle submission.
