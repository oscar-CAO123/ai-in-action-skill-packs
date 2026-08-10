#!/usr/bin/env python3
"""Free stand-in plates, so the layout can be judged before a cent is spent.

These are NOT the format's look. They exist to exercise the two laws end to end: a mass
in the middle band, deliberate empty space above or below it, and a ground colour that
puts each slide on a different branch of the ink law. Every one is stamped PLACEHOLDER.

    python3 plates.py [--out DIR]
"""
import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
ASSETS = Path(__file__).resolve().parent.parent / "assets"

# name, sky/ground pair, mass colour, where the empty space is built
PLATES = [
    ("01-warm-low",  ((122, 74, 44), (58, 32, 18)), (28, 16, 10), "low"),
    ("02-cool-top",  ((16, 34, 52), (10, 20, 32)),  (6, 10, 16),  "top"),
    # Bright on purpose, not mid. A well at mid luminance has a contrast ceiling of about
    # 4.6:1 and cannot carry a headline whatever colour the ink is (tape.headroom).
    ("03-light-low", ((226, 224, 230), (206, 204, 211)), (96, 92, 90), "low"),
    ("04-blue-top",  ((24, 44, 74), (14, 26, 44)),  (8, 12, 20),  "top"),
    ("05-black-mid", ((22, 22, 26), (10, 10, 12)),  (40, 40, 46),  "mid"),
]


def gradient(top, bottom):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t)
                                            for i in range(3)))
    return im


def texture(im, box, strength=64):
    """Detail inside the subject, so the mass reads as occupied and the well finder has
    something to tell apart. A blurred blob with no detail measures as flat as empty sky,
    which is a stand-in artefact rather than anything a real plate does."""
    x0, y0, x1, y1 = [int(v) for v in box]
    d = ImageDraw.Draw(im)
    rng = 7919
    for i in range((x1 - x0) * (y1 - y0) // 160):
        rng = (rng * 1103515245 + 12345) % 2147483648
        x = x0 + rng % max(1, x1 - x0)
        rng = (rng * 1103515245 + 12345) % 2147483648
        y = y0 + rng % max(1, y1 - y0)
        rng = (rng * 1103515245 + 12345) % 2147483648
        v = strength - (rng % (2 * strength))
        base = im.getpixel((min(W - 1, x), min(H - 1, y)))
        d.rectangle([x, y, x + 9, y + 9],
                    fill=tuple(max(0, min(255, c + v)) for c in base))
    return im


def mass(im, colour, band):
    """A soft subject mass, kept OUT of the band the copy is going to use.

    `mid` is the endcard case: the subject splits to the top and bottom edges and the
    middle of the frame is left open, which is the opposite of what the other two do.
    """
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    spans = {"low": [(0.10, 0.55)], "top": [(0.45, 1.00)],
             "mid": [(-0.10, 0.24), (0.78, 1.10)]}[band]
    cx = W * 0.44
    for y0f, y1f in spans:
        y0, y1 = y0f * H, y1f * H
        d.ellipse([cx - W * 0.30, y0, cx + W * 0.30, y1], fill=colour)
        d.ellipse([cx - W * 0.13, y0 - H * 0.05, cx + W * 0.13, y0 + H * 0.09], fill=colour)
        for i in range(6):                   # a little structure so it is not one blob
            x = cx - W * 0.26 + i * W * 0.105
            d.rectangle([x, y0 + H * 0.06, x + W * 0.045, y1 - H * 0.03],
                        fill=tuple(min(255, c + 14 + i * 5) for c in colour))
    layer = layer.filter(ImageFilter.GaussianBlur(26))
    im = Image.composite(layer, im,
                         layer.convert("L").point(lambda v: 255 if v > 12 else 0))
    for y0f, y1f in spans:
        im = texture(im, (cx - W * 0.32, max(0, y0f * H), cx + W * 0.32, min(H, y1f * H)))
    return im


def stamp(im):
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype(str(ASSETS / "Poppins-Medium.ttf"), 22)
    except OSError:
        f = ImageFont.load_default()
    d.text((W - 250, H - 44), "PLACEHOLDER", font=f, fill=(255, 0, 90))
    return im


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    made = []
    for name, (top, bottom), mcol, band in PLATES:
        im = gradient(top, bottom)
        im = mass(im, mcol, band)
        # a soft horizon so the empty band is not a dead flat colour field
        h = Image.new("L", (W, H), 0)
        ImageDraw.Draw(h).rectangle([0, H * (0.62 if band == "low" else 0.30), W, H],
                                    fill=26)
        im = Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), im,
                             h.filter(ImageFilter.GaussianBlur(60)))
        p = out / f"{name}.png"
        stamp(im).save(p)
        made.append(p)
        print("plate", p.name, "empty space:", band)
    return made


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).parent / "plates"))
    build(Path(ap.parse_args().out))
