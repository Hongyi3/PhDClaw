# Status and Decisions Log

Use this file as shared memory for maintainers and coding agents.

## Current focus

- project-schema claim/citation foundation
- validation path normalized around `make check`
- backlog still open for maintainer metadata, evidence ingest, and Quarto render smoke tests

## Decision log

### 2026-03-07
- created prework scaffold for `clawbio-scholar`
- positioned project as a sibling / companion repo rather than a hard fork
- fixed initial structure around packages, scholar skills, benchmarks, and Quarto templates
- audited the repository and confirmed it was scaffold-only before implementation work began
- recorded validation drift: docs used `python` while the local environment only exposed `python3`
- selected `Define Claim and Citation schema` as the highest-leverage first milestone because it unlocks evidence integrity work without widening scope

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
