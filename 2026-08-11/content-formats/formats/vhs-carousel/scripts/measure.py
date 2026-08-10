#!/usr/bin/env python3
"""Measure a carousel: the grade tells, the flat share, and every type block.

This is how the reference was derived and how a house build is checked against it. Point it
at any folder of slides.

    python3 measure.py <dir-of-slides> [--json out.json]

Per slide it prints the tape tells (grain floor, saturation, chroma mis-registration,
scanline periodicity, black floor), how much of the frame is empty by band, and the
largest blocks of type it can find with the ink, the ground and the contrast between them.

Nothing here opens an image for viewing. Everything is read through PIL and numpy.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

from tape import CELL, FLAT_STD, contrast

BANDS = ("top", "mid", "low")


def _luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def _hex(c):
    return "#%02X%02X%02X" % tuple(int(round(v)) for v in c)


def _edges(g):
    e = np.zeros_like(g)
    e[:, :-1] += np.abs(np.diff(g, axis=1))
    e[:-1, :] += np.abs(np.diff(g, axis=0))
    return e


def _label(mask):
    lab = np.zeros(mask.shape, int)
    cur = 0
    for sy in range(mask.shape[0]):
        for sx in range(mask.shape[1]):
            if not mask[sy, sx] or lab[sy, sx]:
                continue
            cur += 1
            stack = [(sy, sx)]
            lab[sy, sx] = cur
            while stack:
                y, x = stack.pop()
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] \
                            and mask[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur
                        stack.append((ny, nx))
    return lab, cur


def grade_tells(a, g):
    rows = g.mean(axis=1)
    d = rows - rows.mean()
    spec = np.abs(np.fft.rfft(d))
    freqs = np.fft.rfftfreq(len(d))
    top = spec[1:].argmax() + 1
    period = round(1 / freqs[top], 1) if freqs[top] else None
    mx, mn = a.max(axis=2), a.min(axis=2)
    r, b = a[..., 0], a[..., 2]
    best, bestc = 0, -2.0
    for s in range(-14, 15):
        c = float(np.corrcoef(np.roll(r, s, axis=1)[:, 20:-20].ravel(),
                              b[:, 20:-20].ravel())[0, 1])
        if c > bestc:
            bestc, best = c, s
    return {
        "grain_floor": round(float(np.abs(g[1:, :] - g[:-1, :]).mean()), 2),
        "mean_saturation": round(float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0).mean()), 3),
        "chroma_shift_px": best,
        "scanline_period_px": period,
        "black_floor_1pct": round(float(np.percentile(g, 1)), 1),
        "white_ceiling_99pct": round(float(np.percentile(g, 99)), 1),
    }


def analyse(path):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    a = np.asarray(im, float)
    g = _luma(a)
    ch, cw = H // CELL, W // CELL
    gg = g[:ch * CELL, :cw * CELL].reshape(ch, CELL, cw, CELL)
    std = gg.std(axis=(1, 3))
    flat = std < FLAT_STD
    dens = _edges(g)[:ch * CELL, :cw * CELL].reshape(ch, CELL, cw, CELL).mean(axis=(1, 3))

    mask = (dens > max(np.percentile(dens, 88), 6.0)) & (std > 18)
    lab, n = _label(mask)
    blocks = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 4:
            continue
        y0, y1 = ys.min() * CELL, (ys.max() + 1) * CELL
        x0, x1 = xs.min() * CELL, (xs.max() + 1) * CELL
        patch = a[y0:y1, x0:x1].reshape(-1, 3)
        pl = _luma(patch)
        med = np.median(pl)
        bg = patch[np.abs(pl - med) < 12]
        bgm = bg.mean(axis=0) if len(bg) else patch.mean(axis=0)
        hi, lo = patch[pl > np.percentile(pl, 96)], patch[pl < np.percentile(pl, 4)]
        if not len(hi) or not len(lo):
            continue
        fg = hi if abs(_luma(hi.mean(axis=0)) - _luma(bgm)) >= \
            abs(_luma(lo.mean(axis=0)) - _luma(bgm)) else lo
        fgm = fg.mean(axis=0)
        blocks.append({
            "cells": int(len(ys)),
            "x_pct": [round(100 * x0 / W), round(100 * x1 / W)],
            "y_pct": [round(100 * y0 / H), round(100 * y1 / H)],
            "ink": _hex(fgm), "ground": _hex(bgm),
            "ground_luma": round(float(_luma(bgm)), 1),
            "contrast": round(contrast(fgm, bgm), 2),
        })
    blocks.sort(key=lambda b: -b["cells"])

    thirds = {"top": flat[:ch // 3], "mid": flat[ch // 3:2 * ch // 3],
              "low": flat[2 * ch // 3:]}
    return {
        "file": path.name, "size": [W, H], "aspect": round(W / H, 4),
        "grade": grade_tells(a, g),
        "flat_pct": round(100 * float(flat.mean()), 1),
        "flat_by_band": {k: round(100 * float(v.mean()), 1) for k, v in thirds.items()},
        "blocks": blocks[:6],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--json")
    args = ap.parse_args()
    files = sorted(p for p in Path(args.dir).iterdir()
                   if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    out = [analyse(p) for p in files]
    for s in out:
        gr, fb = s["grade"], s["flat_by_band"]
        print(f"\n{s['file']}  {s['size'][0]}x{s['size'][1]} ar={s['aspect']}  "
              f"flat {s['flat_pct']}% (top {fb['top']} mid {fb['mid']} low {fb['low']})")
        print(f"  grain={gr['grain_floor']} sat={gr['mean_saturation']} "
              f"chroma={gr['chroma_shift_px']}px scan={gr['scanline_period_px']} "
              f"blacks={gr['black_floor_1pct']} whites={gr['white_ceiling_99pct']}")
        for b in s["blocks"][:3]:
            print(f"  type x{b['x_pct']}% y{b['y_pct']}% ink={b['ink']} "
                  f"ground={b['ground']} L={b['ground_luma']} cr={b['contrast']}")
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=1))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
