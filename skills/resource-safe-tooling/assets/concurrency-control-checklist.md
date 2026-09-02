# Deterministic concurrency controls

Use one case at a time. The adapter should block on controlled events and do no
synthetic work.

## Known-good cases

- [ ] Intent is durable before start is requested.
- [ ] A running operation prevents a second grant when the policy says it must.
- [ ] The maximum in-flight count never exceeds the configured bound.
- [ ] Nested stages retain one operation identity.
- [ ] Completion order follows the promised rule.
- [ ] Restart reconciles old state before granting new work.
- [ ] A simulated clock jump does not steal a live record.
- [ ] Destruction is acknowledged before state changes to absent.
- [ ] A stale workload still receives limits imposed outside it.

## Known-bad cases

- [ ] Requested policy differs from enforced policy and creation is refused.
- [ ] Intent is not durably recorded and the state machine fails.
- [ ] A waiter expires and no work starts.
- [ ] Controller state is unavailable and no work starts.
- [ ] Enumeration finds an unknown survivor and all grants stop.
- [ ] A release names the wrong operation and is refused.

## One ordinary integration run

- [ ] Requested and actual policy are both recorded.
- [ ] Peak process count and each resource metric are named.
- [ ] Wall time is reported as capacity evidence, not a pass threshold.
- [ ] Exit behavior matches the uncapped path.
- [ ] Cleanup leaves no owned residue.
