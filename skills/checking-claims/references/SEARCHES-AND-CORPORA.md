# Searches, corpora, and negative findings

Read `SKILL.md` first. This is the worked method for searches whose conclusion is
larger than their output.

## A negative result proves less than it reads

A search that finds nothing establishes:

- this pattern;
- in these paths;
- at this ref;
- under this tool's parsing and ignore rules;
- returned no match.

It does not establish that the concept, file, behavior, or evidence is absent.

Before saying "nowhere", "none", or "never":

1. Name the intended population.
2. Enumerate its denominator independently.
3. Use the least specific literal that can find a known instance.
4. Confirm a positive control in the same namespace.
5. Print the matches and classify them.
6. Narrow only after seeing what the wider search includes.

A count hides whether the pattern selected the wrong thing. Capture first,
count second.

## The namespace must be able to hold the answer

An identifier lookup can return `not found` because the identifier belongs to a
different store, lifecycle, or namespace. This is common with session ids,
project ids, branch names, run ids, and user-facing names.

Prove the lookup can find a known-live value of the same kind. If it cannot,
conclude nothing and fail closed.

Mutable names are not identity. If absence would cause creation, takeover,
destruction, or duplicate work, key the decision on a stable identifier or make
the next action ask rather than act.

## Use literal matching for literal claims

Search-as-verification fails in both directions:

- line wrapping or whitespace changes split a phrase and produce false absence;
- unescaped regular-expression syntax matches a near miss and produces false
  presence.

Use fixed-string matching when checking a quotation. Normalize whitespace when
formatting is irrelevant. Use a pattern only when the pattern itself is the
claim.

For "did this content land", compare the path or tree against the intended ref.
Searching an uncommitted working tree answers nothing about what was pushed.

## An index is a corpus claim

An index, manifest, or generated contents block may omit files or headings by
design. Searching only it proves absence from the index, not from the repository.

Ask:

- what generated the index;
- what it deliberately excludes;
- whether it is complete or size-limited;
- whether a vanished subject would also vanish from the index.

Two instruments are not independent if both share the layer that omits the
answer. Agreement then proves consistency, not corroboration.

## Read summaries for their omissions

Summary commands frequently omit categories, truncate rows, cap results, or
collapse states. A limit is not a total.

Prefer:

- pagination or explicit all-state filters;
- raw or detailed output for the decisive field;
- a self-contained final verdict on list-producing tools;
- the query and its bound printed beside the result.

A coherent truncated fragment is more dangerous than an error because it gives
the reader a complete-looking story.

## A probe can establish mechanism without establishing rate

One reproduction can prove that a mechanism exists. It says almost nothing about
how often it occurs.

State a mechanism with a verb and a frequency with a number. If one command
produced both, check which half its sample can support.

## A tool returning no text is not an empty source

Dynamic pages, binary artifacts, authentication boundaries, parser failures, and
one missing deep path can all produce empty extraction from a live source.

Separate:

- source unreachable;
- source reachable but unreadable by this tool;
- requested path absent;
- content searched and no match;
- source observed to contain nothing.

Record which state occurred. "Searched and could not find" must not collapse
them.

## Conditions travel with every finding

Attach scope while it is still obvious:

- corpus and exclusions;
- subject and ref;
- time window;
- positive control;
- method and parser;
- result limit;
- what the instrument cannot see.

The quotable sentence is what propagates, and retelling is where conditions
disappear. A precise number does not repair a wrong corpus; it makes the false
finding more persuasive.

## Diagnostic hints are claims too

A plausible cause printed beside a failure terminates the search. Emit a hint
only when the captured evidence matches the shape it diagnoses, and always print
the raw decisive signal.

Do not retry before preserving the first failure. A retry can replace the only
output that would have distinguished "no error" from "the error was captured
from the wrong place".

## Search after mechanism changes

When a workflow, command, or lifecycle is removed:

1. search for its exact actionable form;
2. classify instruction, history, example, and refusal separately;
3. remove or rewrite live instructions;
4. keep recorded history where it explains a reversal;
5. add a check for the obsolete instruction form when its return would be
   dangerous.

A sentence can remain grammatically true while its precondition is no longer
reachable. That is a check that silently stopped checking, expressed in prose.
