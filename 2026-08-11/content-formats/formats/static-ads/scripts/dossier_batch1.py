"""Candidate batch 1 dossier, finished cards only.

The production-ready deliverables and nothing else: no plates, no beds, no rejects, no
superseded renders. Opens in the browser.

    python3 dossier_batch1.py
    python3 dossier_batch1.py --no-open

U7 is left out: it is archived. Its strongest line survives as U4's O1 closing beat; the ladder
rewrite of took the rest of it with the old O3.
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent.parent / "candidate"
OUT = ROOT / "DOSSIER.html"

UNITS = [
    {
        "unit": "U1a",
        "title": "Band on black",
        "status": ("on the board, idea", "#3ddc84"),
        "board": "row 42",
        "note": "\"most young australians think ai is going to take their job, but if you know "
                "how to use it properly, we want to hire you.\"",
        "cards": [("u1a-laptop.png", "")],
    },
    {
        "unit": "U1b",
        "title": "Poster on paper, falling graduate",
        "status": ("on the board, ready", "#3ddc84"),
        "board": "row 43",
        "note": "Comp sci graduate, scared there is no job at the end of it. Newspaper bed at 0.16.",
        "cards": [("u1b-falling-graduate.png", "")],
    },
    {
        "unit": "U3",
        "title": "The paper carousel",
        "status": ("shipped", "#3ddc84"),
        "board": "row 45, pushed five images verified public",
        "note": "The reference implementation of the format. Copy pruned then line-edited by "
                "you the same day.",
        "cards": [("u3/01-cover.png", "cover"), ("u3/02-who-is-asking.png", "who is asking"),
                  ("u3/03-what-they-need.png", "what they need"),
                  ("u3/04-what-it-pays.png", "what it pays"), ("u3/05-close.png", "close")],
    },
    {
        "unit": "U4",
        "title": "THE FIRST SEAT / THE STEP UP / THE TOP",
        "status": ("on the board, ready", "#3ddc84"),
        "board": "row 46, pushed five images verified public",
        "note": "Rebuilt onto the paper-carousel format on then re-spined onto the "
                "tier ladder on your new cover copy. Close is the Michelangelo's David end "
                "card. Every hero slot was shot to the old spine, so all three are still "
                "off-beat: the re-shoot is under way and the pages want re-uploading as each "
                "plate lands.",
        "cards": [("u4/01-cover.png", "cover"),
                  ("u4/02-the-first-seat.png", "the first seat",
                   "hero is u4-o1, bought tools nobody is running. The page wants a young person "
                   "watching the thing they built run."),
                  ("u4/03-the-step-up.png", "the step up",
                   "hero is the FAILED u4-o2: the held page covers the face, so the page has no "
                   "person in it. Worst of the three."),
                  ("u4/04-the-top.png", "the top",
                   "hero is u4-o3, shot for WHAT PROVES IT. The page wants the senior seat "
                   "answering for it."),
                  ("u4/05-close.png", "close")],
    },
    {
        "unit": "U6",
        "title": "Us versus them, splitscreen static",
        "status": ("on the board, ready", "#3ddc84"),
        "board": "row 47, pushed image verified public",
        "note": "Finished. The CTA names the role you place on your reaffirmed call of "
                "while the rest of the batch sells the the entry-level role entry seat.",
        "cards": [("u6/u6-us-vs-them.png", "")],
    },
]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#0d0e10;color:#e8e9ec;
  font-family:'your display typeface',-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif;
  font-weight:400;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1420px;margin:0 auto;padding:56px 40px 120px}
header h1{font-size:34px;font-weight:400;letter-spacing:.01em;margin:0 0 8px}
header p{margin:0;color:#8a8f98;font-size:15px;line-height:1.6;max-width:70ch}
nav{position:sticky;top:0;background:#0d0e10ee;backdrop-filter:blur(8px);
  padding:16px 0;margin:28px 0 0;border-top:1px solid #24262b;border-bottom:1px solid #24262b;
  z-index:20;display:flex;gap:8px;flex-wrap:wrap}
nav a{font-size:13px;padding:6px 13px;border:1px solid #2c2f36;border-radius:999px;color:#b6bac2}
nav a:hover{border-color:#5a5f6a;color:#fff}
section{margin:72px 0 0;scroll-margin-top:76px}
.head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:6px}
.head h2{font-size:26px;font-weight:400;margin:0;letter-spacing:.01em}
.head .ttl{color:#8a8f98;font-size:16px}
.pill{font-size:11px;letter-spacing:.09em;text-transform:uppercase;padding:4px 11px;
  border-radius:999px;border:1px solid currentColor}
.board{color:#6c7280;font-size:13px;margin:0 0 10px}
.note{color:#a2a7b0;font-size:14.5px;line-height:1.65;max-width:74ch;margin:0 0 28px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:26px}
.grid.solo{grid-template-columns:minmax(0,420px)}
figure{margin:0}
.shot{background:#141518;border:1px solid #24262b;border-radius:5px;overflow:hidden}
.shot img{width:100%;display:block}
figure:hover .shot{border-color:#5a5f6a}
figcaption{margin-top:10px;font-size:13px;color:#c3c7ce;line-height:1.5}
figcaption em{display:block;color:#6c7280;font-style:normal;font-size:11.5px;margin-top:3px}
.warn figcaption em{color:#ffb02e}
.warn .shot{border-color:#5c4520}
footer{margin-top:104px;padding-top:22px;border-top:1px solid #24262b;
  color:#6c7280;font-size:12.5px;line-height:1.8}
@media print{body{background:#fff;color:#000}nav{display:none}}
"""


