# project-schema

Canonical JSON Schemas and validation helpers for ClawBio Scholar research objects.

## Implementation approach

- Draft 2020-12 JSON Schema files are the canonical machine-readable contracts.
- Python validation helpers enforce cross-record rules for integrated bundles and figure-manifest integrity checks when raw JSON Schema would be awkward or misleading.
- This package intentionally stops at local validation; it does not perform live DOI/PMID resolution or workflow execution.

## Implemented through the reproducibility bundle milestone

- standalone schemas for `project`, `citation`, `claim`, `analysis-run`, and `figure`
- an integrated `claim-set` bundle format with optional top-level `project` metadata and `analysis_runs`
- a provenance-only `reproducibility-bundle` format with embedded `project`, `analysis_runs`, and `figures`
- Python bundle validation for citation references, analysis-run references, duplicate ids, project alignment, and figure-to-run provenance links
- Python figure validation for duplicate input ids, duplicate panel ids, and panel-to-input references
- example fixtures for valid and invalid claim-set, figure, and reproducibility-bundle validation cases
- pytest coverage for schema loading, round-trip validation, and format checking

## Implemented models

- `Project`
- `Citation`
- `Claim`
- `AnalysisRun`
- `Figure`
- `claim-set`
- `reproducibility-bundle`

## Planned next contracts
- `Release`
- broader project-level entities once downstream packages need them

## Public Python API

```python
from project_schema import (
    SCHEMA_VERSION,
    load_schema,
    validate_claim_set,
    validate_document,
    validate_reproducibility_bundle,
)
```

## Commands

Run the package tests from the repository root:

```bash
pytest tests/test_project_schema.py
```

Run the scaffold validator required by the milestone:

```bash
python3 scripts/validate_scaffold.py
```

Run the full repository validation path:

```bash
make check
```

## Scope boundary

This package slice intentionally stops at local schema validation for `Project`, `Citation`, `Claim`, `AnalysisRun`, `Figure`, `claim-set`, and `reproducibility-bundle`. Release packaging, claim-to-figure linking, live identifier resolution, and RO-Crate/export concerns remain follow-up milestones.
