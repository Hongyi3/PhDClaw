# Architecture

## Core architectural decision

Build **ClawBio Scholar** as a **companion application** to ClawBio, not as a fork that destabilizes the upstream skill library.

## System layers

### 1. Application layer
User-facing surfaces:

- `apps/scholar-ui/`
- future CLI and dashboard surfaces

### 2. Core packages
Reusable logic:

- `packages/project-schema/`
- `packages/evidence-graph/`
- `packages/release-engine/`
- `packages/policy-checks/`

### 3. User-facing scholar skills
Research tasks:

- paper ingest
- evidence synthesis
- DMSP planning
- workflow scaffolding
- manuscript building
- reviewer response
- release shipping

### 4. Output layer
Artifacts should include:

- manuscript files
- figures and tables
- provenance manifests
- reproducibility bundle
- citation metadata
- release bundle

## Research object model

The internal data model should treat the project as a graph of linked scholarly objects.

### Entities

- `Project`
- `Corpus`
- `Dataset`
- `Protocol`
- `DMSP`
- `AnalysisRun`
- `Figure`
- `Table`
- `Claim`
- `Citation`
- `Manuscript`
- `Release`

### Invariants

- every `Claim` resolves to verified literature evidence or a reproducible `AnalysisRun`
- every `Figure` resolves to inputs, parameters, and environment
- every `Release` resolves to citation material and, when published, archived metadata

## Package responsibilities

### `project-schema`
Canonical JSON Schemas, Python cross-record validation, migrations, and examples.

Current implemented foundation: `Project`, `Citation`, `Claim`, `AnalysisRun`, `Figure`, `Release`, standalone figure and release validation, an integrated `claim-set` bundle validator, and a provenance-only `reproducibility-bundle` contract.

### `evidence-graph`
Identifier resolution, citation graph, claim cards, evidence linking.

### `release-engine`
CITATION, CodeMeta, RO-Crate, release manifest, archive prep.

### `policy-checks`
Reporting-guideline checks, AI disclosure checks, unsupported-claim detection, data/code availability checks.
