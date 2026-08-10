#!/usr/bin/env python3
"""The review sheet for ONE format: every industry side by side with its treatment named. FREE.

    python3 sheet_fmt.py F3          # -> out-suite/F3/_F3-composite.png, then opens it

This is the surface the operator reviews a format from, and it was rebuilt by hand for F1 and F3. Every
format from F4 on gets the same sheet, so it lives here instead of being retyped.

Four across at 600px on the suite's own black, industry under each card, plus the treatment note
where the format has one. A card with no render yet is drawn as an empty outline rather than
skipped, so a hole in the set is visible instead of invisible.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from suite_copy import BY_FMT, INDUSTRIES  # noqa: E402
import refs  # noqa: E402

OUT = ROOT / "out-suite"
FONT = ROOT.parent / "assets" / "jost-300.ttf"
COLS, W, GAP, PAD, BG = 3, 640, 36, 40, (18, 18, 18)
REF_W, REF_H = 260, 200          # the reference strip's thumbnails

# What each card's picture actually is, in the operator's words where he named it. Only formats whose
# cards differ from each other need an entry: a format that is one scene seven ways does not.
NOTES = {
    "F3": {
        "construction": "matrix pills",
        "real-estate": "billboard + snap",
        "hospitality": "fresco + 6 arrows",
        "retail": "noir burden",
        "financial-services": "70s corner office",
        "building-services": "the ute at 9pm",
        "professional-services": "marble atlas, cracked",
    },
    # One scene seven ways, so the note is the role that gets struck out on each page.
    "F4": {k: v.lower() for k, v in __import__("plates_suite").F4_ROLES.items()},
}


def references(fmt):
    """The bank entries this format is modelled on, resolved. the operator, 2026-08-10: a generation is
    never shown without the thing it was modelled on sitting next to it."""
    out = []
    for ref, takes in BY_FMT[fmt]["model"]:
        try:
            out.append({**refs.resolve(ref), "takes": takes})
        except KeyError:
            out.append(dict(ref=ref, title="DEAD REFERENCE", image=None, takes=takes))
    return out


def fit(d, text, font, width):
    """Truncate to the MEASURED column width. A character count does not hold: "the checklist
    static" fitted and "The "if you've ever" symptom stack" ran into the next column."""
    if d.textlength(text, font=font) <= width:
        return text
    while text and d.textlength(text + "...", font=font) > width:
        text = text[:-1]
    return text.rstrip() + "..."


def wrap(d, text, font, width, max_lines=4):
    """Greedy wrap to the measured column width. The last line truncates rather than overflowing."""
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if d.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = w
        if len(lines) == max_lines:
            break
    if line and len(lines) < max_lines:
        lines.append(line)
    if len(lines) == max_lines and len(" ".join(lines).split()) < len(words):
        lines[-1] = fit(d, lines[-1] + " ...", font, width)
    return lines


TAKES_LINES = 4


def row_height(entries, lead):
    """Picture rows carry the thumbnail; prose rows do not. Both then carry the principle, which
    is the half the operator actually reads, so it is measured rather than assumed."""
    top = (REF_H + 34) if any(e.get("image") for e in entries) else 62
    return top + TAKES_LINES * lead + 24


def ref_strip(d, im, entries, x0, y0, width, label, small, tiny):
    """The reference strip: what this format is drawn from, and what is taken from each entry.
    Image banks show the picture, prose banks show the id and title, and every one carries its
    principle underneath. the operator, 2026-08-10: a near match is fine as long as the principle is
    named, so the principle is the part that may never be dropped."""
    lead = 26
    d.text((x0, y0), "MODELLED ON", font=small, fill=(120, 120, 120))
    row_h = row_height(entries, lead)
    top = row_h - TAKES_LINES * lead - 24
    y = y0 + 30
    x = x0
    for e in entries:
        img = e.get("image")
        if img and Path(img).suffix.lower() != ".svg":
            thumb = Image.open(img).convert("RGB")
            thumb.thumbnail((REF_W, REF_H), Image.LANCZOS)
            im.paste(thumb, (x, y))
            d.text((x, y + thumb.height + 8), e["ref"], font=small, fill=(190, 190, 190))
        else:
            d.text((x, y), e["ref"], font=label, fill=(190, 190, 190))
            d.text((x, y + 32), fit(d, e["title"], small, REF_W - 12), font=small,
                   fill=(125, 125, 125))
        for n, ln in enumerate(wrap(d, e.get("takes", ""), tiny, REF_W - 12, TAKES_LINES)):
            d.text((x, y + top + n * lead), ln, font=tiny, fill=(150, 150, 150))
        x += REF_W + GAP
        if x + REF_W > x0 + width:
            x = x0
            y += row_h
    return (y + row_h) - y0


def sheet(fmt):
    notes = NOTES.get(fmt, {})
    label = ImageFont.truetype(str(FONT), 26)
    small = ImageFont.truetype(str(FONT), 21)
    cards = []
    for i in INDUSTRIES:
        p = OUT / fmt / f"{fmt}-{i['key']}.png"
        cards.append((i, p if p.exists() else None))

    tiny = ImageFont.truetype(str(FONT), 19)
    entries = references(fmt)
    h = round(W * 1350 / 1080)
    rows = -(-len(cards) // COLS)
    sheet_w = PAD * 2 + COLS * W + (COLS - 1) * GAP
    per_row = max(1, (sheet_w - PAD * 2) // (REF_W + GAP))
    head_h = 30 + (-(-len(entries) // per_row)) * row_height(entries, 26) + 24
    sheet_h = PAD * 2 + head_h + rows * (h + 46) + (rows - 1) * GAP
    im = Image.new("RGB", (sheet_w, sheet_h), BG)
    d = ImageDraw.Draw(im)
    ref_strip(d, im, entries, PAD, PAD, sheet_w - PAD * 2, label, small, tiny)

    for n, (ind, path) in enumerate(cards):
        x = PAD + (n % COLS) * (W + GAP)
        y = PAD + head_h + (n // COLS) * (h + 46 + GAP)
        if path:
            im.paste(Image.open(path).convert("RGB").resize((W, h), Image.LANCZOS), (x, y))
        else:
            d.rectangle([x, y, x + W, y + h], outline=(70, 70, 70), width=2)
            d.text((x + W / 2, y + h / 2), "no render", font=label, fill=(120, 120, 120),
                   anchor="mm")
        name = ind["paper"]
        note = notes.get(ind["key"], "")
        d.text((x, y + h + 14), name, font=label, fill=(200, 200, 200))
        if note:
            d.text((x + d.textlength(name, font=label) + 18, y + h + 14), note, font=label,
                   fill=(125, 125, 125))

    dst = OUT / fmt / f"_{fmt}-composite.png"
    im.save(dst)
    print(f"{len([c for c in cards if c[1]])}/{len(cards)} cards -> {dst}")
    return dst


if __name__ == "__main__":
    for f in sys.argv[1:] or ["F3"]:
        subprocess.run(["open", "-a", "Preview", str(sheet(f))])
