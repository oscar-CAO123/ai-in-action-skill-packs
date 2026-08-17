---
name: static-ads
description: Use when you says "static ad", "single image ad", "Meta static", "make some statics", "static ads for [avatar]", or wants one-image house ad creative rather than video or a carousel. The F7 router. Routes to one of five production sub-skills (type-led, plate-led, ui-mock, hand-drawn, proof) and carries the law they all share: the band, the copy rules, the swipe bank, the funnel label. Format F7 in angles-and-formats.md, the paid-first volume format.
canonical: true
format: F7
router: true
---

# Static Ads (F7), the router

One image, one idea, one accent. The cheapest unit of house creative and the fastest way to test a
pain against a hook before anything gets a runtime.

Production economics are why this format exists. An image costs roughly $50 to make and returns
roughly $300; a video costs roughly $500 and returns roughly $400. **Whenever a static can do the
job of a video, use the static.** Top-of-funnel statics hold $500k+ in lifetime spend in the swipe
bank, so treating statics as bottom-of-funnel is a habit rather than a rule.

**When to pick this format:** paid-first placements, fast pain by hook testing at volume, and
retarget variants off a winner. It is also the validation step before a concept earns a video slot.

This file is a router plus the law every sub-skill inherits. **Read this file, then exactly one
sub-skill.** The sub-skills split by how a card is produced, which is what actually differs between
formats; the words, the band and the evidence rules are the same everywhere and live here.

---

## Router: pick the sub-skill by how the card is made

| Sub-skill | Reach for it when | Formats it owns |
|---|---|---|
| **`type-led/`** | The card is words on black. No photograph, no interface, no drawing. | band, us vs them, problem/solution split, question hook, don't hire this person, PSA comparison split, numbered listicle and tick rows, founder statement |
| **`plate-led/`** | A photographic plate carries the frame and the type is laid over or under it. | advice / advertorial static, editorial masthead embed, annotated hero, long-form native article, before and after, big quote plus star row |
| **`ui-mock/`** | The card imitates a real interface the reader already trusts. | iMessage chat, organic post screenshot, comment reply ad |
| **`hand-drawn/`** | The card is deliberately low fidelity: marker, pen, paper, phone snapshot. | napkin, whiteboard explainer, ultra low-fi |
| **`proof/`** | Any card that puts a real client's words or name on the frame. | quote-card grid, big quote plus star row, founder statement |
| **`lead-magnet/`** | The card closes on one of the seven built lead magnets. Five fixed formats, one per hook, filled across seven industries. | before/after split screen, deliverable shot, newspaper front page, photographed pop-art comic, caution card |
| **`presentations/`** | The copy is approved and the card needs a LOOK. Eight presentations already built, picked and mostly shipped, each with its citation, its gates and its renderer. | news banner, would you rather, inbox, apology letter, search sheet, ticked rows, ruled pad, comparison table |
| **`../permission-carousel/`** | The unit is a CAROUSEL rather than a card: full-bleed fifties photographs, thin your display typeface set into space composed into the plate. Two mechanisms (permission then turn, promise then payoff) and two lengths (two slides, or seven). your favourite format in the batch. | F8 the permission carousel (live), F9 the numbered listicle at full length |

`proof` is a content gate rather than a renderer. It says which words may appear on a card and how
they are cast. It runs **in addition to** whichever of the first four renders the card, never
instead of one.

`presentations` is a second axis rather than a sixth renderer. The first six route by **how the
card is made**; that one routes by **what it looks like when it is finished**, and every entry in
it is a look that has already been built and put in front of you. Reach for it before inventing
a shape, and read `presentations/SKILL.md` section 2 for the method that produced all eight.

The current assignment of all 20 industry cells to formats, with funnel labels and the plate budget,
is `FORMAT-GRID.md` in this folder. That grid is the build spec; this file is the law.

**Which model makes the plate: `../../references/canon/model-routing.md`.** Two of these
sub-skills now have a lane in that table. `hand-drawn/` and any phone-snapshot card are the
retro and authentic shot type, so they go to **your cinematic model** (`soul_cinematic`). `plate-led/`
plates where the composition itself is the design (an editorial masthead, poster-style key art)
go to **your design model** (`gpt_image_2`). Everything reference-conditioned stays on
`your image model`.

**The ratio trap.** This canvas is 1080x1350 and neither `soul_cinematic` nor `gpt_image_2`
offers 4:5. Generate those at 3:4 and crop to the canvas, or keep the card on `your image model`,
which has a native 4:5. **The band is never generated.** It is rendered in PIL by
`scripts/band.py` and no model touches it, so a generated plate is only ever what sits behind.

