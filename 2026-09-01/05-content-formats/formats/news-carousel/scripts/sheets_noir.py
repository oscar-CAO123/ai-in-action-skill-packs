#!/usr/bin/env python3
"""Contact sheets for the noir pain decks. Free, no credits.

    python3 sheets_noir.py wall      # all slide-1s on one labelled wall
    python3 sheets_noir.py decks     # one sheet per deck, 6 slides across
    python3 sheets_noir.py           # both
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("out-noir")
FONT = Path("../assets/Poppins-SemiBold.ttf")
BG = (12, 12, 12)
INK = (210, 210, 210)


def decks():
    return sorted(d for d in OUT.iterdir() if d.is_dir() and d.name.startswith("noir-pain-"))


def label(draw, x, y, text, size):
    f = ImageFont.truetype(str(FONT), size)
    draw.text((x, y), text, font=f, fill=INK)


def wall():
    """Every slide-1 at half size, 5 across, labelled with its slug."""
    ds = decks()
    tw, th = 540, 675
    cap = 46
    pad = 14
    cols = 5
    rows = -(-len(ds) // cols)
    W = cols * (tw + pad) + pad
    H = rows * (th + cap + pad) + pad
    sheet = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(sheet)
    for i, d in enumerate(ds):
        p = d / "slide-01.png"
        if not p.exists():
            continue
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + cap + pad)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        label(draw, x + 4, y + th + 8, d.name.replace("noir-pain-", ""), 30)
    out = OUT / "WALL-slide-01.png"
    sheet.save(out)
    print(f"{out}  {sheet.size}  {len(ds)} decks")


def deck_sheets():
    """One sheet per deck: 6 slides across at 45 percent, numbered."""
    tw, th = 486, 608
    cap = 40
    pad = 12
    for d in decks():
        slides = sorted(d.glob("slide-*.png"))
        W = len(slides) * (tw + pad) + pad
        H = th + cap + 2 * pad + 44
        sheet = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(sheet)
        label(draw, pad, pad, d.name, 34)
        for i, p in enumerate(slides):
            x = pad + i * (tw + pad)
            y = pad + 44
            sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
            label(draw, x + 4, y + th + 6, p.stem.replace("slide-", "slide "), 28)
        out = OUT / f"SHEET-{d.name}.png"
        sheet.save(out)
        print(f"{out}  {sheet.size}  {len(slides)} slides")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    if mode in ("wall", "both"):
        wall()
    if mode in ("decks", "both"):
        deck_sheets()
