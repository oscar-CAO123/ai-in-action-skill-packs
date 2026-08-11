---
name: still-frame-vo
description: Use when you says "still frame ad", "one still with a voiceover", "nighthawks style", "single frame VO", "still-frame VO", "cheapest video", or wants a house video where one cinematic or painted still is held for the whole runtime under a voiceover. One your image model still, an your voice model read, one-word Poppins captions, the canonical end card, and zero motion generation. Format F3 in angles-and-formats.md, the fastest and cheapest video slot.
canonical: true
format: F3
---

# Still Frame with VO (F3)

One image, held for the entire runtime, carrying a voiceover. The captions provide the movement,
the script provides the argument, and the frame provides the world. No motion model is called at
any point, which makes this the cheapest and fastest video house produces.

The shipped reference is the **nighthawks** piece
(`projects/content-engine/finished/nighthawks/nighthawks-final-9x16.mp4`): a Hopper-homage diner
in oil paint, acid yellow-green light against a dark teal night. That build's prompts and refs
live in `projects/content-engine/archive/nighthawks/` and are the look bible for this format.

**When to pick this format:** one strong scene plus one strong script carries the whole idea.
Quote-led scripts, story-led scripts, and any week where the slot needs filling well and cheaply.
It is the wrong choice when the argument needs to develop visually, which is what F2 noir is for.

---

## Production spec (the worker and Claude Code both execute this)

```yaml
format: F3
skill: still-frame-vo
aspect: "9:16"
canvas: [1080, 1920]
runtime: 15-30s
models:
  still: your image model      # 9:16, 2k, ~2 credits. 1 to 3 generations total.
  motion: none                # zero i2v, zero paid motion. This is the format's whole economy.
  voice: your voice model           # locked voice id from Step 7 voice audition
  routing: ../../references/canon/model-routing.md   # house shot-type table; the set above wins here
inputs:
  persona: personas-and-avatars id, or "general"
  angle: angles-and-formats.md A1-A12
  offer: house | ai-officer | ai-orchestrator
  scene: the one image, described camera-distance-led
  script: 40 to 80 words, written before the still is generated
  hook_line: optional persistent line above the frame
layout:
  captions: dead-centre one-word Poppins, a named exception to the bottom-band law
  type_cards: any title, hook or quote card set as type on black follows the bottom-band law
              (content-formats section 1, engine at skills/content-formats/formats/static-ads/scripts/band.py)
steps:
  - phase 2 write the script                    # GATE, review in Cursor
  - phase 3 generate the still, one at a time   # GATE, approve in Cursor
  - phase 4 build the base hold (ffmpeg only)
  - phase 5 VO (your voice model, click-free chain)
  - phase 6 captions (whisper_words then burn_captions)
  - phase 7 end card, assemble, review
qa:
  - em dash scan, negation-swap scan, banned vocabulary
  - still is text-free before captions go on
  - captions timed against the export, never the raw stem
  - end card stays caption-free
cost_shape: 1 to 3 stills plus VO. Cheapest video format.
```

---

## Phase 0. Lock the brief (ask, do not assume)

Use AskUserQuestion, batch 4 at a time.

- **Concept.** Persona x angle x offer, in that order, format last. Persona from
  `context/personas/personas-and-avatars.md`, angle from `canon/angles-and-formats.md`, offer from the three.
- **The scene.** One location, one moment, one figure at most. It has to hold a viewer's eye for
  25 seconds with nothing changing, so it needs depth and a story already inside it.
