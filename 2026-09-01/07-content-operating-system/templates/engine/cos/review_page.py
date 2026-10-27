"""The review page.

One self-contained HTML file. No network calls, no build step, no framework. It opens from a
file URL and it still works in two years.

What is on it: each idea in rank order in a single column, and beside each one a muted rail
carrying the evidence it came from. Keep and cut, and nothing else. No dashboards, no charts,
no metadata blocks. An idea with an empty evidence rail never reaches this page, because
ideate.py drops it.
"""

from __future__ import annotations

import html
import json


def esc(value) -> str:
    return html.escape(str(value or ""))


def render(queue: dict, cfg: dict) -> str:
    project = esc(cfg.get("project", {}).get("name") or "Content queue")
    generated = esc(queue.get("generated", "")[:16].replace("T", " "))
    note = queue.get("agent_note", "")

    banner = ""
    if note and "DID NOT RUN" in note:
        banner = f'<div class="banner">{esc(note)}</div>'

    cards = "\n".join(_card(i) for i in queue.get("ideas", []))

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{project} , queue {generated[:10]}</title>
<style>
:root {{
  --bg: #101114; --ink: #e9e7e2; --muted: #8b8a86; --line: #26282d;
  --rail: #16181c; --accent: #c9a227; --cut: #6b2f2f;
  --font: ui-sans-serif, -apple-system, "Segoe UI", system-ui, sans-serif;
}}
@media (prefers-color-scheme: light) {{
  :root {{ --bg: #faf9f7; --ink: #1a1a1a; --muted: #6c6b67; --line: #e2e0da;
           --rail: #f1efe9; --accent: #8a6d1f; --cut: #a34a4a; }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font);
        font-size: 15px; line-height: 1.55; }}
header {{ padding: 48px 32px 24px; max-width: 1180px; margin: 0 auto; }}
h1 {{ font-size: 22px; font-weight: 600; margin: 0 0 4px; letter-spacing: -0.01em; }}
.sub {{ color: var(--muted); font-size: 13px; }}
.banner {{ max-width: 1180px; margin: 0 auto 24px; padding: 14px 18px;
           border: 1px solid var(--cut); border-radius: 4px; color: var(--ink);
           font-size: 13px; }}
main {{ max-width: 1180px; margin: 0 auto; padding: 0 32px 96px; }}
.idea {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 32px;
         padding: 32px 0; border-top: 1px solid var(--line); align-items: start; }}
.idea.cut {{ opacity: 0.32; }}
.rank {{ color: var(--muted); font-size: 12px; letter-spacing: 0.08em;
         text-transform: uppercase; margin-bottom: 10px; }}
.hook {{ font-size: 19px; font-weight: 600; line-height: 1.35; margin: 0 0 12px;
         letter-spacing: -0.01em; }}
.angle {{ margin: 0 0 16px; color: var(--ink); }}
.q {{ border-left: 2px solid var(--accent); padding: 4px 0 4px 14px; margin: 0 0 16px;
      font-size: 16px; }}
.q .label {{ display: block; font-size: 11px; letter-spacing: 0.1em; color: var(--muted);
             text-transform: uppercase; margin-bottom: 4px; }}
.script {{ white-space: pre-wrap; background: var(--rail); padding: 16px 18px;
           border-radius: 4px; font-size: 14px; margin: 0 0 16px; }}
.meta {{ font-size: 12px; color: var(--muted); }}
.meta span {{ margin-right: 16px; }}
.rail {{ background: var(--rail); border-radius: 4px; padding: 18px; font-size: 12.5px;
         color: var(--muted); }}
.rail h3 {{ font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;
            margin: 0 0 12px; color: var(--muted); font-weight: 600; }}
.rail blockquote {{ margin: 0 0 14px; padding: 0; color: var(--ink); font-size: 13px; }}
.rail .src {{ display: block; margin-top: 4px; color: var(--muted); font-size: 11.5px; }}
.rail a {{ color: var(--muted); }}
.acts {{ margin-top: 18px; display: flex; gap: 8px; }}
button {{ font-family: var(--font); font-size: 12px; padding: 6px 14px; border-radius: 3px;
          border: 1px solid var(--line); background: transparent; color: var(--muted);
          cursor: pointer; }}
button.on {{ border-color: var(--accent); color: var(--accent); }}
button.cut.on {{ border-color: var(--cut); color: var(--cut); }}
footer {{ max-width: 1180px; margin: 0 auto; padding: 0 32px 64px; }}
#out {{ width: 100%; min-height: 120px; background: var(--rail); color: var(--ink);
        border: 1px solid var(--line); border-radius: 4px; padding: 12px;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px;
        display: none; }}
