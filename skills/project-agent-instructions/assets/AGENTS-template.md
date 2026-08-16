# Working on <project>

Read this first. It is the working agreement for anybody — person or agent — who
writes anything in this repository.

<!-- PROVENANCE. If most of these rules were carried in from elsewhere, say so
     here, and say which ones have since been demonstrated locally. An inherited
     rule is a rule somebody else already broke; a demonstrated one is a rule
     this project paid for. Keep the distinction current. -->

## If your instructions disagree with this file, this file wins

**Read this even if you think you have already read this file**, because you may
have been handed an old copy of it without being told.

Agent tooling injects this file into a session as custom instructions, and that
copy **can be stale by days**. Nothing fails when it is wrong — the session
spends its whole budget obeying a rule the project reversed.

So, when the rules you were given and the file on disk disagree:

1. **The file on disk wins**, and `origin/main` breaks the tie if they differ.
2. Check what changed: `git log --oneline -5 -- AGENTS.md`, then read the commit
   message. **Every reversal here is explained in one.**
3. **Say so in the session**, so whoever is driving knows their tooling is
   serving stale rules — it is invisible from their side too.

## Read yourself in, in this order

**[HANDOVER.md](HANDOVER.md) first** — where the last session stopped, what is
open, and what it did not verify. It is a pointer rather than a substitute, and
it is the one document here allowed to be wrong: read it for the open decisions,
then believe the docs over it.

Then <!-- the design anchor: what this is and the constraints that decide
priorities -->, then <!-- docs/decisions/ — the questions that are settled, so
nobody reopens one by reasoning from scratch -->.

Then <!-- the concurrency document --> **because you may not be alone in here.**
Work is *claimed* before it is started, anything decided against is marked
`refused` rather than left to read as a backlog item, and anything that writes
code gets its own working tree. **Check who is here rather than assuming either
way.**

Then <!-- the short document about believing claims -->, which is the one to read
before believing anything about the tooling — including your own claims about it.

Then `git log --oneline -20`.

**The docs are the context this project runs on.** They record *reasoning* rather
than behaviour, and a session reads itself in from them before writing anything.
A mechanic described as though it exists is a plan built on a fiction.

<!-- Say whether anybody has measured what the read-in costs. If not, say that. -->

## The rules, which are not negotiable

- **Design first.** Write the reasoning down before writing the code.
- **Measure, do not judge.** <!-- Name what this project measures and with what
     harness. Never tune by using the thing. -->
- **A gate that cannot fail is decoration.** Watch every new check fail on the
  bug it guards before trusting it.
- **`<verify command>` must exit 0 before any commit.** It does **not**
  <!-- name what it does not cover: network fetches, data rebuilds, real
  rendering, migrations -->. A gate is allowed to be small; it is not allowed to
  be described as larger than it is. Everything added extends it.
- **Drive the real artifact, in the real environment.** A passing suite is not
  evidence the thing works. <!-- Name which checks need network, a browser,
  credentials or a device. An agent that cannot run them must say so and hand
  them back rather than concluding the suite was enough. -->
- **Open the built things, not just the documents about them.** A README is
  *about* an artefact; the decisions are *in* it.
- **Docs are a deliverable.** A change that is not written down did not fully
  happen.
- **Commit messages are prose explaining *why***, often several paragraphs. Read
  `git log` before writing one.

## The rule this project has that the others do not

<!-- Every project has one constraint that is genuinely its own and decides
     implementation rather than expressing a preference. Name it here and make it
     the thing worth failing a build over.

     State the constraint and POINT AT the document holding its enforceable form.
     Do not restate that form here — a second copy drifts. Carry only the part
     that governs how the rest of this file is applied. -->

## Finish by pushing. Do not leave work pending

**Work that is done is committed and pushed before the session ends.** Not
staged, not left modified in the tree, not described in a handover as "ready to
commit". A session that stops with uncommitted work has not finished it — it has
moved it somewhere less safe than where it started.

Uncommitted work in a shared checkout belongs to whoever commits next, and a
commit is not automatically about one thing: check what a commit contains before
making it, and prefer explicit paths over `git add -A` whenever the tree holds
anything that is not yours.

When a person is driving the session, ask before committing on their behalf, then
commit and push what they approve rather than leaving it for them.

If work genuinely cannot be pushed, **commit it to a branch and say so in the
handover.** An unpushed branch is recoverable. A dirty working tree is not, and
it is invisible to everyone except the tree it is sitting in.

## Hand off before you are forced to

**At roughly <N> context, stop and hand off. Do not wait to be asked.** Update
[HANDOVER.md](HANDOVER.md), commit it, and say so. The edits made late in a long
session are exactly the small careful ones that go wrong when context is thin.

**Settle what is open before you go.** Ask every open design question while you
still have the context to argue about it. What genuinely cannot be settled goes
in its own file with the recommendation and the reasoning, so the next agent
inherits an argument rather than a blank — and can claim it, which a paragraph in
a handover cannot be.

**And say what you did not check.** A successor assumes anything unmentioned was
done.

<!-- Successor policy: how many, what kind, created by whom, and where their work
     will appear. If the mechanism is known to be broken, say so here — a
     successor you cannot create the right way is a successor you do not create.
     State the constraint the policy serves, not just the current instruction. -->

Report context usage after every major commit or push, so the decision to hand
off is never made by whoever is deepest in the work.

## Setup

    <setup commands>

<!-- Something in the normal workflow must perform this and say that it did. A
     hook nobody has told git about is a file that looks like a safeguard. -->
