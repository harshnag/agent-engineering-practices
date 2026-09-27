# Vocabulary and phrase lists

Words are the weakest signal because they drift with each model release. Treat them as evidence only in clusters: three or more from these lists in a short passage, or one word repeated across a document. A formal word outside these lists is not a tell.

Sources: excess-vocabulary studies of PubMed and arXiv abstracts (Kobak et al. 2024, "Delving into ChatGPT usage in academic writing through excess vocabulary"; Juzek & Ward 2024, "Why does ChatGPT 'delve' so much?"), Wikipedia's "Signs of AI writing", blader/humanizer, tropes.fyi, stop-slop, and the EQ-Bench / antislop-sampler over-representation lists (Apache-2.0).

## Tier A: high-signal words (the documented spike words)

delve, tapestry, testament, underscore (verb), pivotal, intricate / intricacies, meticulous / meticulously, showcase, garner, bolster, foster / fostering, interplay, realm, multifaceted, commendable, noteworthy, invaluable, embark, beacon, enduring, vibrant, bustling, nestled, ever-evolving, landscape (abstract), navigate (figurative), unwavering, profound, resonate, elevate, harness, unleash, unlock (figurative), seamless / seamlessly, robust (figurative), leverage (verb), streamline, holistic, paramount, symphony (figurative), mosaic (figurative), crucible, cornerstone, linchpin, game-changer, cutting-edge, groundbreaking

Keep technical senses: "robust estimator", "landscape orientation", "gated by a feature flag", "leverage ratio".

## Tier B: common in AI text, normal in human text

crucial, key (adjective), vital, essential, significant, valuable, enhance, ensure, align with, highlight (verb), emphasize, comprehensive, dynamic, innovative, transformative, empower, facilitate, utilize, optimize, insights, journey (figurative), ecosystem (figurative), framework (figurative), paradigm, synergy, nuanced, subtle, newfound, countless, myriad, plethora, a wide array of, a diverse range of

## Stock phrases

- in today's fast-paced / digital / ever-changing world
- in the realm of
- it's important to note / it's worth noting / it bears mentioning
- plays a crucial / pivotal / key role in
- a testament to
- stands as / serves as a reminder
- a rich tapestry of
- navigating the complexities of
- the ever-evolving landscape of
- at the end of the day
- when it comes to
- in a world where
- at its core
- not only ... but also
- whether you're a X or a Y
- dive into / deep dive / let's dive in
- unlock the full potential / unleash the power of
- take X to the next level
- a game-changer for
- a double-edged sword
- only time will tell
- the future looks bright

## Magic adverbs and filler transitions

quietly, deeply, fundamentally, truly, genuinely, remarkably, incredibly, profoundly, effortlessly, seamlessly, inherently, inevitably, ultimately, arguably, notably, importantly, interestingly, crucially, essentially, basically, literally, actually (as emphasis), simply (as emphasis), really (as emphasis)

Moreover, Furthermore, Additionally, In addition, That being said, With that in mind, On the other hand (with no first hand), In essence, Ultimately

## Business and tech jargon swaps

| Instead of | Try |
|---|---|
| leverage | use |
| utilize | use |
| facilitate | help, run, let |
| navigate (challenges) | handle, deal with |
| unpack | explain |
| lean into | accept, commit to |
| double down | commit further |
| circle back | return to |
| deep dive | close look, analysis |
| move the needle | change the result |
| actionable insights | findings you can act on (or name them) |
| best-in-class / world-class | name the comparison |
| robust (figurative) | reliable, tested, name the property |
| seamless | name what doesn't break |
| empower users to | let users |
| going forward / moving forward | from now on, or cut |

## Chat residue (delete on sight)

Great question; Certainly; Of course; Absolutely; Sure thing; I'd be happy to; Happy to help; I hope this helps; I hope this clarifies; Let me know if; Feel free to; Don't hesitate to; Would you like me to; Shall I; Want me to; Is there anything else; As an AI; As a large language model; I don't have personal opinions, but; Here's a [comprehensive] overview; You're absolutely right; Good catch

Stray artifacts: `citeturn0search0`, `[oaicite:N]`, `:contentReference[oaicite:N]{index=N}`, `utm_source=chatgpt.com`, `【N†source】`

## Fiction slop

Fiction has its own list. EQ-Bench's creative-writing slop analysis measured these as heavily over-represented in model output compared with human fiction.

Names: Elara, Kael, Elias, Silas, Thorne, Lyra, Seraphina, Aria, Evelyn, Amelia, Clara, Lila, Lena, Lily, Liam, Ethan, Samantha, Marcus, Jaxon, Zephyr, "a young woman named..."

Words: whispered, murmured, gaze, shadows, flicker(ed/ing), echo(ed/ing), shimmering, glow, faint, scent, etched, crimson, obsidian, towering, swirling, pulsed, unease, dread, anticipation, newfound, testament, unwavering, tapestry, symphony, palpable, visceral

Phrases:
- took a deep breath / taking a deep breath, steeling herself
- voice barely above a whisper / voice barely audible
- couldn't help but feel / wonder / notice
- couldn't shake the feeling that
- a shiver ran down her spine / sent a chill down
- heart pounding in her chest / heart hammered against his ribs
- the air was thick with (tension / the scent of)
- words hung in the air / silence hung heavy
- casting long shadows / the sun dipped below the horizon
- eyes wide with a mixture of fear and
- a smile playing on his lips / a grin spreading across her face
- brow furrowed in concentration
- let out a breath she didn't know she was holding
- something shifted / something akin to
- days turned into weeks
- ready to face whatever challenges lay ahead
- a renewed sense of purpose
- knew one thing for certain
- dust motes danced in the light
- mind racing with possibilities

Structural fiction tells: every scene ends on a reflective line or a lesson; characters explain their feelings in dialogue ("I feel betrayed because..."); triads of sensory detail in every paragraph; conflict resolved through a heartfelt conversation; villains who monologue their motive; the ending wraps up neatly with hope; "It was a reminder that..."
