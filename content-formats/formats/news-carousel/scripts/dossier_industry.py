#!/usr/bin/env python3
"""Compose THE review dossier for the single-card industry statics. One file, all five industries.

    python3 dossier_industry.py

Writes `out-industry/_dossiers/INDUSTRY-STATICS-DOSSIER.html`, self-contained: images are
embedded as data URIs, so the dossier can be opened, moved or sent on its own.

Every card is shown against the evidence it was built from, pulled live out of that industry's
playbook at `context/pain-wiki/industries/<slug>.md`: the ranked pain in the owner's own words,
the call count, the verbatim quote, the house's angle on it, and the lead-magnet question the card
walks the reader into.

Card N answers playbook pain N. The magnet question is NOT positional: it comes from the card's
own `q` field, because three of the five playbooks order their questions differently from their
pains. Do not reintroduce a positional lookup here.
"""
import base64
import html
import io
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from decks_industry import (INDUSTRY_STATICS, MAGNETS,  # noqa: E402
                            band_lines)
from plates_real import PLATE_STYLES, SCENES  # noqa: E402

WIKI = ROOT.parents[4] / "context" / "pain-wiki"
OUT = ROOT / "out-industry"
DEST = OUT / "_dossiers" / "INDUSTRY-STATICS-DOSSIER.html"
IMG_W = 820


def parse_playbook(slug):
    """Ranked pains and the lead-magnet questions out of one industry playbook."""
    src = (WIKI / "industries" / f"{slug}.md").read_text()

    pains = []
    block = re.search(r"^## Pains, ranked\n(.*?)^## ", src, re.S | re.M)
    for m in re.finditer(r"^### (\d+)\. (.+?)\n(.*?)(?=^### |\Z)",
                         block.group(1) if block else "", re.S | re.M):
        body = m.group(3)
        def field(name):
            f = re.search(rf"\*\*{name}\.\*\* (.+?)(?=\n\n|\Z)", body, re.S)
            return " ".join(f.group(1).split()) if f else ""
        desc = re.split(r"\n\*\*", body.strip())[0]
        pains.append({"rank": int(m.group(1)), "title": m.group(2).strip(),
                      "desc": " ".join(desc.split()),
                      "evidence": field("Evidence"), "angle": field("Angle")})

    lm = re.search(r"^## Lead magnet: (.+?)\n(.*?)^## ", src, re.S | re.M)
    questions, lede = [], ""
    if lm:
        lede = " ".join(lm.group(2).strip().split("\n")[0].split())
        for q in re.finditer(r"^(\d+)\. (.+?)$", lm.group(2), re.M):
            questions.append({"n": int(q.group(1)), "q": q.group(2).strip()})
    return pains, questions, lede


def corpus_row(slug):
    """The industry's line from the wiki INDEX, so the dossier states its own sample size."""
    for line in (WIKI / "INDEX.md").read_text().splitlines():
        if line.startswith(f"| [[{slug}]]"):
            c = [x.strip() for x in line.strip("|").split("|")]
            return {"calls": int(c[1]), "businesses": int(c[2]), "records": int(c[4])}
    return {"calls": 0, "businesses": 0, "records": 0}


def data_uri(png):
    im = Image.open(png).convert("RGB")
    im.thumbnail((IMG_W, IMG_W * 4))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def accent_html(lines):
    """Render the authored copy the way the card sets it, with the accent span marked."""
    text = html.escape(" ".join(lines))
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="acc">\1</span>', text)


def title_of(slug):
    return slug.replace("-and-", " & ").replace("-", " ").title()


