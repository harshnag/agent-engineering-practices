# Pattern catalogue

Each entry lists what to watch for, why it reads as AI, the fix, and when to keep it. Tier 1 acts on one sighting. Tier 2 acts when repeated or clustered. Tier 3 only counts with company.

Several examples are adapted from blader/humanizer (MIT) and Wikipedia's "Signs of AI writing". The rest are original.

---

## A. Staging instead of stating (Tier 1)

### A1. Not X but Y (negative parallelism)

Watch for: not X but Y; not just / not only / not merely X, but (also) Y; it's not X, it's Y; X, not Y; X rather than Y used for drama; the split form ("This isn't about X. It's about Y."); the causal reveal ("not because X, but because Y"); the countdown ("Not X. Not Y. Just Z."); the clipped tail ("..., no guessing", "..., no fluff"); "stops being X and starts being Y".

Why: The negative half rebuts something nobody said, so the positive half feels bigger. It's the single most-cited AI tell. People used it before LLMs, but not in every paragraph.

Fix: State Y. If both halves carry information, keep both as plain statements.

Keep when: the reader actually believes X and needs correcting ("The file isn't corrupt; it's gzip-compressed, so `cat` shows garbage").

> Before: It's not just a tool, it's a mindset shift. Not because the tech is hard, but because habits are.
> After: Adopting it means changing habits more than learning the tool.

> Before: Not ten. Not fifty. Five hundred and twenty-three lint violations.
> After: The linter reported 523 violations.

### A2. One-line closers and dramatic fragments

Watch for: a standalone line that repeats the paragraph ("That's the real win."); "Let that sink in."; "Read that again."; "Full stop."; "Period."; rows of fragments ("No setup. No config. No friction."); spaced emphasis ("Every. Single. Day."); the same closer after each section.

Why: The line asks the reader to pause without adding anything. RLHF-tuned models write for skimmers: one thought per line, no state to hold.

Fix: Cut the closer. Merge fragments into one sentence with a claim.

Keep when: the short line adds a new fact.

> Before: Then the migration finished. Zero downtime. Zero data loss. Zero complaints. That's the power of planning.
> After: The migration finished without downtime or data loss.

### A3. Self-answered rhetorical questions

Watch for: "The result? X." "The catch? Y." "The worst part? Z." "Why does this matter? Because..." "So what does this mean for you?" "What if I told you..."

Why: The question exists only to make its own answer sound dramatic.

Fix: State the answer as a sentence.

> Before: The result? A 40% drop in latency.
> After: Latency dropped 40%.

### A4. Staged run-ups and false suspense

Watch for: Here's the thing; Here's the kicker; Here's where it gets interesting; Here's what most people miss; Here's why that matters; Let's dive in; Let's break this down; Let's unpack this; Let's explore; Without further ado; The truth is; The reality is; The uncomfortable truth; It turns out; Let me be clear; Real talk; Honestly? / Look, as a standalone opener; "Buckle up".

Why: The writer announces a point instead of making it, or acts out candor before a routine claim.

Fix: Delete the run-up and start with the point. "Honestly" inside a casual sentence is normal. The tell is the standalone opener.

> Before: Here's the thing: most caching bugs aren't about caching. Let's break it down.
> After: Most caching bugs come from stale invalidation keys.

### A5. Deep-sounding sayings and invented concept labels

Watch for: at its core; the real question is; what really matters; the heart of the matter; X is the language/currency/architecture of Y; X becomes a trap; X is not a tool but a mirror; invented labels built from a domain word plus paradox, trap, creep, divide, vacuum, tax, or inversion ("the supervision paradox", "the context tax"), used as if they were established terms.

Why: An ordinary point dressed up as an aphorism or as a coined theory, skipping the argument.

Fix: Write the plain claim. If a label is worth coining, define it once and argue for it.

> Before: Trust is the currency of onboarding. Teams fall into the activation trap.
> After: New users stay when early steps work reliably. Teams often push features before that baseline holds.

### A6. Arguing with no one

Watch for: This isn't (mainly) about; I'm not saying; To be clear; Don't get me wrong; This is not to say; Some might argue... but; A tempting approach would be; You might think... but; It would be easy to just.

Why: Rebuttals to objections nobody raised, often left over from earlier drafts or from the model's own reasoning.

