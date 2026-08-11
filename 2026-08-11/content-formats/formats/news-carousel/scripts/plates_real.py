#!/usr/bin/env python3
"""Real-world plates for the single-card industry statics.

    python3 plates_real.py                                  # DRY RUN, prints every prompt
    python3 plates_real.py construction-and-trades --go      # generate that industry, one at a time
    python3 plates_real.py construction-and-trades systems --go
    python3 plates_real.py <industry> --regrade              # re-grade from raw, free, no generation

Settled with you : the painted noir plates come off these cards and are replaced with
real-world captures. The look is not invented here. It is the **F8 plate-style bank** already built
for the industry-build carousels, at
`projects/content-engine/ideas/industry-build-carousels/styles.json`, and this rig composes its
prompts the same way `gen_plates.py` does (head + shot + body + brief + tail) and applies the same
free ffmpeg grade from `grade_plate.sh`. Same universe, one card instead of a grid.

Two rules that are specific to these plates:

  - **No people.** you, . Every brief is a scene you would actually find in that kind of
    business with nobody in it: the desk after everyone has gone, the bench, the counter, the file
    wall. An empty room reads as the pain; a person in frame reads as a stock photo.
  - **One style per industry set**, unlike the carousels. The F8 law casts style per quadrant because
    a 2x2 grid is meant to look like four sources at once. These post one at a time, so a single
    style per industry is what makes five cards read as one campaign.

Plates land raw in `plates-real/<industry>/<slug>.raw.png` and graded beside them as
`<slug>.png`. The graded file is what `build_industry.py` composites. Re-grading is free, so a style
can be retuned without paying to shoot the scene again.
"""
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from decks_industry import INDUSTRY_STATICS  # noqa: E402

F8 = ROOT.parents[4] / "projects" / "content-engine" / "ideas" / "industry-build-carousels"
STYLES = json.loads((F8 / "styles.json").read_text)["styles"]
GRADE_SH = F8 / "grade_plate.sh"
OUT = ROOT / "plates-real"
HF = "/opt/homebrew/bin/your generation platform"

# ONE style across all five industries: `vhs-camcorder`, the house retro look. you, .
#
# The first pass cast a different F8 stock per vertical (film-16mm, betacam-broadcast, super8-home,
# vhs-camcorder, press-flash). Five stocks made five rows that did not read as one campaign, and the
# press-flash row read as a different brand entirely. VHS is the canonical retro degrade in this
# house, so every plate now carries it and the set holds together on the surface as well as the copy.
#
# Per-vertical stocks are kept below, commented, because they are the F8 cast of record for the
# industry-build carousels. Do not delete them: the 2x2 grid format still uses them.
PLATE_STYLES = dict.fromkeys(
    [
        "construction-and-trades",
        "real-estate-and-property-management",
        "hospitality-and-food-service",
        "retail-and-ecommerce",
        "financial-services-and-insurance",
    ],
    "vhs-camcorder",)

# The F8 per-vertical cast, retired on this format . Restore by replacing the dict above.
F8_VERTICAL_STYLES = {
    "construction-and-trades": "film-16mm",
    "real-estate-and-property-management": "betacam-broadcast",
    "hospitality-and-food-service": "super8-home",
    "retail-and-ecommerce": "vhs-camcorder",
    "financial-services-and-insurance": "press-flash",
}

