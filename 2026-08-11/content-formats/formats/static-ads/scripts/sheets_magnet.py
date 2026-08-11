#!/usr/bin/env python3
"""Review surfaces for the lead-magnet statics. FREE.

    python3 sheets_magnet.py            # build MAGNET-DOSSIER.html, then open it in Chrome
    python3 sheets_magnet.py --sheet    # also write a contact sheet PNG

The dossier is the surface you walks: every card at review size, grouped by industry, with the
copy, the HOOKS.md id, the magnet it closes on and whether the card is built or still waiting on
a plate printed beside it. Cells that have not been shot render as a labelled gap rather than
being left out, so the holes in the set are visible instead of invisible.
"""
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from magnet_copy import COPY, HOOKS, INDUSTRIES  # noqa: E402

OUT = ROOT / "out-magnet"
DOSSIER = ROOT.parent / "MAGNET-DOSSIER.html"
ASSETS = ROOT.parent / "assets"

FILES = {
    "split": "F-M1-split.png",
    "deliverable": "F-M2-deliverable.png",
    "editorial": "F-M3-editorial.png",
    "billboard": "F-M4-billboard.png",
    "caution": "F-M5-caution.png",
}

CSS = f"""
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{ASSETS}/jost-300.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500; src:url('{ASSETS}/jost-500.ttf'); }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0B0B0F;color:#E8E8ED;font-family:'your display typeface',system-ui;font-weight:300;
     padding:48px 56px 120px}}
h1{{font-weight:300;font-size:34px;letter-spacing:0.01em;margin-bottom:6px}}
.lede{{opacity:.62;font-size:17px;max-width:900px;line-height:1.5;margin-bottom:40px}}
h2{{font-weight:500;font-size:15px;letter-spacing:0.16em;text-transform:uppercase;
   margin:52px 0 4px;color:#4B9EFF}}
.meta{{opacity:.55;font-size:15px;margin-bottom:20px}}
.row{{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}}
.cell{{width:296px}}
.cell img{{width:296px;display:block;border-radius:4px;background:#141419}}
.gap{{width:296px;height:370px;border:1px dashed #34343E;border-radius:4px;display:flex;
     align-items:center;justify-content:center;text-align:center;padding:24px;
     color:#6C6C7A;font-size:14px;line-height:1.45}}
.tag{{font-size:12px;letter-spacing:0.14em;text-transform:uppercase;opacity:.7;
     margin:10px 0 4px}}
.copy{{font-size:13px;line-height:1.45;opacity:.82}}
.id{{font-size:12px;opacity:.45;margin-top:4px;font-style:normal}}
b{{font-weight:500;color:#4B9EFF}}
"""


def cell(industry, hook_key):
    h = HOOKS[hook_key]
    c = COPY[hook_key](industry)
    png = OUT / industry["key"] / FILES[hook_key]
    if png.exists:
        art = f'<img src="{png.resolve.as_uri}">'
    else:
        art = (f'<div class="gap">{h["fmt"]} not built<br>'
               f'waiting on a paid plate</div>')
    body = " ".join(v if isinstance(v, str) else " ".join(v) for v in c.values)
    body = body.replace("[[", "<b>").replace("]]", "</b>")
    return (f'<div class="cell">{art}'
            f'<div class="tag">{h["fmt"]} &middot; {html.escape(h["label"])}</div>'
            f'<div class="copy">{body}</div>'
            f'<div class="id">{html.escape(h["hooks_id"])}</div></div>')


def build:
    rows = []
    for i in INDUSTRIES:
        cells = "".join(cell(i, k) for k in HOOKS)
        plate = i["plate"] or "NO PLATE ON DISK"
        rows.append(
            f'<h2>{html.escape(i["name"])}</h2>'
            f'<div class="meta">{html.escape(i["avatar"])} &nbsp;&middot;&nbsp; '
            f'{html.escape(i["magnet"])} &nbsp;&middot;&nbsp; {html.escape(i["route"])} '
            f'&nbsp;&middot;&nbsp; plate: {html.escape(plate)}</div>'
            f'<div class="row">{cells}</div>')
    built = sum(1 for i in INDUSTRIES for k in HOOKS if (OUT / i["key"] / FILES[k]).exists)
    doc = (f'<meta charset="utf-8"><title>Lead-magnet statics</title><style>{CSS}</style>'
           f'<h1>Lead-magnet statics</h1>'
           f'<p class="lede">Five hooks, seven industries, 35 cards. Every card closes on a lead '
           f'magnet that exists as a built page. {built} of 35 rendered. '
           f'Formats: F-M1 split screen, F-M2 deliverable shot, F-M3 fake editorial, '
           f'F-M4 filmed billboard, F-M5 caution card.</p>'
           + "".join(rows))
    DOSSIER.write_text(doc)
    print(f"{built}/35 rendered -> {DOSSIER}")
    return DOSSIER


def sheet:
    """A flat contact sheet of everything built, for a thumbnail-size read."""
    from PIL import Image
    pngs = [OUT / i["key"] / FILES[k] for i in INDUSTRIES for k in HOOKS]
    pngs = [p for p in pngs if p.exists]
    if not pngs:
        return None
    tw, th, cols = 270, 338, 5
    rows = (len(pngs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * tw, rows * th), "#0B0B0F")
    for n, p in enumerate(pngs):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        sh.paste(im, ((n % cols) * tw, (n // cols) * th))
    out = OUT / "_SHEET.png"
    sh.save(out)
    print(f"contact sheet -> {out}")
    return out


if __name__ == "__main__":
    d = build
    if "--sheet" in sys.argv:
        sheet
    subprocess.run(["open", "-a", "Google Chrome", str(d)], check=False)
