#!/usr/bin/env python3
"""Tests for cache_report.py against a synthetic session store with known answers.

Run:  python skills/token-efficiency/scripts/test_cache_report.py
Set CACHE_REPORT=/path/to/copy.py to run the same tests against a mutated copy.
"""
import importlib.util
import io
import json
import os
import sqlite3
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "cache_report", os.environ.get("CACHE_REPORT", os.path.join(HERE, "cache_report.py")))
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

T0 = 1_800_000_000_000  # ms
MIN = 60_000
PRICES = {"input": 4.0, "cache_read": 0.2, "cache_write": 5.0, "output": 20.0}  # USD per MTok
CREDITS = {k: v * 100 / 1e6 for k, v in PRICES.items()}  # credits per token


def iso(t):
    import datetime as dt
    return dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc).isoformat().replace("+00:00", "Z")


def details(model, inp, read, write, out, prices=PRICES):
    lines = []
    for kind, n in (("input", inp - read - write), ("cache_read", read), ("cache_write", write), ("output", out)):
        # costPerBatch is nano-credits per batch; USD 1 = 100 credits = 1e11 nano-credits
        lines.append(dict(batchSize=1_000_000, costPerBatch=int(prices[kind] * 1e11), tokenCount=n,
                          tokenType=kind, model=model))
    return json.dumps(lines)


class Fixture:
    def __init__(self):
        self.dir = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.dir.name, "session-store.db")
        self.state = os.path.join(self.dir.name, "session-state")
        con = sqlite3.connect(self.db)
        con.execute("""create table assistant_usage_events (id integer primary key, session_id text,
            agent_id text, model text, input_tokens int, output_tokens int, cache_read_tokens int,
            cache_write_tokens int, duration_ms int, created_at text, token_details_json text)""")
        self.con = con

    def call(self, session, start_min, inp, read, write, model="claude-x", agent=None, dur_s=10, prices=PRICES):
        start = T0 + start_min * MIN
        self.con.execute(
            "insert into assistant_usage_events (session_id, agent_id, model, input_tokens, output_tokens,"
            " cache_read_tokens, cache_write_tokens, duration_ms, created_at, token_details_json)"
            " values (?,?,?,?,?,?,?,?,?,?)",
            (session, agent, model, inp, 100, read, write, dur_s * 1000, iso(start + dur_s * 1000),
             details(model, inp, read, write, 100, prices)))

    def events(self, session, items):
        os.makedirs(os.path.join(self.state, session), exist_ok=True)
        with open(os.path.join(self.state, session, "events.jsonl"), "w", encoding="utf-8") as fh:
            for it in items:
                fh.write(json.dumps(it) + "\n")

    def calls(self, **kw):
        self.con.commit()
        return cr.load_calls(self.db, **kw)


def tool(call_id, name, start_min, end_min, args=None, agent=None):
    s = {"type": "tool.execution_start", "timestamp": iso(T0 + start_min * MIN),
         "data": {"toolCallId": call_id, "toolName": name, "arguments": args or {}}}
    e = {"type": "tool.execution_complete", "timestamp": iso(T0 + end_min * MIN),
         "data": {"toolCallId": call_id}}
    if agent:
        s["agentId"] = e["agentId"] = agent
    return [s, e]


