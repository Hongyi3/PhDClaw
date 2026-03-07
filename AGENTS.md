# AGENTS.md

This file defines the working contract for Codex and any other coding agent operating in this repository.

## Mission

Build **ClawBio Scholar** into a professional, publication-grade, open-source research operating system for biomedical PhD workflows.

The target outcome is not "more AI features." The target outcome is:

- evidence-grounded claims
- reproducible analyses
- provenance-complete figures and tables
- thesis/article-ready outputs
- citable, archivable software releases

## Non-negotiables

1. **Do not widen scope casually.** Stay focused on biomedical / computational-biology PhD workflows unless a human explicitly changes scope.
2. **No fake citations, ever.** Any literature-facing feature must verify identifiers and source resolution.
3. **Reproducibility beats convenience.** Prefer deterministic workflows, explicit metadata, and rerunnable outputs.
4. **Keep unpublished work local-first.** Default to local handling and explicit network boundaries.
5. **Keep diffs scoped.** One issue or one milestone step per change set.
6. **Synchronize docs with code.** Code changes that affect behavior must update the relevant docs in the same branch.
7. **Do not silently introduce new product claims** in README, docs, or UI that are not backed by implementation.
8. **Use placeholders honestly.** When a file is a template or stub, label it clearly.
9. **Push completed Codex changes.** After completing any Codex-authored scoped repository change, commit and push the current branch to GitHub before ending the task, unless a human explicitly says not to or pushing is blocked. Never bundle unrelated local changes in that push.

## Source-of-truth files

Before starting work, read these files in order:

1. `README.md`
2. `plans/master-plan.md`
3. `plans/implement.md`
4. `plans/documentation.md`
5. relevant file(s) in `docs/`
6. relevant skill instructions in `.agents/skills/`

## Execution style

When implementing:

1. restate the exact issue or milestone step in your own words
2. inspect the nearest existing code and docs
3. make the smallest coherent change that solves the problem
4. add or update validation
5. update docs that changed behavior, commands, architecture, or scope
6. append a short status note to `plans/documentation.md`

## Repository conventions

- Prefer Python for core packages and validation tooling.
- Prefer Quarto for manuscript, thesis, and docs templates.
- Keep package boundaries explicit.
- Keep schemas and metadata machine-readable.
- Favor plain text artifacts (`.md`, `.json`, `.yaml`, `.qmd`) over opaque formats.

## Forbidden shortcuts

- no hallucinated bibliographies
- no "temporary" hidden credentials in code or docs
- no vague TODO-only implementations merged as complete
- no breaking changes to repo structure without updating the plan docs
- no replacing a standards-based workflow with a black-box shortcut

## Validation checklist for every non-trivial change

- [ ] scoped to one issue / milestone step
- [ ] docs updated where relevant
- [ ] validation added or updated
- [ ] changelog or status note added in `plans/documentation.md`
- [ ] no unreviewed placeholder claims
- [ ] no fake citations or unverifiable references introduced

## Where to put things

- product architecture -> `docs/01-architecture.md`
- roadmap and milestones -> `docs/02-roadmap.md` and `plans/master-plan.md`
- evaluation logic -> `docs/03-evaluation.md` and `benchmarks/`
- release and archival logic -> `packages/release-engine/`
- policy and integrity checks -> `packages/policy-checks/`
- user-facing ClawBio Scholar skills -> `scholar-skills/`
- Codex-only helper skills -> `.agents/skills/`

## Escalation rules

Escalate to a human by leaving a crisp note in `plans/documentation.md` when you hit:

- licensing uncertainty
- policy uncertainty
- scope change requests
- dependency choices with long-term consequences
- external-service decisions that affect privacy or maintenance burden

## Definition of done

A milestone is done only when it is implemented, documented, validated, and reflected in the status log.
