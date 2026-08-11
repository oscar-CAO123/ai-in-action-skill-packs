#!/usr/bin/env python3
"""F-M1, the before / after split screen. Hook 1: "[Avatar]: this is the real reason you're still
[painpoint]."

    python3 build_split.py                  # every industry whose two plates are shot
    python3 build_split.py construction     # one
    python3 build_split.py --composite      # write the split image only, no band, for crop tuning

Two paid plates per industry, then everything here is free and re-runnable.

The argument is the picture, not a caption. Left is the pain, one low source, the room covered,
the face hidden by posture. Right is the same person in the same room with the light up and the
work moving, face visible behind a flat cartoon censor bar. **No BEFORE or AFTER lettering
anywhere**: you, . The light and the posture carry it.

## The two hand-set tables, and why they are hand-set

`CROP` is the usable region of each raw plate, in fractions. The `vhs-camcorder` head asks for
"a video frame, shot on tape" and this model sometimes renders a picture OF a frame: the scene
inset with dark bands around it, in defiance of the style tail's explicit ban. An automatic trim
was written and thrown away, because no brightness threshold separates a band from a tenebrist
BEFORE half. The setting that cleared the AFTER plate's bands ate 645px of the BEFORE plate's
dark room. Fourteen boxes tuned by eye, once per plate, are exact and free.

`BAR` is the censor bar over the eyes on the AFTER half, in fractions of the finished 540x1350
half. It cannot be computed: there is no face detector in this rig and the plates frame the
subject differently every time. Set it once per plate off the composite, which
`--composite` writes for exactly that purpose.

Both tables follow the pattern the house already uses for `ARROW_TARGETS` in `build_industry.py`
and the mark placement in `build_caution.py`: measure once, write it down, never guess at render
time.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from band import render_card  # noqa: E402
from magnet_copy import COPY, INDUSTRIES  # noqa: E402

PLATES = ROOT / "plates-magnet"
OUT = ROOT / "out-magnet"

W, H = 1080, 1350
HALF = W // 2
INK = (16, 16, 20)

FULL = (0.0, 0.0, 1.0, 1.0)

# (x0, y0, x1, y1) as fractions of the raw plate, plus `anchor`: where across that region the
# tall 2:5 window is centred. 0.5 is the middle of the region.
CROP = {
    "construction": {
        "before": dict(box=FULL, anchor=0.55),
        # this plate came back inset: dark blurred bands top and bottom, thin bars either side
        "after": dict(box=(0.016, 0.192, 0.983, 0.842), anchor=0.55),
    },
    "real-estate": {
        "before": dict(box=FULL, anchor=0.5),
        "after": dict(box=FULL, anchor=0.5),   # re-shot outdoors, full bleed
    },
    "hospitality": {
        "before": dict(box=FULL, anchor=0.5),
        "after": dict(box=FULL, anchor=0.5),
    },
    "retail": {
        "before": dict(box=FULL, anchor=0.5),
        "after": dict(box=FULL, anchor=0.5),
    },
    "financial-services": {
        "before": dict(box=FULL, anchor=0.5),
        "after": dict(box=FULL, anchor=0.5),
    },
    "building-services": {
        "before": dict(box=FULL, anchor=0.5),
        "after": dict(box=FULL, anchor=0.5),
    },
    "professional-services": {
        "before": dict(box=FULL, anchor=0.5),
        "after": dict(box=FULL, anchor=0.5),
    },
}

# (x0, y0, x1, y1) as fractions of the finished 540x1350 half. None means the bar has not been
# set yet, and the card renders without it so the miss is visible rather than silent.
BAR = {
    "construction": (0.20, 0.203, 0.70, 0.268),
    "real-estate": (0.30, 0.256, 0.72, 0.312),
    # re-measured off a 2x gridded head crop of each AFTER half, full size. The five
    # below were all off: financial services and professional services sat on the mouth and the
    # nose, hospitality and retail cleared the eyes but stopped short of the far one.
    "hospitality": (0.36, 0.216, 0.74, 0.252),
    "retail": (0.36, 0.285, 0.76, 0.324),
    "financial-services": (0.33, 0.334, 0.73, 0.372),
    "building-services": (0.08, 0.242, 0.56, 0.280),
    "professional-services": (0.36, 0.282, 0.71, 0.320),
}


def kicker(label, y=92, size=30):
    """The magnet name over the top of the plate, centred and letterspaced.

    Drawn twice, a soft black pass under the white pass, because the AFTER half is a daylit wall
    and a plain white label vanishes into it.
    """
    from PIL import ImageFont
    f = ImageFont.truetype(str(ROOT.parent / "assets" / "jost-300.ttf"), size)
    tw = f.getlength(label) + 0.09 * size * max(len(label) - 1, 0)
    x = W / 2 - tw / 2
    return (f'<text class="anno" font-size="{size}" x="{x:.1f}" y="{y}" '
            f'stroke="#000" stroke-width="4" stroke-opacity="0.45" fill="none">{label}</text>'
            f'<text class="anno" font-size="{size}" x="{x:.1f}" y="{y}">{label}</text>')


def half_image(plate, spec):
    """Crop to the usable region, take a 2:5 window centred on the anchor, fill 540x1350."""
    from PIL import Image
    im = Image.open(plate).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = spec["box"]
    im = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    cw, ch = im.size

    # the tallest 2:5 window that fits, centred on the anchor and clamped to the region
    win_w = min(cw, round(ch * HALF / H))
    win_h = round(win_w * H / HALF)
    if win_h > ch:
        win_h, win_w = ch, round(ch * HALF / H)
    cx = spec["anchor"] * cw
    left = round(min(max(cx - win_w / 2, 0), cw - win_w))
    top = round((ch - win_h) / 2)
    return im.crop((left, top, left + win_w, top + win_h)).resize((HALF, H), Image.LANCZOS)


def composite(key):
    from PIL import Image, ImageDraw
    specs = CROP.get(key)
    if not specs:
        return None, f"no crop set for {key}"
    paths = {h: PLATES / key / f"split-{h}.png" for h in ("before", "after")}
    missing = [h for h, p in paths.items if not p.exists]
    if missing:
        return None, f"no plate for {', '.join(missing)}"

    card = Image.new("RGB", (W, H), INK)
    card.paste(half_image(paths["before"], specs["before"]), (0, 0))
    card.paste(half_image(paths["after"], specs["after"]), (HALF, 0))

    d = ImageDraw.Draw(card)
    bar = BAR.get(key)
    if bar:
        # the censor bar is drawn, never prompt-baked, the same call the pop-art sunglasses get
        # on the news-collage cards. Flat black, hard edges, no feather.
        x0, y0, x1, y1 = bar
        d.rectangle((HALF + x0 * HALF, y0 * H, HALF + x1 * HALF, y1 * H), fill=(0, 0, 0))
    # the seam. Hard, 2px, no gutter and no rounding.
    d.rectangle((HALF - 1, 0, HALF, H), fill=(232, 232, 237))

    dst = PLATES / key / "split-composite.png"
    card.save(dst)
    return dst, "bar set" if bar else "NO BAR SET, run --composite and fill BAR"


if __name__ == "__main__":
    argv = sys.argv[1:]
    keys = [a for a in argv if not a.startswith("--")] or None
    n = 0
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        plate, note = composite(i["key"])
        if not plate:
            print(f"  {i['key']:22} SKIPPED, {note}")
            continue
        if "--composite" in argv:
            print(f"  {i['key']:22} {plate}  ({note})")
            continue
        copy = COPY["split"](i)
        out = OUT / i["key"] / "F-M1-split.png"
        # you, : the magnet goes back INTO the paragraph and the top kicker comes
        # off. `band.py` flattens the lines it is given into one justified block, so the CTA
        # arrives as the closing sentence of the same block rather than as a second tier.
        # `lift` raises the whole block off the bottom edge.
        report = render_card([copy["head"], copy["cta"] + "."], out, plate=plate,
                             theme="noir-lower", plate_full=True, plate_fade=True, lift=64)
        print(f"  {i['key']:22} {report}   {note}")
        n += 1
    print(f"\n{n} cards -> {OUT}")
