# o210_c9_opening (Claude/o-series, 2026-09-15). Overlay for the o199c stack.
# Public finding (nathanjacob "Beyond V43", cluster C9 = top-0.5% teams): drop the turn-0 wheat flip
# (buy 23 / sell 30, then sell 13 / buy 5 on turn 1) and just buy the 5 wheat the plants need; hires and
# animals stay on turn 1. Reported 96.5% vs V43 in 200 games. Same tape prefix as ours, so a direct test.
_O210_STEP0 = [['BUY_PRODUCT', 'WHEAT', 5]]
_O210_STEP1 = [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 2], ['BUY_ANIMAL', 'SHEEP', 2]]
for _o210_tape in list(_ROUTES.values()) + list(_IMPL.chassis.routes.values()):   # chassis keeps its own copy
    _o210_tape[0] = dict(_o210_tape[0], market=[list(o) for o in _O210_STEP0])
    _o210_tape[1] = dict(_o210_tape[1], market=[list(o) for o in _O210_STEP1])
del _o210_tape
agent = globals().pop('agent')
