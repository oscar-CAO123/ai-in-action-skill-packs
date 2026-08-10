---
name: industry-build-carousel
description: Use when the operator says "industry build carousel", "industry carousel", "what an AI hire builds", "vertical carousel", "grid carousel", or wants a house carousel that shows the actual systems an embedded the role you place builds for one industry. Builds a 4:5 carousel: a full-bleed 2x2 grid where each quadrant is shot in a DIFFERENT house style (painted noir, VHS camcorder, 16mm, Super 8, Betacam, security camera, press flash), with a white node diagram walking clockwise around a square ring centred on the frame. Format F8 in angles-and-formats.md.
canonical: false
format: F8
status: in gate (Step-6-style). Not a valid pick for the weekly draw until it passes.
---

# Industry-Build Carousel (F8, the vertical carousel)

The answer to the one question every employer-side prospect asks: what does an AI hire actually
build for a business like mine? Each slide is one named system, drawn as a loop of icon nodes
walking clockwise around a centred square ring, over four painted quadrants that narrate that
system's story.

The vehicle is lifted from a @derivenotes grid carousel and rebuilt in the house noir world. Where
F5 news-carousel borrows the trust of a news headline, F8 borrows the trust of a workflow board:
it reads as the actual system someone would hand you, drawn rather than designed at you.

**One carousel per vertical, and the vertical list is fixed.** The 21 industries in
`context/pain-wiki/industries/` are the only valid verticals; each one has a playbook with its pains
already ranked, an angle written per pain, and a named lead magnet. The workflows are chosen from
that playbook, never guessed. Construction is batch 1 because it is the largest industry in the
corpus (55 calls, 50 businesses) and the deepest well in the wiki (262 mined records across 56
companies).

**All nineteen are written and sit at the reference shape (2026-08-05).** `other` is uncategorised
and has no playbook, so it is not a vertical, and **Building Services was dropped by the operator on
2026-08-05** and parked at `verticals/_parked/`, fully authored and never shot. Its batch number 6
is retired rather than reused. The nineteen live in `verticals/`, each with a complete data file: four systems chosen off that playbook's ranked pains, the workflows node by
node, a stat per system with its provenance, the collage cover with its own diorama angle, a style
cast onto every one of its twenty-one plates, and the magnet-led closing. Every one renders today
with labelled placeholders, so a vertical is reviewable before a cent is spent. `VERTICALS.md` is
the index, and it also carries the ad-targeting shape for each industry.

The other nineteen were brought up from the pre-reference shape on 2026-08-05 in one free pass: covers
recast from a 2x2 to the collage, angles assigned in batch order so no two consecutive carousels
share one, briefs stripped of the 124 instances of lighting and format language left over from when
style was per carousel, shot sizes normalised to the studio five, and the closing switched to the
moire Thinker. The beat casting is spread across the batch on purpose, so no slot is dominated by
one style. Twenty carousels that shot every build the same way would read as one template.

**Every vertical already has a lead magnet.** The playbook names it and gives its full 8-question
quiz with graded answers and a result framing, so the closing CTA is a lookup rather than a writing
job: Construction is The Site-to-Profit Readiness Check, Real Estate The AI-Ready Agency Score,
Hospitality The Wow Factor Audit, and so on down all 20 playbooked industries.

## THE REFERENCE SET (2026-08-05)

**Real Estate is the finished carousel. Judge every new vertical against it.** It is the only one
with all twenty-one plates shot.

`export/real-estate-and-property-management/` holds it: `01-cover` through `06-closing` in swipe
order plus a contact sheet. Twenty-one paid plates. What that build settled, all of it now law:

| Decision | The set |
|---|---|
| Plate style | Per QUADRANT, four formats inside one grid, cast to the beat |
| Cover | Four torn cutouts pasted at angles, at least one the clay diorama |
| Hook | Three patterns rotating in batch order, centred on its own scrim, `{n}` filled in code |
| Cover angle | Rotates every carousel, logged in `cover-angles.json` |
| Closing | One moire-graded sculpture, The Thinker, full bleed. Two blocks only |
| Part tag | `part 1` on the cover, nowhere else. Every vertical opens its own series |
| Branding | The house lockup ONCE, on the closing page only |
| Diagram | Unchanged across all four slides, monochrome white on any plate underneath |

Construction was ported into `verticals/` on 2026-08-05 and brought up to this set. Its old
four-slide build stays on disk at `slides.json` as the diagram's origin, reachable as the slug
`slides`, and nothing reads it any more.

**The plate style is a bank, cast per quadrant (2026-08-05).** Ten entries in `styles.json`, each a
generation formula plus a free ffmpeg grade. Painted noir is still the flagship. Section 2a is the
bank and its laws.

**Lineage:** the rig, the batch plan and the quadrant briefs are
`projects/content-engine/ideas/industry-build-carousels/` (`build.py`, `PLAN.md`, `QUADRANTS.md`).
The painted style is the noir-machine anchor shared with F2 noir-painterly. When the format locks,
the rig moves to `scripts/` here, the way F5's did.

---

