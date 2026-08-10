#!/usr/bin/env python3
"""The three candidate posters: geometry and type first, plates after.

    python3 build_candidate_posters.py            # renders layout with placeholder plates
    python3 build_candidate_posters.py --plates   # uses the real plates once they exist

Copy of record: BATCH-1-COPY.md U1 and U4. Spec of record: candidate-angles/POSTER-SPEC.md.
Everything here is free. The plates are the only paid part and they are generated one at a
time by hand, never from this script.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from poster import render_poster  # noqa: E402
from band import render_card  # noqa: E402

OUT = Path(__file__).parent.parent / "candidate"
PLATES = OUT / "plates"

# Two layouts, settled with the operator 2026-08-07 after the first proof.
#   band    plate bleeds the whole 1080x1350 frame, ALL type in the bottom well, faded up from
#           the foot so it carries white type. u1a only now: u4 became a carousel on
#           2026-08-07 and lives in build_u4.py.
#   poster  type above the figure and below it, plate in the middle third. u1b ONLY, because
#           the falling graduate is the one image that wants air above and below it.
BAND = [
    {
        "slug": "u1a-laptop",
        "unit": "U1a",
        "plate": "u1a-from-behind.png",
        # The figure came out on 2026-08-07. "Almost two in three" rested on a 63 per cent that
        # only ever appeared in press write-ups of the Anyway / KPMG / Microsoft study; the
        # primary report is not published and the write-ups contradict each other on the
        # remainder. the operator's call: drop the number, keep the shape, say "most".
        "lines": ["most young australians think ai is going to take their job,",
                  "but if you know how to use it properly, [[we want to hire you.]]"],
    },
]

POSTERS = [
    {
        "slug": "u1b-falling-graduate",
        "unit": "U1b",
        "ground": "plate",
        "plate": "u1b-falling-graduate-collage.png",
        "top": ["about to finish a comp sci degree",
                "and scared there is no job",
                "at the end of it?"],
        "bottom": ["if you know how to use ai properly,",
                   "[[we want to hire you.]]"],
    },
]


def main():
    use_plates = "--plates" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)

    for b in BAND:
        plate = PLATES / b["plate"]
        have = use_plates and plate.exists()
        png = OUT / f"{b['slug']}.png"
        fit = render_card(b["lines"], png, plate=plate if have else None,
                          theme="noir-lower", plate_full=have, plate_fade=have,
                          ground=b.get("ground", "dark"))
        print(f"{b['unit']:<5} {b['slug']:<24} {fit:<26} "
              f"{'real plate, bleed' if have else 'no plate'}")

    for p in POSTERS:
        plate = PLATES / p["plate"]
        have = use_plates and plate.exists()
        png = OUT / f"{p['slug']}.png"
        fit = render_poster(p["top"], p["bottom"], png, ground=p["ground"],
                            plate=plate if have else None)
        state = "real plate" if have else "placeholder"
        print(f"{p['unit']:<5} {p['slug']:<24} {fit:<16} {state}")


if __name__ == "__main__":
    main()
