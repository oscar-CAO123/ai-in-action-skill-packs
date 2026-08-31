#!/usr/bin/env python3
"""Rough magazine cutouts, and the fan they sit in. FREE, no generation.

    python3 cutouts.py --demo        # writes one cut piece to /tmp for eyeballing

Spec of record: `engine/reference-bank/style-packs/paper-cutouts/STYLE-GUIDE.md`.

A cutout is a SUBJECT masked out of an existing frame, given a pure white border with a rough
imperfect edge, textured so it does not look too perfect, and dropped with a soft shadow so it
reads as stuck on top of the page.

THE EDGE IS GENERATED, NOT DRAWN. A clean vector outline reads as a sticker. The cut path is
displaced by seeded value noise, the same idea as the `#rough` turbulence filter the F8 loop
diagram applies to its tiles, so every piece tears differently and none of them tears twice the
same way.

MASKING. The oil-on-paper plates key on luma for nothing: black paint against bare paper. The
VHS and F8 frames are photographic and will not key, and `rembg` is not installed (it goes
through the `dependency-audit` skill and your go first), so `mask_luma` is the only matte
this file carries today. `mask_rect` is the fallback: the whole frame as a torn rectangle.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).parent
BORDER = 0.028        # white border, as a share of the longest side (halved ROUGH = 0.034         # edge displacement, as a share of the longest side
SHADOW = (10, 14, 26) # (dx, dy, blur) for the drop shadow


def _noise(shape, seed, octaves=(6, 13, 29)):
    """Seeded value noise in [-1,1], smooth enough to tear paper rather than serrate it."""
    rng = np.random.default_rng(seed)
    acc = np.zeros(shape, dtype=np.float32)
    amp = 1.0
    for o in octaves:
        g = rng.normal(0, 1, (o, o)).astype(np.float32)
        up = np.asarray(Image.fromarray(((g - g.min()) / max(np.ptp(g), 1e-6) * 255)
.astype(np.uint8)).resize(shape[::-1], Image.BICUBIC),
                        dtype=np.float32) / 255.0
        acc += (up - 0.5) * amp
        amp *= 0.55
    return np.clip(acc / max(np.abs(acc).max(), 1e-6), -1, 1)


def mask_luma(im, thresh=0.62, close=9):
    """Matte a painted plate: everything darker than bare paper is the subject.

    The oil plates are the one family that keys for free, so this is where cutting starts. The
    close pass fills the paper-coloured gaps INSIDE a figure (the head void on the mascot
    plates, the bare paper between a coat and an arm), which would otherwise punch holes
    through the middle of the cut piece.
    """
    a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    m = (a < thresh).astype(np.uint8) * 255
    mi = Image.fromarray(m)
    mi = mi.filter(ImageFilter.MaxFilter(close)).filter(ImageFilter.MinFilter(close))
    return mi


def trim_dark(im, tol=38):
    """Crop a uniform surround off a photographic plate, whatever colour it is.

    Every style tail in this rig bans letterboxing and a frame within the frame, and the models
    do it anyway in both directions: the O1 hero came back with hard BLACK bars top and bottom,
    and the O2 press hero came back as a print mounted on a pale GREY card. A torn print of
    either is a torn print of a border.

    So the trim reads the surround's colour off the corners rather than assuming black, and eats
    rows and columns inward only while they stay within `tol` of it. A plate with no surround
    loses nothing, because its first row already differs.
    """
    a = np.asarray(im.convert("RGB"), dtype=np.float32)
    h, w = a.shape[:2]
    corners = np.stack([a[0, 0], a[0, w - 1], a[h - 1, 0], a[h - 1, w - 1]])
    # The median of the four corners, so one corner carrying picture cannot set the reference.
    ref = np.median(corners, axis=0)
    flat = (np.abs(a - ref).max(axis=2) <= tol)
    rows = flat.mean(axis=1) < 0.94        # a row that is almost entirely surround
    cols = flat.mean(axis=0) < 0.94
    if not rows.any() or not cols.any():
        return im
    y0, y1 = int(np.argmax(rows)), len(rows) - int(np.argmax(rows[::-1]))
    x0, x1 = int(np.argmax(cols)), len(cols) - int(np.argmax(cols[::-1]))
    return im.crop((x0, y0, x1, y1))


def trim_border(im, thresh=70, frac=0.6, seed_frac=0.5, rounds=2):
    """Eat a dark RING off a plate, which is the failure `trim_dark` cannot reach.

    `trim_dark` removes a uniform surround by reading its colour off the corners. That handles a
    plate floating on a pale mount or sitting in black bars. It does NOT handle the third thing
    the models keep doing, which the u4-o1 plate came back as: a picture inset in a white page
    AND ruled with a hard black border. The corners say white, so the trim stops the moment it
    meets the black rule and leaves the rule in, and a polaroid of that is a print of a frame
    inside a frame inside a frame.

    So this walks each side inward for as long as that whole line is mostly dark, which eats a
    rule of any thickness and stops the instant real picture appears. A plate with no rule loses
    nothing, because its first line already fails the test.

    DESTRUCTIVE ON A DARK PICTURE, so call it only on a plate you have LOOKED AT and confirmed
    is ruled. It seeds on the lines that are mostly dark, and a photograph that simply has a big
    dark field reads as its own frame: u4-o3 has no border at all and this took it from 1968 rows
    to 1122, eating the bottom third. `build_u4.RAW_TO_CLEAN` carries the per-plate opt-in.

    ADDITIVE, : nothing already built calls it. `polaroid` is deliberately left alone
    because U3 is shipped and live and its three plates trim identically either way.
    """
    a = np.asarray(im.convert("L"), dtype=np.int32)
    h, w = a.shape
    dark = a < thresh
    # SEED ON THE RING, not on the outer edge. Walking inward from the edge does nothing here:
    # outside the rule is the white page, so the very first line fails the dark test and the
    # walk stops before it starts. So find the lines that are mostly dark first, and take their
    # bounding box as the starting frame.
    # The SEED is looser than the walk. At the walk's own 0.6 the ruled plate found no
    # rows at all and the whole pass silently did nothing.
    rows = np.where(dark.mean(axis=1) > seed_frac)[0]
    cols = np.where(dark.mean(axis=0) > seed_frac)[0]
    if not len(rows) or not len(cols):
        return im
    y0, y1 = int(rows.min()), int(rows.max()) + 1
    x0, x1 = int(cols.min()), int(cols.max()) + 1
    for _ in range(rounds):
        before = (y0, y1, x0, x1)
        while y0 < y1 - 1 and (a[y0, x0:x1] < thresh).mean() > frac:
            y0 += 1
        while y1 > y0 + 1 and (a[y1 - 1, x0:x1] < thresh).mean() > frac:
            y1 -= 1
        while x0 < x1 - 1 and (a[y0:y1, x0] < thresh).mean() > frac:
            x0 += 1
        while x1 > x0 + 1 and (a[y0:y1, x1 - 1] < thresh).mean() > frac:
            x1 -= 1
        if (y0, y1, x0, x1) == before:
            break
    return im.crop((x0, y0, x1, y1))


def mask_rect(im, inset=0.0):
    """The whole frame as a piece: a torn print rather than a masked subject.

    THIS IS WHAT EVERY PHOTOGRAPHIC PLATE USES TODAY. `mask_luma` was tried on the live-action
    VHS heroes and fails twice over: those frames are dark overall, so the threshold takes the
    whole frame as subject, and the one genuinely bright area, the screen-lit cheek, comes out
    ABOVE the threshold and gets punched out as a hole through the middle of the face.

    Keying a photograph needs a real matte, which means `rembg`, which is not installed and goes
    through the `dependency-audit` skill and your go first. Until then a live-action hero is a
    torn rectangular print, which is a real magazine-cutout look in its own right rather than a
    compromise: the tear and the white border still do the work.
    """
    w, h = im.size
    m = Image.new("L", (w, h), 0)
    d = int(min(w, h) * inset)
    m.paste(255, (d, d, w - d, h - d))
    return m


def _tear(mask, seed, amount):
    """Push the mask's edge around with noise so the cut is torn rather than machined."""
    a = np.asarray(mask, dtype=np.float32) / 255.0
    n = _noise(a.shape, seed)
    # Displace by thresholding a blurred mask against the noise field: where the noise is high
    # the edge pulls in, where it is low it pushes out. Blurring first is what makes the result
    # a wandering edge rather than a fringe of speckle.
    b = np.asarray(Image.fromarray((a * 255).astype(np.uint8))
.filter(ImageFilter.GaussianBlur(amount * 0.9)), dtype=np.float32) / 255.0
    return Image.fromarray(((b + n * 0.42 > 0.5) * 255).astype(np.uint8))


