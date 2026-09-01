# The static format bank, everything we have

Pulled from the canonical sources only: `SKILL.md` (the F7 router, sections 0-3),
`FORMAT-GRID.md` (the 20-cell grid + build status via `inventory.py` GRID),
`references/hooks/HOOKS.md` Part A1 (the archetype set), `references/scripts/archetypes.md`,
`references/FIGMA-PICKS.md`, and the rendered output directories under `scripts/out-*`.

**35 distinct static formats.** 12 are built, 23 are not.

> **The reference layer is the 41 Figma extracts in
> `context/advertising/static-ads-bank/templates/` and nothing else.** The scraped Meta and
> LinkedIn swipe banks were pulled out on and moved to
> `Archive/old-context/static-ads-swipe-banks-/`. Do not re-scrape or cite them.

---

## 1. `type-led` , words on black, no photograph (10 formats)

Owns the band law, the fit solver, one justified block, one blue accent.
Tier A renders on the existing rig today. Tier B holds the band geometry but needs a rows-or-columns
template written against `band.py` first.

| # | Format | Archetype | Funnel | Status |
|---|---|---|---|---|
| 1 | Band (one justified block, bottom 506px) | house default | TOF | **BUILT**, 5 industries |
| 2 | Problem / solution split | S2 | MOF | Tier A, renders today |
| 3 | Question hook | S12 | TOF | Tier A, renders today |
| 4 | Don't hire this person | S6 | TOF | Tier A, renders today |
| 5 | Stop trying to use AI (one enormous statement) | S9 | TOF | prototype in `out/` |
| 6 | The checklist static ("Eight problems. One hire.") | S14 | TOF | prototype in `out/` |
| 7 | Us vs them | S11 | MOF | Tier B template needed |
| 8 | PSA comparison split | Figma `PSA 4` | MOF | Tier B template needed |
| 9 | Numbered listicle / tick rows | Figma `5 - 1x1` | BOF | Tier B template needed |
| 10 | Founder statement card (a founder) | , | MOF | verbatim statement, then Tier A |

S14's original line was "These aren't eight problems", which is the banned negation swap. Canonical
line is now **"Eight problems. One hire."**

## 2. `plate-led` , a photographic plate carries the frame (7 formats)

Owns plate composition and the de-text pass. Every one of these has a VHS plate already on disk.

| # | Format | Archetype | Funnel | Status |
|---|---|---|---|---|
| 11 | News headline | S1 | TOF | prototype in `out/` |
| 12 | Advice / advertorial static | V11 | TOF | template needed, plate exists |
| 13 | Editorial masthead embed | Figma `Ad 104/107/18` | TOF | template needed, plate exists |
| 14 | Annotated hero, leader lines | Figma `Ad 111/13` | BOF | SVG overlay needed, plate exists |
| 15 | Long-form native article static | S13 | TOF | template needed, plate exists |
| 16 | Before and after (one plate, two grades) | S10 | MOF | two grades of one VHS plate |
| 17 | Big quote plus star row | , | MOF | testimonial capture, plate exists |

Masthead embed is gated: **only a masthead house has genuinely appeared in.** A fabricated masthead is
a fabricated endorsement.

## 3. `ui-mock` , imitates an interface the reader already trusts (3 formats)

| # | Format | Archetype | Funnel | Status |
|---|---|---|---|---|
| 18 | iMessage / WhatsApp chat | S3 | TOF | renderer needed, free |
| 19 | Organic post screenshot | S15 | TOF | renderer needed, free |
| 20 | Comment reply ad | , | TOF | renderer + **1 paid plate**, authorised, unshot |

Invented names only, never a real client. The comment reply's Figma donor (`image_41`) works
because the comment is real, so that cell is gated on a real comment.

## 4. `hand-drawn` , deliberate low fidelity (3 formats)

| # | Format | Archetype | Funnel | Status |
|---|---|---|---|---|
| 21 | Napkin ("stop doing XYZ" / "hire a house instead") | S5 | TOF | renderer needed, renders free first |
| 22 | Whiteboard explainer | , | TOF | renderer needed, renders free first |
| 23 | Ultra low-fi static (screenshot-grade, phone-flat) | , | TOF | **1 paid plate**, authorised, unshot |

Napkin and whiteboard render as drawn artwork before anyone pays for a photograph of real paper.

## 5. `proof` , a content gate, not a renderer (1 format unique to it)

Real attributed quotes only. Overlaps `type-led` and `plate-led` on which words may appear.

| # | Format | Funnel | Status |
|---|---|---|---|
| 24 | Quote-card grid (3 real construction clients) | MOF | testimonial capture, then Tier B |

Casting: H&L Construction, Vitale Projects and Northwear go on construction. Hive Property goes on
real estate. Financial services has no client on the site and takes the founder statement instead.
Kasun D is candidate-side and stays out of employer-facing cards entirely.

## 6. `lead-magnet` , closes on one of the seven built magnets (5 formats)

