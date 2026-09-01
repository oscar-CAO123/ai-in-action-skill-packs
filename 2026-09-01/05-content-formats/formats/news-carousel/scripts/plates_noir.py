#!/usr/bin/env python3
"""Generate and composite the B&W noir-painterly carousel decks, one paid job at a time.

    python3 plates_noir.py noir-pain-admin              # every missing plate, then composite
    python3 plates_noir.py noir-pain-admin 2 3          # only those slide numbers
    python3 plates_noir.py noir-pain-admin --recomp     # no generation, composite only

Same contract as `plates.py`: one `your image model` still per slide at 5:4 (the closest
ratio to the 1080x844 plate area above the band), dispatched strictly one at a time and
downloaded before the next is sent, so an interrupt costs at most one generation.

What differs from `plates.py`:
  - Prompts are the noir STYLE + scene + LIGHT blocks in `decks_noir.py`, not the photoreal
    Faceless Reframe look.
  - The band renders on the `noir` theme in `band.py`: your display typeface 200, all caps, justified, one
    blue accent. Passed explicitly as `theme="noir"`; omitting it silently falls back to the
    Anton default, which is what shipped the first 22 decks.
  - Annotations are your display typeface labels on hairline leader lines, drawn here as SVG over the raw
    plate. Coordinates are per slide and set by eye AFTER the plate exists, because the
    label has to point at something the model actually painted.

Plates land in `plates-noir/<slug>/`, finished slides in `out-noir/<slug>/`.
"""
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "static-ads" / "scripts"))
from band import render_card  # noqa: E402
from decks_noir import NOIR_DECKS  # noqa: E402

HF = "/opt/homebrew/bin/your generation platform"

# Tool marks. Text annotations were tried and cut on ; the plate now carries the
# logos of the stack the automations are built on instead. They sit in one row in the black
# gap between the painted subject and the band, so no mark ever covers paint.
#
# EVIDENCE NOTE: the admin board records no tool against its three Hub builds. These marks
# carry the counted stack from your content store interview evidence (Claude 198, ChatGPT/GPT 102,
# n8n 71 of 483 populated transcript_summary rows, is a claim about what
# operators use, not a claim about these three specific builds.
LOGOS = (ROOT.parents[4] / "projects" / "content-engine" / "ideas"
         / "museum-gallery-carousels" / "assets" / "logos")

# Every annotation is one group sitting on a single baseline in the black gap between the
# painted subject and the band, so no mark ever covers paint: a small white tool logo, the
# label beside it, and a hairline leader rising from the group to the thing it names.
BASE = 792            # text baseline; the band starts at 844
RISER = 722           # the height the leader stub climbs before it turns to the object
FONT_PX = 25
TRACKING = 0.09       # em, matches the .anno class in band.py
LOGO_PX = 30
LOGO_PAD = 13
MIN_GUTTER = 34       # clear air between two annotation groups on the same baseline

# Must match the `.anno` weight the noir theme sets in band.py, or the measured group
# widths drift from what Chrome actually paints and the leaders miss their objects.
FONT = (ROOT.parents[3] / "content-formats" / "formats" / "static-ads" / "assets"
        / "display-300.ttf")


def text_width(s):
    """Exact advance width of the label, so a group can be centred or right-aligned."""
    from PIL import ImageFont
    f = ImageFont.truetype(str(FONT), FONT_PX)
    return f.getlength(s) + TRACKING * FONT_PX * max(len(s) - 1, 0)


def logo_paths(name):
    """Pull the path geometry out of a 24x24 mono logo SVG."""
    svg = (LOGOS / f"{name}.svg").read_text()
    return re.findall(r'<path[^>]*\sd="([^"]+)"', svg)


