---
name: static-ads-comparison-table
description: Presentation sub-skill. Two headings over two tinted columns on black, one marked row against one marked row, the pairing carried by a CSS grid rather than by line lengths. Use for any two-column contrast, and as the control any more interesting shape has to beat. Built for F7 and F33, awaiting the pick. Read formats/static-ads/presentations/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: tpl:image 9.png
renderer: scripts/f7_variants.py build_table
---

# Comparison table

**The mechanism.** The plainest way to put two options side by side, done properly. It is what a
contrast format is always specified as and rarely gets, so **treat it as the control**: a more
interesting shape has to beat it rather than merely differ from it.

## 1. What is taken from the reference

`tpl:image 9.png`: **the two-column comparison panel, structure only.** Two headings above two
tinted columns, one marked row against one marked row.

NOT its cream bed, NOT its lilac panel and NOT its title case, because the house is black, one blue
accent and sentence case (`../../SKILL.md` section 0). Nothing borrowed needs a citation of its
own.

## 2. The grid is the fix

**Two independently wrapping columns cannot pair their rows.** That single problem held F7 and F33
up for the whole suite: each column wrapped as its own paragraph, so row two on the left lined up
with row two on the right only when the line lengths happened to agree, and the next industry's
wording broke it.

**One CSS grid pairs them, because a grid row sizes to its taller cell.** Row two on the left
always starts level with row two on the right, whatever the wording does.

Three details that go with it:

- **The mark and the text sit in an INNER row inside the cell.** Centring the cell's own flex line
  puts the mark halfway down a multi-line block; the reference aligns every mark with the first
  line of the row it marks.
- **The grid's own font-size is what the fit solves**, so every row on both sides lands on one
  size. The headings carry an absolute size so the cascade never drags them along.
- **Corner radii come from first-child and last-child rules**, so the stack reads as two panels
  rather than as N boxes.

## 3. The panels

Fills with no borders, the way the reference draws them: a flat lift off black on the them side,
the accent at a tenth on the us side. **The blue is one accent used twice** (the panel and its
ticks) rather than a second colour.

**On a one-row card the panels carry a height floor.** One line a side gives content-height panels
that leave a third of the frame empty, and the reference draws its panels tall whatever is in them,
so the floor is the reference's own behaviour rather than padding invented to fill space.

**The floor is 560 when the card has a head and 720 when it does not** (the operator, 2026-08-10). At 720
with a head the column overran its own padding box and **the CTA's second line rendered underneath
the logo.** The head closes the same hole the 720 floor was opened to close, so with a head the
floor only has to stop the panel collapsing.

## 4. The trap that a passing fit does not catch

**A fit that passes is not a card that reads.** At its own 64px maximum the F33 column solved
cleanly and broke "Leaves with / the / knowledge." across three ragged lines. **Cap the maximum by
eye**, per card, and read the render back before reporting it.

## 5. The open question

This is the first card in the suite to put copy **inside a container**. F1, F3, F5 and F6 all sit
on a bare bed, so the open call is whether the tinted panel is one lift too many for a house that
is otherwise type on void. It is written into the dossier beside the card.

## 6. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 f7_variants.py table                     # both formats, agnostic, free
python3 f7_variants.py table --fmt F33           # one format
python3 f7_variants.py table --industry retail   # one vertical
python3 f7_review.py                             # the dossier, beside its reference
```
