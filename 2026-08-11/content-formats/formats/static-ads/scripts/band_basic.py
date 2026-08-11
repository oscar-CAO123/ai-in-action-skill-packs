#!/usr/bin/env python3
"""Renderer for the basic type-led statics. Sentence case, top anchored, left aligned.

Deliberately NOT band.py. That engine implements the news-carousel band: bottom 506px, all
caps, justified flush on both margins. This one implements what the Figma scaffolds do, which
is the opposite on all three counts, and the difference is the point of the format test.

Three layouts, all free, all headless Chrome:

  stack   headline plus subheading, top anchored
  rows    a labelled Today / With a house pair
  cols    two labelled columns of tick rows

Accent markup is [[double brackets]], same as band.py, and there is one accent per card.
"""
import html
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W, H = 1080, 1350
BLUE = "#1269FF"
PAD = 84

CSS = f"""
@font-face {{ font-family:'your display typeface'; font-weight:200; src:url('{ASSETS}/jost-200.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{ASSETS}/jost-300.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500; src:url('{ASSETS}/jost-500.ttf'); }}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.card{{position:relative;width:{W}px;height:{H}px;background:#000;overflow:hidden;
      padding:{PAD}px;display:flex;flex-direction:column;justify-content:flex-start}}
/* Sentence case. No text-transform anywhere in this file, on purpose. */
.head{{font-family:'your display typeface';font-weight:300;color:#fff;line-height:1.08;letter-spacing:-0.005em;
      text-align:left}}
.sub{{font-family:'your display typeface';font-weight:200;color:#fff;line-height:1.35;text-align:left;
     margin-top:0.55em}}
.accent{{color:{BLUE}}}
/* Every card closes on its own industry's magnet. Small, white, sat at the foot. */
.cta{{font-family:'your display typeface';font-weight:300;color:#fff;letter-spacing:0.11em;
     text-transform:uppercase;margin-top:auto;padding-top:0.9em;line-height:1.3}}
/* rows: Today against With a house */
.label{{font-family:'your display typeface';font-weight:300;color:#fff;letter-spacing:0.14em;
       text-transform:uppercase;margin-bottom:0.5em}}
.rowset{{margin-top:auto;margin-bottom:auto}}
.row{{padding:0.62em 0}}
.rowlab{{font-family:'your display typeface';font-weight:300;letter-spacing:0.14em;text-transform:uppercase;
        color:#fff;opacity:.85;margin-bottom:0.18em}}
.rowtxt{{font-family:'your display typeface';font-weight:200;color:#fff;line-height:1.1}}
.rule{{height:1px;background:#fff;opacity:.22;margin:0.5em 0}}
.blue .rowtxt,.blue .rowlab{{color:{BLUE};opacity:1}}
/* cols: us against them */
.colset{{display:flex;gap:0;margin-top:auto;margin-bottom:auto;align-items:stretch}}
.col{{flex:1 1 0;min-width:0}}
.vrule{{width:1px;background:#fff;opacity:.22;margin:0 34px}}
.colhead{{font-family:'your display typeface';font-weight:300;color:#fff;line-height:1.12;margin-bottom:0.7em}}
.colrow{{font-family:'your display typeface';font-weight:200;color:#fff;line-height:1.25;margin-bottom:0.42em}}
.col.blue .colhead,.col.blue .colrow{{color:{BLUE}}}
#rule{{position:absolute;visibility:hidden;white-space:nowrap;font-family:'your display typeface';
      font-weight:300;font-size:100px}}
"""

