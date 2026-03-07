"""Validation helpers for the first ClawBio Scholar schema slice."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from typing import Mapping, Sequence

from jsonschema import Draft202012Validator

SCHEMA_VERSION = "1.0.0"
_SUPPORTED_SCHEMAS = frozenset({"citation", "claim", "claim-set"})


class ProjectSchemaValidationError(ValueError):
    """Raised when a document fails schema or bundle validation."""


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict:
    """Load a bundled JSON Schema by name."""

    if name not in _SUPPORTED_SCHEMAS:
        supported = ", ".join(sorted(_SUPPORTED_SCHEMAS))
        raise KeyError(f"Unsupported schema {name!r}. Expected one of: {supported}.")

    schema_path = files("project_schema.schemas").joinpath(f"{name}.json")
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_document(name: str, data: Mapping[str, object]) -> None:
    """Validate a single citation, claim, or claim-set document."""

    if not isinstance(data, Mapping):
        raise ProjectSchemaValidationError(f"{name} document must be a JSON object.")

    if name == "citation":
        _ensure_citation_identifier(data)
    if name == "claim":
        _ensure_claim_support(data)

    validator = Draft202012Validator(load_schema(name))
    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path)
        if location:
            raise ProjectSchemaValidationError(f"{name}.{location}: {error.message}") from error
        raise ProjectSchemaValidationError(f"{name}: {error.message}") from error


def validate_claim_set(data: Mapping[str, object]) -> None:
    """Validate a claim-set document and its cross-record references."""

    validate_document("claim-set", data)

    citations = _as_mapping_sequence(data.get("citations", []), "claim-set.citations")
    claims = _as_mapping_sequence(data.get("claims", []), "claim-set.claims")

    for index, citation in enumerate(citations):
        try:
            validate_document("citation", citation)
        except ProjectSchemaValidationError as exc:
            raise ProjectSchemaValidationError(f"claim-set.citations[{index}]: {exc}") from exc

    for index, claim in enumerate(claims):
        try:
            validate_document("claim", claim)
        except ProjectSchemaValidationError as exc:
            raise ProjectSchemaValidationError(f"claim-set.claims[{index}]: {exc}") from exc

    citation_ids = [str(citation["id"]) for citation in citations]
    claim_ids = [str(claim["id"]) for claim in claims]
    _ensure_unique_ids(citation_ids, "citation")
    _ensure_unique_ids(claim_ids, "claim")

    known_citation_ids = set(citation_ids)
    for claim in claims:
        claim_id = str(claim["id"])
        citation_support = claim.get("citation_support") or []
        analysis_run_ids = claim.get("analysis_run_ids") or []
        if not citation_support and not analysis_run_ids:
            raise ProjectSchemaValidationError(
                f"claim {claim_id!r} must include at least one support link or analysis_run_id."
            )
        for support in citation_support:
            citation_id = support["citation_id"]
            if citation_id not in known_citation_ids:
                raise ProjectSchemaValidationError(
                    f"claim {claim_id!r} references unknown citation_id {citation_id!r}."
                )


def _as_mapping_sequence(value: object, label: str) -> Sequence[Mapping[str, object]]:
    if not isinstance(value, list):
        raise ProjectSchemaValidationError(f"{label} must be a JSON array.")
    for item in value:
        if not isinstance(item, Mapping):
            raise ProjectSchemaValidationError(f"{label} entries must be JSON objects.")
    return value


def _ensure_citation_identifier(data: Mapping[str, object]) -> None:
    identifiers = [data.get("doi"), data.get("pmid"), data.get("pmcid")]
    if not any(identifier for identifier in identifiers):
        raise ProjectSchemaValidationError(
            "citation must include at least one identifier: doi, pmid, or pmcid."
        )


def _ensure_claim_support(data: Mapping[str, object]) -> None:
    citation_support = data.get("citation_support") or []
    analysis_run_ids = data.get("analysis_run_ids") or []
    if not citation_support and not analysis_run_ids:
        claim_id = data.get("id", "<unknown>")
        raise ProjectSchemaValidationError(
            f"claim {claim_id!r} must include at least one support link or analysis_run_id."
        )


def _ensure_unique_ids(ids: Sequence[str], label: str) -> None:
    seen = set()
    duplicates = []
    for item in ids:
        if item in seen:
            duplicates.append(item)
        seen.add(item)
    if duplicates:
        repeated = ", ".join(sorted(set(duplicates)))
        raise ProjectSchemaValidationError(f"Duplicate {label} ids are not allowed: {repeated}.")
