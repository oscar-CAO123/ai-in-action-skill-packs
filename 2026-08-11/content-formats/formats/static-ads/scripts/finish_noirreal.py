#!/usr/bin/env python3
"""Finishing passes for the illustrated noir plates. FREE, no generation.

    python3 finish_noirreal.py bottleneck-illus

Two passes, each applied to only half the frame, split on saturation:

  * The **window** is the only saturated region in the plate, so it masks cleanly. It takes
    the **VSL grade**: warm amber cast, lifted milky blacks, slight desaturation and grain,
    the scanned direct-response look from plates_retro.py.
  * The **illustrated interior** is pure black and white, so it takes the inverse mask and
    gets the **moire shimmer** from the house tool at
    `projects/content-engine/engine/tools/moire/moire.py`.

Moire is never prompt-baked. It is an interference artifact between two periodic grids and it
only exists when it is generated at delivery resolution and composited over an approved plate.
The house tool is the one that does that, so this calls it rather than reimplementing it.

Writes `<slug>-finished.png` beside the source.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).parent
PLATES = ROOT / "plates-noirreal"
MOIRE = (ROOT.parents[4] / "projects/content-engine/engine/tools/moire/moire.py")


def window_mask(img, feather=10):
    """1.0 inside the window aperture, 0.0 in the painted interior.

    Two things had to be worked around to get this right, both measured off the plate:

      * **Plain saturation leaves holes.** The sky, the concrete mixer and the pale stacks
        inside the window are near-neutral, so a saturation mask lets the moire leak through
        them and stripe the photograph.
      * **The painted room is not perfectly neutral.** An oil-noir render carries residual
        warmth in skin, timber and the match flame, so the bounding box of "any saturated
        pixel" swallows two thirds of the frame.

    The window has a signature the painted room does not: blue sky and orange high-vis. So
    detect chroma that is specifically blue-dominant or warm-dominant, take the row and column
    bands where that signature lives, and fill that rectangle.
    """
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    chroma = a.max(2) - a.min(2)
    blue = (a[..., 2] - a[..., 0]) > 12
    warm = (a[..., 0] - a[..., 2]) > 28
    win = (chroma > 16) & (blue | warm)
    h, w = win.shape
    rows, cols = win.mean(1), win.mean(0)
    if rows.max <= 0:
        return np.zeros((h, w), dtype=np.float32)
    ys = np.nonzero(rows > rows.max * 0.10)[0]
    xs = np.nonzero(cols > cols.max * 0.10)[0]
    m = np.zeros((h, w), dtype=np.uint8)
    m[ys.min:ys.max, xs.min:xs.max] = 255
    m = Image.fromarray(m).filter(ImageFilter.GaussianBlur(feather))
    print(f"  window aperture x {xs.min}-{xs.max}, y {ys.min}-{ys.max} "
          f"({100*(xs.max-xs.min)*(ys.max-ys.min)/(w*h):.0f}% of frame)")
    return np.asarray(m, dtype=np.float32) / 255.0


def vsl_grade(img):
    """Warm amber, lifted blacks, softened saturation, grain. The plates_retro look."""
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    # lift the blacks and roll the highlights, the scanned-print curve
    a = 0.095 + a * 0.880
    a = np.clip(a, 0, 1) ** 0.94
    # amber cast
    a[..., 0] *= 1.115
    a[..., 1] *= 1.010
    a[..., 2] *= 0.840
    # pull saturation back toward the print
    lum = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 0.72
    # grain
    rng = np.random.default_rng(7)
    a += rng.normal(0, 0.019, a.shape).astype(np.float32)
    return np.clip(a, 0, 1)


def moire_still(img, out_png):
    """Render one moire frame over the plate using the house tool."""
    w, h = img.size
    with tempfile.TemporaryDirectory as td:
        src = Path(td) / "plate.png"
        img.convert("RGB").save(src)
        mp4 = Path(td) / "m.mp4"
        r = subprocess.run(
            [sys.executable, str(MOIRE), "--plate", str(src), "--out", str(mp4),
             "--still", str(out_png), "--mode", "displace", "--seconds", "1",
             "--width", str(w), "--height", str(h), "--pitch", "6",
             "--opacity", "0.30", "--safe-top", "0.0"],
            capture_output=True, text=True)
        if not Path(out_png).exists:
            sys.exit(f"moire tool produced no still:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")


def finish(slug):
    src = PLATES / f"{slug}.png"
    if not src.exists:
        sys.exit(f"no plate at {src}")
    img = Image.open(src).convert("RGB")
    base = np.asarray(img, dtype=np.float32) / 255.0
    m = window_mask(img)[..., None]

    graded = vsl_grade(img)                      # the window
    with tempfile.TemporaryDirectory as td:
        still = Path(td) / "moire.png"
        moire_still(img, still)
        moired = np.asarray(Image.open(still).convert("RGB").resize(img.size),
                            dtype=np.float32) / 255.0

    # window takes the grade, interior takes the moire, and the feathered mask joins them
    out = graded * m + moired * (1 - m)
    # keep the interior strictly neutral: moire must not tint the black and white
    out = np.clip(out, 0, 1)
    lum = out @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    out = out * m + (lum[..., None] * np.ones(3, dtype=np.float32)) * (1 - m)

    dst = PLATES / f"{slug}-finished.png"
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(dst)
    cover = float(m.mean)
    print(f"{dst}\n  window mask covers {cover*100:.1f}% of the frame, "
          f"graded; the remaining {100-cover*100:.1f}% took the moire")


if __name__ == "__main__":
    for s in (sys.argv[1:] or ["bottleneck-illus"]):
        finish(s)
