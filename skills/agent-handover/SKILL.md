---
name: agent-handover
description: How to preserve task state and end a session without losing its reasoning — checkpoints, context-pressure recovery, and durable handovers rather than arbitrary token cutoffs. Use when assessing context usage or a restart rule, when compaction or missing constraints threaten continuity, when asked to wrap up or hand off, when creating a successor, when finishing work, or when writing, updating or reading a HANDOVER file.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Handing over

A session ends. Everything it learned that is not written down ends with it.

Two things are being defended at once and they pull against each other: the
successor needs to know where things stand, and the successor must not be
*misled* by a summary that can omit constraints or lag behind the repository.

## Write it before you are forced to

> **Checkpoint while continuity is intact. Recover from observed context
> pressure or lost task state, not a guessed session lifetime.**

At meaningful work boundaries, record decisions, rejected approaches, pending
work and verification limits in the owning docs or work items. Keep the handover
as pointers to that durable state. Do not wait for a warning to preserve the
reasoning needed to recover; the handover itself is an editing task.

Capacity warnings, missing constraints, contradictory decisions and repeated
re-discovery are reasons to pause and re-check continuity. Re-read authoritative
instructions, relevant decisions, working-tree state and pending actions before
continuing. These symptoms call for recovery even without proof that context
length caused them.

If relevant work remains and the runtime supports it, compaction can relieve
capacity pressure. Preserve durable state first and re-check it afterwards:
**compaction is not lossless, and a larger window does not guarantee quality.**
If sufficient room or coherent task state cannot be restored, hand off the
unfinished work with explicit unknowns. Use fresh context for unrelated work;
resuming a session is not necessarily a fresh-context reset.

**Do not create a successor for completed work.** For a necessary handoff,
identify the unfinished scope and follow `agent-concurrency`: one writer per
working tree, explicit ownership, and the project's admission and retirement
rules. Never remove a live session's tree, including your own.

### Name the counter before acting on it

When context pressure affects the next step, report the runtime's current
occupancy, effective model/tier and counter source if available, including any
response reserve relevant to the reading. If unavailable, say so rather than
manufacturing a count or percentage.

Do not substitute cumulative session or billed usage, transcript/corpus size
estimates, or advertised capacity for current active context. **Routine commits
and pushes do not require a token report.** Budget for read-in by measuring its
actual prompt boundary separately from the corpus; label estimates as estimates.

No universal restart count or percentage is established by the reviewed
evidence. Do not replace the old cutoff with another guess. A quantitative local
policy needs a defined counter, runtime/model/tier and comparable outcomes,
including recovery cost. The public sources and limits are in
[CONTEXT-HANDOFF-EVIDENCE.md](references/CONTEXT-HANDOFF-EVIDENCE.md);
they are not measurements of a private desktop runtime.

Durable reasoning makes recovery possible, not cost-free. If handing off needs
reconstruction, preserve what is missing before leaving it to another session.

## It is a file in the repository, not a message

> **A handover passed session-to-session in a kickoff prompt is one lost message
> away from gone.**

A file is read by whoever turns up next, survives a session nobody resumed, and
shows up in a diff when it goes stale. A message has none of those properties,
and the handover is the most droppable artefact a project has.

## It is the one document allowed to be wrong

State this inside the file, in the file's own voice:

> **Do not trust this file over the docs.** It is one session's summary of where
> things stood when it stopped. The docs are reasoned and gated; this is a note.
> If they disagree, the docs are right and this is stale — fix it.

That sentence is what makes the file safe to write quickly, and what stops a
successor building on a stale summary. Without it a handover accumulates
authority it never earned, and the reasoned documents stop being read at all.

The corollary is a rule for the writer:

> **Anything load-bearing goes in a doc first, and the handover links to it.** A
> decision reachable only from the handover is in the wrong place.

## Say how to re-check; do not quote what rots

Every status figure in a handover has an expiry date. Branch names, commit
counts, how many items are open, whether the tree is clean — all false within a
day, and all reading as current forever.

Give the command instead of the answer:

