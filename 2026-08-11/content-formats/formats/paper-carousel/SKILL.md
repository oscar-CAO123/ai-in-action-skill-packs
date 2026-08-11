---
name: paper-carousel
description: The collaged paper carousel (Theme B). A dark full-bleed cover, information pages set on a heavily collaged paper sheet with a polaroid fan, and a sculpture end card. Use when building or editing a candidate-facing or client-facing Theme B carousel, or when a task mentions the paper carousel, the polaroid fan, the O-spine, the inversion law, or the sculpture end card.
---

# Paper Carousel (Theme B, the collaged information carousel)

Declared as a shape on built out and locked on against U3, the first
carousel to carry the whole format. It grew out of section 1e of `news-carousel/SKILL.md` and now
owns itself; that section points here.

**The cheapest carousel in the house.** One paid still for the cover, one for each hero that is
cast to a beat, and everything else is free and re-runnable: the sheets, the type, the collage,
the fan furniture, the ink marks and the end card.

## The arc

| Slide | Ground | Type | Picture |
|---|---|---|---|
| 1, the cover | dark | white | the painting full bleed, black fade climbing off the bottom edge |
| 2 to n-1 | the collaged paper sheet | black | the polaroid fan and the loose paper |
| n, the close | near black | white, blue CTA | the sculpture end card |

**THE INVERSION LAW.** The ends invert against the middle. That is what makes the set read as a
set rather than a run of pages, and it is what gives the carousel a front door.

The close was briefly a bookend that returned to the cover's painting. It is not: it is the
sculpture end card, so every house carousel ends the same way.

## 1. The cover

Band layout, plate bleeding the full frame, all type in the bottom well on the dark ground.

- **The picture must fill the frame.** An oil-on-paper plate is a painting sitting on a sheet,
  and running it full bleed leaves pale strips of bare paper down the card's edges. **Crop INSIDE
  the paint, not to its bounding box**: the bbox reaches the furthest ragged stroke and still
  carries the margin. `build_u3.COVER_CROP` is the worked example.
- **The divider rule.** A 2px rule in the ink colour, 44px above the first line of type, running
  **the type's measure, not the card's**. `band.render_card(rule=True)` positions it in the fit
  pass, because the top of the copy block is not knowable until the type has been broken.
- **No blue accent on the ends.** The band's accent is blue by theme and this family takes its
  ends all black.
- The poster geometry (type above and below the figure) was tried and rejected: this plate's
  painting runs into the top third and the second headline line vanished into black paint.

## 2. The information pages

### Type

- **Left-weighted.** Type takes the card's own 64px margin and runs 58 per cent of the width. The
  right band is reserved for the fan, so the two never negotiate for space at render time.
- **Nothing is indented.** The number, the header and every body line share one left edge. An
  earlier pass hung the number in a gutter and indented the body to the header; that cost the
  body 138px of an already narrow measure and held it at 40px.
- **The O-spine.** A large thin number hanging at the left, the header beside it on the same
  line. The spine runs **across the carousel**, O1 to On, and does not restart per page.
- **Header 500 and uppercase, body 300 and sentence case.** The body matches the number's weight
  rather than the band's hairline 200, and keeps the copy's own capitalisation.
- **Headers are one to four words.**
- **An authored blank line is a short gap**, about a third of a line, not an empty line. In a
  430px measure the copy breaks to twice as many lines and three full-height blanks were holding
  the body down to 29px.
- **Every page in a set renders at one size.** Solve each page, then re-render them all at the
  smallest result. Solved independently they came out at 45, 42 and 41px, which reads as three
  pages that could not agree.

### The header row is anchored, not centred

`.blk` centres its block vertically, which is right for a page that stands alone and wrong for a
set. U3's copy pass left a 478px page beside an 883px one and the centring dropped the short
page's O-number 230px below the other two, so the three headers walked down the carousel. Same
failure as three pages solving to three different type sizes, and the same fix: pin the thing
that has to agree. `.blk.left` anchors at `padding-top:130px`.

Only `.blk.left` moved, and a caller gets that class only by passing a header, so the sibling
units are structurally out of reach. **Checksum them anyway.**

### The copy

