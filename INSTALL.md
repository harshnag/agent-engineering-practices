# Installing

Every agent below reads the same open [Agent Skills](https://agentskills.io/specification)
format, so you install once per machine and the rules are available everywhere.

**Nothing here runs code at install time.** A skill is Markdown plus, in one
case, two scripts you run deliberately.

---

## The one-liner

    gh skill install harshnag/agent-engineering-practices --all --scope user

That places the seven skills in `~/.copilot/skills/`, which **GitHub Copilot CLI
and Microsoft Scout both read**. Confirm:

    gh skill list

Requires a recent `gh` — `gh skill` is in preview, so if the command is not
found, update the CLI first:

    gh --version && gh extension upgrade --all

### Install one skill rather than all seven

Recommended for a first look. Start with the shortest and most broadly
applicable:

    gh skill install harshnag/agent-engineering-practices checking-claims

Add more by name at any time: `agent-concurrency`, `agent-handover`,
`measured-changes`, `external-data-claims`, `verify-in-the-real-thing`,
`project-agent-instructions`.

### Per-project instead of per-user

Drop `--scope user` to install into the current repository, so the rules travel
with the codebase and apply to everyone working in it:

    gh skill install harshnag/agent-engineering-practices --all

---

## Microsoft Scout

Scout discovers `SKILL.md` folders in `~/.copilot/skills/`, so **the one-liner
above is the installation** — there is no separate step.

Scout also reads `~/.copilot/m-skills/`, which syncs across your devices. To use
that instead:

    git clone https://github.com/harshnag/agent-engineering-practices /tmp/aep
    mkdir -p ~/.copilot/m-skills
    cp -R /tmp/aep/skills/* ~/.copilot/m-skills/

Then start a new Scout session and ask it to list the skills it can see.

> **Verify rather than assume.** Scout is not among `gh skill install`'s
> `--agent` targets, so installation relies on the shared directory rather than
> on explicit support. Confirm it loads for you before relying on it — which is
> `checking-claims` applied to this page.

## GitHub Copilot

**Copilot CLI** reads `~/.copilot/skills/`. The one-liner is all that is needed.

**Copilot coding agent and Copilot in the IDE** pick up repository-level
instructions, so the highest-leverage move is not installing skills at all — it
is putting an `AGENTS.md` in the repository. `project-agent-instructions` ships a
template:

    cp skills/project-agent-instructions/assets/AGENTS-template.md AGENTS.md

Fill in the bracketed sections and commit it. Every Copilot session in that
repository then starts from it.

## Claude Code

    gh skill install harshnag/agent-engineering-practices --all --agent claude-code

Or manually, into the personal skills directory:

    git clone https://github.com/harshnag/agent-engineering-practices /tmp/aep
    mkdir -p ~/.claude/skills
    cp -R /tmp/aep/skills/* ~/.claude/skills/

## Cursor, and other agents

`gh skill install` supports roughly 45 targets. List them:

    gh skill install --help

For anything not on that list, the format is a plain directory — copy
`skills/<name>/` into whatever location your agent reads, keeping the folder
structure intact. `SKILL.md` must stay at the root of its folder and its `name`
field must match the folder name.

---

## Confirming it actually works

Installation is not activation, and this is the step most people skip.

1. **Confirm the files are where you think.**

       ls ~/.copilot/skills/

2. **Start a fresh agent session** — skills are read at startup.

3. **Ask directly:** *"Which skills do you have available?"* The agent should
   name them. Only each skill's name and description are loaded at this point.

4. **Trigger one, and check it engaged.** Ask something the description covers,
   such as *"I need to add a check that catches a regression — how should I know
   it works?"* You should get the mechanism from `measured-changes`: watch it
   fail on the bug it guards before trusting it.

If nothing engages, the description is the thing to look at — it is the only part
loaded at startup, and therefore the only thing deciding whether a skill is ever
activated.

## Updating

    gh skill update --all

## Removing

Delete the folder:

    rm -rf ~/.copilot/skills/checking-claims

---

## Rolling this out to a team

A suggested order, cheapest first:

1. **One person installs `checking-claims` and uses it for a week.** It is short
   and it applies to everything.
2. **Add `AGENTS.md` to one repository**, from the template. This is the change
   with the largest effect, because it applies to every agent session in that
   codebase whether or not anybody installed anything.
3. **Add `agent-concurrency`** once more than one agent or engineer works in the
   same repository — it is the one whose absence causes damage rather than
   inefficiency.
4. **Turn on branch protection**, using
   `skills/agent-concurrency/references/AUTOMATING-REVIEW.md`. Prove each control
   can refuse before believing it.

Skills are per-user, so adoption does not need to be all-or-nothing, and nothing
here changes anyone's workflow until they read a rule and choose to apply it.
