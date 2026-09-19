# Adopting a contract workflow without a second system

The [skill](../SKILL.md#maintain-current-contracts-without-replacing-history)
owns the procedure. This reference explains adoption and review; its examples
are illustrative, not a new source of project requirements.

## Start with roles, not directories

Inventory the documents relevant to the requested scope. Classify each as
instructions, current contract, proposed change, history, research, or a route.
A long topic document can hold several roles if their boundaries are explicit.
Choose one owner per requirement, not necessarily one file per subsystem.

Start with a bounded change unless a whole-corpus migration was requested.
For that migration, classify the entire agreed corpus, including entrypoints,
templates, tests, and old links. A search for a new heading cannot find the
unclassified documents it was supposed to cover.

The adopting project's read-in should answer three different questions:

| Reader's question | Route |
|---|---|
| What is required now, and how can I check it? | Maintained contract and scenario evidence |
| What change is proposed, who owns it, and what remains? | The existing pending-work queue and its claimable item |
| Why this rule, and what was tried or rejected? | Accessible topic history and dated research |

Keep `AGENTS.md` as the working agreement. Vendor steering or constitution
files, if adopted, must have an explicit scope and route to the same authority,
not independently maintain the same instructions.

## A small worked example

Suppose a tool currently refuses an unreadable input file. A request proposes
support for a second input format. These are invented facts for the example,
not observations about a tool shipped here.

The existing current contract owns `INPUT-1`, the unreadable-input refusal.
The claimable work item proposes `INPUT-2`, accepting the new format. It links
`INPUT-1` as an unchanged boundary instead of copying its wording. Its design
explains how format detection works; that implementation detail does not become
an externally promised API by appearing in the current contract.

| Case | Intended evidence route | What still needs checking |
|---|---|---|
| `INPUT-1`: unreadable input is refused | Source error branch and regression assertion | The test actually creates an unreadable input and reaches that branch |
| `INPUT-2`: supported new format succeeds | Parser and assertion on parsed output | Both the accepted input and the required output are exercised |
| `INPUT-3`: malformed new format is refused | Parser and known-bad input assertion | The refusal is explicit, not an empty success-shaped result |

Before implementation, those planned assertions are **unverified**, not
automated coverage that already exists. After running them, record the exact
revision, invocation, outcome and scope. If a real-environment check is required,
link its procedure and observation separately; a local unit test does not
inherit that boundary.

If inspection discovers the supposed `INPUT-1` refusal is already broken,
record the mismatch. Do not rewrite the accepted contract to allow silent
success or fix unrelated behavior without a scope decision.

The reviewed change updates the current owner with accepted cases and evidence.
If another branch changed that owner meanwhile, reconcile the intended behavior
with a reviewer; conflict-free text is not proof of compatible requirements.
History keeps the format choice, rejected alternatives and verification limits.
Once those records and routes survive independently, delete the completed item
under the existing queue protocol. Do not introduce an archive full of apparently
pending tasks. Any retained packet must be clearly historical and outside the
pending listing.

For a behavior-preserving repair, `INPUT-1` would remain unchanged: the packet
records a regression fix and evidence, not a fictitious new requirement.

## Migration is not deletion

When an old topic document owns current claims and history together, either keep
its current section as the sole owner or move that authority and leave a
prominent route. Label old positions as historical, preserve meaningful anchors
or redirects, and link history from the current owner. A link only in git history
is not a usable read-in route.

Move stale actionable wording out of the current route without erasing the
observations and reversals that explain it. Do not rename every heading, impose
a universal page-size cap, or summarize all history merely to fit a template.
Bound any separate compression work using the selector in the memory skill.

## What a local checker could establish

Reuse the repository's existing Markdown parsing, link resolution, test runner,
and verification entrypoint before introducing new tooling. These are possible
checks, **not checks this skill installs**:

| Structural promise | Deterministic negative control | Limit |
|---|---|---|
| Required sections and evidence fields exist | Remove one required field from a valid fixture | Presence does not establish useful content |
| Scenario IDs have one declared owner | Duplicate an ID in a second owner | Different IDs can still describe the same requirement |
| Evidence targets resolve | Replace a target or anchor with a missing one | A resolving test may not exercise the scenario |
| Required subjects remain reachable | Delete a known required owner and its generated index entry | Needs an independent expected inventory; discovery alone shrinks with deletion |
| Pending work has one route | Add a forbidden second queue to a fixture in the declared discovery scope | Cannot find queues outside that scope |

Start green, prove each mutation changed the intended property, and require the
specific check to refuse it. Re-run after changing fixtures or check logic.
Keep valid history and allowed project layouts as positive controls. State the
discovered corpus and failures explicitly; unreadable files cannot silently
disappear. `checking-claims` and `measured-changes` own the full gate-validity
method.

A shape checker cannot prove unique *semantic* ownership, requirement
completeness, truthful evidence, passing runtime behavior, or the usefulness of
preserved reasoning. Those need source inspection, behavioral checks and a
different reviewing context. Do not report a structural pass as contract
verification.

## No vendor decision follows automatically

The [dated evidence review](SPEC-WORKFLOW-EVIDENCE.md) distinguishes product
documentation from measured results. A framework can standardize artifacts;
it can also duplicate the mechanisms already present. Evaluate a specific gap
before adopting one, and keep the project's isolation, resource, evidence,
review and delivery controls intact.

## File-first coordination

**Decision, 2026-09-18.** Extend the existing
[memory procedure](../SKILL.md#coordinate-through-owned-files-first), not the
queue. Assignments and progress belong in the claimable item; durable decisions
belong in topic history; handovers route to both. The coordination skill owns
live-control decisions, not another copy of the work specification.

**Evidence boundary.** The user requested this policy in the origin project.
Its proposed documentation section was read as a provisional, uncommitted
artifact on this date after its named remote branch was unavailable. That is
evidence of requested design intent, not of a landed rule, measured reduction
in messaging, or operational enforcement. Private source names, paths and
domain details are deliberately not reproduced. The existing
[public framework comparison](SPEC-WORKFLOW-EVIDENCE.md) supports separation
of artifact roles; it does not establish an OpenSpec messaging ban. No framework
is installed or required by this decision.

**Why this shape.** A chat-only decision is hard to discover and can arrive
after its replacement. Files preserve an inspectable owner, but isolated trees
do not share uncommitted edits. Therefore a usable pointer identifies a readable
revision, not merely a filename. A branch locates ongoing work; the exact commit
identifies what the receiver read. Read-only inspection avoids contaminating
the receiver's own checkout.

Rejected alternatives: a second coordination ledger recreates contention and
competing authority; a total messaging ban strands workers that cannot discover
updates and delays urgent safety stops; interpreting a progress file as a
heartbeat confuses recorded work with present life or capacity. Native claim,
review, publishing and admission gates remain unchanged.

### Acceptance and verification boundary

These are manual policy-review cases, not installed automated checks or claims
that a session transport was exercised:

| Case | Required reading outcome | Owning surface |
|---|---|---|
| Assignment or progress changes | Update the existing item, not a second queue or chat specification | Skill procedure and item template |
| Receiver has another worktree | Read repository, branch, exact revision, path and section without editing another tree | Skill procedure and handover template |
| Artifact exists only as an unpublished edit | Mark provisional, identify location/time; do not call it a stable handoff | Skill procedure |
| Routine acknowledgment or status request | Omit it; essential discovery wakeups remain possible | Skill procedure and coordination skill |
| Pointer cannot be read | Report the inaccessible artifact minimally; state remains unresolved | Skill procedure |
| Urgent correction cannot await publication | Stop unsafe action, then persist and point to the correction; preserve correction ordering | Skill procedure and coordination skill |
| Claim or progress timestamp looks quiet | Use live instruments; do not infer admission, death or reclaim permission | Skill procedure and coordination skill |

Review these cases against the linked procedure and templates in the candidate
revision. The publish and inventory gates cover their documented structural
boundaries only; they do not enforce message traffic, prove pointer access for
every receiver, or measure collaboration quality. No new checker is introduced.
