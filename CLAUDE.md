# Shared project instructions

Read and follow `AGENTS.md` and `HANDOFF.md` before working in this repository.
They are the canonical project rules for Claude Code, Codex, and other agents.

Do not create a new validation framework or copy experiment-specific runners.
Read `docs/reusable-validation.ko.md` and reuse:

- `tools/run-validation.ps1`
- `tools/validation_v1.py`
- `tools/validation_stats_v1.py`

New evaluations normally need only `configs/validation/<experiment>.json` and a
new result directory. Search existing tools before adding helpers. Document an
actual missing capability before extending tools; preserve frozen artifacts.

Agent implementation does not authorize simulation execution. Hand off the code;
validation is designed after review, the user executes the supplied command, and
results are reviewed after the user reports completion.
