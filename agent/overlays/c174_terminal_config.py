
# c174 terminal configuration: use the same exact lockstep edge search only in
# the final 23 callbacks, where future liquidity is no longer a reason to prefer
# absolute own revenue over final score margin.
_C172_MIN_STEP = 696
_C172_MAX_STEP = 718
_C172_SCORE_GATE = 0.965
_C172_STREAK_GATE = 6
_C172_CASH_GAP = 3000.0
_C172_BEHIND_SLACK = 3000.0
_C172_EDGE_GAIN = 10.0
_C172_OWN_FLOOR = -1000000000.0