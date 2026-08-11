#!/usr/bin/env python3
"""The newsprint-CLIPPING type engine: the copy is printed ON a torn piece of newspaper.

    from clip import render_card
    render_card("Breaking: Aussie retailers can finally stop [[hiring more staff to grow]].",
                "Take the Retail Ops AI Readiness Check ->",
                "Aussie retailers: stop [[hiring more staff to grow]].",
                "You are scaling the problem.", plate, Path("out/x.png"))

This is a sibling of `band.py`, not a replacement for it. `band.py` sets the canonical
news-carousel band: white your display typeface on black, bottom 506px, justified flush. This engine instead
runs the plate as a full-bleed photo carrying three things at once, top to bottom:

  * **A top your display typeface header**, "Breaking: [avatar] can finally stop [pain]", set over a black
    top-down fade so white type reads against whatever the photo is doing underneath, with a
    small CTA line beneath it naming the industry's lead magnet. you, .
  * **A black censorship bar over the subject's eyes**, replacing the pop-art sunglasses.
    Found by colour, not guessed: the glasses are the only saturated blue in the plate, so the
    bar is placed and angled off the actual blob rather than a fixed offset.
  * **A torn newspaper clipping** in the bottom right, printed with its own headline, the
    survivor of the earlier arrow-and-band passes. Its ground is either a paid i2i extract from
    `clip_paper.py` (preferred, and the only one that reads as a real page) or a synthetic paper
    built from real Library of Congress scans with HTML type laid over it, kept as a free
    fallback for a card that has not been shot yet.

No arrow. The first pass pointed one at the subject off the paper's edge; you, had it removed once the top header gave the card a stronger read on its own.
"""
import html
import math
import os
import re
import subprocess
import tempfile
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = Path(__file__).parent
SRC = ROOT / "collage-src"
WORK = ROOT / "clip-paper"
ASSETS = ROOT.parent / "assets"
CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W, H = 1080, 1350
BLUE = "#1269FF"
INK = "#141210"                 # newsprint black is never true black

# The clipping, in card coordinates before rotation. It is deliberately larger than the frame
# on two sides: a piece of paper that stops inside the frame reads as a pasted chip, which is
# the same note you gave on the collage bed. Left/top are torn, right/bottom bleed away.
CLIP_X, CLIP_Y, CLIP_W, CLIP_H = 420, 930, 740, 525
CLIP_ROT = -7
# The measure is narrower than the paper it sits on. The clipping is rotated and bleeds off two
# edges, so the card's own right edge cuts the paper at about x=658 at the foot of the block and
# the card's bottom edge cuts it at about y=381 at the left margin. Those two numbers are the
# white space, and the type is set to fill it.
PAD_X, PAD_TOP, MEASURE = 44, 30, 600
TEXT_H = 335

# The top header's vertical budget, and it is a HARD one because it is what keeps the block off
# the subject's head. `collage_news.SUBJ_H` bottom-anchors the cut-out, so the crown lands at
# H - int(H * SUBJ_H) + 12 = y=350 on every card. The header must finish above that with room to
# spare: at 268 of headline the construction card ran three lines at 76px and bottomed out at
# y=348, two pixels clear, which is not a margin. These four numbers are the whole budget.
HDR_TOP = 46                    # where the header block starts
HDR_GAP = 22                    # headline to CTA
HDR_CTA = 29                    # the CTA line's own height at 24px
HDR_BOTTOM = 330                # the block may not cross this, 20px clear of the crown
HDR_AVAIL = HDR_BOTTOM - HDR_TOP - HDR_GAP - HDR_CTA


def _rng(key):
    return np.random.default_rng(zlib.crc32(key.encode) & 0xFFFFFFFF)