The format's laws are not enough to make a page read well, and the first U3 build proved it: the
layout was locked and you still called the copy "not up to standard". Two passes fixed it.

- **Break every line by hand, to about 27 characters** in the 626px measure. Lines do not wrap,
  they shrink the page: `render_sheet` solves one size for the whole block.
- **Fewer lines buys bigger type.** The prune took U3 from 41px to 52px without touching a
  single setting. Cutting copy is the cheapest typographic improvement available.
- **Cut the scaffolding.** "They have already tried it themselves" is four words wrapped around
  "they tried it themselves". Most authored paragraphs carry two or three per page.
- **Show, do not tell, when a list will do it.** "They bought the tools, they tried it themselves,
  it half worked" became "E-commerce. Civil engineering. Construction. Professional services." A
  list is scannable, and it is the only kind of line a reader can check themselves against.
- **The highlight is the payoff and it must be a claim you can stand behind.** Two were cut from
  U3 for over-claiming. "One firm can only find about a hundred and fifty of you" hid house behind
  a third party, so it became "We have found 152+ people in the country who can do it, so far."
  "You would start on the first line" told a stranger which rung was theirs, which broad targeting
  cannot support, so the highlight moved onto the band itself. **Prefer a claim about the offer
  over a claim about the reader.**
- **Numbers set in digits on the information pages.** The family spells them out and
  `decks_candidate.py` gives the reason: "matching decks_noir.py, because the band runs large
  caps". A caps band is the case for words. A 52px sentence-case body page is not, and "$70k to
  $120k" is both what the website says and what a job ad says.
- **Name things.** Three unlabelled salary bands are trivia. "the entry-level role, the entry seat.
  $70k to $120k" is a career ladder.
- **Re-measure after every copy change.** New line breaks move the type block, and the fan
  origins and the `EXTRAS` were both set against the old one. On U3's second pass the block grew
  to row 1225 and put a scrap straight through the payoff line.

### The highlighter

Emphasis is a **highlighter**, never an underline and never a flat block of hex. Four things
separate a marker stroke from a filled rectangle and `paper_sheet.highlighter` carries all
four: a chisel tip so the ends are angled, a wandering edge from a turbulence displacement,
density variation along the run, and translucency so the paper reads through the colour.

house blue at about 30 per cent. `box-decoration-break: clone` is load bearing: Chrome's default
slices one background across every line fragment, so a three-line highlight came out as one
stroke stretched and cut into thirds.

### The three depth layers

The page has three, and the gap between them is the point. Two layers alone jumps from a whisper
to a shout.

1. **The bed**, baked into the sheet. `collage_bed_paper` at `SHEET_AMPLITUDE` over
   `SHEET_LAYERS`, currently 0.30 and 17. That is well above the 0.16 over 11 locked for a
   PAINTED plate, and the two settings are separate on purpose: on a painted plate the bed
   competes with the figure, and on a blank page it competes with nothing.
2. **The mid-ground band**, `cutouts.edge_band`. A newspaper collage entering off the top
   edge, bowing out to the right margin, running down it and turning back in at the bottom, at
   about 58 per cent opacity, every piece rotated to the tangent so the run reads as one gesture.
   It goes on **before** the fan.
3. **The foreground**: the polaroid fan, the loose shreds and the ink marks, at full strength.

**Every unit owns its own sheets.** They used to share filenames, so re-texturing one carousel
silently re-textured another. Build with `build_sheets.py <unit>`.

### The polaroid fan

Three polaroids per page, fanning out of the right band.

- **The piece is a polaroid.** A machined white frame, thin on three sides and deep at the foot,
  a hairline inside the window, a soft drop shadow. No tear and no ragged edge: what carries the
  hand is the fan, the tilt and the shadow. Torn magazine cutouts were tried across several
  passes and rejected.
- **The picture runs the degraded noir treatment**: greyscale, print grain, uneven exposure, and
  one of the seven F8 tints. The reference for the lighting is the O2 press frame.
- **The hero is biggest and lands on top**, about 1.6 to 1.7 times the supporting pieces. The two
  behind take a slight opacity decrease.
