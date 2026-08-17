#!/usr/bin/env python3
"""Render the tape carousel: grade the plate, find the well, colour the ink, lay the type.

    python3 build.py                  # grade what is missing, render every slide to ./out
    python3 build.py --regrade        # re-run the grade even if a graded plate exists
    python3 build.py --out DIR        # somewhere else
    python3 build.py --plates DIR     # real shots instead of scripts/plates

The type is rendered crisp on top of the already graded plate, never composited under the
grade. Every slide's ink is taken off the ground it sits on and checked against the
contrast floor for its role, and the check is printed and written to report.json. A slide
that fails is still rendered, so the failure is visible rather than silently corrected.
"""
import argparse
import base64
import html
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import tape
from decks import DECK, SLIDES

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / "assets"
CHROME = os.environ.get(
    "CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W, H = 1080, 1350
BLUE = "#1269FF"
INSET = 0.035           # keep type off the well's own edges, fraction of the frame
MIN_INSET_PX = 46

# type scale per slide kind: (head px ceiling, head font, body px, eyebrow px)
SCALE = {
    "hook":    (96, "Anton", 34, 24),
    "beat":    (78, "Anton", 32, 24),
    "stat":    (260, "Anton", 36, 24),
    "endcard": (84, "Anton", 30, 24),
}
ADVANCE = {"Anton": 0.44, "Poppins": 0.53}   # measured mean glyph advance / font size
SLOP = 1.06


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def grade(src, dst, cast):
    cmd = [str(ROOT / "grade.sh"), str(src), str(dst),
           str(cast.get("sat", 1.15)), str(cast.get("lift", 0.02)),
           str(cast.get("soft", 2.2)), str(cast.get("grain", 16))]
    subprocess.run(cmd, check=True)


def pick_well(graded, slide):
    """The well: either the one the deck names, or the largest empty box in its band."""
    if slide["well"] != "auto":
        box = slide["well"]
        return {**tape.sample(graded, box), "x": box[0], "y": box[1],
                "w": box[2], "h": box[3], "source": "deck"}

    band = slide.get("band", "low")
    wells = tape.find_wells(graded, band=band)
    if not wells:
        raise SystemExit(
            f"no well in the {band} band of {Path(graded).name}. The plate has no empty "
            f"space built into it there, which is a plate problem, not a type problem. "
            f"Re-shoot the plate with the space composed in, or move the copy to a band "
            f"that has one.")
    # An empty band is the point, so it is never the warning. An empty FRAME is: it means
    # the plate has no subject and the carousel is five colour fields with words on them.
    pick = max(wells, key=lambda w: w["w"] * w["h"])
    frame = tape.band_flat_share(graded, "any")
    note = "auto" if frame <= 92 else \
        f"auto, WARNING the whole frame is {frame}% empty, so this plate has no subject in it"
    return {**pick, "source": note}


def fit(text, font, ceiling, width_px, height_px, line_h=1.06):
    """Largest size that keeps the text inside the well, by measured glyph advance."""
    words = text.split()
    for size in range(ceiling, 15, -2):
        per_line = max(1, int(width_px / (size * ADVANCE[font] * SLOP)))
        lines, cur = 1, 0
        for w in words:
            take = len(w) + (1 if cur else 0)
            if cur + take > per_line and cur:
                lines += 1
                cur = len(w)
            else:
                cur += take
        if lines * size * line_h <= height_px:
            return size, lines
    return 16, 99


def render(slide, graded, well, out_png):
    kind = slide["kind"]
    head_ceiling, head_font, body_px, eyebrow_px = SCALE[kind]

    ink_head, cr_head, note = tape.ink_for(well["ground"], "stat" if kind == "stat" else "head")
    ink_body, cr_body, _ = tape.ink_for(well["ground"], "body")
    accent, cr_accent, _ = tape.ink_for(well["ground"], "eyebrow", accent=BLUE)

    inset = max(MIN_INSET_PX, int(W * INSET))
    box_w = int(W * well["w"] / 100) - 2 * inset
    box_h = int(H * well["h"] / 100) - 2 * inset
    if box_w < 240 or box_h < 120:
        raise SystemExit(f"well too small on {Path(graded).name}: {box_w}x{box_h}px after "
                         f"inset. Build more empty space into the plate.")

    body_lines = 0
    reserve = 0
    if slide.get("eyebrow"):
        reserve += int(eyebrow_px * 2.4)
    if slide.get("body"):
        _, body_lines = fit(slide["body"], "Poppins", body_px, box_w, box_h, 1.34)
        reserve += int(body_lines * body_px * 1.34 + body_px * 0.9)
    head_px, _ = fit(slide["head"], head_font, head_ceiling, box_w, max(60, box_h - reserve))

    ff = "Anton" if head_font == "Anton" else "PoppinsSB"
    parts = []
    if slide.get("eyebrow"):
        parts.append(f'<div class="eyebrow" style="color:{accent}">'
                     f'{html.escape(slide["eyebrow"])}</div>')
    parts.append(f'<div class="head" style="color:{ink_head};font-size:{head_px}px;'
                 f'font-family:{ff}">{html.escape(slide["head"])}</div>')
    if slide.get("body"):
        parts.append(f'<div class="body" style="color:{ink_body};font-size:{body_px}px">'
                     f'{html.escape(slide["body"])}</div>')

    doc = f"""<!doctype html><meta charset="utf-8"><style>
@font-face {{ font-family:'Anton'; src:url('{ASSETS}/Anton-Regular.ttf'); }}
@font-face {{ font-family:'PoppinsSB'; src:url('{ASSETS}/Poppins-SemiBold.ttf'); }}
@font-face {{ font-family:'PoppinsM'; src:url('{ASSETS}/Poppins-Medium.ttf'); }}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.plate{{position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover}}
.well{{position:absolute;
  left:{well['x']}%;top:{well['y']}%;width:{well['w']}%;height:{well['h']}%;
  padding:{inset}px;display:flex;flex-direction:column;justify-content:center;
  align-items:{'center' if slide.get('align') == 'center' else 'flex-start'};
  text-align:{slide.get('align', 'left')}}}
.eyebrow{{font-family:'PoppinsSB';font-size:{eyebrow_px}px;letter-spacing:.16em;
  text-transform:uppercase;margin-bottom:{int(eyebrow_px * 0.9)}px}}
.head{{line-height:1.04;letter-spacing:-.01em;text-transform:uppercase}}
.body{{font-family:'PoppinsM';line-height:1.34;margin-top:{int(body_px * 0.9)}px;
  max-width:100%}}
</style>
<img class="plate" src="data:image/png;base64,{b64(graded)}">
<div class="well">{''.join(parts)}</div>"""

    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={out_png}", f"--window-size={W},{H}",
                        "--default-background-color=00000000", f"file://{tmp}"],
                       check=True, capture_output=True)
    finally:
        os.unlink(tmp)

    floor_head = tape.FLOOR["stat" if kind == "stat" else "head"]
    room = tape.headroom(well["ground"])
    return {
        "headroom": round(room, 2),
        "verdict": ("ok" if cr_head >= floor_head else
                    (f"the well is mid-luminance (L{well['luma']}), ceiling {room:.1f}:1, "
                     f"so no ink can clear {floor_head}:1. Darken or brighten the well in "
                     f"the plate." if room < floor_head else
                     "ink fell short of the floor, check the well sample")),
        "slide": out_png.name, "kind": kind, "plate": slide["plate"],
        "cast": slide["cast"],
        "well": {k: well[k] for k in ("x", "y", "w", "h")},
        "well_source": well["source"], "well_spread": well.get("spread"),
        "ground": well["ground"], "ground_luma": well["luma"],
        "ink_head": ink_head, "contrast_head": round(cr_head, 2),
        "floor_head": floor_head, "ink_law": note,
        "ink_body": ink_body, "contrast_body": round(cr_body, 2),
        "eyebrow_colour": accent, "eyebrow_is_your_table": accent == BLUE,
        "head_px": head_px,
        "pass": cr_head >= floor_head and cr_body >= tape.FLOOR["body"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "out"))
    ap.add_argument("--plates", default=str(ROOT / "plates"))
    ap.add_argument("--regrade", action="store_true")
    args = ap.parse_args()

    plates = Path(args.plates)
    out = Path(args.out)
    graded_dir = out / "graded"
    out.mkdir(parents=True, exist_ok=True)
    graded_dir.mkdir(exist_ok=True)

    report = []
    for i, slide in enumerate(SLIDES, 1):
        src = plates / slide["plate"]
        if not src.exists():
            sys.exit(f"missing plate {src}. Run plates.py for stand-ins, or drop the shot in.")
        graded = graded_dir / src.name
        if args.regrade or not graded.exists():
            grade(src, graded, slide["cast"])
        well = pick_well(graded, slide)
        rec = render(slide, graded, well, out / f"{i:02d}.png")
        report.append(rec)
        flag = "ok  " if rec["pass"] else "FAIL"
        print(f"{flag} {rec['slide']}  well {rec['well_source']} "
              f"x{rec['well']['x']} y{rec['well']['y']} {rec['well']['w']}x{rec['well']['h']}%  "
              f"ground {rec['ground']} L{rec['ground_luma']}  ink {rec['ink_head']} "
              f"cr {rec['contrast_head']} (floor {rec['floor_head']}, ceiling "
              f"{rec['headroom']})  {rec['ink_law']}")
        if not rec["pass"]:
            print(f"     {rec['verdict']}")

    (out / "report.json").write_text(json.dumps(
        {"deck": DECK, "slides": report}, indent=1))
    bad = [r["slide"] for r in report if not r["pass"]]
    print(f"\n{len(report)} slides -> {out}")
    print("contrast: all slides clear their floor" if not bad
          else f"contrast FAILURES: {', '.join(bad)}")


if __name__ == "__main__":
    main()
