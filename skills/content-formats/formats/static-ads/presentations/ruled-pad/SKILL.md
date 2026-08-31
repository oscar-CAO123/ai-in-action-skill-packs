---
name: static-ads-ruled-pad
description: Presentation sub-skill. The card written by hand in pen on an aged ruled pad, every line of writing sitting ON a rule, with the marks and connectors drawn in two passes. Use for any list, contrast or worked argument that should read as thinking rather than as marketing. Built twice, as the F6 hand checklist (LIVE) and the F7/F33 two-column board. Read formats/static-ads/presentations/SKILL.md, formats/static-ads/hand-drawn/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: arch:S14, arch:S5, local:a competitor-6-formats/04-whiteboard-diagram
renderer: scripts/f6_variants.py build_hand, scripts/f7_variants.py build_board
---

# Ruled pad

**The mechanism.** Handwriting reads as thinking rather than as marketing. The reader watches the
argument being made instead of receiving a finished one, and the hand puts a person behind the
claim without showing one.

Built in two shapes so far and they share every rule below:

| Shape | Format | Argument | Cites |
|---|---|---|---|
| **Checklist** | F6 hand | A list of pains, all ticked, one line drawn from all of them into a single box | `arch:S14` |
| **Two columns** | F7, F33 | A contrast, hand-ruled apart, paired row for row | `arch:S5` for the medium, `local:a competitor-6-formats/04-whiteboard-diagram` for the frame |

## 1. The medium is the citation

`arch:S5` is the entry that authorises pen on paper: "Left: stop doing [xyz]. Right: hire a Chief
Agent Officer instead. Hand-drawn, cheap, high contrast. **The pen-and-paper aesthetic is a
retention mechanic in itself and signals that this is not an ad.**"

`arch:S14` is the checklist: "a handwritten list of pain lines, all ticked, with one line drawn
from all of them down to a single box reading the role you place."

**The two-column card was a whiteboard until ** and is now a pad, on your instruction.
The a competitor card keeps the frame it contributed (the black brand bars, the action pill, the drawn
columns); S5 replaces the surface. The citation changed with the medium rather than being left
pointing at a board.

## 2. The law: every line of writing sits ON a rule

**This is the whole format.** A ruled sheet whose writing floats between the lines is the tell that
kills the card, and it is invisible in code.

1. **Generate the rules FROM the row positions**, never as a repeating background. One origin, one
   step, and every block placed against the same grid.
2. **Every line-height is a whole number of rules**, so line two lands on a rule whenever line one
   does. A head set on a two-rule leading puts both of its lines on rules.
3. **Compute the baseline, do not guess it.** CSS centres the FONT's box in the line box, so the
   first baseline sits at `lineHeight/2 + (ascent - descent)/2 * size`, and nothing about it is
   symmetrical. Bradley Hand Bold measures **ascent 0.846em, descent 0.396em**, read off
   `fontBoundingBoxAscent` in the browser.

   **A guessed baseline puts the writing about 10px above the rule, and 10px is exactly the tell.**
   The first pass on the two-column card used half-leading plus half the size, which is what the em
   box would give, and every line on the render floated.

## 3. What the hand is, and what it is allowed to do

- **The face is Bradley Hand Bold**, which ships with macOS, so no new face enters the design
  system. Loaded with a `local` stack plus the system path as a fallback.
- **Legible beats authentic** (`../../hand-drawn/SKILL.md`). Read the render back at 440px, the
  contact-sheet size, before reporting the card.
- **Imperfection is sparse.** One wobble per stroke, no distressing.
- **Strokes are drawn twice.** The box, the tick, the cross and every underline are two passes that
  do not quite agree, which is what a pen going back over a line looks like.
- **Rotations are small on a ruled pad.** A rotation big enough to read as hand-written also lifts
  the line off the rule it is supposed to be sitting on. The two-column card runs 0.16 to 0.25
  degrees; the checklist, which has no columns to keep level, runs up to 0.55.
- **Jitter and ghost tables are FIXED, never `Math.random`.** A random renderer means the version
  you approved is not the version that rebuilds.

