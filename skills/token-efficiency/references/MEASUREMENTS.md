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
share it. **No skill was published in that thread** as of 2026-10-18 02:00 UTC,
read through the HN Algolia API, so there was nothing to install. This skill is
written from the mechanism and from measurement instead.

Other tactics named in the thread, and what became of them here:

| Tactic | Outcome |
|---|---|
| A background task that reports every N minutes, to keep the cache valid | Adopted as the check-in rule, but only for short-lifetime models, after the counterfactual below |
| Stop letting the agent run tests | Not adopted. Tests are the feedback loop; `bounded-iteration` makes them targeted instead |
| A harness that compacts just before the cache expires | Reported for another harness and not verified here |
| Script the deterministic steps; call the model only for judgement | Consistent with "make long waits rare"; not measured |
| A reader's agent found 92% of its cache-write tokens came from rewrites after 5+ minute gaps | Their figure, unverified. Here the comparable share was much smaller; see below |

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

    python scripts/cache_report.py --until 2026-10-18T02:00:00

- Source: `~/.copilot/session-store.db`, table `assistant_usage_events`, opened
  read-only; tool timelines from `~/.copilot/session-state/<session>/events.jsonl`.
- Predicate: every row with non-null `input_tokens` and `duration_ms`, created
  before 2026-10-18 02:00 UTC.
- Result: 39,954 model calls in 167 sessions, 2026-09-07 17:25 to 2026-10-18
  01:59 UTC. Main agents and sub-agents both included.

Three facts about the store were established before anything was counted,
because each one changes every number below:

1. `created_at` marks the end of a call. Of 39,694 consecutive call pairs in the
   same thread, 131 started before the previous call ended if `created_at` is an
   end time, and 13,793 if it is a start time. Start is therefore
   `created_at − duration_ms`.
2. `input_tokens` is uncached input + cache read + cache write. The per-call cost
   lines in `token_details_json` add up to it.
3. A cost line's `costPerBatch` is in billionths of a credit per `batchSize`
   tokens. Summed, the lines give the spend below.

## Results

The report's output for that selection, unedited:

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
   same context / short gap        190,545   15.6% of spend
   same context / long gap         120,390    9.8% of spend
   shrank / long gap                13,648    1.1% of spend
   shrank / short gap               11,316    0.9% of spend

4. Long-gap cold calls with an unchanged context, by what filled the gap
       75,627 credits  n=259  human idle (a user message arrived in the gap)
       17,348 credits  n=96   inside one tool call: powershell  7m initial_wait=400; 6m initial_wait=400; 6m initial_wait=400
       13,265 credits  n=49   inside one tool call: read_powershell  10m delay=600; 7m delay=420; 6m delay=600
       11,793 credits  n=87   agent idle awaiting a notification
        2,356 credits  n=14   inside one tool call: ask_user

5. Expected net saving from checking in during agent-controllable long gaps
   model                 gaps  observed  expected   every 4m  every 10m  every 20m  every 25m   break-even
   claude-opus-5.5        182    33,265    34,466     28,138     -7,465     -2,751     -2,018   24
   gpt-6-astra            148     6,367    21,170     -8,157     -6,023     -1,565       -673   12
   gpt-6.1-sol            149     2,268     3,916     -4,387     -1,281       -228         -6   24
   gpt-5.5                 57       474       786     -3,528       -885       -177        -56   9
   claude-sonnet-5          1        19         0         -8         -2          0          0   12
   gpt-5.4-mini             3        14         1        -25         -8         -3         -2   9
```

The same command with `--intervals 2,3,15,30` gave, for claude-opus-5.5,
21,078 at two minutes and 25,757 at three, and negative values at 15 and 30. For
gpt-6-astra and gpt-6.1-sol, all four intervals were negative.

All 145 cold calls in section 4 that one `powershell` or `read_powershell` call
filled had a wait setting (`initial_wait` or `delay`) of 300 seconds or more.

## Cache lifetime by model

| Model family in Copilot | Observed | Documented by the provider |
|---|---|---|
| Claude (Opus 5.5) | 0 of 90 cold from 3 to 5 minutes; 48% from 5 to 5.5; 97% or more beyond | Five minutes from the start of the previous request |
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

They do not explain short-gap cold calls. Those cost 15.6% of spend, and 75% of
that was on one GPT-6 model. In 165 of the 170 Claude cases, 40,000 to 70,000
tokens were still read from cache (median 52,106) while the rest was rewritten.
That fits the system prompt and tools staying cached while the history changed,
through compaction or the agent runtime rewriting history. It was not confirmed.

The check-in cost is an estimate. The counterfactual charges each check-in a
cached read of the previous prompt, 250 output tokens and 300 appended tokens.
The 250 is the 25th percentile of main-agent output per call, measured at 242 to
245 tokens across the three largest models: the size of a minimal call, not of a
measured check-in.

Expected and observed costs agree for one model and not another. The
counterfactual applies one cold-rate curve per model, pooled across all
contexts. For claude-opus-5.5 the expected and observed costs of the same gaps
agree (34,466 and 33,265). For gpt-6-astra they do not (21,170 and 6,367): the
pooled curve overstates misses for those particular gaps, so checking in on
that model is worse than the table shows.

Nothing here says which model did the work better. The per-call cost of a model
prices a quality decision and cannot make it.

## The report was mutation-tested

Start green: `python scripts/test_cache_report.py` passes eleven tests. Then
each behaviour was broken in a temporary copy, the copy was checked to contain
the change, and the unchanged tests were pointed at it with `CACHE_REPORT`:

| Mutation | Caught by |
|---|---|
| Treat `created_at` as the start | `test_created_at_is_end_so_start_subtracts_duration` |
| Invert the cold threshold | five tests, including `test_warm_call_is_not_cold` |
| Never mark a call as shrank | `test_compaction_is_shrank_not_ttl` |
| Price a zero cache-write rate as free | `test_zero_cache_write_price_means_rebuild_at_input_price` |
| Drop the human-idle check | `test_user_message_in_gap_is_human_idle` |
| Report a missing timeline as agent idle | `test_missing_events_reports_unread_not_a_cause` |
| Pool sub-agent tool spans under the main agent | `test_sub_agent_gap_uses_its_own_tool_spans` |
| Let the cold curve decrease | `test_cold_curve_is_non_decreasing_and_sparse_buckets_inherit` |
| Measure the gap from the previous call's end | `test_long_gap_miss_is_cold_same_context_with_excess`, `test_warm_call_is_not_cold` |

Two defects were found while building the report, before the tests existed,
and each now has a test. A zero cache-write price had been read as free, which
made misses on models without a write charge look like savings. And the first
counterfactual credited check-ins with preventing misses at any interval, which
claimed a 25-minute check-in saved as much on a five-minute cache as a
four-minute one.
