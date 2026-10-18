---
name: token-efficiency
description: How an agent gets the same work done for fewer tokens by measuring where spend goes, keeping a prompt cache warm across long waits only when the arithmetic says so, keeping context lean, and treating model choice as the largest cost decision. Use when about to wait on a test suite, build, sub-agent, session or command that may run for minutes; choosing a wait, poll, delay or timeout; deciding whether to delegate to a sub-agent; resuming a session after a break; choosing a model or reasoning effort; or when asked about token burn, credits, cache hits, cache TTL, or cost.
license: MIT
compatibility: The report script needs Python 3 and no third-party packages. It reads the GitHub Copilot CLI local session store; the rules apply to any agent tool.
metadata:
  provenance: Derived from public provider documentation and one operator's measured agent sessions, 2026
  author: harshnag
  version: "1.0"
---

# Token efficiency

Every model call sends the whole context again. The provider bills the part it
still holds in its prompt cache at a fraction of the input price, and the part
it has to rebuild at a premium. So the price of a call is roughly:

> **context size × price per token, where the price depends on whether the
> cache is still warm.** Model rate, context size, number of calls, and cache
> state are the levers. They are not the same size, and the one people talk
> about is rarely the largest.

Current rates make the gap large. Reading a cached prefix costs 0.025 to 0.1 of
the input price, depending on the model; rebuilding it costs 1.25 times the
input price where the provider charges for cache writes. The same prompt costs
12 to 50 times more when the cache has gone cold.

The cache lives for a fixed time after the last call that used it. Anthropic
documents five minutes, **measured from the start of the request**, so time
spent generating counts against it. OpenAI documents at least thirty minutes
for GPT-5.6 and later. Nothing that happens between calls refreshes it: a test
run, a build, a sub-agent working, a human reading. Only the next call does.

## Measure before optimising

The claim that motivates most advice here, that a test suite running longer than
five minutes burns tokens, is true for some models and false for others reached
through the same tool. Run the report on your own sessions before changing
anything:

    python scripts/cache_report.py [--since 2026-10-01] [--session <id>]

It opens the local session store read-only and prints its selection and
definitions first, then:

1. spend by token type and by model, with median and p90 prompt size;
2. the cold-call rate by gap, per model. The column where the rate steps from
   near 0% to near 100% is that model's cache lifetime as you run it;
3. cold-call cost split into compaction, short gaps, and long gaps;
4. what filled each long gap: a human, one tool call (with its wait setting), or
   the agent idling on a notification;
5. the expected net saving from checking in at several intervals, using each
   model's measured cold-rate curve.

