---
name: agent-handover
description: How to end a session so the next one does not start from nothing — what a handover file contains, what it must not contain, when to write it, and why it is a file in the repository rather than a message. Use when a session is running low on context, when asked to wrap up or hand off, when creating a successor session, when finishing a piece of work, when writing or updating a HANDOVER file, or when starting a session and deciding how much of a handover to believe.
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
*misled* by a note written by whoever had the least context left of anybody who
worked on it.

## Write it before you are forced to

> **Stop and hand off at a context threshold you set in advance. Do not wait to
> be asked.**

The edits made late in a long session are exactly the small careful ones that go
wrong when context is thin — and the handover itself is an editing task.

Two supports make the threshold real rather than aspirational:

- **Report context usage after every major commit or push**, so the decision to
  hand off is never made solely by whoever is deepest in the work.
- **Budget for the read-in.** A project whose instructions prescribe reading
  several thousand lines has spent part of every session's budget before any work
  happens. If nobody has measured how much, say so rather than assume it is
  small.

Handing off is cheap *because* the reasoning lives elsewhere: in the docs, in the
instructions file, in the open items. If handing off feels expensive, that is the
symptom — something load-bearing exists only in the session.

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
6. **Where the reasoning lives** — links only.
7. **Keeping this file honest.**

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