- **They fan from one shared origin**, roughly 20 degrees between pieces. Every piece rotates
  about that origin, not its own centre, or the three end up stacked rather than fanned. Angle
  order and stack order are **independent**: derive the angle from the draw index and the hero
  ends up tilted the full spread, lying on its side.
- **The origin is measured per page** against the rendered base, then written into the unit's
  `FANS` table so every later render is free and deterministic. Same habit as `build_split.py`'s
  CROP and `mascot.py`'s VOIDS.

### The loose paper

Torn newsprint shreds and hand-drawn ink marks in the corners and margins, **alongside** the fan
rather than inside it, placed absolutely from a hand-set `EXTRAS` table. Measure each region's
occupancy off the rendered base rather than guessing. `cutouts.mark` carries six shapes in the
same `#rough` turbulence the F8 loop diagram uses, so everything drawn in this rig reads as one
hand.

## 3. The sculpture end card

The same end card the F8 industry-build carousels close on, forked in `endcard.py`: the radial
veil at the moire style's three stops, a 240px top scrim, a 760px tall scrim, white lines at
bottom 252, the blue `#4B9EFF` CTA at 176, the lockup at 46.

**The monument changes from carousel to carousel.** The Thinker is F8's. The bank is
`static-ads/references/monuments/`, with the prompt phrase and a `used_by` field per entry so a
monument is claimed once. Three of them are top-half portraits only.

**The moire is never prompt-baked** and **you grade once.** A plate lifted from the F8 rig is
already graded, and running the chain again crushes the sculpture to black.

## 4. Casting: the law that matters most

**Every picture must mean what its slide says.** This is the one that was broken hardest and cost
the most: heroes were picked from whatever plates were lying around, so a slide about walking a
work floor got a stock shot of hands and a slide about businesses waiting got an empty room with
nobody in it.

`industry-build-carousel/SKILL.md` section 2a already states it: **cast the style to the beat,
not to the industry**, and **mixing the formats is the effect**. Both halves bind here.

- Take the most concrete beat on the slide and shoot that.
- **Vary the medium across the pages** for contrast: live action, then press photograph, then
  drawn. Never three of the same.
- **Nothing recycled from another carousel goes in the hero slot.**

Worked example, U3:

| Page | Beat | Picture | Medium |
|---|---|---|---|
| O1 | they tried it themselves and it half worked | an owner at night, hand in his hair, boxes still taped shut | live action, VHS |
| O2 | walk in, find the work being done by hand | a young person with a notebook watching an older worker copy papers into a ledger | press photograph |
| O3 | the three bands and the published rule | a drawn three-rung ladder | drawn, free |