# One solve for the whole card: grow the type until the tallest element stops fitting. The
# headline drives it and everything else is a ratio of it, so a card never mixes two scales.
FIT = """
document.fonts.load('300 100px "your display typeface"','AZ09')
 .then(function{return document.fonts.load('200 100px "your display typeface"','AZ09');})
 .then(function{return document.fonts.ready;})
 .then(function{
  var card=document.querySelector('.card');
  var avail=card.clientHeight-2*PADPX, base=card.clientWidth-2*PADPX;
  var lo=20, hi=420, best=lo;
  for(var i=0;i<26;i++){
    var mid=(lo+hi)/2;
    card.style.fontSize=mid+'px';
    var h=0, over=false;
    var kids=card.children;
    for(var k=0;k<kids.length;k++) h+=kids[k].getBoundingClientRect.height;
    // a line that cannot fit the column width at this size is an overflow too
    var spans=card.querySelectorAll('.measure');
    for(var s=0;s<spans.length;s++)
      if(spans[s].getBoundingClientRect.width>base+1) over=true;
    // a wrapping block overflows the column when a single word is wider than it
    var blocks=card.querySelectorAll('.head,.sub,.colhead,.colrow,.cta');
    for(var b=0;b<blocks.length;b++)
      if(blocks[b].scrollWidth>blocks[b].clientWidth+1) over=true;
    if(h<=avail && !over){ best=mid; lo=mid; } else { hi=mid; }
  }
  card.style.fontSize=best+'px';
  var used=0, kids=card.children;
  for(var k=0;k<kids.length;k++) used+=kids[k].getBoundingClientRect.height;
  document.documentElement.dataset.fitted=
    Math.round(best)+'px, fill '+Math.round(used/avail*100)+'%';
});
""".replace("PADPX", str(PAD))


def markup(s):
    """[[accent]] -> span, everything else escaped."""
    out, i, inside = [], 0, False
    while i < len(s):
        if s.startswith("[[", i):
            out.append('<span class="accent">')
            inside = True
            i += 2
        elif s.startswith("]]", i):
            out.append("</span>")
            inside = False
            i += 2
        else:
            out.append(html.escape(s[i]))
            i += 1
    if inside:
        out.append("</span>")
    return "".join(out)


def cta_for(spec):
    if not spec.get("cta"):
        return ""
    return (f'<div class="cta" style="font-size:0.215em">'
            f'{html.escape(spec["cta"])}</div>')


def body_for(spec):
    k = spec.get("kind", "stack")
    if k == "stack":
        # em sizes are relative to the solved card size, so one solve settles both tiers
        h = f'<div class="head" style="font-size:1em">{markup(spec["head"])}</div>'
        s = (f'<div class="sub" style="font-size:0.315em">{markup(spec["sub"])}</div>'
             if spec.get("sub") else "")
        return h + s + cta_for(spec)
    if k == "rows":
        rows = []
        for lab, txt, blue in spec["rows"]:
            rows.append(
                f'<div class="row{" blue" if blue else ""}">'
                f'<div class="rowlab" style="font-size:0.26em">{html.escape(lab)}</div>'
                f'<div class="rowtxt measure" style="font-size:1em">{html.escape(txt)}</div>'
                f'</div>')
        inner = '<div class="rule"></div>'.join(rows)
        return (f'<div class="label" style="font-size:0.24em">'
                f'{html.escape(spec["label"])}</div>'
                f'<div class="rowset">{inner}</div>' + cta_for(spec))
    if k == "cols":
        cols = []
        for headline, items, blue in spec["cols"]:
            rows = "".join(f'<div class="colrow" style="font-size:0.40em">'
                           f'{html.escape(t)}</div>' for t in items)
            cols.append(f'<div class="col{" blue" if blue else ""}">'
                        f'<div class="colhead" style="font-size:0.72em">'
                        f'{html.escape(headline)}</div>{rows}</div>')
        return (f'<div class="label" style="font-size:0.24em">'
                f'{html.escape(spec["label"])}</div>'
                f'<div class="colset">{cols[0]}<div class="vrule"></div>{cols[1]}</div>'
                + cta_for(spec))
    raise ValueError(spec.get("kind"))


def render(spec, png):
    doc = (f'<meta charset="utf-8"><style>{CSS}</style>'
           f'<div class="card">{body_for(spec)}</div>'
           f'<div id="rule"></div><script>{FIT}</script>')
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
    Path(tmp).unlink
    m = re.search(r'data-fitted="([^"]+)"', dom)
    return m.group(1) if m else "?"