---

## 0. The layout law, applies to every house static)

**Every mark lives in the bottom 1.5/4 of the frame.** At 1080x1350 that band is 506px tall with
its top edge at y=844. Nothing renders above that line. The band is the whole design.

**The band carries one block of type and nothing else.** One size per card, white, with a
single blue accent. No kicker, no standfirst, no second tier, no rules, no logo. A grey secondary
tier is what made earlier passes read small, so there is no grey.

**The face is a theme, not part of the law.** `scripts/band.py` `THEMES` holds the face, weight,
transform, tracking, leading and accent for each direction, and `render_card(..., theme=)` picks
one. Two are live: `anton` (condensed, blue accent) and `noir` (**your display typeface 200**, blue accent, 0.02em
tracking, `anno_weight` 300), which the news-carousel format moved to on to sit on the
locked design system's display weight. A theme changes the face and the case; the band geometry, the
justification and the one-size-per-card fit are the law and hold across all of them.

**ALL CAPS IS THE NEWS-CAROUSEL DOCTRINE, NOT THE HOUSE DOCTRINE.** Caps belong
to the F5 news-carousel band and the five band keepers that inherit it. **Every other static sets
sentence case by default.** your display typeface is the house face and it is usable across all twenty formats; the
uppercase transform is not. A format that sets caps because the rig defaults to caps is a bug rather
than a decision. `THEMES[...]["transform"]` is what changes, and a sentence-case theme is the right
way to do it rather than pre-casing the copy string.

Twenty formats set in one face at one case is the failure this test exists to avoid. **If the reader
cannot tell two cells apart at thumbnail size, the test returns nothing**, so case, weight and
measure are part of what varies between formats.

**The block is set flush on both margins and fills the band.** Every line runs the full safe width
(x64 to x1016) and the stack fills the band top to bottom. Line breaks are a fit decision made by
the renderer, not an authoring one: `lines` in `ads.py` is copy, and the rig re-breaks it.

How `scripts/band.py` implements it, and the traps already paid for:

- The renderer walks the candidate line counts, scoring each on how much of the band it fills
  minus how uneven the line widths are, then keeps the best. Chasing fill alone crams in lines and
  blows out the tracking; chasing evenness alone collapses to two lines and an empty band.
- Justification goes into the **word gaps** first, capped at `WORD_GAP_MAX` of the type size, and
  only the remainder into letter-spacing. Opening the letters inside a word is the thing that
  reads as broken.
- **`document.fonts.ready` is not enough on its own.** The card starts with an empty copy div, so
  nothing has requested the face and the promise resolves instantly against fallback metrics, which
  are about 1.4x wider and silently undersize every card. The fit waits on
  `document.fonts.load('<weight> 100px "<family>"')` first. Do not remove that, and do not drop the
  weight from it: a theme whose face only ships at 200 and 300 gets no match on a bare 400 lookup,
  which puts the trap straight back.
- Widths are measured on an inline-block span inside each line, never on the line div, which is
  always the full column width and reports zero slack.
- `LH` is 0.95 and the leftover height goes into even gaps between lines, capped at `GAP_MAX`.
  Tighter leading collides with the ink Anton hangs below the baseline.

### The recorded deviations this test only)

you ruled that the format test may break the band law where the format cannot exist inside a
bottom type band. Two deviations are recorded, and both are scoped to this test:

1. **Native mocks break the band entirely.** An iMessage thread, a post screenshot, a photographed
   napkin or an annotated hero cannot live in the bottom 506px. `ui-mock` and `hand-drawn` own the
   whole frame, and the plate-led mocks (editorial masthead embed, annotated hero) break it too.
   Listed cell by cell in `FORMAT-GRID.md` section 3.
2. **Three type-led shapes keep the band but structure it.** PSA comparison split, numbered listicle
   and tick rows, and the quote-card grid put rows or columns inside the 506px band rather than one
   justified block. Geometry holds, the one-block clause does not. `type-led/SKILL.md` section 2
   governs what a structured band may contain.
