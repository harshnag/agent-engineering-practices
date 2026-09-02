---
name: resource-safe-tooling
description: Design and run build, test, benchmark, concurrency, and process-control tooling without endangering a shared host or mistaking coordination for containment. Use when adding parallel workers, stress or load tests, repeated mutation loops, CPU-heavy CI, machine admission checks, process cleanup or reaping, background servers, PID or process-group signalling, concurrency tests, or any command that may consume most of a shared or low-resource machine.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Resource-safe tooling

Worktrees split files, branches, and indexes. They do not split the machine
underneath them.

The threat is not a malicious program. It is several ordinary commands, each
correct in isolation, multiplying on a host that also carries interactive work,
CI, browsers, and other sessions.

> **The machine is the one shared resource the repository cannot isolate by
> convention.**

## Coordination is not containment

Keep three layers distinct:

| Layer | What it can promise |
|---|---|
| Coordination | who should run and in what order |
| Priority | who should win when work contends |
| Hard enforcement | consumption cannot cross a boundary |

A lock, queue, token, environment variable, worker count, or polite scheduler
inside the checkout is coordination. Checkout code can bypass or rewrite it.
Process priority is defense in depth. Only a limit imposed outside the workload
is a machine boundary.

> **Never borrow the language of enforcement for a cooperative control.**

If hard isolation is unavailable, say which aggregate risk remains accepted.
Do not imply it away.

## A per-process cap is not a machine-wide budget

A checked-in worker limit bounds one invocation. Several sessions each honoring
it still multiply past the machine's capacity, and a build tool may fan out
internally after your limit.

Use per-invocation caps anyway: they are useful containment and should have no
override that can exceed the checked-in ceiling. But describe them precisely:

> **This bounds one command, not the host.**

Keep the checks, samples, and assertions intact. Reduce simultaneous work rather
than weakening what one run verifies.

## Ask about the machine before creating more work

Most fleet instruments ask about work that already exists: open items, sessions,
branches, or processes. None answers the decision made immediately before
dispatch: *is there room for one more?*

Where admission is necessary:

- use separate verdicts for **clear**, **tight but measured**, and **refuse**;
- exit non-zero on refusal;
- treat every input that could undercount as refusal;
- reserve atomically before returning permission, or two readers can spend the
  same last slot;
- do not expire an uncertain reservation into permission; require an explicit,
  identified release;
- borrow limits from their authoritative configuration rather than introducing
  another number that can drift.

> **"Tight" means a complete valid measurement. It is not a worried name for
> uncertainty.**

A cooperative admission protocol can cost more than it buys. Measure it. If it
leaves a silent machine unused while adding no enforceable boundary, retire it
without pretending the earlier measurements were false; the objective changed.

## Refuse saturation on a shared interactive host

Synthetic saturation includes CPU spinners, process swarms, repeated
high-concurrency runs, concurrent verification storms, and timing tests that
manufacture pressure to make a race likely.

The rule also covers ordinary tooling:

> **A rule that exempts the command run every day is not a rule about
> saturation.**

Do not run saturation work merely because the host is currently quiet. An
isolated time window is not resource isolation, and a bare dedicated machine is
not a hard limit. A saturation experiment needs a hard-bounded environment,
explicit human authorization, a stop condition, and monitoring outside the
workload.

An incident may justify this operational refusal without proving a root cause.
Write separately:

- what the logs prove;
- what overlapped in time;
- what remains unattributed;
- why the consequence still makes the risk unacceptable.

Confidence and proximity are not attribution.

## Prove concurrency with state, not pressure

Timing is a weak concurrency oracle. Process startup, scheduling, cleanup, and
the checker itself can consume the margin, so a loaded host turns a product
assertion into an operating-system assertion.

Prefer a deterministic executor:

1. Each operation records that it started.
2. It returns an unresolved promise or waits at a barrier the test controls.
3. The test inspects the number and identity of in-flight operations.
4. The test releases one operation at a time and checks the transition.

