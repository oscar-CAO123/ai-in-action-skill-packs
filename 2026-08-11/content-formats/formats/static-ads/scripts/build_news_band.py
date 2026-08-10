#!/usr/bin/env python3
"""Lay the CANONICAL news-carousel band over the ripped collage plate. Free.

    python3 build_news_band.py construction

The band geometry is the news-carousel one: `band.py`, bottom 506px, your display typeface 200, justified flush
on both margins, one blue accent. Two departures, both the operator's call on 2026-08-06:

  * **lowercase**, via the additive `noir-lower` theme. Case is the only thing it changes.
  * **full bleed with the fade kept**, via `plate_full=True, plate_fade=True`. The plate runs the
    whole frame instead of stopping above a black band, and the carousel's bottom-up fade climbs
    the well from the bottom edge so the type still has something to sit on. The fade was dropped
    for one pass on 2026-08-06 and the copy became unreadable across the hi-vis; the operator called it
    back the same day.

Copy is the CONTRARIAN fill from basics.py, lowercased, because the band template line was
already used on the first pass of this card.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from band import render_card                                    # noqa: E402

ROOT = Path(__file__).parent
PLATES = ROOT / "collage-news"
OUT = ROOT / "out-news"

# Lowercase, and the CONTRARIAN fill rather than the band template, because the band line was
# already used on the first pass of this card. Copy is verbatim from basics.py, lowercased.
COPY = {
    "construction": ["aussie construction businesses: stop [[hiring more admin staff]].",
                     "you are scaling the problem."],
    "real-estate": ["aussie real estate agencies: stop [[hiring a bigger admin team]].",
                    "you are scaling the problem."],
    "hospitality": ["aussie hospitality businesses: stop [[doing more interviews]].",
                    "a bad hire still costs you a season."],
    "retail": ["aussie retailers: stop [[hiring more staff to grow]].",
               "you are scaling the problem."],
    "financial-services": ["aussie insurance brokers: stop [[spending another weekend on it]].",
                           "you have a brokerage to run."],
}


def build(key):
    p = PLATES / f"{key}.png"
    if not p.exists():
        sys.exit(f"no collage plate at {p}, run collage_news.py first")
    lines = COPY[key]
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{key}-band.png"
    fit = render_card(lines, dst, plate=p, theme="noir-lower", plate_full=True, plate_fade=True)
    print(f"{key:20} {fit}")
    print(f"  {dst}")


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["construction"]):
        build(k)
