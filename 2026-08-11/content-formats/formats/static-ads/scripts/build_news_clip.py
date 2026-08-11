#!/usr/bin/env python3
"""The five news-collage cards, re-set as a torn newspaper clipping instead of the band.

    python3 build_news_clip.py                 # all five
    python3 build_news_clip.py hospitality     # one

you, across several passes off the original `-band` cards:

  1. **The clipping's own type stops being a caption and becomes newsprint.** `clip.py` prints
     it on a torn piece of paper entering from the bottom right, rather than `band.py`'s
     white-on-black bottom band.
  2. **Two of the five change copy.** Construction, real estate and retail keep their lines.
     Hospitality moves to the `tribal-knowledge` declarative and financial services to the
     `admin` callout, both named off INVENTORY.html.
  3. **The arrow is gone.** An early pass pointed one at the subject off the paper's edge; once
     the top header carried its own hook, the arrow was redundant and cut.
  4. **A top your display typeface header carries the actual hook now.** "Breaking: [avatar] can finally stop
     [pain]", over a black top-down fade, with a small CTA line under it naming the industry's
     lead magnet. The newspaper clipping is the supporting prop, not the headline any more.
  5. **The pop-art sunglasses are replaced by a black censorship bar** over the eyes, found by
     colour off the actual plate rather than assumed.

Every line here, on both the header and the clipping, is a FILL of a named `basics.py` shape
against a `basics.py` pain, verbatim, in sentence case. Nothing is free-written.

  construction        headcount        contrarian
  real-estate         admin            contrarian
  retail              headcount        contrarian
  hospitality         tribal-knowledge declarative       <- changed
  financial-services  admin            callout           <- changed
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from clip import render_card                                       # noqa: E402
from basics import MAGNETS                                         # noqa: E402

ROOT = Path(__file__).parent
PLATES = ROOT / "collage-news"
OUT = ROOT / "out-news"

# (headline, deck) for the newspaper clipping itself. The headline carries the single blue
# accent when no paid extract exists yet and this HTML fallback is what renders.
COPY = {
    "construction": (
        "Aussie construction businesses: stop [[hiring more admin staff]].",
        "You are scaling the problem."),
    "real-estate": (
        "Aussie real estate agencies: stop [[hiring a bigger admin team]].",
        "You are scaling the problem."),
    "retail": (
        "Aussie retailers: stop [[hiring more staff to grow]].",
        "You are scaling the problem."),
    # hospitality/tribal-knowledge--declarative. This is the one shape whose accent sits in the
    # deck rather than the headline, and it is left where basics.py put it.
    "hospitality": (
        "Aussie hospitality businesses don't need to use AI.",
        "They need [[one person who owns it]]. That person stops you having to keep the "
        "playbook in one person's head."),
    # financial-services/admin--callout
    "financial-services": (
        "Aussie insurance brokers don't have to [[drown in paperwork]] anymore.",
        "One hire. That is the whole change."),
}

# (avatar, pain) for the new top header: "Breaking: {avatar} can finally stop {pain}." `avatar`
# is each pain's `who` from basics.py PAINS verbatim, already the correct noun per industry
# (language-rules.md: agencies for real estate, retailers, brokers, never a blind "businesses").
# `pain` is the gerund clause basics.py already carries for that exact pain: `wrong` (the wrong
# fix) for the three contrarian cards, since that is what their own clipping headline already
# says and the header should echo it; `ing`/the deck's own clause for the two that changed shape,
# since those two no longer run the contrarian template.
HEADER = {
    "construction": ("Aussie construction businesses", "hiring more admin staff"),
    "real-estate": ("Aussie real estate agencies", "hiring a bigger admin team"),
    "retail": ("Aussie retailers", "hiring more staff to grow"),
    "hospitality": ("Aussie hospitality businesses", "keeping the playbook in one person's head"),
    "financial-services": ("Aussie insurance brokers", "drowning in paperwork"),
}


def build(key):
    plate = PLATES / f"{key}.png"
    if not plate.exists:
        sys.exit(f"no collage plate at {plate}, run collage_news.py first")
    avatar, pain = HEADER[key]
    topline = f"Breaking: {avatar} can finally stop [[{pain}]]."
    cta = f"{MAGNETS[key]} ->"
    head, deck = COPY[key]
    dst = OUT / f"{key}-clip.png"
    print(f"{key:20} {render_card(topline, cta, head, deck, dst, plate)}")
    print(f"  {dst}")


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(COPY)):
        if k not in COPY:
            sys.exit(f"unknown card {k}. have: {list(COPY)}")
        build(k)
