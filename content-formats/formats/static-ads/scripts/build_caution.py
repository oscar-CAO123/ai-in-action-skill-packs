#!/usr/bin/env python3
"""F-M5, the caution card. Hook 5: "[avatar]. Please be careful. Do not touch AI before this audit."

    python3 build_caution.py                 # every industry with a plate on disk
    python3 build_caution.py construction    # one
    python3 build_caution.py --marks         # print which mark each industry gets

FREE for the five industries whose VHS plate is already shot. Building Services and Professional
Services need one plate each; `plates_magnet.py --fmt caution` carries those two briefs.

This is the canonical news-carousel card: plate y0 to 844, band y844 to 1350, `noir` theme, ALL
CAPS, `band.py` doing the fit. the operator, 2026-08-06: this is the one format in the lead-magnet set
that keeps caps, because it IS the news-carousel format and it is the control the other four are
judged against.

**One deliberate deviation, recorded rather than silent.** the operator cut the leader-arrow annotation
off the industry statics on 2026-08-06, which put those cards under "nothing is drawn over the
plate". This card draws over the plate on purpose: an AI emblem with a caution mark across it is
the whole format. The magnet rides underneath it as a plain centred label with no leader line,
which is the lightest way to name the asset without reviving the arrow.

The emblem is DRAWN, never generated. A model asked for a hazard sign over a laptop returns a
warped sign with invented lettering on it, and the plate underneath is already paid for.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
NEWS = ROOT.parents[1] / "news-carousel" / "scripts"

from band import render_card  # noqa: E402
from magnet_copy import COPY, INDUSTRIES  # noqa: E402

PLATES_REAL = NEWS / "plates-real"
OUT = ROOT / "out-magnet"
ASSETS = ROOT.parent / "assets"

W, PLATE_H = 1080, 844
BLUE = "#1269FF"

# the operator, 2026-08-06, second pass: **the laptop is gone, the mark is much larger, everything is
# centred and symmetrical, and it centres on the PLATE AREA, not the whole card.** The plate runs
# y0 to 844, so the mark's centre is y=422 and not the card's own 675. Nothing tilts and nothing
# is offset, so the only thing that varies between industries is which mark the card carries.
CX, CY = W / 2, PLATE_H / 2

# One scale per mark, not one for both. The triangle's local box is 156 units tall and the X's
# is 192, so a shared scale draws the X a quarter larger than the triangle: it ran into the
# magnet label at the foot of the plate and touched the top edge of the frame. These two numbers
# land both marks at the same 530px optical height.
MARK_SCALE = {"hazard": 3.4, "cross": 2.76}

LOOK = {
    "construction":          dict(mark="hazard"),
    "real-estate":           dict(mark="cross"),
    "hospitality":           dict(mark="hazard"),
    "retail":                dict(mark="cross"),
    "financial-services":    dict(mark="hazard"),
    "building-services":     dict(mark="cross"),
    "professional-services": dict(mark="hazard"),
}


def hazard():
    """The standard warning triangle with the bar and dot. Drawn in a local box centred on the
    origin and scaled up at draw time, so the stroke weights below are pre-scale: at SCALE 3.4
    a 7 becomes a 24px line on the card."""
    return (
        f'<path d="M0 -78 L92 78 L-92 78 Z" fill="#0B0B0F" fill-opacity="0.66" '
        f'stroke="#fff" stroke-width="7" stroke-linejoin="round"/>'
        f'<rect x="-8" y="-26" width="16" height="62" rx="8" fill="#fff"/>'
        f'<circle cx="0" cy="55" r="9" fill="#fff"/>')


def cross():
    """A heavy hand-cut X. Two bars, not a glyph, so it holds at thumbnail size."""
    return (
        f'<path d="M-96 -96 L96 96" stroke="#fff" stroke-width="16" '
        f'stroke-linecap="square"/>'
        f'<path d="M96 -96 L-96 96" stroke="#fff" stroke-width="16" '
        f'stroke-linecap="square"/>')


MARKS = {"hazard": hazard, "cross": cross}


def overlay(industry, look):
    """The mark plus the magnet label, both centred on the plate area.

    The mark is drawn twice, a soft black pass under the white pass, the same trick
    `build_industry.arrow_overlay` uses: these plates are VHS and a pure white line disappears
    wherever the tape blows a highlight out.
    """
    from PIL import ImageFont
    label = COPY["caution"](industry)["anno"]
    f = ImageFont.truetype(str(ASSETS / "jost-300.ttf"), 30)
    tw = f.getlength(label) + 0.09 * 30 * max(len(label) - 1, 0)

    g = MARKS[look["mark"]]()
    s = MARK_SCALE[look["mark"]]
    return (
        f'<g opacity="0.5" transform="translate({CX + 4},{CY + 4}) scale({s * 1.015})" '
        f'stroke="#000">{g}</g>'
        f'<g transform="translate({CX},{CY}) scale({s})">{g}</g>'
        f'<text class="anno" font-size="30" x="{W / 2 - tw / 2:.1f}" y="{PLATE_H - 52}">'
        f'{label}</text>')


def plate_for(industry):
    """The industry's VHS plate. Five reuse a keeper already shot for the news-carousel statics;
    Building Services and Professional Services have no keeper, so they get one shot into this
    set's own plate folder by `plates_magnet.py <industry> caution --go`."""
    if industry["plate"]:
        p = PLATES_REAL / industry["plate"]
        if p.exists():
            return p
    own = ROOT / "plates-magnet" / industry["key"] / "caution-plate.png"
    return own if own.exists() else None


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--marks" in argv:
        for k, v in LOOK.items():
            print(f"  {k:22} {v['mark']}  at ({v['cx']},{v['cy']})  "
                  f"scale {v['scale']}  tilt {v['tilt']}")
        sys.exit(0)
    keys = [a for a in argv if not a.startswith("--")] or None
    n = skipped = 0
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        plate = plate_for(i)
        if not plate:
            print(f"  {i['key']:22} SKIPPED, no plate. "
                  f"Shoot it: python3 plates_magnet.py {i['key']} caution --go")
            skipped += 1
            continue
        copy = COPY["caution"](i)
        out = OUT / i["key"] / "F-M5-caution.png"
        report = render_card(copy["lines"], out, plate=plate, theme="noir",
                             overlay=overlay(i, LOOK[i["key"]]))
        print(f"  {i['key']:22} {LOOK[i['key']]['mark']:6} {report}")
        n += 1
    print(f"\n{n} cards, {skipped} waiting on a plate -> {OUT}")
