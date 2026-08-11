#!/usr/bin/env python3
"""Build the review dossier for a rendered tape carousel and open it in the browser.

    python3 dossier.py [--out DIR]

One self-contained HTML file: every slide at review size, the well that was found drawn
over it, the ground and ink swatches with the measured contrast, and the grade cast that
produced the plate. Everything on the page comes from report.json, so the page cannot
claim a slide passed when the render says otherwise.
"""
import argparse
import base64
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve.parent


def b64(p):
    return base64.b64encode(Path(p).read_bytes).decode


CSS = """
:root{--bg:#0e0f12;--card:#16181d;--line:#262a33;--txt:#e8eaf0;--mut:#8a8fa3;--blue:#1269FF}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--txt);font:15px/1.55 -apple-system,BlinkMacSystemFont,
  'Segoe UI',sans-serif;padding:40px}
h1{font-size:26px;letter-spacing:-.01em;margin-bottom:6px}
.sub{color:var(--mut);margin-bottom:6px}
.angle{color:var(--txt);margin-bottom:28px;max-width:900px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:26px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.shot{position:relative;line-height:0}
.shot img{width:100%;display:block}
.well{position:absolute;border:2px dashed rgba(18,105,255,.95);
  box-shadow:0 0 0 1px rgba(0,0,0,.5) inset}
.well span{position:absolute;top:-1px;left:-1px;background:var(--blue);color:#fff;
  font:600 11px/1 sans-serif;padding:4px 6px;letter-spacing:.06em}
.meta{padding:16px 18px}
.row{display:flex;justify-content:space-between;gap:12px;padding:5px 0;
  border-bottom:1px solid var(--line);font-size:13px}
.row:last-child{border:0}
.row b{font-weight:600;color:var(--mut);font-variant-numeric:tabular-nums}
.sw{display:inline-block;width:13px;height:13px;border-radius:3px;vertical-align:-2px;
  margin-right:6px;border:1px solid rgba(255,255,255,.25)}
.tag{display:inline-block;padding:3px 9px;border-radius:20px;font:600 11px/1.5 sans-serif;
  letter-spacing:.06em}
.ok{background:rgba(40,190,120,.16);color:#42d391}
.bad{background:rgba(255,70,90,.16);color:#ff6b7d}
.verdict{color:#ff6b7d;font-size:12px;padding-top:8px}
.notes{margin-top:34px;border-top:1px solid var(--line);padding-top:22px;
  color:var(--mut);max-width:900px;font-size:13px}
.notes b{color:var(--txt)}
"""


def main:
    ap = argparse.ArgumentParser
    ap.add_argument("--out", default=str(ROOT / "out"))
    args = ap.parse_args
    out = Path(args.out)
    rep = json.loads((out / "report.json").read_text)
    deck, slides = rep["deck"], rep["slides"]

    cards = []
    for s in slides:
        w = s["well"]
        tag = ('<span class="tag ok">CONTRAST OK</span>' if s["pass"]
               else '<span class="tag bad">CONTRAST FAIL</span>')
        verdict = "" if s["pass"] else f'<div class="verdict">{s["verdict"]}</div>'
        cast = s["cast"]
        cards.append(f"""<div class="card">
  <div class="shot"><img src="data:image/png;base64,{b64(out / s['slide'])}">
    <div class="well" style="left:{w['x']}%;top:{w['y']}%;width:{w['w']}%;height:{w['h']}%">
      <span>WELL {w['w']}x{w['h']}%</span></div></div>
  <div class="meta">
    <div class="row"><span>{s['slide']} , {s['kind']}</span>{tag}</div>
    <div class="row"><span>ground</span>
      <b><i class="sw" style="background:{s['ground']}"></i>{s['ground']} L{s['ground_luma']}</b></div>
    <div class="row"><span>ink, {s['ink_law']}</span>
      <b><i class="sw" style="background:{s['ink_head']}"></i>{s['ink_head']}</b></div>
    <div class="row"><span>contrast, head</span>
      <b>{s['contrast_head']}:1 (floor {s['floor_head']}, ceiling {s['headroom']})</b></div>
    <div class="row"><span>contrast, body</span><b>{s['contrast_body']}:1</b></div>
    <div class="row"><span>eyebrow</span>
      <b><i class="sw" style="background:{s['eyebrow_colour']}"></i>
      {'house blue' if s['eyebrow_is_your_table'] else 'blue refused, took the ink law'}</b></div>
    <div class="row"><span>grade cast</span>
      <b>sat {cast['sat']} lift {cast['lift']} soft {cast['soft']} grain {cast['grain']}</b></div>
    <div class="row"><span>well source</span><b>{s['well_source']}</b></div>
    {verdict}
  </div></div>""")

    sources = "".join(f"<li>{x}</li>" for x in deck["sources"])
    html = f"""<!doctype html><meta charset="utf-8"><title>F12 tape carousel , {deck['slug']}</title>
<style>{CSS}</style>
<h1>F12 tape carousel , {deck['slug']}</h1>
<div class="sub">{len(slides)} slides at 1080x1350. Hook structure: {deck['hook_structure']}.
  Audience: {deck['audience']}.</div>
<div class="angle">{deck['angle']}</div>
<div class="grid">{''.join(cards)}</div>
<div class="notes">
  <p><b>The dashed box is the well</b>, the empty region the finder located inside the band the
  deck asked for. The type is laid inside it with an inset, and the ink is taken off the ground
  sampled from that exact box.</p>
  <p><b>Ceiling</b> is the best contrast any ink could reach on that ground. When the ceiling is
  under the floor the plate is the problem, not the type: a mid-luminance well tops out near
  4.6:1 whatever colour the words are.</p>
  <p><b>Sourced from:</b><ul>{sources}</ul></p>
</div>"""
    path = out / "dossier.html"
    path.write_text(html)
    subprocess.run(["open", str(path)])
    print("dossier ->", path)


if __name__ == "__main__":
    main
