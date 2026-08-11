#!/usr/bin/env python3
"""Tier B: the structured band. Rows and columns inside the same bottom 506px.

`band.py` renders Tier A, one justified block, and it is the law. Six of the type-led formats
carry an argument that cannot compress to one sentence (a stack of symptoms, a two-column
contrast, a numbered list), and `type-led/SKILL.md` section 2 scopes Tier B to exactly that.

    from band_rows import render_rows
    render_rows(dict(head="...", rows=["...", "..."], answer="..."), Path("out/x.png"))

What Tier B keeps from the law, unchanged:

  - **The 506px well and nothing above it.** Top edge stays at y=844.
  - **Flush margins.** Every row runs x64 to x1016, the same column as a Tier A line.
  - **One face, one size for the body rows.** A number or a column label may sit one step
    smaller and that is the only second size on the card.
  - **One blue accent for the whole card**, never one per row.
  - **No grey.** White at full strength or blue. Grey is what made the earlier passes read small.

## The fit

The size is solved, not authored, exactly as Tier A solves its own. Binary search the largest
size at which the whole block still fits the well, then stop. Two traps this rig has already paid
for and both bite here:

  - **`clientWidth` counts padding**, so the row column is given an explicit 952px width and the
    fit never reads a width off a padded element.
  - **`margin-top:auto` defeats a fit search**, because an auto margin absorbs all overflow and
    the block reports as fitting at every size. The well stacks from the bottom with a flex
    `justify-content:flex-end` and no auto margins anywhere inside it.
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
WELL = H * 3 // 8          # 506, the band. Identical to band.py.
PAD = 64
COL = W - 2 * PAD          # 952, the flush column every row runs in
BLUE = "#1269FF"

ACC = re.compile(r"\[\[(.+?)\]\]")


def markup(s):
    """Escape, then turn [[...]] into the one blue accent."""
    return ACC.sub(r'<span class="accent">\1</span>', html.escape(s))


# ---------------------------------------------------------------------------------------------
# Per-format treatment.
#
# `../SKILL.md` section 0 names the failure this table exists to stop: "Twenty formats set in one
# face at one case is the failure this test exists to avoid. If the reader cannot tell two cells
# apart at thumbnail size, the test returns nothing." Measured on : F1, F3, F4 and F5
# came back as one card printed four times, all your display typeface 200, sentence case, full measure.
#
# Caps is NOT available as a lever. It belongs to the news-carousel doctrine and nothing else.
# What is left, and what this table varies: weight, measure, alignment and a hairline rule.
TREATMENTS = {
    "F1":  dict,                                            # the control, the house band
    # F3 opened out on . At measure 700 the question set in four short lines against a
    # 316px right margin, which you read as cramped rather than as a column: "fit it into three
    # lines and spread it out, increase the margin." A wider measure buys the three lines, the
    # bigger pad puts real air at both edges, and the looser leading spreads them.
    # `max_size` is what actually buys the three lines. The solver maximises size subject to the
    # well's height, so widening the measure on its own just returns a BIGGER four-line set: the
    # first attempt at 912 came back at 72.4px still in four lines. Capping the size means more
    # characters fit per line, the question falls in three, and the slack left over at the top of
    # the well is the air you asked for.
    "F3":  dict(measure=912, align="left", leading=1.22, pad=84, max_size=66),
    "F4":  dict(weight=300, rule=True),                       # heavier, ruled off above
    "F5":  dict(align="justify", leading=1.02),               # the biggest statement in the set
    "F10": dict(measure=880),
}


def css(font_files, t=None):
    t = t or {}
    faces = "".join(
        f"@font-face {{ font-family:'your display typeface'; font-weight:{w}; src:url('{ASSETS}/{f}'); }}"
        for w, f in font_files)
    col = t.get("measure", COL)
    pad = t.get("pad", PAD)
    weight = t.get("weight", 200)
    align = t.get("align", "left")
    lead = t.get("leading", 1.18)
    # Case and tracking are treatment keys rather than authored into the copy string, which is
    # what `../SKILL.md` section 0 asks for: "a sentence-case theme is the right way to do it
    # rather than pre-casing the copy string". Both default to off, so no existing format moves.
    # Only the news-headline variant sets them, because caps is the news-carousel doctrine and
    # nothing else in the suite may reach for it.
    transform = t.get("transform", "none")
    tracking = t.get("tracking", "normal")
    return f"""
{faces}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.card{{position:relative;width:{W}px;height:{H}px;background:#000;overflow:hidden}}
.plate{{position:absolute;left:0;top:0;width:{W}px;height:{H - WELL}px;object-fit:cover}}
.plate-fade{{position:absolute;left:0;width:{W}px;height:180px;
        top:calc({H}px - {WELL}px - 180px);
        background:linear-gradient(to bottom,rgba(0,0,0,0),#000)}}
/* The full-bleed variant, ported from band.py unchanged so a Tier A and a Tier B card sit on
   the same plate identically. `.plate-fade` assumes the plate STOPS above the band and dies
   into black; a bleeding plate has picture all the way down, so the fade climbs the well from
   the bottom edge instead of landing on top of it. Never full black at the foot, or the bleed
   is pointless: it darkens the picture enough to carry white type and no further. */
.plate-bleed-fade{{position:absolute;left:0;bottom:0;width:{W}px;height:{WELL + 470}px;
        background:linear-gradient(to top,rgba(0,0,0,0.94) 0%,rgba(0,0,0,0.88) 26%,
                                   rgba(0,0,0,0.70) 48%,rgba(0,0,0,0.38) 72%,
                                   rgba(0,0,0,0) 100%)}}
/* The well IS the band. Stacks from the bottom, no auto margins anywhere, because an auto
   margin absorbs overflow and the fit search then passes at every size. */
.well{{position:absolute;left:0;right:0;bottom:0;height:{WELL}px;padding:0 {pad}px {pad}px;
      display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden}}
/* explicit width: clientWidth counts padding, so nothing downstream may measure it.
   `flex:0 0 auto` is the same family of trap as the auto margin above, and it cost the F1
   professional services card a truncated first line. The block is a flex ITEM, so it shrinks
   to the well by default; its content then spills out through the TOP of the padding box, and
   `scrollHeight` does not count overflow in that direction. The fit search read 412px against
   442px available and passed at a size whose real content is 522px. Never let it shrink. */
/* `font-variant-ligatures:none` is not cosmetic. your display typeface's ff ligature reads as "tt" at display
   size, and the F3 hospitality card shipped a headline saying "two weeks ott". */
.block{{flex:0 0 auto;width:{col}px;font-family:'your display typeface';font-weight:{weight};color:#fff;
      line-height:{lead};text-align:{align};font-variant-ligatures:none;
      text-transform:{transform};letter-spacing:{tracking}}}
.rule{{width:{col}px;height:1px;background:rgba(255,255,255,.30);margin-bottom:0.66em}}
.head{{margin-bottom:0.5em}}
.row{{display:flex;align-items:baseline;gap:0.5em}}
.num{{font-weight:300;opacity:.55;font-size:0.62em;min-width:1.4em}}
.arrow{{opacity:.5;padding:0 0.35em}}
.answer{{margin-top:0.55em}}
.cols{{display:flex;gap:0;width:{col}px}}
.col{{flex:1;min-width:0}}
.col + .col{{padding-left:34px;border-left:1px solid rgba(255,255,255,.22);margin-left:34px}}
.lbl{{font-weight:300;font-size:0.6em;letter-spacing:.14em;text-transform:uppercase;
     opacity:.6;margin-bottom:0.55em;display:block}}
.accent{{color:{BLUE}}}
.cta{{font-weight:300;font-size:0.56em;letter-spacing:.05em;opacity:.78;margin-top:0.7em}}
"""


# The fit MUST wait for your display typeface. `band.py` carries this trap in its own comment and this engine was
# written without it: the search ran against whatever face was resolved at that instant, which on
# a cold start is the fallback. Fallback metrics are narrower, so the solver returned a size that
# then took an extra line once your display typeface swapped in, and the extra line overflowed the TOP of the well
# and was clipped. It cost the F1 professional services card its whole first line, and it is
# intermittent by nature: the screenshot pass and the dump-dom pass are two separate Chrome runs,
# so the same card measured 5 lines in one and 4 in the other.
#
# `document.fonts.ready` alone does not fix it. The card starts empty, nothing has requested the
# face, and the promise resolves instantly against the fallback. The face has to be asked for by
# name first, which is what `load` does here.
FIT = """
document.fonts.load('%WEIGHT% 100px "your display typeface"', 'AZ09').then(function{
  return document.fonts.ready;
}).then(function{
  const block = document.querySelector('.block');
  const well  = document.querySelector('.well');
  // the usable height is the well minus its own bottom padding, measured once
  const avail = %AVAIL%;
  let lo = 14, hi = %MAXSIZE%, best = 14;
  for (let n = 0; n < 24; n++) {
    const mid = (lo + hi) / 2;
    block.style.fontSize = mid + 'px';
    if (block.scrollHeight <= avail && block.scrollWidth <= %COL%) { best = mid; lo = mid; }
    else { hi = mid; }
  }
  block.style.fontSize = best + 'px';
  document.title = best.toFixed(1) + 'px, fill ' +
    Math.round(100 * block.scrollHeight / avail) + '%';
});
"""


def body_html(c, t=None):
    """Build the block for whichever Tier B shape this card is."""
    t = t or {}
    out = []
    if t.get("rule"):
        out.append('<div class="rule"></div>')
    if c.get("head"):
        out.append(f'<div class="head">{markup(c["head"])}</div>')

    if c.get("them") or c.get("us"):
        # two-column contrast
        def col(label, items):
            # A bare string is one row, not one row per character. F33 passes its columns as
            # single sentences and the first pass iterated them letter by letter, which the fit
            # solver then reported as 14px at 152% overflow.
            if isinstance(items, str):
                items = [items]
            rows = "".join(f'<div class="row">{markup(str(x))}</div>' for x in items)
            return f'<div class="col"><span class="lbl">{markup(label)}</span>{rows}</div>'
        out.append('<div class="cols">'
                   + col(c.get("them_label", ""), c.get("them", []))
                   + col(c.get("us_label", ""), c.get("us", []))
                   + '</div>')
    elif c.get("left") and c.get("right"):
        out.append('<div class="cols">'
                   f'<div class="col"><div class="row">{markup(c["left"])}</div></div>'
                   f'<div class="col"><div class="row">{markup(c["right"])}</div></div>'
                   '</div>')
    elif c.get("pairs"):
        for a, b in c["pairs"]:
            out.append(f'<div class="row">{markup(a)}'
                       f'<span class="arrow">&rarr;</span>{markup(b)}</div>')
    elif c.get("rows"):
        for n, r in enumerate(c["rows"], 1):
            num = f'<span class="num">{n}</span>' if c.get("numbered") else ""
            out.append(f'<div class="row">{num}{markup(str(r))}</div>')

    if c.get("answer"):
        out.append(f'<div class="answer">{markup(c["answer"])}</div>')
    if c.get("cta"):
        out.append(f'<div class="cta">{markup(c["cta"])}</div>')
    return "".join(out)


def render_rows(c, png, plate=None, chrome=None, treatment=None,
                plate_full=False, plate_fade=False, overlay=None):
    """Render one card. Returns the fit report.

    `plate_full` bleeds the image over the whole frame rather than stopping it above the well,
    and `plate_fade` climbs the gradient up from the bottom edge so the type reads across it.
    you, : that pair is the F1 treatment.
    """
    t = treatment or {}
    font_files = [(200, "jost-200.ttf"), (300, "jost-300.ttf"), (500, "jost-500.ttf")]
    art = ""
    if plate:
        src = Path(plate).resolve.as_uri
        if plate_full:
            art = f'<img class="plate" src="{src}" style="height:{H}px">'
            if plate_fade:
                art += '<div class="plate-bleed-fade"></div>'
        else:
            art = f'<img class="plate" src="{src}"><div class="plate-fade"></div>'
    js = (FIT.replace("%AVAIL%", str(WELL - PAD))
.replace("%COL%", str(t.get("measure", COL)))
.replace("%WEIGHT%", str(t.get("weight", 200)))
.replace("%MAXSIZE%", str(t.get("max_size", 96))))
    # Raw SVG in frame coordinates over the whole card. Same contract band.py already carries;
    # added so an annotated plate can still use the band.
    over = ""
    if overlay:
        over = (f'<svg style="position:absolute;left:0;top:0;pointer-events:none" '
                f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">{overlay}</svg>')

    doc = (f'<meta charset="utf-8"><style>{css(font_files, t)}</style>'
           f'<div class="card">{art}<div class="well">'
           f'<div class="block">{body_html(c, t)}</div></div>{over}</div>'
           f'<script>{js}</script>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    png = Path(png)
    png.parent.mkdir(parents=True, exist_ok=True)
    # `--virtual-time-budget` is required now that the fit waits on the font promise: without it
    # the capture can land before the search has run and the card screenshots at the unfitted
    # default size.
    subprocess.run([chrome or CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--virtual-time-budget=4000",
                    f"--window-size={W},{H}",
                    f"--screenshot={png}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    # read the fit back out of the title the page wrote
    r = subprocess.run([chrome or CHROME, "--headless", "--disable-gpu",
                        "--virtual-time-budget=4000",
                        "--dump-dom", f"--window-size={W},{H}", f"file://{tmp}"],
                       capture_output=True, text=True)
    m = re.search(r"<title>(.*?)</title>", r.stdout or "")
    os.unlink(tmp)
    return m.group(1) if m else "rendered"
