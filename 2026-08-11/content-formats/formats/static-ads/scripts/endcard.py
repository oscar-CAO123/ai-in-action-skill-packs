#!/usr/bin/env python3
"""The sculpture end card: the last page of a Theme B carousel. FREE once the plate exists.

    python3 endcard.py --demo        # renders with a placeholder, no plate needed

the operator, 2026-08-10: the last page of this format is the same end card the canonical F8
industry-build carousel closes on, the classic sculpture in the moire-degraded treatment with
the text at the bottom, **except the monument changes from carousel to carousel**. The Thinker
belongs to F8. Everything else about the card is a straight fork: the same veil, the same two
scrims, the same white lines, the same blue CTA, the same lockup in the same place.

THIS REPLACES THE BOOKEND CLOSE. The inversion law locked earlier the same day had the last page
return to the cover's treatment. It now reads: inverted cover, paper information pages, sculpture
end card. The carousel ends the way every house carousel ends.

THE FURNITURE IS COPIED FROM `industry-build-carousels/loop_diagram.py`, not reinvented: the
radial veil at the moire style's own three stops, the 240px top scrim, the 760px tall scrim, the
close block at bottom 252, the CTA at bottom 176 in #4B9EFF, and the lockup at bottom 46. Edit
them together or the two formats drift.

THE MOIRE IS NEVER PROMPT-BAKED. `engine/tools/moire/README.md` is explicit: a model low-passes
the 2 to 6px gratings that create interference and paints decorative op-art instead. The plate
asks for the CARRIER, a fine metal mesh in deep focus, and `grade()` beats the real pattern out
of it afterwards. That chain is lifted from the F8 `grade_plate.sh` `moire` case.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
PLATES = ROOT.parent / "candidate" / "plates"
MONUMENTS = ROOT.parent / "references" / "monuments" / "monuments.json"
CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W, H = 1080, 1350
BLUE = "#4B9EFF"
INK = "#F4F3EC"
VEIL = (0.36, 0.62, 0.80)      # the moire-sculpture style's own three stops

CSS = """
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{a}/jost-300.ttf'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; overflow:hidden; background:#06060e; }}
.stage {{ position:relative; width:{w}px; height:{h}px; overflow:hidden; background:#06060e; }}
.plate {{ position:absolute; inset:0; width:{w}px; height:{h}px; object-fit:cover;
  display:block; }}
.veil {{ position:absolute; inset:0; z-index:2;
  background:radial-gradient(120% 80% at 50% 38%, rgba(6,6,14,{v0:.2f}) 0%,
  rgba(6,6,14,{v1:.2f}) 58%, rgba(6,6,14,{v2:.2f}) 100%); }}
.top-scrim {{ position:absolute; left:0; right:0; top:0; height:240px; z-index:2;
  background:linear-gradient(180deg, rgba(8,8,16,.72) 0%, rgba(8,8,16,0) 100%); }}
.tall-scrim {{ position:absolute; left:0; right:0; bottom:0; height:760px; z-index:2;
  background:linear-gradient(0deg, rgba(8,8,16,.92) 0%, rgba(8,8,16,.70) 38%,
  rgba(8,8,16,.30) 70%, rgba(8,8,16,0) 100%); }}
.close {{ position:absolute; left:78px; right:78px; bottom:252px; z-index:6; text-align:center;
  font-family:'your display typeface'; font-weight:300; color:#F4F6FB; font-size:70px; line-height:1.14;
  text-shadow:0 5px 20px rgba(0,0,0,.95); }}
.cta {{ position:absolute; left:0; right:0; bottom:176px; z-index:6; text-align:center;
  font-family:'your display typeface'; font-weight:300; color:{blue}; font-size:25px; letter-spacing:2.6px;
  text-transform:uppercase; text-shadow:0 3px 14px rgba(0,0,0,.95); }}
.brand {{ position:absolute; bottom:46px; left:0; right:0; text-align:center; z-index:6; }}
.brand img {{ height:84px; filter:brightness(0) invert(1); }}
.ph {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  background:#14141a; color:#6b6b76; font-family:'your display typeface'; font-weight:300; font-size:30px;
  text-align:center; padding:0 120px; }}
"""

# The moire beat, lifted from `industry-build-carousels/grade_plate.sh`, the `moire` case. The
# downscale-to-two-fifths and back on nearest neighbour is what creates the interference; the
# geq lays the scan beat over it. Same chain, so the two formats shimmer identically.
GRADE = ("scale={dw}:-2:flags=neighbor,scale={w}:{h}:flags=neighbor,"
         "geq=lum='lum(X,Y)*(0.74+0.26*sin(Y*2.3)+0.10*sin(X*1.1))':cb='cb(X,Y)':cr='cr(X,Y)',"
         "rgbashift=rh=4:bh=-4,"
         "eq=contrast=1.16:saturation=0.66:gamma=1.02,"
         "noise=alls=14:allf=t+u,"
         "vignette=PI/4")


def grade(src, dest=None):
    """Beat the moire out of a plate that was shot with a real mesh in it. FREE."""
    from PIL import Image
    src = Path(src)
    dest = Path(dest or src.with_name(src.stem + "-moire.png"))
    w, h = Image.open(src).size
    f = GRADE.format(dw=w * 2 // 5, w=w, h=h)
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
                        "-vf", f, "-frames:v", "1", str(dest)], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"moire grade FAILED:\n{r.stderr[:500]}")
    return dest


def monuments():
    """The scraped bank. Reference only: the plate is generated, never composited from these."""
    return json.loads(MONUMENTS.read_text())["items"] if MONUMENTS.exists() else []


def render(png, lines, cta, plate=None, note=""):
    """One end card. `lines` is the white block, `cta` the blue line under it."""
    css = CSS.format(a=ASSETS, w=W, h=H, blue=BLUE,
                     v0=VEIL[0], v1=VEIL[1], v2=VEIL[2])
    if plate and Path(plate).exists():
        art = f'<img class="plate" src="{Path(plate).resolve().as_uri()}">'
    else:
        art = f'<div class="ph">{note or "no sculpture plate yet"}</div>'
    logo = (ASSETS / "house-logo.svg").resolve().as_uri()
    doc = (f'<meta charset="utf-8"><style>{css}</style><div class="stage">{art}'
           f'<div class="veil"></div><div class="top-scrim"></div><div class="tall-scrim"></div>'
           f'<div class="close">{"<br>".join(lines)}</div>'
           f'<div class="cta">{cta}</div>'
           f'<div class="brand"><img src="{logo}"></div>'
           f'</div>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    png = Path(png)
    png.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{H}",
                        f"--screenshot={png}", Path(tmp).as_uri()],
                       check=True, capture_output=True)
    finally:
        os.unlink(tmp)
    return png


def main():
    if "--demo" not in sys.argv:
        sys.exit("usage: endcard.py --demo")
    out = ROOT.parent / "candidate" / "u3" / "_endcard-demo.png"
    render(out, ["Find out if you qualify", "in three minutes."], "Click the link below.",
           note="sculpture plate goes here")
    print("wrote", out.name, f"({len(monuments())} monuments in the bank)")


if __name__ == "__main__":
    main()
