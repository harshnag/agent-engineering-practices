# Measurements behind token-efficiency

Dated evidence, not rules. Everything here was observed between 2026-09-07 and
2026-10-18 by one operator on GitHub Copilot CLI and the GitHub Copilot app, at
the prices GitHub published in October 2026. The rules in `SKILL.md` are meant
to survive these numbers changing; the numbers are not.

## Where the question came from

A Hacker News thread on 2026-10-17 (comment 50129838 and its replies, under
story 50129045) claimed that agent workflows running tests for more than five
minutes let the prompt cache expire, so the next call reprocessed everything as
uncached input. The commenter said they had written a skill "to better manage
agents, including a way to keep the caches valid". Another reader asked them to
share it. **That skill was not published in the thread**: read twice through
the HN Algolia API, last at 02:42 UTC on 2026-10-18, there was no reply from the
author and no link.

Other tactics named in the thread, and what became of them here:

| Tactic | Outcome |
|---|---|
| A background task that reports every N minutes, to keep the cache valid | Adopted as the check-in rule, but only for short-lifetime models, after the counterfactual below |
| Stop letting the agent run tests | Not adopted. Tests are the feedback loop; `bounded-iteration` makes them targeted instead |
| A harness that compacts just before the cache expires | Reported for another harness and not verified here |
| Script the deterministic steps; call the model only for judgement | Consistent with "make long waits rare"; not measured |
| A reader's agent found 92% of its cache-write tokens came from rewrites after 5+ minute gaps | Their figure, unverified, and a different quantity from any reported here |

## Public keep-alive skills, evaluated

Three public skills address the same problem. None is the one the thread
mentioned, and none fits GitHub Copilot as published. Read on 2026-10-18.