| | How to check |
|---|---|
| Branch | `git branch --show-current` |
| Recent work | `git log --oneline -12` |
| Unpushed | `git log --oneline origin/main..main` |
| Open pull requests | `gh pr list` |
| Working tree | `git status --short` |
| Who else is here | the session list, plus the open-items directory for claims |
| The gate | the verification command, and what its exit code means |

A command is self-dating. It cannot report last week's state.

## Say what you did not verify

> **A successor assumes anything unmentioned was done.**

Give this a heading of its own so it cannot be quietly omitted, and state the
*boundary* of what was checked rather than the effort spent:

- Not "tested in a browser" but which browser, at which widths, against which
  environment — and what was never opened.
- Not "the gate passes" but what the gate does not cover: network fetches, data
  rebuilds, real rendering, migrations.
- Anything you could not do because you were sandboxed, firewalled, or missing
  credentials. **Hand that check back explicitly** rather than concluding the
  suite was sufficient. See the `verify-in-the-real-thing` skill.

With several agents reading the file at once, an unstated omission is assumed
done in parallel.

If delivery is in scope, separate the boundaries rather than writing "shipped":
reviewed head, gated head, merged revision, deployment run, and observed runtime
identity. Record an expected refusal, such as an exact-head mismatch, as a safety
outcome rather than collapsing it into "failed."

## Settle what is open before you go

> **Ask every open design question while you still have the context to argue
> about it.** A question left for the successor is one it must answer with less
> of the reasoning than you have.

What genuinely cannot be settled does not go in the handover as a paragraph. It
goes in its own file, with **the recommendation and the reasoning**, so the next
agent inherits an argument rather than a blank — and can *claim* it, which a
paragraph cannot be. See the `agent-concurrency` skill for the claim protocol and
the four states.

## Finish by pushing

Work that is done is committed and pushed before the session ends. Not staged,
not left modified, not described in the handover as "ready to commit".

> **A session that stops with uncommitted work has not finished it — it has moved
> it somewhere less safe than where it started.**

A dirty working tree is invisible to everyone except the tree it sits in, and in
a shared checkout it belongs to whoever commits next. If work genuinely cannot
land — unfinished, or a decision is outstanding — **commit it to a branch and say
so in the handover.** An unpushed branch is recoverable; a dirty tree is not.

When a person is driving the session, ask before committing on their behalf, then
commit and push what they approve rather than leaving it for them.

## Keeping the file honest

Four rules, and they belong *inside* the handover as its last section so whoever
edits it next reads them:

- **Update it before you hand off, not after you are asked.** It is worth exactly
  as much as its last edit.
- **Anything load-bearing goes in a doc first.**
- **Settle open questions while you still have the context to argue about them.**
- **State what you did not verify.**

## Structure

`assets/HANDOVER-template.md` is the shape, ready to copy. In outline:

1. A pointer to the instructions file and the docs, and the *do not trust this
   over the docs* warning.
2. **Where things stand** — commands to run, not figures.
3. **What is open** — a pointer to the open items, not a list.
4. **Who continues this**, if anybody, and where their work will appear. If
   nobody was created, say so and why: silence reads as a successor that exists,
   and the project waits for an agent nobody made.
5. **What was not verified.**
6. **Delivery identity**, when the work was meant to land or deploy — pull
   request and base, reviewed/gated head, merged revision, exact deployment run,
   and observed build identity. Write "not observed" rather than inferring one
   boundary from another.
7. **Where the reasoning lives** — links only.
8. **Keeping this file honest.**

## What a handover is not

- **Not a substitute for the docs.** If it is the only place something is
  explained, move it.
- **Not a plan for the successor.** Handing over a phase the next session did not
  choose wastes the one advantage it has, which is reading the current state with
  fresh context. Point at what is open and let it pick.
- **Not a changelog.** `git log` already exists and does not go stale.
- **Not a place to be reassuring.** The value is concentrated entirely in the
  parts that admit something.

Why each of these is the rule, and the failures behind them, is in
[references/REASONING.md](references/REASONING.md) — read it when arguing about
one of them, not to apply them.