## Production spec (the worker and Claude Code both execute this)

```yaml
format: F8
skill: industry-build-carousel
canvas: [1080, 1350]           # 4:5, rendered at device-scale 2 to 2160x2700
pages: 6                       # cover + 4 system slides + closing
plate: nano_banana_pro at 4:5, 2k, one job at a time, style anchor as --image-references
routing: ../../references/canon/model-routing.md   # house shot-type table. nano keeps this lane: native 4:5 plus 14 image references for the style anchor
plate_style: per QUADRANT in each quadrant's `style`. plateStyle is only the fallback
quadrants: 4 per page          # 21 stills for a full carousel: 16 slides, 4 cover cutouts, 1 closing
renderer: headless-chrome      # CHROME_BIN env, macOS default fallback
fonts:
  - jost-400.ttf               # EVERYTHING on every page. No second face anywhere
logo: assets/house-logo.svg      # the closing page ONLY, forced white by CSS filter
rig:
  slides: projects/content-engine/ideas/industry-build-carousels/loop_diagram.py   # CANONICAL
  stitch: stitch.py, numbered export plus a contact sheet for judging the set
  data: verticals/<slug>.json, one per industry. Nineteen. _parked/ is dropped, never read
  styles: styles.json, the plate-style bank
  gen: gen_plates.py, ONE generator for every vertical and every style
  grade: grade_plate.sh, the free ffmpeg pass that makes four plates read as one grid
  cover_angles: cover-angles.json, the eight camera angles on the diorama plus the used ledger
  index: VERTICALS.md (all 20, style, systems, magnet, targeting) + QUADRANTS.md (Construction)
inputs:
  vertical: the industry, one carousel each. Batch order in VERTICALS.md
  style: one per QUADRANT, cast to its beat. Four formats inside every grid
  systems: 4 named systems, one per slide, chosen from that vertical's ranked pains in the wiki
  workflow: 4 to 8 nodes per system, each tagged trigger | ai | you
  stat: one figure per system with its pain-wiki provenance recorded in pillSrc
  quadrants: 4 shot briefs per slide, narrating trigger, old way, the build, the result
  magnet: the vertical's named quiz. The default CTA is the soft generic line
steps:
  - pick the 4 systems from that vertical's playbook, then write verticals/<slug>.json
  - cast a style to each quadrant, warmest against coldest, and pick the cover angle
  - python3 loop_diagram.py <slug>, review the structure and copy on placeholders, free
  - python3 gen_plates.py <slug>, read the composed prompts, still free
  - python3 gen_plates.py <slug> --go, one paid job at a time, reviewing stills before compositing
  - re-render, then review the FULL pages in Cursor, never the folder
qa:
  - em dash scan (must be zero)
  - grade scan: channel means per plate. Magenta or colour on a grayscale style is a GRADE bug,
    not a generation one, and re-grading is free. See section 8b for the one-liner
  - negation-swap scan
  - banned vocabulary per content-formats section 1
  - IP law: the flowchart publishes the shape of the pattern, never a candidate's build
  - scope check: the stat carries the scope its source supports, one business means one business
  - every plate comes back wordless; a plate with baked lettering is regenerated. A plate carrying
    a FABRICATED social post, name or handle is never shipped, whatever else it gets right
  - style check: the four quadrants of a page carry DIFFERENT styles, cast to their beats, with
    the warmest sitting against the coldest. A page that came out uniform is recast, not shipped
  - cover angle check: the angle differs from the previous carousel's, and cover-angles.json's
    `used` ledger is updated. Two consecutive covers on the same angle is a defect
  - hook check: `hookPattern` differs from the previous carousel's in batch order, a pattern C
    question carries its `hookSrc` deck, and the count is written `{n}` rather than typed
  - label check: the company type in the hook matches that industry's Targeting section in the pain
    wiki. A label that names a wider trade than the corpus supports is a targeting error, not a
    wording one, and it is the fastest way to spend budget on the wrong room
  - underline check: the drawn blue rule sits under its phrase and no further. `.u` must stay an
    inline-block with an explicit svg width, or the rule silently reverts to a fixed 200px
  - brief check: no shot brief carries lighting, framing convention or format language. That
    belongs to the style, and a brief that states it will fight whatever style it is cast in
  - GRAYSCALE CHECK, on grayscale styles only (noir-oil, cctv-plate, press-flash). The colour
    styles are meant to be colour and the grade sets their saturation. nano_banana_pro returns
    colour even when the prompt says pure grayscale: 2 of the 12 Construction plates came back warm (max channel spread 139
    on the dusk exterior, 60 on the pipeline screen). Desaturate in place rather than paying to
    regenerate, and keep the original under assets/_colour-originals/:
      python3 -c "from PIL import Image; import numpy as np, glob
      [print(p, (np.asarray(Image.open(p).convert('RGB')).astype(int).max(2) -
       np.asarray(Image.open(p).convert('RGB')).astype(int).min(2)).max())
       for p in sorted(glob.glob('assets/s*-q*-paint.png'))]"
    Anything above about 12 is colour. **That number is a candidate, not a defect** (the operator,
    2026-08-06): he closed all 18 F8 flags unfixed, because variation across the set is wanted and
    a batch desaturated to pass a measurement reads as one template. Fix only where the colour is
    clearly a GRADE BUG, a cast across every plate in one style or a plate that disagrees with the
    other three in its own grid. When it is: Image.merge('RGB', [im.convert('L')] * 3)
  - every node's icon matches its own step, checked against the annotation
  - the diagram is monochrome white, blue only on the title number
  - nothing is drawn over the plates. They run clean
  - the house lockup appears on the closing page and nowhere else
  - the closing card is the sculpture, not a montage of the slides
  - judge the set on the contact sheet from stitch.py, never page by page. Six pages that each
    work alone can still read as six unrelated posts
outputs: render/cover.png, render/slide-1..4.png, render/closing.png
```