# (industry, card slug) -> the shot. `brief` is one plain sentence describing a real scene with
# nobody in it. Keep it concrete and ordinary: the model paints what is named and invents the rest.
SCENES = {
    # you, : the first pass put four screens on the desk and it was too busy. One
    # laptop on a bare table. The pain is carried by the copy, so the plate does not have to
    # illustrate "disconnected" by stacking hardware in the frame.
    ("construction-and-trades", "systems"): {
        "shot": "Medium-wide shot",
        "brief": "A single laptop open on a bare site office table, a small stack of printed "
                 "dockets and a mobile phone beside it, nothing else on the surface, the chair "
                 "pushed back and empty"},
    ("construction-and-trades", "double-handling"): {
        "shot": "Overhead close shot",
        "brief": "Two identical copies of the same job paperwork laid side by side on a site office "
                 "desk, one filed in a manila job folder and one loose beside the keyboard, a "
                 "carbon-copy docket book open between them"},
    ("construction-and-trades", "bottleneck"): {
        "shot": "Medium shot",
        "brief": "The owner's desk in a demountable site office at the end of the day, the chair "
                 "empty, the desk phone message light on, and an in-tray overflowing with job "
                 "folders waiting to be signed"},
    # you, : the interior-desk versions came off the four keeper plates. Four of the five
    # keepers were interiors of the same kind of room, so the set read as one office rather than five
    # industries. Each keeper now shows the place the business actually is. Financial services keeps
    # its lamp-lit ledger desk, which you named as the benchmark the others are graded against.
    ("construction-and-trades", "quoting"): {
        "shot": "Wide shot",
        "brief": "An Australian residential construction site at the end of the day, a half-built "
                 "timber frame standing on a concrete slab with scaffolding up one side, stacked "
                 "timber and site gear on the slab, a ute parked at the kerb with its tailgate down"},
    ("construction-and-trades", "headcount"): {
        "shot": "Wide shot",
        "brief": "A small site office with one desk buried in paperwork and a second desk beside it "
                 "completely bare, a monitor still boxed and an unopened office chair carton "
                 "standing where the next hire would sit"},

    ("real-estate-and-property-management", "admin"): {
        "shot": "Medium-wide shot",
        "brief": "A sales agency desk covered in printed contracts and form folders, an open ring "
                 "binder of listing paperwork, a franking machine and a document tray filled past "
                 "the top beside the keyboard"},
    ("real-estate-and-property-management", "systems"): {
        "shot": "Medium shot",
        "brief": "An agency workstation running two monitors and a laptop side by side, each on a "
                 "different property system, a tablet upright on a stand beside them and a printed "
                 "rent roll spreadsheet taped to the desk partition"},
    ("real-estate-and-property-management", "bottleneck"): {
        "shot": "Wide shot",
        "brief": "The principal's glass-walled office at a real estate agency after hours, the "
                 "chair empty and the desk phone lit, a tray of signed and unsigned authority "
                 "forms on the desk, the open-plan sales desks dark behind the glass"},
    ("real-estate-and-property-management", "numbers"): {
        "shot": "Overhead close shot",
        "brief": "A printed spreadsheet of agent figures marked up by hand in pen on an agency "
                 "desk, a calculator resting on top of it and a monitor behind showing a "
                 "half-built report"},
    # you, : explicitly NOT an agency interior. A house, with a clock in the foreground
    # entering from the left edge. The clock is generated in the scene as a real object rather than
    # composited on top, because nothing is drawn over a plate on this format.
    ("real-estate-and-property-management", "leadgen"): {
        "shot": "Wide shot",
        "brief": "An Australian suburban brick house seen from the street in flat daylight, and a "
                 "large round analogue clock in the immediate foreground entering the frame from the "
                 "left edge, close to the lens and far larger than the house behind it, its face "
                 "turned squarely to the camera with its hands clearly visible"},

    ("hospitality-and-food-service", "numbers"): {
        "shot": "Wide shot",
        "brief": "The dining floor of an Australian pub after close, tables laid with chairs pushed "
                 "in, the bar running along the back wall with its taps and stools, the overhead "
                 "lights turned down low"},
    ("hospitality-and-food-service", "hiring"): {
        "shot": "Medium-wide shot",
        "brief": "A venue office noticeboard covered with a handwritten roster grid and printed "
                 "resumes pinned in a row beside it, a coffee-ringed clipboard on the desk below"},
    ("hospitality-and-food-service", "admin"): {
        "shot": "Overhead close shot",
        "brief": "A function room table set up as a makeshift desk, a laptop open beside printed "
                 "menu packages, loose photo prints spread across the cloth and a folder of past "
                 "proposals held open with a glass"},
    ("hospitality-and-food-service", "tribal-knowledge"): {
        "shot": "Close shot",
        "brief": "A commercial kitchen pass at the end of service, a splattered handwritten recipe "
                 "card taped to the shelf above the bench, a row of unlabelled containers and a "
                 "notebook left open on the steel"},
    ("hospitality-and-food-service", "presence"): {
        "shot": "Wide shot",
        "brief": "An empty restaurant floor before opening, chairs still upturned on the tables, "
                 "one light left on over the bar and the front doors closed"},

    ("retail-and-ecommerce", "systems"): {
        "shot": "Wide shot",
        "brief": "The floor of a small Australian retail shop after close, stocked shelving running "
                 "down both walls, a service counter with a till at the back of the room, the lights "
                 "still on"},
    ("retail-and-ecommerce", "bottleneck"): {
        "shot": "Medium shot",
        "brief": "A stockroom office with the chair empty and the desk phone off its cradle, a "
                 "wall of sticky notes stuck around the monitor and an approval tray stacked with "
                 "purchase orders"},
    ("retail-and-ecommerce", "numbers"): {
        "shot": "Overhead close shot",
        "brief": "A shop counter after close with a till roll unspooled across it, a printed sales "
                 "report marked up in pen and a calculator sitting on top of the paper"},
    ("retail-and-ecommerce", "admin"): {
        "shot": "Close shot",
        "brief": "A retail receiving bench piled with opened cartons, packing slips clipped to a "
                 "board, a handwritten stock count sheet and a pen resting on it"},
    ("retail-and-ecommerce", "headcount"): {
        "shot": "Wide shot",
        "brief": "A stockroom aisle stacked to the ceiling with unprocessed cartons, a single "
                 "empty picking trolley parked in the middle of the aisle"},

    ("financial-services-and-insurance", "context"): {
        "shot": "Overhead close shot",
        "brief": "A broker's desk with the same client's details written out three times over, "
                 "once in a paper file, once on a notepad and once on a printed form, all three "
                 "open side by side"},
    ("financial-services-and-insurance", "admin"): {
        "shot": "Medium-wide shot",
        "brief": "A broker's office wall of lever-arch client files floor to ceiling, an "
                 "overflowing document tray on the desk below and a stapled application pack left "
                 "open beside it"},
    ("financial-services-and-insurance", "bottleneck"): {
        "shot": "Medium shot",
        "brief": "A broker's desk after hours, a laptop open beside a whiteboard covered in a "
                 "hand-drawn process flow with arrows and crossings-out, sticky notes stuck in a "
                 "row along the bottom of the board"},
    ("financial-services-and-insurance", "dormant-book"): {
        "shot": "Wide shot",
        "brief": "A storage room of archive boxes of client files on steel shelving, dust settled "
                 "along the upper rows and one box pulled down and left open on the floor"},
    ("financial-services-and-insurance", "trust"): {
        "shot": "Close shot",
        "brief": "A locked filing cabinet in a broker's office with the key still in the lock, a "
                 "compliance folder squared on top of it and a shredder standing beside it"},
}


