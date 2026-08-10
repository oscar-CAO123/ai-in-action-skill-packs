#!/usr/bin/env python3
"""The newspaper EXTRACT the clipping is cut from. ONE paid job at a time.

    python3 clip_paper.py                       # DRY RUN, prints the prompt, spends nothing
    python3 clip_paper.py construction --go     # ONE paid i2i job, ~2 credits

the operator, 2026-08-06: the synthetic ground in `clip.py` reads as blank paper with our headline
dropped on it. He wants the clipping to be an actual extract of a newspaper, with our line set
as the page's own headline and the rest of the page's text left alone but slightly blurred.

Method is the house i2i one: a REAL public-domain Library of Congress scan from `collage-src/`
goes in as the reference, and the prompt changes exactly one thing about it. That is the whole
design of the prompt, and the reason it is so insistent about it: this model rewrites a page
wholesale if you let it, and a rewritten page is a fabricated newspaper.

**The recorded deviation.** `layers/editorial-layer/SKILL.md` bans generated legible text
outright, because gibberish newsprint is the tell. the operator overrode that here on 2026-08-06 for
the headline specifically, which is the one line on the card that has to be read. Two guards
stay on: the rest of the page is asked for slightly out of focus so nothing else invites
reading, and the prompt bans a masthead, a publication name and a byline, so the output can
never read as a real outlet running a real story. That ban is the same one `plates_news.py`
carries, for the same reason.

Review the result before shipping it. The failure to look for is the model rewriting the whole
page in its own invented type rather than keeping the reference's columns.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_news_clip import COPY                                      # noqa: E402

ROOT = Path(__file__).parent
SRC = ROOT / "collage-src"
OUT = ROOT / "clip-paper"
HF = "/opt/homebrew/bin/higgsfield"

# One scan per card, so the five clippings are cut from five different pages.
REF = {
    "construction": "building-trade-contracto-01.jpg",
    "real-estate": "building-trade-contracto-02.jpg",
    "hospitality": "building-trade-contracto-03.jpg",
    "retail": "building-trade-contracto-04.jpg",
    "financial-services": "building-trade-contracto-01.jpg",
}

# Where the headline sits on the page, and it has been wrong twice.
#   Pass 1 set it across the FULL page width. The clipping bleeds off the right edge of the card
#   by design, so a headline that reaches the paper's right edge loses its last word off the
#   frame, and there is no compositing fix: those two edges are the same line.
#   Pass 2 kept the margin but ran the block three quarters of the way DOWN the page, so the
#   headline owned the cutting and the cutting owned the card.
# The cutting was then condensed, and the operator, 2026-08-06, with that room in front of him: the
# headline takes the whole of it, and every card takes the SAME structure the construction page
# came back with. That page put the headline down the left half as a tall stack of short lines
# with real columns beside it, and it is the structure of record. Only the size of the type
# changes between cards, so a long line sets smaller and a short one sets bigger.
MEASURE = (
    "The headline runs down the LEFT HALF of the page as a tall stack of short lines in large "
    "bold serif type. It starts at the very top of the page and the last line of it, together "
    "with the standfirst in much smaller type directly beneath, finishes by THREE FIFTHS of the "
    "way down the page. The type is sized so the stack fills that space: a long headline sets "
    "smaller and takes more lines, a short one sets larger. The RIGHT HALF of the page is "
    "ordinary narrow columns of small newspaper type from top to bottom, and the BOTTOM THIRD "
    "of the page is the same small columns running right across it. The headline never crosses "
    "into the right half, never runs below three fifths of the page height, and never comes "
    "near the right-hand edge of the page.")

# The construction page came back with the 'i' of "hiring" printed as a broken hybrid glyph.
# One malformed letter in the headline is the whole card, so it is now called out.
LETTERS = (
    "Every letter of the headline and the standfirst is a correctly formed, complete letterform "
    "in one consistent typeface. No letter is broken, doubled, merged with its neighbour or "
    "overprinted, and no stray marks sit on or beside any letter.")

KEEP = (
    "This is the same newspaper page as the reference image and nothing about it is redesigned. "
    "The paper is the same aged off-white newsprint with the same stains, the same fibre and the "
    "same fold marks. The columns are in the same places, at the same widths, with the same "
    "column rules between them. The ink is the same slightly broken black letterpress ink. It is "
    "photographed flat, filling the frame, with no border, no edge of the page and no background "
    "around it.")

BLUR = (
    "Every other line of type on the page is left exactly where the reference has it, unchanged "
    "in size and position, but rendered very slightly out of focus, as though the camera focused "
    "on the headline alone. The small type stays soft enough that a reader takes it in as columns "
    "of newsprint rather than stopping to read a word of it. The headline and its standfirst are "
    "the only sharp type on the page.")

# Pass 2 reproduced the reference's own nameplate, "The Washington Herald", beside our headline,
# which reads as a real outlet running our story. Naming what to delete beats banning a category.
BAN = (
    "The masthead, nameplate and newspaper title carried by the reference image are deleted and "
    "replaced by ordinary columns of type. There is no masthead, no newspaper name, no "
    "publication title, no date line, no page number, no byline, no journalist's name, no "
    "photograph, no illustration, no logo and no company name anywhere on the page. Nothing "
    "modern appears. No hand, no desk and no surface is visible.")

# One ink. the operator, 2026-08-06: the blue accent goes. A newspaper prints black, and a spot colour
# on one phrase is the thing that gives the page away as artwork.
INK = ("Every word on the page is printed in the same black newspaper ink, the headline and the "
       "standfirst included. No colour of any kind appears anywhere on the page.")


def prompt(key):
    head, deck = COPY[key]
    head = head.replace("[[", "").replace("]]", "")
    deck_plain = deck.replace("[[", "").replace("]]", "")
    return (
        f"A photograph of a printed newspaper page. {KEEP} "
        f"ONE thing about the page is different from the reference: its main headline. That "
        f"headline sits at the top of the page in large bold serif newspaper type, in "
        f"sentence case, set on two or three lines, and it reads exactly and only: "
        f"\"{head}\" Directly under it, separated by a thin horizontal rule, one standfirst line "
        f"in much smaller roman type reads exactly and only: \"{deck_plain}\" "
        f"The headline is exactly {len(head.split())} words long, in that order, and no word in "
        f"it is printed twice: it came back with \"admin admin\" on two runs of the real estate "
        f"page, so count the words. Every word of both is spelled exactly as given, with no "
        f"extra words, and the type is crisp and completely legible. "
        f"{LETTERS} {INK} {MEASURE} {BLUR} {BAN}")


def shoot(key):
    ref = SRC / REF[key]
    if not ref.exists():
        sys.exit(f"no reference scan at {ref}")
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{key}-news.png"
    if dst.exists():
        dst.replace(OUT / f"{key}-news.prev.png")
        print(f"kept the old extract at {key}-news.prev.png")
    cmd = [HF, "generate", "create", "nano_banana_pro", "--prompt", prompt(key),
           "--image-references", str(ref), "--aspect_ratio", "3:2", "--resolution", "2k",
           "--wait", "--wait-timeout", "8m", "--wait-interval", "5s", "--json"]
    print(f"firing ONE job: {key} newspaper extract")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "[" not in r.stdout:
        sys.exit(f"higgsfield failed (exit {r.returncode}):\n{r.stdout[:1500]}\n{r.stderr[:800]}")
    job = json.loads(r.stdout[r.stdout.index("["):])[0]
    url = job.get("result_url")
    if not url:
        sys.exit(f"no result_url:\n{json.dumps(job)[:1500]}")
    print(f"job {job.get('id')}")
    subprocess.run(["curl", "-sSL", "-o", str(dst), url], check=True)
    print(f"saved {dst}  ({dst.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    args = sys.argv[1:]
    go = "--go" in args
    picks = [a for a in args if not a.startswith("--")] or list(COPY)
    for k in picks:
        if k not in COPY:
            sys.exit(f"unknown card {k}. have: {list(COPY)}")
    if not go:
        for k in picks:
            print(f"\n===== {k} =====\nref: collage-src/{REF[k]}\n\n{prompt(k)}\n")
        print("DRY RUN. Nothing spent. Add --go to shoot, ONE at a time.")
    else:
        if len(picks) > 1:
            sys.exit("one paid job at a time. name a single card.")
        shoot(picks[0])