**All five BUILT across all seven industries, 35 cards, all shipped and live board.** Roughly 63 paid
`your image model` jobs spent. Every plate is shot, so all five re-render free from here.

| # | Format | Sub-skill | Paid plates |
|---|---|---|---|
| 25 | F-M1 Before / after split screen | `split-screen/` | 2 per industry, all 14 shot |
| 26 | F-M2 Deliverable shot (headless Chrome on the real report) | `deliverable-shot/` | none, ever |
| 27 | F-M3 Newspaper front page | `newspaper/` | 1 per industry, all 7 shot |
| 28 | F-M4 Filmed billboard | `billboard/` | 1 per industry, all 7 shot |
| 29 | F-M5 Caution card | `caution-card/` | 2 total, both shot |

## 7. Built one-offs and locked looks, outside the grid (6 formats)

| # | Format | Where | Status |
|---|---|---|---|
| 30 | News-collage keeper, band treatment | `out-news/*-band.png` | **BUILT**, LOCKED canonical |
| 31 | News-collage keeper, torn-clipping treatment | `out-news/*-clip.png` | **BUILT**, LOCKED canonical |
| 32 | Watercolour window | `out-noirreal/` | **BUILT** 5 industries, LOCKED plate-led |
| 33 | Consultant vs house card | `out-white/versus-*.png` | **BUILT** 5 industries |
| 34 | house in the cubicles card | `out-white/admin-*.png` | **BUILT** 5 industries |
| 35 | Retro one-off (double-handling) | `out-retro/` | **BUILT**, 1 card |

The five news-collage keepers are the only cards in the industry set finished end to end: plate,
cutout, editorial bed, tear and type.

---

## 8. The Figma reference layer, 41 extracts ranked

`references/FIGMA-PICKS.md`. Forty scaffolds reviewed one by one against a single test: **house has no
product to photograph**, so the scaffolds that transfer are the ones whose argument survives the
product being removed. **Fourteen of the forty fail that test outright.**

**Tier 1, build these five.** Four of the five need no image at all.

1. `VetNotes Static Ads .png` , the B2B service card. The closest thing to house in the library.
2. `image_9.png` , the two-column comparison table.
3. `PSA 4.png` (+ the 9x16 cut `PSA 1-9x16.png`) , the PSA split.
4. `Frame 466.png` , the editorial headline plus ticked rows.
5. `Power 3 - 1x1.png` , the italic statement plus a 2x2 tick grid.

**Tier 2, build after the first five.**

6. `Ad 104/107/18.png` , publication masthead, headline in the publication's voice, photo below.
7. `Ad 25.png` , boxed kicker, headline, photo well, three stacked benefit bars.
8. `5 - 1x1.png` , numbered list, circled numerals, sentence case, nothing else.
9. `43.png` / `43-1.png` , question headline, answer clause, three pill benefits over a photo.
10. `Ad 111.png` / `Ad 13.png` , photo with benefit pills around it, stars above. Stars only if real.

**Tier 3, only with real material.**

11. `Imessage.png` / `Frame 437.png` , iMessage chrome. Invented names only.
12. `image_41.png` , needs a real comment.
13. `Ad 106.png` / `Ad 108.png` , call-out arrow plus a big testimonial. Gated by `proof/`.

**Copy the structure. Never the words, and never a competitor's claim.**

---

## 9. In the hook bank but not cast to a layout

From `references/hooks/HOOKS.md` A1. These are copy lines with no assigned renderer.

- **S4 IG story responses** , **BANNED** unless the reactions are real. Fabricated testimonials are
  the one thing that gets an account penalised, and trust is existential for this brand.
- **S7 The most wanted hire** , "The most wanted hire in Australia just dropped in price."
- **S8 Did you know** , "Did you know... you don't need to use AI in your [avatar] business."
- **S16 Carousel** and **S17 Webinar carousel** , carousels, not statics. Out of scope for F7.

---

## 10. The law that binds all 35

- **The band law** (`SKILL.md` section 0: every mark in the bottom 506px.
- **Recorded deviation, this test only:** native mocks may break the band, because an iMessage
  thread, a tweet screenshot or a photographed napkin cannot exist inside a bottom type band, and
  breaking it is the point of the test. Breaking it: iMessage, organic post screenshot, napkin,
  whiteboard, ultra low-fi, comment reply, editorial masthead embed, annotated hero.
- **Funnel position is decided before the creative.** A format is good or bad *at a position*. A
  cell can only be read against others at the same position. Current spread across the 20-cell
  grid: 11 TOF, 7 MOF, 2 BOF.
- **Feature call-outs only work at bottom of funnel**, so the two Figma-derived cells are both BOF,
  never cold.
- **Hooks are FILLED from `references/hooks/HOOKS.md`** with the id cited, never free-written.
- **house language rules bind every word**: construction business never building business, hospitality
  business never venue, trades not building services, "AI agent" in full where the industry already
  uses "agent" for a person. No em dashes. No negation swap.
- **One paid job at a time, never batched. Construction end to end first, shown to you, before
  anything is paid for on the other six.**
