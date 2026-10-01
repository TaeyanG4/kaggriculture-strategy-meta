# Documentation index

Status legend: **current** = still describes how the repository works today;
**reference** = still accurate for its subject, but that subject is no longer the
active workstream; **historical** = kept as a dated record and superseded by
later evidence.

Start with the top-level [README](../README.md) ([한국어](../README.ko.md)), then
`HANDOFF.md` (START HERE block = current state and pending owner decisions).

## Operating rules and process

| Document | What it covers | Status |
|---|---|---|
| [agent-validation-protocol.ko.md](agent-validation-protocol.ko.md) | Four evaluation groups (fixed baselines, diverse strong policies, weakness attackers, top observed), evidence boundaries, fresh confirmation | current |
| [reusable-validation.ko.md](reusable-validation.ko.md) | How to write a validation config and run the shared runner; stages, seeds, health rules, statistics | current (v1 contract; v3/v4 notes in research-tools) |
| [research-tools.ko.md](research-tools.ko.md) | Tool catalogue: runners v2/v3, overage timing contract, replay/identity audits, builders | current |
| [research-guardrails.md](research-guardrails.md) | Owner rules accumulated during the c300–c1000 research cycles (small-improvement policy, download exceptions, retry rules) | current |
| [release-checklist.md](release-checklist.md) | Steps before opening the repository: no competition data, no credentials, licenses, Kaggle rule 6.b Discussion post (draft included) | current |
| [completion-driven-research.ko.md](completion-driven-research.ko.md) | Completion-notification driven research loop used in the late cycles | current |
| [c300-research.ko.md](c300-research.ko.md) | c300-series research framing (live-loss decomposition, opening mirror) | reference |
| [o-validation-process.ko.md](o-validation-process.ko.md) | o-series validation process (planner candidates) | reference |
| [experiment-history-and-lessons.ko.md](experiment-history-and-lessons.ko.md) | Ledger of what was tried and why it failed; read before proposing a retry | current |

## Infrastructure

| Document | What it covers | Status |
|---|---|---|
| [simulation-league.md](simulation-league.md) | Rebuilt simulation league runner (`src/kaggriculture_meta/league.py`), official loader, seed plans | current |
| [public-league.ko.md](public-league.ko.md) | Public notebook league: collection, extraction, native reacting matches, rating | current (service stopped 2026-10-01) |
| [team-league-access.ko.md](team-league-access.ko.md) | Team login gateway and tunnel for the league UI | reference |
| [overnight-validation-plan.ko.md](overnight-validation-plan.ko.md) | Unattended batch validation plan | reference |
| [o-batch-validation-plan.ko.md](o-batch-validation-plan.ko.md) | Deferred narrow-intervention batch plan | reference |

## Baselines and adopted public sources

| Document | What it covers | Status |
|---|---|---|
| [public-v27-adoption.md](public-v27-adoption.md) | First public champion (Kaito Fukami v27), exact hashes, local checks | historical |
| [public-v37-adoption.md](public-v37-adoption.md) | Public V37 (Ahmed Berat Özer) and the c110 derivative; Master Engine V2 comparison | historical |

## Planner (o-series) workstream

| Document | What it covers | Status |
|---|---|---|
| [o-handoff-2026-09-16.ko.md](o-handoff-2026-09-16.ko.md) | Chronological hand-off of the planner cycles | historical |
| [o-planner-candidate-roadmap.ko.md](o-planner-candidate-roadmap.ko.md) | Planner candidate roadmap | historical |
| [o-planner-parallel-briefs.ko.md](o-planner-parallel-briefs.ko.md) | Parallel briefs for planner experiments | historical |
| [o-planner-proxy-plan.ko.md](o-planner-proxy-plan.ko.md) | Proxy evaluation plan | historical |
| [o-opening-redesign-plan.ko.md](o-opening-redesign-plan.ko.md) | Opening redesign plan (round-trip mirror) | historical |

## Dataset workstream (strategy meta V1)

| Document | What it covers | Status |
|---|---|---|
| [gate-2026-09-11.md](gate-2026-09-11.md) | Go/no-go gate evidence for the bounded current-meta build | historical |
| [v1-schema.md](v1-schema.md) | Public schema candidate for the 48-column strategy fingerprint table | reference |
| [data-dictionary.md](data-dictionary.md) | Column dictionary for the V1 table | reference |

## Early roadmap

| Document | What it covers | Status |
|---|---|---|
| [championship-roadmap-and-meta-analysis.md](championship-roadmap-and-meta-analysis.md) | 2026-09-12 proposal; its header marks which claims were later disproved | historical (superseded) |

## Reports

`reports/` holds about 300 dated evidence files, mostly in Korean, one per
candidate or review. `reports/o-index-2026-09-19.ko.md` maps which planner-era
artifacts are current versus superseded. Candidate reports are named
`c<id>-<topic>-<date>.ko.md`; search by candidate id.