def user(at_min):
    return {"type": "user.message", "timestamp": iso(T0 + at_min * MIN), "data": {}}


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        f = self.f
        f.call("s1", 0, 100_000, 0, 100_000)          # cold start
        f.call("s1", 2, 102_000, 100_000, 2_000)      # warm, 2 min gap
        f.call("s1", 8, 104_000, 0, 104_000)          # cold after 6 min gap, same context
        f.call("s1", 8.5, 30_000, 0, 30_000)          # compaction: shrank, short gap
        f.events("s1", tool("t1", "read_powershell", 2.2, 7.9, {"delay": 600}))
        self.ps = list(cr.pairs(f.calls(), cr.rates(f.calls())))

    def tearDown(self):
        self.f.con.close()
        self.f.dir.cleanup()

    def test_created_at_is_end_so_start_subtracts_duration(self):
        c = self.f.calls()[0]
        self.assertAlmostEqual(c["start"], T0, delta=1)
        self.assertAlmostEqual(c["end"] - c["start"], 10_000, delta=1)

    def test_warm_call_is_not_cold(self):
        self.assertFalse(self.ps[0]["cold"])
        self.assertAlmostEqual(self.ps[0]["gap"], 2.0, places=3)

    def test_long_gap_miss_is_cold_same_context_with_excess(self):
        p = self.ps[1]
        self.assertTrue(p["cold"])
        self.assertFalse(p["shrank"])
        self.assertAlmostEqual(p["gap"], 6.0, places=3)
        # 102k lost tokens x (5.0 - 0.2) USD/MTok = USD 0.4896 = 48.96 credits
        self.assertAlmostEqual(p["excess"], 48.96, places=2)

    def test_compaction_is_shrank_and_rebuild_is_capped_at_the_current_prompt(self):
        p = self.ps[2]
        self.assertTrue(p["cold"])
        self.assertTrue(p["shrank"])
        self.assertLess(p["gap"], 5)
        # only the 30k tokens actually sent can have been rebuilt, not the previous 104k
        self.assertAlmostEqual(p["excess"], 30_000 * (CREDITS["cache_write"] - CREDITS["cache_read"]), places=6)

    def test_gap_attributed_to_the_tool_call_that_filled_it(self):
        label, knobs = cr.attribute(self.ps[1], cr.load_events(self.f.state, "s1", {}))
        self.assertEqual(label, "inside one tool call: read_powershell")
        self.assertEqual(knobs, "delay=600")

    def test_tool_call_outranks_a_message_that_arrived_while_it_ran(self):
        self.f.events("s1", tool("t1", "read_powershell", 2.2, 7.9, {"delay": 600}) + [user(5)])
        label, _ = cr.attribute(self.ps[1], cr.load_events(self.f.state, "s1", {}))
        self.assertEqual(label, "inside one tool call: read_powershell")

    def test_user_message_in_an_uncovered_gap_is_human_idle(self):
        self.f.events("s1", [user(5)])
        label, _ = cr.attribute(self.ps[1], cr.load_events(self.f.state, "s1", {}))
        self.assertEqual(label, cr.HUMAN)
        self.assertFalse(cr.controllable(label))

    def test_uncovered_gap_without_a_message_is_unattributed_idle(self):
        self.f.events("s1", tool("t1", "view", 2.2, 2.3))
        label, _ = cr.attribute(self.ps[1], cr.load_events(self.f.state, "s1", {}))
        self.assertEqual(label, cr.IDLE)
        self.assertTrue(cr.controllable(label))

    def test_missing_events_reports_unread_not_a_cause(self):
        label, _ = cr.attribute(self.ps[1], cr.load_events(self.f.state, "no-such-session", {}))
        self.assertEqual(label, cr.UNREAD)
        self.assertFalse(cr.controllable(label))

    def test_sub_agent_gap_uses_its_own_tool_spans(self):
        f = self.f
        f.call("s2", 0, 50_000, 0, 50_000, agent="a1")
        f.call("s2", 7, 51_000, 0, 51_000, agent="a1")
        f.events("s2", tool("m", "view", 0.5, 6.9) + tool("x", "powershell", 0.3, 6.9, {"initial_wait": 400}, agent="a1"))
        ps = [p for p in cr.pairs(f.calls(session="s2"), {}) if p["cur"]["agent"] == "a1"]
        label, knobs = cr.attribute(ps[0], cr.load_events(f.state, "s2", {}))
        self.assertEqual(label, "inside one tool call: powershell")
        self.assertEqual(knobs, "initial_wait=400")

    def test_zero_cache_write_price_means_rebuild_at_input_price(self):
        prices = dict(PRICES, cache_write=0.0, input=5.0, cache_read=0.5)
        f = self.f
        f.call("s3", 0, 10_000, 0, 0, model="gpt-x", prices=prices)
        f.call("s3", 40, 10_000, 0, 0, model="gpt-x", prices=prices)
        calls = f.calls(session="s3")
        # (5.0 - 0.5) USD/MTok = 450 credits per million tokens
        self.assertAlmostEqual(cr.miss_rate(calls[1], cr.rates(calls)), 450 / 1e6, places=9)
        p = list(cr.pairs(calls, cr.rates(calls)))[0]
        self.assertGreater(p["excess"], 0)

    def test_report_runs_and_states_its_selection(self):
        out = io.StringIO()
        cr.report(self.f.calls(), self.f.state, 5.0, [4.0], 1, out=out)
        text = out.getvalue()
        self.assertIn("Selection: 4 model calls, 3 same-thread pairs, 1 sessions", text)
        self.assertIn("inside one tool call: read_powershell", text)


