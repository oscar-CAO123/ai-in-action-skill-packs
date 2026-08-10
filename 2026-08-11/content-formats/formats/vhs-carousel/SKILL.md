---
name: vhs-carousel
description: Use when the operator says "tape carousel", "VHS carousel", "the degraded photo carousel", "type in the negative space", or wants a house carousel where each slide is one full-bleed VHS-degraded photograph with the copy sitting inside empty space composed into the shot. Builds 4:5 slides at 1080x1350: the plate fills the frame, the well is found in the plate, and the ink colour is taken off the ground it lands on. Format F12 in angles-and-formats.md.
canonical: false
format: F12
status: built and rendering on stand-in plates. Not a valid pick for the weekly draw until a real shot set passes review.
---

# Tape Carousel (F12, type in the negative space)

One photograph per slide, running the full frame, degraded like a dubbed tape. No card, no
scrim, no headline bar, no gradient behind the words. The copy sits in a flat empty region
that was **composed into the shot on purpose**, and it takes its colour from whatever ground
it lands on: cream on warm dark, white on cool dark, near black on bright.

Where F5 news-carousel borrows the trust of a headline and F8 borrows the trust of a workflow
board, F12 borrows the trust of found footage. It reads as something that was recorded rather
than designed, and the words read as a caption someone added to it.

**The vehicle is lifted from `@elevenstoic`** (`instagram.com/p/DbQkpEOAl1l/`, 12 slides,
12,868 likes) and rebuilt in the house's world. The reference is ingested, measured and written up
at `content-engine/engine/reference-bank/carousels/DbQkpEOAl1l/`. Read that ENTRY.md before
changing anything here: every law below is a measured number off those twelve slides, not a
preference.

## The two laws

**1. The empty space is built into the plate, and it is never in the middle.** The subject
holds the centre. The copy goes above it or below it, in space the prompt asked for. Measured
on the reference: the top third is empty 34% to 89% of the time (median 84%), the middle third
24% to 68% (median 50%). A plate with the subject centred and no room around it is a failed
plate, and the build says so rather than laying type over a face.

**2. The ink is taken off the ground, and it flips on luminance.** Thirty-six measured type
blocks split at a ground value of about 45%:

| Ground | Ink | Reference contrast |
|---|---|---|
| Dark, value under 45% | near white, value 98%, saturation 4% | median 12.4 : 1 |
| Dark AND warm (hue 14 to 55) | cream, hue 35 to 60, saturation 17 to 35% | |
| Dark AND cool (hue 200 to 270) | pure white, saturation 0 to 3% | |
| Light, value 45% and over | reference goes tonal | median **3.1 : 1** |

house keeps the first three rows and **refuses the fourth**. A 3:1 headline does not survive a
feed thumbnail, so on a bright ground F12 goes to a dark ink instead and holds the floor.

### The contrast floors

| Role | Floor |
|---|---|
| hook, headline, stat, CTA | **7 : 1** |
| body, eyebrow | **4.5 : 1** |

`tape.ink_for()` walks the ink away from the ground until the floor is cleared. The house blue
can be requested for an eyebrow and **will be refused** when it does not clear 4.5:1 on that
ground, which is most dark blue plates.

### The plate law that follows from the floors

A well at mid luminance **cannot** carry a headline whatever colour the type is. White gives
`1.05/(L+0.05)`, black gives `(L+0.05)/0.05`, and the two cross at relative luminance 0.179
where the ceiling is 4.58:1. For a 7:1 headline the well needs relative luminance **at or
under 0.10, or at or over 0.30**.

So the direction to the plate is: **make the empty space properly dark or properly bright.**
A grey wall, an overcast sky, a mid-tone road: all unusable for a headline. `tape.headroom()`
returns the ceiling and the build prints it on every slide.

## The grade

The house already owns a VHS grade at `content-engine/ideas/talkshow-vsl/bin/vhs-grade.sh`.
**Do not use it here.** That one emulates tube cameras dubbed to tape: 8px `rgbashift`, hard
scanlines, barrel distortion. The reference carries none of that. Measured across its twelve
slides: chroma mis-registration **0px on all twelve**, no scanline periodicity on nine of
twelve.

What it does carry, and what `scripts/grade.sh` reproduces:

