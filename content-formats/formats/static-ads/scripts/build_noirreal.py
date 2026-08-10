#!/usr/bin/env python3
"""Composite the ultra-realistic noir cards. Free.

    python3 build_noirreal.py

The watercolour plate sits on white cold-pressed paper and keeps its own deckled paper edge,
so it is PLACED at the top of the card rather than bled full-frame, and the type sits below it
in the paper margin in dark ink. A dark scrim would fight the medium.

Copy is the locked copy from basics.py. **One shape swap**: construction/bottleneck is
assigned `versus` in the grid, and a two-column versus cannot sit on a hero photograph, so
this runs the `callout` fill of the same pain instead. Recorded rather than silently changed.
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
PLATES = ROOT / "plates-noirreal"
OUT = ROOT / "out-noirreal"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1080, 1350

CSS = f"""
@font-face{{font-family:'your display typeface';font-weight:200;src:url('{ASSETS}/jost-200.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:300;src:url('{ASSETS}/jost-300.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:500;src:url('{ASSETS}/jost-500.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;background:var(--paper);overflow:hidden}}
:root{{--paper:#f4f2ee;--ink:#0f1020;--blue:#1269ff;--t3:rgba(15,16,32,.58)}}
.card{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--paper)}}
/* The plate is 4:5, the same ratio as the card, so it bleeds full frame and the type sits
   OVER the artwork. Legibility comes from a paper-coloured wash rather than a dark scrim: a
   dark scrim fights watercolour, a wash of the paper's own colour reads as part of it. */
.plate{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 object-position:center 22%;display:block}}
.wash{{position:absolute;inset:0;background:
 linear-gradient(180deg, rgba(244,242,238,.99) 0%, rgba(244,242,238,.97) 20%,
 rgba(244,242,238,.86) 26%, rgba(244,242,238,.40) 31%, rgba(244,242,238,0) 36%)}}
.top{{position:absolute;left:76px;right:76px;top:74px}}
.head{{font-family:'your display typeface';font-weight:300;font-size:54px;line-height:1.07;color:var(--ink);
 letter-spacing:-.008em}}
.acc{{color:var(--blue)}}
.sub{{font-family:'your display typeface';font-weight:300;font-size:23px;line-height:1.4;
 color:var(--t3);margin-top:13px}}
.cta{{display:flex;align-items:center;gap:18px;margin-top:18px}}
.cta i{{flex:1 1 auto;height:1px;background:rgba(15,16,32,.20)}}
.cta span{{flex:0 0 auto;font-family:'your display typeface';font-weight:500;font-size:16px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--ink);white-space:nowrap}}
"""


def markup(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith("[[", i):
            out.append('<span class="acc">'); i += 2
        elif s.startswith("]]", i):
            out.append("</span>"); i += 2
        else:
            out.append(html.escape(s[i])); i += 1
    return "".join(out)


# the operator, 2026-08-06: the CTA gains "to learn more", and the card runs across all five industries.
# Each head is the locked `bucket` fill for that industry's owner-bottleneck pain, straight from
# basics.py. Hospitality has no bottleneck cell, so it takes `presence`, which is the same
# argument in that industry's words: the place needs you on site for it to run.
# the operator, 2026-08-06: the hook shape for this row is now "Still dealing with [pain] as a [avatar]?".
# [avatar] is the PERSON, not the business, because "as a" needs a role. [pain] stays the pain the
# card already carried, worded in that industry's own terms so the three bottleneck cards do not
# come out word-identical.
# the operator, 2026-08-06: the pain goes FLAT across all five. The per-industry wordings were his first
# ask and his second was to drop them, so every card now runs the same line and only the avatar
# changes, which is what makes it read as one campaign rather than five separate arguments.
PAIN_FLAT = "Every decision still running through you"
PAIN = {
    "construction": (PAIN_FLAT, "a construction business owner"),
    "real-estate": (PAIN_FLAT, "a real estate business owner"),
    "hospitality": (PAIN_FLAT, "a hospitality business owner"),
    "retail": (PAIN_FLAT, "a retail business owner"),
    "financial-services": (PAIN_FLAT, "an insurance business owner"),
}

BUCKET = {
    "construction": ("Aussie construction businesses", "run every decision through the owner"),
    "real-estate": ("Aussie real estate agencies", "run every decision through the principal"),
    "hospitality": ("Aussie hospitality businesses", "be on site for it to run"),
    "retail": ("Aussie retailers", "run every decision through the owner"),
    # the operator, 2026-08-06: "build the automation themselves" is not what house targets a broker
    # on. Swapped to the `admin` bucket, which is the pain this picture actually argues:
    # the owner at ease while the work carries on without him.
    "financial-services": ("Aussie insurance brokers", "drown in paperwork"),
}
MAGNET = {"construction": "Take the Site-to-Profit Readiness Check",
          "real-estate": "Take the AI-Ready Agency Score",
          "hospitality": "Take the Wow Factor Audit",
          "retail": "Take the Retail Ops AI Readiness Check",
          "financial-services": "Take the Broker and Adviser AI Readiness Check"}

_pain, _who = PAIN["construction"]
CARDS = {
    "bottleneck": dict(
        plate="bottleneck-illus-finished.png",
        head=f"[[{_pain}]] as {_who}?",
        sub="One hire. That is the whole change.",
        cta="Take the Site-to-Profit Readiness Check to learn more"),
}

for _ind in ("real-estate", "hospitality", "retail", "financial-services"):
    _pain, _who = PAIN[_ind]
    CARDS[f"bottleneck-{_ind}"] = dict(
        plate=f"bottleneck-illus-{_ind}.png",
        head=f"[[{_pain}]] as {_who}?",
        sub="One hire. That is the whole change.",
        cta=f"{MAGNET[_ind]} to learn more")


def build(key):
    c = CARDS[key]
    p = PLATES / c["plate"]
    if not p.exists():
        print(f"  skip {key}: no plate at {p}")
        return
    doc = (f'<meta charset="utf-8"><style>{CSS}</style><div class="card">'
           f'<img class="plate" src="{p.resolve().as_uri()}"><div class="wash"></div>'
           f'<div class="top"><div class="head">{markup(c["head"])}</div>'
           f'<div class="sub">{html.escape(c["sub"])}</div>'
           f'<div class="cta"><span>{html.escape(c["cta"])}</span><i></i></div></div></div>')
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc); tmp = f.name
    png = OUT / f"{key}.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    f"--screenshot={png}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    Path(tmp).unlink()
    print(f"  {png}")


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(CARDS)):
        build(k)
