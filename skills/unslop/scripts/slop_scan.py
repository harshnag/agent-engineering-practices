#!/usr/bin/env python3
"""Scan prose for AI-writing tells and report weighted density.

Usage:
  python slop_scan.py FILE [FILE ...]
  cat draft.md | python slop_scan.py
  python slop_scan.py draft.md --json
  python slop_scan.py draft.md --max 8      # exit 1 if weighted density > 8 per 1k words
  python slop_scan.py story.txt --fiction   # also check fiction slop lists

Code blocks, inline code, URLs, and front matter are ignored. Results are evidence
for a human-quality review, not proof of AI authorship.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass, field

WEIGHTS = {1: 3.0, 2: 1.5, 3: 0.5}

def words(*items: str) -> str:
    return r"\b(?:" + "|".join(items) + r")\b"

# (id, tier, description, regex, flags)
RULES: list[tuple[str, int, str, str, int]] = [
    # Tier 1
    ("not-x-but-y", 1, "Not X but Y / not just X but Y",
     r"\bnot\s+(?:just|only|merely|simply|about)\b[^.!?\n]{0,80}?\bbut\b", re.I),
    ("its-not-x-its-y", 1, "It's not X, it's Y (incl. split across sentences)",
     r"\b(?:is|are|was|were|it's|that's)(?: not|n't)\s+(?:just |only |merely |simply |about )?[^.!?\n]{1,60}?[.;,:\u2014\u2013-]+\s*(?:it|this|that|they|he|she|we|you)(?:'s| is| are|'re| was| were)\b", re.I),
    ("not-because", 1, "Not because X, but because Y",
     r"\bnot because\b[^.!?\n]{1,80}[.,;]?\s*(?:but\s+)?because\b", re.I),
    ("countdown", 1, "Countdown negation (Not X. Not Y. Z.)",
     r"(?:^|[.!?]\s+)Not (?:a |an |the )?[^.!?\n]{1,30}\.\s+Not (?:a |an |the )?[^.!?\n]{1,30}\.", 0),
    ("self-answered-q", 1, "Self-answered question (The result? X.)",
     r"(?:^|[.!?]\s+)(?:The|And the|But the|So the)\s+(?:\w+\s){0,3}\w+\?\s+[A-Z]", 0),
    ("chatbot-residue", 1, "Chatbot residue",
     words(r"great question", r"certainly!", r"of course!", r"absolutely!", r"I hope this helps",
           r"I hope this clarifies", r"let me know if", r"feel free to", r"don't hesitate to",
           r"would you like me to", r"happy to help", r"I'd be happy to", r"as an AI",
           r"as a large language model", r"you're absolutely right", r"is there anything else"), re.I),
    ("chat-artifact", 1, "Chat tool artifact",
     r"citeturn\d|\[oaicite:\d+\]|contentReference\[|utm_source=chatgpt\.com|\u3010\d+\u2020", 0),
    ("knowledge-hedge", 1, "Knowledge-limit hedge / guessed gap",
     words(r"as of my (?:last|latest) (?:update|training)", r"my knowledge cutoff", r"while specific details (?:are|remain) (?:limited|scarce)",
           r"not (?:widely|publicly|extensively) (?:documented|available|disclosed)", r"based on (?:the )?available information",
           r"maintains a low profile"), re.I),
    ("closer", 1, "Emphasis closer",
     words(r"let that sink in", r"read that again", r"full stop\.", r"that's the (?:real )?(?:win|point|lesson|secret)",
           r"and that's okay", r"make no mistake"), re.I),
    ("run-up", 1, "Staged run-up / false suspense",
     words(r"here's the (?:thing|kicker|catch|deal|truth|problem)", r"here's (?:what|why|where|how) (?:it gets|most people|you need|that matters|this matters)",
           r"let's (?:dive|delve|break (?:this|it) down|unpack|explore)", r"without further ado", r"the (?:uncomfortable |simple |hard )?truth is",
           r"the reality is", r"it turns out", r"let me be clear", r"real talk", r"buckle up"), re.I),
    ("significance", 1, "Inflated significance / legacy",
     words(r"(?:stands|serves) as a (?:testament|reminder)", r"a testament to", r"(?:pivotal|crucial|vital|key|significant) (?:moment|role|turning point)",
           r"marking a (?:pivotal|significant|new)", r"reflect(?:s|ing)? (?:a )?broader", r"(?:enduring|lasting) legacy", r"indelible mark",
           r"setting the stage for", r"(?:ever-)?evolving landscape", r"despite these challenges", r"the future looks bright",
           r"exciting times (?:lie )?ahead", r"paving the way for", r"deeply rooted"), re.I),
    ("ing-rider", 1, "Shallow -ing rider",
     r",\s+(?:thereby\s+|further\s+)?(?:highlighting|underscoring|emphasizing|showcasing|reflecting|symbolizing|cementing|solidifying|fostering|cultivating|contributing to|paving the way)\b", re.I),
    ("saying", 1, "Deep-sounding saying / invented label",
     words(r"at its core", r"the real question is", r"what really matters", r"the heart of the matter",
           r"is the (?:language|currency|architecture) of", r"\w+ (?:paradox|trap)\b"), re.I),
    ("strawman", 1, "Arguing with no one",
     words(r"I'm not saying", r"to be clear,", r"don't get me wrong", r"this is not to say", r"a tempting approach would be",
           r"one might be tempted", r"some might (?:say|argue)"), re.I),
    ("borrowed-authority", 1, "Vague attribution",
     words(r"experts (?:say|argue|believe|agree|note)", r"studies (?:show|suggest)", r"research (?:shows|suggests)", r"observers (?:have )?(?:noted|cited)",
           r"industry reports", r"(?:critics|many) (?:have )?(?:argued|noted|say)", r"active social media presence"), re.I),
    ("signpost", 1, "Signposted structure / recap",
     words(r"in conclusion", r"to sum up", r"in summary", r"in this (?:article|post|section|guide),? (?:we|I)(?:'ll| will)",
           r"as we(?:'ve| have) seen", r"key takeaways?"), re.I),
    # Tier 2
    ("dash", 2, "Em/en dash or spaced double hyphen", r"\u2014|(?<=\w)\s?\u2013\s?(?=[a-z])|\s--\s", 0),
    ("triad", 3, "X, Y, and Z triad", r"(?<!, )\b\w+(?: \w+)?, \w+(?: \w+)?,? and \w+\b", 0),
    ("false-range", 2, "From X to Y (false range)", r"\bfrom [a-z]+(?: [a-z]+)? to [a-z]+(?: [a-z]+)?(?:,| and)", re.I),
    ("copula-dodge", 2, "Avoiding is/has (serves as, boasts)", words(r"serves as", r"stands as", r"functions as", r"acts as a", r"boasts"), re.I),
    ("sales", 2, "Sales / brochure language",
     words(r"nestled", r"in the heart of", r"breathtaking", r"must-visit", r"rich (?:cultural )?(?:heritage|history|tapestry)", r"renowned",
           r"groundbreaking", r"world-class", r"unparalleled", r"game-changer", r"cutting-edge", r"unlock the (?:full )?(?:power|potential)",
           r"elevate your", r"take \w+ to the next level"), re.I),
    ("teacher", 2, "Teacher / pitch voice", words(r"think of it (?:as|like)", r"imagine a world", r"put simply", r"simply put", r"in simple terms"), re.I),
    ("candor", 2, "Performed candor", words(r"I'm going to be honest", r"since we're being honest", r"and yes, I", r"this (?:isn't|is not) a rant", r"I promise"), re.I),
    ("stakes", 2, "Stakes inflation",
     words(r"fundamentally (?:reshape|change|transform)", r"define the next era", r"something entirely new", r"change everything", r"revolutioni[sz]e"), re.I),
    ("listicle-prose", 2, "Listicle in a trench coat", r"(?m)^(?:The|My) (?:first|second|third|fourth|fifth) (?:\w+ )?(?:is|was|takeaway|lesson|reason|wall|step)\b", 0),
    ("bold-bullet", 2, "Bold-first bullet", r"(?m)^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]{1,60}\*\*\s*:?", 0),
    ("emoji-deco", 2, "Emoji/arrow decoration",
     r"[\u2192\u21d2\u2705\u2728\u274c\u26a1\u2b50]|[\U0001F300-\U0001FAFF]", 0),
    # Tier 3
    ("magic-adverb", 3, "Magic adverb",
     words(r"quietly", r"deeply", r"fundamentally", r"truly", r"genuinely", r"remarkably", r"incredibly", r"profoundly",
           r"seamlessly", r"effortlessly", r"inherently", r"arguably"), re.I),
    ("filler-transition", 3, "Filler transition",
     r"(?:^|[.!?]\s+)(?:Moreover|Furthermore|Additionally|Notably|Importantly|Interestingly|Crucially|Ultimately),|\bit(?:'s| is) worth noting\b|\bit bears mentioning\b", re.I | re.M),
    ("hedge-stack", 3, "Stacked hedges", words(r"could potentially", r"might potentially", r"may potentially", r"could arguably", r"might arguably", r"possibly could"), re.I),
    ("false-agency", 3, "False agency", words(r"the data (?:tells|shows) us", r"the (?:decision|answer|pattern) emerge[sd]", r"the market rewards", r"the culture shift(?:s|ed)"), re.I),
    ("vague-declarative", 3, "Vague declarative",
     words(r"the (?:implications|stakes|consequences) are (?:significant|high|real|profound)", r"the reasons are (?:structural|complex)"), re.I),
    ("curly-quote", 3, "Curly quotes", r"[\u201c\u201d\u2018\u2019]", 0),
]

VOCAB_A = [
    "delve", "delves", "delving", "tapestry", "testament", "underscores", "underscore", "underscoring", "pivotal",
    "intricate", "intricacies", "meticulous", "meticulously", "showcase", "showcases", "showcasing", "garner",
    "garnered", "bolster", "bolstered", "foster", "fosters", "fostering", "interplay", "realm", "multifaceted",
    "commendable", "noteworthy", "invaluable", "embark", "embarking", "beacon", "enduring", "vibrant", "bustling",
    "ever-evolving", "landscape", "navigate", "navigating", "unwavering", "profound", "resonate", "resonates",
    "elevate", "harness", "unleash", "seamless", "robust", "leverage", "leveraging", "streamline", "holistic",
    "paramount", "symphony", "mosaic", "cornerstone", "linchpin",
]
FICTION_WORDS = [
    "elara", "kael", "elias", "silas", "thorne", "lyra", "seraphina", "whispered", "murmured", "gaze", "flickered",
    "flickering", "shimmering", "etched", "crimson", "obsidian", "palpable", "unease", "newfound",
]
FICTION_PHRASES = [
    r"took a deep breath", r"voice (?:barely )?(?:above )?a whisper", r"voice barely audible", r"couldn't help but (?:feel|wonder|notice)",
    r"couldn't shake the feeling", r"(?:shiver|chill) (?:ran |run |down )", r"heart (?:pounding|hammered|hammering)",
    r"air was thick with", r"hung (?:heavy )?in the air", r"casting long shadows", r"dipped below the horizon",
    r"a mixture of", r"smile playing on", r"brow furrowed", r"breath (?:she|he|they) didn't know", r"something akin to",
    r"days turned into weeks", r"whatever challenges lay ahead", r"renewed sense of purpose", r"dust motes danced",
    r"mind rac(?:ed|ing)",
]


@dataclass
class Hit:
    rule: str
    tier: int
    desc: str
    line: int
    text: str


@dataclass
class Report:
    source: str
    words: int
    hits: list[Hit] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def clean(text: str) -> str:
    """Blank out code, URLs and front matter but keep line numbers stable."""
    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"\A---\n.*?\n---\n", blank, text, flags=re.S)
    text = re.sub(r"```.*?```|~~~.*?~~~", blank, text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", blank, text)
    # Link targets before bare URLs: a URL match that swallows the closing ")"
    # would otherwise let the link pattern run on and blank whole paragraphs.
    text = re.sub(r"\]\([^)\n]*\)", blank, text)
    text = re.sub(r"https?://[^\s)>\]]+|www\.[^\s)>\]]+", blank, text)
    comments = [m.span() for m in re.finditer(r"<!--.*?-->", text, flags=re.S)]
    def blank_code(m: re.Match) -> str:
        if any(s <= m.start() < e for s, e in comments):
            return m.group(0)
        return blank(m)
    # Indented code block: 4+ spaces after a blank line, outside HTML comments.
    text = re.sub(r"(?m)(?<=\n\n)(?:(?: {4}|\t).*(?:\n|$)|[ \t]*\n(?=(?: {4}|\t)))+", blank_code, text)
    return text


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def snippet(text: str, start: int, end: int) -> str:
    s = max(0, text.rfind("\n", 0, start) + 1)
    e = text.find("\n", end)
    e = len(text) if e == -1 else e
    line = text[s:e].strip()
    return line if len(line) <= 140 else line[:137] + "..."


def rhythm(text: str) -> dict:
    prose = "\n".join("" if re.match(r"\s*(?:#|[-*+]\s|\d+[.)]\s|\||>)", l) else l for l in text.splitlines())
    sents = [s for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.split()) >= 1]
    lens = [len(s.split()) for s in sents]
    paras = [p for p in re.split(r"\n\s*\n", prose) if p.strip()]
    one_line = sum(1 for p in paras if len(re.findall(r"[.!?](?:\s|$)", p.strip())) <= 1 and len(p.split()) < 20)
    out = {"sentences": len(lens), "paragraphs": len(paras)}
    if len(lens) >= 5:
        mean = statistics.mean(lens)
        sd = statistics.pstdev(lens)
        out.update(mean_sentence_words=round(mean, 1), sentence_length_cv=round(sd / mean, 2) if mean else 0)
    if paras:
        out["short_single_sentence_paragraph_ratio"] = round(one_line / len(paras), 2)
    return out


def scan(text: str, source: str, fiction: bool) -> Report:
    cleaned = clean(text.lstrip("\ufeff").replace("\r\n", "\n"))
    norm = cleaned.replace("\u2019", "'").replace("\u2018", "'")
    rep = Report(source=source, words=len(re.findall(r"[A-Za-z][A-Za-z'-]*", cleaned)))
    for rid, tier, desc, pattern, flags in RULES:
        target = cleaned if rid in ("curly-quote",) else norm
        for m in re.finditer(pattern, target, flags):
            if rid == "triad" and target[target.rfind("\n", 0, m.start()) + 1:].lstrip().startswith("|"):
                continue
            s = m.start() + len(m.group(0)) - len(m.group(0).lstrip(".!?\n\t "))
            rep.hits.append(Hit(rid, tier, desc, line_of(target, s), snippet(target, s, m.end())))
    vocab_re = re.compile(words(*[re.escape(w) for w in VOCAB_A]), re.I)
    for m in vocab_re.finditer(norm):
        rep.hits.append(Hit("ai-vocab", 3, f"AI vocabulary: {m.group(0).lower()}", line_of(norm, m.start()), snippet(norm, m.start(), m.end())))
    if fiction:
        for m in re.finditer(words(*FICTION_WORDS), norm, re.I):
            rep.hits.append(Hit("fiction-word", 3, f"Fiction slop word: {m.group(0).lower()}", line_of(norm, m.start()), snippet(norm, m.start(), m.end())))
        for m in re.finditer(words(*FICTION_PHRASES), norm, re.I):
            rep.hits.append(Hit("fiction-phrase", 2, f"Fiction slop phrase: {m.group(0).lower()}", line_of(norm, m.start()), snippet(norm, m.start(), m.end())))
    rep.hits.sort(key=lambda h: (h.line, h.tier))
    rep.stats = rhythm(cleaned)
    return rep


def summarize(rep: Report) -> dict:
    by_rule: dict[str, dict] = {}
    for h in rep.hits:
        key = "ai-vocab" if h.rule == "ai-vocab" else h.rule
        d = by_rule.setdefault(key, {"tier": h.tier, "desc": h.desc if key != "ai-vocab" else "AI vocabulary", "count": 0})
        d["count"] += 1
    vocab = by_rule.get("ai-vocab")
    if vocab and rep.words and vocab["count"] / rep.words * 1000 >= 6:
        vocab["tier"] = 2  # a dense cluster is stronger evidence than scattered words
    weighted = sum(WEIGHTS[d["tier"]] * d["count"] for d in by_rule.values())
    density = weighted / rep.words * 1000 if rep.words else 0.0
    if density < 4:
        verdict = "clean"
    elif density < 10:
        verdict = "some tells: review flagged lines"
    elif density < 20:
        verdict = "sloppy: rewrite recommended"
    else:
        verdict = "heavy slop: rewrite"
    warnings = []
    cv = rep.stats.get("sentence_length_cv")
    if cv is not None and rep.stats.get("sentences", 0) >= 12 and cv < 0.35:
        warnings.append(f"flat rhythm: sentence-length CV {cv} (<0.35)")
    ratio = rep.stats.get("short_single_sentence_paragraph_ratio")
    if ratio is not None and rep.stats.get("paragraphs", 0) >= 6 and ratio > 0.4:
        warnings.append(f"fragmented: {int(ratio * 100)}% of paragraphs are one short sentence")
    return {"weighted": round(weighted, 1), "per_1k_words": round(density, 1), "verdict": verdict,
            "by_rule": dict(sorted(by_rule.items(), key=lambda kv: (kv[1]["tier"], -kv[1]["count"]))), "warnings": warnings}


def print_report(rep: Report, summ: dict, limit: int) -> None:
    print(f"== {rep.source}: {rep.words} words | weighted tells {summ['weighted']} | "
          f"{summ['per_1k_words']}/1k words | {summ['verdict']}")
    for w in summ["warnings"]:
        print(f"   ! {w}")
    if rep.stats:
        print("   rhythm: " + ", ".join(f"{k}={v}" for k, v in rep.stats.items()))
    if not rep.hits:
        return
    print("   counts: " + "; ".join(f"T{d['tier']} {k} x{d['count']}" for k, d in summ["by_rule"].items()))
    shown = 0
    for tier in (1, 2, 3):
        for h in (h for h in rep.hits if h.tier == tier):
            if shown >= limit:
                print(f"   ... {len(rep.hits) - shown} more (use --limit)")
                return
            print(f"   T{h.tier} L{h.line:<4} {h.desc}: {h.text}")
            shown += 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Scan prose for AI-writing tells.")
    ap.add_argument("files", nargs="*", help="files to scan (default: stdin)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--fiction", action="store_true", help="include fiction slop words/phrases")
    ap.add_argument("--limit", type=int, default=60, help="max hits to print per file")
    ap.add_argument("--max", type=float, default=None, help="exit 1 if any file exceeds this weighted density per 1k words")
    args = ap.parse_args()

    inputs: list[tuple[str, str]] = []
    if args.files:
        for f in args.files:
            with open(f, encoding="utf-8", errors="replace") as fh:
                inputs.append((f, fh.read()))
    else:
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        inputs.append(("<stdin>", sys.stdin.read()))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    failed = False
    results = []
    for name, text in inputs:
        rep = scan(text, name, args.fiction)
        summ = summarize(rep)
        if args.max is not None and summ["per_1k_words"] > args.max:
            failed = True
        if args.json:
            results.append({"source": name, "words": rep.words, **summ, "stats": rep.stats,
                            "hits": [h.__dict__ for h in rep.hits]})
        else:
            print_report(rep, summ, args.limit)
    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
