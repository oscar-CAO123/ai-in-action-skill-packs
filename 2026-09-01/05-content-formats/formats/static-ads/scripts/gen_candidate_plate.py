#!/usr/bin/env python3
"""Generate ONE candidate poster plate. Paid. One at a time, never batched.

    python3 gen_candidate_plate.py u1a          # dry run, prints the prompt only
    python3 gen_candidate_plate.py u1a --go     # dispatches the paid job

Plates land in `../candidate/plates/<slug>.png`. Re-run `build_candidate_posters.py --plates`
afterwards to composite the type over them.

ROUTING (settled with you .
  u1a  `soul_cinematic` at 21:9. references/canon/model-routing.md gives retro and authentic
       shots to your cinematic model, "the one model that returns an image reading as captured rather
       than rendered", which is what "ultra-realistic with imperfections" asks for. The plate
       is the middle third only, 1080x450, so 21:9 is the closest supported ratio to 2.4:1.
  u1b  `your image model` at 4:5, full bleed. The noir-painterly style lock in F2's own
       SKILL.md outranks the general routing table, and this plate carries its own paper
       ground behind the type, so it fills the whole 1080x1350 frame.
  u4   same as u1b, on a plain white ground.

FACES. The house noir STYLE block hardcodes faceless silhouettes. your rule, :
"faces when I say so, otherwise none". He said so for u1a (a mugshot) and u4 (the gaunt
falling face). u1b's graduate stays faceless.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HF = "/opt/homebrew/bin/your generation platform"
OUT = Path(__file__).parent.parent / "candidate" / "plates"

# The house vhs-camcorder tail, lifted verbatim from ideas/industry-build-carousels/styles.json.
# The date-stamp ban is load bearing: that style's own qa note records the model baking a
# camcorder timestamp into the corner unless the tail forbids it.
VHS_TAIL = ("Amateur home-video look, low fidelity, soft optics, muted washed colour, visible "
            "tape softness and faint chroma bleed. Not a clean photograph, not a film still. "
            "Full-bleed frame, no border, no film edge, no sprocket holes, no letterboxing, no "
            "frame within the frame. Single clean exposure. No timestamp, no date stamp, no "
            "on-screen display, no text, no lettering, no numbers anywhere in the image.")

# you, on the u1a v3 plate: "less degraded, brighter". The full tail above
# crushes the room to black and smears the picture. This keeps the tape as a texture rather
# than as the subject, and asks for a bright well-exposed frame.
VHS_TAIL_LIGHT = (
    "A light home-video look: gently soft optics and slightly muted colour with only a trace "
    "of tape texture, clean enough to read every part of the picture. Bright, generously "
    "exposed, open shadows with detail in them, nothing crushed to black. Full-bleed frame, "
    "no border, no film edge, no sprocket holes, no letterboxing, no vignette, no frame within "
    "the frame. Single clean exposure. No timestamp, no date stamp, no on-screen display, no "
    "text, no lettering, no numbers anywhere in the image.")

# The canonical noir style, lifted verbatim from news-carousel/scripts/decks_noir.py, with the
# faceless clause cut where you has authorised a face and the ground swapped off black.
NOIR = ("A moody black-and-white oil painting in high-contrast film-noir style, thick visible "
        "brushstrokes, painterly chiaroscuro, hand-painted animation still, not a photograph.")

# Oil on paper: the canonical noir SUB-STYLE declared by you off the u1b plate.
# Spec of record is formats/noir-painterly/SKILL.md Phase 2b. These two constants are that
# section's PAPER and MARKS blocks verbatim; edit the skill and this together or they drift.
# Assembly is PAPER + <the scene> + MARKS, exactly as the parent is STYLE + scene + LIGHT.
PAPER = ("A moody black-and-white oil painting in high-contrast film-noir style, thick visible "
         "brushstrokes and heavy impasto, hand-painted, not a photograph. It is painted directly "
         "onto a sheet of warm off-white paper with visible fibre, tooth and a few age flecks. "
         "The paper is the whole ground and fills the frame edge to edge.")

MARKS = ("The hand shows: a few loose spots and flecks of black paint dotted around the page away "
         "from the subject, one or two strokes that stop short or miss where they were going, a "
         "thin dry-brush skip where the bristles ran out of paint, and faint smudges and "
         "fingerprints on the bare paper. Purely black and white paint with no colour of any "
         # The edge ban was strengthened : the U7 cover came back as a photographed
         # sheet with a deckle edge, a white surround and a drop shadow, all four already
         # banned by the shorter wording. Naming the failure outright is what holds it.
         "kind. The paper fills the entire frame and runs off all four edges: this is the "
         "artwork itself, never a photograph of a sheet, so there is no paper edge, no deckle "
         "or torn edge, no corner, no canvas edge, no border, no mount, no frame, no drop "
         "shadow, no white surround and no desk or surface behind or around it anywhere. "
         "Absolutely no text, no lettering, no signage, no labels, no logos and no numbers "
         "anywhere.")

PLATES = {
    # v1 was REJECTED by you and must not be re-run. It asked for a literal
    # booking photo: "the way a person looks into a booking camera", expressionless, eyes-only
    # crop, plus a stack of blemish / bloodshot / dark-circles / stubble, lit by a harsh flat
    # on-camera flash. Those composite into an arrest photo of someone who looks unwell. The
    # word "mugshot" in the brief meant an extreme close-up of an archetype, nothing more.
    # v2 keeps ONLY the tape format and changes every one of those choices.
    "u1a": {
        "job": "soul_cinematic",
        "aspect": "3:4",          # your cinematic modeltic has no 4:5; generate 3:4 and let the rig crop
        "note": "from behind, wide, laptop at night",
        # v2 rejected: face visible, subject in the top half, flat dark laptop lid filling the
        # bottom, which composited as a dead black gap above the type.
        # v3 rejected: right idea, wrong distance and grade. you: "further back, further
        # back, less degraded, brighter." v3 sat right on his shoulder, crushed the room to
        # black and smeared the picture with tape artefacts.
        # v4 pulls the camera well back into the room, lifts the exposure so the room reads,
        # and swaps to VHS_TAIL_LIGHT so the tape is a texture rather than the subject.
        "prompt": (
            "A home-video frame shot on tape from across a room. A wide view from well behind "
            "an ordinary Australian man in his early twenties who is sitting at a desk in a "
            "bedroom at night, seen from the back. He is small in the frame with plenty of "
            "room around him: the camera is several metres back, near the doorway, and we can "
            "see the desk, the chair, the wall and the floor around him. His face is never "
            "visible at any point. In front of him an open laptop sits on the desk and its "
            "bright screen throws soft light forward across the desk and up onto him and the "
            "wall. A warm lamp is also on somewhere in the room, so the whole space is clearly "
            "lit and easy to read rather than dark. He sits slightly hunched with one hand at "
            "the keyboard, in a plain t-shirt. The lower part of the frame is the lit desk and "
            "floor. Framed slightly off-centre and shot handheld, as though nobody composed it "
            "carefully. The laptop screen is a soft rectangle of light with nothing readable "
            "on it. " + VHS_TAIL_LIGHT),
    },
    "u1b": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "falling graduate on paper, faceless, full bleed",
        # THIS IS THE APPROVED PROMPT. Do not add anatomy to it.
        # A v2 was tried that named the head, the arched back, both arms, each leg and the
        # direction of travel. It came back correct and completely literal, a rendered man in a
        # gown, and you rejected it and restored this one . The gesture IS the
        # style. See noir-painterly/SKILL.md Phase 2b.
        "prompt": (
            PAPER + " A single figure in a university graduation gown and mortarboard cap falls "
            "slowly through open air, tumbling, gown and sleeves streaming upward, painted in "
            "thick black oils. Any human figure is a neutral faceless silhouette with no face "
            "and no features. The figure sits in the middle third of a tall vertical frame and "
            "the top third and the bottom third are left as completely empty bare paper. A "
            "single hard key light rakes across the falling figure, brilliant white highlights "
            "on one edge, the rest of the figure solid black. " + MARKS),
    },
    "u4": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "first person push, gaunt falling face",
        # Moved onto the oil-on-paper sub-style (PAPER + MARKS) on after you
        # declared it canonical. It was written before that existed and asked for flat plain
        # white; paper is the house ground now and it matches the approved u1b.
        # A FACE IS AUTHORISED HERE. you named the gaunt falling face specifically, which is
        # the only exception to the faceless clause on this card.
        # Kept gestural on purpose. The u1b lesson: describe the movement and let the paint
        # find the body. Do not add a body plan to this prompt.
        "prompt": (
            PAPER + " A first-person point of view: the viewer's own two hands and forearms "
            "reach up from the bottom of the frame, palms open, caught mid-shove, painted in "
            "thick black oils. Falling away below them a gaunt hollow-cheeked figure tumbles "
            "backwards through open air, its face turned up toward the viewer, eyes wide and "
            "mouth open, the features sunken. The hands and the falling figure sit in the "
            "middle third of a tall vertical frame and the top third and the bottom third are "
            "left as completely empty bare paper. A single hard key light rakes from high on "
            "one side, brilliant white highlights on the hands and the upturned face, the rest "
            "solid black. " + MARKS),
    },
    # U7's Theme B cover, the only paid plate in that carousel. you moved U7 off the 5-plate
    # black F5 rig onto Theme B on paper so this is one still instead of five.
    # Gestural per the sub-style: subject, garment, movement, then stop. Faceless, no face
    # authorised on this card.
    "u7": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "u7 cover, against the crowd",
        # v1 was the lone climb, and it left the figure floating with dead paper around it.
        # you, : fill the page with a crowd all facing the other way and take it
        # aerial, so the card reads as one person going against everyone. Band layout, so the
        # painting fills the whole frame rather than sitting in the middle third.
        "prompt": (
            PAPER + " A high aerial view looking straight down on a dense crowd of small "
            "figures packed across the whole page, painted in thick black oils as a mass of "
            "repeating dark strokes and long cast shadows. Every figure in the crowd is dressed "
            "the same and walking the same way, all of them streaming in one direction across "
            "the frame together. One single figure near the centre walks the opposite way, "
            "straight against the flow, and the crowd parts into a narrow clear channel of bare "
            "paper around that one figure. Any human figure is a neutral faceless silhouette "
            "with no face and no features. The crowd runs off all four edges of the frame and "
            "fills it completely, so nothing floats in empty space. A single hard key light "
            "rakes across the crowd from high on one side, brilliant white highlights along the "
            "tops of the figures, the rest solid black. " + MARKS),
    },
    # U3's cover, the mascot poster. One paid still for the whole carousel.
    #
    # THE HEAD IS DELIBERATELY ABSENT. The house mark is a wordmark and MARKS bans lettering
    # inside a plate, so asking for "the logo as the head" returns garbled letterforms. The
    # figure is painted headless and `build_u3.py` composites the real SVG over the neck, the
    # same way hand-drawn type is a font laid over the plate rather than paint. That also
    # keeps the mascot exact and reusable on U6 for no extra spend.
    #
    # Gestural per the sub-style: subject, garment, movement, then stop. The u1b lesson holds,
    # do not add a body plan to this prompt.
    "u3": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "u3 mascot poster, headless recruiter pointing out",
        "prompt": (
            PAPER + " A single figure stands square to the viewer in an old recruiting-poster "
            "pose, painted in thick black oils: a long formal coat and high collar, one arm "
            "thrown straight out toward the viewer with the index finger pointing directly at "
            "them, the other arm at the side. The figure has NO head and NO face at all: the "
            "coat and collar simply stop at an empty neckline and there is bare paper above it, "
            "so the space where a head would be is left completely empty and unpainted. The "
            "figure sits in the middle third of a tall vertical frame and the top third and the "
            "bottom third are left as completely empty bare paper. A single hard key light "
            "rakes from high on one side, brilliant white highlights along the pointing arm and "
            "the shoulders, the rest solid black. " + MARKS),
    },
    # THE VHS-NOIR CUTOUT SET. Four subjects, cut out once and reused across
    # every Theme B carousel. The fan law is one style per piece and no two the same on a page,
    # the way the F8 grid deliberately mixes four treatments, and the bank was all painted noir,
    # which you called "too much watercolour". These are the real-photograph half of it.
    #
    # WRITTEN TO BE CUT OUT, not to be a scene. The subject sits clear of its surroundings so it
    # mattes cleanly. No painted style block here on purpose: this set is the counterweight to
    # the oils, and from it is the HERO of every information page. Nothing recycled
    # from another carousel goes in that slot.
    #
    # VHS_TAIL_LIGHT, NOT VHS_TAIL. The first pass used the heavy tail and the plate came back
    # crushed almost to black, the same failure you rejected on u1a v3. A cutout has to read as
    # a figure at about 700px on a cream page, so it cannot be tenebrist: the tape is a texture
    # here, never the subject.
    "vhs-screen": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "vhs cutout, person at a screen",
        "prompt": (
            "A home-video frame shot on tape. One ordinary Australian person in their twenties "
            "sits at a desk half turned away, lit almost entirely by the screen in front of "
            "them, so the light rakes across one side of the face while the other side still "
            "holds detail. They fill the middle of the frame with clear space around them and "
            "the room behind them is a plain wall with nothing on it, so the figure reads as a "
            "single separate shape against it. " + VHS_TAIL_LIGHT),
    },
    "vhs-hands": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "vhs cutout, hands on a keyboard",
        "prompt": (
            "A home-video frame shot on tape, close in on a pair of hands typing on the "
            "keyboard of a laptop computer on an office desk. It is a computer keyboard with "
            "square keys, never a piano and never any musical instrument. No face and no body "
            "above the forearms. Hard light comes from one side and "
            "picks out the knuckles and the edge of the keys, the desk past the hands falling "
            "quietly away so the hands read as a single separate shape. The hands sit in "
            "the middle of the frame with clear space around them. The picture fills the whole "
            "frame edge to edge: it is never a small inset floating in a white or grey surround, "
            "there is no border, no mount, no letterbox bar and no frame within the frame "
            "anywhere. " + VHS_TAIL_LIGHT),
    },
    "vhs-room": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "vhs cutout, empty business interior",
        "prompt": (
            "A home-video frame shot on tape of a small empty Australian workplace at night: a "
            "few desks, a counter and a chair, nobody in it at all. One hard light source from "
            "the side throws long shadows across the floor while the room still reads. Shot "
            "square on from across the room, the furniture grouped in the middle "
            "of the frame with clear space around it. " + VHS_TAIL_LIGHT),
    },
    "vhs-desk": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "vhs cutout, two people across a desk",
        "prompt": (
            "A home-video frame shot on tape. Two ordinary Australian people sit across a desk "
            "from each other, one leaning in and explaining something, the other listening. They "
            "are seen from the side, both in the middle of the frame with clear space around "
            "them. One hard light from behind them rims both figures and the room past them is "
            "a plain wall, so the pair read as a single separate shape. " + VHS_TAIL_LIGHT),
    },
    # EPHEMERA FOR THE CUTOUT FAN. Two stills, cut out once and reused
    # forever across every Theme B carousel. Torn scraps and pen marks are built in code for
    # nothing; tape and staples are the two that need real material and a real shadow, which is
    # why these are the only pieces of the fan that cost anything.
    #
    # These are ASSET plates, not scene plates: several pieces laid on bare paper, well
    # separated, so `cutouts.py` can lift each one on its own. No noir style block, because a
    # tenebrist strip of tape is unusable as an object.
    "tape": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "tape strips, asset sheet",
        "prompt": (
            "A flat overhead photograph of a sheet of warm off-white paper with visible fibre. "
            "Lying on it are six separate short strips of translucent matte adhesive tape, each "
            "one torn at both ends with ragged uneven edges, laid well apart from each other "
            "with clear empty paper between them so no two strips touch or overlap. The strips "
            "sit at different angles. Each one casts a soft shadow and shows the faint creases, "
            "dulled patches and trapped air bubbles of tape that has been pressed down by hand. "
            "Even soft daylight from one side, sharp focus, the whole sheet in frame and filling "
            "it edge to edge. No text, no lettering, no numbers, no printing, no logos and no "
            "objects other than the tape anywhere in the image."),
    },
    "staples": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "staples, asset sheet",
        "prompt": (
            "A flat overhead photograph of a sheet of warm off-white paper with visible fibre. "
            "Pressed into it are eight separate metal staples, each one driven flat into the "
            "paper so only the small bright crimped bar shows, laid well apart from each other "
            "with clear empty paper between them so no two staples touch or overlap. They sit "
            "at different angles. Each one catches a hard glint along its top edge and casts a "
            "small tight shadow, and the paper around each is slightly dimpled and puckered "
            "where the staple pulled it in. Even soft daylight from one side, sharp focus, the "
            "whole sheet in frame and filling it edge to edge. No text, no lettering, no "
            "numbers, no printing, no logos and no objects other than the staples anywhere in "
            "the image."),
    },
    # U6's two halves. Each one is a window 540 wide by 743 tall inside the card, so both plates
    # are generated 4:5 and cropped by the column; the figure wants to fill its own frame rather
    # than sit in a middle third the way the single-image cards do.
    #
    # THE MEDIUM IS OIL ON PAPER. D2 permits watercolour on candidate units and the authored U6
    # asked for it, but every other card in the batch shipped in the oil-on-paper sub-style and
    # one watercolour card would read as a different campaign.
    "u6l": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "u6 them, the wall of backs",
        "prompt": (
            PAPER + " A row of figures in dark suits stands shoulder to shoulder straight across "
            "the frame, painted in thick black oils, every one of them turned away from the "
            "viewer with their backs squared and their shoulders set. Any human figure is a "
            "neutral faceless silhouette with no face and no features. The row fills the frame "
            "and runs off both side edges so nothing floats in empty space. A single hard key "
            "light rakes from high on one side, brilliant white highlights along the tops of the "
            "shoulders, the rest solid black. " + MARKS),
    },
    # The mascot half. Generated headless, `mascot.py` lays the mark in. Deliberately the mirror
    # of u3: that figure points at the viewer, this one offers a hand to them.
    "u6r": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "u6 us, the offered hand",
        "prompt": (
            PAPER + " A single figure in a long formal coat and high collar stands square to the "
            "viewer, painted in thick black oils, one arm reaching out toward them with the hand "
            "open and offered, palm up. The figure has NO head and NO face at all: the coat and "
            "collar simply stop at an empty neckline and there is bare paper above it, so the "
            "space where a head would be is left completely empty and unpainted. The figure "
            "fills the frame and the coat runs off the bottom edge so nothing floats in empty "
            "space. A single hard key light rakes from high on one side, brilliant white "
            "highlights along the offered arm and the shoulders, the rest solid black. " + MARKS),
    },
    # u3 v1 came back with the painting inside a ruled box, bare paper margins outside it and a
    # faint pencil rule down the right side. MARKS bans a frame within the frame outright and
    # this is the same "floats in empty space" failure you rejected on u4 v1. you, :
    # run the extend. i2i off the RAW plate, never off the mascot composite, so the head void
    # stays bare paper and `mascot.py` re-lays the mark afterwards.
    "u3x": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "u3 extended to fill the page",
        "refs": ["u3-u3-mascot-poster.png"],
        "prompt": (
            "Take the painting in the reference image and extend it outward so it fills the "
            "entire sheet from edge to edge. Keep the exact same subject, composition and "
            "brushwork: the figure in the long formal coat and high collar, one arm thrown out "
            "toward the viewer with the index finger pointing directly at them. Do not change "
            "the pose. The figure still has NO head and NO face: the empty head-shaped area of "
            "bare unpainted paper above the collar must stay exactly as it is, the same shape "
            "and the same bare paper, and nothing may be painted into it. Paint MORE of the "
            "same scene around the figure so nothing floats in empty space and there is no "
            "painted rectangle sitting on a sheet: the dark background and its brushwork carry "
            "all the way out to all four edges of the frame, the coat continues down and out of "
            "the bottom of the frame, and loose black oil strokes and spatter carry out to the "
            "corners. There is no ruled line, no pencil border and no painted edge anywhere. "
            + PAPER + " " + MARKS),
    },
    # you, : "extend it out from where it currently is, so it takes up the whole
    # scene". The v1 painting floats in the middle of the sheet with dead paper above and below.
    # This grows the SAME painting outward to fill the page rather than rolling a new one, so
    # the figure, the hands and the face he approved all survive. i2i off the v1 plate.
    "u4x": {
        "job": "your image model",
        "aspect": "4:5",
        "note": "u4 extended to fill the page",
        "refs": ["u4-first-person-push.png"],
        "prompt": (
            "Take the painting in the reference image and extend it outward so it fills the "
            "entire sheet from edge to edge. Keep the exact same subject, composition and "
            "brushwork: the viewer's own two hands and forearms reaching up from the bottom of "
            "the frame, and the gaunt hollow-cheeked figure tumbling backwards away from them "
            "with its face turned up, eyes wide and mouth open. Do not change their poses or "
            "their expressions. Paint MORE of the same scene around them so nothing floats in "
            "empty space: the forearms continue down and out of the bottom corners of the "
            "frame, the falling figure's coat and limbs carry further out, and loose black oil "
            "strokes and spatter carry the movement out toward all four edges. " + PAPER + " "
            + MARKS),
    },
}


# THE HERO IS CAST TO THE BEAT. This is the law the first pass broke: hero
# images were picked from whatever plates were lying around, so a slide about walking a work
# floor got a stock shot of hands and a slide about businesses waiting got an empty room.
# `industry-build-carousel/SKILL.md` section 2a already states it for the F8 grid, "cast the
# style to the beat, not to the industry", and "mixing the formats inside the grid is the
# effect". Both halves bind here.
#
#   O1  an owner alone with a half-working setup      live action, VHS
#   O2  watching work being done by hand              press photograph, hard flash
#   O3  the three-rung ladder                         DRAWN, built in code, costs nothing
#
# Three media across three pages, getting less literal as the carousel goes on. O3 is absent
# below because a drawn piece is not a plate: `cutouts.ladder()` builds it for free.
#
# The press blocks are `press-flash` from `industry-build-carousels/styles.json`, verbatim.
PRESS_HEAD = "A black-and-white press photograph."
PRESS_BODY = ("on 35mm with direct on-camera flash, hard shadow thrown on the wall behind the "
              "subject, everything beyond a couple of metres falling to black")
PRESS_TAIL = ("Push-processed black-and-white film, coarse grain, blown highlights, deep blacks. "
              "Photojournalism, not a rendering. Full-bleed frame, no border, no film edge, no "
              "sprocket holes, no letterboxing, no frame within the frame. Single clean "
              "exposure. No text, no lettering, no numbers anywhere in the image.")

PLATES.update({
    # O1. The beat is "they tried it themselves, it half worked, they are waiting on a person".
    # So: the owner, alone, in their own place, with something half-built in front of them.
    "hero-o1": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "hero o1, owner with a half-working setup",
        "prompt": (
            "A home-video frame shot on tape. An Australian small business owner in their "
            "forties sits alone at night in their own workplace, a small office behind a shop "
            "floor, leaning in toward a computer screen with one hand still on the mouse and the "
            "other pushed back through their hair. Their expression is tired and unconvinced, "
            "the look of somebody whose own attempt at something has half worked. The screen "
            "light falls across their face and the desk, and around them are the things they "
            "have already bought: a second monitor pushed aside, a printer, boxes still taped "
            "shut. The room behind them is plain and clearly lit enough to read. They sit in the "
            "middle of the frame with clear space around them. The picture fills the whole frame "
            "edge to edge and is never a small inset floating in a surround. " + VHS_TAIL_LIGHT),
    },
    # O2. The beat is "walk in, find the work being done by hand". So: the observer and the
    # manual task in one frame, in the medium that reads as reportage rather than as a set-up.
    "hero-o2": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "hero o2, watching work done by hand",
        "prompt": (
            PRESS_HEAD + " A young person stands back a couple of paces watching an older worker "
            "do a job by hand at a bench: papers being sorted and copied out one at a time into "
            "a ledger by hand. The watcher holds a small notebook and is writing in it, eyes on "
            "the work rather than on the page. Both people are in the frame and the worker's "
            "hands are clearly visible at the task. Shot square " + PRESS_BODY + ". "
            + PRESS_TAIL),
    },
})


# U4'S HEROES . U4 was rebuilt off the plain style onto the paper carousel, and the
# casting law bars anything recycled from another carousel out of a hero slot, so U3's three
# plates cannot carry these pages. Three keys.
#
# O3 was going to be free: a drawn `cutouts.ladder` as the third medium. It does not survive the
# fan (rails rotate into giant diagonals, labels land on the photographs) and it only repeated
# the body copy, so the page takes a photograph after all.
#
# THE MEDIA ARE SWAPPED AGAINST U3 ON PURPOSE. U3 runs live-action on O1 and press on O2. U4
# runs press on O1 and live-action on O2, so two carousels carrying adjacent beats never compose
# the same way.
#
# RE-CAST ONTO THE LADDER, your go. The three v1 plates below were shot to the old
# spine (THE SWITCH / THE SEAT / WHAT PROVES IT) and the rewrite replaced it with THE FIRST SEAT /
# THE STEP UP / THE TOP, so every one of them was off its beat and the casting law was broken on
# all three hero slots. The ladder needs three PEOPLE at three seniorities, which is the one thing
# none of the v1 plates carried. The v1 prompts are kept above each key as the record of what was
# shot and why it no longer fits; the notes carry `v2` so the new file lands beside the old raw
# instead of overwriting a plate that has been paid for.
#
# THE THREE MEDIA, which the v1 set got wrong. Section 4 of the skill wants live action, then
# press, then drawn, and never three of the same: the v1 set ran press, live action, press. Now
# it is VHS live action, then flashlit press, then the house oil-on-paper for the top rung, which
# is also the medium that suits the only page naming the role you place.
#
# EVERY SCREEN IS SEEN EDGE ON AND EVERY SHEET IS BLANK. Both are load bearing rather than fussy:
# u4-o2 v1 covered the desk in garbled lettering, which every tail in this rig bans, and a legible
# monitor is the other way that failure gets in.
PLATES.update({
    # O1, THE FIRST SEAT. The beat is the last line of the page: hand one repeated job to an AI
    # agent you built, and STAY TO WATCH IT RUN. So the concrete thing to shoot is a young person
    # watching, hands off, while the work happens without them. Watching is the whole point, so
    # the hands must be visibly idle or the picture reads as somebody typing.
    #
    # v1 shot the OLD O1, "bought tools nobody is running": a back room of sealed
    # cartons with no person in it at all. It is a good plate for that beat and it is the wrong
    # beat for this one, because a page about the first seat cannot show an empty room.
    "u4-o1": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "u4 hero o1 v2, watching it run",
        "prompt": (
            "A home-video frame shot on tape. A young person sits at a desk in a small ordinary "
            "Australian workplace, leaning back a little in the chair with both hands off the "
            "keyboard and resting in their lap, watching a monitor work on its own. Their whole "
            "face is clearly visible and completely unobstructed, lit by the light coming off "
            "the screen, absorbed and slightly pleased rather than posed. Shot from the side of "
            "the desk so the monitor is seen edge on and its face cannot be read. Beside them a "
            "second chair is pushed back and empty and a tray of paperwork sits untouched. "
            "Nothing is held up and nothing covers any part of their face. Any paper in the "
            "picture is plain and blank: no writing, no print, no handwriting and no markings of "
            "any kind. " + VHS_TAIL_LIGHT),
    },
    # O2, THE STEP UP. The beat is the page's own list: you own what gets built, what it is
    # allowed to touch, and WHO SIGNS IT OFF. So the concrete thing to shoot is the sign-off
    # itself: one person deciding over work two other people brought them. The seniority gap
    # between the three figures is what makes the page a step up rather than a second first seat.
    #
    # v1 FAILED twice over and must not be re-run. It shot the old O2, "the seat
    # mid-build", and the model laid the held page flat across the face, so the hero of the page
    # had no person in it, and it covered the desk in documents whose lettering rendered as
    # garble. Its fixes (nothing held up, the face named as unobstructed, the paper named blank)
    # are all kept here.
    "u4-o2": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "u4 hero o2 v2, signing it off",
        "prompt": (
            PRESS_HEAD + " Three people stand at a bench in an ordinary Australian workplace. "
            "The one in the middle is plainly the senior of the three, older and in charge, "
            "standing square over the bench with a pen in hand resting on a sheet, part way "
            "through deciding. The two either side are younger and are watching that decision, "
            "one with arms folded, and have plainly brought the work to be looked at. All three "
            "faces are clearly visible and unobstructed and nobody holds anything up in front of "
            "them. Plain blank sheets lie flat on the bench: no writing, no print, no "
            "handwriting, no diagrams and no markings of any kind on any sheet, and no screen is "
            "visible anywhere. Shot square from across the bench " + PRESS_BODY + ". "
            + PRESS_TAIL),
    },
    # O3, THE TOP. The beat is the senior seat deciding what the business hands to AI agents at
    # all, AND ANSWERING FOR IT. So the concrete thing to shoot is the answering: one person on
    # their feet in front of the people who will hold them to it.
    #
    # THE MEDIUM IS THE HOUSE OIL ON PAPER, which makes this the drawn page of the three. It also
    # suits the rung: this is the only page in the batch allowed to name the role you place, and
    # a painted plate reads as the top of a ladder where a flash photograph reads as a room.
    # Assembly is PAPER + scene + MARKS, which is the sub-style's own order.
    #
    # v1 shot the old O3, "the thing built and running": a junior standing beside a
    # wall screen they had wired up. That is a first-rung picture, and it is the plate currently
    # miscast on this page.
    "u4-o3": {
        "job": "soul_cinematic",
        "aspect": "3:4",
        "note": "u4 hero o3 v2, answering for it",
        "prompt": (
            PAPER + " The painting shows one person on their feet at the head of a long "
            "boardroom table, mid-sentence, one hand flat on the table and the other open in "
            "front of them, answering the room. They are the most senior person in the picture "
            "and they carry it. Four or five others sit along the table turned in their chairs "
            "towards them, listening, their backs and shoulders nearest the viewer. The standing "
            "figure's face is clearly visible, lit hard from a tall window at the side so the "
            "table and the seated figures fall away into deep shadow. Seen from the far end of "
            "the table at seated eye level. " + MARKS),
    },
})


# THE SCULPTURE END CARD. The last page of a Theme B carousel is the same
# end card the F8 industry-build carousels close on, except the monument changes per carousel.
# The Thinker belongs to F8 and is never reused here.
#
# The style blocks below are `moire-sculpture` from `industry-build-carousels/styles.json`,
# verbatim. Edit them together or the two formats stop matching. THE MOIRE IS NOT IN THE PROMPT:
# the tail explicitly bans it, because a model low-passes the fine gratings that create real
# interference and paints decorative op-art instead. The plate asks for the CARRIER, a fine metal
# mesh in deep focus, and `endcard.grade()` beats the pattern out afterwards for nothing.
SCULPT_HEAD = "A classical bronze sculpture in a dark gallery."
SCULPT_BODY = ("lit by one hard raking museum light from the side, seen through a fine metal "
               "mesh screen a short distance in front of it, deep focus so both the mesh and "
               "the bronze stay sharp, the gallery behind falling to black")
SCULPT_TAIL = ("Sharp photograph, real museum lighting, the patina and tool marks catching the "
               "light. No interference pattern, no banding, no glitch effects in the plate "
               "itself. Full-bleed frame, no border, no film edge, no letterboxing, no frame "
               "within the frame. Single clean exposure. No text, no lettering.")
CROP_CLAUSE = {
    # you named the framing for three of the seven. Saying it in the prompt is the only way to
    # stop the model deciding for itself where to cut a full-length figure.
    "top": ("The frame is a tight vertical portrait of the upper body only and stops at the "
            "chest: no waist, no hips, no legs and no lower body anywhere in the picture."),
    "full": "The whole sculpture stands in the frame with clear dark space around it.",
}


def _monuments():
    """Build one plate key per monument in the bank, `mon-<slug>`."""
    src = (Path(__file__).parent.parent / "references" / "monuments" / "monuments.json")
    if not src.exists():
        return {}
    out = {}
    for m in json.loads(src.read_text())["items"]:
        out[f"mon-{m['slug']}"] = {
            "job": "your image model",
            "aspect": "4:5",
            "note": f"end card, {m['title']}",
            "prompt": (f"{SCULPT_HEAD} Medium shot: {m['label']}, {SCULPT_BODY}. "
                       f"{CROP_CLAUSE[m['crop']]} {SCULPT_TAIL}"),
        }
    return out


PLATES.update(_monuments())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or args[0] not in PLATES:
        sys.exit(f"usage: gen_candidate_plate.py <{'|'.join(PLATES)}> [--go]")
    key = args[0]
    p = PLATES[key]
    dest = OUT / f"{key}-{p['note'].split(',')[0].replace(' ', '-')}.png"

    print(f"plate  : {key}  ({p['note']})")
    print(f"model  : {p['job']}  aspect {p['aspect']}  quality 2k")
    print(f"dest   : {dest}")
    print(f"\nprompt :\n{p['prompt']}\n")

    if "--go" not in sys.argv:
        print("DRY RUN. Nothing dispatched. Add --go to spend.")
        return

    # The two models name their size param differently, verified off `your generation platform model get`
    # on : soul_cinematic takes `quality` (1.5k, 2k), your image model takes
    # `resolution` (1k, 2k, 4k). Passing the wrong one is a hard failure, not a fallback.
    size = "--quality" if p["job"] == "soul_cinematic" else "--resolution"
    cmd = [HF, "generate", "create", p["job"], "--prompt", p["prompt"],
           "--aspect_ratio", p["aspect"], size, "2k", "--wait", "--json"]
    # i2i refinement. The house habit is to feed the approved image back as a reference rather
    # than roll a fresh one, so the thing already signed off survives the change.
    for r in p.get("refs",):
        ref = (OUT / r).resolve()   # OUT is the plates dir; refs are bare filenames
        if not ref.exists():
            sys.exit(f"reference plate missing: {ref}")
        cmd += ["--image-references", str(ref)]
    print("dispatching one paid job...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "[" not in r.stdout:
        sys.exit(f"generation FAILED (exit {r.returncode}):\n{(r.stderr or r.stdout)[:600]}")
    url = json.loads(r.stdout[r.stdout.index("["):])[0]["result_url"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    trim(dest)
    print(f"saved {dest}")


def trim(png, pct=0.02):
    """Shave 2 per cent off every edge.

    Every style tail in the house bans a border, a film edge and a frame within the frame,
    and the models add one anyway: the u1a v2 plate came back with a rounded dark vignette
    about 12px thick on the top and left. The band composites with object-fit:cover, so that
    edge survives the crop and shows as a hard line down the side of the card. Cheaper to
    shave it than to re-roll the generation.
    """
    from PIL import Image
    im = Image.open(png)
    w, h = im.size
    dx, dy = int(w * pct), int(h * pct)
    im.crop((dx, dy, w - dx, h - dy)).save(png)


if __name__ == "__main__":
    main()
