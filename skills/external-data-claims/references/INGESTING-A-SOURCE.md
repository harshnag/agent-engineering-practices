# Ingesting a source

Read `SKILL.md` first. This is the operational checklist and the fuller reasoning
behind the two rules that do the most work. It loads on demand, so it is here
rather than in the skill body.

## Before you write any mapping

- [ ] **Find the publisher's own documentation of the schema**, and read what
      each field *is* rather than what its name suggests. Where no documentation
      exists, record that — it is a fact about your confidence, not a gap to fill
      with inference.
- [ ] **Enumerate the full vocabulary of every categorical field, across the
      source's entire history**, and diff it against a recent window. Values that
      appear only historically are exactly the ones a recent-window mapping
      silently drops.
- [ ] **Identify the standardised key for every field you will select on.** If
      the only available key is a human-readable label, say so explicitly — you
      are now selecting on prose somebody types.
- [ ] **Find out what the publisher withholds, and at what rate**, per category.
      Measure it; do not assume a rate you saw elsewhere.
- [ ] **Establish what a missing value means in this source.** Not collected, not
      applicable, withheld, zero, and unknown are five different things, and many
      publishers use one representation for several of them.
- [ ] **Record the snapshot** — version, date, query, row count. A figure that
      cannot name its snapshot cannot be reproduced.

## While mapping

- [ ] Every source category maps to a named entry, **including the excluded
      ones**, each with a stated reason.
- [ ] Unrecognised category → **hard failure**, not a default.
- [ ] Every join logs its unmatched rows, by category.
- [ ] Every count you emit carries its predicate: field, values, window, version.
- [ ] Distinguish the kinds of not-a-number **in the data model**, not only at
      the point of display. One nullable column cannot carry four claims.

## After the first run

- [ ] **Compare against a figure the publisher themselves report**, if one
      exists. A total that disagrees with the publisher's own is the cheapest
      available signal that a predicate is wrong.
- [ ] **Look at the distribution, not the aggregate.** A band holding almost
      everything, or almost nothing, is a broken scale wearing the shape of a
      finding.
- [ ] **Re-run it.** From `checking-claims`: a claim that came from a command is
      checked by running the command again. In the origin project, every silent
      defect in the ingest research was found this way and by nothing else.
- [ ] **Watch the ingest fail** on a deliberately unmapped category before
      trusting that it would. A gate that cannot fail is decoration.

## Why the selection predicate is the anchor rule

Because it is the only one of these that makes the others *checkable*.

A count published with its predicate can be disputed: somebody can disagree with
the window, the field, or the value set, and the disagreement is about something
written down. A bare count admits no such conversation — the only available
responses are to trust it or to redo the work.

That is also why the rule is *publish it next to the count* rather than *record
it somewhere*. A predicate in a methodology document and a figure in an interface
are two artefacts, and the figure is the one that travels. Every quotation of the
number strips the document.

The failure has a characteristic feel worth learning to recognise. In the origin
project the wrong slice **did not look like an error — it looked like a smaller
population.** A wrong predicate does not produce a corrupt number. It produces a
coherent number about a different set, and coherence is what review is checking
for.

## Why the silent default is the most dangerous single behaviour

Tolerating unknown input is *correct* in most production systems. It is what
keeps old saved data working, what stops one bad row taking down a pipeline, and
what makes a format extensible. It is the right default nearly everywhere.

It is catastrophic at exactly one boundary: **the point where somebody else's
vocabulary becomes yours.**

There, an unrecognised value is not a tolerable irregularity. It is a category
you have no opinion about, being assigned the opinion *nil* — and the
representation of *nil* is identical to the representation of *we considered this
and excluded it*, which is a decision somebody made deliberately and wrote down.

Same bytes, opposite meanings. Nothing downstream can distinguish them, and no
amount of review at the display layer recovers the difference, because the
information was destroyed at ingest.

This is the same rule `measured-changes` states about harness fixtures — *silent
tolerance is correct in production and catastrophic in a harness* — arriving from
the data side. The general form:

> **Tolerance is right where you own the vocabulary and wrong where you are
> borrowing one.**

## Why "no data" needs more than one treatment

The collapse is seductive because it is honest at the top level: you genuinely do
not know. The problem is that the four *not-known* causes have materially
different implications for whoever reads it — and that a measured zero, which is
knowledge, must not join them.

- *Too few to show* is a statistical caution. The measurement happened; the
  number is unstable. More time or a wider unit fixes it.
- *No denominator* is a gap in **your own** reference data. The observations
  exist and you cannot compute a rate. Fixing it is your job, not the
  publisher's.
- *Nothing observed* may mean the thing did not happen, or that nobody reported
  it, or that this unit is not covered by the source at all. It is the one state
  that can conceal a total absence of coverage.
- *Withheld* means it exists and you are not permitted to see it. Rendering it as
  absence is straightforwardly false.
- *A measured zero* is none of the above. You looked and there was nothing, which
  is a finding — and the only reason it is listed here is that it is the value
  every one of the four above gets silently rendered as.

Collapsing them tells the reader "we don't know" while discarding *why*, and the
why is the part that decides what they should do about it.

## What makes this whole class worth the trouble

Every failure in this skill produces a plausible number. None produce a crash, a
red test, or a visible defect. The entire class is invisible to the normal
signals a project runs on — which is why every mitigation here is *at ingest* and
*loud*: a hard failure, a logged drop, a published predicate, a distinct
treatment.

You do not catch these by looking harder at the output. Looking at the output is
what everybody was already doing.