def _scan_crop(key, salt, ar, out_w, lo, hi, grain=0.045, zoom=(0.55, 0.85), blur=0.0):
    """A real LOC scan, cropped at aspect `ar`, its range squeezed into `lo..hi`.

    Same compression trick as the collage bed: squeezing both ends of a real scan is what turns
    a photograph of a page into a printable ground. `lo`/`hi` near 1.0 give paper for a headline
    to sit on; a wide range gives a column of type that still reads as type.

    `zoom` matters as much as the range. The scans are only about 1,000px wide, so a crop of
    half a page blown up to the clipping reproduces the page's display ads at headline size, and
    they fight our headline however pale they are. A full-page crop puts the same ink on the
    paper at texture scale instead.
    """
    scans = sorted(SRC.glob("*.jpg"))
    if not scans:
        raise SystemExit("no scans in collage-src/")
    r = _rng(key + salt)
    im = Image.open(scans[int(r.integers(len(scans)))]).convert("L")
    cw = int(im.width * float(r.uniform(*zoom)))
    ch = int(cw / ar)
    if ch > im.height:
        ch = im.height
        cw = int(ch * ar)
    x = int(r.integers(0, max(1, im.width - cw)))
    y = int(r.integers(0, max(1, im.height - ch)))
    im = im.crop((x, y, x + cw, y + ch)).resize((out_w, int(out_w / ar)), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im, dtype=np.float32) / 255.0
    a = lo + (a - a.min) / max(float(np.ptp(a)), 1e-6) * (hi - lo)
    g = r.normal(0, 1, a.shape).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 40 + 128).clip(0, 255)).astype(np.uint8))
.filter(ImageFilter.GaussianBlur(0.5)), dtype=np.float32) / 255.0
    return np.clip(a + (g - g.mean) * grain, 0, 1)


