#!/usr/bin/env python3
"""Lay the house mark into the head void of a painted plate. FREE and re-runnable.

    python3 mascot.py u3        # writes candidate/plates/u3-mascot.png

WHY THIS EXISTS. The campaign mascot is "the figure whose head is the house logo". The mark is a
wordmark, and every style tail in this rig bans lettering inside a generated plate because the
models garble it, so the head is never painted. The plate is generated with an empty neckline
and the real SVG is laid into that void here. Same contract as hand-drawn type being a font
over the plate: the brand asset stays exact and the slide re-runs for nothing.

THE MARK IS THE house LINE ONLY. The full lockup is "house" over "Partners". The void on a 1782px
plate is about 190px wide, which is 115px once the card is composited down to 1080, and at that
width the word Partners sets around 8px and turns to mud. The house line alone still reads, and
the A-as-arrow is the part of the mark that carries. `part="lockup"` keeps the whole thing for
any plate whose void is big enough to take it.

VOIDS ARE HAND-SET, one row per plate, the same way `build_split.py` hand-sets CROP and BAR.
There is no head detector here and the models frame the figure differently every time, so the
box gets measured once off the plate and written down. Measure with:

    python3 mascot.py <key> --measure     # prints the bright blob it found in the upper mass
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
PLATES = ROOT.parent / "candidate" / "plates"
LOGO = ASSETS / "house-logo.svg"
CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# The head void in each plate's own pixels, (x0, y0, x1, y1). Measured once, never guessed.
VOIDS = {
    # u3, the recruiting-poster figure. Void runs head-and-neck down into the collar; the box
    # below is the head part only, so the mark sits where a face would and the neck stays bare.
    "u3": {"plate": "u3-u3-mascot-poster.png", "void": (800, 495, 990, 720)},
    # u3x, the same figure extended to the sheet on . The extend kept the void and
    # grew it, so the mark sets about 20 per cent larger here than on v1. This is the plate U3
    # actually ships on; u3 stays in the table as the record.
    "u3x": {"plate": "u3x-u3-extended-to-fill-the-page.png", "void": (797, 485, 1000, 700)},
    # u6r has no enclosed void. That plate's whole ground is bare paper, so instead of a painted
    # head silhouette with a hole in it there is just an open collar with paper above. The box
    # here is the space a head would occupy above the collar, and the mark floats on the paper.
    # Same device, and it reads cleaner than u3x because nothing crowds it.
    "u6r": {"plate": "u6r-u6-us.png", "void": (769, 300, 1001, 540)},
}

# How much of the void the mark fills across. Full width crowds the painted edge and reads as a
# sticker; 0.86 leaves the bare paper margin that makes it look set into the hole.
FILL = 0.86

# A DRAWN HEAD, for the plates that have no painted one. On the U3 cover the mark sits inside a
# head the model painted, so it reads as a face. u6r has only an open collar on bare paper, and
# the bare mark floating above it reads as a caption rather than a head. So
# the contour is drawn here and the mark set inside it, which is the same contract as the mark
# itself: the brand asset stays exact, the plate is never asked to paint lettering.
#
# The box is plate pixels, (x0, y0, x1, y1). The CHIN SITS INSIDE THE COLLAR ON PURPOSE. Black
# drawn over the collar's black is invisible, so the jaw lines vanish into the coat instead of
# stopping in mid air above it, and the head reads as worn rather than pasted on.
HEADS = {
    "u6r": {"plate": "u6r-u6-us.png", "box": (795, 280, 1025, 625), "stroke": 13, "mark": 0.70},
}


def head_svg(box, stroke, w, h):
    """A brush-drawn head contour in plate coordinates, transparent everywhere else."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    cx = x0 + bw / 2

    def p(fx, fy):
        return f"{x0 + bw * fx:.1f},{y0 + bh * fy:.1f}"

    # Cranium, temple, cheek, jaw, chin, and back up the other side. Deliberately not mirrored:
    # the right temple runs a touch wider and the chin sits a touch left of centre, because a
    # symmetrical head reads as a vector shape rather than a painted one.
    d = (f"M {p(0.50, 0.00)} "
         f"C {p(0.20, 0.01)} {p(0.00, 0.13)} {p(0.005, 0.33)} "
         f"C {p(0.01, 0.50)} {p(0.05, 0.66)} {p(0.14, 0.79)} "
         f"C {p(0.23, 0.91)} {p(0.35, 0.99)} {p(0.49, 1.00)} "
         f"C {p(0.64, 0.99)} {p(0.77, 0.91)} {p(0.86, 0.78)} "
         f"C {p(0.95, 0.65)} {p(1.00, 0.49)} {p(1.00, 0.32)} "
         f"C {p(0.99, 0.12)} {p(0.79, 0.01)} {p(0.50, 0.00)} Z")
    # TWO PASSES, because one even stroke reads as a marker balloon next to an oil painting.
    # The base line carries the shape; the dashed pass rides on top at double the weight with
    # long gaps, so the contour presses and lifts the way a loaded brush does. Each pass gets its
    # own turbulence seed, so they wander apart and the edge frays instead of doubling cleanly.
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
<filter id="b1" x="-20%" y="-20%" width="140%" height="140%">
  <feTurbulence type="fractalNoise" baseFrequency="0.009" numOctaves="3" seed="7"/>
  <feDisplacementMap in="SourceGraphic" scale="16" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="b2" x="-20%" y="-20%" width="140%" height="140%">
  <feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="2" seed="23"/>
  <feDisplacementMap in="SourceGraphic" scale="22" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<path d="{d}" fill="none" stroke="#0a0a0a" stroke-width="{stroke}"
      stroke-linecap="round" stroke-linejoin="round" filter="url(#b1)"/>
