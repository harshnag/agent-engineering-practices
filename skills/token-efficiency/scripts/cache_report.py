#!/usr/bin/env python3
"""Where did agent token spend go, and which prompt-cache misses were avoidable?

Reads the GitHub Copilot CLI local session store read-only:
  ~/.copilot/session-store.db          per-call token usage (assistant_usage_events)
  ~/.copilot/session-state/*/events.jsonl   tool and message timeline, for attribution

Standard library only. Nothing is written anywhere.

Definitions used throughout (printed again in the report):
  thread   consecutive model calls with the same session, agent and model
  gap      start of a call minus start of the previous call in its thread
           (the provider cache lifetime is measured from request start)
  hit      cache-read tokens of a call / prompt tokens of the previous call, capped at 1
  cold     hit < 0.5: most of the prefix the previous call established was not reused
  shrank   prompt fell below 0.8 x the previous prompt (compaction or a new context)
  lost     tokens of the previous prompt that this call rebuilt instead of reading,
           capped at this call's own prompt: min(previous, current) - cache read
  excess   lost x (cache-write or input price - cache-read price)
"""
import argparse
import collections
import datetime as dt
import json
import math
import os
import sqlite3
import sys

COLD = 0.5
SHRANK = 0.8
MIN_BUCKET = 5
BUCKETS = [0, 1, 3, 4, 5, 5.5, 7, 10, 20, 30, 45, 60, math.inf]
CHECKIN_OUTPUT_TOKENS = 250
CHECKIN_APPENDED_TOKENS = 300
HUMAN = "human idle (a user message arrived in the gap)"
UNREAD = "unread (no events.jsonl for this session)"
IDLE = "unattributed agent idle (no tool call covered the gap)"


def ms(stamp):
    return dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp() * 1000


def load_calls(db, since=None, until=None, session=None):
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    where = ["input_tokens is not null", "duration_ms is not null"]
    args = []
    if since:
        where.append("created_at >= ?")
        args.append(since)
    if until:
        where.append("created_at < ?")
        args.append(until)
    if session:
        where.append("session_id = ?")
        args.append(session)
    q = f"""select session_id, coalesce(agent_id, ''), model, input_tokens,
                   coalesce(cache_read_tokens, 0), coalesce(cache_write_tokens, 0),
                   coalesce(output_tokens, 0), duration_ms, created_at, token_details_json
            from assistant_usage_events where {' and '.join(where)}"""
    calls = []
    for s, a, m, inp, cr, cw, out, du, ca, tj in con.execute(q, args):
        end = ms(ca)
        details = json.loads(tj) if tj else []
        price = {d["tokenType"]: d["costPerBatch"] / d["batchSize"] / 1e9 for d in details}
        calls.append(dict(session=s, agent=a, model=m, inp=inp, read=cr, write=cw, out=out,
                          start=end - du, end=end, details=details, price=price))
    con.close()
    calls.sort(key=lambda c: (c["session"], c["agent"], c["model"], c["start"]))
    return calls


def rates(calls):
    """Fallback price per token in AI credits by (model, token type), for calls whose own
    cost lines omit a token type. A call's own lines win, because price tiers vary by prompt size."""
    r = {}
    for c in calls:
        for k, v in c["price"].items():
            r[(c["model"], k)] = v
    return r


def price(c, r, kind):
    v = c["price"].get(kind)
    return v if v is not None else r.get((c["model"], kind))


def miss_rate(c, r):
    """Extra cost per token of rebuilding a prefix instead of reading it. A zero cache-write
    price means "not applicable" (rebuilt tokens bill as plain input), not "free"."""
    full = price(c, r, "cache_write") or price(c, r, "input")
    read = price(c, r, "cache_read")
    if not full or read is None:
        return None
    return full - read


def checkin_cost(prev, r):
    """One minimal call: a cached read of the prompt, a little output, a little appended."""
    return (prev["inp"] * (price(prev, r, "cache_read") or 0)
            + CHECKIN_OUTPUT_TOKENS * (price(prev, r, "output") or 0)
            + CHECKIN_APPENDED_TOKENS * (price(prev, r, "cache_write") or price(prev, r, "input") or 0))


