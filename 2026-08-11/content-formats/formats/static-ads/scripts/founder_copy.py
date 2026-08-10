#!/usr/bin/env python3
"""The founder copy layer. Every word here is quoted, attributed and sourced.

    python3 founder_copy.py            # print every card's copy
    python3 founder_copy.py --check    # the gate, free

`proof/SKILL.md` governs this file absolutely: **real attributed words only.** Nothing here is
written by us and nothing here may be edited into something the founder did not say. The `--check`
gate refuses to pass a quote with no `source`, so an invented line cannot reach a card by accident.

The one thing we DO author is the frame around the quote: the kicker, the attribution line and the
CTA. Those are ours. The words between the quotation marks are not.
"""
import sys

BLUE_OPEN, BLUE_CLOSE = "[[", "]]"

FOUNDERS = {
    "simon": dict(
        name="a founder",
        role="Co-founder, the business",
        # Culture Kings is Simon's, verifiable, and the strongest credential house can point at.
        credential="Co-founded Culture Kings from a Gold Coast market stall. "
                   "Built it to a $600M exit on the New York Stock Exchange. "
                   "100% bootstrapped. No investors. No debt.",
        credential_source="projects/webinar-landing/copy/copy-deck.md:43",
    ),
    "emil": dict(
        name="Emil Juresic",
        role="Chairman, NGU Real Estate. Co-founder, the business",
        credential="Arrived in Australia at 16 with less than zero. "
                   "Now chairs a group doing $4B+ in annual sales across 16 offices, "
                   "with 500+ staff and $500M+ in developed property.",
        credential_source="the business/context/house-partners-context.md:334",
    ),
}

# Every quote carries the file and line it was read from. A quote with no source does not render.
QUOTES = {
    "lead-domino": dict(
        who="simon",
        text="The the role you place is the most important hire I've ever seen. "
             "It's the lead domino.",
        accent="the most important hire I've ever seen",
        source="the business/context/house-partners-context.md:349",
        public=False,
    ),
    "weeks-to-minutes": dict(
        who="emil",
        text="Within days of deploying AI agents, processes taking weeks now take minutes.",
        accent="processes taking weeks now take minutes",
        source="the business/context/house-partners-context.md:347",
        # Already on the website, so this is the safest line in the bank to put on paid media.
        public=True,
        public_at="yourdomain.example",
    ),
    "never-give-up": dict(
        who="emil",
        text="Never give up.",
        accent="Never give up",
        source="the business/context/house-partners-context.md:336",
        public=False,
    ),
    "teaching-learning": dict(
        who="emil",
        text="A successful business must be a continual teaching-learning environment.",
        accent="a continual teaching-learning environment",
        source="the business/context/house-partners-context.md:338",
        public=False,
    ),

    # ---- Simon, from the house's own VSL recording, approved by the operator 2026-08-07 ------------------
    # Transcribed twice, whisper small.en then medium.en, and both passes agree on the substance
    # of every line below. Full capture and the transcript at `proof/capture-simon-vsl.md`.
    # Source format is the file plus the timestamp, so any line can be replayed and checked.
    "two-weeks-ahead": dict(
        who="simon",
        text="If someone's two weeks ahead of you, they're two months ahead of you in AI time.",
        accent="two months ahead of you in AI time",
        source="simon-vsl-16x9.mp4 @ 0:32",
        public=False,
    ),
    "operational-layer": dict(
        who="simon",
        text="AI has to be the operational layer of your team.",
        accent="the operational layer",
        source="simon-vsl-16x9.mp4 @ 0:45",
        public=False,
    ),
    "completely-own": dict(
        who="simon",
        text="I truly believe you need someone on your team that's going to completely own this.",
        accent="completely own this",
        source="simon-vsl-16x9.mp4 @ 1:01",
        public=False,
    ),
    # The best-evidenced line in the whole bank. The welcome pack's Civil Plumbing NT placement
    # and Sarah Curran's own discovery call both record the $25M tender taking two weeks; Simon
    # puts the number on the after.
    "eight-seconds": dict(
        who="simon",
        text="The 25 million dollar quotes go from two weeks to, I kid you not, eight seconds.",
        accent="eight seconds",
        source="simon-vsl-16x9.mp4 @ 1:46",
        public=False,
        corroborated=("welcome-pack Civil Plumbing NT; "
                      "context/pain-wiki/companies/territory-water-solutions.md:43"),
    ),
    "biggest-hire": dict(
        who="simon",
        text="This is the biggest hire that you could do in 2026.",
        accent="the biggest hire",
        source="simon-vsl-16x9.mp4 @ 2:07",
        public=False,
    ),
    "candlelight": dict(
        who="simon",
        text="This is like the difference between going from candlelight to electricity.",
        accent="candlelight to electricity",
        source="simon-vsl-16x9.mp4 @ 2:12",
        public=False,
    ),
    "day-in-december": dict(
        who="simon",
        text="Something that takes a week to build now is going to be a day in December.",
        accent="a day in December",
        source="simon-vsl-16x9.mp4 @ 0:11",
        public=False,
    ),
}

