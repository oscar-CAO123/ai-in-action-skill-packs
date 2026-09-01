---
name: static-ads-search-sheet
description: Presentation sub-skill. A phone search-suggestion sheet on black, one typed stem completed five ways, each completion a pain. Use when a symptom stack should read as self-diagnosis rather than as a claim. Shipped as the F6 search variant, shipped and live and the strongest of the three. Read formats/static-ads/presentations/SKILL.md, formats/static-ads/ui-mock/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: local:a competitor-6-formats/03-search-bar
renderer: scripts/f6_variants.py build_search
---

# Search sheet

**The mechanism.** Self-diagnosis. The reader has typed one of those lines themselves, so five of
them stacked under one stem says the five are one problem before the card has claimed anything.
The interface authenticates and the list argues.

you picked this as the strongest of the three F6 shapes.

## 1. What is taken from the reference

`local:a competitor-6-formats/03-search-bar`: the suggestion sheet, matched closely. A rounded white
card on black, a status row, a label, the typed stem in a grey pill, then the completions, each
one repeating the stem in dark type and finishing it in grey.

**The stem/completion split is the whole thing.** Dark stem, grey completion, is what makes five
lines read as one query rather than as five sentences.

## 2. The gate that cannot move

**"Suggestions", never the platform's name.** `../../ui-mock/SKILL.md` section 3 bans interface
branding outright, and a platform's name on a house ad would also read as an endorsement, which is a
policy problem as well as a trust one. Everything else about the chrome is matched: the sheet
radius, the status row, the grey pill, the magnifier at the left of every row and the arrow into
the field at the right.

**The face is the platform's system stack, never your display typeface.** A suggestion sheet set in your display typeface stops
reading as a screenshot, and reading as a screenshot is the entire mechanism.

## 3. The stem is where the copy problem lives

The shipped stem is **"why is my business"**, and each completion finishes it with one pain.

**your ruling, binds every future card of this shape:** the suite's pain
lines are written for a card speaking TO the owner, so the owner is the actor and "you" is the
object ("still running every decision through you"). Put "why is my business" in front of one and
**the business becomes the actor**, which reads as "my business runs decisions through me" and
personifies a thing that has no hands. His words: "that's personifying the business in a way that
we don't want ... rephrase the pain points so they actually make sense in the context of what we
are describing, which is an amorphous thing, the business."

**So a completion is written for the business as the subject, and a pronoun swap is not the
rewrite.** `f6_variants.me` (your -> my, you -> me) is the FALLBACK only and it leaves the
personification fully intact.

**The five agnostic completions are hand-written and the seven verticals are NOT.** Each vertical
still needs its own search column, written for the business as the subject, before its card ships.
This is the outstanding item on the format and it is written into the card's `notes` on your content store
row.

## 4. The trap that cost three passes

**`scrollWidth` does not report a flex container's inline overflow.** Every row in the sheet
reported 872 (the container's own width) while the type ran 100px past it, so the shared fit passed
at every candidate size and the text ran under the arrow.

**Measure `getBoundingClientRect.right` on the text itself**, against the arrow's own left edge,
in page coordinates. `f6_variants.FIT_SEARCH` is that search.

Two related traps in the same card:

- **`clientWidth` counts padding and `scrollWidth` counts the left inset back in.** Padding on the
  element being fitted bottoms the search out at its 8px floor. Put it on a wrapper.
- **The arrow is absolutely placed with an EMPTY FLEX SPACER holding its width open.**
  `margin-left:auto` ragged the arrows across three x positions, because a nowrap flex item cannot
  shrink. Taking the arrow out of flow fixed the alignment and broke the fit, because Chrome leaves
  a container's end-side padding out of `scrollWidth`. The spacer is inside the flex line, so it
  counts.

## 5. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 f6_variants.py search                    # agnostic, free
python3 f6_variants.py search --industry retail  # one vertical
python3 f6_review.py                             # the dossier, beside its reference
python3 crm_f6_variants.py --status              # the live rows, read off the board
```
