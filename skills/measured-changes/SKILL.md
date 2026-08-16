---
name: measured-changes
description: Practices for changing systems whose behaviour must be measured rather than judged — tuning constants, scores, weights, heuristics, ranking, or performance, and for building test gates that actually catch things. Use when about to tune a value by trying it, when adding a check or gate that guards a property, when a measurement surprises you, when a golden or snapshot baseline fails, when describing what a verification command covers, or when deciding whether a check belongs in the fast gate or a slower one.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Measured changes

For any system where **the effect you are making is smaller than the variance
you can perceive**. Balance constants, scoring weights, ranking, heuristics,
retry budgets, cache sizes, latency, conversion. The rules below separate tuning
from guessing, and every one came from a wrong number that looked right.

## Design before code

Write the reasoning down before writing the change: what the current behaviour
is, why it is wrong, what you expect the change to do, and **what number would
tell you it did**.

This is not ceremony. It is the only way to notice afterwards that you got the
result you wanted for a reason you did not intend.

> **A mechanic described as though it exists is a plan built on a fiction.**
> Before building on a behaviour you believe the system has, find the code or
> the test that shows it. Prose describing a feature is not evidence the feature
> is there.

## Never tune by trying it

> **The loop is: edit the constant, run the harness, read the table.** Never
> tune by using the thing. Effects are single percentage points, and human
> judgement cannot see them through run-to-run variance.

Using the system tells you whether it is broken. It cannot tell you whether a
1.5pp change went the right way, and it will confidently tell you it did.

Where the output is a *judgement about someone* — a score, a rank, a risk
rating — this stops being a quality rule and becomes an accountability one.
**The difference between a defensible score and a libel is a harness**, and no
amount of squinting at a visualisation substitutes.

## Sample size is a property of the effect, not of the harness

The standard error on a proportion is roughly `sqrt(0.25/n)`:

| Samples | Standard error |
|---|---|
| 1,000 | ±1.6pp |
| 5,000 | ±0.7pp |
| 20,000 | ±0.35pp |
| 40,000 | ±0.25pp |

**If the effect you are measuring is smaller than that, you are measuring
noise.** Two real examples of what this feels like from the inside: a result
that was *impossible by construction* — a superset scoring worse than its
subset — and an "underperforming" component that was being run with different
settings from everything it was compared against. Both read as bugs. Neither
was.

> **If a result surprises you, re-run it with more samples before believing
> it.** Surprise is the cheapest available signal that a measurement is wrong,
> and it is usually right about that.

An effect ten times smaller needs roughly a hundred times the samples. Give
those measurements their own, higher counts rather than sharing one number
across the suite.

## A check that flips on noise is worse than no check

A measured value of 39.9% against a 40% floor passes at 5,000 samples and fails
at 40,000. That is not a passing check; it is a coin toss with a threshold drawn
on it.

**Land mid-band with margin either side**, and record the measured figure with
the sample size it came from. A property sitting *just above* a line is the
worst place it can be, because the system then does not fix it and nobody looks
again.

## A gate that cannot fail is decoration

The anchor rule, and the most expensive one to learn.

A sweep across three very different values returned **byte-identical** results
and printed PASS every time. The harness built its own fixture, the fixture was
missing the very component being varied, and the system dropped the unknown
input silently — as designed, because tolerating unknown input is what keeps old
saved data working.

So the check ran, compared a thing against itself, and reported a healthy
spread.

> **A gate that cannot fail is decoration. A gate that silently measures nothing
> is worse, because it looks like evidence.**

Three practices follow:

- **Watch every new gate fail on the bug it guards, before trusting it.** If you
  cannot make it go red, you have not written a check.
- **Fixtures must assert their own completeness.** A helper that assembles a
  test fixture should *throw* when something it was asked for is missing, rather
  than returning an empty value. Silent tolerance is correct in production and
  catastrophic in a harness.
- **Mutation works after the fact.** Copy the module to a temp path, break one
  behaviour, point the untouched test at the copy. No edit to real source, so it
  is safe in a shared tree and possible long after the code merged.

## The checks that matter are the rules, not the arithmetic

Arithmetic errors are loud. The failures worth building gates for are the ones
that produce a plausible result:

- an input category that is unmapped, and silently defaults to zero
- a weight or constant with no recorded derivation
- a state that is styled and never actually produced
- a prohibited word or claim reaching user-facing copy

That last one is not hypothetical: in the origin project, a copy gate **caught a
forbidden word in the project's own text, inside a sentence arguing against
using it.** That is the whole argument for having it.

> **A value that silently defaults is indistinguishable from a deliberate
> exclusion** — opposite intent, identical representation, in the output and the
> interface and every export. Make the default an error, or make it visible.

## Describe your gate accurately

> **A gate is allowed to be small. It is not allowed to be described as larger
> than it is.**

State plainly what the verification command does *not* cover — network fetches,
data rebuilds, real rendering, migrations. An agent that reads "verify must pass
before commit" and concludes verify is sufficient will ship the thing verify
never looked at.

## Structural checks and numeric checks are different things

Some assertions encode a *design promise* — "this strategy should beat that one
under these conditions". Others encode a *measured range*.

> **When a structural check starts failing, either a constant went too far or
> the design changed. Decide which before adjusting the target.** Moving the
> threshold to make it green converts a design promise into a record of whatever
> the code currently does.

## A golden baseline failure is two different events

If you pin outputs against committed constants, a failure is either:

1. **An intended change** — regenerate the baseline and explain it in the commit
   message, or
2. **An accident.**

These are not interchangeable, and regenerating without deciding which one it is
destroys the only signal the baseline exists to give. State the measured
resolution too — "the corpus moves on a 0.01% change to this constant" tells the
next person how much sensitivity they are holding.

Anything already computed under the old numbers — stored ratings, historical
tables, cached results, published figures — is why this matters: a silent
regeneration invalidates data that has already shipped.

## Know which changes need re-verification, and why

Isolate sources of randomness so cosmetic additions provably cannot move a
result — for example, giving presentation its own RNG stream, separate from
simulation.

The payoff is a real diagnostic: **adding a line of copy cannot change the
numbers, and if it does, something is drawing from the wrong generator.**

## Keep the gate that runs everywhere cheap

If a fast gate runs on every deploy and a slow one runs in CI, expensive checks
belong in the slow one — and something must *enforce* that, or they migrate.

Write a test that fails when an expensive check appears in the cheap gate. The
rule is easy to state and impossible to remember at the moment somebody adds one
more assertion.

## Record it, or it did not fully happen

- **Docs are a deliverable.** A measured result that lives only in a terminal is
  gone. Put the number, the target, and the sample size in the document that
  explains the system.
- **Commit messages explain *why*.** The diff already says what changed. The
  reasoning — what was measured, what it replaced, what was rejected — exists
  nowhere else.
- **A number in prose is a measurement with an expiry date.** Write "39.9% at
  5,000 samples, against a 40% floor" rather than "just under the floor". A
  figure carrying the run it came from is a recorded observation and does not
  rot; a bare one reads as current forever.

## The suite is not enough

This has its own skill — see `verify-in-the-real-thing`. The short form:

> **Drive the real artifact, in the real environment.** In the origin projects,
> essentially every real defect was found that way and none by the test suite.

If you cannot — sandbox, firewall, missing credentials — **say so explicitly and
hand that check back.** Concluding the suite was sufficient is the failure this
rule exists to prevent.
