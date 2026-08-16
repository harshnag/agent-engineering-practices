# Agent engineering practices

Portable working rules for AI coding agents, packaged as
[Agent Skills](https://agentskills.io/specification) — the open `SKILL.md`
format that GitHub Copilot, Microsoft Scout, Claude Code, Cursor and ~45 other
agents load on demand.

**These were not written as guidance. Each rule was paid for by a specific
production failure**, in two codebases that ran multiple agents against real
work for months. This repository is the extraction: the rules, generalised to
the mechanism underneath, so they transfer to any team.

## Install

    gh skill install harshnag/agent-engineering-practices --all --scope user

Every agent that reads `~/.copilot/skills/` picks them up automatically. Confirm
with `ls ~/.copilot/skills/` — you should see seven directories. If you have
installed any of them before, add `--force`, because `--all` aborts the batch
rather than skipping what is already there.

[INSTALL.md](INSTALL.md) covers Scout, Copilot CLI, Claude Code, Cursor, and
manual installation for anything else, and the four-step check that a skill has
actually *activated* rather than merely installed.

## The problem these address

An agent's failure mode is not bad code. It is **plausible** work — output that
passes review, passes the suite, and is wrong in a way nothing surfaces.

The pattern repeats across every rule here:

- A test harness that **cannot fail** reports a healthy spread, because its
  fixture was missing the thing being varied.
- A suite of interactive checks passes while a full-screen overlay swallows
  every click, because programmatic clicks do not hit-test.
- A category the ingest does not recognise silently becomes zero — which is
  byte-identical to a deliberate exclusion, and means the opposite.
- A confident claim about the build system that nobody ran a command to check,
  which produces no symptom until it produces a plan.

None of these are caught by working harder or reviewing more carefully. They are
caught by specific, checkable practices, which is what this repository is.

## The seven skills

| Skill | What it governs |
|---|---|
| [`checking-claims`](skills/checking-claims/) | Deciding whether a claim is true before acting on it — especially claims about your own tooling |
| [`measured-changes`](skills/measured-changes/) | Tuning anything whose effect is smaller than its noise, and building gates that can actually fail |
| [`verify-in-the-real-thing`](skills/verify-in-the-real-thing/) | Why a passing suite is not evidence the thing works |
| [`external-data-claims`](skills/external-data-claims/) | Consuming other people's data without inheriting their assumptions |
| [`agent-concurrency`](skills/agent-concurrency/) | Multiple agents on one repository: isolation, claiming work, and landing through review |
| [`agent-handover`](skills/agent-handover/) | Ending a session so the next one does not start from nothing |
| [`project-agent-instructions`](skills/project-agent-instructions/) | Writing the `AGENTS.md` that governs a repository |

## Three ideas that carry most of the value

**A gate that cannot fail is decoration.** The most expensive lesson here. If you
have not watched a check go red on the bug it guards, you have not written a
check — you have written something that looks like evidence. This applies to test
suites, to CI, and to AI code review alike.

**A claim about your own tooling needs evidence exactly as much as a claim about
the code.** Domain logic gets measured, because nobody trusts it without a test.
Tooling gets *reasoned about*, because it feels like the kind of thing you can
simply know. Nothing fails when you are wrong about it.

**The author cannot review their own work.** Every check an author would run is
one they already ran, in the vocabulary that produced the defect. This is why an
agent must never approve its own pull request, and why an automated reviewer that
has never rejected anything is decoration under the first rule.

## Why the skill format, and not a wiki page

Three properties that a document does not have:

1. **It loads itself.** Only each skill's name and description — roughly 100
   tokens — sit in context at startup. The full body loads when the agent decides
   the skill is relevant; supporting files load only if it needs them. Guidance
   nobody remembers to link is guidance that does not exist.
2. **It is one copy, versioned.** These same rules previously lived as documents
   copied between repositories, and the copies had **already diverged** — each
   having learned something the others had not, with nothing anywhere noticing.
   A skill has `gh skill update`.
3. **It is agent-agnostic.** One open specification, read by roughly 45 agents,
   so the practice does not have to be re-litigated per tool.

## Adoption

Start with one skill, not seven. `checking-claims` is the shortest and has the
widest application; `agent-concurrency` is the one to take first if more than one
agent or engineer touches a repository.

Then `project-agent-instructions` ships a template for the `AGENTS.md` that makes
the practice local to a codebase, and `agent-concurrency` ships runnable
enforcement:

- `scripts/pre-commit` — refuses a second agent committing in a working tree
  another agent holds, and tells it how to move its work safely.
- `scripts/open.ts` — derives what work is open from the files themselves, so
  there is no shared index for parallel agents to contend over.
- `references/AUTOMATING-REVIEW.md` — branch protection, required checks,
  CODEOWNERS and automated reviewers, each with how to prove it can refuse.

## Provenance and evidence

Each skill states its rule and records that it was extracted rather than
invented. **The originating codebases are private and are not named**, which
forces a discipline worth having on its own terms:

> **Ship the rules; link the evidence.**

A rule is portable. The failure that produced it is not. Restating a specific
project's domain detail in a repository that has neither would turn a recorded
observation into an unverifiable assertion — which is the exact failure
`checking-claims` is about. So the mechanism travels and the domain does not.

Where a skill does carry a story, it is because the mechanism is the transferable
part, and it is told without the subject matter.

## Contributing

[AGENTS.md](AGENTS.md) is the working agreement, including the house style, the
one gate this repository has, and what that gate does **not** check — which is
most of what makes a skill good.

MIT licensed. Corrections that come with a reproduction are especially welcome;
several rules here exist because somebody re-ran a command instead of re-reading
a claim.
