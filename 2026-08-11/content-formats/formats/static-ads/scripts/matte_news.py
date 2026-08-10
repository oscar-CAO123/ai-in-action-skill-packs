#!/usr/bin/env python3
"""Cut the subject out with a local matting model. FREE, no generation.

    python3 matte_news.py construction retail

Replaces the paid chroma-green step. the operator, 2026-08-06: the i2i cut was costing a paid job per
industry AND failing about half the time. On a dense location it tints the scene green instead of
deleting it, which nothing downstream can key, and construction alone burned three jobs without
ever producing a usable plate.

`hyperframes remove-background` runs `u2net_human_seg` locally through CoreML in about two
seconds a frame and lifts the person straight off the original photograph. No green screen, no
paid job, no failure mode. It reads whichever plate already carries the pop-art sunglasses:
the cut plate if one exists, otherwise the site plate.

One known limit: the model segments PEOPLE. A box or a tray held away from the body can be
dropped. Check the matte before shipping a pose that depends on the prop.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from plates_news import SCENES                                        # noqa: E402

ROOT = Path(__file__).parent
CUT = ROOT / "cut-news"
PLATES = ROOT / "plates-news"


def matte(slug):
    src = CUT / f"{slug}.png"
    if not src.exists():
        src = PLATES / f"{slug}.raw.png"
    if not src.exists():
        sys.exit(f"no plate to matte for {slug}")
    dst = CUT / f"{slug}.matte.png"
    print(f"matting {slug} from {src.name}")
    r = subprocess.run(["npx", "--yes", "hyperframes@latest", "remove-background",
                        str(src), "-o", str(dst)], capture_output=True, text=True)
    if r.returncode != 0 or not dst.exists():
        sys.exit(f"remove-background failed for {slug}:\n{r.stderr[-1200:]}")
    print(f"  {dst.name}  ({dst.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    for s in (sys.argv[1:] or list(SCENES)):
        if s not in SCENES:
            sys.exit(f"unknown scene {s}. have: {list(SCENES)}")
        matte(s)
