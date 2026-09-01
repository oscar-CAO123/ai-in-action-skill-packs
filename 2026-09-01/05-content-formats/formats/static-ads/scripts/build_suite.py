#!/usr/bin/env python3
"""Render the suite. Batch 1 is the ten type-led formats plus the founder statement.

    python3 build_suite.py                    # every batch whose renderer exists
    python3 build_suite.py --batch 1          # one batch
    python3 build_suite.py --fmt F6           # one format, all seven industries
    python3 build_suite.py --fmt F6 construction

Free, every run. Nothing in the type-led batch needs a plate, so the whole of Batch 1 renders
from black and costs nothing.

## Which renderer a format gets

**Tier A**, `band.py`: the card is one justified block. `render_card()` flattens whatever lines it
is given into that block, which is why a format whose argument is a list cannot use it.

**Tier B**, `band_rows.py`: rows or columns inside the same 506px well. Written because
six of the ten type-led formats carry an argument that does not compress to one sentence.

`type-led/SKILL.md` section 2 used to put a four-row ceiling on Tier B and to say us-vs-them should
set as one block rather than two columns. Both were measured and both were amended by you on
: the ceiling is five (five short rows solve to 38.4px at 100% fill, which reads at
thumbnail) and the contrast shapes render as two columns (66.5px at 95% fill, larger than most
Tier A cards). The amendment and its measurements are recorded in that skill.

**These are pilots.** Every card here is copy set into the house band, which puts all type in the
bottom 506px and leaves 844px of black above it. On a plate-led format that space holds the
photograph. On a type-only format it is still an open design question and you has flagged it.
"""
import html
import os
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from band import render_card  # noqa: E402
from band_rows import TREATMENTS, render_rows  # noqa: E402
from suite_copy import BY_FMT, FORMATS, cards_for  # noqa: E402

OUT = ROOT / "out-suite"
W = 1080

# Tier A formats carry one block. They are NOT interchangeable: measured on F1, F3,
# F4 and F5 came back as one card printed four times. `band_rows.TREATMENTS` gives each its own
# weight, measure, alignment and rule so the reader can tell them apart at thumbnail, which
# `../SKILL.md` section 0 requires of every cell in this test.
TIER_A = {"F1", "F3", "F4", "F5", "F10"}

# None means no ceiling. `type-led/SKILL.md` says four; your own F6 list is five and the
# render holds, so this stays open until he rules. Set it to 4 to enforce the skill.
MAX_ROWS = None


def kicker(label, y=96, size=30):
    """Attribution across the top, letterspaced, shrunk to fit.

    Lives here rather than in the band because `band.py` flattens every line into ONE block, so
    an attribution passed as a line arrives welded to the last sentence of the quote.
    """
    from PIL import ImageFont
    margin = 64
    while size > 16:
        f = ImageFont.truetype(str(ROOT.parent / "assets" / "display-300.ttf"), size)
        tw = f.getlength(label) + 0.09 * size * max(len(label) - 1, 0)
        if tw <= W - 2 * margin:
            break
        size -= 1
    x = W / 2 - tw / 2
    return (f'<text class="anno" font-size="{size}" x="{x:.1f}" y="{y}" '
            f'stroke="#000" stroke-width="4" stroke-opacity="0.45" fill="none">{label}</text>'
            f'<text class="anno" font-size="{size}" x="{x:.1f}" y="{y}">{label}</text>')


# Formats whose cards sit on a full-bleed plate from `plates_suite.py`. A format is listed here
# and the plate is picked up per industry the moment it is on disk, so a half-shot set still
# renders: the industries with a plate get the bleed, the rest fall back to black.
PLATED = {"F1", "F3", "F4"}
PLATES = ROOT / "plates-suite"