---

## 1. The six-page arc

**The cover and closing were restyled onto the locked system on 2026-08-05** and now render from
`loop_diagram.py` with the slides. `build.py` and its navy serif treatment are superseded.

**The two end cards do not use the grid** (the operator, 2026-08-05). The four-up montage is for the four
system slides only. The cards each carry one idea:

- **Cover: a pasted collage of four cutouts.** A 2x2 that looks torn out rather than laid out:
  each panel is clipped on an irregular torn edge, rotated a few degrees, given a paper margin and
  a heavy drop shadow, and pasted onto a dark canvas ground. The four cutouts deliberately carry
  **different canonical styles**, so the cover samples the whole carousel before the reader swipes
  into it.
  **At least one cutout is always THE diorama:** a pair of large hands arranging a miniature
  clay-animation set of that industry on a tabletop, the way someone plays with a doll set, on
  `noir-oil`. Real estate is a tiny clay agent in front of a model house with a miniature for-sale
  board; construction is the same hands over a model site; hospitality over a model dining room.
  The industry is the toy and the operator is the hands, which is the offer stated as an image
  before a word of it is read.
  Over it: the `part 1` tag on a top scrim and the hook **centred in the frame** on its own radial
  scrim, in your display typeface 400 at 76px with a **drawn** blue underline on the key phrase (an SVG path through
  the `#rough` filter, never a text-decoration).

  **The part tag is `part 1`, on the cover, and appears on no other page** (the operator, 2026-08-05).
  Every vertical opens its own series at part 1 rather than announcing itself as number N of twenty,
  which reads as a back catalogue nobody has seen. Follow-ups inside an industry take part 2 onward.

  **The hook rotates across THREE patterns (the operator, 2026-08-05).** One line run twenty times is one
  post duplicated twenty times, the same argument that rotates the cover angle. Each pattern is
  three parts, and the middle one carries the drawn blue rule:

  | | Pre | Underlined | Post |
  |---|---|---|---|
  | A | `The {n} automations` | `the top 1%` | `of {company type} use` |
  | B | `{Company type} think` | `they don't need AI` | `until they see these {n} automations` |
  | C | `{pain question}` | `Build these {n}` | `automations first.` |

  Assigned in batch order so no two consecutive carousels run the same pattern, recorded per file in
  `cover.hookPattern`. Real Estate holds A because it is the shot reference set. The split is not
  even: C carries the most specific claim and only earns four of the nineteen, because a pain
  question that does not match the vertical's own top pain is worse than the generic line.

  **`{company type}` comes from that industry's Targeting section in
  `context/pain-wiki/industries/<slug>.md`, never from what fits the sentence** (the operator,
  2026-08-05). Two labels were wrong about who house sells to before this was a rule: "motor trade
  businesses" for a corpus of dealerships, crash repair and mechanic workshops, and "software
  businesses" for a corpus of SMB SaaS and MSP founders. **Financial Services is "brokerages", not
  "broking firms", everywhere.** Read the playbook before writing the label.

  **C's pain question is never written fresh.** It is lifted from the slide-1 opener of a shipped
  noir pain deck in `formats/news-carousel/scripts/decks_noir.py`, which is the proven pain line for
  this audience, sentence-cased for the F8 cover's your display typeface. Pick the deck whose pain matches the
  vertical's own slide-1 pain and record it in `cover.hookSrc`. This is the hook-fill law applied to
  F8: pick a named structure and cite it, never free-write.

  **The number comes from the slide count in code, never typed.** The skill claimed this from the
  day the format locked and the data still carried a literal `4` until 2026-08-05. It is now real:
  write `{n}` in any of the three parts and `build_cover()` fills it, so a cover cannot promise more
  systems than the carousel teaches.

  **The angle changes every single time (the operator, 2026-08-05).** The scene is fixed, the camera is
  not. `cover-angles.json` holds eight named angles and a `used` ledger; a new carousel takes an
  angle no recent carousel has taken, and never the one immediately before it. Twenty covers of one
  idea from one camera reads as a post duplicated twenty times; from twenty positions it reads as a
  series. Record the angle in the vertical file's `cover.angle` and in the ledger when it is shot.