## 4. One accent, where a pen would make it

- **Checklist:** the blue is the box and the line running into it. Everything else is ink.
- **Two columns:** the blue is the us column, its heading, its hand rule and its ticks, which is
  where a second pen would plausibly go. **The head is therefore written entirely in ink and the
  copy's own accent span is dropped**, because a blue word in the head would be a second place the
  accent lives.

## 5. The surface

Reused from `f6_variants`, so both cards sit on the same paper:

- `PAPER_AGED` `#F0E8D5`, a pad that has sat around.
- `tooth`, two layers of `feTurbulence` multiplied over the base: one at high frequency for
  grain, one at very low frequency for the uneven blotching that makes paper read as aged rather
  than as flat card. Fixed seeds.
- `.vig`, a soft darkening into all four edges. A sheet is never evenly lit, and that is what stops
  a rendered paper reading as a flat swatch.
- The rules in `RULE` blue-grey and a `MARGIN_RULE` red vertical.

**Nothing here is photographed and nothing costs a credit.** `../../hand-drawn/SKILL.md` section 5
is explicit that a hand-made card is HTML, CSS and SVG rather than a generated image, and the same
logic holds for the surface: a generated sheet of paper cannot be nudged, and a photographed one is
a paid job.

## 6. The marks

- **A mark placed at its row's own y hangs a line-height below its own writing** and reads as
  marking the gap. It needs its own rise: the checklist uses a flat `TICK_RISE` of 20, the
  two-column card uses `0.3 * size` so it scales with the row.
- Marks sit **out in the margin**, to the left of the red rule, which is where a mark on a pad
  goes.
- **A cross against a tick** on the three-row card. **A cross against a drawn ring** on the one-row
  card, because a tick inside the ring is the same gesture twice, which
  `../../hand-drawn/SKILL.md` section 2 rules out.

## 7. The ring, and the trap it cost

The circle round the answer is **drawn in the browser after `fonts.ready`, from the measured box of
the block it rings**. Two passes at setting it in Python both failed on screen, because the type
wraps to a different number of lines per industry.

**An ellipse sized to a text block's half-width and half-height passes INSIDE its corners.** The
first pass ringed the block at `width/2 + 44` and the arc went straight through the first word and
the last. **Both radii need at least root two of the half-box**; `RING_JS` uses 1.42.

**The ring reaches 1.42 half-heights above the block**, so the row it rings has to start well clear
of anything above it. On F33 a row set three rules below the underline still put the top of the
circle through the blue hand rule; it sits four rules down now.

## 8. The brand furniture question, settled two different ways

- **Checklist (F6 hand):** carries the logo, which is **a deliberate override of two written
  rules.** `../../SKILL.md` section 0 says the band carries no logo, and
  `../../hand-drawn/SKILL.md` section 2 bans brand furniture on this sub-skill outright. your
  instruction, so the set reads as one campaign. The cost is real on the card whose
  whole mechanism is looking unbranded, so **it takes the smallest mark of the set**.
- **Two columns (F7/F33):** settled by structure rather than by override. The a competitor frame puts
  the brand in a **bar outside the drawing**, so the ban on brand furniture ON the drawing still
  holds. The bars carry the logo and an action pill.

**A bar needs its own in-flow logo.** `f6_variants.logo` positions the mark ABSOLUTELY; dropped
into a flex bar it leaves the row with nothing to space out, so the whole logo renders on top of
the pill. `f7_variants.bar_logo` stays in the flow.

**The route on a bar is the pill, not the sentence.** The full agnostic CTA does not fit a brand
bar, so the pill names the quiz instead.

## 9. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"

python3 f6_variants.py hand                       # the checklist, agnostic, free
python3 f6_review.py                              # its dossier
python3 crm_f6_variants.py --status               # the live F6 rows

python3 f7_variants.py board                      # the two-column card, both formats
python3 f7_variants.py board --fmt F33            # one format
python3 f7_variants.py board --industry retail    # one vertical
python3 f7_review.py                              # its dossier
```
