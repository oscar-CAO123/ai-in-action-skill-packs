#!/usr/bin/env python3
"""Compose the review dossier for the 11 ready-to-go noir pain carousels.

    python3 dossier_noir_review.py

Writes `out-noir/_dossiers/NOIR-READY-DOSSIER.html`, self-contained: every slide is embedded
as a data URI, so the dossier opens, moves or sends on its own.

The point of the review: these 11 carousels sit in the CRM content page under `ready`, and the
copies live in Supabase Storage are the retired Anton renders with plate annotations. The local
renders in `out-noir/<slug>/` are the current canon (thin your display typeface 200 band, annotations cut). Each
row shows the new slide large with the superseded Anton slide beside it, so the swap can be
judged slide by slide before anything is written to storage.

The Anton slides are the ones pulled down from storage, parked in `out-noir/_superseded/<slug>/`.
"""
import base64
import html
import io
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / "out-noir"
SUP = OUT / "_superseded"
DEST = OUT / "_dossiers" / "NOIR-READY-DOSSIER.html"

NEW_W = 700   # the current render, the thing being judged
OLD_W = 240   # the retired render, reference only

# The 11 carousels sitting in `ready` on the CRM content page, in CRM title order.
CAROUSELS = [
    ("noir-pain-admin", "Noir carousel: back-office admin", "back-office-admin"),
    ("noir-pain-cx", "Noir carousel: customer experience risk", "customer-experience-risk"),
    ("noir-pain-systems", "Noir carousel: disconnected systems", "disconnected-systems"),
    ("noir-pain-inbox", "Noir carousel: inbox overload", "inbox-overload"),
    ("noir-pain-leads", "Noir carousel: leads going cold", "lead-follow-up"),
    ("noir-pain-numbers", "Noir carousel: nobody trusts the numbers", "data-mess"),
    ("noir-pain-delivery", "Noir carousel: operations and delivery drag", "ops-delivery-drag"),
    ("noir-pain-quoting", "Noir carousel: quoting and estimating", "quoting-estimating"),
    ("noir-pain-execution-gap", "Noir carousel: the execution gap", "ai-know-how-gap"),
    ("noir-pain-leadgen", "Noir carousel: the lead generation ceiling", "lead-gen-ceiling"),
    ("noir-pain-bottleneck", "Noir carousel: the owner bottleneck", "owner-bottleneck"),
]

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
.slug{color:var(--acc);font-size:13.5px;font-weight:600;font-family:ui-monospace,SFMono-Regular,monospace}
.icount{display:flex;gap:20px;margin-top:11px;flex-wrap:wrap;font-size:12.5px;color:var(--mut)}
.icount b{color:var(--txt)}
.rowwrap{padding:4px 32px 12px}
.row{display:grid;grid-template-columns:1fr minmax(200px,260px);gap:26px;background:var(--card);
     border:1px solid var(--line);border-radius:12px;padding:20px;margin-top:18px;align-items:start}
.row img{width:100%;border-radius:8px;display:block}
.rank{display:inline-block;background:#21262d;color:var(--mut);font-weight:700;font-size:12px;
      padding:2px 9px;border-radius:6px;margin-bottom:9px}
.rank.new{color:var(--warm)}
.k{color:var(--mut);font-size:11px;letter-spacing:.09em;text-transform:uppercase;margin:0 0 6px}
.old{opacity:.62}
.old:hover{opacity:1}
footer{border-top:1px solid var(--line);margin-top:26px;padding:22px 32px 40px;
       color:var(--mut);font-size:13px}
footer b{color:var(--warm)}
footer li{margin-bottom:6px}
@media(max-width:900px){.row{grid-template-columns:1fr}}
"""


def data_uri(path, width):
    """Embed a slide, resized and JPEG'd so the whole dossier stays a sane single file."""
    im = Image.open(path).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    parts = []

    nav = "".join(
        f'<a href="#{slug}">{html.escape(title.replace("Noir carousel: ", ""))}<b>6</b></a>'
        for slug, title, _ in CAROUSELS
    )

    for slug, title, tag in CAROUSELS:
        rows = []
        for i in range(1, 7):
            new_p = OUT / slug / f"slide-{i:02d}.png"
            old_p = SUP / slug / f"slide-{i:02d}.png"
            old_html = (
                f'<div class="old"><p class="k">retired (live now)</p>'
                f'<img src="{data_uri(old_p, OLD_W)}"></div>'
                if old_p.exists() else
                '<div class="old"><p class="k">retired</p></div>'
            )
            rows.append(
                f'<div class="row"><div><span class="rank new">SLIDE {i}</span>'
                f'<img src="{data_uri(new_p, NEW_W)}"></div>{old_html}</div>'
            )
            print(f"  {slug} slide-{i:02d}")

        parts.append(
            f'<section id="{slug}"><div class="ihead"><h2>{html.escape(title)}</h2>'
            f'<div class="slug">content-media/{slug}/</div>'
            f'<div class="icount"><span>tags <b>noir, F5, pain, {tag}</b></span>'
            f'<span>slides <b>6</b></span><span>status <b>ready</b></span></div></div>'
            f'<div class="rowwrap">{"".join(rows)}</div></section>'
        )

    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Noir ready carousels: thin-your display typeface review</title>
<style>{CSS}</style></head><body>
<header><h1>Noir pain carousels, ready-to-go: thin-your display typeface review</h1>
<div class="sub">The 11 carousels sitting under <code>ready</code> on the CRM content page. The
large slide is the current canon out of <code>out-noir/&lt;slug&gt;/</code>: thin your display typeface 200 band,
all caps, justified, one blue accent, plate annotations cut. The small slide beside it is what is
live in Supabase Storage right now, the retired Anton render with annotations. Nothing has been
written to storage yet.</div>
<div class="stats"><span>carousels <b>11</b></span><span>slides <b>66</b></span>
<span>duplicate local copies <b>0</b></span><span>storage paths unchanged, DB writes <b>0</b></span></div>
</header>
<nav>{nav}</nav>
{"".join(parts)}
<footer><b>On approval:</b> the 66 slides overwrite their existing
<code>content-media/&lt;slug&gt;/slide-NN.png</code> paths with x-upsert. Because the paths do not
move, <code>media_urls</code> and <code>thumbnail_url</code> stay valid and no
<code>content_items</code> row is touched. Storage serves <code>cache-control: no-cache</code>,
so the CRM picks the new slides up immediately.
<ul><li>Rollback: the retired Anton slides are parked at
<code>out-noir/_superseded/&lt;slug&gt;/</code>, byte-identical to what is live now.</li>
<li>The 11 noir carousels still under <code>idea</code> are untouched.</li></ul></footer>
</body></html>"""

    DEST.write_text(doc)
    mb = DEST.stat().st_size / 1e6
    print(f"\nwrote {DEST}  ({mb:.1f} MB)")


if __name__ == "__main__":
    main()
