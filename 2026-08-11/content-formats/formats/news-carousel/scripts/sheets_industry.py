#!/usr/bin/env python3
"""Contact sheets for the 25 industry statics. Free, no credits.

    python3 sheets_industry.py           # one sheet per industry (5 cards across) + the 25-up wall
    python3 sheets_industry.py wall      # the wall only
    python3 sheets_industry.py sheets    # the per-industry sheets only

Writes into out-industry/_sheets/.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("out-industry")
SHEETS = OUT / "_sheets"
FONT = Path("../assets/Poppins-SemiBold.ttf")
BG = (12, 12, 12)
INK = (210, 210, 210)
DIM = (128, 128, 128)


def industries():
    return sorted(d for d in OUT.iterdir() if d.is_dir() and not d.name.startswith("_"))


def label(draw, x, y, text, size, fill=INK):
    draw.text((x, y), text, font=ImageFont.truetype(str(FONT), size), fill=fill)


def sheets():
    """One sheet per industry: its 5 pain cards across, each captioned with its pain slug."""
    tw, th = 486, 608
    cap, pad, head = 44, 14, 52
    for d in industries():
        cards = sorted(d.glob("*.png"))
        W = len(cards) * (tw + pad) + pad
        H = head + th + cap + 2 * pad
        sheet = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(sheet)
        label(draw, pad, pad, d.name.replace("-", " ").upper(), 34)
        for i, p in enumerate(cards):
            x = pad + i * (tw + pad)
            y = pad + head
            sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
            label(draw, x + 4, y + th + 8, p.stem, 28, DIM)
        out = SHEETS / f"SHEET-{d.name}.png"
        sheet.save(out)
        print(f"{out}  {sheet.size}  {len(cards)} cards")


def wall():
    """All 25 cards, 5 across, one industry per row."""
    tw, th = 400, 500
    cap, pad, head = 38, 12, 46
    rows = industries()
    W = 5 * (tw + pad) + pad
    H = len(rows) * (head + th + cap + pad) + pad
    sheet = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(sheet)
    for r, d in enumerate(rows):
        top = pad + r * (head + th + cap + pad)
        label(draw, pad, top, d.name.replace("-", " ").upper(), 30)
        for i, p in enumerate(sorted(d.glob("*.png"))[:5]):
            x = pad + i * (tw + pad)
            y = top + head
            sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
            label(draw, x + 4, y + th + 6, p.stem, 24, DIM)
    out = SHEETS / "WALL-industry-statics.png"
    sheet.save(out)
    print(f"{out}  {sheet.size}  {len(rows)} industries")


if __name__ == "__main__":
    SHEETS.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    if mode in ("sheets", "both"):
        sheets()
    if mode in ("wall", "both"):
        wall()