def _texture(im, seed):
    """Rough the interior up so the piece does not look freshly rendered.

    Print grain plus a slight uneven exposure across the piece, which is what a real cutout off
    a printed page carries. Small numbers on purpose: this reads at a glance, never as an effect.
    """
    a = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, a.shape[:2]).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 40 + 128).clip(0, 255)).astype(np.uint8))
.filter(ImageFilter.GaussianBlur(0.5)), dtype=np.float32) / 255.0
    a = a + (g - g.mean())[..., None] * 0.085
    a = a * (1.0 + _noise(a.shape[:2], seed + 1, octaves=(3, 5))[..., None] * 0.10)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


# The seven F8 grades, as flat tints. The real chains are ffmpeg and live in that format's
# `grade_plate.sh`; a cutout is one small still on a cream page, so it takes the tint the grade
# lands on rather than the whole chain. Named identically so the two never drift apart.
TINTS = {
    "none": None,
    "vhs": (198, 202, 214),
    "film16": (214, 205, 186),
    "super8": (222, 199, 168),
    "betacam": (196, 206, 210),
    "cctv": (200, 202, 198),
    "press": (206, 206, 206),
}


def cut(src, seed=0, mask=None, tint="none", height=None):
    """One finished piece, RGBA, ready to paste. White border, torn edge, shadow included.

    `height` IS THE SUBJECT'S HEIGHT, not the source plate's. The plate is cut at native size
    and the result is then trimmed to what actually survived the mask before it is scaled, so a
    piece asked for at 1040px is 1040px of figure.

    Sizing the plate first was the earlier shape and it lies: an oil plate is mostly bare paper,
    so a 1040px plate carries maybe 500px of figure floating in a mostly empty canvas, and every
    placement is then computed against a footprint that does not exist. That is what put two
    thirds of the falling graduate off the card while the numbers said it fitted.
    """
    im = Image.open(src).convert("RGB")
    # Work at a sane resolution. Cutting at the plate's native 1782x2212 is correct and far too
    # slow: the noise field, the two tears and the texture pass all run per pixel, nine pieces a
    # carousel, and a build went from seconds to minutes. Twice the target height keeps more
    # detail than the finished piece can show, and the tear is scaled off the working size so
    # the edge is identical in character either way.
    if height and im.height > height * 2:
        work = height * 2
        im = im.resize((max(1, round(im.width * work / im.height)), work), Image.LANCZOS)
    m = mask if mask is not None else mask_luma(im)
    if m.size != im.size:
        m = m.resize(im.size, Image.NEAREST)

    long_side = max(im.size)
    m = _tear(m, seed, ROUGH * long_side)

    # Black and white always. Colour is refused on this page; a tint is applied over the grey,
    # never instead of it, so a tinted piece is still a monotone.
    body = ImageOps.grayscale(_texture(im, seed)).convert("RGB")
    if TINTS.get(tint):
        t = np.asarray(body, dtype=np.float32) / 255.0
        c = np.array(TINTS[tint], dtype=np.float32) / 255.0
        body = Image.fromarray((np.clip(t * c, 0, 1) * 255).astype(np.uint8))

    # The white border is the mask grown outward, and it gets its own tear so the paper edge and
    # the image edge are not the same line offset by a constant.
    grow = max(3, int(BORDER * long_side))
    edge = m.filter(ImageFilter.MaxFilter(grow if grow % 2 else grow + 1))
    edge = _tear(edge, seed + 7, ROUGH * long_side * 0.7)

    pad = grow + SHADOW[2] + max(SHADOW[0], SHADOW[1])
    W, H = im.width + pad * 2, im.height + pad * 2
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.paste((20, 18, 16, 105), (pad + SHADOW[0], pad + SHADOW[1]), edge)
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(SHADOW[2])))

    paper = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paper.paste((255, 255, 255, 255), (pad, pad), edge)
    out.alpha_composite(paper)

    art = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    art.paste(body, (pad, pad), m)
    out.alpha_composite(art)

    # Trim the empty canvas away, THEN scale, so `height` is the subject.
    box = out.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if box:
        out = out.crop(box)
    if height and out.height:
        out = out.resize((max(1, round(out.width * height / out.height)), height),
                         Image.LANCZOS)
    return out


