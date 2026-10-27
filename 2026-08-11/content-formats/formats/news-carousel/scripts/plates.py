#!/usr/bin/env python3
"""Generate the image plates for a carousel deck, one paid job at a time.

    python3 plates.py three-automations            # every missing plate for that deck
    python3 plates.py three-automations 2 3        # only those slide numbers
    python3 plates.py three-automations --recomp   # no generation, just re-composite

One `your image model` still per slide at 5:4, which is the closest ratio to the 1080x844
plate area above the band. Jobs are dispatched strictly one at a time and each is
downloaded before the next is sent, so an interrupt costs at most one generation.

The plate fills the frame ABOVE the band; the band itself stays pure black and keeps its
single block of Anton, so the bottom-band law is untouched. See band.py.

Prompts live in PROMPTS keyed by deck slug. House visual spec is the Faceless Reframe in
content-formats/SKILL.md section 9: semi-premium and precise, deep near-black navy, ONE
restrained electric blue accent, shallow depth of field, real material texture. Never any
text, lettering, signage, logos or numbers in the plate, because baked-in AI type is
banned and garbles.
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "static-ads" / "scripts"))
from band import render_card  # noqa: E402
from decks2 import DECKS  # noqa: E402
from decks_pains import PAIN_DECKS  # noqa: E402

DECKS = DECKS + PAIN_DECKS

HF = "/opt/homebrew/bin/your generation platform"

LOOK = ("Deep near-black navy palette, one restrained electric blue accent, shallow depth "
        "of field, real material texture, fine film grain, controlled lighting, precise and "
        "understated, semi-premium editorial photography. No people, no text, no lettering, "
        "no signage, no logos, no numbers. The lower third of the frame falls away into "
        "near black.")

PROMPTS = {
    "three-automations": {
        1: "A small Australian business back office late in the evening. A dense stack of "
           "paper invoices, delivery dockets and timesheets piled on a dark timber desk, lit "
           "only by the cool glow of an off-frame monitor. " + LOOK,
        2: "Macro photograph of a phone lying face up on a dark timber desk beside a closed "
           "laptop, its screen throwing a single soft blue notification glow across the "
           "grain. One enquiry arriving in a quiet room. " + LOOK,
        3: "Macro photograph of a stack of metal office filing trays in a dark room, papers "
           "sorted cleanly into each tier, a narrow band of blue light picking out one tray "
           "in the middle of the stack. " + LOOK,
        4: "Tight macro photograph, extreme close range, of a printed bar chart on matte "
           "paper lying on a dark timber desk, the bars catching a thin edge of blue light, "
           "the rest of the sheet falling into shadow. Abstract and graphic, shot at an "
           "oblique angle so nothing is readable. " + LOOK,
        5: "A tidy empty desk in an Australian office at the end of the day, chair pushed in, "
           "monitor dark, one shaft of late blue evening light across the clean timber "
           "surface. Nothing left to do. " + LOOK,
        6: "Macro photograph of an open laptop on a dark desk, screen glowing an even soft "
           "blue with no readable content, inviting and calm, a notebook and pen resting "
           "beside it. " + LOOK,
    },
}

# Hand-drawn white annotations, per deck and slide. Drawn in the composite as SVG so they
# stay crisp and cost nothing. Tail starts just above the type block.
OVERLAYS = {
    "three-automations": {
        1: ('<g fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" '
            'stroke-linejoin="round">'
            '<path d="M712 828 C 706 762, 700 700, 668 648 C 640 602, 600 570, 566 548"/>'
            '<path d="M566 548 C 588 560, 606 566, 624 566"/>'
            '<path d="M566 548 C 574 570, 578 590, 576 610"/>'
            '</g>'),
    },
}


def generate(prompt, dest, tries=4):
    """Dispatch ONE paid still and download it. Blocks until the job finishes.

    The CLI returns exit 3 intermittently under load. Retrying the same prompt succeeds,
    so transient failures are retried with a backoff rather than killing the run. A failed
    dispatch is not billed, so a retry costs nothing extra.
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
    deck = next(d for d in DECKS if d["slug"] == slug)
    plates = ROOT / "plates" / slug
    out = ROOT / "out2" / slug

    for i, copy in enumerate(deck["slides"], 1):
        if only and i not in only:
            continue
        plate = plates / f"slide-{i:02d}.png"
        if not plate.exists() and not recomp:
            prompt = deck.get("plates", [None] * 99)[i - 1] or PROMPTS[slug][i]
            print(f"slide-{i:02d}  generating ...", flush=True)
            generate(prompt, plate)
        report = render_card(copy, out / f"slide-{i:02d}.png",
                             plate=plate if plate.exists() else None,
                             overlay=OVERLAYS.get(slug, {}).get(i))
        print(f"slide-{i:02d}  {report}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
