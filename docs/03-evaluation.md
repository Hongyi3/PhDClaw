# Evaluation Plan

This project should not be judged by "looks useful" demos. It should be judged by research-software quality.

## Primary metrics

### 1. Reference integrity
Percent of generated references that resolve to real identifiers and valid metadata.

### 2. Unsupported-claim rate
Sampled rate of scientific claims that lack verified backing.

### 3. Reproducibility success
Rate at which clean environments can reproduce exemplar outputs from the release artifact.

### 4. Reporting completeness
Coverage of required reporting-checklist items for targeted study designs.

### 5. External reproducibility
Success rate for an external user rerunning an exemplar without maintainer intervention.

## Benchmark folders

- `benchmarks/gold-claims/`
- `benchmarks/literature-retrieval/`
- `benchmarks/reproducibility/`
- `benchmarks/reporting-completeness/`

## Release gates

A release candidate should fail if:

- references do not resolve
- claims are unsupported
- provenance manifests are incomplete
- exemplar reruns fail
- citation metadata is missing
