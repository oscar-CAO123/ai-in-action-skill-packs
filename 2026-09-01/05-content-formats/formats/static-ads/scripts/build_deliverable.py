#!/usr/bin/env python3
"""F-M2, the deliverable shot. Hook 2: "Don't use AI in your [avatar] business before this audit."

    python3 build_deliverable.py                 # all seven, free
    python3 build_deliverable.py construction    # one

FREE. No generation anywhere in this format. The image on the card is a headless-Chrome capture
of the asset's own scored report, taken by `shot_report.py`.

The layout, settled with you : white ground, black your display typeface, sentence case, the hook at
the top, an arrow pointing down, the deliverable centred under it.

**Seven cards, one format, seven presentations.** The copy shape does not vary, so if the picture
does not vary either the set reads as one ad posted seven times. What moves per industry is how
the capture sits on the page: the angle, the width, the shadow depth, how far the arrow travels,
and whether the deliverable is one sheet, a stacked pair, or squared up flat. Nothing else.

This is the only card in the set that is not black. That is deliberate: it is the one BOF-shaped
cell in a set of curiosity hooks, and a white page reads as a document rather than an ad.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from band_basic import markup  # noqa: E402
from magnet_copy import INDUSTRIES, COPY  # noqa: E402

ASSETS = ROOT.parent / "assets"
SHOTS = ROOT / "out-magnet" / "_shots"
OUT = ROOT / "out-magnet"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 1080, 1350
PAD = 84
BLUE = "#1269FF"
INK = "#101014"

# Per-industry presentation. `tilt` in degrees, `width` in px on a 1080 card, `drop` is the
# shadow spread, `travel` is how far the arrow falls before the deliverable starts, and `style`
# picks the arrangement. Hand-set by eye rather than generated, because seven is few enough to
# cast and a formula would land three of them on the same angle.
LOOK = {
    "construction":          dict(tilt=-3.5, width=880, drop=52, travel=64,  style="single"),
    "real-estate":           dict(tilt=2.5,  width=820, drop=40, travel=92,  style="stack"),
    "hospitality":           dict(tilt=-1.2, width=900, drop=64, travel=52,  style="single"),
    "retail":                dict(tilt=4.0,  width=800, drop=36, travel=104, style="single"),
    "financial-services":    dict(tilt=-5.0, width=840, drop=48, travel=72,  style="stack"),
    "building-services":     dict(tilt=1.5,  width=860, drop=56, travel=84,  style="flat"),
    "professional-services": dict(tilt=-2.2, width=830, drop=44, travel=96,  style="stack"),
}

CSS = f"""
@font-face {{ font-family:'your display typeface'; font-weight:200; src:url('{ASSETS}/display-200.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{ASSETS}/display-300.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500; src:url('{ASSETS}/display-500.ttf'); }}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#fff}}
.card{{position:relative;width:{W}px;height:{H}px;background:#fff;overflow:hidden;
      padding:{PAD}px;display:flex;flex-direction:column;align-items:center}}
.hook{{font-family:'your display typeface';font-weight:300;color:{INK};line-height:1.08;
      letter-spacing:-0.005em;text-align:center;width:100%}}
.accent{{color:{BLUE}}}
.arrow{{display:block;margin:0 auto}}
.stage{{flex:1 1 auto;display:flex;align-items:center;justify-content:center;width:100%;
       position:relative}}
.shot{{display:block;border-radius:10px;background:#0A0A10}}
/* the stacked pair sits behind and slightly off, so the card reads as a document with pages */
.behind{{position:absolute;border-radius:10px;background:#0A0A10;opacity:0.55}}
.cta{{font-family:'your display typeface';font-weight:500;color:{INK};letter-spacing:0.14em;
     text-transform:uppercase;font-size:24px;text-align:center;padding-top:6px}}
"""

# One solve, same shape as band_basic.py: grow the hook until the tallest element stops fitting.
# The `document.fonts.load` wait is not optional. The card starts with an empty div, so nothing
# has requested your display typeface, `fonts.ready` resolves instantly against fallback metrics roughly 1.4x
# wider, and every card silently undersizes.
FIT = """
document.fonts.load('300 100px "your display typeface"','AZ09')
 .then(function(){ return document.fonts.ready; })
 .then(function(){
  var hook=document.querySelector('.hook');
  var card=document.querySelector('.card');
  var avail=CAP;
  var lo=28, hi=140, best=lo;
  for(var i=0;i<24;i++){
    var mid=(lo+hi)/2;
    hook.style.fontSize=mid+'px';
    var r=hook.getBoundingClientRect();
    var over = hook.scrollWidth > hook.clientWidth+1;
    if(r.height<=avail && !over){ best=mid; lo=mid; } else { hi=mid; }
  }
  hook.style.fontSize=best+'px';
  document.documentElement.dataset.fitted =
    Math.round(best)+'px, '+Math.round(hook.getBoundingClientRect().height)+'px tall';
});
"""


def arrow_svg(travel):
    """A thin down arrow. Its length is part of what varies per card."""
    h = travel
    return (f'<svg class="arrow" width="34" height="{h}" viewBox="0 0 34 {h}">'
            f'<line x1="17" y1="0" x2="17" y2="{h - 13}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M6 {h - 15} L17 {h} L28 {h - 15}" fill="none" stroke="{INK}" '
            f'stroke-width="2" stroke-linecap="square"/></svg>')


def stage_html(shot, look):
    from PIL import Image
    w = look["width"]
    iw, ih = Image.open(shot).size
    h = round(w * ih / iw)
    src = shot.resolve().as_uri()
    shadow = f"box-shadow:0 {look['drop'] // 2}px {look['drop']}px rgba(16,16,20,0.30);"
    tilt = 0 if look["style"] == "flat" else look["tilt"]
    behind = ""
    if look["style"] == "stack":
        # two ghosts, each a little further off, so the pile reads as more than one page
        for i, (dx, dy, rot) in enumerate(((16, 14, tilt + 2.4), (30, 26, tilt + 4.6))):
            behind += (f'<div class="behind" style="width:{w}px;height:{h}px;'
                       f'transform:translate({dx}px,{dy}px) rotate({rot}deg);'
                       f'z-index:{i};{shadow}"></div>')
    img = (f'<img class="shot" src="{src}" style="width:{w}px;height:{h}px;position:relative;'
           f'z-index:5;transform:rotate({tilt}deg);{shadow}">')
    return f'<div class="stage">{behind}{img}</div>'


def render(industry, png):
    key = industry["key"]
    look = LOOK[key]
    copy = COPY["deliverable"](industry)
    shot = SHOTS / f"{key}-report.png"
    if not shot.exists():
        raise SystemExit(f"no report capture for {key}. Run: python3 shot_report.py {key}")

    # The hook block gets a third of the card; the deliverable and the arrow take the rest.
    cap = 300
    doc = (f'<meta charset="utf-8"><style>{CSS}</style><div class="card">'
           f'<div class="hook">{markup(copy["head"])}</div>'
           f'{arrow_svg(look["travel"])}'
           f'{stage_html(shot, look)}'
           f'<div class="cta">{html.escape(copy["cta"])}</div>'
           f'</div><script>{FIT.replace("CAP", str(cap))}</script>')

    png = Path(png)
    png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    f"--screenshot={png}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    dom = subprocess.run([CHROME, "--headless", "--disable-gpu",
                          "--virtual-time-budget=4000", "--dump-dom", f"file://{tmp}"],
                         capture_output=True, text=True).stdout
    Path(tmp).unlink()
    m = re.search(r'data-fitted="([^"]+)"', dom)
    return m.group(1) if m else "?"


if __name__ == "__main__":
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or None
    n = 0
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        out = OUT / i["key"] / "F-M2-deliverable.png"
        print(f"  {i['key']:22} {LOOK[i['key']]['style']:7} {render(i, out)}")
        n += 1
    print(f"\n{n} cards -> {OUT}")
