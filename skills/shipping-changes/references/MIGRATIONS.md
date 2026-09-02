# Migrations when merging deploys

Read `SKILL.md` first. This file carries the worked protocol and the failure
taxonomy for schema changes.

## Decide the compatibility sequence first

Classify the change before writing it:

| Change | Safe sequence |
|---|---|
| additive nullable field or isolated object | migrate, confirm, deploy readers/writers |
| new required field | add nullable/defaulted form, backfill, deploy use, enforce later |
| rename | add new, dual-write, backfill, switch reads, stop old writes, remove later |
| type or semantic change | add parallel representation and migrate through it |
| deletion | stop every reader and writer first, observe, then remove |

If old and new code cannot both run against the intermediate schema, one
automatic deployment cannot make the change safe.

## Pre-merge protocol

1. Identify the exact schema predicate the new code requires.
2. Ask production directly; do not infer it from a migration ledger.
3. Apply only the compatible expansion.
4. Re-read the schema and compare with the predicate.
5. Confirm the pull request head has not changed.
6. Merge with an expected-head guard.
7. Follow the exact deployment and read back running identity.

The migration and merge are a small distributed transaction. The schema
confirmation is valid for the reviewed head only while that head remains fixed.

## Migration ordering is a property

If files encode order in names, gate the property rather than one naming style:

- every migration has an ordering key;
- keys are unique;
- lexical order equals numeric order;
- the loader applies exactly that order.

A fixed-width numeric prefix is a common way to buy the property. The promise is
the order, not the width.

## State the unproved boundary

A loader test proves the sorted order applies to a test database. It does not
prove production received migrations in that order, especially when people can
apply them individually.

Production confirmation asks the schema the code meets. A partially populated
ledger can be worse than none: it answers in the expected format about only one
of several ways state changed.
