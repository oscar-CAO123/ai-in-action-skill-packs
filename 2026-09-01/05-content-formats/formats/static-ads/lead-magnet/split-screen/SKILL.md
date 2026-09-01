---
name: lead-magnet-split-screen
description: F7.6.1. The before/after split screen for a lead-magnet static. Two VHS plates of the same person in the same room, hard centre seam, pain on the left and the work moving on the right. Use when building F-M1 for a new industry or re-running an existing one. Read formats/static-ads/SKILL.md and lead-magnet/SKILL.md first.
parent: static-ads-lead-magnet
format: F7.6.1
---

# F-M1, the before / after split screen

**Hook 1:** `[Avatar]: this is the real reason you're still [painpoint].`
HOOKS.md: **P2** cause and symptom, opened with **P5** name the avatar.

The argument is the picture. Left is the pain, one low source, the room covered, the face hidden
by posture. Right is the same person in the same room with the light up and the work moving,
face visible behind a flat cartoon censor bar.

**No BEFORE or AFTER lettering anywhere.** The light and the posture carry it.

## Build

```
python3 plates_magnet.py <industry> split before --go    # ONE paid job
python3 plates_magnet.py <industry> split after  --go    # ONE paid job
python3 build_split.py <industry> --composite            # free, for tuning
python3 build_split.py <industry>
```

**2 paid jobs per industry.** Both at 4:5, cropped to 540x1350 halves.

## The law

- **`subject` is written ONCE and used verbatim in both halves.** Only the light, the posture and
  the state of the room change. A different person on the right kills the format, and the rig
  asserts the clause is byte-identical before it will dispatch either job.
- **Cast the face treatment to the half.** Before: hidden by posture. After: visible with the
  censor bar. you, .
- **The censor bar is drawn, never prompt-baked.** Flat black, hard edges, no feather.
- Copy is the `noir-lower` theme with `lift=64`, and the magnet is the closing sentence of the
  same paragraph, not a second tier.

## Traps already paid for

- **"Head in both hands" is not a hiding instruction.** State the hidden face as a fact about the
  frame (`FACE_HIDDEN`) or the model returns hands on the forehead and the whole face in view.
- **9:16 makes this model letterbox.** Shoot 4:5. Do not put 9:16 back.
- **Do not try to auto-trim the letterbox.** It was built and thrown away: no brightness
  threshold separates a band from a tenebrist BEFORE half. The setting that cleared the bands ate
  645px of the dark room.
- **`band.py` flattens its lines into one justified block.** That is why the CTA reads as the
  closing sentence and why it must not be passed as a second tier.

## The two hand-set tables

Both in `build_split.py`, both tuned once per plate, off `--composite`:

| Table | What it fixes |
|---|---|
| `CROP` | the usable region of each raw plate, in fractions, after the model's letterboxing |
| `BAR` | the censor bar, ON THE EYES, in fractions of the finished 540x1350 half |

`BAR` cannot be computed: there is no face detector here and every plate frames the subject
differently. Measure it, write it down, never guess at render time.
