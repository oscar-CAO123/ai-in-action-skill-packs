---
name: permission-carousel
description: Use when you says "permission carousel", "the they-say format", "the two-slide notice", "the period noir carousel", "the 50s carousel", "the full-length carousel", or wants a house carousel built as full-bleed period-noir photographs at 1080x1350 with thin your display typeface set natively into space composed into the plate. Covers both mechanisms (permission-and-turn, promise-and-payoff) and both lengths (two slides, or full length at seven). Declared canonical off F8, extended off F9 the same day.
canonical: true
status: LOCKED. Shot on real plates . F8's pair is shipped and live; F9's three carousels are built and awaiting copy.
---

# The period carousel

Full-bleed mid-century photographs at 1080x1350, thin your display typeface set straight onto them with no scrim, no
card and no gradient. The space the type sits in is **composed into the plate**, never found
afterwards.

Declared canonical off F8. you: "love it. Lock that in as a new canonical style as a
new format skill." Extended the same day off F9's three carousels: "This is probably my favourite
carousel format we've ever made ... train the canonical skill on all of these outputs."

**The name is historical.** It was born as the permission carousel and it now carries two
mechanisms. Do not rename the folder: `f8_notice.py`, the card's own records and the router table all point
at this path.

## The four laws

**1. The type sits in space composed into the plate, never over a face and never over a light.**
The figure is briefed LOW and the empty band is briefed dark, so the plate arrives with the room
in it. A plate with the subject centred and no room beside it is a failed plate. **The "never over
a light" half was learned the expensive way**: a warehouse dock lamp burned through the word
"tells", and a tall lit doorway ran a column of light straight through a line. Empty is not enough.
The ground has to be dark.

**2. Every block is centred in the band above the head.** you, : "move the text down a
little bit so it's more in the centre point between the top of his head." Measure the head off the
plate, then centre the block between the top of the frame and it. **Never a fixed y**: the figure
lands somewhere different in every plate.

**3. One carousel is one roll of film.** Same era, same grain, same treatment, same person, and at
full length **the same room**. A carousel that changes location every slide is a mood board. Five
frames of one workplace is a story.

**4. Somebody else says it** (permission mechanism only). The opening line is attribution, not
permission in the house's voice. "They say you'll win if you..." gives the turn someone to be wrong
about. An earlier pass opened "It's perfectly legal to", which grants the permission in our own
voice and leaves the turn with nobody to contradict.

## The two mechanisms

Both open on a slide that makes no claim. That is the engine in both: nothing to argue with means
nothing to scroll past.

### A. Permission, then the turn (F8, live)

**Slide 1 grants permission and it is a trap.** A flat line attributing the advice to somebody
else, then five things the reader already does, set as though none of it were a problem. **Slide 2
turns it**: the verdict on one line, the reason quieter under it, the route quieter again.

The mechanism is agreement. The reader nods down slide 1 because every line is true of them, and
slide 2 spends that agreement in one move.

### B. The promise, then the payoff (F9)

**Slide 1 promises a count and withholds it.** The head and nothing else: "Five things no one tells
you before you put AI in your business." **The rest pays it**, one thing per slide, then the route
on the close.

The mechanism is the open loop, which is `hook:A3` read literally: the number in the head is the
only reason to swipe, so nothing else may appear on slide 1. A promise slide that also shows the
first item has already spent itself.

## The two lengths

**Two slides.** Setup, then the landing. Right when the payoff is one move.

**Full length: SEVEN slides**, and this is the shape you picked as his favourite.

| # | kind | carries |
|---|---|---|
| 1 | promise | the head alone |
| 2-6 | item | one numeral, one line |
| 7 | close | the route alone |

**An item slide carries no route and no count.** Repeating the CTA on every slide turns a carousel
into five ads in a row; the promise is already spent on slide 1. The only thing that changes
between the five is the numeral and the line, and that sameness is what makes the swipe read as a
list.

**The opening and closing plates do double duty.** `-one` opens and `-two` closes, which is what
each was briefed and lit for, so going from two slides to seven costs five new frames rather than
seven.

## What it is modelled on

Every entry cites an id and names what is taken, per the citation law.

