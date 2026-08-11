---
name: static-ads-plate-led
description: F7 sub-skill. A photographic plate carries the frame and the type is laid over or under it. Owns plate composition, the VHS look, the de-text pass, the annotation overlay and the grade. Use for the advice / advertorial static, editorial masthead embed, annotated hero, long-form native article, before and after, and the big quote plus star row. Read formats/static-ads/SKILL.md first for the shared law.
parent: static-ads
format: F7.2
---

# F7.2 Plate-led statics

## LOCKED: the watercolour window format (you, The format of record for plate-led industry cards. Approved on the construction / owner-bottleneck
card and locked. Reference build: `scripts/plates_noirreal.py` + `finish_noirreal.py` +
`build_noirreal.py`, output at `scripts/out-noirreal/bottleneck.png`.

**The plate.** 4:5 native, one paid `your image model` job.
- The **interior and the figure are watercolour**: translucent washes bleeding wet-into-wet, blooms
  and backruns, granulation, bare white paper through every highlight, on cold-pressed paper.
- **The figure is FACELESS.** The face is blank unpainted paper, no eyes, no nose, no mouth. This is
  the house faceless rule, kept.
- **The window is a real photograph in full colour**, and it is the only colour in the frame. The
  colour stops at the window frame. The window sits at desk height behind the figure and runs nearly
  the full width.
- The scene shows **the industry's own work continuing without the owner**.

**Two free finishing passes**, both masked, never prompt-baked:
- **Moire** on the watercolour only, from the house tool at
  `projects/content-engine/engine/tools/moire/moire.py` via `--still`.
- **VSL grade** on the window only: warm amber, lifted blacks, softened saturation, grain.
- The mask detects the window by its own signature, **blue sky plus orange high-vis**, not raw
  saturation. Watercolour carries residual warmth in skin and timber, and a saturation mask blows
  the aperture out to two thirds of the frame.

**The card.** Plate bleeds full frame. Copy sits in the band **above the figure's head** and never
crosses him, over a **top-weighted wash in the paper's own colour**, not a dark scrim: a dark scrim
fights watercolour. Dark ink type, one blue accent, your display typeface only, CTA as a thin rule under the sub.

**Medium note.** Watercolour supersedes the oil-noir ruling **for this static family
only**. The F2 VSL boards still specify oil-noir. The oil version of this plate is parked at
`scripts/plates-noirreal/_versions/oil-noir-/`.

**Open risk:** the lit cigarette. Meta restricts tobacco imagery and it may get the creative
rejected. Unresolved.

---

## LOCKED: the ripped news-collage format (you, The second format of record for plate-led industry cards, a sibling of the watercolour window above,
not a replacement. Approved across all five industries and locked. Reference build:
`scripts/plates_news.py` + `cut_news.py` + `collage_news.py` + `build_news_band.py`, output at
`scripts/out-news/<industry>-band.png`, contact sheet `scripts/out-news/sheet-news.png`.

**Two paid jobs per industry, never more.** The site plate, then the chroma-green cut. Everything
after that is free.

**The site plate.** 4:5, `vhs-camcorder` from the F8 style bank, graded by the free
`grade_plate.sh vhs` chain. A business owner interviewed on location, chest up, plain unbranded
microphone, mid-sentence, looking off-lens. Every surface in the location is blank: the `NO_TEXT`
clause is not optional, this model writes legible signage onto anything in shot and it has already
cost two re-shoots (a named cafe with a full menu board, and a legible "For Sale").

**The cut.** One i2i job off the RAW plate onto flat chroma green, so the cutout carries clean colour
while the graded plate stays behind the tear. The subject is alone in it, holding the microphone
themselves, and the location is deleted rather than tinted.

**The sunglasses are GENERATED, not drawn.** Pop-art shades on every subject: heavy black contour,
flat `#1269FF` lens, Ben-Day dot field, one white glint. Described in the prompt as a flat comic
graphic so they read drawn inside a photoreal frame. The compositor never paints them on.

