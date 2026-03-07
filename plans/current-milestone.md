# Current Milestone

This file is the canonical live-stage record for ClawBio Scholar.

## Project status summary

- Repository scaffold, governance files, validation baseline, and milestone continuity are in place.
- `packages/project-schema` now implements `Project`, `Citation`, `Claim`, `AnalysisRun`, `Figure`, `Release`, integrated `claim-set` bundle validation, and a provenance-only `reproducibility-bundle` contract.
- The next active milestone after this completed step is the `Corpus` schema so evidence-ingest work can build on a typed project-level collection contract.
- Placeholder maintainer metadata in public citation files remains unresolved, but this repository continued Phase 1 work by explicit human instruction.

## Current phase

`Phase 1 — Core data model`

## Current milestone

`Define Release schema in packages/project-schema`

## Why this milestone matters

- This milestone adds the first machine-readable release manifest that can point at citation material and bundled reproducibility artifacts.
- A staged local `Release` contract is the narrow bridge between provenance validation and later release-engine packaging without widening into archive publication, RO-Crate export, or metadata generation.

## In scope now

- A machine-readable staged `release` schema in `packages/project-schema`.
- Standalone `validate_document("release", ...)` support plus Python integrity checks for release artifact references and artifact kinds.
- Valid and invalid release fixtures, narrow pytest coverage, schema-version alignment, and progress/doc updates required to keep repository state accurate.

## Out of scope now

- Placeholder maintainer metadata cleanup in `CITATION.cff`, `codemeta.json`, and `CODEOWNERS`.
- CFF or CodeMeta content validation, RO-Crate packaging, release generation, archive publication, identifier resolution, and workflow execution.
- Any schema expansion beyond the minimum standalone `Release` contract, including corpus ingest behavior or claim-to-figure linking.

## Acceptance criteria

- `packages/project-schema` exposes a real, documented `release` schema.
- `load_schema("release")` and `validate_document("release", ...)` work locally.
- At least one valid release fixture passes round-trip validation and invalid fixtures fail the intended release integrity rules.
- Docs reflect the implementation accurately.
- `plans/current-milestone.md` and `plans/documentation.md` record final status, validation, and the exact next milestone.

## Validation commands

```bash
python3 scripts/validate_scaffold.py
pytest tests/test_project_schema.py
make check
```

## Current status

- State: completed
- Validation: `python3 scripts/validate_scaffold.py`; `pytest tests/test_project_schema.py`; `make check`
- Continuity note: this milestone builds on the already-complete Phase 1A foundation, Phase 1B figure provenance contract, and reproducibility bundle contract while preserving the earlier blocked Phase 0 metadata cleanup task as deferred follow-up work.

## Risks / blockers

- Placeholder maintainer metadata is still unresolved in public citation files and remains a follow-up outside this milestone.
- Future schema milestones should keep standalone JSON Schemas and Python validation rules aligned so release manifests, bundle contracts, and downstream release-engine logic do not drift.
- Citation-material links in the `Release` fixture intentionally stop at manifest-level references; content validation for `CITATION.cff` and `codemeta.json` remains a later release-engine milestone.

## Exact next milestone after completion

`Define Corpus schema in packages/project-schema`

## Update protocol

1. Read this file before implementation. If it is missing or stale, rebuild it from `plans/documentation.md`, `plans/master-plan.md`, `plans/implement.md`, the issue files, and relevant docs before coding.
2. When starting a milestone, update `Current phase`, `Current milestone`, `In scope now`, `Acceptance criteria`, and `Current status`.
3. Before ending work, update `Current status`, `Validation commands`, `Risks / blockers`, and `Exact next milestone after completion`.
4. Append a dated entry to `Status history` for every meaningful milestone change or conflict resolution.
5. If blocked by a genuine human decision, keep the milestone active, record the blocker, and do not silently skip ahead.

## Status history

### 2026-03-07 — Repository scaffold established

- Created the initial repository scaffold, governance files, plans, issue backlog, and validation path.

### 2026-03-07 — Claim and citation schema slice completed

- Implemented the first `project-schema` slice for `Citation`, `Claim`, and `claim-set`.
- Added fixture-backed validation coverage and normalized repository checks around `make check`.

### 2026-03-07 — Milestone continuity recovered

- Introduced `plans/current-milestone.md` as the canonical live-stage file.
- Recovered the active state as `Phase 0 — Positioning and repo hygiene` / `Replace placeholder metadata in citation files` because `plans/master-plan.md` defines the canonical milestone order and that milestone remains incomplete.
- Preserved the completed schema slice as recorded progress instead of treating later partial Phase 1 work as the active milestone.

### 2026-03-07 — Phase 1A started by explicit human override and completed

- A human explicitly directed the repository to begin `Phase 1A — Research object schema foundation` despite the blocked Phase 0 metadata cleanup task.
- Completed the first production-quality schema foundation for `Project`, `Citation`, `Claim`, and `AnalysisRun` in `packages/project-schema`.
- Added round-trip example coverage, cross-record validation for `claim-set`, and synced the relevant docs to the implemented state.

### 2026-03-07 — Phase 1B figure provenance manifest schema completed

- Added the first standalone `Figure` provenance manifest contract to `packages/project-schema`.
- Bumped the schema collection to `1.2.0`, added valid/invalid figure fixtures, and extended pytest coverage for figure-specific integrity rules.
- Set the exact next milestone to `Add reproducibility bundle contract in packages/project-schema`.

### 2026-03-07 — Reproducibility bundle contract completed

- Added the first provenance-only `reproducibility-bundle` contract to `packages/project-schema` with embedded `project`, `analysis_runs`, and `figures`.
- Bumped the schema collection to `1.3.0`, added valid/invalid reproducibility-bundle fixtures, and extended pytest coverage for bundle-level provenance checks.
- Set the exact next milestone to `Define Release schema in packages/project-schema`.

### 2026-03-07 — Release schema milestone started

- Promoted `Define Release schema in packages/project-schema` to the active Phase 1 milestone based on the repository progress files.
- Locked the milestone scope to a staged local release manifest plus fixtures, tests, and doc/progress synchronization.

### 2026-03-07 — Release schema milestone completed

- Added the staged `Release` contract to `packages/project-schema`, including artifact-link validation for citation material and reproducibility bundles.
- Bumped the schema collection to `1.4.0`, added valid/invalid release fixtures, and extended pytest coverage for release-specific integrity and format checks.
- Set the exact next milestone to `Define Corpus schema in packages/project-schema`.
