#!/usr/bin/env python3
"""Find annotation leader dots that land on nothing.

    python3 check_dots.py                 # every deck that has plates on disk
    python3 check_dots.py noir-pain-inbox # one deck

A dot is placed by hand against a painting the model has already made, so the failure mode is
a coordinate that points at bare void or at a crushed-black silhouette. Both read to a viewer as
a line to nowhere. This samples a box around each dot on the composited slide and flags any that
sits in flat darkness.

Two numbers matter. `mean` is how lit the area is; `sd` is how much is going on in it. Flat and
dark on both means there is nothing there to name. A dark subject against a lit background still
passes, because the sd picks up the edge.

Slides whose plate has not been generated yet are skipped, not failed.
"""
import statistics
import sys
from pathlib import Path

from PIL import Image

from decks_noir import NOIR_DECKS

ROOT = Path(__file__).parent
BOX = 30          # half-width of the sample box, in card pixels
DOT = 8           # skip this radius, it is the drawn dot itself
MEAN_FLOOR = 26   # below this the area is effectively black
SD_FLOOR = 16     # below this nothing is happening in it


def sample(im, dx, dy):
    px = [im.getpixel((x, y))
          for x in range(max(dx - BOX, 0), min(dx + BOX, im.width), 4)
          for y in range(max(dy - BOX, 0), min(dy + BOX, im.height), 4)
          if abs(x - dx) > DOT or abs(y - dy) > DOT]
    return statistics.mean(px), statistics.pstdev(px)


def main():
    only = set(sys.argv[1:])
    flagged = checked = skipped = 0
    for deck in NOIR_DECKS:
        if only and deck["slug"] not in only:
            continue
        plates = ROOT / "plates-noir" / deck["slug"]
        out = ROOT / "out-noir" / deck["slug"]
        for i, marks in enumerate(deck.get("annotations", []), 1):
            slide = out / f"slide-{i:02d}.png"
            if not (plates / f"slide-{i:02d}.png").exists() or not slide.exists():
                skipped += len(marks)
                continue
            im = Image.open(slide).convert("L")
            for label, _logo, dx, dy, _ax, _an in marks:
                checked += 1
                mean, sd = sample(im, dx, dy)
                if mean < MEAN_FLOOR and sd < SD_FLOOR:
                    flagged += 1
                    print(f"{deck['slug'][10:]:14s} s{i:02d}  {label[:26]:26s} "
                          f"({dx},{dy})  mean {mean:5.1f}  sd {sd:5.1f}  POINTS AT NOTHING")
    print(f"\nchecked {checked}, flagged {flagged}, skipped {skipped} (plate not generated yet)")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
