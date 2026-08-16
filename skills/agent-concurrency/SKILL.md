---
name: agent-concurrency
description: Protocol for multiple AI agents working on the same repository without destroying each other's work — claiming tasks, isolating working trees, landing changes through reviewed pull requests, and distinguishing tasks from refusals. Use when running agents in parallel, delegating to sub-agents, enabling scheduled or heartbeat runs, creating a successor or background session, picking up work from a shared backlog, opening or merging a pull request, being asked to approve or review a change, setting up branch protection or required checks, or when asked to "finish whatever is pending".
license: MIT
compatibility: The claim protocol needs git. The tree lock is a POSIX sh pre-commit hook. The listing script needs Node 20+ with TypeScript execution (node >= 22.6 or tsx).
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Working alongside other agents

For any repository where more than one agent may be active: parallel sub-agents,
scheduled or heartbeat runs, background tasks, a successor session, or simply a
human who opens two windows.

**Check who is here before assuming either way.** List the active sessions and
the working trees. That is cheaper than the mixture a shared tree produces.

## The mechanism, in one line

> **One agent, one working tree, one branch, landing as a pull request.**

That is the settled answer, and everything below is either the reasoning for it
or the backstop for when somebody does not follow it.

    git worktree add ../proj-<name> -b <branch>

A worktree is a checkout nothing else has a share of, it is already on its own
branch, and its work arrives as a reviewable pull request rather than as commits
appearing on the trunk. A session with no local tree at all — a cloud or remote
task — has the same property.

**An in-place session on the shared checkout is the thing to avoid.** It is
right for a person driving it and for reading. It is wrong for anything running
unattended.

### This rule moved three times, and the history is the useful part

Worth having rather than obeying, because each reversal was a reasonable
response to the previous failure:

1. **"Create the successor yourself, don't ask"** — because asking had gone
   wrong: a session asked a peer *and* created one when the request seemed to
   resolve elsewhere. **Asking somebody to do a thing and then doing it yourself
   is not redundancy, it is two of the thing.**
2. **"Creating the successor is the human's job"** — because rule 1 let local
   sessions accumulate on one checkout until there were eight.
3. **"Create it in the cloud"** — because a cloud task removes the hazard *by
   construction* rather than by discipline, and can be steered from a phone.
4. **Back to "its own worktree"** — because the cloud call turned out to create
   a session that never receives its kickoff prompt, and because the tree lock
   now refuses a second agent outright, so the accumulation rule 3 was reaching
   for discipline to avoid is enforced against instead.

> **Three positions, one constraint, and the constraint is the only durable
> part: the unit of safety is a working tree, and agents must not share one.**

When you meet a rule like this, extract the constraint rather than the
instruction. The instruction is about whatever tooling existed that week.

## Landing on the trunk goes through review, and you are not the reviewer

The branch is half the mechanism. The other half is what happens at the end of
it, and an agent that pushes straight to the trunk has skipped it.

> **The trunk is protected, and work reaches it through a reviewed pull
> request.** Not a direct push, not a self-approved pull request, not a
> fast-forward merge somebody performed on their own work.

The reason is not process hygiene. It is that **the author is the one party who
structurally cannot review the work**:

- Every check the author would run is a check they already ran, in the
  vocabulary that produced the defect. `checking-claims` states the general form
  — *a search inherits the assumption that makes the mistake possible*.
- Review is cheap for a second reader because they have no stake, which makes
  checking *easy*, not *unnecessary*. A second reader who defers is not a
  reviewer.
- An agent has an additional failure mode a person does not: it wrote the
  reasoning, the commit message, and the pull request body, so a self-review
  compares a claim against the same claim restated.

### The rules that follow

1. **Never approve your own pull request.** Most forges refuse this outright, and
   where they do not, the approval is a green tick with nothing behind it.
2. **Never merge unreviewed work to the trunk because you are confident**, or
   because you are the only contributor, or because a gate passed. A passing gate
   is evidence about the gate — see `measured-changes`.
3. **The reviewer is a different context.** A person, or an agent session that
   did not write the change and does not receive the author's reasoning as
   given. An agent reviewing its own branch in the same session is the author.