- **Closing: one sculpture, full bleed.** Rodin's The Thinker on `moire-sculpture`, a bronze
  photographed off a screen so interference banding and dot crawl ripple across it. The oldest
  image of thinking work arriving through the newest medium.

  **Two type blocks, and only two** (the operator, 2026-08-05). The `One operator. Four systems. Live in
  90 days.` offer block is CUT. What remains is the line, then the CTA under it:

  ```
  But don't start by building. Start by discovering.
  TAKE THE AI READINESS QUIZ TODAY.
  ```

  **The CTA is deliberately soft.** It does not sell the placement, it sends them to the quiz.
  Every vertical still carries its named magnet in the `magnet` block, so a specific score can go
  back into the CTA if a campaign wants it, but the default is this generic line across all twenty.

That is 5 paid plates for the two cards, so a full six-page carousel is 21 generations.

| Page | What it does |
|---|---|
| Cover | Full-bleed 4-shot montage of the vertical's world, the hook overlaid, `part N` tag. No card. |
| Slide 1 | System 1. The workflow that hits the vertical's deepest pain first. |
| Slide 2 | System 2. |
| Slide 3 | System 3. |
| Slide 4 | System 4. |
| Closing | The offer line and one CTA, pointing at that vertical's lead magnet. |

Four systems is the ceiling. A fifth slide costs four more paid stills and buys nothing, because
the reader has already answered the question the cover asked.

## 2. The locked visual system

**The quadrants.** Four full-bleed stills meeting at a centre seam, generated on `nano_banana_pro`
at 4:5 and 2k, one paid job at a time. Which world they are shot in is set by the carousel's
`plateStyle`. Painted noir is one of seven and is still the flagship.

The prompt formula does not vary. `gen_plates.py` composes it, so it is never hand-written:

```
[style head] [shot size] [style body]. [the scene, naming the single light source and what it
is brightest on]. [style tail] No text.
```

"No legible text" replaces "No text" whenever the scene contains a screen, a page or a printed
document, which is most of them. `gen_plates.py` decides that from the brief.

## 2a. The plate-style bank (added 2026-08-05)

Twenty carousels in the same painted noir would read as twenty of the same post. The plates carry
the vertical's world, so the world changes with the vertical while the diagram never does.

**The bank lives in `styles.json`.** Each style is two layers:

1. **Generation.** A `head`, `body` and `tail` that compose into the prompt formula above, plus an
   optional `anchor` passed as `--image-references`. Anchors come from the studio palette at
   `projects/content-formats-studio/palette-refs/`, which is where the 16mm, 8mm, Betacam and 35mm
   reference frames already sit. Painted noir keeps the noir-machine anchor.
2. **A grade.** A free ffmpeg chain in `grade_plate.sh`, run over every plate after download.
   **This layer is the reason the format survives leaving noir.** Four plates generated as four
   separate jobs will never agree on grain, colour and fidelity, and a 2x2 grid shows that
   disagreement immediately. One shared grade per carousel forces the agreement, for nothing.

| Style | The world | Grade | Grayscale |
|---|---|---|---|
| `noir-oil` | Hand-painted B&W oils, one hard key, everything else crushed | none | yes |
| `vhs-camcorder` | Consumer camcorder dubbed to tape, milky blacks, chroma running past its edges | vhs | no |
| `film-16mm` | Observational documentary, real grain, halation, available light | film16 | no |
| `super8-home` | Someone's own home-movie footage of their own business, warm and faded | super8 | no |
| `betacam-broadcast` | 1994 corporate video, hard video light, saturated, interlaced | betacam | no |
| `cctv-plate` | The ceiling camera nobody thinks about, wide, grey, unflattering | cctv | yes |
| `press-flash` | A newspaper frame, direct flash, hard shadow behind, black past two metres | press | yes |

**The laws.**

- **The style is per QUADRANT, and one grid deliberately carries four of them** (the operator,
  2026-08-05). The grid reads as a wall of footage of the same business pulled from four different
  places: someone's home video, the office security camera, a screen recording, the broadcast
  package. **Mixing the formats inside the grid is the effect.** A grid in one uniform treatment is
  the miss. `plateStyle` at the top of a vertical file is the fallback for a quadrant that names
  none, not the style of the carousel.
- **Cast the style to the beat, not to the industry.** The trigger, the old painful way, the build
  and the result are four different kinds of evidence, so give them four different kinds of film.
  Contrast is the job: put the warmest style next to the coldest one. Real Estate slide 1 is the
  worked example, Super 8 into security camera into camcorder into broadcast.
- **The brief describes the scene. The style describes the treatment.** Never write lighting, a
  framing convention or a format into a shot brief, or it fights whatever style it gets cast in.
  "A vendor's hand signing a listing authority across a kitchen bench" is a brief. "hard flash,
  square-on, shot on 16mm" belongs to the style.
- **The diagram never changes.** Monochrome white ink, the same ring, the same furniture, whatever
  is underneath. The plates are the world; the diagram is the brand.
- **The veil follows the heaviest plate.** Each style carries a three-stop `veil`, and the renderer
  takes the maximum across the four styles a slide is carrying, so the white diagram holds over the
  brightest quadrant in the grid.