This separates three claims that are often collapsed:

- operations can overlap;
- overlap is bounded;
- completion order has a promised relationship to start order.

> **Timeouts contain deadlock. Event order proves the property.**

Widening a barrier timeout does not weaken the concurrency assertion. Widening a
wall-clock performance bound does.

### An oracle must not race its own evidence

Avoid liveness files that are deleted on exit, global marker namespaces that
accumulate across waves, and child processes that can finish before peers inspect
them. Evidence that outlives every run becomes a visitors' book; evidence that
disappears with a fast run creates false failures.

Generation-scope every artifact and assert cleanup separately. Better, remove
processes and clocks from unit-level concurrency checks entirely by injecting
the executor.

Never synchronously block the thread that services the test runner's timeout.
An awaited timeout cannot fire while its own event loop is blocked. Yield and
bound each wait leg explicitly.

`assets/concurrency-control-checklist.md` gives known-good and known-bad controls.

## One ordinary run completes the evidence

After deterministic controls pass, take one ordinary run of the real command.
Record:

- requested policy versus actual readback;
- peak process count;
- peak resource use, with each metric named;
- wall time as capacity-planning evidence, not a pass threshold;
- exit-code parity with the uncapped command;
- cleanup residue.

Do not add repeated runs, concurrent runs, induced pressure, or a spinner merely
to make the evidence feel stronger. The deterministic test proves the property;
the ordinary run proves the integration exists.

## Numeric process identity cannot authorize a later signal

A process id or process-group id can be correct when inspected and belong to
something else when signalled. Checking start time, executable, arguments,
parent, owner, group, and working directory only moves the race between the last
check and the action. It does not make them atomic.

Ports and command names answer neighboring questions:

- a closed port does not mean no processes remain;
- freeing one port is not cleanup;
- a command line can mention a target without being it;
- a generic runtime name is not project ownership;
- an archived session may leave every child running.

> **A snapshot may authorize a report. It cannot authorize destructive cleanup
> unless the platform exposes a stable handle to the validated process.**

If it does not, make cleanup report-only. Do not leave a destructive flag hidden
behind an otherwise safe census, and do not turn the refusal into instructions
for raw signals, port killers, name-based killers, or signalling the report's
numbers by hand.

Cooperative lifecycle control is the repair: the process owns a private control
channel, authenticates a stop request, acknowledges shutdown, and the controller
waits on the same stable handle it started. If start and safe stop cannot ship
together, persistent start stays disabled.

## Crash recovery is about environments

A volatile record naming one process group is lost with the controller and may
later name recycled work.

Before starting work:

1. durably publish the environment identity and intended resource policy;
2. start the environment;
3. read back the actual policy and bind it to the record.

After a crash or resume, grant nothing until every durable record is reconciled
and each old environment is explicitly adopted or destroyed by a mechanism that
can prove ownership. Age is not an oracle.

## Mutation windows are broken repositories

A mutation test deliberately creates the defect it guards. A crash between
apply and restore leaves sabotage with no label saying it was temporary.

- mutate only a disposable copy or worktree;
- refuse a target with uncommitted changes;
- confirm the mutation changed the intended property independently of the gate;
- run one known-good and one known-bad control, not a repetition loop;
- restore in the same operation with signal traps;
- hash-compare before and after, then inspect status.

Signal traps are interruption-safe, not crash-safe. Restoring from the last
commit is safe only in a known-clean disposable target; in a dirty tree it
destroys legitimate work and reports a perfectly clean loss.

## Report boundaries on every run

Every resource tool prints what it proves and what it cannot:

- per-process containment versus machine-wide enforcement;
- process census versus ownership;
- temporal overlap versus causal attribution;
- wall time versus correctness;
- ordinary-run evidence versus saturation behavior.

A clean report is believed. A falsely empty one is worse than having no tool.
