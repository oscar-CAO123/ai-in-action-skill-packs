---
name: static-ads-lead-magnet
description: F7 sub-skill. The five lead-magnet statics: one visual format per hook, filled across seven industries, every card closing on a lead magnet that exists as a built page. Use when you asks for statics for the lead magnets, for a new industry's magnet ads, or to re-run any of the five formats. Read formats/static-ads/SKILL.md first for the shared law.
parent: static-ads
format: F7.6
---

# F7.6 Lead-magnet statics

Five hooks you supplied on each given its own visual format, filled per industry.
**35 cards: 7 industries x 5 formats.**

The reason the set exists: the 25 existing industry statics all close on
`decks_industry.MAGNETS`, which names five assets that were never built. The seven that exist are
in `projects/lead-magnet-funnels/build/`, and every card here closes on one of those.

## Router: one sub-skill per format

**Read this file, then exactly one sub-skill.** Each owns its own build, its own law and its own
paid traps; this file carries only what all five share.

| id | Sub-skill | Format | Hook | HOOKS.md | Paid jobs |
|---|---|---|---|---|---|
| F7.6.1 | `split-screen/` | Before / after split screen | `[Avatar]: this is the real reason you're still [painpoint]` | P2 + P5 | 2 per industry |
| F7.6.2 | `deliverable-shot/` | Deliverable shot | `Don't use AI in your [avatar] business before this audit` | S2 | none |
| F7.6.3 | `newspaper/` | Newspaper front page | `The truth about using AI in your [avatar] business` | A3, C9 | 1 per industry |
| F7.6.4 | `billboard/` | Filmed billboard **(LOCKED canonical)** | `[Avatar], are you still...` plus three pains | A4 + P5 | 1 to 2 per industry |
| F7.6.5 | `caution-card/` | Caution card | `[Avatar]. Please be careful. Do not touch AI...` | S2 + P5 | 2 total |

## The five formats, at a glance

| id | Format | Hook | HOOKS.md | Paid jobs |
|---|---|---|---|---|
| F-M1 | Before / after split screen | `[Avatar]: this is the real reason you're still [painpoint]` | P2 + P5 | 2 per industry |
| F-M2 | Deliverable shot | `Don't use AI in your [avatar] business before this audit` | S2 | none |
| F-M3 | Newspaper front page | `The truth about using AI in your [avatar] business. It's a lot easier than you think` | A3, C9 | 1 per industry |
| F-M4 | Filmed billboard | `Still...` plus the top three ranked pains, plus the magnet | A4 + P5 | 1 per industry |
| F-M5 | Caution card | `[avatar]. Please be careful. Do not touch AI before you do this audit.` | S2 + P5 | 2 total |

**30 paid jobs for the full set.** F-M4's copy is generated INTO the plate, not composited.

## Run it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"

python3 magnet_copy.py                 # every filled line, free
python3 magnet_copy.py --check         # the copy gate. Run before anything renders

python3 plates_magnet.py               # all 30 prompts, DRY RUN, spends nothing
python3 plates_magnet.py <industry> split before --go        # ONE paid job
python3 plates_magnet.py <industry> --regrade                # free re-grade from raw