- Every style carries its own `qa` note for the way it fails, and `use_for` for where it lands.

**The quadrant story.** The four shots narrate the system rather than decorating it:

`Q1 the trigger -> Q2 the old painful way -> Q3 the build working -> Q4 the result`

**Nothing is drawn over the plates.** Green computer-vision bounding boxes with confidence scores
were the original conceit and were **cut by the operator on 2026-08-05**. The plates run clean. The
overlay code is gone from `build.py` and the `cv` arrays left in `slides.json` are inert. Do not
reinstate them.

**The loop (LOCKED 2026-08-05, this is the format).** The diagram is a node graph in n8n's
grammar, walked clockwise around a square ring centred on the frame. It replaced a torn notebook
card carrying a hand-drawn flowchart, which is retired: the card sat in the middle of the frame
and made the composition a photograph with a note stuck to it.

- **The ring adapts to the workflow (2026-08-05).** A node ALWAYS sits on all four corners, then
  the spare steps take edge midpoints in the order top, bottom, right, left. So 4 steps is the
  bare corners, 6 adds the top and bottom midpoints, 7 adds the right, 8 fills all four. Every
  consecutive pair therefore shares an edge, every connector is a straight run along it, and the
  dashed return closes up the left edge. **The square is always complete at any node count.**
- **4 to 8 steps.** Outside that the renderer stops rather than drawing a broken ring: below four
  there is no loop worth drawing, above eight the tiles and labels collide.
- **The square is fixed.** Same centred position and span on every slide, so the set holds its
  rhythm as you swipe. The labels shrink to 240px on any edge carrying three nodes.
- **The icon is the node.** Each step is a solid white tile, 108px, holding one black mark and
  nothing else. No text inside, no card, no label. A small black step-number badge sits on the top
  left corner.
- **Annotations live outside** for top and bottom nodes, and **inside the empty centre** for the
  left and right edge nodes, all in your display typeface 400 on their own drawn leader arrow pointing into the
  tile. Uniform geometry across all seven: 76px from tile edge to text, 54px of leader. Each
  label is pinned by the edge facing its tile, so a second line grows away from the node and the
  gap holds.
- **The centre stays empty.** The painting reads through it. The system name, the rule and the
  before-to-after figure that used to sit there were cut.
- **Monochrome white.** One ink, `#F4F3EC`, across tiles, connectors, leaders and annotations.
  The blue is gone from the diagram entirely.
