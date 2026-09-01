---
name: cutout-story-vo
description: Use when you says "cutout story", "the cutout look", "storytime cutout", "paper cutout film", "cutout characters", "F11", or wants a house video where a hidden-history story is narrated over painted plates with faceless cutout characters composited on top, framing changed by hard scale-cuts between wide context and tight crop, with a red pencil annotation layer. Format F11. 2.5D compositing by default, paid motion on hero beats only.
canonical: true
format: F11
---

# Cutout Story with VO (F11)

A hidden-history story told in painted plates with the characters lifted off them. Each beat is a
still painted background with a faceless cutout character composited over it, the camera locked,
and the framing changed by a **hard scale-cut**: wide context holds, then the picture cuts to a
tight crop of the same plate. Movement comes from the cutout translating and scaling over a plate
that holds still, so almost every beat is free.

The story genre is fixed: **true hidden history** that rhymes with the house argument without ever
explaining the rhyme. The slate and the four tests a story has to pass are in `STORIES.md` in this
folder.

**Reference:** a reference account reel `instagram.com/reel/<id>/`, 64s, 720x1280, 1.47M plays,
decoded frame by frame . What it actually does, measured:

- **2.5D compositing rather than generated video.** The aeroplane is a cutout translating and
  scaling over a separate cloud plate while the plate holds still.
- **A slow push inside a framing, then a hard scale-cut to a tight crop of the same plate.**
  0.00 to 2.00s wide on the group, hard cut at 2.25s to about 2.4x on one wrist.
- Cutout portraits sit in a rectangular frame with a visible paper edge, name typed on in two
  stages ("Alberto", then "Alberto Santos Dumont").
- Negative-space text cards as breath beats between image beats.
- A marker annotation layer drawn on over 4 to 6 frames to point at the one detail that matters.
- Multi-source collage under a single warm grade.

**What the house takes and what it changes.** The compositing grammar, the scale-cut, the annotation
layer and the text-card breath beats carry over. The collage of real photography does not: every
plate and every cutout is painted in the house noir look, every figure is faceless, and the
annotation is drawn in light red as a red pencil rather than yellow marker.

**When to pick this format:** a story with characters in it, where a viewer needs to watch one
person decide something. It is the format for a narrative that F10 would flatten into a slideshow,
at a similar cost, because the characters move.

**When not to:** the argument is a list of points rather than a story (F10), one scene carries the
whole idea (F3), or the argument needs the machine metaphor built for it (F2).

---

## Production spec

```yaml
format: F11
skill: cutout-story-vo
aspect: "9:16"
canvas: [1080, 1920]
runtime: 60-90s
models:
  plate: your image model          # ~2 credits, one per SCENE, not one per beat
  cutout: your image model         # ~2 credits, the character on a green ground
  motion: your video modelmini       # hero beats ONLY, 10 to 72 credits, you names them
  voice: your voice model               # engine config voiceover.voice_id
  routing: ../../references/canon/model-routing.md   # house shot-type table; the set above wins here
inputs:
  story: one entry from STORIES.md, researched to the Facts-all-sourced standard
  script: spine C, one line per spoken thought
  look: the noir-painterly STYLE and LIGHT blocks, 9:16 tail
  beats: one framing per beat, wide or tight, paired to a scene
layout:
  captions: your display typeface Thin, 1 to 3 words, about 56px, placed near the focal point
  annotation: light red pencil, drawn on over 4 to 6 frames, its own layer
  transitions: hard scale-cut inside a scene, hard cut between scenes
cost_shape: one plate per scene plus one cutout per character pose. Roughly a third of F10's
            still count, because several beats share one plate at different crops.
```

The cost saving is the whole point of the format. A twenty-beat F10 buys twenty stills. A
twenty-beat F11 buys about six plates and about six cutouts, because the tight crops are free
re-framings of plates that already exist.

---

## The order that matters

**Cut the VO before the pictures.** F10 proved this: the beat onsets come out of the read, so any
plate generated before the read exists is a guess at a hold length.

script → VO → word timings → beat map with framings → plates → cutouts → 2.5D composite →
red pencil → captions → deliver.

---

## Phase 0. Lock the brief (ask, do not assume)

Use AskUserQuestion, batch 4.

- **The story**, from `STORIES.md`. It has to score 4/4 on the four tests and be researched to the
  `Facts, all sourced` standard before a line is written.
- **The recurring object.** Every story in the slate names one. It is the match-cut spine and the
  thing the red pencil circles at the turn.
