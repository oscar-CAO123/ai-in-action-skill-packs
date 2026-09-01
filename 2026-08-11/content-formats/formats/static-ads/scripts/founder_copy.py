#!/usr/bin/env python3
"""The founder copy layer. Every word here is quoted, attributed and sourced.

    python3 founder_copy.py            # print every card's copy
    python3 founder_copy.py --check    # the gate, free

**Read this first.** This file came out of a working content engine, and the founder bank in it
held real people, their real credentials and their real recorded words, most of them marked
`public=False`. All of that was removed before publishing. What is left is the structure, the
gate, and placeholder entries in the right shape. Replace `FOUNDERS` and `QUOTES` with your own.

`proof/SKILL.md` governs this file absolutely: **real attributed words only.** Nothing here is
written by us and nothing here may be edited into something the founder did not say. The `--check`
gate refuses to pass a quote with no `source`, so an invented line cannot reach a card by accident.

The one thing we DO author is the frame around the quote: the kicker, the attribution line and the
CTA. Those are ours. The words between the quotation marks are not.

## The rule the `public` flag exists for

A founder saying something to you in a meeting has not agreed to it going on paid media. Mark a
quote `public=True` only when it is already published somewhere you can point at, and record where
in `public_at`. Everything else is `public=False`, which means it is usable internally and needs an
explicit sign-off before a stranger can see it. Getting this wrong is how a private remark ends up
in an ad, and it is the reason the bank that used to be in this file is not in it any more.
"""
import sys

BLUE_OPEN, BLUE_CLOSE = "[[", "]]"

# Replace with your own. `credential` is the one line that earns the quote its authority, and it
# needs a source like everything else. Keep it to something a stranger could verify.
FOUNDERS = {
    "founder-a": dict(
        name="<founder name>",
        role="<role, organisation>",
        credential="<one verifiable line: what they built, at what scale, over what period>",
        credential_source="<file:line, or the public URL it is published at>",),
    "founder-b": dict(
        name="<founder name>",
        role="<role, organisation>",
        credential="<one verifiable line>",
        credential_source="<file:line, or the public URL>",),
}

# Every quote carries the file and line it was read from. A quote with no source does not render.
# Source format for a recording is the file plus the timestamp, so any line can be replayed and
# checked by somebody who was not in the room.
QUOTES = {
    "placeholder-belief": dict(
        who="founder-a",
        text="<a sentence the founder actually said, transcribed, not tidied up>",
        # The accent must appear in the text verbatim, or the gate refuses the card.
        accent="transcribed, not tidied up",
        source="<file:line, or recording.mp4 @ 0:32>",
        public=False,),
    "placeholder-published": dict(
        who="founder-b",
        text="<a sentence already published somewhere you can point at>",
        accent="somewhere you can point at",
        source="<file:line>",
        # Already published, so this is the safest kind of line to put on paid media.
        public=True,
        public_at="<the URL it is already published at>",),
}

# The house CTA across the whole founder strand. Ours, not theirs, so it sits outside the quote.
CTA = "<your call to action>"


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
    return dict(head=quoted(key), sub=attribution(QUOTES[key]), cta=CTA)


def split_copy(key):
    """Format 25, the before / after split screen, both halves mid-sentence."""
    return dict(head=quoted(key), sub=attribution(QUOTES[key]), cta=CTA)


CARDS = [
    dict(id="FS-1", fmt="Founder statement", quote="placeholder-belief", build="statement"),
    dict(id="FS-2", fmt="Founder statement", quote="placeholder-published", build="statement"),
    dict(id="FS-3", fmt="Split screen, mid-sentence", quote="placeholder-belief", build="split"),
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
        if q.get("public") and not q.get("public_at"):
            bad.append(f"{key}: marked public with nowhere to point at")
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