4. **Give the reviewer the claims, not just the diff.** State what you verified,
   at what boundary, and what you did not — the reviewer's most valuable move is
   checking a claim you were sure of.
5. **A review that has never rejected anything is decoration.** The same rule as
   any gate: if it cannot fail, it is not a check. Watch it reject something, or
   assume it approves by default.

### An agent asked to approve its own work should refuse and say why

This is worth stating explicitly, because the request is reasonable-sounding and
the refusal looks unhelpful. Approving your own change is not a formality that
unblocks the work; it is the deletion of the only step that could have caught
what you got wrong. Say that, and offer the alternative — a reviewer, or a merge
performed knowingly without review by somebody who is entitled to make that call.

**Where the trunk is deployed**, this stops being about code quality and becomes
the same argument as the tree lock: the failure lands on people who were not
present when the decision was made.

`references/AUTOMATING-REVIEW.md` covers how to enforce all of this — branch
protection, required checks, automated reviewers, and the ways each of them can
be made decorative.

## Why sharing a tree is not survivable

Two reasons, and the second is the one that actually bites.

**A verification run that spans another agent's edits reports on a mixture no
commit contains.** If the suite takes minutes and another agent is editing
throughout, green means nothing — the tree it measured never existed and never
will. Red is worse, because it is unattributable: the failure belongs to a
combination neither agent wrote.

**A shared tree is a shared git index.** `git add -A` commits whatever the other
agent had half-written. Not a conflict, not an error — a commit whose message
describes one change and whose diff contains two.

That is not hypothetical. In the origin project, one commit carries eighty-one
lines of a second agent's work, swept in while that agent was three minutes into
a verification run the project *requires* it to make. Neither agent did anything
wrong and neither could have seen it.

**The content survived; the explanation did not** — and it was unrecoverable,
because fixing it means rewriting a pushed branch others have already fetched. A
sweeping commit cannot be undone, only annotated.

## Work is claimed, and a claim is a commit

A prose list of what is open is an **invitation**, not an assignment. Two agents
reading "doing X is recommended next" both do X, and neither is doing anything
wrong.

There is already a mutual-exclusion primitive and it needs no infrastructure:
**a push is a compare-and-swap.** A non-fast-forward rejection means somebody
else moved first.

1. Open work lives as **one file per item**, in a directory such as `docs/open/`.
2. Claiming is editing that file's status and pushing it, **as its own commit,
   before starting**.
3. If the push is rejected, somebody claimed something meanwhile. Re-read and
   pick again.

> **The rejection is the lock working.** `--force` is how an agent destroys
> another's work while believing it is unblocking itself. Never force.

**One file per item is the load-bearing half.** Two agents claiming different
items touch disjoint paths, so git merges them with nobody arbitrating. A single
shared list is a file every agent writes — which makes the most droppable
artefact in the project also its most contended.

See `assets/item-template.md` for the item format the listing script parses.

### A claim expires, because agents die

An agent that stops mid-item leaves a claim nobody can take, and an item nobody
may touch is indistinguishable from an item nobody wants.

A claim carries **the time it was made**, and a claim older than **four hours**
is stale and may be taken by writing a new one over it.

Taking a stale claim is **ordinary, not rude** — stated here so nobody has to
decide whether it is allowed. Check the log for the claim's branch first: work
that reached a commit is worth continuing rather than restarting.

## Four states, and only one of them is a task

| State | Means | May an agent start it? |
|---|---|---|
| `open` | Nobody has done it and nobody is doing it | **Yes** |
| `claimed` | Somebody is, since a stated time | Only if the claim is stale |
| `blocked` | Decided *for*, waiting on something that is not effort | **No** — the blocker is named, and it is what to check |
| `refused` | Decided *against*, with the reasoning recorded | **No.** Not a task, and never will be |

> **A refusal that is not written down as a refusal reads as a backlog item.**
> Having the reasoning in a document is not enough — the *list* has to say so,
> because the list is what a task-finisher reads.

This matters most for an agent asked to "finish whatever is pending", which is
what a kickoff prompt says, what a scheduled run does, and what any agent does
when handed a list. A refused item sitting next to real work gets built. It
passes CI. It ships something the project decided against.

**There is deliberately no `done`.** A finished item is *deleted*, and what it
found moves into the document it is about. A fifth state grows a list whose
whole value is being short enough that somebody reads all of it first.

