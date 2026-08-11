---
name: static-ads-ticked-rows
description: Presentation sub-skill. A headline held at the top and evenly ticked rows carrying the bottom, set in ink on a sheet of creased paper. Use as the control shape for any list or symptom stack. Shipped as the F6 rows variant, LIVE on the CRM. Read formats/static-ads/presentations/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: tpl:Frame 466
renderer: scripts/f6_variants.py build_rows
---

# Ticked rows

**The mechanism.** The plainest one in the bank: a headline, then a list, each row ticked. It reads
as a list because it is one.

**Treat it as the control.** It is what a list format is always specified as and rarely gets, so a
more interesting shape has to beat it rather than merely differ from it.

## 1. What is taken from the reference

`tpl:Frame 466`: **the row rhythm only.** One headline held at the top of the frame, evenly ticked
rows carrying the bottom, and deliberate empty space between the two.

NOT its funnel position: `tear:4` is the teardown note on Frame 466 and it is why only the rhythm
transfers. NOT its white bed, its green tick or its title case, because the house is black, one
blue accent and sentence case (`../../SKILL.md` section 0).

## 2. The bed is a recorded exception

**Creased paper, not black** (you, . A sheet folded into six and opened out.

Taking the card off black **flips the type to ink and leaves the blue on the ticks only**, which is
a live exception to the pure-black rule and is written into the card's `notes` on the CRM row.

**A crease is a shadow with a highlight on its other side**, which is why one gradient draws it and
a plain line does not. Two vertical folds and two horizontal, plus the shared tooth, plus a
vignette. Nothing is photographed.

## 3. The rows sit centred in what the headline leaves

your instruction, same day: move the five points up so they are centre-aligned. The template's
deliberate hole is still there, it is just shared above and below the rows now rather than sitting
entirely above them. `margin: auto 0` on the row list, not `margin-top: auto`.

## 4. Two independent fits, never one

A display headline and a row stack solve against different wells, and one fit for both undersizes
whichever is longer. The head takes its own search and the rows take theirs.

## 5. The logo foot is a deliberate override

you, : "we need to add the the business logo to the bottom", on all three F6 shapes, so
the set reads as one campaign. `../../SKILL.md` section 0 says the band carries no logo. This is
flagged rather than taken quietly.

**The fill rule has to name `polygon` as well as `path`.** The house logo's A crossbar is a
`<polygon>` and everything else is a `<path>`, so a path-only rule leaves the crossbar at its
default black: invisible on a black bed, and a second shade of dark on paper.

## 6. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 f6_variants.py rows                    # agnostic, free
python3 f6_variants.py rows --industry retail  # one vertical
python3 f6_review.py                           # the dossier, beside its reference
python3 crm_f6_variants.py --status            # the live rows, read off the board
```