python3 shot_report.py                 # free: capture every asset's scored report
python3 build_split.py --composite     # free: the split image, for tuning CROP and BAR
python3 build_split.py / build_deliverable.py / build_editorial.py
python3 build_billboard.py / build_caution.py
python3 sheets_magnet.py --sheet       # dossier + contact sheet, opens in Chrome
```

## The law this set adds

**Sentence case everywhere except F-M5**, which is the news-carousel card and inherits its caps
band. F-M1 uses the `noir-lower` theme with `lift=64`.

**Case-by-case deviations from the house law, all recorded, none silent:**

- F-M1 and F-M5 draw over the plate. The leader-arrow annotation was cut off the industry
  statics on ; these two carry an overlay because the overlay IS the format.
- F-M2 is the only white card in the house.
- F-M3 is the one deliberate break from your display typeface-only. A newspaper set in your display typeface is not a newspaper,
  and the borrow is the whole format. Didone masthead and headline, Georgia body, both off the
  system font stack. Built on `../references/newspaper-template.webp`.
- F-M4 carries a **Snapchat text bar**, built from `../references/snapchat-text-template.webp`:
  full-width `rgba(0,0,0,0.42)` scrim, white REGULAR-weight Helvetica Neue at 0.56 of the bar
  height with 130px side margins. **Translucent, not the flat `#767676` the template samples at**
  (that value is the mock's own light-grey page showing through). Dragged below the board so it
  clears the copy, and it is where the avatar is named.
- F-M4's billboard copy is **generated into the plate**, so that card's type is the only type in
  the set the house rig does not set. It is the one plate with **no grade at all**: you took the
  VHS off this format, so it is a clean daylight phone photo, pulled back, first-person. The
  photographer's own left arm **extends in from the LEFT EDGE, roughly horizontal**, close to the
  lens and out of focus. Not the bottom corner, not upright. It is set by an i2i refine off the
  approved plate, never a fresh roll: a fresh roll moves the scenery. Rejects are in `_versions/`.
- F-M5's mark is centred on the PLATE AREA (y=422), not the card. you, .

**Two tables are hand-set, never computed**, and every one is tuned once per plate:

| Table | File | What it fixes |
|---|---|---|
| `CROP` | `build_split.py` | the usable region of each raw plate, after the model's letterboxing |
| `BAR` | `build_split.py` | the censor bar, on the eyes, in fractions of the finished half |

## Traps already paid for

- **9:16 makes this model letterbox.** It renders a picture OF a video frame, scene inset, dark
  bands around it, and the style tail's explicit ban does not stop it. Everything shoots 4:5.
- **An automatic letterbox trim does not work.** No brightness threshold separates a band from a
  tenebrist BEFORE half: the setting that cleared the bands ate 645px of the dark room.
- **"Head in both hands" is not a hiding instruction.** State the hidden face as a fact about the
  frame or the model returns hands on the forehead and the whole face in view.
- **The report is 56,313px tall.** Capture cuts above section 01, and it shoots at a tall viewport
  then crops, because the report reveals its blocks on scroll and a short viewport captures them
  at opacity 0.
- **This model CAN set type when it is short, in caps and quoted line by line.** That is how F-M4
  gets its billboard copy, and it reverses the old house assumption. It still cannot be trusted
  with it: check every returned plate letter by letter before grading and re-roll on a typo.
- **Compositing type onto a blank billboard reads as a mock-up.** A working homography build was
  rejected for exactly that. Generate the copy into the plate.
- **`margin-top:auto` and wrapped text both defeat a fit search.** An auto margin absorbs all
  overflow so `scrollHeight` always equals `clientHeight`; wrapped text reports
  `scrollWidth == clientWidth`. Learned on the rejected build, and it binds any future fit.
- **`band.py` flattens every line it is given into one justified block.** A CTA passed as a second
  line becomes the last sentence of the paragraph. That is what F-M1 wants and what the first
  pass did not.

## State, **ALL 35 CARDS BUILT.** 7 industries x 5 formats. Every paid plate is shot; the whole set is now
free to re-render.

**Construction is on your content store board**, 5 rows, `crm_magnet.py`, snapshot and REVERSE written. The
other 30 are built and waiting on your review before they go anywhere.

Known defects, none blocking:

- **hospitality F-M4** prints `[TAKE THE MARGIN AUDIT]` with square brackets around the CTA. One
  refine fixes it.
- **hospitality and building-services split plates** carry burned-in camcorder date stamps
  (`NOV 14`, `DEC 04 1998`) that the style tail bans. One refine each.
- **professional-services F-M1** fits its band at 42% rather than 100%. Legible, but the type is
  smaller than the other six. `band.py`'s line-count scorer, not this rig.
