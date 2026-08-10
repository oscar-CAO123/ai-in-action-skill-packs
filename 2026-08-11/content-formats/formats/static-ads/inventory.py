#!/usr/bin/env python3
"""Everything built in the static-ads set, on one self-contained page. FREE, re-runnable.

    python3 inventory.py        # writes INVENTORY.html, then open it

Reads what is actually on disk rather than what the docs claim, so it cannot drift. Thumbnails
are embedded as base64, so the file opens anywhere with nothing beside it.

Written 2026-08-06 because `DOSSIER.html` only covers the 20 copy cards plus the news-carousel
keepers, and by then four more rigs had rendered work it never sees.
"""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
S = ROOT / "scripts"
OUT = ROOT / "INVENTORY.html"
THUMB_W = 340

# The 20 format cells from FORMAT-GRID.md, plus the five band keepers, with what each still needs.
# (industry, pain, format, funnel, sub-skill, what it needs)
GRID = [
    ("Construction", "systems", "Us vs them (S11)", "MOF", "type-led", "Tier B template"),
    ("Construction", "double-handling", "Napkin (S5)", "TOF", "hand-drawn", "renderer"),
    ("Construction", "bottleneck", "Advice / advertorial static (V11)", "TOF", "plate-led",
     "template, VHS plate exists"),
    ("Construction", "quoting", "BAND KEEPER", "TOF", "news-collage", "BUILT"),
    ("Construction", "headcount", "Quote-card grid, 3 real clients", "MOF", "proof",
     "testimonial capture, then Tier B"),
    ("Real estate", "admin", "iMessage / WhatsApp chat (S3)", "TOF", "ui-mock", "renderer"),
    ("Real estate", "systems", "PSA comparison split", "MOF", "type-led", "Tier B template"),
    ("Real estate", "bottleneck", "Big quote plus star row", "MOF", "proof",
     "testimonial capture, VHS plate exists"),
    ("Real estate", "numbers", "Annotated hero, leader lines", "BOF", "plate-led",
     "SVG overlay, VHS plate exists"),
    ("Real estate", "leadgen", "BAND KEEPER", "TOF", "news-collage", "BUILT"),
    ("Hospitality", "numbers", "BAND KEEPER", "TOF", "news-collage", "BUILT"),
    ("Hospitality", "hiring", "Don't hire this person (S6)", "TOF", "type-led",
     "Tier A, renders today"),
    ("Hospitality", "admin", "Editorial masthead embed", "TOF", "plate-led",
     "template, VHS plate exists"),
    ("Hospitality", "tribal-knowledge", "Whiteboard explainer", "TOF", "hand-drawn", "renderer"),
    ("Hospitality", "presence", "Before and after (S10)", "MOF", "plate-led",
     "two grades of one VHS plate"),
    ("Retail", "systems", "BAND KEEPER", "TOF", "news-collage", "BUILT"),
    ("Retail", "bottleneck", "Ultra low-fi static", "TOF", "hand-drawn",
     "PAID PLATE 1 of 2, authorised, unshot"),
    ("Retail", "numbers", "Numbered listicle / tick rows", "BOF", "type-led", "Tier B template"),
    ("Retail", "admin", "Comment reply ad", "TOF", "ui-mock",
     "PAID PLATE 2 of 2, authorised, unshot"),
    ("Retail", "headcount", "Problem / solution split (S2)", "MOF", "type-led",
     "Tier A, renders today"),
    ("Financial services", "context", "BAND KEEPER", "TOF", "news-collage", "BUILT"),
    ("Financial services", "admin", "Question hook (S12)", "TOF", "type-led",
     "Tier A, renders today"),
    ("Financial services", "bottleneck", "Organic post screenshot (S15)", "TOF", "ui-mock",
     "renderer"),
    ("Financial services", "dormant-book", "Long-form native article (S13)", "TOF", "plate-led",
     "template, VHS plate exists"),
    ("Financial services", "trust", "Founder statement, a founder", "MOF", "proof",
     "verbatim statement, then Tier A"),
]

