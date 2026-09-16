# Rebuilt simulation league

For new candidate selection and promotion, first apply the user-agreed
[agent validation protocol](agent-validation-protocol.ko.md). It defines fixed
historical baselines, diverse reacting opponents, separate weakness attackers,
top-1-to-3 evidence boundaries and fresh confirmation. The commands and seed plans
below document the original runner; do not reuse observed historical holdouts as
unseen tests. Current local simulations are user-run with completion/failure notices.

The replacement runner is `src/kaggriculture_meta/league.py`. It uses the pinned
Kaggriculture 1.32.7 engine and Kaggle's actual Python source loader. Each game
runs in a new subprocess, with separately initialized policy globals for each
seat. A policy receives only its normal observation and the engine configuration
after the engine removes the hidden seed. This runner is not a security sandbox.

## Reproduce a candidate evaluation

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -v
$env:LEAGUE_ENGINE_TESTS='1'
.venv/Scripts/python.exe -m unittest discover -s tests -p test_league_engine.py -v
.venv/Scripts/python.exe -m src.kaggriculture_meta.league run --plan configs/league_20260912_validation.json --candidate agent/c110_reserve8.py --stage holdout --out state/agent_experiments/my_c110_holdout --workers 4
```

Use a different output directory for every candidate and stage. Do not run two
coordinators against the same output directory concurrently. Repeat an identical
command to resume it. If source bytes, the harness, engine, plan or stage changed,
resumption is rejected; use a new output directory. Source snapshots are stored
by SHA-256. Logs, per-match jobs, results and raw evidence remain local under
ignored `state/agent_experiments/`.

The fixed plans have 12 training seeds, 16 selection seeds and 32 holdout seeds.
Both seats use every seed. Only training permits a partial `--seed-limit` screen.
All seed lists are validated for overlap and duplicates. A later research cycle
needs new holdout seeds; the 2026-09-12 holdout becomes historical after it is read.
The configuration seed controls the evaluator and is never added to policy inputs.

Each match records policy and engine fingerprints, resolved seed, both final
statuses, 719 decision calls / 720 states, action digests, local decision timings,
policy telemetry, farm checkpoints and the actual shop path. The default hard
wall limit is 90 seconds per subprocess. A crash, deadline failure or incomplete
match is a failure, not a win. Calls over one second are reported separately from
the engine's status/overage rules. Local timing does not establish Kaggle Docker
runtime performance.

## Interpretation

- Opponents with identical bytes are deduplicated. A renamed V37 clone is not
  another independent opponent. Self-play is excluded unless explicitly enabled.
- Results are reported per opponent, broad route family and seat. The current
  four-opponent plan covers two related public route families, not four independent
  elite implementations. It does not contain the private current leader's policy.
- Confidence summaries resample whole seed blocks, retaining both seats and
  opponents together. Degenerate all-win/all-tie samples receive no bootstrap
  interval. No local percentage is converted into a claimed leaderboard rating.
- Same seed does **not** imply the same shops. Weed generation consumes RNG draws
  only on empty tiles before the engine draws a shop. Policy changes can therefore
  alter subsequent shops. Native matches retain this official engine behavior.

## Recorded diagnostics

```powershell
.venv/Scripts/python.exe -m src.kaggriculture_meta.replay_lab --candidate agent/c110_reserve8.py --replays state/agent_experiments/plateau_audit_20260912/replays --out state/agent_experiments/my_fixed_diagnostics
```

The original two action tapes must reproduce every recorded shop arrival and the
exact final rewards before a counterfactual is accepted. The default diagnostic
fixes the recorded shop path in the evaluator, then replaces one player with the
candidate. The other player remains a frozen action tape. `--mode native_frozen_opponent`
retains native shop generation instead. Neither mode is a match against a reacting
private elite policy. Only the evaluator sees future shops; candidates never do.
Do not pool either diagnostic with the native reacting league.

## Candidate build and packaging

```powershell
.venv/Scripts/python.exe -m src.kaggriculture_meta.build_candidate --output state/agent_experiments/new_c110.py --sale-horizon 8
.venv/Scripts/python.exe -m src.kaggriculture_meta.package_agent --source agent/c110_reserve8.py --out submission/c110_reserve8
```

The exact public V37 parent is immutable. The builder preserves all upstream
notices and emits a self-contained standard-library policy with a change notice.
The packaging gate compiles it, inspects the two literal embedded code bodies,
checks imports, writes a deterministic `submission.tar.gz` containing only
`main.py`, and verifies its extracted bytes. It refuses to replace different
existing artifacts. Static inspection complements actual loader matches; it is
not a proof of security or strategic quality.

Other builder switches reproduce research hypotheses. The broad no-op repair,
early tomato, expanded fertilizer and inventory purchase reduction experiments
did not qualify for promotion. In particular, purchase reduction caused animal
losses despite aggregate stock forecasts; do not enable it in a submission.