| Skill | What it does | Fit for Copilot |
|---|---|---|
| [ARahim3/cachebeat](https://github.com/ARahim3/cachebeat) | A Claude Code `Stop` hook (`asyncRewake`) that sends a tiny heartbeat after N idle minutes, default 50, for Claude Code's one-hour cache | Depends on Claude Code's hook and plugin variables. Its own text says that with the five-minute lifetime "no practical heartbeat helps", which is the lifetime Copilot gives Claude models |
| [santiquiroz/claude-prompt-cache-keepalive](https://github.com/santiquiroz/claude-prompt-cache-keepalive) | A ladder of background timer jobs whose completion wakes an idle Claude Code session, for its sixty-minute cache | Its hooks are Claude Code's. Its stated limit, "beyond ~20 ticks it is cheaper to let it expire", is the break-even arithmetic in `SKILL.md` |
| [OnlyTerp/prompt-cache-skills](https://github.com/OnlyTerp/prompt-cache-skills) | Patches to the caching code of open-source harnesses such as Cline, Roo Code, Continue and Aider | Copilot is not one of the harnesses it patches |

The timer idea raises a question these numbers can answer: would a heartbeat
while the human is away recover part of the 5.8% lost to breaks? For the 67
human-idle long gaps on claude-opus-5.5, using the curve and check-in cost of
section 5 below, a four-minute heartbeat would have saved 1,536 credits net if
it stopped after 6 ticks, 759 after 12 and 127 after 24, and lost 10,711 if it
never stopped. The best case is about 0.1% of spend, on a wake mechanism nobody
has tested in Copilot, so `SKILL.md` does not recommend one.

## Primary sources

- Anthropic, [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).
  Default lifetime five minutes, "refreshed for no additional cost each time the
  cached content is used", and "measured from the start of the request that
  writes or reads the cache entry, not from the end of its response". A one-hour
  lifetime exists at twice the input price per written token. Cache writes 1.25×
  input; reads 0.1× input, except 0.05× for Claude Opus 5.5 and Sonnet 5.5 and
  0.025× for Claude Fable 5.1 and Mythos 5.1.
- OpenAI, [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).
  GPT-5.6 and later: lifetime "at least 30 minutes after the latest write or
  reuse", cache writes 1.25× input, reads 0.1× (0.05× for GPT-6.1 Sol). GPT-5.5:
  typically around 30 minutes, up to 24 hours, no write charge. Earlier models
  with in-memory retention: typically 5 to 10 minutes of inactivity.
- GitHub, [Models and pricing for GitHub Copilot](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)
  and [the usage-based billing announcement](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/).
  Since 2026-06-01 Copilot bills input, output, cached and cache-write tokens at
  per-model rates, converted to AI credits at USD 0.01 per credit. So in
  Copilot a cache miss is the user's cost, not only the provider's.
- GitHub, [Managing context in GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management).
  Tool output over 20 KiB is saved to a file with a preview kept in context;
  compaction starts near 80% of the context window.
- [trsdn/copilot-cache-ttl](https://github.com/trsdn/copilot-cache-ttl), an
  independent harness that seeds a cache through Copilot CLI and probes it after
  controlled delays. It reports 4.0 to 4.8 minutes for the Claude 4.x models it
  tested, 15.5 minutes for gpt-5.4-mini, 17.3 for gpt-5.5, and 30 or more for
  gpt-5-mini and gpt-5.3-codex. Different models from most of those measured
  below, so it corroborates the method and the Claude figure rather than the
  GPT-6 one.

## Selection

From the repository root:

    python skills/token-efficiency/scripts/cache_report.py --until 2026-10-18T02:00:00

- Source: `~/.copilot/session-store.db`, table `assistant_usage_events`, opened
  read-only; tool timelines from `~/.copilot/session-state/<session>/events.jsonl`.
- Predicate: every row with non-null `input_tokens` and `duration_ms`, created
  before 2026-10-18 02:00 UTC.
- Result: 39,954 model calls and 39,533 same-thread pairs in 167 sessions,
  2026-09-07 17:25 to 2026-10-18 01:59 UTC. Main agents and sub-agents both
  included. A thread is one session, agent and model.

Three facts about the store were established before anything was counted,
because each one changes every number below:

1. `created_at` marks the end of a call. The report's second line counts the
   pairs that contradict each reading, with a 50 ms tolerance: read as an end
   time, 151 of the 39,533 pairs would overlap the call before them; read as a
   start time, 13,752 would start while the previous call was still running.
   With no tolerance the counts are 154 and 13,889. Start is therefore
   `created_at − duration_ms`.
2. `input_tokens` is uncached input + cache read + cache write. The per-call cost
   lines in `token_details_json` add up to it.
3. A cost line's `costPerBatch` is in billionths of a credit per `batchSize`
   tokens. Summed, the lines give the spend below.

Main-agent calls on claude-opus-5.5 took a median 7 seconds (p90 20, p99 75).
Of 8,161, 421 took more than 30 seconds, 134 a minute or more, and 2 four minutes
or more. The lifetime is counted from the start of a call, so `SKILL.md` budgets
a wait as 270 seconds minus the previous call's duration: 240 seconds after the
roughly 95% of calls that take under 30 seconds, and 180 when the duration is
unknown.

## Results

The report's output for that selection, unedited except for the explanatory
lines under each heading:

```text
1. Spend by token type (AI credits; 1 credit = USD 0.01)
   total 1,225,294
   cache_read        677,974   55.3%
   cache_write       415,588   33.9%
   output            115,981    9.5%
   input              15,750    1.3%

   model                calls    credits  per call  median prompt  p90 prompt
   gpt-6-astra          12814    928,469      72.5        217,115     572,123
   claude-opus-5.5      10103    143,343      14.2        218,529     513,343
   gpt-6.1-sol           8861    102,048      11.5        225,719     512,273
   gpt-5.5               6400     45,565       7.1         89,040     172,267
   grok-4.7               113      1,816      16.1        174,972     263,701
   gemini-3.8-flash       874      1,611       1.8        148,359     290,943
   claude-sonnet-5        276      1,448       5.2        111,555     225,885
   gpt-5.4-mini           468        830       1.8        106,282     185,178
   gpt-5.6-sol             25        157       6.3         97,511     110,986
   mai-code-1.1-flash      20          5       0.2         33,628      38,774

2. Cold calls by gap since the previous call started (models with >= 50 pairs)
   model                      0+       1+       3+       4+       5+     5.5+       7+      10+      20+      30+      45+      60+   (cold% / pairs)
   gpt-6-astra           2%/9865  3%/2104   7%/242   7%/106   18%/39   15%/85   23%/64   27%/78   35%/23  100%/18   92%/12  100%/41
   claude-opus-5.5       2%/9174   2%/502    0%/52    0%/38   48%/21   97%/31   99%/73  100%/93  100%/12   100%/6    86%/7   97%/34
   gpt-6.1-sol           1%/6714  5%/1382   6%/198   13%/86    3%/32   11%/70   19%/73  23%/104   23%/31  100%/10   93%/15   98%/40
   gpt-5.5               1%/6101   1%/129    0%/20    8%/12    4%/28     0%/2    0%/12    0%/10        -        -        -   100%/5
   gemini-3.8-flash       2%/845   11%/18        -        -        -        -        -   100%/2   100%/1        -        -   100%/2
   gpt-5.4-mini           3%/433    0%/19     0%/2        -        -        -     0%/1        -        -   100%/2        -        -
   claude-sonnet-5        0%/249    0%/10        -     0%/1        -        -        -   100%/1        -        -        -        -
   grok-4.7               5%/106     0%/4        -        -        -        -     0%/1        -        -        -        -        -

3. Excess credits from cold calls, by cause (long gap = 5+ minutes)
   same context / short gap        188,280   15.4% of spend
   same context / long gap         119,211    9.7% of spend
   shrank / long gap                 5,690    0.5% of spend
   shrank / short gap                3,644    0.3% of spend

4. Long-gap cold calls with an unchanged context, by what filled the gap
       67,041 credits  n=222  human idle (a user message arrived in the gap)
       21,179 credits  n=108  inside one tool call: powershell  7m initial_wait=400; 6m initial_wait=400; 6m initial_wait=400
       13,492 credits  n=50   inside one tool call: read_powershell  10m delay=600; 7m delay=420; 6m delay=600
       11,741 credits  n=87   unattributed agent idle (no tool call covered the gap)
        4,073 credits  n=22   inside one tool call: ask_user
        1,686 credits  n=16   inside one tool call: task

5. Expected net saving from checking in during long gaps that one tool call filled
   model                 gaps  observed  expected   every 4m  every 10m  every 20m  every 25m   break-even
   claude-opus-5.5        168    30,978    30,564     26,144     -4,178     -1,452       -967   24
   gpt-6-astra             84     4,494     8,222     -3,406       -968        -24         20   12
   gpt-6.1-sol            112     1,246     3,058     -2,348       -241          0          0   24
   gpt-5.5                 52        87         ?          ?       -104          0          0   9
```

The same command with `--intervals 2,3,15,30` gave, for claude-opus-5.5,
20,819 at two minutes, 24,322 at three, −1,762 at fifteen and −502 at thirty.
For gpt-6-astra it gave −12,271, −7,734, −94 and −114; for gpt-6.1-sol −3,394,
−1,220, 0 and 0. A zero means no gap of that model was long enough for a
check-in at that interval to happen.

Derived from the same selection:

- Human breaks: 67,041 + 4,073 for `ask_user` = 71,114 credits, 5.8% of spend.
- Waits the agent chose, where one tool call filled the gap: `powershell`,
  `read_powershell` and `task` together = 36,357 credits, 3.0% of spend.
- Unattributed idle: 11,741 credits, 1.0%. No tool call covered those gaps and
  no message arrived, so nothing shows who chose them. They are excluded from
  section 5.
- All 158 cold calls in section 4 that one `powershell` or `read_powershell`
  call filled had a wait setting (`initial_wait` or `delay`) of 300 seconds or
  more.

## Cache lifetime by model

| Model family in Copilot | Observed | Documented by the provider |
|---|---|---|
| Claude (Opus 5.5) | 0 of 90 cold from 3 to 5 minutes; 48% from 5 to 5.5; 97 to 100% in every later bucket except 45 to 60 minutes, 6 of 7 | Five minutes from the start of the previous request |
| GPT-6 (Astra, 6.1 Sol) | 3 to 35% cold from 3 to 30 minutes, broadly rising with the gap; 92% or more beyond 30 | At least 30 minutes after the latest write or reuse |
| GPT-5.5 | At most 8% cold below 20 minutes; 5 cold of 5 beyond 60; nothing between | Typically around 30 minutes |

The GPT-6 rows disagree with the documented minimum: up to a third of calls
were cold well inside thirty minutes, with an unchanged context. Why was not
established. Copilot's deployment, routing between cache hosts, and a prefix
change the cold test cannot see are all consistent with it, and none was tested.

## What these numbers do not show

They do not generalise on their own. This is one operator, one agent tool and
six weeks, a mix of interactive and unattended sessions, and models with few
pairs have no usable curve.

They do not explain short-gap cold calls. Those cost 15.4% of spend, and 75% of
that was on one GPT-6 model. In 165 of the 170 Claude cases, 40,000 to 70,000
tokens were still read from cache (median 52,106) while the rest was rewritten.
That fits the system prompt and tools staying cached while the history changed,
through compaction or the agent runtime rewriting history. It was not confirmed.

The shrank rows of section 3 are upper bounds. A compacted prompt shares an
unknown prefix with the one before it, so the rebuild is capped at the new
prompt's size rather than measured.

The check-in cost is an estimate. The counterfactual charges each check-in a
cached read of the previous prompt, 250 output tokens and 300 appended tokens.
The 250 is the 25th percentile of main-agent output per call, measured at 242 to
245 tokens across the three largest models: the size of a minimal call, not of a
measured check-in. It also treats intervals as start-to-start and charges the
same curve at every check-in.

Expected and observed costs agree for one model and not another. Section 5 uses
one curve per model of the expected fraction of the prompt rebuilt at each gap,
pooled across all contexts. For claude-opus-5.5 the expected and observed costs
of the same gaps agree (30,564 and 30,978). For gpt-6-astra they do not (8,222
and 4,494): the pooled curve overstates rebuilds for those particular gaps, so
checking in on that model is worse than the table shows.

Nothing here says which model did the work better. The per-call cost of a model
prices a quality decision and cannot make it.

## How the report was checked

A reviewer in a separate context read the first version and found seven defects
the author had not: the documented command path did not say which directory it
ran from; the counterfactual charged every cold call as a full rebuild, so a
call that reused 49% of its prompt cost the same as one that reused none;
sparse buckets became measured zeroes; the four-minute rule ignored the
previous call's own duration; compaction was charged for tokens the new prompt
no longer contained; a user message outranked the tool call that had actually
filled a gap; and the commit message claimed a counterfactual test that did not
exist. Three figures in this file were also wrong. Each defect now has a test,
and every figure above comes from the corrected script.

The same reviewer then read the fixes and found five more. Four were accepted.
Gaps no tool call explained had still been counted as waits the agent chose;
they are now reported separately and left out of section 5. A flat 240-second
wait exceeded the stated budget after the 5% of calls that take over 30
seconds; the rule is now 270 seconds minus the previous call's duration, with
180 as the fallback. An interval at which no check-in happens had been reported
as unknown when its net is exactly zero. And the timestamp counts did not
reproduce, because they used an unstated 50 ms tolerance; the report now
computes and labels them. The fifth, that `task` has no background mode, was
rejected: the main agent's `task` tool takes `mode: background`, and 169 of the
254 `task` calls in these sessions' timelines, across 46 sessions, used it. The
reviewer's own tool set evidently lacks that parameter.

Two earlier defects were found by the author while building the report: a zero
cache-write price had been read as free, and the first counterfactual credited
check-ins at any interval with preventing misses, which claimed a 25-minute
check-in saved as much on a five-minute cache as a four-minute one.

## The report was mutation-tested

Start green: `python skills/token-efficiency/scripts/test_cache_report.py`
passes twenty-three tests. Then each behaviour was broken in a temporary copy, the
copy was checked to differ from the original, and the unchanged tests were
pointed at it with `CACHE_REPORT`:

| Mutation | Caught by |
|---|---|
| Treat `created_at` as the start | `test_created_at_is_end_so_start_subtracts_duration` |
| Invert the cold threshold | five tests, including `test_warm_call_is_not_cold` |
| Never mark a call as shrank | `test_compaction_is_shrank_and_rebuild_is_capped_at_the_current_prompt` |
| Price a zero cache-write rate as free | `test_zero_cache_write_price_means_rebuild_at_input_price` |
| Let a user message outrank a covering tool call | `test_tool_call_outranks_a_message_that_arrived_while_it_ran` |
| Drop the human-idle check | `test_user_message_in_an_uncovered_gap_is_human_idle` |
| Report a missing timeline as agent idle | `test_missing_events_reports_unread_not_a_cause` |
| Pool sub-agent tool spans under the main agent | `test_sub_agent_gap_uses_its_own_tool_spans` |
| Measure the gap from the previous call's end | `test_long_gap_miss_is_cold_same_context_with_excess`, `test_warm_call_is_not_cold` |
| Charge compaction for the whole previous prompt | `test_compaction_is_shrank_and_rebuild_is_capped_at_the_current_prompt` |
| Count any cold call as a full rebuild in the curve | `test_partial_loss_counts_by_its_fraction_not_as_a_full_miss`, `test_curve_is_non_decreasing_across_sampled_buckets` |
| Let the curve decrease | `test_curve_is_non_decreasing_across_sampled_buckets` |
| Fill a sparse bucket with the value before it | `test_unsampled_bucket_is_unknown_not_zero` |
| Let compacted pairs shape the curve | `test_compacted_pairs_do_not_shape_the_curve` |
| Assume a check-in never misses | `test_checking_in_under_the_lifetime_pays_and_over_it_does_not`, `test_exact_multiple_leaves_a_full_final_interval` |
| Charge the final stretch at the whole gap | the same two |
| Count unattributed idle as a wait the agent chose | `test_uncovered_gap_without_a_message_is_unattributed_and_not_counted_as_chosen` |
| Count `ask_user` as a wait the agent chose | `test_ask_user_is_a_human_wait_not_an_agent_choice` |
| Consult the curve when no check-in happens | `test_no_check_in_is_exactly_zero_even_when_the_curve_is_unknown` |
| Swap the two timestamp readings | `test_timestamp_check_counts_contradictions_of_each_reading` |
| Compare against the previous call's start, not its end | the same |
