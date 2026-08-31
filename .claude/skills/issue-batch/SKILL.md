---
name: issue-batch
description: Run a set of issues from board to merged — what order, which ones can safely share a branch, and the concrete path a branch takes to land here. Use when starting work on one or more issues, when deciding what to start next, or when told to "do the issues".
---

# Working a batch of issues

The user rarely has one issue. An idea becomes several, and more appear as coding
starts. This is how a set of them gets worked without the batch costing more than
the work.

Inside a single issue, the **writing-plans** and **executing-plans** skills own
the work: plan, batches, verification, PR. This skill owns everything outside
that — which issue is next, what must not share a branch, and what happens after
`make check` goes green. Hand off to them at "ready to build", pick it back up at
"the PR is open".

## One issue at a time, and the arithmetic agrees

CLAUDE.md's *Branches workflow* says we work one thing at a time. That is also
what the numbers say here, so nobody needs to re-derive the industry default of
many branches in flight and propose the tooling that goes with it:

- **CI is not the bottleneck.** The two workflows run concurrently and finish in
  **20–40 seconds** on this repo's own history. Pipelining a second branch to hide
  that wait buys nothing, and every branch that is not first still pays a rebase
  for each merge ahead of it — over shared code that is N(N−1)/2 rebases, and a
  rebase buys no correctness.
- **Nothing links across the two halves.** Python and TypeScript each type-check
  themselves; there is no build step that fails only when two branches are put
  together, which is what would make a merge queue worth building.
- **What replaces it is worse, not better.** `frontend/src/lib/schemas/` and
  `lib/api/` hand-mirror `backend/schemas/`, and **nothing checks the mirror**.
  The workflows are path-filtered, so a PR touching only `backend/**` never
  runs the frontend gates and vice versa. Two branches can be green apart and
  broken together and no gate will ever say so. The answer to that is scoping
  — see *Group the work* — not a queue.

So the batch is **sequential**: take the next issue, carry it to merged, then look
again. What is scarce here is attention and collisions, not CPU.

## The files where everything collides

A clean rebase is seconds of `git`; a colliding one is a whole session. These are
the files every second change appends to, and two branches landing in one at once
is the case to avoid:

- `frontend/src/i18n/locales/{en,pt,es}.json` — three bundles, every user-facing
  string, and **no gate checks that a key added to one exists in the others**. A
  merge that keeps one side silently drops translations.
- `backend/api/endpoints.py` — every new resource appends a router include.
- `frontend/src/routes/__root.tsx` and `frontend/src/styles.css` — the layout and
  the design-system token allowlists.
- `frontend/bun.lock` and `backend/requirements*.txt` — **never hand-merge a
  lockfile.** CI installs with `--frozen-lockfile`, so a plausible-looking
  resolution fails there and nowhere else. Take one side, re-run `bun install`,
  commit the result.
- `frontend/src/routeTree.gen.ts` — **generated**, and it says so in its own first
  lines. Never resolve it by hand: take either side and let `bun run dev` or
  `bun run build` rewrite it.
- `.env.example` — appending is fine; making a new setting *required* breaks every
  other checkout on the next pull, so say so in the PR.