**The card.**
- The subject is cut out in **their own colour**, centred across, **bottom-anchored at 88% and bled
  past the bottom edge**. Never centred vertically: the plates frame chest-up, so a vertical centre
  ends in a hard slice across the torso mid-card.
- **Half the original background is kept** behind a jagged seeded tear, graded VHS site on the right,
  paper collage on the left. **No white lip on the tear.** The subject keeps their own cut edge.
- **The plate bleeds the full frame and the carousel's bottom-up fade is kept** (`plate_full=True,
  plate_fade=True`). The fade is what makes the copy readable across a lit subject. It was dropped
  for one pass and immediately called back.
- Copy is **lowercase**, via the additive `noir-lower` theme, one blue accent, your display typeface only.

**The newspaper configuration varies per card, and only in three ways.** Five decks running one
collage read as five crops of a single image. `COLLAGE` in `collage_news.py` sets, per industry: the
**angle** the scraps sit at, **which scan** each scrap and the bed is torn from, and where the
**light spots** fall, which is the `luma` range on each scrap. The tear, the placement, the fade and
the type do not vary.

**Newsprint is REAL, always.** Public-domain Library of Congress scans in `scripts/collage-src/`,
provenance in `sources.json`. Generated newsprint is banned outright: gibberish headlines are the
tell.

**Keying notes that cost money to learn**, all in `key_green`: threshold 0.25 not 0.10 (chroma
background measures 0.44, hi-vis 0.06, and the low threshold perforated the vest); a hysteresis pass
for the veiled location the i2i leaves behind; largest connected component, never a fixed flood seed;
`MIRROR_SITE` when the plate's own subject would otherwise appear beside their own cutout; and
`PATCH_GREEN` to mask an intruding interviewer, which is free where a re-shoot is not.

---


A photograph does the stopping and the type does the arguing. This is the only sub-skill that spends
money, so it is also the one with the hardest gates.

**Read `../SKILL.md` first.** Section 0 is the band law, section 2 the copy rules, section 4 the
funnel label. This file covers the plate.

---

## 1. The six formats

| Format | Archetype | The argument | Funnel | Band |
|---|---|---|---|---|
| **Advice / advertorial static** | V11 | Reads as an article, teaches before it sells | TOF | breaks |
| **Editorial masthead embed** | S1 | The pain set as a masthead headline over the scene | TOF | breaks |
| **Annotated hero** | house | Leader lines calling out what is wrong in the frame | BOF | breaks |
| **Long-form native article** | S13 | Primary text does the work, the image earns the click | TOF | keeps |
| **Before and after** | S10 | One frame twice, two states, two grades | MOF | keeps |
| **Big quote plus star row** | house | A real client's words at scale, gated by `../proof/` | MOF | keeps |

Cell assignments: `../FORMAT-GRID.md` section 2. Which cells break the band law: section 3.

## 2. The look is settled, do not re-cast it

**Every plate in the industry set is `vhs-camcorder` from the F8 style bank**, one style house-wide,
graded by the free `grade_plate.sh vhs` chain. you approved this on is the style
of record in `news-carousel/SKILL.md` section 1a. The old per-vertical cast (16mm, Betacam, Super 8,
VHS, press flash) is kept commented as `F8_VERTICAL_STYLES` because the F8 grid format still uses it.

A new plate for this sub-skill matches the VHS look unless you has authorised a different look for
that specific cell. Two such looks are authorised and unshot: a screenshot-grade flat look for ultra
low-fi and a phone-snapshot flash look for the comment reply, both owned by other sub-skills.

## 3. Composing a plate

- **Show the place the business is**, not another desk. Four keeper plates were re-shot on
  for exactly this: a construction job site, a suburban house, a pub dining floor, a
  retail shop floor. Financial services keeps its lamp-lit ledger desk as the benchmark you grades
  the others against.
- **Compose for the type.** Subject in the upper half, the lower portion falling into dark empty
  space where the copy will sit. A subject sitting low in the frame is unusable.
- **No people in any plate.** Not a silhouette, not a hand, not a reflection. A financial services
  plate broke this with a photographer silhouette and had to be demoted off the keeper set.
- **Nothing is drawn over a plate.** A prop the copy needs is composed into the scene instead, which
  is how the real estate clock got there. The one exception is the annotated hero, whose leader
  lines are the format.
- **Ask for no on-image text.** your image model bakes gibberish signage into set dressing unless told
  not to. Anything legible that survives is a defect: the real estate plate shipped with
  "APPRAISAL REQUEST SLIPS , UNOPENED" readable on a folder and needed a refine.

## 4. Spending rules (these are hard)

- **One paid job at a time.** Dry-run first, print the prompt, spend on one, look at it, then the
  next. Roughly 2 credits a job.
- **Refine, never re-roll, a frame you has approved.** `--refine --go` keeps the composition and
  fixes the defect. A re-roll throws away an approved frame and costs the same.
- **A paid raw that survives a failed grade is recovered with `--regrade`, which is free.** Never
  re-shoot to fix a grade.
- **Try the free fix first.** The retail and hospitality plates show dark speckle where VHS noise
  pooled on flat lit surfaces, and a lower-noise `--regrade` costs nothing and should be tried
  before anything is re-shot.
- Old plates are parked under `_versions/` rather than overwritten.

## 5. Laying the type in

`band.py` `render_card(lines, png, plate=<path>, overlay=<svg>, theme=)` is the renderer.

- `plate=` fills the frame **above** the band and falls off to black at its lower edge, so the join
  is invisible and the band stays pure black with its single block of type. A card that keeps the
  band law needs nothing else.
- `overlay=` takes raw SVG drawn on a 1080x1350 viewBox, which is how an annotated hero gets its
  leader lines and labels. Annotations set in your display typeface at `anno_weight`, 25px, 0.09em tracking, white at
  0.88 opacity. `arrow_overlay` in `news-carousel/scripts/build_industry.py` is the working
  reference implementation.
- **Type is never generated inside an image.** Every word on a house static is laid in the composite
  where it is legible, correctly spelled, on-brand and editable.
- A format that breaks the band (advertorial, masthead embed, annotated hero) needs its own template
  written against the same engine. None exist yet.

## 6. QA

- **The avatar is named in the type**, the pain is that avatar's own, and the card lands a question
  or a claim. Parent `SKILL.md` section 2. A plate showing the right workplace does not name the
  avatar on its own: the words have to do it.
- **Case belongs to the format.** All caps carries the news-carousel band and the keepers. An
  advertorial, a long-form native and a masthead embed are read as prose and set sentence case.
- Check the plate at full resolution for legible lettering before the type goes on. Speckle is fine,
  a readable word is a defect.
- No people, no drawn marks outside the annotated hero.
- One blue accent, funnel label recorded, sources recorded.
- Before and after: the two states have to be readable as the same frame, or the format fails. Two
  grades of one plate is the free route; two painted panels is two more paid stills and is outside
  the current budget.

## 7. Running it

```
cd "the business/skills/content-formats/formats/news-carousel/scripts"

python3 plates_real.py                                    # dry run, all 25, spends nothing
python3 plates_real.py <industry> <slug>                  # dry run, one
python3 plates_real.py <industry> <slug> --go             # shoot, ONE paid job at a time
python3 plates_real.py <industry> <slug> --refine --go    # i2i fix, keeps the approved frame
python3 plates_real.py <industry> --regrade               # re-grade from raw, FREE
python3 build_industry.py                                 # re-render from plates on disk, ~3 min
```

Scene briefs, `PLATE_STYLES` and `NO_PEOPLE` live in `plates_real.py`.
