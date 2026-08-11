---
name: static-ads-presentations
description: F7 sub-skill router. The eight card presentations built and picked during the 2026-08 static suite, each one canonised as its own sub-skill with its citation, its gates and its renderer. Use when a static format has approved copy and needs a presentation, when you asks to "build it in each shape", or when reusing one of the shipped looks (news banner, would-you-rather, inbox, apology letter, search sheet, ticked rows, ruled pad, comparison table). Read formats/static-ads/SKILL.md first for the shared law.
parent: static-ads
---

# F7.7 Presentations, the shipped look bank

`../SKILL.md` routes by **how the card is made** (type-led, plate-led, ui-mock, hand-drawn, proof,
lead-magnet). This layer routes by **what the card looks like when it is finished**. Every entry
here is a presentation that was built, rendered, put in front of you and either shipped to the
CRM or is sitting in front of him now. Nothing in this folder is a proposal.

**Why it exists.** The suite's copy was finished everywhere and presentation was the only
bottleneck, so the same question kept being answered from scratch: what does this card look like.
Each of these was paid for once, in real defects on real renders. They are written down so the next
format picks a shape instead of inventing one.

---

## 1. The eight

| Presentation | Cites | The mechanism | Bed | Renderer | Status |
|---|---|---|---|---|---|
| **`news-banner/`** | `local:a competitor-8-statics/06-editorial-headline-still` | A report about the reader's market, not a message to the reader | plate, full bleed | `f5_variants.build_news` | LIVE on the CRM |
| **`would-you-rather/`** | `local:a competitor-8-statics/05-would-you-rather` | A forced choice with a rigged pair, answered before the CTA | black | `f5_variants.build_rather` | LIVE on the CRM |
| **`inbox/`** | `local:a competitor-8-statics/04-inbox-screenshot` | Trespass. Mail addressed to somebody else | mail chrome | `f5_variants.build_inbox` | LIVE on the CRM |
| **`apology-letter/`** | `local:a competitor-8-statics/03-apology-letter` | The frame swap. An apology promises information, so the body argues while the reader is still reading the apology | warm paper | `f5_variants.build_apology` | LIVE on the CRM |
| **`search-sheet/`** | `local:a competitor-6-formats/03-search-bar` | Self-diagnosis. The reader has typed one of those lines themselves | black, white sheet | `f6_variants.build_search` | LIVE on the CRM |
| **`ticked-rows/`** | `tpl:Frame 466` | Headline held at the top, evenly ticked rows carrying the bottom | creased paper | `f6_variants.build_rows` | LIVE on the CRM |
| **`ruled-pad/`** | `arch:S14`, `arch:S5` | Written by hand on lined paper, every line sitting on a rule | aged ruled paper | `f6_variants.build_hand`, `f7_variants.build_board` | F6 LIVE, F7/F33 awaiting the pick |
| **`comparison-table/`** | `tpl:image 9.png` | Two headings over two tinted columns, the pairing carried by a grid | black | `f7_variants.build_table` | awaiting the pick |

Seven rows are on the CRM as of all tagged `suite-static`: four `f5-variant` and three
`f6-variant`, all status `ready`, read back with `crm_f5_variants.py --status` and
`crm_f6_variants.py --status`.

## 2. The method that produced all eight, and the one to repeat

Proven four times now, on F5, F6, F7 and F33. Repeat it exactly.

1. **Take the approved copy as fixed.** Every shape carries the SAME copy from `suite_copy.py`, so
   the only variable down the page is presentation. A shape that needs its own wording is a second
   format, not a presentation.
2. **Build one card per transferable shape from the reference bank.** Industry-agnostic, free,
   nothing paid and nothing pushed.
3. **Put them side by side in an HTML dossier**, each card beside its own reference and its own
   gate. `f7_review.py` is the cleanest of the four and the only one that carries two formats on
   one page.
4. **you picks by looking.** Do not describe the options in chat, and do not spend a credit
   before he picks.
5. **The picked shape rolls out to the seven verticals**, then a `crm_*_variants.py` copied from
   `crm_f6_variants.py` pushes it (INSERT only, dry by default, writes a REVERSE file).

## 3. What binds every presentation here

- **The citation law.** Every shape declares `MODEL[shape] = (id, what we take from it)`, the id
  resolves through `refs.py`, and the second half names the principle rather than repeating the id.
  The gate runs before anything renders.
- **Look at the render.** Read the output PNG and confirm the named change landed. Every defect in
  this folder was invisible in the code and obvious on screen.
- **Rendered, never photographed.** Paper, creases, rules and chrome are drawn in the browser, so
  every surface is one line to change and none of it costs a credit.
- **Fixed tables, never `Math.random`.** A random renderer means the version you approved is not
  the version that rebuilds.
- **`../proof/SKILL.md` is absolute.** No invented quote, rating, result figure or composite client
  on any of these cards.
- **`context/language-rules.md`** binds every house-facing word on all of them.

## 4. The recorded exceptions

These presentations each break something written down, and each break is your call rather than a
drift. They are listed here so nobody "fixes" them.

| Break | Where | Whose call |
|---|---|---|
| The card comes off black | `apology-letter/`, `ticked-rows/`, `ruled-pad/` | you, |
| The band law is set aside for a banner | `news-banner/` | you, |
| Brand furniture on a hand-made card, against `../hand-drawn/SKILL.md` section 2 | `ruled-pad/` (F6 hand) | you, |
| A negation swap in the copy | `inbox/` | your dictated wording, unruled |
| The copy is not the approved sentence verbatim | `inbox/`, `news-banner/` | recorded at each renderer |
| No route on the card at all | `would-you-rather/` | shipped knowingly |

## 5. Related

- `../SKILL.md` section 0, the layout law every one of these either keeps or is recorded as breaking
- `../hand-drawn/SKILL.md`, which binds `ruled-pad/`
- `../ui-mock/SKILL.md` section 3, no interface branding, which binds `inbox/` and `search-sheet/`
- `../../../references/scripts/a competitor-formats-teardowns-.md`, the six format verdicts
- `../../../references/canon/objection-bank.md`, where contrast copy is sourced from
- `.claude/handovers/static-suite.md`, live status for the suite
