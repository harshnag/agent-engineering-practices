/**
 * What is open, derived from the item files rather than from a list.
 *
 *     node scripts/open.ts [directory]      # default: docs/open
 *
 * ## Why this exists
 *
 * Open work is split into one file per item so that two agents claiming two
 * different items touch disjoint paths, and git merges them with nobody
 * arbitrating. That is right, and in the origin project it was undone
 * by the index that shipped alongside it: a table naming every item and its
 * state, which every claim had to edit.
 *
 * Measured over forty commits, that table was **the most written file in the
 * repository** — ahead of every document and every source file. The per-item
 * split had moved the contention rather than removing it, and put it back in
 * exactly the shape the protocol warns about: a file every agent writes.
 *
 * Worse, it was *mandated*. A test asserted that every item appeared in the
 * index, so an agent claiming an item could not avoid the shared file even if
 * it wanted to. The check was defending something real — an item nothing links
 * to is invisible — and it bought that by making discoverability somebody's job
 * to maintain.
 *
 * A directory listing already is an index. This prints it with the states
 * filled in, so nothing has to be kept in step and nothing can drift: the item
 * file is the only place its status lives, and claiming touches one path that
 * no other agent has any reason to touch.
 *
 * ## What this deliberately does not do
 *
 * It does not write anything. A generated file committed to the repository
 * would be a shared file again — every agent regenerating it on every claim —
 * with the added property of looking authoritative while being stale. The
 * output goes to stdout and nowhere else.
 *
 * ## If you gate anything, invert it
 *
 * Do not assert that the index names every item. Assert that the index names
 * *no* item, and that this listing shows all of them.
 */

import { readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const dir = resolve(process.argv[2] ?? 'docs/open');

interface Item {
  file: string;
  title: string;
  status: string;
  claimed: string | null;
  blockedOn: string | null;
}

const VALID_STATUSES = new Set(['open', 'claimed', 'blocked', 'refused']);

/** Read one item; malformed coordination data is not an empty/default state. */
function parse(file: string): Item {
  const body = readFileSync(join(dir, file), 'utf8');
  const line = (label: string) =>
    new RegExp(`^\\*\\*${label}:\\*\\*[ \\t]*(.*)$`, 'm').exec(body)?.[1]?.trim() ??
    null;
  const title = /^#\s+(.+)$/m.exec(body)?.[1]?.trim();
  const status = line('Status')?.toLowerCase();
  const claimed = line('Claimed');
  const blockedOn = line('Blocked on');

  if (!title) throw new Error(`${file}: missing '# ' title`);
  if (!status || !VALID_STATUSES.has(status)) {
    throw new Error(
      `${file}: Status must be open, claimed, blocked, or refused`,
    );
  }
  if (!claimed) throw new Error(`${file}: missing Claimed field`);
  if (status === 'claimed' && claimed === '—') {
    throw new Error(`${file}: claimed item has no owner and timestamp`);
  }
  if (status !== 'claimed' && claimed !== '—') {
    throw new Error(`${file}: only a claimed item may name a claimant`);
  }
  if (status === 'blocked' && !blockedOn) {
    throw new Error(`${file}: blocked item has no Blocked on field`);
  }

  return {
    file,
    title,
    status,
    claimed,
    blockedOn,
  };
}

export function items(): Item[] {
  let entries: string[];
  try {
    entries = readdirSync(dir);
  } catch (err) {
    // The documented default is `docs/open`, and the protocol says to create it
    // only when a second agent turns up — so "not there yet" is an ordinary
    // state, not an error worth a stack trace.
    if ((err as NodeJS.ErrnoException).code === 'ENOENT') return [];
    throw err;
  }

  return entries
    .filter((f) => f.endsWith('.md') && f !== 'README.md')
    .sort()
    .map(parse);
}

/** Sorted so the only state that is a task comes first. */
const RANK: Record<string, number> = {
  open: 0,
  claimed: 1,
  blocked: 2,
  refused: 3,
};

function main(): void {
  const all = items().sort(
    (a, b) => (RANK[a.status] ?? 9) - (RANK[b.status] ?? 9),
  );

  if (all.length === 0) {
    console.log(
      `LOCAL OPEN-WORK VERDICT: no items in ${dir}; this checkout only.`,
    );
    return;
  }

  const width = Math.max(...all.map((i) => i.title.length));
  const open = all.filter((i) => i.status === 'open');

  console.log();
  for (const item of all) {
    const label = item.status.toUpperCase().padEnd(8);
    console.log(`  ${label} ${item.title.padEnd(width)}  ${item.file}`);

    // The detail that decides whether a non-open item is yours to touch.
    if (item.status === 'claimed' && item.claimed && item.claimed !== '—') {
      console.log(`  ${''.padEnd(8)} └ claimed ${item.claimed}`);
    }
    if (item.status === 'blocked' && item.blockedOn) {
      console.log(`  ${''.padEnd(8)} └ blocked on ${item.blockedOn}`);
    }
  }

  console.log();
  console.log(
    `LOCAL OPEN-WORK VERDICT: ${open.length} of ${all.length} items in ${dir} ` +
      'are open; this checkout only, and only open is actionable.',
  );
}

try {
  main();
} catch (error) {
  const detail = error instanceof Error ? error.message : String(error);
  console.error(`LOCAL OPEN-WORK VERDICT: UNREADABLE in ${dir}; ${detail}`);
  process.exitCode = 1;
}
