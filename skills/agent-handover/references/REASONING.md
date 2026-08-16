# Why the handover rules are what they are

Read `SKILL.md` first. This carries the reasoning and the failures behind the
rules, which you do not need in order to follow them. It loads on demand, so it
is here rather than in the skill body.

## The handover was a message, and that was the failure

Both origin projects started by passing the handover session-to-session in a
kickoff prompt. Both moved it into the repository, and they got there by
different routes — which is the reason to believe the conclusion rather than
either argument.

One arrived at it from **droppability**: the handover was the most important
artefact in the project and the only one not written down. That project had
already recorded the identical failure about its own agent instructions, which
arrive injected into a session from a copy that can be stale by days.

The other arrived at it from **contention**. Once several agents could read the
repository at the same time, a list of open work inside the handover became a
file every one of them had to write. A paragraph in a handover cannot be claimed
by one agent; a file can.

Two independent routes to one answer is the strongest evidence a practice rule
gets, and it is worth noticing when it happens.

## Why the file must call itself unreliable

The temptation is to write a handover that is correct and keep it correct. That
fails in a specific way: the file accumulates authority, the successor reads it
instead of the docs, and the docs stop being read. A handover believed over the
reasoned documents is worse than none, because it is a single unreviewed summary
standing in front of everything that was gated.

So the disclaimer is not modesty. It is a load-bearing instruction that sets the
precedence order, and it has to live in the file because the file is what gets
read first.

One origin project states the reason alongside the rule: the handover is written
"by whoever had the least context left of anybody who worked on it". That is
structurally true of every handover ever written, which is why the disclaimer is
not a project-specific hedge.

## The successor question reversed three times

Who creates the next session, and what kind, is genuinely unsettled. The
reversals are recorded in the `agent-concurrency` skill, because the durable part
is a concurrency constraint rather than a handover one.

What belongs here is what the reversals imply about handover *text*:

> **A rule that has moved three times should be written down with its history,
> not with its current answer alone.**

An instruction stated flatly reads as settled and is obeyed after it stops being
true. The same instruction carrying its positions lets the next agent recognise a
fourth situation when it arrives, because it can see which constraint the
instruction was serving.

One concrete consequence: **if no successor was created, say so and say why.**
Silence reads as a successor that exists. In an origin project this was not
hypothetical — the documented way to create one produced a session that appeared
in the sidebar and never received its kickoff prompt, which looks exactly like a
successor that is thinking.

## Why "how to check" beats "what it is"

One origin project rewrote its *Where things stand* section into commands after a
stale count survived several sessions: the prose said how many items were open,
the directory said otherwise, and nothing in a diff showed the disagreement.

The general form is a rule from `measured-changes`:

> **A number in prose is a measurement with an expiry date.** A figure carrying
> the run it came from is a recorded observation and does not rot; a bare one
> reads as current forever.

## Why "what was not verified" is a heading and not a habit

The failure mode is not dishonesty, it is compression. A session that drove the
app in one browser at two widths writes "verified in the browser" — true, and
read as more than it says.

A heading does three things a habit does not:

1. **It is visible when missing.** An empty section is a question; an absent
   habit is nothing.
2. **It separates the boundary of what was checked from the effort spent**, which
   are constantly conflated.
3. **It gives a blocked agent somewhere to hand a check back to.** The default
   conclusion of a sandboxed agent is that the suite was sufficient — see the
   `verify-in-the-real-thing` skill for why that is nearly always wrong.

In one origin project this section runs to several hundred lines of a
six-hundred-line file. That ratio is not an accident: the parts of a handover
that admit something are the parts that cannot be reconstructed from the
repository.

## Why open questions must be settled before leaving

The asymmetry is the whole argument. The session holding the question has the
reasoning that raised it, the alternatives it already rejected, and the context
that makes one answer obviously wrong. None of that survives unless written, and
writing all of it costs more than answering the question.

So the cheap move is to settle it — and the expensive move *looks* cheap, because
its cost lands on somebody else.

Where it genuinely cannot be settled — it needs a person, an external dependency,
or a decision nobody has authority to make — the item file carries the
recommendation and the reasoning. An item that only names the question has moved
the cost without reducing it.

## Why finishing means pushing

The three reasons, in the order an origin project paid for them:

1. **Uncommitted work in a shared checkout belongs to whoever commits next.** Two
   sessions' work sat modified in one tree at once and neither could see the
   other. A commit lock stops the commit, which is the shot; it cannot stop the
   staging, which is the loaded gun.
2. **A commit is not automatically about one thing.** While committing exactly
   this rule, a staged deletion of a data file was swept into a commit whose
   message was about something else. It was caught by listing the commit's files
   and looking — not by any gate — and was free to fix only because nothing had
   been pushed. Prefer explicit paths over `git add -A` whenever the tree holds
   anything that is not yours.
3. **Push may be deploy.** Where the trunk is what the public gets, a commit
   sitting on a laptop is a fix nobody has.

The first two are concurrency failures, which is why this rule is not merely
tidiness. The `agent-concurrency` skill is the fuller treatment.