Fix: Remove the defense. If a real claim is inside it, state that claim.

Keep when: the objection is attributed or is one a reader would actually raise and the text answers it in full.

---

## B. Inflation and borrowed authority (Tier 1 unless noted)

### B1. Inflated significance, legacy, and broader trends

Watch for: stands/serves as a testament/reminder; a pivotal/crucial/vital/key moment/role; marking/shaping the; represents a shift; underscores/highlights its importance; reflects broader; enduring/lasting legacy; indelible mark; deeply rooted; setting the stage for; evolving landscape; focal point; stock sections ("Challenges and Legacy", "Future Outlook"); "Despite these challenges, X continues to thrive"; send-offs ("The future looks bright", "Exciting times lie ahead", "a step in the right direction").

Why: Models attach importance to any detail, from etymology to population figures. Wikipedia editors flag this more than any other pattern.

Fix: Keep the fact and drop the halo. End on the last concrete fact. If the source states real plans, use them.

> Before: The institute was established in 1989, marking a pivotal moment in the evolution of regional statistics and reflecting a broader movement toward decentralization.
> After: The institute was established in 1989, as part of a wider decentralization of Spanish administration.

### B2. Shallow -ing riders

Watch for: a sentence-final participle phrase: highlighting, underscoring, emphasizing, showcasing, reflecting, symbolizing, ensuring, fostering, cultivating, contributing to, cementing, solidifying, paving the way for, encompassing.

Why: It bolts unsupported analysis onto a plain fact. RAG-enabled models even pin it on named sources that never said it ("Ebert highlighted its lasting influence").

Fix: Cut the rider, or make it a separate claim the source supports.

> Before: The logo uses blue and gold, symbolizing trust and excellence and reflecting the company's commitment to its customers.
> After: The logo is blue and gold.

### B3. Borrowed authority and notability padding

Watch for: experts argue; observers note; industry reports suggest; studies show; some critics; several publications (meaning two); cited/featured/profiled in [list of outlets]; independent coverage; trade publications; active social media presence; over N followers.

Fix: Name the source and what it said, or cut the claim. Never invent a source. Note that a missing citation on its own is not a tell, since most writing is unsourced.

### B4. Vague association

Watch for: associated with; in connection with; linked to; tied to; involved in, where the source gives a specific relationship.

Fix: Name the relationship (founded, chairs, funded, sued). If the source doesn't say, keep the vague wording rather than inventing a role.

### B5. Avoiding "is" and "has" (Tier 2)

Watch for: serves as; stands as; functions as; acts as; operates as; represents; marks; boasts; features; offers; maintains; refers to.

Fix: Use is, are, has.

> Before: Gallery 825 serves as the exhibition space and boasts over 3,000 square feet.
> After: Gallery 825 is the exhibition space. It has 3,000 square feet.

### B6. Sales and travel-brochure language (Tier 2)

Watch for: nestled; in the heart of; boasts; vibrant; rich (heritage, history, tapestry); breathtaking; stunning; must-visit; renowned; groundbreaking; diverse array; seamless; cutting-edge; world-class; unparalleled; elevate your; unlock the power of; game-changer.

Fix: Say what the thing is and does.

### B7. Stakes inflation and "the truth is simple" (Tier 2)

Watch for: "This will fundamentally reshape how we think about everything"; "will define the next era"; "something entirely new"; "History is unambiguous"; "The answer is simple"; "The real story is...", as a dismissal of everything said before.

Fix: Claim only what the evidence supports. If something is simple, show it simply instead of saying so.

---

## C. Rhythm by rule (Tier 2)

### C1. Em and en dashes as universal connectors

Rule: The final text uses no em dashes (—) or en dashes (–) as clause connectors, and no spaced ` -- ` either, unless the writer's sample uses them. In that case, match the sample's rate. Leave dashes in code, paths, URLs, and number ranges ("pages 10–12") alone.

Why: A dash lets the writer skip deciding how two clauses relate. Models use 20 in a piece where a person uses 2. One dash is weak evidence on its own. A text full of them is not.

Fix: Choose the real relation: period, comma, colon, parentheses, or a rebuilt sentence. Don't swap every dash for a semicolon, which is the same habit in different punctuation.

### C2. Forced triads, tricolon stacks, and false ranges