def pairs(calls, r):
    prev = None
    for c in calls:
        key = (c["session"], c["agent"], c["model"])
        if prev and prev[0] == key and prev[1]["inp"]:
            p = prev[1]
            gap = (c["start"] - p["start"]) / 60000
            hit = min(1.0, c["read"] / p["inp"])
            lost = max(0, min(p["inp"], c["inp"]) - c["read"])
            mr = miss_rate(c, r)
            cost = lost * mr if mr is not None else 0.0
            cold = hit < COLD
            yield dict(prev=p, cur=c, gap=gap, hit=hit, cold=cold,
                       shrank=c["inp"] < SHRANK * p["inp"],
                       lost_frac=lost / p["inp"], lost_cost=cost,
                       excess=cost if cold else 0.0)
        prev = (key, c)


def bucket(g):
    for lo, hi in zip(BUCKETS, BUCKETS[1:]):
        if lo <= g < hi:
            return lo
    return BUCKETS[-2]


def loss_curve(ps, model):
    """Expected fraction of the previous prompt rebuilt, by gap bucket, from same-context pairs.
    Forced non-decreasing across sampled buckets, since an expired entry stays expired.
    A bucket with fewer than MIN_BUCKET pairs is None: unknown, never a measured zero."""
    acc = collections.defaultdict(list)
    for p in ps:
        if p["cur"]["model"] == model and not p["shrank"]:
            acc[bucket(p["gap"])].append(p["lost_frac"])
    curve, run = [], 0.0
    for lo in BUCKETS[:-1]:
        xs = acc.get(lo, [])
        if len(xs) >= MIN_BUCKET:
            run = max(run, sum(xs) / len(xs))
            curve.append(run)
        else:
            curve.append(None)
    return curve


def at(curve, g):
    return curve[BUCKETS.index(bucket(g))]


def checkin_net(gaps, curve, intervals, r):
    """Expected credits saved by checking in every i minutes during each gap, against not checking in.
    Intervals are start-to-start: a wait of w seconds after a call lasting d gives w + d.
    Returns (expected cost without check-ins, [net saving per interval]); None where any gap needs
    an unsampled bucket."""
    def f(g):
        return at(curve, g)
    base, nets = 0.0, [0.0] * len(intervals)
    for p in gaps:
        prev, mr = p["prev"], miss_rate(p["cur"], r) or 0
        miss, k, fw = prev["inp"] * mr, checkin_cost(prev, r), f(p["gap"])
        if fw is None or base is None:
            base = None
        else:
            base += fw * miss
        for j, i in enumerate(intervals):
            if nets[j] is None:
                continue
            n = max(0, math.ceil(p["gap"] / i) - 1)
            fi, fres = f(i), f(p["gap"] - n * i)
            if fw is None or fres is None or (n and fi is None):
                nets[j] = None
                continue
            nets[j] += fw * miss - (n * k + n * (fi or 0) * miss + fres * miss)
    return base, nets


def load_events(state_dir, session, cache):
    if session in cache:
        return cache[session]
    path = os.path.join(state_dir, session, "events.jsonl")
    if not os.path.exists(path):
        cache[session] = None
        return None
    starts, spans, users = {}, collections.defaultdict(list), []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"tool.execution_' not in line and '"user.message"' not in line:
                continue
            try:
                e = json.loads(line)
            except ValueError:
                continue
            t, d = ms(e["timestamp"]), e.get("data") or {}
            agent = e.get("agentId") or ""
            if e["type"] == "user.message":
                users.append(t)
            elif e["type"] == "tool.execution_start":
                args = d.get("arguments") if isinstance(d.get("arguments"), dict) else {}
                knobs = " ".join(f"{k}={args[k]}" for k in ("initial_wait", "delay", "timeout", "mode")
                                 if k in args)
                starts[d.get("toolCallId")] = (t, d.get("toolName") or "?", knobs, agent)
            elif e["type"] == "tool.execution_complete":
                s = starts.pop(d.get("toolCallId"), None)
                if s:
                    spans[s[3]].append((s[0], t, s[1], s[2]))
    cache[session] = (spans, users)
    return cache[session]


