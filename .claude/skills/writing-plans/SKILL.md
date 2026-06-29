---
name: writing-plans
description: Use when you have an agreed design or spec for a multi-step change, before touching code. Produces a concrete, step-by-step implementation plan.
---

# Writing Plans

Write an implementation plan precise enough that someone with no context for this
codebase could follow it: which files to touch per task, the actual code, the
exact commands to verify, and where it gets committed. Bite-sized tasks. DRY,
YAGNI, test-driven, frequent commits.

**Context:** Work happens on a `feat/`/`fix/` branch (no worktrees). The plan
lives in the Issue it implements (or the PR) — **never** in a separate plan file.

## Ground rules

A plan obeys the repo's existing rules — don't restate them, point to them: the
architecture, layer boundaries, and length limits live in CLAUDE.md (and
`backend/CLAUDE.md`, `frontend/CLAUDE.md`). Two operational reminders for the
steps you write: every task's verification is `make check` (or the layer's
`make backend` / `make frontend`), and the work finishes by opening a PR per
CLAUDE.md, carried out with the **executing-plans** skill.

## Bite-sized task granularity

Each step is one action (2–5 minutes), e.g.:
- Write the failing test
- Run it, confirm it fails
- Write the minimal code to pass
- Run the test, confirm it passes
- Commit

## Plan shape

Put the plan in the issue/PR with this header, then the tasks:

> **Goal:** [one sentence]
> **Approach:** [2–3 sentences]
> **Verification:** `make check` (or the relevant layer target)

### Task N: [name]

**Files:** Create / Modify (`exact/path:lines`) / Test (`exact/path`)

**Steps** (each its own line, with the exact command and expected result):
1. Write the failing test — `<test code>`
2. Run `cd backend && .venv/bin/python -m pytest tests/...::name -v` → expect FAIL
3. Write the minimal implementation — `<code>`
4. Re-run the test → expect PASS
5. `git commit -m "feat: ..."`

(Frontend tasks use `cd frontend && bun run test` with Vitest instead.)

## Remember
- Exact file paths and complete code — not "add validation".
- Exact commands with expected output; the final verification is `make check`.
- DRY, YAGNI, test-first, frequent commits, small tasks.
- When the plan is agreed, implement it with the **executing-plans** skill.
