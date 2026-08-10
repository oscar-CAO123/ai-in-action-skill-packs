#!/usr/bin/env python3
"""Render house news-headline carousels (4:5, 1080x1350), type-only on pure black.

The format borrows a tabloid breaking-news splash. Four slide types carry the arc:

    splash   giant Anton caps, centred, bottom-anchored, one blue accent phrase
    report   a small Anton eyebrow over a Poppins body block, news-report third person
    stat     one enormous blue figure with a Poppins caption under it
    endcard  Anton CTA lines over the house logo lockup and the url

Copy lives in decks.py. Edit there, re-run this.

    python3 build.py                       # every deck, into ./out
    python3 build.py con-03                # one deck
    python3 build.py --out /path/to/dir    # somewhere else
"""
import os
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from decks import DECKS, ENDCARD

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

LOGO_SVG = re.sub(r"<\?xml.*?\?>", "", (ASSETS / "house-logo.svg").read_text(), flags=re.S)
LOGO_SVG = LOGO_SVG.replace("<svg ", '<svg fill="#FFFFFF" ', 1)

W, H = 1080, 1350
BLUE = "#1269FF"
SAFE = 984            # 1080 minus the 48px side padding
ANTON_ADVANCE = 0.44  # measured average glyph advance as a fraction of font size
POPPINS_ADVANCE = 0.53
SLOP = 1.05           # safety margin on every width estimate

# The splash is bottom-anchored and owns the lower half of the card.
SPLASH_BUDGET = 640
BODY_SIZE, BODY_LH = 40, 1.42

CSS = f"""
@font-face {{ font-family:'Anton'; src:url('{ASSETS}/Anton-Regular.ttf'); }}
@font-face {{ font-family:'PoppinsSB'; src:url('{ASSETS}/Poppins-SemiBold.ttf'); }}
@font-face {{ font-family:'PoppinsM'; src:url('{ASSETS}/Poppins-Medium.ttf'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; overflow:hidden; background:#000; }}
.card {{ position:relative; width:{W}px; height:{H}px; background:#000;
        padding:0 48px; display:flex; flex-direction:column; overflow:hidden; }}
.card.bottom {{ justify-content:flex-end; }}
.card.mid {{ justify-content:center; }}
.kicker {{ display:flex; align-items:center; gap:22px; margin-bottom:32px; }}
.kicker.top {{ position:absolute; top:64px; left:48px; right:48px; margin:0; }}
.kicker .rule {{ flex:1; height:2px; background:rgba(255,255,255,0.55); }}
.kicker .mark {{ font-family:'PoppinsSB'; font-size:24px; letter-spacing:6px;
        color:#fff; text-transform:uppercase; white-space:nowrap; }}
.stage {{ padding-bottom:120px; }}
.headline {{ font-family:'Anton'; color:#fff; text-transform:uppercase;
        letter-spacing:0.5px; line-height:0.94; text-align:center; }}
.headline .line {{ white-space:nowrap; }}
.accent {{ color:{BLUE}; }}
.eyebrow {{ font-family:'Anton'; font-size:44px; letter-spacing:2px; color:{BLUE};
        text-transform:uppercase; margin-bottom:28px; }}
.body {{ font-family:'PoppinsM'; font-size:{BODY_SIZE}px; line-height:{BODY_LH};
        color:#E8EAF0; }}
.body p + p {{ margin-top:26px; }}
.figure {{ font-family:'Anton'; color:{BLUE}; text-transform:uppercase;
        letter-spacing:1px; line-height:0.9; text-align:center; }}
.caption {{ font-family:'PoppinsM'; font-size:36px; line-height:1.4; color:#C7CBD6;
        text-align:center; margin-top:54px; }}
.logo {{ width:400px; margin:104px auto 0; display:block; }}
.logo svg {{ width:100%; height:auto; display:block; }}
.url {{ font-family:'PoppinsM'; font-size:34px; letter-spacing:3px; color:#8A8FA3;
        text-align:center; margin-top:36px; }}
.counter {{ position:absolute; bottom:56px; left:0; right:0; text-align:center;
        font-family:'PoppinsM'; font-size:24px; letter-spacing:4px; color:#8A8FA3; }}
"""

