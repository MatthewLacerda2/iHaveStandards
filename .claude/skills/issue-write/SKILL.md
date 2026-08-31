---
name: issue-write
description: Write an issue for this repo — what makes each of its three parts good, which labels it carries, and when Claude may file one unprompted. Use when filing an issue, splitting an idea into issues, or deciding whether something noticed mid-work deserves one.
---

# Writing an issue

The unit of work here is a well-specified issue. A future Claude reads it **cold**
and says *"I understand the assignment, I know how to proceed."* That is what lets
an issue be worked without the person who asked for it sitting there to be asked.

CLAUDE.md's *Issues* section owns the mechanics — the three parts, the
`[V]`/`[SF]`/`[RE]`/`[OT]` title tag, the labels, assignment. Don't restate
them. This skill is
the judgement they don't carry: what makes each part good, and when to refuse.

**Reaching agreement on the idea is the `brainstorming` skill's job, not this
one.** Come here once the idea is agreed — or when nobody agreed anything because
you found the thing yourself mid-work.

## What makes the three parts good

- **Context** — the problem, and what we want once it's addressed. This is the
  half that survives. An issue whose reasoning is written down can be re-judged
  when circumstances change; one without it can only be obeyed or ignored.
- **Suggestion** — the shape of the work, *not* the implementation intrinsics.
  Name the decisions the implementer must make and leave them theirs. Say what is
  explicitly **out of scope**; a boundary stated once saves an argument later.
  CLAUDE.md is clear that the Suggestion may not survive contact with the code —
  write it as the best current guess, not as a spec to be defended.
- **Definition of done** — what the resulting PR delivers, in terms someone can
  check. "`make check` green" is table stakes and not a definition of done on its
  own. What should a person be able to *do* that they couldn't before?

**Evidence beats assertion.** An issue that quotes a real file, a failing test, a
lint rule, an error the app actually printed, is one nobody has to re-derive.
"`lib/schemas/items.ts` still has `title` but the backend renamed it to `name` in
`schemas/items.py`" is worth more than "the schemas are out of sync".

**Cite what it relates to.** Sibling issues, the PR that exposed it, the rule in
CLAUDE.md it turns on. A future reader arrives with no memory of today.

**Write it in the language of the product.** The person who owns this repo may
not read code. The Context must make sense to them; the Suggestion may get
technical, and should stay short when it does.

## The three gates

An idea becomes an issue only when all three hold. If any fails, **push back
instead of complying** — CLAUDE.md's *Push back on dead weight* is a duty, not a
permission.

1. **Understanding.** You can restate the *problem*, not just the solution being
   asked for. If your restatement is only their words handed back, you don't have
   it yet — ask one more question. Don't guess and build.
2. **Value.** It moves the product. The failure mode here is a solution polished
   before the problem is pinned down; when you see it, say so and go back to the
   problem.
3. **Craft.** It can be built inside this repo's decided shape: the backend's four
   layers in one direction with DB access only in `repositories/`; pages that
   never fetch, only `lib/api/`; the color and typography allowlists; every
   user-facing string through `i18next`; the file, handler and test length limits;
   every gate in the `Makefile` and nowhere else. If the idea can only be built by
   breaking one of those, say so and propose the shape that doesn't. If it can
   only be built by *changing* one of those, that's a `refactor` issue of its own,
   and it goes first.

## Filing what you notice

Claude may open an issue autonomously, and should, for anything that will recur
or that a tool would solve more than once — provided the benefit outweighs the
cost of building it.

**A `fix` is always filable.** The test above is about whether something is worth
*building*; it is never about whether a defect is worth *recording*. Keep the
description brief and carry on. If the defect questions a decision or exposes a
foundational crack, tell the user — that part is a judgement call.

The strongest issues come out of doing the work: a claim in CLAUDE.md that quietly
became false, a gate that stopped meaning what it says, a translation key added to
`en.json` and never to `pt.json`. Those are findings, and findings are cheap to
lose.

**File rather than fix** when the thing found is outside the branch in hand. A
branch that grows to cover everything it noticed is a branch nobody can review —
and here, one nobody can *describe* in the PR's four sections.

## Labels

**Stage labels are the only absolute stop, and at most one applies. Absence means
ready.**

- `idea` — might not be worth doing; parked until the user decides. **Never
  started.**
- `planning` — worth doing, but we don't yet know how. **Never started.**
- `human` — needs a person in the loop end to end. **Never started.**
- *(none)* — anyone can say "do issue N" and an agent can take it from there.

**The judgement lives in the label**, so put it on honestly. Broad or vague is
what `planning` is for. A Claude-written issue **must** carry one of the three if
it is a breaking change, changes what the user sees or types, needs a judgement
call, or changes a decided convention.

A `fix` usually should **not** carry one — it is specific, the deciding already
happened when the thing broke, and nothing is gained by making it wait.

Primary labels (one at least): `feat` · `fix` · `refactor`. Additive, alongside a
primary: `docs` · `idea` · `planning` · `human`. `minor` may appear alone or with
anything, and means the fix is small enough to ride along in another issue's PR.

## Priority

**refactor → fix → feat.** `docs` never waits its turn.

That order is CLAUDE.md's *Foundations come first* applied to a queue: `refactor`
changes how we do things, so everything built before it lands gets built the old
way and rewritten later. It is also the label that touches the most files, so
landing it first is the rebase nobody else has to pay.

Priority orders what gets **merged**, not what gets **worked**.

## Relationships

Use GitHub's **Blocked by / Blocks**, and **sub-issues** when one is literal
groundwork for another. Link when one lays groundwork, makes the next meaningfully
easier, or would conflict too much if done at the same time.

**The dependency graph is the plan** — there are no rigid batches.

**Do not split for parallelism.** If a parent's sub-issues all touch the same
files, they are one issue; the `issue-batch` skill has why that costs more than it
saves here.

**Backend and frontend halves of one change are one issue.** Nothing in this repo
checks that `frontend/src/lib/schemas/` still matches `backend/schemas/`, and CI's
path filters mean a backend-only PR never runs the frontend gates at all. Split
across two issues, the two halves are green separately and broken together, and no
gate anywhere will say so. This is the single most expensive split available.

If a `planning` issue would change how another is implemented or thought of, mark
that other one **blocked by** it.

## Closing

The PR title is `{issue_number}-{branch_name}` and the body opens with
`Closes #{issue_number}` — and **check the number**. A typo'd `Closes #N` closes
the wrong issue, or none, silently, and nothing verifies it.