| Tell | Reference | Argument |
|---|---|---|
| Grain floor | 6.97 to 12.17 | `grain`, and it is not 1:1. The measured floor lands near `grain/5.5`, so the usable range is 38 to 67. Default 48. |
| Mean saturation | **0.054 to 0.635** | `sat`. Cast **per plate**, never once across the set. |
| Black floor | 0.6 crushed to 28.5 milky | `lift`, 0.00 to 0.12 |
| Softness | SD resolution loss | `soft`, the downscale divisor, 1.6 to 3.0 |
| Chroma shift | 0px | not offered |
| Scanlines | none | not offered |

**Cast the grade per plate.** Twelve slides graded identically read as one filter applied to a
folder. The reference's saturation moves by a factor of twelve across its set, and one of its
slides is effectively monochrome.

**`format=gbrp` before the bloom is load-bearing.** Left in YUV, the screen blend runs on the
chroma planes as well as luma and turns every plate magenta. This was a real bug in the first
build, caught by measuring the rendered output rather than by looking at it.

## The type

Crisp on top of the already graded plate, never composited under the grade. the operator's call on
2026-08-10: legibility beats the extra bit of authenticity, and small body copy dissolves when
it goes through the grain.

- **Anton** for the headline and the stat, uppercase, line-height 1.04.
- **Poppins SemiBold** for the eyebrow (uppercase, 0.16em tracking), **Poppins Medium** for
  the body at line-height 1.34.
- The type block is inset 3.5% of the frame (never under 46px) from the well's own edges, so
  it never kisses the subject.
- Sizes are solved per slide against the well, by measured glyph advance (Anton 0.44, Poppins
  0.53, 6% slop). A well under 240x120px after inset is an error, not a smaller font.

## The arc

Five slides, the house length. Twelve is the reference's length and it is not ours.

| Slide | Kind | Job |
|---|---|---|
| 1 | `hook` | the hook, filled from a named structure in `references/hooks/HOOKS.md`, id cited in the deck |
| 2 | `beat` | the symptom, in the reader's own language from the pain wiki |
| 3 | `beat` | the cause |
| 4 | `stat` | one figure, traced to a source in the deck's `sources` list |
| 5 | `endcard` | the CTA and the url |

## Build it

```
scripts/plates.py     stand-in plates, free, stamped PLACEHOLDER, so layout is judged before spend
scripts/grade.sh      the tape grade, cast per plate
scripts/tape.py       the two laws: find_wells, ink_for, headroom, contrast
scripts/decks.py      the copy and the cast, one dict per slide
scripts/build.py      grade, find the well, colour the ink, lay the type, render, report
scripts/measure.py    measure any carousel: grade tells, empty share, type blocks, contrast
scripts/dossier.py    the review dossier, self-contained HTML, opens in the browser
```

```
python3 plates.py                      # stand-ins, only until real plates exist
python3 build.py --regrade             # render every slide into ./out
python3 measure.py out                 # check the output lands in the reference's bands
python3 dossier.py                     # review sheet in the browser
python3 build.py --plates /path/to/shots   # the real set
```

`build.py` prints a line per slide and writes `out/report.json`: the well it found, the ground
it sampled, the ink it chose, the contrast, the ceiling and pass or fail. **A slide that fails
still renders**, so the failure is visible instead of quietly corrected.

## Generating the plates

Route retro and authentic shots to **Higgsfield Soul Cinema** (`soul_cinematic`) per
`references/canon/model-routing.md`. It has no 4:5, so generate at 3:4 and crop to 1080x1350.

The prompt has one extra job over a normal plate: **ask for the empty space, and say how dark
it is.** Name the region, put the subject off centre, and keep the tape look out of the prompt
because the grade adds it afterwards. Something like: "shot from across the room, the owner
small in the lower third and off to the left, the whole upper half a deep unlit wall in shadow,
nothing on it".

Then check it before writing a word of type:

```
python3 tape.py /path/to/plate.png     # prints flat share by band, then every well with its ink
```

## Gates

The house floor applies: the content-formats QA gate, no em dashes, no negation-swaps, banned
vocabulary, every number traced, `context/language-rules.md` for every house-facing word. On top
of that, F12 does not ship until:

1. Every slide clears its contrast floor in `report.json`.
2. `measure.py` puts the set inside the reference's bands: grain floor 7 to 12, saturation
   varying by plate, chroma shift 0px.
3. The dossier has been looked at, not just the numbers. The measured pass is necessary and it
   is not sufficient.
