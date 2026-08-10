#!/usr/bin/env python3
"""The two laws of the tape carousel, in one place.

    find_wells(path)   where the plate has flat, empty space big enough to hold copy
    ink_for(ground)    what colour the type takes on that ground
    contrast(a, b)     WCAG contrast ratio, the gate both laws answer to

Both laws were measured off the reference set at
`content-engine/engine/reference-bank/carousels/DbQkpEOAl1l/` and the numbers behind them
are written up in that folder's ENTRY.md. Re-derive with `measure.py`.
"""
import colorsys

import numpy as np
from PIL import Image

CELL = 30           # analysis cell, source pixels
FLAT_STD = 14.0     # a cell is empty when its luma std is under this
DARK_GROUND = 0.45  # ground value below which the ink flips to near white

# Contrast floors. The reference runs 12.4:1 median on dark grounds and collapses to
# 3.1:1 on light ones. house keeps the dark-ground behaviour and refuses the light-ground
# behaviour for any line that carries the message.
FLOOR = {"hook": 7.0, "head": 7.0, "body": 4.5, "eyebrow": 4.5, "stat": 7.0, "cta": 7.0}


# --------------------------------------------------------------------------- colour
def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(c):
    return "#%02X%02X%02X" % tuple(int(round(max(0, min(255, v)))) for v in c)


def rel_lum(c):
    c = np.asarray(_rgb(c) if isinstance(c, str) else c, float) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def headroom(ground):
    """The best contrast ANY ink can reach on this ground.

    Pure white gives 1.05/(L+0.05), pure black gives (L+0.05)/0.05, and the two cross at
    L=0.179 where the ceiling is 4.58:1. So a mid-luminance well cannot carry a headline
    at 7:1 no matter what colour the type is: the fix is a darker or brighter well in the
    plate, never a different ink. A 7:1 headline needs L at or under 0.10, or at or over
    0.30.
    """
    lb = rel_lum(ground)
    return max(1.05 / (lb + 0.05), (lb + 0.05) / 0.05)


def ink_for(ground, role="head", accent=None):
    """The ink law. Returns (hex, contrast_ratio, note).

    Dark ground: near white, tinted cream when the ground is warm, left pure when it is
    cool. Light ground: a dark warm ink, because the reference's tonal cream measures
    3.1:1 and will not survive a feed thumbnail.

    `accent` is honoured only when it already clears the role's floor on this ground,
    so the house blue can be asked for and will be refused rather than laid down illegibly.
    """
    r, g, b = (v / 255 for v in (_rgb(ground) if isinstance(ground, str) else ground))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    hdeg = h * 360
    floor = FLOOR.get(role, 4.5)

    if accent and contrast(accent, ground) >= floor:
        return accent, contrast(accent, ground), "accent cleared the floor"

    warm = (hdeg <= 70 or hdeg >= 340) and s > 0.25
    if v < DARK_GROUND:
        if warm:
            ink_s = min(0.33, 0.06 + 0.35 * s)     # cream, carrying the ground's warmth
            note = "dark warm ground, cream"
            hue = 50 / 360
        else:
            ink_s, hue, note = 0.02, h, "dark cool ground, white"
        ink_v = 0.98
    else:
        # light ground: go dark, and keep the ground's hue family so it still belongs
        hue = h if s > 0.12 else 22 / 360
        ink_s, ink_v = min(0.30, max(0.12, s * 0.5)), 0.30
        note = "light ground, dark ink"

    def build(val, sat):
        return _hex([c * 255 for c in colorsys.hsv_to_rgb(hue, sat, val)])

    ink = build(ink_v, ink_s)
    cr = contrast(ink, ground)
    # Walk the value away from the ground until the floor is cleared, then stop.
    step = 0.03 if ink_v < 0.5 else -0.03
    guard = 0
    while cr < floor and 0.0 <= ink_v <= 1.0 and guard < 40:
        ink_v = max(0.0, min(1.0, ink_v + (-step if ink_v < 0.5 else step)))
        ink_s = max(0.0, ink_s - 0.01)
        ink = build(ink_v, ink_s)
        cr = contrast(ink, ground)
        guard += 1
        if ink_v in (0.0, 1.0):
            break
    return ink, cr, note


