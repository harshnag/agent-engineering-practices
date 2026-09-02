---
name: coordinating-agents
description: Coordinate a fleet of AI agents without treating stale session metadata, partial censuses, or delivered messages as ground truth. Use when orchestrating multiple workers, dispatching sub-agents or project sessions, deciding whether a worker is alive, issuing holds or corrections, monitoring a queue, archiving sessions, relaying findings between agents, or running scheduled and heartbeat agents.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Coordinating agents

A worker knows its own tree, command, and failure. A coordinator knows the queue
and which workers depend on which result. Neither has both views.

> **Local view beats remote view on local questions and loses on global ones.**

This is position, not seniority. A coordinator explaining a worker's failure is
doing the thing its position is worst at; ask for the failure output. A worker
deciding global queue order is doing the mirror image; volunteer the local cost
and let the coordinator place it.

## Make disagreement cheap

A coordinator cannot audit its own confident claims. It can make a worker's
check inexpensive:

- send the exact file, assertion, and clause rather than a paraphrase;
- say that the file on disk outranks the message;
- ask to be corrected;
- act visibly when corrected.

> **A paraphrase can be contested only with an opinion. A quotation can be
> contested with a command.**

The first duty of a fleet is not agreement. It is making a locally defensible,
globally wrong decision visible before several workers act on it.

## Delivery is not assignment

A successful create or send call proves that a request was accepted. It does not
prove a worker received the intended brief, understood the same item, or started
it.

Confirm an assignment by the worker claiming the named item in the shared work
protocol. A substantive message is not enough; the wrong well-formed brief is
still well formed.

> **A well-behaved worker with no instructions looks exactly like a well-behaved
> worker following them.**

Read back dispatch parameters immediately:

- the repository and checkout;
- the base branch;
- the item claimed;
- the execution mode;
- the identifier used for future messages.

The worker should perform the same readback on itself before writing.

## A census is not a count unless it can see the whole population

Session lists, checkout directories, process tables, branch refs, lock files,
transcripts, and pull requests each observe a different population. Unioning
them double-counts; choosing one undercounts.

Use each only for the direction it supports:

- recent file or commit activity is positive evidence of life, never evidence of
  death;
- an idle notification proves a turn ended in the past, not that the session is
  alive now;
- zero open pull requests means work may have landed, not that workers stopped;
- a missing active identifier may be evidence of exit only if the instrument can
  first see a known-live session;
- snapshot fields describe when they were written, not when they are read.

> **A field that was true when written will be read as true when read.**

If an instrument is built on undocumented state, make it prove it can see itself.
Failure to see its known-live subject must refuse the inference rather than
authorize cleanup.

### Lists end with a verdict

A long census can be truncated into a coherent fragment that says the opposite
of the whole. Every list-producing command ends with a self-contained one-line
verdict:

> `OTHER WORKERS PRESENT: 4; do not archive or claim their work.`

No exceptions, no wrapped sentence, and no flag the reader must already know to
request. The verdict is a reading aid, not a gate on other sessions' state.

## Liveness and death are asymmetric

A live worker can answer a direct message. Silence can mean dead, busy,
disconnected, awaiting approval, blocked on a person, or unable to receive the
message.

So:

1. Probe directly.
2. Treat a reply as evidence of life.
3. Treat every absence as unresolved.
4. Escalate or leave the worker alone; do not convert a timeout into ownership.

A last-activity timestamp is not a slow heartbeat. Long uninterrupted work is
exactly when it goes quiet.

Before archiving, use `agent-concurrency`'s pre-destruction protocol. Never
archive a worktree whose session is still running, including your own.

## Distinguish information from permission

"Tell me before you do this" is read as "wait for me", because waiting fails
silently while proceeding without permission leaves a visible error.

Mark every instruction as one of:

- **Inform:** act when the stated predicates hold, then report the result.
- **Stop and ask:** do not act; the outcome depends on a fact only the recipient
  or a person can supply.

Reserve stop-and-ask for real shared-state or human-presence decisions. A
session that waits produces no error, no red build, and no artifact. It simply
stops.

When a fleet-wide hold is necessary:

- name it;
- state what work it covers and what it excludes;
- do not block the mandatory gate needed to commit finished work;
- give workers staggered, named release slots;
- carry an expiry as recovery, not as a simultaneous release;
- lift it explicitly.

A shared expiry is a stampede, especially when resuming work triggers CI.

## Corrections have authority, time, and a channel

A correction is another claim. Apply `durable-project-memory`: update the
durable artifact first, then send a dated pointer and its evidence.

There is an additional coordination hazard:

> **Send a correction through the same channel as the claim it corrects.**

A faster channel can overtake the original. The mistaken message then arrives
last and reads as current. If a faster path is unavoidable, say exactly what
pending message it overtakes.

An interrupt names the state it is true of and gives one command for re-checking
it. It decays after one relevant change, often faster than the instruction it
corrects.

## Stop stale report loops

Replying to an old state report wakes the sender, which composes another report
against an even older world. Thorough replies can keep the loop alive longest.

Check whether the report contains a genuine request. Reply once if it does, then
stop. Silence is the only thing that drains a stale outbound queue.

Every state report carries a timestamp or, preferably, the command that
reconstructs the state. If the sender performs another relevant action after
reporting completion, it sends the changed fact too.

## Use the sideways channel for immediacy, not durability

Direct agent-to-agent messaging is useful because it can arrive before the next
handover. It is not project memory, a work claim, or evidence.

- Say the finding sideways so it arrives in time.
- Commit it so it arrives at all.
- Send the pointer, not a perishable payload.
- Carry the source chain; each relay otherwise drops the clause that lets the
  recipient weigh the claim.

Name the correspondent for credit. Cite the durable artifact for evidence.

## Coordinate the queue that matters

Ask what the queue is for and who waits at its far end. A tidy batch is not a
deliverable. Merge finished, reviewed, inexpensive work promptly rather than
holding it behind work that needs a scarce environment.

Before ordering expensive actions:

- the coordinator asks each worker what its action actually costs;
- the worker volunteers local cost and prerequisites without waiting to be
  asked;
- machine load is attributed by checkout or environment, not generic process
  name;
- decisions use an interval or an event, not one snapshot.

If you can see an effect and cannot evaluate its consequence, escalate. "Probably
fine" and "probably ruined" are the same unsupported move in opposite directions.

## Scheduled agents need an explicit empty result

For scheduled or heartbeat work:

- measure activation and read-in cost before enabling the schedule;
- put the recurring budget beside the schedule and report accumulated spend;
- make "no open work" a successful terminal outcome;
- state what the run must not invent, weaken, regenerate, or deploy;
- give blocked work a named hand-back path;
- ensure a stale tick received after standing down performs only a read-only
  check that the real coordinator exists, then exits.

A recurring cost is not a cost decided once.

## What a coordinator may never infer

Do not infer:

- death from silence or age;
- ownership from a pid, process name, or port;
- completion from a merged pull request;
- delivery from a successful dispatch call;
- global truth from one worker's local report;
- local cause from the coordinator's global view;
- machine capacity from a census of work.

Each has a neighboring instrument that returns a plausible true answer to the
wrong question. `checking-claims` governs those instruments;
`resource-safe-tooling` governs the machine and process boundary.
