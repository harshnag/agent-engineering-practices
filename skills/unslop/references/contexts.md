# Genre rules

The core patterns apply everywhere. These notes cover what changes by genre.

## Chat replies to a user

- Give the answer in the first sentence. Don't restate the question, praise it, or say what you are about to do.
- Match length to the question. Don't add headings to a short answer.
- Use bullets only for parallel items the reader will scan. Use prose for reasoning.
- Stop when you're done: no "I hope this helps", no "Would you like me to...", no summary.
- Say "I don't know" or "I couldn't verify X" plainly instead of padding.

## Commit messages

- Subject: imperative mood, about 50 characters and no more than 72, no trailing period, no emoji. "Fix race in credit update", not "Enhanced robustness of credit handling ✨".
- Body, only when needed: why the change was made and anything non-obvious. The diff already shows what changed.
- Don't list every file touched. Avoid "This commit...", "comprehensive", "robust", "various improvements", "enhance", and "streamline".
- Follow the repository's existing convention (Conventional Commits, ticket prefixes) when there is one.

## Pull request descriptions

- Open with one or two sentences on what changed and why, in plain words.
- Then cover only what a reviewer needs: how you tested it, risks, follow-ups, screenshots for UI changes.
- Skip boilerplate headings (Summary / Changes / Testing / Impact) on small PRs. Use a template only when the repo has one.
- No bold-label bullet walls, no emoji checklists, no "This PR introduces a comprehensive...", no restating the diff file by file.
- Mention anything you didn't do or couldn't verify.

## READMEs

- First line: what it is and who it's for, concretely. "CLI that converts HEIC photos to JPEG in bulk", not "A powerful, seamless solution for all your image needs 🚀".
- Put the install and a minimal usage example near the top.
- No emoji headings or "✨ Features" sections of bold-first bullets. Plain headings, short lists.
- Skip badges and "Why X?" marketing unless the project needs them.
- Leave out "Contributing" and "License" boilerplate beyond a line or two unless it matters.

## Code comments and docstrings

- Explain why, not what. `i += 1  # increment i` is slop.
- Don't narrate history ("Added to fix...", "Previously we..."). That belongs in the commit message.
- A docstring that repeats the function name adds nothing. Document contracts, units, edge cases, and side effects.
- No emoji in comments, logs, or CLI output unless the project already uses them.
- Match the density and tone of the surrounding code.

## Technical docs

- Describe current behavior. Put changes in changelogs and migration guides.
- Use concrete examples with real commands, real output, and real error strings.
- Use sentence-case headings. Use a heading only where a reader would navigate.
- Avoid "simply", "just", and "easily". They are false reassurance, and they insult the reader when the step fails.
- Don't add a "Conclusion" section to reference docs.

## Email and Slack

- Put the ask or the news in the first line. Context comes second.
- Keep it short, and write like you talk to this person.
- Keep normal greetings and sign-offs, since they predate chatbots. Drop "I hope this email finds you well" and "Please don't hesitate to reach out".
- One topic per message where possible.

## Social posts (LinkedIn, X, blogs)

- The engagement template is a strong tell: a hook line, then one-sentence paragraphs, then "Here's what I learned:", three to five bold lessons, and a closing question ("Agree?", "What do you think?").
- Write in real paragraphs. Give one specific story or number instead of a moral. Skip the question bait.
- No hashtag walls or emoji bullets.

## Essays and opinion

- Keep the writer's opinions, uncertainty, mixed feelings, humor, and asides. You may add a reaction where the writer would.
- Argue a point instead of surveying "both sides" by default.
- End when the argument ends. A last concrete image or implication beats a summary.

## Encyclopedic and reference writing

- Keep the tone neutral. State facts with their sources, and leave out significance claims unless a source makes them.
- No sections on "Legacy", "Challenges", or "Future outlook" unless sources cover them.
- Don't pad notability with media lists or social follower counts.
- If a detail isn't documented, leave it out. Don't guess ("likely", "presumably").

## Fiction

- Invented detail is the job here, so the fidelity rule doesn't apply. The pattern rules still do.
- Avoid the names, words, and phrases in `vocabulary.md` > Fiction slop.
- Show emotion through action and specifics. Don't have characters explain their feelings.
- Not every scene should end on a reflective line or a lesson. Leave some tension unresolved.
- Vary sentence rhythm with the pace of the scene. Avoid a triad of sensory details in every paragraph.
- Let dialogue be oblique. People interrupt each other, dodge, and misunderstand.