# ---------------------------------------------------------------------------- wells
def _luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def flat_map(path):
    """Per-cell (is_flat, mean_rgb) for one plate."""
    a = np.asarray(Image.open(path).convert("RGB"), float)
    H, W, _ = a.shape
    ch, cw = H // CELL, W // CELL
    a = a[:ch * CELL, :cw * CELL]
    cells = a.reshape(ch, CELL, cw, CELL, 3)
    mean = cells.mean(axis=(1, 3))
    g = _luma(a).reshape(ch, CELL, cw, CELL)
    flat = g.std(axis=(1, 3)) < FLAT_STD
    return flat, mean, (W, H)


BANDS = {"top": (0, 40), "mid": (28, 72), "low": (55, 100), "any": (0, 100)}


def find_wells(path, band="any", min_w_pct=34, min_h_pct=9, top_n=6):
    """Largest all-flat rectangles inside `band`, biggest area first.

    Returns dicts in percent of frame: x, y, w, h, plus the well's mean colour, its
    luma and how flat it is. Percent so a deck stays readable and survives a re-crop.

    The band is a hard constraint, not a preference. A deck that says the copy sits low
    gets a well in the low third or an error, never a box quietly placed somewhere else.
    """
    flat, mean, (W, H) = flat_map(path)
    ch, cw = flat.shape
    lo, hi = BANDS[band]
    keep = np.zeros(ch, bool)
    keep[int(ch * lo / 100):max(1, int(round(ch * hi / 100)))] = True
    flat = flat & keep[:, None]
    min_w = max(1, round(cw * min_w_pct / 100))
    min_h = max(1, round(ch * min_h_pct / 100))

    # histogram-of-heights over the flat mask: every maximal all-flat rectangle
    heights = np.zeros(cw, int)
    found = []
    for y in range(ch):
        heights = np.where(flat[y], heights + 1, 0)
        stack = []
        for x in range(cw + 1):
            hcur = heights[x] if x < cw else 0
            start = x
            while stack and stack[-1][1] >= hcur:
                sx, sh = stack.pop()
                if sh >= min_h and (x - sx) >= min_w:
                    found.append((sh * (x - sx), sx, y - sh + 1, x - sx, sh))
                start = sx
            stack.append((start, hcur))

    found.sort(reverse=True)
    out, taken = [], []
    for area, x, y, w, h in found:
        box = (x, y, x + w, y + h)
        if any(not (box[2] <= t[0] or box[0] >= t[2] or box[3] <= t[1] or box[1] >= t[3])
               for t in taken):
            continue
        taken.append(box)
        patch = mean[y:y + h, x:x + w].reshape(-1, 3)
        col = patch.mean(axis=0)
        out.append({
            "x": round(100 * x / mean.shape[1], 1),
            "y": round(100 * y / mean.shape[0], 1),
            "w": round(100 * w / mean.shape[1], 1),
            "h": round(100 * h / mean.shape[0], 1),
            "ground": _hex(col),
            "luma": round(float(_luma(col)), 1),
            "spread": round(float(np.abs(patch - col).mean()), 1),
            "area_pct": round(100 * area / (ch * cw), 1),
        })
        if len(out) >= top_n:
            break
    return out


def band_flat_share(path, band="any"):
    """How much of a band is empty. Near 100 means the finder had nothing to tell apart:
    the plate is a flat field, not a composed frame with space built into it."""
    flat, _, _ = flat_map(path)
    ch = flat.shape[0]
    lo, hi = BANDS[band]
    sl = flat[int(ch * lo / 100):max(1, int(round(ch * hi / 100)))]
    return round(100 * float(sl.mean()), 1)


def sample(path, box):
    """Mean colour of an explicit box, given as percentages [x, y, w, h]."""
    a = np.asarray(Image.open(path).convert("RGB"), float)
    H, W, _ = a.shape
    x0, y0 = int(W * box[0] / 100), int(H * box[1] / 100)
    x1, y1 = x0 + int(W * box[2] / 100), y0 + int(H * box[3] / 100)
    patch = a[max(0, y0):min(H, y1), max(0, x0):min(W, x1)].reshape(-1, 3)
    col = patch.mean(axis=0)
    return {"ground": _hex(col), "luma": round(float(_luma(col)), 1),
            "spread": round(float(np.abs(patch - col).mean()), 1)}


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(f"\n{p}  flat by band: " + "  ".join(
            f"{b}={band_flat_share(p, b)}%" for b in ("top", "mid", "low")))
        for w in find_wells(p):
            ink, cr, note = ink_for(w["ground"])
            print(f"  well x{w['x']} y{w['y']} {w['w']}x{w['h']}%  ground {w['ground']} "
                  f"L{w['luma']} spread {w['spread']}  ->  ink {ink} cr {cr:.1f} ({note})")
