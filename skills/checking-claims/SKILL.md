---
name: checking-claims
description: Rules for deciding whether a claim is true before acting on it, especially claims about tooling, searches, censuses, CI, and test gates. Use when about to state how tooling works, interpreting an empty or partial result, quoting a count, searching for absence, choosing a corpus or denominator, reading a linter or reviewer finding, asserting a test catches something, or reviewing an inherited fact, cost, discouragement, or instruction.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Checking claims

Seven rules about believing things. Each came from a confident inference that
nobody checked, and each cost real work before it was caught.

None of them are about *looking harder*. Looking harder is what the person who
made the mistake was already doing.

## Where wrong beliefs concentrate: tooling, not the domain

Domain logic gets measured, because nobody trusts a domain claim without a
test. **Tooling gets reasoned about**, because it feels like the kind of thing
you can simply know — and a wrong belief about a build system produces no
symptom until it produces a plan.

> **A claim about your own tooling needs evidence exactly as much as a claim
> about the code.** `ls`, `curl`, or a run you can point at. The reason it feels
> different is that nothing fails when you are wrong.

In practice: before writing "CI runs X on every push", "the deploy step runs
the test suite", "this binding is why the route 404s", or "that command isn't
available here" — run something that shows it.

## A finding is an inference until somebody checks, whoever generated it

A tool's output arrives formatted like a result, with a file and a line number,
and reads as though the checking has already happened. It has not.

> **A finding from a tool is more likely to be believed than one from a person,
> not less.** Treat a linter's verdict, a scanner's report, and a reviewer's
> comment as the same kind of object: a claim with an author.

And the reverse error is just as common:

> **A tool you have not run is not evidence, and neither is the reasoning you
> did instead of running it.** A candidate reasoned from how something is built
> and a candidate named by measurement are different kinds of thing, and only
> one of them is an answer.

If a tool you already have installed can answer the question, ask it before
reasoning about the answer.

### The subject is part of the evidence

Running the right command in the wrong checkout, against the wrong ref, or over a
cached view is not weaker evidence. It is evidence about another subject.

> **"Measured, not reasoned" answers how you know so convincingly that it can
> hide the question that matters: measured on what?**

Prefer commands that carry their repository, ref, environment, time window, and
selection predicate. Record those arguments with the conclusion.

## A search inherits the assumption that makes the mistake possible

When you grep to establish whether something is a convention, the pattern
usually filters on the very property being counted — so it quietly answers the
question it was meant to ask.

> **A search for a pattern finds the instances that state it fully, and misses
> exactly the ones that rely on it being already established** — which are the
> ones that prove it is established.

A house style is proved by the places that *modify* the base treatment rather
than restate it, and no pattern for the base treatment finds those. If a count
decides something, classify the unfiltered matches by hand.

Related, and just as common: **a claim cannot be checked by a search that
excludes the checker.** "Skip the test files" is a habit rather than a decision,
and the test file is often the counterexample.

Negative searches need more discipline than positive ones because absence leaves
no artifact. Prove the namespace and corpus can express the answer, find a known
positive control first, print matches before counting them, and use fixed-string
matching unless a pattern is intentional.

`references/SEARCHES-AND-CORPORA.md` carries the full method.

## A count without its definition is not a fact

Whether a tally is 25 or 33 usually turns on an inclusion question nobody wrote
down. Neither the question nor its answer is recoverable from the figure, and
both get settled silently by whoever writes it.

Quote the definition and the sample size with the number, always. Two
measurements at different arguments are not evidence about each other.

Count at the actor when the observer cannot express the interval. A server trace,
session store, or process listing does not necessarily know where one user
action, session turn, or run begins and ends.

## A command can answer a neighboring question perfectly

This is more dangerous than a command that fails: the output is true.

- a branch range answers ancestry, not whether the content landed under another
  commit;
- a closed port answers whether something listens there, not whether owned
  processes remain;
- zero open pull requests answers what is queued, not whether workers stopped;
- run success answers the workflow, not whether required steps executed.

Before trusting a command, write the question it actually answers. If the
conclusion needs another verb or subject, run another instrument.

### Neutral is a result, not a pass

Absent, queued, pending, skipped, and unreadable are distinct from pass and fail.
A source that never publishes the status you requested may return a reassuring
neutral value forever.

> **Blindness must never render as a negative finding.**

If the source cannot be read, report `unread` and why. If no observation was
made, report `unverified`. Do not initialize an uncertain path to zero, false,
empty, or success.

