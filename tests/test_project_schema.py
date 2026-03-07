"""Tests for the first project-schema implementation slice."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from project_schema import (
    SCHEMA_VERSION,
    ProjectSchemaValidationError,
    load_schema,
    validate_claim_set,
    validate_document,
)

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "packages" / "project-schema" / "examples"


def _load_json(relative_path: str) -> dict:
    return json.loads((EXAMPLES_DIR / relative_path).read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", ["citation", "claim", "claim-set"])
def test_load_schema_supports_expected_names(name: str) -> None:
    schema = load_schema(name)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_validate_real_claim_set_fixture() -> None:
    document = _load_json("claim-set-valid.json")

    validate_document("claim-set", document)
    validate_document("citation", document["citations"][0])
    validate_document("claim", document["claims"][0])
    validate_claim_set(document)

    assert document["schema_version"] == SCHEMA_VERSION


def test_validate_claim_set_rejects_missing_citation_identifier() -> None:
    document = _load_json("invalid/claim-set-missing-citation-identifier.json")

    with pytest.raises(ProjectSchemaValidationError, match="identifier"):
        validate_claim_set(document)


def test_validate_claim_set_rejects_dangling_citation_reference() -> None:
    document = _load_json("invalid/claim-set-dangling-citation.json")

    with pytest.raises(ProjectSchemaValidationError, match="unknown citation_id 'missing-citation'"):
        validate_claim_set(document)


def test_validate_claim_set_rejects_unsupported_claim() -> None:
    document = _load_json("invalid/claim-set-unsupported-claim.json")

    with pytest.raises(ProjectSchemaValidationError, match="support link or analysis_run_id"):
        validate_claim_set(document)


def test_validate_claim_set_rejects_duplicate_ids() -> None:
    document = _load_json("claim-set-valid.json")
    document["citations"].append(document["citations"][0].copy())

    with pytest.raises(ProjectSchemaValidationError, match="Duplicate citation ids"):
        validate_claim_set(document)
