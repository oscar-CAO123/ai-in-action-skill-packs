---
name: static-ads-would-you-rather
description: Presentation sub-skill. A forced binary on black, two options with a drawn house graphic each, answered in the reader's head before the CTA. Use when the argument is a choice between the reader's current move and the hire. Shipped as the F5 rather variant, shipped and live. Read formats/static-ads/presentations/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: local:a competitor-8-statics/05-would-you-rather
renderer: scripts/f5_variants.py build_rather
---

# Would you rather

**The mechanism.** A forced choice with a rigged pair. The reader answers it in their head before
they reach the CTA, so the argument is made by them rather than to them.

## 1. What is taken from the reference

`local:a competitor-8-statics/05-would-you-rather`: **the binary and the rigging.** Two options set as
a question, where one of them is the behaviour the card is arguing against. The reference also
carries a photographed object pair; that part does not transfer, see section 3.

## 2. The pair that shipped

> **Would you rather?**
> A. Buy another AI tool and hope this one sticks.
> B. Hire one person who builds everything custom to your business.

**A is a way of working, never a named competitor.** That is the teardown's own note on this
format and it is the gate. Here A is the reader's current move, which is the exact behaviour the
approved F5 head argues against, so the binary and the sentence are one argument rather than two.

B is your wording, . It beats "owns where the work goes" because it answers the
objection A raises: a bought tool is generic by definition, so "custom to your business" is the
thing the tool cannot be, and the binary stops being a preference.

## 3. The two pictures are drawn, not shot

your call, . The reference photographs two objects and house has no object: the thing
being compared is a pile of software against one person, and neither photographs honestly without
inventing a product or hiring a model.

So the pair is house graphics, free, inside the locked system: no photograph, no competitor mark,
no face, one accent.

- **A is many faint outlines.** A 4x4 grid of blank tiles, unbranded by construction.
- **B is one solid blue figure**, at the weight of the whole grid.

The argument is carried by count and weight before a word is read, which is what the reference's
own object pair does with volume.

**A shot pair can still land later without the layout moving.** `RATHER_SHOTS` takes a file path in
either slot and a real image always wins over the drawing.

## 4. The bed stays black

The reference runs white with a brand-coloured shape closing the bottom third. The house equivalent
of that shape is the blue quadrant, so the ground does not also have to move.

## 5. Known, and shipped knowingly

**This card carries NO route.** No CTA line, no quiz sentence, no foot strip. Written into its
`notes` in the card's own notes. It ships that way because the binary closes itself, and it is the open item
if the format is scaled.

## 6. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 f5_variants.py rather                    # agnostic, free
python3 f5_variants.py rather --industry retail  # one vertical
python3 f5_review.py                             # the dossier, beside its reference
```