Watch for: lists of three adjectives or nouns ("fast, secure, and scalable"); three parallel examples followed by a lesson; back-to-back tricolons; four- and five-item versions; "from X to Y" where X and Y don't sit on a scale ("from startups to cultural transformation").

Fix: Check that each item adds a distinct idea. Develop the strongest one, use two, or vary the structure. Keep three when there really are three.

> Before: The event features keynotes, panels, and networking. Attendees can expect innovation, inspiration, and insight.
> After: The event has talks and panels, with time between sessions to meet people.

### C3. Repeated openings (anaphora)

Watch for: three or more sentences in a row that start with the same word or frame ("They assume... They assume..."; "She noted... She noted...").

Fix: Merge the sentences, change the subject, or lead with the action. Deliberate rhetorical repetition in a speech is fine.

### C4. Metronome rhythm

Watch for: consecutive sentences of similar length; every paragraph about the same size; every paragraph ending on a punchy short line; stacks of one-sentence paragraphs.

Fix: Vary sentence length on purpose. Let some paragraphs run long and some be two sentences. Let endings differ. The scanner reports a sentence-length variation figure, and a value under about 0.35 over a long text suggests a flat rhythm.

### C5. Stacked qualifiers (Tier 3)

Watch for: could potentially; might arguably; it's possible that it may; to some extent perhaps.

Fix: Keep one qualifier when the doubt is real. Ordinary hedges like "tends to" and "often" are normal human writing.

### C6. Hyphenated pairs everywhere (Tier 3)

Watch for: cross-functional, data-driven, high-quality, real-time, long-term, end-to-end, hyphenated in every position.

Fix: Hyphenate before a noun ("a high-quality report"). Drop the hyphen after it ("the report is high quality").

---

## D. Voice and stance (Tier 2 unless noted)

### D1. Teacher voice and patronizing analogies

Watch for: Think of it as...; It's like a...; Imagine a world where...; In simple terms; Put simply; Simply put; "Let's walk through..."

Fix: For expert readers, state the thing directly. Use an analogy only if it is clearer than the original concept, and only once.

### D2. Performed candor and false vulnerability

Watch for: "And yes, I'll admit..."; "I'm going to be honest"; "Since we're being honest"; "This isn't a rant; it's a diagnosis"; "I promise"; "And that's okay."

Why: Real vulnerability is specific and a bit uncomfortable. The AI version is polished and risk-free.

Fix: Delete it, or replace it with the specific admission.

### D3. False agency (Tier 3)

Watch for: inanimate things doing human actions. "The data tells us", "the decision emerged", "the culture shifted", "the market rewards", "a complaint becomes a fix", "the conversation moves toward".

Fix: Name who did it ("The team fixed it that week"). If no specific actor fits, "you" can work.

### D4. Narrator from a distance (Tier 3)

Watch for: "People tend to..."; "Nobody designed this"; "This is why..."; "This happens because...", used as lecturer framing.

Fix: Put the reader in the scene, or state the mechanism directly.

### D5. Passive voice and missing subjects (Tier 3)

Watch for: "Mistakes were made"; "It is believed that"; "No configuration needed."; "Results are preserved automatically."

Fix: Use active voice when the actor matters. Passive is fine when the actor really is unknown or irrelevant, as in "The server was patched in 2023."

### D6. Magic adverbs and filler transitions (Tier 3)

Watch for: quietly, deeply, fundamentally, truly, genuinely, remarkably, incredibly, profoundly, seamlessly, effortlessly; Moreover, Furthermore, Additionally, Notably, Importantly, Interestingly, Crucially, It's worth noting, It bears mentioning.

Fix: Cut the word and see whether anything was lost. Keep adverbs that carry meaning ("run it locally", "fails intermittently"). Stop-slop says to kill every adverb. Don't follow that blindly.

### D7. Vague declaratives (Tier 3)

Watch for: "The implications are significant." "The reasons are structural." "The stakes are high." "The consequences are real." "This is the deepest problem."

Fix: Name the implication, the reason, or the stake, or cut the sentence.

---

## E. Formatting by rule (Tier 2)

### E1. Bold-first bullets and scattered bold

Watch for: every bullet starts with **Label:**; bold on random phrases inside paragraphs; acronyms bolded together with their expansions.

