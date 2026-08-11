#!/usr/bin/env python3
"""The companion CHROMA-GREEN plate that `collage_news.py` keys the subject out of. Paid.

    python3 cut_news.py construction          # DRY RUN, prints the prompt, spends nothing
    python3 cut_news.py construction --go     # ONE paid i2i job, ~2 credits

Until now this step was run by hand, which is why the first construction cut took two jobs and
still left the scaffolding half-green. It is a script so the other four industries get one
repeatable path, and so the prompt is reviewable before anything is spent.

Method is `bin_gen_cut.sh` from cio-1981-noir: i2i off the approved plate onto flat chroma green,
which keeps the face, the clothing and the lighting while giving `key_green` something it can
actually key. The reference is the RAW plate, not the graded one, so the cutout carries clean
colour instead of the VHS degrade. The graded plate is still what fills the right of the tear.

you, two changes on top of that method:

  * **The sunglasses are generated on him**, not drawn on afterwards by the compositor. They are
    described as a flat comic graphic rather than a real pair, so they still read pop art.
  * **He is framed full length.** The first plate stopped at his waist, so the cutout ended in a
    hard horizontal slice across his torso halfway down the card. Nothing in the compositor can
    invent the rest of him, so the framing has to come from the plate.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from plates_news import SCENES                                        # noqa: E402

ROOT = Path(__file__).parent
PLATES = ROOT / "plates-news"
OUT = ROOT / "cut-news"
HF = "/opt/homebrew/bin/your generation platform"

# What the subject is wearing, per industry, so the prompt can name it and hold the identity.
WEARING = {
    "construction": "a white hard hat and a hi-vis vest over a work shirt and work trousers",
    "real-estate": "business dress",
    "hospitality": "an apron over their work clothes",
    "retail": "their shop-floor work clothes",
    "financial-services": "business dress",
}

# The pose the cut has to PRESERVE. you, : the plates stopped being talking heads, so
# the cut can no longer restate a standing interview or it throws the pose the plate was paid for.
POSE = {
    "construction": "holding a sheet of drawings in both hands and looking up from it",
    "real-estate": "standing and holding a plain unbranded foam-covered handheld microphone "
                   "themselves, in their own hand, up towards their chin",
    "hospitality": "leaning in and setting a plate of food down with one plate still in hand",
    "retail": "reaching up to place a plain unbranded boxed item onto a shelf",
    "financial-services": "seated behind a desk and leaning forward in conversation",
}

GLASSES = (
    "The one thing added to them: a pair of pop-art sunglasses sitting squarely on their face "
    "over both eyes, drawn as a flat comic graphic rather than a real photographed pair, with a "
    "single heavy black outline of even weight, flat bright blue lenses, a field of evenly "
    "spaced lighter blue Ben-Day halftone dots across each lens, one hard white diagonal glint "
    "streak on each lens, a solid black bridge over the nose and one solid black arm running "
    "back towards the ear. The sunglasses are opaque, so neither eye is visible through them.")

# you, : mid-thigh, not head to feet. The copy band takes the bottom 500px of the
# card, so a full-length figure would drop his face to about a third of its current size, and the
# face is what the card is for. Mid-thigh is far enough down that the cutout ends on his legs
# instead of slicing his torso.
# FRAMING is GONE. It asked the model to reframe wider so the body was not cut off, and it was
# ignored on every one of the eight jobs that carried it. Worse, it competes with the one
# instruction that actually matters here, which is deleting the location: the two failures where
# the model merely TINTED the site green instead of replacing it were both dense scenes carrying
# the most instructions. The truncation it was meant to solve is already solved for free by
# bottom-anchoring the subject in `collage_news.py`.

# The financial-services cut kept the interviewer: that plate has an off-camera arm holding the
# microphone, and because the arm reaches all the way in to the subject it keys as one blob with
# them and lands on the card as a disembodied shoulder. The subject holds the microphone
# themselves, so there is only ever one body in the frame to cut out.
ALONE = (
    "The person is completely alone in the frame. There is no second figure. No hand, arm, "
    "shoulder, sleeve or any other body part belonging to anyone else appears anywhere in the "
    "image.")

# Financial services is the one card you wants as a PAIR. The shot is over the client's
# shoulder, so the client is the near foreground and cannot be keyed away without leaving the
# broker talking to nobody. Both are lifted onto the green as one connected mass.
PAIR = {
    "financial-services": (
        "Two people are kept, and only these two: the broker across the desk, sharp and facing "
        "us, and the client seen from behind in the near foreground, of whom only the back of "
        "the head and one shoulder are visible. They are lifted together as one connected group "
        "with the desk between them, in the same positions and at the same sizes as the "
        "reference. The client is never turned around and their face is never shown. No third "
        "person appears anywhere."),
}

# The hospitality cut came back with the whole cafe still standing in the upper left, fully
# opaque under a green cast. Nothing downstream can key that out, so the clause now bans the
# faded remnant by name instead of only asking for green.
GREEN = (
    "The background is one flat uniform pure chroma key green, edge to edge and corner to "
    "corner, with no texture, no gradient, no pattern, no objects, no horizon, no glow, no "
    "vignette and no shadow cast onto it. The original location is deleted completely: not "
    "faded, not tinted, not blurred, not shown through the green and not left as a ghost or a "
    "watermark in any part of the frame. Every wall, every window, every fitting, every piece "
    "of furniture and every vehicle is replaced by that same flat green. The people themselves "
    "carry no green at all. No text, no lettering, no signage, no labels and no numbers "
    "anywhere in the image.")


def prompt(slug):
    who = PAIR.get(slug, ALONE)
    return (f"A photograph of the same person as in the reference image, keeping their exact "
            f"face, their exact hair, their build, their skin, their expression and {WEARING[slug]} "
            f"in the same colours, lit the same way, and holding the SAME POSE as the reference: "
            f"{POSE[slug]}, with their face turned toward the camera. {GREEN} {who} {GLASSES}")


def shoot(slug):
    ref = PLATES / f"{slug}.raw.png"
    if not ref.exists:
        sys.exit(f"no reference plate at {ref}, run plates_news.py {slug} --go first")
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{slug}.png"
    if dst.exists:
        dst.replace(OUT / f"{slug}.prev.png")
        print(f"kept the old cut at {slug}.prev.png")
    cmd = [HF, "generate", "create", "your image model", "--prompt", prompt(slug),
           "--image-references", str(ref), "--aspect_ratio", "4:5", "--resolution", "2k",
           "--wait", "--wait-timeout", "8m", "--wait-interval", "5s", "--json"]
    print(f"firing ONE job: {slug} cut")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "[" not in r.stdout:
        sys.exit(f"your generation platform failed (exit {r.returncode}):\n{r.stdout[:1500]}\n{r.stderr[:800]}")
    job = json.loads(r.stdout[r.stdout.index("["):])[0]
    url = job.get("result_url")
    if not url:
        sys.exit(f"no result_url:\n{json.dumps(job)[:1500]}")
    print(f"job {job.get('id')}")
    subprocess.run(["curl", "-sSL", "-o", str(dst), url], check=True)
    print(f"saved {dst}  ({dst.stat.st_size // 1024} KB)")


if __name__ == "__main__":
    args = sys.argv[1:]
    go = "--go" in args
    picks = [a for a in args if not a.startswith("--")] or ["construction"]
    for s in picks:
        if s not in SCENES:
            sys.exit(f"unknown scene {s}. have: {list(SCENES)}")
    if not go:
        for s in picks:
            print(f"\n===== {s} =====\nref: plates-news/{s}.raw.png\n\n{prompt(s)}\n")
        print("DRY RUN. Nothing spent. Add --go to shoot, ONE at a time.")
    else:
        if len(picks) > 1:
            sys.exit("one paid job at a time. name a single scene.")
        shoot(picks[0])
