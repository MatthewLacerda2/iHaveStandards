---
name: executing-plans
description: Use when you have an agreed implementation plan to carry out. Executes it in small batches with a review checkpoint between batches.
---

# Executing Plans

Load the plan, review it critically, execute in small batches, and report between
batches for review. Work on the `feat/`/`fix/` branch (no worktrees).

## The process

**1. Load and review**
- Read the plan (from the issue/PR it lives in).
- Review it critically — note any gaps, risks, or unclear steps.
- If you have concerns, raise them before starting. Otherwise create a task list
  and proceed.

**2. Execute a batch** — default: the first 3 tasks. For each task:
- Mark it in progress.
- Follow the steps exactly (the plan is bite-sized for a reason).
- Run the verification the plan specifies; the overall gate is `make check`
  (or `make backend` / `make frontend` for the layer you touched).
- Mark it done.

**3. Report** — when the batch is done, show what changed and the verification
output, then say "Ready for feedback."

**4. Continue** — apply any feedback, then run the next batch. Repeat until done.

**5. Finish** — when all tasks are done and `make check` is green, open the PR per
CLAUDE.md's Pull Requests section (it covers the title, the four sections,
assignment, and "never merge without the user's say-so"). Don't duplicate those
rules here.

## Stop and ask when
- You hit a blocker mid-batch (a missing piece, a test won't pass, a step is unclear).
- The plan has a gap that prevents starting.
- A verification fails repeatedly.

Don't force through blockers and don't guess — stop and ask.

## Remember
- Review the plan critically first.
- Follow steps exactly; don't skip verifications (`make check`).
- Between batches: report and wait.
- Finish through a PR, per CLAUDE.md.