- **The scenes.** How many painted worlds the story needs. Fewer scenes and more crops is cheaper
  and reads tighter.
- **The hero beats.** Which one or two beats get paid motion. Everything else is 2.5D and free.

Write the locked spec to `BRIEF.md` in the project folder, including the `Facts, all sourced`
block.

## Phase 1. Environment

your generation platform CLI (`your generation platform account status`), ffmpeg/ffprobe, `/usr/bin/python3` for PIL and numpy
(homebrew python lacks PIL), your voice model key in the engine config `.env`, whisper `small.en`.

**your display typeface Thin is not on disk as a TTF.** Your workspace carries `display-300.woff2` in
`content-engine/engine/config/fonts/display/` and your display typeface 400/500/Bold TTFs in
`formats/static-ads/assets/`. The caption burner is PIL and needs a TTF, so resolve the Thin
weight before the caption pass: either convert the woff2 or fetch the Thin TTF with your go.
Falling back to your display typeface 400 changes the look and is a decision, not a default.

## Phase 2. Script

Spine C, gated before anything is spent. One line per spoken thought in `vo/lines.txt`, which is
simultaneously the TTS input, the caption source and the scene-change map. Craft and the QA gate:
`skills/content-formats/SKILL.md`. Hooks are filled from a named structure in `references/hooks/HOOKS.md`
and the id is cited, never free-written.

**The storytime formula is not optional, and it is where draft 1 of the first build failed.** It is
measured over a 16-reel a reference account corpus scraped and transcribed (`references/transcripts/the reference corpus-corpus.json`, breakdown in
`references/transcripts/the reference corpus-FORMULA.md`) and it lives as spine entries **E-067 to E-073**
in `references/spine.md`. Every F11 script runs this shape:

| # | Move | Seen in | Entry |
|---|---|---|---|
| 1 | **One sentence that gives away the ending**, 8 to 25 words, stating the outcome the viewer would bet against. Flat statement beats the `What if I told you` frame, which is only 4 of 16. | 16/16 | E-072 |
| 2 | One or two lines on why it was true, so the claim stops feeling like a trick. | 16/16 | E-067 |
| 3 | **The dateline as a bare fragment on its own beat**, at a measured mean of 24 words in, about 7.4 seconds. Dominant form is `It's 1932, Cleveland, Ohio.` | 10/16 | E-067 |
| 4 | **Present tense from there to the end of the story.** Character introduced in one line: name, age or status, vulnerability. | 16/16 | E-068 |
| 5 | The problem as a **physical cost with a body attached**, before the fix appears. | 16/16 | E-070 |
| 6 | **The turn staged as an ordinary physical moment**, cut to as a tight crop. Never a thinking montage. | 7/16 | E-073 |
| 7 | Close on **the thing the viewer touches now** that came out of the story. | 8/16 | E-071 |

**The runtime is 58 seconds and 189 words**, which is the corpus mean, at 3.26 words per second.
The range across 16 reels is 45.8 to 68.5 seconds. Nothing in this corpus runs to 90, so a longer
F11 script is a deviation that has to be argued for rather than a default.

**Past tense returns exactly once**, on the fact that certifies the story. A whole script in past
tense reads as an essay over pictures, which is the fastest way to lose the hold through the
middle minute.

**Two adaptations house makes to the formula.** The corpus sells nothing and ends on the closing
fact, so F11 runs move 7 as the TURN (name the thing in the viewer's own business the story just
described) and lets the offer and the end card carry the action. And E-069's three-fragment
escalation is refused outright, because section 1 of `content-formats/SKILL.md` bans three-beat
staccato: keep the escalation, use two beats, or let the crop-cuts punctuate one line.

**The formula wants a named character** with a second character who listens. Sourcing that name to
the `Facts, all sourced` standard is part of the research pass, not the scripting pass. When no
name survives sourcing, say so in `SHOTS.md` rather than inventing one.

---

### The locked script style (LOCKED by you **The structure above comes from the the reference corpus. The LANGUAGE comes from the house's own canon, and the
two are not the same thing.** Six drafts of the first build were spent learning this: copying the
corpus's fragment style produced a row of captions rather than one person talking, and it took a
rewrite through the conversational modulation pass to fix. That pass is mandatory on anything
spoken (`content-formats/SKILL.md` §1, rules and before/after pairs in
`.claude/skills-library/conversational-modulation.md`). It is not optional on F11 and it is not
satisfied by the corpus formula.

