#!/usr/bin/env python3
"""White-ground noir-painterly plates for the basic statics. ONE paid job at a time.

    python3 plates_white.py                 # dry run, prints every prompt, spends nothing
    python3 plates_white.py <slug>          # dry run, one
    python3 plates_white.py <slug> --go     # shoot it, ONE job, ~2 credits
    python3 plates_white.py <slug> --refine --go   # i2i fix, keeps the approved frame

your direction, . Two deliberate departures from the house noir plates, both his
call and both recorded here so nobody "corrects" them back:

  1. **White ground, not black.** `decks_noir.py` LIGHT drops the lower quarter into solid
     black. These invert it: flat bright white, figures in black and grey on top.
  2. **People are the subject.** The VHS plate rule is no people in any plate. These are
     figures at desks, because the argument IS the person in the middle.

Still house style: faceless neutral silhouettes, thick oil brushwork, chiaroscuro, purely
black and white with no colour.

**No text is generated inside the plate.** The arrow and the "Your the role you place" label
are drawn in the composite as SVG in the locked 200x80 line-art language, where they are
legible, correctly spelled and editable.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "plates-white"
HF = "/opt/homebrew/bin/your generation platform"

STYLE = ("A black-and-white oil painting in high-contrast film-noir style painted on a bright "
         "flat white ground, thick visible brushstrokes, painterly chiaroscuro, hand-painted "
         "animation still, not a photograph. Every human figure is a neutral faceless "
         "silhouette with no face, no hair detail and no gender cues.")

LIGHT = ("Bright even light on a clean flat white background, luminous white through rich "
         "mid-greys to solid black, thick oil-paint texture, vintage noir mood. Straight-on "
         "eye-level view, symmetrical composition, generous empty white space above the "
         "figures, 5:4. Purely black, white and grey with absolutely no colour of any kind. "
         "Absolutely no text, no lettering, no signage, no labels, no logos, no arrows, no "
         "symbols and no numbers anywhere in the image. The painted scene bleeds to all four "
         "edges and fills the frame completely: this is the artwork itself, never a photograph "
         "of a canvas, so there is no canvas edge, no border, no mount, no frame and no wall "
         "or surface behind or around it anywhere.")

SCENES = {
    # real-estate / admin / contrarian
    "admin-row": (
        "Five office workers sit in one straight unbroken row of identical open cubicles, seen "
        "square on from the front, each at a desk with a monitor and stacks of paper. The two "
        "figures on the far left and the two on the far right, together with their desks, "
        "monitors and cubicle walls, are painted in the palest washed-out pencil grey, thin and "
        "barely there, dissolving into the white ground. The single figure at the exact centre "
        "of the row, and only that figure and that desk, is painted in full deep black and rich "
        "mid-greys with the heaviest and most confident brushwork in the whole frame, sitting "
        "upright and clear, so the eye lands on the centre of the row immediately and stays "
        "there."),
    # real-estate / bottleneck / versus
    "versus-operators": (
        "Two office workers, one on the left and one on the right, each seated square on at "
        "their own desk in their own cubicle, with a wide band of empty bright white running "
        "between them down the centre of the frame. The figure on the left is painted in pale "
        "washed-out grey, hunched and thin, almost dissolving into the white, their desk buried "
        "under high leaning stacks of paper and folders. The figure on the right is painted in "
        "full deep black and rich mid-greys with heavy confident brushwork, sitting upright and "
        "still, their desk completely clear except for one single monitor."),
}


# you, : both cards run across all five industries, and the rule he set is "same
# character and set, camera moves only". So the other four are not fresh generations, they are
# i2i off the APPROVED real estate frame with nothing changed but the camera. A fresh prompt
# would re-cast the figures and the set every time and the five would stop reading as one
# campaign, which is the whole point of holding them still.
CAMERA = {
    "construction": "The camera moves to a low three-quarter view from the left, looking slightly "
                    "up along the row so the desks recede to the right.",
    "hospitality": "The camera moves to a high three-quarter view from the right, looking down "
                   "over the desks so the tops of the cubicle walls are visible.",
    "retail": "The camera moves in closer and lower, square on, so the figures fill more of the "
              "frame and the outermost desks are cropped by the edges.",
    "financial-services": "The camera moves back and to the left, a wide flat view with the row "
                          "set lower in the frame and more empty white above it.",
}
HOLD = ("Keep everything else identical to the reference image: the same figures in the same "
        "poses, the same desks, monitors, paper and cubicles, the same number of figures, the "
        "same one figure painted in deep black while the others stay pale washed-out grey, the "
        "same brushwork, the same flat white ground and the same purely black-and-white palette. "
        "Only the camera position changes. Do not add, remove or re-cast anything.")

# base plate each variant is shot from
VARIANTS = {f"{base}-{ind}": base
            for base in ("admin-row", "versus-operators") for ind in CAMERA}


def prompt(slug):
    if slug in VARIANTS:
        base = VARIANTS[slug]
        ind = slug[len(base) + 1:]
        return f"{STYLE} {SCENES[base]} {CAMERA[ind]} {HOLD} {LIGHT}"
    return f"{STYLE} {SCENES[slug]} {LIGHT}"


def shoot(slug, refine=False):
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{slug}.png"
    cmd = [HF, "generate", "create", "your image model", "--aspect_ratio", "5:4",
           "--resolution", "2k", "--prompt", prompt(slug), "--wait", "--json"]
    if slug in VARIANTS:
        ref = OUT / f"{VARIANTS[slug]}.png"
        if not ref.exists():
            sys.exit(f"no approved base frame at {ref}")
        cmd += ["--image-references", str(ref)]
    elif refine:
        if not dst.exists():
            sys.exit(f"no approved frame at {dst} to refine")
        cmd += ["--image", str(dst)]
    print(f"firing ONE job: {slug}{' (refine)' if refine else ''}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"your generation platform failed:\n{r.stdout}\n{r.stderr}")
    # The CLI returns a JSON LIST and the image is at [0]["result_url"].
    # Same contract as plates_noir.py; do not "simplify" this to a dict lookup.
    if "[" not in r.stdout:
        sys.exit(f"no job in response:\n{r.stdout[:2000]}")
    job = json.loads(r.stdout[r.stdout.index("["):])[0]
    url = job.get("result_url")
    if not url:
        sys.exit(f"job returned no result_url:\n{json.dumps(job)[:2000]}")
    print(f"job {job.get('id')}  {url[:90]}")
    subprocess.run(["curl", "-sSL", "-o", str(dst), url], check=True)
    print(f"saved {dst}  ({dst.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    args = sys.argv[1:]
    go = "--go" in args
    refine = "--refine" in args
    picks = [a for a in args if not a.startswith("--")] or list(SCENES)
    known = list(SCENES) + list(VARIANTS)
    for slug in picks:
        if slug not in known:
            sys.exit(f"unknown scene {slug}. have: {known}")
    if not go:
        for slug in picks:
            print(f"\n===== {slug} =====\n{prompt(slug)}\n")
        print("DRY RUN. Nothing spent. Add --go to shoot, ONE at a time.")
    else:
        if len(picks) > 1:
            sys.exit("one paid job at a time. name a single scene.")
        shoot(picks[0], refine)