# F3 is seven answers to one question rather than one scene seven ways, so two of its cards do
# not use the band at all. you, .
#
#   billboard  the plate IS the card. The question is printed on the board inside the photograph,
#              so there is no type to set: the only composited element is the Snapchat bar, which
#              is phone UI over the footage rather than something on the board.
#   poster     the falling-graduate geometry from `poster.py`: headline black and lowercase in
#              the top third, plate through the middle, CTA in the bottom third, plus the two
#              annotation arrows.
GEOMETRY = {
    ("F3", "real-estate"): "billboard",
    # Hospitality was the poster geometry until you saw it composited: "can we just make it the
    # text instead of the two-split, just the canonical band style with the black fade as well."
    # It now runs the ordinary plated band and only keeps its annotation layer.
}

# The Snapchat bar answers the billboard's own question. Same values as the proven
# `build_billboard.py`, which is the card this borrows from.
SNAP = {("F3", "real-estate"): "Definitely not."}

# The annotation pairs: (label, where the arrow points), as a fraction of the frame.
ANNOTATE = {
    # Anchors sit BELOW the top third. The first pass put them at 0.19 and they landed straight
    # on the headline, which owns 0 to 450px on a poster.
    # Six pains crowding in on the man in the gap, three per hand, each label sitting in its own
    # clear plaster and its arrow coming in from a different edge. Five are the hospitality pain
    # bank verbatim (`suite_pains.BY_INDUSTRY['hospitality']`); "mountains of admin" and "trying
    # to make sales" are your own wording for the two sides.
    #
    # Everything stays above y=0.62. The band's type block starts at 844px, which is 0.625, and a
    # label below that line lands in the copy.
    #
    # Labels are kept SHORT on purpose. The figure stands dead centre from x 0.42 to 0.62, and a
    # full pain-bank sentence at 34px runs about 500px, which walks a left-anchored label straight
    # into his legs and a right-anchored one into his back. Every tip lands on a hand, never on
    # bare plaster: the first pass pointed two of them into the gap below the left hand.
    # Six tails, no two of them near each other: one pair comes down from the top, one pair in
    # from the sides, one pair up from below. The two left ones and the two right ones were
    # stacked 85px apart in the last pass and read as one clump each.
    #
    # The two at the top read downward, so their labels sit above their tails. The four that read
    # upward carry `below`, which drops the label clear underneath the tail instead: you,
    # wants each of those verifiably below where its arrow starts, and a label 18px
    # ABOVE an upward tail sits right on the stroke.
    #
    # `size` exists for the two long ones. The figure stands from x 0.40 to 0.63 and a 25-letter
    # label centred at 34px walks straight into him.
    ("F3", "hospitality"): [
        # the left hand: the admin side
        dict(text="mountains of admin", tip=(0.21, 0.26), tail=(0.17, 0.13)),
        dict(text="losing time with the family", tip=(0.17, 0.36), tail=(0.20, 0.50),
             below=True, size=28),
        dict(text="rostering", tip=(0.31, 0.42), tail=(0.28, 0.56), below=True),
        # the right hand: the growth side
        dict(text="trying to make sales", tip=(0.84, 0.28), tail=(0.82, 0.13)),
        dict(text="hiring on gut feel", tip=(0.88, 0.38), tail=(0.84, 0.48), below=True),
        dict(text="everything relying on you", tip=(0.76, 0.46), tail=(0.80, 0.58),
             below=True, size=28),
    ],
    # you, : the boulder is the business, and it says so. White ink, because this one
    # lands on a black-and-white noir painting rather than on light plaster.
    ("F3", "retail"): [
        dict(text="your retail business", tip=(0.46, 0.28), tail=(0.20, 0.12), ink="#f2f2f2"),
    ],
}

# A poster fits each block on its own and a single long line solves tiny: the hospitality
# headline came back at 24px on one line, smaller than its own CTA. The break is authored.
POSTER_LINES = {
    ("F3", "hospitality"): ["could you take two weeks off right now",
                            "without your hospitality business",
                            "falling over?"],
}


def suite_plate(f, i):
    if f["id"] not in PLATED or not i:
        return None
    p = PLATES / f["id"] / f"{i['key']}.png"
    return p if p.exists else None