3. **The news-collage keepers drop the band entirely and run top-and-bottom.** you, .
   The card is a full-bleed plate carrying three marks instead of one bottom band:
   - **A top your display typeface header** over a black top-down fade, "Breaking: [avatar] can finally stop
     [pain].", with a small uppercase CTA line under it naming that industry's lead magnet. This
     is the card's real hook. It sits in the **locked display weight, your display typeface 200, ls -0.025em**
     (`context/design-system/SCHEMA.md` section 2). An early pass set it in your display typeface Bold 700 and it
     stopped reading as house immediately, which is the exact failure that file names: nothing above
     600 exists in this system. The single blue accent lives here, on the pain clause.
   - **A black censorship bar over the subject's eyes**, replacing the pop-art sunglasses. Placed
     and angled by finding the lens colour on the plate, never a fixed offset.
   - **A smaller cut-out.** `collage_news.SUBJ_H` dropped from 0.88 to 0.75 to make the room the
     header needs. The cut-out is bottom-anchored, so that number is what sets where the crown
     lands: y=350. `clip.py` holds the matching budget (`HDR_BOTTOM` 330) and prints a warning if
     a card's header ever overruns it, because the two constants are only correct together.

   Two per-card mechanisms in `collage_news.py` exist because the plates are not interchangeable,
   and both are opt-in tables rather than blanket behaviour:

   - **`ALIGN_SITE`** puts the graded site plate through the SAME transform as the cut-out, so the
     plate's own copy of the subject lands exactly behind him. Construction needs it: that plate
     frames him on the right, the cut-out is centred, and his graded ghost stood beside himself.
     The plate is then at the subject's scale rather than cover scale, so its edges are clamped to
     fill the frame. `MIRROR_SITE` is the older workaround for the same fault; a card uses one or
     the other, never both.
   - **`KEEP_PROP`** restores a prop the human-segmentation matte dropped. Financial services needs
     it: her left forearm runs behind the desk paperwork, so the matte cut the arm to a ragged
     point in mid-air. The prop joins the alpha but NOT the person's box, so scale and anchor still
     come from the figure and adding a prop never resizes the person against the rest of the set.
   - **A torn newspaper clipping** in the bottom right, printed with the industry's own headline
     and standfirst in one black ink, because a newspaper prints one ink and the accent is already
     spent above.

   The engine is `scripts/clip.py`, the copy `scripts/build_news_clip.py`, and the paper itself is
   a paid i2i extract from `scripts/clip_paper.py`. Outputs are `out-news/*-clip.png`; the earlier
   `out-news/*-band.png` set is kept beside them. **There is no arrow.** One pointed at the subject
   off the paper's edge for several passes and was cut once the header carried the hook.

Outside this test the law is unchanged and one block is the house default.

## 1. The archetype set and where each one now lives

The archetypes are `skills/content-formats/references/scripts/archetypes.md` S1 to S16, plus V11 the
advertorial. They name the shape of the **words**, never the layout.

| Archetype | Shape of the argument | Sub-skill |
|---|---|---|
| S1 news headline | Borrows the authority of the news frame | `plate-led` |
| S2 problem / solution split | Stacked pains resolving into one answer | `type-led` |
| S3 iMessage chat | A thread the reader recognises | `ui-mock` |
| S5 napkin | The owner's own medium, pen on paper | `hand-drawn` |
| S6 don't hire this person | A reverse command the reader is already inside | `type-led` |
| S9 stop trying to use AI | One enormous statement, the compressed thesis | `type-led` |
| S10 before and after | The same frame twice, two states | `plate-led` |
| S11 us vs them | Category education by contrast | `type-led` |
| S12 question hook | Curiosity and confrontation. Needs the strongest line | `type-led` |
| S13 long-form copy static | Primary text does the work, the image earns the click | `plate-led` |
| S14 the checklist static | Pain stacking into one answer | `type-led` |
| S15 organic post screenshot | A personal post, not an ad | `ui-mock` |
| V11 advice / advertorial | Reads as an article, teaches before it sells | `plate-led` |

**S4 IG story responses stays out** unless the reactions are real. Fabricated testimonials are the
one thing that will get an account penalised, and trust is existential for this brand. See `proof/`.

**S14's original line is rewritten.** The archetype opened it with "These aren't eight problems",
which is the negation swap the house rules ban everywhere. The canonical line is now
"Eight problems. One hire."

## 2. The copy rules (every sub-skill)

**CALL OUT THE AVATAR ON EVERY CARD.** The reader has to see themselves named
before they read anything else. A card that opens on a pain with nobody attached to it is a card
about a general problem, and a general problem belongs to nobody. Name the industry plus the word
business, or the role, in the reader's own vocabulary: construction businesses, real estate
agencies, hospitality businesses, retailers, insurance brokers. `WHO` in
`news-carousel/scripts/decks_industry.py` is the list of record and `context/language-rules.md`
binds it.

