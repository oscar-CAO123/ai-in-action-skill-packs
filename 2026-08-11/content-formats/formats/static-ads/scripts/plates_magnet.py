#!/usr/bin/env python3
"""Every paid plate for the lead-magnet statics. DRY RUN by default, spends nothing.

    python3 plates_magnet.py                          # print all 30 prompts, free
    python3 plates_magnet.py construction             # one industry's prompts
    python3 plates_magnet.py --fmt split              # one format across every industry
    python3 plates_magnet.py construction split before --go     # shoot ONE job
    python3 plates_magnet.py construction --regrade   # re-grade from raw, free
    python3 plates_magnet.py --refine construction split after --go   # i2i fix, keeps the frame

Four of the five formats need generation. F-M2 (the deliverable shot) needs none: it is a
headless-Chrome capture of a page that already exists.

| Format | Jobs | Aspect | Style |
|---|---|---|---|
| F-M1 split screen | 2 per industry, 14 | 4:5, cropped to 540x1350 | vhs-camcorder |
| F-M3 editorial coverage | 1 per industry, 7 | 3:2 | vhs-camcorder |
| F-M4 billboard plate | 1 per industry, 7 | 4:5 | clean phone photo, copy generated |
| F-M5 caution plate | 2, the industries with no plate | 5:4 | vhs-camcorder |

**30 jobs total, 4 of them before the first review gate.** One at a time, always. the operator's
standing rule: never batch paid jobs, review the still before the next is sent.

Four traps this rig is written around, all already paid for:

  - **9:16 makes this model letterbox.** The first split-screen job came back as a landscape
    scene pillarboxed inside a tall dark frame, a picture of a screen rather than a scene, and
    the style tail's "no letterboxing, no frame within the frame" did not stop it. Shot at 4:5,
    which is the aspect the whole house uses, it composes edge to edge. The half is cropped to
    540x1350 from there. Do not put 9:16 back.

  - **The model writes legible signage onto anything in shot.** The `No text.` tail is not
    optional and it has already cost two re-shoots (a named cafe with a full menu board, and a
    legible "For Sale"). Check the returned still before grading.
  - **A split screen dies if the person changes.** `subject` is written ONCE per industry and
    substituted verbatim into both prompts. The rig asserts the two are byte-identical before
    it will dispatch either one.
  - **This model CAN set type when it is short, in caps and quoted line by line**, which is how
    F-M4 gets its billboard copy. It cannot be trusted with it: check every returned plate letter
    by letter before grading, and re-roll on a typo rather than accepting it.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from magnet_copy import INDUSTRIES, BY_KEY  # noqa: E402

VAULT = ROOT.parents[5]
F8 = (VAULT / "the business" / "projects" / "content-engine" / "ideas"
      / "industry-build-carousels")
STYLES = json.loads((F8 / "styles.json").read_text())["styles"]
GRADE_SH = F8 / "grade_plate.sh"
OUT = ROOT / "plates-magnet"
HF = "/opt/homebrew/bin/higgsfield"

NO_PEOPLE = ("The scene is completely empty of people. No person, no figure, no silhouette, "
             "no hands, no reflection of a person anywhere in the frame.")

# ---------------------------------------------------------------------------------------------
# F-M1. The split screen.
#
# `subject` is the person, and it is used VERBATIM in both halves. Only the light, the posture
# and the state of the room change. A different face on the right reads as a stock photo pair
# and the format stops working, which is the one thing F9 already learned the hard way.
#
# The BEFORE half hides the face by posture: head in both hands, or seen from behind. The AFTER
# half faces camera so the compositor can lay the flat cartoon censor bar across the eyes.
# the operator, 2026-08-06: cast the treatment to the half.
#
# "head in both hands" is NOT enough on its own. The first construction job came back with the
# hands on the forehead and the whole face, eyes included, in clear view. Every before clause now
# states the hiding explicitly, as a fact about the frame rather than a description of a pose.
FACE_HIDDEN = ("His face is completely hidden and not visible at all in the frame. "
               "No eyes, no mouth, no facial features are visible anywhere.")
FACE_HIDDEN_HER = ("Her face is completely hidden and not visible at all in the frame. "
                   "No eyes, no mouth, no facial features are visible anywhere.")
SPLIT = {
    "construction": dict(
        subject="an Australian construction business owner in his forties with short dark hair, "
                "wearing a navy work shirt with the sleeves rolled up and an unmarked hi-vis vest "
                "over it, in a demountable site office",
        before="buried at the desk with his head in both hands, the desk covered with three open "
               "laptops and stacks of printed job dockets, one low desk lamp the only light in the "
               "room and everything past it falling to black",
        after="sitting upright at the same desk facing the camera with his hands resting on the "
              "desk, the desk clear except for one closed laptop, daylight through the site office "
              "window filling the whole room"),
    "real-estate": dict(
        she=True,
        subject="an Australian real estate agency principal in her forties with dark hair tied "
                "back, wearing a charcoal blazer over a plain white shirt, in a glass-walled "
                "agency office",
        before="seen from behind with her shoulders dropped, facing a desk stacked with printed "
               "contracts and form folders piled higher than the monitor, one low lamp and the "
               "rest of the office dark",
        # the operator, 2026-08-06: the after half moves OUTSIDE. The office-to-office pair read as one
        # room twice; an open home is where the work actually lands when the admin comes off.
        after="standing outside on the front lawn at a busy open-home auction, upright and at "
              "ease facing the camera with a clipboard under one arm, a crowd of buyers gathered "
              "on the grass and the footpath behind her, a brick suburban house behind them, "
              "clear daylight"),
    "hospitality": dict(
        subject="an Australian hospitality business owner in his fifties with close-cropped greying "
                "hair, wearing a plain black apron over a grey shirt, in a pub dining room",
        before="head in both hands over a spread of printed supplier invoices and a handwritten "
               "takings sheet on a dining table, chairs still upturned on the tables behind him, "
               "one light left on over the bar",
        after="standing upright behind the same table facing the camera, the table clear except "
              "for a tablet lying flat on it, the dining room lit and set for service behind him"),
    "retail": dict(
        she=True,
        subject="an Australian retail shop owner in her thirties with her hair pulled back, "
                "wearing a plain dark polo shirt, behind the service counter of her shop",
        before="seen from behind with her shoulders dropped, facing a counter buried under "
               "purchase orders with sticky notes stuck all around the monitor, the shop floor "
               "dark behind her",
        after="standing behind the same counter facing the camera with her arms folded easily, "
              "the counter clear, the shop floor lit and fully stocked behind her"),
    "financial-services": dict(
        subject="an Australian insurance broker in his forties wearing a white shirt with the "
                "collar open and no tie, in an office lined floor to ceiling with lever-arch "
                "client files",
        before="head in both hands at the desk over the same client's details written out three "
               "times across a paper file, a notepad and a printed form all open side by side, "
               "one desk lamp and the rest of the room black",
        after="sitting upright at the same desk facing the camera with one closed client file "
              "squared in front of him, daylight filling the office and the file wall behind "
              "him straightened"),
    "building-services": dict(
        subject="an Australian plumbing and electrical services business owner in his forties "
                "wearing a plain navy work polo with no printing on it, in a small trade workshop "
                "office",
        before="seen from behind with his shoulders dropped, facing a card index drawer pulled "
               "right out and packed tight with old paper customer job cards, one low lamp and "
               "the workshop dark behind him",
        after="standing upright beside the same desk facing the camera, the card index drawer "
              "closed and a single tablet on the desk, daylight through the open workshop roller "
              "door filling the office"),
    "professional-services": dict(
        subject="an Australian accounting firm principal in his fifties wearing a light blue shirt "
                "and no jacket, in a firm office with a boardroom table visible through the door "
                "behind him",
        before="head in both hands at the desk over a printed timesheet marked up heavily in red "
               "pen, stacks of client files piled either side of it, one desk lamp and the rest "
               "of the room dark",
        after="sitting upright at the same desk facing the camera with one timesheet squared in "
              "front of him and the desk otherwise clear, daylight through the office window "
              "filling the room"),
}

# ---------------------------------------------------------------------------------------------
# F-M3. The editorial coverage photo. The industry's own landscape, busy and working, because an
# article photo shows the industry rather than one owner's bad day. People are wanted here, which
# is the opposite of the caution plates below.
COVERAGE = {
    "construction": "An Australian residential construction site in the middle of a working day, "
                    "a timber frame going up on a concrete slab with scaffolding up one side, two "
                    "workers in hi-vis moving materials across the slab",
    "real-estate": "An open-home auction on the front lawn of an Australian suburban house, a "
                   "crowd of about thirty people standing on the grass and the footpath facing an "
                   "auctioneer who stands on the front steps",
    "hospitality": "The dining room of a busy Australian pub at full service, every table taken, "
                   "staff moving between them carrying plates, the bar crowded at the back of the "
                   "room",
    "retail": "The floor of a busy Australian retail shop mid-afternoon, customers moving along "
              "stocked shelving down both walls and a queue of three people at the service counter",
    "financial-services": "An open-plan Australian insurance brokerage mid-morning, brokers at "
                          "their desks on the phone, a wall of lever-arch client files running "
                          "down one side of the room",
    "building-services": "An Australian tradesman's service van parked in a suburban driveway with "
                         "its side door slid open and tools racked inside, a technician carrying a "
                         "toolbag toward the front door of the house",
    "professional-services": "A boardroom in an Australian accounting firm mid-meeting, four "
                             "people seated around a long table with laptops and printed document "
                             "packs open in front of them",
}

# ---------------------------------------------------------------------------------------------
# F-M4. The filmed billboard.
#
# the operator, 2026-08-06, third and final call on this format:
#
#   1. **The pop-art comic is scrapped.** Parked in `plates-magnet/<industry>/_versions/`.
#   2. **Zoom in.** The billboard fills the frame. The first pass framed the whole roadside and
#      the board was a third of the card.
#   3. **The copy is NATIVE to the prompt, not composited.** A blank face with the type mapped on
#      by homography was built and rejected: it read as a mock-up rather than a photograph of a
#      real board. The exact lines are quoted into the prompt and the model sets them.
#   4. **Canonical VHS**, the `vhs-camcorder` style off the F8 bank, shot as if on a camcorder.
#
# That reverses the house rule that this model cannot set legible type. It can when the copy is
# short, in caps, and quoted line by line. **Check every returned plate letter by letter before
# grading** and re-roll rather than accepting a typo: a misspelt billboard is the whole card.
BILLBOARD = {
    "construction": "an Australian outer-suburban arterial road, a housing estate under "
                    "construction blurred behind it with timber frames and a crane on the skyline",
    "real-estate": "a leafy Australian suburban shopping strip, brick and weatherboard houses "
                   "blurred behind it",
    "hospitality": "an Australian city corner, the brick upper wall of a pub and a bus stop "
                   "blurred behind it in late afternoon light",
    "retail": "the car park of an Australian suburban shopping centre, trolley bays and the "
              "centre awning blurred behind it",
    "financial-services": "an Australian city street, glass office towers and a tram wire "
                          "blurred behind it",
    "building-services": "an Australian light-industrial service road, roller-door workshops and "
                         "parked trade vans blurred behind it",
    "professional-services": "an Australian city-fringe street, awnings and low-rise office "
                             "frontages blurred behind it",
}


# The look, the operator 2026-08-06 (fourth pass). NOT the F8 `vhs-camcorder` style: the tape grade came
# off this format. A clean modern phone photo, pulled further back so the board sits in the middle
# distance, with the photographer's own left hand reaching in to point at it.
BILLBOARD_HEAD = "A vertical photograph in portrait orientation."
BILLBOARD_BODY = ("shot handheld in clear natural daylight with ordinary snapshot colour, "
                  "sharp and clean, standing back across the road so the whole billboard sits in "
                  "the middle distance with the street, the verge and open sky around it")
# The arm has to read as the VIEWER'S OWN, not a bystander's. Entering from the left edge at
# billboard height reads as a second person standing off to the side, which is exactly what the
# first pass returned. It has to come up out of the BOTTOM-LEFT CORNER, close to the lens and
# steeply foreshortened, the way your own arm looks when you point at something you are filming.
# the operator, 2026-08-06: the arm is the LEFT hand of the person holding the phone behind the camera,
# and it must be BLURRED, not high res. Several rolls came back with a sharp, detailed forearm
# that read as the subject of the photo rather than as the viewer's own hand in the foreground.
BILLBOARD_HANDS = ("One bare human arm reaches into the frame from the LEFT EDGE, about halfway "
                   "up, extending sideways and forward toward the billboard with the index "
                   "finger pointing at it. It is the LEFT arm of the person taking this photo, "
                   "who is holding the camera in their other hand just behind the lens, so the "
                   "arm is seen along its length and foreshortened. It is far too close to the "
                   "lens to be in focus: render it STRONGLY out of focus and soft, low in detail, "
                   "with no sharp skin texture, no visible hairs and no crisp edges, reading as a "
                   "blurred foreground shape while the billboard behind it stays perfectly sharp. "
                   "Only that one forearm and hand are visible. No shoulder, no body, no face, no "
                   "second arm and no other person anywhere in the frame.")
BILLBOARD_TAIL = ("This image IS the photograph the phone took. Do not show a phone, a phone "
                  "screen, a camera, a camera interface, shutter buttons, app icons or any "
                  "device anywhere in the frame, and do not put the scene inside a screen or a "
                  "second frame. Clean modern phone photography, not film, not tape, no grain, "
                  "no vignette, no retro treatment of any kind. Full-bleed frame, no border, no "
                  "letterboxing, no frame within the frame. No timestamp, no watermark, no "
                  "overlay graphics. No other signage, lettering or logos anywhere else in the "
                  "frame.")


def billboard_prompt(key):
    """Compose the F-M4 prompt with the copy quoted line by line.

    Three things here are the operator's calls and each one reverses an earlier pass:

      - **No VHS.** The tape grade came off this format on the fourth pass. `grade` is `none`.
      - **Further back**, so the board is in the middle distance rather than filling the frame.
      - **The type is thin your display typeface**, the house display weight, not the heavy sans the first
        generated pass used.

    A thin face on a board in the middle distance is the hardest ask yet for the model's
    spelling. Check every returned plate letter by letter before it is used and re-roll on a
    typo: a misspelt billboard is the whole card.
    """
    from magnet_copy import COPY, BY_KEY
    c = COPY["billboard"](BY_KEY[key])
    bullets = " ".join(f'"{b}"' for b in c["bullets"])
    return (
        f'{BILLBOARD_HEAD} Wide shot {BILLBOARD_BODY}. '
        f'A large roadside billboard standing above {BILLBOARD[key]}. {BILLBOARD_HANDS} '
        f'The billboard is printed with this exact wording, and every word is spelled exactly '
        f'as written here, set in a very thin, light-weight geometric sans-serif with wide round '
        f'letterforms, in dark charcoal on a plain off-white background. '
        f'Across the top, one headline line: "{c["head"]}". '
        f'Below it, three lines each starting with a round bullet point: {bullets}. '
        f'At the bottom, centred inside a thin rounded-rectangle outline drawn as a pill '
        f'shape: {c["box"]}. Write those words exactly, with no square brackets, no '
        f'quotation marks and no other punctuation around them. '
        f'The type is large, evenly set, correctly spelled and clearly legible from across the '
        f'road, filling the board with a generous margin around it. Nothing else is printed on '
        f'the billboard: no logo, no picture, no web address, no extra words. {BILLBOARD_TAIL}'
    )


# ---------------------------------------------------------------------------------------------
# F-M5. The two caution plates. Five industries already have a graded VHS plate on disk; these
# two do not. Same no-people law as the existing 25, because an empty room reads as the pain and
# a person in frame reads as a stock photo.
CAUTION_PLATES = {
    "building-services": dict(
        shot="Medium-wide shot",
        brief="A small trade workshop office at the end of the day, the chair pushed back and "
              "empty, one closed laptop on the desk, a card index drawer of old paper customer job "
              "cards pulled open beside it and a rack of van keys hanging on the wall"),
    "professional-services": dict(
        shot="Medium shot",
        brief="An accounting firm office at the end of the day, the chair empty, one closed laptop "
              "on the desk, a squared stack of client files beside it and a long boardroom table "
              "visible through the open door behind"),
}


# ---------------------------------------------------------------------------------------------
# REFINES. An i2i pass off a plate already on disk, never a fresh roll, so the frame that was
# approved survives and only the named thing changes. Same rule as `plates_real.REFINES`.
#
# Empty for now. The comic's two refines (photograph the page, then pull back to a first-person
# POV) went with the comic when the operator scrapped it on 2026-08-06; both are in git history if the
# technique is ever wanted again. The billboard needs none: its face is blank on purpose and the
# copy is composited.
REFINE = {
    # the operator, 2026-08-06: the model branded the van "ACME PLUMBING & ELECTRICAL". The style tail
    # bans lettering and it wrote it anyway, which is the same trap the news-collage plates hit.
    # Refined off the approved frame so only the paintwork changes.
    ("editorial", "coverage"): (
        "Keep this exact photograph, its framing, its scenery, its lighting and its grade "
        "completely unchanged. Remove every word, letter, logo, phone number and marking from "
        "the van so it is a plain unmarked white work van with no signwriting of any kind on any "
        "panel or door. Remove any lettering from the worker's clothing as well. Change nothing "
        "else in the image."),
    # the operator, 2026-08-06, final note on F-M4. The pulled-back first-person re-shoot changed the
    # scenery, and he prefers the earlier scene, so this runs i2i off the plate already on disk:
    # the road, the verge, the board and its copy all survive, and only the pointing hand is
    # restated. A fresh roll would move the scene again, which is the whole thing being avoided.
    ("billboard", "plate"): lambda key: billboard_cta_refine(key),
    # arm only, for a plate whose board is already correct. Selected with --arm.
    #
    # TWO references go with this one: the plate being fixed FIRST, the construction plate SECOND.
    # Words alone could not hold the arm still. Three industries came back with it sharp, upright
    # or swung across the frame, so the second reference carries the arm itself and the prompt
    # only has to say which picture each thing comes from. the operator, 2026-08-07: "adapt the exact one
    # you use for the construction one and stitch it onto that."
    ("billboard", "arm"): lambda key: (
        "You are given two photographs. The FIRST is the photograph being edited. The SECOND is a "
        "reference, used ONLY for the blurred arm in its lower left corner.\n\n"
        "Return the FIRST photograph completely unchanged: the same framing, the same scenery, "
        "the same sky, the same lighting and grade, the same billboard in the same place, and "
        "every single word printed on the board exactly as it is printed, letter for letter.\n\n"
        "Change one thing. Delete the arm currently in the first photograph, filling the space it "
        "occupied with the scenery that belongs behind it. Then reproduce the arm from the SECOND "
        "photograph in its place: the same pose, the same angle across the frame, the same entry "
        "point at the lower left corner, the same size relative to the frame, and above all the "
        "same heavy defocus, so it is a soft foreground shape with indistinct melting edges while "
        "the billboard stays perfectly sharp. Match its brightness and colour to the light in the "
        "first photograph. Nothing else from the second photograph appears: not its road, not its "
        "sky, not its buildings, not its billboard. Only the arm."),
}

# THE HOUSE ARM. the operator, 2026-08-07: the construction plate's arm is the one, and all seven carry
# it, so the format reads as one campaign shot by one person rather than seven separate photos.
# The seven approved frames each came back with their own arm (upright, raised, wristwatch, from
# the bottom edge), so this rides along with the CTA swap and both change in a single paid pass.
#
# Written WITHOUT the phone clause the earlier version carried. That clause contradicted this
# rig's most expensive trap: naming a phone, a camera or the photographer's other hand made the
# model draw an iPhone with full camera UI, then a second arm holding a handset. Two rolls burned.
# The geometry below pins the same arm without naming any of the three, and bans the wristwatch
# that came back on the real estate plate.
#
# First pass at this was too polite and the model ignored both halves of it: real estate came back
# with a sharp, upright, raised arm. Rewritten to lead with the defocus, to state the angle as a
# fact three ways, and to name the failure it must not repeat. the operator, 2026-08-07.
BILLBOARD_ARM = (
    "Replace the foreground arm completely. The new arm is a single bare left forearm and hand, "
    "held right up against the lens and therefore FAR OUT OF FOCUS: it is a soft blurred "
    "foreground shape with indistinct, melting edges, blurred so heavily that no skin texture, "
    "no knuckle and no fingernail can be resolved, while the billboard behind it stays perfectly "
    "sharp. It enters at the LEFT EDGE of the frame around the middle of the picture and runs "
    "ACROSS the frame to the right, lying almost flat and level. It is foreshortened, seen end-on "
    "along its length, with the index finger extended toward the billboard. It is NOT raised, NOT "
    "vertical, NOT angled up from the bottom of the frame, and NOT sharp. Only the forearm and "
    "hand appear: no shoulder, no body, no second person, no wristwatch, no sleeve or cuff, no "
    "second hand, and nothing held in it.")


def billboard_cta_refine(key):
    """Swap the line inside the button on the board, and nothing else.

    Why this exists, the operator 2026-08-07: the program-wide rename to "The [Industry] AI Audit" was
    shot as a fresh roll per industry, which moved the scene, tightened the crop and put a heavy
    dark frame round the board. He rejected all seven. The approved frames were restored off
    `_versions/billboard-oldname-20260806/`, so the only thing left wrong on them is the name
    printed on the board, and that is an i2i job off the plate itself.

    Two industries need more than the button:

      - **building services** is now "trades" in every word said out loud, so its headline moves
        too. Two changes in one pass rather than two paid passes.
      - **hospitality** already carries the new name, but the model wrapped it in square brackets
        and dropped the outline, which is the punctuation trap this rig has hit twice. The generic
        wording below bans brackets and restates the outline, so it fixes itself.

    The trap that costs money here: never name a phone, a camera or the photographer's other hand.
    Two rolls were burned on it. This prompt names neither, and the arm is only ever "unchanged".
    """
    from magnet_copy import COPY, BY_KEY
    c = COPY["billboard"](BY_KEY[key])
    head = ""
    if key == "building-services":
        head = (f'Also change the headline at the top of the board so it reads exactly '
                f'"{c["head"]}", set in the same capitals, weight, size and position as the '
                f'headline it replaces. ')
    return (
        "Keep this exact photograph completely unchanged: the same framing, the same scenery, "
        "the same sky, the same lighting and grade, and the same billboard in the same position "
        "at the same angle. Keep every bullet line on the board exactly as it is printed. "
        f"{head}"
        "Change the short line at the bottom of the board so it reads exactly "
        f'"{c["box"]}", spelled exactly that way and nothing else. Set it in the same thin '
        "sans-serif capitals, at the same size and in the same position as the line it replaces, "
        "centred inside a single thin rounded outline. Put no brackets, no quotation marks and no "
        f"punctuation of any kind around it. {BILLBOARD_ARM} Change nothing else in the image.")


def compose_vhs(shot, brief, people=True):
    """Same assembly as the F8 rig and `plates_real.compose`, so these sit in that universe
    exactly. `people=False` adds the explicit exclusion the caution plates carry."""
    s = STYLES["vhs-camcorder"]
    tail = "" if people else " " + NO_PEOPLE
    return "%s %s %s. %s.%s %s No text." % (s["head"], shot, s["body"], brief.rstrip("."),
                                            tail, s["tail"])


def compose_billboard(shot, scene):
    return "%s %s %s. %s. %s" % (BILLBOARD_HEAD, shot, BILLBOARD_BODY, scene.rstrip("."),
                                 BILLBOARD_TAIL)


def jobs(keys=None, only_fmt=None):
    """Every paid job in the set, in build order: the free-gated formats' plates first."""
    out = []
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        k = i["key"]
        s = SPLIT[k]
        for half in ("before", "after"):
            brief = f"{s['subject']}, {s[half]}"
            if half == "before":
                brief += ". " + (FACE_HIDDEN_HER if s.get("she") else FACE_HIDDEN)
            out.append(dict(
                industry=k, fmt="split", role=half, aspect="4:5", grade="vhs",
                prompt=compose_vhs("Medium shot", brief)))
        out.append(dict(
            industry=k, fmt="editorial", role="coverage", aspect="3:2", grade="vhs",
            prompt=compose_vhs("Wide shot", COVERAGE[k])))
        out.append(dict(
            industry=k, fmt="billboard", role="plate", aspect="4:5", grade="none",
            prompt=billboard_prompt(k)))
        if k in CAUTION_PLATES:
            p = CAUTION_PLATES[k]
            out.append(dict(
                industry=k, fmt="caution", role="plate", aspect="5:4", grade="vhs",
                prompt=compose_vhs(p["shot"], p["brief"], people=False)))
    if only_fmt:
        out = [j for j in out if j["fmt"] == only_fmt]
    return out