POLA_SIDE = 0.055     # white frame on the two sides and the top, as a share of the width
POLA_FOOT = 0.215     # the deep bottom lip, which is what makes it read as a polaroid
POLA_STOCK = (250, 248, 242)


def polaroid(src, seed=0, height=520, tint="press", trim=True):
    """One polaroid print. FREE.

    you, after the torn-cutout passes fell short: every piece in the fan is a
    polaroid, and they fan out the way the cutouts did. That is a different object from a
    magazine cutout and it is built differently: a polaroid has a MACHINED white frame, thin on
    three sides and deep at the foot, so the tear and the ragged edge are gone. What carries the
    hand is the fan, the tilt and the shadow.

    The picture inside runs the degraded noir treatment: greyscale, the print grain and uneven
    exposure `_texture` already lays down, and one of the F8 tints. you named the O2 press
    frame as the reference for the lighting he wants.
    """
    im = Image.open(src).convert("RGB") if not isinstance(src, Image.Image) else src
    if trim:
        im = trim_dark(im)

    # The window is 4:5, the format's own shape, so every polaroid in a fan agrees.
    w = im.width
    win_h = round(w * 1.25)
    if im.height > win_h:
        top = (im.height - win_h) // 3      # bias up: faces sit in the upper half of a frame
        im = im.crop((0, top, w, top + win_h))
    else:
        win_h = im.height

    body = ImageOps.grayscale(_texture(im, seed)).convert("RGB")
    if TINTS.get(tint):
        t = np.asarray(body, dtype=np.float32) / 255.0
        c = np.array(TINTS[tint], dtype=np.float32) / 255.0
        body = Image.fromarray((np.clip(t * c, 0, 1) * 255).astype(np.uint8))

    side = max(6, round(w * POLA_SIDE))
    foot = max(18, round(w * POLA_FOOT))
    W, H = w + side * 2, win_h + side + foot
    pad = SHADOW[2] + max(SHADOW[0], SHADOW[1])
    out = Image.new("RGBA", (W + pad * 2, H + pad * 2), (0, 0, 0, 0))

    card = Image.new("RGBA", (W, H), POLA_STOCK + (255,))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sh.paste((18, 16, 14, 118), (pad + SHADOW[0], pad + SHADOW[1], pad + SHADOW[0] + W,
                                 pad + SHADOW[1] + H))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(SHADOW[2])))
    card.paste(body, (side, side))
    # A hairline inside the window, so the print sits IN the frame rather than on it.
    ImageDraw.Draw(card).rectangle([side - 1, side - 1, side + w, side + win_h],
                                   outline=(214, 210, 202), width=1)
    out.alpha_composite(card, (pad, pad))

    if height:
        out = out.resize((max(1, round(out.width * height / out.height)), height),
                         Image.LANCZOS)
    return out


