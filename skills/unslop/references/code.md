# Code slop

AI-written code usually reads well and passes CI. Its failures are consistent across projects because the same model reaches for the same shapes, so you can catch them with a checklist. CodeRabbit's study of 470 repositories found about 1.7x more issues in AI-assisted PRs. Veracode found security flaws in roughly 45% of AI-generated samples.

Use this when writing code (prevention) and when reviewing a diff (detection). Always compare against the base branch and the conventions of the surrounding files.

## P1: fix before merge

1. Blanket error handling. `except Exception: pass`, `catch (e) {}`, or catch-log-continue around code whose failure should stop the program. Ask what failure is being swallowed and whether execution should really continue. Catch the specific error, or let it propagate.
2. Race blindness. A read-modify-write on shared state with no transaction, lock, or atomic operation (`x = get(); x += 1; save(x)`). Ask what happens if two of these run in the same millisecond.
3. Hallucinated APIs. Methods, parameters, config keys, or CLI flags that sound right but don't exist, or that the library silently ignores. Check each unfamiliar call against the real docs or source.
4. Plausible but wrong security checks. `or` where the rule needs `and`, checking the wrong field, trusting a client-supplied value, auth that is missing on one route. Read each check slowly against the intended rule.
5. Fake tests. Tests that mock the unit under test, assert that a mock returns what it was told to, assert only "no exception", or snapshot garbage. Ask what real bug would make this test fail. If none would, the test is decoration.
6. Silenced type checking. `as any`, `# type: ignore`, `@ts-ignore`, `!` non-null assertions, or `unsafe` casts added to make errors go away. Fix the type instead.

## P2: fix before it spreads

7. Over-abstraction. An interface, factory, strategy, or base class with exactly one implementation. A wrapper that only forwards calls. Inline it until a second use exists.
8. Config cargo cult. Constants promoted to env vars, flags, or settings that will never have a second value. Inline them.
9. Duplicate helpers. A new utility that already exists in the codebase under another name. Search before adding.
10. Defensive noise. Null checks, type checks, and try/catch on values already validated upstream or guaranteed by types. Validate at the boundary and trust inside it.
11. Scope creep. The diff adds retries, caching, logging wrappers, CLI flags, or refactors nobody asked for. Extra code has to justify itself.
12. Backward-compat shims nobody needs. Old names re-exported, deprecated paths kept "just in case" in a private codebase, `v2` or `_new` or `_enhanced` copies next to the original.
13. Pattern drift. Code in a different era or style from the file around it: sync calls in an async service, class components in a hooks codebase, a new error-handling style, a different logger.

## P3: clean up when you're in the file

14. Narrating comments. Comments that restate the next line, section banners on ten-line functions, and docstrings that repeat the signature. Keep only comments that explain why.
15. Change-log comments. `// Added X to fix Y`, `// Updated to use Z`, `// FIXED:`. History belongs in git.
16. Placeholder residue. `// ... rest of the code`, `# TODO: implement`, `pass  # placeholder`, stub functions that return a hardcoded value, or an "example" API key.
17. Verbose, hedged naming. `userDataResponseObject`, `handleProcessDataHelperFunction`, `isValidAndNotEmptyCheck`. Match the codebase's naming.
18. Emoji and chatter in output. Emoji in logs, CLI output, or commit messages. `print("✅ Done!")`. Friendly banners in library code.
19. Magic numbers. `timeout=37`, `sleep(1.5)`, `range(0, 256)` with no explanation. Name the constants that carry meaning.
20. Unrequested artifacts. New `SUMMARY.md`, `CHANGES.md`, or `IMPLEMENTATION_NOTES.md` files, example scripts, or demo tests the user didn't ask for.
21. Import clutter. Unused imports, imports inside functions for no reason, deprecated module paths. Let the linter handle this.
22. Over-logging. `logger.info` on every branch, and logging secrets or whole request bodies.

## Writing code without slop

- Read neighboring files first. Match their structure, error handling, naming, comment density, and test style.
- Make the smallest change that fully solves the request. Don't add unrequested features, flags, or abstractions.
- Search for an existing helper before writing one.
- Let errors surface unless there's a specific, handled recovery.
- Write tests that would fail if the behavior broke, with at least one edge case.
- Verify every API you're unsure of against docs or source before using it.
- Run the project's own linter, type checker, and tests.

## Review output format

When reviewing, list findings as `P1/P2/P3 | file:line | pattern | one-line fix`. Quote the offending snippet. Skip style nits the linter would catch.