| id | what is taken |
|---|---|
| `local:perfectly-fine/01-perfectly-legal-list` | the copy shape: one flat line in a light weight on a left margin, generous leading, sentence case, no terminal punctuation. **NOT its flat ground**, which is the thing being replaced. |
| `local:perfectly-fine/02-period-photo-grain` | the look: a colourised mid-century photograph, grain in the shadows, softened resolution, warm skin against a cooler ground. **NOT that account's watermark, rule or caption bar.** |
| `../noir-painterly/SKILL.md` | the lighting: single hard key, crushed blacks, the figure read as a silhouette. Grayscale is not mandatory, so this runs warm. |
| `hook:A3` | the promise mechanism only: the count in the head is the open loop. |

## The type

Thin **your display typeface** and nothing else, white, over the plate with **no scrim, no card and no gradient**. A
scrim is what both references refuse, and it is the admission that the plate was not composed with
room in it.

| Role | Weight | Size | Placement |
|---|---|---|---|
| opening line | 300 | 46-54 | top left, 78px margin, centred in the head band |
| list items on one slide | 200 | 40 | en-dash bullets, line-height 1.62 |
| verdict | 300 | 58 | centred |
| reason | 200 | 36 at 80% | under the verdict |
| route, riding under a list | 300 | 25 at 58-62% | under the stack |
| route, on its own close slide | 300 | 44 | centred in the head band |
| item line, full length | 200 | 54-56, `text-wrap:balance` | under its numeral |

**The blue accent is OFF on a plate.** On black cards the head carries one blue span; on a warm
period plate blue reads as a second light source in the room. Plain white.

**No logo and no lockup on any slide.** Neither reference carries brand furniture. The route is one
quiet line and nothing else.

### The preferred list treatment: outlined display numerals

you, : "I also love the format of the next one's text. Fuck yeah. Save that as a
preference for this style of carousel."

| Role | Treatment |
|---|---|
| numeral, in a stack of five | your display typeface 500, 82px, `color:transparent`, `-webkit-text-stroke:3px rgba(255,255,255,.82)`, fixed 132px column |
| numeral, alone on an item slide | the same stroke at 190px, 4px, the line under it |
| the count on the promise slide | the same stroke at 250px, above the head line |
| line | your display typeface 200, beside or under the numeral |

**Why it holds on a photograph**: a filled numeral at that size is a block of white competing with
the line it numbers, and a thin ring disappears into a dark plate. The stroke is loud enough to be
the picture and open enough to let the plate through it. **3px is the floor**; 2px read as a ghost.

### Hand marks on a hook: the ring and the underline

you, on the F9 hook: a word can be **circled in the canonical handwriting circle** and
another **underlined**, both by hand, both on a plate. `f9_carousel.MARK_JS` is the implementation
and `{word}` / `[word]` are the markers in the copy string.

**Both are drawn in the browser off the measured box of the word**, the same method the ruled-pad
card uses, because the word moves whenever the type re-wraps and a hand-set path is only right for
one wrap.

**The ring factor is NOT the block factor.** `f7_variants` rings a block at root two of the
half-box, because a rectangle's corners have to sit inside the arc. A three-letter word has no
corners to clear, and 1.42 threw the arc 37px past the word on both sides and cut through the
neighbours. **A single word wants about 1.10 horizontally and 1.30 vertically, with the room coming
from padding on the span** (38px each side reads as clear).

**White, not the house blue**, same call as the head: blue on a warm period plate reads as a second
light source in the room.

### Measuring the head band

`static-ads/scripts/f9_headroom.py` is the probe and `f9_carousel.HEAD_Y` is the table, keyed by
plate with the x window recorded beside each value.

**It asks for the figure's own column, and that is deliberate.** An automatic version that
thresholded the plate and took the lit mass touching the bottom edge returned the top of the OFFICE
DESKS (1297 against a true 608): these figures are dark silhouettes and are never the brightest
thing in frame. Every plate also has a practical lamp in it, and a lamp is brighter than any face.

**On a frame with no head, measure the thing the frame is about**: the top of the papers, the lathe
wheel, the lit doorway. The rule is really "where the empty ground stops".

## The copy

**Five items.** Six was tried and the rhythm sags; five reads in one breath.

**Every line has to be recognisable rather than clever.** Two sources are legitimate: LIFTED from
`suite_pains` in the second person, or authored by you. F8's shipped pair is his, dictated.

**A written list is the failure mode.** If the reader does not recognise a line, the setup does not
land and the payoff has nothing to spend.

## The plates

**your cinematic model (`soul_cinematic`)**, per `references/canon/model-routing.md`: the one model that
returns an image reading as captured rather than rendered. **It has no 4:5**, so generate at **3:4**
and crop to 1080x1350, **keeping the TOP** of the tall frame, because that is where the type goes.

### The composition strings, used verbatim

