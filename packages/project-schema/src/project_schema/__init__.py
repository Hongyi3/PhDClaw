"""Public API for ClawBio Scholar project-schema validation helpers."""

from project_schema.api import (
    SCHEMA_VERSION,
    ProjectSchemaValidationError,
    load_schema,
    validate_claim_set,
    validate_document,
)

__all__ = [
    "SCHEMA_VERSION",
    "ProjectSchemaValidationError",
    "load_schema",
    "validate_claim_set",
    "validate_document",
]
