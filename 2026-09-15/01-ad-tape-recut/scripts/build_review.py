"""review.html: every recipe as the spoken script, with a rail carrying stage, runtime, each
segment's timecodes and source, and flags. The analysis deliverable. Reads tape.json, bank.json,
recipes.json, transcripts/. Nothing is rendered here."""
import json, html, subprocess, os
from pathlib import Path

HERE = Path.cwd()
TAPE = json.load(open(HERE / "tape.json"))
BANK = {k: v for k, v in json.load(open(HERE / "bank.json")).items() if not k.startswith("_")}
RECIPES = {k: v for k, v in json.load(open(HERE / "recipes.json")).items() if not k.startswith("_")}
T = {p.stem: json.load(open(p)) for p in (HERE / "transcripts").glob("*.json") if not p.stem.endswith(".words")}
WORDS = {p.stem.replace(".words", ""): json.load(open(p)) for p in (HERE / "transcripts").glob("*.words.json")}

def stem(prefix): return TAPE["films"][prefix]["stem"]

def parse(tok):
    if "@" in tok:
        sid, rng = tok.split("@"); a, b = map(float, rng.split("-")); return sid, a, b
    return tok, None, None

def words(sid, s=None, e=None):
    p, ss, ee, st, beat = BANK[sid]
    s = ss if s is None else s; e = ee if e is None else e
    st_ = stem(p)
    if st_ in WORDS:
        txt = " ".join(w for a, b, w in WORDS[st_] if a >= s - 0.05 and a < e - 0.05)
    else:
        txt = " ".join(x["text"] for x in T[st_]["segments"] if x["start"] >= s - 0.05 and x["end"] <= e + 0.05)
    return txt, e - s

cards = []
for rid, r in RECIPES.items():
    script, total, rail, flags = [], 0.0, [], []
    speakers = set()
    for tok in r["segments"]:
        sid, a, b = parse(tok); txt, d = words(sid, a, b); total += d
        p, ss, ee, st, beat = BANK[sid]
        speakers.add(TAPE["films"][p]["speaker"])
        script.append(txt)
        rail.append(f"{sid} · {p} · {(a if a is not None else ss):.2f} to {(b if b is not None else ee):.2f} · {beat}")
        if st == "X": flags.append(f"{sid}: {beat}")
    if len(speakers) > 1: flags.append("crosses speakers (law 2)")
    settings = {TAPE["films"][BANK[parse(t)[0]][0]]["setting"] for t in r["segments"]}
    if len(settings) > 1: flags.append(f"crosses settings {sorted(settings)} (law 3)")
    cards.append(f"""<article><h2>{html.escape(rid)} · {html.escape(r['name'])}</h2>
<div class=script>{'<br><br>'.join(html.escape(s) for s in script)}</div>
<aside><div><b>stage</b> {html.escape(r['stage'])}</div><div><b>speaker</b> {html.escape(', '.join(sorted(speakers)))}</div><div><b>runtime</b> {total:.0f}s</div>
<div><b>segments</b><br>{'<br>'.join(html.escape(x) for x in rail)}</div>
{('<div class=flag><b>flags</b><br>' + '<br>'.join(html.escape(f) for f in flags) + '</div>') if flags else ''}
<div><b>note</b> {html.escape(r.get('note',''))}</div></aside></article>""")

page = f"""<!doctype html><html><head><meta charset=utf-8><title>Recipes · review</title><style>
body{{background:#0d1117;color:#c9d1d9;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;padding:48px 24px 120px}}
main{{max-width:1100px;margin:0 auto}} h1{{font-size:13px;letter-spacing:.2em;text-transform:uppercase;text-align:center;color:#8b949e;margin:0 0 40px}}
article{{display:grid;grid-template-columns:1fr 300px;gap:32px;padding:32px 0;border-top:1px solid #21262d}} h2{{grid-column:1/-1;margin:0 0 8px;font-size:18px;color:#e6edf3}}
.script{{font-size:18px;color:#e6edf3}} aside{{font-size:12px;color:#8b949e;line-height:1.7}} aside b{{color:#c9d1d9}} .flag{{color:#d29922}}
</style></head><body><main><h1>{len(RECIPES)} recipes · nothing rendered</h1>{''.join(cards)}</main></body></html>"""
(HERE / "review.html").write_text(page)
print(len(RECIPES), "recipes on review.html")
if os.environ.get("OPEN"):
    subprocess.run(["open" if os.uname().sysname == "Darwin" else "xdg-open", str(HERE / "review.html")])   # ENV
