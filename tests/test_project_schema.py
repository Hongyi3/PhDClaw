"""Tests for the Phase 1 core data model foundation."""

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
    validate_reproducibility_bundle,
)

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "packages" / "project-schema" / "examples"


def _load_json(relative_path: str) -> dict:
    return json.loads((EXAMPLES_DIR / relative_path).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "name",
    [
        "analysis-run",
        "citation",
        "claim",
        "claim-set",
        "corpus",
        "figure",
        "project",
        "release",
        "reproducibility-bundle",
    ],
)
def test_load_schema_supports_expected_names(name: str) -> None:
    schema = load_schema(name)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_validate_real_claim_set_fixture_round_trip() -> None:
    document = _load_json("claim-set-valid.json")
    round_tripped = json.loads(json.dumps(document))

    validate_document("claim-set", round_tripped)
    validate_document("project", round_tripped["project"])
    validate_document("citation", round_tripped["citations"][0])
    validate_document("analysis-run", round_tripped["analysis_runs"][0])
    validate_document("claim", round_tripped["claims"][0])
    validate_claim_set(round_tripped)

    assert round_tripped["schema_version"] == SCHEMA_VERSION


def test_validate_real_figure_fixture_round_trip() -> None:
    document = _load_json("figure-valid.json")
    round_tripped = json.loads(json.dumps(document))

    validate_document("figure", round_tripped)

    assert round_tripped["project_id"] == "samtools-methods-note"


def test_validate_real_corpus_fixture_round_trip() -> None:
    document = _load_json("corpus-valid.json")
    round_tripped = json.loads(json.dumps(document))

    validate_document("corpus", round_tripped)

    assert round_tripped["holdings"][0]["citation_id"] == "li-2009-samtools"


def test_validate_real_reproducibility_bundle_fixture_round_trip() -> None:
    document = _load_json("reproducibility-bundle-valid.json")
    round_tripped = json.loads(json.dumps(document))

    validate_document("reproducibility-bundle", round_tripped)
    validate_reproducibility_bundle(round_tripped)

    assert round_tripped["schema_version"] == SCHEMA_VERSION


def test_validate_real_release_fixture_round_trip() -> None:
    document = _load_json("release-valid.json")
    round_tripped = json.loads(json.dumps(document))

    validate_document("release", round_tripped)

    assert round_tripped["status"] == "candidate"


def test_validate_claim_set_rejects_missing_citation_identifier() -> None:
    document = _load_json("invalid/claim-set-missing-citation-identifier.json")

    with pytest.raises(ProjectSchemaValidationError, match="identifier"):
        validate_claim_set(document)


def test_validate_claim_set_rejects_dangling_citation_reference() -> None:
    document = _load_json("invalid/claim-set-dangling-citation.json")

    with pytest.raises(ProjectSchemaValidationError, match="unknown citation_id 'missing-citation'"):
        validate_claim_set(document)


def test_validate_claim_set_rejects_dangling_analysis_run_reference() -> None:
    document = _load_json("invalid/claim-set-dangling-analysis-run.json")

    with pytest.raises(
        ProjectSchemaValidationError, match="unknown analysis_run_id 'missing-analysis-run'"
    ):
        validate_claim_set(document)


def test_validate_claim_set_rejects_unsupported_claim() -> None:
    document = _load_json("invalid/claim-set-unsupported-claim.json")

    with pytest.raises(ProjectSchemaValidationError, match="support link or analysis_run_id"):
        validate_claim_set(document)


def test_validate_figure_rejects_unknown_panel_input_reference() -> None:
    document = _load_json("invalid/figure-panel-missing-input.json")

    with pytest.raises(ProjectSchemaValidationError, match="unknown input_id 'missing-input'"):
        validate_document("figure", document)


def test_validate_corpus_rejects_unknown_holding_citation_reference() -> None:
    document = _load_json("invalid/corpus-holding-dangling-citation.json")

    with pytest.raises(ProjectSchemaValidationError, match="unknown citation_id 'missing-citation'"):
        validate_document("corpus", document)


def test_validate_corpus_rejects_duplicate_citation_ids() -> None:
    document = _load_json("corpus-valid.json")
    document["citations"].append(document["citations"][0].copy())

    with pytest.raises(ProjectSchemaValidationError, match="Duplicate corpus citation ids"):
        validate_document("corpus", document)


def test_validate_corpus_rejects_duplicate_holding_ids() -> None:
    document = _load_json("corpus-valid.json")
    document["holdings"].append(document["holdings"][0].copy())

    with pytest.raises(ProjectSchemaValidationError, match="Duplicate corpus holding ids"):
        validate_document("corpus", document)


def test_validate_figure_rejects_duplicate_input_ids() -> None:
    document = _load_json("figure-valid.json")
    document["inputs"].append(document["inputs"][0].copy())

    with pytest.raises(ProjectSchemaValidationError, match="Duplicate figure input ids"):
        validate_document("figure", document)


def test_validate_figure_rejects_duplicate_panel_ids() -> None:
    document = _load_json("figure-valid.json")
    document["panels"].append(document["panels"][0].copy())

    with pytest.raises(ProjectSchemaValidationError, match="Duplicate figure panel ids"):
        validate_document("figure", document)


def test_validate_claim_set_rejects_duplicate_ids() -> None:
    document = _load_json("claim-set-valid.json")
    document["citations"].append(document["citations"][0].copy())

    with pytest.raises(ProjectSchemaValidationError, match="Duplicate citation ids"):
        validate_claim_set(document)


def test_validate_claim_set_requires_project_when_analysis_runs_are_present() -> None:
    document = _load_json("claim-set-valid.json")
    document.pop("project")

    with pytest.raises(ProjectSchemaValidationError, match="claim-set.project is required"):
        validate_claim_set(document)


