#!/usr/bin/env python3
"""Paid plates for the 20-format suite, format by format. DRY RUN by default, spends nothing.

    python3 plates_suite.py                              # every prompt in the set, free
    python3 plates_suite.py --fmt F1                     # one format across all seven
    python3 plates_suite.py F1 construction              # one prompt
    python3 plates_suite.py F1 construction --go         # shoot ONE job
    python3 plates_suite.py F1 construction --regrade    # re-grade from raw, free
    python3 plates_suite.py --refine F1 construction --go # i2i fix, keeps the frame

**One paid job at a time.** `--go` refuses to run unless exactly one job is selected. Review the
returned still before the next is sent. your standing rule and this rig will not override it.

## F1, the band The band format keeps its type exactly as it is and gains a full-bleed plate behind it.
Four calls, all his:

  - **Full-bleed behind type**, not a top-half inset and not a hard black band.
  - **VHS camcorder documentary**, the `vhs-camcorder` style off the F8 bank, graded free by
    `grade_plate.sh vhs`. Same universe as the news collage and the lead-magnet plates.
  - **The work happening.** People visible doing the trade, so the industry is legible at
    thumbnail size. Not the admin side and not an empty room.
  - **Bottom-up fade** to black under the type, which is the treatment the news band already
    uses. That is a free compositor pass, not part of the plate.

Because the fade eats the lower third, every prompt composes the work into the **upper two
thirds** and leaves plain ground, floor or bench below it. A plate whose subject sits low loses
its head to the gradient.

Two traps inherited from `plates_magnet.py`, both already paid for:

  - **This model writes legible signage onto anything in shot**, and it has signwritten a work
    van unprompted. The `No text.` tail is not optional and `NO_BRANDING` restates it for the
    surfaces these scenes actually contain.
  - **The tail's own no-timestamp clause is load bearing.** The camcorder style bakes a date
    stamp into the corner without it.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from suite_copy import INDUSTRIES, BY_KEY  # noqa: E402

VAULT = ROOT.parents[5]
F8 = (VAULT / "the business" / "projects" / "content-engine" / "ideas"
      / "industry-build-carousels")
STYLES = json.loads((F8 / "styles.json").read_text())["styles"]
GRADE_SH = F8 / "grade_plate.sh"
OUT = ROOT / "plates-suite"
HF = "/opt/homebrew/bin/your generation platform"

# The type sits in the lower third over a fade to black, so the plate has to leave that space
# quiet. Getting there is a CAMERA instruction, not a layout instruction, and the difference has
# cost three paid jobs.
#
# Pass 1 asked for "the lower third of the frame" to be plain. The model read that as an
# instruction to DIVIDE the picture: trades and professional services both came back as a scene
# in a hard-edged box across the top with a separate blurred floor pasted underneath, seam and
# all. Pass 2 restated it as one continuous photograph and banned the seam, the band, the panel,
# the inset and the border by name, and also banned the date stamp by name after retail returned
# one. It came back with the seam still there AND a stamp reading 03/12/98 14:30, which is the
# oldest trap in this house: naming a thing to forbid it is one more mention of it.
#
# Pass 3 says nothing about the frame at all. A low camera puts floor in the near foreground on
# its own, and the quiet band the type needs falls out of the lens rather than out of a rule.
LOWER_THIRD = ("The camera is held low, near waist height, so the floor or ground runs away "
               "from the lens across the whole near foreground and the people and their work "
               "sit further back and higher up in the frame.")

# The van that came back signwritten "ACME PLUMBING & ELECTRICAL" cost a refine on the magnet
# rig. Every surface these scenes contain gets named here rather than trusting the style tail.
NO_BRANDING = ("Every surface in the scene is blank and unbranded: no signage, no shopfront "
               "name, no menu board, no printed forms, no screen with anything readable on it, "
               "no logo, no lettering on any vehicle, garment, box or wall anywhere in frame.")

# ---------------------------------------------------------------------------------------------
# F1. The industry's own work, mid-job, with people in it.
#
# Deliberately NOT the magnet rig's editorial-coverage scenes. Those are wide 3:2 article photos
# shot to sit inside a news layout. These are 4:5 native, framed close enough that the trade is
# unmistakable at thumbnail size, and weighted high for the fade.
F1_SCENES = {
    "construction": dict(
        shot="Medium-wide shot",
        brief="An Australian residential construction site in the middle of a working day, two "
              "carpenters in plain hi-vis fixing a timber wall frame upright on a concrete slab, "
              "scaffolding and a part-framed second storey above them, the bare slab and cut "
              "offcuts running toward the camera"),
    "real-estate": dict(
        shot="Medium-wide shot",
        brief="An open home at an Australian brick suburban house, a real estate agent in a "
              "charcoal blazer standing at the open front door talking to a couple on the "
              "threshold while more buyers come up the front path behind them, the lawn and "
              "driveway running toward the camera"),
    "hospitality": dict(
        shot="Medium shot",
        brief="The pass of an Australian pub kitchen at full service, two chefs in plain black "
              "aprons plating up under the heat lamps while a floor staff member lifts plates "
              "away, steam and movement behind them, the stainless bench running toward the "
              "camera"),
    "retail": dict(
        shot="Medium shot",
        brief="The floor of a busy Australian retail shop mid-afternoon, the shop owner in a "
              "plain dark polo shirt restocking a shelf while two customers browse the aisle "
              "behind her, stocked shelving down both walls, the polished floor running toward "
              "the camera"),
    "financial-services": dict(
        shot="Medium shot",
        brief="An open-plan Australian insurance brokerage mid-morning, three brokers at their "
              "desks on headsets with paper client files open in front of them, a wall of "
              "lever-arch files running down one side of the room, the nearest empty desk "
              "running toward the camera"),
    # Rewritten after three rolls. The original brief put the scene in a laundry with
    # a second tradesperson "through the doorway behind him", and every roll framed the whole
    # photograph inside a doorway: first as a hard seam with a pasted floor, then as a soft inset
    # with a blurred surround. Naming a doorway in an interior is what built the frame. This one
    # is outdoors with no aperture in it at all.
    "building-services": dict(
        shot="Medium shot",
        brief="An Australian plumbing and electrical tradesman in a plain navy work polo "
              "kneeling on a suburban driveway beside his open service van, tool racks and "
              "shelving visible inside the van, lengths of copper pipe and fittings laid out on "
              "the concrete beside him, a second tradesperson lifting a toolbag out of the back "
              "of the van, the driveway running toward the camera"),
    # Same fix as trades, same cause. The original brief put "a glass partition and the rest of
    # the firm visible behind" in shot, and the model built the whole photograph inside that
    # aperture: an inset picture with a hard horizontal edge that sliced the first line of copy
    # in half. Any opening named in the brief becomes the frame. This one has no aperture.
    "professional-services": dict(
        shot="Medium shot",
        brief="A meeting in an Australian accounting firm, a principal in a light blue shirt "
              "talking across a long table to two clients, printed document packs and open "
              "laptops between them, shelves of client files along the wall behind them, the "
              "near end of the table running toward the camera"),
}

# ---------------------------------------------------------------------------------------------
# F3, the question hook. you, card by card.
#
# F1 is one scene rewritten seven ways. F3 is the opposite: seven different ideas answering the
# same question, so every card carries its own medium, its own aspect and in two cases its own
# geometry. A scene may therefore override `style`, `grade` and `aspect`, and may supply a
# finished `prompt` instead of a `brief` when the style bank does not describe its look.
#
# Not written yet: trades and professional services. you: "then we'll work on the rest after."

# The noir blocks, lifted verbatim from formats/noir-painterly/SKILL.md phase 2. A style LOCK
# outranks this rig, so they are copied rather than paraphrased. No 4:5 tail exists in that skill
# (it ships 16:9 and 9:16), so the vertical tail is adapted from the 9:16 one: the subject is held
# off dead centre and the lower frame stays dark, which is also what the band needs.
NOIR_STYLE = ("A moody black-and-white oil painting in high-contrast film-noir style, thick "
              "visible brushstrokes, painterly chiaroscuro, hand-painted animation still, not a "
              "photograph. Any human figure is a neutral faceless silhouette with no face, no "
              "hat, no gender cues.")
NOIR_LIGHT = ("A single hard key light rakes from high on one side, catching the one glowing "
              "white element and the edges of the objects around it with brilliant specular "
              "highlights while the rest falls into deep crushed black. Inky tenebrist shadows, "
              "luminous white to solid black, thick oil-paint texture, vintage noir cinema mood. "
              "The subject is held above the centre of the frame with the lower frame kept dark "
              "and empty, tall vertical composition.")

# The noir blocks describe a painting, and the model duly painted one ON A PAGE: the first retail
# roll came back as a canvas with white paper margin on all four sides. The F8 style bank carries
# a bleed clause of its own and the noir blocks do not, so it is added here.
NOIR_BLEED = ("The painting fills the entire image from edge to edge with no border, no margin, "
              "no canvas edge, no frame and no white paper anywhere around it.")

F3_SCENES = {
    # The Matrix offer, reshot rather than copied. Hands and forearms only, so no face question
    # arises and nothing identifies a person. The blue pill is the role and the red is carrying
    # on alone, and that reading is carried by light and framing, never by lettering.
    "construction": dict(
        shot="Extreme close-up",
        # you, : light on the second hand too. The first roll left the whole right
        # side of the frame in shadow, so the offer read as one pill rather than a choice. Both
        # hands are now lit and the blue keeps its edge by being the brighter of the two.
        brief="Two open human palms held out toward the lens in a dim room, one pill resting in "
              "each palm. BOTH hands and both palms are clearly lit and fully visible, each "
              "catching its own light so neither is lost in shadow. The pill in the left palm is "
              "a deep electric blue and is the brightest thing in the picture, catching a hard "
              "specular highlight. The pill in the right palm is dull red, lit more softly but "
              "still plainly visible on a lit palm. Only the two forearms and hands are in the "
              "frame, cropped at the elbow, with no shoulders, no body, no face and no second "
              "person. Behind the hands the room falls away into darkness with a construction "
              "site visible far back through a window, out of focus"),

    # The billboard, on the F3 VHS look rather than the magnet rig's clean phone photo. The copy
    # is set NATIVELY by the model, quoted line by line, which `plates_magnet.py` proved this
    # model can do when the lines are short. Check every returned plate letter by letter.
    "real-estate": dict(
        shot="Medium-wide shot",
        aspect="4:5",
        # you, : "the text isn't actually properly on the billboard." The first roll
        # set the two lines small, flat and low on a mostly empty board, so they read as an
        # overlay floating in front of it rather than as ink printed on a surface photographed at
        # an angle. The fix is to state the printing as a physical fact: the type is ON the vinyl,
        # it follows the same perspective as the board, it fills the board, and it carries the
        # same light and softness as the rest of the photograph.
        brief="A large roadside billboard filling most of the frame, standing above a leafy "
              "Australian suburban shopping strip with brick and weatherboard houses blurred "
              "behind it. The billboard face is seen slightly from one side, so it recedes in "
              "perspective. Two lines of large dark charcoal type are PRINTED ONTO the off-white "
              "vinyl of that board, part of the board itself: the lettering lies flat on the "
              "surface, recedes in exactly the same perspective as the board, is lit by the same "
              "daylight and carries the same softness and texture as the rest of the photograph. "
              "The two lines are centred on the board and are large enough to fill it almost edge "
              "to edge with only a small even margin around them, set in a thin light-weight "
              "geometric sans-serif with wide round letterforms. The wording is exactly this, "
              "spelled exactly as written: \"COULD YOU TAKE TWO WEEKS OFF RIGHT NOW\" on the "
              "first line, \"WITHOUT YOUR REAL ESTATE AGENCY FALLING OVER?\" on the second line. "
              "Nothing else is printed on the billboard: no logo, no picture, no web address, no "
              "extra words"),

    # Two mediums in one frame, the same move the watercolour window already makes: the fingers
    # are a Renaissance fresco and the man wedged between them is the house noir oil figure.
    # Ultra close on the gap, which is where the whole idea lives.
    "hospitality": dict(
        shot="Extreme close-up",
        aspect="4:5",
        grade="none",          # a fresco does not take a tape grade, and neither does the noir
        prompt=(
            "An extreme close-up of two outstretched index fingers reaching toward each other "
            "from opposite sides of the frame, almost touching, filling the picture. The two "
            "hands and fingers are painted as a Renaissance fresco: warm Italian oil and plaster, "
            "soft modelled flesh tones, cracked and aged plaster surface, faded pigment, the "
            "surface of a very old ceiling painting. "
            "In the narrow gap between the two fingertips stands one small human figure, braced "
            "sideways with both arms extended, one palm pushing hard against each fingertip, "
            "holding them apart, knees bent and body straining under the pressure. That figure "
            "alone is painted in a completely different medium: a black-and-white oil painting in "
            "high-contrast film-noir style, thick visible brushstrokes, painterly chiaroscuro, "
            "and he is a neutral faceless silhouette with no face, no hat and no gender cues. "
            "The clash between the warm cracked fresco and the black noir figure is deliberate "
            "and both are fully rendered. "
            "The fingers and the gap are held in the upper two thirds of the tall frame. "
            "No text, no lettering, no numerals and no writing anywhere in the image.")),

    # The corner office, straight VHS. Camera sits ON the desk looking up at him, which is the
    # vlog framing you asked for, and the warm 70s grade rides on top of the tape look.
    "financial-services": dict(
        shot="Low-angle medium shot from desk height",
        brief="An Australian insurance broker in his forties in a well-cut mid-century suit with "
              "a narrow tie, sitting at a large desk in a high corner office, writing on a pad of "
              "paper with a fountain pen, head down and absorbed in the work. The camera sits on "
              "the desk itself, low and close, looking up and across at him past the edge of the "
              "pad, so the near desk surface is a soft blurred foreground and he is the one thing "
              "in focus. Behind him a wall of window looks out over Sydney Harbour with the "
              "Harbour Bridge clearly visible, blown out and hazy in warm afternoon light. Warm "
              "amber vintage nineteen-seventies colour, soft haze, deep shadows in the corners of "
              "the room"),

    # The burden, in the locked house painting style. `prompt` rather than `brief` because the
    # noir style is its own block system and does not come out of the F8 style bank.
    "retail": dict(
        aspect="4:5",
        grade="none",
        # First roll was unreadable: the boulder did not separate from the background and the
        # light block's "one glowing white element" became a glowing orb where the head should
        # be. The pose is now described as a silhouette seen side on, and the glowing element is
        # named so the model stops choosing one.
        prompt=(
            NOIR_STYLE + " "
            "The figure is seen in full from the side, in clear profile against an empty pale "
            "background, so his whole silhouette reads at a glance. He walks from right to left, "
            "bent almost double under one single enormous jagged boulder that rests across his "
            "shoulders and upper back. Both of his arms are hooked backward over the boulder to "
            "hold it in place, the way a man carries a cross. His back is almost horizontal, his "
            "head hangs down toward the ground, his knees are bucyour video modeland one leg drags behind "
            "him. The boulder is a single solid mass several times the size of his whole body and "
            "is unmistakably a heavy rock. There is nothing else in the picture: no other figure, "
            "no buildings, no landscape, only bare ground under his feet. "
            + NOIR_LIGHT.replace("the one glowing white element",
                                 "the top edge of the boulder") + " "
            + NOIR_BLEED + " No text, no lettering and no writing anywhere in the image.")),

    # you, : "the ute at 9pm". Straight VHS, the same universe as F1, and the only
    # card in F3 that answers the question with the man himself rather than with a metaphor.
    #
    # It overrides both house clauses because both were written for a room. `LOWER_THIRD` puts the
    # camera at waist height with floor running away from the lens, which inside a cab would be a
    # footwell, and `NO_BRANDING` forbids a lit screen outright, which is the light source here.
    # The replacements keep what each clause is for: a quiet dark lower frame, and no invented
    # lettering anywhere.
    #
    # Nothing outside the cab is described. The trap that cost five paid jobs is that any aperture
    # named in a brief becomes the frame, and a windscreen is an aperture.
    "building-services": dict(
        shot="Medium close shot from the passenger seat",
        lower=("The camera is close and a little low, so the man and the phone sit above the "
               "centre of the tall frame and the dark of the cab fills the near foreground below "
               "them."),
        branding=("Every surface in the cab is blank and unbranded: no lettering on his shirt, no "
                  "printed forms, no logo on any object, and the phone screen is a plain bright "
                  "glow with nothing readable on it."),
        brief="An Australian tradesman in a plain navy work polo sitting in the driver's seat of "
              "his work ute late at night, still belted in, both hands resting on the bottom of "
              "the steering wheel and his head tipped back against the headrest, plainly tired. A "
              "mobile phone lies face up on the dashboard beside him with its screen glowing "
              "bright white, and that glow is the only real light in the picture, lifting one "
              "side of his face, the top of the wheel and the edge of the dashboard out of the "
              "dark. A clipboard, a few loose hand tools and a takeaway coffee cup sit on the "
              "seat beside him. Everything further back inside the cab falls away into darkness"),

    # you, : "marble atlas, cracked". A finished prompt because museum sculpture was
    # not in the F8 style bank when this was shot, and `grade="none"` because polished marble does
    # not take a tape grade any more than the fresco did.
    #
    # you locked the look the moment he saw it, so it is now `marble-monument` in the bank
    # (`industry-build-carousels/styles.json`) and any format after this one casts it from there
    # rather than copying this prompt. This scene keeps its own wording so the approved plate
    # stays reproducible.
    #
    # It shares a thought with retail's noir burden and has to stay a different picture: white not
    # black, stone not paint, standing not walking, a carved building not a boulder, and the crack
    # is the whole point. The bleed and the dark lower frame are borrowed from the noir blocks
    # because both problems are the same ones (a painted margin, and type sitting over a busy
    # bottom edge).
    "professional-services": dict(
        aspect="4:5",
        grade="none",
        prompt=(
            "A single white marble sculpture standing in the middle of a dark museum gallery, "
            "photographed as a real carved object under museum lighting. The sculpture is a man "
            "in a modern business suit, the jacket, shirt and tie all carved in the same white "
            "marble, standing with his knees bent and his back straining as he holds an enormous "
            "carved stone cornice across his shoulders and raised forearms, the weight of a whole "
            "building pressing down on him. His head is bowed low between his arms so his face is "
            "turned toward the ground and lost in shadow. Fine hairline cracks run through the "
            "marble across both shoulders, down one forearm and through the plinth at his feet, "
            "with a little dust of broken stone scattered on the plinth. "
            "A single hard museum spotlight rakes across him from high on one side, so the "
            "polished marble catches brilliant white highlights along the cornice and his "
            "shoulders while the gallery around him falls away into deep empty black. He is held "
            "above the centre of the tall frame with the lower frame kept dark and empty. "
            + NOIR_BLEED.replace("The painting", "The photograph") + " "
            "No text, no lettering, no numerals and no writing anywhere in the image.")),
}

# ---------------------------------------------------------------------------------------------
# F4, "Don't hire this person". you, : the classifieds page, struck out.
#
# One scene seven ways, like F1, but on a different medium so the two never read as the same ad:
# a jobs page shot flat under a hard press flash. The role that gets struck is the hire the
# headline is arguing against, so it changes per industry and nothing else does.
#
# Three things this scene needs that the house clauses do not give it:
#
#   - It is a picture OF type, so `NO_BRANDING` cannot ban readable words outright. It is replaced
#     with a clause that allows exactly one legible thing and makes everything else unreadable,
#     which is the same move the `newsprint` style makes and the billboard proved.
#   - `LOWER_THIRD` is a camera instruction for a room. This is an overhead of a flat object.
#   - `press` grades the colour out twice, and the red ink is the entire idea. It shoots on the
#     new `press-ink` grade instead, which pulls saturation down rather than out.
#
# The trap to watch on every returned plate: this model writes its own headlines onto anything
# that looks like a page. Read each one letter by letter before it is composited.
F4_ROLES = {
    "construction": "PROJECT ADMINISTRATOR",
    "real-estate": "SALES ASSISTANT",
    "hospitality": "DUTY MANAGER",
    "retail": "OPERATIONS ASSISTANT",
    "financial-services": "CLIENT SERVICE OFFICER",
    "building-services": "SERVICE COORDINATOR",
    "professional-services": "PRACTICE ADMINISTRATOR",
}

# The first real estate roll pulled back far enough to show the whole sheet with desk on all four
# sides, so the ringed listing came back the size of a stamp and the paper read as an object in a
# frame rather than as the picture. "Fills the upper part of the frame" was not a distance, so the
# camera chose one. This says how close, and where the listing sits, in one clause.
F4_LOWER = ("The camera is close over the page so the newsprint fills the frame edge to edge, "
            "with only the near edge of the paper and the plain dark desk beneath it crossing the "
            "very bottom of the picture. The ringed listing sits above the middle of the tall "
            "frame and is large in the picture, easily read at a glance.")

# The financial services roll put a real brand in shot: the pen came back as a BIC with the name
# legible down the barrel. The clause covered the page and not the object lying on it, so the pen
# is now described as plain rather than left to the model.
F4_BRANDING = ("The only readable words anywhere in the picture are the ones named above. Every "
               "other line of type on the page is small, soft and impossible to read, and there "
               "is no masthead, no logo, no photograph and no illustration anywhere on the page. "
               "The pen is a plain unmarked ballpoint with a smooth blank barrel.")


def f4_page(role):
    return (
        "A colour photograph of a folded newspaper jobs page lying on a plain dark desk, shot "
        "from directly overhead with a hard direct on-camera flash. The page is dense grey "
        "newsprint: narrow columns of small type and a few small heavy headings, with visible "
        "halftone dot screen, paper fibre and a soft fold line across it. "
        # The trades roll came back ringed and NOT struck, which reads as "pick this one" and
        # argues the opposite of the headline. The X is now described as its own object sitting
        # on top of the ring rather than as a property of the ringing.
        "One single listing near the middle of the page has been ringed by hand in thick red "
        "ballpoint, and then crossed out: two long straight red lines are drawn hard across the "
        "listing corner to corner, crossing each other in one clear X that sits on top of the "
        "ring, the ink glossy and biting into the paper fibre. "
        "That one listing carries a heading in larger dark type, "
        "spelled exactly as written and nothing else: \"%s\". "
        "A red ballpoint pen lies on the paper beside it. "
        "The picture is almost colourless, grey paper and grey type under the flash, and the red "
        "ink and the red pen are the only colour anywhere in it. %s %s "
        "Push-processed film look, coarse grain, blown highlights, deep blacks. A photograph, not "
        "a rendering. Full-bleed frame, no border, no film edge, no sprocket holes, no "
        "letterboxing, no frame within the frame. Single clean exposure." % (
            role, F4_LOWER, F4_BRANDING))


F4_SCENES = {k: dict(prompt=f4_page(role)) for k, role in F4_ROLES.items()}

FORMATS = {
    "F1": dict(scenes=F1_SCENES, aspect="4:5", grade="vhs", style="vhs-camcorder"),
    # you, : "the VHS grain on these is too hard." F3 takes the soft tape grade.
    "F3": dict(scenes=F3_SCENES, aspect="4:5", grade="vhs-soft", style="vhs-camcorder"),
    "F4": dict(scenes=F4_SCENES, aspect="4:5", grade="press-ink", style="press-flash"),
}

# i2i fixes off a plate already on disk, never a fresh roll, so an approved frame survives and
# only the named thing changes. Written per format as its plates come back.
REFINE = {}


def compose(style, shot, brief, lower=None, branding=None):
    """Same assembly as the F8 rig and `plates_magnet.compose_vhs`, so these sit in that
    universe exactly, plus the two clauses this format needs.

    Both clauses were written for a scene in a room and a scene may replace either one when that
    is not where it is set. Replace, never drop: the quiet lower frame and the ban on invented
    lettering are what the band and the model respectively need."""
    s = STYLES[style]
    return "%s %s %s. %s. %s %s %s No text." % (s["head"], shot, s["body"], brief.rstrip("."),
                                                lower or LOWER_THIRD, branding or NO_BRANDING,
                                                s["tail"])


def jobs(fmts=None, keys=None):
    out = []
    for fmt, spec in FORMATS.items():
        if fmts and fmt not in fmts:
            continue
        for i in INDUSTRIES:
            k = i["key"]
            if keys and k not in keys:
                continue
            if k not in spec["scenes"]:
                continue
            sc = spec["scenes"][k]
            # A scene may override any of the format's defaults, and may hand over a finished
            # prompt when its look does not come out of the style bank at all (the noir painting,
            # the fresco). Everything else is composed the house way.
            prompt = sc.get("prompt") or compose(
                sc.get("style", spec["style"]), sc["shot"], sc["brief"],
                sc.get("lower"), sc.get("branding"))
            out.append(dict(fmt=fmt, industry=k,
                            aspect=sc.get("aspect", spec["aspect"]),
                            grade=sc.get("grade", spec["grade"]),
                            prompt=prompt))
    return out


def paths(job):
    d = OUT / job["fmt"]
    return d / f"{job['industry']}.raw.png", d / f"{job['industry']}.png"


def grade(raw, dst, style):
    if style == "none":
        dst.write_bytes(raw.read_bytes())
        return
    subprocess.run(["bash", str(GRADE_SH), style, str(raw), str(dst)], check=True)


def dispatch(job, refine_from=None):
    """ONE paid generation, downloaded before this function returns."""
    raw, dst = paths(job)
    raw.parent.mkdir(parents=True, exist_ok=True)
    cmd = [HF, "generate", "create", "your image model", "--prompt", job["prompt"],
           "--aspect_ratio", job["aspect"], "--resolution", "2k", "--wait", "--json"]
    if refine_from:
        cmd += ["--image-references", str(Path(refine_from).resolve())]
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
    if "--fmt" in argv:
        args.append(argv[argv.index("--fmt") + 1])

    fmts = [a for a in args if a in FORMATS] or None
    keys = [a for a in args if a in BY_KEY] or None
    js = jobs(fmts, keys)

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
        prompt = REFINE.get((j["fmt"], j["industry"]))
        if not prompt:
            raise SystemExit(f"no refine written for {j['fmt']}/{j['industry']}")
        raw, dst = paths(j)
        if not dst.exists():
            raise SystemExit(f"nothing to refine from: {dst} does not exist")
        print(f"\n{j['fmt']} {j['industry']}  REFINE off {dst.name}\n\n{prompt}\n")
        if "--go" not in flags:
            print("DRY RUN, nothing spent. Add --go to shoot it.")
            return
        vers = dst.parent / "_versions"
        vers.mkdir(exist_ok=True)
        for f in (raw, dst):
            if f.exists():
                (vers / f.name).write_bytes(f.read_bytes())
        dispatch({**j, "prompt": prompt}, refine_from=dst)
        return

    if "--go" in flags:
        if len(js) != 1:
            raise SystemExit(f"--go takes exactly ONE job, {len(js)} selected. "
                             f"Never batch paid jobs.")
        j = js[0]
        print(f"\n{j['fmt']} {j['industry']}  {j['aspect']}\n\n{j['prompt']}\n")
        dispatch(j)
        return

    for j in js:
        raw, dst = paths(j)
        state = "ON DISK" if dst.exists() else "not shot"
        print(f"\n{'=' * 92}\n{j['fmt']}  {j['industry']}  {j['aspect']}  "
              f"grade={j['grade']}  [{state}]\n\n{j['prompt']}")
    print(f"\n\n{len(js)} paid jobs selected. DRY RUN, nothing spent. "
          f"Add --go with exactly one job to shoot it.")


if __name__ == "__main__":
    main()
