# Implementation Runbook

Use this file as the operational instruction set for Codex.

## Working rules

1. Follow `plans/master-plan.md` as the source of truth.
2. Work one milestone step or one GitHub issue at a time.
3. Keep diffs scoped.
4. Run validation before considering a task complete.
5. Update docs in the same branch as the implementation.
6. Append a short note to `plans/documentation.md` after each meaningful change.
7. After completing any Codex-authored scoped repository change, commit and push the current branch to GitHub before ending the task, unless a human explicitly says not to or pushing is blocked. Never bundle unrelated local changes in that push.

## Standard task loop

### 1. Read context
Read:
- `AGENTS.md`
- `plans/master-plan.md`
- relevant docs
- nearest package / template / skill directory

### 2. Define acceptance criteria
Write the acceptance criteria in the PR body or issue notes before implementing.

### 3. Implement
Prefer the minimum complete change.

### 4. Validate
At minimum:
```bash
make check
```

When code exists, also run the narrowest relevant validation such as:

```bash
pytest tests/test_project_schema.py
```

### 5. Sync docs
Update any changed commands, architecture notes, repo map, or product claims.

### 6. Log status
Add a note to `plans/documentation.md`:
- what changed
- why
- validation run
- follow-ups

### 7. Commit and push
After completing any Codex-authored scoped repository change, commit and push the current branch to GitHub before ending the task, unless a human explicitly says not to or pushing is blocked. Never bundle unrelated local changes in that push.

## Stop conditions

Pause and document before proceeding when:

- a change implies major scope drift
- a licensing decision is needed
- a dependency has long-term architectural implications
- there is policy ambiguity around AI, citations, or data handling
