# The industry format grid (F7 build spec, your decision on : the 25 industry statics keep **ranked pain #3** in each industry on
the current bottom-band VHS format, and the other **20 cells each get a different static format** so
the format itself is what gets tested. This file is the assignment, and the sub-skill split that
F7 gets broken into to build them.

Approve or amend the grid before anything renders.

---

## 1. What the corpus says before a single cell gets built

Three findings from the corpus pull change how this grid is designed. Full detail in
`references/scripts/a reference brand-teardowns.md` (static doctrine section) and the refreshed swipe bank.

**A format is not good or bad, it is good or bad at a funnel position.** a reference brand audits creative by
position first: Magic Mind scored 9 on bottom-of-funnel execution and 6 on scalability, because
bottom-of-funnel carries a spend ceiling. So **every cell below is labelled TOF, MOF or BOF**, and a
cell can only be read against others at the same position.

**Curiosity pulls the click, clarity closes the sale, and the landing page is where most statics fall
apart.** Every one of the current 25 cards is pure curiosity pointing at five magnet pages that do
not exist. That is a larger risk to this set than any layout choice, and it is called out again in
section 5.

**The advice / advertorial static earns a cell of its own.** V11 in `references/scripts/archetypes.md`
already carries it, and the research bank lists "long-form native statics, text-heavy, reads like an
article screenshot" as a top-of-funnel shape. The archetype's own hard requirement governs the cell:
an advertorial only performs when the click lands on a page that genuinely teaches, so the answer has
to actually be there. It is cell `construction/quoting` below.

a reference brand's warning lands on the Figma layer directly: template shapes are built to serve warm
audiences, and **feature call-outs only work at the bottom of funnel**. The two Figma-derived cells
are therefore both BOF, never cold.

---

## 2. The grid

One card per industry keeps the band format: VHS plate above, one justified your display typeface 200 block in the
bottom 506px. **The keeper is chosen for pain variety, not by rank** (see the note under the table),
so the five survivors cover five different pains.

**The five keepers moved off the band on .** Each card now runs a your display typeface 200 "Breaking:"
header and a CTA line over a top-down black fade, a black censorship bar over the subject's eyes
in place of the pop-art sunglasses, and a torn newspaper clipping in the bottom right carrying the
industry headline in one black ink. No arrow. `scripts/build_news_clip.py`, outputs
`out-news/*-clip.png`, law recorded as deviation 3 in `SKILL.md` section 0. Two of the five also
changed copy on your call, so the pains in the table below no longer describe those cards:
**hospitality** runs `tribal-knowledge--declarative` instead of `numbers`, and **financial
services** runs `admin--callout` instead of `context`. Construction, real estate and retail are
unchanged. Every line is still a verbatim `basics.py` fill of a named HOOKS template.

| Industry | Pain (deck order) | Format | Funnel | Plate |
|---|---|---|---|---|
| **Construction & Trades** | 1 systems | Us vs them (S11) | MOF | type only |
| | 2 double-handling | Napkin (S5) | TOF | rendered, free |
| | 3 bottleneck | Advice / advertorial static (V11) | TOF | existing VHS |
| | **4 quoting** | **band (keeper)** | TOF | existing VHS |
| | 5 headcount | Quote-card grid (3 real construction clients) | MOF | type only |
| **Real Estate & PM** | 1 admin | iMessage / WhatsApp chat (S3) | TOF | UI mock |
| | 2 systems | PSA comparison split | MOF | type only |
| | 3 bottleneck | Big quote plus star row (Hive Property) | MOF | existing VHS |
| | 4 numbers | Annotated hero, leader lines | BOF | existing VHS |
| | **5 leadgen** | **band (keeper)** | TOF | existing VHS |
| **Hospitality & Food** | **1 numbers** | **band (keeper)** | TOF | existing VHS |
| | 2 hiring | Don't hire this person (S6) | TOF | type only |
| | 3 admin | Editorial masthead embed | TOF | existing VHS |
| | 4 tribal-knowledge | Whiteboard explainer | TOF | rendered, free |
| | 5 presence | Before and after (S10) | MOF | existing VHS, two grades |
| **Retail & E-commerce** | **1 systems** | **band (keeper)** | TOF | existing VHS |
| | 2 bottleneck | **Ultra low-fi static** | TOF | **new plate, paid** |
| | 3 numbers | Numbered listicle / tick rows | BOF | type only |
| | 4 admin | **Comment reply ad** | TOF | **new plate, paid** |
| | 5 headcount | Problem / solution split (S2) | MOF | type only |
| **Financial Services** | **1 context** | **band (keeper)** | TOF | existing VHS |
| | 2 admin | Question hook (S12) | TOF | type only |
| | 3 bottleneck | Organic post screenshot (S15) | TOF | UI mock |
| | 4 dormant-book | Long-form native article static (S13) | TOF | existing VHS |
| | 5 trust | Founder statement card (a founder) | MOF | type only |

