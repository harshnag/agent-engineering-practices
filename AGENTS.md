# Working on agent-engineering-practices

The working agreement for anybody — person or agent — who writes anything here.

**Almost nothing in this repository was learned here.** Every skill except
`cross-model-review` was extracted from two private production codebases; that
one is an adopted protocol and its frontmatter says so. That makes the provenance
rule from `project-agent-instructions` load-bearing: where a rule is inherited
rather than demonstrated here, this file says so. Do not let that soften it —
**an inherited rule is a rule somebody else already broke.**

**Each skill's `metadata.provenance` is the authority on where it came from.** If
you add one that was neither extracted nor demonstrated here, say which it is
there and correct this paragraph and the README in the same change, rather than
letting one sentence keep speaking for the whole tree.

## Read yourself in, in this order

1. **[README.md](README.md)** — what this is and the rule that governs it.
2. **The skills**, which are the product. Start with
   `skills/checking-claims/SKILL.md` — it is short, and it is the one to read
   before believing anything about the tooling here, including your own claims
   about it. Read `skills/agent-concurrency/SKILL.md` before writing anything,
   because it governs how work lands.
3. `git log --oneline -20`. The commit messages carry the design reasoning and
   are longer than the diffs.

> This order departs from the one `project-agent-instructions` prescribes, which
> puts the handover first. That assumes a reader who already knows the project.
> Here the product *is* the repository and most readers arrive having installed a
> skill, so the README comes first. The exception is stated rather than taken
> silently, which is what the skill asks for when its order does not fit.