def card(entry):
    rel, cap = entry[0], entry[1]
    warn = entry[2] if len(entry) > 2 else ""
    p = ROOT / rel
    w, h = Image.open(p).size
    meta = f"{w}x{h}"
    cls = ' class="warn"' if warn else ""
    lines = "<br>".join(x for x in (cap,) if x) or Path(rel).stem
    tail = f"<em>{warn}</em>" if warn else f"<em>{meta}</em>"
    return (f'<figure{cls}><a href="{rel}" target="_blank">'
            f'<div class="shot"><img src="{rel}" loading="lazy" alt="{rel}"></div></a>'
            f'<figcaption>{lines}{tail}</figcaption></figure>')


def main():
    missing = [e[0] for u in UNITS for e in u["cards"] if not (ROOT / e[0]).exists()]
    body = []
    for u in UNITS:
        label, colour = u["status"]
        cards = [e for e in u["cards"] if (ROOT / e[0]).exists()]
        solo = " solo" if len(cards) == 1 else ""
        body.append(
            f'<section id="{u["unit"].lower()}"><div class="head"><h2>{u["unit"]}</h2>'
            f'<span class="ttl">{u["title"]}</span>'
            f'<span class="pill" style="color:{colour}">{label}</span></div>'
            f'<p class="board">{u["board"]}</p><p class="note">{u["note"]}</p>'
            f'<div class="grid{solo}">{"".join(card(e) for e in cards)}</div></section>')

    total = sum(len(u["cards"]) for u in UNITS)
    nav = "".join(f'<a href="#{u["unit"].lower()}">{u["unit"]}</a>' for u in UNITS)
    stamp = datetime.now().strftime("%-d %b %Y, %-I:%M%p").lower()

    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Candidate batch 1, finished cards</title><style>{CSS}</style></head><body><div class="wrap">
<header><h1>Candidate batch 1, finished cards</h1>
<p>The production-ready deliverables, {total} in all, aimed at the the entry-level role entry seat.
Plates, beds and rejects are left out. Click any card for the full-size file.</p></header>
<nav>{nav}</nav>
{"".join(body)}
<footer>Generated {stamp} by scripts/dossier_batch1.py. U7 is excluded: archived, and only its
closing bar survives, as U4's O1.<br>Missing from disk: {", ".join(missing) if missing else "none"}.
</footer></div></body></html>"""

    OUT.write_text(html)
    print(f"{OUT}  ({total} cards, {len(missing)} missing)")
    if "--no-open" not in sys.argv:
        subprocess.run(["open", str(OUT)])


if __name__ == "__main__":
    main()