### Why the keeper is not ranked pain #3

Holding rank #3 across all five put **owner-bottleneck on three of the five keepers**, because
construction, real estate and financial services all rank it third. Construction and real estate came
out as near-duplicate cards separated only by "through the owner" against "through the principal". A
control group for a format test cannot be near-single-pain, so you moved it on to one
distinct pain per industry, each the most ownable pain that industry has: **quoting, lead follow-up,
tribal knowledge, reporting lag, the dormant client book.**

Each displaced format moved onto the freed cell rather than being dropped, and three of them read
better there than where they started:

- **Advice / advertorial static** now sits on construction/bottleneck, which is the shape's natural
  subject ("why the business stops when you do") rather than quoting.
- **Organic post screenshot** now sits on financial services/bottleneck, whose pain is the owner
  personally building the automation. A personal-profile post is exactly how that gets said.
- **Editorial masthead embed** now sits on hospitality/admin, the Sunday-night spreadsheet, which is
  an editorial headline already.
- **Big quote plus star row** moved to real estate/bottleneck. Testimonials are proof rather than
  pain-matched, so the Hive Property quote works on any real estate cell.

**20 cells, 20 distinct formats, no repeats.** Funnel spread is 11 TOF, 7 MOF, 2 BOF. The TOF weight
is deliberate: the house's problem is cold prospecting, and every TOF cell here is a native or advertorial
shape, which is what the $250k-a-month static accounts actually run. The two BOF cells are the two
drawn from the Figma template layer, which is where that layer belongs.

### Casting notes

- **Testimonials are cast to the client's own industry.** H&L Construction, Vitale Projects and
  Northwear go on construction (three real clients, which is why construction gets the grid shape).
  Hive Property goes on real estate. Financial services has no client on the site, so it takes the
  founder statement instead of a borrowed quote. Kasun D is candidate-side and stays out of
  employer-facing cards entirely.
- **"Don't hire this person" sits on hospitality/hiring** because the pain is hiring, so the reverse
  command reads as a joke the reader is already inside.
- **The napkin goes to construction/double-handling** because pen and paper is that owner's own
  medium, and the pain is two copies of one docket.

---

## 3. The band-law deviation (recorded, not silent)

