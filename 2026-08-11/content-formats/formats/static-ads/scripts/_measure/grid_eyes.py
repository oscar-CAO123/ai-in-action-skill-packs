#!/usr/bin/env python3
"""Grid the AFTER half at full size so the censor bar is MEASURED, not guessed.

The trap this exists for: reading eye positions off a downscaled strip without applying the
display scale factor put four bars on noses and brows. This renders the half bar-free at 540x1350,
crops the head region, upscales 2x, and labels every gridline in fractions of the FULL half, so
the numbers read off it drop straight into build_split.BAR.

    python3 grid_eyes.py <industry> [ytop] [ybot]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
from build_split import CROP, HALF, H, PLATES, half_image  # noqa: E402

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

key = sys.argv[1]
ytop = float(sys.argv[2]) if len(sys.argv) > 2 else 0.12
ybot = float(sys.argv[3]) if len(sys.argv) > 3 else 0.52

half = half_image(PLATES / key / "split-after.png", CROP[key]["after"])

# crop the head band, then upscale so the eyes are unambiguous at display size
y0, y1 = round(ytop * H), round(ybot * H)
crop = half.crop((0, y0, HALF, y1))
Z = 2
crop = crop.resize((HALF * Z, (y1 - y0) * Z), Image.LANCZOS)
d = ImageDraw.Draw(crop, "RGBA")
f = ImageFont.truetype(str(SCRIPTS.parent / "assets" / "jost-300.ttf"), 22)

# horizontal lines every 0.01 of the full half height, labelled in full-half fractions
yf = round(ytop, 2)
while yf <= ybot:
    py = (yf * H - y0) * Z
    heavy = abs(yf * 100 - round(yf * 100 / 5) * 5) < 1e-6
    d.line((0, py, HALF * Z, py), fill=(255, 0, 0, 230 if heavy else 90), width=2 if heavy else 1)
    if heavy:
        d.text((6, py + 2), f"{yf:.2f}", font=f, fill=(255, 0, 0, 255))
    yf = round(yf + 0.01, 4)

# vertical lines every 0.05 of the half width
xf = 0.0
while xf <= 1.0001:
    px = xf * HALF * Z
    heavy = abs(xf * 100 - round(xf * 100 / 10) * 10) < 1e-6
    d.line((px, 0, px, (y1 - y0) * Z), fill=(0, 90, 255, 230 if heavy else 90),
           width=2 if heavy else 1)
    if heavy:
        d.text((px + 4, 6), f"{xf:.2f}", font=f, fill=(0, 90, 255, 255))
    xf = round(xf + 0.05, 4)

dst = OUT / f"grid-{key}.png"
crop.save(dst)
print(f"{dst}   half=540x1350  crop y {ytop}-{ybot}  zoom {Z}x")