CSS = """
:root{--bg:#0d1117;--card:#161b22;--line:#2a313c;--txt:#e6edf3;--mut:#8b949e;--acc:#2f81f7;--warm:#e3b341}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);
     font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header{padding:30px 32px 16px;border-bottom:1px solid var(--line)}
h1{margin:0 0 8px;font-size:25px}
.sub{color:var(--mut);font-size:13.5px;max-width:960px;margin-top:8px}
.sub code{color:var(--txt);font-size:12.5px}
.stats{display:flex;gap:24px;margin-top:16px;flex-wrap:wrap;font-size:13px;color:var(--mut)}
.stats b{color:var(--acc)}
nav{position:sticky;top:0;z-index:10;display:flex;gap:8px;flex-wrap:wrap;
    padding:12px 32px;background:rgba(13,17,23,.95);backdrop-filter:blur(8px);
    border-bottom:1px solid var(--line)}
nav a{background:var(--card);border:1px solid var(--line);color:var(--txt);text-decoration:none;
      padding:6px 13px;border-radius:20px;font-size:12.5px}
nav a b{color:var(--mut);font-weight:400;margin-left:4px}
section{scroll-margin-top:62px}
.ihead{padding:34px 32px 0}
h2{margin:0 0 6px;font-size:21px}
.magnet{color:var(--acc);font-size:14.5px;font-weight:600}
.ilede{color:var(--mut);font-size:13.5px;max-width:900px;margin-top:6px}
.icount{display:flex;gap:20px;margin-top:11px;flex-wrap:wrap;font-size:12.5px;color:var(--mut)}
.icount b{color:var(--txt)}
.rowwrap{padding:4px 32px 12px}
.row{display:grid;grid-template-columns:minmax(260px,400px) 1fr;gap:26px;background:var(--card);
     border:1px solid var(--line);border-radius:12px;padding:20px;margin-top:18px}
.row img{width:100%;border-radius:8px;display:block}
.rank{display:inline-block;background:#21262d;color:var(--mut);font-weight:700;font-size:12px;
      padding:2px 9px;border-radius:6px;margin-bottom:9px}
.rank.new{color:var(--warm)}
h3{margin:0 0 10px;font-size:16.5px;line-height:1.35}
.k{color:var(--mut);font-size:11px;letter-spacing:.09em;text-transform:uppercase;margin:15px 0 4px}
.v{font-size:13.5px}
.v.mut{color:var(--mut)}
.quote{border-left:2px solid var(--line);padding-left:12px;color:var(--mut);font-size:13px}
.copy{background:#0d1117;border:1px solid var(--line);border-radius:8px;padding:12px 14px;
      font-size:14px;line-height:1.5;letter-spacing:.01em}
.acc{color:var(--acc)}
.plate{font-size:12.5px;color:var(--mut)}
.plate b{color:var(--txt);font-weight:600}
footer{border-top:1px solid var(--line);margin-top:26px;padding:22px 32px 40px;
       color:var(--mut);font-size:13px}
footer b{color:var(--warm)}
footer li{margin-bottom:6px}
@media(max-width:820px){.row{grid-template-columns:1fr}}
"""


# the operator, 2026-08-06: the format grid keeps ONE card per industry on this band format and replaces the
# other twenty cells with twenty different static formats. `--keepers` renders only the five
# survivors. Grid: formats/static-ads/FORMAT-GRID.md.
#
# The keeper was ranked pain #3 for about an hour, and that put the SAME pain on three of the five
# (construction, real estate and financial services all rank owner-bottleneck third), leaving
# construction and real estate as near-duplicate cards separated only by "owner" against "principal".
# A control group for a format test cannot be near-single-pain, so the operator moved it to one distinct pain
# per industry, each the most ownable pain that industry has.
#
# the operator, 2026-08-06 (second pass): hospitality, retail and financial services move to their
# TOP-ranked pain. Real estate is explicitly excepted and stays on lead follow-up. Construction was
# not named and stays on quoting, which is its most ownable pain even though it ranks fourth.
# The five still cover five distinct pains, which was the point of moving off rank #3.
KEEPERS = {
    "construction-and-trades": "quoting",              # rank 4, kept: most ownable
    "real-estate-and-property-management": "leadgen",   # rank 5, kept: the operator's exception
    "hospitality-and-food-service": "numbers",          # rank 1
    "retail-and-ecommerce": "systems",                  # rank 1
    "financial-services-and-insurance": "context",      # rank 1
}


