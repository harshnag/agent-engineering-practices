---
name: external-data-claims
description: Consuming somebody else's dataset without inheriting their assumptions — publishing the selection predicate beside every count, hard-failing on unrecognised categories, keeping nothing-observed, too-few, withheld and a measured zero as distinct claims, and never letting a derived number travel without what produced it. Use when ingesting a third-party or public dataset, mapping source categories to your own, joining datasets, computing a score or index from data you did not collect, choosing thresholds or bands, deciding how to display missing data, or writing a figure into a document, deck or interface.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Claims made out of other people's data

Every dataset was collected by somebody, for a purpose that was not yours, using
definitions they chose and did not necessarily write down. A number computed from
it inherits all of that and displays none of it.

The failures below are all **silent**. Each produces a plausible figure, changes
nothing visible downstream, and is found only when somebody re-runs the work with
a different definition.

## The dataset measures the process that produced it

> **A dataset is a record of the collection, not of the thing.** Reports measure
> reporting. Survey responses measure who answers. Logged errors measure what was
> instrumented. Anything that treats the two as the same is an unchecked claim.

It is the kind of wrong `checking-claims` is about: it produces no symptom until
it produces a plan.

Write the distinction into the **name**. A field called `events` is read as
events by everybody downstream forever; `reported_events` is not. Where only a
subset of records carries the property you group by, name the count for what it
is — *records that carried a location*, never *events* — because a large fraction
may never have carried one.

## Always publish the selection predicate next to the count

The anchor rule.

> **A count without its definition is not a fact.** Whether a tally is 25 or 33
> almost always turns on an inclusion question nobody wrote down, and neither the
> question nor its answer is recoverable from the figure.

In the origin project, a class was selected by filtering a free-text description
field on a literal label, where a standardised code was the correct key. It
returned **a 17% slice** of the true class, because the description field held
locally-invented strings rather than the standard's labels.

The transferable part is not the undercount:

> **The slice had a materially different distribution from the true class**, so
> it did not merely undercount — it produced a *different finding, with the same
> shape as a correct one.*

So: **select on the standardised key, never on a human-readable label**, and
publish the predicate — the field, the values, the window, the version — beside
every number you quote.

## An unrecognised category must be an error, not a zero

> **A value that silently defaults is indistinguishable from a deliberate
> exclusion** — opposite intent, identical representation, in the output and the
> interface and every export.

Two enforceable rules follow:

- **Exclusions are named entries with stated reasons.** If a category is left
  out, it is out *on the record*, with the argument attached. An exclusion that
  exists only as an absence cannot be reviewed, defended, or noticed.
- **The ingest hard-fails on any source category it does not recognise.** Not a
  warning, not a log line. A build that stops.

Vocabularies drift, and the drift is invisible. In the origin project a source's
category list held **43 distinct values across its full history and 37 in the
last twelve months** — and the six missing included two of the highest-weighted
categories in the mapping. A vocabulary built from the recent window would have
scored the most severe possible input as a non-event, raising nothing.

> **Build your vocabulary from the source's full history, not from a recent
> window**, and re-derive it on every ingest.

## Nothing observed, too few, no denominator and withheld are four claims, not one

A single "no data" treatment collapses distinct claims into one representation —
the silent-default failure again, at the presentation layer. **A measured zero is
a fifth thing and is not "no data" at all**, which is exactly why it must not
share a representation with any of them.

Keep them apart in the data model as well as visually:

| State | Cause | What it actually says |
|---|---|---|
| **Too few to show** | below a stability threshold | measured, but not stable enough to report |
| **No denominator** | the reference data you need is missing | the numerator is known; a *rate* cannot be computed |
| **Nothing observed** | no records reached you | you have no observation at all |
| **Withheld** | the publisher suppressed it | it exists and you are not permitted to see it |
| **A measured zero** | you observed, and the count was zero | a real finding, and the only one of these that is |

Two consequences, because they are the ones that get skipped:

- **Never render a withheld or unmeasured value as zero, or in the same treatment
  as a genuine low value.** No data is not a good result.
- **Where a category is systematically withheld above some rate, refuse to
  present it at that granularity at all.** Report it only at a level where it is
  complete, flagged as unavailable below that.

