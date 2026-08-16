---
name: verify-in-the-real-thing
description: Why a passing test suite is not evidence that a built thing works, and what to do instead — driving the real artifact in the real environment, opening built artefacts rather than the documents about them, and handing back the checks you could not run. Use when about to call work done, when a suite passes and nothing has been opened, when reviewing or building a user interface, when writing a check for a rendering or interaction bug, when reading a README about an artefact, or when sandboxed or firewalled out of the environment the thing actually runs in.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Verify in the real thing

> **Drive the real artifact, in the real environment, before calling anything
> done.**

In the origin projects, essentially every real defect was found that way and
almost none by the test suite. That is not an argument against tests. It is a
statement about *which* defects a suite is shaped to catch.

## The suite and the artifact fail differently

A test asserts a claim somebody thought to make, against an object it constructs
itself. A person meets the assembled thing, in a real runtime, with everything
else present at the same time.

The defects living in that gap are the ones nobody thought to assert, and they
are usually *composition* failures — two correct pieces producing a wrong whole:

- **Stacking, layering, and paint order.** What is on top of what, and whether
  anything covers anything else.
- **Hit-testing.** Whether a press lands on the element you believe it does.
- **Cascade and specificity.** Which of two rules from two files won, resolved at
  load order.
- **Late arrival.** What moves when content loads, and what it moves *onto*.
- **Legibility, contrast, and scale.** Whether a person can read the thing.
- **Anything the platform draws for you** — rounding, safe areas, system chrome,
  colour management, device pixel ratio.

None of those has a natural assertion. All are visible in about a second to
somebody looking at the thing.

## Programmatic clicks do not hit-test

The sharpest instance, and the mechanism is the transferable part.

In one origin project, a shipped web app declared `.modal { display: grid }`.
That outranks the browser's own `[hidden] { display: none }`, so a blank
full-screen overlay sat over the entire app from first paint and swallowed every
click.

**The whole harness passed**, interactive checks included — because programmatic
`.click()` and direct function calls **do not hit-test**. The suite was driving
the app through a sheet of glass it could not see. A person found it in about a
second.

> **A test that calls a handler is testing the handler. Only something that
> dispatches a real event through the real compositor is testing the interface.**

The rule it generalises to:

> **If the failure is invisible to the mechanism that checks for it, adding
> checks of that kind cannot find it.** More assertions in the same style produce
> more confidence and no more coverage.

Afterwards the harness gained a check for *that specific mechanism* — whether
anything occludes the app at the point a person would press — and it was watched
failing on the real defect before being trusted. That is the correct sequence,
and it is `measured-changes`' *a gate that cannot fail is decoration* applied to
a defect you have just found.

## Open the built things, not just the documents about them

The same failure one level up, and it costs more.

In one origin project a session read a directory's `README.md`, skipped the
design artefacts the README described, and rebuilt an entire front end from
scratch in the wrong language — missing half the product, because several
product decisions existed only *in* those artefacts and in no prose about them.

> **A README is *about* an artefact. The decisions are *in* it.**

So when a repository contains a built thing — mockups, a design file, a deck, a
generated report, a sample output, a fixture — **open it**. The document beside it
is a summary written by somebody who had already seen it, and a summary is
precisely where a decision nobody thought to mention disappears.

This is `checking-claims`' inheritance rule with a different artefact type: prose
describing an artefact is a claim about the artefact.

## What "the real environment" means

Every step away from the deployed thing is a step where a defect can hide. Name
the ones you skipped:

| Step | What it can hide |
|---|---|
| A component in isolation | everything above about composition |
| The assembled app under a dev server | build-time transforms, minification, asset paths |
| A production build served locally | the real origin, headers, caching, CDN behaviour |
| The deployed thing | nothing structural — this is the artifact |
| One browser | engine-specific cascade, layout, and event behaviour |
| One viewport | anything gated on width, and any layout that only reflows |
| A desktop browser at a narrow width | touch targets, system chrome, real device pixel ratio |
| A real device | almost nothing, which is why it is worth the trouble |

> **A measurement is scoped to the conditions it was taken at.** In one origin
> project a perfect performance score was recorded and then re-read as a general
> fact; it was true of one viewport, on one run. Record the conditions with the
> result, or you have written down a different quantity from the one you measured.

## Re-confirm after a change; do not inherit the earlier tick

Once something has been verified by hand, the tick attaches to the *version that
was opened*, not to the artefact.

In one origin project an app icon was confirmed on a real device home screen —
the one check nothing automated could reach. The artwork then changed by a single
dot, and it was **confirmed again on the device** rather than inheriting the
earlier result.

That is the discipline: a hand check is a measurement, and `checking-claims` says
a measurement does not generalise past its arguments. The cheap version — when
you change something that was only ever verified by looking, look again.

## When you cannot do it, hand the check back

Sandboxes, firewalls, missing credentials, no browser, no device. This is common,
and it is not the failure. The failure is what an agent concludes next.

> **A blocked agent will conclude the suite was enough.** It is the only evidence
> it has, it is green, and nothing anywhere contradicts it.

So state the rule explicitly:

1. **Say plainly which checks you could not run**, and why.
2. **Hand them back** — in the handover, in the pull request, in the item. Name
   them as outstanding rather than describing the work as verified.
3. **Do not substitute reasoning.** "The change is small and the tests pass" is
   the exact inference this skill exists to interrupt.
4. **Do not weaken the check to make it runnable.** A rendering check converted
   into a source-level assertion is a different check wearing the same name.

A project depending on real-environment verification should say so in its
instructions file, name which checks need network, a browser, or credentials, and
require an agent that cannot run them to hand them back. See the
`project-agent-instructions` skill.

## Describe what you verified, at its real boundary

"Verified in the browser" is true of one browser, at one width, against one
environment — and is read as more than it says.

Write the boundary instead: which engine, which widths, which environment, and
what was never opened. That sentence belongs in the handover and in the commit
message, and it is the difference between a recorded observation and a
reassurance.

---

The anatomy of that overlay failure, a taxonomy of defects a suite is
structurally blind to, and a checklist for driving a change by hand are in
[references/WHAT-A-SUITE-CANNOT-SEE.md](references/WHAT-A-SUITE-CANNOT-SEE.md).
