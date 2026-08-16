# Handover

Where this stopped, what is open, and what was not verified.

**Read [AGENTS.md](AGENTS.md) first**, then this, then the docs it names.

> **Do not trust this file over the docs.** It is one session's summary of where
> things stood when it stopped, written by whoever had the least context left of
> anybody who worked on it. The docs are reasoned and gated; this is a note. If
> they disagree, the docs are right and this is stale — fix it.

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

<!-- Name the successor, what kind it is, and where its work will appear — a
     branch, a pull request, the trunk. If no successor was created, SAY SO AND
     WHY. Silence reads as a successor that exists, and the project waits for an
     agent nobody made. -->

## What was not verified

Stated plainly, because a successor assumes anything unmentioned was done.

<!-- State the boundary, not the effort. Not "tested in a browser" but which
     browser, which widths, which environment, and what was never opened. Not
     "the gate passes" but what the gate does not reach — network fetches, data
     rebuilds, real rendering, migrations. Anything you were sandboxed or
     firewalled out of goes here, handed back explicitly. -->

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
