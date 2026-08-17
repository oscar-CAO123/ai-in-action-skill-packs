#!/usr/bin/env python3
"""F-M4, the filmed billboard. Hook 4: "[avatar], are you still..." plus the top three ranked
pains, plus the magnet.

    python3 build_billboard.py                 # every industry whose plate is shot
    python3 build_billboard.py construction    # one

One paid plate per industry. This file adds one thing to it and nothing else.

## What this format is now (third and final call)

**The billboard copy is generated INTO the plate, not composited onto it.**
`plates_magnet.billboard_prompt` quotes the headline, the three bullets and the CTA line by line
and the model sets them. Two earlier builds are dead and should not be revived:

  - the pop-art comic panel, scrapped outright;
  - a blank billboard face with the copy mapped on by homography (`matrix3d` off a hand-set
    `QUAD`). It worked, and it read as a mock-up rather than a photograph of a real board.

**So this file is a compositor with exactly one job: the Snapchat text bar.** That bar is phone
UI sitting over the footage, not something printed on the billboard, which is why it is the one
element still drawn here.

## The Snapchat bar

Measured off the template you downloaded, mirrored at
`../references/snapchat-text-template.webp` (720x1280):

| | Template | As a fraction |
|---|---|---|
| bar colour | samples `#767676` | ships as `rgba(0,0,0,0.42)`, translucent |
| bar top | y 213 | 0.1664 of frame height |
| bar height | 74px | 0.0578 |
| text | white, regular weight, plain grotesque, centred | ships at 0.56 of bar height |

Three things about it were wrong across the first two passes and are now fixed:

  - **It is a translucent black scrim, not a solid grey slab.** The template samples as a flat
    `#767676` only because that mock sits on a light grey page; lifting that value literally
    produced an opaque block. The footage has to read through it.
  - **The text is smaller than the template's ratio and sits well inside the frame.** The
    template's sample line is two words; ours runs the full width, so at the template ratio it
    touched both edges.
  - **It is dragged clear of the billboard copy**, not left at the tool's default drop position.

The face is Helvetica Neue, not your display typeface. Same call as the newspaper card's Didone: this is a
borrowed interface, and setting it in the house face is what would make it read as fake.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from magnet_copy import COPY, INDUSTRIES  # noqa: E402

PLATES = ROOT / "plates-magnet"
OUT = ROOT / "out-magnet"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 1080, 1350

# Off the template, then corrected by you on the fourth pass: the flat `#767676` the template
# samples at is what that mock renders over a light grey page, and lifting it literally gave a
# heavy opaque slab. The real tool draws a TRANSLUCENT black scrim, so the footage reads through
# it. Sampled grey stays as the reference value; what ships is the scrim.
SNAP_SCRIM = "rgba(0, 0, 0, 0.42)"
# The template's own bar sits at 0.1664, but that is only where the tool drops it before you
# drag it. On these plates the billboard fills the top two thirds, so 0.1664 lands the bar
# straight across the headline. It goes below the board instead, over the road, which is both
# clear of the copy and where a person filming would actually have dragged it.
SNAP_TOP = 0.665
SNAP_H = 0.0578
# Smaller than the template's own ratio and with real side margins, because the template's
# sample line is two words and ours runs the width of the card: at 0.73 the text touched
# both edges of the frame.
SNAP_FONT = 0.56           # of the bar's height
SNAP_PAD = 130            # px either side, so the line sits well inside the frame

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.card{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.plate{{position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover}}
/* the Snapchat text tool: a TRANSLUCENT black band edge to edge, white regular-weight
   grotesque centred inside it with real side margins. Never an opaque slab, never bold,
   never the house face. */
.snap{{position:absolute;left:0;width:{W}px;background:{SNAP_SCRIM};
      display:flex;align-items:center;justify-content:center;
      padding:0 {SNAP_PAD}px;overflow:hidden}}
.snap span{{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:400;
           color:#fff;white-space:nowrap;line-height:1}}
"""

# The bar text shrinks to fit rather than wrapping, which is what the real tool does.
FIT = """
(function(){
  var s=document.querySelector('.snap span');
  // AVAIL is passed in, not read off the bar: `clientWidth` counts the element's padding, so
  // reading it there hands the fit the full 1080 and the line runs to both frame edges with
  // the side margins doing nothing. Same trap the newspaper masthead hit.
  var avail=AVAIL;
  var size=START;
  s.style.fontSize=size+'px';
  while(s.scrollWidth>avail && size>10){ size-=1; s.style.fontSize=size+'px'; }
  document.documentElement.dataset.fitted=Math.round(size)+'px';
})();
"""


def render(industry):
    key = industry["key"]
    plate = PLATES / key / "billboard-plate.png"
    if not plate.exists():
        return None, "no plate shot"
    c = COPY["billboard"](industry)
    bar_h = round(SNAP_H * H)
    doc = (
        f'<meta charset="utf-8"><style>{CSS}</style><div class="card">'
        f'<img class="plate" src="{plate.resolve().as_uri()}">'
        f'<div class="snap" style="top:{round(SNAP_TOP * H)}px;height:{bar_h}px">'
        f'<span>{html.escape(c["snap"])}</span></div>'
        f'</div><script>{FIT.replace("START", str(round(bar_h * SNAP_FONT))).replace("AVAIL", str(W - 2 * SNAP_PAD))}</script>')

    out = OUT / key / "F-M4-billboard.png"
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
    Path(tmp).unlink()
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
        print(f"  {i['key']:22} snap {note}")
        n += 1
    print(f"\n{n} cards -> {OUT}")