@media (max-width: 900px) {{ .idea {{ grid-template-columns: 1fr; }} }}
</style></head><body>
<header>
  <h1>{project}</h1>
  <div class="sub">{generated} &nbsp;·&nbsp; {esc(queue.get('records_considered'))} records
    over {esc(queue.get('lookback_days'))} days &nbsp;·&nbsp;
    {len(queue.get('ideas', []))} ideas</div>
</header>
{banner}
<main>
{cards}
</main>
<footer>
  <button onclick="dump()">Copy decisions</button>
  <textarea id="out" readonly></textarea>
</footer>
<script>
const KEY = 'cos-' + {json.dumps(queue.get('generated', ''))};
let state = {{}};
try {{ state = JSON.parse(localStorage.getItem(KEY) || '{{}}'); }} catch (e) {{ state = {{}}; }}

function paint() {{
  document.querySelectorAll('.idea').forEach(el => {{
    const id = el.dataset.id;
    const v = state[id];
    el.classList.toggle('cut', v === 'cut');
    el.querySelector('.keep').classList.toggle('on', v === 'keep');
    el.querySelector('.cut').classList.toggle('on', v === 'cut');
  }});
}}
function set(id, v) {{
  state[id] = state[id] === v ? undefined : v;
  try {{ localStorage.setItem(KEY, JSON.stringify(state)); }} catch (e) {{}}
  paint();
}}
function dump() {{
  const out = document.getElementById('out');
  out.style.display = 'block';
  out.value = JSON.stringify(state, null, 2);
  out.select();
  try {{ document.execCommand('copy'); }} catch (e) {{}}
}}
paint();
</script>
</body></html>"""


def _card(idea: dict) -> str:
    rank = esc(idea.get("rank", ""))
    idea_id = f"i{rank}"
    hook = esc(idea.get("hook") or idea.get("angle") or "untitled")
    angle = esc(idea.get("angle", "")) if idea.get("hook") else ""
    question = esc(idea.get("founder_question", ""))
    script = esc(idea.get("script", ""))

    meta_bits = []
    if idea.get("format"):
        meta_bits.append(f"<span>{esc(idea['format'])}</span>")
    if idea.get("hook_structure"):
        meta_bits.append(f"<span>hook: {esc(idea['hook_structure'])}</span>")
    if idea.get("proof_tier"):
        meta_bits.append(f"<span>proof: {esc(idea['proof_tier'])}</span>")
    if idea.get("why_now"):
        meta_bits.append(f"<span>{esc(idea['why_now'])}</span>")

    quotes = []
    for item in idea.get("evidence_detail", []):
        link = (f' <a href="{esc(item["permalink"])}">source</a>'
                if item.get("permalink") else "")
        quotes.append(
            f'<blockquote>{esc(item["text"])}'
            f'<span class="src">{esc(item["source_type"])} · {esc(item["date"])} · '
            f'{esc(item["record_id"])}{link}</span></blockquote>'
        )

    return f"""<article class="idea" data-id="{idea_id}">
  <div>
    <div class="rank">{rank}</div>
    <h2 class="hook">{hook}</h2>
    {f'<p class="angle">{angle}</p>' if angle else ''}
    {f'<div class="q"><span class="label">Founder question</span>{question}</div>'
     if question else ''}
    {f'<div class="script">{script}</div>' if script else ''}
    <div class="meta">{''.join(meta_bits)}</div>
    <div class="acts">
      <button class="keep" onclick="set('{idea_id}','keep')">Keep</button>
      <button class="cut" onclick="set('{idea_id}','cut')">Cut</button>
    </div>
  </div>
  <aside class="rail">
    <h3>Evidence</h3>
    {''.join(quotes)}
  </aside>
</article>"""
