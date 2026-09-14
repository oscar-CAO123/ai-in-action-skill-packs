"""review.html: filters by speaker, theme, relevance and score; each card is the clip, the hook,
the quote and a rail with the source at the exact second. Also writes CLIPS.md. OPEN=1 opens it."""
import json, re, html, subprocess, os
from pathlib import Path

H = Path.cwd()
clips = json.load(open(H / "clips.json"))
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]
def dest(c): return H / "clips" / c["speaker"] / f"n{c['n']:03d}_{c['id']}_{slug(c['hook'])}.mp4"
have = [c for c in clips if dest(c).exists()]
def ts(s): s = int(s); return f"{s//60}:{s%60:02d}"
SPEAKERS = sorted({c["speaker"] for c in clips}); THEMES = sorted({t for c in clips for t in c["themes"]})
cards = []
for c in sorted(have, key=lambda c: (-c["score"], c["relevance"] != "core", c["n"])):
    rel = dest(c).relative_to(H)
    tags = " ".join(f"<span class=t>{html.escape(t)}</span>" for t in c["themes"])
    conf = "" if c["speaker_confidence"] == "high" else f"<span class=warn>speaker {c['speaker_confidence']}</span>"
    prec = "" if c.get("precision") == "anchored" else f"<span class=warn>cut {c.get('precision')}</span>"
    hm = "<span class=warn>host mode</span>" if c.get("host_mode") else ""
    up = c["uploaded"]; up = f"{up[:4]}-{up[4:6]}-{up[6:]}" if up and len(up) == 8 else up
    cards.append(f"""<article data-f="{c['speaker']}" data-r="{c['relevance']}" data-t="{' '.join(c['themes'])}" data-s="{c['score']}">
<video preload="none" controls src="{html.escape(str(rel))}"></video>
<div class=body><div class=hook>{html.escape(c['hook'])}</div>
<div class=meta><b>n{c['n']:03d}</b> · {c['speaker']} · {int(c['dur'])}s · score {c['score']} · {c['relevance']} {conf} {prec} {hm}</div>
<div class=tags>{tags}</div><p class=q>{html.escape(c['quote'])}</p>
<div class=rail>{html.escape(c['title'])}<br>{html.escape(c['channel'])} · {up} · <a href="https://youtu.be/{c['id']}?t={int(c['t0'])}" target=_blank>{ts(c['t0'])} to {ts(c['t1'])}</a><br><i>{html.escape(c['why'])}</i><br><code>{html.escape(str(rel))}</code></div></div></article>""")
page = f"""<!doctype html><html><head><meta charset=utf-8><title>Soundbites · review</title><style>
body{{background:#0d1117;color:#c9d1d9;font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;padding:40px 24px 120px}}
main{{max-width:1180px;margin:0 auto}} h1{{color:#e6edf3;font-size:13px;letter-spacing:.2em;text-transform:uppercase;text-align:center;margin:0 0 8px}}
p.intro{{text-align:center;color:#8b949e;font-size:13px;max-width:760px;margin:0 auto 28px}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:28px;position:sticky;top:0;background:#0d1117;padding:12px 0;z-index:2;border-bottom:1px solid #2a313c}}
.bar button{{background:#161b22;color:#c9d1d9;border:1px solid #30363d;border-radius:14px;padding:4px 12px;font-size:12px;cursor:pointer}} .bar button.on{{background:#2f81f7;color:#fff;border-color:#2f81f7}}
.bar .count{{color:#8b949e;font-size:12px;align-self:center;margin-left:8px}}
article{{display:grid;grid-template-columns:420px 1fr;gap:24px;padding:24px 0;border-top:1px solid #21262d}} article.hide{{display:none}}
video{{width:420px;max-width:100%;background:#000;border-radius:6px}}
.hook{{color:#e6edf3;font-size:19px;font-weight:600;line-height:1.35;margin-bottom:6px}} .meta{{color:#8b949e;font-size:12px;margin-bottom:8px}} .meta b{{color:#2f81f7}}
.warn{{color:#d29922;margin-left:8px}} .tags{{margin-bottom:10px}} .t{{display:inline-block;background:#161b22;border:1px solid #30363d;border-radius:10px;font-size:11px;padding:1px 8px;margin-right:4px;color:#8b949e}}
.q{{margin:0 0 12px;color:#c9d1d9;font-size:14px}} .rail{{color:#8b949e;font-size:12px;line-height:1.6}} .rail a{{color:#2f81f7;text-decoration:none}} .rail code{{font-size:11px;color:#6e7681}}
@media(max-width:900px){{article{{grid-template-columns:1fr}} video{{width:100%}}}}
</style></head><body><main>
<h1>Soundbites</h1>
<p class=intro>{len(have)} clips cut from {len({c['id'] for c in have})} episodes. Raw 1080p sections, cut on caption word timings with under a second of padding each side; an edit step tightens the edges. Yellow flags: speaker attribution judged from the transcript only, a cut whose edge fell back to the 15 second stamp, or a host-mode episode.</p>
<div class=bar>
<button data-k=f data-v=all class=on>All speakers</button>{''.join(f'<button data-k=f data-v="{s}">{html.escape(s)}</button>' for s in SPEAKERS)}
<span style="width:12px"></span><button data-k=r data-v=all class=on>All</button><button data-k=r data-v=core>Core</button><button data-k=r data-v=general>General</button>
<span style="width:12px"></span><button data-k=t data-v=all class=on>Any theme</button>{''.join(f'<button data-k=t data-v="{t}">{html.escape(t)}</button>' for t in THEMES)}
<span style="width:12px"></span><button data-k=s data-v=all class=on>Any score</button><button data-k=s data-v=5>5 only</button>
<span class=count id=count></span></div>
{''.join(cards)}
</main><script>
const st={{f:'all',r:'all',t:'all',s:'all'}};
document.querySelectorAll('.bar button').forEach(b=>b.onclick=()=>{{st[b.dataset.k]=b.dataset.v;document.querySelectorAll(`.bar button[data-k=${{b.dataset.k}}]`).forEach(x=>x.classList.remove('on'));b.classList.add('on');apply()}});
function apply(){{let n=0;document.querySelectorAll('article').forEach(a=>{{const ok=(st.f=='all'||a.dataset.f==st.f)&&(st.r=='all'||a.dataset.r==st.r)&&(st.t=='all'||a.dataset.t.split(' ').includes(st.t))&&(st.s=='all'||a.dataset.s==st.s);a.classList.toggle('hide',!ok);if(ok)n++}});document.getElementById('count').textContent=n+' clips'}}
apply();
</script></body></html>"""
(H / "review.html").write_text(page)
lines = ["# Soundbites · index", "", f"{len(have)} clips cut. Columns: n, speaker, seconds, score, relevance, themes, hook, source, file.", ""]
for c in sorted(have, key=lambda c: c["n"]):
    lines.append(f"- n{c['n']:03d} · {c['speaker']} · {int(c['dur'])}s · {c['score']} · {c['relevance']} · {','.join(c['themes'])} · **{c['hook']}** · {c['title'][:60]} (youtu.be/{c['id']}?t={int(c['t0'])}) · `{dest(c).relative_to(H)}`")
(H / "CLIPS.md").write_text("\n".join(lines) + "\n")
print(len(have), "clips on the page")
if os.environ.get("OPEN"):
    subprocess.run(["open" if os.uname().sysname == "Darwin" else "xdg-open", str(H / "review.html")])   # ENV
