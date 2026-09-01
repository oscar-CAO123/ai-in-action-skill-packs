#!/usr/bin/env python3
"""Render house news carousels under the bottom-band law.

    python3 build2.py                 # every deck in decks2.py
    python3 build2.py con-03-v2       # one deck

Copy lives in decks2.py. Output goes to ./out2/<slug>/slide-NN.png at 1080x1350.

Every slide is one block of Anton in the bottom 1.5/4 of the frame, one size per slide,
white with a single blue accent, flush on both margins and filling the band. The tabloid
and splash directions are gone: the law removes the masthead, the standfirst, the grey
tier, the rules, the counter and the logo, which is everything the two differed on.
The renderer is shared with the statics, see skills/content-formats/formats/static-ads/scripts/band.py.
"""
import sys
from pathlib import Path

from decks2 import DECKS
from decks_pains import PAIN_DECKS

DECKS = DECKS + PAIN_DECKS

ROOT = Path(__file__).parent
BAND = ROOT.parent.parent / "static-ads" / "scripts"
sys.path.insert(0, str(BAND))

from band import render_card  # noqa: E402


if __name__ == "__main__":
    picked = [d for d in DECKS if not sys.argv[1:] or d["slug"] in sys.argv[1:]]
    if not picked:
        sys.exit(f"no deck matched. slugs: {[d['slug'] for d in DECKS]}")
    for deck in picked:
        out = ROOT / "out2" / deck["slug"]
        for i, copy in enumerate(deck["slides"], 1):
            report = render_card(copy, out / f"slide-{i:02d}.png")
            print(f"{deck['slug']} slide-{i:02d}  {report}")
    print("done")
