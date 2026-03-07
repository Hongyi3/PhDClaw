# Master Plan

This file is the source of truth for milestone sequencing.

## North star

Build **ClawBio Scholar** as a companion project to ClawBio with this invariant:

> every claim cited, every figure reproducible, every release citable

## Phase 0 — Positioning and repo hygiene

- confirm repository name and scope
- align README and public narrative with real capabilities
- add citation, governance, and security baseline files
- define package boundaries and exemplar projects
- set up CI, issue forms, CODEOWNERS, and release metadata

**Exit criteria**
- repo identity finalized
- scaffold validated
- first public roadmap approved

## Phase 1 — Core data model

Implement the research object model with these entities:

- Project
- Corpus
- Dataset
- Protocol / DMSP
- AnalysisRun
- Figure
- Table
- Claim
- Citation
- Manuscript
- Release

**Exit criteria**
- machine-readable schema exists
- round-trip examples pass
- provenance links supported between claims, runs, and outputs

## Phase 2 — Evidence system

Build paper ingest and evidence mapping:

- DOI / PMID / BibTeX / PDF metadata ingestion
- identifier validation
- evidence cards and claim extraction
- contradiction / overlap flags
- verified reference graph

**Exit criteria**
- bibliography resolution works on exemplar corpora
- unsupported-reference rate is near zero on benchmark fixtures

## Phase 3 — Workflow and provenance

Build workflow scaffolding and run tracking:

- project bootstrapper
- workflow scaffolder
- run manifest
- environment capture
- figure provenance
- reproducibility bundle exporter

**Exit criteria**
- one-command rerun path exists for exemplar outputs
- provenance graph links outputs to inputs and parameters

## Phase 4 — Manuscript system

Build publication-facing outputs:

- Quarto article template
- Quarto thesis template
- lab notebook template
- reviewer response template
- AI usage ledger and disclosure blocks
- reporting-guideline completeness checks

**Exit criteria**
- end-to-end exemplar outputs a thesis chapter and article draft
- reporting checklist coverage is visible and testable

## Phase 5 — Release engine

Build open-science packaging:

- CITATION.cff generation or validation
- CodeMeta generation or validation
- RO-Crate packaging
- Zenodo-ready release checks
- changelog and archival prep

**Exit criteria**
- release candidate emits citable metadata
- artifact can be archived and cited

## Phase 6 — Evaluation and credibility

Build benchmarks and pilot evidence:

- literature retrieval benchmark
- unsupported-claim benchmark
- reproducibility benchmark
- reporting completeness benchmark
- external rerun pilot

**Exit criteria**
- at least two end-to-end exemplars succeed on clean rerun
- benchmark methodology documented

## Phase 7 — Public influence

- polish docs site
- ship v1.0
- archive DOI-backed release
- submit JOSS paper
- prepare Bioinformatics-style software note
- recruit external pilot labs

**Exit criteria**
- public release archived
- software paper draft ready
- external reproducibility evidence documented
