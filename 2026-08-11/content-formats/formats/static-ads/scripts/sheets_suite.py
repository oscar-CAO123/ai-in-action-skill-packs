#!/usr/bin/env python3
"""The review surface for the whole suite copy: 35 formats x 7 industries. FREE.

    python3 sheets_suite.py       # build SUITE-DOSSIER.html, then open it in Chrome

Every card at reading size, grouped by sub-skill then format, with its HOOKS.md id, funnel
position and gate status printed beside it. Gated cards render as a labelled block rather than
being left out, so the holes in the set are visible instead of invisible.

Filter by industry from the header. Self-contained: fonts are embedded off `assets/`, so the
page opens anywhere with no network.
"""
import base64
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from magnet_copy import INDUSTRIES  # noqa: E402
from suite_copy import FORMATS, KILLED, cards_for  # noqa: E402

ASSETS = ROOT.parent / "assets"
DOSSIER = ROOT.parent / "SUITE-DOSSIER.html"

SKILLS = ["type-led", "plate-led", "ui-mock", "hand-drawn", "proof"]

# Order the copy keys so a card always reads top to bottom the way it is laid out.
KEY_ORDER = ["kicker", "head", "sub", "body", "left", "right", "rows", "turns", "them_label",
             "them", "us_label", "us", "pins", "before", "after", "answer", "comment", "reply",
             "names", "source", "cta"]


def font(name):
    return base64.b64encode((ASSETS / name).read_bytes()).decode()


def accent(s):
    s = html.escape(s)
    return s.replace("[[", '<b>').replace("]]", '</b>')


CSS = f"""
@font-face {{ font-family:'your display typeface'; font-weight:300;
  src:url(data:font/ttf;base64,{font('jost-300.ttf')}) format('truetype'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500;
  src:url(data:font/ttf;base64,{font('jost-500.ttf')}) format('truetype'); }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0B0B0F;color:#E8E8ED;font-family:'your display typeface',system-ui;font-weight:300;
     padding:44px 52px 140px}}
h1{{font-weight:300;font-size:34px;margin-bottom:6px}}
.lede{{opacity:.62;font-size:16px;max-width:880px;line-height:1.55;margin-bottom:26px}}
.bar{{position:sticky;top:0;background:#0B0B0Fee;backdrop-filter:blur(8px);z-index:9;
     padding:14px 0 18px;margin-bottom:26px;border-bottom:1px solid #1e1e28}}
button{{font-family:inherit;font-weight:300;font-size:14px;color:#E8E8ED;background:#14141c;
     border:1px solid #26263a;border-radius:99px;padding:7px 16px;margin-right:7px;cursor:pointer}}
button.on{{background:#1269ff;border-color:#1269ff}}
h2{{font-weight:300;font-size:13px;letter-spacing:.22em;text-transform:uppercase;
    opacity:.5;margin:52px 0 14px;border-bottom:1px solid #1e1e28;padding-bottom:10px}}
.fmt{{margin:26px 0 40px}}
.fh{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:4px}}
.fid{{font-weight:500;font-size:19px;color:#1269ff}}
.fn{{font-size:19px}}
.meta{{font-size:13px;opacity:.5}}
.hook{{font-size:13px;opacity:.62;margin-bottom:16px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}
.card{{background:#101019;border:1px solid #1e1e28;border-radius:12px;padding:16px 18px}}
.ind{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;opacity:.45;
     margin-bottom:10px}}
.k{{font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.34;margin-top:9px}}
.v{{font-size:16px;line-height:1.42}}
.v b{{font-weight:300;color:#4d92ff}}
.cta{{margin-top:12px;padding-top:11px;border-top:1px solid #1e1e28;font-size:14px;opacity:.72}}
.gated{{background:#1a1206;border-color:#4a3410}}
.gtag{{display:inline-block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
      background:#personally;color:#ffb454;border:1px solid #4a3410;border-radius:4px;
      padding:3px 8px;margin-bottom:10px}}
.src{{font-size:11px;opacity:.38;margin-top:8px;word-break:break-all}}
"""
CSS = CSS.replace("#personally", "#241a08")


