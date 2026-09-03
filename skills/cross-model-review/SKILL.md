---
name: cross-model-review
description: Protocol for having every implementation plan and every diff critiqued by a different model in a fixed reciprocal pair — before implementation and before landing — with substantive findings only, an explicit author disposition on each one, a bounded re-review rule, and a record that tells a clean review apart from a skipped one. Use when starting implementation from a plan, preparing to commit or hand off, invoking or acting as a reviewer, deciding whether a revision needs another cycle, deciding what a reviewer may edit, choosing which models review which, or when the named reviewer cannot be reached.
license: MIT
metadata:
  provenance: Adopted protocol, 2026; not extracted from the origin codebases
  author: harshnag
  version: "1.0"
---

# Cross-model review

> **A change is critiqued by a model that did not write it, at two points:
> before implementation, and before it lands.**

The pair is **fixed and reciprocal** — two named models, A and B. When A authors,
B reviews. When B authors, A reviews. The pair is declared once in the project's
instructions and is not chosen per change.

Fixing it is the load-bearing part. A reviewer selected per change is a decision
the author makes about their own work, and an author who is late chooses the
cheapest reviewer. Reciprocity removes the other failure: neither model is *the
reviewer*, so the role follows authorship rather than status.

## What this adds, and what it does not prove

`agent-concurrency` already establishes the prior rule — the author cannot review
their own work, and the reviewer must be a **different context**. That rule is
satisfied by a second session of the same model, and this protocol does not
retract it.

What this adds is a preference for a different **model**, on the reasoning that a
second context of the same model shares a training distribution, shares priors,
and therefore shares characteristic blind spots. A different context removes
*stake*. It does not remove *shared priors*.

> **That is a diversification hypothesis, adopted deliberately. It is not
> measured.** Nothing here establishes that a different model finds defects a
> second context of the same model would have missed.

State it that way and no further. In particular, do not write that the pair
"catches what the same model misses" — that is a measurement claim, and it has no
measurement behind it. What would settle it is planted-defect calibration in both
directions, recorded; `references/RUNNING-THE-REVIEW.md` gives the procedure.
Until somebody runs it, the honest description is *adopted*, not *proven*.

## Two checkpoints — and they are not gates

1. **The plan is reviewed before implementation begins.**
2. **The diff is reviewed before commit or final handoff.**

They review different objects, so neither substitutes for the other. A diff
review cannot recover a wrong plan: by the time there is a diff, the design has
been paid for, and the reviewer is reading an implementation of the wrong thing.
The plan checkpoint is where a finding is cheap.

> **Both are enforced by instruction, not by a runtime hook. Nothing refuses when
> one is skipped**, no exit code changes, and no check goes red.

This repository's own rule is that a gate which cannot fail is decoration. This
is not a decorative gate; it is **not a gate at all**, and the expensive mistake
is calling it one — because a checkpoint described as a gate gets counted as
evidence by everybody downstream, including the next agent reading the record.

Two consequences follow, and they are the whole reason the rest of this file is
specific:

- **The record is the only artifact that a review happened.** A review nobody can
  point at did not happen, and cannot be distinguished later from one that was
  skipped in a hurry.
- **The protocol has to be self-reporting.** Where a gate would refuse, this can
  only require that the omission is *stated*.

## Substantive findings only

The bar, and it is deliberately narrow:

| Report | Do not report |
|---|---|
| An error in logic, behaviour, or data handling | Style, formatting, naming preference |
| A claim asserted without evidence, or unverifiable as written | A rewrite of something already correct |
| A violated project rule or convention | A summary of what the diff does |
| A verification that is missing, or that cannot fail | Speculation with no stated mechanism |
| A design that will not survive its next known change | Anything the author already stated as a known limit |

> **Finding nothing is a legitimate outcome and must be reportable as one.** A
> reviewer that always finds something is exploiting the author's inability to
> tell filler from signal — and, by the same rule as any check, a reviewer that
> has never rejected anything is decoration.

Invoke the reviewer against the **artifact and the repository**, not against the
author's reasoning. Do not pass the plan's justification, the commit message, or
the pull request body as context to be agreed with. Treat them as claims with an
author. Ask the reviewer to check them, and specifically to re-run whatever the
author says was verified.

## Every finding gets a disposition, and silence is not one

The author answers each numbered finding with exactly one of:

- **Accepted** — changed, with the change identified.
- **Rejected** — not changed, **with the reasoning recorded**.
- **Deferred** — not changed now, with a named carrier: an issue, a work item, or
  a stated follow-up. Deferred with no carrier is rejected while sounding
  otherwise.

> **The author decides; the reviewer does not hold a veto.** A reviewer's claim
> needs checking exactly as much as an author's, and deference produces the wrong
> answer at the moment it feels most warranted — when the correction comes from
> whoever has been right all day.