def fake_pair(gap, lost_frac, shrank=False, model="m"):
    return {"cur": {"model": model}, "gap": gap, "lost_frac": lost_frac, "shrank": shrank}


class CurveTests(unittest.TestCase):
    def test_partial_loss_counts_by_its_fraction_not_as_a_full_miss(self):
        ps = [fake_pair(0.5, 0.0)] * 5 + [fake_pair(6, 0.4)] * 5
        curve = cr.loss_curve(ps, "m")
        self.assertAlmostEqual(cr.at(curve, 6), 0.4)

    def test_curve_is_non_decreasing_across_sampled_buckets(self):
        ps = [fake_pair(0.5, 0.02)] * 5 + [fake_pair(5.2, 0.9)] * 5 + [fake_pair(8, 0.5)] * 5
        curve = cr.loss_curve(ps, "m")
        self.assertAlmostEqual(cr.at(curve, 5.2), 0.9)
        self.assertAlmostEqual(cr.at(curve, 8), 0.9)

    def test_unsampled_bucket_is_unknown_not_zero(self):
        ps = [fake_pair(0.5, 0.02)] * 5 + [fake_pair(12, 1.0)] * 4
        curve = cr.loss_curve(ps, "m")
        self.assertIsNone(cr.at(curve, 12))
        self.assertIsNone(cr.at(curve, 40))

    def test_compacted_pairs_do_not_shape_the_curve(self):
        ps = [fake_pair(0.5, 0.0)] * 5 + [fake_pair(0.5, 1.0, shrank=True)] * 50
        self.assertAlmostEqual(cr.at(cr.loss_curve(ps, "m"), 0.5), 0.0)


def gap_of(minutes, tokens=100_000):
    c = {"model": "claude-x", "inp": tokens, "price": dict(CREDITS)}
    return {"prev": c, "cur": c, "gap": minutes}


def five_minute_curve():
    return [0.02 if lo < 5 else 1.0 for lo in cr.BUCKETS[:-1]]


class CheckinTests(unittest.TestCase):
    M = 100_000 * (CREDITS["cache_write"] - CREDITS["cache_read"])        # 48 credits per rebuild
    K = (100_000 * CREDITS["cache_read"] + cr.CHECKIN_OUTPUT_TOKENS * CREDITS["output"]
         + cr.CHECKIN_APPENDED_TOKENS * CREDITS["cache_write"])           # 2.65 credits per check-in

    def test_checking_in_under_the_lifetime_pays_and_over_it_does_not(self):
        base, (at4, at10) = cr.checkin_net([gap_of(20)], five_minute_curve(), [4, 10], {})
        self.assertAlmostEqual(base, self.M)
        self.assertAlmostEqual(at4, self.M - (4 * self.K + 4 * 0.02 * self.M + 0.02 * self.M))
        self.assertGreater(at4, 0)
        self.assertAlmostEqual(at10, self.M - (self.K + self.M + self.M))
        self.assertLess(at10, 0)

    def test_exact_multiple_leaves_a_full_final_interval(self):
        _, (net,) = cr.checkin_net([gap_of(8)], five_minute_curve(), [4], {})
        self.assertAlmostEqual(net, self.M - (self.K + 0.02 * self.M + 0.02 * self.M))

    def test_gap_shorter_than_the_interval_needs_no_check_in(self):
        _, (net,) = cr.checkin_net([gap_of(3)], five_minute_curve(), [4], {})
        self.assertAlmostEqual(net, 0.0)

    def test_unknown_bucket_makes_the_answer_unknown(self):
        curve = five_minute_curve()
        curve[cr.BUCKETS.index(10)] = None
        base, (at4, at10) = cr.checkin_net([gap_of(20)], curve, [4, 10], {})
        self.assertIsNotNone(base)
        self.assertIsNotNone(at4)
        self.assertIsNone(at10)


if __name__ == "__main__":
    unittest.main(verbosity=1)
