---
name: before-after-splitscreen
description: Use when you says "before and after", "split screen", "splitscreen", "before/after carousel", "the painting one", or wants a house static showing a business owner before and after they hire a the role you place. Builds a 4:5 split screen: two classical oil paintings of the same owner in the same room meeting at a hard centre seam, their pains listed in your display typeface over the dark half and what changed listed over the light half. Format F9 in angles-and-formats.md.
canonical: false
format: F9
status: in gate (Step-6-style). Not a valid pick for the weekly draw until it passes.
---

# Before / After Split Screen (F9)

One person, one room, two paintings. On the left is the owner before a the role you place, with
their pains listed over them in their own words. On the right is the same owner after, with the
short list of what changed.

The format works because of an asymmetry the reader feels before they read a word: six lines of
grievance on a dark half against four calm ones on a light half. F5 argues with a headline, F8
argues with a diagram, and F9 argues with a portrait.

**The list is the format.** Every line on the left is a real pain from that vertical's playbook in
`context/research-corpus/industries/`, in the owner's own words, with its evidence recorded in `src`.
Invented pains kill it, because the whole effect depends on an owner reading their own week.

**Status: authored no panels shot yet.** The rig renders on labelled placeholders, and
the prompt pair is written. Nothing has been paid for.

**Lineage:** the rig is `projects/content-engine/ideas/before-after-splitscreen/`. It borrows the
furniture from F8 (your display typeface 400, ink `#F4F3EC`, blue `#4B9EFF` on the accent, the house lockup at the
foot, the `#rough` turbulence filter on the seam) so the two formats read as one house.

---

## Production spec

```yaml
format: F9
skill: before-after-splitscreen
canvas: [1080, 1350]           # 4:5, rendered at device-scale 2 to 2160x2700
panels: 2 per unit             # left BEFORE, right AFTER. 2 paid stills per unit
plate: your image model at 4:5, 2k, one job at a time
routing: ../../references/canon/model-routing.md   # house shot-type table. nano keeps this lane: it is the only model with a native 4:5
renderer: headless-chrome      # CHROME_BIN env, macOS default fallback
fonts:
  - display-400.ttf               # everything on the frame
logo: assets/house-logo.svg      # canonical lockup, forced white by CSS filter
rig:
  render: projects/content-engine/ideas/before-after-splitscreen/render.py
  gen: projects/content-engine/ideas/before-after-splitscreen/gen_panels.py
  data: projects/content-engine/ideas/before-after-splitscreen/units.json
inputs:
  vertical: the industry, which sets the pains and the closing CTA
  subject: ONE subject clause, used verbatim in both prompts so it is the same person twice
  before[]: 4 to 6 pains in the owner's words, from that vertical's playbook
  after[]: 3 to 4 lines, what the same week looks like once the systems run
  src: the provenance for every pain on the left
steps:
  - open the vertical's playbook and take the pains verbatim off "Pains, ranked"
  - write the subject clause once, then the two plate briefs against it
  - python3 render.py, review the copy and the asymmetry on placeholders, free
  - python3 gen_panels.py, read both prompts, still free
  - python3 gen_panels.py --go, two paid jobs, one at a time
  - re-render and review the full page in Cursor
qa:
  - the left list is longer than the right list. Always. The asymmetry is the argument
  - every left line traces to the playbook, and src records which call count it came from
  - the two panels are the same person in the same room. A different face on the right
    breaks the format completely
  - both faces are turned away or in shadow, per the house rule
  - no lettering baked into either painting
  - em dash scan, negation-swap scan, banned vocabulary per content-formats section 1
  - scope check: a pain quoted as one business's number is written as one business's number
```

---

## 1. The visual system

**Two panels, hard seam, no gutter.** The split is vertical at x=540, so each panel is a tall
portrait frame. No rounding, no drop shadow, no gap. The seam is a 2px ink rule carrying the
`#rough` turbulence filter, which is the only hand-drawn element on the page.

**Classical oil, one pair of prompts.** Both panels are old-master oil painting, and the prompts
share the subject clause **verbatim**. Only two things change:

| | Before | After |
|---|---|---|
| Light | Tenebrist. One low warm source close to the subject, the rest deep umber to near black | Luminous. Clear daylight from a tall window filling the room |
| Posture | Buried, hand at the forehead, head down and away | Upright, turned toward the light, shoulders easy |
| Room | The same room, covered | The same room, clear |

That is the entire visual argument, and it is why the subject clause cannot be rewritten between
the two prompts. A different person on the right reads as a stock photo pair.

**Faces turned away or in shadow**, the same law as the noir world. Classical portraiture with a
lost profile is period-correct, so the rule costs nothing here.

**The veils are deliberately unequal.** The BEFORE panel is crushed (0.62 to 0.88) so six lines of
type hold over it. The AFTER panel is left much brighter (0.34 to 0.72) with only four lines to
carry. The reader sees the difference in the light before they read either list.

## 1a. The stacked photographic variant, not built)

A second layout for the same argument, taken from `a reference account` and recorded at
`projects/content-engine/engine/reference-bank/carousels/DbGk7k-l5sC/ENTRY.md`. Where the painted
split above runs left to right and lists both sides in full, this one runs top to bottom and puts
one pair of lines per slide across a whole carousel.

**The unit.** One frame holds two full-bleed photographs, one above the other, meeting near
mid-frame. No rule, no border, no gutter, no split-screen device. Only the pictures meet. The
measured changeover on the reference sits at 48.5% of the frame height.