This is the mistake the first Tier B prototypes made: the rows agitated real pains and named nobody,
so nothing in the frame told a retailer the card was theirs.

**AGITATE THE SPECIFIC PAIN, NEVER THE CATEGORY.** The card names what this avatar loses, in the
words they used on the call, taken from that industry's playbook. Generic operational pain is not
agitation.

**EVERY CARD IS A QUESTION OR A DECLARATIVE STATEMENT ABOUT THE PAIN**, whichever the format calls
for, and the format decides which. A fragment, a label or a naked noun phrase is neither, and it
gives the reader nothing to agree or disagree with.

The three above are one test applied together: **who is this for, what is it costing them, and what
is the claim or the question.** A card missing any of the three does not render.

**One idea per card.** A static that carries two ideas carries neither at thumbnail size.

**One blue accent, never two.** Mark it with `[[double brackets]]`. It goes on the number or the
role, whichever is the surprise. An accent can span two hand-broken lines and the renderer closes
and reopens the span across the break.

**Ground every number.** Figures come from `context/research-corpus/` (the industry playbook's raw-evidence
tables when the ad is vertical-specific, the theme page when it is general-pain) and
`context/personas/personas-and-avatars.md`, and get recorded in the ad's `source` field. Never invent
a number, never name a real company or person outside the `proof` gate.

**Scope discipline.** A figure from one discovery call says one business. A figure from a census or
an aggregate may be framed plurally. Promoting a firm figure to an industry figure because the
plural reads better is the error that cost the v1 news decks their re-render.

**Verify a pain's meaning against the playbook before rewording its clause.** The insurance card was
reworded this way on and the rewrite was right because the playbook's own angle carried
it. Do not skip the check.

**house terminology is canonical.** `context/language-rules.md` binds every word: construction
businesses never builders, hospitality business never venue, re-enter never re-key. Name the
reader's business by its industry plus the word business.

**The hook rules apply.** A naked capability line is not a hook, a question mark does not make a
hook, and anything a competitor could run unchanged is not a hook. Full doctrine and the five
grading criteria: `skills/content-formats/SKILL.md` section 7.

**House floor.** No em dashes, no negation swaps, banned-vocabulary clean, contractions on, one
owner addressed.

## 3. The reference layer

**The Figma layout library is the reference layer for F7. The scraped swipe banks are not.**
your call, .

**Start at `references/FIGMA-PICKS.md` in this folder.** Forty scaffolds from
`context/advertising/static-ads-bank/templates/`, reviewed one by one, ranked for house by a single
test: **house has no product to photograph**, so the scaffolds that transfer are the ones whose
argument survives the product being removed. Fourteen of the forty fail that test outright.

The five in Tier 1, in build order: the **VetNotes B2B service card** (the closest thing to house in
the library), the **two-column comparison table**, the **PSA split**, the **editorial headline plus
ticked rows**, and the **italic statement plus a 2x2 tick grid**. Four of the five need no image at
all. FIGMA-PICKS.md carries the house fill for each and the three rig changes they need.

**Copy the structure. Never the words, and never a competitor's claim.**

**Every format cites what it is modelled on, and the citation is checked.** `scripts/refs.py` resolves an id to its entry and opens the picture where there is one, and both
copy gates fail on a format whose `model` is empty or whose id is dead. The citable banks are
`hook`, `arch`, `tear`, `hex`, `tpl`, `local` and `style`. Run `refs.py` for what is in each,
`suite_copy.py --fmt <F>` to see one format's references with the file and line they live at, and
`sheet_fmt.py <F>` to draw them as a MODELLED ON strip above the cards for review.

**Three formats are uncited and cannot be generated until you picks their references:** F10
Founder statement, F17 Big quote and F24 Testimonials, all three proof-gated quote formats with no
archetype or scaffold in the bank that fits them.

**The scraped swipe banks are GONE from the reference layer.** Every scraped
Meta and LinkedIn record, the consolidators, the galleries and the derived taxonomy were moved to
`Archive/old-context/static-ads-swipe-banks-/` and are not a source of anything. Do not
re-scrape, do not rebuild them, and do not cite them. The reference layer is the 41 Figma extracts
in `context/advertising/static-ads-bank/templates/` and nothing else.

## 4. Funnel position is decided before the creative

a reference brand audits creative by funnel position before he judges the execution, because a format is good
or bad **at a position** rather than good or bad. Magic Mind scored 9 on bottom-of-funnel execution
and 6 on scalability for exactly this reason: bottom of funnel carries a spend ceiling.