Fix: Remove the decoration. If the labels carry no information of their own, turn the list into prose. Keep bold for one truly critical warning.

> Before:
> - **Performance:** Performance has been improved through optimization.
> - **Security:** Security has been enhanced with encryption.
> After: The update speeds up page loads and adds encryption at rest.

### E2. Listicle in a trench coat

Watch for: "The first... The second... The third..." paragraphs; "First takeaway... Second takeaway..."

Fix: If it's a list, use a real list. If it's an argument, connect the ideas with reasons instead of ordinals.

### E3. Decorative headings, emoji, arrows, and rules

Watch for: Title Case Headings; emoji before headings or bullets (🚀 ✨ 💡 ✅); arrows (→ ⇒) in prose; a horizontal rule between every section; an H1 that repeats the title; a heading followed by a sentence that restates it.

Fix: Use sentence case. Remove emoji and arrows ("->" in a technical flow is fine). Keep rules only between truly separate parts.

### E4. Curly quotes and Unicode decoration (Tier 3)

Watch for: “smart quotes” and ’ in plain-text, code, or markdown contexts where the writer types straight quotes; ellipsis characters (…); non-breaking oddities.

Fix: Use straight quotes where the target format does. Most word processors curl quotes automatically, so this is weak evidence on its own.

### E5. Over-structuring short content

Watch for: headings and bullets on a four-sentence answer; a table for two items; "## Summary" on a paragraph.

Fix: Use prose. Add structure only when the reader will scan or navigate.

---

## F. Composition (Tier 2)

### F1. Fractal summaries and signposting

Watch for: "In this article/section, we'll explore"; "As we've seen"; "In conclusion"; "To sum up"; "In summary"; "Key takeaways"; a closing paragraph that restates every point; section intros that preview and section outros that recap.

Fix: Delete the previews and recaps. A conclusion earns its place only if it adds a decision, a recommendation, or a consequence.

### F2. One-point dilution

Watch for: one thesis restated with new metaphors in every section; 3,000 words carrying 600 words of content.

Fix: Say it once, support it, and cut the restatements. Length should follow content.

### F3. Dead metaphor

Watch for: one metaphor (walls and doors, ecosystems, engines, journeys) used five or more times.

Fix: Use it once, then speak literally.

### F4. Historical analogy stacking

Watch for: rapid lists of famous companies or eras to build authority ("Apple didn't build Uber. Stripe didn't build Shopify..."; "the web, mobile, cloud, and now AI").

Fix: Keep one analogy that actually fits and explain why it fits, or cut them all.

### F5. "Despite its challenges..." formula

Watch for: praise, then "faces challenges such as...", then "Despite these challenges, [optimistic line]".

Fix: State the problems plainly and stop.

### F6. Content duplication

Watch for: a paragraph or section repeated word for word, or nearly so, in a long piece.

Fix: Delete the duplicate.

---

## G. Leftovers from chat and drafting (Tier 1)

### G1. Chatbot residue

Watch for: Great question!; Certainly!; Of course!; Absolutely!; You're absolutely right; I hope this helps; Let me know if you have any questions; Feel free to reach out; Would you like me to...; Want me to...?; Happy to help; Here is a [summary/overview] of...; "As an AI..."; stray tokens such as "citeturn0search0", "[oaicite:0]", "contentReference", and "utm_source=chatgpt.com".

Fix: Delete the wrapper and keep the content. Check the start and end of the text especially.

### G2. Knowledge-limit hedges and speculative gap-filling

Watch for: as of my last update; as of [date], for no reason; while specific details are limited; based on available information; not publicly available/documented; maintains a low profile; likely [grew up / studied / began]; it is believed that.

Fix: Say what the sources don't show, or remove the sentence. Never present a guess as fact.

### G3. Writing about the previous version

Watch for: docs or comments that describe what changed ("This replaces the old O(n²) loop", "Now uses X instead of Y", "Updated to...").

Fix: Describe current behavior. History belongs in changelogs, commit messages, and migration guides.

### G4. Placeholder and template residue

Watch for: [Your Name], [Insert X], "Lorem ipsum", "TODO: add details", leftover markdown fences around a plain answer, "Subject:" lines inside a message body.

Fix: Fill in the placeholder from the source, or ask the user.