def test_validate_reproducibility_bundle_rejects_unknown_upstream_analysis_run() -> None:
    document = _load_json("invalid/reproducibility-bundle-unknown-upstream-analysis-run.json")

    with pytest.raises(
        ProjectSchemaValidationError, match="unknown upstream_analysis_run_id 'missing-analysis-run'"
    ):
        validate_reproducibility_bundle(document)


def test_validate_reproducibility_bundle_rejects_input_output_mismatch() -> None:
    document = _load_json("invalid/reproducibility-bundle-input-output-mismatch.json")

    with pytest.raises(ProjectSchemaValidationError, match="no matching output artifact id"):
        validate_reproducibility_bundle(document)


def test_validate_reproducibility_bundle_rejects_duplicate_figure_ids() -> None:
    document = _load_json("reproducibility-bundle-valid.json")
    document["figures"].append(document["figures"][0].copy())

    with pytest.raises(ProjectSchemaValidationError, match="Duplicate figure ids"):
        validate_reproducibility_bundle(document)


def test_validate_reproducibility_bundle_rejects_project_mismatch() -> None:
    document = _load_json("reproducibility-bundle-valid.json")
    document["analysis_runs"][0]["project_id"] = "other-project"

    with pytest.raises(ProjectSchemaValidationError, match="does not match reproducibility-bundle"):
        validate_reproducibility_bundle(document)


def test_validate_reproducibility_bundle_requires_bundle_local_provenance_link() -> None:
    document = _load_json("reproducibility-bundle-valid.json")
    document["figures"][0].pop("upstream_analysis_run_ids")
    document["figures"][0]["inputs"][0].pop("source_analysis_run_id")

    with pytest.raises(ProjectSchemaValidationError, match="bundled provenance link"):
        validate_reproducibility_bundle(document)


def test_validate_release_rejects_unknown_reproducibility_bundle_artifact() -> None:
    document = _load_json("invalid/release-unknown-reproducibility-bundle.json")

    with pytest.raises(ProjectSchemaValidationError, match="unknown artifact_id 'missing-bundle'"):
        validate_document("release", document)


def test_validate_release_rejects_citation_artifact_kind_mismatch() -> None:
    document = _load_json("invalid/release-citation-kind-mismatch.json")

    with pytest.raises(ProjectSchemaValidationError, match="expected 'citation-cff'"):
        validate_document("release", document)


def test_validate_release_requires_archive_for_published_status() -> None:
    document = _load_json("invalid/release-published-missing-archive.json")

    with pytest.raises(ProjectSchemaValidationError, match="'archive' is a required property"):
        validate_document("release", document)


@pytest.mark.parametrize(
    ("schema_name", "mutation_path", "bad_value", "expected_error"),
    [
        ("project", ("project", "created_at"), "2026/03/07", "is not a 'date'"),
        (
            "analysis-run",
            ("analysis_runs", 0, "started_at"),
            "2026-13-07T09:00:00Z",
            "is not a 'date-time'",
        ),
        ("corpus", ("holdings", 0, "collected_at"), "2026/03/08", "is not a 'date'"),
        ("citation", ("citations", 0, "verification", "access_url"), "not a uri", "is not a 'uri'"),
    ],
)
def test_validate_document_enforces_declared_formats(
    schema_name: str, mutation_path: tuple[object, ...], bad_value: str, expected_error: str
) -> None:
    if schema_name == "corpus":
        document = _load_json("corpus-valid.json")
        invalid_document = document
    else:
        document = _load_json("claim-set-valid.json")
        if schema_name == "project":
            invalid_document = document["project"]
        elif schema_name == "citation":
            invalid_document = document["citations"][0]
        else:
            invalid_document = document["analysis_runs"][0]

    target = document
    for part in mutation_path[:-1]:
        target = target[part]
    target[mutation_path[-1]] = bad_value

    with pytest.raises(ProjectSchemaValidationError, match=expected_error):
        validate_document(schema_name, invalid_document)


def test_validate_figure_enforces_generated_at_format() -> None:
    document = _load_json("figure-valid.json")
    document["generated_at"] = "2026-03-07 09:20:00"

    with pytest.raises(ProjectSchemaValidationError, match="is not a 'date-time'"):
        validate_document("figure", document)


def test_validate_release_enforces_archive_landing_page_url_format() -> None:
    document = _load_json("release-valid.json")
    document["status"] = "published"
    document["released_at"] = "2026-03-07T11:00:00Z"
    document["archive"] = {
        "service": "zenodo",
        "version_identifier": "10.5281/zenodo.1234567",
        "landing_page_url": "not a uri",
        "archived_at": "2026-03-07T11:30:00Z",
    }

    with pytest.raises(ProjectSchemaValidationError, match="is not a 'uri'"):
        validate_document("release", document)


@pytest.mark.parametrize(
    "schema_name",
    [
        "analysis-run",
        "citation",
        "claim",
        "claim-set",
        "corpus",
        "figure",
        "project",
        "release",
        "reproducibility-bundle",
    ],
)
def test_schema_ids_track_schema_version(schema_name: str) -> None:
    schema = load_schema(schema_name)
    assert schema["$id"].endswith(f"-{SCHEMA_VERSION}.json")


def test_bundle_schemas_track_schema_version_constant() -> None:
    claim_set_schema = load_schema("claim-set")
    reproducibility_bundle_schema = load_schema("reproducibility-bundle")

    assert claim_set_schema["properties"]["schema_version"]["const"] == SCHEMA_VERSION
    assert reproducibility_bundle_schema["properties"]["schema_version"]["const"] == SCHEMA_VERSION