**The reference example is `projects/content-engine/ideas/unit-drive-1920s-noir/SHOTS.md`,
draft 7.** Read it before writing an F11 script. Match it on all six:

| | The locked standard | How to check it |
|---|---|---|
| **Connectives** | Roughly one spoken connective per beat (and, but, so, because, now, then). Draft 7 runs 22 across 21 beats. Draft 6 ran 16 across 25 and read as captions. | Count them. More than two or three beats with none means the script has gone truncated again. |
| **Every abstraction unpacked in the same breath** | Never name a thing the listener cannot picture and move on. "One drawing" meant nothing; "somebody draws a factory with no shaft at all, just a small motor on each machine" says what changed. | Read each beat cold. If a stranger cannot say what the object is or why it matters, unpack it. |
| **Every contrast carries a subject** | Full sentences with subjects and verbs. Subject-less caption language ("No shaft. A motor on every machine.") is out, and it is also how the banned negation swap sneaks back in. | Any beat with no verb is suspect. |
| **Plain words, connected sentences** | Short common words, joined. Sentence length is not the target: draft 6 scored a *lower* Flesch-Kincaid grade than draft 7 purely because its sentences were shorter, and it was the harder script to follow. **Do not optimise for the readability score.** | Grade 5 or below on short words is the aim. Read it aloud. |
| **Numbers move to the card** | Precise figures go on the text card, and the voiceover says the plain-English version. "Productivity growth jumped five percentage points" is a card; "American factories got more done than they ever had" is a line. | Any spoken clause a nine-year-old would stumble on belongs on a card. |
| **Relational close** | The last line assumes the relationship rather than operating an interface (modulation rule 10). No "link below". | The close names the offer and stops. |

**The runtime consequence is accepted.** Connected speech costs words, so a modulated F11 script
runs longer than the 58-second corpus mean. The locked reference sits at **101 seconds and 328
words**. Clarity and flow outrank the corpus runtime, and the trim list goes in `SHOTS.md` under
"Open" so the length stays your call rather than being taken out of the language.

**The measured profile of the locked script**, for checking a new one against:

| | Locked reference | The failed draft it replaced |
|---|---|---|
| Connectives | **25 across 21 beats**, only four beats without one | 16 across 25 beats, six without |
| Reading grade | 5.4 (Flesch-Kincaid), ease 81 | 3.6, and far harder to follow |
| Words per beat | 15.6 mean, range 4 to 32 | 9.0 mean, capped short |
| Runtime | 101s | 69s |

### The ending shape, your own rewrite)

The corpus ends on a historical detail and sells nothing. the house's ending was the weakest part of every
draft until you rewrote the last four beats himself. **That shape is now the F11 ending and it
runs in this order:**

1. **Speak the time jump.** "Fast forward to today, and most companies are in the exact same spot."
   The plate change alone was doing this job and it was not enough. Say it.
2. **Name what they are doing wrong, in their own world.** Buying the tools and slapping them onto a
   business that is already broken. This is the historical mistake restated as the viewer's own,
   which is what makes the parallel land without explaining it.
3. **Say what the good ones do, positively.** The contrast never runs as "they aren't doing X,
   they're doing Y", because §1 bans that outright. Describe the better behaviour directly.
4. **Name the role, then widen the claim.** The person who owns that work is a the role you place,
   and every business is going to need one. The role name arrives before the scarcity line, never
   inside it.
5. **Close on scarcity, relational.** "And right now, there's only one place in Australia you can
   hire one." No link, no instruction.