**The seam is the type.** Both photographs are graded down to near black where they meet, and the
copy sits inside that shared darkness, so it reads as one caption block floating mid-frame rather
than two labelled panels. Nothing is cropped to make room for the type, so both photographs stay
whole.

**This is the only band exemption in the house** (`content-formats` section 1). It exists because the
type IS the seam. It does not license type above y=844 on any other format, including the painted
split above, which stays inside the band.

**The copy frame is fixed and repeats without variation.** Two lines per slide, a label plus a
statement, twice: the visible half, then the hidden half. The reader learns it on slide 1 and reads
the rest at a glance. Changing the frame between slides destroys the format.

**The reveal half always carries a countable number; the visible half never needs one.** Same
provenance rule as the left-hand list above: the number comes from `context/research-corpus/` or the Hub
build it describes, with its source recorded in `src`.

**The grade split is the honest signal.** On slides where the hidden work is unglamorous, desaturate
the lower photograph to black and white while the upper one keeps colour, so the reveal reads as
evidence rather than promotion. Applied by judgement, on roughly half the slides, never as a rule.

**Slide 1 buys the swipe with an origin image rather than a number**, and the closing slide lands the
moral on a single photograph.

**What the house changes from the reference.** Faces stay turned away or in shadow, per the house rule.
The accent is `#1269FF`, never the reference's red. The pairing is the reader's week before and
after a the role you place, or house against the alternative they are considering, never a
founder flex. And the caption carries the argument, because the reference's caption carries none.

## 2. The type

- Everything is your display typeface 400, the canonical face.
- A letterspaced uppercase tag at the top of each column: `before a your offer` on the
  left, `after` on the right. The right tag is blue.
- The lists sit under the tags, one line per item, each on a short rule. The left rules are ink,
  the right rules are blue.
- The closing line and the single CTA sit in the footer over a scrim, with the house lockup beneath.
- One CTA, taken from the vertical's lead magnet in the playbook. Never two.

## 3. The lists, which are the whole point

**Left: 4 to 6 pains, in their words.** Lowercase, no punctuation at the end, each one a plain
statement of a week. Pull them from the playbook's "Pains, ranked" section and its quotes, so the
line is something an owner in that industry has actually said. Six is the ceiling: past that the
type shrinks and the panel becomes a wall.

**Right: 3 to 4 lines, and no more.** The right side wins by being shorter. Each line answers a
specific line on the left rather than making a general promise, and none of them claim an outcome
the pain wiki cannot support.

**Never pair a left line with a right line that overclaims it.** "still typing listings at 10pm"
is answered by "listings go to market the day they are signed", which is a description of the
system. It is not answered by "gets her evenings back", which is a promise nobody has measured.

## 4. The data contract (`units.json`)

```
vertical, name, brand, brandTail, corpus
units[]:
  n                     the unit number
  title                 internal label, not rendered
  subject               ONE clause, used verbatim in both prompts. This is the format's spine
  beforeLabel, afterLabel   the two column tags
  before[]              4 to 6 pains, their words
  after[]               3 to 4 lines, what changed
  src                   provenance for the left list: call counts and the quotes behind it
  beforePlate: shot, brief
  afterPlate:  shot, brief
  beforeImg, afterImg   written by gen_panels.py once the plates exist
closing: line, cta
```

Panels without an image render as labelled placeholders, so the copy and the asymmetry are
reviewable before anything is paid for.

## 5. Running it

```
cd "the business/projects/content-engine/ideas/before-after-splitscreen"

python3 render.py              # every unit, free
python3 render.py 1            # one unit
python3 gen_panels.py          # DRY RUN, prints both prompts
python3 gen_panels.py --go     # PAID, two jobs, one at a time
python3 gen_panels.py --go 1   # PAID, one unit
```

Two paid stills per unit, which makes F9 the cheapest painted format in the system. A full
vertical set of four units is eight generations against F8's twenty.

## 6. The laws that bind this format

- **The education law.** F9 does not teach a system, so it never runs alone in a slot. Pair it with
  an F8 or an F5 that shows the build, or it reads as a mood piece.
- **The IP law.** The right-hand list describes the shape of what an operator builds, never a
  candidate's actual build or tool chain.
- **Scope discipline.** Every number on the left carries the scope its source supports.
- **House rules.** No em dashes, no negation swaps, no banned vocabulary, no AI tells.

## 7. Gotchas

- The model id is `your image model`. `your image model_2` 404s.
- **The two panels drift.** Generated as two jobs, the model will change the person's age, hair or
  clothing between them. The shared subject clause is the mitigation, not a guarantee. Check the
  pair side by side before compositing, and regenerate the AFTER panel against the BEFORE rather
  than regenerating both.
- The model bakes gilt frames and canvas edges into anything asked for as a painting. The tail bans
  them explicitly; regenerate a panel that comes back framed, because a painted frame cannot sit
  flush against the seam.
- Chrome resolves from `CHROME_BIN` with the macOS default as its fallback. Do not hardcode it.
- A six-line left list at 27px is the maximum before the column runs into the footer scrim. If a
  seventh pain matters, it belongs in a second unit.

## 8. Related

- `formats/industry-build-carousel/SKILL.md`, F8, which shares the furniture and the research-corpus
  discipline.
- `formats/noir-painterly/SKILL.md`, F2, the other painted world.
- `context/research-corpus/industries/`, the source of every line on the left and of the closing CTA.
- `references/canon/angles-and-formats.md`, the format registry.
- `projects/content-engine/engine/reference-bank/carousels/STYLE-GUIDE.md`, theme A, the reference
  behind the stacked variant in section 1a, and its full read at `carousels/DbGk7k-l5sC/ENTRY.md`.
