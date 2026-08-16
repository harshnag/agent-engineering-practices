# What a suite cannot see

Read `SKILL.md` first. This is the worked detail: the anatomy of the failure that
produced the rule, a taxonomy of defects a suite is structurally blind to, and a
checklist for driving a change by hand. It loads on demand, so it is here rather
than in the skill body.

## Anatomy of the overlay failure

From an origin project, and worth reconstructing because every step was
individually reasonable.

**The code.** A modal was hidden with the `hidden` attribute — the platform's own
mechanism, backed by a user-agent rule of `[hidden] { display: none }`. The
stylesheet separately said `.modal { display: grid }`, to lay the modal out when
it was shown.

**The bug.** An author stylesheet rule beats a user-agent rule regardless of
specificity. So `display: grid` won, the attribute did nothing, and a full-screen
element with no visible content sat above everything from first paint.

**Why the harness could not see it.** Every check passed, the interactive ones
included, because they worked one of two ways:

- calling the handler function directly, which never involves the DOM at all; or
- calling `element.click()`, which dispatches to *that element* and performs no
  hit-testing.

Neither asks the question the bug answers: *if a person pressed at these
coordinates, what would receive it?* Only a real pointer event, dispatched
through the compositor at a position, does that.

**Why more checks would not have helped.** Every additional assertion in the same
style inherits the same blindness. This is `checking-claims`' rule about searches
— *a search inherits the assumption that makes the mistake possible* — in its
testing form:

> **A check written in the vocabulary that hides the bug cannot find the bug, and
> passing tells you only that the vocabulary is consistent.**

**The repair.** Not "add more interaction tests". A check for the *specific
mechanism*: that nothing occludes the root at the point a person would press. And
it was watched failing on the real defect before being trusted, which is the only
thing separating it from decoration.

## The taxonomy: what a suite is structurally blind to

Not a list of things nobody got round to asserting. These are categories where
the assertion cannot be written in the language the suite speaks.

**Composition.** Every element is correct; the arrangement is not. Overlaps,
occlusion, stacking contexts, z-order, clipping, overflow. Each component's test
passes because each component is fine.

**Resolution-at-runtime.** Which of two rules won, decided by load order rather
than by source. From an origin project: *a shared class name across two
stylesheets is a coin toss resolved at load order.* A source-level check reads
both files and sees both rules; the browser produces one outcome.

**Hit-testing and input routing.** What receives a press. Covered above.

**Timing and late arrival.** What is on screen at 200ms versus at 2s, and what
moves when the difference resolves. The counter-intuitive form, from an origin
project: *what moves is not what arrives late — it is what arrives late* **above**
*something else.* A late insertion stops being cosmetic the moment it lands on a
tap target.

**Platform-drawn output.** Corner rounding, safe areas, system chrome, colour
management, font fallback, device pixel ratio. Your code is not what produces the
pixels.

**Legibility.** Contrast, size, truncation, whether a label can be read at the
scale it is drawn. A test can assert a hex value; it cannot assert that a person
can read it.

**Domain-shaped rendering.** Any project whose output is a drawn artefact rather
than text has more of this surface than most — anything with a coordinate
transform, a threshold that changes what is shown at different scales, a
continuous value mapped to colour, content fetched in pieces as you move around
it, or labels that must not collide. All are things a test asserts a value for
and a person sees the result of.

**The environment itself.** Whether the build output is what ran, whether asset
paths resolve at the real origin, whether the data displayed is the data the
pipeline produces. A suite that constructs its own fixtures never asks.

## The one that reverses the rule

Worth stating so this is not read as "tests are useless".

A hand check finds the defect. It does **not** stop the defect recurring, does
not run on the next change, and is scoped to the one version somebody opened. So
the sequence is:

1. Drive the real thing. Find the defect.
2. Write a check for **the mechanism**, not for the symptom.
3. **Watch it fail** on the real defect.
4. Fix, and watch it pass.

Step 3 is not optional and is the one usually skipped, because by the time the
check is written the bug is already fixed. `checking-claims` gives the recovery:
copy the module to a temp path, reintroduce the break in the copy, point the
untouched check at the copy.

## Driving a change by hand: a checklist

Not a ceremony. The point is to record the boundary, so it is short and every
line ends up in the handover.

- [ ] **Build it the way it ships**, not the way it develops. Then serve that.
- [ ] **Open it and interact using real input** — press, scroll, type, drag. Do
      not call anything.
- [ ] **Look at first paint**, before data arrives. Then look again after.
- [ ] **Two widths at least**, one of them narrow enough to reflow.
- [ ] **One real device** if the artefact has any mobile story at all.
- [ ] **Read the console.** Errors that break nothing visible today are the ones
      that break something next week.
- [ ] **Check the thing you changed *and* the thing next to it.** Composition
      failures are not local.
- [ ] **Write down the boundary**: which engine, which widths, which environment,
      and what you never opened.

## When the artefact is not a screen

The rule is not about user interfaces. Substitute the artefact:

| Artefact | "Drive the real thing" means |
|---|---|
| A CLI | run it in a real shell, with real arguments, and read the output |
| A data pipeline | run it against the real source, not a fixture, and look at what came out |
| An API | call it over the network, with real auth, from outside the process |
| A document or deck | open the rendered output, not the markup |
| A migration | run it against a copy of the real database |
| A generated file | open the generated file |

In each case the suite constructs its own input, and the real source is the thing
that changed underneath you.
