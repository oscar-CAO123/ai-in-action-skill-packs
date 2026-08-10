#!/usr/bin/env python3
"""Render the single-card industry pain statics.

    python3 build_industry.py                     # every card, reusing plates already on disk
    python3 build_industry.py construction-and-trades
    python3 build_industry.py --plates            # generate ONLY the missing new plates, then stop

Cards land in `out-industry/<industry>/<pain-slug>.png`.

Plate policy. A card whose `plate` names an existing noir deck reuses that deck's wordless
`slide-01` straight off disk, so the whole set costs nothing to re-render. A card whose
`plate` starts with `industry-` has no plate on disk and gets one paid nano_banana_pro job,
dispatched one at a time and downloaded before the next is sent, exactly as `plates_noir.py`
does it. Those land in `plates-noir/<plate>/slide-01.png` and are reused from then on.

Band: the `noir` theme, thin your display typeface, same as the carousels. No annotations, no overlay.
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "static-ads" / "scripts"))
from band import render_card  # noqa: E402
from decks_industry import (INDUSTRY_STATICS, NEW_PLATES, anno_label,  # noqa: E402
                            band_lines)
from decks_noir import LIGHT, STYLE  # noqa: E402

HF = "/opt/homebrew/bin/higgsfield"
PLATES = ROOT / "plates-noir"
REAL = ROOT / "plates-real"
OUT = ROOT / "out-industry"

# Card space is 1080x1350; the plate fills y 0..844 and the band starts at 844.
W, PLATE_H = 1080, 844
BASE = 792            # annotation baseline, in the black the plate fades into
RISER = 706           # height the leader climbs before it turns toward the subject
# 30px, not the 25px the `.anno` class sets. That size was for three station labels sharing a
# baseline; here one label carries the whole CTA, so it takes the room.
FONT_PX = 30
TRACKING = 0.09       # em, matches the .anno class in band.py
FONT = (ROOT.parents[3] / "content-formats" / "formats" / "static-ads" / "assets"
        / "jost-300.ttf")


def generate(prompt, dest, tries=4):
    """Dispatch ONE paid still and download it. Blocks until the job finishes."""
    for attempt in range(1, tries + 1):
        r = subprocess.run(
            [HF, "generate", "create", "nano_banana_pro", "--aspect_ratio", "5:4",
             "--resolution", "2k", "--prompt", prompt, "--wait", "--json"],
            capture_output=True, text=True)
        if r.returncode == 0 and "[" in r.stdout:
            url = json.loads(r.stdout[r.stdout.index("["):])[0]["result_url"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url, dest)
            return url
        print(f"   attempt {attempt} failed (exit {r.returncode}), retrying", flush=True)
        time.sleep(15 * attempt)
    raise RuntimeError(f"generation failed after {tries} attempts: {dest}")


# Hand-set arrow targets, in card space (1080x1350, plate is y 0..844). `subject_point` aims at the
# brightest paint, which is right on a tenebrist plate and wrong on a real-world one whenever the
# brightest thing in frame is a window rather than the subject. Override here when it misses.
ARROW_TARGETS = {
    # The window is the brightest thing in the room; the pain is the empty second desk.
    ("construction-and-trades", "headcount"): (620, 355),
}


def subject_point(png):
    """Where on the card the arrow should land: the centre of mass of the plate's lit subject.

    These plates are tenebrist, so the painted subject IS the bright region and everything else
    falls to black. Take the brightest pixels and average them. Done on the card's coordinates,
    not the source file's, because the plate is drawn `object-fit: cover` into 1080x844 and is
    cropped on the way in.

    Set by measurement rather than by eye because there are 25 of them, then checked on the
    contact sheet. Override by hand if one lands on a dark patch.
    """
    from PIL import Image
    im = Image.open(png).convert("L")
    w, h = im.size
    s = max(W / w, PLATE_H / h)
    off_x, off_y = (W - w * s) / 2, (PLATE_H - h * s) / 2

    small = im.resize((120, int(120 * h / w)))
    px = list(small.getdata())
    sw, sh = small.size
    # Ignore the bottom third: the plate fades to black there and the label already sits in it.
    live = [(i % sw, i // sw, v) for i, v in enumerate(px) if i // sw < sh * 0.68]
    cut = sorted(v for _, _, v in live)[int(len(live) * 0.93)]
    hot = [(x, y) for x, y, v in live if v >= cut]
    cx = sum(x for x, _ in hot) / len(hot) * (w / sw)
    cy = sum(y for _, y in hot) / len(hot) * (h / sh)

    tx = min(max(cx * s + off_x, 150), W - 150)
    ty = min(max(cy * s + off_y, 120), 600)
    return round(tx), round(ty)


def arrow_overlay(label, target):
    """The CTA as a leader arrow: a centred your display typeface label under the plate, a hairline rising out
    of it, and an arrowhead landing on the painted subject."""
    from PIL import ImageFont
    f = ImageFont.truetype(str(FONT), FONT_PX)
    tw = f.getlength(label) + TRACKING * FONT_PX * max(len(label) - 1, 0)
    lx = W / 2
    tx, ty = target

    # Stop the head just short of the subject so the point reads as aiming at it, not sitting on it.
    dx, dy = tx - lx, ty - RISER
    seg = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / seg, dy / seg
    hx, hy = tx - ux * 12, ty - uy * 12
    head, spread = 26, 0.40
    # Two barbs, splayed off the shaft direction. The shaft stops at the head's back edge so
    # the line never prints through the solid triangle.
    back = (hx - ux * head, hy - uy * head)
    b1 = (back[0] - uy * head * spread, back[1] + ux * head * spread)
    b2 = (back[0] + uy * head * spread, back[1] - ux * head * spread)

    shaft = f"M{lx:.1f} {BASE - 38} L{lx:.1f} {RISER} L{back[0]:.1f} {back[1]:.1f}"
    tri = f"M{hx:.1f} {hy:.1f} L{b1[0]:.1f} {b1[1]:.1f} L{b2[0]:.1f} {b2[1]:.1f} Z"

    # The arrow is white and, by construction, it points at the brightest paint in the frame,
    # so on its own the head disappears into the lit subject it is naming. Everything is drawn
    # twice: a soft black pass underneath carries it over the highlights, the white pass on top
    # carries it over the crushed blacks.
    return (
        f'<text class="anno" font-size="{FONT_PX}" x="{lx - tw / 2:.1f}" y="{BASE}">{label}</text>'
        f'<path d="{shaft}" fill="none" stroke="#000" stroke-width="4.6" stroke-opacity="0.5"/>'
        f'<path d="{tri}" fill="none" stroke="#000" stroke-width="4.6" stroke-opacity="0.5" '
        f'stroke-linejoin="round"/>'
        f'<path d="{shaft}" fill="none" stroke="#fff" stroke-width="1.7" stroke-opacity="0.85"/>'
        f'<path d="{tri}" fill="#fff" fill-opacity="0.95"/>')


def plate_path(name, industry=None, slug=None):
    """The real-world plate if one has been shot, otherwise the painted noir plate.

    `plates-real/<industry>/<slug>.png` is canonical as of 2026-08-06: the operator replaced the painted
    noir plates with real-world captures shot by `plates_real.py`. The noir path stays as the
    fallback so an industry that has not been shot yet still renders.
    """
    if industry and slug:
        real = REAL / industry / f"{slug}.png"
        if real.exists():
            return real
    folder = name if name.startswith("industry-") else f"noir-pain-{name}"
    return PLATES / folder / "slide-01.png"


def ensure_plates():
    """Generate any `industry-` plate that is not on disk yet. One paid job at a time."""
    missing = [n for n in NEW_PLATES if not plate_path(n).exists()]
    if not missing:
        print("all plates present, nothing to generate")
        return
    print(f"{len(missing)} plate(s) to generate, one at a time")
    for name in missing:
        print(f"{name}  generating ...", flush=True)
        generate(f"{STYLE} {NEW_PLATES[name]} {LIGHT}", plate_path(name))
        print(f"{name}  done", flush=True)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--plates" in sys.argv:
        ensure_plates()
        return
    ensure_plates()
    only = set(args)
    for deck in INDUSTRY_STATICS:
        if only and deck["industry"] not in only:
            continue
        print(f"=== {deck['industry']} ===")
        out = OUT / deck["industry"]
        for card in deck["cards"]:
            plate = plate_path(card["plate"], deck["industry"], card["slug"])
            if not plate.exists():
                print(f"{card['slug']}  SKIPPED, no plate at {plate}")
                continue
            # No overlay. the operator cut the leader-arrow annotation on 2026-08-06, which puts these
            # cards back under section 2c: nothing is drawn over the plate. `arrow_overlay`,
            # `subject_point` and `ARROW_TARGETS` stay on disk with the rest of the annotation
            # machinery and are not canonical; reviving them needs the operator's go again.
            report = render_card(band_lines(deck["industry"], card),
                                 out / f"{card['slug']}.png", plate=plate, theme="noir")
            print(f"{card['slug']:18} {report}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
