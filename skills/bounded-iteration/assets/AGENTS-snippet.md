## Bounded iteration

<!-- Paste into AGENTS.md and fill in both commands. Prove the fast command
     fails on a broken input before relying on it. -->

- **Smallest check first.** Iterate with `<fast command running one test or
  job>`. Run `<full suite command>` once before committing. Filter logs for
  failures.
- **Diagnose, then change.** After a failure, find the cause with one targeted
  print or state dump before editing. Never nudge a number and rerun to see.
- **Two strikes.** If the same check fails twice after fixes, stop patching,
  write down the believed cause and change approach. After a third failure,
  report blocked with evidence.
- **Checks test the product.** Never add data, flags or exemptions that exist
  only to satisfy a check. Fix the design, or change the check openly.
- **Time boxes.** Every delegated task states a time box, a stop condition, the
  fastest verification command and a report format. At the box, commit only
  verified work and report progress, blockers and the next step.
- **Progress is visible.** Reports name what now works that did not, with the
  command that shows it. "Still tuning" twice means re-scope.
- **Watch for loops.** Small numeric diffs undoing each other, the same failing
  assertion, or tool calls rising with no newly passing checks mean stop and
  diagnose. Orchestrators check sub-agent diffs mid-run and intervene early.
- **Batch and reuse.** Read needed files once, in parallel. Give sub-agents
  exact files, commands and a prior example.
