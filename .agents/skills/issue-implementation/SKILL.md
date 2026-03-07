---
name: issue-implementation
description: Use this skill when implementing one scoped repository issue or milestone step from the plan.
---

# issue-implementation

## Trigger

Use this skill when the task is to implement a **single** issue, milestone step, or tightly scoped repository change.

Do not use it for broad brainstorming or repo-wide rewrites.

## Procedure

1. Read `AGENTS.md`, `plans/master-plan.md`, and the linked issue or task.
2. Restate the acceptance criteria.
3. Inspect the nearest relevant files.
4. Make the minimum complete implementation.
5. Run the narrowest validation available.
6. Update docs affected by the change.
7. Append a short status note to `plans/documentation.md`.

## Output contract

Return:
- what changed
- validation run
- files touched
- any follow-up work left intentionally out of scope
