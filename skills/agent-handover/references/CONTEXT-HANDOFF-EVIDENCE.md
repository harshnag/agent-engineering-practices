# Does context size determine when to hand off?

**Researched 2026-09-07.** This note tests the inherited instruction to choose a
context threshold in advance, stop there, and report usage after each major
commit or push. It records public primary sources, not private project incidents
or runtime telemetry.

**Finding:** the sources reviewed support context management and recovery from
lost task state. They do not establish a universal coding-session restart count
or percentage. Withdrawing that claim does not establish that arbitrarily long
sessions are reliable.

## What was being claimed here

At repository revision `b613601`, `agent-handover/SKILL.md` required a pre-set
threshold and `project-agent-instructions/assets/AGENTS-template.md` offered
`<N>` for adopters to fill in. Neither instruction defined the counter,
model/tier, or an outcome comparison that would justify a value. A configurable
placeholder is not evidence for the policy it asks a reader to configure.

The associated requirement to report context after pushes also assumed that the
runtime exposed a meaningful current reading. A number labelled "tokens" is not
enough to establish that.

## Public primary sources and their boundaries

### GitHub: occupancy, usage totals and capacity are different

[Managing context in Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management)
documents `/context` as current occupancy against the active model's window,
including instructions, tools, messages and a response/headroom buffer. It
describes background compaction and a later pause if compaction has not finished.
Those scheduling thresholds are not quality-based instructions to replace a
session. Compaction summarizes history and can lose details.

The page supports long-running multi-phase work. Its reasons to start fresh
include unrelated work, important context lost through compaction, and an
approach that needs a clean start. Resuming restores a prior session and its
checkpoints; it is not documented as a fresh-context reset.

The [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
separates `/context` from `/usage`, which reports session metrics including
per-model token totals. It documents `/compact` and a selectable context tier.
The usage description does not supply a complete billing or cache-accounting
schema.

[Supported models: extended capabilities](https://docs.github.com/en/copilot/reference/ai-models/supported-models#models-with-extended-capabilities)
documents an optional larger window for supported configurations, with increased
credit consumption and regular context recommended by default. An advertised
option does not identify the effective configuration of a particular session,
and capacity is not a guarantee of reasoning quality.

The GitHub documentation file revisions checked were:

| Document | Revision |
|---|---|
| Context management | [`630376564b4a3293bae1824c22f204520fdf56e9`](https://github.com/github/docs/blob/630376564b4a3293bae1824c22f204520fdf56e9/content/copilot/concepts/agents/copilot-cli/context-management.md), 2026-07-15 |
| CLI command reference | [`4aa30882aaea7927d8b642db1e2e7a808f183a83`](https://github.com/github/docs/blob/4aa30882aaea7927d8b642db1e2e7a808f183a83/content/copilot/reference/copilot-cli-reference/cli-command-reference.md), 2026-09-07 |
| Supported models | [`be4d995f7eb07f2bbcf1a9f6b664ff91f7f31a11`](https://github.com/github/docs/blob/be4d995f7eb07f2bbcf1a9f6b664ff91f7f31a11/content/copilot/reference/ai-models/supported-models.md), 2026-09-04 |

**Scope:** these are public Copilot CLI contracts, not measurements of a desktop
app, a private runtime, or another agent. No runtime occupancy, effective tier
or compaction behavior was measured here. Check the actual tool's supported
operations before prescribing these commands.

### Vendor guidance: manage context without promising lossless recovery

[Anthropic's context-engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
describes degradation as a gradient rather than a hard cliff, recommends
high-signal context and durable notes, and warns that aggressive compaction can
discard subtle but critical information. This is vendor engineering guidance,
not an experiment identifying an optimal coding-session restart count.

[OpenAI's compaction guide](https://developers.openai.com/api/docs/guides/compaction)
shows a configurable `compact_threshold` of `200000` in an example. It triggers
on rendered token count and continues with compacted state: it is not a
fresh-session recommendation. The standalone compaction input must still fit
within the model's window, and the compacted state is opaque. The page does not
establish that the example is an optimum or that compaction is lossless.

### Original empirical work: degradation is not a universal restart boundary

[Chroma's Context Rot report](https://www.trychroma.com/research/context-rot)
evaluates 18 models using controlled retrieval variants, conversational question
answering and repeated-text reproduction. It reports non-uniform degradation
affected by input length and content. Simple needle retrieval is not sufficient
evidence of general long-context reliability.

This is the authors' original report, not an experiment reproduced here. Its
results concern the tested models and tasks, not every later model or coding
workflow. It does not compare continued versus restarted coding sessions or
their reconstruction costs.

## Keep four quantities separate

| Quantity | What it can establish |
|---|---|
| Current active context, effective model/tier and response reserve | Whether the next request has room; occupancy can shrink after compaction. |
| Cumulative session input/output or billed usage | Activity or spend under the counter's accounting. Repeated history may be counted repeatedly; totals are not current occupancy. |
| Advertised maximum window | Capacity for a supported configuration, not proof that this session selected it or uses it reliably. |
| Document or prompt size estimates, such as characters divided by four | Rough size of a specified corpus or prompt, not actual tokenization or loaded context. |

A per-request input count needs a defined schema, cache treatment and
relationship to the actual prompt before it can stand in for occupancy. A
read-in estimate needs a named prompt boundary; the whole document corpus is
not that boundary.

## Decision and what remains unproved

Replace the unsupported restart threshold and routine reporting mandate with
durable checkpoints and observable recovery triggers. Capacity warnings,
missing constraints, contradictory decisions and repeated re-discovery warrant
checking continuity, not guessing a lifetime token count. Use supported
compaction when appropriate; re-read authoritative state afterwards. Hand off
unfinished work when continuity cannot be restored, and create no successor
for completed work.

Do not substitute another count, percentage, compaction count or elapsed-time
limit, and do not automatically select a larger window. A future quantitative
policy needs a defined counter and runtime/model/tier, comparable tasks, outcome
quality and recovery cost before it earns a number.

**Verification boundary and negative findings:** the public pages above and the
local instructions were read; the GitHub file revisions were checked through
the repository API. No reviewed source established a universal restart boundary
or lossless compaction. No controlled coding-session comparison or runtime
experiment was performed here. The replacement is a conservative policy
decision, not a measured optimum or a claim that context degradation is solved.