def paths(job):
    d = OUT / job["industry"]
    stem = f"{job['fmt']}-{job['role']}"
    return d / f"{stem}.raw.png", d / f"{stem}.png"


def assert_same_subject(key):
    """The one check that protects the split screen. Both halves must carry the identical
    subject clause, character for character, or the two panels are two different people."""
    s = SPLIT[key]
    a = compose_vhs("Medium shot", f"{s['subject']}, {s['before']}")
    b = compose_vhs("Medium shot", f"{s['subject']}, {s['after']}")
    common = s["subject"]
    if common not in a or common not in b:
        raise SystemExit(f"FATAL: subject clause is not verbatim in both halves for {key}")
    return True


# Letterboxing is handled by HAND, in `build_split.CROP`, not by a detector here.
#
# An automatic trim was written and thrown away. The bands this model prints are sometimes near
# black and sometimes a blurred dark grey, so no single brightness threshold separates a band
# from a tenebrist BEFORE half: at the setting that removed the AFTER plate's bands it ate 645px
# of the BEFORE plate's dark room, and at the setting that spared the room it missed the bands
# entirely. Fourteen hand-set crop boxes, tuned once when each plate is shot, are exact, free
# and visible in the file. Same call the rig already makes for arrow targets and mark placement.


def grade(raw, dst, style):
    if style == "none":
        dst.write_bytes(raw.read_bytes())
        return
    subprocess.run(["bash", str(GRADE_SH), style, str(raw), str(dst)], check=True)