def industry_section(deck, keepers=False):
    slug = deck["industry"]
    pains, questions, lede = parse_playbook(slug)
    corpus = corpus_row(slug)

    if keepers:
        k = KEEPERS[slug]
        idx = next(n for n, c in enumerate(deck["cards"]) if c["slug"] == k)
        cards, offset = [deck["cards"][idx]], idx
    else:
        cards, offset = deck["cards"], 0

    rows = []
    for j, card in enumerate(cards):
        i = j + offset
        pain = pains[i] if i < len(pains) else {}
        qn = card["q"]
        q = next((x["q"] for x in questions if x["n"] == qn), "")
        scene = SCENES.get((slug, card["slug"]), {})
        is_new = False
        plate = (f'Shot on <b>{PLATE_STYLES[slug]}</b> from the F8 style bank. '
                 f'{html.escape(scene.get("shot",""))}: {html.escape(scene.get("brief",""))}.')
        rows.append(f"""
<div class="row">
  <div><img loading="lazy" src="{data_uri(OUT / slug / f"{card['slug']}.png")}" alt="{card['slug']}"></div>
  <div>
    <span class="rank{' new' if is_new else ''}">PAIN {i+1}{' · NEW PLATE' if is_new else ''}</span>
    <h3>{html.escape(pain.get('title',''))}</h3>
    <div class="v mut">{html.escape(pain.get('desc',''))}</div>
    <div class="k">The card as set</div>
    <div class="copy">{accent_html(band_lines(slug, card))}</div>
    <div class="k">Evidence</div>
    <div class="quote">{html.escape(pain.get('evidence',''))}</div>
    <div class="k">the house's angle</div>
    <div class="v">{html.escape(pain.get('angle',''))}</div>
    <div class="k">Walks into magnet question {qn}</div>
    <div class="v mut">{html.escape(q)}</div>
    <div class="k">Plate</div>
    <div class="plate">{plate}</div>
  </div>
</div>""")

    return corpus, f"""
<section id="{slug}">
  <div class="ihead">
    <h2>{html.escape(title_of(slug))}{' &middot; keeper' if keepers else ''}</h2>
    <div class="magnet">{html.escape(MAGNETS[slug])}</div>
    <div class="ilede">{html.escape(lede)}</div>
    <div class="icount">
      <span><b>{corpus['calls']}</b> discovery calls</span>
      <span><b>{corpus['businesses']}</b> businesses</span>
      <span><b>{corpus['records']}</b> wiki pain records</span>
      <span>playbook <code>{slug}.md</code></span>
    </div>
  </div>
  <div class="rowwrap">{''.join(rows)}</div>
</section>"""


