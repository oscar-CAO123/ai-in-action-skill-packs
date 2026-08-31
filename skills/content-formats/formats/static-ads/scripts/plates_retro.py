#!/usr/bin/env python3
"""Retro VSL-style plates: warm, grainy, scanned-print direct-response look. ONE job at a time.

    python3 plates_retro.py                  # dry run, prints prompts, spends nothing
    python3 plates_retro.py <slug>           # dry run, one
    python3 plates_retro.py <slug> --go      # shoot it, ONE job, ~2 credits
    python3 plates_retro.py <slug> --refine --go

your direction off an `a reference account` reference post. **The reference images were not
visible**: Instagram blocks Firecrawl and your scraping API quota was exhausted, so only the caption
was read verbatim and the visual is built from your own description, "a retro sort of
VSL-style image on a shot relevant to the pain point". Treat the look as unverified against
the reference until you confirms it.

The third plate family, alongside `plates_noir.py` (black-ground noir) and `plates_white.py`
(white-ground noir). This one is photographic rather than painted: warm amber, heavy grain,
the look of a scanned print out of an old sales letter.

**No text is generated inside the plate.** Type is laid in the composite by `build_retro.py`.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "plates-retro"
HF = "/opt/homebrew/bin/your generation platform"

STYLE = ("A grainy colour photograph shot on expired 35mm film in the early 1980s, warm amber "
         "and faded sepia cast, heavy visible film grain, soft focus falloff at the edges, "
         "slightly blown highlights and milky lifted blacks, the look of a scanned print "
         "reproduced in an old direct-response sales letter. Nostalgic, muted, imperfect, "
         "authentically dated.")

FRAME = ("Shot square on from directly above, flat lay, the subject filling the middle of the "
         "frame with generous empty surface around it, 5:4. No people, no hands, no faces and "
         "no bodies anywhere in the image. Absolutely no text, no lettering, no handwriting, "
         "no signage, no labels, no logos and no legible numbers anywhere: any paperwork is "
         "blurred, creased and illegible. The photograph bleeds to all four edges and fills "
         "the frame completely, with no border, no mount, no frame and no surface visible "
         "behind or around the photograph itself.")

SCENES = {
    # construction / double-handling / callout
    "double-handling": (
        "A carbon-copy job docket book lies open on a dusty construction site office desk, its "
        "yellow and pink duplicate pages fanned apart, and directly beside it sits the beige "
        "keyboard of an old computer with a second identical docket propped against it. The "
        "same job, written once and then entered again."),
    # construction / systems / question
    "systems": (
        "Seven separate beige and grey office machines crowd one small desk, an old computer "
        "terminal, a fax machine, a desk telephone, a calculator, a card index box, a ring "
        "binder and a stack of loose paperwork, each facing a slightly different direction "
        "with cables running everywhere and none of them connected to each other."),
}


def prompt(slug):
    return f"{STYLE} {SCENES[slug]} {FRAME}"


def shoot(slug, refine=False):
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{slug}.png"
    cmd = [HF, "generate", "create", "your image model", "--aspect_ratio", "5:4",
           "--resolution", "2k", "--prompt", prompt(slug), "--wait", "--json"]
    if refine:
        if not dst.exists():
            sys.exit(f"no approved frame at {dst} to refine")
        cmd += ["--image", str(dst)]
    print(f"firing ONE job: {slug}{' (refine)' if refine else ''}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "[" not in r.stdout:
        sys.exit(f"your generation platform failed (exit {r.returncode}):\n{r.stdout[:1500]}\n{r.stderr[:800]}")
    job = json.loads(r.stdout[r.stdout.index("["):])[0]
    url = job.get("result_url")
    if not url:
        sys.exit(f"no result_url:\n{json.dumps(job)[:1500]}")
    print(f"job {job.get('id')}")
    subprocess.run(["curl", "-sSL", "-o", str(dst), url], check=True)
    print(f"saved {dst}  ({dst.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    args = sys.argv[1:]
    go, refine = "--go" in args, "--refine" in args
    picks = [a for a in args if not a.startswith("--")] or list(SCENES)
    for s in picks:
        if s not in SCENES:
            sys.exit(f"unknown scene {s}. have: {list(SCENES)}")
    if not go:
        for s in picks:
            print(f"\n===== {s} =====\n{prompt(s)}\n")
        print("DRY RUN. Nothing spent. Add --go to shoot, ONE at a time.")
    else:
        if len(picks) > 1:
            sys.exit("one paid job at a time. name a single scene.")
        shoot(picks[0], refine)
