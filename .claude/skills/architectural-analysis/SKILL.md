---
name: architectural-analysis
description: Use for an architectural health audit — cross-file duplication, layer/architecture violations, dead code across files, and poor cohesion. Run it after a refactor or a major feature, before marking a PR ready for review. Read-only: it reports, it never edits; focuses on what the quality gates can't catch.
---

# Architectural Analysis

A read-only audit of structural health. **It never edits files** — it reports
findings (in chat, or as a GitHub Issue if action is warranted). We do not write
audit report files.

## Start here: don't re-audit what the gates already enforce

`make check` already fails on a lot, so don't spend effort re-finding it:
- **Backend** (ruff + `house_lint.py`): unused imports/vars (`F`), missing type
  annotations (`ANN`), bugbear smells (`B`), files > 350 lines, handlers > 50,
  tests > 50.
- **Frontend** (ESLint): unused vars, raw color literals, hand-rolled form
  controls, non-token typography, files > 550 lines, one component per file.

Spend your effort on what the linters **can't** see across the whole codebase:

1. **Layer / architecture violations** (the rules linters don't encode)
2. **Cross-file duplication** (the same logic in several places)
3. **Cross-file dead code** (exported, imported nowhere)
4. **Poor cohesion** (a file doing too much, even under the line limit)

## Architecture violations to hunt

The rules themselves live in CLAUDE.md (and `backend/CLAUDE.md`,
`frontend/CLAUDE.md`) — read them there. Your job is to find where the code
breaks them. Common violations:

**Backend** (the 4-layer rule): DB access (SQLAlchemy queries / sessions)
anywhere but `repositories/`; a repository opening its own session instead of
taking one (breaks the test rollback); business logic stuck in a handler.

**Frontend** (pages never reach the network): a route or component calling
`fetch` instead of the typed SDK; auth/token handling outside `client.ts`;
`lib/schemas/` drifting from the backend models.

## The process

1. **Map the codebase.** Glob the backend (`backend/**/*.py`) and frontend
   (`frontend/src/**/*.{ts,tsx}`). Make a checklist so coverage is systematic.
2. **Check layer boundaries.** Grep for the violations above (e.g. DB/session
   imports outside `repositories/`; `fetch(` or network calls under `routes/` or
   components). Read each suspect — confirm it's real, not a false positive.
3. **Find duplication.** Look for the same logic in multiple places (similar
   helpers, repeated blocks, parallel implementations of one concept). Read each
   candidate; confirm the logic is truly the same before flagging.
4. **Find cross-file dead code.** For exported symbols, check whether anything
   imports them anywhere. Account for legitimate non-import use (public API,
   dynamic access, framework hooks, tests) before calling it dead.
5. **Spot poor cohesion.** Files that mix unrelated responsibilities even within
   the length limits — candidates for splitting.

For every finding, record: where it is, why it's a problem, your confidence
(high / medium / low), and a concrete recommendation. Verify before you flag —
default to caution when unsure.

## Reporting

Summarize in chat, grouped by category (layer violations → duplication → dead
code → cohesion), highest-impact first, with `file:line` references and
confidence. If the findings warrant work, offer to open an **Issue** (Context /
Suggestion / Definition of done) — don't start fixing inside this skill.

## Principles
- **Read-only** — never edit, never "just fix it" here.
- **Be systematic** — cover the whole tree; track progress with a checklist.
- **Verify before flagging** — confirm duplicates and dead code are real.
- **Skip what the gates already catch** — add signal, don't repeat the linters.
- **No report files** — findings go in chat or an issue.