def dispatch(job, refine_from=None, also_ref=None):
    """ONE paid generation, downloaded before this function returns.

    `also_ref` is a SECOND image reference, passed after the plate being refined. The model takes
    `image_references` as an array (up to 14), so a refine can be shown both the frame it must
    keep and a frame it must copy one element out of. That is how the house arm gets onto a plate
    exactly rather than approximately: describing it in words moved it every time.
    """
    raw, dst = paths(job)
    raw.parent.mkdir(parents=True, exist_ok=True)
    cmd = [HF, "generate", "create", "nano_banana_pro", "--prompt", job["prompt"],
           "--aspect_ratio", job["aspect"], "--resolution", "2k", "--wait", "--json"]
    if refine_from:
        cmd += ["--image-references", str(Path(refine_from).resolve())]
    if also_ref:
        cmd += ["--image-references", str(Path(also_ref).resolve())]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "[" not in r.stdout:
        raise SystemExit(f"generation failed:\n{r.stderr[-800:]}")
    url = json.loads(r.stdout[r.stdout.index("["):])[0]["result_url"]
    urllib.request.urlretrieve(url, raw)
    grade(raw, dst, job["grade"])
    print(f"  shot -> {dst}")
    return dst


def main():
    argv = sys.argv[1:]
    flags = [a for a in argv if a.startswith("--")]
    args = [a for a in argv if not a.startswith("--")]
    only_fmt = None
    if "--fmt" in argv:
        only_fmt = argv[argv.index("--fmt") + 1]
        args = [a for a in args if a != only_fmt]

    keys = [a for a in args if a in BY_KEY] or None
    picked = [a for a in args if a not in BY_KEY]
    js = jobs(keys, only_fmt)
    # Each named term NARROWS the selection. `construction split before` has to mean one job,
    # not two: an OR here matched both halves of the split and tripped the one-job guard.
    for term in picked:
        js = [j for j in js if term in (j["fmt"], j["role"])]

    if "--regrade" in flags:
        for j in js:
            raw, dst = paths(j)
            if raw.exists():
                grade(raw, dst, j["grade"])
                print(f"  regraded {dst}")
        return

    if "--refine" in flags:
        if len(js) != 1:
            raise SystemExit(f"--refine takes exactly ONE job, {len(js)} selected.")
        j = js[0]
        # --arm re-states the house arm on a plate whose board is already right, so a billboard
        # that only missed the arm does not pay to have its copy re-set as well.
        role = "arm" if "--arm" in flags else j["role"]
        prompt = REFINE.get((j["fmt"], role))
        if callable(prompt):          # per-industry refines, e.g. the billboard CTA swap
            prompt = prompt(j["industry"])
        if not prompt:
            raise SystemExit(f"no refine written for {j['fmt']}/{j['role']}")
        raw, dst = paths(j)
        if not dst.exists():
            raise SystemExit(f"nothing to refine from: {dst} does not exist")
        print(f"\n{j['industry']} {j['fmt']}/{j['role']}  REFINE off {dst.name}\n\n{prompt}\n")
        if "--go" not in flags:
            print("DRY RUN, nothing spent. Add --go to shoot it.")
            return
        # keep the approved frame on disk before it is replaced
        vers = dst.parent / "_versions"
        vers.mkdir(exist_ok=True)
        for f in (raw, dst):
            if f.exists():
                (vers / f.name).write_bytes(f.read_bytes())
        # the arm refine is shown the construction plate as its second reference
        also = None
        if role == "arm" and j["industry"] != "construction":
            also = OUT / "construction" / "billboard-plate.png"
        dispatch({**j, "prompt": prompt}, refine_from=dst, also_ref=also)
        return

    if "--go" in flags:
        if len(js) != 1:
            raise SystemExit(f"--go takes exactly ONE job, {len(js)} selected. "
                             f"Never batch paid jobs.")
        j = js[0]
        if j["fmt"] == "split":
            assert_same_subject(j["industry"])
        print(f"\n{j['industry']} {j['fmt']}/{j['role']}  {j['aspect']}\n\n{j['prompt']}\n")
        dispatch(j)
        return

    for key in {j["industry"] for j in js}:
        assert_same_subject(key)
    for j in js:
        raw, dst = paths(j)
        state = "ON DISK" if dst.exists() else "not shot"
        print(f"\n{'=' * 92}\n{j['industry']}  {j['fmt']}/{j['role']}  "
              f"{j['aspect']}  grade={j['grade']}  [{state}]\n\n{j['prompt']}")
    print(f"\n\n{len(js)} paid jobs selected. DRY RUN, nothing spent. "
          f"Add --go with exactly one job to shoot it.")


if __name__ == "__main__":
    main()
