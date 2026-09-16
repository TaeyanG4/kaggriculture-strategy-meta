# o173b_no_c124 (Claude/o-series, 2026-09-15). Ablation overlay on o162.
# Removes C124 late feed abstention (overlaps o159 feed gate).
# Late global rebinding: the next wrapper now calls the ablated overlay's own parent, skipping it.
_C126_PARENT = _C124_PARENT
