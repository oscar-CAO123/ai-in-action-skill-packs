#!/usr/bin/env python3
"""News-interview plates in the canonical VHS camcorder look. ONE paid job at a time.

    python3 plates_news.py                 # dry run, prints prompts, spends nothing
    python3 plates_news.py <slug> --go     # shoot it, ONE job, ~2 credits
    python3 plates_news.py <slug> --regrade  # re-grade the raw, FREE

the operator's direction 2026-08-06: fork the reference carousel into the canonical VHS / camcorder
look, as if the avatar is being interviewed on the news. One per industry.

**The reference carousel was never visible.** Instagram blocks Firecrawl and the Apify quota is
exhausted, so this is built from the operator's description, not from the creative. Not a verified fork.

The style is not invented here. `vhs-camcorder` head/body/tail come straight out of the F8
`styles.json` so this stays in sync with the plates the rest of the set already uses, and the
free `grade_plate.sh vhs` chain does the degrade afterwards. The grade does most of the work,
so the generated plate stays clean and well exposed.

**Nothing that implies real media coverage.** No station ident, no channel logo, no ticker, no
"breaking news", no masthead, no named journalist and no outlet. The style tail already bans
overlay graphics and date stamps; those are also the things that would turn this from "shot on
a camcorder" into a fabricated news report. The lower-third is laid in by `build_news.py` and
names the AVATAR'S ROLE, never a person.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
F8 = ROOT.parents[4] / "projects/content-engine/ideas/industry-build-carousels"
STYLE = json.loads((F8 / "styles.json").read_text())["styles"]["vhs-camcorder"]
GRADE_SH = F8 / "grade_plate.sh"
OUT = ROOT / "plates-news"
HF = "/opt/homebrew/bin/higgsfield"

# the operator, 2026-08-06: the owners stop talking to camera and get caught in their own environment.
# REAL ESTATE IS THE EXCEPTION and keeps the interview setup exactly as approved. The other four
# are mid-task, with one requirement that is not cosmetic: the face has to turn far enough toward
# the lens for the pop-art sunglasses to read, because the shades are the signature of the format.
SETUP = ("A single person stands facing camera being interviewed on location, framed from the "
         "chest up slightly off-centre with the location clearly readable behind them, a plain "
         "unbranded foam-covered handheld microphone held up into the bottom of the frame from "
         "just off camera, mid-sentence, looking just off-lens at an unseen interviewer.")

WORKING = ("A candid documentary frame of a person caught in the middle of their own work, "
           "absorbed in the task and not posing, with the place they work clearly readable "
           "around them. There is no microphone and no interviewer. Their head is turned far "
           "enough toward the camera that both eyes and the full front of their face are "
           "clearly visible, as though they have just glanced up at the lens mid-task.")

# The style's own QA note warns that this model writes legible headings onto anything in shot,
# and it did: the first hospitality plate came back with a named cafe and a full menu board on
# the wall. That breaks two rules at once, the layer's ban on generated text and the ban on
# inventing a named business, so the ban is stated in the prompt rather than left to the tail.
NO_TEXT = ("Every surface in the location is blank. No signage, no sign boards, no menu boards, "
           "no chalkboards, no whiteboards, no posters, no notices, no labels, no price tickets, "
           "no branding, no logos, no business name and no writing of any kind anywhere in the "
           "frame, including on walls, boards, windows, vehicles, packaging and clothing.")

# `interview` marks the one scene that keeps the old SETUP. Everything else runs WORKING.
INTERVIEW = {"real-estate"}

SCENES = {
    "construction": (
        "The subject is an Australian construction business owner wearing a white hard hat and a "
        "hi-vis vest over a work shirt, up on their own active building site, reading a sheet of "
        "drawings held in both hands and looking up from it, with steel frames, scaffolding and "
        "stacked timber around them."),
    # The For Sale board is gone from this scene. It contradicted NO_TEXT: the model painted
    # legible "For Sale" lettering onto it, and generated type inside a plate is banned outright.
    # A suburban house and a parked car read as real estate on their own.
    "real-estate": (
        "The subject is an Australian real estate principal in business dress, standing on the "
        "footpath outside a suburban brick house with a low front fence, a garden bed and a "
        "parked car behind them."),
    "hospitality": (
        "The subject is an Australian hospitality business owner in an apron, leaning in to set "
        "plates of food down onto a laid table on their own dining floor, one plate still in "
        "hand, with the seated diners' backs to us and more tables and a service pass behind "
        "them."),
    # the operator, 2026-08-06: the first retail owner read as the same man as the construction one,
    # weathered, fair-haired, fifties. The five cards run as a set, so the subject is described
    # away from that one on purpose.
    "retail": (
        "The subject is an Australian retail business owner in their early thirties, with dark "
        "hair and a full dark beard, of stocky build, restocking a shelf on their own shop "
        "floor, reaching up to place plain unbranded boxed stock onto the shelving with an open "
        "carton at their feet."),
    # the operator, 2026-08-06: the broker sits ACROSS a desk from a client and we shoot past that
    # client's shoulder, and she has to read as a different person from the hospitality owner,
    # who is a brown-haired woman in her fifties. Hence early forties, short blonde hair, slim.
    "financial-services": (
        "The subject is an Australian insurance broker in her early forties with short blonde "
        "hair and a slim build, in business dress, seated behind her own desk in a small office "
        "and leaning forward in conversation with a client seated opposite her. The camera is "
        "behind and just over the client's shoulder, so the back of the client's head and one "
        "shoulder fill the near corner of the frame, out of focus, and the broker is the sharp "
        "subject across the desk. Papers on the desk between them, filing and a window behind "
        "her."),
}


# The sunglasses move into the PLATE. They used to be added by the paid chroma-green cut, which
# was the second job per industry and the one that kept failing. `matte_news.py` now does the
# cutting for free, so the plate is the only paid step and it has to carry the shades itself.
GLASSES = (
    "The subject is wearing a pair of pop-art sunglasses squarely on their face over both eyes, "
    "drawn as a flat comic graphic rather than a real photographed pair, with a single heavy "
    "black outline of even weight, flat bright blue lenses, a field of evenly spaced lighter "
    "blue Ben-Day halftone dots across each lens, one hard white diagonal glint streak on each "
    "lens, a solid black bridge over the nose and one solid black arm running back towards the "
    "ear. The sunglasses are opaque, so neither eye is visible through them.")


def prompt(slug):
    setup = SETUP if slug in INTERVIEW else WORKING
    return (f"{STYLE['head']} {setup} {SCENES[slug]} The subject is {STYLE['body']}. "
            f"{GLASSES} {NO_TEXT} {STYLE['tail']}")


def grade(raw, dst):
    subprocess.run(["bash", str(GRADE_SH), STYLE.get("grade", "vhs"), str(raw), str(dst)],
                   check=True)


def shoot(slug):
    OUT.mkdir(parents=True, exist_ok=True)
    raw, dst = OUT / f"{slug}.raw.png", OUT / f"{slug}.png"
    cmd = [HF, "generate", "create", "nano_banana_pro", "--aspect_ratio", "4:5",
           "--resolution", "2k", "--prompt", prompt(slug), "--wait", "--json"]
    print(f"firing ONE job: {slug}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "[" not in r.stdout:
        sys.exit(f"higgsfield failed (exit {r.returncode}):\n{r.stdout[:1500]}\n{r.stderr[:800]}")
    job = json.loads(r.stdout[r.stdout.index("["):])[0]
    url = job.get("result_url")
    if not url:
        sys.exit(f"no result_url:\n{json.dumps(job)[:1500]}")
    print(f"job {job.get('id')}")
    subprocess.run(["curl", "-sSL", "-o", str(raw), url], check=True)
    grade(raw, dst)
    print(f"saved {dst}  ({dst.stat().st_size // 1024} KB), raw kept at {raw.name}")


if __name__ == "__main__":
    args = sys.argv[1:]
    go, regrade = "--go" in args, "--regrade" in args
    picks = [a for a in args if not a.startswith("--")] or list(SCENES)
    for s in picks:
        if s not in SCENES:
            sys.exit(f"unknown scene {s}. have: {list(SCENES)}")
    if regrade:
        for s in picks:
            raw = OUT / f"{s}.raw.png"
            if raw.exists():
                grade(raw, OUT / f"{s}.png")
            else:
                print(f"  no raw for {s}")
    elif not go:
        for s in picks:
            print(f"\n===== {s} =====\n{prompt(s)}\n")
        print("DRY RUN. Nothing spent. Add --go to shoot, ONE at a time.")
    else:
        if len(picks) > 1:
            sys.exit("one paid job at a time. name a single scene.")
        shoot(picks[0])
