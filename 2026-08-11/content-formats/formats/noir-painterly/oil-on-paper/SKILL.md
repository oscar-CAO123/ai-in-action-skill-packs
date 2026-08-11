---
name: noir-painterly-oil-on-paper
description: F2 sub-skill. The same black-and-white noir oils, painted onto a sheet of warm paper instead of set inside a black environment. Use when you says "oil on paper", "the paper noir", "the paper style", "paint it on paper", or wants a candidate-facing painted plate. Owns the PAPER and MARKS prompt blocks, the gesture rule, and the light-ground band. Read formats/noir-painterly/SKILL.md first for the parent style.
parent: noir-painterly
format: F2.1
canonical: true
---

# F2.1 Oil on paper

Declared canonical by you on off the plate in `examples/01-gesture-founding-plate.png`.

**The difference from the parent is what the ground IS.** F2 paints a world and lets it fall away
into crushed black, so the frame is a place. This paints a subject onto a page, so the frame is an
artefact: a sheet somebody worked on. Nothing recedes, nothing is lit from behind, there is no
room. Paint on paper, with air around it.

**When to use it.** Candidate-facing work (audience A), where the parent's black world reads heavy
and corporate. Employer-facing work stays in the black environment. Approved on the candidate side
as deviation D1 in `projects/content-engine/candidate-angles/BATCH-1-COPY.md`.

---

## 1. The prime example

`examples/01-gesture-founding-plate.png` is the plate this sub-style was declared off, and
`examples/05-composited-card-u1b.png` is it finished as a card. Everything below is what that plate
does, written down.

| File | What it shows |
|---|---|
| `01-gesture-founding-plate.png` | **The founding plate.** A graduate falling, painted as a gesture. |
| `02-full-page-extend.png` | The style filling a whole page instead of floating in the middle. |
| `03-before-the-extend.png` | The same painting before it was extended. Shows the floating problem. |
| `04-counter-example-too-literal.png` | **What NOT to do.** The same brief with the anatomy spelled out. |
| `05-composited-card-u1b.png` | Finished card, poster layout, centred ink type on the plate's own paper. |
| `06-composited-card-u4.png` | Finished card, band layout on the light ground. |

## 2. The two blocks

Assembly is `PAPER + <the scene> + MARKS`, exactly as the parent is `STYLE + scene + LIGHT`.
Both blocks live in code at `formats/static-ads/scripts/gen_candidate_plate.py` as the constants
`PAPER` and `MARKS`. **Edit the file and this page together or they drift.**

**PAPER**
> *A moody black-and-white oil painting in high-contrast film-noir style, thick visible
> brushstrokes and heavy impasto, hand-painted, not a photograph. It is painted directly onto a
> sheet of warm off-white paper with visible fibre, tooth and a few age flecks. The paper is the
> whole ground and fills the frame edge to edge.*

**MARKS** (the imperfection block, your ask : "add a few human mistakes")
> *The hand shows: a few loose spots and flecks of black paint dotted around the page away from the
> subject, one or two strokes that stop short or miss where they were going, a thin dry-brush skip
> where the bristles ran out of paint, and faint smudges and fingerprints on the bare paper. Purely
> black and white paint with no colour of any kind. The paper fills the entire frame and runs off
> all four edges: this is the artwork itself, never a photograph of a sheet, so there is no paper
> edge, no deckle or torn edge, no corner, no canvas edge, no border, no mount, no frame, no drop
> shadow, no white surround and no desk or surface behind or around it anywhere. Absolutely no
> text, no lettering, no signage, no labels, no logos and no numbers anywhere.*

**The edge ban is load bearing and was strengthened on ** after the U7 cover came back
as a photographed sheet with a deckle edge, a white surround and a drop shadow, all four already
banned by the shorter wording. Naming the failure explicitly ("never a photograph of a sheet")
is what holds it.

**MARKS is not decoration.** Without it the plate comes back as a clean digital illustration on a
paper texture. The flecks, the missed strokes and the fingerprints are what make it read as a
physical object somebody made.

## 3. The gesture rule (the one that matters most)

**The figure is a gesture, not an anatomy.** Describe the movement and the cloth and let the paint
find the body. "Tumbling, gown and sleeves streaming upward" is the right level of instruction. The
reader gets one or two anchors, a mortarboard, a hand, a hem, and completes the rest themselves.
That is what makes it read as a painting rather than as an illustration of a person.

**Spelling out the anatomy kills it, and this was tested rather than assumed.** A second version of
the founding plate named the head, the arched back, both arms, each leg and the direction of
travel. It came back technically correct and completely literal: a rendered man in a gown, legible
at a glance and generic, with none of the force of the gestural version. you rejected it and
restored the abstract plate. Compare `01-gesture-founding-plate.png` against
`04-counter-example-too-literal.png` before writing any scene block.

**So:** name the subject, the garment and the movement, then stop. If a plate comes back too
abstract to place, add ONE anchor object. Never a body plan.

## 4. What carries over, and what must never be pasted back in

**Carries over from the parent, unchanged.**
- The faceless clause, unless you authorises a face for a specific plate. His rule, :
  **"faces when I say so, otherwise none."**
- Pure black and white. No colour, ever.
- The single hard key on the subject, so the paint keeps one bright edge and one dark mass.
- Detailed positive prose, camera-distance-led. Never JSON, never a wall of negatives.

**Dropped, and it breaks the style if you paste it back.**
- The crushed-black environment, the tenebrist shadow world, and "the lower quarter falls away into
  solid black". On paper there is nothing to fall away into.
- **"The painted scene bleeds to all four edges."** The PAPER bleeds; the painting does not.
  Leaving that line in makes the model flood the sheet and the paper ground disappears.

## 5. Composition, and the extend

The default composition puts the subject in the middle third with bare paper above and below,
which is what the poster layout wants. **It leaves the painting floating** if the card is a band
instead: compare `03-before-the-extend.png` against `02-full-page-extend.png`.

**To fill the page, extend rather than re-roll.** Feed the approved plate back as an i2i reference
on `your image model` and ask for MORE of the same scene carried out to the edges, naming what
continues (limbs out of the bottom corners, spatter toward all four edges) and stating that poses
and expressions do not change. The face, the hands and the brushwork survive intact. The rig
supports this: `gen_candidate_plate.py` takes a `refs` list of bare plate filenames.

## 6. Two things that composite it

**The light-ground band.** `formats/static-ads/scripts/band.py` takes `ground="light"`: paper
background `#f3ece1`, ink `#0a0a0a`, and both fades climb to paper instead of black. Default stays
`"dark"` and was proven byte-identical when the option landed. Use it whenever a paper plate goes
into the band layout. The fade dissolving the paint under the type is a feature: it is what keeps
ink copy legible over solid black brushwork.

**The editorial bed.** `formats/static-ads/scripts/collage_bed_paper.py` slots a Library of
Congress newspaper bed into the bare paper behind the paint, by keying the paint off the plate's
own luma. It reuses `collage_news.paper_bed` and differs in one line: that bed is written to be
ADDED to lift crushed blacks, and a paper ground needs it to DARKEN instead. Bed amplitude is
locked at **0.16** (deviation D5, above L-EDIT's measured 0.02 to 0.12). Bed only, never foreground
cutouts, per `layers/editorial-layer/SKILL.md`.

## 7. Related

Parent style: `formats/noir-painterly/SKILL.md`. The bed: `layers/editorial-layer/SKILL.md`.
The band and poster engines: `formats/static-ads/scripts/band.py` and `poster.py`.
Live use and deviations: `projects/content-engine/candidate-angles/BATCH-1-COPY.md`.
