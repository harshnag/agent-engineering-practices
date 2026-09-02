---
name: project-agent-instructions
description: Writing and maintaining the AGENTS.md that governs a repository — what belongs in it, what belongs in a linked document instead, how to route a large reasoning corpus, how to record inherited rules, and how to detect stale or missing injected instructions. Use when setting up agent instructions, editing or reviewing an AGENTS.md or CLAUDE.md, designing an agent read-in order, noticing instructions disagree with the repository or vanished after a workspace change, deciding whether a rule belongs in instructions or a doc, or onboarding agents onto a project.
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

The file on disk wins **between copies**. It can still be false about the
repository. A freshness check comparing injected text with disk proves agreement,
not truth; pipeline, deploy, and tooling claims still need their own instruments.

### Missing is worse than stale

A stale injected copy can be compared with the file on disk. A session whose
working tree was removed while it was still running may receive **no project
instructions at all**, and it has lost the repository containing the checker
that could say so.

> **Never archive or remove a working tree while its session is still live,
> including your own.**

If the current directory is no longer a checkout, stop. Read the instructions
from a healthy checkout and use the session manager's live identity rather than
a creation-time metadata file. Session ids and branch names often exist in more
than one namespace, and a stored value can be correct when written but stale
after a rename or restore.

Where the agent runtime exposes a session-start hook, run an instruction
freshness check there. A check that runs only when somebody already suspects
staleness protects the sessions least likely to need it.

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

## Prescribe a routed read-in, and put the handover first

Not a list of documents. An **order**, with one sentence per entry saying what
question that document answers, so a session can stop early when it has what it
needs.

The compulsory order that both origin projects converged on:

1. **The handover** — where the last session stopped, what is open, what it did
   not verify. Say in the instructions that it is the one document allowed to be
   wrong, and that the docs win over it. See the `agent-handover` skill.
2. **The README or design anchor** — what this is, and the constraints that
   decide priorities.
3. **The concurrency document** — *because you may not be alone in here.* This
   belongs early, not late; it governs whether the session may write at all.
4. **The short one about believing things** — before trusting any claim about the
   tooling, including your own.
5. **`git log --oneline -20`.**

Two things to state alongside the order:

- **Everything else is routed by task.** Give each document one sentence saying
  what question it answers. A list of every document in sequence is not strict;
  once it exceeds a session's budget it is impossible, and every reader routes
  informally anyway.
- **The read-in is not free.** Measure the compulsory prompt boundary and the
  corpus separately. The total corpus is a routing warning, not a claim about one
  request's token usage.
- **What the docs are *for*.** They record reasoning rather than behaviour. That
  is why re-deriving an answer already in them is how a second, divergent copy
  starts.

Long documents need addressing: a generated contents block with an explicit
size budget, plus a heading or symbol search that reports line numbers. The
index routes; it does not summarize. Say when a size ceiling drops subsections,
or the largest document presents the shallowest map without admitting it.

See `durable-project-memory` for the full workflow: task routing, bounded
compression, research notes, and the distinction between project memory and a
portable skill.

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
- **Research is a deliverable.** A finding acquired outside the repository is
  committed with its date, sources, verification boundary, and negative findings
  before the project acts on it. (`durable-project-memory`)
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

### A current-state layer for a long reasoning document

A long document may open with a short "how it works now" block when the historical
reasoning below has reversed several times. To keep that layer from becoming a
second stale handover:

- each fact names the file or command that decides it;
- it carries no dates, measurements, or perishable counts;
- it names only real, checkable artifacts;
- it has a size cap, so adding means replacing;
- it appears before the history.

This makes drift loud and cheap to check. It does not prove the block is true.
Comparing it with another copy of itself cannot do that.

Two properties are worth gating in a check, because they are what a file like
this quietly loses:

- **One copy.** The rule lives in one place, because a second copy can only
  drift.
- **Reachable.** A document nothing links to is gone in practice whatever it
  contains — so the instructions file must point at it.

Generated agreement is not completeness. An index derived from current headings
stays green if a heading and its index entry disappear together. Any check for
required material needs an independent inventory or a mutation that removes a
known required subject.

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
