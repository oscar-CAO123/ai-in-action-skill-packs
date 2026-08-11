#!/usr/bin/env python3
"""The founder statics. a founder and Emil Juresic, real words over real frames.

    python3 build_founder.py                    # every card whose plates exist
    python3 build_founder.py --statement        # type only, no image, always renders
    python3 build_founder.py --split            # the mid-sentence split screen
    python3 build_founder.py --composite        # write the split image only, for crop tuning

Free, every run. No paid plate has ever been shot for this strand and none is planned: the
founders' own recorded footage is the plate.

## No censor bar here, and that is the point

`build_split.py` hides the BEFORE face by posture and bars the AFTER face, because those subjects
are anonymous stand-ins for the reader. **The founder is the opposite.** His face IS the proof, so
both halves are open and the card is attributed by name underneath.

## What the seam is doing

Left is Simon composed, hands together, mid-word. Right is Simon animated, both hands wide, mid-
word. Same set, same shirt, same camera, same afternoon. The seam reads as one man changing
register rather than as two photographs, which is the whole reason a matched pair is worth hunting
for in `_measure/frame_pick.py`.

## CROP is hand-set, same as everywhere else in this rig

The source is 16:9 and the halves are 2:5, so a window keeps roughly a fifth of the frame width.
Where that window sits decides whether the card is a portrait or a picture of a shoulder. There is
no face detector in this rig, so it is measured once off `--composite` and written down, exactly
as `build_split.py` does with its own table.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from band import render_card  # noqa: E402
from founder_copy import CARDS, CTA, QUOTES, attribution, quoted  # noqa: E402

PLATES = ROOT.parent / "assets" / "founders"
OUT = ROOT / "out-founder"

W, H = 1080, 1350
HALF = W // 2
INK = (16, 16, 20)

# `anchor` is where across the source frame the tall 2:5 window is centred, in fractions.
# Measured off --composite at full size, never guessed.
# Measured off a 20-column gridded copy of each source frame at full size, the same
# method `_measure/grid_eyes.py` uses on the F-M1 censor bar. Guessing put the composed half at
# 0.60 and sliced Simon's face in two at the card's left edge.
SPLIT = {
    "simon": dict(
        left=dict(plate="simon-vsl-composed.png", anchor=0.50),
        right=dict(plate="simon-vsl-open-hands.png", anchor=0.47),),
}


def window(path, anchor):
    """Take the tallest 2:5 window that fits, centred on the anchor, fill 540x1350."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    cw, ch = im.size
    win_w = min(cw, round(ch * HALF / H))
    win_h = round(win_w * H / HALF)
    if win_h > ch:
        win_h, win_w = ch, round(ch * HALF / H)
    cx = anchor * cw
    left = round(min(max(cx - win_w / 2, 0), cw - win_w))
    top = round((ch - win_h) / 2)
    return im.crop((left, top, left + win_w, top + win_h)).resize((HALF, H), Image.LANCZOS)


def composite(who):
    from PIL import Image, ImageDraw
    spec = SPLIT.get(who)
    if not spec:
        return None, f"no split set for {who}"
    paths = {s: PLATES / spec[s]["plate"] for s in ("left", "right")}
    missing = [s for s, p in paths.items if not p.exists]
    if missing:
        return None, f"no plate for {', '.join(missing)}"

    card = Image.new("RGB", (W, H), INK)
    card.paste(window(paths["left"], spec["left"]["anchor"]), (0, 0))
    card.paste(window(paths["right"], spec["right"]["anchor"]), (HALF, 0))
    # the seam. Hard, 2px, no gutter and no rounding, same as F-M1.
    ImageDraw.Draw(card).rectangle((HALF - 1, 0, HALF, H), fill=(232, 232, 237))

    dst = PLATES / f"{who}-split-composite.png"
    card.save(dst)
    return dst, "ok"


def kicker(label, y=96, size=30):
    """The attribution, set across the top of the card, letterspaced.

    It cannot live in the band. `band.py` flattens every line it is given into ONE justified
    block, so an attribution passed as a line arrives welded to the last sentence of the quote
    and the card reads as though Simon said his own name and job title out loud. The name goes
    to the top, the quote keeps the band, and the two stop competing.

    Drawn twice, a soft black pass under the white pass, because the plate behind it is a daylit
    room and plain white lettering vanishes into the far wall.

    **The size shrinks to fit.** At a fixed 30px this centred on a width wider than the card and
    silently clipped "EMIL" off the left edge, because his attribution carries two organisations.
    Measure the drawn width including the letterspacing, then step down until it clears the
    margin. Never centre on an unmeasured width; that is the same trap `clientWidth` set on the
    newspaper masthead.
    """
    from PIL import ImageFont
    margin = 64
    while size > 16:
        f = ImageFont.truetype(str(ROOT.parent / "assets" / "jost-300.ttf"), size)
        tw = f.getlength(label) + 0.09 * size * max(len(label) - 1, 0)
        if tw <= W - 2 * margin:
            break
        size -= 1
    x = W / 2 - tw / 2
    return (f'<text class="anno" font-size="{size}" x="{x:.1f}" y="{y}" '
            f'stroke="#000" stroke-width="4" stroke-opacity="0.45" fill="none">{label}</text>'
            f'<text class="anno" font-size="{size}" x="{x:.1f}" y="{y}">{label}</text>')


def build_statement(card):
    """Format 10. Type only. The safest card in the whole bank: no image, no rights exposure."""
    q = QUOTES[card["quote"]]
    out = OUT / f"{card['id']}-statement.png"
    return render_card([quoted(card["quote"]), CTA], out, theme="noir-lower",
                       overlay=kicker(attribution(q).rstrip(".").upper))


def build_split(card):
    """Format 25, founder cut. Both halves mid-sentence, both faces open."""
    q = QUOTES[card["quote"]]
    plate, note = composite(q["who"])
    if not plate:
        return None, note
    out = OUT / f"{card['id']}-split.png"
    report = render_card([quoted(card["quote"]), CTA], out,
                         plate=plate, theme="noir-lower", plate_full=True,
                         plate_fade=True, lift=64,
                         overlay=kicker(attribution(q).rstrip(".").upper))
    return report, note


if __name__ == "__main__":
    argv = sys.argv[1:]
    only = None
    if "--statement" in argv:
        only = "statement"
    if "--split" in argv:
        only = "split"

    if "--composite" in argv:
        for who in SPLIT:
            dst, note = composite(who)
            print(f"  {who:10} {dst}  ({note})")
        sys.exit(0)

    n = 0
    for card in CARDS:
        if only and card["build"] != only:
            continue
        if card["build"] == "statement":
            print(f"  {card['id']:6} {card['fmt']:28} {build_statement(card)}")
            n += 1
        elif card["build"] == "split":
            report, note = build_split(card)
            if report is None:
                print(f"  {card['id']:6} SKIPPED, {note}")
                continue
            print(f"  {card['id']:6} {card['fmt']:28} {report}   {note}")
            n += 1
    print(f"\n{n} founder cards -> {OUT}")
