---
name: brainstorming
description: Use BEFORE any non-trivial creative work — a new feature, page, component, or behavior change — to turn a rough idea into an agreed design. Skip it only for simple, already-clear execution. Explores intent, constraints, and approach before any code.
---

# Brainstorming Ideas Into Designs

Turn a rough idea into an agreed design through plain, collaborative dialogue,
then capture it as a GitHub Issue. The person you are working with is
non-technical: keep the conversation about the *problem* and what success looks
like, not the implementation — this is CLAUDE.md's "How we work" stance applied
to a dialogue.

## The process

**Understand the idea**
- First look at the current state: relevant files, the README, recent commits.
- Ask questions **one at a time** — multiple choice when you can, open-ended when
  you must. Only ask what genuinely matters; if the conversation, the code, or
  CLAUDE.md already answers it, don't ask. If you have no real questions, say so
  and move on.
- Pin down: the problem, who it's for, the constraints, and what "done" looks like.

**Explore approaches**
- Propose 2–3 approaches with honest trade-offs. Lead with your recommendation
  and say why. Apply YAGNI — cut anything that doesn't serve the stated problem,
  unless the person is deliberately building toward a longer-term vision.

**Present the design**
- Once you understand what you're building, present it in small chunks
  (~200–300 words) and check after each: "does this look right so far?"
- Cover what matters for the change: the user-facing flow, where it lives in the
  architecture (which layers/files), the data flow, the error cases, and how it
  will be tested. Go back and revise when something doesn't fit.

## After the design

**Capture it as an Issue** (not a file — we never write plan/design markdown):
write it up per CLAUDE.md's Issues section — its three parts, scope tag, labels,
and assignment. Follow those rules there; don't repeat them here.

**If continuing to implementation:**
- Ask: "Ready to build?" Create a `feat/` or `fix/` branch (we do **not** use
  worktrees). Then use the **writing-plans** skill to turn the design into a
  concrete plan.

## Key principles

- **One question at a time** — don't overwhelm.
- **Only ask what's load-bearing** — this isn't an interview; if it's clear, build.
- **YAGNI ruthlessly** — the smallest design that solves the problem.
- **Always explore 2–3 approaches** before settling.
- **Validate in sections** — small chunks, confirm as you go.
- **Plain language** — the person is non-technical; talk about the problem.