**Label every card TOF, MOF or BOF at authoring time**, in the ad record, or the test cannot be read
afterwards. A card is only compared against other cards at the same position.

**Curiosity pulls the click, clarity closes the sale, and the landing page is where most statics fall
apart.** A curiosity card pointing at a page that does not teach immediately wastes the click. Full
doctrine: the static section at the end of `references/scripts/a reference brand-teardowns.md`.

**Feature call-outs only work at bottom of funnel**, which makes the annotated-hero shape a warm
shape rather than a cold one.

## 5. Running the rig

```
cd "the business/skills/content-formats/formats/static-ads/scripts"

# 1. add the ad to ads.py (slug, template, persona, angle, offer, funnel, source, copy)
python3 build.py                        # every ad
python3 build.py s9-own-it              # one ad
python3 build.py --out ~/Desktop/ads    # somewhere else

# 2. contact sheet
cd out && ffmpeg -v error -framerate 1 -pattern_type glob -i "*.png" \
  -vf "scale=440:550,tile=3x2:padding=10:color=#333333" -frames:v 1 sheet.png -y

# 3. review
open -a Cursor "$PWD/sheet.png"
```

`scripts/band.py` is the shared engine: `render_card(lines, png, plate=, overlay=, theme=)`. It is
the only renderer any sub-skill calls for a band, and `plate=` and `overlay=` are how a plate-led
card gets its image and its annotation layer. Chrome headless takes about 2.5s a card, so a batch of
twenty needs splitting across calls.

The industry set runs on its own rig at `formats/news-carousel/scripts/` (`decks_industry.py` for
copy, `plates_real.py` for plates, `build_industry.py` to render, `dossier_industry.py` and
`sheets_industry.py` for review). Commands are in the handover.

## 6. Testing doctrine (why volume is the point)

- **Fifteen hooks against two bodies beats two hooks against five bodies**, nearly always. Statics
  are how house buys that ratio cheaply.
- **A pain by hook matrix** is the batch unit: one pain, six archetypes, or one archetype, six
  pains. Both produce a real read on what the audience responds to.
- **Meta reads a different image as a different creative**, so a fatigued concept revives on a
  fresh archetype without rewriting the offer.
- **The portfolio model applies.** Many concepts clearing the quality bar, spend decides the
  winner, nobody predicts it. Diversity means new persona and angle concepts, never six versions
  of one line.
- **A format test needs a control.** The five band cards in `FORMAT-GRID.md` are it, and they were
  chosen for pain variety rather than by rank so the control group is not near-single-pain.

## 7. Gotchas (the shared renderer)

- **A headline line that is too long shrinks the whole headline**, because the fit is driven by the
  longest line. Re-break the lines rather than raising the cap.
- **Hand-break the sub line too.** `sub` and `standfirst` accept a list of lines as well as a
  string. A string auto-wraps and will orphan the last word. Two balanced hand-broken lines read
  better every time.
- **Type apostrophes as plain ASCII** in `ads.py`; the renderer escapes them.
- **`fit` is measured, not guessed.** If type comes back small, the copy is too long for the
  archetype, which is the copy telling you something.
- **Check the card at thumbnail size**, because that is where the auction sees it. The contact
  sheet is the honest view.
- Keep superseded versions rather than overwriting a named asset blind.

## 8. Related

- Build spec for the current set: `FORMAT-GRID.md` (this folder).
- Canon: `skills/content-formats/references/canon/angles-and-formats.md` (F7),
  `context/personas/personas-and-avatars.md`.
- Evidence: `context/research-corpus/INDEX.md`. Vertical-specific work starts at
  `context/research-corpus/industries/<slug>.md` (ranked pains with angles, language, targeting);
  general-pain work at `context/research-corpus/pains/<slug>.md`; objection beats at
  `context/research-corpus/objections/<slug>.md` and `references/canon/objection-bank.md`.
- Archetype source: `skills/content-formats/references/scripts/archetypes.md`.
- Static doctrine: `skills/content-formats/references/scripts/a reference brand-teardowns.md`, the static section
  at the end.
- Swipe bank and templates: `context/advertising/static-ads-bank/` (`README.md` records the method
  and how to refresh the pull).
- Copy craft, hook doctrine and the QA gate: `skills/content-formats/SKILL.md`.
- Terminology: `context/language-rules.md`. Design system: `context/your own brand tokens`.
- The carousel siblings when one frame is not enough: `formats/news-carousel/` (F5),
  `skills/best-time-carousel/` and `skills/webinar-carousel/` (F6).
