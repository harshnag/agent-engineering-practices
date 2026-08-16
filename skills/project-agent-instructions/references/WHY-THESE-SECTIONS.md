# Why these sections, and what happens without each

Read `SKILL.md` first. This is the reasoning behind the shape, written as
failures rather than as principles, because each section exists because something
went wrong without it. It loads on demand.

## Why precedence comes first

It is the only section that changes how every other section is read, and it is
the only one that is *invisible* when missing.

A stale injected instruction arrives with exactly the authority of a checked one.
There is no formatting difference, no warning, no timestamp. An agent obeying a
reversed rule looks identical to an agent obeying the current one — from the
inside and from the outside — and the divergence is only visible to somebody who
directly compares the injected text against the file on disk.

That is why the section has to say *how to check* rather than merely *the file
wins*. "The file wins" is unactionable if you cannot see that they differ. The
three steps — file on disk, then `git log` on the file, then say so in the
session — are what turn the precedence rule into something an agent can execute.

**Without it:** a session spends its whole budget correctly implementing a rule
the project abandoned, and nothing at any point fails.

## Why provenance is worth a clause on every rule

Two failure modes, in opposite directions.

**Without provenance, an inherited rule gets discarded.** A reader who has never
seen a rule bite here reasonably concludes it is somebody's preference. The rules
most worth keeping are exactly the ones whose failure is rare and expensive, so
"it has never happened here" is what they all look like right up until they
happen.

**Without provenance, a locally demonstrated rule is not credited.** The most
persuasive thing an instructions file can say is *this one is no longer
inherited, and here is what it cost.* One origin project's most-obeyed rule is
the one carrying that sentence.

There is also a maintenance property. Marking provenance forces a decision each
time a rule is edited: has this been demonstrated here yet? A file where
everything is marked inherited forever is a file nobody has re-read.

## Why the read-in is an order and not a list

A list gets read top to bottom, or not at all, and a session that runs out of
patience stops somewhere arbitrary. An order with a reason per entry lets it stop
somewhere *chosen*.

The two entries that are always misplaced:

**The handover goes first, not last.** It is the only document that tells you
what is currently true. Reading the reasoned documents first and the handover
last means re-reading them with the state in mind.

**Concurrency goes early, not late.** It governs whether the session may write at
all, and in which tree. An agent that reads it after starting work has already
taken the action it would have prevented. Both origin projects moved it earlier
after exactly that.

**Without a stated order:** every session invents one, and the ones that matter
get read last or not at all.

## Why the gate must describe its own boundary

This is the highest-value single sentence in an instructions file, and it is
counter-intuitive: the file is more useful when it *reduces* confidence in the
project's own tooling.

The mechanism is that "run verify before committing" is read as "verify is what
correct means". Nothing in the sentence says that, and every agent infers it,
because it is the only quality bar the file names.

So the boundary has to be stated as explicitly as the requirement:

> **A gate is allowed to be small. It is not allowed to be described as larger
> than it is.**

**Without it:** an agent ships the entire class of thing the gate does not look
at, and reports the work as verified. See the `verify-in-the-real-thing` skill —
the default conclusion of a blocked or sandboxed agent is that the suite was
sufficient, and a file that does not contradict that is agreeing with it.

## Why one project-specific rule gets its own section

Because everything else in the file is generic, and a reader who recognises the
generic parts will skim. The section that is *only true here* is the one that
cannot be inferred from experience elsewhere, and it needs to be visibly
different in the document for that reason.

The discipline that keeps it useful: **the section states the constraint and
points at the enforceable form; it does not restate the enforceable form.** The
enforceable version is long, it changes, and a second copy in the instructions
file is a copy that drifts.

## Why "additions replace rather than accumulate"

These files grow. Every addition is individually justified, every addition was
prompted by something real, and the total becomes unreadable — at which point it
stops being read, which costs more than any individual rule was worth.

The mechanism is from `checking-claims`:

> **A diff has no denominator.** What gets reviewed is the change; the property
> being violated belongs to the whole; and nothing in the workflow puts anybody
> in front of the second.

Nobody reviewing an addition is looking at the length. There is no natural moment
at which somebody reads the whole file and asks whether it is still readable, so
the instruction to replace rather than append has to be written down and pointed
at during edits.

The related rule — **state a limit, never a current size** — exists because a
file that says how long it currently is has embedded a measurement that rots, in
the document specifically about not doing that.

## Why setup must install itself

A `## Setup` section is a claim that something has been done, and it is checked
by nobody.

The specific case that produced the rule: a pre-commit hook committed to the
repository, with a `git config core.hooksPath` line in the setup section. Every
clone that never ran the line had the file and not the protection — and the file
being present is what makes it look protected.

> **A hook nobody has told git about is a file that looks like a safeguard.**

So the verification command performs the setup and says that it did. The general
form is worth carrying beyond hooks: **an instruction that must be followed
exactly once, by a human, on every machine, will not be.**

## What to leave out

Three things that get put in an instructions file and should not be:

- **Architecture.** It is long, it changes, and it is only needed by sessions
  touching that area. Link it.
- **Status.** Anything about what is currently being worked on belongs in the
  handover, which is the file allowed to go stale.
- **Anything you cannot say in a way that could be violated.** "Write good code"
  costs a line on every activation and changes no decision.
