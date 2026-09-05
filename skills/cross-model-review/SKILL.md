---
name: cross-model-review
description: Protocol for having every implementation plan and every diff critiqued by a different model in a fixed reciprocal pair — before implementation and before landing — with substantive findings only, a read-only reviewer, an explicit author disposition on each finding, an approve/revise verdict per cycle, a bounded re-review rule, and a record that tells a clean review apart from a skipped one. Use when starting implementation from a plan, preparing to commit or hand off, invoking or acting as a reviewer, recording or auditing a review, deciding whether a revision needs another cycle, resolving a disagreement between author and reviewer, choosing which models review which, or when the named reviewer cannot be reached.
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

> **The author decides what the artifact says; the reviewer decides whether the
> review passed.** These are different powers, and collapsing them in either
> direction breaks the protocol. A reviewer's claim needs checking exactly as much
> as an author's, and deference produces the wrong answer at the moment it feels
> most warranted — when the correction comes from whoever has been right all day.

A recorded rejection is worth more later than a recorded acceptance. An
acceptance is visible in the diff; a rejection is invisible everywhere else, and
it is the thing a later reader will otherwise re-litigate from scratch.

### Every cycle ends with a reviewer verdict

The dispositions are the author's. The **verdict** is the reviewer's, and it is
recorded per cycle:

| Verdict | Means | Effect |
|---|---|---|
| `approve` | Nothing above the bar remains | The checkpoint is passed |
| `revise` | At least one substantive finding stands unresolved | **The artifact does not proceed** |

`revise` blocks implementation, commit, or handoff. It is not advisory, and an
author who reads it as advisory has removed the checkpoint while leaving its
record in place.

Without a verdict, an author can reject every substantive finding on the merits
and proceed, and the record shows a completed review with dispositions on
everything — which is indistinguishable from a review that passed. **That is the
gap a per-cycle verdict closes: a review has to be able to conclude *no*.**

Two ways out of `revise`, and no third:

1. **Resolve and re-review.** Address the standing findings; the next cycle
   returns a verdict on the delta. **Available only while cycles remain** — see
   the bound below.
2. **Escalate the disagreement, explicitly and with attribution.** If the author
   rejects a finding on the merits and the reviewer does not withdraw it, that is
   an unresolved disagreement between two parties who both may be right. It goes
   to a **human**, named in the record, who decides. It does not get closed by
   the author because they are the author, and it does not get closed by the
   reviewer because they hold the verdict.

At the bound, only the second remains. Otherwise `revise` and "resolve and
re-review" form a loop with no exit, which is the same unbounded protocol in a
different costume.

This is why the reviewer's power is bounded at the verdict and does not extend to
the content. It cannot compel a change; it can refuse to say the review passed,
which forces the disagreement into the open instead of into whoever is more
insistent.

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

**There is no sanctioned third cycle.** Escalation sends the disagreement to a
human to *decide*; it does not authorise the pair to run again. A human can of
course direct another cycle — nothing here is enforced, and every rule in this
file yields to a person who overrules it. But that is an **override of the
bound**, and it is recorded as one, naming who directed it. Recording it as the
protocol working is the more damaging error: it converts the bound into a
formality that any sufficiently motivated party can satisfy by asking, and leaves
no evidence the limit was ever reached.

## The review is findings-only, and the reviewer is read-only

> **A reviewer reports findings. It does not edit the artifact.** Not a typo, not
> a comment, not a rename.

A reviewer that edits has become an author who also holds review authority over
their own edit, and nothing in the protocol reviews it. The edit arrives inside
the review, which is the one artifact everybody downstream treats as scrutiny
rather than as material needing scrutiny.

The cheap objection is that forbidding a one-word fix is bureaucracy. It is
cheaper than the alternative: a fix reported as a finding costs the author one
line and stays inside the mechanism, while a fix applied by the reviewer leaves
the mechanism entirely and looks identical afterward.

**This rule was reversed.** An earlier version preferred a read-only reviewer
while permitting edits under a materiality test. The test is sound and the
permission was not — an exception defined by effect still has to be *applied* by
somebody, and the person applying it is the one who wants the exception.
`references/RUNNING-THE-REVIEW.md` carries the reversal as a worked example.

### If a reviewer edited anyway, materiality decides what happens next

The rule above is instruction-enforced like everything here, so it will
occasionally be broken. When it is, the edit does not get a free pass for having
arrived inside a review, and the label the editor puts on it settles nothing.

**Material — a new cycle is required:** a change to executable behaviour, to an
interface, to a test or to what it covers, to a rule or instruction, to a claim,
to configuration, or to what was verified.

**Not material:** an edit that provably changes none of the above. It still gets
an author disposition, like any other finding.

> "A mechanical rename" is a claim about a diff, not a category of diff. A rename
> can break a reference, and in a documentation repository the prose *is* the
> product — so a comment fix can be the most material change in the change.

## The record, and what its absence means

Record, at one authoritative location named in project instructions:

- the artifact and its **exact revision**:
  - *a diff* — a commit sha; reviewed before commit, the staged tree id, then the
    sha it became, confirmed to carry that same tree. A patch digest names the
    change rather than the result;
  - *a plan* — a plan that lives in the repository needs **both** its path and a
    commit or blob id: a sha alone does not say which file was read, and a path
    alone moves. **A plan that lives in a chat, a session, or an issue thread
    still needs an identity**, or the most consequential checkpoint is the one
    whose subject cannot be produced later. Record a digest of the reviewed text,
    plus the session or event identifier that locates it. Reconstructing "the
    plan we reviewed" from memory is not a revision;
  - a path is not a revision, and a branch name is not one either, because both
    move;
- the **author** model and effort level;
- the **reviewer** model **and effort level**, each recorded twice — **as
  requested** and **as confirmed by the runtime**. They are four facts, not two:
  a fallback can change the effort without changing the model, and a review run
  at a lower effort than requested is a different review. Where the runtime does
  not report one, record it `unconfirmed`; a model's own account of which model
  it is, or how hard it thought, is a claim rather than a confirmation;
- the invocation or session identifier, so the review can be found again;
- the outcome state and the **reviewer's verdict** for the cycle;
- each finding and its disposition.

Three outcome states, and no others:

| State | Means |
|---|---|
| `no-findings` | The review ran and reported nothing above the bar |
| `findings-dispositioned` | The review ran; every finding has an author disposition |
| `blocked` | The review could not run, with the reason |

The outcome state says whether the review *ran*. The verdict says what it
*concluded*. Both are needed: `findings-dispositioned` with a `revise` verdict is
a blocked artifact, and recording only the first makes it look finished.

They are not independent. **`blocked` takes the verdict `not-run`** — a reviewer
that never ran concluded nothing, and any other value there is invented. Every
other outcome takes `approve` or `revise` and never `not-run`, or a review that
did run can be recorded as though it did not.

> **Requested and confirmed are different facts.** A pairing that silently falls
> back to the author's own model, or to a lower effort level, produces a record
> indistinguishable from a real cross-model review. The pairing cannot be audited
> from the reviewer's *claimed* identity alone.

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
