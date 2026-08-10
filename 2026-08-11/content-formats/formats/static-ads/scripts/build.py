#!/usr/bin/env python3
"""Render house single-image static ads (format F7).

    python3 build.py                      # every ad in ads.py
    python3 build.py s9-own-it            # one ad
    python3 build.py --lead               # headline-only cut, into out-lead/
    python3 build.py --out ~/Desktop/ads  # somewhere else

Copy lives in ads.py. Output goes to ./out/<slug>.png at 1080x1350 (4:5).
Type is laid in the composite by headless Chrome, never generated inside an image.

The card is one block of Anton in the bottom band, white with a single blue accent.
Every line is set at its own size so it runs the full safe width, and the number of lines
is chosen so the stack fills the band top to bottom. No second tier, no rules, no logo.
"""
import sys
from pathlib import Path

from ads import ADS
from band import render_card

ROOT = Path(__file__).parent

# The Build Breakdown statics (added 2026-08-06) live in ads_builds and render on this rig,
# so the list falls through to them rather than duplicating the renderer.
try:
    from ads_builds import BUILD_ADS

    ADS = list(ADS) + BUILD_ADS
except ImportError:
    pass


def render(a, out_dir, key):
    report = render_card(a[key], out_dir / f"{a['slug']}.png")
    print(f"{a['slug']:26} {report}")


if __name__ == "__main__":
    args = sys.argv[1:]
    key = "lead" if "--lead" in args else "lines"
    args = [x for x in args if x != "--lead"]
    out_dir = ROOT / ("out-lead" if key == "lead" else "out")
    if "--out" in args:
        i = args.index("--out")
        out_dir = Path(args[i + 1]).expanduser()
        args = args[:i] + args[i + 2:]
    out_dir.mkdir(parents=True, exist_ok=True)
    picked = [a for a in ADS if not args or a["slug"] in args]
    if not picked:
        sys.exit(f"no ad matched {args}. slugs: {[a['slug'] for a in ADS]}")
    for a in picked:
        render(a, out_dir, key)
    print("done")
