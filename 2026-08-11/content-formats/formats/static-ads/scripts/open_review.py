#!/usr/bin/env python3
"""The review surface for every suite format whose presentation is still OPEN. FREE.

    python3 open_review.py           # -> ../OPEN-FORMATS.html, opens in the browser

One section per format: what it says, what it is modelled on and what is taken from each
reference, what it renders as today, and the decision waiting on the operator. The cards are the live
PNGs on disk, so this page is never a snapshot that has drifted from the renders.

House rule, 2026-08-10: a dossier is HTML and it opens in the browser.
"""
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from suite_copy import BY_FMT, cards_for  # noqa: E402
import refs  # noqa: E402

OUT = ROOT / "out-suite"
OPEN_FMTS = ["F5", "F6", "F7", "F8", "F9", "F33", "F10"]

# The decision each one is actually waiting on, in one sentence. This is the only hand-kept text.
WAITING = {
    "F5": "A presentation. It is one enormous statement, and the top half of the card is empty.",
    "F6": "A rows template. The five symptom rows have nowhere to sit inside the band law.",
    "F7": "A two-panel template. Them and us need labelled columns the band law allows.",
    "F8": "A split template. The PSA shape needs a hard centre division.",
    "F9": "A rows template with circled numerals, per the scaffold it is modelled on.",
    "F33": "A columns template. Same geometry problem as F7, different content.",
    "F10": "A reference first. It cites nothing, so the citation law blocks it before anything else.",
}


def thumbs(fmt):
    d = OUT / fmt
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.png") if not p.name.startswith("_"))


def refs_html(fmt):
    out = []
    for ref, takes in BY_FMT[fmt]["model"]:
        try:
            e = refs.resolve(ref)
            pic = ""
            if e.get("image") and Path(e["image"]).suffix.lower() != ".svg":
                rel = Path(e["image"]).resolve()
                pic = f'<img class="refpic" src="file://{rel}">'
            out.append(f'<div class="ref">{pic}<b>{html.escape(e["ref"])}</b>'
                       f'<span class="t">{html.escape(e["title"])}</span>'
                       f'<span class="takes">{html.escape(takes)}</span></div>')
        except KeyError:
            out.append(f'<div class="ref dead"><b>{html.escape(ref)}</b>'
                       f'<span class="t">DEAD REFERENCE</span></div>')
    if not out:
        out.append('<div class="ref dead"><b>NOTHING CITED</b>'
                   '<span class="t">Blocked by the citation law until it names a reference</span>'
                   '</div>')
    return "".join(out)


def copy_html(fmt):
    rows = []
    for i, c in cards_for(BY_FMT[fmt]):
        name = i["paper"] if i else c.get("label", "-")
        parts = []
        for k, v in c.items():
            if k in ("gated", "label", "quote_key", "source"):
                continue
            v = " / ".join(v) if isinstance(v, list) else str(v)
            v = html.escape(v).replace("[[", '<em>').replace("]]", "</em>")
            parts.append(f'<div class="line"><span class="k">{k}</span>{v}</div>')
        rows.append(f'<tr><td class="ind">{html.escape(name)}</td><td>{"".join(parts)}</td></tr>')
    return "".join(rows)


CSS = """
*{box-sizing:border-box}body{margin:0;background:#0f0f0f;color:#e8e8e8;
font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:44px 40px 140px}
h1{font-size:30px;font-weight:600;margin:0 0 6px}
h2{font-size:22px;font-weight:600;margin:0 0 2px}
.lede{color:#8a8a8a;max-width:820px;margin:0 0 10px}
.fmt{border-top:1px solid #262626;margin-top:46px;padding-top:26px}
.meta{color:#8a8a8a;font-size:13px;margin:0 0 14px}
.waiting{background:#2f2a12;color:#e3c76a;display:inline-block;padding:6px 12px;border-radius:4px;
font-size:13px;margin:0 0 18px}
.strip{display:flex;gap:14px;overflow-x:auto;padding:4px 0 14px}
.strip figure{margin:0;flex:0 0 auto;width:186px}
.strip img{width:186px;border:1px solid #222;border-radius:3px;display:block}
.strip figcaption{color:#7a7a7a;font-size:11px;letter-spacing:.05em;text-transform:uppercase;
padding-top:6px}
.refs{display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap;margin:6px 0 20px}
.ref{background:#151515;border:1px solid #232323;border-radius:6px;padding:12px 14px;width:290px}
.ref.dead{border-color:#4a2020}
.ref b{display:block;color:#fff;font-size:14px;font-weight:600}
.ref .t{display:block;color:#909090;font-size:12.5px;margin:1px 0 7px}
.ref .takes{display:block;color:#b9b9b9;font-size:12.5px;line-height:1.45}
.refpic{width:100%;border-radius:3px;margin-bottom:9px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:4px}
td{padding:9px 12px 9px 0;border-bottom:1px solid #1c1c1c;vertical-align:top}
.ind{color:#8a8a8a;width:180px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;
padding-top:11px}
.line{margin:2px 0}.k{display:inline-block;width:74px;color:#6e6e6e;font-size:11.5px;
text-transform:uppercase;letter-spacing:.05em}
em{color:#4d90fe;font-style:normal}
"""


def build():
    secs = []
    for fmt in OPEN_FMTS:
        f = BY_FMT[fmt]
        # Label every thumbnail. The strip is filename-ordered, so without a caption the first
        # card in the row is trades while the copy table below it starts on construction.
        pics = "".join(
            f'<figure><img src="file://{p.resolve()}">'
            f'<figcaption>{html.escape(p.stem.replace(fmt + "-", "").replace("-", " "))}'
            f'</figcaption></figure>' for p in thumbs(fmt))
        secs.append(f"""
<div class="fmt"><h2>{fmt} &nbsp;{html.escape(f["name"])}</h2>
<p class="meta">{f["skill"]}, {f["funnel"]}, batch {f["batch"]} &nbsp;·&nbsp;
{len(cards_for(f))} cards &nbsp;·&nbsp; fills {html.escape(f["hooks_id"])}</p>
<div class="waiting">Waiting on: {html.escape(WAITING[fmt])}</div>
<div class="refs">{refs_html(fmt)}</div>
<div class="strip">{pics or '<span class="meta">nothing rendered</span>'}</div>
<table>{copy_html(fmt)}</table></div>""")

    doc = f"""<!doctype html><meta charset="utf-8">
<title>Open formats, review</title><style>{CSS}</style>
<h1>The seven open formats</h1>
<p class="lede">Every suite format whose copy is approved and whose presentation is not decided.
Each one shows what it is modelled on and what is taken from that reference, what it renders as
today, and the decision it is waiting on. Cards are the live PNGs on disk.</p>
{"".join(secs)}"""
    dst = ROOT.parent / "OPEN-FORMATS.html"
    dst.write_text(doc)
    print(f"-> {dst}")
    return dst


if __name__ == "__main__":
    subprocess.run(["open", str(build())])
