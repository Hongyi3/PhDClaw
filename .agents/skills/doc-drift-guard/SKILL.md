---
name: doc-drift-guard
description: Use this skill when code, structure, commands, or scope changed and repository docs may now be stale.
---

# doc-drift-guard

## Trigger

Use this skill whenever implementation changes affect:
- commands
- repository structure
- architecture
- public positioning
- scope
- examples
- release or validation instructions

## Procedure

1. Find every doc impacted by the code change.
2. Update the docs in the same branch.
3. Remove stale claims or counts.
4. Keep wording precise and professional.
5. Ensure README, architecture docs, and plan docs do not contradict each other.

## Output contract

List:
- docs updated
- stale claims removed
- any docs still intentionally deferred
