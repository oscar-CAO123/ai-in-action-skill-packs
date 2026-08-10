#!/usr/bin/env python3
"""Slot an editorial bed BEHIND the paint on an oil-on-paper plate. FREE, no generation.

    python3 collage_bed_paper.py

Reads the approved `u1b` plate, keys the black oil figure off it by luma, lays a Library of
Congress newspaper bed into the bare paper behind it, and writes a new plate. The approved
figure is never regenerated, only masked.

WHY THIS IS NOT `collage_news.paper_bed` USED DIRECTLY. That bed was built for a plate whose
ground is BLACK: it returns a luma image that is ADDED, lifting crushed blacks into paper.
This plate's ground is already warm paper, so adding light does nothing visible. The same bed
has to be applied as a DARKENING instead, which is the one line of difference below. The bed
itself, its compression, its spots and its grain, all still come from `paper_bed`.

SETTINGS (the operator, 2026-08-07)
  * Bed strength 0.20 to 0.30, a deliberate deviation from L-EDIT's measured 0.02 to 0.12.
    He asked for "mid": legible as collage at full size, still a bed at feed size. Recorded
    the same way D1 to D4 are recorded in BATCH-1-COPY.md.
  * BED ONLY. `layers/editorial-layer/SKILL.md` says F2 noir-painterly takes the bed and no
    foreground cutouts or it stops being the format. the operator held that rule.
  * No film references. An earlier ask for Social Network stills was withdrawn; everything
    here is public domain from Chronicling America, cited in collage-src-university/sources.json.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from collage_news import paper_bed, W, H  # noqa: E402

ROOT = Path(__file__).parent
# FIVE texture families, not one. A bed built from a single material reads as that material
# however you arrange it, which is what "can't just be one newspaper" meant (the operator 2026-08-07).
# Each layer of the bed is drawn from a DIFFERENT family in rotation, so the sheet under the
# paint is newsprint over map hatching over an engraved plate over a ruled ledger.
SRC = ROOT / "collage-src-university"          # newsprint, the original family
TEX = ROOT / "collage-src-textures"            # maps, prints, ledger, technical


def families():
    """Every family that actually has files, newsprint first. Each is a list of paths."""
    fams = [sorted(SRC.glob("*.jpg"))]
    for d in sorted(TEX.glob("*/")):
        got = sorted(d.glob("*.jpg"))
        if got:
            fams.append(got)
    return [f for f in fams if f]
PLATE = ROOT.parent / "candidate/plates/u1b-falling-graduate-on-paper.png"
OUT = ROOT.parent / "candidate/plates/u1b-falling-graduate-collage.png"

# Whole pages, overlapping, every one bleeding off at least one edge. A page that stops inside
# the frame reads as a pasted chip, which `paper_bed` records as the thing the operator rejected.
# (scan index, scale as a multiple of the frame, rotation, centre x, centre y)
CFG = dict(
    bed_luma=(0.20, 0.30),
    note="university and engineering pages, crossed, the middle kept quietest",
    layers=[
        (0, 1.35, -4, 0.22, 0.20),
        (4, 1.25, 6, 0.80, 0.26),
        (7, 1.30, -3, 0.18, 0.76),
        (2, 1.20, 5, 0.84, 0.80),
        (5, 1.45, -8, 0.50, 0.50),
        (8, 1.15, 9, 0.50, 0.06),
        (9, 1.15, -6, 0.50, 0.96),
    ],
    # Soft lifts that keep the centre of the page calmer than its corners, so the falling
    # figure sits in the quietest part of the bed rather than fighting a headline.
    spots=[(0.50, 0.46, 0.42, 0.05)],
)

AMPLITUDE = 0.16      # LOCKED by the operator 2026-08-07 off a three-way compare at 0.30 / 0.16 / 0.09

# A BLANK SHEET RUNS HEAVIER THAN A PAINTED PLATE (the operator, 2026-08-10).
#
# 0.16 was locked against `u1b`, where the bed lands in the paper AROUND a black oil figure and
# competes with it. A Theme B information page has no painting on it at all, and at 0.16 the same
# bed reads as nothing: the pages came back looking like plain paper. These two settings push
# both levers the docstring above describes, amplitude and quantity, and they apply to sheets
# only, so every painted plate in the batch is untouched.
SHEET_AMPLITUDE = 0.30
SHEET_LAYERS = 17


def layers_for(seed, fams):
    """A different arrangement per slide, drawing each layer from a different family.

    Whole pages only, every one bleeding off at least one edge. A page that stops inside the
    frame reads as a pasted chip, which `paper_bed` records as the thing the operator rejected.
    Returns (path, scale, angle, cx, cy) tuples: paths, not indices, because the families are
    different lengths and an index into a flat list would bias toward the biggest family.
    """
    rng = np.random.default_rng(seed)
    out = []
    for i in range(9):
        fam = fams[i % len(fams)]          # rotate families so every one is represented
        out.append((
            fam[int(rng.integers(0, len(fam)))],
            float(rng.uniform(1.15, 1.55)),
            float(rng.uniform(-11, 11)),
            float(rng.uniform(0.06, 0.94)),
            float(rng.uniform(0.04, 0.96)),
        ))
    return out


def mixed_bed(seed, fams, n_layers=11):
    """Stack the families so they COMPOUND instead of covering each other.

    Two failure modes were hit before this shape, both worth keeping written down:

      1. `collage_news.paper_bed` blits each page over the last, so with a full-page mask only
         the top two or three survive. Adding layers changed nothing and the bed read as one
         newspaper however it was arranged.
      2. Multiply-darkening fourteen FULL-FRAME layers at a low alpha went the other way: every
         pixel got darkened by every layer, contrast collapsed and the bed came out a flat wash.

    So each layer gets a soft REGION as well as an alpha. A page only contributes where its
    region lands, feathered at the edge, which means different parts of the sheet carry
    different material and they interleave where the regions overlap. That is the "subtle in
    its mixture, still noticeable" the operator asked for on 2026-08-07.

    Returns a luma bed in [0,1], 1 = bare paper.
    """
    rng = np.random.default_rng(seed)
    acc = np.ones((H, W), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

    for i in range(n_layers):
        fam = fams[i % len(fams)]                 # rotate, so no family is crowded out
        src = fam[int(rng.integers(0, len(fam)))]
        im = Image.open(src).convert("L")

        scale = float(rng.uniform(1.1, 1.7))
        f = scale * max(W / im.width, H / im.height)
        im = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
        im = im.rotate(float(rng.uniform(-12, 12)), expand=True, resample=Image.BICUBIC,
                       fillcolor=255)

        pg = np.asarray(im, dtype=np.float32) / 255.0
        canvas = np.ones((H, W), dtype=np.float32)
        cx, cy = float(rng.uniform(0.1, 0.9)), float(rng.uniform(0.1, 0.9))
        x, y = int(W * cx - pg.shape[1] / 2), int(H * cy - pg.shape[0] / 2)
        sx, sy = max(0, x), max(0, y)
        ex, ey = min(W, x + pg.shape[1]), min(H, y + pg.shape[0])
        if ex <= sx or ey <= sy:
            continue
        canvas[sy:ey, sx:ex] = pg[sy - y:ey - y, sx - x:ex - x]

        # The region: a soft ellipse covering part of the frame, feathered so no layer shows an
        # edge. Without this every layer applies everywhere and the bed averages to nothing.
        rx = float(rng.uniform(0.34, 0.72))
        ry = float(rng.uniform(0.34, 0.72))
        gx, gy = float(rng.uniform(0.05, 0.95)), float(rng.uniform(0.05, 0.95))
        d = np.hypot((xx - W * gx) / (W * rx), (yy - H * gy) / (H * ry))
        region = np.clip(1.0 - d, 0, 1) ** 1.4

        alpha = float(rng.uniform(0.34, 0.62))
        acc *= (1.0 - alpha * region * (1.0 - canvas))

    return np.clip(acc, 0, 1)


def apply_bed(src, dest, amp=AMPLITUDE, seed=7, n_layers=11):
    """Lay the editorial bed into the bare paper of `src` and write `dest`.

    The paint is masked off by the plate's own luma, so on a painted plate the bed lands only
    on the paper around the figure, and on a blank sheet it lands everywhere.
    """
    fams = families()
    if not fams:
        raise SystemExit(f"no scans under {SRC} or {TEX}")
    rgb = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS),
                     dtype=np.float32) / 255.0

    lo, hi = CFG["bed_luma"]
    raw = mixed_bed(seed, fams, n_layers=n_layers)
    rngv = max(float(np.ptp(raw)), 1e-6)
    bed = lo + (raw - raw.min()) / rngv * (hi - lo)
    # the same texture pass paper_bed applies; without it the bed reads as a flat wash
    g = np.random.default_rng(seed).normal(0, 1, (H, W)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 40 + 128).clip(0, 255)).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0
    bed = np.clip(bed + (g - g.mean()) * 0.05, 0, 1)
    # Back out the structure, then invert it: 1 where the scan carried ink, 0 where it was bare
    # newsprint. This is the darkening map.
    ink = 1.0 - np.clip((bed - lo) / (hi - lo), 0, 1)

    # Where the paint is, the bed must not land. Blurred so it dies out around the brush edge
    # instead of stopping on a hard line.
    luma = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    paper = np.clip((luma - 0.34) / 0.30, 0, 1) ** 1.5
    paper = np.asarray(Image.fromarray((paper * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(2.0)), dtype=np.float32) / 255.0

    res = rgb * (1.0 - (amp * ink * paper))[..., None]
    Image.fromarray((np.clip(res, 0, 1) * 255).astype(np.uint8)).save(dest)
    return dest


def main():
    amp = float(sys.argv[1]) if len(sys.argv) > 1 else AMPLITUDE
    out = OUT if len(sys.argv) < 3 else OUT.with_name(sys.argv[2])
    apply_bed(PLATE, out, amp=amp, seed=7)
    print(f"{PLATE.name} -> {out.name}  amplitude {amp}")


if __name__ == "__main__":
    main()
