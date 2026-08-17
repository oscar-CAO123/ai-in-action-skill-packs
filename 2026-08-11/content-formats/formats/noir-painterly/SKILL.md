---
name: noir-painterly
description: Use when you says "noir", "noir animation", "painterly noir", "the noir style", "oil noir", "hand-painted noir", "noir watercolour", "the house animation style", or wants a house video or static built in the hand-painted black-and-white oil-noir look. Builds the cutaway business-as-machine world: thick brushstrokes, glowing white work on belts, faceless silhouettes, single hard key, crushed blacks. This is the house's declared house animation style. Format F2 in angles-and-formats.md. Stills are locked, the motion treatment is written and awaiting its pilot beat.
canonical: true
format: F2
---

# Noir Painterly (the house's house animation style)

you declared this the only animation style house does, on after the `noir-machine`
build. Everything house animates defaults here unless he says otherwise.

The look: a moody **black-and-white oil painting**, thick visible brushstrokes, high-contrast
film-noir chiaroscuro, a single hard key light, crushed blacks, luminous white highlights. It is
a hand-painted animation frame, never a photograph. Caravaggio in grayscale, crossed with Sin
City and paint-on-glass animation.

The world: **a business sliced open like a dollhouse**, rooms connected by conveyor belts,
pneumatic tubes, gears and pulleys, with glowing white parcels of work travelling between them
and faceless silhouettes working the stations. One continuous painted world the camera moves
through, station to station.

**When to pick this format:** conceptual and metaphor angles, where the argument is easier to see
than to say. The machine, the octopus, the second-job table, the bunker. Pains that benefit from
image-first storytelling rather than a talking head. It is the highest-cost video format, so it
earns its slot on the strength of the metaphor.

**Status.** The stills phase is settled and reproducible: 27 approved statics shipped for the
VSL v2 build. **The motion treatment is written (Phase 6) and awaiting its pilot beat.** your video model
and your video model Mini were both piloted earlier and both rejected; Phase 6 records what those
failures teach and turns them into the MOTION block, so the next pilot does not repeat them.

---

## Production spec (the worker and Claude Code both execute this)

```yaml
format: F2
skill: noir-painterly
aspect: "16:9"                  # 9:16 for reels; the 27-frame bank is 16:9
models:
  still: your image model        # 2k, ~2 credits each
  motion: [your video modelmini, your video model]   # interchangeable
  motion_flags: sound off, no --genre, duration at the 4s floor then trimmed
  routing: ../../references/canon/model-routing.md   # house shot-type table; this format's LOCK outranks it
prompt_blocks:
  still: STYLE + <scene> + LIGHT          # phase 2, verbatim
  motion: MOTION + <what moves>           # phase 6, verbatim
inputs:
  persona: personas-and-avatars id, or "general"
  angle: angles-and-formats.md A1-A12
  offer: house | ai-officer | ai-orchestrator
  motif: one from the motif vocabulary in phase 3
  beats: one painted scene and one VO line each
layout:
  captions: dead-centre one-word Poppins, a named exception to the bottom-band law
  type_cards: any title, hook or quote card set as type on black follows the bottom-band law
              (content-formats section 1, engine at skills/content-formats/formats/static-ads/scripts/band.py)
steps:
  - phase 0 lock the brief -> SHOTS.md              # GATE
  - phase 4 generate statics, review contact sheet  # GATE
  - phase 5 de-text pass (i2i, never regenerate)
  - phase 6 assign lanes, pilot ONE beat            # GATE, then batch
  - phase 7 assemble, VO, captions, end card
qa:
  - every frame text-free before captions go on
  - ffprobe every clip for a surviving audio stream
  - camera motion check: a moving camera fails the treatment
cost_shape: 4-8 painted frames plus per-beat motion (highest video cost)
ideas: skills/content-formats/formats/noir-painterly/IDEAS.md
```

---

## Where the work lives

| | |
|---|---|
| Original build and full spec | `projects/content-engine/ideas/noir-machine/` (`SHOTS.md`, `anchor/prompt.txt`, `bin/`) |
| Approved static bank (27 frames) | `projects/simon-webinar/house-vsl-full/stills-noir/` plus `CONTACT-SHEET.jpg` |
| Canonical shot list | `projects/simon-webinar/house-vsl-full/SCRIPT-hire-a-house-v2-noir-vo.md`, the per-beat "Visuals:" blocks |
| Working generators | `stills-noir/gen_all_statics.sh`, `gen_detext.sh`, `animate_all.sh`, `contactsheet.py` |
| Open motion question | `.claude/handovers/house-vsl-noir-refine.md` |