**Downstream repos add two more.** Once this template's deferred upgrades land
(see CLAUDE.md's *Upgrade paths*), Alembic's revision chain is genuinely
serial: two branches each writing a migration produce two heads, and that is a
real reason to land one before starting the other. A single deploy target, once
there is one, is the other. Neither exists in the template as shipped; if your
repo has them, they outrank everything above.

## Group the work before splitting it

**Split by responsibility, not by parallelism.** If a parent's sub-issues all
touch the same files, they are **one branch**, not one each.

Splitting an issue so several agents can run at once optimises the half that was
never scarce, and manufactures collisions: four sub-issues each appending to
`en.json` is four rebases and four PRs for one coherent change.

**A change that crosses backend and frontend is one branch and one PR.** Because
of the path filters and the unchecked schema mirror, splitting it is the one split
that can put a broken `main` past every gate we have.

Sub-issues are for work that is genuinely separable *in the code* — not for work
that is merely listable.

## Starting

- **Assign the user the moment work begins** — CLAUDE.md's rule, and unassigned is
  what "free for grabs" means. **Unassign** if it turns out the issue was never
  started.
- Branch `feat/…` or `fix/…` off the latest `main`, named after what it does. **A
  branch, not a worktree** — CLAUDE.md's *Branches workflow*.
- Do **not** open the PR until there is something to review. A draft PR here
  runs **no CI at all** (both workflows carry `if: !draft`), so a draft is a
  claim about nothing, not an early safety net.

## The path to merged

Once the work is done and the plan's tasks are finished:

1. **`make check` green locally.** Scope to the layer while iterating
   (`make backend` / `make frontend`); run the whole thing before the PR. CI
   invokes these exact targets — that is the point of the `Makefile`.
2. **Rebase on the latest `main`** and push.
3. **Open the PR ready for review, not draft.** Title `{issue_number}-{branch}`,
   body opening `Closes #N` and structured as CLAUDE.md's four sections
   (Context / Solution / Surface / Result). Assign the user; link the issue.
4. **Read which checks were *supposed* to run.** `backend` runs on `backend/**`,
   `frontend` on `frontend/**`, both on `Makefile`. A PR touching only docs,
   `CLAUDE.md` or `.claude/` runs **neither**, and zero checks there is the
   correct answer, not a failure. Zero checks on a PR that *did* touch
   `backend/**` means the run has not appeared yet — usually because the PR
   was readied seconds after the push. Wait for it; never treat absent as green.
5. **Merge only on the user's say-so.** CLAUDE.md is unambiguous: once that say-so
   is given, carry it through without pausing — push, wait for green, merge. If CI
   fails, stop and report rather than improvising.
6. **Delete the branch.**

A red PR that is already ready **stays ready** and is fixed in the next commit.
Draft is for work that is genuinely unfinished or handed over — which is exactly
CLAUDE.md's "if you can't finish" case: push what you have, mark it draft, comment
the bottleneck, tag the user.

## Re-read the board after every merge

A merge changes the graph. Whatever the merged issue blocked is fair game the
moment it lands, so the decision is one merge wide, not one batch wide. Re-read,
then apply priority — **refactor → fix → feat**, `docs` any time.

**A stage label is the only absolute stop.** `idea`, `planning` and `human` mean
*not yet*, and no amount of the issue looking ready overrides that; only the user
removing the label does. Everything else is startable the moment it exists,
including an issue filed a minute ago.

## Briefing a subagent

Point it at `CLAUDE.md` first — plus `backend/CLAUDE.md` or `frontend/CLAUDE.md`
for the layer it is in — then the issue. Issues here are written to be read cold.
Beyond that:

- Name the **base commit** and what landed recently that it must respect.
- Tell it the verification is `make check`, and that it must **not merge** —
  merging needs the user's say-so and belongs to the session running the batch.
- Tell it to use **writing-plans** and **executing-plans** rather than restating
  those protocols, and **architectural-analysis** before readying a refactor or a
  large feature.
- **Scratch filenames must carry the issue number.** A shared scratchpad has
  already swapped one PR's description for another's.

## Model, as a hint

Judgement work — design, deciding what a feature should do, triage — wants the
strongest model. A rebase, an import list, a translation key copied into two more
bundles does not. The line is not crisp, so err upwards.

## When to hand back to the user

The person who owns this repo is not a developer. That changes what a hand-back is
for: **a question they can answer is about the product** — what should happen, who
it is for, what a thing is called, whether it is worth doing at all. **A question
about the code is yours.** A type, a file layout, a library choice, a test
strategy, how to name a variable: decide it, do it, and say in the PR's *Solution*
which way you went and why. If the only way you can phrase a question is in
jargon, it is not theirs to answer — answer it yourself.

Hand back when:

- ≈3 attempts at the same failure. Say what you tried; do not thrash.
- The decision is genuinely theirs — anything a `planning` or `human` label would
  have carried, anything that changes what the user sees or types, anything that
  reverses a decision the issue already made.

Then: push what exists, leave the PR **draft**, comment the bottleneck on the PR,
tag the user, and stop.

If nobody is there to ask, prefer leaving the question as a comment on the issue
and moving to the next issue over stalling on it.

## Reporting back

The user is not reading the transcript. Report in the language of the product, not
the diff.

**When things went well, say what the result is** — what they can now do that they
could not. **When something surprised you, say what the surprise was.** That does
not mean things went badly; we write it down because the more we can predict, the
better we get.

Two things interrupt a running batch rather than waiting for the report, because
they are the ones the user would want to overrule while overruling is still
possible: **a change to files outside this repo**, and **a decision reversed** —
where the issue said one thing and the branch did another.
