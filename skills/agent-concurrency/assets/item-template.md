# <One sentence naming the problem, not the solution>

**Status:** open
**Claimed:** —
**Found:** <date, and how — by hitting it, or by reading>

<!-- `scripts/open.ts` reads exactly four things: the `# ` title, `**Status:**`,
     `**Claimed:**`, and `**Blocked on:**` (which appears further down, only when
     a thing is blocked). `**Found:**` is for humans and is not parsed. Keep the
     format:

       **Status:**      open | claimed | blocked | refused
       **Claimed:**     an em dash when nobody holds it, otherwise a session
                        identifier AND A TIMESTAMP — age is diagnostic input
                        to the project's liveness policy, not permission to
                        steal a quiet claim
       **Blocked on:**  only when status is `blocked`; name the thing, not the
                        feeling. It is what the next agent should check.

     Only `open` is a task. `blocked` is waiting on something that is not
     effort. `refused` was decided against and never becomes work, however much
     it looks like the last item on a plan.

     There is deliberately no `done`. A finished item is DELETED only after its
     findings, decisions and verification have durable, accessible owners.
     This same item is the change packet when behavior changes; do not create
     a second proposal/task queue. The sections below are adaptable, not fields
     validated by the listing script. -->

## What is wrong

<!-- The observation, not the remedy. What happens, what should happen, and how
     you know — a command, a log line, a screen. If this was reasoned rather
     than observed, say so here; that is the difference between a defect and a
     suspicion, and both are worth filing under different headings. -->

## What to do

<!-- The recommendation and the reasoning, so whoever picks this up inherits an
     argument rather than a blank. This is the section that makes an item worth
     more than a line on a list.

     Where a decision inside the work is itself open, state the recommendation
     and why, including which direction the error falls in if you are wrong. -->

## What this does not fix

<!-- Optional, and usually the most useful section. The remedy above almost
     never restores everything the defect took; saying which part survives stops
     the next agent closing this and believing more than they should. -->

## Contract delta and acceptance

<!-- For a behavior change, link each affected current requirement owner and
     name added, modified or removed scenario IDs. State preconditions, action
     and expected outcome, including failure and compatibility cases. Link
     unchanged requirements instead of restating them.

     For a repair with unchanged requirements, say "no requirement delta" and
     link the existing cases. A documentation migration changes authority and
     routes, not behavior. Omit this section when it is genuinely inapplicable. -->

## Work and evidence

<!-- Put the bounded tasks and dependencies here, within this one claim.
     Per acceptance case, link the implementation and exact automated assertion
     or manual procedure. Planned checks are unverified. Record actual results
     with revision, command/procedure, environment and limits; a linked file or
     checked task box is not a passing test.

     Name checks not run or blocked and why. Preserve existing verification,
     review and delivery predicates; a structural spec check does not replace
     them. For new checks, name and run deterministic negative controls. -->

## Reconciliation before closure

<!-- Update affected contract owners with the reviewed behavior and evidence.
     Preserve decisions, rejected alternatives and findings in the topic's
     durable history, with links both to and from the current owner. Preserve
     existing anchors or redirects. Resolve concurrent requirement changes by
     review, not automatic spec merge. Only then delete this completed item.
     Keep genuinely outstanding work in this queue under its existing states. -->

## Where the reasoning is

<!-- Links only. Anything load-bearing belongs in the document it is about, not
     here — an item is deleted when it is finished, and everything in it goes
     with it. -->