KICKER = ('<div class="kicker"><span class="rule"></span>'
          '<span class="mark">the business</span><span class="rule"></span></div>')


def accent(text):
    return re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span class="accent">{m.group(1)}</span>',
                  html.escape(text))


def wrapped(chars, size, col, advance):
    """How many lines a string of `chars` characters takes in a column of `col` px."""
    return max(1, -(-int(chars * size * advance * SLOP) // col))


def fit_headline(lines, budget=SPLASH_BUDGET, cap=104):
    """Largest Anton size that keeps every hand-broken line on one line, inside the budget."""
    plain = [re.sub(r"\[\[|\]\]", "", ln) for ln in lines]
    longest = max(len(ln) for ln in plain)
    by_width = SAFE / (longest * ANTON_ADVANCE * SLOP)
    by_height = budget / (len(lines) * 0.94)
    return int(min(cap, by_width, by_height))


def fit_figure(text, cap=260):
    return int(min(cap, SAFE / (len(text) * ANTON_ADVANCE * SLOP)))


def body(s):
    t = s["type"]
    if t == "splash":
        size = fit_headline(s["lines"])
        rendered = "\n".join(f'<div class="line">{accent(ln)}</div>' for ln in s["lines"])
        return "bottom", (f'{KICKER}<div class="stage">'
                          f'<div class="headline" style="font-size:{size}px">{rendered}'
                          f'</div></div>')
    if t == "report":
        eyebrow = (f'<div class="eyebrow">{html.escape(s["eyebrow"])}</div>'
                   if s.get("eyebrow") else "")
        paras = "\n".join(f"<p>{accent(p)}</p>" for p in s["paragraphs"])
        return "bottom", (f'{KICKER}<div class="stage">{eyebrow}'
                          f'<div class="body">{paras}</div></div>')
    if t == "stat":
        size = fit_figure(s["figure"])
        top = KICKER.replace('class="kicker"', 'class="kicker top"')
        return "mid", (f'{top}<div class="figure" style="font-size:{size}px">'
                       f'{html.escape(s["figure"])}</div>'
                       f'<div class="caption">{html.escape(s["caption"])}</div>')
    if t == "endcard":
        size = fit_headline(s["lines"], budget=340, cap=84)
        rendered = "\n".join(f'<div class="line">{accent(ln)}</div>' for ln in s["lines"])
        return "mid", (f'<div class="headline" style="font-size:{size}px">{rendered}</div>'
                       f'<div class="logo">{LOGO_SVG}</div>'
                       f'<div class="url">{html.escape(s["url"])}</div>')
    raise ValueError(t)


def slides_for(deck):
    """The five-slide news arc: hook, scene, cost, reveal, CTA."""
    return [
        {"type": "splash", "lines": deck["headline"]},
        {"type": "report", "eyebrow": deck.get("eyebrow", "The scene"),
         "paragraphs": deck["scene"]},
        {"type": "stat", "figure": deck["figure"], "caption": deck["caption"]},
        {"type": "splash", "lines": deck["reveal"]},
        {"type": "endcard", **ENDCARD},
    ]


def render(deck, out_root):
    slides = slides_for(deck)
    out = out_root / deck["slug"]
    out.mkdir(parents=True, exist_ok=True)
    n = len(slides)
    for i, s in enumerate(slides, 1):
        align, inner = body(s)
        counter = "" if s["type"] == "endcard" else f'<div class="counter">{i:02d} / {n:02d}</div>'
        doc = (f'<meta charset="utf-8"><style>{CSS}</style>'
               f'<div class="card {align}">{inner}{counter}</div>')
        with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
            f.write(doc)
            tmp = f.name
        png = out / f"slide-{i:02d}.png"
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{H}",
                        f"--screenshot={png}", f"file://{tmp}"],
                       stderr=subprocess.DEVNULL, check=True)
        Path(tmp).unlink()
    print(f"{deck['slug']}: {n} slides -> {out}")


if __name__ == "__main__":
    args = sys.argv[1:]
    out_root = ROOT / "out"
    if "--out" in args:
        i = args.index("--out")
        out_root = Path(args[i + 1]).expanduser()
        args = args[:i] + args[i + 2:]
    for d in DECKS:
        if not args or d["slug"] in args:
            render(d, out_root)
    print("done")
