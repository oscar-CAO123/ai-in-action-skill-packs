#!/usr/bin/env python3
"""Make a clean 1080x1350 paper sheet, and set a full-page block of type on it. FREE.

    python3 paper_sheet.py            # regenerates candidate/plates/_paper-sheet.png

WHY. Theme B on paper is a cover plate followed by slides that are type and nothing else.
Those slides still have to sit on the SAME paper as the cover or the carousel comes apart, and
generating a blank sheet per slide would be paid and would drift. So the sheet is lifted out of
an already-approved plate: a bare region of `u1b-falling-graduate-on-paper.png`, tiled up to the
frame with a mirror so the fibre never repeats visibly.

The type layout is Theme B's, not the band's. `news-carousel/SKILL.md` section 1e is explicit
that information slides sit OUTSIDE the bottom-band law and carry their own scale, so this sets
one centred block over the whole sheet rather than a block in the bottom 506px.
"""
import html
import os
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
PLATES = ROOT.parent / "candidate" / "plates"
SHEET = PLATES / "_paper-sheet.png"
SOURCE = PLATES / "u1b-falling-graduate-on-paper.png"
CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W, H = 1080, 1350
PAD = 96
INK = "#0a0a0a"

# THE LEFT-WEIGHTED COLUMN (you, revised the same day).
#
# Type is the main feature of an information page, so it takes the card's own left margin, the
# same 64px the band gives the cover, and runs 58 per cent of the width. The right band is left
# for the cutout fan. NOTHING IS INDENTED: the number, the heading and every body line share one
# left edge at 64px.
#
# The first pass hung the number in a 138px gutter and indented the body to the heading. That
# cost the body 138px of an already narrow measure and held it at 40px, which you rejected as
# too small. One flush left edge gives the measure back.
LEFT = 64                     # the card's own margin, matching `band.PAD`
COLW = int(W * 0.58)          # 626, the type column's width
HEAD_GAP = 46                 # heading block to the first body line


BLUE = "#1269FF"


def highlighter(seed=3, colour=BLUE, alpha=0.30):
    """A real highlighter stroke as an inline SVG data URI. FREE.

    you, : "I don't want just a block of hex, I want it to appear as if it is a real
    highlighter." The reference he sent is a flat rectangle, so this goes past it. Four things
    separate a marker stroke from a filled box, and all four are here:

      * a CHISEL TIP, so the two ends are angled rather than square, and the stroke overshoots
        the word at one end and falls short at the other;
      * a WANDERING EDGE, from a turbulence displacement, the same filter the F8 loop diagram
        uses on its tiles;
      * DENSITY VARIATION along the run, because a real tip lays more ink where it starts and
        where it slows, and streaks where the felt lifts;
      * TRANSLUCENCY, so the paper's texture reads straight through the colour.

    The viewBox is deliberately long. The stroke stretches to whatever it is laid behind, and a
    short box would smear the turbulence into bands as it scaled.
    """
    import urllib.parse
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" '
        f'preserveAspectRatio="none">'
        f'<defs>'
        f'<filter id="w" x="-6%" y="-25%" width="112%" height="150%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.006 0.05" numOctaves="3" '
        f'seed="{seed}" result="n"/>'
        f'<feDisplacementMap in="SourceGraphic" in2="n" scale="16" '
        f'xChannelSelector="R" yChannelSelector="G"/>'
        f'</filter>'
        # the felt streaks: a few slightly lighter runs along the stroke
        f'<linearGradient id="s" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="0.30"/>'
        f'<stop offset="0.22" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset="0.62" stop-color="#fff" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        f'</linearGradient>'
        # the ends: denser where the tip landed and where it lifted
        f'<linearGradient id="e" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{colour}" stop-opacity="0.55"/>'
        f'<stop offset="0.08" stop-color="{colour}" stop-opacity="0"/>'
        f'<stop offset="0.93" stop-color="{colour}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{colour}" stop-opacity="0.45"/>'
        f'</linearGradient>'
        f'</defs>'
        f'<g filter="url(#w)">'
        # the chisel: left end angled one way, right end the other, and the run is not level
        f'<path d="M6,26 L994,14 L1000,86 L2,92 Z" fill="{colour}" fill-opacity="{alpha}"/>'
        f'<path d="M6,26 L994,14 L1000,86 L2,92 Z" fill="url(#e)"/>'
        f'<path d="M6,26 L994,14 L1000,86 L2,92 Z" fill="url(#s)"/>'
        f'</g></svg>')
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


