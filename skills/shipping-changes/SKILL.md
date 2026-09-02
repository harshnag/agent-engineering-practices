---
name: shipping-changes
description: Safely carry reviewed work from pull request through merge and deployment — pinning the exact head that passed, monitoring the exact post-merge run, applying migrations before an automatic deploy, verifying deployed identity, separating artifact trust domains, and interpreting skipped, queued, absent, or cancelled work honestly. Use when opening, updating, merging, or auto-merging a pull request; deploying to production; changing a schema; diagnosing a green merge that did not ship; designing deployment automation; or claiming which commit is live.
license: MIT
metadata:
  provenance: Extracted from two private production codebases, 2026
  author: harshnag
  version: "1.0"
---

# Shipping changes

Landing is not "the pull request merged". It ends when the exact reviewed change
has reached its intended environment, every required job reached a terminal
state, and the running artifact identifies itself as that change.

`agent-concurrency` governs who authors and reviews. This skill governs what
happens after review.

## Establish what merging does

Write one current line in the project instructions:

| Action | Effect | Decided by |
|---|---|---|
| Merge to the trunk | no deploy / queued deploy / immediate deploy | the current pipeline definition |

If the trunk auto-deploys, merging **is** the deployment. Every instruction
phrased "before deploying" is therefore a pre-merge predicate.

> **A document that is merely stale makes you do the old thing. A document whose
> claim has inverted makes you do the dangerous thing, confidently, with a
> citation.**

Do not prove this by comparing two copies of the same prose. Read the current
pipeline and probe the running system.

## Autonomy is bounded by predicates

An agent may merge and deploy without another permission step when the repository
already authorizes that behavior and all checked-in and operation-specific
predicates hold.

That autonomy does not waive:

- review by a different context;
- exact-head verification;
- migration ordering;
- fresh human presence for identity operations;
- explicit authorization for destructive production-data decisions;
- monitoring through the terminal deployment result.

Permission and safety are different dimensions. Removing a redundant permission
step does not remove a predicate.

## Pin the merge to what passed

Reading a pull request head and merging it are two operations over a mutable
value. A push can land between them.

1. Resolve the current head identifier.
2. Find the required run for **that exact head**.
3. Read jobs and steps, not only the run-level conclusion.
4. Re-check review and mergeability.
5. Merge with an expected-head guard.

> **A head-mismatch refusal is the safety mechanism working.**

Do not drop the guard to make the command succeed. Fetch the new head, review
the delta, and start the predicates again.

A worker saying it is finished pushing cannot close this race: review feedback
is itself a reason to push again.

## A successful run may have checked nothing

Run-level success describes the workflow. A required job may have been skipped,
and a job can succeed after every meaningful step was conditionally omitted.

Treat these as distinct states:

| State | Meaning |
|---|---|
| passed | the named checks executed on the exact subject and passed |
| failed | a named check executed and failed |
| queued or pending | no verdict yet |
| skipped or absent | unverified, unless omission is an explicit accepted path |
| unreadable | the monitor could not ask; never render as pass or fail |
| cancelled | incomplete; the trunk does not roll back |

Duration is not evidence that a browser, build, migration, or deploy ran. Read
the step list and its annotations.

Copy diagnostic artifacts before re-running a failed job when a re-run replaces
or deletes them.

## Follow the exact post-merge run

Branch names and "latest run" queries race with the next merge. Capture the
post-merge commit and exact run identifier, then follow that run through all
required jobs.

Do not stop at green CI if deployment is a separate job or service. A cancelled
or absent deploy leaves the trunk advanced and production unchanged.

Separate two event questions:

- **Is anything in flight that can deploy this commit?**
- **What commit is running now?**

"Production is behind" does not answer whether anything is coming. A useful
monitor distinguishes in flight, inert, contradicted, and unreadable.

## Verify identity from the running artifact

Build a commit identifier into the artifact and expose an uncached, unauthenticated
readback that performs no database work. After deployment, require:

