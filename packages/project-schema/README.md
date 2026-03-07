# project-schema

Canonical schemas for ClawBio Scholar.

## Implemented in this milestone

- JSON Schema contracts for `citation`, `claim`, and `claim-set`
- Python validation helpers for bundle-level checks that JSON Schema alone does not express cleanly
- example fixtures for valid and invalid claim sets
- pytest coverage for schema loading and validation behavior

## Implemented models
- `Citation`
- `Claim`
- `claim-set`

## Planned next models
- `AnalysisRun`
- `Figure`
- `Release`
- broader project-level entities once downstream packages need them

## Public Python API

```python
from project_schema import (
    SCHEMA_VERSION,
    load_schema,
    validate_claim_set,
    validate_document,
)
```

## Commands

Run the package tests from the repository root:

```bash
pytest tests/test_project_schema.py
```

Run the full repository validation path:

```bash
make check
```

## Scope boundary

This package slice intentionally stops at local schema validation. Live DOI/PMID resolution, benchmark harnesses, and additional research-object schemas remain follow-up milestones.
