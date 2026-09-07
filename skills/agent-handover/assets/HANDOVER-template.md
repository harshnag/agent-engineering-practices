# Handover

Where this stopped, what is open, and what was not verified.

**Read [AGENTS.md](AGENTS.md) first**, then this, then the docs it names.

> **Do not trust this file over the docs.** It is one session's summary of where
> things stood when it stopped, and can omit constraints or lag behind the
> repository. The docs are reasoned and gated; this is a note. If they disagree,
> the docs are right and this is stale — fix it.

## Where things stand

Everything here rots, so each row says how to re-check it rather than asking you
to believe a figure somebody typed.

| | How to check |
|---|---|
| Branch | `git branch --show-current` |
| Recent work | `git log --oneline -12` |
| Unpushed | `git log --oneline origin/main..main` |
| Open pull requests | `gh pr list` |
| Working tree | `git status --short` |
| Who else is here | the session list, and `docs/open/` for claims |
| The gate | `<verify command>` must exit 0 — and see what it does *not* cover |

<!-- Then, in prose: what the last session was doing and why. Link the doc that
     carries the reasoning; do not restate it here. -->

## What is open

Open work lives in [`docs/open/`](docs/open/), one file per item, because it must
be claimable. **Read the states before picking anything** — only `open` is a
task, `blocked` is waiting on something that is not effort, and `refused` was
decided against and never becomes work.

<!-- Do not write a count here. It goes stale the first time anybody claims one.
     Point at the listing command instead. -->

## Who continues this

<!-- Completed work needs no successor. For a necessary continuation, name the
     unfinished scope, successor, ownership and where its work will appear —
     its own branch and working tree, landing through a pull request. Follow the
     project's admission and retirement rules; never remove a live session's
     tree. If no successor was created, SAY SO AND WHY. Silence reads as a
     successor that exists, and the project waits for an agent nobody made.
     For a context-related handoff, state the observed trigger, what recovery
     was attempted and what remains uncertain. Report occupancy with its source
     only if available and relevant; do not infer it from lifetime usage. -->

## What was not verified

Stated plainly, because a successor assumes anything unmentioned was done.

<!-- State the boundary, not the effort. Not "tested in a browser" but which
     browser, which widths, which environment, and what was never opened. Not
     "the gate passes" but what the gate does not reach — network fetches, data
     rebuilds, real rendering, migrations. Anything you were sandboxed or
     firewalled out of goes here, handed back explicitly. -->

## Delivery identity

<!-- If delivery was in scope, record the pull request and intended base,
     reviewed/gated head revision, merged revision, exact deployment run, and
     observed runtime build identity. Write "not observed" for an unknown
     boundary. A green branch does not prove the merged tree or deployment. -->

## Where the reasoning lives

Not here. <!-- Links only. If something is explained only in this file, it is in
the wrong place — move it into the doc it is about and link that. -->

## Keeping this file honest

- **Update it before you hand off, not after you are asked.** It is worth exactly
  as much as its last edit.
- **Anything load-bearing goes in a doc first**, and this file links to it.
- **Settle open questions while you still have the context to argue about them.**
  A question left here is one the next session answers with less of the reasoning
  than you had.
- **State what you did not verify.** The alternative is a successor assuming it
  was done — and with several agents reading this at once, the assumption is made
  in parallel.
