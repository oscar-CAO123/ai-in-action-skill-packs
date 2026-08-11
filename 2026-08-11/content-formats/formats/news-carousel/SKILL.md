---
name: news-carousel
description: Use when you says "news carousel", "news headline carousel", "breaking news carousel", "tabloid carousel", "pain carousel", or wants a house carousel built in the news-headline style. Builds a 4:5 carousel on pure black: a thin-your display typeface headline band under a hand-painted B&W noir machine plate. Format F5 in angles-and-formats.md, the canonical house carousel.
canonical: true
format: F5
---

# News Carousel (F5, the canonical carousel)

the house's breaking-news static, run as a carousel. A thin-your display typeface headline band on pure black, under a
hand-painted black-and-white noir plate of the machine world. The trust is borrowed from the news
format, so the type does almost nothing clever and the headline does the arguing.

This is the default static slot in the weekly seven. Any pain with a hard number routes here
first, and only goes to another format when the number will not carry a headline.

**Lineage:** static archetype **S1 News headline** in `skills/content-formats/references/scripts/archetypes.md`,
and the `News-Anchored Performance Ad` entry in the concept bank. The single-card original is
`projects/content-engine/ideas/news-headline/card.html`.

**The plate direction is canonical as of .** Photoreal stock plates are retired: they
were generic, they shared no world with anything else house makes, and they said nothing about the
build. The noir plate is the same painted world as the F2 films, so a carousel and a film teach
the same visual vocabulary. The retired photoreal
decks stay renderable in `decks_pains.py` and `plates.py` for reference; nothing new is built
there.

---

## Production spec (the worker and Claude Code both execute this)

```yaml
format: F5
skill: news-carousel
canvas: [1080, 1350]      # 4:5
slides: 5 (house-reveal arc) | 6 (pain arc, see section 1)
plate: your image model at 5:4, ~2 credits each, one job at a time
routing: ../../references/canon/model-routing.md   # house shot-type table. nano keeps this lane: it is the only model with a native 5:4. The band stays PIL, never generated
renderer: headless-chrome
fonts: [jost-200 (band)]                # the ONLY type on the card. your display typeface only. See section 2c.
theme: noir                             # band.py THEMES key. Anton is retired on this format.
layout: bottom-band law, see content-formats section 1 and static-ads section 0
density: every slide is a headline, about three lines, one idea
rig:
  build: skills/content-formats/formats/news-carousel/scripts/plates_noir.py    # CANONICAL, carousel
  copy: skills/content-formats/formats/news-carousel/scripts/decks_noir.py
  paid: scripts/build_industry.py + decks_industry.py    # single-card industry set, section 1a
  engine: skills/content-formats/formats/static-ads/scripts/band.py          # shared with the statics
  retired: scripts/plates.py + decks_pains.py (photoreal plates), build2.py + decks2.py (type only)
  legacy: scripts/build.py + decks.py                                    # v1 arc, 13 decks in out/
inputs:
  persona: personas-and-avatars id, or "general" for general-pain targeting
  angle: angles-and-formats.md A1-A12
  offer: house | ai-officer | ai-orchestrator
  figure: the number, with its pain-wiki or context/personas/personas-and-avatars.md provenance recorded
  scope: firm | industry            # what the figure is actually true of. See section 3.
  motifs: the noir motif vocabulary, noir-painterly SKILL.md phase 3. No board required.
  slides: headlines, about three lines each, written into decks_noir.py
steps:
  - write the headlines into decks_noir.py `slides`, with the long-form as provenance
  - write one painted scene per slide into `plates`, composed from the motif vocabulary
  - set `annotations` to a list of empty rows, one per slide. See section 2c.
  - python3 plates_noir.py <slug>          # generates missing plates, then composites
  - contact sheet, review in Cursor
qa:
  - em dash scan (must be zero)
  - negation-swap scan
  - banned vocabulary per content-formats section 1
  - scope check: every number carries the same scope the source supports
  - one blue accent per slide, never two
  - every plate comes back wordless; a plate with baked lettering is regenerated or de-texted
  - nothing drawn over the plate: no labels, no leaders, no logos
outputs: scripts/out-noir/<slug>/slide-01..NN.png, plates in scripts/plates-noir/<slug>/
```

---

## 1a. The single-card industry variant (canonical for paid

The carousel above is the organic format. The **paid** set is one card, and it retired the 22
general-pain noir carousels as the live set on .

**The shape.** Five industries, five pains each, 25 cards. Every card is one pain, targeted at one
industry, closing on that industry's own lead magnet. Sets never mix.

| Industry | Lead magnet (names the set and the destination, carried in the caption) |
|---|---|
| Construction & Trades | The Site-to-Profit Readiness Check |
| Real Estate & Property Management | The AI-Ready Agency Score |
| Hospitality & Food Service | The Wow Factor Audit |
| Retail & E-commerce | The Retail Ops AI Readiness Check |
| Financial Services & Insurance | The Broker and Adviser AI Readiness Check |

