"""Validation helpers for the Phase 1 core data model foundation."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from functools import lru_cache
from importlib.resources import files
from typing import Mapping, Sequence
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_VERSION = "1.5.0"
_SUPPORTED_SCHEMAS = frozenset(
    {
        "analysis-run",
        "citation",
        "claim",
        "claim-set",
        "corpus",
        "figure",
        "project",
        "release",
        "reproducibility-bundle",
    }
)
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATE_TIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
_FORMAT_CHECKER = FormatChecker()


class ProjectSchemaValidationError(ValueError):
    """Raised when a document fails schema or bundle validation."""


@_FORMAT_CHECKER.checks("date")
def _check_date(instance: object) -> bool:
    if not isinstance(instance, str):
        return True
    if not _DATE_PATTERN.fullmatch(instance):
        return False
    try:
        date.fromisoformat(instance)
    except ValueError:
        return False
    return True


@_FORMAT_CHECKER.checks("date-time")
def _check_date_time(instance: object) -> bool:
    if not isinstance(instance, str):
        return True
    if not _DATE_TIME_PATTERN.fullmatch(instance):
        return False
    try:
        datetime.fromisoformat(instance.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


@_FORMAT_CHECKER.checks("uri")
def _check_uri(instance: object) -> bool:
    if not isinstance(instance, str):
        return True
    parsed = urlparse(instance)
    return bool(parsed.scheme and (parsed.netloc or parsed.path))


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
    """Validate a single schema-backed project-schema document."""

    if not isinstance(data, Mapping):
        raise ProjectSchemaValidationError(f"{name} document must be a JSON object.")

    if name == "citation":
        _ensure_citation_identifier(data)
    if name == "claim":
        _ensure_claim_support(data)

    validator = Draft202012Validator(
        load_schema(name), format_checker=_FORMAT_CHECKER
    )
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

    if name == "figure":
        _ensure_figure_integrity(data)
    if name == "corpus":
        _ensure_corpus_integrity(data)
    if name == "release":
        _ensure_release_integrity(data)


def validate_claim_set(data: Mapping[str, object]) -> None:
    """Validate a claim-set document and its cross-record references."""

    validate_document("claim-set", data)

    project = _as_optional_mapping(data.get("project"), "claim-set.project")
    citations = _as_mapping_sequence(data.get("citations", []), "claim-set.citations")
    claims = _as_mapping_sequence(data.get("claims", []), "claim-set.claims")
    analysis_runs = _as_mapping_sequence(data.get("analysis_runs", []), "claim-set.analysis_runs")

    if "analysis_runs" in data and project is None:
        raise ProjectSchemaValidationError(
            "claim-set.project is required whenever claim-set.analysis_runs is present."
        )

    if project is not None:
        validate_document("project", project)

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

    for index, analysis_run in enumerate(analysis_runs):
        try:
            validate_document("analysis-run", analysis_run)
        except ProjectSchemaValidationError as exc:
            raise ProjectSchemaValidationError(
                f"claim-set.analysis_runs[{index}]: {exc}"
            ) from exc

    citation_ids = [str(citation["id"]) for citation in citations]
    claim_ids = [str(claim["id"]) for claim in claims]
    analysis_run_ids = [str(analysis_run["id"]) for analysis_run in analysis_runs]
    _ensure_unique_ids(citation_ids, "citation")
    _ensure_unique_ids(claim_ids, "claim")
    _ensure_unique_ids(analysis_run_ids, "analysis_run")

    known_citation_ids = set(citation_ids)
    known_analysis_run_ids = set(analysis_run_ids)
    for claim in claims:
        claim_id = str(claim["id"])
        citation_support = claim.get("citation_support") or []
        supporting_analysis_run_ids = claim.get("analysis_run_ids") or []
        if not citation_support and not supporting_analysis_run_ids:
            raise ProjectSchemaValidationError(
                f"claim {claim_id!r} must include at least one support link or analysis_run_id."
            )
        for support in citation_support:
            citation_id = support["citation_id"]
            if citation_id not in known_citation_ids:
                raise ProjectSchemaValidationError(
                    f"claim {claim_id!r} references unknown citation_id {citation_id!r}."
                )
        for analysis_run_id in supporting_analysis_run_ids:
            if analysis_run_id not in known_analysis_run_ids:
                raise ProjectSchemaValidationError(
                    f"claim {claim_id!r} references unknown analysis_run_id {analysis_run_id!r}."
                )

    if project is not None:
        project_id = str(project["id"])
        for analysis_run in analysis_runs:
            analysis_run_id = str(analysis_run["id"])
            analysis_run_project_id = str(analysis_run["project_id"])
            if analysis_run_project_id != project_id:
                raise ProjectSchemaValidationError(
                    "analysis_run "
                    f"{analysis_run_id!r} project_id {analysis_run_project_id!r} "
                    f"does not match claim-set.project.id {project_id!r}."
                )


def validate_reproducibility_bundle(data: Mapping[str, object]) -> None:
    """Validate a reproducibility-bundle document and its provenance links."""

    validate_document("reproducibility-bundle", data)

    project = _as_optional_mapping(data.get("project"), "reproducibility-bundle.project")
    analysis_runs = _as_mapping_sequence(
        data.get("analysis_runs", []), "reproducibility-bundle.analysis_runs"
    )
    figures = _as_mapping_sequence(data.get("figures", []), "reproducibility-bundle.figures")

    if project is None:
        raise ProjectSchemaValidationError("reproducibility-bundle.project is required.")

    validate_document("project", project)

    for index, analysis_run in enumerate(analysis_runs):
        try:
            validate_document("analysis-run", analysis_run)
        except ProjectSchemaValidationError as exc:
            raise ProjectSchemaValidationError(
                f"reproducibility-bundle.analysis_runs[{index}]: {exc}"
            ) from exc

    for index, figure in enumerate(figures):
        try:
            validate_document("figure", figure)
        except ProjectSchemaValidationError as exc:
            raise ProjectSchemaValidationError(
                f"reproducibility-bundle.figures[{index}]: {exc}"
            ) from exc

    project_id = str(project["id"])
    analysis_run_ids = [str(analysis_run["id"]) for analysis_run in analysis_runs]
    figure_ids = [str(figure["id"]) for figure in figures]
    _ensure_unique_ids(analysis_run_ids, "analysis_run")
    _ensure_unique_ids(figure_ids, "figure")

    analysis_runs_by_id = {str(analysis_run["id"]): analysis_run for analysis_run in analysis_runs}

    for analysis_run in analysis_runs:
        analysis_run_id = str(analysis_run["id"])
        analysis_run_project_id = str(analysis_run["project_id"])
        if analysis_run_project_id != project_id:
            raise ProjectSchemaValidationError(
                "analysis_run "
                f"{analysis_run_id!r} project_id {analysis_run_project_id!r} "
                f"does not match reproducibility-bundle.project.id {project_id!r}."
            )

    for figure in figures:
        figure_id = str(figure["id"])
        figure_project_id = str(figure["project_id"])
        if figure_project_id != project_id:
            raise ProjectSchemaValidationError(
                "figure "
                f"{figure_id!r} project_id {figure_project_id!r} "
                f"does not match reproducibility-bundle.project.id {project_id!r}."
            )

        upstream_analysis_run_ids = figure.get("upstream_analysis_run_ids") or []
        sourced_inputs = [
            item
            for item in _as_mapping_sequence(figure.get("inputs", []), f"figure {figure_id!r} inputs")
            if item.get("source_analysis_run_id")
        ]
        if not upstream_analysis_run_ids and not sourced_inputs:
            raise ProjectSchemaValidationError(
                f"figure {figure_id!r} must include at least one bundled provenance link."
            )

        for analysis_run_id in upstream_analysis_run_ids:
            if analysis_run_id not in analysis_runs_by_id:
                raise ProjectSchemaValidationError(
                    f"figure {figure_id!r} references unknown upstream_analysis_run_id "
                    f"{analysis_run_id!r}."
                )

        for figure_input in sourced_inputs:
            source_analysis_run_id = str(figure_input["source_analysis_run_id"])
            if source_analysis_run_id not in analysis_runs_by_id:
                raise ProjectSchemaValidationError(
                    f"figure {figure_id!r} input {figure_input['id']!r} references unknown "
                    f"source_analysis_run_id {source_analysis_run_id!r}."
                )

            _ensure_figure_input_matches_analysis_output(
                figure_id=figure_id,
                figure_input=figure_input,
                analysis_run=analysis_runs_by_id[source_analysis_run_id],
            )


def _as_mapping_sequence(value: object, label: str) -> Sequence[Mapping[str, object]]:
    if not isinstance(value, list):
        raise ProjectSchemaValidationError(f"{label} must be a JSON array.")
    for item in value:
        if not isinstance(item, Mapping):
            raise ProjectSchemaValidationError(f"{label} entries must be JSON objects.")
    return value


def _as_optional_mapping(value: object, label: str) -> Mapping[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ProjectSchemaValidationError(f"{label} must be a JSON object.")
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


def _ensure_figure_integrity(data: Mapping[str, object]) -> None:
    inputs = data.get("inputs") or []
    panels = data.get("panels") or []

    input_ids = [str(item["id"]) for item in inputs]
    panel_ids = [str(panel["id"]) for panel in panels]

    _ensure_unique_ids(input_ids, "figure input")
    _ensure_unique_ids(panel_ids, "figure panel")

    known_input_ids = set(input_ids)
    for panel in panels:
        panel_id = str(panel["id"])
        for input_id in panel.get("input_ids", []):
            if input_id not in known_input_ids:
                raise ProjectSchemaValidationError(
                    f"figure panel {panel_id!r} references unknown input_id {input_id!r}."
                )


def _ensure_corpus_integrity(data: Mapping[str, object]) -> None:
    citations = _as_mapping_sequence(data.get("citations", []), "corpus.citations")
    holdings = _as_mapping_sequence(data.get("holdings", []), "corpus.holdings")

    for index, citation in enumerate(citations):
        try:
            validate_document("citation", citation)
        except ProjectSchemaValidationError as exc:
            raise ProjectSchemaValidationError(f"corpus.citations[{index}]: {exc}") from exc

    citation_ids = [str(citation["id"]) for citation in citations]
    holding_ids = [str(holding["id"]) for holding in holdings]
    _ensure_unique_ids(citation_ids, "corpus citation")
    _ensure_unique_ids(holding_ids, "corpus holding")

    known_citation_ids = set(citation_ids)
    for index, holding in enumerate(holdings):
        citation_id = str(holding["citation_id"])
        if citation_id not in known_citation_ids:
            raise ProjectSchemaValidationError(
                "corpus.holdings"
                f"[{index}].citation_id references unknown citation_id {citation_id!r}."
            )


def _ensure_release_integrity(data: Mapping[str, object]) -> None:
    citation = _as_optional_mapping(data.get("citation"), "release.citation")
    if citation is None:
        raise ProjectSchemaValidationError("release.citation must be a JSON object.")

    artifacts = _as_mapping_sequence(data.get("artifacts", []), "release.artifacts")
    artifact_ids = [str(artifact["id"]) for artifact in artifacts]
    _ensure_unique_ids(artifact_ids, "release artifact")
    artifacts_by_id = {str(artifact["id"]): artifact for artifact in artifacts}

    _ensure_release_artifact_kind(
        artifacts_by_id=artifacts_by_id,
        artifact_id=str(citation["cff_artifact_id"]),
        expected_kind="citation-cff",
        label="release.citation.cff_artifact_id",
    )
    _ensure_release_artifact_kind(
        artifacts_by_id=artifacts_by_id,
        artifact_id=str(citation["codemeta_artifact_id"]),
        expected_kind="codemeta-json",
        label="release.citation.codemeta_artifact_id",
    )

    reproducibility_bundle_artifact_ids = data.get("reproducibility_bundle_artifact_ids") or []
    for index, artifact_id in enumerate(reproducibility_bundle_artifact_ids):
        _ensure_release_artifact_kind(
            artifacts_by_id=artifacts_by_id,
            artifact_id=str(artifact_id),
            expected_kind="reproducibility-bundle",
            label=f"release.reproducibility_bundle_artifact_ids[{index}]",
        )


def _ensure_release_artifact_kind(
    *,
    artifacts_by_id: Mapping[str, Mapping[str, object]],
    artifact_id: str,
    expected_kind: str,
    label: str,
) -> None:
    artifact = artifacts_by_id.get(artifact_id)
    if artifact is None:
        raise ProjectSchemaValidationError(
            f"{label} references unknown artifact_id {artifact_id!r}."
        )

    artifact_kind = str(artifact["kind"])
    if artifact_kind != expected_kind:
        raise ProjectSchemaValidationError(
            f"{label} references artifact {artifact_id!r} with kind {artifact_kind!r}; "
            f"expected {expected_kind!r}."
        )


def _ensure_figure_input_matches_analysis_output(
    *,
    figure_id: str,
    figure_input: Mapping[str, object],
    analysis_run: Mapping[str, object],
) -> None:
    input_id = str(figure_input["id"])
    analysis_run_id = str(analysis_run["id"])
    outputs = _as_mapping_sequence(
        analysis_run.get("outputs", []), f"analysis_run {analysis_run_id!r} outputs"
    )
    matching_output = next(
        (output for output in outputs if str(output.get("id")) == input_id),
        None,
    )
    if matching_output is None:
        raise ProjectSchemaValidationError(
            f"figure {figure_id!r} input {input_id!r} references source_analysis_run_id "
            f"{analysis_run_id!r} but no matching output artifact id {input_id!r} exists."
        )

    for field_name in ("path", "sha256", "media_type"):
        if field_name in figure_input and field_name in matching_output:
            if figure_input[field_name] != matching_output[field_name]:
                raise ProjectSchemaValidationError(
                    f"figure {figure_id!r} input {input_id!r} {field_name} "
                    f"{figure_input[field_name]!r} does not match analysis_run "
                    f"{analysis_run_id!r} output value {matching_output[field_name]!r}."
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