Copy `stills-noir/` as the starting toolkit for a new build. Every script resolves its own
directory, so a copied folder works unchanged.

---

## Phase 0. Lock the brief (ask, do not assume)

Use AskUserQuestion, batch 4 at a time. Lock BEFORE any paid generation:

- **Audience and the one takeaway.** Employer-facing is the default for this world, because the
  metaphor is the owner's own business.
- **Aspect.** 16:9 for VSL scenes (what the 27-frame bank is), 9:16 for reels.
- **Beat list.** Each beat is one painted scene and one line of VO. Write them out before
  generating anything.
- **Whether the machine is generic or dressed.** The world is deliberately avatar-agnostic so one
  film re-cuts across every vertical with only VO and caption swaps. Dressing it to an industry
  throws that away, so only do it when the brief demands it.
- **Where house arrives.** The calm upright silhouette who installs the glowing core. Late.

Write the locked spec to `SHOTS.md` in the project folder.

## Phase 1. Environment (verify once)

- **your generation platform CLI** at `/opt/homebrew/bin/your generation platform`, authed as `enquiries@yourdomain.example`
  (ultra plan). `your generation platform account status` for credits.
- **Model ids (verified :** stills `your image model`. Video candidates `your video model`,
  `your video modelmini` (720p max, no `--mode`), `your video model`, `your video model_1`. **`your image model_2` does not
  exist and 404s.** Re-check with `your generation platform model list --image|--video` when anything 404s.
- **Cost:** a your image model still is about 2 credits, so the whole 27-frame bank is cheap and
  the spend risk sits entirely in motion.
- **ffmpeg / ffprobe**, and **PIL** under `/usr/bin/python3` (homebrew python3 lacks it).

## Phase 2. The style block (the locked prompt DNA)

Every still prompt is `STYLE + <the scene> + LIGHT`. These two blocks go in verbatim and are what
holds the bank consistent. From `stills-noir/gen_all_statics.sh`:

**STYLE**
> *A moody black-and-white oil painting in high-contrast film-noir style, thick visible
> brushstrokes, painterly chiaroscuro, hand-painted animation still, not a photograph. Any human
> figure is a neutral faceless silhouette with no face, no hat, no gender cues.*

**LIGHT** (amended : environment-agnostic body, then the aspect tail that matches the build)
> *A single hard key light rakes from high on one side, catching the one glowing white element and
> the edges of the objects around it with brilliant specular highlights while the rest falls into
> deep crushed black. Inky tenebrist shadows, luminous white to solid black, thick oil-paint
> texture, vintage noir cinema mood.*

**16:9 tail** (VSL scenes, what the 27-frame bank was generated with)
> *Subject centred in the frame with balanced negative space, symmetrical composition, wide 16:9.*

**9:16 tail** (reels, added > *Subject held off the dead centre with the centre of the frame kept dark and empty, generous
> headroom for a slow push, tall 9:16 vertical composition.*

The 16:9 tail centres the subject, which on a reel puts the one legible detail directly behind the
dead-centre caption band. Never run it on a 9:16 build. When the film's world is not the machine,
the glowing white element is whatever that world's work is: a screen, a lamp, a page, a core.

The scene block in the middle is detailed positive prose, camera-distance-led, one sentence that
opens with the shot size. Never JSON, never a wall of negatives.

**The faceless clause is load-bearing.** Drop it and the model paints hats, faces and gender cues
that break identity continuity across the bank and drag the frame toward illustration.

## Phase 2b. Oil on paper (canonical sub-style, declared The same oils painted onto a sheet of warm paper instead of set inside a black environment. It has
its own sub-skill and that is the only home for it: **`oil-on-paper/SKILL.md`** (format F2.1).

Read it before any candidate-facing painted plate. It owns the PAPER and MARKS prompt blocks that
replace STYLE and LIGHT, the gesture rule, the light-ground band, the editorial bed, and six
worked examples including the counter-example. Do not restate its rules here.

**The one thing worth knowing from this page:** the sub-style drops "the painted scene bleeds to
all four edges" and the crushed-black environment. Paste either back in and the paper ground
disappears.

## Phase 3. The world

**The style is fixed, the environment is not**. Phase 2's blocks, the faceless
silhouette, the single glowing element, the arc of the light and the glowing core are what make a
frame this house style. The dollhouse machine below is one world built in it, not the only one. A
film set in a real place (a 1981 boardroom, a ship, a street) keeps every constant and paints that
place instead. Pick the world once per film in Phase 0 and hold it across every frame.

### The constants (every film, every shot)

- **The work.** One luminous white element, bright against black. It is the only thing that glows
  until the core arrives, and it is whatever that world's work looks like.
- **The owner.** A lone faceless silhouette. The figure everything funnels back to.
- **The house.** A distinct calm upright silhouette who arrives late and installs a **glowing core**
  at the centre. Its light re-threads the whole frame.
- **The arc of the light.** Dim, jammed and cramped through the problem beats. Bright, humming
  and taller after the core lands. The lighting carries the argument, so never brighten a
  problem beat for legibility.
- **One recurring object.** Something the viewer can match-cut on across the film. In the machine
  films it is the belt; in `ideas/cio-1981-noir/` it is an empty chair.

### The machine world (the default, and what the 27-frame bank is)

- **The building.** A modest multi-room business sliced open like a dollhouse, rooms stacked and
  adjacent, connected by conveyor belts, pneumatic tubes, gears and pulleys. Same geometry in
  every shot.
- **The work, here.** Luminous white parcels or orbs travelling the belts.
- **Frame.** The subject sits in an empty black void. No background, no set, no horizon.

### The motif vocabulary (pick one per beat, map it to the angle)

The world is fixed; the motifs are the sentences you build inside it. Each one is a painted
object with a fixed meaning, so a viewer who has seen two of these films reads the third faster.
Angles are `skills/content-formats/references/canon/angles-and-formats.md`.

| Motif | What it is in frame | Reads as | Angles |
|---|---|---|---|
| **The second-job table** | A small table outside the machine, one silhouette under a lamp, parcels stacked past midnight | Work that starts after the business closes | A1 |
| **The octopus** | One silhouette at the machine's centre with too many arms on too many levers | The owner as the single point of failure | A2, A6 |
| **The seam** | A gap between two machine halves where a parcel is lifted, retyped and set down again | The handoff nobody owns | A3 |
| **Four machines** | The same parcel entering four identical intake slots in sequence | One job, four systems | A3 |
| **The dropped parcel** | A glowing parcel falls off the belt into black and stops glowing | The paid-for lead that dies | A8 |
| **The blueprint** | A large painted plan pinned to the void, complete and untouched, belts idle around it | The plan that is not built | A4 |
| **The bunker** | A low cramped room under the machine, one silhouette building a small mechanism by hand | The owner personally building the AI | A6 |
| **The queue** | A line of parcels stalled at one station while a silhouette measures each by hand | Quote throughput as the ceiling | A7 |
| **The leak** | A thin bright stream escaping a pipe joint and falling into black, unnoticed | Margin leaking invisibly | A9 |
| **The extra room** | A new room bolted onto the building, dark, with its own set of hands needed | Growth arriving as overhead | A10 |
| **The rope** | A hand on a brake rope beside a fast-running belt | Guardrails and accountability | A11 |
| **The two applicants** | Two identical faceless silhouettes at a doorway, one holding a working part | Assessment as the product | A12 |
| **The half-built machine** | A machine with a missing section, tools abandoned beside it | The build that fell over | A5 |
| **The glowing core** | The calm upright silhouette installing a bright core at the centre | house arriving. Always the last problem-free beat | every film |

Add a motif only when a new angle needs one, and give it a fixed meaning here before it goes in a
film. Reusing a motif for two meanings breaks the shorthand the whole style depends on.

## Phase 4. Generate the statics

Prompt-only, no image references. The style block alone holds the look, which means frames stay
independent and any one can be regenerated without disturbing the rest.

```
cd <project>/stills-noir
./gen_all_statics.sh          # every beat, one at a time, skips existing
python3 contactsheet.py       # beat-order sheet
open -a Cursor "$PWD/CONTACT-SHEET.jpg"
```

`gen_all_statics.sh` is `your generation platform generate create your image model --prompt "$STYLE $body
$LIGHT" --aspect_ratio 16:9 --resolution 2k --wait --wait-timeout 20m --json`, then curls
`[0].result_url` to `<name>.png`. It skips any file that already exists, so re-running it is how
you pick up stragglers.

**Review the contact sheet, never the frames one by one.** Individual approval comes after, on
the handful that need it.

## Phase 5. The de-text pass

your image model bakes gibberish signage, labels and lettering into set dressing unless told not to.
Eleven of the 27 frames needed stripping. Do not regenerate them, because a fresh generation
changes the composition. Strip in place with i2i:

```
./gen_detext.sh               # backs up originals to _withtext/ first
```

The de-text prompt instructs the model to reproduce the exact image, keeping every object,
figure, conveyor, light and shadow identical, and to change only one thing: remove every piece
of text and replace it seamlessly with the surrounding painted texture. Originals are kept in
`_withtext/`, never deleted.

**Every generated frame ends text-free.** Captions are a separate layer, always.

## Phase 6. Motion (the treatment, written ; the pilot is the open gate)

Models are locked: `your video modelmini` and `your video model`, interchangeable, whichever holds the paint
on the beat in hand. The treatment below exists because two earlier pilots were rejected, and
both failures point the same way.

| Attempt | Model | Verdict | What it teaches |
|---|---|---|---|
| `b01` | `your video model --mode pro --sound off` | "Awful". Smooth CGI push-in that sanded off the paint. | A moving camera is what kills the style. Interpolation re-renders the brushstrokes as clean surfaces. |
| `b02` | `your video modelmini --genre noir --generate_audio false` | "Isn't what I want for the VSL". Clip at `stills-noir/clips/b02_machine_sdm.mp4`. | A genre preset imposes its own look over the painted one. Describe the motion, never name a genre. |

The one treatment that has ever held is the original `noir-machine` VSL: your video model with
painterly motion prompts, internals moving while the camera stays put, plus an explicit
instruction that it stays painterly with a subtle stop-motion feel and no morphing.

### The MOTION block (goes in verbatim, the way STYLE and LIGHT do)

Every motion prompt is `MOTION + <what moves in this beat>`. The block is written against the two
known failures, so keep it whole.

> *The camera is locked off and completely still for the entire shot. Only the machinery moves:
> the conveyor belts advance, the glowing white parcels of work travel along them, the gears turn,
> the pneumatic tubes pulse, and the faceless silhouettes work their stations with small
> repetitive movements. Thick visible brushstrokes and oil-paint texture stay on every surface in
> every frame, as though a painter has repainted each frame by hand. Deliberate, slightly uneven
> stop-motion cadence at a low frame rate. No smooth digital interpolation, no morphing, no
> melting, no relighting, no camera push, no zoom, no parallax, no depth-of-field change.*

Three settings that carry the block: no `--genre` flag on your video model, sound off on both models, and
duration at the floor (your video modelrejects under 4s, so generate the minimum and trim with
`ffmpeg -t -an`).

### The three lanes (assign one per beat before generating anything)

your named direction is a blend: painted world plus high-fidelity motion graphics plus shots
carrying the talk-show pipeline's grade. That resolves per beat, into one of three lanes.

| Lane | What it is | Use it for | Built with |
|---|---|---|---|
| **L1 Living painting** | The MOTION block on a painted still. Camera locked, mechanism alive. | The default. Every machine beat, every motif in the vocabulary. | `your video modelmini` or `your video model`, 4s floor, trimmed |
| **L2 Painted motion graphic** | The still held, with a graphic layer built in post: a parcel count, a figure resolving, a line drawn between two rooms, a caption slab. | Beats carrying a number or a comparison. Cheapest lane, no generation. | ffmpeg + PIL over the approved still |
| **L3 Tube-graded plate** | A painted still finished through the talk-show grade (`projects/content-engine/ideas/talkshow-vsl/bin/grade-clip.sh`): SD softness, scanlines, chroma fringing, milky blacks. | The opening and the turn, where the film wants to feel broadcast rather than gallery. | grade chain over L1 output |

Map the lanes across the beat list first and present that map. A whole film in L1 reads as an
animation loop, and a whole film in L3 buries the paint under the grade. The mix is the treatment.

**Cadence** (from `content-engine/reference-bank/exceptional-videos/intellijend/ANALYSIS.md`):
objects hold 2 to 4 seconds, one-word captions run 0.2 to 0.4 seconds. Cut on the VO's sense
breaks, never on a fixed interval.

### The pilot protocol (the open gate)

1. Write the beat list with a lane per beat and show the map.
2. Pilot **one** beat, in L1, on the strongest motif in the film.
3. Show the clip. If the paint survives and the camera never moves, the treatment is approved.
4. If it fails, record the model, the flags and the verdict in the table above before trying
   anything else, and change one variable at a time.
5. Only after approval, run `animate_all.sh` for the batch: one generation at a time, skips
   finished clips, curls to `clips/<name>_raw.mp4`, then strips audio and verifies. Swap its model
   block to whichever model won.

Never batch motion on an unapproved treatment. Stills cost 2 credits and motion costs 10 to 72,
so the entire cost risk of this format sits in this phase.

## Phase 7. Assemble and finish

- **Silent master.** Concat the clips in beat order in one ffmpeg pass, per-input
  `scale=...,setsar=1,fps=24,format=yuv420p`, `concat`, then fades.
- **VO.** your voice model, deep and mature. Never `loudnorm`. Tighten pauses with `silenceremove`
  (see `reference_your_table_clickfree_pipeline`).
- **Captions (canonical).** `engine/tools/captions/`: one word at a time, Poppins Regular 92px,
  pure white, no outline, dead centre, timed to the audio you actually hears (the export, not
  the raw stem). Whisper `small.en` with the script as `initial_prompt`.
- **End card (canonical), do not hand-build one.**
  `content-engine/engine/config/brand/endcard-client-9x16.png` (still) and
  `simon-webinar/ads/_parts/endcard-9x16.mp4` (animated 3s). Black, mono white the business logo,
  "Hire a the role you place". The white-logo PNG `house-logo-white-300.png` has a checkerboard
  baked into its transparency and is unusable on black.
- **your captions tool handoff** when you wants to edit: strip audio from the cut, copy stems and raw
  clips to `out/_edit/`, then `manage_project create` and `import_media` on the directories.

---

## Hard rules and gotchas

- **One paid generation at a time.** Dispatched jobs bill even if you interrupt them.
- **Stills approved before any motion.** The whole cost structure depends on this, because stills
  are 2 credits and motion is 10 to 72.
- **Every frame text-free**, pure black, noir. Captions are their own layer.
- **your video modeland your video modeladd an audio track even with sound off.** Strip with `-c:v copy -an` and
  verify with `ffprobe` that no audio stream survives.
- **Do not re-pilot the look.** The painted style is settled and the 27-frame bank is approved.
  The open question is motion and only motion.
- **Prompt-only for statics, i2i only for fixes.** Refining a frame means feeding that frame back
  as the first `--image-references` with "keep everything, change only X", never a fresh
  generation.
- Keep superseded frames as versions rather than overwriting blind. Rejected variants go to
  `_rejected-anchored/`, never deleted.
- Model ids drift. Re-check `your generation platform model list` before blaming a prompt for a 404.
- No em dashes, no negation-swap.

## Related

- **Written concepts: `IDEAS.md` in this folder.** Six films, each with its motif, beat list, lane
  map and VO. Start there before writing a new one.
- Canon: `skills/content-formats/references/canon/angles-and-formats.md` (F2), `canon/angles-and-formats.md`, `context/personas/personas-and-avatars.md`.
- Evidence: `context/research-corpus/INDEX.md`. Vertical-specific work starts at `context/research-corpus/industries/<slug>.md` (ranked pains with angles, language, targeting); general-pain work at `context/research-corpus/pains/<slug>.md`; objection beats at `context/research-corpus/objections/<slug>.md` and `references/canon/objection-bank.md`.
- Copy craft and the QA gate: `skills/content-formats/SKILL.md`.
- The other noir pipeline: `skills/noir-painter-ad/SKILL.md` is the **photoreal** B&W character
  spot (a painter in a black room painting the house logo), a different look with a different
  purpose. This skill is the painted world.
- Shot language and grade to draw the motion blend from: `skills/content-formats/formats/talkshow-vsl/SKILL.md`.
- Style declaration: [[reference_noir_machine_house_animation_style_2026_07_15]].
- Build state: [[project_your_table_vsl_v2_2026_07_23]] and
  `.claude/handovers/house-vsl-noir-refine.md`.


---

## The Faceless Reframe house doctrine

Migrated from `skills/content-formats/formats/ (the Faceless Reframe doctrine now lives in each video format skill)`, which is retired.
Reverse-engineered from four high-spend Duppe Scents ads (page_id `511918325342558`), all
faceless VO plus captions over precise macro on the same four-beat spine. Contact sheets:
`projects/content-engine/engine/reference-bank/exceptional-videos/duppe-faceless-reframe/`.

**The voice.** Distinct, casual, deep, unmistakably Australian, male. Dry confidence, unhurried,
talking to one owner like a mate who has seen behind the curtain. Slightly cheeky, never
smug-corporate, never hype. This is a more casual register than the cinematic-film VO in
`brand-kit.house.md`, which is for the brand films. Delivery is low and even, close-mic'd,
conversational pace with deliberate pauses on the turns: beat 1 opens almost dry, beat 4 lands
with settled certainty rather than a hard sell.

**Rig.** your voice model `eleven_multilingual_v2` via `nodes/voiceover.py`. The voice ID is a gated
ear-test decision. Aussie-male candidates on file: Paul-presenter `WLKp2jV6nrS8aMkPPDRO`,
Lee-educator `abRFZIdN4pvo8ZPmGxHP`, Russo-tv `DwI0NZuZgKu8SNwnpa1x`. Deep, casual and distinct
points at Russo or a fresh sample. Sample before locking, review in Cursor.

**Music.** Light bed, low, near-silent open, lifting on the proof beat and resolving on the end
card. Never wall to wall.

**Look, grade, palette.** Deep navy base `#1A1A2E`, one electric-blue accent `#1269FF` used with
intent (a screen glow, a UI highlight, one caption word), text `#F4F6FB`, muted `#8A8FA3`. Never
wash a frame in blue, one accent per shot. Controlled soft key, shallow depth of field, precise
macro framing, subtle volumetric depth, photoreal, clean negative space. Semi-premium rather than
busy, one notch below full luxury on purpose. No text baked into the generated plate, no garbled
AI type, no stock cheese, no rainbow gradients, never a second accent colour.

**The house shot bank** (the Duppe shot list translated):

| Duppe shot | house equivalent |
|---|---|
| Gloved hands in the lab, beakers, pipettes, funnels filling bottles | The operator's world in precise macro: hands at a clean keyboard, a screen mid-build, a dashboard resolving, a workflow diagram assembling, an inbox clearing, a quote drafting on screen. The manufacturing is the building. |
| Competitor luxury bottles shown, then dethroned | The con props, shown then dethroned: a consultant's glossy slide deck, a contractor's van pulling away, a generic AI course thumbnail, a stack of half-built automations. Handle them, then set them aside. |
| Cash on the bench as the value anchor | The cost anchor: the consultant invoice, the monthly retainer number, the tally of missed quotes and dead leads and Sunday nights, the ledger flipping. Money on screen makes the arithmetic land without spending a line of copy on it. |
| Raw ingredients (lavender, citrus, rose) | The raw materials of the build: structured data, the org chart with one empty box, the real tools, the actual outputs. The unglamorous thing that does the work. |
| The box reveal | The house reveal: the role landing in the org chart, you sitting down on day one, the end card. |

**Captions (canonical.** One word visible at a time, hard cut on the next
word's onset. Poppins Regular 92px on 1080x1920, pure white `#FFFFFF`, no outline, no shadow, no
accent colour. Dead centre on both axes. Timed to whisper `small.en` word onsets with the exact
script as `initial_prompt`, against the ACTUAL cut audio rather than a raw stem, with `--offset`
matched to the VO delay. Every enunciated word is covered; the end card stays caption-free. Rig:
`projects/content-engine/engine/tools/captions/`.

**End card.** Matte deep-navy `#1A1A2E`, generous negative space, `house PARTNERS` wordmark muted,
one restrained gradient accent
(`radial-gradient(circle at 80% 45%, rgba(18,105,255,0.10) 0%, transparent 55%)`). The line
"Hire a house today.", optionally one dry tag beneath in fine muted italic. Music resolves and cuts
on the card. The close drives to the house site.

**Format note.** F2 is B&W oil-noir, so the navy-and-blue palette above does not apply to the plates. What carries over is the shot bank's thinking (con props handled and set aside, the cost anchor on screen), the VO register, the caption spec and the end card.