def snap_bar(text):
    """The Snapchat text tool: a TRANSLUCENT black band edge to edge, white regular-weight
    grotesque centred inside it. Values lifted from `build_billboard.py`, which is the card this
    borrows from, except the top: that card puts the bar below a board filling the top two
    thirds, and here the board sits lower, so the bar rides under it at 0.78."""
    scrim, top, h, pad = "rgba(0, 0, 0, 0.42)", 0.78, 0.0578, 130
    bar = round(h * 1350)
    css = (f".snap{{position:absolute;left:0;width:1080px;background:{scrim};"
           f"top:{round(top * 1350)}px;height:{bar}px;display:flex;align-items:center;"
           f"justify-content:center;padding:0 {pad}px;overflow:hidden}}"
           ".snap span{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:400;"
           "color:#fff;white-space:nowrap;line-height:1}")
    # shrink to fit rather than wrap, which is what the real tool does. AVAIL is passed in
    # because clientWidth counts the padding.
    js = (f"(function(){{var s=document.querySelector('.snap span');var size={round(bar*0.56)};"
          f"s.style.fontSize=size+'px';"
          f"while(s.scrollWidth>{1080 - 2 * pad}&&size>10){{size-=1;s.style.fontSize=size+'px';}}"
          "})();")
    return css, f'<div class="snap"><span>{html.escape(text)}</span></div>', js


def anno_svg(items):
    """Hand-drawn annotation arrows and their labels, composited over a finished plate.

    you, : the labels are drawn by the rig, never generated into the image, so the
    wording stays exact and free to change. Ink is dark because these land on light plaster.
    """
    import math
    W, H = 1080, 1350
    out = []
    for a in items:
        SIZE = a.get("size", 34)
        ink = a.get("ink", "#141414")
        tx, ty = a["tip"][0] * W, a["tip"][1] * H
        # `tail` is where the ARROW STARTS, and the label sits centred directly ON TOP of it.
        # you, : "the start of the arrow, that is where the text is placed, not
        # adjacent to the arrow but rather on top, so each of them has an end." Earlier passes
        # hung the label off to one side and ran the stroke past its shoulder, which read as one
        # long line with words parked beside it rather than as a labelled pointer.
        sx, sy = a["tail"][0] * W, a["tail"][1] * H

        # A single curved stroke. The control point bows PERPENDICULAR to the run rather than
        # sitting above both ends: an earlier version used `min(ay, ty) - 40`, which on a long
        # diagonal threw the curve out to the frame edge and back.
        mx, my = (sx + tx) / 2, (sy + ty) / 2
        dx, dy = tx - sx, ty - sy
        n = max((dx * dx + dy * dy) ** 0.5, 1)
        bow = 0.12 * n
        cx, cy = mx - dy / n * bow, my + dx / n * bow
        out.append(f'<path d="M {sx:.0f} {sy:.0f} Q {cx:.0f} {cy:.0f} {tx:.0f} {ty:.0f}"'
                   f' fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>')
        # arrowhead, rotated to the tangent at the tip, which is the line from the control point
        ang = math.degrees(math.atan2(ty - cy, tx - cx))
        out.append(f'<path d="M 0 0 L -26 -10 L -26 10 Z" fill="{ink}" '
                   f'transform="translate({tx:.0f},{ty:.0f}) rotate({ang:.0f})"/>')
        # the label, centred over the tail. `below` drops it under instead, for a tail that sits
        # at the top of the frame with no room above it.
        ly = sy + SIZE + 10 if a.get("below") else sy - 18
        out.append(f'<text x="{sx:.0f}" y="{ly:.0f}" text-anchor="middle" font-family="your display typeface" '
                   f'font-weight="300" font-size="{SIZE}" fill="{ink}">'
                   f'{html.escape(a["text"])}</text>')
    return "".join(out)