# Fixes to a plate whose composition is already approved. These run as image-to-image against the
# plate already on disk, never as a fresh generation, so the frame you signed off survives and
# only the named thing changes. Same rule as the rest of the house: refine from the image, do not
# re-roll and hope.
REFINES = {
    # you, . your image model printed "MONITOR" and "OFFICE CHAIR" on the cartons despite
    # the no-text clause. The frame was approved, so only the lettering comes off.
    ("construction-and-trades", "headcount"):
        "Keep this exact frame, composition, lighting and grain unchanged. Remove every printed "
        "word, label, logo and marking from the cardboard boxes so they are plain unmarked brown "
        "cartons. Change nothing else in the image.",
}


# The no-people rule has to be IN the prompt, not just in the brief's silence. The first pass left
# it implicit and five of the twenty-five came back with a person at the desk: the F8 style bodies
# describe how a crew would frame a room, so the model fills it. Stated as an explicit exclusion.
# "The room" was in here until when two keeper briefs moved outdoors (a construction site
# and a house from the street) and the sentence stopped describing the scene it was attached to.
NO_PEOPLE = ("The scene is completely empty of people. No person, no figure, no silhouette, no hands, "
             "no reflection of a person anywhere in the frame.")


def compose(style_key, shot, brief):
    """Same assembly as the F8 rig's `compose`, so these plates sit in that universe exactly,
    plus the explicit no-people exclusion these statics carry."""
    s = STYLES[style_key]
    return "%s %s %s. %s. %s %s No text." % (s["head"], shot, s["body"], brief.rstrip("."),
                                             NO_PEOPLE, s["tail"])


