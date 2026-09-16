# o173a_no_c126 (Claude/o-series, 2026-09-15). Ablation overlay on o162.
# Removes C126 feed-buffer (funds imminent grain pickups); o159 now wraps C124 directly.
# Late global rebinding: the next wrapper now calls the ablated overlay's own parent, skipping it.
_O159_PARENT = _C126_PARENT