Two strings decide every brief. Paste one at the end of every prompt.

```
TOP_THIRD          The upper third of the picture is plain dark wall and nothing else,
                   unbroken and bare.

TOP_THREE_FIFTHS   The upper three fifths of the picture is plain dark wall and nothing
                   else, unbroken and bare, with no fittings, no windows and no markings
                   on it.
```

Three fifths for anything carrying a stack of five or an oversized numeral; a third for a single
line. **Name the fraction AND the camera distance.** "Fills the lower half" alone is not strong
enough: on a seated subject the model reads the pose and frames tight.

### The film string, used verbatim on every plate in a set

```
Shot on colour film in the mid nineteen fifties and scanned from the print: fine grain sitting in
the shadows, softened resolution, slightly faded dyes, warm skin against a cooler ground. The frame
is a photograph rather than an illustration.
```

One string across a whole set is what makes six or seven frames read as one roll.

### The frame vocabulary for a full-length set

Five item frames in ONE room, each a different distance and a different action. Five frames of a
man standing in the same room is one frame printed five times.

| frame | brief |
|---|---|
| mid | at a desk or bench, both hands on it, head down. ~3m |
| wide | very small and alone at the far end of the room under one light. ~10-12m |
| hands | **only the forearms and hands enter the picture, the rest of him outside the frame entirely.** ~1m |
| doorway | a **low wide** doorway in the lower two fifths, him a silhouette against the lit yard. ~8m |
| seated | on the edge of a desk or leaning on a machine, small in the frame. ~7m |

**Rooms that work**: a period study, an office of empty desks at night, a machine shop, a warehouse
loading dock. **Rooms that fight the format**: a station, a shopfront, a bar. Their whole character
is signage, and this model writes legible signage onto anything in shot.

## Build it

```
scripts live in ../static-ads/scripts/

# the two-slide build (F8)
python3 f8_notice.py                          # both slides on free beds, PLACEHOLDER
python3 f8_notice.py --plates one.png two.png # over the real plates
python3 f8_notice_plates.py                   # DRY RUN, both prompts, spends nothing
python3 f8_notice_plates.py one --go          # ONE paid job
python3 crm_f8_notice.py                      # DRY RUN of the push. --go inserts + REVERSE

# the full-length build (F9)
python3 f9_carousel.py                        # every carousel on free beds
python3 f9_carousel.py --plates               # over the real plates
python3 f9_carousel.py countdown --plates     # one carousel
python3 f9_carousel_plates.py                 # DRY RUN, every brief
python3 f9_carousel_plates.py countdown-i3 --go   # ONE paid job
python3 f9_carousel_plates.py countdown-i3 --crop # re-crop, free
python3 f9_headroom.py countdown-i3 100 1000      # measure the head band
python3 f9_carousel_review.py                 # F9-CAROUSELS.html, opens in the browser
```

## Traps already paid for

- **`--go` takes exactly one plate.** Read the returned still before sending the next.
- **A brief that places the subject without naming the frame's empty half will fill the frame.**
  Three re-shoots, one failure: "he is an out-of-focus shape behind them" put a head in the top
  corner twice, and "fills the lower half" framed a seated man tight. Name the fraction and the
  distance, every time.
- **On a hands frame the person belongs OUTSIDE the frame.** "Only the forearms and hands enter the
  picture" is the line that works. Anything else puts a face in the middle of the shot, and one
  came back with him peering through the spokes of the wheel.
- **A tall doorway is a column of light through the type band.** Brief it low and wide.
- **A centred block on a close-up lands on the face.** F8's slide 2 shipped with that defect.
  Left-anchored type over a figure composed low cannot.
- **Any aperture named in a brief becomes the frame.** Describe the camera by distance instead.
- **Banning a thing by name summons it.** Say what is in the room, not what must not be.
- **A prop arrives branded**, so every object is described as plain and unmarked.
- **Cropping a tall frame symmetrically eats the space the type needs.** Keep the top.
- **A four-word line wraps its last word alone.** `text-wrap:balance` on the item line; without it
  "...still stops when you / do." orphaned on three slides at once.
- **A dossier strip that scrolls sideways hides the carousel.** Seven slides beside a notes panel
  showed three and put four off the edge. The slides wrap, the notes go underneath.
- **your cinematic model occasionally returns a white scan border** down both edges. No crop of ours removes
  it; re-shoot.
- **An anachronism will arrive if the room allows one.** A period STUDY, not a home office. Watch
  the props: one desk frame came back with a push-button telephone.
