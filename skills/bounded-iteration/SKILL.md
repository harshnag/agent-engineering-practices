---
name: bounded-iteration
description: Rules that keep an agent's time, tool calls and tokens proportional to verified progress, so it does not go in circles. Use when iterating on a failing test or check, adjusting values by trial, rerunning a slow suite, deciding when to stop or re-scope, writing a prompt for a sub-agent, monitoring a running worker for loops or check-gaming, reporting progress, or giving a project fast targeted test entry points.
license: MIT
metadata:
  provenance: Extracted from a private production codebase, 2026
  author: harshnag
  version: "1.0"
---

# Bounded iteration

Effort is wall time, tool calls and tokens. Progress is a check that passes now
and did not before. An agent in a loop spends the first without producing the
second, and every individual step looks reasonable.

> **Effort that does not change which checks pass is not progress, however
> busy it looks.**

## The failure this prevents

In the origin project, a sub-agent asked to rebuild one self-contained unit of
content ran for about 90 minutes and more than 100 tool calls. It changed
numeric values by one unit at a time, and after each change reran the full
suite, 63 jobs and about 60 seconds, reading the whole log. It also added data
that only a contract check read and the product ignored, so the check passed
while the property it guarded was absent.

Three habits compounded: a slow feedback loop, guessing instead of diagnosing,
and satisfying the check instead of the design. The repair was a filter that ran
one job in about 2 seconds, and the rules below.

## Smallest check first

- Iterate on the narrowest check that can fail on what you are changing: one
  test, one job, one file's parse or type-check.
- Run the full suite once, after the targeted check passes and before
  committing. Not after every edit.
- Filter output for failures: exit code, a one-line summary, the failing
  assertion. Read a full log only when the filtered view does not explain it.
- If one iteration costs more than about a minute, fixing the loop is the first
  task. Usually that means adding a targeted entry point.

## Diagnose, then change

After a failure, find the cause with one targeted observation before editing: a
print, a state dump, the assertion's actual and expected values, a debugger
stop. The edit should then predict its own result.

> **Never nudge a number and rerun to see.**

If a value really has to be found by search, write the search as a script that
sweeps the range and prints a table, not as a sequence of hand edits.
`measured-changes` covers tuning when the effect is smaller than the noise.

## Two strikes

If the same check fails twice after attempted fixes, stop patching. Write down
the believed cause and the evidence for it, then change approach: a different
hypothesis, a smaller reproduction, reading the code the check exercises, or
asking.

After a third failure, report blocked with evidence: the check, each attempt,
its output, and what you now believe.

"The same check" means the same assertion failing the same way. A different
failure is information, and may be progress.

## Checks test the product

Never add data, flags, branches, fixtures or exemptions that exist only to make
a check pass. The test is simple: **if the only reader of a change is the check,
the change fakes the property the check guards.**

Fix the design. If the check itself is wrong, change it openly, give the
reasoning in the commit message, and flag it for review. Skipping a test,
widening a tolerance, and loosening a pattern are check changes too.
`measured-changes` covers structural checks that encode a design promise.

## Time boxes and stop conditions

Every task, and every delegated task without exception, starts with a time box
and a stop condition: what done looks like, and what makes the approach wrong.

At the box, commit only verified work and report progress, blockers and the next
step. The box is a checkpoint that forces a decision about the approach, not a
deadline to rush toward. Extending it is a decision somebody makes explicitly.

## Progress is visible

A report names what now works that did not, with evidence: the command and its
result. "Edited twelve files", "still tuning" and "nearly there" describe
activity.

Two consecutive reports with no newly passing check mean re-scope: split the
task, change the approach, or return it blocked.

## Batch and reuse

- Read the files you need once, in parallel. Do not re-read unchanged files.
- Keep the outputs you already have rather than regenerating them.
- Give a sub-agent the exact files, commands and a prior example, so it does not
  spend its budget rediscovering what you already know.

## Signals of looping

| Signal | Usual meaning |
|---|---|
| Consecutive diffs that change only small numeric literals, often undoing each other | Guessing. Diagnose. |
| The same assertion or error text across runs | Two strikes applies. |
| Tool calls rising while the count of passing checks is flat | No progress. Re-scope. |
| The full suite run per edit, or full logs read each time | The feedback loop is too slow. |
| Test data, fixtures, flags or exemptions growing while product code does not | Probable check-gaming. |
| The same files read again | Lost state. Write it down. |
| Reports repeating "adjusting", "tuning", "almost" | No measurable progress. |

At each report, and roughly every twenty tool calls, count checks newly passing
since the last count. Zero twice in a row is a stop.

## Delegating to a sub-agent

The prompt carries, explicitly:

1. The goal, with done stated as a check that passes.
2. The time box, in wall time or tool calls, and the stop condition.
3. The fastest verification command, and the full-suite command to run once at
   the end.
4. The exact files, a prior example, and known constraints.
5. What it must not do: add check-only data, loosen checks, commit unverified
   work.
6. The reporting format:

```
Now passes:   <check> - <command> -> <result>
Still fails:  <check> - <believed cause> - <evidence>
Attempts on current failure: <n>
Changed files: <paths>
Blocked on / next step: <one line>
```

While it runs:

- Check the diff mid-run rather than waiting for the final report. Look for
  numeric churn and for data that only a check reads. A report is the worker's
  claim; the diff is evidence (`checking-claims`).
- Intervene at the first signal. A correction naming the specific signal
  costs one message. Letting a loop reach its box costs the box.
- If the approach is wrong, stop the worker and re-brief it rather than
  correcting it step by step.

`coordinating-agents` covers dispatch, liveness and corrections.

## Projects provide fast, targeted entry points

An agent can only iterate as fast as the project lets it. Provide:

- a way to run one test, job or file by name in seconds, such as a filter flag,
  documented in `AGENTS.md` beside the full-suite command;
- output that ends with a one-line summary and a nonzero exit on failure, with
  failures easy to filter;
- validators that can run on a single artifact.

The fast entry point must run the same check as the full suite, not a lighter
variant. Watch it fail on a broken input before trusting it: a filter that
matches nothing and exits 0 is a gate that cannot fail.

## Paste into your AGENTS.md

[`assets/AGENTS-snippet.md`](assets/AGENTS-snippet.md) is a short block for a
project's own instructions file. Fill in its two commands; a rule naming a
command that does not exist is decoration.
