---
name: durable-project-memory
description: Turn engineering work into durable project memory without bloating every agent prompt — deciding what belongs in a reasoning document versus a repeatable skill, recording root causes and external research, correcting stale claims, and routing large documentation corpora. Use when closing an investigation, writing a design or research note, deciding whether to create a skill, preserving findings from web or vendor research, correcting advice already sent to another agent, compressing long documentation, or designing how agents find the right part of a large documentation set.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Durable project memory

A solved problem is not durable because the code landed. The observation,
rejected explanations, decision, and verification are usually absent from the
diff, and the next session can rediscover all four.

The answer is not to put everything in the instructions file or to create a
skill for every bug. Those make all future sessions pay for knowledge they may
never need.

> **A project fact belongs in the project's reasoning. A repeatable workflow
> belongs in a skill.**

## Record the whole result, not only the remedy

Before closing an investigation, write four things into the document that owns
the affected system:

1. **Report:** what was observed, at which boundary, and when.
2. **Root cause:** what is proved, separated from what is merely consistent with
   the evidence.
3. **Decision:** what changed, what was refused, and why.
4. **Verification:** what was run or opened, including what it cannot establish.

A fix without the report cannot be recognised when it recurs. A decision without
the rejected alternatives gets reversed by somebody who rediscovers only their
advantages. A verification with no boundary becomes reassurance.

Commit messages still explain why a particular diff exists. They do not replace
the reasoning document: a later session routes by subject, not by guessing which
commit discussed it.

## Choose the artifact by the job

| Knowledge | Where it belongs |
|---|---|
| A rule every session must apply immediately | the project instructions, in its shortest actionable form |
| A project-specific design, failure, or decision | the reasoning document for that subsystem |
| Current state, unfinished work, or an unverified boundary | the handover or a claimable work item |
| Evidence learned outside the repository | a dated research note, linked from the decision it supports |
| A workflow reusable across projects | a skill |
| A one-off command result | nowhere, unless it supports a durable claim |

> **A new skill for every failure is bloat. A finding left only in a session is
> amnesia.**

Promote a project rule into a skill only after you can state the mechanism
without the project's names, vocabulary, thresholds, commands, or operating
environment. If removing those details removes the lesson, it is project memory,
not a portable workflow.

## External research is a deliverable

Research acquired outside the repository is unusually droppable: it can be
expensive to obtain and completely invisible in the code diff.

> **Commit the finding before acting on it.**

Use one note per question so parallel researchers touch disjoint files. Every
note carries:

- **The date.** Vendor behavior and public guidance move.
- **The source beside the claim it supports.** A bibliography does not say which
  sentence a source establishes.
- **The verification boundary.** State what you read in a primary source and
  what came from a summary, search result, or secondary source.
- **Negative findings.** Record what you looked for and did not find; otherwise
  the next session cannot distinguish "nobody checked" from "checked, absent".

The research note owns the evidence. The subsystem document owns the decision
made from it and links back. Keeping those separate lets a decision change
without deleting the evidence that once supported it.

`assets/research-note-template.md` is a portable starting shape.

## Corrections do not inherit authority

A message headed "correction" is another claim, not an override.

1. Correct the durable artifact first.
2. Point to the replacement with a date.
3. State the evidence and scope behind it.
4. Withdraw the old claim when the evidence is too thin to found a replacement.

> **Thin evidence can retract a claim. It cannot silently promote itself into a
> stronger one.**

Keep perishable values, commands, model names, thresholds, and current state out
of kickoff messages. Send a pointer, method, and scope instead. The receiver can
then re-read current truth rather than inheriting a number that was already
aging when sent.

## Route a large corpus; do not prescribe reading all of it

An instruction to read more documentation than fits in a session is not strict.
It is unfollowable, so every session invents a route without saying so.

Use three layers:

1. **A small compulsory entry set:** current handover, concurrency rules, recent
   history, and the instruction-freshness check.
2. **A task-to-document routing table:** which document answers which class of
   question.
3. **Addressing inside long documents:** generated contents plus a heading or
   symbol search that carries line numbers.

An index is for addressing, not summarizing. It helps a reader arrive at the
right neighborhood; it does not license reading less of the topic being changed.
Read neighboring sections once routed, because a mechanism one level above the
current symptom is often the reusable part.

### Budget indexes by what readers consume

Heading counts are a poor index budget. A few long headings can cost more than
many short ones, and a generated block is paid on every read even when the
document is not.

Use a byte or token ceiling, state what the index omits when it crosses the
ceiling, and provide the cheaper fallback command next to it. A shallow index
must announce that subsections are absent; otherwise it is most incomplete
exactly where the document is largest while presenting itself as complete.

> **Addressing that degrades silently becomes a coherent fragment of the
> corpus, and a coherent fragment is easily mistaken for the whole.**

Put the final count or verdict on the last line of listing tools as well as near
the top. Output can be truncated at either end by callers, logs, or context
limits. A partial list with no visible denominator can state the opposite of the
complete result.

## Compress only when a selector still selects

"Shorten the docs without losing anything" is an unbounded editorial task. It
has no objective stopping condition and eventually replaces reasoning with a
summary.

Bound compression with a selector:

- exact repeated units,
- stale current-state claims,
- duplicated rules with one authoritative home,
- generated material whose cost exceeds its budget,
- or sections no route reaches.

Measure before and after. Stop when the selector no longer finds candidates.
The remaining length is not proof the corpus is ideal; it is proof that this
compression task is finished.

## Make the memory reachable

A durable note that no read-in route, subsystem document, or search convention
can reach is gone in practice.

Checks worth having:

- the project instructions still link to the research convention;
- research notes carry a date, a source, and a verification boundary;
- every generated index agrees with the headings that exist;
- the routing table names every load-bearing reasoning document.

Each needs an independent oracle. A heading-derived index cannot detect a
heading and its index entry disappearing together; compare against an
independent expected inventory or mutate a known required section away and
watch the check fail.

This is `checking-claims` applied to memory: agreement between two artifacts
derived from the same source proves consistency, not completeness.