def edge_band(size, seed=0, n=8, opacity=0.58, span=(-0.06, 1.06)):
    """A newspaper collage running down the right side and curving round both corners.

    THE THIRD DEPTH LAYER. The page had two: the editorial bed baked into
    the sheet, which is nearly subliminal, and the foreground of polaroids, shreds and ink marks
    at full strength. This sits between them, so the right side of the card has something
    happening in the middle distance instead of jumping from a whisper to a shout.

    It is a BAND, not a scatter. The pieces follow a curve that enters off the top edge, bows out
    to the right margin, runs down it, and turns back in at the bottom, and each piece is rotated
    to the tangent so the run reads as one gesture. Every piece bleeds off an edge or overlaps
    its neighbours, so nothing sits in the frame as a chip.

    Returns an RGBA layer to composite UNDER the fan.
    """
    W, H = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    rng = np.random.default_rng(seed)
    t0, t1 = span

    def point(t):
        """A quadratic bow: in at the top, out at the right margin, back in at the bottom."""
        x = W * (0.86 + 0.30 * (1.0 - (2.0 * t - 1.0) ** 2))
        y = H * t
        return x, y

    for i in range(n):
        t = t0 + (t1 - t0) * (i / max(n - 1, 1))
        x, y = point(t)
        x += float(rng.uniform(-46, 46))
        y += float(rng.uniform(-40, 40))
        h = int(rng.uniform(0.17, 0.30) * H)
        # tangent of the curve, so the run turns with the corners rather than staying upright
        x2, _ = point(min(t + 0.04, 1.2))
        ang = np.degrees(np.arctan2(H * 0.04, x2 - x)) - 90
        piece = scrap(seed=int(seed * 100 + i), height=h,
                      tint=("press" if i % 2 else "none"))
        piece = piece.rotate(-(ang + float(rng.uniform(-14, 14))), expand=True,
                             resample=Image.BICUBIC)
        piece.putalpha(piece.getchannel("A").point(lambda v: int(v * opacity)))
        layer.alpha_composite(piece, (int(x - piece.width / 2), int(y - piece.height / 2)))
    return layer


