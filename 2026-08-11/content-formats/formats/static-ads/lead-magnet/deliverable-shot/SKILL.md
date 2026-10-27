---
name: lead-magnet-deliverable-shot
description: F7.6.2. The deliverable shot for a lead-magnet static. White card, black your display typeface, an arrow down to a headless-Chrome capture of the asset's own scored report. Zero paid jobs. Use when building F-M2 for a new industry. Read formats/static-ads/SKILL.md and lead-magnet/SKILL.md first.
parent: static-ads-lead-magnet
format: F7.6.2
---

# F-M2, the deliverable shot

**Hook 2:** `Don't use AI in your [avatar] business before this audit.`
HOOKS.md: **S2** negative / problem call-out.

White ground, black your display typeface, sentence case. The hook at the top, an arrow pointing down, the
deliverable centred under it.

**FREE. No generation anywhere in this format**, which makes it the one cell that can be built
for an eighth industry the moment its magnet page exists.

## Build

```
python3 shot_report.py <industry>        # capture the scored report
python3 build_deliverable.py <industry>
```

## The law

- **The deliverable is the filled scored report**, reached through the prototype's own
  `jumpToReport`, the same path its "Skip to a filled report" button uses.
- **Capture is headless Chrome at 2x.** Deterministic, no window chrome, no cursor, retina sharp,
  free to re-shoot after any edit to the asset. you chose this over a driven browser.
- **Nothing in `build/` is modified.** The rig copies the prototype to a temp file *inside*
  `build/` so relative assets still resolve, appends a bootstrap script, shoots, and deletes it.
- **This is the only white card in the house.** Deliberate: it is the one bottom-of-funnel-shaped
  cell in a set of curiosity hooks, and a white page reads as a document rather than an ad.

## Variation is in the presentation, not the copy

Seven cards, one format. What moves per industry in `build_deliverable.LOOK`: the rotation angle,
the capture width, the shadow depth, how far the arrow travels, and whether the deliverable is a
single sheet, a stacked pair or squared up flat. Seven cards that are recognisably one format and
not one image.

## Traps already paid for

- **The Systems Audit report is 56,313px tall at 1200 wide.** Dropped whole onto a 1080x1350 card
  that is a 1:47 sliver with nothing legible in it. `SECS = 0` cuts above section 01, which keeps
  the score head, the topline and the CTA bar and nothing else.
- **The report reveals its blocks on scroll.** Screenshotting at exactly the cut height returned a
  card with the score on it and nothing else, because everything below the capture viewport's
  fold was still at opacity 0. Shoot at a tall viewport, then crop the top off the result.