`scripts/test_cache_report.py` covers it against a synthetic store with known
answers. Nine deliberate mutations were each caught; see
[the measurements](references/MEASUREMENTS.md#the-report-was-mutation-tested).

In the one data set measured so far (40,000 calls over six weeks), the levers
ranked like this:

| Lever | Measured size |
|---|---|
| Model rate | one model took 76% of spend at five to six times the per-call cost of the next two, at the same median prompt size |
| Context size | cache reads were 55% of spend; the median prompt was about 220K tokens |
| Cold cache with unchanged context, short gap | 15.6% of spend; provider or agent-runtime behaviour an agent mostly cannot change |
| Cold cache after a human break | 6.4% |
| Cold cache during a wait the agent chose | 3.5% |

So the five-minute rule is real, and in that data the avoidable part of it was
under 4% of spend. Fix it, because the fix is nearly free. Do not mistake it
for the main lever.

## Know the cache lifetime of the model you are on

The lifetime is set by the provider and the tool that calls it, not by you, and
**models reached through the same tool differ by a factor of six**. Read it from
section 2 of the report or from a published measurement, and record the date.
The values observed in GitHub Copilot CLI in October 2026 are in
[the measurements](references/MEASUREMENTS.md#cache-lifetime-by-model): about
five minutes for Claude models, about thirty minutes for the GPT-6 family.

## A wait longer than the lifetime: check in, or accept one rebuild

A check-in is one cheap call before the cache expires. It costs one cached read
of the context plus a little output. One avoided rebuild pays for

    break-even = (rebuild price − read price) / read price

check-ins. That is 24 for a model whose cached reads cost 0.05 of input, and
about 12 at 0.1. With a five-minute lifetime and a check-in every four minutes,
checking in pays for waits up to roughly 90 or 45 minutes respectively. Past
that, one rebuild is cheaper; stop checking in and wait.

When the lifetime is long and misses inside it are probabilistic, check-ins
rarely pay. On the measured thirty-minute models, every interval tested from 2
to 30 minutes cost more than it saved, while four-minute check-ins on the
five-minute models saved about 28,000 credits net.

On a model with a short lifetime:

- Never block in one wait longer than about four minutes. The lifetime runs
  from the start of the previous call, so that call's own duration counts too.
  In the measured data, waits written as `initial_wait=400` or `delay=600`
  caused 145 rebuilds.
- A check-in reads a status line or the tail of the output. It does not re-read
  the log, re-plan, or re-open files. Its output tokens are billed at the output
  rate, and a check-in that reasons for 2,000 tokens can cost as much as the
  cached read it was protecting.
- Prefer a bounded wait to ending the turn. An agent that stops to await a
  notification sends nothing, so the cache expires whatever the wait.

In GitHub Copilot CLI that means `initial_wait` and `read_powershell` `delay`
at 240 seconds or less, and `read_agent` with its default timeout, which is
already under the limit.

If the tool's own instructions or the user say not to poll, that instruction
wins. The measured
saving was about 2% of spend: worth taking, never worth a conflict.

## Make long waits rare

Cheaper than keeping a cache warm through a wait is not waiting.

- Iterate on the narrowest check and run the full suite once, as
  `bounded-iteration` sets out. A suite longer than the lifetime, run after
  every edit, pays one full rebuild per run.
- Start long work in the background and do independent work meanwhile. Each
  useful call refreshes the cache for nothing.
- When waits are long by nature, hours rather than minutes, one rebuild per wait
  is the correct price. Do not check in for hours.

## Context is paid for on every call

A token in the context is billed again on every later call. At a 220K-token
prompt and a cached read price of USD 0.20 per million tokens, re-reading the
context costs 4.4 credits per call before the model does anything.

- Filter command output to the failing assertion and the summary line. Do not
  page whole logs into the conversation.
- View line ranges of large files, and do not re-read files that have not
  changed.
- Delegate verbose exploration to a sub-agent that returns a summary, when the
  parent still has many calls to make. A sub-agent starts cold: its first call
  wrote a median 24,000 tokens in the measured data. Delegation pays when
  tokens kept out of the parent × the parent's remaining calls × the read price
  exceeds that.
- Start a fresh session for unrelated work rather than resuming a large one.
  The first call after a break longer than the lifetime rebuilds the whole
  context, which for new work is paying to reload history it does not need.

## Model rate is the largest lever, and it is a quality decision

At the same prompt size, per-call cost differed five- to sixfold between models.
Spend on a model is a choice about output quality that the token numbers only
price; they cannot make it for you. What they can show is where an expensive
model is doing work a cheaper one does as well: searching, running and
summarising tests, reading logs, mechanical edits. Make that a decision per task
or per sub-agent rather than a session default. Reasoning effort is the same
decision at a smaller scale, because reasoning tokens bill as output.

## What not to chase

- Cold calls after short gaps with an unchanged context. They come from
  compaction, from the agent runtime rewriting history, from tool lists changing, or
  from the provider not reusing a prefix. Report them; do not invent rituals to
  prevent them.
- Spending to use up an allowance, or checking in past break-even "to be safe".
  Both are spending presented as saving.
- A check-in loop that exists so a dashboard shows a high cache-hit rate. The
  target is credits per unit of verified work, not the hit rate.

## Signals

| Signal | Usual meaning |
|---|---|
| A single wait of five minutes or more on a short-lifetime model | The next call rebuilds the whole context |
| `delay`, `timeout` or `initial_wait` of 300 seconds or more | The same, chosen in advance |
| Each check-in reads a full log | Context growing for nothing; read the tail |
| Prompt above 200K and rising during mechanical work | Delegate it, or start fresh for the next task |
| Many cold calls with unchanged context and short gaps | Runtime or provider; record it, do not fix it |
| One model dominating spend at several times the per-call cost | Decide per task whether it is earning that |

## The numbers here are one operator's

Every figure in this file comes from one person's six weeks with one agent
tool, at October 2026 prices, measured as described in
[the measurements](references/MEASUREMENTS.md). Cache lifetimes, prices and
runtime behaviour change without notice. Run the report, and replace these
numbers with yours before arguing from them.
