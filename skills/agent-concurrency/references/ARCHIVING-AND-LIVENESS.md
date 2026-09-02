# Archiving sessions and worktrees

Read `SKILL.md` first. This is the pre-destruction protocol for a session,
worktree, or branch.

## Liveness first

Never remove a checkout while its session is running. Check before destruction,
not after.

Recent file or commit activity is positive evidence of life. Silence and age are
not evidence of death. Probe the session directly; treat a response as live and
no response as unresolved.

An idle notification says a turn ended in the past. It is not an archive clock.

## Five independent questions

### 1. Uncommitted work

Inspect tracked, staged, and untracked changes. A missing or unreadable checkout
is an error, not a clean result. Do not pipe a fallible status command straight
into a counter; the pipe can turn failure into a reassuring zero.

### 2. Commits with no other carrier

Ask which commits are reachable from the branch and from no trunk or upstream
ref. Print the exact predicate used.

An ancestry difference after squash, rebase, cherry-pick, or recommit does not
prove the content is unlanded. Confirm touched paths by content and ask the forge
whether the branch tip belonged to a merged pull request.

### 3. Stashes

Stashes live in the repository's shared object store rather than in one
worktree. They survive checkout deletion and are easy to strand. Record their
creator and purpose; never drop one you did not create.

Prefer a named recovery branch. A stash addressed by stack position can move
between inspection and pop.

### 4. Local branches nobody named

Enumerate every local head, not only checked-out branches and remote refs. A
branch with no worktree and no upstream is invisible to both listings.

Classify unmerged work as in flight, landed under another identity, superseded,
or unreadable. Re-landing a superseded branch can restore errors later work
removed.

### 5. Running environments

Archiving a session does not stop its background processes. Use a report-only
census and the cooperative lifecycle protocol from `resource-safe-tooling`.
Ports, process names, and numeric ids cannot authorize destructive cleanup.

## Destructive step

Immediately before acting, re-run every predicate. Protect deletion with an
expected identity so the branch or session cannot change between inspection and
destruction.

Afterwards verify the intended object is absent. A missing path proves only that
the path is gone, not that its work was clean.

Where only the creator can archive a session, leave the complete dated
verification for that creator rather than pretending the action occurred.
