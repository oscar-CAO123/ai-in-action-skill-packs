#!/usr/bin/env python3
"""Composite the white-ground noir cards. Free, headless Chrome.

    python3 build_white.py            # both
    python3 build_white.py admin      # one

Layout, the operator's direction 2026-08-06: hook as top text, the CTA directly under it as a thin
line across the middle of the page, and the painted plate filling the bottom. White ground,
`--light-text` on `#fff`, one blue accent, your display typeface only.

The arrow and its label are drawn HERE as SVG, never generated inside the plate, so the
lettering is legible, correctly spelled and editable. Plates come from plates_white.py.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
PLATES = ROOT / "plates-white"
OUT = ROOT / "out-white"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1080, 1350

CSS = f"""
@font-face{{font-family:'your display typeface';font-weight:200;src:url('{ASSETS}/jost-200.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:300;src:url('{ASSETS}/jost-300.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:500;src:url('{ASSETS}/jost-500.ttf')}}
:root{{--ink:#0f1020;--blue:#1269ff;--rule:rgba(15,16,32,.16);--t3:rgba(15,16,32,.55);--ground:#f5f7f6}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;background:var(--ground);overflow:hidden}}
.card{{position:relative;width:{W}px;height:{H}px;background:var(--ground);overflow:hidden}}
.top{{position:absolute;left:84px;right:84px;top:92px}}
.head{{font-family:'your display typeface';font-weight:300;font-size:76px;line-height:1.08;color:var(--ink);
 letter-spacing:-.005em}}
.acc{{color:var(--blue)}}
.sub{{font-family:'your display typeface';font-weight:300;font-size:27px;line-height:1.4;color:var(--t3);
 margin-top:20px}}
/* the CTA is one thin line across the middle, rules either side of it */
/* the operator, 2026-08-06: blow the lead-magnet line up. It was 17px, which is smaller than the sub
   it sits under, so the one thing the card asks the reader to DO read as a footnote. Tracking
   comes down with the size going up, because the longest magnet name (the broker and adviser
   one, 45 characters) has to stay on one line inside the 912px column. */
.cta{{display:flex;align-items:center;gap:20px;margin-top:34px}}
.cta i{{flex:1 1 auto;height:1px;background:var(--rule);min-width:0}}
.cta span{{flex:0 0 auto;font-family:'your display typeface';font-weight:500;font-size:28px;letter-spacing:.08em;
 text-transform:uppercase;color:var(--ink);white-space:nowrap}}
/* the painted plate fills the bottom. Its own ground is white, so the join is invisible. */
.plate{{position:absolute;left:0;bottom:0;width:{W}px;display:block}}
.overlay{{position:absolute;left:0;top:0;pointer-events:none}}
.lbl{{font-family:'your display typeface';font-weight:500;font-size:26px;letter-spacing:.03em;fill:var(--blue)}}
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


# An arrow entering from above and landing on the centre figure, plus its label. Drawn in the
# locked line-art language: one stroke weight, no icon set.
def arrow_down(x, y_from, y_to, label, label_x, label_y, anchor="end"):
    return (f'<path d="M{x} {y_from} L{x} {y_to}" stroke="#1269ff" stroke-width="3" fill="none"/>'
            f'<path d="M{x-13} {y_to-18} L{x} {y_to} L{x+13} {y_to-18}" stroke="#1269ff" '
            f'stroke-width="3" fill="none" stroke-linejoin="round"/>'
            f'<text class="lbl" x="{label_x}" y="{label_y}" text-anchor="{anchor}">'
            f'{html.escape(label)}</text>')


# the operator, 2026-08-06: both white cards run across all five industries. The painting is the same
# set and the same figures every time, shot from a different camera angle, so the set reads as one
# campaign and only the words change. Nouns are the locked ones from basics.py (`short`), which is
# why real estate says "agency" and financial services says "brokerage" rather than "business".
SHORT = {"construction": "construction business", "real-estate": "agency",
         "hospitality": "hospitality business", "retail": "retail business",
         "financial-services": "brokerage"}
WHO = {"construction": "Aussie construction businesses",
       "real-estate": "Aussie real estate agencies",
       "hospitality": "Aussie hospitality businesses", "retail": "Aussie retailers",
       "financial-services": "Aussie insurance brokers"}
MAGNET = {"construction": "Take the Site-to-Profit Readiness Check",
          "real-estate": "Take the AI-Ready Agency Score",
          "hospitality": "Take the Wow Factor Audit",
          "retail": "Take the Retail Ops AI Readiness Check",
          "financial-services": "Take the Broker and Adviser AI Readiness Check"}
# The wrong fix each industry reaches for, verbatim from basics.py. Real estate's is the operator's own
# wording from 2026-08-06 ("another admin staff member"), not the basics.py fill.
# the operator, 2026-08-06: hospitality and retail move off their basics.py fills onto the same
# shape as the others. "Put a part-timer on it" was not the same kind of wrong fix as the
# rest, and "to grow" was surplus on retail.
WRONG = {"construction": "hire more admin staff", "real-estate": "hire another admin staff member",
         "hospitality": "hire another staff member", "retail": "hire more staff",
         "financial-services": "hire a bigger back office"}

# Where the two figures actually stand, per card, as x in the 1080 frame. Read off each rendered
# plate: the camera moved for every industry, so a single hardcoded pair of arrows lands on a
# cubicle wall instead of a head. (consultant, chief agent officer).
VERSUS_X = {
    "versus": (220, 703),
    "versus-construction": (302, 832),
    "versus-hospitality": (262, 800),
    "versus-retail": (86, 896),
    "versus-financial-services": (324, 700),
}
ADMIN_X = {"admin": 540, "admin-construction": 540, "admin-hospitality": 518,
           "admin-retail": 541, "admin-financial-services": 542}


def versus_overlay(cx, kx):
    """The two labelled arrows, placed on whichever x each figure ended up at."""
    def one(x, label, colour):
        lx = min(max(x, 118), 962)               # keep the label off both margins
        return (f'<text class="lbl" x="{lx}" y="694" text-anchor="middle" '
                f'style="fill:{colour}">{html.escape(label)}</text>'
                f'<path d="M{x} 712 L{x} 762" stroke="{colour}" stroke-width="3"/>'
                f'<path d="M{x-11} 746 L{x} 762 L{x+11} 746" stroke="{colour}" stroke-width="3" '
                f'fill="none" stroke-linejoin="round"/>')
    return one(cx, "A consultant", "rgba(15,16,32,.55)") + one(kx, "A the role you place",
                                                               "#1269ff")


CARDS = {
    "admin": dict(
        plate="admin-row.png",
        head="Aussie real estate agencies. Please don't "
             "[[hire another admin staff member]] before doing this.",
        sub="You are scaling the problem.",
        cta="Take the AI-Ready Agency Score",
        # the centre figure sits dead centre of the plate
        overlay=arrow_down(540, 712, 812, "Your the role you place", 512, 690, "end"),
    ),
    "versus": dict(
        plate="versus-operators.png",
        head="Stop trying to use AI in your [[agency]] without doing this first.",
        sub="",     # the operator 2026-08-06: the sub goes, on every versus card

        cta="Take the AI-Ready Agency Score",
        overlay=versus_overlay(*VERSUS_X["versus"]),
    ),
}

# The other four industries of each card, filled from the tables above. Real estate keeps the two
# hand-written entries as the reference build; nothing here overwrites them.
for _ind in ("construction", "hospitality", "retail", "financial-services"):
    CARDS[f"admin-{_ind}"] = dict(
        plate=f"admin-row-{_ind}.png",
        head=f"{WHO[_ind]}. Please don't [[{WRONG[_ind]}]] before doing this.",
        sub="You are scaling the problem.", cta=MAGNET[_ind],
        overlay=arrow_down(ADMIN_X[f"admin-{_ind}"], 712, 812,
                           "Your the role you place",
                           ADMIN_X[f"admin-{_ind}"] - 28, 690, "end"))
    CARDS[f"versus-{_ind}"] = dict(
        plate=f"versus-operators-{_ind}.png",
        head=f"Stop trying to use AI in your [[{SHORT[_ind]}]] without doing this first.",
        sub="", cta=MAGNET[_ind],
        overlay=versus_overlay(*VERSUS_X[f"versus-{_ind}"]))


def build(key):
    c = CARDS[key]
    p = PLATES / c["plate"]
    if not p.exists():
        print(f"  skip {key}: no plate at {p}")
        return
    # An empty sub renders nothing at all, rather than an empty div still carrying its margin.
    sub = f'<div class="sub">{html.escape(c["sub"])}</div>' if c["sub"] else ""
    doc = (f'<meta charset="utf-8"><style>{CSS}</style><div class="card">'
           f'<img class="plate" src="{p.resolve().as_uri()}">'
           f'<div class="top"><div class="head">{markup(c["head"])}</div>{sub}'
           f'<div class="cta"><span>{html.escape(c["cta"])}</span><i></i></div></div>'
           f'<svg class="overlay" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'{c["overlay"]}</svg></div>')
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
