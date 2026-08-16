# Automating review, without automating away the review

Read `SKILL.md` first for why the trunk is protected and why the author cannot be
the reviewer. This is the operational half: how to enforce it, and how each
mechanism fails quietly.

Everything here is subject to the rule the enforcement exists to serve:

> **A gate that cannot fail is decoration. A gate that silently approves is
> worse, because it looks like review.**

So each section ends with how to make that mechanism fail on purpose. If you have
not seen it refuse something, you have not installed it — you have installed the
appearance of it.

## 1. Protect the trunk, or none of the rest matters

Every other control here is advisory until direct pushes are impossible. On
GitHub, a ruleset or branch protection on the default branch:

    gh api -X POST repos/{owner}/{repo}/rulesets \
      -f name='protect main' -f target=branch -f enforcement=active \
      -F 'conditions[ref_name][include][]=~DEFAULT_BRANCH' \
      -F 'rules[][type]=deletion' \
      -F 'rules[][type]=non_fast_forward' \
      -F 'rules[][type]=pull_request'

The three that carry the weight:

| Rule | What it stops |
|---|---|
| `pull_request` | direct pushes to the trunk — the whole point |
| `non_fast_forward` | force-pushes rewriting history others have fetched |
| `deletion` | removing the branch |

Then, inside the `pull_request` rule, the parameters that decide whether review is
real: `required_approving_review_count` (at least 1),
`dismiss_stale_reviews_on_push` (an approval is of a diff, not of a branch), and
`require_last_push_approval` — which is the one that specifically closes the
self-approval loophole, because it stops the last pusher approving.

**Two things to know before relying on it.** Repository admins are frequently
exempt by default, so the person most likely to be driving an agent is the person
least protected by the rule — check `bypass_actors` and empty it. And on some
plans, protection of private repositories is limited; verify on the actual
repository rather than assuming.

**Make it fail:** from a clean clone, commit to the trunk and push. You must be
rejected. If you are not, you have configured nothing.

    git commit --allow-empty -m "should be refused" && git push origin main

## 2. Required status checks

Approval and correctness are different questions. A human approval says somebody
looked; a required check says the gate ran and passed on *this* commit.

Name the checks explicitly in the ruleset, and set
`strict_required_status_checks_policy` so a branch must be up to date with the
trunk before merging — otherwise two individually-green branches merge into a
broken trunk, which is the verification-across-a-mixture failure from `SKILL.md`
in a different costume.

**The characteristic silent failure** is a required check that is not running at
all. A renamed workflow, a job skipped by a path filter, or a check that was
never reported leaves the requirement satisfied by nothing — and a skipped job
frequently reports as success.

**Make it fail:** push a commit that breaks the thing the check guards, and watch
the merge refuse. Then confirm the *name* in the ruleset still matches the job's
name after any workflow rename.

## 3. CODEOWNERS, for routing rather than for rigour

`.github/CODEOWNERS` assigns reviewers automatically by path:

    /skills/                @org/practices-maintainers
    /scripts/               @org/platform
    *.md                    @org/docs

With `require_code_owner_reviews`, it becomes an approval requirement rather than
a suggestion.

Its value is that the right person is asked without anybody remembering to ask.
Its limit is that it routes; it does not make anybody read. **A team listed as an
owner with one member who approves everything is a routing table, not a review.**

**Make it fail:** open a pull request touching an owned path, approve it as a
non-owner only, and confirm the merge is still blocked.

## 4. Automated reviewers, including agents

An automated reviewer — a code-review action, a bot, or an agent session invoked
against the diff — is genuinely useful, and is the easiest of all of these to turn
into decoration.

Three rules make it worth having:

- **It must be able to reject.** If it only ever comments, it is a linter with
  opinions. Decide deliberately whether it blocks; do not discover the answer
  later.
- **It must not be the author.** An agent reviewing a branch it wrote in the same
  session is the author with a second prompt. Invoke it as a separate context
  that receives the diff and the repository — and *not* the author's reasoning,
  plan, or commit message as justification. Ask it to check claims, not to agree
  with them.
- **Its approval must not satisfy a human requirement.** Configure it so a bot
  approval does not count toward `required_approving_review_count`, or you have
  automated the tick rather than the review.

**The strongest use is adversarial rather than confirmatory.** Prompt it to
reproduce claimed verifications rather than to summarise the change. Ask it
specifically to re-run anything the author says was checked, and to treat commit
messages and pull request bodies as claims with an author rather than as context.

That instruction is not theoretical: in this repository's own history, a review
agent given it found a figure carried in from an origin project **that the origin
had already retracted** — inside the skill about verification, next to the rule
*a claim survives by being inherited*. No gate here checks prose, and no author
re-reads a line they did not write. See `checking-claims`.

**Make it fail:** give it a diff with a defect you planted, in a category you
expect it to cover. If it approves, you have measured its coverage, which is
worth knowing before you rely on it.

## 5. Merge queues, if changes land faster than checks run

A merge queue re-tests each change against the trunk as it will actually exist
when merged, serialising the landings. It closes the "two green branches, one red
trunk" window that strict status checks only narrow.

Worth it when contention is real; unnecessary when one change lands a day. **It
is not a review mechanism** and does not substitute for one.

## 6. What to automate last, or not at all

- **Auto-merge on approval** is fine. It moves the decision earlier rather than
  removing it — the approval is now also a merge authorisation, so say so.
- **Auto-approval of any kind** is the thing this document exists to argue
  against. An automation that approves when checks pass has redefined review as
  the checks, and the checks are what review exists to catch the gaps in.
- **A bypass path for "urgent" changes** should be a person's explicit, recorded
  decision. An automated exception is used far more than anybody intends, and
  hardest at the moment care matters most.

## A one-page setup, for a small repository

Enough to be real, cheap enough to be kept:

1. Ruleset on the default branch: pull request required, one approval, dismiss
   stale approvals on push, require last-push approval, block force-push and
   deletion, no admin bypass.
2. One required status check that actually runs the project's gate.
3. `CODEOWNERS`, once more than one person or team exists.
4. A review agent invoked adversarially on each pull request — non-blocking at
   first, and **not** counted as the approval.
5. Prove each of the first four can refuse, in order, before believing any of
   them.

Step 5 is the one that gets skipped, and it is the only one that turns the other
four from configuration into a gate.
