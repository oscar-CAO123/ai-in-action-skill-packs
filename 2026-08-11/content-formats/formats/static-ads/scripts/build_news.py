#!/usr/bin/env python3
"""Composite the VHS news-interview cards. Free.

    python3 build_news.py                # all with a plate on disk
    python3 build_news.py construction

The locked watercolour format puts the copy ABOVE the head. That cannot apply here: an
interview frames the subject from the chest up, so their head is already at the top and the
only clean band is the bottom. That is also where a lower-third belongs, so the two agree.

**Nothing implies real media coverage.** No station ident, no channel logo, no ticker, no
masthead, no journalist and no outlet. The lower-third names the AVATAR'S ROLE, never a person,
so the card claims an owner was interviewed about their own trade, not that house was on the news.
Text is laid in here, never generated inside the plate.
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
PLATES = ROOT / "plates-news"
COLLAGE = ROOT / "collage-news"
OUT = ROOT / "out-news"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1080, 1350

CSS = f"""
@font-face{{font-family:'your display typeface';font-weight:200;src:url('{ASSETS}/display-200.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:300;src:url('{ASSETS}/display-300.ttf')}}
@font-face{{font-family:'your display typeface';font-weight:500;src:url('{ASSETS}/display-500.ttf')}}
:root{{--blue:#1269ff}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;background:#000;overflow:hidden}}
.card{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.plate{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 object-position:center 30%}}
.scrim{{position:absolute;inset:0;background:
 linear-gradient(180deg, rgba(4,5,15,0) 40%, rgba(4,5,15,.45) 55%, rgba(4,5,15,.88) 68%,
 rgba(4,5,15,.97) 80%)}}
.bottom{{position:absolute;left:70px;right:70px;bottom:70px}}
/* the lower-third: a blue keyline and the avatar's ROLE, never a name */
.lt{{display:flex;align-items:center;gap:16px;margin-bottom:26px}}
.lt b{{display:block;width:6px;height:30px;background:var(--blue);flex:0 0 auto}}
.lt span{{font-family:'your display typeface';font-weight:500;font-size:22px;letter-spacing:.15em;
 text-transform:uppercase;color:#fff}}
.head{{font-family:'your display typeface';font-weight:300;font-size:66px;line-height:1.07;color:#fff;
 letter-spacing:-.008em}}
.acc{{color:#5b93ff}}
.sub{{font-family:'your display typeface';font-weight:300;font-size:26px;line-height:1.4;
 color:rgba(255,255,255,.80);margin-top:18px}}
.cta{{display:flex;align-items:center;gap:18px;margin-top:26px}}
.cta i{{flex:1 1 auto;height:1px;background:rgba(255,255,255,.32)}}
.cta span{{flex:0 0 auto;font-family:'your display typeface';font-weight:500;font-size:16px;letter-spacing:.16em;
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


# Copy is the locked copy from basics.py, verbatim.
CARDS = {
    "construction": dict(
        role="Construction business owner",
        head="Aussie construction businesses. Still [[running on disconnected systems]]?",
        sub="You don't have to be.",
        cta="Take the Site-to-Profit Readiness Check"),
    "real-estate": dict(
        role="Real estate principal",
        head="Aussie real estate agencies. Still [[guessing at your own numbers]]?",
        sub="You don't have to be.",
        cta="Take the AI-Ready Agency Score"),
    "hospitality": dict(
        role="Hospitality business owner",
        head="Aussie hospitality businesses. Still [[being on site for it to run]]?",
        sub="You don't have to be.",
        cta="Take the Wow Factor Audit"),
    "retail": dict(
        role="Retail business owner",
        head="Aussie retailers don't have to [[do the admin by hand]] anymore.",
        sub="One hire. That is the whole change.",
        cta="Take the Retail Ops AI Readiness Check"),
    "financial-services": dict(
        role="Insurance broker",
        head="Aussie insurance brokers don't have to [[drown in paperwork]] anymore.",
        sub="One hire. That is the whole change.",
        cta="Take the Broker and Adviser AI Readiness Check"),
}


def build(key, collage=False):
    """collage=True stands the cut-out subject on the editorial collage from collage_news.py."""
    c = CARDS[key]
    p = (COLLAGE if collage else PLATES) / f"{key}.png"
    if not p.exists():
        print(f"  skip {key}: no plate at {p}")
        return
    doc = (f'<meta charset="utf-8"><style>{CSS}</style><div class="card">'
           f'<img class="plate" src="{p.resolve().as_uri()}"><div class="scrim"></div>'
           f'<div class="bottom">'
           f'<div class="lt"><b></b><span>{html.escape(c["role"])}</span></div>'
           f'<div class="head">{markup(c["head"])}</div>'
           f'<div class="sub">{html.escape(c["sub"])}</div>'
           f'<div class="cta"><span>{html.escape(c["cta"])}</span><i></i></div>'
           f'</div></div>')
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc); tmp = f.name
    png = OUT / (f"{key}-collage.png" if collage else f"{key}.png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    f"--screenshot={png}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    Path(tmp).unlink()
    print(f"  {png}")


if __name__ == "__main__":
    args = sys.argv[1:]
    coll = "--collage" in args
    for k in ([a for a in args if not a.startswith("--")] or list(CARDS)):
        build(k, coll)