def render_card(i, c):
    gated = c.get("gated")
    label = i["name"] if i else c.get("label", "")
    out = [f'<div class="card {"gated" if gated else ""}" data-ind="{i["key"] if i else "founder"}">',
           f'<div class="ind">{html.escape(label)}</div>']
    if gated:
        out.append(f'<div class="gtag">gated</div>'
                   f'<div class="v" style="opacity:.75">{html.escape(gated)}</div>')
    for k in KEY_ORDER:
        if k not in c:
            continue
        v = c[k]
        if k == "cta":
            out.append(f'<div class="cta">{accent(str(v))}</div>')
            continue
        if k == "source":
            out.append(f'<div class="src">{html.escape(str(v))}</div>')
            continue
        out.append(f'<div class="k">{k}</div>')
        if isinstance(v, list):
            for t in v:
                out.append(f'<div class="v">{accent(str(t))}</div>')
        else:
            out.append(f'<div class="v">{accent(str(v))}</div>')
    out.append("</div>")
    return "".join(out)


def build(only_batch=None):
    n_cards = n_gated = 0
    body = []
    batches = sorted({f["batch"] for f in FORMATS})
    for b in batches:
        if only_batch and b != only_batch:
            continue
        fs = [f for f in FORMATS if f["batch"] == b]
        n = sum(len(cards_for(f)) for f in fs)
        body.append(f'<h2>Batch {b} <span style="opacity:.6">'
                    f'({len(fs)} formats, {n} cards, {fs[0]["skill"]})</span></h2>')
        for f in fs:
            cs = cards_for(f)
            cards = []
            for i, c in cs:
                n_cards += 1
                if c.get("gated"):
                    n_gated += 1
                cards.append(render_card(i, c))
            per = ' <span class="meta">one card per quote</span>' if not f["per_industry"] else ""
            body.append(
                f'<div class="fmt">'
                f'<div class="fh"><span class="fid">{f["id"]}</span>'
                f'<span class="fn">{html.escape(f["name"])}</span>'
                f'<span class="meta">{f["skill"]} &middot; {f["funnel"]}</span>{per}</div>'
                f'<div class="hook">fills {html.escape(f["hooks_id"])}</div>'
                f'<div class="grid">{"".join(cards)}</div></div>')

    buttons = ['<button class="on" data-f="all">All</button>']
    buttons += [f'<button data-f="{i["key"]}">{html.escape(i["name"])}</button>'
                for i in INDUSTRIES]
    buttons += ['<button data-f="founder">Founder</button>']

    js = """
const bs=[...document.querySelectorAll('button')];
bs.forEach(b=>b.onclick=()=>{
  bs.forEach(x=>x.classList.remove('on')); b.classList.add('on');
  const f=b.dataset.f;
  document.querySelectorAll('.card').forEach(c=>{
    c.style.display=(f==='all'||c.dataset.ind===f)?'':'none';});
  document.querySelectorAll('.fmt').forEach(m=>{
    const any=[...m.querySelectorAll('.card')].some(c=>c.style.display!=='none');
    m.style.display=any?'':'none';});
});"""

    title = f"Batch {only_batch}" if only_batch else "all copy"
    doc = (f'<meta charset="utf-8"><title>house static suite, {title}</title>'
           f'<style>{CSS}</style>'
           f'<h1>The static suite, {title}</h1>'
           f'<div class="lede">{n_cards} cards, {n_cards - n_gated} authored, {n_gated} gated '
           f'on real material. {len(KILLED)} formats were cut on 2026-08-07. Every line fills a '
           f'named structure in references/hooks/HOOKS.md with its id cited. Bold is the blue '
           f'accent, one per card.</div>'
           f'<div class="bar">{"".join(buttons)}</div>'
           f'{"".join(body)}<script>{js}</script>')
    DOSSIER.write_text(doc)
    return n_cards, n_gated


if __name__ == "__main__":
    b = int(sys.argv[sys.argv.index("--batch") + 1]) if "--batch" in sys.argv else None
    n, g = build(b)
    print(f"  {n} cards, {g} gated -> {DOSSIER}")
    subprocess.run(["open", "-a", "Google Chrome", str(DOSSIER)])
