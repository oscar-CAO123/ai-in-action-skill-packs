#!/usr/bin/env python3
"""Composite the retro VSL cards: bold type over a full-bleed warm plate. Free.

    python3 build_retro.py              # all
    python3 build_retro.py double-handling

Shape taken from the `@aipbi` reference the operator sent, adapted to the locked system: heavy
display type sitting over a warm photographic ground, the claim doing the work, one blue
accent, your display typeface only. **The reference images were never visible** (Instagram blocks Firecrawl,
Apify quota exhausted), so the look is built from the caption plus the operator's description and is
unverified against the original.

Legibility over a photograph is the whole problem here, so the plate carries a dark scrim
under the type. Copy is the locked copy from basics.py, unchanged.
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
PLATES = ROOT / "plates-retro"
OUT = ROOT / "out-retro"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1080, 1350

CSS = f"""
@font-face{{font-family:'your display typeface';font-weight:200;src:url('{ASSETS}/jost-200.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:300;src:url('{ASSETS}/jost-300.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:500;src:url('{ASSETS}/jost-500.ttf')}}
:root{{--blue:#1269ff}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;background:#000;overflow:hidden}}
.card{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.plate{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
/* the scrim is what makes type legible over a warm photograph. Top-weighted so the
   subject in the lower half stays readable as a picture. */
.scrim{{position:absolute;inset:0;background:
 linear-gradient(180deg, rgba(6,4,2,.86) 0%, rgba(6,4,2,.62) 34%, rgba(6,4,2,.10) 58%,
 rgba(6,4,2,.34) 84%, rgba(6,4,2,.72) 100%)}}
.top{{position:absolute;left:76px;right:76px;top:84px}}
.head{{font-family:'your display typeface';font-weight:300;font-size:82px;line-height:1.06;color:#fff;
 letter-spacing:-.01em;text-shadow:0 2px 30px rgba(0,0,0,.45)}}
.acc{{color:#7aa9ff}}
.sub{{font-family:'your display typeface';font-weight:300;font-size:28px;line-height:1.4;
 color:rgba(255,255,255,.82);margin-top:22px}}
.foot{{position:absolute;left:76px;right:76px;bottom:74px;display:flex;align-items:center;
 gap:20px}}
.foot i{{flex:1 1 auto;height:1px;background:rgba(255,255,255,.34)}}
.foot span{{flex:0 0 auto;font-family:'your display typeface';font-weight:500;font-size:18px;letter-spacing:.16em;
 text-transform:uppercase;color:#fff;white-space:nowrap}}
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


CARDS = {
    # construction / double-handling / callout. Copy verbatim from basics.py.
    "double-handling": dict(
        plate="double-handling.png",
        head="Aussie construction businesses don't have to [[double-handle every job]] anymore.",
        sub="One hire. That is the whole change.",
        cta="Take the Site-to-Profit Readiness Check"),
    "systems": dict(
        plate="systems.png",
        head="Aussie construction businesses. Still [[running on disconnected systems]]?",
        sub="You don't have to be.",
        cta="Take the Site-to-Profit Readiness Check"),
}


def build(key):
    c = CARDS[key]
    p = PLATES / c["plate"]
    if not p.exists():
        print(f"  skip {key}: no plate at {p}")
        return
    doc = (f'<meta charset="utf-8"><style>{CSS}</style><div class="card">'
           f'<img class="plate" src="{p.resolve().as_uri()}"><div class="scrim"></div>'
           f'<div class="top"><div class="head">{markup(c["head"])}</div>'
           f'<div class="sub">{html.escape(c["sub"])}</div></div>'
           f'<div class="foot"><span>{html.escape(c["cta"])}</span><i></i></div></div>')
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
