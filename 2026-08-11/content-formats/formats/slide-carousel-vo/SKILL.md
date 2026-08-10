---
name: slide-carousel-vo
description: Use when the operator says "slide film", "carousel film", "projector film", "slide ad", "a still per point", "the CIO 1981 style", "history film", or wants a house video where a narrated argument is told across many painted stills, one per point, cut to the voiceover's own word timings, with Kodak-carousel transitions, a VHS grade and one-word captions. Format F10. Zero motion generation.
canonical: true
format: F10
---

# Slide Carousel with VO (F10)

A narrated argument told in painted slides. The voiceover is cut first, every word gets a
timestamp, and the picture changes on the **point** rather than the sentence: forty-odd stills at
roughly a two second hold. Slide changes land as a projector advance (a beat of black, then the
next slide flicks up and settles, with a clunk), everything sits under a camcorder VHS grade, and
the canonical one-word captions go on last.

No motion model is called at any point. The movement is entirely the cut, the flick and the tape.

**Reference:** @null.histories on Instagram, hidden-history stories narrated over held frames,
crossed with the Chris Moran reel the moiré pass came from. Worked example and the whole rig:
`projects/content-engine/ideas/cio-1981-noir/` (shipped 2026-08-05, 87s, 44 beats, 49 stills).

**When to pick this format:** a story or an argument that moves through many small points, where
each point has its own image. History parallels, mechanism walkthroughs, ranked lists read aloud.
It is the format for a script that would stall on one frame (F3) and does not need a metaphor
world built for it (F2).

**When not to:** a single scene carries the whole idea (use F3), or the argument is easier to see
than to say (use F2).

---

## Production spec

```yaml
format: F10
skill: slide-carousel-vo
aspect: "9:16"
canvas: [1080, 1920]
runtime: 60-120s
models:
  still: nano_banana_pro          # ~2 credits each, one per beat
  motion: none                    # the economy of the format
  voice: elevenlabs               # engine config voiceover.voice_id
  sfx: elevenlabs sound-generation
  routing: ../../references/canon/model-routing.md   # house shot-type table; the set above wins here
inputs:
  concept: persona x angle x offer
  script: spine C, one line per spoken thought
  look: the house noir blocks, or any locked still register
  beats: one point per still, split off the word timings
layout:
  captions: dead-centre one-word Poppins, the canonical rig
  transitions: black + flick-up on line changes, hard cut on the rest
cost_shape: one still per beat plus VO plus two SFX. No video generation.
```

---

## The order that matters

**Cut the VO before the pictures.** The beat map's onsets come out of the voiceover, so every
still generated before the read exists is a guess at a hold length. The build that worked ran:

script → VO → word timings → beat map → stills → carousel → grade → sound → captions → deliver.

Doing stills first cost three full re-times on the worked example.

---

## Phase 0. Lock the brief (ask, do not assume)

Use AskUserQuestion, batch 4.

- **The argument.** What the story has to prove. Everything else follows it.
- **Density.** One still per point is the format. Confirm the target hold (about 2s) so the beat
  count is known before any spend.
- **Transitions.** Which changes get the projector treatment and which are plain cuts. Doing all
  of them is relentless; the worked example put the projector on the line changes only.
- **Sound.** Clunk on the majors, a much softer tick on the hard cuts, both generated rather than
  licensed.

## Phase 1. Environment

Higgsfield CLI (`higgsfield account status` for credits), ffmpeg/ffprobe, `/usr/bin/python3` for
PIL and numpy (homebrew python lacks PIL), the ElevenLabs key in the engine config `.env`, whisper
`small.en`, and the captions fonts. `scripts/` here holds the rig; every script resolves its own
directory, so copy the folder into the project and run in place.

## Phase 2. Script

Spine C, written and gated before anything is spent. One line per spoken thought in `vo/lines.txt`,
because that file is simultaneously the TTS input, the caption source and the major-change map.
Craft and the QA gate: `skills/content-formats/SKILL.md`.

## Phase 3. VO

`scripts/vo_stems.sh` cuts one stem per line so line boundaries stay exact, then
`scripts/join_vo.py` trims each stem's own head and tail, butts them together over controlled gaps
and writes `vo/timeline.json`.

- **Gaps are the pace control.** 0.12s default with 0.20 to 0.35 at the turns reads tight. Going
  to 0.30/0.45-0.70 adds about five seconds across twenty lines.
- **Never `loudnorm`.** Static peak normalisation only.
- **Heal, then re-align.** `vo_utils.heal_clicks` clears join clicks but returns an mp3 stream, so
  it prepends encoder delay. Measure the head silence before and after and trim the difference
  back off, or every cut in the film drifts.