MARKS = {
    # Each is a path in a 400x400 box. Drawn, not typeset, and never closed neatly: a real pen
    # overshoots and doubles back, so the circle laps itself and the arrow's head is two strokes.
    "circle": "M330,150 C330,60 240,40 190,58 C110,86 70,190 96,264 C124,344 246,368 306,318 "
              "C356,276 366,196 336,132 C322,102 300,86 276,78",
    "arrow": "M60,300 C130,250 210,190 320,120 M320,120 L262,132 M320,120 L300,178",
    "underline": "M50,220 C150,196 260,192 356,206 M62,248 C160,228 262,226 344,238",
    "tick": "M80,210 L164,290 L330,96",
    "cross": "M90,100 L316,306 M312,102 L94,304",
    "bracket": "M300,60 C200,70 150,140 152,200 C154,262 210,326 302,340",
}


def mark(kind="circle", seed=0, height=220, width=8, ink="#141414"):
    """One hand-drawn ink mark. FREE.

    The ephemera that sit in the page's empty corners alongside the polaroid fan: an arrow, a
    circled word, a double underline. Same `#rough` turbulence displacement the F8 loop diagram
    puts on every tile and connector, so a drawn element in this rig always reads as one hand.
    """
    import os
    import subprocess
    import tempfile
    d = MARKS.get(kind, MARKS["circle"])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" '
           f'viewBox="0 0 400 400"><defs><filter id="r">'
           f'<feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="3" '
           f'seed="{seed}" result="n"/>'
           f'<feDisplacementMap in="SourceGraphic" in2="n" scale="4.0"/></filter></defs>'
           f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{width}" '
           f'stroke-linecap="round" filter="url(#r)"/></svg>')
    doc = (f'<style>*{{margin:0;padding:0}}html,body{{width:400px;height:400px;'
           f'background:transparent}}</style>{svg}')
    chrome = os.environ.get("CHROME_BIN",
                            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    out = Path(tempfile.mkdtemp()) / "mark.png"
    try:
        subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000", "--window-size=400,400",
                        f"--screenshot={out}", Path(tmp).as_uri()],
                       check=True, capture_output=True)
    finally:
        os.unlink(tmp)
    im = Image.open(out).convert("RGBA")
    box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if box:
        im = im.crop(box)
    if height and im.height:
        im = im.resize((max(1, round(im.width * height / im.height)), height), Image.LANCZOS)
    return im


def scrap(seed=0, height=420, tint="none", family=None):
    """A torn scrap of NEWSPRINT. Free: the scans are already on disk for the paper bed.

    Newsprint by default. `collage_bed_paper.families()` returns eight families, and
    drawing at random handed the fan scraps of fabric, sheet music and map hatching, which come
    back as grey blurs at scrap size and read as a smudge rather than as a torn piece of paper.
    Newsprint is the only family that still says "newspaper" at 420px. Pass `family` to override.
    """
    from collage_bed_paper import families
    fams = families()
    fam = fams[family] if family is not None else fams[0]   # index 0 is collage-src-university
    rng = np.random.default_rng(seed)
    src = fam[int(rng.integers(0, len(fam)))]
    im = Image.open(src).convert("RGB")
    # A strip off the page, not the whole page: a scrap is a piece somebody tore, and a full
    # scan pasted on the sheet reads as a second background rather than as an object.
    w = int(im.width * float(rng.uniform(0.28, 0.52)))
    h = int(im.height * float(rng.uniform(0.16, 0.34)))
    x = int(rng.integers(0, max(1, im.width - w)))
    y = int(rng.integers(0, max(1, im.height - h)))
    im = im.crop((x, y, x + w, y + h))
    return cut_image(im, seed=seed + 3, mask=mask_rect(im), tint=tint, height=height)


