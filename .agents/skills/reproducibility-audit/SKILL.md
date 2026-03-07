---
name: reproducibility-audit
description: Use this skill when reviewing workflow, provenance, or release artifacts for reproducibility completeness.
---

# reproducibility-audit

## Trigger

Use this skill for any task involving:
- workflow manifests
- provenance
- run metadata
- reproducibility bundles
- figure or table regeneration
- release-readiness checks

## Audit checklist

- are inputs identifiable?
- are outputs linked to a run?
- are parameters and environment captured?
- is there a rerun path?
- are checksums or equivalent integrity data present?
- can a future user reconstruct the output without the agent?

## Output contract

Return:
- pass / fail assessment
- missing metadata
- exact remediation actions