<path d="{d}" fill="none" stroke="#0a0a0a" stroke-width="{stroke * 2.1:.0f}"
      stroke-linecap="round" stroke-linejoin="round" filter="url(#b2)"
      stroke-dasharray="230 120 74 210 150 90" stroke-dashoffset="60" opacity="0.92"/>
</svg>"""


def apply_head(key, dest=None):
    """Draw the head contour onto the plate and set the house mark inside it. Free, idempotent."""
    spec = HEADS[key]
    plate = PLATES / spec["plate"]
    im = Image.open(plate).convert("RGBA")
    x0, y0, x1, y1 = spec["box"]

    svg = head_svg(spec["box"], spec["stroke"], im.width, im.height)
    with tempfile.NamedTemporaryFile("w", suffix=".svg", dir=ROOT, delete=False) as f:
        f.write(svg)
        tmp = f.name
    out = Path(tempfile.mkdtemp()) / "head.png"
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000",
                        f"--window-size={im.width},{im.height}", f"--screenshot={out}",
                        Path(tmp).as_uri()], check=True, capture_output=True)
    finally:
        os.unlink(tmp)
    im.alpha_composite(Image.open(out).convert("RGBA"))

    # The mark sits in the upper half of the head, where a face is, not in the middle of the
    # whole shape, which would drop it onto the jaw.
    mark = mark_png(int((x1 - x0) * spec["mark"]))
    mx = x0 + ((x1 - x0) - mark.width) // 2
    my = int(y0 + (y1 - y0) * 0.42) - mark.height // 2
    im.alpha_composite(mark, (mx, my))

    dest = Path(dest or PLATES / f"{key}-head.png")
    im.convert("RGB").save(dest)
    print(f"{key}  head {x1-x0}x{y1-y0}, mark {mark.width}px at {mx},{my}  ->  {dest.name}")
    return dest


def mark_png(width, part="house"):
    """Render the logo to a transparent PNG `width` px across, cropped to the wanted part."""
    svg = LOGO.resolve().as_uri()
    h = int(width * 521.2 / 1023.1)
    doc = (f'<style>*{{margin:0;padding:0}}html,body{{width:{width}px;height:{h}px}}'
           f'img{{width:{width}px;display:block}}</style><img src="{svg}">')
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    out = Path(tempfile.mkdtemp()) / "mark.png"
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000",
                        f"--window-size={width},{h}", f"--screenshot={out}",
                        Path(tmp).as_uri()], check=True, capture_output=True)
    finally:
        os.unlink(tmp)
    im = Image.open(out).convert("RGBA")
    if part == "lockup":
        return im
    # Crop to the house line: find the horizontal gap between the two lines of the lockup by
    # looking for the widest run of empty rows, rather than hardcoding a fraction of the height.
    ink = np.asarray(im)[:, :, 3] > 16
    rows = ink.any(axis=1)
    gaps, run = [], None
    for y, on in enumerate(rows):
        if not on and run is None:
            run = y
        elif on and run is not None:
            gaps.append((y - run, run, y))
            run = None
    if not gaps:
        return im
    _, top, _ = max(gaps)
    return im.crop((0, 0, im.width, top))


def apply_mascot(key, dest=None, part="house"):
    spec = VOIDS[key]
    plate = PLATES / spec["plate"]
    x0, y0, x1, y1 = spec["void"]
    im = Image.open(plate).convert("RGBA")
    mark = mark_png(int((x1 - x0) * FILL), part=part)
    mx = x0 + ((x1 - x0) - mark.width) // 2
    my = y0 + ((y1 - y0) - mark.height) // 2
    im.alpha_composite(mark, (mx, my))
    dest = Path(dest or PLATES / f"{key}-mascot.png")
    im.convert("RGB").save(dest)
    print(f"{key}  mark {mark.width}x{mark.height} at {mx},{my}  ->  {dest.name}")
    return dest


def measure(key):
    """Print the largest bright blob in the upper half of the painted mass, to set a void by."""
    from scipy import ndimage
    a = np.asarray(Image.open(PLATES / VOIDS[key]["plate"]).convert("L"))
    lab, n = ndimage.label(a < 110)
    sz = ndimage.sum(a < 110, lab, range(1, n + 1))
    ys, xs = np.where(lab == int(np.argmax(sz)) + 1)
    print(f"painted mass  x {xs.min()}-{xs.max()}  y {ys.min()}-{ys.max()}")
    top = ys.min() + (ys.max() - ys.min()) // 2
    sub = a[ys.min():top, xs.min():xs.max()] > 195
    l2, n2 = ndimage.label(sub)
    s2 = ndimage.sum(sub, l2, range(1, n2 + 1))
    for j in np.argsort(s2)[::-1][:3]:
        yy, xx = np.where(l2 == j + 1)
        print(f"  blob {int(s2[j]):>7}px  x {xx.min()+xs.min()}-{xx.max()+xs.min()}  "
              f"y {yy.min()+ys.min()}-{yy.max()+ys.min()}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or args[0] not in (VOIDS | HEADS):
        sys.exit(f"usage: mascot.py <{'|'.join(VOIDS | HEADS)}> [--measure] [--lockup] [--head]")
    if "--measure" in sys.argv:
        measure(args[0])
    elif "--head" in sys.argv:
        apply_head(args[0])
    else:
        apply_mascot(args[0], part="lockup" if "--lockup" in sys.argv else "house")