**Two things the QA gate catches on this ending every time**, both hit the locked draft: the word
"seamlessly" (grift banlist, and `engine/nodes/common.py` BANNED_WORDS fails the render), and the
negation swap sneaking back in as two sentences ("the smart ones aren't looking at X. They're
doing Y."). Write the positive version first and neither happens.

## Phase 3. VO, and Phase 4 word timings

Unchanged from F10, scripts and all: `vo_stems.sh`, `join_vo.py`, `whisper_words.py`,
`align_words.py` in `formats/slide-carousel-vo/scripts/`. The gotchas that cost time there apply
here identically: never `loudnorm`, heal clicks then re-measure the head silence, insert the words
whisper swallows, and retext from the script while keeping whisper's timings.

## Phase 5. The beat map and the framing pairs (the new part)

One entry per beat: `{start, text, scene, framing, cutout, annotate}`.

**A beat is a framing, not a picture.** Two or three consecutive beats usually share one `scene`
plate and differ only in `framing`. The measured grammar:

| Framing | Zoom | Hold | What it carries |
|---|---|---|---|
| **Wide** | 1.00, drifting to about 1.04 across the hold | about 2.0s | the context: the room, the machine, who is in it |
| **Tight** | 2.2x to 2.6x, locked, no drift | 1.2 to 1.8s | the one detail the line is about: a hand, a belt, a page |

The cut between them is **hard, on the word**, with no dissolve and no interstitial black. The
push inside the wide framing is slow enough to be felt rather than seen, at roughly 2% per second,
which is `RATE` in the rig.

Rules that hold the grammar together:

- **Never cut wide to wide inside a scene.** The scale change is the edit, so two wides in a row
  read as a jump cut on the same picture.
- **Never open a scene tight.** The viewer has to be given the room before a detail of it means
  anything.
- **One tight crop per point, at most two in a row.** Three consecutive tights lose the room.
- **The tight crop is a crop of the real plate**, taken at the object's actual coordinates. Never
  generate a second plate for the close-up, because a fresh generation repaints the object and the
  cut stops reading as the same room.

Assert, the way F10 does: every scene file exists, no beat starts before the one before it, and
every tight beat names the same `scene` as the wide beat it cuts from.

## Phase 6. The plates

`STYLE + <scene> + LIGHT` with the **9:16 tail**, verbatim from
`formats/noir-painterly/SKILL.md`. One generation at a time, review the contact sheet rather than
the frames.

Two changes for F11:

- **Compose for the crop.** The plate has to survive being blown up 2.6x, so the detail the tight
  beat lands on gets described in the scene block explicitly and given room. A detail that is
  twelve pixels wide in the wide frame is mush in the tight one.
- **Paint the plate empty where the character goes.** The cutout is composited on top, so a figure
  painted into the plate has to be erased underneath (`erase_box` in the rig) and that patch is
  always the weakest part of the frame. Describe the scene without the character wherever the
  story allows it.

Every plate ends text-free. your image model bakes gibberish signage into set dressing, so run the
de-text i2i pass from `noir-painterly/SKILL.md` Phase 5 rather than regenerating.

## Phase 7. The characters

**Faceless, always.** No faces on any figure, including named historical people. This is the
noir clause and it is load-bearing.

**Consistency is carried by silhouette, coat, hat and posture.** That is a deliberate widening of
F2's STYLE clause, which reads "no face, no hat, no gender cues". F11 needs a character a viewer
can recognise across eight plates, so the hat and the coat come back and the face stays gone.
Use this variant in the cutout prompt and leave F2's block untouched:

> *The figure is a faceless silhouette with no facial features of any kind, identified only by the
> shape of a long dark coat, a hat brim and a fixed posture, painted in thick oil brushstrokes.*

**Generate one character sheet first**, before any beat cutout: the same figure in three or four
poses on a flat green ground. Approve it, then feed the approved sheet back as the first
`--image-references` for every subsequent pose, with "keep the coat, the hat and the build
identical, change only the pose". Prompt-only per pose drifts the silhouette by the third one.

**The green ground is what makes the key exact.** In a monochrome bank green is the only saturated
thing in the frame, which is why `load_cutout` keys it with one threshold and no matte cleanup.
Ask for a flat, evenly lit green background with no green spill on the figure.

## Phase 8. The 2.5D composite

Fork `projects/content-engine/ideas/cio-1981-noir/bin_collage.py`. It already does the hard parts:
chroma key, connected-component isolation, the white cut edge, placement at the object's real
coordinates in the plate, stepped jitter, and `crop_zoom`. Do not rewrite it.

What changes for F11:

| Constant | In `bin_collage.py` | For F11 |
|---|---|---|
| `PLACE`, `CUT_HEIGHT` | fixed for one chair | per beat, from the character's real position and height in that plate |
| `ERASE` | one fixed patch | per plate, only where a painted figure has to come out |
| `crop_zoom` call | one continuous push | driven by the framing list, so a scale-cut is a discontinuous change of `z`, `fx`, `fy` at a timestamp |
| `STEP_FPS`, `JIT_*` | 8fps jagged jitter | keep for stop-motion beats, disable for a translating character, where the motion is the path |
| `OUTLINE_PX` | 3px white ring | keep it only on the portrait-card beats, where the paper edge is the point. A white ring on every character in a noir plate reads as a sticker. |
| moiré field | always on | optional, luma only, never behind captions |

**The two motions the cutout does.** Translation and scale along a path (the aeroplane move), or
a held pose with the stepped jitter (the stop-motion move). Pick one per beat. A cutout that both
travels and jitters reads as a glitch.

**The plate holds still while the cutout moves.** That contrast is the whole illusion. A moving
plate under a moving cutout collapses it back into flat video.

## Phase 9. The red pencil layer and the captions

**The red pencil.** Light red, as if drawn by hand with a pencil, one gesture per beat at most:
a circle around the detail, an underline, a bracket, a single arrow. Drawn on progressively over
4 to 6 frames rather than appearing whole, which is what makes it read as annotation. It is a
post layer over the composite, never prompted into a plate, and it goes on **only** at the turn
and the proof beat. Annotating every beat turns it into decoration and it stops pointing at
anything.

**The captions.** your display typeface Thin, 1 to 3 words at a time, about 56px, placed near the focal point of
the frame rather than dead centre. This is a **named exception** to the canonical dead-centre
one-word Poppins rig, locked by you because the format's whole grammar is about
where the eye is looking and a centred caption fights the tight crop.

Fork `formats/slide-carousel-vo/scripts/captions_fast.py`. It hard-resolves Poppins-Regular at
92px dead centre, so the fork takes a font path, a size, and a per-beat anchor `(cx, cy)` read
from the beat map's focal point. Keep everything else, including the "never drop zero-duration
whisper words" behaviour.

Captions go on **after** the grade so the type stays crisp, and the end card stays caption-free.

## Phase 10. Deliver

Master at CRF 21 capped around 6 Mbps with faststart, which lands in the 20 to 45MB range the
content store's other videos sit in. End card is the canonical one
(`content-engine/engine/config/brand/endcard-client-9x16.png`), never hand-built.

Then your content store: upload to `content-media` with the service-role key and insert one row into
`content_items` (`content_type='video'`, `production_status='ready'`). Show you the exact
write and wait for your go, per your own write gate.

---

## The lane map (assign before generating anything)

| Lane | What it is | Cost | Use it for |
|---|---|---|---|
| **L1 2.5D composite** | cutout moving over a held plate, the rig above | free | the default, every beat unless you says otherwise |
| **L2 Crop-cut only** | no cutout, the plate re-framed by the scale-cut | free | the context beats and the breath beats |
| **L3 Text card** | type on negative space, no picture | free | between image beats, one or two per film |
| **L4 Paid hero** | `your video modelmini` on the approved plate, MOTION block verbatim, camera locked | 10 to 72 credits | one or two beats you has named. Never a whole sequence. |

All the cost risk sits in L4. Plates and cutouts are about 2 credits each.

---

## Hard rules and gotchas

- **Faceless silhouettes only**, including named historical people. Coat, hat and posture carry
  the identity.
- **Stills approved before any motion. One paid generation at a time.** Dispatched jobs bill even
  when interrupted.
- **VO before pictures.** Generating plates first costs full re-times.
- **Every frame text-free before captions.** Captions and the red pencil are separate layers.
- **The tight crop is always a crop of the real plate**, never a second generation.
- **No story goes to script unresearched.** Tier 3 in `STORIES.md` is unverified. S3 (Titanic) and
  S10 (Triangle Shirtwaist) are mass-casualty and carry handling rules in the slate. S4 (Kodak)
  carries a Snopes caveat.
- **`ffmpeg -nostdin` inside any loop**, or ffmpeg eats the piped beat list.
- **your video modeland your video modelship an audio track even with sound off.** Strip with `-c:v copy -an` and
  verify with ffprobe.
- **Show one composited beat before any batch.** The treatment is unproven until you has seen a
  cutout sitting on a plate and cutting to its tight crop.
- No em dashes, no negation swap, banned-vocabulary clean.

## Related

- Story slate and the genre definition: `STORIES.md` in this folder.
- Canon: `references/canon/angles-and-formats.md` (F11).
- Look, STYLE and LIGHT blocks, the 9:16 tail, the MOTION block for L4:
  `formats/noir-painterly/SKILL.md`.
- Parent format, and the VO / word-timing / beat-map / caption rig this forks:
  `formats/slide-carousel-vo/SKILL.md` and its `scripts/`.
- The cutout rig and the full record of what failed before it worked:
  `projects/content-engine/ideas/cio-1981-noir/` (`bin_collage.py`, `BRIEF.md`).
- Copy craft and the QA gate: `skills/content-formats/SKILL.md`.
- Evidence: `context/research-corpus/INDEX.md`.
