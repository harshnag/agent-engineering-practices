# Delivery checklist

## Before merge

- [ ] State what merging currently does.
- [ ] Confirm review came from a different context.
- [ ] Resolve the exact pull request head.
- [ ] Read required jobs and steps for that exact head.
- [ ] For conditional checks, recover the original event, actual checked
      revision, diff endpoints and selection predicate from retained run
      evidence; confirm skips remain valid after any retargeting.
- [ ] Reconcile affected contract owners and inspect scenario evidence at that
      head; keep structural validation distinct from behavioral results.
- [ ] Preserve decisions and verification limits in accessible history before
      deleting the completed change item from the existing queue.
- [ ] Confirm the base and mergeability.
- [ ] Apply and confirm any compatible production migration.
- [ ] Merge with an expected-head guard.

## After merge

- [ ] Capture the merge commit and exact post-merge run.
- [ ] Follow every required job to a terminal state.
- [ ] Treat skipped, absent, queued, pending, cancelled, and unreadable as
      distinct from passed.
- [ ] Confirm the deployment job actually ran.
- [ ] Read back the running artifact identity.
- [ ] Compare user-reachable bytes where that boundary exists.

## Record

- [ ] Reviewed head and gating run.
- [ ] Actual checked revision, original event and effective comparison scope;
      current PR metadata alone does not establish the old run's inputs.
- [ ] Merge commit and post-merge run.
- [ ] Migration predicate and confirmation.
- [ ] Running identity and byte boundary.
- [ ] Anything not run or not readable.
- [ ] Affected contract/history links, with repository and runtime evidence
      clearly distinguished.