def anchor_for(style_key):
    a = STYLES[style_key].get("anchor")
    return str((F8 / a).resolve) if a else None


def dispatch(prompt, anchor, raw):
    """One paid generation. Blocks until the job returns and the file is on disk.

    5:4, not the carousels' 4:5. These plates fill the 1080x844 area above the band.
    """
    cmd = [HF, "generate", "create", "your image model", "--prompt", prompt,
           "--aspect_ratio", "5:4", "--resolution", "2k", "--wait", "--json"]
    if anchor:
        cmd += ["--image-references", anchor]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "[" not in r.stdout:
        raise RuntimeError(f"generation failed (exit {r.returncode}): {(r.stderr or r.stdout)[:300]}")
    url = json.loads(r.stdout[r.stdout.index("["):])[0]["result_url"]
    raw.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, raw)


def grade(style_key, raw, dest):
    g = STYLES[style_key].get("grade", "none")
    subprocess.run(["bash", str(GRADE_SH), g, str(raw), str(dest)], check=True,
                   stdout=subprocess.DEVNULL)


def main:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    go, regrade = "--go" in sys.argv, "--regrade" in sys.argv
    refine = "--refine" in sys.argv
    want_ind = args[0] if args else None
    want_slug = args[1] if len(args) > 1 else None

    todo = []
    for deck in INDUSTRY_STATICS:
        ind = deck["industry"]
        if want_ind and ind != want_ind:
            continue
        for card in deck["cards"]:
            scene = SCENES.get((ind, card["slug"]))
            if not scene or (want_slug and card["slug"] != want_slug):
                continue
            todo.append((ind, card["slug"], scene))

    if not todo:
        print("nothing authored for that selection yet")
        return

    for ind, slug, scene in todo:
        style = PLATE_STYLES[ind]
        raw = OUT / ind / f"{slug}.raw.png"
        dest = OUT / ind / f"{slug}.png"
        prompt = compose(style, scene["shot"], scene["brief"])

        if regrade:
            grade(style, raw, dest)
            print(f"regraded  {ind}/{slug}")
            continue
        if refine:
            fix = REFINES.get((ind, slug))
            if not fix:
                print(f"{ind}/{slug}  no refine authored, skipping")
                continue
            if not go:
                print(f"=== REFINE {ind}/{slug} ===\n{fix}\n")
                continue
            print(f"{ind}/{slug}  refining from the approved plate ...", flush=True)
            raw.rename(raw.with_suffix(".prefix.png"))
            dispatch(fix, str(raw.with_suffix(".prefix.png").resolve), raw)
            grade(style, raw, dest)
            print(f"{ind}/{slug}  refined -> {dest}", flush=True)
            continue
        if not go:
            print(f"=== {ind}/{slug}  [{style}] ===\n{prompt}\n")
            continue
        if dest.exists:
            print(f"{ind}/{slug}  exists, skipping")
            continue
        print(f"{ind}/{slug}  generating ...", flush=True)
        dispatch(prompt, anchor_for(style), raw)
        grade(style, raw, dest)
        print(f"{ind}/{slug}  done -> {dest}", flush=True)

    if not go and not regrade:
        print(f"DRY RUN, {len(todo)} plate(s). Re-run with --go to generate.")


if __name__ == "__main__":
    main
