# Shared project instructions

Read and follow `AGENTS.md` and `HANDOFF.md` before working in this repository.
They are the canonical project rules for Claude Code, Codex, and other agents.
All agents now use **HANDOFF.md as the single shared worklog** (owner instruction,
2026-09-19). Its archive sections contain the former c-working/c-worklog/o-working
contents. Do not recreate those files. Record author and timestamp in the latest-work
section; search existing tools before implementing helpers. Read the first ~70 lines
for current state and search archived history by candidate ID instead of loading it all.
Start with the **START HERE** section at the top of `HANDOFF.md` (current state, rules,
pending owner decisions), then `reports/o-index-2026-09-19.ko.md` for which artifacts are
current vs superseded. Older sections of both files are dated history.

Do not create a new validation framework or copy experiment-specific runners.
Read `docs/reusable-validation.ko.md` and reuse:

- `tools/run-validation.ps1`
- `tools/validation_v1.py`
- `tools/validation_stats_v1.py`

New evaluations normally need only `configs/validation/<experiment>.json` and a
new result directory. Search existing tools before adding helpers. Document an
actual missing capability before extending tools; preserve frozen artifacts.

Agent implementation does not authorize simulation execution by itself: validation is
designed and its rules fixed before any game. Since 2026-09-18 21:12 the owner has delegated
running local campaigns to Claude (one campaign at a time, canonical runner, 8 workers);
Kaggle submission, blind-seed use and promotion remain the owner's decisions.
