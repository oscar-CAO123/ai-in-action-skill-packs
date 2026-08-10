#!/usr/bin/env python3
"""Cut the interview subject out and stand him on an editorial collage. FREE, no generation.

    python3 collage_news.py construction

the operator's direction 2026-08-06: cut the subject out and put textured 2D cutouts behind him,
newspaper and paper scraps, deliberately NOT in the VHS look so they stick out against him.

Method is the house one, not a new dependency. `bin_gen_cut.sh` in cio-1981-noir lifts a
subject by i2i onto flat chroma green and `bin_collage.py` keys it; the same two functions are
reused here, adapted in one way: that bank is monochrome so its despill greyscales everything,
and this plate is colour, so the despill here only pulls the green fringe instead.

Rules taken from `layers/editorial-layer/SKILL.md`:
  * **No legible generated text, ever.** Gibberish newsprint is the tell. Every scrap here is a
    real public-domain Library of Congress scan from collage-src/, recorded in sources.json.
  * **Torn paper edge**, a white ring 2 to 4px at 1080 wide, via add_outline.
  * **Cutouts are graded harder than the bed** so they stay legible as foreground.
  * **Never over a face.** The scraps are placed by explicit boxes that avoid the head.

Deviations from that skill, both the operator's call and both recorded:
  * The skill says static ads take the **bed only**, no foreground cutouts. This uses both.
  * The skill says **one or two cutouts per shot**. This runs four, because the ask was "all
    sorts of cutouts".
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = Path(__file__).parent
CUT = ROOT / "cut-news"
SRC = ROOT / "collage-src"
PLATES = ROOT / "plates-news"
OUT = ROOT / "collage-news"
W, H = 1080, 1350       # full frame: the plate bleeds and the type sits on it
# Subject height as a fraction of the frame, bottom-anchored. the operator, 2026-08-06: down from 0.88
# to make room for the top header. The subject is bottom-anchored, so this number sets where the
# crown lands: at 0.88 the head topped out at y=174 and the "Breaking:" block sat across the hard
# hat. The header block runs to about y=343 on its tallest card (three lines at 76px plus the CTA
# line), so 0.75 puts the crown at y=350 and the two never meet.
SUBJ_H = 0.75

# The site plate still has the subject standing in it, and the cutout only covers the middle of
# the card, so when the plate's subject sits RIGHT of centre they reappear beside their own
# cutout on the far side of the tear. Mirroring the plate throws them left, where the cutout
# covers them, and the location reads the same either way. One entry per plate that needs it.
MIRROR_SITE = {"hospitality", "retail", "financial-services"}

# Boxes to paint green on the cut plate BEFORE keying, as fractions of the plate (x0,y0,x1,y1).
# The financial-services plate has the interviewer's arm reaching in from the bottom left to hold
# the microphone, and it touches the subject, so it keys as one blob with her and arrives on the
# card as a disembodied shoulder. Two paid re-shoots failed to remove it (the second barely
# greened the room at all), so it is masked here instead, which costs nothing and is exact.
# the operator, 2026-08-06, after re-reading the reference reel: the paper is a BED, not a set of pasted
# chips. The first pass cut small rectangles, gave each a white edge and sat them inside the frame,
# and he called it "so perfectly cut out and truncated". The reel (@chrismoran__ DY7TSLJAQef,
# decoded at `layers/editorial-layer/reference-decode-b.png`) does the opposite: whole pages,
# overlapping, tilted a few degrees, running OFF all four edges with no cut edge anywhere, then
# both ends of the range squeezed toward the middle so the paper is felt rather than read. The
# measured band from that skill is luma 0.02 to 0.12 with a texture pass worth about +0.04.
#
# The configuration still varies per card in the three ways the operator named, now expressed in the bed:
#   layers    (scan, scale, angle, cx, cy) , WHICH scan, and the ANGLE it lies at. `scale` is a
#             multiple of the frame, so anything at or over 1.0 runs off the edges by design.
#   spots     (cx, cy, radius, lift) , the LIGHT SPOTS, soft radial lifts on the compressed bed.
#             This is the only thing that brightens paper now, and it never lifts past `bed_luma`
#             by more than the lift itself.
#   bed_luma  (min, max) the whole bed is compressed into before the spots and the texture.
COLLAGE = {
    # Two pages crossing near-square, light pooling top-left and low right.
    "construction": dict(bed_luma=(0.022, 0.118), note="crossed pages, gentle rake", layers=[
        (0, 1.35, -6, 0.38, 0.34),
        (2, 1.20, 9, 0.72, 0.74),
        (1, 0.95, -3, 0.18, 0.86),
    ], spots=[(0.20, 0.22, 0.42, 0.055), (0.78, 0.70, 0.34, 0.038)]),
    # One big page raked hard across the frame, one under it. Light stacked down the left.
    "real-estate": dict(bed_luma=(0.020, 0.108), note="single hard rake", layers=[
        (2, 1.50, -13, 0.46, 0.42),
        (3, 1.15, 7, 0.80, 0.20),
        (0, 1.05, 4, 0.30, 0.88),
    ], spots=[(0.12, 0.34, 0.46, 0.060), (0.16, 0.78, 0.30, 0.034)]),
    # Four pages laid nearly square to the frame, light scattered as small flecks.
    "hospitality": dict(bed_luma=(0.026, 0.124), note="stacked square, flecked light", layers=[
        (1, 1.28, -2, 0.42, 0.30),
        (3, 1.10, 3, 0.66, 0.66),
        (2, 1.00, -4, 0.16, 0.72),
        (0, 0.92, 2, 0.86, 0.14),
    ], spots=[(0.22, 0.16, 0.26, 0.052), (0.70, 0.44, 0.24, 0.040),
              (0.30, 0.82, 0.28, 0.046)]),
    # Two pages thrown well off square, one blazing passage top-left, the rest held down.
    "retail": dict(bed_luma=(0.018, 0.100), note="off-square slabs, one hot corner", layers=[
        (3, 1.45, 16, 0.34, 0.30),
        (1, 1.30, -11, 0.74, 0.68),
    ], spots=[(0.18, 0.18, 0.40, 0.072), (0.84, 0.86, 0.22, 0.026)]),
    # Three pages running as a broken diagonal, light weighted to the foot of the frame.
    "financial-services": dict(bed_luma=(0.024, 0.114), note="broken diagonal, foot-lit", layers=[
        (0, 1.32, -8, 0.30, 0.22),
        (2, 1.18, 12, 0.62, 0.56),
        (3, 1.08, -5, 0.84, 0.90),
    ], spots=[(0.34, 0.88, 0.44, 0.062), (0.66, 0.24, 0.26, 0.030)]),
}

# Cards whose site plate is placed by ALIGNING IT TO THE CUT-OUT rather than centre-cropped.
# the operator, 2026-08-06, on construction: the plate frames him on the RIGHT of the frame, the cut-out
# is centred, so his own graded ghost stood beside himself on the far side of the tear and the two
# layers read as two different photographs. Aligned, the plate's copy of him sits exactly behind
# the cut-out and the card reads as one image with the newsprint torn off it, which is what this
# rig was always supposed to do. The cost is that the plate is then at the SUBJECT's scale, which
# is smaller than cover, so the bed shows at two edges; on this card those edges are under the
# header fade and behind the clipping. `MIRROR_SITE` is the older workaround for the same problem
# and the two are mutually exclusive.
ALIGN_SITE = {"construction"}

# Props the human-segmentation matte drops that the pose actually needs. `matte_news.py` names
# this limit in its own docstring: the model segments PEOPLE, so anything held or leaned on goes.
# On financial services her left forearm runs behind the stack of paperwork on the desk, so the
# matte cuts the arm to a ragged point in mid-air. Restoring the paper puts the arm behind
# something again. Selected as the large bright desaturated blob in the LOWER part of the plate,
# which separates it from the equally bright wall behind her.
KEEP_PROP = {
    "financial-services": dict(bright=0.60, sat=0.16, below=0.50, min_px=100_000,
                               note="the desk paperwork her left forearm goes behind"),
}

PATCH_GREEN = {
    # Her jacket's left edge sits at x=0.47 for every row below y=0.575, and the arm and the
    # microphone are entirely left of 0.455, so the box clears her by a comfortable margin.
    "financial-services": [(0.00, 0.575, 0.455, 1.00)],
}


def rip_mask(w, h, seed=11, jag=46, step=26):
    """1.0 on the LEFT of a jagged diagonal tear, 0.0 on the right.

    A straight diagonal reads as a wipe. Paper tears in short irregular runs, so the boundary
    walks down the frame in `step`-sized moves with a random horizontal kick each time, and the
    kick is seeded so the tear is identical on every re-render.
    """
    rng = np.random.default_rng(seed)
    ys = np.arange(0, h + step, step)
    xs = np.linspace(w * 0.74, w * 0.26, len(ys)) + rng.normal(0, jag, len(ys))
    edge = np.interp(np.arange(h), ys, xs)                 # x of the tear at every row
    xx = np.arange(w)[None, :]
    return (xx < edge[:, None]).astype(np.float32)


def key_green(path, thresh=0.25, patches=()):
    """Key the flat chroma green, then keep ONLY the blob the subject sits in.

    The i2i pass does not green the whole frame evenly. It flattens most of it but leaves parts
    of the original location showing, sometimes fully opaque: the hospitality cut came back with
    the whole cafe still in the upper left. Refining that is money for nothing, and it does not
    have to be, because the pass always leaves a clean green rim around the subject. So every
    surviving fragment is a separate island and the subject is simply the biggest one.

    This used to flood fill from a fixed point in the frame, which assumed the subject stands in
    the middle. The hospitality subject stands right of centre, the seed landed in the green, and
    the fill returned the background instead of him. Largest-component needs no seed at all.

    Colour is kept; only the green fringe is despilled.
    """
    im = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    if patches:
        h0, w0 = im.shape[:2]
        chroma = np.array([0.22, 0.63, 0.24], dtype=np.float32)      # the plate's own key green
        for x0, y0, x1, y1 in patches:
            im[int(h0 * y0):int(h0 * y1), int(w0 * x0):int(w0 * x1)] = chroma
        print(f"  painted {len(patches)} box(es) green before keying")
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    d = g - np.maximum(r, b)
    # Hysteresis, the Canny trick. The pass often leaves the location showing THROUGH the green
    # rather than under it, half strength, and the retail shelving came back fused to the
    # subject's shoulder so no amount of eroding would separate them. A single threshold cannot
    # win: high enough to take that veil also takes hi-vis yellow. Two can. `thresh` marks what
    # is definitely background, half of it marks what is merely green-ish, and only the green-ish
    # pixels that can be reached from a definite one are background too. Measured across the four
    # cuts, this drops the retail veil (50.7% of frame to 44.2%) and moves the others under 0.2%.
    green = ndimage.binary_propagation(d > thresh, mask=(d > thresh * 0.5))
    solid = Image.fromarray(((~green) * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))
    lab, n = ndimage.label(np.asarray(solid) > 127)
    if not n:
        sys.exit(f"nothing survived the key in {path}")
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    picked = lab == (int(np.argmax(sizes)) + 1)
    print(f"  {n} islands, subject blob is {100*picked.mean():.1f}% of the frame")
    # Seal what interior holes are left. This used to run a 45px kernel, because a 0.10 key
    # threshold was taking the hi-vis with it. Measured on the construction cut: the chroma
    # background sits at g-max(r,b) = 0.44 and the vest at 0.06 or below, so a 0.25 threshold
    # separates them outright and the vest stops perforating. A smaller kernel matters: a close
    # wide enough to bridge a vest strip also drags background green up to half its width INSIDE
    # the mask, which is what put a hard green line down his arm and around the yellow.
    m8 = Image.fromarray((picked * 255).astype(np.uint8))
    k = 15
    m8 = m8.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))
    picked = np.asarray(m8) > 127
    print(f"  after hole close {100*picked.mean():.1f}%")
    a = (picked * 255).astype(np.uint8)
    # close pinholes, then soften and tighten the edge back up
    a = Image.fromarray(a).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(2.0))
    a = np.asarray(a, dtype=np.float32) / 255.0
    a = np.clip((a - 0.45) / 0.35, 0, 1)
    # Despill, restricted to a band around the silhouette. the operator, 2026-08-06: the hi-vis was
    # coming back patchy orange-green. A colour test alone cannot separate chroma green from
    # hi-vis yellow-green, so it was capping green INSIDE the vest as well as on the rim. Real
    # spill only lands within a few pixels of the cut, so the test now also has to sit in the
    # dilate-minus-erode band around the mask, which leaves the vest untouched.
    m8b = Image.fromarray((picked * 255).astype(np.uint8))
    rim = (np.asarray(m8b.filter(ImageFilter.MaxFilter(21)), dtype=np.float32)
           - np.asarray(m8b.filter(ImageFilter.MinFilter(21)), dtype=np.float32)) / 255.0
    fringe = ((d > thresh * 0.30) & (rim > 0.5)) | (d > thresh * 0.80)
    spill = np.minimum(g, (r + b) / 2 + 0.06)
    rgb = np.stack([r, np.where(fringe, spill, g), b], axis=2)
    ys, xs = np.where(a > 0.15)
    if not len(ys):
        sys.exit(f"nothing keyed out of {path}")
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return rgb[y0:y1, x0:x1], a[y0:y1, x0:x1]


def prop_mask(rgb, cfg):
    """The one prop the human matte dropped, as a mask. See `KEEP_PROP`.

    Bright and desaturated finds paper, but it also finds the wall behind her, so the blob is
    additionally required to START below `below` of the plate height. Measured on the financial
    services plate: the paperwork blob tops out at 0.69 of the height, the wall at 0.03.
    """
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    lab, n = ndimage.label((mx > cfg["bright"]) & ((mx - mn) < cfg["sat"]))
    if not n:
        return None
    keep, h = None, rgb.shape[0]
    for i in range(1, n + 1):
        blob = lab == i
        ys = np.where(blob.any(axis=1))[0]
        if blob.sum() >= cfg["min_px"] and ys.min() > h * cfg["below"]:
            if keep is None or blob.sum() > keep.sum():
                keep = blob
    return keep


def read_matte(path, keep=0.02, prop=None):
    """Take the alpha straight off a matted RGBA plate and trim it to the subject.

    The matting model gives a clean edge already, so this only tightens the very soft tail (a
    stray 1% alpha over the whole frame would make the bounding box the whole frame) and crops.

    Returns `(rgb, alpha, meta)`. `meta` carries the geometry the caller needs to place the cut:
    the crop's origin in the ORIGINAL plate's coordinates, and the PERSON's box inside the crop.
    They differ whenever a `KEEP_PROP` prop is restored, and the person's box is what the scale
    and the anchor are taken from, so adding a prop never changes how big the person renders.
    """
    im = np.asarray(Image.open(path).convert("RGBA"), dtype=np.float32) / 255.0
    rgb, a = im[..., :3], im[..., 3]
    lab, n = ndimage.label(a > 0.5)
    if n > 1:                                    # drop anything the model found that is not the
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))   # main figure
        big = lab == (int(np.argmax(sizes)) + 1)
        a = a * ndimage.binary_dilation(big, np.ones((9, 9)))
        print(f"  matte had {n} pieces, kept the largest")
    # Despill the edge. Construction and retail are matted off cut plates the i2i had already
    # tinted green, so the silhouette carries a green rim that the matte happily keeps. The test
    # is confined to a band around the edge, the same reason as in `key_green`: unconstrained, it
    # would cap the green in hi-vis and in foliage too.
    m8 = Image.fromarray(((a > 0.5) * 255).astype(np.uint8))
    rim = (np.asarray(m8.filter(ImageFilter.MaxFilter(15)), dtype=np.float32)
           - np.asarray(m8.filter(ImageFilter.MinFilter(15)), dtype=np.float32)) / 255.0
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    fringe = ((g - np.maximum(r, b)) > 0.045) & (rim > 0.5)
    rgb = np.stack([r, np.where(fringe, np.minimum(g, (r + b) / 2 + 0.04), g), b], axis=2)

    # CUT the chroma that the matte kept INSIDE the mask. The construction and retail cuts are
    # matted off i2i plates that were generated onto flat chroma green, and the human segmenter
    # happily keeps a lobe of that green wherever it had to guess: under his hand, where the
    # drawings he is holding used to be, it kept a saturated green blob the size of his fist.
    # The despill above cannot touch it because that test is confined to a band around the
    # outline, by design. Nothing a person wears on these five plates is chroma green, so a
    # straight colour cut inside the mask is safe here; hi-vis reads orange, not green.
    # Only SOLID green counts. An unrestricted colour cut also takes the few-pixel green rim the
    # i2i leaves along hair and cloth, and cutting a rim instead of despilling it notches the
    # silhouette: it put a row of chunks along the hospitality subject's hair. An opening on the
    # chroma mask keeps blobs thicker than the kernel and drops every rim, so the fist-sized blob
    # under the construction hand still goes and the rims are left to the despill above.
    ch8 = Image.fromarray((((g - np.maximum(r, b)) > 0.10) * 255).astype(np.uint8))
    chroma = np.asarray(ch8.filter(ImageFilter.MinFilter(21))
                        .filter(ImageFilter.MaxFilter(21))) > 127
    if chroma.any():
        a = a * (~chroma)
        a = np.asarray(Image.fromarray((a * 255).astype(np.uint8))
                       .filter(ImageFilter.MedianFilter(5)), dtype=np.float32) / 255.0
        print(f"  cut {int(chroma.sum())}px of kept chroma out of the mask")

    # HARDEN the edge before it ever reaches `add_outline`. That function paints white wherever
    # alpha is under 1, which is right for a 3px magazine cut and wrong for the wide band of
    # uncertain alpha the matting model leaves where it had to guess. On the construction plate
    # it guesses around both hands, because the drawings he is holding are dropped, and the
    # result on the card was a 25px white glow with his fingers lost inside it. Squeezing the
    # band to about a third of its width turns that back into a cut edge. the operator, 2026-08-06.
    soft = float(((a > 0.05) & (a < 0.95)).mean() * 100)
    # One opening first. What is left at the construction hand after the chroma cut is a thin
    # ghost of the drawings he is holding, hanging off his wrist, and the white cut edge turns
    # any sliver like that into a hook. An opening deletes anything thinner than the kernel and
    # leaves everything else where it is; measured on this plate, 15 takes the ghost and leaves
    # his knuckles and the real-estate microphone untouched.
    a = np.asarray(Image.fromarray((a * 255).astype(np.uint8))
                   .filter(ImageFilter.MinFilter(15)).filter(ImageFilter.MaxFilter(15)),
                   dtype=np.float32) / 255.0
    a = np.clip((a - 0.50) / 0.22, 0, 1)
    print(f"  edge hardened, soft band was {soft:.2f}% of the crop, now "
          f"{float(((a > 0.05) & (a < 0.95)).mean() * 100):.2f}%")

    # Despill a second time, against the FINAL outline. The first pass measures its rim off the
    # matte's own edge, and cutting the chroma blob moves that edge, which left a green thread
    # along the new boundary at the construction cuff.
    m8 = Image.fromarray(((a > 0.5) * 255).astype(np.uint8))
    rim = (np.asarray(m8.filter(ImageFilter.MaxFilter(19)), dtype=np.float32)
           - np.asarray(m8.filter(ImageFilter.MinFilter(19)), dtype=np.float32)) / 255.0
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    f2 = ((g - np.maximum(r, b)) > 0.028) & (rim > 0.5)
    rgb = np.stack([r, np.where(f2, np.minimum(g, (r + b) / 2 + 0.02), g), b], axis=2)
    print(f"  second despill took {int(f2.sum())}px along the final edge")

    ys, xs = np.where(a > keep)
    if not len(ys):
        sys.exit(f"empty matte at {path}")
    py0, py1, px0, px1 = int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1
    print(f"  matte covers {100*(a > 0.5).mean():.1f}% of the frame, "
          f"despilled {int(fringe.sum())}px of edge")

    # Restore the dropped prop, if this card names one. It joins the alpha but NOT the person box,
    # so `build` still scales and anchors off the figure alone.
    if prop is not None:
        pm = prop_mask(rgb, prop)
        if pm is None:
            print(f"  WANTED a prop ({prop['note']}) but found no blob matching it")
        else:
            a = np.maximum(a, pm.astype(np.float32))
            print(f"  restored {int(pm.sum())}px of prop: {prop['note']}")
    ys, xs = np.where(a > keep)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1
    meta = {"orig": (x0, y0),
            "person": (px0 - x0, py0 - y0, px1 - px0, py1 - py0)}
    return rgb[y0:y1, x0:x1], a[y0:y1, x0:x1], meta


def add_outline(rgb, alpha, px):
    """White magazine cut edge: dilate the alpha, paint the ring white, subject back on top."""
    a8 = Image.fromarray((alpha * 255).astype(np.uint8))
    grown = np.asarray(a8.filter(ImageFilter.MaxFilter(px * 2 + 1)), dtype=np.float32) / 255.0
    grown = np.asarray(Image.fromarray((grown * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.8)), dtype=np.float32) / 255.0
    m = alpha[..., None]
    return np.ones_like(rgb) * (1 - m) + rgb * m, np.clip(grown, 0, 1)


def blit(dst, rgb, alpha, x, y):
    h, w = alpha.shape
    H_, W_ = dst.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W_, x + w), min(H_, y + h)
    if x1 <= x0 or y1 <= y0:
        return dst
    sx0, sy0 = x0 - x, y0 - y
    a = alpha[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)][..., None]
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + rgb[sy0:sy0 + (y1 - y0),
                                                          sx0:sx0 + (x1 - x0)] * a
    return dst


def paper_bed(cfg, scans, seed=7):
    """The editorial bed: whole pages overlapping and bleeding off every edge, then compressed.

    Straight from the reference reel's method, in its order: lay the supporting images in,
    precomp them to ONE layer, then squeeze both ends of that layer's range toward the middle so
    it reads as texture instead of as a second picture. The compression is the whole trick, and
    it is why nothing here is cropped to a rectangle or given a cut edge: a page that stops
    inside the frame reads as a pasted chip, which is what the operator rejected.

    Returns a single-channel luma bed, already at `cfg["bed_luma"]`, spotted and textured.
    """
    layer = np.zeros((H, W), dtype=np.float32)
    covered = np.zeros((H, W), dtype=np.float32)
    for scan_i, scale, angle, cx, cy in cfg["layers"]:
        # `scan_i` is an index into `scans` for the industry beds that have always used
        # this. The candidate paper bed passes a Path directly instead, because it draws
        # each layer from a different family and a flat index would bias to the biggest.
        src = scan_i if isinstance(scan_i, (str, Path)) else scans[scan_i % len(scans)]
        im = Image.open(src).convert("L")
        # scale is a multiple of the FRAME, so >= 1.0 overruns it on purpose
        s = scale * max(W / im.width, H / im.height)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        page = np.asarray(im, dtype=np.float32) / 255.0
        keep = np.ones(page.shape, dtype=np.float32)
        rgba = Image.fromarray((page * 255).astype(np.uint8)).convert("L")
        msk = Image.fromarray((keep * 255).astype(np.uint8))
        rgba = rgba.rotate(angle, expand=True, resample=Image.BICUBIC)
        msk = msk.rotate(angle, expand=True, resample=Image.BICUBIC)
        pg = np.asarray(rgba, dtype=np.float32) / 255.0
        mk = np.asarray(msk, dtype=np.float32) / 255.0
        x = int(W * cx - pg.shape[1] / 2)
        y = int(H * cy - pg.shape[0] / 2)
        layer = blit(layer[..., None], pg[..., None], mk, x, y)[..., 0]
        covered = blit(covered[..., None], np.ones_like(pg)[..., None], mk, x, y)[..., 0]

    # anywhere no page landed, fall back to the mid tone so the bed never holes out to black
    layer = np.where(covered > 0.5, layer, float(layer[covered > 0.5].mean()) if covered.any()
                     else 0.5)

    lo, hi = cfg["bed_luma"]
    rng = max(float(np.ptp(layer)), 1e-6)
    bed = lo + (layer - layer.min()) / rng * (hi - lo)

    # the light spots: soft radial lifts, the only thing that brightens paper now
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for sx, sy, rad, lift in cfg.get("spots", ()):
        d = np.hypot((xx - W * sx) / (W * rad), (yy - H * sy) / (H * rad))
        bed = bed + lift * np.clip(1.0 - d, 0, 1) ** 2

    # the texture pass. The skill is explicit that this is part of the technique, not a flourish:
    # without it the lifted black reads as a crushed-black failure rather than as paper.
    rng2 = np.random.default_rng(seed)
    grain = rng2.normal(0, 1, (H, W)).astype(np.float32)
    grain = np.asarray(Image.fromarray(((grain * 40 + 128).clip(0, 255)).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0
    return np.clip(bed + (grain - grain.mean()) * 0.08, 0, 1)


def torn_edge(mask, px=5):
    """The white paper lip along the tear: the mask's own boundary, dilated and painted."""
    m8 = Image.fromarray((mask * 255).astype(np.uint8))
    grow = np.asarray(m8.filter(ImageFilter.MaxFilter(px * 2 + 1)), dtype=np.float32) / 255.0
    shrink = np.asarray(m8.filter(ImageFilter.MinFilter(px * 2 + 1)), dtype=np.float32) / 255.0
    band = np.clip(grow - shrink, 0, 1)
    return np.asarray(Image.fromarray((band * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32) / 255.0


def build(key):
    scans = sorted(SRC.glob("*.jpg"))
    if not scans:
        sys.exit("no scans in collage-src/, run fetch_loc.py first")
    OUT.mkdir(parents=True, exist_ok=True)

    cfg = COLLAGE[key]
    bed = paper_bed(cfg, scans)
    canvas = np.repeat(bed[..., None], 3, axis=2)
    canvas *= np.array([1.02, 1.00, 0.94], dtype=np.float32)             # faint paper warmth
    print(f"  bed: {len(cfg['layers'])} pages, {len(cfg.get('spots', ()))} light spots, "
          f"{cfg['note']}")

    # The subject, cut out, with the same white magazine edge. the operator, 2026-08-06: he keeps his
    # OWN colour. The earlier greyscale pass is reversed, so the hi-vis and the skin carry
    # through and the mono newsprint is what he reads against instead. The pop-art sunglasses
    # are generated onto him by cut_news.py, so nothing is drawn over him here.
    # A local matte, if `matte_news.py` has produced one, beats the paid chroma key outright:
    # it needs no green plate at all and cannot half-fail the way the i2i does.
    mt = CUT / f"{key}.matte.png"
    if mt.exists():
        rgb, a, meta = read_matte(mt, prop=KEEP_PROP.get(key))
    else:
        rgb, a = key_green(CUT / f"{key}.png", patches=PATCH_GREEN.get(key, ()))
        meta = {"orig": (0, 0), "person": (0, 0, rgb.shape[1], rgb.shape[0])}

    # Scale and anchor come from the PERSON's box, never the crop's. When a `KEEP_PROP` prop is
    # restored the crop grows around the figure, and scaling off the crop would silently shrink
    # the person on that one card while the other four stayed put.
    ppx, ppy, ppw, pph = meta["person"]
    target_h = int(H * SUBJ_H)
    s = target_h / pph
    nw, nh = int(rgb.shape[1] * s), int(rgb.shape[0] * s)
    rgb = np.asarray(Image.fromarray((rgb * 255).astype(np.uint8)).resize((nw, nh),
                     Image.LANCZOS), dtype=np.float32) / 255.0
    a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((nw, nh),
                   Image.LANCZOS), dtype=np.float32) / 255.0
    rgb, a = add_outline(rgb, a, 3)
    # The PERSON is centred across and BOTTOM-ANCHORED down the page, running a little past the
    # edge. The plate frames him to the waist however the prompt asks for more, so a centred blit
    # ends in a hard horizontal slice across his torso mid-card. Bleeding him off the bottom puts
    # that cut outside the frame and the eye completes the rest of him.
    px = int(W / 2 - (ppx + ppw / 2) * s)
    py = int(H + 12 - (ppy + pph) * s)

    # the operator, 2026-08-06: keep HALF the original background. The graded VHS site plate fills the
    # right of a jagged diagonal tear and the paper collage fills the left, so the card reads as
    # the newsprint being ripped off the footage rather than replacing it.
    site_p = PLATES / f"{key}.png"
    if site_p.exists():
        site = Image.open(site_p).convert("RGB")
        if key in ALIGN_SITE:
            # Put the plate through the SAME transform as the cut-out, so the plate's own copy of
            # the subject lands exactly behind him. At the subject's scale the plate no longer
            # covers the frame, and what it misses stays bed.
            sw, sh = int(site.width * s), int(site.height * s)
            sarr = np.asarray(site.resize((sw, sh), Image.LANCZOS), dtype=np.float32) / 255.0
            ox = px - int(meta["orig"][0] * s)
            oy = py - int(meta["orig"][1] * s)
            # At the subject's scale the plate is smaller than the frame, so it is sampled with
            # CLAMPED coordinates: past its edge the last row and column repeat. Leaving those
            # bands as bed instead put a bright newsprint panel down the right of the card that
            # read as a pasted rectangle. The plate's own edges here are dark scaffolding, so
            # extending them just continues the photograph.
            gx = np.clip(np.arange(W) - ox, 0, sw - 1)
            gy = np.clip(np.arange(H) - oy, 0, sh - 1)
            arr = sarr[np.ix_(gy, gx)]
            print(f"  site aligned to the cut-out at {s:.3f}x, origin ({ox},{oy}), "
                  f"edges clamped")
            m = rip_mask(W, H)[..., None]
            canvas = canvas * m + arr * (1 - m)
        else:
            if key in MIRROR_SITE:
                site = site.transpose(Image.FLIP_LEFT_RIGHT)
            sc_ = max(W / site.width, H / site.height)
            site = site.resize((int(site.width * sc_) + 1, int(site.height * sc_) + 1),
                               Image.LANCZOS)
            left = (site.width - W) // 2
            site = np.asarray(site.crop((left, 0, left + W, H)), dtype=np.float32) / 255.0
            # A hard jagged cut, NO white lip along it. the operator, 2026-08-06: the wide outline on the
            # tear reads as a sticker edge. The subject keeps his cut edge; the tear does not.
            m = rip_mask(W, H)[..., None]
            canvas = canvas * m + site * (1 - m)
    else:
        print(f"  no site plate at {site_p}, collage only")

    canvas = blit(canvas, rgb, a, px, py)

    # No local fade: band.py's own .plate-fade drops the join into the band.
    dst = OUT / f"{key}.png"
    Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8)).save(dst)
    print(f"{dst}  ({dst.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["construction"]):
        build(k)
