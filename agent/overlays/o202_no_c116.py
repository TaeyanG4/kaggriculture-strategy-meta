# o202_no_c116 (Claude/o-series, 2026-09-15). Ablation on the o199c stack: disable C116 (route-10 YARN/PET day-6 COW pair -> SHEEP pair).
# Live loss 109149306 (YARN, PET first; 4 milk shops later): C116 chose sheep, rival kept cows, wool crashed to $11 while milk rose to $191 -> -2.7k.
_c116_controller = lambda observation, parent, state: parent
agent = globals().pop('agent')