- **Tightening a single line** is `vo_utils.tighten` on that stem, then rejoin.

## Phase 4. Word timings and alignment

`whisper_words.py` against the **exported audio**, then `scripts/align_words.py`, which is what
makes the captions trustworthy:

- **Insert what whisper swallows.** It drops a word occasionally ("look" in "And now look who runs
  the world"), and a missing word silently shifts every timing after it.
- **Retext from the script.** Whisper writes "60s" where the script says "sixties". The timings
  are whisper's, the spelling is always the script's.
- **Strip whisper's own marker** off the first token.

## Phase 5. The beat map

One entry per point: `{start, text, still, fx, fy, major}`.

- Splits are token offsets within a line, so a beat can start mid-sentence on the exact word.
- **A major is the first beat of a spoken line.** Flag it here. Do not try to detect it by matching
  beat onsets against the stem starts, because those are different measurements and it silently
  finds almost nothing.
- Assert the count matches the still list, that every still file exists, and that no beat starts
  before the one before it.

## Phase 6. The stills

One per beat, one generation at a time. `STYLE + <scene> + LIGHT`, with the 9:16 tail from
`formats/noir-painterly/SKILL.md`. Review the contact sheet, never the frames one by one.

Scenes are literal: the line says two men invented a job title, so the frame is two men at a desk.
The moment a still stands in for a point it does not show, that beat reads as filler.

## Phase 7. Carousel render

`scripts/carousel.py`. Holds each still for its beat, and on a major: three frames of black at the
**end of the outgoing beat**, then the incoming slide flicks up from below over five frames with a
back-out overshoot and settles. Putting the black at the start of the incoming beat instead lands
the new picture a fifth of a second after its word.

It writes the silent body plus the SFX cue lists.

## Phase 8. Grade, sound, captions

- **VHS on the body only** (`scripts/finish.sh` carries the camcorder chain). The end card is the
  brand card and never gets graded; captions go on after the grade so the type stays crisp.
- **Sound:** ElevenLabs `sound-generation` for both cues. A clunk on the majors around 0.34 gain,
  a much softer tick on the hard cuts. Majors fire on the black, minors on the cut frame.
- **Captions:** `scripts/captions_fast.py`, identical look to the canonical rig. Use it rather than
  `engine/tools/captions/burn_captions.py`, which opens one looped PNG input per word and stalls
  past roughly eighty words.

## Phase 9. Deliver

Master at CRF 18 is enormous under tape grain (105MB for 87s). Ship a CRF 21 encode capped around
6 Mbps with faststart, which lands in the 20-45MB range the CRM's other videos sit in. Thumbnail
comes from the **graded body before captions**, or a caption word gets baked into it.

Then the CRM: upload to the `content-media` bucket with the service-role key, and insert one row
into `content_items` (`content_type='video'`, `production_status='ready'`). Show the exact write
and wait for the operator's go, per the standing Supabase gate.

---

## Hard rules and gotchas

- **`ffmpeg -nostdin` inside any loop.** Without it ffmpeg eats the piped beat list and the later
  beats come out at fractions of a second.
- **A stem's last silence is not always its tail.** Once a stem has been tightened, the last
  detected silence is an internal pause; treating it as the tail cuts real speech off the end of
  the line. The tail only counts if it runs to the end of the file.
- **Never drop zero-duration whisper words.** They render fine, since each word shows until the
  next word's onset. Dropping them deletes real words from the captions.
- **Zero motion generation.** Calling an i2v model makes this F2 and it should route there. A
  Kling 3.0 versus Seedance 2.0 Mini split test on the worked example picked Seedance, at roughly
  65 credits per 5s clip, which is about 2,900 credits to animate forty-four beats. That is a
  separate decision and a separate format.
- **The cutout treatment was tried and dropped.** Lifting each frame's subject as a floating
  magazine cutout: i2i either redraws the object at a new size and angle, or refuses to green out
  the room, and segmenting off the plate gives a blobby edge. Notes in the worked example's BRIEF.
- No em dashes, no negation swap, banned-vocabulary clean.
- Deliver by opening the local mp4.

## Related

- Canon: `references/canon/angles-and-formats.md` (F10).
- Look: `formats/noir-painterly/SKILL.md` for STYLE, LIGHT and the 9:16 tail.
- Voice and click-free chain: `reference_your_table_clickfree_pipeline`, `engine/tools/vo_utils.py`.
- Captions governance: `engine/tools/captions/README.md`.
- Optional shimmer instead of a push: `engine/tools/moire/`.
- Worked example: `projects/content-engine/ideas/cio-1981-noir/`.