- the expected trunk identifier;
- a clean-build marker;
- a parseable response from the intended environment.

A null, dirty, older, different, or unreadable identifier fails deployment even
when the upload command exited zero.

Identity and bytes are complementary:

- artifact identity says which source revision is serving;
- a digest comparison says whether user-reachable bytes match what was built.

Equal bytes cannot identify a server-only change. Correct identity cannot prove
every client asset matches. State each boundary beside its result.

## Compare the complete user-reachable graph

A deploy probe that selects one convenient file, compares names, or warns on
failure is not a boundary.

Start from the entry artifact, parse every referenced asset, and compare content
digests. Treat unparseable references as failures rather than omissions. Report
missing, unexpected, and mismatched artifacts separately.

Correct environments may differ in expected ways. "Not identical" is not a
useful failure condition unless identity is the invariant. Compare the net
user-visible difference across the span, not the union of intermediate commits.

## Migrations happen before an automatic deploy

When merging triggers deployment:

1. Probe the live schema the new code will meet.
2. Apply the compatible migration.
3. Probe again and confirm the intended shape.
4. Merge pinned to the already-reviewed head.

The migration ledger is not the schema when another path can change production.
Ask the object the code actually uses.

Only an additive, backward-compatible expansion usually has a safe one-deploy
order. A rename, type change, constraint, or deletion needs an expand/migrate/
contract sequence across multiple deployments.

The failure mode depends on the access path:

- isolated new storage often fails only its new feature;
- a change on a hot path fails loudly and broadly;
- a change on a cold or optional path can fail silently because absence is a
  normal presentation.

Silence makes pre-merge confirmation more important, not less.

See `references/MIGRATIONS.md` and `assets/delivery-checklist.md`.

## The deploy environment is a separate trust domain

Credentials must not be available to untrusted-branch code. File permissions do
not protect a secret from code running as the same user.

The stronger design:

1. A gated environment builds the complete artifact once.
2. It hashes every part and binds the manifest to the gated trunk identifier.
3. A deploy environment that never runs checkout code verifies the manifest.
4. Host-held policy checks the artifact's destination and configuration.
5. The uploader installs nothing and executes no artifact-supplied scripts.

A digest mismatch is fatal even if the platform's default validation only warns.

`references/DEPLOY-TRUST-BOUNDARY.md` covers the design and its controls.

## Dry run must be structurally incapable of shipping

A flag passed through the wrong wrapper can reach a diagnostic child while the
real deploy child still uploads.

Test that:

- dry run starts exactly the expected child;
- the flag reaches the real side-effect boundary;
- no upload-capable child can run;
- only named safe flags pass through;
- changing a target requires a separate explicit option.

Do not rely on blind argument passthrough. Production should not be one
unreviewed argument away.

## Do not hide the consequential command

A convenience wrapper around merge or deploy is not enforcement when the
underlying command remains available. It shortens the dangerous path and hides
the head pin, predicates, and exact-run monitoring the visible form teaches.

Automate the checks and readbacks. Keep the consequential operation explicit.

Where a mistake cannot be refused, detect the harm retrospectively and print the
detector's blind population on every run. A detector that watches bad outcomes
cannot prove the safe protocol was followed when no harm happened.

## A merged tree can inherit evidence only by identity

If the merged tree is byte-identical to the exact tree whose gate passed, the
result transfers without another run. The empty diff is the evidence.

This requires:

- the identifier the gate actually ran on, not a later branch tip;
- a freshly fetched trunk;
- comparison of complete trees.

A real merge of diverging trees produces a tree no prior run saw. That is when
post-merge verification is necessary, even without conflict markers.

## Finish with a delivery record

Record:

- reviewed head;
- run that gated it and the jobs that actually executed;
- merge commit;
- post-merge run and deployment result;
- migration precondition and confirmation, if any;
- running artifact identity;
- byte-verification boundary, if any;
- anything skipped, unreadable, or handed back.

The record should contain identifiers and predicates, not "green" or "deployed"
without the subject they describe.
