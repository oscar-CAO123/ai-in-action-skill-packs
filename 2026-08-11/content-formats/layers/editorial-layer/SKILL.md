---
name: editorial-layer
description: Use when you says "editorial layer", "newspaper cutouts", "make it feel editorial", "layered background", "archival cutouts", "newsprint", "collage layer", or wants a house video to stop sitting on flat black and instead sit on layered archival imagery, or wants newspaper and editorial fragments cut out and floating in a shot. A layer, not a format: it bolts onto F2, F10 and F11 without changing them.
canonical: true
layer: L-EDIT
---

# The editorial layer (L-EDIT)

Two things one technique gives you: a **bed** that replaces flat black behind the picture, and
**cutouts** of archival paper floating in it. Both are built from the same source material, real
imagery that supports the subject, and both are graded the same way.

**Reference:** a reference account\_\_ reel `instagram.com/p/<id>/`, 42.4s, 720x1280, 1.22M plays,
scraped and decoded frame by frame . Caption: *"One of the easiest ways to make motion
graphics feel more editorial."* The reel is a tutorial, so it states the method rather than only
demonstrating it. Decoded contact sheets are `reference-decode-a.png` and `reference-decode-b.png`
in this folder; the source clip is
`projects/content-engine/engine/reference-bank/reels/ref-editorial-DY7TSLJAQef.mp4`.

**The claim it makes, in its own words:** a solid background is fine because it does not distract
from the main content, "but if every background is just a flat color, eventually the piece begins
lacking identity."

---

## The method (verbatim from the reel, in order)

1. **Pull in a few images that support the subject of your video.** Its own examples: newspaper
   scans, and the architecture of the institution being talked about.
2. **Precomp them.** They become one layer, not several.
3. **Add a tint effect on top.**
4. **Set the blacks to a dark grey instead of pure black.**
5. **Push the whites slightly brighter, so the contrast stays subtle.**
6. **Add a little bit of texture** over the top: a grain, scratch or paper scan.

Step 4 and 5 together are the whole trick. The layer is not dimmed, it is **compressed**: both ends
of its range are pulled toward the middle so the imagery reads as texture rather than as a second
picture competing with the subject.

## What the numbers actually are (measured, not quoted)

Luma sampled off full-resolution frames of the reel. `p05` and `p95` are the fifth and
ninety-fifth percentiles, which is where the eye reads a level.

| Frame | What it is | p01 | p05 | median | p95 |
|---|---|---|---|---|---|
| 5.2s | **The "before".** Flat black background | 0.000 | 0.004 | 0.004 | 0.984 |
| 39.2s | **The finished bed**, dark passage | 0.024 | 0.059 | 0.067 | 0.106 |
| 38.6s | The finished bed with more imagery in frame | 0.027 | 0.063 | 0.094 | 0.384 |
| 41.2s | After the texture pass | 0.094 | 0.102 | 0.184 | 0.710 |

**The rule the numbers give you:** the bed lives between about **0.02 and 0.12** luma, median near
**0.07 to 0.10**, and it never touches zero. Flat black sits at 0.004, so the lift is small in
absolute terms and total in effect. The texture pass adds roughly **+0.04** on top of that.

Two consequences worth stating:

- **A bed that reads clearly on your monitor is too strong.** At p95 = 0.106 the imagery is barely
  legible in isolation. That is correct. It is felt, not read.
- **The texture pass is what stops it looking like a mistake.** Without it the lifted black looks
  like a crushed-black failure. With it, it looks like paper.

## The tension with the house's noir, and how it resolves

F2 `noir-painterly` is built on **crushed blacks**, and its LIGHT block says the rest "falls into
deep crushed black". This technique says do not use pure black. Both are right, at different
depths:

- **The plate keeps its crushed blacks.** Nothing about the painted frame changes.
- **The bed sits UNDER the plate** and shows through only where the plate is already at zero. The
  painted image still resolves to black at its own edges; what changes is that the black now has
  paper in it.

That ordering is the whole reconciliation and it is not optional. A bed composited **over** a noir
plate greys the picture out and fails the style.

---

## Mode A: the bed

The bed replaces the dead black in the frame. Composite order is bed, then plate keyed by its own
luma, then everything else.

```
bed        = tint(compress(collage of source images), lo=0.02, hi=0.12)
bed        = bed + texture * 0.04
alpha      = smoothstep(plate_luma, 0.00, 0.06)      # the plate's own blacks are the holes
frame      = bed * (1 - alpha) + plate * alpha
```

