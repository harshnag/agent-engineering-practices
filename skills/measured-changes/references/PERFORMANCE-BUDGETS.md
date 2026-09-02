# Performance budgets by payer

Read `SKILL.md` first. This file turns "fast" into separately enforceable
quantities.

## Five budgets

| Budget | Subject | Typical instrument |
|---|---|---|
| First-arrival download | assets reachable from the built entry artifact | built reference graph and compressed bytes |
| Interaction wait | action to visible or otherwise user-observable completion | real input in the real client |
| Verification | developer time and conclusiveness | phase timings plus protected sample counts |
| CI | queue time, wall time, and quota | exact jobs and billing units |
| Deployment | build, upload, rollout, and confirmation | exact post-merge run and identity readback |

State which are enforced and which are aspirations. Never tick a combined row
because one half gained a gate.

## Budget by reach

File type does not tell you whether every user downloads an artifact. Derive
first-arrival reach from the built entry's complete reference graph.

Then walk every emitted asset and require it to fall under some budget. Otherwise
weight can move into an unbudgeted file without any guarded number changing.
Exemptions use exact names and carry a reason.

## Use bytes and name the proxy

Write byte limits as bytes. Decimal and binary unit labels differ enough to
consume ordinary headroom while both figures remain technically correct.

The build's compressed size is usually a proxy for user transfer; an edge may
recompress or negotiate differently. A stable proxy is valuable for detecting
change even when it is not the delivered truth. State the boundary.

Use per-kind budgets where one large category's slack could hide a doubling of a
small category.

## A ratchet fails in both directions

A useful budget reports three different failures:

- **over:** the build exceeds the ceiling;
- **loose:** the ceiling's slack has grown large enough to admit the regression
  it exists to catch;
- **drift:** the build no longer agrees with the recorded measurement.

Lowering a ceiling after a measured saving is ordinary. Raising one requires a
new measurement and a written argument.

Do not invent a universal slack percentage. Calibrate the hole against the class
of regression the budget is intended to catch, and say when that calibration has
not been done.

## Measure cost under drift

Use phases within one run or a control the change cannot affect. A before/after
across changing host load is a claim about both the code and the machine.

Do not optimize the step whose name sounds expensive. Measure the breakdown.