def render_special(geo, f, i, c, plate, out):
    """The two F3 cards that do not use the band."""
    if geo == "billboard":
        css, bar, js = snap_bar(SNAP[(f["id"], i["key"])])
        doc = (f'<meta charset="utf-8"><style>'
               f'*{{margin:0;padding:0;box-sizing:border-box}}'
               f'html,body{{width:1080px;height:1350px;overflow:hidden;background:#000}}'
               f'.card{{position:relative;width:1080px;height:1350px;overflow:hidden}}'
               f'.plate{{position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover}}'
               f'{css}</style>'
               f'<div class="card"><img class="plate" src="{plate.resolve().as_uri()}">'
               f'{bar}</div><script>{js}</script>')
        return shoot(doc, out)

    # poster: the falling-graduate geometry, plus the annotation layer
    from poster import render_poster
    key = (f["id"], i["key"])
    top = POSTER_LINES.get(key) or [c["head"].replace("[[", "").replace("]]", "").lower()]
    anno = anno_svg(ANNOTATE.get(key, []))
    return render_poster(top, [c["cta"].lower()], out, ground="plate", plate=plate,
                         overlay=anno)


def shoot(doc, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as fh:
        fh.write(doc)
        tmp = fh.name
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--virtual-time-budget=4000",
                    "--window-size=1080,1350", f"--screenshot={out}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    Path(tmp).unlink()
    return "composited"


def slug(f, i, c):
    if i:
        return f"{f['id']}-{i['key']}"
    return f"{f['id']}-{c.get('quote_key', 'card')}"


def build_one(f, i, c):
    out = OUT / f["id"] / f"{slug(f, i, c)}.png"
    if c.get("gated"):
        return None, c["gated"]

    # The founder statement keeps `band.py`, because its attribution is an SVG overlay across the
    # top of the frame and the band engine is the only one that carries an overlay layer.
    if c.get("quote_key"):
        over = kicker(c["kicker"].rstrip(".").upper())
        return render_card([c["head"], c["cta"]], out, theme="noir-lower", overlay=over), None

    plate = suite_plate(f, i)
    geo = GEOMETRY.get((f["id"], i["key"])) if i else None
    if geo:
        if not plate:
            return None, f"{geo} card, plate not shot"
        return render_special(geo, f, i, c, plate, out), None

    body = dict(c)
    if MAX_ROWS and isinstance(body.get("rows"), list):
        body["rows"] = body["rows"][:MAX_ROWS]
    body["numbered"] = f["id"] == "F9"               # the listicle is the only numbered shape
    anno = anno_svg(ANNOTATE.get((f["id"], i["key"]), [])) if i else ""
    return render_rows(body, out, treatment=TREATMENTS.get(f["id"]),
                       plate=plate, plate_full=bool(plate), plate_fade=bool(plate),
                       overlay=anno or None), None


if __name__ == "__main__":
    argv = sys.argv[1:]
    want_fmt = argv[argv.index("--fmt") + 1] if "--fmt" in argv else None
    want_batch = int(argv[argv.index("--batch") + 1]) if "--batch" in argv else None
    keys = [a for a in argv if not a.startswith("--") and not a.isdigit()
            and not a.startswith("F")] or None

    n = skipped = 0
    for f in FORMATS:
        if want_fmt and f["id"] != want_fmt:
            continue
        if want_batch and f["batch"] != want_batch:
            continue
        if f["batch"] != 1 and not want_fmt and not want_batch:
            continue                                  # only batch 1 has a renderer today
        print(f"\n{f['id']}  {f['name']}")
        for i, c in cards_for(f):
            if i and keys and i["key"] not in keys:
                continue
            report, gated = build_one(f, i, c)
            name = i["key"] if i else c.get("quote_key", "-")
            if gated:
                print(f"  {name:24} SKIPPED, {gated}")
                skipped += 1
                continue
            print(f"  {name:24} {report}")
            n += 1
    print(f"\n{n} cards rendered, {skipped} gated -> {OUT}")