The specification budget is 5,000 tokens and 500 lines per `SKILL.md`, and every
skill is inside it. Nobody has measured what reading all of them costs in
practice. Re-derive rather than trusting a number in this file:

    for f in skills/*/SKILL.md; do echo "$(wc -l < "$f") lines  $(( $(wc -c < "$f") / 4 )) tokens  $f"; done

## The rules

- **Ship the rules; link the evidence.** Below. The rule this repository exists
  to demonstrate, and the one most easily broken while writing a skill about not
  breaking it.
- **A gate that cannot fail is decoration.** Mutation-test every check here
  before trusting a pass. See *The gate*.
- **Design first.** The reasoning goes in the commit message before the file goes
  in the tree. The diff already says what changed.
- **Docs are a deliverable**, and here the docs *are* the deliverable.
- **`main` is protected, and work lands through a pull request.** No direct
  pushes, no force-pushes, no branch deletion. **Never approve your own pull
  request** — an author cannot review their own work, and an agent asked to
  approve its own change should refuse and say why. See
  [`skills/agent-concurrency/references/AUTOMATING-REVIEW.md`](skills/agent-concurrency/references/AUTOMATING-REVIEW.md).

  **Stated precisely, because a gate must not be described as larger than it
  is:** the ruleset requires a pull request and blocks force-push and deletion,
  and all three were proved able to refuse. It currently requires **zero**
  approvals, because with one contributor a one-approval rule would block every
  merge — nobody can approve their own. So the review requirement above is
  presently a *rule*, not a *gate*. Raise `required_approving_review_count` to 1
  and turn on `require_last_push_approval` the moment a second person can
  review, and prove it refuses before believing it.
- **Anything that writes gets its own working tree.**
  `skills/agent-concurrency/` is the protocol.
- **Plans and diffs are critiqued by the other model in the pair.** Below, under
  *The review pair*. `skills/cross-model-review/` is the protocol; this file is
  where the pair is actually bound.

## Ship the rules; link the evidence

A rule is portable. The failure that produced it is not. Restating a specific
project's domain detail in a repository that has neither turns a recorded
observation into an unverifiable assertion — exactly what `checking-claims` is
about.

The house style, which is not negotiable because it is what the rule looks like
in practice:

- **The originating codebases are private and are never named**, in frontmatter
  or in prose. `metadata.provenance` records that a skill was extracted, and
  nothing more. **Never add a link into a private repository** — it leaks a name
  and resolves for nobody.
- **The body says *the origin project***, never a name.
- **No domain specifics, ever.** Not the subject matter, not the vocabulary, not
  the entity names. A rule that cannot be stated without them is not portable
  yet, and the fix is to find the mechanism underneath rather than to smuggle the
  domain across.
- **A story is carried only where the mechanism is the transferable part.**
  Figures are fine and worth keeping: *113 of 116 units in the worst band* is a
  recorded observation. Naming what the units were is somebody else's project.

This rule has failed three times, and **all three failures happened here**, which
is why this section is this long:

1. A session wrote four skills carrying the origin projects' names and subject
   matter throughout. A reader caught it; no check existed yet.
2. The check, once written, immediately failed on frontmatter recorded as a bare
   path rather than a URL. The fix was to make the data uniform, not to widen the
   pattern: **a check loosened to accommodate the data it just caught is a check
   that has been turned off.**
3. A generic sentence kept a list of examples that were all drawn from one
   project's subject matter — invisible to any string search, and caught only by
   a reviewer reading for it. **The grep catches names. It cannot catch a
   domain.**

## The shape of a skill

    skills/<name>/
      SKILL.md          rules — loaded in full on every activation
      references/       worked reasoning — loaded only when asked for
      scripts/          runnable
      assets/           templates

> **The trigger for moving something into `references/` is that it is not needed
> on every activation — not that the file is long.**

`SKILL.md` carries what an agent must know to *follow* the rule. `references/`
carries what it needs to *argue about* the rule — derivations, histories of
reversal, checklists for one operation. A skill needs no reference file when it
has no such material.

Frontmatter must carry `name` (matching the directory), `description` (what it
does *and* when to use it — the only part loaded at startup, so it is what
decides whether the skill is ever activated), `license`, and `metadata`.

## The review pair

Every implementation plan is critiqued before implementation starts, and every
diff is critiqued before it is committed or handed off, by the **other** model in
this fixed pair:

| Author | Reviewer |
|---|---|
| GPT-5.6 Sol, high effort | Claude Opus 5, high effort |
| Claude Opus 5, high effort | GPT-5.6 Sol, high effort |

`skills/cross-model-review/SKILL.md` is the protocol — substantive findings only,
an explicit disposition on every finding, no review-of-review, and materiality
judged by semantic effect. The bindings it requires a project to make are these:

- **Record location:** the pull request body — one authoritative location — using
  `skills/cross-model-review/assets/review-record-template.md`. Record the
  reviewer model and effort **as requested and as confirmed by the runtime**;
  they are different facts, a silent fallback to the author's own model is
  otherwise invisible, and the reviewer's own account of which model it is does
  not settle it.
- **Cycle bound:** two review cycles per artifact lineage — the plan is one
  lineage, the diff that implements it is another, and revising an artifact does
  not start a fresh count. **The second cycle is terminal for the pair:** a
  material change made in it, or a disagreement that survives it, goes to a
  human, not to a third model cycle and not out unreviewed.
- **Unavailable reviewer:** the review is `blocked`, and `blocked` is not
  permission to proceed. Wait, escalate, or record an attributed decision to ship
  unreviewed. **Never substitute the author's own model.**
- **A human author** is reviewed by Claude Opus 5, as is **a model outside the
  pair** — named rather than left to the author, because a reviewer chosen per
  change is a choice the author makes about their own work. **Mixed authorship**
  is reviewed by whichever member wrote none of it, and by a human if both
  contributed.
- **Absence of a record means unverified, not clean.**

**This is instruction-enforced. It is not a gate, and nothing in the repository
refuses when it is skipped** — which is exactly why the record is the only
evidence it happened. Do not describe it as a gate; the rule above about not
describing a gate as larger than it is applies hardest to the mechanism that has
no enforcement at all.

**Demonstrated here, not inherited.** The change that added
`skills/cross-model-review/` was itself authored by Claude Opus 5 and reviewed by
GPT-5.6 Sol at both checkpoints. **The full record — every finding and its
disposition — is in the body of the pull request that added it**, per the binding
above; the commit message carries the design reasoning, not the record, because
one authoritative location is the point. Two findings are worth naming here
because neither was in the diff: one caught this repository calling an unenforced
checkpoint a *gate*, and one caught the opening sentence of this file claiming
every rule here was extracted — a claim the change itself would have falsified.
**Both were in the framing rather than the code**, which is the class of defect a
second reader exists for.

**Neither direction of the pair has been calibrated with a planted defect**, so
its coverage is unmeasured. `skills/cross-model-review/references/RUNNING-THE-REVIEW.md`
has the procedure.

## The gate

    gh skill publish --dry-run .

It must pass before any commit. It checks names against the agentskills.io rules,
that each name matches its directory, that required frontmatter is present, that
`allowed-tools` is a string rather than an array, and that install metadata is
stripped. All five were confirmed able to fail, by mutation.

**It does not check anything else**, and one gap is severe enough to be a rule:

> **The gate cannot tell you a skill disappeared.** A directory with no
> `SKILL.md` is silently skipped. Runs over seven skills, six, and one produced
> **byte-identical output and exit 0** — same checksum — because nothing on a
> passing run names a skill or counts them.

So compare the tree with an independently maintained expected inventory:

    scripts/check-skill-inventory.sh

Unlike comparing the number of directories with the number of `SKILL.md` files,
this can detect deletion of a whole skill because the expected list does not
shrink with the tree. If a skill is intentionally added or removed, update the
script in the same change.

A second silent-skip case: a name containing a character outside the discovery
pattern is not reported at all — the skill simply drops out.

Also unchecked: prose, relative links, whether a script runs, and the evidence
rule above. **Everything that makes a skill good here is unchecked**, which is
why review is a requirement rather than a courtesy.

The scripts in `skills/agent-concurrency/scripts/` are not covered by the gate at
all. If you change them, run them.

## Setup

Nothing to install. `gh` must be recent enough to have `gh skill`, in preview:

    gh skill --help
