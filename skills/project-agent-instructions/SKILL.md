---
name: project-agent-instructions
description: Writing and maintaining the AGENTS.md that governs a repository — what belongs in it, what belongs in a linked document instead, how to record which rules are inherited rather than demonstrated, and why the file on disk outranks the copy injected into your session. Use when setting up agent instructions in a new repository, editing or reviewing an AGENTS.md or CLAUDE.md, deciding whether a rule belongs in the instructions or in a doc, noticing your instructions disagree with the repository, or onboarding agents onto a project for the first time.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# The instructions file

`AGENTS.md` is the working agreement for anybody — person or agent — who writes
anything in a repository. It is read by every session, so every line in it is
paid for on every activation, and everything in it that is wrong is obeyed.

`assets/AGENTS-template.md` is the shape. This file is why each part of that
shape exists.

## Your copy may be stale, and the file on disk wins

The first section of the file, because it governs how the rest is read.

Agent tooling injects instruction files into a session as custom instructions,
and **that copy can be days old**. In one origin project a session began with
injected instructions describing a rule the repository had reversed 33 hours
earlier. Local trunk, remote trunk, and the working tree all agreed; the
divergence existed only in what the agent had been told.

> **An agent's own instructions are a claim about the repository, and they need
> evidence like any other.** Nothing fails when they are wrong. The session
> spends its whole budget obeying a rule the project reversed.

So state the precedence explicitly, in the file:

1. **The file on disk wins**, and the remote trunk breaks the tie if they differ.
2. Check what changed: `git log --oneline -5 -- AGENTS.md`, then read the commit
   message. Every reversal should be explained in one.
3. **Say so in the session**, so whoever is driving knows their tooling is
   serving stale rules — it is invisible from their side too.

And write the file so this is checkable: **explain every reversal in a commit
message**, so step 2 returns something.

## Say which rules are inherited and which were demonstrated here

The provenance convention, and it is the most transferable thing in this skill.

Most rules in a mature instructions file were learned somewhere else. Saying so
costs a clause and buys two things: a reader can tell which rules this project
has actually tested, and nobody quietly discards a rule on the grounds that it
has never bitten *here*.

> **Where a rule is inherited rather than demonstrated here, say so. Do not let
> that soften it: an inherited rule is a rule somebody else already broke.**

Then **promote a rule when it is demonstrated locally**, and name what happened.
In one origin project, two inherited rules were demonstrated within hours of
arriving, and the file was edited to say which two and where the evidence lives.
That edit is what keeps the convention honest — without it, everything stays
marked "inherited" forever and the marking stops meaning anything.

## Prescribe a read-in order, and put the handover first

Not a list of documents. An **order**, with one sentence per entry saying what
question that document answers, so a session can stop early when it has what it
needs.

The order that both origin projects converged on:

1. **The handover** — where the last session stopped, what is open, what it did
   not verify. Say in the instructions that it is the one document allowed to be
   wrong, and that the docs win over it. See the `agent-handover` skill.
2. **The README or design anchor** — what this is, and the constraints that
   decide priorities.
3. **Settled decisions** — the questions that are closed, so nobody reopens one
   by reasoning from scratch.
4. **The concurrency document** — *because you may not be alone in here.* This
   belongs early, not late; it governs whether the session may write at all.
5. **The short one about believing things** — before trusting any claim about the
   tooling, including your own.
6. **`git log --oneline -20`.**

Two things to state alongside the order:

- **The read-in is not free.** If it prescribes thousands of lines, a session has
  spent part of its budget before doing anything. Say so, and say whether anybody
  has measured it.
- **What the docs are *for*.** They record reasoning rather than behaviour. That
  is why re-deriving an answer already in them is how a second, divergent copy
  starts.

## The rules, and what makes one belong here

Keep the list short, and make every entry the kind of thing that changes what an
agent does today. A good test: if it cannot be violated, it is not a rule.

The durable core, each of which has its own skill here:

- **Design first.** Write the reasoning down before writing the code.
- **Measure, do not judge** — anything whose effect is smaller than its variance.
  (`measured-changes`)
- **A gate that cannot fail is decoration.** Watch every new check fail on the
  bug it guards before trusting it. (`measured-changes`)
- **Drive the real artifact in the real environment.**
  (`verify-in-the-real-thing`)
- **Docs are a deliverable.** A change that is not written down did not fully
  happen.
- **Commit messages are prose explaining *why*.** Read `git log` before writing
  one.
- **You are not alone in here** — claim work, own your working tree.
  (`agent-concurrency`)
- **Finish by pushing.** (`agent-handover`)

### Describe your gate accurately

> **A gate is allowed to be small. It is not allowed to be described as larger
> than it is.**

Name the verification command, say it must exit 0 before any commit, and then say
what it does **not** do — no network fetches, no data rebuild, no real rendering,
no migrations. An agent that reads "verify must pass before commit" and concludes
verify is sufficient will ship the thing verify never looked at.

If some checks need network, a browser, credentials, or a device, **list them**,
and require an agent that cannot run them to say so and hand them back.

### Name the one rule this project has that the others do not

Every project has something that is genuinely its own — a constraint that decides
implementation rather than a preference. Give it a section, and make it the thing
worth failing a build over.

Do not restate its detail in the instructions file. Point at the document that
holds the enforceable form, and carry only the part that governs how the rest of
the file is applied.

## What belongs in a doc instead

The instructions file is loaded by every session, so it competes for the same
budget as the work. Move anything that is:

- **Long.** If it needs more than a paragraph of reasoning, it is a document.
- **Only relevant sometimes.** Deployment, data pipelines, one subsystem.
- **Load-bearing enough to be argued about.** An argument needs room, and the
  instructions file is the wrong place to have one.

Two properties are worth gating in a check, because they are what a file like
this quietly loses:

- **One copy.** The rule lives in one place, because a second copy can only
  drift.
- **Reachable.** A document nothing links to is gone in practice whatever it
  contains — so the instructions file must point at it.

## Setup belongs in the file, and must install itself

Anything an agent has to run once — a hooks path, a dependency install — goes in
a `## Setup` section, and something in the normal workflow should perform it.

> **A hook nobody has told git about is a file that looks like a safeguard.**

Have the verification command install it and say that it did. Where a package
manager exists, hang it off a `prepare` script.

## Keeping it honest

- **Every reversal is explained in a commit message.** That is what makes the
  stale-copy check above return an answer.
- **Additions replace rather than accumulate.** These files grow past being
  readable, and every addition was justified at the time. From `checking-claims`:
  *a diff has no denominator* — what gets reviewed is the change, while the
  property being violated belongs to the whole.
- **A rule nobody has ever applied is a candidate for deletion**, and saying it
  is inherited is how you can tell.
- **State a limit, never a current size.** A number in prose is a measurement
  with an expiry date.

---

The template is [assets/AGENTS-template.md](assets/AGENTS-template.md). The
reasoning behind the section order, and what happens when each is missing, is in
[references/WHY-THESE-SECTIONS.md](references/WHY-THESE-SECTIONS.md).