The layout law (SKILL.md section 0 puts every mark in the bottom 506px. you
ruled on that **native mocks may break it for this test**, because an iMessage thread, a
tweet screenshot or a photographed napkin cannot exist inside a bottom type band, and breaking it is
the point of the test.

Breaks the band law: iMessage chat, organic post screenshot, napkin, whiteboard, ultra low-fi,
comment reply, editorial masthead embed, annotated hero.

Keeps the band law: us vs them, PSA split, quote-card grid, big quote plus stars, listicle and tick
rows, problem/solution split, question hook, don't hire this person, founder statement, before and
after, long-form native, advice / advertorial static.

The law still binds every type-led shape, and it stays the house default outside this test.

---

## 4. Plate budget

you authorised **two paid plates**, one per new look, approved one at a time and then reused across
industries. Every other cell is free.

| Job | Look | Used by |
|---|---|---|
| 1 | Screenshot-grade, phone-flat, no film character | ultra low-fi |
| 2 | Phone snapshot with on-camera flash | comment reply |

Three cells could take a paid plate later and are deliberately rendered free first, so nothing gets
paid for before you has seen whether the free version holds:

- **Napkin** and **whiteboard** render as drawn artwork rather than a photograph of real paper.
- **Before and after** uses the same VHS plate twice at two grades rather than the two painted panels
  F9 specifies. Two painted panels is 2 more paid stills and is not in this budget.

### Separate from the two: one keeper plate needs a refine

The five keepers are the control group, so they are the cards that most need clean plates. Checked at
full resolution on after the keepers moved to top pain:

| Keeper | Plate |
|---|---|
| construction/quoting | clean. Blueprint body text degraded to speckle, no readable word |
| **real-estate/leadgen** | **"APPRAISAL REQUEST SLIPS - UNOPENED" is legible on the folder** |
| hospitality/numbers | clean. Laptop screen is speckle, the carton is plain unmarked |
| retail/systems | clean. The CRT reads as a database screen with no readable word |
| financial-services/context | clean. Ledger pages are pure speckle |

Moving the keepers to top pain took this from three flagged plates to one, because the two worst
offenders (hospitality's legible "CHEF'S SPECIAL" and financial services' photographer silhouette,
which broke the no-people rule outright) are no longer keepers. They stay flagged on the cells they
now sit on, where they are less exposed.

The fix for real-estate/leadgen is
`plates_real.py real-estate-and-property-management leadgen --refine --go`, one paid job at roughly 2
credits, which keeps the approved composition and removes only the lettering. **Not authorised yet**,
and separate from the two-plate budget above.

---

## 5. The open risk this grid does not fix

Every TOF cell is a curiosity shape, and curiosity clicks evaporate when the landing page does not
educate immediately. The five industry magnet pages still do not exist; only the generic
`/ai-readiness` quiz is built.

**Recommendation:** point the advice / advertorial cell at a real house advice page rather than a magnet
quiz, and treat the advice page as part of that cell's build, since V11's own requirement is that the
teaching has to be there when the click arrives. you has the magnet pages in a separate session, so
this is a flag, not a blocker for rendering.

---

## 6. The F7 sub-skill split (BUILT your note on : F7 needs breaking into sub-skills, one per sub-format it covers, rather
than staying one skill with a template table. Twenty formats do not want twenty skills, so they group
by **how they are produced**, which is what actually differs between them:

| Sub-skill | What it owns | Formats |
|---|---|---|
| `type-led` | The band law, the fit solver, one justified block, one blue accent | us vs them, PSA split, problem/solution split, question hook, don't hire this person, listicle and tick rows, founder statement, band |
| `plate-led` | A photographic plate plus laid-in type, plate composition rules, the de-text pass | advice / advertorial static, editorial masthead embed, annotated hero, long-form native, before and after, big quote plus stars |
| `ui-mock` | Faithful interface chrome: message threads, post cards, comment rows | iMessage chat, organic post screenshot, comment reply |
| `hand-drawn` | Marker, pen and paper, whiteboard, deliberate low fidelity | napkin, whiteboard, ultra low-fi |
| `proof` | Real attributed quotes only, the fabrication ban, industry casting | quote-card grid, big quote plus stars, founder statement |

`proof` deliberately overlaps `type-led` and `plate-led`: it is a content gate on which words may
appear rather than a renderer. The renderers are the first four.

**Built on .** Five sub-skill files now exist as `formats/static-ads/<name>/SKILL.md`
(F7.1 type-led, F7.2 plate-led, F7.3 ui-mock, F7.4 hand-drawn, F7.5 proof), and the parent
`SKILL.md` is now the router carrying the shared law: the band (section 0), the archetype-to-sub-skill
map (1), the copy rules (2), the swipe bank (3), the funnel label (4), the rig (5), testing doctrine
(6) and the renderer traps (7). Read the router plus exactly one sub-skill. No renderer changed and
nothing rendered.

**One thing the split had to resolve.** Sections 2 and 3 above put PSA comparison split, numbered
listicle and tick rows, and the quote-card grid inside the band law, and those three shapes cannot
compress to one justified block. `type-led/SKILL.md` section 2 splits the band into **Tier A** (the
pure one-block law, six formats, renders today) and **Tier B** (rows or columns inside the same
506px, three formats, needs a template written). Tier B holds the band geometry, the single face, the
flush margins, one blue accent for the whole card and a four-row ceiling; it gives up only the
one-block clause, and only for this test. Recorded as deviation 2 in the parent SKILL.md section 0.

---

## 7. Build order

1. you approves or amends this grid.
2. ~~Split F7 into the five sub-skills, parent becomes the router.~~ **DONE .**
3. Build the free cells: `type-led`, then `ui-mock`, then `hand-drawn` renders, then `plate-led` on
   the existing VHS plates. Tier A type-led cells render on the existing rig; Tier B, the ui-mocks
   and the hand-drawn cards each need a template written against `band.py` first.
4. Contact sheet plus dossier of all 25, walk it with you.
5. Only then shoot the two paid plates, one at a time, for ultra low-fi and comment reply.
6. Nothing reaches the CRM without your explicit go. Archiving the 22 old carousels is still an
   unmade Supabase write.