SECTIONS = [
    ("The five news-collage keepers", "LOCKED as canonical 2026-08-06. The only cards in the set "
     "that are finished end to end: plate, cutout, editorial bed, tear and type. Two type "
     "treatments are on disk: `-band` is the original news-carousel band, `-clip` sets the same "
     "cards as a torn newspaper clipping with an arrow on the subject (build_news_clip.py).",
     [S / "out-news"], ("-band.png", "-clip.png")),
    ("The 20 copy cards", "Copy is LOCKED, every line a fill of a named template in "
     "references/hooks/HOOKS.md. These are rendered on the plain band, NOT in their assigned "
     "formats. This is the batch waiting on images.",
     [S / "out-basics"], (".png",)),
    ("Format prototypes", "Now three formats running across ALL FIVE industries, 15 cards, built 2026-08-06. The watercolour window (other LOCKED plate-led format), the consultant-vs-house card and the house-in-the-cubicles card. Each holds the same figures and set in every industry and moves only the camera, so the five read as one campaign; for the watercolour, the view through the window changes too. Plus the retro one-off.",
     [S / "out-noirreal", S / "out-white", S / "out-retro"], (".png",)),
    ("Superseded", "Earlier passes kept for reference. Not part of the current set.",
     [S / "out", S / "out-half", S / "out-lead"], (".png",)),
]


def thumb(p):
    im = Image.open(p).convert("RGB")
    im.thumbnail((THUMB_W, THUMB_W * 3), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=72)
    return base64.b64encode(buf.getvalue()).decode()


def collect(dirs, suffixes):
    out = []
    for d in dirs:
        if not d.exists():
            continue
        for p in sorted(d.rglob("*.png")):
            if p.name.startswith("_") or "sheet" in p.name.lower():
                continue
            if not any(p.name.endswith(s) for s in suffixes):
                continue
            out.append(p)
    return out


def main():
    parts, total = [], 0
    for title, blurb, dirs, sfx in SECTIONS:
        files = collect(dirs, sfx)
        total += len(files)
        cards = "".join(
            f'<figure><img src="data:image/jpeg;base64,{thumb(p)}" alt="">'
            f'<figcaption>{p.parent.name}/<b>{p.stem}</b></figcaption></figure>'
            for p in files)
        parts.append(f'<section><h2>{title} <span class="n">{len(files)}</span></h2>'
                     f'<p class="blurb">{blurb}</p><div class="grid">{cards}</div></section>')

    built = sum(1 for r in GRID if r[5] == "BUILT")
    rows = "".join(
        f'<tr class="{"done" if r[5] == "BUILT" else ""}"><td>{r[0]}</td><td>{r[1]}</td>'
        f'<td>{r[2]}</td><td class="f">{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>'
        for r in GRID)

    OUT.write_text(f"""<!doctype html><meta charset="utf-8">
<title>Static ads, everything built</title>
<style>
:root {{ color-scheme: dark; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:48px 40px 90px; background:#0d0d0f; color:#e9e9ec;
       font:15px/1.55 'your display typeface','Helvetica Neue',system-ui,sans-serif; }}
h1 {{ font-size:34px; font-weight:300; letter-spacing:.01em; margin:0 0 6px; }}
.lede {{ color:#9a9aa4; max-width:74ch; margin:0 0 40px; }}
h2 {{ font-size:19px; font-weight:400; margin:52px 0 4px; padding-bottom:8px;
     border-bottom:1px solid #26262c; }}
.n {{ color:#1269FF; font-size:14px; }}
.blurb {{ color:#8e8e98; max-width:80ch; margin:10px 0 22px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:20px; }}
figure {{ margin:0; }}
figure img {{ width:100%; display:block; border-radius:3px; background:#000; }}
figcaption {{ font-size:11.5px; color:#7e7e88; margin-top:7px; word-break:break-word; }}
figcaption b {{ color:#c9c9d2; font-weight:500; }}
table {{ width:100%; border-collapse:collapse; margin-top:20px; font-size:13.5px; }}
th {{ text-align:left; font-weight:500; color:#8e8e98; padding:8px 12px 8px 0;
     border-bottom:1px solid #26262c; }}
td {{ padding:8px 12px 8px 0; border-bottom:1px solid #1c1c22; vertical-align:top; }}
tr.done td {{ color:#1269FF; }}
td.f {{ color:#7e7e88; }}
.wrap {{ overflow-x:auto; }}
</style>
<h1>Static ads, everything built</h1>
<p class="lede">Read off disk on 2026-08-06, not from the docs. {total} rendered cards in four
groups, then the 25-cell grid with what each cell still needs. {built} of 25 cells are finished.</p>
{''.join(parts)}
<section><h2>The 25-cell grid <span class="n">{built} of 25 built</span></h2>
<p class="blurb">Assignments from FORMAT-GRID.md. The five keepers are the news-collage cards above.
Every other cell has its copy written and nothing rendered in its assigned format.</p>
<div class="wrap"><table>
<tr><th>Industry</th><th>Pain</th><th>Format</th><th>Funnel</th><th>Sub-skill</th>
<th>What it still needs</th></tr>{rows}</table></div></section>
""", encoding="utf-8")
    print(f"{OUT}  ({OUT.stat().st_size // 1024} KB, {total} cards)")


if __name__ == "__main__":
    main()
