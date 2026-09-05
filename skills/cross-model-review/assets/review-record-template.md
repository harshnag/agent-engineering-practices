# Cross-model review record

One block per review. Keep it where review already happens — normally the pull
request body — rather than in a file nobody opens.

---

**Artifact:** [plan | diff] — say which; the identity fields below differ by type,
and "reviewed the change" names nothing.
**Exact revision:**
- *diff:* [commit sha or PR head sha; reviewed before commit, the staged tree id
  from `git write-tree` — that is the identifier naming the whole reviewed tree.
  A patch digest identifies the change but not the tree: the same patch on a
  different base produces a different result, so record the base too if you use
  one.]
- *plan in the repository:* [the repo-relative path **and** the commit sha the
  reviewed version was read at — or the blob id, which pins the content even if
  the file is later moved. A sha alone does not say which file was reviewed, and
  a path alone moves under you.]
- *plan in a chat, session, or issue thread:* [digest of the exact reviewed text,
  e.g. `shasum -a 256`, **and** the session or event id that locates it. Without
  this the plan checkpoint has no auditable subject — which is the checkpoint
  where a finding is cheapest and the artifact is least durable.]

**Committed as:** [sha, once it lands — confirm `git rev-parse <sha>^{tree}`
equals the reviewed tree id]
**Checkpoint:** [plan-before-implementation | diff-before-landing]
**Date:** [YYYY-MM-DD]

**Author:** [model] at [effort] effort
**Reviewer requested:** [model] at [effort] effort
**Reviewer confirmed by the runtime — model:** [model reported by the invocation
itself, or `unconfirmed`]
**Reviewer confirmed by the runtime — effort:** [effort reported by the
invocation itself, or `unconfirmed`]
[Do not copy the requested values into the confirmed fields, and do not accept
the reviewer's own account of which model it is or how hard it thought. A
fallback can change the effort without changing the model.]
**Invocation:** [session or agent id, so the review can be found again]

**Outcome:** [`no-findings` | `findings-dispositioned` | `blocked`] — did the
review run?
[If `blocked`: why, and which exit was taken — waited, escalated, or proceeded
unreviewed by an attributed decision.]

**Reviewer verdict:** [`approve` | `revise` | `not-run`] — what did it conclude?
[`revise` blocks the artifact. Record which findings stand, and either the next
cycle or the named human the disagreement was escalated to. `not-run` is
permitted **only** when the outcome is `blocked`, because a reviewer that never
ran concluded nothing; anywhere else it is a missing verdict wearing a value.]

**Cycle:** [n] of [bound], counting cycles on this artifact's whole lineage

| # | Finding | Disposition |
|---|---|---|
| 1 | [one claim, stated so it can be checked] | accepted — [what changed] |
| 2 | [...] | rejected — [reasoning] |
| 3 | [...] | deferred — [named carrier: issue, item, follow-up] |

**Calibration status of this direction:** [unmeasured | last calibrated
YYYY-MM-DD, planted defect found / missed]

---

Rules this shape exists to enforce, each of which has been got wrong before:

- **Absence of a block means unverified, not clean.** A missing record is not a
  `no-findings` record.
- **Outcome and verdict are different questions.** Whether the review ran, and
  what it concluded. `findings-dispositioned` with a `revise` verdict is a
  blocked artifact; recording only the outcome makes it read as finished.
- **The two fields constrain each other.** `blocked` takes `not-run` and nothing
  else — there is no verdict to have. Every other outcome takes `approve` or
  `revise` and never `not-run`, or an artifact that was reviewed can be recorded
  as though it never was. Neither combination is a formatting detail: each is a
  way to leave the record looking complete while the checkpoint did not happen.
- **Requested and confirmed are separate fields, for model *and* effort**,
  because a silent fallback to the author's own model — or to a cheaper effort
  level — is otherwise invisible. The reviewer's own account cannot settle it,
  since a fallback reads the same prompt.
- **Every finding has exactly one disposition.** Silence is not one, and
  "deferred" without a carrier is a rejection in disguise.
- **A rejected finding the reviewer does not withdraw is not closed.** It is an
  unresolved disagreement, and it goes to a named human.
- **The revision is exact, including for a plan.** "Reviewed the branch" is not a
  reviewed revision; branches move. A plan in the repository needs its path *and*
  a commit or blob id — a sha alone does not say which file, a path alone moves
  under you. A plan that lived only in a conversation needs a digest and a
  session id, or the checkpoint has no subject anybody can produce later.
- **A record retrofitted to a schema newer than the review says so, and leaves
  what it cannot honestly reconstruct marked as not recorded.** A verdict
  reconstructed by the author is the author speaking for the reviewer, and a
  digest computed after the fact attests to nothing. Not recorded is a real
  finding about the record; back-filling it manufactures the evidence the record
  exists to be.