A recorded rejection is worth more later than a recorded acceptance. An
acceptance is visible in the diff; a rejection is invisible everywhere else, and
it is the thing a later reader will otherwise re-litigate from scratch.

## Termination is a property of the protocol, not of anybody's judgement

- **No review-of-review.** The reviewer's report is not itself submitted for
  review, and the author's dispositions are not reviewed as an artifact. Neither
  is a change.
- **But a materially revised artifact is not exempt.** Re-reviewing a plan or
  diff that materially changed is *artifact* review, not meta-review, and
  accepted fixes must not escape review by being called dispositions.
- **Re-review is scoped to the delta**, not to the whole artifact again.
- **The bound counts cycles per lineage, not per revision.** A plan and the diff
  that implements it are two lineages; a plan revised three times is one. Count
  per revision and "a material revision is a new artifact" resets the bound
  forever — an unbounded protocol wearing a bound.
- **Set the bound in project instructions.** Two cycles per lineage is a
  reasonable default.
- **The last allowed cycle is terminal for the pair.** If it produces a material
  change, or a disagreement survives it, that goes to a **human** — not to a
  third model cycle, and not out of the door unreviewed. Without this the bound
  has the opposite defect from the one it fixes: the final fix ships with nobody
  having read it.

Banning meta-review terminates nothing on its own; only the bound does. An
unbounded protocol with a ban on recursion still loops, one legitimate revision
at a time.

## Materiality is semantic, not editorial

A reviewer's own edits do not start a new cycle. That exception is defined by
**effect**, not by the label the editor puts on the edit.

**Material — a new cycle is required:** a change to executable behaviour, to an
interface, to a test or to what it covers, to a rule or instruction, to a claim,
to configuration, or to what was verified.

**Not material:** an edit that provably changes none of the above.

> "A mechanical rename" is a claim about a diff, not a category of diff. A rename
> can break a reference, and in a documentation repository the prose *is* the
> product — so a comment fix can be the most material change in the change.

**Prefer a read-only reviewer.** A reviewer that edits is an author holding review
authority, and this exception is precisely what they will reach for. Where the
reviewer must edit, the author dispositions those edits like any other finding.

## The record, and what its absence means

Record, at one authoritative location named in project instructions:

- the artifact and its **exact revision** — a commit sha; for a diff reviewed
  before it is committed, the staged tree id, then the sha it became, confirmed
  to carry that same tree. A patch digest names the change rather than the
  result. A path is not a revision and a branch name is not one either, because
  both move;
- the **author** model and effort level;
- the **reviewer** model and effort level, both **as requested** and **as
  confirmed by the runtime** — a model's own account of which model it is is a
  claim, not a confirmation;
- the invocation or session identifier, so the review can be found again;
- the outcome state;
- each finding and its disposition.

Three outcome states, and no others:

| State | Means |
|---|---|
| `no-findings` | The review ran and reported nothing above the bar |
| `findings-dispositioned` | The review ran; every finding has an author disposition |
| `blocked` | The review could not run, with the reason |

> **Requested and confirmed are different facts.** A pairing that silently falls
> back to the author's own model produces a record indistinguishable from a real
> cross-model review. The pairing cannot be audited from the reviewer's *claimed*
> identity alone.

**Absence of a record means unverified — never clean.** This is the general rule
that blindness must not render as a negative finding: nothing was observed, which
is a third state, and it is not a pass.

## When the reviewer cannot be reached

`blocked` is a state, not permission. A blocked review does not authorise
implementation, commit, or handoff. Three legitimate exits, in order of
preference: wait; escalate to a human; or proceed with an **explicit, attributed,
recorded** decision to ship unreviewed.

> **Never quietly substitute the author's own model.** A silent downgrade turns
> the protocol into a record of itself.

Project instructions must also settle the cases the fixed pair does not name, or
each session settles them differently and none of them says so:

- **A human author** — one member of the pair reviews; which one is a project
  decision.
- **A model outside the pair** — it is an author with no reciprocal partner.
  Name which member reviews it.
- **Mixed authorship** — reviewed by whichever pair member wrote none of the
  material under review. If both contributed, the artifact needs a human.
- **A model switch mid-change** — the reviewer follows whoever wrote the material
  being reviewed, not whoever is driving now.

## What belongs in project instructions rather than here

This file is the protocol. The binding is local and perishable — model names age
faster than anything else in an engineering document, and a skill that hard-codes
two of them is wrong on a schedule.

Put in `AGENTS.md`, completely rather than as a pointer: the two model identities
and their effort levels, the authoritative record location, the cycle bound, the
unavailability policy, and the authorship cases above.

`references/RUNNING-THE-REVIEW.md` covers invocation, the calibration procedure
that would move the hypothesis above from adopted to measured, and the failure
modes that make this protocol decorative. `assets/review-record-template.md` is
the record shape.