def annotation(label, logo, dot_x, dot_y, at_x, anchor, spans=None):
    tw = text_width(label)
    width = tw + (LOGO_PX + LOGO_PAD if logo else 0)
    left = {"start": at_x, "middle": at_x - width / 2, "end": at_x - width}[anchor]
    # Groups sit on one baseline, so two that overlap would print on top of each other.
    # Catch it here rather than finding it on a contact sheet.
    if spans is not None:
        for a, b, other in spans:
            if left < b + MIN_GUTTER and a < left + width + MIN_GUTTER:
                raise ValueError(f'annotation "{label}" collides with "{other}" '
                                 f'({left:.0f}..{left + width:.0f} vs {a:.0f}..{b:.0f})')
        spans.append((left, left + width, label))
    out = []
    if logo:
        d = "".join(f'<path d="{p}"/>' for p in logo_paths(logo))
        # The 24-unit mark is centred on the text's optical middle, not its baseline.
        top = BASE - FONT_PX * 0.72 - (LOGO_PX - FONT_PX * 0.72) / 2
        out.append(f'<g transform="translate({left:.1f} {top:.1f}) '
                   f'scale({LOGO_PX / 24:.4f})" fill="#fff" fill-opacity="0.85">{d}</g>')
    out.append(f'<text class="anno" x="{left + width - tw:.1f}" y="{BASE}">{label}</text>')
    # The leader leaves from the middle of the group and never crosses the label.
    lx = left + width / 2
    out.append(f'<g fill="none" stroke="#fff" stroke-width="1.4" stroke-opacity="0.6">'
               f'<path d="M{lx:.1f} {BASE - 34} L{lx:.1f} {RISER} L{dot_x} {dot_y}"/></g>'
               f'<circle cx="{dot_x}" cy="{dot_y}" r="4.5" fill="#fff" fill-opacity="0.9"/>')
    return "".join(out)


def overlay_for(deck, slide):
    rows = deck.get("annotations", [])
    marks = rows[slide - 1] if slide <= len(rows) else None
    if not marks:
        return None
    spans = []
    return "".join(annotation(*m, spans=spans) for m in marks)


def generate(prompt, dest, tries=4):
    """Dispatch ONE paid still and download it. Blocks until the job finishes.

    The CLI returns exit 3 intermittently under load and a failed dispatch is not billed,
    so transient failures are retried with a backoff rather than killing the run.
    """
    for attempt in range(1, tries + 1):
        r = subprocess.run(
            [HF, "generate", "create", "your image model", "--aspect_ratio", "5:4",
             "--resolution", "2k", "--prompt", prompt, "--wait", "--json"],
            capture_output=True, text=True)
        if r.returncode == 0 and "[" in r.stdout:
            url = json.loads(r.stdout[r.stdout.index("["):])[0]["result_url"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url, dest)
            return url
        print(f"   attempt {attempt} failed (exit {r.returncode}), retrying", flush=True)
        time.sleep(15 * attempt)
    raise RuntimeError(f"generation failed after {tries} attempts: {dest}")


def main():
    slug = sys.argv[1]
    args = sys.argv[2:]
    recomp = "--recomp" in args
    only = {int(a) for a in args if a.isdigit()}
    # The 22 general-pain decks live in decks_noir. The industry Build Breakdown decks
    # (added live in decks_builds and render on the same rig, so the lookup
    # falls through to them rather than duplicating the compositor.
    decks = list(NOIR_DECKS)
    try:
        from decks_builds import BUILD_DECKS
        decks += BUILD_DECKS
    except ImportError:
        pass
    deck = next(d for d in decks if d["slug"] == slug)
    plates = ROOT / "plates-noir" / slug
    out = ROOT / "out-noir" / slug

    for i, copy in enumerate(deck["slides"], 1):
        if only and i not in only:
            continue
        plate = plates / f"slide-{i:02d}.png"
        if not plate.exists() and not recomp:
            print(f"slide-{i:02d}  generating ...", flush=True)
            generate(deck["plates"][i - 1], plate)
        report = render_card(copy, out / f"slide-{i:02d}.png",
                             plate=plate if plate.exists() else None,
                             overlay=overlay_for(deck, i), theme="noir")
        print(f"slide-{i:02d}  {report}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