def build_sheet(src=SOURCE, dest=SHEET):
    """Lift a bare patch of paper and grow it to a full frame by mirrored tiling."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # The top-left eighth of the founding plate is bare paper: the figure sits centre and the
    # top third is empty by construction. Verified against the plate rather than assumed.
    patch = im.crop((0, 0, w // 2, h // 4))
    a = np.asarray(patch, dtype=np.uint8)
    # mirror out to 2x2 so the join is continuous, then resize to the frame
    top = np.concatenate([a, a[:, ::-1]], axis=1)
    tile = np.concatenate([top, top[::-1, :]], axis=0)
    Image.fromarray(tile).resize((W, H), Image.LANCZOS).save(dest)
    return dest


CSS = """
@font-face {{ font-family:'your display typeface'; font-weight:200; src:url('{a}/jost-200.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{a}/jost-300.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500; src:url('{a}/jost-500.ttf'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; overflow:hidden; }}
.card {{ position:relative; width:{w}px; height:{h}px; }}
.sheet {{ position:absolute; inset:0; width:{w}px; height:{h}px; object-fit:cover; }}
/* TWO LAYOUTS. `.blk` alone is the original centred full-width block, which U4 and U7 are
   already built on and which must not move. `.blk.left` is the canonical layout:
   the block stops at the type column so the right band stays clear for the cutout fan. A
   caller opts in by passing a header, and everything below keys off that one class. */
.blk {{ position:absolute; inset:0; padding:{pad}px; display:flex; flex-direction:column;
  justify-content:center; align-items:center; }}
/* THE HEADER ROW IS ANCHORED, NOT CENTRED . `.blk` centres its block vertically,
   which is right for a page that stands alone and wrong for a set: a copy pass left U3 with a
   478px page beside an 883px one, and the centring dropped the short page's O-number 230px
   below the other two, so the three headers walked down the carousel. Same failure as three
   pages solving to three different type sizes, and the same fix: pin the thing that has to
   agree. Only `.blk.left` moves, and only a caller passing a header gets that class, so U4,
   U7 and both U1 variants are untouched. Verified by checksum. */
.blk.left {{ position:absolute; left:{left}px; top:0; right:auto; bottom:auto;
  width:{colw}px; height:{h}px; padding:{pad}px 0; align-items:flex-start;
  justify-content:flex-start; padding-top:130px; }}
/* Number and heading share one line, and it starts at the same left edge as every body line.
   Nothing is indented anywhere on the page. */
.head {{ display:flex; align-items:baseline; width:100%; }}
.num {{ font-family:'your display typeface'; font-weight:200; color:{ink}; letter-spacing:0.01em;
  margin-right:0.34em; }}
.hdr {{ font-family:'your display typeface'; font-weight:500; color:{ink}; text-transform:uppercase;
  letter-spacing:0.01em; line-height:1.1; white-space:nowrap; }}
.t {{ font-family:'your display typeface'; font-weight:200; color:{ink}; text-transform:lowercase;
  letter-spacing:0.02em; line-height:1.42; text-align:center; flex:0 0 auto;
  white-space:nowrap; }}
/* The body matches the number's family weight rather than the band's hairline 200, and keeps
   the copy's own capitalisation instead of forcing lowercase. */
.blk.left .t {{ text-align:left; margin-top:{hgap}px; font-weight:300;
  text-transform:none; }}
/* The lead-in number on each item. One step heavier so the list reads as a list without
   introducing a second size, which is the same restraint the band uses. */
.t b {{ font-weight:300; }}
.t em {{ font-style:normal; text-decoration:underline; text-underline-offset:0.18em;
  text-decoration-thickness:0.04em; }}
/* Emphasis on the canonical layout is a HIGHLIGHTER, not an underline. `box-decoration-break`
   is load bearing: Chrome's default slices one background across every line fragment of an
   inline, so a three-line highlight came out as one stroke stretched and cut into thirds.
   Cloning gives each line its own complete stroke, which is how a marker actually works. */
.blk.left .t em {{ text-decoration:none;
  background-image:url("{hl}");
  background-repeat:no-repeat; background-size:100% 0.92em; background-position:0 0.10em;
  -webkit-box-decoration-break:clone; box-decoration-break:clone;
  padding:0 0.10em; margin:0 -0.10em; }}
/* An authored blank line on the left layout. Shorter than a full line so the beats stay
   separated without the page paying a whole line of height for each one: in a 432px measure
   the copy breaks to twice as many lines, and three full-height blanks were holding the body
   down to 29px. The centred layout keeps its full-height blanks, because U4 and U7 are set on
   them and their pages have height to spare. */
.blk.left .t i.gap {{ display:inline-block; height:0.34em; }}
"""

# The header and the body solve SEPARATELY, and the header solves first.
#
# Solving them as one block is wrong: the header is one short line and the body is a dozen, so a
# single solver drives both down to whatever the body needs and the header stops reading as a
# header. Here the number and header take their own sizes, shrinking only if a long header would
# overrun the column, and the body gets whatever height is left.
FIT_JS = """
document.fonts.load('200 100px "your display typeface"', 'AZ09').then(function{
  return document.fonts.ready;
}).then(function{
  const el = document.querySelector('.t'), box = el.parentElement;
  const cs = getComputedStyle(box);
  const room = box.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
  // The measure is the box's CONTENT width less `.t`'s own left margin, which is zero on the
  // canonical layout because nothing is indented. Dropping the padding terms here once handed
  // the centred layout 1080px instead of 888 and silently resized every U4 and U7 information
  // page, which is the kind of drift the sibling checksum exists to catch.
  const wide = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)
             - parseFloat(getComputedStyle(el).marginLeft);
  const head = document.querySelector('.head');
  let headH = 0;
  if (head) {
    const hdr = head.querySelector('.hdr');
    head.querySelector('.num').style.fontSize = NUMPX + 'px';
    let hp = HDRPX;
    hdr.style.fontSize = hp + 'px';
    while (hp > 24 && hdr.scrollWidth > wide + 1) { hp -= 2; hdr.style.fontSize = hp + 'px'; }
    headH = head.getBoundingClientRect.height + parseFloat(getComputedStyle(el).marginTop);
  }
  const avail = room - headH;
  // The cap is layout-dependent. Raising it globally let U4's and U7's closes, which
  // were both sitting ON the old 78px ceiling, solve larger and silently redraw two
  // cards that are already on the board.
  let lo = 20, hi = MAXPX, best = 20;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    el.style.fontSize = mid + 'px';
    if (el.getBoundingClientRect.height <= avail && el.scrollWidth <= wide + 1) {
      best = mid; lo = mid + 1;
    } else { hi = mid - 1; }
  }
  if (FORCEPX) best = FORCEPX;
  el.style.fontSize = best + 'px';
  document.title = best + 'px ' + Math.round(el.getBoundingClientRect.height) + '/' + Math.round(avail);
});
""".replace("NUMPX", "104").replace("HDRPX", "62")


def _spans(lines):
    """Escape, join, THEN resolve the markers.

    Resolving them line by line broke any `[[accent]]` that spanned an authored line break:
    the opening line had no closing `]]` so nothing matched and the brackets rendered as
    literal text on the card. Joining first means a marker can wrap across lines the way the
    copy actually reads.

    An authored blank line becomes a SHORT gap, not an empty line. In a 432px measure the copy
    breaks to roughly twice as many lines as it did at full width, and at that point three
    full-height blanks were eating about two and a half lines of height and holding the whole
    page down to 29px. The gap keeps the beats separated and gives the height back to the type.
    """
    joined = "<br>".join(html.escape(ln) if ln else '<i class="gap"></i>' for ln in lines)
    joined = re.sub(r"\[\[(.+?)\]\]", r"<em>\1</em>", joined, flags=re.S)
    joined = re.sub(r"\{\{(.+?)\}\}", r"<b>\1</b>", joined, flags=re.S)
    return joined


def render_sheet(lines, png, sheet=SHEET, chrome=None, header=None, n=None, force_px=None):
    """One information slide: a left-weighted block of type over the paper sheet.

    `n` is the slide's place on the O-spine, which runs across the whole carousel rather than
    restarting per page, and `header` is its 1 to 4 word title. Pass neither and the page
    renders as body copy alone, which is what the sibling carousels still do.

    `force_px` overrides the solved body size. Pages solve to different sizes because they carry
    different amounts of copy, and three pages at 45, 42 and 41px read as three pages that could
    not agree. The caller solves every page first, then re-renders them all at the smallest
    result, which is the same instinct `band.py` follows when it optimises for even colour
    rather than for the most lines.
    """
    css = CSS.format(a=ASSETS, w=W, h=H, pad=PAD, ink=INK, left=LEFT, colw=COLW,
                     hgap=HEAD_GAP, hl=highlighter)
    art = f'<img class="sheet" src="{Path(sheet).resolve.as_uri}">'
    head = ""
    if header:
        num = f"O{n}" if n else ""
        head = (f'<div class="head"><span class="num">{html.escape(num)}</span>'
                f'<span class="hdr">{html.escape(header)}</span></div>')
    doc = (f'<meta charset="utf-8"><style>{css}</style><div class="card">{art}'
           f'<div class="blk{" left" if header else ""}">{head}'
           f'<div class="t">{_spans(lines)}</div></div>'
           f'</div><script>{FIT_JS.replace("FORCEPX", str(force_px or 0)).replace("MAXPX", "120" if header else "78")}</script>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    png = Path(png)
    png.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run([chrome or CHROME, "--headless", "--disable-gpu",
                        "--virtual-time-budget=4000", "--hide-scrollbars",
                        f"--window-size={W},{H}", f"--screenshot={png}", Path(tmp).as_uri],
                       check=True, capture_output=True)
        dom = subprocess.run([chrome or CHROME, "--headless", "--disable-gpu",
                              "--virtual-time-budget=4000", "--hide-scrollbars",
                              f"--window-size={W},{H}", "--dump-dom", Path(tmp).as_uri],
                             capture_output=True, text=True)
        m = re.search(r"<title>(.*?)</title>", dom.stdout)
        return m.group(1) if m else "?"
    finally:
        os.unlink(tmp)


if __name__ == "__main__":
    print("sheet ->", build_sheet)
