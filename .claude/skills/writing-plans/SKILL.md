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

## This repo's ground rules (bake them into every plan)

- **Verification is `make check`** (or `make backend` / `make frontend` for the
  layer you touched). That single gate is lint + build + tests; CI runs the same.
- **Backend** (Python, FastAPI): respect the 4 layers — `api/` → `schemas/` →
  `repositories/` → `models/`, with `services/` for logic. DB access lives only in
  `repositories/`. Files ≤ 350 lines, handlers ≤ 50, tests ≤ 50. Tests use
  `pytest` and roll back. Type annotations are required (ruff `ANN`).
- **Frontend** (React, Bun): pages never `fetch` — they call `lib/api/<domain>.ts`,
  which calls the one `client.ts`. Use the design-system tokens and ShadCN
  primitives (raw colors / hand-rolled inputs fail lint). Tests use Vitest.
- **Finish** by opening a PR per CLAUDE.md (four sections; assign the user; close
  the issue). Carry the plan out with the **executing-plans** skill.

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
