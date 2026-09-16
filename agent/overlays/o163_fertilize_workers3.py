# SPDX-License-Identifier: Apache-2.0
# o163_fertilize_workers3 (Claude/o-series, 2026-09-15). Overlay appended after o159b+o162 on c150.
"""Endgame fertilizer expansion: the 2750+ cluster performs ~9 more FERTILIZE actions per game than
our lineage (88-loss divergence audit). c150's EXP182 input planner caps its hired fertilizer
tours at _R51_INPUT_MAX_WORKERS = 2 (read at call time from the module global). Raise to 3 —
all other EXP182 gates (value >= 1.5*cost+50, cash >= 3000 reserve, shed <= 95, market slots,
V219/V233 coexistence) stay as they are, so this only allows a third tour when the planner's own
economics already approve it. Behaviour is otherwise byte-identical to the parent.
"""
_R51_INPUT_MAX_WORKERS = 3
