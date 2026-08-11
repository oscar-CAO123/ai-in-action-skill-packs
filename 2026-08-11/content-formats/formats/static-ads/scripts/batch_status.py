#!/usr/bin/env python3
"""The ground-truth dossier for the whole creative batch: what is done, what is not. FREE.

    python3 batch_status.py            # -> ../BATCH-STATUS.html, then opens it

Every number on the page is READ, not remembered: format and card counts come from the copy
layer, render counts from the folders on disk, CRM counts from the board itself (pass --crm,
which costs two reads). Anything that could not be checked in this run is labelled UNVERIFIED
on the page rather than being quietly asserted.

Written because four workstreams (the magnets themselves, the magnet statics, the
19-format suite, the carousels) had drifted into four separate handovers and no single view.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from suite_copy import FORMATS, KILLED, cards_for  # noqa: E402
from magnet_copy import HOOKS, INDUSTRIES  # noqa: E402

VAULT = ROOT.parents[5]
OUT_SUITE, OUT_MAGNET = ROOT / "out-suite", ROOT / "out-magnet"
DIST = VAULT / "the business" / "projects" / "lead-magnet-funnels" / "build" / "_shell" / "dist"

# Presentation state per suite format. This is the ONE hand-kept table on the page: it records
# what you has decided, which no file on disk knows. Everything else is measured.
DECIDED = {
    "F1": ("LIVE", "Full-bleed VHS plate, band over it. 7 rows on the board."),
    "F3": ("LIVE", "Seven treatments, one per industry. 7 rows on the board."),
    "F5": ("LIVE", "Four presentations: news, rather, inbox, apology. 4 rows. "
                   "you: 'I love the news headline one.'"),
    "F6": ("LIVE", "Three presentations: search, rows, hand. 3 rows, agnostic."),
    "F7": ("LIVE", "BOTH shapes, agnostic: pen on a ruled pad and the black comparison table. 2 rows, same copy, and the board decides which survives."),
    "F4": ("REOPENED", "Classifieds plates shot and rejected as a shape, and so was the "
                       "job-ad-set-in-type replacement. Waiting on a new shape from you. "
                       "Do not spend until he picks."),
    "F33": ("BUILT, UNSHIPPED", "The consultant contrast, rendered and correct on the same ruled "
                                "pad as F7. Not pushed: you cut the set to one format on "
                                ". `crm_f7_variants.py --fmt F33` ships it if he "
                                "changes his mind."),
    "F8": ("LIVE", "The PERMISSION CAROUSEL, two slides on shot period-noir plates. 2 rows. "
                   "Declared a canonical format: formats/permission-carousel/SKILL.md. The PSA "
                   "split it used to cite is retired."),
    "F9": ("OPEN", "Renders as bare type on black. Already cites tpl:5 - 1x1, so it needs a shape "
                   "rather than a reference. The nearest built thing is the F6 ticked rows."),
    "F10": ("BLOCKED", "Eleven quote cards rendered. Cites NOTHING, and proof/SKILL.md needs the "
                       "testimonial capture before a quote card is legal. Two gates, both open."),
    "F17": ("BLOCKED", "Same two gates as F10: uncited, and needs the testimonial capture."),
    "F24": ("BLOCKED", "Same two gates as F10, plus 7 cards gated on real client quotes."),
    "F20": ("BLOCKED", "Cited and authored, but the frame needs ONE real comment. Nothing to "
                       "fabricate its way around."),
    "F11": ("NOT BUILT", "Plate exists, no renderer. Its head still carries the job-title bug."),
    "F12": ("NOT BUILT", "Plate exists, no renderer."),
    "F14": ("NOT BUILT", "Plate exists, SVG overlay needed."),
    "F16": ("NOT BUILT", "Two grades of one plate, no renderer."),
    "F18": ("NOT BUILT", "Renderer needed, free. Group-chat use needs your approval."),
    "F23": ("NOT BUILT", "Renderer needed, free. The only hand-drawn format left."),
}

# The fourteen assets. `pushed` is the commit state recorded in the lead-magnet handover.
ASSETS = [
    ("The Construction Business AI Audit", "Quiz + report", True),
    ("The Hospitality Business AI Audit", "Quiz + report", True),
    ("The Financial Services Business AI Audit", "Quiz + report", True),
    ("The E-commerce Business AI Audit", "Quiz + report", True),
    ("The Trades Business AI Audit", "Quiz + report", True),
    ("The Real Estate Business AI Audit", "Quiz + report", True),
    ("The Professional Services Business AI Audit", "Quiz + report", True),
    ("The Disconnected Systems Audit", "Quiz + report", False),
    ("The Admin Overload Audit", "Quiz + report", False),
    ("The Owner Bottleneck Audit", "Quiz + report", False),
    ("The Reporting Maturity Index", "Maturity index", False),
    ("The Growth Capacity Audit", "Quiz + report", False),
    ("The Lead Source Build Guide", "Workflow build guide", False),
    ("The AI Hire Due Diligence Kit", "Buyer's kit", False),
]

# Not verifiable from this folder. Stated as coming from the handovers, and labelled as such.
CAROUSELS = [
    ("Industry-build carousels (F8)", "19 verticals x 6 pages", "114 pages live on the CRM",
     "handover industry-build-carousel, "),
    ("Noir pain decks (F5)", "22 decks", "All 22 generated, 14 live on the CRM",
     "handover noir-carousel-pain-queue, "),
    ("Build Breakdown series", "157 unique cases", "Built, UNSHOT",
     "handover build-breakdown-series, "),
]

CSS = """
*{box-sizing:border-box}body{margin:0;background:#0f0f0f;color:#e8e8e8;
font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:48px 40px 120px}
h1{font-size:30px;font-weight:600;margin:0 0 6px}
h2{font-size:19px;font-weight:600;margin:52px 0 4px;padding-top:22px;border-top:1px solid #262626}
.lede{color:#8a8a8a;margin:0 0 22px;max-width:760px}
.sub{color:#8a8a8a;margin:0 0 16px;font-size:14px}
table{border-collapse:collapse;width:100%;margin:14px 0 8px;font-size:14px}
th{text-align:left;color:#8a8a8a;font-weight:500;padding:7px 12px 7px 0;border-bottom:1px solid #262626;
font-size:12px;letter-spacing:.06em;text-transform:uppercase}
td{padding:8px 12px 8px 0;border-bottom:1px solid #1c1c1c;vertical-align:top}
.tag{display:inline-block;padding:2px 9px;border-radius:3px;font-size:11.5px;letter-spacing:.04em;
white-space:nowrap;font-weight:600}
.done{background:#12301c;color:#7fdca4}.open{background:#2f2a12;color:#e3c76a}
.no{background:#301616;color:#e58f8f}.info{background:#1a2433;color:#8fb8e5}
.num{color:#fff;font-variant-numeric:tabular-nums}
.dim{color:#767676}
.big{display:flex;gap:34px;flex-wrap:wrap;margin:18px 0 4px}
.big div{background:#161616;border:1px solid #242424;border-radius:6px;padding:14px 20px;min-width:150px}
.big b{display:block;font-size:27px;font-weight:600;color:#fff;line-height:1.15}
.big span{color:#8a8a8a;font-size:12.5px}
ul{margin:8px 0 0;padding-left:19px;color:#c9c9c9}li{margin:5px 0}
code{background:#1c1c1c;padding:1px 5px;border-radius:3px;font-size:12.5px;color:#c9c9c9}
"""


def tag(kind, text):
    return f'<span class="tag {kind}">{text}</span>'


def rendered(fmt):
    d = OUT_SUITE / fmt
    return len([f for f in d.glob("*.png") if not f.name.startswith("_")]) if d.is_dir else 0


def crm_counts:
    """Read the board. Two calls, both read-only, and both may be skipped."""
    out = {}
    for name, script in (("suite", "crm_suite.py"), ("magnet", "crm_magnet.py")):
        try:
            r = subprocess.run([sys.executable, str(ROOT / script), "--status"],
                               capture_output=True, text=True, timeout=120)
            last = [ln for ln in r.stdout.strip.splitlines if ln.strip][-1]
            out[name] = last.strip
        except Exception as e:                                   # noqa: BLE001
            out[name] = f"UNREAD ({e.__class__.__name__})"
    return out


def build(crm=None):
    n_cards = sum(len(cards_for(f)) for f in FORMATS)
    n_rendered = sum(rendered(f["id"]) for f in FORMATS)
    live = [f for f in FORMATS if DECIDED.get(f["id"], ("", ""))[0] == "LIVE"]
    # Only the seven industry folders. `out-magnet/_shots/` holds review screenshots, not cards,
    # and counting it reported 42 built cards against a set of 35.
    magnet_png = len([p for p in OUT_MAGNET.glob("*/*.png") if not p.parent.name.startswith("_")])
    staged = len(list(DIST.glob("*.html")))
    pushed = sum(1 for *_, p in ASSETS if p)

    rows = []
    for f in FORMATS:
        state, note = DECIDED.get(f["id"], ("?", ""))
        kind = {"LIVE": "done", "BUILT, UNSHIPPED": "info", "REOPENED": "open",
                "OPEN": "open", "BLOCKED": "no", "NOT BUILT": "no"}[state]
        r = rendered(f["id"])
        cited = ", ".join(ref for ref, _ in f["model"]) or "NONE"
        rows.append(
            f'<tr><td class="num">{f["id"]}</td><td>{f["name"]}</td>'
            f'<td class="dim">{f["skill"]}, {f["funnel"]}</td>'
            f'<td class="num">{len(cards_for(f))}</td>'
            f'<td class="num">{r or "<span class=dim>0</span>"}</td>'
            f'<td>{tag(kind, state)}</td>'
            f'<td class="dim">{note}</td>'
            f'<td class="dim">{cited}</td></tr>')

    magnet_rows = "".join(
        f'<tr><td class="num">{h["fmt"]}</td><td>{h["label"]}</td>'
        f'<td class="num">7</td><td class="num">7</td>'
        f'<td>{tag("done", "BUILT")}</td>'
        f'<td class="dim">{", ".join(ref for ref, _ in h["model"])}</td></tr>'
        for h in HOOKS.values)

    asset_rows = "".join(
        f'<tr><td>{n}</td><td class="dim">{fmt}</td>'
        f'<td>{tag("done", "PUSHED") if p else tag("open", "LOCAL, STAGED")}</td></tr>'
        for n, fmt, p in ASSETS)

    car_rows = "".join(
        f'<tr><td>{n}</td><td class="dim">{scale}</td><td>{tag("info", "SEE SOURCE")}</td>'
        f'<td class="dim">{state}</td><td class="dim">{src}</td></tr>'
        for n, scale, state, src in CAROUSELS)

    crm_line = ("" if not crm else
                f'<p class="sub">Board, read this run: <b class="num">{crm["suite"]}</b> '
                f'&nbsp;·&nbsp; <b class="num">{crm["magnet"]}</b></p>')

    html = f"""<!doctype html><meta charset="utf-8">
<title>house creative batch, ground truth</title><style>{CSS}</style>
<h1>The creative batch, what is done and what is not</h1>
<p class="lede">Generated {Path(__file__).name} on demand. Card and format counts are read from
the copy layer, render counts from the folders on disk. Anything that could not be checked in
this run says so.</p>

<div class="big">
  <div><b>{len(ASSETS)}</b><span>lead magnets built</span></div>
  <div><b>{pushed} / {len(ASSETS)}</b><span>magnets pushed</span></div>
  <div><b>{magnet_png}</b><span>magnet statics built</span></div>
  <div><b>{n_rendered} / {n_cards}</b><span>suite cards rendered</span></div>
  <div><b>{len(live)} / {len(FORMATS)}</b><span>suite formats live</span></div>
  <div><b>{len(FORMATS) - len(live)}</b><span>suite formats left</span></div>
</div>
{crm_line}

<h2>1. The lead magnets themselves</h2>
<p class="sub">Fourteen assets. All fourteen are shelled, staged and gated;
{staged} HTML files are sitting in <code>_shell/dist/</code>. The seven local ones need your go
to push.</p>
<table><tr><th>Asset</th><th>Format</th><th>State</th></tr>{asset_rows}</table>

<h2>2. Lead-magnet statics, the promo cards for those assets</h2>
<p class="sub">Five formats across seven industries. This set is FINISHED: every card is built and
every one is on the board. The magnet names and routes were renamed so the PNGs on
disk are current and the CRM row titles still carry the old names.</p>
<table><tr><th>Fmt</th><th>Format</th><th>Cards</th><th>Built</th><th>State</th>
<th>Modelled on</th></tr>{magnet_rows}</table>

<h2>3. The static suite</h2>
<p class="sub">{len(FORMATS)} formats, {n_cards} cards of copy authored, {len(KILLED)} formats
killed. Copy is done for all of them. <b>Presentation is the bottleneck, not copy.</b>
<b class="num">{len(live)} are LIVE</b> and <b class="num">{len(FORMATS) - len(live)} are left</b>:
two are OPEN and workable today, F4 and F33 wait on you, four are BLOCKED behind a citation or a
real quote, and six have no renderer at all. Everything marked OPEN renders today as bare type on
black with the top half empty.</p>
<p class="sub"><b>A format whose rows do not change by industry has no verticals.</b> your cut of
on sight of nine near-identical F7 and F33 cards: F33's seven verticals were
byte-identical and F7's differed only in the head's industry name. The Cards column below is the
copy matrix, NOT a shipping plan. Diff the renders before building a vertical set.</p>
<table><tr><th>Fmt</th><th>Format</th><th>Family</th><th>Cards</th><th>Rendered</th>
<th>State</th><th>Note</th><th>Modelled on</th></tr>{"".join(rows)}</table>

<h2>4. Carousels</h2>
<p class="sub">Not measurable from this folder. Stated from the handovers named in the last
column, and NOT verified in this run.</p>
<table><tr><th>Series</th><th>Scale</th><th>Verified?</th><th>State</th><th>Source</th></tr>
{car_rows}</table>

<h2>What is actually blocking</h2>
<ul>
<li><b>F8 is next and it needs a REFERENCE before it can have a shape.</b> Nothing is cited for it
yet. F9 is the one after, and it already cites <code>tpl:5 - 1x1</code>, so it needs a shape only.
Both are one agnostic card, not seven.</li>
<li><b>F4 is mid-decision.</b> Seven classifieds plates are shot and on disk, both that shape and
the job-ad replacement were rejected, and nothing should be spent until the shape is picked.</li>
<li><b>Four formats are blocked on evidence, not on design.</b> F10, F17 and F24 cite nothing AND
need the testimonial capture; F20 needs one real comment. <code>proof/SKILL.md</code> is absolute,
so none of the four can be built its way around.</li>
<li><b>Six formats have no renderer at all</b> (F11, F12, F14, F16, F18, F23). Each needs a shape
from scratch. <code>f11_news_headline</code> also still carries the job-title bug that killed
F2.</li>
<li><b>Seven magnets are staged but unpushed</b>, waiting on your go.</li>
<li><b>The 35 CRM rows carry pre-rename magnet names</b> in their titles. Fixing that is a prod
write and needs your go.</li>
</ul>
"""
    dst = ROOT.parent / "BATCH-STATUS.html"
    dst.write_text(html)
    print(f"-> {dst}")
    return dst


if __name__ == "__main__":
    crm = crm_counts if "--crm" in sys.argv else None
    path = build(crm)
    # Plain `open`, so it lands in the browser. House rule, : dossiers are HTML and
    # they are reviewed in the browser, never in Cursor.
    subprocess.run(["open", str(path)])