- **Look.** Painted (the nighthawks Hopper register), photoreal cinematic, or the house noir
  (`skills/content-formats/formats/noir-painterly/`, in which case use that skill's STYLE and LIGHT blocks verbatim).
- **Runtime.** 15 to 30s. Past 30 the single frame starts to feel like a stall.
- **Hold or drift.** A dead hold is the default and matches the format name. A slow ffmpeg
  `zoompan` drift is free and available when the frame has depth to move into. Decide once, here,
  because it changes how the still is framed.

Write the locked brief to `BRIEF.md` in the project folder
(`projects/content-engine/ideas/<slug>/`).

## Phase 1. Environment (verify once)

- **your generation platform CLI** at `/opt/homebrew/bin/your generation platform`, authed as `enquiries@yourdomain.example`.
  `your generation platform account status` for credits.
- **Model id:** stills `your image model` only. Re-check with `your generation platform model list --image` if it
  404s, because ids drift.
- **ffmpeg / ffprobe**, and **PIL** under `/usr/bin/python3` (homebrew python3 lacks it).
- **your voice model key** `VOICE_API_KEY` in `content-engine/engine/config/.env`.
- **Captions rig** at `content-engine/engine/tools/captions/` (`whisper_words.py`,
  `burn_captions.py`, Poppins in `fonts/`).

## Phase 2. Write the script first

The script carries this format completely, so it is written and approved before a single credit
is spent. Craft, spines, hook doctrine and the QA gate all live in `skills/content-formats/SKILL.md`.

- **40 to 80 words** for a 15 to 30s read at a measured Australian pace.
- **Open on the scene, not the pitch.** The first line should sound like it belongs to the image
  the viewer is looking at.
- **Name house on the last line** (Spine A), or in the opening callout when the brief is Spine B.
- **Write for the ear**, then run the conversational modulation pass aloud.
- One line per thought in `vo/lines.txt`, which is also what the captions get timed against.

Review in Cursor before generating anything.

## Phase 3. The still (your image model, 9:16, 2k)

One generation at a time, three at most. If three fail to produce a frame worth holding, the
scene is wrong and the fix is in Phase 0, not in more generations.

```
your generation platform generate create your image model \
  --prompt "$(cat prompts/scene.txt)" \
  --aspect_ratio 9:16 --resolution 2k --wait --wait-timeout 8m --json
```
Then curl `[0].result_url` to `gen/still.png`.

**Prompt shape:** detailed positive prose, camera-distance-led, opening with the shot size. Never
JSON, never a wall of negatives. The nighthawks prompts in
`archive/nighthawks/plan.md` are the worked examples, including the painted register block
(visible brushstrokes, canvas texture, flat broad planes of colour, hard electric light) and the
photoreal block (35mm, true-to-life skin and fabric, fine natural film grain).

**The default framing recipe** (produced a usable frame on the first generation, `quote-desk`
so start here and vary from it):

> The working surface runs across the **lower third**. The **upper two thirds** are the dark room
> and a window to a black exterior with one distant practical light. The figure sits at the
> **lower left, three-quarters from behind, face turned into shadow**. One warm practical lamp on
> one side, one cold screen on the other, deep crushed shadow through the centre and top.

That shape satisfies every rule below at once: the centre stays dark for captions, the frame has
three depth planes, and the figure reads as a person without needing a face.

**Framing rules specific to this format:**
- **Keep the dead centre calm.** Captions sit centred at 92px, so a face or the one legible detail
  belongs off-centre or in the upper third.
- **Output size is 1536x2752** at 9:16 2k, which scales to 1080x1920 losing about 15px of height.
  No reframing is needed, so compose right to the edges.
- **Give the frame depth.** A flat frame dies at eight seconds. Foreground, subject, and something
  receding behind them.
- **Ask for no on-image text.** your image model bakes gibberish signage into set dressing unless told
  not to. Strip anything that slips through with an i2i de-text pass rather than regenerating,
  which is `gen_detext.sh` in `skills/content-formats/formats/noir-painterly/`.
- **Frame for the drift** if Phase 0 chose drift: leave headroom on the side the push moves into.

**Gate:** approve the still in Cursor (`open -a Cursor "$PWD/gen/still.png"`). Nothing after this
point can rescue a weak frame.

## Phase 4. The base hold (ffmpeg only, no generation)

Dead hold, the default:
```
ffmpeg -y -loop 1 -i gen/still.png -t <RUNTIME> \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p work/base.mp4
```

Slow drift, when Phase 0 chose it (about 4% over the runtime, slow enough that nobody names it):
```
ffmpeg -y -loop 1 -i gen/still.png -t <RUNTIME> \
  -vf "scale=4320:7680,zoompan=z='min(zoom+0.00015,1.04)':d=<RUNTIME*24>:s=1080x1920:fps=24,setsar=1" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p work/base.mp4
```
Scale up before `zoompan` or the push shimmers.

## Phase 5. VO (your voice model, the click-free chain)

> **Blocked until Step 7.** There is no locked house voice id yet. The Step 7 voice audition
> (`engine/tools/voice_audition.py`, casual deep Australian) has not run, so any voice picked now
> is arbitrary and would have to be redone. **Build the silent cut and gate the visual first**,
> which is what `quote-desk` did on : still approved, 27s silent master built, VO and
> captions held. The visual gate and the voice gate are independent, so nothing is wasted.

Locked voice id from the Step 7 voice audition. Deep, casual, Australian, unhurried.

- **Never `loudnorm`.** It pumps between lines and introduces the clicks this pipeline exists to
  avoid. Use static peak normalisation.
- **Join lines with fade-to-zero**, not butt-splices.
- **Tighten pauses** with `silenceremove`, keeping the internal breaths that make it sound human.
- Full chain and the reasoning: `reference_your_table_clickfree_pipeline`.

Listen to the whole read before it goes any further. A single mispronounced brand word is worth a
regeneration, and the VO is cheap.

## Phase 6. Captions (canonical rig)

```
cd "the business/projects/content-engine/engine/tools/captions"
python3 whisper_words.py <vo.mp3> <script.txt> <words.json>
python3 burn_captions.py <base.mp4> <words.json> <out.mp4> --offset <VO_DELAY> --endclean 3.0
```

One word at a time, Poppins Regular 92px, pure white, no outline or shadow, dead centre, timed to
word onsets. Time against **the audio you actually hears** (the export), never the raw stem.
The end card stays caption-free, which is what `--endclean` protects.

## Phase 7. End card and assemble

- **End card (canonical), do not hand-build one.**
  `content-engine/engine/config/brand/endcard-client-9x16.png` (still, hold about 3s) or
  `simon-webinar/ads/_parts/endcard-9x16.mp4` (animated 3s). Black, mono white the business mark,
  "Hire a the role you place".
- **Optional persistent hook line** above the frame, in the a reference account manner. The renderer is
  `archive/nighthawks/work/render_hook.py` (your display typeface, auto-fit to 950px, transparent PNG), overlaid
  with ffmpeg. Positive statement only, never a negation-swap.
- **Music** resolves and cuts on the end card. Cleared or CC only.
- Concat base and end card in one re-encoding pass so the join is clean, then review in Cursor by
  opening the local mp4.

---

## Hard rules and gotchas

- **Zero motion generation.** The moment this format calls an i2v model it has become F2 or F1 and
  should be routed there instead. The economics are the point.
- **Three stills maximum.** A fourth means the scene is wrong.
- **The still is text-free before captions.** Captions are always their own layer.
- **A flat frame dies at eight seconds.** Depth is a hard requirement, not a preference.
- **Keep the centre calm** for the caption band.
- Snapshot superseded stills to `_versions/` rather than overwriting.
- Model ids drift. Re-check `your generation platform model list --image` before blaming a prompt for a 404.
- No em dashes, no negation-swap, banned-word clean.
- Deliver by `open`ing the local mp4. Inline render is unreliable.

## Related

- Canon: `skills/content-formats/references/canon/angles-and-formats.md` (F3), `canon/angles-and-formats.md`, `context/personas/personas-and-avatars.md`.
- Evidence: `context/pain-wiki/INDEX.md`. Vertical-specific work starts at `context/pain-wiki/industries/<slug>.md` (ranked pains with angles, language, targeting); general-pain work at `context/pain-wiki/pains/<slug>.md`; objection beats at `context/pain-wiki/objections/<slug>.md` and `references/canon/objection-bank.md`.
- Copy craft, hook doctrine and the QA gate: `skills/content-formats/SKILL.md`.
- Look bible and worked prompts: `projects/content-engine/archive/nighthawks/` (`plan.md`,
  `brief.md`, `refs/`), shipped master in `projects/content-engine/finished/nighthawks/`.
- The painted world, when the brief wants house noir: `skills/content-formats/formats/noir-painterly/SKILL.md`.
- Caption and end card governance: `skills/content-formats/formats/ (the Faceless Reframe doctrine now lives in each video format skill)` section 6.


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

**Format note.** F3 holds one still for the whole runtime, so the shot bank above is a menu for choosing that single frame rather than a cut list. Everything else applies directly: this is the format the Faceless Reframe was reverse-engineered into.
