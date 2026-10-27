#!/usr/bin/env python3
"""Cut the construction plate's arm out as a feathered matte, so it can be stitched onto the
billboards whose own arm came back wrong. Free and exact: the same pixels, not a re-description.

Colour alone cannot do this. The plate is warm-graded end to end, so the road (219,190,184) and
the dry grass (160,135,133) sit on the same values as the arm (155,132,127 in shadow). What DOES
separate it is focus: the arm is held against the lens and is the only large smooth thing in the
lower left, while the asphalt, the verge and the shrub all carry high-frequency grain. So the
matte is cut on LOCAL VARIANCE first, warmth second.

    python3 arm_matte.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

PLATES = Path(__file__).resolve().parent.parent / "plates-magnet"
OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

src = Image.open(PLATES / "construction/billboard-plate.png").convert("RGB")
W, H = src.size
a = np.asarray(src).astype(np.float32)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
lum = a.mean(2)

# local standard deviation over a 9px window: E[x^2] - E[x]^2
k = 9
mean = ndimage.uniform_filter(lum, k)
var = ndimage.uniform_filter(lum * lum, k) - mean * mean
sd = np.sqrt(np.clip(var, 0, None))

smooth = sd < 3.2                      # defocused
warm = (R - B > 18) & (R - G > 8)      # skin rather than sky or shadow
bright = lum > 96
m = smooth & warm & bright

# the arm only ever lives in the lower left, and it must reach the left edge
box = np.zeros_like(m)
box[int(0.48 * H):H, 0:int(0.42 * W)] = True
m &= box

# keep the one blob that touches the left edge, then fill its holes (the dark knuckle crease
# fails the brightness test and would otherwise punch a window through the arm)
lab, n = ndimage.label(m)
edge = set(np.unique(lab[:, 0])) - {0}
if not edge:
    raise SystemExit("no component reaches the left edge, loosen the thresholds")
best = max(edge, key=lambda i: (lab == i).sum())
m = lab == best
m = ndimage.binary_fill_holes(m)
m = ndimage.binary_closing(m, np.ones((25, 25)))
m = ndimage.binary_fill_holes(m)

img = Image.fromarray((m * 255).astype(np.uint8))
img = img.filter(ImageFilter.MinFilter(5))          # pull in off the halo
img = img.filter(ImageFilter.GaussianBlur(9))       # feather: the source edge is soft anyway

cov = np.asarray(img).astype(np.float32) / 255.0
ys, xs = np.where(cov > 0.5)
print(f"matte covers {100 * (cov > 0.5).mean():.2f}% of the frame")
print(f"bbox x {xs.min()}-{xs.max()}  y {ys.min()}-{ys.max()}  (frame {W}x{H})")

img.save(OUT / "arm-mask.png")
cut = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cut.paste(src, (0, 0), img)
cut.save(OUT / "arm-cut.png")

prev = Image.new("RGB", (W, H), (90, 140, 90))      # green so any stray road reads instantly
prev.paste(src, (0, 0), img)
prev.resize((W // 2, H // 2), Image.LANCZOS).save(OUT / "arm-preview.png")
print("wrote arm-mask.png, arm-cut.png, arm-preview.png")
