#!/usr/bin/env python3
"""F-M3, the newspaper front page. Hook 3: "The truth about using AI in your [avatar] business.
It's a lot easier than you think."

    python3 build_editorial.py                 # every industry whose coverage plate is shot
    python3 build_editorial.py construction    # one

One paid coverage plate per industry, everything here free.

**Built on the newspaper template you downloaded**, `~/Desktop/template.webp`, mirrored into
`../references/newspaper-template.webp`. you, : the first version was digital-article
chrome and read as our own authored page, which is the one thing this format cannot do. The
template's furniture is what does the work, so it is followed rather than referenced:

  rule, issue line and date, rule
  full-width Didone masthead
  rule
  hero photograph
  lead headline
  two body columns plus a reversed sidebar box
  rule, footer line

**The masthead is the industry's own word.** Not an invented publication. A made-up trade title
close to a real Australian one is what gets a creative pulled, and one word does the same job.

**This card is the one deliberate break from the your display typeface-only design system.** A newspaper set in
your display typeface is not a newspaper, and the whole format is the borrow. Didone for the masthead and
headline, Georgia for the body, both off the system font stack. Flagged rather than silent: the
lock covers house-branded surfaces, and this card is dressed as somebody else's paper on purpose.
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
from magnet_copy import COPY, INDUSTRIES  # noqa: E402

PLATES = ROOT / "plates-magnet"
OUT = ROOT / "out-magnet"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 1080, 1350
PAD = 46
INK = "#0B0B0B"
PAPER = "#FCFBF8"
DATE = "Thursday, 6 August 2026"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{PAPER}}}
.card{{position:relative;width:{W}px;height:{H}px;background:{PAPER};overflow:hidden;
      padding:{PAD}px {PAD}px 0;display:flex;flex-direction:column;color:{INK}}}
.hair{{height:2px;background:{INK}}}
.thin{{height:1px;background:{INK}}}
.issue{{display:flex;justify-content:space-between;align-items:baseline;
       font-family:Georgia,serif;font-weight:700;font-size:20px;padding:9px 0}}
.mast{{font-family:Didot,'Bodoni 72',Georgia,serif;font-weight:700;text-align:center;
      line-height:0.86;letter-spacing:-0.01em;padding:14px 0 18px;white-space:nowrap}}
.hero{{width:100%;flex:1 1 0;min-height:0;object-fit:cover;display:block;margin-top:14px}}
.lede{{font-family:Didot,'Bodoni 72',Georgia,serif;font-weight:700;line-height:1.02;
      letter-spacing:-0.012em;padding:16px 0 4px}}
.accent{{font-style:italic}}
.cols{{display:flex;gap:22px;align-items:stretch;padding:12px 0 0;flex:0 0 auto}}
.col{{flex:1 1 0;min-width:0}}
.colh{{font-family:Georgia,serif;font-weight:700;font-size:23px;line-height:1.15;
      margin-bottom:6px}}
.colb{{font-family:Georgia,serif;font-size:18px;line-height:1.34;text-align:justify;
      hyphens:auto}}
.side{{flex:0 0 268px;background:#3A3A3A;color:{PAPER};padding:16px 18px}}
.side .colh{{color:{PAPER};font-size:24px}}
.side .colb{{color:{PAPER};font-size:18px;text-align:left}}
.foot{{display:flex;justify-content:space-between;align-items:baseline;
      font-family:Georgia,serif;font-weight:700;font-size:19px;padding:9px 0 12px}}
"""

# Two solves, both binary searches, same shape as every other rig here: the masthead grows until
# it fills the column width, the lead headline grows until it fills its allowance.
FIT = """
(function{
  function fitWidth(el, avail, lo, hi){
    var best=lo;
    for(var i=0;i<26;i++){
      var mid=(lo+hi)/2; el.style.fontSize=mid+'px';
      if(el.scrollWidth<=avail){ best=mid; lo=mid; } else { hi=mid; }
    }
    el.style.fontSize=best+'px'; return best;
  }
  function fitBlock(el, availH, lo, hi){
    var best=lo;
    for(var i=0;i<26;i++){
      var mid=(lo+hi)/2; el.style.fontSize=mid+'px';
      var ok = el.getBoundingClientRect.height<=availH && el.scrollWidth<=el.clientWidth+1;
      if(ok){ best=mid; lo=mid; } else { hi=mid; }
    }
    el.style.fontSize=best+'px'; return best;
  }
  var m=document.querySelector('.mast'), l=document.querySelector('.lede');
  // MEASURE, not the parent's clientWidth: `.card` is padded and clientWidth counts padding,
  // so the masthead was solved 92px too wide and ran its last letter off the page.
  var a=fitWidth(m, MEASURE, 40, 260);
  var b=fitBlock(l, LEDECAP, 26, 90);
  document.documentElement.dataset.fitted=Math.round(a)+'/'+Math.round(b)+'px';
});
"""


def render(industry):
    key = industry["key"]
    shot = PLATES / key / "editorial-coverage.png"
    if not shot.exists:
        return None, "no coverage plate"
    c = COPY["editorial"](industry)
    doc = (
        f'<meta charset="utf-8"><style>{CSS}</style><div class="card">'
        f'<div class="hair"></div>'
        f'<div class="issue"><span>Issue 01, AI at Work</span>'
        f'<span>&bull; {DATE}</span></div>'
        f'<div class="thin"></div>'
        f'<div class="mast">{html.escape(c["paper"])}</div>'
        f'<div class="hair"></div>'
        f'<img class="hero" src="{shot.resolve.as_uri}">'
        f'<div class="lede">{markup(c["head"])}</div>'
        f'<div class="cols">'
        f'<div class="col"><div class="colh">{html.escape(c["col1h"])}</div>'
        f'<div class="colb">{html.escape(c["col1"])}</div></div>'
        f'<div class="col"><div class="colh">{html.escape(c["col2h"])}</div>'
        f'<div class="colb">{html.escape(c["col2"])}</div></div>'
        f'<div class="side"><div class="colh">{html.escape(c["cta"])}</div>'
        f'<div class="colb">Free, and the report is on screen the moment you finish.</div>'
        f'</div></div>'
        f'<div class="thin" style="margin-top:12px"></div>'
        f'<div class="foot"><span>the business</span>'
        f'<span>{html.escape(industry["route"])}</span></div>'
        f'</div><script>{FIT.replace("LEDECAP", "196").replace("MEASURE", str(W - 2 * PAD))}</script>')

    out = OUT / key / "F-M3-editorial.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    f"--screenshot={out}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    dom = subprocess.run([CHROME, "--headless", "--disable-gpu",
                          "--virtual-time-budget=4000", "--dump-dom", f"file://{tmp}"],
                         capture_output=True, text=True).stdout
    Path(tmp).unlink
    m = re.search(r'data-fitted="([^"]+)"', dom)
    return out, (m.group(1) if m else "?")


if __name__ == "__main__":
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or None
    n = 0
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        out, note = render(i)
        if not out:
            print(f"  {i['key']:22} SKIPPED, {note}")
            continue
        print(f"  {i['key']:22} mast/lede {note}")
        n += 1
    print(f"\n{n} cards -> {OUT}")