- **Marks:** every node names its own `icon` in `slides.json`. The mark must match the STEP, never
  its position on the ring. The positional list in `STEP_ICON` is a fallback for an unset node and
  produced wrong marks on the first pass of slides 2 to 4 (an envelope for "receipts + timesheets
  in", a drafted document for "posts to xero / myob"). A `logo` path on the node takes precedence
  over both, for steps where naming the product helps.
  Icon set today: `mail plans calc draft tap send clock receipt tag bank post flag chart folder
  sync link message bell funnel calendar gauge`. Add to `ICONS` in `loop_diagram.py` when a step
  needs a mark the set does not carry.
- **The pen quality survives the structure.** The `#rough` turbulence displacement filter
  (`baseFrequency 0.013`, `scale 3.0`) still bends every tile edge and connector, tiles carry
  seeded eight-value asymmetric corner radii, and each connector is drawn with its own control
  points. Nothing is rotated and nothing is scattered: the looseness is in the line, never in the
  layout.

## 3. The nodes, which are the whole point

Four to eight steps, lowercase, each a plain statement of what happens. Every node carries a kind:

- `trig` the trigger, what starts it
- `ai` the machine doing the work
- `you` the one human decision

**Exactly one `you` node per system.** That node is the entire promise of the offer: the owner
stays in charge of the decision and stops doing the labour around it. Two `you` nodes reads as a
job. Zero reads as a robot the reader will not trust.

**Construction slide 3 broke this law and was fixed on the port (2026-08-05).** "The Job Sync" ran
five nodes with no `you` step, so it read as a robot with nobody in it. The added node is the owner
confirming the job before it spins up across the three systems. It is the one piece of authored copy
in that port rather than a move, so it is the first thing to check if Construction reads wrong.

The kind tags were removed from the annotations on 2026-08-05, so the `you` step is now marked
only by its dashed tile border. It is quieter than it was. If a slide needs that step to carry
more weight, change the tile, never add the label back.

## 4. The data contract (`verticals/<slug>.json`)

This is the modulation surface. A new vertical is a new file, and the rig does not change.
All twenty verticals live here, Construction included: it was ported off `slides.json` on
2026-08-05 when it was brought up to the reference set. `slides.json` stays on disk as the record
of the retired four-slide build and the rig reads it only for the slug `slides`.

```
vertical, name              the slug and the display name, matching the pain-wiki folder
part                        its number in the batch, per VERTICALS.md
plateStyle                  a key from styles.json. The FALLBACK only, for a quadrant naming none
styleNote                   the one-line restatement of that, kept in the file so it travels with it
brand, brandTail            the footer wordmark
corpus                      calls, businesses, confidence, wiki records. Say when a pack is thin
audience                    who the carousel is for, taken from the playbook's Targeting section
magnet: name, promise       the lead magnet, which sets the closing CTA
voice                       their words, and the words to avoid, from the playbook's Language section
cover: mode, hookPre, hookUnderline, hookPost, part ("part 1"), angle, panels[4]
       hookPattern               A, B or C. Never the same as the previous carousel's
       hookSrc                   pattern C only. Which noir pain deck the question came from
slides[]:
  n, title                  the system's name
  pain, painSrc             the playbook pain it answers, and the evidence behind it
  nodes[]: txt, kind, icon  kind = trig | ai | you. icon names the mark, and is REQUIRED
                            optional "logo": a tool logo path, which overrides the icon
  payloadH, payloadB[]      the plain-language payload, three lines
  pillPre, pillHi, pillPost the stat, the blue-circled middle
  pillSrc                   PROVENANCE. Where the number came from and at what scope
  quadrants[4]:
    pos                     "TL / trigger" etc, the narrative role
    style                   THIS QUADRANT's style, cast to its beat. Falls back to plateStyle
    shot                    the shot size, from the studio palette vocabulary
    img                     assets/<slug>/s<N>-q<n>.png, absent until generated
    label                   the shot brief, shown as a placeholder until img exists
    cv[]                    INERT. The overlay was cut 2026-08-05 and is no longer rendered
closing: lines[] (two), cta. NO part tag, NO offer block
```

Quadrants without an `img` render as labelled placeholders, so a vertical can be reviewed for
copy and structure before a cent is spent on stills.

`pillSrc` is not decoration. It is how scope discipline is enforced: a figure from one business
gets published as one business's figure, and four of the twenty packs are thin enough that this is
the only thing standing between the format and a claim it cannot support.

## 5. Spinning a new vertical, or a new lead magnet

1. Open that vertical's playbook at `context/pain-wiki/industries/<slug>.md`. Its "Pains, ranked"
   section already gives the top pains in the owner's own words, each with a call count, a strongest
   quote and a written angle. Pick the four systems that answer its top four pains, and record the
   call counts as provenance. If the vertical has no playbook, fall back to the theme pages in
   `context/pain-wiki/pains/` and say so in the brief.
2. Write the four workflows node by node. Check the `you` node is exactly one per system.
3. Write the stat for each, with provenance, at the scope the source supports.
4. Write four quadrant briefs per slide against the narrative roles in section 2.
5. Write `verticals/<slug>.json` and render with placeholders. Review the structure and copy first.
6. Pick the `plateStyle` off the bank, checking it against the verticals either side of it.
7. Only then generate the 20 stills, one paid job at a time, reviewing before compositing.
8. Re-render and review the full pages in Cursor.

**All nineteen unbuilt verticals are past step 6.** The files exist, they render on placeholders,
their covers are recast, their quadrants are cast per beat and their briefs are clean. What is left
for each is the operator's read of the placeholder set and then the paid plate run.

**Lead-magnet modulation.** The systems and the quadrants stay; the closing changes. The magnet
sets the closing line and the single CTA, and the cover hook is written to promise what the magnet
delivers. One magnet per carousel, never two, because a second CTA halves the first. Take the magnet
name and its promise line straight from the vertical's playbook rather than inventing one; the
playbook's "Result framing" paragraph is also the copy for the quiz result page if that gets built.

## 6. The laws that bind this format

- **The education law.** This format satisfies it by construction: the flowchart is the teach.
  Do not add a pain-only slide.
- **The IP law.** These builds were described by candidates in interviews, so their architecture
  is the candidate's property. The flowchart publishes the shape of the pattern, what it reads,
  what it decides and what it hands back. It never publishes a candidate's actual build, their
  tool chain, or anything that identifies the business.
- **Scope discipline.** Every number carries the scope its source supports.
- **House rules.** No em dashes, no negation swaps, no banned vocabulary, no AI tells.

## 7. Layout spec (locked)

- Canvas 1080x1350, screenshotted at `--force-device-scale-factor=2` to 2160x2700.
- Full-bleed 2x2 grid, no gutters, quadrants meeting at the centre seam.
- Ring centred at (540, 566), span 262 FIXED, tiles 108px, icons 54px.
- Slot walk clockwise from top left: corners always filled, then midpoints in the order
  top, bottom, right, left. 4 to 8 nodes, enforced by the renderer.
- Annotations 21.5px your display typeface 400, 272px wide, 76px off the tile, on 54px leaders.
- Title at `bottom:258px` in your display typeface 400 at 48px with a blue step number. The Minecraft pixel face
  is retired: every piece of type on the slide is now your display typeface.
- **The house lockup appears ONCE per carousel, on the closing page only** (the operator, 2026-08-05).
  Cover and slides 1 to 4 carry no mark at all. Six lockups in six swipes reads as branding; one
  at the end reads as a signature. `lockup()` in `loop_diagram.py` is the single gate, and only
  the closing passes `brand=True`.
- On that last page: the lockup at `bottom:46px`, 84px tall, forced white by
  `filter:brightness(0) invert(1)`. The letter-spaced text wordmark is retired.
- Bottom scrim 400px behind both for legibility, soft enough to keep the plates readable.
- A radial veil over the quadrants so the white diagram holds against the painting.
- Cover carries no card: montage, scrim, hook band, `part N` tag.

## 8. Running it

```
cd "the business/projects/content-engine/ideas/industry-build-carousels"

python3 loop_diagram.py                       # Construction, all six pages to render/, free
python3 loop_diagram.py <slug>                # any vertical, all six pages, free
python3 loop_diagram.py <slug> 2              # one slide
python3 loop_diagram.py <slug> cover closing  # just the two end pages

python3 gen_plates.py <slug>                  # DRY RUN. Prints all 21 composed prompts, free
python3 gen_plates.py <slug> --go             # PAID. 21 plates, one job at a time
python3 gen_plates.py <slug> --go 2           # PAID. One slide's four quadrants
python3 gen_plates.py <slug> --go cover       # PAID. The cover montage
python3 gen_plates.py <slug> --grade          # re-grade what is on disk, free
python3 stitch.py <slug>                      # export/ the six pages numbered + a contact sheet

./grade_plate.sh <chain> in.png out.png       # one plate by hand, free
python3 build.py                              # cover + closing ONLY; its slide path is superseded
```

`gen_plates.py` skips any quadrant already on disk, so a re-run picks up stragglers rather than
paying twice, and it wires new plates into the vertical file when they finish. Quadrants with no
still yet render as labelled placeholders, so a vertical is reviewable before any spend. The old
`gen_slide1_noirpaint.sh` and `gen_slides234_noirpaint.sh` are superseded and kept only as the
record of the Construction run.

**Twenty-one plates per vertical, so the fourteen remaining carousels are 294 paid generations.**
Nothing dispatches without `--go`, and `--go` needs the operator's explicit word every time.

**The closing plate is the same shot in every carousel**, so fourteen of those generations buy the
identical Thinker. Copying one graded closing across the fourteen asset folders would take the batch
to 280 and cost nothing. That is the operator's call, not a silent optimisation: a single reused
image is also the strongest series signature available, and regenerating it risks twenty slightly
different Thinkers.

## 8b. What the first three shot runs taught (2026-08-05)

Real Estate, Construction and Hospitality are shot, 63 paid plates, **zero job failures across all
three**. All three are live in the CRM at `board_order` 23 to 25 with their six pages in
`content-media/f8-<slug>/`. What they changed:

**Two grade bugs, both batch-wide, both found by measuring rather than looking.**

- **`film16` graded every plate magenta.** Its halation `blend=all_mode=screen` ran in YUV, so it
  screened the U and V planes as well as Y, and both rising off 128 is magenta: mean 103,60,101 off
  a neutral 108,103,95 raw. `format=gbrp` before the split fixes it. **Betacam was checked and is
  genuinely unaffected**, because its trailing `geq` holds the chroma, so it was left alone.
- **`cctv` and `press` re-coloured after desaturating.** ffmpeg's `noise` perturbs each channel
  independently, so a single `hue=s=0` at the head is undone by the grain. Both chains now run it
  at BOTH ends.

**Measure the grade, do not eyeball it.** Both bugs were invisible in a thumbnail and obvious in a
channel-mean. Run this after every paid run, before rendering:

```
python3 -c "from PIL import Image; import numpy as np, json, sys
d=json.load(open('verticals/<slug>.json')); G={'noir-oil','cctv-plate','press-flash'}
pl=[(q['style'],q['img']) for q in d['cover']['panels']]+[(d['closing']['plate']['style'],d['closing']['plate']['img'])]
pl+=[(q['style'],q['img']) for s in d['slides'] for q in s['quadrants']]
for st,i in pl:
  a=np.asarray(Image.open(i).convert('RGB')).astype(float); m=a.reshape(-1,3).mean(0)
  sp=int((a.astype(int).max(2)-a.astype(int).min(2)).max())
  if m[0]>m[1]+8 and m[2]>m[1]+8: print('MAGENTA', i)
  if st in G and sp>12: print('COLOUR ON GRAYSCALE', i)"
```

**Check the RAW, not the graded plate, when deciding whether the model returned colour.** The
grayscale check in section 7 globs the pre-grade file for a reason: run it on the graded plate and
the film grain reads as a colour cast every time.

**The real failure mode is baked text and off-brief returns, not colour.** Construction lost five
of twenty-one plates to it and Hospitality two, so budget roughly one in five on a screen-heavy
vertical. In order of severity:

- **`s4-q3` came back carrying a fabricated social post**: an invented person's name and handle,
  rendered as a real screenshot. That is the one category that must never ship, and "No legible
  text" did not stop it. When a brief names a dashboard, a feed or a queue, say what the screen is
  NOT: no social post, no avatar, no handle, no username.
- Legible lettering survives "No legible text" whenever the scene's whole point is a screen or a
  document: a "LEAD PIPELINE" title, a seven-line missed-call list, an "ESTIMATE" heading over a
  dollar table. Screens and paper are the highest-risk briefs in the format.
- **The noir anchor drags composition harder than the gotcha in section 9 says.** Construction
  `s1-q1` asked for a builder reading his phone in a half-framed house and returned the anchor's own
  machine hall. On a scene with a person and a specific place, drop the anchor rather than fight it.

**Hospitality is the cleaner reference for a shot run than Construction.** Its clay diorama cover is
the best in the set and its slides 1 to 3 came back clean. Judge a new vertical's plates against it.

- The model id is `nano_banana_pro`. `nano_banana_2` 404s.
- **A style anchor drags composition, not just treatment. This already happened.** The first paid
  Super 8 plate (Real Estate s1-q1, 2026-08-05) came back with a film-gate border and sprocket
  notch baked in, plus a ghosted double exposure, because the palette-ref anchor was a photograph
  **of a film strip**. A baked border is fatal here: the quadrant cannot sit flush in a full-bleed
  2x2. **Only `noir-oil` keeps an anchor now**, because its anchor is bespoke and proven. Every
  other style is prompt-only and bans the frame furniture in its tail.
- **The grade lands on whatever it is given.** A muddy or underexposed plate graded to VHS becomes
  unusable. Generate clean and well exposed, then degrade. Grading is free, so iterate there rather
  than paying for another generation.
- **ffmpeg refuses to write over its own input**, which crashed the first paid run mid-batch.
  `gen_plates.py` now downloads to `<key>.raw.png` and grades into `<key>.png`, so the untouched
  original survives and a style can be retuned with `--grade` for nothing. `grade_plate.sh` routes
  an in-place call through a temp file.
- Icons: the set is 36 marks and covers calls, searches, compliance, stock, freight and people as
  well as the original office vocabulary. Add to `ICONS` in `loop_diagram.py` when a step needs a
  mark the set does not carry, and never let a node fall through to the positional fallback.
- **A job can fail server-side and the CLI reports it as a timeout.** One Construction plate came
  back `Error: timed out waiting for job <id> (last status "in_progress")` after the 8m wait.
  Query it before paying again: `higgsfield generate get <id> --json` returns `status: failed`
  with a null result URL, which means retry. Re-running the gen script retries only the missing
  quadrant, because it skips anything already on disk.
- Chrome resolves from `CHROME_BIN` with the macOS default as its fallback. Do not hardcode it.
- Plates come back at 4:5 and the quadrant crops are square-ish, so compose each shot with its
  subject central and expect the edges to be lost.
- Two quadrants in a carousel that both resolve on a handshake will read as a duplicate. Vary the
  framing and the light deliberately, or change the result beat.
- `random.seed(slide["n"] * 7 + 41)` fixes every drawn value, so a given slide's jitter is
  identical across renders. Do not remove it, or the diagram redraws itself every build.
- The `#rough` filter stays on `.flow`, which holds the tiles. Putting it on the whole stage
  would wobble the paintings and the type as well, and the effect collapses.
- Annotations are pinned by the edge facing their tile, never by their top edge. Pin them by the
  top and a two-line label drifts away from its node while a one-line label sits too close.
- `build.py` is **fully superseded** as of 2026-08-05. `loop_diagram.py` renders all six pages.
  The file stays on disk only as the record of the retired navy serif treatment.
- **The cover pair drifts.** Generated as two jobs, the model will change the owner's age, hair or
  clothing between the before and the after. The shared `subject` clause is the mitigation, not a
  guarantee. Check the pair side by side, and regenerate the AFTER panel rather than both.
- The moire grade's dial is the sine amplitude in `grade_plate.sh`. Too much and the banding
  flattens the sculpture's form into stripes; the point is that it ripples across the bronze.

## 10. Related

- `formats/news-carousel/SKILL.md`, F5, the canonical carousel.
- `formats/noir-painterly/SKILL.md`, F2, the same painted world in motion.
- `references/canon/angles-and-formats.md`, the format and angle registry. Part 3 carries 60 worked
  six-slide carousel concepts, three per industry, from the Discovery Intelligence Report. They are
  structure only: 18 of the 360 slide lines are marked `NEG` for a banned negation-swap.
- `ideas/industry-build-carousels/VERTICALS.md`, the batch index: all twenty with their style, their
  four systems, their magnet, their ad targeting, and which packs are too thin to publish loudly.
- `ideas/industry-build-carousels/styles.json`, the plate-style bank, and `grade_plate.sh`, its
  second layer.
- `projects/content-formats-studio/palette-refs/`, the studio's cinematography reference library, which
  is where the style anchors and the shot-size vocabulary come from.
- `context/pain-wiki/industries/`, the 21 valid verticals. Each playbook holds that vertical's ranked
  pains with an angle per pain, its lead magnet, its language do and do-not lists, and its targeting.
- `context/pain-wiki/MARKET.md`, the industry distribution, which is the batch-order argument.
- `projects/content-engine/ideas/museum-gallery-carousels/`, the same job in a different vehicle,
  parked pending this format's lock.