## 5. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 build_sheets.py u3          # the collaged sheets, one seed per slide
python3 build_u3.py                 # every page, free
python3 build_u3.py --bare          # no fan and no loose paper, for measuring a new origin
python3 gen_candidate_plate.py <key>        # dry run
python3 gen_candidate_plate.py <key> --go   # ONE paid job
python3 mascot.py <key>             # lay the house mark into a plate's head void
```

Engines: `paper_sheet.py` (the sheet and the information-page type), `band.py` (the cover),
`cutouts.py` (polaroids, scraps, marks, the fan, the mid-ground band, the ladder),
`endcard.py` (the close), `collage_bed_paper.py` and `build_sheets.py` (the bed),
`mascot.py` (the composited house mark).

## 6. Do not repeat these

Every one of these was hit while building U3.

- **A cover on the light ground.** Matching the cover to the paper slides made the whole carousel
  one temperature with no front door.
- **A full-bleed divider rule.** It runs the type's measure.
- **Sizing a piece by its plate rather than its subject.** An oil plate is mostly bare paper, so
  a 760px piece carries maybe 400px of figure floating in an empty canvas and every placement is
  computed against a footprint that does not exist.
- **Luma-keying a photograph.** A VHS frame is dark overall so the threshold takes the whole
  frame, and the one bright area, a screen-lit cheek, comes out above the threshold and gets
  punched out as a hole through the face. Real matting needs rembg, which is unaudited.
- **Trusting a plate's framing.** Every style tail here bans letterboxing and a frame within the
  frame, and the models do it anyway in both directions: black bars on one plate, a grey mount on
  the next. `cutouts.trim_dark` reads the surround colour off the corners and eats it.
- **Pushing fan pieces out along their arm.** On a right-hand fan that is straight off the card:
  the pieces were rendering, just past the edge.
- **Editing a shared engine without checksumming the siblings.** `paper_sheet.py` and `band.py`
  are shared with U4 and U7. Two separate changes, a width calculation and a fit cap, silently
  resized cards that were already on the board.
- **Re-running a sibling's build script without its flags.** Verifying the checksum gate meant
  rebuilding every sibling, and `build_candidate_posters.py` run with no `--plates` re-rendered
  u1a and u1b with PLACEHOLDER plates, overwriting two cards that are live on the CRM. The gate
  caught it at 15 of 17 and `--plates` restored them byte-identically. **Read a sibling script's
  docstring before you run it to prove you did not break it.**
- **Seeding a per-page effect off a leftover loop counter.** `lay_band(png, seed=i)` sat in a
  second loop that did not bind `i`, so all three pages took the first loop's final value and
  carried a byte-identical mid-ground band. The pages are supposed to never read as the same
  page twice, and nothing in the output announces that they do.
- **A pen mark that rings nothing.** When a copy pass shortens a page, an ink circle placed
  against the old block ends up floating in blank paper, which reads as a mistake rather than as
  a hand. A ring has to land on something: move it onto the newsprint and it becomes a ringed
  classified.
- **Cutting at native plate resolution.** The mask, both tears and the texture pass run per
  pixel; a build went from seconds to nearly four minutes. Work at twice the target height.

## 7. QA gates

```
grep -c $'—\|–' <file>                                                  # must be 0
grep -nE "not [a-z ]{1,25}, (it|that|this|they)'?s |, not a " <file>    # must be empty
```

Plus, every build:

- **Checksum the sibling units** before and after touching a shared engine. They must be
  byte-identical.

```
cd "the business/skills/content-formats/formats/static-ads"
shasum candidate/u7/*.png candidate/u4/*.png candidate/u1a-*.png candidate/u1b-*.png > /tmp/sib.txt
# ...make the change, then rebuild EVERY unit, minding each script's own flags...
shasum -c /tmp/sib.txt          # all 17 must be OK
```

- **The fan must not intrude into the type column.** `lay_fan` measures and prints the intrusion.
- **The hero's centroid must sit on the card**, at least 90px from any edge. It may bleed, but it
  must never lose its subject to the crop.
- **Every page in the set must solve to the same size**, and the header row must land at the same
  height on all of them.
- **Read the render.** Every one of the failures in section 6 was found by looking at the output,
  not by reading the diff.

## 8. Pushing a finished carousel to the CRM

`scripts/crm_u3.py` is the worked example. One row, not one per page: a carousel is one post,
which is the convention U7 set at row 44.

```
python3 crm_u3.py            # DRY RUN, prints every upload and the INSERT verbatim
python3 crm_u3.py --status   # what batch-1 already has on the board
python3 crm_u3.py --go       # upload, insert, write a REVERSE
```

- **Read the copy off the renderer, never retype it.** `body` is assembled from `build_u3.COVER`,
  `SLIDES`, `CLOSE_LINES` and `CLOSE_CTA`, so the board cannot drift from the card.
- **INSERT only.** Never DROP, ALTER, DELETE or UPDATE, and **your explicit go every time**,
  after he has seen the statement the dry run prints.
- **Snapshot before, REVERSE after**, both into `scripts/_crm/`, matching the files already there.
- **Guard the re-run.** The script refuses to insert if a row with the same title exists, so a
  second run cannot double-post.
- Public bucket `content-media`, one folder per set, `media_urls` in carousel order and
  `thumbnail_url` pointing at the cover.

## 9. Related

- `news-carousel/SKILL.md` section 1e, which this grew out of and which now points here.
- `industry-build-carousel/SKILL.md` section 2a, the style bank, the grades and the casting law.
- `noir-painterly/oil-on-paper/SKILL.md`, the painted sub-style the covers use.
- `engine/reference-bank/style-packs/paper-cutouts/STYLE-GUIDE.md`, the cutout material bank.
- `engine/tools/moire/README.md`, the moire pass and why it is never prompt-baked.
