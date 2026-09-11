# Kaggle release preparation — 2026-09-11

## Status

**PREPARED LOCALLY; NOT PUBLISHED.**

The bounded current-meta V1 has been packaged into a local ignored release directory using the current Kaggle CLI metadata template. A private script-kernel package has also been prepared locally. No `kaggle datasets create`, `kaggle datasets version`, or `kaggle kernels push` command has been run for this project.

## Dataset package

- Owner: `taeyangg4`
- Proposed title: **Kaggriculture Current Meta Fingerprints**
- Proposed slug: `taeyangg4/kaggriculture-current-meta-fingerprints`
- Subtitle: **Openings, economy and resource allocation from official daily episodes**
- License: `CC0-1.0`
- Data files: exactly one, `strategy_meta.csv`
- Rows: 336
- Columns: 48
- Bytes: 122,674
- SHA-256: `7c4249d0fabbf186e059304ebf8a901471bf80ecf193b7b21125dab556f21744`

The title, subtitle, and slug fit the current Kaggle CLI metadata length constraints. The local package copy has the same SHA-256 as the final release candidate.

Live Kaggle CLI search found no Dataset using the proposed slug at the release-prep checkpoint. This must still be rechecked immediately before create.

The description explicitly states that this is a deterministic bounded sample of official daily source manifests, not a random full-ladder estimate. It also states that the experimental family label is not ground truth, that no validated winning formula or counter-strategy claim is made, and that raw replay JSON is not redistributed.

## Data dictionary

The tracked data dictionary is `docs/data-dictionary.md`. It documents all 48 public V1 columns and the sampling/outcome-analysis caveats.

## First notebook package

- Proposed title: **Kaggriculture Current Meta Quicklook**
- Proposed kernel slug: `taeyangg4/kaggriculture-current-meta-quicklook`
- Code source: `notebooks/01_current_meta_quicklook.py`
- Kernel type: `script`
- Language: Python
- Private: yes
- Internet: disabled
- GPU/TPU: disabled
- Dataset source: proposed current-meta Dataset slug

Live Kaggle CLI search found no Kernel using the proposed quicklook slug at the release-prep checkpoint.

The script was smoke-tested locally against the final 336-row / 48-column release candidate. It loads the data, prints source-scope caveats, builds daily aggregates, and renders separate charts for animal allocation, crop allocation, opening diversity, and turn-168 cash. It also shows the experimental family mix and a clearly labeled descriptive winner/loser table.

The notebook intentionally does **not** claim that any early feature predicts victory. Project-level paired testing found no non-outcome feature that passed all current robustness criteria.

## Publication blockers / gates

1. The scheduled 2026-09-11 official daily source has not yet been observed as public in the live CLI checks performed during this work session.
2. When that source appears, append it with the same 24-quantile selection rule and rerun core QA/provenance.
3. Reconfirm the exact dataset slug is unused immediately before create.
4. Reconfirm the active-competition public-code rule before making the notebook public. Keep the GitHub repository private until that gate is explicitly satisfied.
5. Only after those checks should `kaggle datasets create` be considered. The first notebook should follow the Dataset and use the actual live Dataset ref.