The plate's luma IS the matte, so nothing has to be masked by hand and the bed can never crawl
over a lit object. Tune `hi` in the smoothstep, not the bed's brightness: raising it opens more of
the plate's shadow to the bed, which is a compositional decision, where raising the bed's level is
just a mistake.

**The bed drifts, it does not sit still.** A slow push or lateral drift, slower than the plate's
own Ken Burns move, so the two never look locked together. About half the plate's rate.

## Mode B: the cutouts

Archival fragments floating in the frame: a newspaper column, a headline, a patent diagram, an
advertisement, a photographic corner. This is what makes it read as collage rather than as a
background treatment.

- **Torn or cut paper edge.** A visible white or off-white edge, 2 to 4px at 1080 wide. The rig
  already has this as `add_outline` in `ideas/cio-1981-noir/bin_collage.py`.
- **They bob.** Same sine as any other collage element: a slow vertical ride with a small counter
  sway and counter-rotation, non-harmonic periods so no two elements move in step.
- **They are graded harder than the bed**, because they are foreground and have to be legible:
  compress to roughly **0.06 to 0.55** rather than 0.02 to 0.12. A cutout you cannot read is
  decoration; the point is that a viewer can catch one word of the headline.
- **One or two per shot, never more.** Three fragments plus a character plus a plate is a mess.
- **Never over a face, and never over the caption band.**

## Sourcing (public domain first, and cite it)

The material has to be genuinely public domain, and the source gets recorded next to the asset the
way `BRIEF.md` records the `Facts, all sourced` block.

| Source | What it is good for |
|---|---|
| **Chronicling America** (`chroniclingamerica.loc.gov`, Library of Congress) | US newspapers 1770 to 1963, full-page scans, an open API, unambiguously public domain. The first stop for any period between 1880 and 1929 |
| **Library of Congress Prints & Photographs** | Photographs, architecture, industry, street scenes, with a rights statement per item |
| **Internet Archive** and **Prelinger Archives** | Film, and scanned trade journals and catalogues |
| **Wikimedia Commons** | Fast, but check the licence per file rather than trusting the category |
| **Google Patents** | Patent drawings, which are period-correct line art and read beautifully as a cutout |

**Generate rather than scan when nothing is being claimed.** If the fragment is atmosphere, a
generated period newspaper is fine and easier to control. If the fragment is being presented as
evidence of a specific real thing, it has to be the real scan, sourced. Do not blur that line.

**Text on a fragment is real text.** Generated newsprint produces gibberish that a viewer will
pause on. Either use a real scan, or crop so no headline is legible.

---

## Where it plugs into each format

| Format | How to use it |
|---|---|
| **F11 `cutout-story-vo`** | Natural home. The bed under every plate, cutouts on the beats where the story touches the record: a dateline, a figure, a proof beat. The rig is already built for it: `bin_beat.draw_floats` takes the cutouts and `blit` places them |
| **F2 `noir-painterly`** | Bed only, and only under. The painted world does not take foreground paper without becoming a different format |
| **F10 `slide-carousel-vo`** | Both, and it is the cheapest way to lift a slide film that is reading flat |
| **Static ads** | Bed only. The bottom-band law still governs all type |

## Hard rules

- **The bed goes under the plate, keyed by the plate's own luma.** Over the top it greys out the
  picture and fails the noir style.
- **Bed luma 0.02 to 0.12. Cutout luma 0.06 to 0.55.** Measured off the reference, not guessed.
- **The texture pass is part of the technique**, not a finishing flourish. Without it the lifted
  black reads as a crush failure.
- **Public domain, sourced and recorded.** Real scans whenever the fragment is doing evidentiary
  work.
- **No legible generated text, ever.** Gibberish newsprint is the tell.
- **One or two cutouts per shot.** Never over a face, never behind a caption.
- **The bed drifts at about half the plate's rate.** Locked together, the illusion collapses.

## Related

- The collage grammar this extends and the rig that implements it:
  `formats/cutout-story-vo/SKILL.md` (F11) phase 8, and
  `projects/content-engine/ideas/cio-1981-noir/bin_collage.py` (`add_outline`, `blit`).
- The look it has to respect: `formats/noir-painterly/SKILL.md` (F2) phase 2.
- Working implementation and the float layer:
  `projects/content-engine/ideas/unit-drive-1920s-noir/bin_beat.py` (`draw_floats`, `grade_cut`).
- Copy craft and the QA gate: `skills/content-formats/SKILL.md`.
