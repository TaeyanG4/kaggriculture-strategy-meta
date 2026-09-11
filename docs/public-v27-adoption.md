# Public v27 adoption checkpoint

Date: 2026-09-11

Primary champion: `agent/public_v27_kaito.py`

Source: Kaito Fukami, Kaggle notebook `25/27 Strict-Future | v27 Midgame Meta Reset`, Apache 2.0.
Exact upstream SHA-256: `f48c21166eac68d1b05a401f04f94a2eb6154e65415af64893672365ff33c7b8`.
The notebook credits the 719-action observable route backbone to Ezzzzzekki, public replay episode `91493566`, seat 0. Do not claim that route as original project work.

Local `kaggle-environments==1.32.7` validation:
- Rancher Rita: 12/12, mean margin +120873.8
- Broker Bea: 12/12, mean margin +25355.5
- Ledger Lena: 12/12, mean margin +24869.4
- Slotter Silas: 12/12, mean margin +24776.8
- Closer Cleo initial: 10/12, mean margin +6306.1
- Closer Cleo fresh confirmation: 38/40, mean margin +9343.2, both seats 95%, all DONE

Independent comparison:
- `optimize_project_performance/agent/strict_future_v27.py` has the exact same SHA-256.
- Direct 4-seed paired-seat match: 8/8 ties, mean margin 0.0.
- Therefore the two worktrees independently converged on the same executable policy.

Small independent screens before inspecting the other worktree:
- observation-driven terminal salvage from step 717: no score change on tested close/loss seeds.
- `_DEMAND_ALPHA` variants 0.0, 0.5, 1.0: none flipped the known tier-9 loss seed.
- Keep the exact public parent as champion until a fresh-gate derivative beats it.

Live Kaggle CLI readback on 2026-09-11:
- baseline_v7 submission 56166731: COMPLETE, Public Score 385.7
- v27 submission 56167312: COMPLETE, Public Score 991.7
These are live ladder ratings and should not be confused with notebook titles or historical 3000-class ratings.