## Do not build an index of the items

The trap, and it is not obvious.

Splitting a list into one file per item removes contention only if nothing has
to be kept in step with the pieces. In the origin project an index file naming
every item was added alongside the split — and measured across forty commits it
became **the most written file in the repository**, ahead of every document and
every source file. Claiming meant editing your item *and* the index. Worse, a
test *required* it, so the gate defending discoverability was manufacturing the
contention.

> **Splitting a file does not remove contention if something has to be kept in
> step with the pieces.** An index is the pieces, listed again, in one file.

Derive it instead. `scripts/open.ts` reads the state out of the item files and
prints them, `open` first:

    node scripts/open.ts [directory]

It writes nothing — a generated file committed to the repo would be a shared
file again, with the added property of looking authoritative while stale. A
derived view **cannot disagree with what it describes**, which is the second
payoff and the reason to reach for this shape generally.

If you gate anything, invert it: the index file may no longer *name* any item,
and the listing must show all of them.

## When a rule is not enough

Everything above is a rule an agent follows, and rules work because the agent
that would do damage is the agent reading the rule.

**The shared-index failure broke that assumption.** The agent that lost was not
present at the moment it lost — it was mid-verification, doing what the project
required. Both agents followed every rule. No degree of care closes a window you
are not awake for.

> **Enforce the failures the loser cannot see coming; leave the rest as rules.**
> A rule is cheaper, is readable, and explains itself — but it can only protect
> against the mistakes of whoever is reading it.

`scripts/pre-commit` gives a working tree to the first agent that commits in it
and refuses the next one, for the same four hours a claim takes to go stale,
printing the `git worktree add` line it should have run instead. Install it:

    cp scripts/pre-commit .githooks/pre-commit
    chmod +x .githooks/pre-commit
    git config core.hooksPath .githooks

Four details are deliberate, and each was a bug avoided:

- **A person is never refused.** The hazard is two agents sharing an index. A
  guard that blocks the human is a guard that gets uninstalled. It keys off the
  agent session environment variable, which a person's shell does not have.
- **The lock lives in `$GIT_DIR`**, so every worktree gets its own for free and
  it never appears in `git status`. A lock file in the tree would be one more
  thing for the next `git add -A` to sweep, which would be a joke at its own
  expense.
- **It should install itself** wherever a package manager exists, from a
  `prepare` script or equivalent, because `core.hooksPath` is per-clone and a
  hook nobody has told git about is a file that looks like a safeguard. The copy
  shipped here cannot do that for you — it is a plain `sh` script with no
  packaging — so whatever your verify command is, have it run the `git config`
  line and say that it did.
- **`--no-verify` is the wrong move**, and the refusal says so. It does not make
  the tree safe; it makes you the second agent in it.

## What is deliberately still shared

Splitting has a cost, and the distinction that decides it:

> **Contention at the start of work is structural and worth engineering away;
> contention at the end of it is editorial and worth living with.**

- **Narrative documents** are contended by *addition*, and additions to
  different sections merge without arbitration. Splitting them per-finding
  destroys the thing that makes a project legible.
- **A handover file** is written once per session, at the end, by an agent that
  is finishing rather than starting — so it never sits in front of every agent
  the way an index does. A conflict in it is two people describing the same
  state, which wants resolving rather than avoiding.

## For scheduled and heartbeat runs

An agent that wakes on a timer is the sharpest version of every problem above,
because it arrives without anybody deciding it should.

- **Measure what arriving costs before enabling it.** In the origin project the
  hourly agents were switched off because they spent their budget on reading
  themselves in rather than on working — and that cost had never been measured.
- **Give it something to do when there is nothing to do**, explicitly, or it
  will find something. "There is no open item" must be a legitimate outcome that
  ends the run.
- **Name what it must not do.** The dangerous moves are the ones a careful
  engineer would make on purpose: making slow measurements cheaper (which
  silently reduces their power — see the `measured-changes` skill), and
  regenerating a baseline rather than deciding whether the change was intended.
- **A blocked or sandboxed agent will conclude the suite was enough.** State
  which checks need network, a browser, or credentials, and require an agent
  that cannot run them to say so and hand them back.
