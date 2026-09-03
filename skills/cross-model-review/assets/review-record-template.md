# Cross-model review record

One block per review. Keep it where review already happens — normally the pull
request body — rather than in a file nobody opens.

---

**Artifact:** [plan | diff]
**Exact revision:** [commit sha, or PR head sha; for a diff reviewed before it is
committed, the staged tree id from `git write-tree` — that is the identifier that
names the whole reviewed tree. A patch digest identifies the change but not the
tree: the same patch on a different base produces a different result, so record
the base too if you use one. A path is not a revision and neither is a branch
name.]
**Committed as:** [sha, once it lands — confirm `git rev-parse <sha>^{tree}`
equals the reviewed tree id]
**Checkpoint:** [plan-before-implementation | diff-before-landing]
**Date:** [YYYY-MM-DD]

**Author:** [model] at [effort] effort
**Reviewer requested:** [model] at [effort] effort
**Reviewer confirmed by the runtime:** [model reported by the invocation itself,
or `unconfirmed` — do not copy the requested value here, and do not accept the
reviewer's own account of which model it is]
**Invocation:** [session or agent id, so the review can be found again]

**Outcome:** [`no-findings` | `findings-dispositioned` | `blocked`]
[If `blocked`: why, and which exit was taken — waited, escalated, or proceeded
unreviewed by an attributed decision.]

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
- **Requested and confirmed are separate fields** because a silent fallback to
  the author's own model is otherwise invisible — and the reviewer's own account
  of which model it is cannot settle it, since a fallback model reads the same
  prompt.
- **Every finding has exactly one disposition.** Silence is not one, and
  "deferred" without a carrier is a rejection in disguise.
- **The revision is exact.** "Reviewed the branch" is not a reviewed revision;
  branches move. A diff reviewed before commit still has an identity — record the
  staged tree id, then confirm the landed commit carries that same tree. A patch
  digest is weaker: it identifies the change, not the result, and the same patch
  on a different base is a different tree.
