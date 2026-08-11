#!/usr/bin/env python3
"""Ultra-realistic noir plates: photoreal B&W interior, the window outside in full colour.

    python3 plates_noirreal.py                 # dry run, prints prompts, spends nothing
    python3 plates_noirreal.py <slug> --go     # shoot it, ONE job, ~2 credits
    python3 plates_noirreal.py <slug> --refine --go

your direction . The fourth plate family, and it breaks with the other three
on purpose:

  - `plates_noir.py`      painted noir, black ground
  - `plates_white.py`     painted noir, white ground
  - `plates_retro.py`     warm grainy 35mm, direct-response look
  - **this one**          PHOTOREAL noir, not painted. you: "realistic noir style, ultra
                          realistic noir style", explicitly not the oil-painted house look.

**The selective-colour rule is the whole idea.** The room, the man and everything inside are
pure high-contrast black and white. The view through the window is the only colour in the
frame, so the eye goes straight out to the site that is running without him.

**People are in, and faces are in.** The standing plate rule is no people and faceless
silhouettes; you overrode both for this family. Recorded so nobody reverts it.

**No text generated inside the plate.** Type is laid in by `build_retro.py`.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "plates-noirreal"
HF = "/opt/homebrew/bin/your generation platform"

STYLE = ("An ultra-realistic cinematic photograph in classic 1940s film-noir style, shot on "
         "35mm with a fast lens, razor-sharp photoreal detail, hard directional key light "
         "raking across the room, deep crushed shadows, visible cigarette haze in the light "
         "beam, fine film grain. A real photograph, absolutely not a painting, not an "
         "illustration and not a rendering.")

# The illustrated variant. **WATERCOLOUR, and the figure is faceless.** you reopened the
# medium on and directed watercolour for this static family, which supersedes the
# oil-noir ruling FOR THIS FAMILY ONLY. The F2 VSL boards keep oil-noir. The oil
# version of this plate is parked at plates-noirreal/_versions/oil-noir-/.
STYLE_ILLUS = ("A hand-painted black and grey watercolour illustration on cold-pressed paper. "
               "Translucent washes of ink and grey pigment bleeding wet-into-wet, soft blooms "
               "and backruns where the water pooled, granulation in the pigment, hard edges "
               "only where a wash dried, loose gestural brushwork, and bare white paper left "
               "showing through every highlight. Unmistakably a watercolour painting, not an "
               "oil painting and absolutely not a photograph. The man is a neutral FACELESS "
               "figure: his face is left as blank unpainted paper with no eyes, no nose, no "
               "mouth and no features of any kind. Only the interior of the room and the man "
               "are painted this way.")

COLOUR = ("The entire interior of the room, the desk, the furniture and the man himself are "
          "rendered in pure high-contrast black and white with no colour whatsoever. The view "
          "through the window behind him is the ONLY part of the frame carrying colour, and it "
          "is fully saturated natural daylight colour. The colour stops exactly at the window "
          "frame.")

FRAME = ("Shot square on at desk height from across the room, the man centred with the wide "
         "window filling the background behind him, balanced negative space, {ar}. Absolutely "
         "no text, no lettering, no signage, no labels, no logos and no numbers anywhere in "
         "the image. The image bleeds to all four edges and fills the frame completely, "
         "with no border, no mount and no frame.")

# scene -> (prompt body, aspect ratio, style block)
SCENES_META = {"bottleneck-window": ("5:4", "photo"),
               "bottleneck-illus": ("4:5", "illus")}

SCENES = {
    # construction / owner bottleneck
    "bottleneck-window": (
        "A man in period-accurate 1940s noir dress, dark three-piece suit, waistcoat, shirt "
        "sleeves and a loosened tie, sits leaned right back in a wooden swivel chair behind a "
        "heavy timber desk with both feet crossed up on the desktop, completely at ease, "
        "cupping a lit match to the cigarette in his mouth so the flare catches his face and "
        "the underside of his hat brim. Behind him a wide horizontal window runs almost the "
        "full width of the frame, its sill level with the desktop, and through it a busy "
        "daytime construction site in full colour: tower cranes, steel frames, scaffolding, "
        "stacked timber, concrete and workers in orange high-visibility vests moving under a "
        "bright blue sky."),
    # construction / owner bottleneck, illustrated interior + real window, 4:5
    "bottleneck-illus": (
        "A man in period-accurate 1940s noir dress, dark three-piece suit, waistcoat and a "
        "loosened tie, wearing a fedora, sits leaned right back in a wooden swivel chair behind "
        "a heavy timber desk with both feet crossed up on the desktop, completely at ease, "
        "cupping a lit match to the cigarette at his mouth. He and the whole room around him "
        "are painted in watercolour and his face is blank unpainted paper. Behind him a wide "
        "horizontal window runs almost the full width of the frame, its sill level with the "
        "desktop, and through that window, and ONLY through that window, is a real photograph "
        "of a busy daytime construction site in full colour: tower cranes, steel frames, "
        "scaffolding, stacked timber, a concrete mixer and workers in orange high-visibility "
        "vests under a bright blue sky. The painted room and the photographic window meet "
        "exactly at the window frame."),
}


# you, : the LOCKED watercolour window runs across all five industries. His rule is
# "same character and set, camera moves only", so the other four are i2i off the APPROVED
# construction frame: the same painted man, hat, chair, desk and room, moved to a new camera
# position. The ONE thing that changes besides the camera is what is visible through the window,
# because the format's whole argument is that industry's own work continuing without the owner.
THROUGH = {
    "real-estate": ("a suburban street of brick houses in full colour on a bright day, front "
                    "fences, garden beds, parked cars and an agent walking up a driveway"),
    "hospitality": ("a busy daytime dining room in full colour, laid tables, staff in aprons "
                    "carrying plates and a service pass behind them"),
    "retail": ("a busy daytime shop floor in full colour, shelving stacked with boxed stock, a "
               "counter and staff moving between the aisles"),
    "financial-services": ("a busy daytime open-plan office in full colour, desks, screens, "
                           "filing and brokers on the phone under bright windows"),
}
# you, second pass: the first four angles read as the same shot five times. The
# cause was not these lines, it was `FRAME`, which hardcodes "shot square on at desk height" and
# simply overrode them. Variants now use FRAME_VAR, which carries the framing rules without the
# camera position, and the moves below are large enough to be unmistakable.
ANGLE = {
    "real-estate": (
        "Shot from a LOW angle down near floor level, looking steeply UP at him past the near "
        "corner of the desk, so the underside of the desktop and the soles of his shoes dominate "
        "the foreground and the window sits high across the top of the frame behind his head."),
    "hospitality": (
        "Shot from HIGH above and behind his right shoulder, looking down over him at a steep "
        "angle, so we see the top of his hat, the desktop below and the window beyond him "
        "further down the frame."),
    "retail": (
        "Shot from his RIGHT in near profile, side on at desk height, so he is seen edge on with "
        "his hat brim and the line of his crossed legs in silhouette and the window runs left to "
        "right across the whole background behind him."),
    "financial-services": (
        "Shot WIDE from the far corner of the room at standing height, well back and off to his "
        "left, so the corner of the room, the side wall and the whole desk are in shot, he sits "
        "small on the right of the frame and the window runs away from us into the distance."),
}
FRAME_VAR = ("{angle} Balanced negative space, 4:5. Absolutely no text, no lettering, no signage, "
             "no labels, no logos and no numbers anywhere in the image. The image bleeds to all "
             "four edges and fills the frame completely, with no border, no mount and no frame.")
# Second rewrite, . The first HOLD said "keep everything else identical to the reference
# image", and against an i2i reference that instruction wins every argument: four re-shoots came
# back as the reference framing with a new window. Identity and composition have to be separated
# and the change made an explicit requirement, not a preference.
# you, third pass: the i2i reference is DROPPED for the variants. Five paid jobs
# proved the reference wins every argument, reproducing the construction framing however the
# camera was described, because "match this image" and "move the camera" cannot both be obeyed.
# The variants now generate fresh from the written scene and hold the character in WORDS instead,
# which is enough to keep the same suit, hat, pose and room without pinning the composition.
HOLD_VAR = (
    "The man is the same recurring character in every image in this set: a 1940s noir private "
    "detective in a dark three-piece suit, waistcoat and loosened tie with a fedora on his head, "
    "his face left as blank unpainted paper with no features, leaned right back in a wooden "
    "swivel chair with both feet crossed on the desktop, cupping a lit match to the cigarette at "
    "his mouth, entirely at ease. The room is the same: a heavy timber desk, plain painted walls "
    "and one wide horizontal window behind him.")

HOLD = ("Keep everything else identical to the reference image: the same man in the same clothes "
        "and fedora, in the same leaned-back pose with both feet crossed on the desktop cupping "
        "the same lit match to the same cigarette, his face still blank unpainted paper, the same "
        "chair, the same heavy timber desk, the same painted watercolour room and the same wide "
        "horizontal window with its sill level with the desktop. The room stays watercolour and "
        "only the view through the window is a real colour photograph, and the two still meet "
        "exactly at the window frame. Do not re-cast the man or redraw the room.")

VARIANTS = {f"bottleneck-illus-{ind}": "bottleneck-illus" for ind in THROUGH}


def prompt(slug):
    if slug in VARIANTS:
        ind = slug[len("bottleneck-illus-"):]
        body = (SCENES["bottleneck-illus"].replace(
            "a busy daytime construction site in full colour: tower cranes, steel frames, "
            "scaffolding, stacked timber, a concrete mixer and workers in orange high-visibility "
            "vests under a bright blue sky", THROUGH[ind]))
        # angle FIRST, then identity, then the composition-must-change clause
        return (f"{STYLE_ILLUS} {ANGLE[ind]} {body} {HOLD_VAR} {COLOUR} "
                f"{FRAME_VAR.format(angle=ANGLE[ind])}")
    ar, kind = SCENES_META.get(slug, ("5:4", "photo"))
    style = STYLE_ILLUS if kind == "illus" else STYLE
    return f"{style} {SCENES[slug]} {COLOUR} {FRAME.format(ar=ar)}"


def shoot(slug, refine=False):
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{slug}.png"
    ar = "4:5" if slug in VARIANTS else SCENES_META.get(slug, ("5:4", "photo"))[0]
    cmd = [HF, "generate", "create", "your image model", "--aspect_ratio", ar,
           "--resolution", "2k", "--prompt", prompt(slug), "--wait", "--json"]
    if slug in VARIANTS:
        pass          # NO reference: it pins the composition. See HOLD_VAR.
    elif refine:
        if not dst.exists:
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
    print(f"saved {dst}  ({dst.stat.st_size // 1024} KB)")


if __name__ == "__main__":
    args = sys.argv[1:]
    go, refine = "--go" in args, "--refine" in args
    picks = [a for a in args if not a.startswith("--")] or list(SCENES)
    known = list(SCENES) + list(VARIANTS)
    for s in picks:
        if s not in known:
            sys.exit(f"unknown scene {s}. have: {known}")
    if not go:
        for s in picks:
            print(f"\n===== {s} =====\n{prompt(s)}\n")
        print("DRY RUN. Nothing spent. Add --go to shoot, ONE at a time.")
    else:
        if len(picks) > 1:
            sys.exit("one paid job at a time. name a single scene.")
        shoot(picks[0], refine)
