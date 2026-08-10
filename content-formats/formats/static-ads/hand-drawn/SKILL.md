---
name: static-ads-hand-drawn
description: F7 sub-skill. Deliberately low fidelity: marker, pen, paper, whiteboard, phone snapshot. Owns the rules that keep low fidelity readable rather than sloppy. Use for the napkin, the whiteboard explainer, and the ultra low-fi static. Read formats/static-ads/SKILL.md first for the shared law.
parent: static-ads
format: F7.4
---

# F7.4 Hand-drawn statics

The card looks like it was made in thirty seconds by the person talking, which is why it gets read
before it gets classified. Low fidelity is a decision the card has to make on purpose and hold
completely, because half-polish reads as a mistake.

**Read `../SKILL.md` first.** This sub-skill breaks the band law by design, recorded on 2026-08-06
for this test. A drawing cannot live inside a bottom type band.

**Cost: free first.** All three render as drawn artwork before anything is photographed. Only the
ultra low-fi look has a paid plate authorised, and it stays unshot until the free version has been
looked at.

---

## 1. The three formats

| Format | Archetype | The argument | Funnel | Plate |
|---|---|---|---|---|
| **Napkin** | S5 | The owner's own medium: one sum, worked in pen | TOF | rendered, free |
| **Whiteboard explainer** | house | The process drawn once, the break circled | TOF | rendered, free |
| **Ultra low-fi** | house | A screenshot-grade card with no craft at all | TOF | new plate, paid, unshot |

Cell assignments: `../FORMAT-GRID.md` section 2. **The napkin goes to construction / double-handling**
because pen and paper is that owner's own medium and the pain is two copies of one docket.

## 2. Commit to the fidelity

- **One medium per card.** Pen on a napkin, marker on a whiteboard, or a flat screenshot. Mixing a
  clean typeset headline into a hand-drawn card kills both.
- **Legible beats authentic.** A real scrawl at thumbnail size is a grey smudge. The handwriting has
  to be loose and readable at 440px wide, which is the contact-sheet size and the honest view.
- **Imperfection is deliberate and sparse.** One correction, one crossed-out figure, one wobbly
  underline. Repeat the trick and the card reads as designed-to-look-undesigned, which is worse than
  clean.
- **No logo, no brand colour panel, no CTA button.** The moment brand furniture appears the card is
  an ad again. The blue accent is allowed as one mark, and only where a pen would plausibly make it.
- **Nothing in the frame that a napkin or whiteboard would not carry**, which rules out a masthead,
  a star row and a stock photo.

## 3. The three, specifically

**Napkin.** One arithmetic that the owner has done in their head and never on paper. The sum is the
argument, so the numbers have to be grounded in the playbook's raw-evidence table and the scope has
to hold: one discovery call says one business, never an industry. It is drawn artwork rather than a
photograph of real paper, so nothing about it needs a paid still.

**Whiteboard explainer.** The process the reader already runs, drawn once, with the break circled.
Four boxes maximum. The circle is the only accent. This is the one hand-drawn card that can carry a
second idea, and it still should not.

**Ultra low-fi.** No craft, on purpose: system font, flat background, a screenshot's worth of
character. The authorised paid plate for it is a screenshot-grade, phone-flat look with no film
character at all, which is the opposite of the VHS house look and the reason it needs its own job.
Render the free version first and only shoot if the free one is not flat enough.

## 4. Writing the copy

Handwritten copy is speech. Short, contracted, lower case where a person would write lower case, and
no marketing cadence. The pain comes from the playbook's verbatim call quotes.

**The avatar is named on the card**, in the heading of the napkin sum, the title on the whiteboard,
or the first line of the low-fi card. Parent `SKILL.md` section 2. **The card lands a question or a
claim**, and a napkin sum is a claim only when the total is stated.

**Sentence case or the writer's own natural case.** All caps is the news-carousel doctrine and it
does not travel here; nobody hand-letters a napkin in caps.

House floor still applies in full: no em dashes, no negation swap, banned vocabulary, house
terminology. A hand-drawn card is not exempt from the language rules because it looks casual.

## 5. Building it

No template exists yet. The route is HTML, CSS and inline SVG rendered by the same headless Chrome
path `band.py` uses, with a handwriting face and drawn strokes as SVG paths. Keep each medium as its
own template function so the napkin's paper and the whiteboard's surface are reusable.

**Do not generate a hand-drawn card as an image.** Text generated inside an image is the one thing
the house rules never allow, and a generated scrawl also cannot be corrected.

## 6. QA

- Read it at 440px wide before anything else. If a word is unclear there, the card fails.
- One medium, one accent, no brand furniture.
- Numbers grounded and scoped, sources recorded, funnel label recorded.
- Em dash scan, negation-swap scan, banned vocabulary, house terminology.