# The six strips on the tape asset sheet, in the sheet's own pixels. Measured once off
# `plates/tape-tape-strips.png`, the same measure-once habit as `mascot.VOIDS`. The sheet was
# shot with the strips well apart precisely so each one lifts on its own.
TAPE_SHEET = "tape-tape-strips.png"
TAPE_STRIPS = [
    (122, 144, 752, 796),      # 0  top left, steep
    (1090, 265, 1626, 1051),   # 1  top right, near vertical
    (415, 719, 1117, 1172),    # 2  middle, shallow
    (50, 1239, 630, 2024),     # 3  bottom left, long
    (818, 1150, 1371, 1570),   # 4  centre right, short
    (995, 1416, 1681, 1924),   # 5  bottom right
]


def tape(strip=0, seed=0, height=380):
    """One torn strip lifted off the tape asset sheet. FREE, the sheet is already shot.

    Tape is the one supporting piece that had to be photographed rather than built in code: it
    needs real material, real creases and a real shadow. Shot once as a sheet of six well-spaced
    strips, so every carousel from here draws from it for nothing.
    """
    src = ROOT.parent / "candidate" / "plates" / TAPE_SHEET
    im = Image.open(src).convert("RGB").crop(TAPE_STRIPS[strip % len(TAPE_STRIPS)])
    return cut_image(im, seed=seed, mask=mask_rect(im), height=height)


LADDER_CSS = """
* {{ margin:0; padding:0; }}
html,body {{ width:{w}px; height:{h}px; background:transparent; }}
svg {{ display:block; }}
.rung {{ fill:none; stroke:#141414; stroke-width:7; stroke-linecap:round;
  filter:url(#rough); }}
.rail {{ fill:none; stroke:#141414; stroke-width:6; stroke-linecap:round;
  filter:url(#rough); }}
.band {{ font-family:'your display typeface'; font-weight:400; font-size:44px; fill:#141414;
  letter-spacing:0.02em; }}
"""


def ladder(bands=("70 to 120", "120 to 180", "180 to 250+"), height=620, seed=4):
    """The three-rung pay ladder, DRAWN. Free: no plate, no generation.

    O3's beat is the three bands and the published rule for moving between them, and your
    call on was to break from photographs there: a drawn piece as the third medium,
    after the live-action O1 and the press-photo O2.

    The line quality is the house's, the `#rough` turbulence displacement the F8 loop diagram
    puts on every tile and connector, so a drawn piece in this rig always looks like the same
    hand. The rungs climb left to right so the ladder reads as progression rather than as a
    chart, and each carries its band.
    """
    import os
    import subprocess
    import tempfile
    W, H = 760, 620
    rows = []
    for i, b in enumerate(bands):
        y = H - 90 - i * 170
        x0, x1 = 60 + i * 60, 420 + i * 90
        rows.append(f'<path class="rung" d="M{x0},{y} L{x1},{y}"/>'
                    f'<text class="band" x="{x0 + 6}" y="{y - 22}">{b}</text>')
    rails = (f'<path class="rail" d="M40,{H - 40} L{40 + 120},60"/>'
             f'<path class="rail" d="M{420},{H - 40} L{420 + 190},60"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}"><defs><filter id="rough">'
           f'<feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="3" '
           f'seed="{seed}" result="n"/>'
           f'<feDisplacementMap in="SourceGraphic" in2="n" scale="3.0"/>'
           f'</filter></defs>{rails}{"".join(rows)}</svg>')
    doc = (f'<meta charset="utf-8">'
           f'<style>@font-face {{ font-family:\'your display typeface\'; font-weight:400; '
           f'src:url("{(ROOT.parent / "assets" / "display-300.ttf").resolve().as_uri()}"); }}'
           f'{LADDER_CSS.format(w=W, h=H)}</style>{svg}')
    chrome = os.environ.get("CHROME_BIN",
                            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    out = Path(tempfile.mkdtemp()) / "ladder.png"
    try:
        subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000", f"--window-size={W},{H}",
                        f"--screenshot={out}", Path(tmp).as_uri()],
                       check=True, capture_output=True)
    finally:
        os.unlink(tmp)
    im = Image.open(out).convert("RGBA")
    # Drawn pieces get no white border and no tear: they are ink on the page, not something
    # cut out and stuck to it. Only the scale.
    if height:
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    return im


