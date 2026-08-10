#!/usr/bin/env python3
"""Build the F7 review dossier: every static in the set, in one page.

    python3 dossier.py          # writes DOSSIER.html, then open it in Chrome

Free and re-runnable. Reads the cards off disk rather than re-rendering, so it always shows
what actually exists.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
CARDS = ROOT / "scripts/out-basics"
KEEPERS = ROOT.parent / "news-carousel/scripts/out-industry"
TEMPLATES = ROOT.parents[3] / "context/advertising/static-ads-bank/templates"
ASSETS = ROOT / "assets"
OUT = ROOT / "DOSSIER.html"

INDUSTRIES = [
    ("construction", "Construction & trades", "construction-and-trades", "quoting",
     "Site-to-Profit Readiness Check"),
    ("real-estate", "Real estate & property management", "real-estate-and-property-management",
     "leadgen", "AI-Ready Agency Score"),
    ("hospitality", "Hospitality & food service", "hospitality-and-food-service", "numbers",
     "Wow Factor Audit"),
    ("retail", "Retail & e-commerce", "retail-and-ecommerce", "systems",
     "Retail Ops AI Readiness Check"),
    ("financial-services", "Financial services & insurance", "financial-services-and-insurance",
     "context", "Broker and Adviser AI Readiness Check"),
]

# shape -> the HOOKS.md template it fills, and the image relationship it takes
SHAPE = {
    "callout":      ("A1 / S1 news headline", "4. image is the hero", "Plate below a caption band"),
    "question":     ("A1 / S12 question hook", "4. image is the hero", "Plate below a caption band"),
    "declarative":  ("A1 / S8 did you know", "1. image itemises", "Panel, rows counting the hire"),
    "contrarian":   ("S1 contrarian engine", "1. image itemises", "Panel, rows counting the cost"),
    "before-after": ("A1 / S10 before and after", "6. two subjects", "One plate, two grades"),
    "versus":       ("A1 / S11 us vs them", "2. image argues", "Hairline grid, line-art per cell"),
}

PICKS = [
    ("VetNotes Static Ads .png", "The B2B service card",
     "Vertical-named headline, trust line, two quote cards, button. The closest thing to house "
     "in the library."),
    ("image 9.png", "The two-column comparison table",
     "Minus rows against tick rows. Pure type, no product. The category-education card."),
    ("PSA 4.png", "The PSA split",
     "Kicker plus an underlined contrast, then two labelled panels."),
    ("Frame 466.png", "Editorial headline plus ticked rows",
     "Large left-aligned advice headline, three ticked lines, no image at all."),
    ("Power 3 - 1x1.png", "Italic statement plus a 2x2 tick grid",
     "Four capabilities on one card without becoming a list."),
]

CSS = f"""
@font-face {{ font-family:'your display typeface'; font-weight:200; src:url('{ASSETS}/jost-200.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{ASSETS}/jost-300.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500; src:url('{ASSETS}/jost-500.ttf'); }}
:root {{ --bg:#04050f; --card:#0c0d1a; --blue:#1269ff; --blue-dim:rgba(18,105,255,.12);
 --t1:#fff; --t3:rgba(255,255,255,.52); --t4:rgba(255,255,255,.28);
 --border:rgba(255,255,255,.08); --border-h:rgba(255,255,255,.18); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--t1); font-family:'your display typeface',system-ui,sans-serif;
 font-weight:300; padding:56px 48px 120px; line-height:1.6; }}
h1 {{ font-weight:200; font-size:44px; letter-spacing:-.01em; margin-bottom:10px; }}
.lede {{ color:var(--t3); max-width:1000px; font-size:17px; margin-bottom:8px; }}
.lede b {{ color:var(--t1); font-weight:500; }}
h2 {{ font-weight:300; font-size:26px; margin:64px 0 6px; padding-top:34px;
 border-top:1px solid var(--border); }}
h2 .n {{ color:var(--t4); font-size:17px; }}
h3 {{ font-weight:500; font-size:15px; letter-spacing:.14em; text-transform:uppercase;
 color:var(--blue); margin:34px 0 14px; }}
.blurb {{ color:var(--t3); font-size:15px; max-width:1000px; margin-bottom:20px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(238px,1fr)); gap:20px; }}
figure {{ background:var(--card); border:1px solid var(--border); border-radius:8px;
 overflow:hidden; }}
figure img {{ width:100%; display:block; background:#000; }}
figcaption {{ padding:11px 12px 13px; font-size:12.5px; line-height:1.5; }}
figcaption b {{ display:block; font-weight:500; font-size:13.5px; margin-bottom:3px; }}
figcaption span {{ display:block; color:var(--t3); }}
.tag {{ display:inline-block; margin-top:7px; font-size:10.5px; letter-spacing:.1em;
 text-transform:uppercase; color:var(--blue); background:var(--blue-dim);
 border-radius:999px; padding:3px 10px; }}
.keeper {{ border-color:var(--border-h); }}
.keeper figcaption b {{ color:var(--blue); }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
.two img {{ width:100%; display:block; border:1px solid var(--border); border-radius:8px; }}
table {{ border-collapse:collapse; width:100%; max-width:1100px; margin:18px 0 8px;
 font-size:14.5px; }}
th,td {{ text-align:left; padding:10px 14px; border-bottom:1px solid var(--border);
 vertical-align:top; }}
th {{ color:var(--t4); font-weight:500; font-size:12px; letter-spacing:.1em;
 text-transform:uppercase; }}
td b {{ font-weight:500; }}
.free {{ color:#4fd1a8; }}
ul {{ padding-left:20px; color:var(--t3); max-width:1000px; font-size:15px; }}
li {{ margin-bottom:6px; }}
li b {{ color:var(--t1); font-weight:500; }}
"""


def fig(src, title, sub, tag="", cls=""):
    t = f'<span class="tag">{tag}</span>' if tag else ""
    return (f'<figure class="{cls}"><img loading="lazy" src="{Path(src).as_uri()}">'
            f'<figcaption><b>{title}</b><span>{sub}</span>{t}</figcaption></figure>')


def build():
    h = [f'<!doctype html><meta charset="utf-8"><title>house statics, F7 dossier</title>'
         f'<style>{CSS}</style>']
    n_cards = sum(len(list((CARDS / i[0]).glob("*.png"))) for i in INDUSTRIES
                  if (CARDS / i[0]).exists())
    h.append('<h1>house statics, the industry set</h1>')
    h.append(f'<p class="lede">Twenty-five cells: five industries by five ranked pains. '
             f'<b>Five are the existing band keepers</b> and <b>{n_cards} are the new basic '
             f'type-led cards</b>, one static per pain point. Copy is locked. Every card is a fill '
             f'of a named template in <b>references/hooks/HOOKS.md</b>, the avatar opens every one, '
             f'and the pain clause is the canonical news-carousel bucket. '
             f'<span class="free">Nothing in this set cost a paid generation.</span></p>')

    for slug, name, keeper_dir, keeper, magnet in INDUSTRIES:
        d = CARDS / slug
        files = sorted(d.glob("*.png")) if d.exists() else []
        h.append(f'<h2>{name} <span class="n">{len(files)} new + 1 keeper</span></h2>')
        h.append(f'<p class="blurb">Every card closes on <b>{magnet}</b>.</p>')
        h.append('<div class="grid">')
        kp = KEEPERS / keeper_dir / f"{keeper}.png"
        if kp.exists():
            h.append(fig(kp, f"{keeper} , the keeper",
                         "The existing band card. All caps, bottom band, VHS plate. "
                         "This is the control the other four are measured against.",
                         "band , control", "keeper"))
        for f in files:
            pain, shape = f.stem.split("--")
            tpl, rel, img = SHAPE.get(shape, ("", "", ""))
            h.append(fig(f, f"{pain} , {shape}", f"Fills {tpl}. Image slot: {img}.", rel))
        h.append('</div>')

    h.append('<h2>The image language <span class="n">two worked examples</span></h2>')
    h.append('<p class="blurb">The lock settles this: <b>compose from site patterns only</b>, and '
             '<b>never bring in an icon set or a stock illustration</b>. So the image slot has '
             'exactly three legal fills: the panel, the hairline grid, and a plate. Both examples '
             'below are built from locked primitives only, and both are free.</p>')
    h.append('<div class="two">')
    for f, t, s in [("dossier-assets/A-panel.png", "Copy claims, panel itemises",
                     "The <b>.rv-panel</b> counts out what one hire covers, one labelled row with "
                     "a bar and a value each. This is the house's answer to Ad 128 counting the cookware."),
                    ("dossier-assets/B-grid.png", "Image argues, copy only frames",
                     "The <b>hairline grid</b>, 1px gap over --border, with line-art SVG per cell "
                     "in the locked 200x80 viewBox language. This is PSA 4 and image 9, in system.")]:
        h.append(f'<div><img src="{(ROOT/f).as_uri()}"><p class="blurb" style="margin-top:12px">'
                 f'<b>{t}.</b> {s}</p></div>')
    h.append('</div>')

    h.append('<h3>Which relationship each shape takes</h3>')
    h.append('<table><tr><th>Shape</th><th>Template filled</th><th>Image relationship</th>'
             '<th>What goes in the slot</th><th>Cost</th></tr>')
    for shape, (tpl, rel, img) in SHAPE.items():
        h.append(f'<tr><td><b>{shape}</b></td><td>{tpl}</td><td>{rel}</td><td>{img}</td>'
                 f'<td class="free">free</td></tr>')
    h.append('</table>')

    h.append('<h2>The reference layer <span class="n">Tier 1 Figma scaffolds</span></h2>')
    h.append('<p class="blurb">The scraped swipe banks were removed on 2026-08-06 and moved to '
             '<b>Archive/old-context/static-ads-swipe-banks-2026-08-06/</b>. The reference layer is '
             'the 41 Figma extracts and nothing else. These five survived the test that <b>house has '
             'no product to photograph</b>, so only scaffolds whose argument holds with the product '
             'removed transfer.</p>')
    h.append('<div class="grid">')
    for fn, title, sub in PICKS:
        p = TEMPLATES / fn
        if p.exists():
            h.append(fig(p, title, sub))
    h.append('</div>')

    h.append('<h2>Open, and what it would take</h2><ul>')
    h.append('<li><b>No card carries an image yet.</b> All 20 are type only. The two examples above '
             'are the proposal, not the set.</li>')
    h.append('<li><b>The three versus cards are near-identical</b> apart from the top line, because '
             'S11 draws generic Them/Us columns. Casting the consultant column to each industry\'s '
             'own wrong-fix would fix it.</li>')
    h.append('<li><b>The five magnet pages still do not exist.</b> Every card closes on a magnet, '
             'and only the generic /ai-readiness quiz is built. Largest open risk to the set.</li>')
    h.append('<li><b>Nothing has reached the CRM.</b> Archiving the 22 old carousels is still an '
             'unmade Supabase write.</li>')
    h.append('</ul>')
    OUT.write_text("\n".join(h))
    print(f"{n_cards} cards + 5 keepers -> {OUT}")


if __name__ == "__main__":
    build()
