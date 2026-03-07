# Status and Decisions Log

Use this file as shared memory for maintainers and coding agents.

## Current focus

- live stage now tracked in `plans/current-milestone.md`
- Phase 1 schema foundation is complete for `Project`, `Citation`, `Claim`, `AnalysisRun`, `Figure`, `Release`, `claim-set`, and the provenance-only `reproducibility-bundle`
- next milestone is `Define Corpus schema in packages/project-schema`; placeholder metadata cleanup remains intentionally deferred pending maintainer confirmation

## Decision log

### 2026-03-07
- created prework scaffold for `clawbio-scholar`
- positioned project as a sibling / companion repo rather than a hard fork
- fixed initial structure around packages, scholar skills, benchmarks, and Quarto templates
- audited the repository and confirmed it was scaffold-only before implementation work began
- recorded validation drift: docs used `python` while the local environment only exposed `python3`
- selected `Define Claim and Citation schema` as the highest-leverage first milestone because it unlocks evidence integrity work without widening scope
- recorded an explicit human override to start `Phase 1A — Research object schema foundation` before the blocked Phase 0 metadata-cleanup milestone was resolved

## Gap analysis

### 2026-03-07 audit
- Core packages were README-only; no machine-readable schemas, package code, or tests existed.
- Benchmarks and examples were placeholders only; no runnable fixtures or reproducibility artifacts existed.
- Public narrative in `README.md` still described the repo as a prework scaffold instead of an early implementation.
- Validation instructions drifted from the environment by assuming `python`; `make check`, lint, and pytest coverage were not yet wired.
- Placeholder maintainer metadata remains in `CITATION.cff`, `codemeta.json`, `CODEOWNERS`, and `paper/joss/paper.md`; this milestone documents the gap but does not widen scope to fix it.

## Change log template

### YYYY-MM-DD
**Task:**  
**Why:**  
**Files changed:**  
**Validation:**  
**Follow-ups:**  

### 2026-03-07
**Task:** Implement claim/citation schema foundation in `packages/project-schema`.  
**Why:** Establish a real, machine-readable research-object contract for evidence integrity work and replace the repo's planning-only posture with a first implemented vertical slice.  
**Files changed:** `packages/project-schema/`, `tests/test_project_schema.py`, `pyproject.toml`, `Makefile`, `.github/workflows/ci.yml`, `README.md`, `plans/implement.md`, `plans/documentation.md`, `issues/01-first-issues.md`.  
**Validation:** `ruff check .`; `pytest`; `make check`.  
**Follow-ups:** Replace placeholder maintainer metadata, add additional research-object schemas (`AnalysisRun`, `Figure`, `Release`), implement identifier resolution in `evidence-graph`, and add Quarto render smoke tests once Quarto is available in the validation environment.

### 2026-03-07
**Task:** Introduce the durable milestone continuity contract and live-stage file.  
**Why:** Make the repository itself the source of truth for current stage, current progress, blockers, and the exact next milestone across Codex runs.  
**Files changed:** `AGENTS.md`, `plans/current-milestone.md`, `plans/implement.md`, `plans/documentation.md`, `scripts/validate_scaffold.py`.  
**Validation:** `python3 scripts/validate_scaffold.py`; `make check`.  
**Follow-ups:** Keep `plans/current-milestone.md` current on every meaningful change; the active metadata milestone remains blocked until a human confirms maintainer identity details, after which the next milestone is `Define AnalysisRun manifest schema in packages/project-schema`.

### 2026-03-07
**Task:** Implement the Phase 1A research-object schema foundation in `packages/project-schema`.  
**Why:** Establish the minimum production-quality schema backbone for evidence integrity, provenance, and later manuscript/release work without widening into downstream systems.  
**Files changed:** `packages/project-schema/`, `tests/test_project_schema.py`, `README.md`, `docs/01-architecture.md`, `docs/02-roadmap.md`, `issues/01-first-issues.md`, `llms.txt`, `plans/current-milestone.md`, `plans/documentation.md`.  
**Validation:** `python3 scripts/validate_scaffold.py`; `pytest tests/test_project_schema.py`; `make check`.  
**Follow-ups:** Define the figure provenance manifest schema next, keep placeholder maintainer metadata cleanup on the backlog pending human-confirmed identity details, and avoid widening into identifier resolution or release packaging before the schema layer is ready.

### 2026-03-07
**Task:** Add the Codex GitHub push rule to the repository contract and runbook.  
**Why:** Require Codex to push its own completed scoped changes while keeping unrelated local work out of those pushes.  
**Files changed:** `AGENTS.md`, `plans/implement.md`, `plans/documentation.md`.  
**Validation:** `python3 scripts/validate_scaffold.py`; `make check`.  
**Follow-ups:** This rule applies only to Codex-authored scoped changes; if pushing is blocked, report the exact failure instead of silently skipping the push.

### 2026-03-07
**Task:** Implement the Phase 1B figure provenance manifest schema in `packages/project-schema`.  
**Why:** Extend the schema backbone from `AnalysisRun` outputs to publication-facing figure artifacts without widening into workflow execution or release packaging.  
**Files changed:** `packages/project-schema/`, `tests/test_project_schema.py`, `README.md`, `docs/01-architecture.md`, `docs/02-roadmap.md`, `issues/01-first-issues.md`, `llms.txt`, `plans/current-milestone.md`, `plans/documentation.md`.  
**Validation:** `pytest tests/test_project_schema.py`; `python3 scripts/validate_scaffold.py`; `make check`.  
**Follow-ups:** Add the reproducibility bundle contract next, keep placeholder maintainer metadata cleanup on the backlog pending human-confirmed identity details, and defer `Release` schema work until the bundle contract is defined.

### 2026-03-07
**Task:** Implement the reproducibility bundle contract in `packages/project-schema`.  
**Why:** Bridge standalone analysis and figure provenance manifests into a single local validation contract that can support later rerun and release milestones without widening into export or workflow execution.  
**Files changed:** `packages/project-schema/`, `tests/test_project_schema.py`, `README.md`, `docs/01-architecture.md`, `docs/02-roadmap.md`, `issues/01-first-issues.md`, `llms.txt`, `plans/current-milestone.md`, `plans/documentation.md`.  
**Validation:** `python3 scripts/validate_scaffold.py`; `pytest tests/test_project_schema.py`; `make check`.  
**Follow-ups:** Define the `Release` schema next, keep placeholder maintainer metadata cleanup on the backlog pending human-confirmed identity details, and defer RO-Crate/export behavior until the release-engine milestone.

### 2026-03-07
**Task:** Implement the staged `Release` schema in `packages/project-schema`.  
**Why:** Add the first local release manifest contract that links citation material and reproducibility bundles without widening into release-engine packaging, metadata generation, or archive publication behavior.  
**Files changed:** `packages/project-schema/`, `tests/test_project_schema.py`, `README.md`, `docs/01-architecture.md`, `docs/02-roadmap.md`, `issues/01-first-issues.md`, `llms.txt`, `plans/current-milestone.md`, `plans/documentation.md`.  
**Validation:** `python3 scripts/validate_scaffold.py`; `pytest tests/test_project_schema.py`; `make check`.  
**Follow-ups:** Define the `Corpus` schema next, keep placeholder maintainer metadata cleanup on the backlog pending human-confirmed identity details, and defer citation-metadata content validation plus RO-Crate/export behavior until the release-engine milestone.
