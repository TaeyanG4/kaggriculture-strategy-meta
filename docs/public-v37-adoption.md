# Public V37 and the c110 derivative

Baseline source: Ahmed Berat Özer, [More Yield, Smarter Labor](https://www.kaggle.com/code/ahmedberatozer/more-yield-smarter-labor).
The complete Apache-2.0 license and upstream attribution to yhay81, prvsiyan,
Dmitrii Gluzdov, thomastschinkel and the other credited contributors remain in
the source. Do not claim these public routes or production controllers as newly
trained project work. No private leaderboard policy source was obtained.

| Artifact | SHA-256 | Role |
| --- | --- | --- |
| `agent/public_v37_more_yield.py` | `94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c` | Exact immutable public baseline |
| `agent/c110_reserve8.py` | `0f31fd48e64cf3040a8fc66b14e98676b6b65916c010e0443fa5855d9ccc63ad` | Selected local derivative |
| `agent/public_master_engine_v2.py` | `0a18d38e8bf8daf921374b64c57a67a8a6901d3676ec9c184f81b7573f4fc29a` | Exact public reacting comparison |

Master Engine source: [Guru Prasaath S, Kaggriculture Master Engine V2](https://www.kaggle.com/code/guruprasaathas111/kaggriculture-master-engine-v2).
Master Engine and V37 share substantial public lineage. The downloaded Dynamic
Route Agent was byte-identical to V37 and is not retained as a separate opponent.

The selected c110 change extends the existing actual-stock sale reservation
window from 4 to 8 future own commands at steps 288 through 695. It retains the
parent's stock cap, per-due-step debt, purchase and pickup barriers, route-boundary
guard, wheat/fertilizer exclusion and native terminal window. The apparent
advantage comes from measured market timing, not a new learned production model.
Changing the window to 16 performed worse in screening. Additional repair,
purchase reduction and production expansion hypotheses failed their gates and
are excluded from c110.

The builder reproduces c110 exactly:

```powershell
.venv/Scripts/python.exe -m src.kaggriculture_meta.build_candidate --output state/agent_experiments/rebuilt_c110.py --sale-horizon 8
```

The old v27 and c101 files remain immutable. `submission/main.py` is still the
previous c101 artifact; the new package has a separate directory. Never infer the
current live submission from that legacy filename. Use the dated implementation
report, submission receipt and Kaggle live readback.

See [simulation-league.md](simulation-league.md) for reproduction and evidence
boundaries, and [league-rebuild-2026-09-12.ko.md](../reports/league-rebuild-2026-09-12.ko.md)
for the measured results and remaining elite gap.