def cut_image(im, seed=0, mask=None, tint="none", height=None):
    """`cut`, for an image already in memory rather than on disk."""
    tmp = ROOT / f"._cut_{seed}.png"
    im.save(tmp)
    try:
        return cut(tmp, seed=seed, mask=mask, tint=tint, height=height)
    finally:
        tmp.unlink(missing_ok=True)


def fan(card, pieces, origin, angles=None, spread=45, start=-45, pin=0.20, push=0,
        opacity=(0.72, 0.86, 1.0)):
    """Paste `pieces` as a fan radiating from `origin`, prominent piece last so it lands on top.

    `pieces` is ordered back to front. Each one is rotated `spread` degrees off the last and
    pinned by its own centre-left to `origin`, so the three share an anchor and open out from it
    the way a hand of cards fans. `origin` is in card pixels and is chosen per page against the
    rendered base, because the type leaves a different gap on every page.

    `opacity` is indexed the same way, back to front, so the LAST value is the prominent piece
    and stays at 1.0. Written the other way round first, which faded the piece that is supposed
    to carry the page and left the scrap behind it reading loudest.

    ANGLE ORDER AND STACK ORDER ARE INDEPENDENT, which is why `angles` exists. Deriving the
    angle from the draw index put the prominent piece at the far edge of the fan, tilted the
    full 45 degrees, and a masked figure lying on its side reads as a mistake rather than as a
    fanned card. Pass `angles=[-45, 45, 0]` against pieces ordered [supporting, supporting,
    prominent] and the hero sits upright in the middle of the fan while still landing on top.
    """
    ox, oy = origin
    for i, piece in enumerate(pieces):
        ang = angles[i] if angles else start + spread * i
        if i < len(opacity) and opacity[i] < 1.0:
            piece = piece.copy()
            piece.putalpha(piece.getchannel("A")
.point(lambda v, o=opacity[i]: int(v * o)))
        # EVERY PIECE ROTATES ABOUT THE SHARED ORIGIN, which is what makes this a fan rather
        # than a stack. Rotating each piece on its own axis and then placing it near the origin
        # was tried first: the three ended up almost on top of each other, because rotating a
        # piece about its own centre moves it nowhere. So the piece is laid into a card-sized
        # layer with its left edge pinned at the origin and its own centre on that line, and
        # the whole layer is then turned about that point. The piece swings out from the pin.
        # `pin` is how far INTO the piece the origin sits. Pinning the left edge exactly put
        # roughly half of a 500px-wide hero past the card's right edge, so the piece meant to
        # carry the page was the least of it you could see. A fifth of the way in keeps the
        # shared anchor and still leaves the piece bleeding.
        # `push` slides each piece OUT along its own arm before the layer is turned, so the three
        # stop sitting on top of each other. A shared pivot alone reads as a congested clump: the
        # angles separate the pieces at their far ends and leave them overlapping almost entirely
        # at the near end, which is where the eye goes. The hero (the last piece) is not pushed,
        # so it keeps the anchor and the supporting pieces move out from under it.
        out = push * (len(pieces) - 1 - i)
        layer = Image.new("RGBA", card.size, (0, 0, 0, 0))
        layer.alpha_composite(piece, (int(ox - piece.width * pin + out),
                                      int(oy - piece.height / 2)))
        card.alpha_composite(layer.rotate(-ang, center=(int(ox), int(oy)),
                                          resample=Image.BICUBIC))
    return card


def main():
    if "--demo" not in sys.argv:
        sys.exit("usage: cutouts.py --demo")
    plates = ROOT.parent / "candidate" / "plates"
    out = Path("/tmp/scratch"
               "/scratchpad")
    p = cut(plates / "u1b-falling-graduate-on-paper.png", seed=4, height=700)
    bg = Image.new("RGBA", (p.width + 80, p.height + 80), (243, 236, 225, 255))
    bg.alpha_composite(p, (40, 40))
    bg.convert("RGB").save(out / "cutout-demo.png")
    print(f"cutout-demo.png  {p.size}")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
