# ClawBio Scholar

**ClawBio Scholar** is a companion project to ClawBio focused on thesis-quality, publication-grade, reproducible biomedical research workflows.

## Product thesis

ClawBio Scholar should become a **local-first research operating system for biomedical and computational-biology PhD work**:

- literature in
- evidence graph built
- study design and data management plan scaffolded
- analysis workflow generated
- figures reproduced with provenance
- manuscript chapters rendered
- release archived with citation metadata

The north star is simple:

> **Every claim cited. Every figure reproducible. Every release citable.**

## Current implementation status

This repository now contains the planning and governance layer plus the first implemented research-object schema slice.

Current working capabilities:

- governance and contributor files
- a Codex-ready `AGENTS.md`
- root-level Codex skills in `.agents/skills/`
- a milestone-by-milestone execution plan in `plans/`
- architecture, evaluation, and launch documents in `docs/`
- GitHub issue forms, CODEOWNERS, CI, and release-prep metadata
- a JSON-Schema-first `project-schema` package for `Citation`, `Claim`, and `claim-set` validation
- example claim-set fixtures and pytest coverage for schema and bundle validation
- Quarto starter templates for article, thesis, and reviewer response workflows
- JOSS paper starter material

## Recommended repository identity

- **Repository name:** `clawbio-scholar`
- **Positioning:** companion application to ClawBio, not a fork
- **Audience v1:** biomedical / computational-biology PhD students and supervisors
- **Core promise:** thesis-ready, reproducible, auditable, open-science-native outputs

## Next 10 tasks

1. Replace placeholder metadata in `CITATION.cff`, `codemeta.json`, and `CODEOWNERS`.
2. Expand `project-schema` beyond `Claim` and `Citation` to cover `AnalysisRun`, `Figure`, and `Release`.
3. Implement the evidence graph package.
4. Add DOI / PMID / BibTeX ingestion.
5. Define unsupported-claim benchmark fixture formats.
6. Define the reproducibility bundle contract.
7. Ship Quarto thesis and article templates with render smoke tests.
8. Add reporting-guideline and AI-disclosure checks.
9. Decide the initial exemplar set: scRNA-seq, UK Biobank, metagenomics.
10. Prepare the first DOI-backed public release and software-paper draft.

## Repo map

```text
.agents/skills/         Codex skills for implementation, doc sync, audits, releases
.github/                issue forms, workflows, pull request template, Dependabot
apps/                   user-facing applications (initially scholar-ui)
benchmarks/             evaluation harnesses and gold sets
docs/                   product thesis, architecture, roadmap, launch, evaluation
examples/               exemplar end-to-end PhD workflows
issues/                 issue backlog and epics
metadata/               RO-Crate and release metadata notes
packages/               reusable core packages
paper/                  JOSS paper and future software-paper materials
plans/                  source-of-truth execution plan for Codex and humans
scholar-skills/         user-facing ClawBio Scholar skills
scripts/                repo validation and helper scripts
templates/              Quarto templates for article, thesis, reviewers
```

## Operating rule

This repository should prefer **credible scope** over broad scope. v1 succeeds by being excellent for a narrow biomedical PhD workflow, not by pretending to serve every discipline.

## Validation

Run the current repo validation path with:

```bash
make check
```

The `project-schema` package can also be exercised directly with:

```bash
pytest tests/test_project_schema.py
```
