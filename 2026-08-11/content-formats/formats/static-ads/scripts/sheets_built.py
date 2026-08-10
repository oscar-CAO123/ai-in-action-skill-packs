#!/usr/bin/env python3
"""The review surface for the BUILT suite cards. FREE.

    python3 sheets_built.py              # every rendered card
    python3 sheets_built.py --batch 1

Reads the PNGs off disk rather than re-rendering, so it always shows what actually exists. A
format with no render yet appears as a labelled gap instead of being left out, so the holes in
the set stay visible.
"""
import base64
import html
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from suite_copy import FORMATS, KILLED, cards_for  # noqa: E402

OUT = ROOT / "out-suite"
DOSSIER = ROOT.parent / "SUITE-BUILT.html"
ASSETS = ROOT.parent / "assets"
THUMB = 300


def font(name):
    return base64.b64encode((ASSETS / name).read_bytes()).decode()


def thumb(p):
    im = Image.open(p).convert("RGB")
    im.thumbnail((THUMB, THUMB * 3), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78)
    return base64.b64encode(buf.getvalue()).decode()


CSS = f"""
@font-face {{ font-family:'your display typeface'; font-weight:300;
  src:url(data:font/ttf;base64,{font('jost-300.ttf')}) format('truetype'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500;
  src:url(data:font/ttf;base64,{font('jost-500.ttf')}) format('truetype'); }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0B0B0F;color:#E8E8ED;font-family:'your display typeface',system-ui;font-weight:300;
     padding:44px 52px 140px}}
h1{{font-weight:300;font-size:34px;margin-bottom:6px}}
.lede{{opacity:.62;font-size:16px;max-width:900px;line-height:1.55;margin-bottom:26px}}
.bar{{position:sticky;top:0;background:#0B0B0Fee;backdrop-filter:blur(8px);z-index:9;
     padding:14px 0 18px;margin-bottom:26px;border-bottom:1px solid #1e1e28}}
button{{font-family:inherit;font-weight:300;font-size:14px;color:#E8E8ED;background:#14141c;
   border:1px solid #26263a;border-radius:99px;padding:7px 16px;margin:0 7px 7px 0;cursor:pointer}}
button.on{{background:#1269ff;border-color:#1269ff}}
.fmt{{margin:34px 0 46px}}
.fh{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:3px}}
.fid{{font-weight:500;font-size:20px;color:#1269ff}}
.fn{{font-size:20px}}
.meta{{font-size:13px;opacity:.5}}
.hook{{font-size:13px;opacity:.6;margin-bottom:15px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax({THUMB}px,1fr));gap:16px}}
figure{{background:#101019;border:1px solid #1e1e28;border-radius:10px;padding:10px;
      display:flex;flex-direction:column;gap:9px}}
img{{width:100%;display:block;border-radius:5px}}
figcaption{{font-size:11px;letter-spacing:.15em;text-transform:uppercase;opacity:.5}}
.miss{{background:#1a1206;border-color:#4a3410;color:#ffb454;font-size:14px;
      min-height:180px;align-items:center;justify-content:center;text-align:center}}
"""


def build(only_batch=None):
    n = miss = 0
    body = []
    for b in sorted({f["batch"] for f in FORMATS}):
        if only_batch and b != only_batch:
            continue
        fs = [f for f in FORMATS if f["batch"] == b]
        for f in fs:
            cells = []
            for i, c in cards_for(f):
                key = i["key"] if i else c.get("quote_key", "card")
                p = OUT / f["id"] / f"{f['id']}-{key}.png"
                if p.exists():
                    n += 1
                    cells.append(f'<figure data-ind="{i["key"] if i else "founder"}">'
                                 f'<img src="data:image/jpeg;base64,{thumb(p)}">'
                                 f'<figcaption>{html.escape(key)}</figcaption></figure>')
                else:
                    miss += 1
                    why = c.get("gated") or "not rendered yet"
                    cells.append(f'<figure class="miss" data-ind='
                                 f'"{i["key"] if i else "founder"}">'
                                 f'{html.escape(key)}<br>{html.escape(why)}</figure>')
            per = ' <span class="meta">one card per quote</span>' if not f["per_industry"] else ""
            body.append(
                f'<div class="fmt" data-batch="{b}">'
                f'<div class="fh"><span class="fid">{f["id"]}</span>'
                f'<span class="fn">{html.escape(f["name"])}</span>'
                f'<span class="meta">batch {b} &middot; {f["skill"]} &middot; {f["funnel"]}</span>'
                f'{per}</div>'
                f'<div class="hook">fills {html.escape(f["hooks_id"])}</div>'
                f'<div class="grid">{"".join(cells)}</div></div>')

    from magnet_copy import INDUSTRIES
    buttons = ['<button class="on" data-f="all">All</button>']
    buttons += [f'<button data-f="{i["key"]}">{html.escape(i["name"])}</button>'
                for i in INDUSTRIES]
    buttons += ['<button data-f="founder">Founder</button>']

    js = """
const bs=[...document.querySelectorAll('button')];
bs.forEach(b=>b.onclick=()=>{
  bs.forEach(x=>x.classList.remove('on')); b.classList.add('on');
  const f=b.dataset.f;
  document.querySelectorAll('figure').forEach(c=>{
    c.style.display=(f==='all'||c.dataset.ind===f)?'':'none';});
  document.querySelectorAll('.fmt').forEach(m=>{
    const any=[...m.querySelectorAll('figure')].some(c=>c.style.display!=='none');
    m.style.display=any?'':'none';});
});"""

    title = f"Batch {only_batch}" if only_batch else "built"
    doc = (f'<meta charset="utf-8"><title>house static suite, {title}</title>'
           f'<style>{CSS}</style><h1>The static suite, {title}, rendered</h1>'
           f'<div class="lede">{n} cards on disk, {miss} not built yet. '
           f'{len(KILLED)} formats were cut on 2026-08-07. Every line fills a named structure in '
           f'references/hooks/HOOKS.md with its id cited above each row.</div>'
           f'<div class="bar">{"".join(buttons)}</div>'
           f'{"".join(body)}<script>{js}</script>')
    DOSSIER.write_text(doc)
    return n, miss


if __name__ == "__main__":
    b = int(sys.argv[sys.argv.index("--batch") + 1]) if "--batch" in sys.argv else None
    n, m = build(b)
    print(f"  {n} built, {m} missing -> {DOSSIER}")
    subprocess.run(["open", "-a", "Google Chrome", str(DOSSIER)])