def main():
    keepers = "--keepers" in sys.argv
    sections, totals, nav = [], {"calls": 0, "businesses": 0, "records": 0}, []
    for deck in INDUSTRY_STATICS:
        corpus, sec = industry_section(deck, keepers=keepers)
        sections.append(sec)
        for k in totals:
            totals[k] += corpus[k]
        nav.append(f'<a href="#{deck["industry"]}">{html.escape(title_of(deck["industry"]))}'
                   f'<b>{1 if keepers else 5}</b></a>')

    cards = 5 if keepers else sum(len(d["cards"]) for d in INDUSTRY_STATICS)

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{'house industry statics , what remains of the existing batch' if keepers else 'house industry statics , review dossier'}</title>
<style>{CSS}</style></head><body>
<header>
  <h1>the business , {'what remains of the existing batch' if keepers else 'single-card industry statics'}</h1>
  {'''<div class="sub"><b>Five cards, one per industry, five different pains.</b> These are the
  survivors of the format grid the operator settled on 2026-08-06: one card per industry keeps this
  bottom-band VHS format, and the other twenty cells are being rebuilt in twenty different static
  formats to test the format itself. The grid is <code>formats/static-ads/FORMAT-GRID.md</code>.</div>
  <div class="sub"><b>The keeper is chosen for pain variety, not by rank.</b> Holding rank #3 across
  the board put owner-bottleneck on three of the five and made construction and real estate
  near-duplicates. Each industry now keeps its most ownable pain instead, so the control group covers
  quoting, lead follow-up, tribal knowledge, reporting lag and the dormant client book.</div>
  <div class="sub">Everything on this page is <b>built, final and on disk</b>. The twenty replaced
  cells still exist too and are not deleted; the full 25-card dossier renders from the same script
  without <code>--keepers</code>.</div>''' if keepers else '''<div class="sub">Five industries, five cards each. Every card is one ranked pain, targeted at one
  industry. This set replaces the 22 general-pain noir carousels, which carried no industry and a
  generic quiz CTA.</div>'''}
  <div class="sub"><b>Plates are real-world captures, no people.</b> the operator replaced the painted noir
  plates on 2026-08-06. Each industry is shot on one style from the F8 plate-style bank at
  <code>ideas/industry-build-carousels/styles.json</code>, composed and graded exactly the way the
  industry-build carousels are. The leader-arrow CTA that briefly rode on the plate was cut the same
  day, so nothing is drawn over the plate and the band is the only type on the card.</div>
  <div class="sub"><b>The band template:</b> <code>AUSSIE &lt;BUSINESS TYPE&gt; ARE FINALLY REALISING
  THEY DON'T HAVE TO &lt;PAIN&gt; ANYMORE.</code> The accent is the pain clause. Because that sentence
  is plural and industry-wide, no playbook figure can ride on it without widening a single firm's
  number into an industry claim, which section 3 forbids. The pain clauses are therefore
  qualitative and every figure stays down here, as the evidence behind the card.</div>
  <div class="sub">Nothing here is invented. Industries are the top five by call volume in
  <code>context/pain-wiki/INDEX.md</code>, and the same five
  <code>ideas/industry-build-carousels/VERTICALS.md</code> maps. Pains, evidence quotes and angles
  are pulled live from each <code>context/pain-wiki/industries/&lt;slug&gt;.md</code> playbook at
  build time. Magnet names are the ones those playbooks already carry.</div>
  <div class="sub"><b>Card N answers playbook pain N.</b> The magnet question is named per card and
  is not positional: hospitality, retail and financial services order their questions differently
  from their pains, and several magnets carry eight questions against five or six ranked pains.</div>
  <div class="stats">
    <span><b>5</b> industries</span>
    <span><b>{cards}</b> cards {'remaining' if keepers else ''}</span>
    {'<span><b>20</b> cells being reformatted</span>' if keepers else f'<span><b>{cards}</b> plates shot</span>'}
    <span><b>{totals['calls']}</b> discovery calls behind the set</span>
    <span><b>{totals['businesses']}</b> businesses</span>
    <span><b>{totals['records']}</b> wiki pain records</span>
  </div>
</header>
<nav>{''.join(nav)}</nav>
{''.join(sections)}
<footer>
  <div>Renders from <code>build_industry.py</code>, copy in <code>decks_industry.py</code>, this page
  from <code>dossier_industry.py</code>. Re-rendering the whole set is free.</div>
  <div style="margin-top:12px">Open, and needing the operator:</div>
  <ul>
    <li><b>The lead magnet named on every card has no page built.</b> Five quizzes, spec'd in full
    in the playbooks, are a separate build.</li>
    <li><b>Nothing is uploaded to the CRM.</b> Archiving the 22 carousels is a Supabase write and
    has not been made.</li>
    {'''<li><b>One of these five plates carries a flagged issue.</b> Real estate/leadgen still shows
    "APPRAISAL REQUEST SLIPS - UNOPENED" legibly on the folder. The other four were checked at full
    resolution on 2026-08-06 and are clean: construction's blueprint text, hospitality's laptop screen
    and financial services' ledger pages all degraded to speckle with no readable word, and retail's
    CRT reads as a database screen without a legible heading.</li>
    <li>Fixing it is <code>plates_real.py real-estate-and-property-management leadgen --refine
    --go</code>, one paid job, roughly 2 credits, and it keeps the approved composition. Not
    authorised yet.</li>
    <li><b>The "using AI" tail is cut from all 25 cards</b>, not just these five. The band now ends on
    the pain.</li>''' if keepers else '''<li>The owner-bottleneck motif carries four of the five industries. Plates never repeat inside
    a set; they do repeat across sets, which is deliberate.</li>'''}
  </ul>
</footer>
</body></html>"""
    dest = DEST.with_name("INDUSTRY-STATICS-KEEPERS.html") if keepers else DEST
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc)
    print(f"{dest}  {dest.stat().st_size/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
