# Public release checklist

Owner decision 2026-10-01: the repository stays **private while the Kaggle
leaderboard is still running**. When the owner decides to open it, follow this
list in order. Items 1–4 were last verified on 2026-10-01 (commit 4a76ea7 and
later); re-run them before flipping.

## 1. No competition data in the repository

Kaggriculture rules forbid transferring, copying, publishing or redistributing
Competition Data to non-participants. The repository therefore contains code,
configs, reports and derived figures only.

- `.gitignore` excludes `state/` (raw replays, downloads, league database,
  experiment outputs), `o_results/`, `o_replays/`, pilot row-level CSVs and
  build artifacts.
- Verify: `git ls-files` has no `episode`, `replay`, `competition` or
  `download` directories, and no JSON/CSV larger than a few hundred KB outside
  `agent/`. Last check: only small schema QA JSON files matched.
- The dataset workstream used Kaggle's separately licensed CC0 daily episode
  datasets; the row-level release candidate stays local.

## 2. No credentials or private data

- Scan tracked files and the staged diff for API keys, tokens, passwords,
  tunnel URLs and e-mail addresses (pattern list in HANDOFF, 2026-10-01 entry).
- The league gateway reads credentials from local files that are not tracked;
  `public-league.html` and `public-league.vbs` contain only `127.0.0.1` URLs.
- Never commit `kaggle.json`, the Cloudflare tunnel address, league user lists
  or `state/public_league/`.

## 3. Third-party licenses

- Embedded public notebooks: Apache-2.0, license and attribution kept verbatim
  inside each embedding source; summary in `NOTICE`.
- Runtime dependency of the agent: Python standard library only.
- Tooling: `kaggle-environments` (Apache-2.0), `matplotlib` (PSF-based
  license) for figures, `kaggle` API client (Apache-2.0). None are vendored.
- Repository license: Apache-2.0 (`LICENSE`).

## 4. Documentation is current

- `README.md` and `README.ko.md` are parallel; sections 6 (Results) and
  7 (Review) are filled in after the final evaluation.
- `docs/INDEX.md` marks historical documents; `HANDOFF.md` START HERE reflects
  the current state.

## 5. Flip visibility and announce on Kaggle (rule 6.b)

Kaggriculture rule 6.b: if Competition Code is shared publicly, it must be made
available to all participants through the competition's Discussion forum or a
competition Notebook. Do both steps together, in this order:

1. `gh repo edit TaeyanG4/kaggriculture-strategy-meta --visibility public --accept-visibility-change-consequences`
2. Post in the Kaggriculture Discussion forum (draft below) with the repository
   link. Optionally attach the final `main.py` as a competition Notebook.

### Discussion post draft

> **Title:** My final solution / source code (layered public-notebook agent + paired validation runner)
>
> Sharing the full source of my final submission and the research repository
> behind it, under Apache-2.0: https://github.com/TaeyanG4/kaggriculture-strategy-meta
>
> **What it is.** The final agent (`c1200`) is a single-file stack of small,
> independently validated layers on top of public Apache-2.0 notebooks (Local
> Best market stack, V54 opening, V37/V27 lineage; all upstream notices kept).
> Each layer wraps the parent policy, changes the action only under a narrow
> observable condition, and confirms the intended own-field transition with an
> engine proxy before emitting it. A public-policy state tracker keeps embedded
> opponent hypotheses, discards those that contradict the observation, and
> reorders the market queue only when every surviving model predicts a gain.
>
> **How it was validated.** Candidate and parent always played identical worlds
> (same seed, seat and opponent) on disjoint seed stages, with health gates for
> 720 states / 719 calls / official timing. A local league collected 400+ public
> notebooks and played ~200k native matches to rate candidates against the live
> population. Negative results are recorded next to adoptions.
>
> **What is not included.** No competition data, replays or private sources;
> only code, configs, reports and figures. Thanks to every author whose public
> notebook this work builds on; attributions are in `NOTICE` and inside the
> sources.

## 6. After release

- Add the Kaggle Discussion URL to `README.md`/`README.ko.md` and `HANDOFF.md`.
- Optionally publish `state/c1200/c1200_final.tar.gz` as a GitHub Release asset
  (it contains `main.py`, `LICENSE.txt`, `NOTICE.txt` only).