**Everything here is already written down, so nothing is invented.** The five industries are the top
five by call volume in `context/pain-wiki/INDEX.md`, and the same five
`projects/content-engine/ideas/industry-build-carousels/VERTICALS.md` maps. The five pains are the
top five ranked pains in `context/pain-wiki/industries/<slug>.md`. The magnet names are the ones
those playbooks and VERTICALS.md already carry. Never write a new pain or a new magnet name here:
add it to the playbook first.

**The magnet question a card lands on is not its position.** Each card carries an explicit `q`.
Construction and real estate happen to order their questions the same as their ranked pains;
hospitality, retail and financial services do not, and several magnets carry eight questions
against five or six ranked pains. Every `q` was read off its playbook and checked by hand. Re-check
them whenever a playbook's magnet changes, and never replace `q` with a positional lookup.

**The band template is locked.** Every card sets exactly one sentence:

```
AUSSIE <BUSINESS TYPE> ARE FINALLY REALISING THEY DON'T HAVE TO <PAIN> ANYMORE.
```

The business type is one plural per industry (`WHO` in `decks_industry.py`): Aussie construction
businesses, real estate agencies, hospitality venues, retailers, insurance brokers. **It must name
the vertical, never gesture at it** (you, : "hospitality venues" not "venues",
"insurance brokers" not "brokers". A bare noun reads as the wrong industry to half the feed. And
**never "Aussie builders"**, which is the audience sense of the word that `context/language-rules.md`
binds. The accent is the pain clause.

**No tail.** A "using AI" tail rode on every card for part of and you cut it the same
day. Do not put it back: the sentence lands on the pain, and naming the mechanism in the band answers
a question the card has not asked yet. What replaces the pain is the offer's job, not the hook's.

**The pain clause is a bucket, not a scene.** your call, against a first pass that was
too situation-specific. Name the pain the way the whole vertical carries it, in the fewest words that
still land: `MANUALLY QUOTE`, not `BURN WEEKS OF SOMEONE'S TIME ON A SINGLE TENDER`. Describe the
pain, never the action that produces it, and speak about the business rather than a person inside it.

Three tests before a clause ships:

1. Would it read true for every business in the vertical, not just the one that said it on the call?
2. Does it name an outcome the owner already feels, rather than a task they perform?
3. Does it fit the band in four or five lines?

If a clause needs a specific tool, a number or a time of day to make sense, it is a scene and it is
too narrow. Detail belongs in the dossier. Buckets repeat across sets on purpose (disconnected
systems, admin by hand and the owner bottleneck are the same pain in five verticals) and never
inside one set.

**Nothing is drawn over the plate.** A leader-arrow CTA reading `TAKE <MAGNET> TODAY` was tried on
and cut the same day, so section 2c holds on these cards as it does on the carousel: the
band is the only type. `arrow_overlay`, `subject_point` and `ARROW_TARGETS` stay in
`build_industry.py` with the rest of the annotation machinery and are not canonical.

**The magnet is therefore not on the card.** It still names the set and the destination, so it
belongs in the caption and the link. Putting it back in the band is a copy change to
`band_lines`, not a new layer.

**The rules that differ from the carousel:**

- **THE LOOK IS CANONICAL: VHS camcorder, house-wide, one style across all five industries.**
  Approved by you . `vhs-camcorder` from the **F8 plate-style bank**
  (`ideas/industry-build-carousels/styles.json`), generated by `plates_real.py` (prompt composed
  head + shot + body + brief + tail exactly as `gen_plates.py` does) and graded by the free
  `grade_plate.sh vhs` chain. This is the style of record for this variant. Do not cast a different
  stock per vertical here.
  - The first pass did cast per vertical (construction 16mm, real estate Betacam, hospitality Super
    8, retail VHS, financial services press flash, from `VERTICALS.md`). Five stocks made five rows
    that did not read as one campaign, and the press-flash row read as a different brand. The
    per-vertical cast is kept commented as `F8_VERTICAL_STYLES` because the 2x2 grid format (F8)
    still uses it. **That cast is F8's, not this variant's.**
  - **Re-grading is free**, so the look can be retuned off the raws without paying to shoot again:
    `plates_real.py <industry> --regrade`. Reach for that before authorising any re-shoot.
  - Two known costs of the VHS chain. It kills fine print (body text degrades to speckle, which is
    useful) but **leaves anything mid-size or larger fully legible**, so it is not a fix for
    incidental text. And its noise **pools into dark speckle blobs on flat lit surfaces** (ceiling
    panels, tabletops), which reads as grime. Lower the noise in the regrade rather than re-shooting.
- **Plates are real-world captures with no people in them** (you, . The painted noir
  plates came off. `NO_PEOPLE` is part of `compose` and says "the scene", not "the room", because
  briefs go outdoors.
- **Show the place the business actually is, not another desk.** you, after the first
  pass made four of the five keeper plates interiors of the same kind of room, so the set read as one
  office rather than five industries. A construction job site, a house from the street, a pub floor, a
  shop floor. The financial services lamp-lit ledger desk is the benchmark the others are graded
  against, and it is the one interior that stays.
- **A prop the copy needs may be composed into the scene, never laid over the plate.** The real
  estate keeper carries a large analogue clock entering frame from the left in front of the house,
  generated as a real object in the shot. Section 2c still forbids drawing anything on top.
- **The brief is a real scene with nobody in it.** An empty scene reads as the pain; a person in frame
  reads as stock.
- **Refine, never re-roll, once a frame is approved.** `plates_real.py --refine` runs image-to-image
  against the plate already on disk so the composition survives and only the named thing changes.
  That is how the carton lettering came off the construction headcount plate.
- **No figures on these cards.** The template's subject is plural and industry-wide, so any number
  riding on it widens one firm's quote into an industry claim, which section 3 forbids, and the
  sentence has no room to scope it. Nearly every playbook number is single-firm ("$150,000 a year",
  "40 to 60 hours", "a thousand clients"). Pain clauses are therefore qualitative and the figures
  live in the dossier as the evidence behind the card. A figure only returns if the sentence
  changes to carry its own scope.
- **Industry nouns do the targeting.** No card names its industry outright. Tender, rent roll,
  function proposal, wholesale PO, file note. That is how the playbooks talk.
- **Plates repeat across sets, never inside one.** The owner-bottleneck motif carries four of the
  five industries. Each set posts to its own audience, so the two never share a feed.

**Two traps the arrow already paid for:**

- **A white arrow disappears into the thing it points at.** The target is picked as the centre of
  mass of the plate's brightest paint, which on a tenebrist plate is the lit subject, so a plain
  white head lands white-on-white. Shaft and head are drawn twice, a soft black pass under a white
  pass, which carries the arrow over highlights and crushed blacks alike. Do not remove the black
  pass.
- **your image model still returns a photographed canvas sometimes.** The `industry-dormant-book` plate
  came back as a stretched canvas on a white wall despite the LIGHT block's explicit clause. The
  painting was good, so it was cropped to the painted rectangle rather than re-rolled;
  `slide-01.uncropped.png` sits beside it. Check a new plate's edges before paying for another.

**The 25 are not all this format any more.** you settled a format grid on : **one card
per industry keeps this band format and the other twenty are being rebuilt in twenty different static
formats** to test the format itself. The grid, its funnel labels and the F7 sub-skill split live in
`formats/static-ads/FORMAT-GRID.md`. This section governs the five keepers and any future card built
in this format.

The keepers are chosen **for pain variety, not by rank**, so the control group covers five different
pains: construction/quoting, real-estate/leadgen, hospitality/numbers, retail/systems,
financial-services/context. Holding a single rank across the board put owner-bottleneck on three of
the five and made two cards near-duplicates. The map is `KEEPERS` in `scripts/dossier_industry.py`.

**Rig.** Copy and plate mapping in `scripts/decks_industry.py`, plates `scripts/plates_real.py`,
renderer `scripts/build_industry.py`, output `out-industry/<industry>/<pain>.png`. Re-rendering all 25
is free. Review surfaces, both free:

```
python3 dossier_industry.py              # all 25, INDUSTRY-STATICS-DOSSIER.html
python3 dossier_industry.py --keepers    # the 5 survivors, INDUSTRY-STATICS-KEEPERS.html
python3 sheets_industry.py               # 5 per-industry sheets + the 25-up wall
```

**Snapshot before any destructive re-render.** `_versions/` holds `pre-vhs/`,
`pre-tail-cut-out-industry/` and `pre-keeper-reshoot/`. A paid raw that survives a failed grade is
recoverable with `--regrade` and must never be re-shot: that happened on construction/quoting and cost
nothing to fix.

## 1. The five-slide arc

Every carousel runs these beats. Only the copy changes.

| # | Job | Canonical reference |
|---|---|---|
| 1 | The hook. The shock, the expose, the testimony. This slide has to work alone. | `out2/con-03-v2/slide-01.png` |
| 2 | The scene, compressed to one line of argument. What actually happens, said once. | `out2/con-03-v2/slide-02.png` |
| 3 | The cost. The number, its frequency, and the scope it is true of. | `out2/con-03-v2/slide-03.png` |
| 4 | The reveal. The role exists and somebody owns it. Names the the role you place. | `out2/con-03-v2/slide-04.png` |
| 5 | "There is one place in Australia you can hire one." Plus the url. | `out2/con-03-v2/slide-05.png` |

**Every slide is a headline.** About three lines, one idea, 90px to 140px of type. Slides 1, 4
and 5 were always written that way; slides 2 and 3 were prose and a captioned figure, and under
the bottom-band law they collapsed into a wall of 47px text with the eyebrow and the quote
attribution reading as part of the sentence. They are now headlines too.

The long-form `scene`, `quote`, `attrib`, `figure` and `caption` fields stay in `decks2.py` as
provenance. They are where each slide's line came from and they no longer render, so the sourced
pull quote is now the raw material for slide 2's line rather than a block on the slide.

**The six-slide pain arc** is the other shape this format runs, and it is what all 22 pain decks
use: the pain as a question, then three numbered builds one per slide, then the result, then the
CTA. Slide 1 carries "you need these three automations ASAP", slides 2 to 4 are "ONE.", "TWO.",
"THREE.", slide 5 opens "THE RESULT", and slide 6 is the quiz CTA.

### 1e. The two reference themes, neither shot yet)

The carousel reference batch at `projects/content-engine/engine/reference-bank/carousels/` produced
two shapes this format now carries alongside the five-slide and six-slide arcs. Both are authored
and unbuilt. Read `carousels/STYLE-GUIDE.md` before building either.

**Theme B, the collaged paper carousel. MOVED to its own skill:
`formats/paper-carousel/SKILL.md`.** It outgrew a section here. It now carries a cover law, a
left-weighted type column with an O-spine, a highlighter, three depth layers of collage, a
polaroid fan, loose paper, a sculpture end card and five engines of its own. Read that skill
before building or editing one; nothing about the format is documented here any more.

The one line worth keeping in place: it is still the cheapest carousel in the house, because
only the cover and the beat-cast heroes are paid and everything else re-runs for free.

**Theme C, the mounted-artefact curation carousel.** One specimen per slide, mounted on a canvas,
with a title line and a caption line. This is the one house shape that does not argue: it shows.

- **It declares its own arc.** Cover, N specimens, close. No scene slide, no cost slide, no reveal.
  The five-slide arc in section 1 does not apply and N is uncapped.
- **The specimen is a Hub build card**, and only a Hub build card. 157 unique builds are already
  deduped and written, and the canvas only holds one kind of specimen before it stops reading as a
  series. A mixed carousel is not this format.
- **Canvas: a warm paper surface is permitted here and nowhere else**, the single
  exception to pure black on a house carousel). It exists because a mounted artefact needs a canvas
  that reads as a mounting board rather than as void. your display typeface stays the only face and `#1269FF` stays
  the only accent.
- **Layout: the title line folds into the band.** No type above y=844. The artefact takes the top
  two thirds of the frame, and the band carries the title line and the caption line as two type
  sizes in one block. The bottom-band law survives on this format.
- **The artefact keeps its native aspect ratio** and carries a soft drop shadow. Cropping every
  specimen to a common shape is what makes a curation carousel read as a template.
- **The caption line names the mechanism**, it does not repeat the title.
- **Refused from the reference:** the hand-drawn highlighter, the sketched underline, serif type,
  borrowed third-party creative, and any cover that promises an escalation the post does not
  deliver.

### 1b. The teach law, binds slides 2 to 4)

Naming an automation and jumping to its number teaches nothing. A reader who has never seen one
of these cannot picture what it is, so the result lands on nobody. Every teach slide therefore
carries three things in this order, and **never the result**:

1. **The name.** Keep the noir naming device: "ONE. THE WORKFLOW ENGINE."
2. **A plain definition.** One clause saying what the thing actually is, in words a builder or a
   clinic owner already uses. "AN ASSISTANT THAT RUNS A WHOLE PROCESS."
3. **The mechanics.** How it operates, as the steps it takes. What it reads, what it decides,
   what it writes back, and where a person still stands in the loop.

**Every figure moves to slide 5.** Slides 2 to 4 carry no percentage, no dollar amount and no
before-and-after time. Slide 5 opens "THE RESULT, ONE BUSINESS EACH:" and carries all three
numbers, which is also what keeps scope discipline (section 3) honest now that the figures sit
together.

**The mechanics are evidence too.** They come from the build's own record in
`projects/house-candidate-knowledge-hub/import-data/staged/builds/`, whose `solution` and
`replicate_steps` fields describe how each build actually works. Translate that into plain
English, never invent a mechanism, and never dress it in the source's stack jargon: "a
graph-based multi-agent framework with RAG" becomes "it works out the next step and opens your
CRM itself". A build whose record describes no mechanism does not earn a teach slide.

**Length is a fit problem, not an authoring one.** Write the clause that explains the thing and
let `band.py` shrink the type to fit. Teach slides land around 6 lines at 55px to 70px against
the 4 lines at 90px to 110px a hook runs. The band geometry and the painted plate do not change.

### 1c. The IP law, binds every teach slide)

The Hub builds were described to us by candidates in interviews. **Their architecture is their
intellectual property, not our content.** A teach slide publishes the shape of the pattern, never
the build that a candidate could recognise as theirs.

Write to the **minimum viable architectural understanding**: the least a reader needs to picture
the thing working and judge whether they want one. In practice that is four questions, and
nothing beyond them.

| Keep | Because |
|---|---|
| What it reads | The reader needs the input to picture it |
| What it decides | This is the part that makes it an automation |
| What it writes back | Without this it sounds like a chatbot |
| Where a person still stands | The approval gate is the trust argument |

Cut everything below. These are the tells that a specific build is being published:

- **Vendor and tool names.** No n8n, no Claude, no Azure, no LangGraph, no Playwright. Say "an
  automation platform", "a model", "a browser agent". The stack is the candidate's choice and
  naming it dates the slide anyway.
- **Counts that fingerprint a build.** "Eleven-way routing", "four clusters", "twenty three
  agents", "fifty small classifiers", "three offices". A number that identifies whose build this
  is belongs nowhere on the card, including slide 5.
- **The candidate's named method.** Where the record carries a proprietary or branded technique
  ("shadow system", "council architecture", "brand brain", "patent-pending similarity scoring"),
  describe the behaviour and drop the name and its distinguishing structure.
- **Sector plus scale together.** Either is fine alone. "A council", "a solar company", "a health
  department" combined with a headcount or a volume narrows it to one identifiable client.
- **Anything the record flags as novel.** If `what_worked` reads as the candidate's edge rather
  than as standard practice, it is the first thing to cut, not the highlight.

The test before a teach slide ships: **could the candidate who described this build read the slide
and recognise it as theirs?** If yes, generalise until the answer is no, and check the slide still
answers the four questions above. Losing the detail is a failure too, the rule is general **and**
still architecturally useful.

Worked example, the same build written three ways:

| | |
|---|---|
| **Too specific** (publishes their IP) | "IT RUNS FOUR AGENT CLUSTERS, ONBOARDING, BRIEFING, CONSUMPTION AND RECOMMENDATION, OVER A SHARED BRAND BRAIN" |
| **Too general** (teaches nothing) | "IT USES AI TO IMPROVE YOUR MARKETING" |
| **Right** | "SEVERAL AGENTS SHARE ONE MEMORY OF YOUR BUSINESS, SO THE ONE THAT RECOMMENDS YOUR NEXT MOVE IS READING WHAT THE OTHERS LEARNED" |

### 1d. The worked set

`scripts/decks_noir.py` holds 22 decks written to sections 1b and 1c and is the reference for
tone and depth. `noir-pain-delivery` is the deck you signed off first and is the cleanest
example of the arc. The before and after on its slide 2:

```
BEFORE  ONE. THE WORKFLOW ENGINE. THE MANUAL OVERHEAD ON ONE
        OPERATION FELL BY [[SIXTY PERCENT.]]

AFTER   ONE. THE WORKFLOW ENGINE. AN ASSISTANT THAT RUNS A WHOLE PROCESS.
        YOU ASK IN PLAIN ENGLISH, IT WORKS OUT THE NEXT STEP, OPENS YOUR
        CRM, EMAIL AND CALENDAR ITSELF, AND WAITS FOR YOUR [[APPROVAL]]
        BEFORE ANYTHING THAT COSTS YOU.
```

The name survives, the definition arrives immediately, the mechanics answer the four questions,
the figure is gone to slide 5, and no tool, count or method from the source record appears.

## 2. The plate (canonical

Every slide sits under a hand-painted plate in the **F2 noir-painterly house style**, the same
world as the VSL films: a business sliced open like a dollhouse, conveyor belts and pneumatic
tubes, glowing white parcels of work, faceless silhouettes, one hard key light, crushed blacks.
Pure black and white, no colour anywhere in the plate.

**Where the scenes come from.** Compose them from the noir motif vocabulary in
`formats/noir-painterly/SKILL.md` phase 3. **A carousel does not need a VSL board and never waits
on one.** The world and the motifs are the constraint; the specific scene is written for the slide
in hand.

The slide-to-beat shape below is what the pain arc wants, whatever the source:

| Slide | What it paints |
|---|---|
| 1 | the pain, as one motif |
| 2, 3, 4 | one build each, as the station that does the work |
| 5 | all three stations lit together |
| 6 | the installer seating the glowing core |

**Where a matching board does exist** (`projects/content-engine/ideas/noir-vsl-<pain>/SHOTS.md`,
currently the eight canonical pains), lift the scenes from it rather than writing new ones, so the
carousel and the film share plates. That is a convenience, not a gate.

**The prompt is `STYLE + <scene> + LIGHT`**, the two blocks verbatim from
`formats/noir-painterly/SKILL.md` phase 2, with two documented overrides held in
`decks_noir.py`: the aspect clause becomes 5:4 rather than "wide 16:9" (finding U1 in the VSL
review is the standing request to give the skill a proper per-aspect variant), and an explicit
no-lettering clause is appended. The scene between them is one sentence of detailed positive
prose that opens with the shot size.

**The plate must fall away into black at its lower edge.** The rig lays a 180px fade from y664
down to the band, so a scene with empty black there joins invisibly. A scene that paints a floor,
a ground plane or a lit room across that zone leaves a hard horizontal edge the gradient cannot
crush, and the card reads as a truncated photo. **Float the subject in void by default**, the way
the sliced-open building floats, and say so in the scene: "standing entirely alone in an empty
black void with no floor and no walls, and the whole lower half of the frame empty solid black".
This cost a reroll on `noir-pain-bottleneck` slide 2 and is free to avoid.

**Every plate comes back wordless.** your image model bakes gibberish signage unless told not to, so a
plate with lettering in it is either regenerated or run through the noir-painterly phase 5 de-text
pass. It is never shipped.

## 2c. No annotations (cut **Nothing is drawn over the plate.** The plate carries the painting, the band carries the
argument, and the black between them stays empty.

The format used to composite a small tool logo, a lowercase your display typeface label and a hairline leader
rising to the object it named, two or three per build slide. you cut them on after
seeing them on the first built queue deck. This was the second retreat: text-only annotations were
cut earlier the same day in favour of logo marks, and now the whole layer is gone.

Set `annotations` to a list of empty rows, one per slide, so `overlay_for` returns None:

```python
"annotations": [[], [], [], [], [], []],
```

**The machinery stays on disk and is not canonical.** `plates_noir.py` still holds `annotation`,
`overlay_for` and the geometry guard, `band.py` still carries the `.anno` class, `jost-500.ttf`
still ships, and `check_dots.py` still audits leader coordinates. Reviving any of it needs your
go, not just a populated `annotations` row.

**The single-card industry variant tried it again on was cut the same day.** A
lead-magnet CTA on a leader arrow ran on all 25 statics for a few hours before you pulled it. The
machinery is `arrow_overlay` in `build_industry.py`, which is now unused. Both surfaces are
annotation-free again, and a populated `annotations` row on any deck is still a mistake.

Two consequences worth knowing:

- **The tool-logo evidence claim is gone with it.** It was only ever standing for the counted CRM
  stack (Claude 198, ChatGPT/GPT 102, n8n 71 of 483 populated `transcript_summary` rows as at
  never for a specific Hub build, so nothing traceable was lost. Evidence now lives
  entirely in the headline copy, where section 3's scope rule already governs it.
- **The black gap under the plate is now visible.** A slide whose band fill comes back under about
  85% shows it as dead space. That is a copy-length problem, so lengthen the headline rather than
  reaching for something to put in the gap.

## 2b. One type direction

The tabloid and splash directions are retired. The bottom-band law removes the masthead, the
standfirst, the grey tier, the rules, the counter and the logo, which is everything the two
differed on, so they render identically. The old renders are parked in `scripts/out2/_superseded/`.

Layout is the law in `content-formats` section 1, executed by the shared engine at
`skills/content-formats/formats/static-ads/scripts/band.py`. Line breaking belongs to the renderer: write the copy as
whole lines and let the rig re-break it to fill the band.

**The band is thin your display typeface as of .** Anton is retired on this format. The band renders on
the `noir` theme in `band.py` `THEMES`: **your display typeface weight 200**, all caps, justified flush both
margins, one blue accent, 0.02em tracking. Weight 200 is the locked design system's display weight
(`context/design-system/SCHEMA.md`: "Display type is weight 200"), so the carousel now sets type in
the same face and weight as every other house surface.

Only the face changed. The bottom-band law, the caps, the justification, the single blue accent and
the one-size-per-card fit are all unchanged, and since the annotations were cut the band is still
the only type on the card.

Two earlier passes on this theme are superseded and should not be revived by accident: the
sentence-case your display typeface 500 band tried and rejected on and its weight-700 accent. The accent
stays blue, because a heavier accent word breaks the even colour a thin face buys. A
`justify: False` option for ragged right stays available and is not canonical.

**Thin type is fit-sensitive.** your display typeface 200 is a lighter, wider face than Anton at the same measure,
so the same copy lands at a smaller size and more lines. Check the fit report: a slide that used to
run 4 lines at 100px now runs 5 to 7 lines at 55px to 90px. That is the engine doing what the law
asks, not a fault.

## 3. Scope discipline (the audit rule that failed v1)

**A number may only claim the scope its source supports.** The CON-03 verbatim says six to seven
touch points per job, errors "sometimes costing up to $30,000 per incident, and roughly 400 a
year". That 400 is one firm's yearly incident count. The v1 headline read it as an industry-wide
figure, which the source does not support and which is the kind of claim that ends a brand whose
whole position is trust.

The rule, applied to every line on every slide:

- **Firm-scope figure**, sourced from one discovery call: the copy says one business. "Hiding in
  one Aussie builder." "It lands about 400 times a year in a single business."
- **Industry-scope figure**, sourced from a census, a survey, or an aggregate in the pain wiki:
  plural framing is allowed. "Across Australian building firms."
- **No source**: ask you. Never round a number into existence, and never promote a firm figure
  to an industry figure because the plural reads better.

Every deck built before needs this audit before it re-renders. The 13 in
`scripts/out/`: `p00-eight-hats`, `p01-second-job`, `p02-thirty-thousand-typo`,
`p04-right-all-along`, `p05-eight-seconds`, `p06-two-thousand-customers`, `p07-no-attribution`,
`p08-octopus`, `p09-headcount-trap`, `p11-three-thousand-unread`, `p12-most-expensive-junior`,
`p13-eighteen-months`, `p16-three-hundred-grand`. The plural-framed headlines ("THE AUSSIE
CONSTRUCTION BUSINESSES WHOSE...", "REVEALED: THE $30,000 TYPO HIDING IN AUSTRALIAN CONSTRUCTION") are where the
error concentrates: check each against its pain-wiki record and rewrite to firm scope where the
record is a single company.

## 4. The copy rules

**Slide 1 is a tabloid headline, written as reported news.** Third person, about the owners it
concerns rather than to the reader. "Revealed: the $30,000 typo hiding in one Aussie builder"
reads as news. "Stop losing $30,000 to typos" reads as an ad and the format collapses.

**One blue accent per slide, never two.** Mark it with `[[double brackets]]`. It goes on the
shock number or the role, whichever is the surprise. Two accents kills both.

**Ground every number in the pain wiki.** Pull the vertical's real figures from its playbook at
`context/pain-wiki/industries/<slug>.md` (the "Raw evidence" tables carry the call counts and the
strongest quote per pain) and the persona's own words from `context/personas/personas-and-avatars.md`.
Never invent a number, never name a real company or person.

**Slide 2 stays reported.** Present tense, third person. Scene, then the pull quote, then the
paragraph that names why nobody catches it. Keep each paragraph to two or three sentences.

**Slide 3's caption does the work the figure cannot.** The number alone is a claim. The caption
traces it: what it is, what it is per, and what makes it recur.

**Slide 4 names house for the first time.** Slides 1 to 3 are all problem. The reveal reads as a
report on what the winners did rather than as an offer.

**On the pain arc, slides 2 to 4 explain and slide 5 counts.** See section 1b. The teach slides
carry name, plain definition and mechanics with no figure at all; every number lands together on
slide 5 under "THE RESULT, ONE BUSINESS EACH:".

House floor per `skills/content-formats/SKILL.md` section 1: no em dashes, no negation-swap,
banned-vocabulary clean, contractions on, one owner addressed.

## 5. Headline templates

Eight mechanics. Each avatar is pre-assigned one in the ideation file, and they swap freely.

| # | Template | Mechanic |
|---|----------|----------|
| 1 | Time / money shock | Owners "shocked" by what the hire gives back |
| 2 | Expose / investigation | "Revealed:" a hidden cost, number-led |
| 3 | Rush / trend report | Everyone serious is filling the same seat |
| 4 | Warning / alert | Direct warning to the owner about the pain |
| 5 | Availability story | The scarce hire is now reachable |
| 6 | Named-role reveal | There is a new seat at the table |
| 7 | First-person testimony | A tabloid quote from a relieved owner |
| 8 | Contrarian report | The winners did the non-obvious thing |

Templates 2 and 8 carry the strongest cross-vertical hooks and are where a batch should start.

## 6. Layout spec (locked)

- **Card:** 1080x1350 (4:5), pure black `#000`.
- **Plate:** fills y 0 to 844, the area above the band, and fades to black at its lower edge so
  the join is invisible. Generated at 5:4, the closest ratio to the 1080x844 area.
- **Band:** the bottom 1.5/4 of the frame, 506px tall, top edge y=844. No plate enters it.
- **Type:** your display typeface 200 uppercase, 0.02em tracking, one size per slide, white, set flush from x64 to
  x1016 and filling the band. Slides land between 55px and 110px, hooks at the top of that range
  and teach slides at the bottom.
- **Accent:** house blue `#1269FF` on `[[bracketed]]` spans only, one per slide. The blue is the
  only colour on the card, because the plate is mono.
- **Absent:** annotations of any kind (labels, leaders, tool logos), masthead, standfirst, eyebrow,
  body copy, pull-quote block, stat figure treatment, counter, footer, logo. No grey anywhere.

Sizing and line breaking are computed by the shared engine, never hand-tuned. **A slide that
comes back under about 55px is carrying too much copy, so cut the copy.** Raising a cap or
re-breaking the lines by hand does nothing: the renderer re-breaks them anyway.

**This spec governs band cards only.** The theme B information slides in section 1e sit outside it,
with their own type scale, still to be measured. Theme C keeps this band with two type sizes in the
one block (title, then caption) and swaps `#000` for the permitted warm paper canvas.

## 7. Running it

```
cd "the business/skills/content-formats/formats/news-carousel/scripts"

# 1. write the deck into decks_noir.py: slides and plates, with `annotations` set to
#    a list of empty rows, one per slide (section 2c).

# 2. generate and composite. Skips plates that already exist, so re-running picks up
#    stragglers. One paid job at a time, downloaded before the next is dispatched.
python3 plates_noir.py noir-pain-admin
python3 plates_noir.py noir-pain-admin 2 3      # only those slides
python3 plates_noir.py noir-pain-admin --recomp # no generation, re-composite only

# 3. contact sheet, then review the FULL slides in Cursor, never the folder
```

`check_dots.py` audited leader coordinates and is dead while annotations are cut. It stays on
disk for the same reason the rest of the machinery does.

Chrome headless takes about 2.5s a slide and a plate takes 60 to 90 seconds, so a full eight-deck
batch runs about an hour. Background it and report once rather than polling.

**Re-compositing costs nothing.** The plate is already on disk, so `--recomp` re-renders the band
as many times as it takes. Only the painted scene costs credits, so copy iteration is free and a
scene change is 2 credits.

`build.py` + `decks.py` are the v1 rig and still render the 13 legacy decks into `out/`. They
stay until the look locks and the decks are re-cut into `decks2.py` with the scope audit applied.

**Two v2 decks ship as worked examples.** `con-03-v2` (CON-03, angle A3, the $30,000 typo) and
`agy-01-eighty-people` (AGY-01, angle A9, the agency paying 80 people to move numbers). The AGY-01
deck is the reference for the scope rule: both of its figures come from one discovery call, so
every line on all five slides says one agency, including the stat label and the caption.

## 8. Gotchas

- **A headline line that is too long silently shrinks the whole headline**, because the fit is
  driven by the longest line. One overlong line drags four good ones down with it.
- **Apostrophes and quotes** go through `html.escape`, so type them as plain ASCII in the deck
  file and let the renderer handle them.
- **Delete stale slides** if an arc ever shrinks, or the contact sheet picks them up.
- **The figure is the accent**, so never also bracket something in its caption.
- The endcard renders no masthead and no counter in either direction. Do not add one.
- **A scene that paints a floor truncates the card.** See section 2. Float the subject in void and
  state the empty lower half in the scene prose, or the plate's ground plane leaves a hard edge
  where the fade meets the band.
- **The band justifies, so short lines track out.** It is the fit engine doing what the law asks,
  and it is most visible on 4-line cards whose lines differ a lot in length. The fix is the copy.
- **A plate is not a stock photo.** Two decks needing the same idea share the motif, not the file:
  generate each one so its composition suits its own slide.

## 9. Related

- Canon: `skills/content-formats/references/canon/angles-and-formats.md` (F5), `canon/angles-and-formats.md`, `context/personas/personas-and-avatars.md`.
- Evidence: `context/pain-wiki/INDEX.md`. Vertical-specific work starts at `context/pain-wiki/industries/<slug>.md` (ranked pains with angles, language, targeting); general-pain work at `context/pain-wiki/pains/<slug>.md`; objection beats at `context/pain-wiki/objections/<slug>.md` and `references/canon/objection-bank.md`.
- Concept bank: `skills/content-formats/references/canon/CONCEPT-BANK.md`. Archetypes: `skills/content-formats/references/scripts/archetypes.md` (S1, S16).
- Concept map: `projects/content-engine/ideas/news-carousels/IDEATION.md` holds 38 carousels,
  one per avatar, each with a headline template and a cost anchor already assigned. Start there.
- Hook bank: `references/hooks/HOOKS.md`. The old `projects/content-engine/ideas/news-carousels/CANONICAL-HOOKS.md` is gone; HOOKS.md absorbed it on and is the bank of record.
- Sibling carousel rigs: `skills/best-time-carousel/` (photo-backed), `skills/webinar-carousel/`
  (frame-backed).
- Copy craft and the QA gate: `skills/content-formats/SKILL.md`.
- **The plate style: `skills/content-formats/formats/noir-painterly/SKILL.md`.** Phase 2 holds the
  STYLE and LIGHT blocks, phase 3 the world and the motif vocabulary, phase 5 the de-text pass.
- **Optional scene source where a board happens to exist:**
  `projects/content-engine/ideas/noir-vsl-<pain>/SHOTS.md`, eight boards, one per canonical pain.
  Merged review: `projects/content-engine/ideas/NOIR-VSL-REVIEW.md`. A carousel never waits on one.
- **The queue: `projects/content-engine/ideas/news-carousels/NOIR-QUEUE.md`**, 38 decks in three
  waves with their builds and painted directions already written.
- Logo marks: `projects/content-engine/ideas/museum-gallery-carousels/assets/logos/`. Unused here
  since annotations were cut (section 2c); still live for other formats.