## A second reader is not the safeguard; checking is

They correlate, because a second reader has no stake in the claim — which makes
checking *easy*, not *necessary*.

> **A reviewer's claim needs checking exactly as much as an author's.**
> Deference produces the wrong answer at the exact moment it feels most
> warranted: when the correction comes from whoever has been right all day.

Corollary: **deferring is cheap; taking the answer on trust is not deferring.**

## Re-running catches what rereading cannot

The one mechanism that works on your own claims.

> **A claim that came from a command is checked by running the command again.**
> It is cheap, it is nobody's judgement, and it is the only move that does not
> inherit the assumption that produced the mistake.

A single measurement written down as a general fact is the standard failure —
"performance is 91" from one cold run, beside a sentence about repeated runs
that was true of a *different* set of runs. The number was not wrong; it was a
different quantity from the one it was recorded as.

## A claim survives by being inherited

> **Nobody checks a line they did not write, even while rewriting around it.**

A diff shows the lines that changed, so an untouched false claim inside a
heavily rewritten section is invisible in exactly the review that would catch
it. Same reason a long document grows: **a diff has no denominator.** What gets
reviewed is the change; the property being violated belongs to the whole; and
nothing in the workflow puts anybody in front of the second.

This is the rule that applies hardest to *this file* and to any set of
practices copied between projects. A rule is portable. The evidence that
produced it belongs to the project it happened in, and restating it somewhere
else turns a recorded observation into an unverifiable assertion.

Facts are not the only claims that inherit:

- A stale **discouragement** stops the next person before they check it.
- A stale **cost estimate** changes which work is attempted, so reality never
  contradicts it.
- A stale instruction can remain true as a sentence while the mechanism that
  made it reachable disappears.

When a mechanism is removed or replaced, search for prose that named it and gate
the obsolete actionable form. A mention in history is not the same as an
instruction still telling somebody what to do.

## A test asserting its own rigour is still a claim

The most self-referential version. A test file whose header says every
assertion was watched failing on the bug it guards is the one kind of
documentation that reads as evidence, and nothing anywhere can tell whether it
is true.

Settle it by **mutation**, which is cheap and works long after the fact:

1. Copy the module under test to a temp path.
2. Break exactly one behaviour in the copy.
3. Independently confirm the mutation changed the intended property.
4. Point the untouched test file at the copy and run it from a green baseline.

Repeat per behaviour the test claims to guard. Two things to watch for:

- **A single-test catch is worth more than a failing suite.** If one break
  reddens one assertion and leaves the rest green, the checks are separated. A
  break that reddens everything tells you only that something is wrong.
- **Mutation against a temp copy needs no edit to the real source**, so it is
  safe in a shared tree and possible after the code is merged — which is what
  makes an old unverified claim recoverable rather than permanent.
- **A passing mutation has two explanations:** the gate missed the defect, or
  the mutation did not create it. An empty mutation diff proves only the second.
- **Re-run the mutation last.** A check watched failing before its own comments
  or fixtures changed has a true claim with an expired timestamp.

If the claim turns out true, that is the *uninformative* outcome, not the
reassuring one. It was true by luck of who wrote it, and the next such header
is a coin toss.

## Attention is not immunity

Agents have committed a failure class within minutes of documenting it. This is
not hypocrisy; prose changes attention and gates change outcomes.

Where a gate is possible, build one. Where deletion, explanation, or project
memory cannot be gated without blocking legitimate work, require a different
reader. A protocol that encourages deletion needs review more than one that
forbids it, because no general check can know which vanished idea was required.

## Applying this

Before you assert something, ask which of these it is:

| The claim | What settles it |
|---|---|
| About tooling, CI, a build, an environment | Run the command. Paste the output. |
| A count, a proportion, a tally | State the definition and the sample size, and classify unfiltered matches |
| From a linter, scanner, or reviewer | Check it against the codebase yourself |
| A number you measured once | Measure again |
| Inherited from an earlier doc or comment | Check it, especially while rewriting around it |
| Empty, pending, skipped, or unreadable output | Report the third state; do not turn it into pass or absence |
| "This test catches that bug" | Start green, prove one mutation applied, and watch that check fail |

The worked examples remain in the private evidence of the origin project. They
are deliberately neither linked nor restated here, per the inheritance rule
above: they are true there, and copying them would make this file an example of
its own failure mode.