def paper(key):
    """The clipping's ground: lifted newsprint, warm, with light falling off to the low right.

    Built as a 2x2 mosaic of four different scans rather than one crop, and that is the whole
    point of it. The scans are about 1,000px wide, so any single-page crop reproduces the page's
    display ads at roughly our headline size and they fight the headline however pale they are:
    the card reads as a double exposure instead of as a printed page. Quartering the paper drops
    the scan's own type to column scale, which is what a headline is supposed to sit on. The
    seams are darkened slightly and read as gutters.
    """
    w, h = CLIP_W * 2, CLIP_H * 2
    a = np.zeros((h, w), dtype=np.float32)
    for i in range(4):
        q = _scan_crop(key, f"paper{i}", (w / 2) / (h / 2), w // 2, 0.905, 0.999,
                       zoom=(0.94, 1.0), blur=1.1)
        a[(i // 2) * (h // 2):(i // 2 + 1) * (h // 2),
          (i % 2) * (w // 2):(i % 2 + 1) * (w // 2)] = q[:h // 2, :w // 2]
    a[:, w // 2 - 3:w // 2 + 3] *= 0.985
    a[h // 2 - 3:h // 2 + 3, :] *= 0.985
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.hypot((xx / w - 0.30) / 1.05, (yy / h - 0.18) / 1.05)
    a = np.clip(a * (1.0 - 0.06 * np.clip(d, 0, 1) ** 1.6), 0, 1)
    rgb = np.stack([a * 1.000, a * 0.977, a * 0.928], axis=2)         # aged paper warmth
    p = WORK / f"{key}-paper.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(p)
    return p


def torn(key, jag=13, step=34):
    """clip-path polygon for the paper: torn down the left and across the top, bleeding right.

    Paper tears in short irregular runs, so each edge walks in `step` moves with a seeded kick.
    The right and bottom edges are pushed past the element bounds because they leave the frame
    and a tear there would never be seen.
    """
    r = _rng(key + "tear")
    pts = []
    for y in range(0, CLIP_H + step, step):                    # left edge, top to bottom
        pts.append((float(r.normal(6, jag)), float(min(y, CLIP_H))))
    pts.append((-6.0, CLIP_H + 8.0))
    pts.append((CLIP_W + 8.0, CLIP_H + 8.0))
    pts.append((CLIP_W + 8.0, -6.0))
    for x in range(CLIP_W, -step, -step):                      # top edge, right to left
        pts.append((float(max(x, 0)), float(r.normal(7, jag))))
    return ", ".join(f"{x:.1f}px {y:.1f}px" for x, y in pts)


# The pop-art lenses are generated as flat bright blue with a Ben-Day dot fill (see
# WEARING/GLASSES in cut_news.py), which nothing else on any of these five plates is: not the
# hi-vis, not the sky, not the collage bed behind. So the lens colour is a reliable detector for
# WHERE the glasses are, and the censor bar is placed and angled off that, not off a guessed
# coordinate the way the old arrow's tip was before it was rewritten to search the matte.
LENS = lambda r, g, b: (b > 0.55) & ((b - r) > 0.20) & (g > r)         # noqa: E731
LENS_MIN_PX = 400                                              # drop stray blue specks this size


def censor_bar(plate_png, pad_along=1.12, pad_across=1.55):
    """A black bar over the eyes, sized and angled off the actual sunglasses blob.

    Returns (cx, cy, width, height, angle_degrees) in card pixels, or None if no plate carries
    the pop-art lens colour (shouldn't happen on these five, but a card without it should not
    crash rather than silently mis-censor). PCA on the kept pixels gives the long axis of the
    lenses, which is the same axis the eyes sit on whatever the head's tilt, so the bar rotates
    with the face instead of assuming it is level.
    """
    a = np.asarray(Image.open(plate_png).convert("RGB"), dtype=np.float32) / 255.0
    mask = LENS(a[..., 0], a[..., 1], a[..., 2])
    lab, n = ndimage.label(mask)
    if not n:
        return None
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i in range(n) if sizes[i] > LENS_MIN_PX])
    if not keep.any:
        return None
    ys, xs = np.where(keep)
    pts = np.stack([xs, ys], axis=1).astype(np.float64)
    mean = pts.mean(axis=0)
    cov = np.cov((pts - mean).T)
    evals, evecs = np.linalg.eigh(cov)
    major, minor = evecs[:, np.argmax(evals)], evecs[:, np.argmin(evals)]
    # macOS Accelerate throws spurious divide/overflow/invalid warnings on this exact matmul
    # shape even though the result is finite and correct (checked by hand against the cov/eigh
    # inputs above); silenced rather than left to spam three lines of noise per card.
    with np.errstate(all="ignore"):
        proj_m, proj_n = (pts - mean) @ major, (pts - mean) @ minor
    half_w = float(max(abs(proj_m.min), abs(proj_m.max))) * pad_along
    half_h = float(max(abs(proj_n.min), abs(proj_n.max))) * pad_across
    angle = math.degrees(math.atan2(major[1], major[0]))
    angle = angle - 180 if angle > 90 else (angle + 180 if angle < -90 else angle)
    return float(mean[0]), float(mean[1]), half_w * 2, half_h * 2, angle


def markup(s, accent=INK):
    """`[[...]]` becomes the accent colour. Everything else is escaped."""
    out, i, on = [], 0, False
    while i < len(s):
        if s.startswith("[[", i):
            out.append(f'<span style="color:{accent}">')
            on, i = True, i + 2
        elif s.startswith("]]", i):
            out.append("</span>")
            on, i = False, i + 2
        else:
            out.append(html.escape(s[i]))
            i += 1
    if on:
        out.append("</span>")
    return "".join(out)


def _autosize_js(sel, avail, min_, max_):
    """Shrink `sel`'s font until its wrapped height clears `avail`. One block, natural wrap.

    This is deliberately simpler than `band.py`'s balanced-line fit: the header is a single
    short sentence that only needs to wrap and shrink, not justify flush on both margins the
    way the house band does, so there is no line-count search to run here.
    """
    return f"""
(function{{
  var el=document.querySelector('{sel}');
  if(!el) return;
  var size={max_};
  for(;size>={min_};size-=1){{
    el.style.fontSize=size+'px';
    if(el.getBoundingClientRect.height<=({avail})) break;
  }}
}});
"""


def render_card(topline, cta, head, deck, png, plate, chrome=None):
    """Render one card. Returns the fit report string.

    `topline`/`cta` are the new top-of-frame your display typeface header and its CTA line, always rendered.
    `head`/`deck` are the newspaper clipping's own copy, used only as a fallback when no paid
    extract exists yet for this card; once `clip_paper.py` has shot one, the extract carries its
    own baked-in headline and `head`/`deck` are ignored.
    """
    key = Path(png).stem.split("-clip")[0]
    extract = WORK / f"{key}-news.png"
    if extract.exists:
        return _render(png, plate, extract, None, None, topline, cta, chrome)
    # No body strip on the synthetic ground: the type fills the cutting, so there is no white
    # left under it for a column of newsprint to sit in.
    return _render(png, plate, paper(key), None, (head, deck), topline, cta, chrome)


def _render(png, plate, ground, bod, type_, topline, cta, chrome):
    key = Path(png).stem.split("-clip")[0]
    bar = censor_bar(plate)
    css = f"""
/* The locked design system, context/design-system/SCHEMA.md section 2: display type is weight
   200, labels are 500 to 600, and NOTHING ABOVE 600 EXISTS. Do not load a bold face here. The
   first pass set this header in your display typeface Bold 700 and it stopped looking like house on sight, which
   is the exact failure that file warns about: "a bold heading is the single fastest way to make
   a page stop being ours". */
@font-face {{ font-family:'your display typeface'; font-weight:200; src:url('{ASSETS}/jost-200.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500; src:url('{ASSETS}/jost-500.ttf'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; overflow:hidden; background:#000; }}
.card {{ position:relative; width:{W}px; height:{H}px; background:#000; overflow:hidden; }}
.plate {{ position:absolute; inset:0; width:{W}px; height:{H}px; object-fit:cover; }}
.censor {{ position:absolute; left:0; top:0; background:#000; }}
/* The top-down fade. It has to hold its density all the way past the CTA line, not just under
   the headline: at a gentler falloff the blue CTA crossed the retail subject's pale hat and the
   real-estate subject's hair and stopped reading. The header block bottoms out near y=290, so
   the fade stays near-opaque to there and only then falls away. */
.topfade {{ position:absolute; left:0; top:0; width:{W}px; height:470px;
        background:linear-gradient(to bottom, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.88) 55%,
                                   rgba(0,0,0,0.66) 72%, rgba(0,0,0,0.24) 88%,
                                   rgba(0,0,0,0) 100%); }}
.topline {{ position:absolute; left:64px; top:{HDR_TOP}px; width:{W - 128}px; }}
/* Hero H1 role: 200, lh 1.1, ls -0.025em, #f8fafc. Large, thin, tightly tracked. */
.topline .headline {{ font-family:'your display typeface'; font-weight:200; color:#f8fafc;
        line-height:1.10; letter-spacing:-0.025em;
        text-shadow:0 2px 22px rgba(0,0,0,0.75); }}
/* Small label role: 500, uppercase, ls 0.08em to 0.12em, in the system blue. Scaled off the
   schema's 13px to suit a 1080px ad rather than a web column. */
.topline .cta {{ font-family:'your display typeface'; font-weight:500; color:{BLUE}; font-size:24px;
        line-height:{HDR_CTA}px; letter-spacing:0.10em; text-transform:uppercase;
        margin-top:{HDR_GAP}px;
        text-shadow:0 1px 12px rgba(0,0,0,0.95), 0 0 4px rgba(0,0,0,0.85); }}
/* No band any more, so nothing needs a fade to sit on. This is grounding only. */
.vig {{ position:absolute; left:0; bottom:0; width:{W}px; height:520px;
       background:linear-gradient(to top, rgba(0,0,0,0.42), rgba(0,0,0,0)); }}
.hold {{ position:absolute; left:{CLIP_X}px; top:{CLIP_Y}px; width:{CLIP_W}px; height:{CLIP_H}px;
        transform:rotate({CLIP_ROT}deg); transform-origin:50% 50%;
        filter:drop-shadow(0 14px 30px rgba(0,0,0,0.86))
               drop-shadow(0 2px 3px rgba(0,0,0,0.5)); }}
.clip {{ position:absolute; inset:0; clip-path:polygon({torn(key)}); overflow:hidden; }}
.clip .ground {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
/* A generated extract carries the headline across its own full width, so it can never be
   cropped horizontally: `cover` took the first and last word off the line. It is fitted to the
   width instead and allowed to fall short at the foot, which is off frame in any case. */
.clip .extract {{ position:absolute; left:0; top:0; width:100%; height:auto; }}
.type {{ position:absolute; left:{PAD_X}px; top:{PAD_TOP}px; width:{MEASURE}px; }}
.kicker {{ height:0; border-top:2.5px solid {INK}; border-bottom:1px solid {INK};
          padding-top:5px; margin-bottom:22px; opacity:0.82; }}
.head {{ font-family:'Times New Roman',Times,serif; font-weight:700; color:{INK};
        line-height:0.98; letter-spacing:-0.012em; }}
/* NO BLUE ON THE NEWSPRINT. A newspaper prints one ink; the accent lives on the header above. */
.deck {{ font-family:'Times New Roman',Times,serif; font-weight:400; color:rgba(20,18,16,0.88);
        line-height:1.26; letter-spacing:0.004em;
        border-top:1px solid rgba(20,18,16,0.55); padding-top:14px; }}
.body {{ position:absolute; left:{PAD_X}px; right:0; top:{PAD_TOP + TEXT_H + 20}px;
        width:{CLIP_W}px; opacity:0.72; }}
"""
    layers = []
    if bar:
        cx, cy, bw, bh, ang = bar
        layers.append(f'<div class="censor" style="left:{cx - bw / 2:.1f}px; '
                      f'top:{cy - bh / 2:.1f}px; width:{bw:.1f}px; height:{bh:.1f}px; '
                      f'transform:rotate({ang:.2f}deg);"></div>')
    layers.append('<div class="topfade"></div>')
    layers.append(f'<div class="topline"><div class="headline">{markup(topline, BLUE)}</div>'
                  f'<div class="cta">{html.escape(cta)}</div></div>')
    layers.append('<div class="vig"></div>')
    cls = "ground" if type_ else "extract"
    clip_inner = f'<img class="{cls}" src="{Path(ground).resolve.as_uri}">'
    if bod:
        clip_inner += f'<img class="body" src="{Path(bod).resolve.as_uri}">'
    if type_:
        clip_inner += (f'<div class="type"><div class="kicker"></div>'
                       f'<div class="head">{markup(type_[0])}</div>'
                       f'<div class="deck">{markup(type_[1])}</div></div>')
    layers.append(f'<div class="hold"><div class="clip">{clip_inner}</div></div>')
    js = (_autosize_js(".topline .headline", HDR_AVAIL, 30, 76)
          + (_autosize_js(".head", TEXT_H, 24, 128) if type_ else ""))
    # The measured bottom of the header block goes into the report so the budget above is
    # checked against what actually rendered, not against arithmetic.
    report = ('var _t=document.querySelector(".topline");'
              'document.documentElement.dataset.fitted="topline "'
              '+getComputedStyle(document.querySelector(".topline .headline")).fontSize'
              '+", block ends y="+Math.round(_t.getBoundingClientRect.bottom)'
              '+(document.querySelector(".head")?", head "'
              '+getComputedStyle(document.querySelector(".head")).fontSize:"");')
    doc = (f'<meta charset="utf-8"><style>{css}</style><div class="card">'
           f'<img class="plate" src="{Path(plate).resolve.as_uri}">'
           f'{"".join(layers)}</div>'
           # The headline text is in the markup from the start (unlike band.py, which injects
           # into an empty div after load), so the browser requests your display typeface as the DOM parses. Both
           # weights are still asked for BY NAME AND WEIGHT before the fit: band.py records that
           # a bare lookup misses a face that only ships at 200, which silently sizes the block
           # against fallback metrics about 1.4x wider.
           f'<script>Promise.all([document.fonts.load(\'200 100px "your display typeface"\', "AZ09"),'
           f'document.fonts.load(\'500 24px "your display typeface"\', "AZ09")])'
           f'.then(function{{ return document.fonts.ready; }})'
           f'.then(function{{ {js}\n{report} }});</script>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    exe = chrome or CHROME
    png = Path(png)
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    "--virtual-time-budget=6000",
                    f"--screenshot={png}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    dom = subprocess.run([exe, "--headless", "--disable-gpu", "--virtual-time-budget=6000",
                          "--dump-dom", f"file://{tmp}"], capture_output=True, text=True).stdout
    Path(tmp).unlink
    if not bar:
        print("  no censor bar placed, no lens colour found on the plate")
    m = re.search(r'data-fitted="([^"]+)"', dom)
    fitted = m.group(1) if m else "?"
    ends = re.search(r"block ends y=(\d+)", fitted)
    if ends and int(ends.group(1)) > HDR_BOTTOM:
        print(f"  HEADER OVERRUNS ITS BUDGET: ends y={ends.group(1)}, "
              f"limit {HDR_BOTTOM}, crown at 350. This card sits on the subject's head.")
    return fitted
