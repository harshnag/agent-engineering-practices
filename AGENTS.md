# Working on agent-engineering-practices

The working agreement for anybody — person or agent — who writes anything here.

**Almost nothing in this repository was learned here.** Every rule was extracted
from two private production codebases. That makes the provenance rule from
`project-agent-instructions` load-bearing: where a rule is inherited rather than
demonstrated here, this file says so. Do not let that soften it — **an inherited
rule is a rule somebody else already broke.**

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
- **`main` is protected, and work lands through a reviewed pull request.** No
  direct pushes and **no approving your own pull request**. An author cannot
  review their own work, and an agent asked to approve its own change should
  refuse and say why. See
  [`skills/agent-concurrency/references/AUTOMATING-REVIEW.md`](skills/agent-concurrency/references/AUTOMATING-REVIEW.md).
- **Anything that writes gets its own working tree.**
  `skills/agent-concurrency/` is the protocol.

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
reversal, checklists for one operation. Three skills have no reference file
because they have no such material.

Frontmatter must carry `name` (matching the directory), `description` (what it
does *and* when to use it — the only part loaded at startup, so it is what
decides whether the skill is ever activated), `license`, and `metadata`.

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

So count them yourself, and treat a disagreement as a failure:

    test "$(ls -d skills/*/ | wc -l)" -eq "$(ls skills/*/SKILL.md | wc -l)"

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
