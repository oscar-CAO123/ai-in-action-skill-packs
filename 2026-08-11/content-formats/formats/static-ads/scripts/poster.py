#!/usr/bin/env python3
"""The candidate poster engine: type, plate, type. Three even thirds of a 1080x1350 frame.

    from poster import render_poster
    render_poster(top, bottom, png, ground="black", plate=Path("..."))

WHY THIS EXISTS. `band.py` sets one block of type in the bottom 506px and nothing above
y=844. the operator approved a new candidate-only layout on 2026-08-07: headline above the figure,
CTA below it, the plate in the middle. That geometry cannot come out of the band engine, so
it gets its own renderer rather than a flag on the old one.

THE LAYOUT (the operator picked "even thirds" off three mocks, 2026-08-07).

    0     ---------------------------  top type block, 450px
    450   ---------------------------  the plate, 1080x450
    900   ---------------------------  bottom type block, 450px
    1350

TWO GROUNDS.
  `black`  the card is black, the plate is INSET into the middle third. Type is white with
           one blue accent. This is u1a, the VHS mugshot card.
  `plate`  the plate is FULL BLEED at 1080x1350 and carries its own ground (generated paper,
           or plain white). Type composites over its top and bottom thirds in black. This is
           u1b and u4, where the ground is part of the generated image.

TYPE. your display typeface 200, all lowercase (the operator, 2026-08-07: both U1 variants go lowercase), centred,
capped small at 52px and set on an 84 per cent measure. The band law's justified-flush-both
setting belongs to the band and does not transfer to a poster. One `[[accent]]` span per
card, same syntax as band.py.

Each block is fitted independently and both blocks centre inside their own third. The cap
matters: without it the solver fills the third and the type shouts over a quiet painted
plate. the operator, 2026-08-07, on the first u1b composite: "significantly smaller, centre-aligned."
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
THIRD = H // 3                # 450
BLUE = "#1269FF"
PAD = 64
INK_DARK = "#0a0a0a"          # type on a paper or white ground, never pure #000


def _spans(lines):
    """`[[x]]` becomes the one accented span. Same contract as band.py."""
    out = []
    for ln in lines:
        parts, i = [], 0
        for m in re.finditer(r"\[\[(.+?)\]\]", ln):
            parts.append(html.escape(ln[i:m.start()]))
            parts.append(f'<em>{html.escape(m.group(1))}</em>')
            i = m.end()
        parts.append(html.escape(ln[i:]))
        out.append("".join(parts))
    return out


CSS = """
@font-face {{ font-family:'your display typeface'; font-weight:200; src:url('{a}/jost-200.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{a}/jost-300.ttf'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; }}
body {{ background:{bg}; overflow:hidden; }}
.card {{ position:relative; width:{w}px; height:{h}px; background:{bg}; }}
.bleed {{ position:absolute; inset:0; width:{w}px; height:{h}px; object-fit:cover;
  display:block; }}
.slot {{ position:absolute; left:0; top:{third}px; width:{w}px; height:{third}px;
  overflow:hidden; }}
.slot img {{ width:{w}px; height:{third}px; object-fit:cover; display:block; }}
.blk {{ position:absolute; left:0; width:{w}px; height:{third}px; padding:0 {pad}px;
  display:flex; flex-direction:column; }}
/* Both blocks centre inside their own third. With the type small, hugging the plate left all
   the empty paper stacked at the outer edges of the frame instead of around the words. */
.top {{ top:0; justify-content:center; padding-top:{pad}px; padding-bottom:40px; }}
.bot {{ top:{bot}px; justify-content:center; padding-top:40px; padding-bottom:{pad}px; }}
/* Centred and small, the operator 2026-08-07. Filling the third made the type shout over a quiet
   painted plate; the paper wants air around the words more than it wants scale. */
.t {{ font-family:'your display typeface'; font-weight:200; color:{ink}; text-transform:lowercase;
  letter-spacing:0.02em; line-height:1.32; flex:0 0 auto; text-align:center;
  width:92%; margin:0 auto; white-space:nowrap; }}
/* The CTA carries the card. the operator, 2026-08-07: "more prominent, stick out a little bit more,
   embolden it a little." One weight step (200 to 300) and a bigger cap, never further: the
   design system's edict is thin your display typeface around 400 and no fat your display typeface anywhere. */
.bot .t {{ font-weight:300; }}
.t em {{ font-style:normal; color:{accent}; }}
/* On a paper ground the accent colour IS the ink, so the one accented span would vanish. It
   carries an underline there instead, off the same `[[...]]` markup. */
.bot .t em {{ text-decoration:underline; text-underline-offset:0.18em;
  text-decoration-thickness:0.04em; }}
"""

FIT_JS = """
// The fit MUST wait for your display typeface. Measured against a fallback face the type comes back too
// small, then reflows wider the moment the webfont lands and overruns the third. And
// fonts.ready alone is a trap, same as band.py line 152: nothing has requested the face
// yet, so it resolves immediately. Ask for it explicitly, then wait.
document.fonts.load('200 100px "your display typeface"', 'AZ09').then(function(){
  return document.fonts.ready;
}).then(function(){
// Grow each block until it fills its third, then step back one. Measured, never guessed.
for (const el of document.querySelectorAll('.t')) {
  const box = el.parentElement;
  const room = () => box.clientHeight - parseFloat(getComputedStyle(box).paddingTop)
                     - parseFloat(getComputedStyle(box).paddingBottom);
  // hi was 96 and the solver always hit the ceiling. 52 is the "significantly smaller" cap.
  // The bottom block gets a higher one so the CTA outsizes the hook rather than matching it.
  let lo = 20, hi = box.classList.contains('bot') ? 64 : 52, best = 20;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    el.style.fontSize = mid + 'px';
    if (el.getBoundingClientRect().height <= room() && el.scrollWidth <= el.clientWidth + 1) {
      best = mid; lo = mid + 1;
    } else { hi = mid - 1; }
  }
  el.style.fontSize = best + 'px';
  el.dataset.px = best;
  el.dataset.h = Math.round(el.getBoundingClientRect().height) + '/' + Math.round(room());
}
document.title = [...document.querySelectorAll('.t')]
  .map(e => e.dataset.px + 'px ' + e.dataset.h).join(' | ');
});
"""


def render_poster(top, bottom, png, ground="black", plate=None, chrome=None, overlay=None):
    """Render one poster. `top` and `bottom` are lists of copy lines. Returns the fit report.

    `overlay` is raw SVG drawn in frame coordinates over the whole card, the same contract
    `band.py` already carries. Added 2026-08-07 for the F3 hospitality annotations.
    """
    if ground == "black":
        bg, ink, accent = "#000", "#fff", BLUE
    elif ground == "plate":
        bg, ink, accent = "#fff", INK_DARK, INK_DARK   # all black type, the operator 2026-08-07
    else:
        raise ValueError(f"unknown ground {ground!r}")

    css = CSS.format(a=ASSETS, w=W, h=H, bg=bg, third=THIRD, bot=H - THIRD, pad=PAD,
                     ink=ink, accent=accent)

    art = ""
    if plate:
        src = Path(plate).resolve().as_uri()
        if ground == "plate":
            art = f'<img class="bleed" src="{src}">'
        else:
            art = f'<div class="slot"><img src="{src}"></div>'
    elif ground == "black":
        art = ('<div class="slot" style="background:#1a1a1a;display:flex;'
               'align-items:center;justify-content:center">'
               '<span style="font-family:your display typeface;font-weight:200;font-size:22px;'
               'letter-spacing:.3em;color:#555">PLATE 1080 x 450</span></div>')

    over = ""
    if overlay:
        over = (f'<svg style="position:absolute;left:0;top:0;pointer-events:none" '
                f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">{overlay}</svg>')

    doc = (f'<meta charset="utf-8"><style>{css}</style><div class="card">{art}'
           f'<div class="blk top"><div class="t">{"<br>".join(_spans(top))}</div></div>'
           f'<div class="blk bot"><div class="t">{"<br>".join(_spans(bottom))}</div></div>'
           f'{over}</div><script>{FIT_JS}</script>')

    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    png = Path(png)
    png.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run([chrome or CHROME, "--headless", "--disable-gpu",
                        "--virtual-time-budget=4000", "--hide-scrollbars",
                        f"--window-size={W},{H}", f"--screenshot={png}",
                        Path(tmp).as_uri()],
                       check=True, capture_output=True)
        dom = subprocess.run([chrome or CHROME, "--headless", "--disable-gpu",
                              "--virtual-time-budget=4000", "--hide-scrollbars",
                              f"--window-size={W},{H}", "--dump-dom",
                              Path(tmp).as_uri()], capture_output=True, text=True)
        m = re.search(r"<title>(.*?)</title>", dom.stdout)
        return m.group(1) if m else "?"
    finally:
        os.unlink(tmp)