def attribute(pair, events):
    """Name what occupied a gap: one tool call covering most of it, else a human message, else
    unattributed idle. A tool call is checked first: a message can arrive while a tool runs."""
    if events is None:
        return UNREAD, ""
    spans, users = events
    lo, hi = pair["prev"]["end"], pair["cur"]["start"]
    best, cover = None, 0.0
    for s in spans.get(pair["cur"]["agent"], []):
        if s[0] < hi and s[1] > lo:
            ov = (min(s[1], hi) - max(s[0], lo)) / max(1.0, hi - lo)
            if ov > cover:
                best, cover = s, ov
    if best and cover >= 0.5:
        return f"inside one tool call: {best[2]}", best[3]
    if pair["cur"]["agent"] == "" and any(lo <= u <= hi for u in users):
        return HUMAN, ""
    return IDLE, ""


def controllable(label):
    return label not in (HUMAN, UNREAD) and "ask_user" not in label


def report(calls, state_dir, long_gap, intervals, min_pairs, out=sys.stdout):
    w = lambda s="": print(s, file=out)
    if not calls:
        w("No calls matched the selection.")
        return
    r = rates(calls)
    sessions = {c["session"] for c in calls}
    first = min(c["start"] for c in calls)
    last = max(c["end"] for c in calls)
    fmt = lambda t: dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    ps = list(pairs(calls, r))
    w(f"Selection: {len(calls)} model calls, {len(ps)} same-thread pairs, {len(sessions)} sessions, "
      f"{fmt(first)} to {fmt(last)} UTC")
    w(__doc__.split("Definitions used throughout (printed again in the report):")[1].strip("\n"))

    w("\n1. Spend by token type (AI credits; 1 credit = USD 0.01)")
    by_type, by_model, n_model, ctx = collections.Counter(), {}, collections.Counter(), collections.defaultdict(list)
    for c in calls:
        n_model[c["model"]] += 1
        ctx[c["model"]].append(c["inp"])
        for d in c["details"]:
            v = d["tokenCount"] * d["costPerBatch"] / d["batchSize"] / 1e9
            by_type[d["tokenType"]] += v
            by_model.setdefault(c["model"], collections.Counter())[d["tokenType"]] += v
    total = sum(by_type.values())
    w(f"   total {total:,.0f}")
    for k, v in by_type.most_common():
        w(f"   {k:12} {v:>12,.0f}  {100 * v / total:5.1f}%")
    w("\n   model                calls    credits  per call  median prompt  p90 prompt")
    for m, cc in sorted(by_model.items(), key=lambda kv: -sum(kv[1].values())):
        s = sum(cc.values())
        xs = sorted(ctx[m])
        w(f"   {m:20}{n_model[m]:>6}{s:>11,.0f}{s / n_model[m]:>10.1f}{xs[len(xs) // 2]:>15,}{xs[int(len(xs) * .9)]:>12,}")

    w(f"\n2. Cold calls by gap since the previous call started (models with >= {min_pairs} pairs)")
    w("   A step from ~0% to ~100% between two columns locates that model's cache lifetime.")
    table = collections.defaultdict(lambda: [0, 0])
    per_model = collections.Counter(p["cur"]["model"] for p in ps)
    for p in ps:
        t = table[(p["cur"]["model"], bucket(p["gap"]))]
        t[0] += 1
        t[1] += p["cold"]
    head = "".join(f"{('%g' % lo) + '+':>9}" for lo in BUCKETS[:-1])
    w(f"   {'model':20}{head}   (cold% / pairs)")
    for m, n in per_model.most_common():
        if n < min_pairs:
            continue
        cells = []
        for lo in BUCKETS[:-1]:
            t = table.get((m, lo))
            cells.append(f"{(f'{100 * t[1] / t[0]:.0f}%/{t[0]}') if t else '-':>9}")
        w(f"   {m:20}{''.join(cells)}")

    w(f"\n3. Excess credits from cold calls, by cause (long gap = {long_gap:g}+ minutes)")
    cls = collections.Counter()
    for p in ps:
        if p["cold"]:
            cls[("shrank" if p["shrank"] else "same context") + (" / long gap" if p["gap"] >= long_gap else " / short gap")] += p["excess"]
    for k, v in cls.most_common():
        w(f"   {k:28} {v:>10,.0f}  {100 * v / total:5.1f}% of spend")
    w("   short gap + same context: the prefix changed or the provider did not reuse it; mostly outside an agent's control.")
    w("   shrank: an upper bound; the common prefix of a compacted prompt is not known.")

    w("\n4. Long-gap cold calls with an unchanged context, by what filled the gap")
    cache, lab_x, lab_n, eg = {}, collections.Counter(), collections.Counter(), collections.defaultdict(list)
    ctl = collections.defaultdict(list)
    for p in ps:
        if p["gap"] < long_gap or p["shrank"]:
            continue
        label, knobs = attribute(p, load_events(state_dir, p["cur"]["session"], cache))
        if p["cold"]:
            lab_x[label] += p["excess"]
            lab_n[label] += 1
            if knobs and len(eg[label]) < 3:
                eg[label].append(f"{p['gap']:.0f}m {knobs}")
        if controllable(label):
            ctl[p["cur"]["model"]].append(p)
    for k, v in lab_x.most_common():
        w(f"   {v:>10,.0f} credits  n={lab_n[k]:<4} {k}  {'; '.join(eg[k])}")

    w("\n5. Expected net saving from checking in during agent-controllable long gaps")
    w("   Uses each model's expected rebuilt fraction by gap (same-context pairs, forced non-decreasing).")
    w(f"   Buckets with < {MIN_BUCKET} pairs are unknown, and an interval that needs one prints '?'.")
    w("   Intervals are start-to-start: a wait of w after a call lasting d gives w + d.")
    w(f"   A check-in costs one cached read of the prompt, {CHECKIN_OUTPUT_TOKENS} output and "
      f"{CHECKIN_APPENDED_TOKENS} appended tokens. Every controllable long gap counts, warm or cold.")
    w("   Break-even = (rebuild price - read price) / read price: check-ins one avoided rebuild pays for.")
    w(f"   {'model':20}{'gaps':>6}{'observed':>10}{'expected':>10}" +
      "".join(f"{'every %gm' % i:>11}" for i in intervals) + "   break-even")
    num = lambda x: f"{x:,.0f}" if x is not None else "?"
    for m, gs in sorted(ctl.items(), key=lambda kv: -sum(p["lost_cost"] for p in kv[1])):
        if per_model[m] < min_pairs:
            continue
        base, nets = checkin_net(gs, loss_curve(ps, m), intervals, r)
        observed = sum(p["lost_cost"] for p in gs)
        mr, rd = miss_rate(gs[0]["cur"], r), price(gs[0]["cur"], r, "cache_read")
        be = f"{mr / rd:.0f}" if mr and rd else "?"
        w(f"   {m:20}{len(gs):>6}{observed:>10,.0f}{num(base):>10}" + "".join(f"{num(x):>11}" for x in nets) + f"   {be}")
    w("   observed = credits actually lost to rebuilds in those gaps; expected = the same from the curve.")
    w("   Positive = checking in at that interval would have cost less than not checking in.")


def main(argv=None):
    home = os.path.join(os.path.expanduser("~"), ".copilot")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--db", default=os.path.join(home, "session-store.db"))
    ap.add_argument("--state-dir", default=os.path.join(home, "session-state"))
    ap.add_argument("--since", help="ISO date or timestamp, inclusive (UTC)")
    ap.add_argument("--until", help="ISO date or timestamp, exclusive (UTC)")
    ap.add_argument("--session", help="restrict to one session id")
    ap.add_argument("--long-gap", type=float, default=5.0, help="minutes; default 5")
    ap.add_argument("--intervals", default="4,10,20,25", help="check-in intervals in minutes, start-to-start")
    ap.add_argument("--min-pairs", type=int, default=50)
    a = ap.parse_args(argv)
    if not os.path.exists(a.db):
        print(f"unread: no session store at {a.db}", file=sys.stderr)
        return 2
    intervals = [float(x) for x in a.intervals.split(",")]
    report(load_calls(a.db, a.since, a.until, a.session), a.state_dir, a.long_gap, intervals, a.min_pairs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