Measure that rate **per source, per ingest**. It is a local policy decision made
by whoever published, it differs between publishers, and a rate observed in one
source tells you nothing about another.

### Missing is not a measurement

The same error one level in. In the origin project a component of a derived score
was computed from a reference dataset holding zero records for a given unit — not
because the quantity there was zero, but because nobody had ever surveyed it.
That unit scored worst-possible. *Unsurveyed* and *absent* are opposite claims
with identical representation.

The repair generalises: **compute over the components that are known, report
which those were, and say so at the point of display.** Nearly half the units in
that dataset turned out to have no observation for that component at all — which
is a fact about the reference data rather than about the world.

## A scale invented in absolute terms is a broken scale that looks like a finding

Thresholds chosen from intuition, or carried over from a different population,
produce output with the exact shape of a result.

In the origin project, hard-coded thresholds that were reasonable for the
population they were written for put **113 of 116 units in the worst band** when
applied to a different one. That is not a finding, it is a broken scale, and it
read as a finding.

> **Derive bands from the distribution you actually have**, and gate on the
> shape: a check that fails when any band holds more than some share of the
> population catches this on the first run.

A hand-set threshold is also a constant with no recorded derivation, which
`measured-changes` names as one of the silent failure classes worth a gate.

## A join is a definition somebody chose

Every join claims two things are the same thing. Records to areas, areas to
populations, categories across sources, this period's boundaries to last
period's.

Each is an inclusion decision, and each is a place where a plausible number comes
out of a wrong pairing. Reference boundaries revised between editions, and
category schemes that differ per publisher, are where this goes wrong in
practice.

**Log and alert on records dropped by a join, broken down by category.** A join
that discards non-matching rows is otherwise completely silent — the count is
simply smaller, and nothing says so.

## The derivation ships with the verdict

> **A number with no visible derivation cannot be argued with by the people it
> describes**, which is the property that makes it harmful rather than merely
> wrong.

Every derived figure should be openable into what drove it: which inputs, which
weights, which window, which version of the source. That is also the only
mechanism by which a wrong figure gets *caught*, since nobody can check a number
whose provenance is unreachable.

**Version-stamp the data on every view**, not on a help page. The figure and the
snapshot it came from travel together or not at all.

## A summary figure travels without its caveats

> **A deck, a summary, or a headline number should carry the fewest and most
> robust figures that will support it.** A research document should carry *more*
> than its conclusions, because its job is to protect the next author from
> rediscovering the same trap.

The mistake is applying either rule to the other: a research document pruned to
its conclusions is a deck nobody can check, and a deck carrying every caveat is a
research document nobody reads. Decide which artefact you are writing before
deciding what to leave out.

## When the output is a judgement about people

If the figure ranks, rates, or scores anything describing a group of people or a
place where they live, the rules above stop being quality practice and become
accountability practice. Two change character entirely:

- **Never input a demographic attribute, or a proxy for one** — and be honest
  that income, property value, and similar variables are proxies.
- **A raw count is a map of exposure and of measurement intensity.** Shipping one
  "temporarily" because normalisation is harder ships the wrong claim under the
  right label.

The enforceable form is necessarily domain-specific and belongs in the project
holding the data. The origin project's version — a numbered list of design rules,
each carrying the exposure that motivates it — is linked in the frontmatter and
is worth reading as a model of what *enforceable* looks like, rather than for its
subject.

## One rule about how you will discover these

From the origin project, and it is the reason to read a list like this rather
than to build your way to it:

> **Building your way to the rule gets you most of the way and then stops,
> silently, exactly where the rule is load-bearing.**

Three distinct "no data" states were needed. Two were reached by building — they
caused visible trouble, so they got fixed. The third was got *wrong*: rendered as
nothing at all, indistinguishable from the background and from being outside the
dataset entirely, **in the very screen arguing that no-data does not mean good.**
It survived a full review pass and five rebuilds without ever looking like a
defect, and was found only when the three states were written out side by side as
distinct claims.

The states you reach by building are the ones that caused you visible trouble.
The state that needs the rule is the one that never did.

---

A checklist for ingesting a new source, and the fuller reasoning behind the
selection-predicate and silent-default rules, is in
[references/INGESTING-A-SOURCE.md](references/INGESTING-A-SOURCE.md).
