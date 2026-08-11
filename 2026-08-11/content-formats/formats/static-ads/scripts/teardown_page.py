#!/usr/bin/env python3
"""Render a teardown doc as a review page: every format beside the still it was read from. FREE.

    python3 teardown_page.py a competitor      # -> ../TEARDOWN-a competitor.html, opens in the browser
    python3 teardown_page.py saas          # the SaaS pull, seven formats
    python3 teardown_page.py formats       # the six-formats pull

The argument matches against the teardown's FILENAME, so any doc in the `tear` bank renders.

The text is read from the teardown markdown and the pictures from the reference bank, so this page
has no content of its own and cannot drift from either.

House rule, : a dossier is HTML and it opens in the browser.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import refs  # noqa: E402

# Two teardowns write the verdict as "**house: ..." and the SaaS one writes "**Transfer: ...".
# Both are read, because the marker is a house style that drifted rather than a difference.
VERDICT = re.compile(r"\*\*(?:house|Transfer): ([^.*]+)", re.I)

CSS = """
*{box-sizing:border-box}body{margin:0;background:#0f0f0f;color:#e8e8e8;
font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:44px 40px 120px}
h1{font-size:30px;font-weight:600;margin:0 0 6px}
.lede{color:#8a8a8a;max-width:820px;margin:0 0 8px}
.item{display:flex;gap:30px;border-top:1px solid #262626;padding:30px 0;align-items:flex-start}
.item img{width:250px;border:1px solid #232323;border-radius:4px;flex:0 0 auto}
.body{flex:1;min-width:0}
h2{font-size:20px;font-weight:600;margin:0 0 4px}
.ref{color:#6f9ad6;font-size:12.5px;font-family:ui-monospace,Menlo,monospace;margin:0 0 12px}
p{margin:0 0 11px;color:#c9c9c9;max-width:760px}
strong{color:#fff;font-weight:600}
.v{display:inline-block;padding:3px 11px;border-radius:3px;font-size:12px;font-weight:600;
margin:0 0 12px;letter-spacing:.03em}
.yes{background:#12301c;color:#7fdca4}.no{background:#301616;color:#e58f8f}
.maybe{background:#2f2a12;color:#e3c76a}
"""


def kind(verdict):
    v = verdict.lower
    if v.startswith(("no", "blocked", "already spent")):
        return "no"
    if v.startswith("yes"):
        return "maybe" if "gated" in v or "only" in v or "with one gate" in v else "yes"
    return "maybe"


def build(which):
    entries = [e for e in refs.doc_entries("tear")
               if which in str(e["src"]).lower and re.match(r"^\d", e["title"])]
    items = []
    for e in entries:
        body = e["body"].splitlines[1:]
        ref = next((ln.strip("` ") for ln in body[:3] if ln.startswith("`local:")), "")
        prose = "\n".join(ln for ln in body if not ln.startswith("`local:")).strip
        verdict = VERDICT.search(prose)
        v = verdict.group(1).strip if verdict else ""
        paras = [p.replace("\n", " ").strip for p in prose.split("\n\n") if p.strip]
        paras = [re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(p)
.replace("&lt;", "<").replace("&gt;", ">")) for p in paras]
        pic = ""
        try:
            img = refs.resolve(ref)["image"]
            pic = f'<img src="file://{Path(img).resolve}">'
        except (KeyError, TypeError):
            pass
        items.append(
            f'<div class="item">{pic}<div class="body"><h2>{html.escape(e["title"])}</h2>'
            f'<p class="ref">{html.escape(ref)}</p>'
            + (f'<span class="v {kind(v)}">house: {html.escape(v)}</span>' if v else "")
            + "".join(f"<p>{p}</p>" for p in paras) + "</div></div>")

    doc = (f'<!doctype html><meta charset="utf-8"><title>Teardown, {which}</title>'
           f"<style>{CSS}</style>"
           f"<h1>{len(items)} static formats, torn down</h1>"
           f'<p class="lede">Extracted from the reel and read one by one. The presenter is masked '
           f"out of every still: he is the walkthrough, not the format, and the block is flat "
           f"rather than painted because the ad behind him is not in the footage. The verdict on "
           f"each is whether it survives house having no product to photograph."
           f"</p>{''.join(items)}")
    dst = ROOT.parent / f"TEARDOWN-{which.upper}.html"
    dst.write_text(doc)
    print(f"{len(items)} formats -> {dst}")
    return dst


if __name__ == "__main__":
    subprocess.run(["open", str(build(sys.argv[1] if len(sys.argv) > 1 else "a competitor"))])
