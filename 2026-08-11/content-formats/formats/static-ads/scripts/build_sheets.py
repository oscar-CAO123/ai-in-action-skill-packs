#!/usr/bin/env python3
"""Build the bedded paper sheets a Theme B carousel sets its information pages on. FREE.

    python3 build_sheets.py u3               # writes _paper-sheet-02..05.png
    python3 build_sheets.py u4 --slides 4    # writes _paper-sheet-u4-02..05.png
    python3 build_sheets.py u3 --amp 0.22    # try a different weight before committing

WHY THIS EXISTS. The sheets on disk were made by hand, one `apply_bed` call at a time, off a
one-liner in the session handover. That worked exactly once: when you asked for heavier
texture on there was no way to re-run them at a new setting, and no record of which
seed produced which page. This script is that record.

ONE SEED PER SLIDE. The whole point of a per-slide sheet is that five pages do not read as the
same page five times, so the seed is derived from the slide number and written into the file
name's position. Re-running with the same arguments reproduces the same sheets exactly.

THE SETTINGS ARE THE SHEET SETTINGS, NOT THE PLATE'S. `collage_bed_paper.AMPLITUDE` stays at
the 0.16 you locked for `u1b`, where the bed competes with a black oil figure. A blank page
has nothing to compete with, so it runs at `SHEET_AMPLITUDE` over `SHEET_LAYERS`. Editing those
two constants and re-running this is the whole tuning loop.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collage_bed_paper import apply_bed, SHEET_AMPLITUDE, SHEET_LAYERS  # noqa: E402
from paper_sheet import build_sheet, SHEET  # noqa: E402

PLATES = Path(__file__).parent.parent / "candidate" / "plates"

# The file-name shape each unit's build script looks for.
#
# U3 GOT ITS OWN PREFIX ON . It used to read the unprefixed `_paper-sheet-NN.png`,
# which is the same set U7 reads. Rebuilding those at the new sheet amplitude would silently
# re-texture U7, a unit that is already on the board and out of scope for this change. Every
# unit now owns its sheets, so tuning one carousel cannot move another.
UNITS = {
    "u3": "_paper-sheet-u3-{i:02d}.png",
    "u4": "_paper-sheet-u4-{i:02d}.png",
    "u7": "_paper-sheet-{i:02d}.png",
    # The static suite borrows the carousel's bed. you, : the paper background is
    # "the canonical one ... the composite paper with the newspapers", the same sheet the Mascot
    # Poster sets its information cards on. It owns its own file so tuning F8 cannot move U3.
    "f8": "_paper-sheet-f8-{i:02d}.png",
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or args[0] not in UNITS:
        sys.exit(f"usage: build_sheets.py <{'|'.join(UNITS)}> [--slides N] [--amp F]")
    unit = args[0]
    slides = int(_opt("--slides", 4))
    amp = float(_opt("--amp", SHEET_AMPLITUDE))

    if not SHEET.exists():
        build_sheet()
    print(f"{unit}: {slides} sheets at amplitude {amp}, {SHEET_LAYERS} layers")
    for i in range(2, 2 + slides):
        dest = PLATES / UNITS[unit].format(i=i)
        # Seed off the slide number so the arrangement is reproducible and distinct per page.
        apply_bed(SHEET, dest, amp=amp, seed=100 + i, n_layers=SHEET_LAYERS)
        print(f"  {dest.name}")


def _opt(flag, default):
    argv = sys.argv
    return argv[argv.index(flag) + 1] if flag in argv else default


if __name__ == "__main__":
    main()
