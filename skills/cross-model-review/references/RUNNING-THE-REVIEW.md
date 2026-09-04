# Running the review

Read `SKILL.md` first for the protocol and for why it is a checkpoint rather than
a gate. This is the operational half: how to invoke the reviewer so the review is
real, how to find out whether the pairing is worth anything, and the ways it
quietly becomes a formality.

## Invoking the reviewer as a genuinely separate context

The reviewer must receive the artifact and the repository. It must **not** receive
the author's reasoning as justification.

That distinction is the difference between a review and a confirmation. An agent
handed "here is my plan and here is why it is right" is being asked to agree; the
same agent handed "here is a plan, here is the repository, check it" is being
asked a question with a real answer.

A workable invocation carries:

1. **Role and pairing, stated.** Who authored, at what effort; who is reviewing,
   at what effort. **A model repeating the pairing back is not confirmation of
   it** — a fallback model reads the same prompt and says the same words, which
   is precisely the failure the record is supposed to expose. Only the runtime's
   own invocation metadata confirms which model answered. Where the runtime does
   not expose it, record `unconfirmed`, and mean it.
2. **What to read first**, by path. A reviewer that has not read the project's
   rules cannot find a violation of them, and will substitute general good
   practice — which is the most convincing way to be useless.
3. **The artifact**, at a stated revision.
4. **The bar**, quoted from `SKILL.md`, including that finding nothing is a
   legitimate outcome and that filler is not wanted.
5. **Numbered findings, and a verdict**, both required. Numbering is so each
   finding can be dispositioned individually — an essay cannot be dispositioned;
   a list can. The verdict is `approve` or `revise`, stated explicitly, because a
   review that cannot conclude *no* is a review the author can complete by
   rejecting everything.
6. **A standing instruction to treat the author's claims as claims** — and to
   re-run anything the author says was verified, rather than accepting it.
7. **Report, do not edit.** State plainly that the reviewer must not modify the
   artifact, including trivially. A patch inside a review is the one change
   nothing downstream reviews.

Point 6 is the highest-yield line in the prompt. The strongest use of an
automated reviewer is adversarial rather than confirmatory: ask it to reproduce
claimed verifications, not to summarise the change.

## Calibration: the procedure that would make the hypothesis measurable

`SKILL.md` states plainly that the value of *cross-model* pairing is adopted, not
measured. It is measurable, cheaply, and until somebody runs this the pairing
should keep saying so.

For each direction of the pair, separately:

1. Take a real artifact the reviewer would plausibly see.
2. Plant exactly one substantive defect, in a category the protocol claims to
   cover — a wrong claim, a check that cannot fail, a broken invariant.
3. **Confirm the mutation actually created the defect**, independently of the
   review. A passing calibration has two explanations, and "the defect was never
   there" is the boring one.
4. Run the review, with the standard prompt and no hint.
5. Record whether it was found, and at what position in the findings.

Work on a copy, never in the tree another agent is reading.

Two results worth separating:

- **A miss tells you the coverage**, which is worth knowing *before* relying on
  the protocol rather than after.
- **A catch by one direction only** is the first real evidence that the two
  models have different blind spots — which is the entire hypothesis. One
  direction catching it is not the same result as both catching it, and the
  record should say which.

Until both directions are calibrated, record them as **unmeasured** rather than
leaving the reader to assume.

## A worked disposition

The shape that makes the record useful later:

> **Finding 4 (reviewer, high):** the plan describes the review checkpoints as
> "mandatory gates", which contradicts the project's own rule that a gate is a
> mechanism able to refuse.
>
> **Disposition: accepted.** Reworded to "checkpoints", with an explicit sentence
> saying the protocol is not a gate and why calling it one is worse than having
> no gate.

And a reversal, which is the most valuable record of all — because a rejection is
not permanent, and the record is what lets it be reopened rather than
re-litigated from nothing:

> **Finding 9, cycle 1 (reviewer, high):** the reviewer-edit exception is
> exploitable; the reviewer should be forbidden from editing entirely.
>
> **Disposition: rejected in part.** A hard prohibition would block the cheapest
> useful case. The exception is instead defined by semantic effect rather than by
> the editor's label, and read-only is stated as the preference.
>
> **Re-raised, cycle 3, verdict `revise`.** An exception defined by effect still
> has to be *applied* by somebody, and the person applying it is the one who
> wants it — so the test never fires on the case it was written for.
>
> **Disposition: accepted; the earlier rejection is reversed.** Review is now
> findings-only and the reviewer is read-only. The materiality test survives as
> the rule for what happens when a reviewer edits anyway.

That exchange is the protocol working as intended: the author rejected on the
merits, the reviewer did not withdraw, and the disagreement stayed visible until
it was settled rather than being closed by whoever spoke last. Note that it took
a `revise` verdict to do it — under dispositions alone the first rejection would
have ended the matter, with the record showing a completed review.

Both shapes are one artifact reference, one claim, one decision, one reason.
Neither requires the reader to reconstruct what was argued.

## How this becomes decoration

Each of these leaves the record looking healthy.

**The reviewer that never rejects.** Same rule as any check: if it cannot fail,
it is not a check. A run of `approve` verdicts is either a well-run project
or an unmeasured reviewer, and nothing in the record distinguishes them. This is
what calibration is for. **Count the `revise` verdicts** — a pair that has never
issued one has not been shown to be able to.

**The verdict that is read as advice.** `revise` blocks. An author who treats it
as a strong suggestion has removed the checkpoint while leaving its record
looking complete, which is worse than skipping the review outright: a skipped
review leaves no record, and this leaves a reassuring one.

**The silent downgrade.** The named model is unavailable, the tool falls back,
and the record says a review happened. Recording the *confirmed* reviewer model
and effort alongside the requested ones is the only defence, and it works only if
somebody reads the pairs as pairs. Effort is the half that gets forgotten: a
fallback to the same model at a lower effort leaves the model field correct and
the review weaker than the one the record describes.

**The review that arrives after the decision.** A diff review requested while the
commit is already being written is a formality with a timestamp. The checkpoint
is before the action, or it is a comment.

**The prompt that leaks the answer.** Handing the reviewer the author's reasoning
produces agreement that reads exactly like independent confirmation. This is the
most common way to get a clean review of a broken change.

**Cycle fatigue.** Every re-review costs latency, so the pressure is always
toward declaring a revision immaterial. The materiality test in `SKILL.md` is
written in terms of effect for this reason — an author under pressure will use
any test written in terms of intent.

**A record nobody reads.** An audit trail with no reader is a cost with no
benefit. Put it where review already happens — the pull request — rather than in
a file whose only visitor is the process that writes it.

## What this protocol does not do

It does not replace branch protection, required checks, or human approval, and it
is not a substitute for the rule that an agent must never approve its own pull
request. It sits earlier and is weaker by construction: it is the practice of
having somebody else read the work, formalised enough to be auditable, and
enforced by nothing but the instruction to do it.

See `agent-concurrency` and its `references/AUTOMATING-REVIEW.md` for the
enforcement layer that can actually refuse.
