---
name: lead-magnet-billboard
description: F7.6.4. The filmed billboard for a lead-magnet static. A clean daylight phone photo of a roadside billboard whose copy is generated INTO the plate, the photographer's own arm pointing in from the left, plus a Snapchat text bar. Use when building F-M4 for a new industry. Read formats/static-ads/SKILL.md and lead-magnet/SKILL.md first.
parent: static-ads-lead-magnet
format: F7.6.4
canonical: true
---

# F-M4, the filmed billboard

**Hook 4:** `[Avatar], are you still...` plus the top three ranked pains, plus the magnet.
HOOKS.md: **A4** question hook, opened with **P5** name the avatar.

**LOCKED as canonical on the construction card, **, after five passes. Reproduce that
card's shape exactly; do not re-litigate the choices below.

## Build

```
python3 plates_magnet.py <industry> billboard --go              # ONE paid job, the scene
python3 plates_magnet.py <industry> billboard --refine --go     # ONE paid job, the arm
python3 build_billboard.py <industry>
```

**1 to 2 paid jobs per industry.** The scene is generated first; the arm is set by an i2i refine
off it.

## The law

**The billboard copy is generated INTO the plate, not composited onto it.**
`plates_magnet.billboard_prompt` quotes the headline, the three bullets and the CTA line by line
and the model sets them. Two builds are dead and must not be revived:

- a pop-art comic panel, scrapped outright;
- a blank billboard face with the copy mapped on by homography off a hand-set `QUAD`. It worked,
  and it read as a mock-up rather than a photograph of a real board.

**No VHS on this format.** `grade="none"`. A clean daylight phone photo, pulled back so the board
sits in the middle distance. The tape grade came off on the fourth pass.

**The type on the board is the canonical thin your display typeface weight**, asked for as a thin light geometric
sans with wide round letterforms.

**The arm extends in from the LEFT EDGE, roughly horizontal**, reaching across the frame to point
at the board while the photographer holds the phone in their right hand. Close to the lens and
clearly out of focus: a soft foreground element the eye passes over.

- **Not the bottom corner and not upright.** That was built and rejected as too dominant.
- **Not entering at board height as a straight-in arm.** That reads as a bystander pointing.
- **The scene is LOCKED once approved, so the arm only ever changes by i2i refine.** A fresh roll
  moves the scenery, which is the exact thing being avoided. `REFINE[("billboard","plate")]`.

## The Snapchat bar

Built from `../../references/snapchat-text-template.webp`, and it is the one composited element
on this card because it is phone UI over the footage rather than something printed on the board.

| | Value |
|---|---|
| scrim | `rgba(0, 0, 0, 0.42)`, **translucent** |
| height | 0.0578 of frame height |
| position | dragged below the board, clear of the copy |
| face | white, REGULAR weight, Helvetica Neue |
| size | 0.56 of bar height, 130px side margins |

**The template samples as a flat `#767676` only because that mock sits on a light grey page.**
Lifting that value literally produces an opaque slab. The footage has to read through it.

## Traps already paid for

- **This model CAN set type when it is short, in caps and quoted line by line**, including in a
  thin weight at middle distance. That reverses the old house assumption. It still cannot be
  trusted: **check every returned plate letter by letter before it is used and re-roll on a
  typo.** A misspelt billboard is the whole card.
- **`clientWidth` counts padding.** It broke the newspaper masthead and then this bar's side
  margins. Pass the measured width into a fit, never read it off a padded element.