# The house CTA across the whole founder strand. Ours, not theirs, so it sits outside the quote.
CTA = "Take the audit."


def attribution(q):
    f = FOUNDERS[q["who"]]
    return f"{f['name']}, {f['role']}."


def quoted(key):
    """The quote with its accent marked up, wrapped in real quotation marks."""
    q = QUOTES[key]
    text = q["text"]
    if q["accent"] and q["accent"] in text:
        text = text.replace(q["accent"], f"{BLUE_OPEN}{q['accent']}{BLUE_CLOSE}", 1)
    return f'"{text}"'


def statement_copy(key):
    """Format 10, the founder statement card. Type only, no image, no rights exposure."""
    return dict(head=quoted(key), sub=attribution(key and QUOTES[key]), cta=CTA)


def split_copy(key):
    """Format 25, the before / after split screen, both halves mid-sentence."""
    return dict(head=quoted(key), sub=attribution(QUOTES[key]), cta=CTA)


CARDS = [
    dict(id="FS-1", fmt="Founder statement", quote="lead-domino", build="statement"),
    dict(id="FS-2", fmt="Founder statement", quote="weeks-to-minutes", build="statement"),
    dict(id="FS-3", fmt="Split screen, mid-sentence", quote="lead-domino", build="split"),
]


def check():
    bad = []
    for key, q in QUOTES.items():
        if not q.get("source"):
            bad.append(f"{key}: NO SOURCE, refuses to render")
        if q["accent"] and q["accent"] not in q["text"]:
            bad.append(f"{key}: accent '{q['accent']}' is not in the quote")
        if "—" in q["text"] or "--" in q["text"]:
            bad.append(f"{key}: em dash in the quote")
        low = q["text"].lower()
        if "it's not" in low and ", it's" in low:
            bad.append(f"{key}: reads as the banned negation swap")
    for c in CARDS:
        if c["quote"] not in QUOTES:
            bad.append(f"{c['id']}: unknown quote {c['quote']}")
        if quoted(c["quote"]).count(BLUE_OPEN) > 1:
            bad.append(f"{c['id']}: more than one accent")
    for k, f in FOUNDERS.items():
        if not f.get("credential_source"):
            bad.append(f"{k}: credential has no source")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        problems = check()
        print("\n".join(f"  {p}" for p in problems) if problems else "clean")
        sys.exit(1 if problems else 0)
    for c in CARDS:
        q = QUOTES[c["quote"]]
        print(f"\n{c['id']}  {c['fmt']}")
        print(f"  {quoted(c['quote'])}")
        print(f"  {attribution(q)}")
        print(f"  {CTA}")
        print(f"  source: {q['source']}" + ("  PUBLIC" if q.get("public") else ""))
