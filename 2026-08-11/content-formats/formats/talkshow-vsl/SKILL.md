---
name: talkshow-vsl
description: Use when the operator says "talk show ad", "old time TV guru", "vintage TV video", "1970s talk show", "guru clip", "talkshow VSL", or wants a house video built in the retro talk-show style. A distinguished older Australian guest on a 1970s TV set delivers one weighty business truth to an unseen host, run through a heavy analog-tape grade, finished with one-word captions, a persistent top hook and the house end card. Two modes, a 20-40s guru clip and a 45-90s full VSL. Format F1 in angles-and-formats.md.
canonical: true
format: F1
---

# Old-Time TV Guru (the 1970s talk-show pipeline)

A distinguished older Australian guest, seated on a 1970s TV talk-show set, delivers a monologue
**to an unseen host** while really speaking to the Australian business owner watching. The whole
thing runs through a heavy analog-tape grade, then gets kinetic captions, a persistent top hook
and the canonical house end card.

First built 2026-07-23 (the "most important hire of the century" spot, modelling the @aipbi
"He is AI" reels). The authority of the format does the persuading, so the guest never sells,
he observes.

**What it produces:** a set of ~8s on-camera Seedance clips (one per script beat, native
lip-synced Australian voice), assembled into an editable Palmier Pro project, graded to the
VHS/tube look, with a high-pass "TV speaker" audio degrade, one-word captions, a persistent top
hook, and the end card. Delivered 9:16 vertical (footage as a centred sliver on black, @aipbi
layout) or 16:9 landscape.

**When to pick this format:** contrarian reframes and authority takes. Pains where an
elder-statesman "the adults have arrived" voice lands hardest: failed DIY (A5), vendor trust
(A11), the owner in the bunker (A6), the execution gap (A4). The authority of the format does the
persuading, so this is the wrong home for a naked callout ad.

---

## Production spec (the worker and Claude Code both execute this)

```yaml
format: F1
skill: talkshow-vsl
modes: [guru-clip, full-vsl]
aspect: "9:16"                 # 16:9 available, vertical is the default
models:
  still: nano_banana_pro       # 16:9 plates, ~2 credits each
  motion: seedance_2_0         # native Australian voice, ~72 credits per 8s at 1080p
  motion_fallback: elevenlabs VO + seedance lip-sync
  routing: ../../references/canon/model-routing.md   # house shot-type table; the set above wins here
inputs:
  persona: personas-and-avatars id, or "general"
  angle: angles-and-formats.md A1-A12
  offer: house | ai-officer | ai-orchestrator
  thesis: the one weighty truth, landing on house in the final line
  hook_line: persistent positive statement shown above the footage
layout:
  captions: dead-centre one-word Poppins, a named exception to the bottom-band law
  type_cards: any title, hook or quote card set as type on black follows the bottom-band law
              (content-formats section 1, engine at skills/content-formats/formats/static-ads/scripts/band.py)
  top_hook: persistent, top of frame, the other named exception
steps:
  - phase 0 lock the brief -> VSL.md            # GATE
  - phase 2 write vo/lines.txt                  # GATE, review in Cursor
  - phase 3 stills, nano_banana_pro             # GATE, approve each in Cursor
  - phase 4 motion, one paid job at a time      # never batched
  - phase 5 assemble (compile_aipbi.py or Palmier)
  - phase 6 grade, audio degrade, captions, top hook, end card
qa:
  - em dash scan, negation-swap scan, banned vocabulary
  - ffprobe every clip meant to be silent for a surviving audio stream
  - captions timed against the export the operator hears, never the raw stem
cost_shape: 1 anchor still + 1-2 motion generations per clip (mid)
ideas: skills/content-formats/formats/talkshow-vsl/IDEAS.md            # 12 written guru-clip concepts
```

---

## Two modes

Pick before Phase 0. They share every phase; the clip mode just runs fewer of them.

| | **Guru clip** | **Full VSL** |
|---|---|---|
| Runtime | 20 to 40s | 45 to 90s |
| Script | 5 to 8 lines, one truth | 15 to 18 lines, full arc |
| Stills | 1 hero close-medium | guest, host, close-medium, two-shot, entrance |
| Clips | 2 to 4 Seedance | 6 to 9 Seedance plus B-roll |
| Structure | cold open on the guest mid-thought, one turn, name house on the last line | the canonical style in Phase 2: forked hook, the turn, three AI systems taught, the bridge, the quiz close |
| Shot plan | one hero close-medium held throughout | intro two-shot, cut to close-medium, reaction beats, CTA |
| Assembly | `compile_aipbi.py` straight to a compile | Palmier project for the operator to edit |
| Spend | roughly 150 to 300 credits | roughly 500 to 700 credits |

The clip mode is the volume format, so batch its scripts against different pains and reuse one
approved hero still across all of them. The VSL is the flagship and gets the full gate stack.

**Working dir convention:** one project folder under
`the business/projects/content-engine/ideas/<slug>/`. Copy `ideas/talkshow-vsl/bin/` as the
starting toolkit (every script below resolves the project dir from its own location). Sub-dirs:
`gen/` (stills, motion prompts), `vo/` (voice), `clips/` (rendered plus `clips/graded/`), `ref/`
(grade reference), `out/` (compiles). The 2026-07-23 build lives at `ideas/talkshow-vsl/`.

---

## Phase 0. Lock the brief (ask, do not assume)

Use AskUserQuestion, batch 4 at a time. Lock BEFORE any paid generation:

- **Mode.** Guru clip or full VSL.
- **Concept before brief.** Persona x angle x offer, in that order, format last. Persona from
  `context/personas/personas-and-avatars.md` (general-pain default, callouts only from the approved
  list). Angle from `canon/angles-and-formats.md` (A1-A12). Offer: house flagship, AI Officer, or AI
  Orchestrator. `IDEAS.md` in this folder holds 12 concepts already built this way.
- **Thesis and CTA.** One weighty business truth that lands on house. The 2026-07-23 spine: the
  one thing that decides every business is who it hires, every era has its defining hire, the
  the role you place is the most important hire of the century. Named on the last line.
- **Avatar.** Who the guest is really talking to. Broad owner by default, or a named vertical
  from the approved callout list (construction is the franchise).
- **Format and runtime.** 9:16 vertical @aipbi layout (default) or 16:9.
- **Guest and host look.** Distinguished older authority (default), everyman operator, or styled
  on a real house figure.
- **Top hook line.** Short positive statement shown above the footage (Phase 6). Never a
  negation-swap.
- **References.** Default model is the @aipbi reels in
  `projects/content-engine/engine/reference-bank/reels/` (owner "AI-Powered Business
  Intelligence"): footage as a band near the top on black, persistent hook above, kinetic
  captions, big black below.

Write the locked brief to `VSL.md` in the project folder. `ideas/talkshow-vsl/VSL.md` is the
template and also carries the era research (three-tube Plumbicon cameras, 2-inch Quadruplex
tape) that justifies the grade.

## Phase 1. Environment and tools (verify once)

- **Higgsfield CLI** at `/opt/homebrew/bin/higgsfield`, authed as `enquiries@yourdomain.example`
  (ultra plan). `higgsfield account status` for credits.
- **Model ids (verified 2026-07-25, these drift):** stills `nano_banana_pro`. Video
  `seedance_2_0` (native audio, the workhorse here), `seedance_2_0_mini` (720p max, no `--mode`),
  `kling3_0`, `veo3_1`. **`nano_banana_2` does not exist and 404s**; the id displayed as "Nano
  Banana 2" in the model list is `nano_banana_flash`, which is a different, weaker model. Run
  `higgsfield model list --image|--video` when anything 404s.
- **Cost (from the ledger):** Seedance 2.0 8s at 1080p is about 72 credits (~$2.40 to $3.10),
  Veo 3.1 8s high is 58, a Nano Banana still is 2. Ultra is 3,000 credits a month. Check
  `higgsfield account transactions` if a number looks off.
- **ffmpeg / ffprobe**, **PIL** (`/usr/bin/python3` has it, homebrew python3 does not),
  **ElevenLabs key** `ELEVENLABS_API_KEY` in `content-engine/engine/config/.env` (fallback voice
  path only).
- **Palmier Pro** running, driven by the MCP client `ideas/revolution-montage/bin/palmier_mcp.py`
  (`python3 <MCP> tools|schema <t>|call <t> <json>`).

## Phase 2. Write it (`vo/lines.txt` plus `VSL.md`)

Deep, measured, distinguished-authority register. Halbert roll, keep the conjunctions. No em
dashes, no negation-swap. Break the monologue into **short single lines**, one thought each, in
`vo/lines.txt`. That line is the unit of a clip and gives per-line control. Review in Cursor.

Craft and the QA gate live in `skills/content-formats/SKILL.md`. This register is its **Register 1
(cinematic)** shifted older and drier: the guest has seen four decades of businesses rise and
fall and is unimpressed by all of it.

**The line that carries a guru clip** is the second one. The first establishes he is worth
listening to, the second states the thing nobody says out loud, and everything after is
consequence.

### The canonical full-VSL style (locked 2026-08-01)

**Full VSL mode has one style and this is it.** The reference implementation is `IDEAS.md` V01,
"The weekend off". Write every VSL against it rather than composing a new arc, and read the arc
notes above V01 in that file plus `skills/content-formats/SKILL.md` 7c before starting.

1. **Fork one script, do not compose.** The source is
   `skills/content-formats/references/scripts/core-pain-vsl-scripts.md`, eighteen written P/S/VSL
   scripts, one per core pain. Take the one whose pain matches and keep its hook in its own
   words. Its hook is either the dream outcome as a question or the pain agitated.
2. **The turn, one line.** "Well, you can. You just need these three AI systems."
3. **Straight into the systems.** The source's machine walkthrough ("so here's your business, the
   work comes in here") is cut. The runtime belongs to the teaching.
4. **Three AI systems, each taught the same way.** A system name, then what it does, then the
   outcome opening on "For example". Order the beats in that sequence every time.
   - **Name the system, never the outcome.** "The auto report builder" is a name. "The job that
     runs itself" is the result, and spending it as the name kills the payoff.
   - **Owner's language, not the builder's.** Say what it plugs into and what it touches. The
     real stack (LangGraph, classifiers, OCR) stays in the concept metadata as the evidence
     trail and never reaches the script.
   - **Industry agnostic**, because these go to the whole market. A build that only pays off for
     one vertical gets dropped however good its number is.
   - **Every build is a published row in the Hub `builds` table**, picked for the size of its
     recorded time saving, with the tools taken from its own `replicate_steps`. Never the
     abstracted `stack` column, and never a build invented at the desk.
   - **The three outcomes must be distinct**, and each carries the scope its source supports.
5. **The bridge, one sentence.** All three are already running somewhere, and the gap widens
   every month it is left. Honest scarcity, no overclaim.
6. **The quiz close**, carried in on "so". The role is never named in this mode: the quiz result
   is what introduces the category.

Roughly 120 to 240 spoken words. The guru-clip mode keeps its own 55 to 110 word arc and the
ordinary 7e close.

## Phase 3. Stills (`nano_banana_pro`, 16:9)

Clean photoreal plates. The tape grade goes on later and is never prompt-baked. Prompts are
detailed positive prose, camera-distance-led. Render with
`bin/render.sh <slug> <prompt-file> [image-refs...]` (set `ASPECT=16:9`).

1. **Guest** reference (`prompt-guest.txt`), then **host** reference. Distinct people, same set.
2. **Close-medium guest** (the hero delivery frame), and for VSL mode also the **intro two-shot**
   and the **entrance / handshake**, each generated with the approved guest and host plates as
   `--image-references` so the faces hold.
3. Approve every still in Cursor before motion. Hard gate. Keep negative space on the side the
   guest faces for captions.
4. **Ask for no on-image text.** Nano Banana bakes gibberish signage into set dressing unless
   told not to. Strip any that slips through with an i2i pass rather than regenerating.

The set and look: 1970s wood-panelled talk-show studio, tan-leather armchairs, burnt-orange
palette, a fern. Distinguished older guest in a brown wide-lapel suit and burnt-orange knitted
tie. Mid-50s host in tan corduroy, blue shirt, cue cards.

## Phase 4. Motion (Seedance 2.0, native voice)

**The voice persists across clips** when you use an identical voice and performance block and the
same close-medium start frame every time. Render one beat-chunk (2 to 3 lines, about 8s) per clip
with `bin/seedance.sh <slug> <motion-prompt> gen/<guest-cu>.png 8 native`. **One paid generation
at a time**, wait for each before the next.

Put the dialogue in double quotes in the prompt. The locked voice and performance block, verbatim
in every delivery prompt (see `bin/motion-native-4.txt`):

> *He speaks in a deep, resonant, unmistakably Australian voice with a broad Australian accent,
> the formal authoritative cadence of a 1970s Australian television news presenter. He enunciates
> smoothly and fluidly, the sentences flowing as one connected articulate thought that rolls off
> the tongue, unhurried and even, never clipped or staccato. Naturalistic performance: his eyes
> drift thoughtfully around the room and glance upward at a couple of moments as he chooses his
> words, he adjusts his suit jacket slightly, and he gesticulates with one hand to emphasise his
> points, lifting his inflection at the key words, with natural lifelike micro-movements
> throughout.*

Without the smooth-plus-movement block the read comes out staccato and stiff, which was rejected
on the first pass. Default native output is American, so the Australian spec has to be heavy.
Entrance and reaction B-roll use the same helper with `native` dropped, or a silent start frame.

**Charge-safety (hard, learned the hard way):** `bin/seedance.sh` and `bin/veo.sh` create the job
exactly once, never retry, then wait by job id, so a dropped connection re-polls the same job
instead of paying again. A parser bug once re-created a job three times and triple-charged. If a
create returns no parseable id, do not re-run: recover with `higgsfield generate list` and
`higgsfield generate wait <id>`.

**Fallback voice path (only if native will not hold):** ElevenLabs per-line VO
(`bin/make_lines.py` reads `vo/lines.txt`, `VOICE_ID` env) then Seedance lip-sync
(`bin/seedance.sh <slug> <prompt> <plate> <dur> <vo.mp3>`). Identical voice guaranteed, more
setup.

## Phase 5. Assemble

- **Palmier project (editable handoff, VSL mode):** `python3 bin/make_palmier.py` builds
  `~/Documents/Palmier Pro/<name>.palmier` with every clip on V1 in order, audio baked in. Add
  `GRADED=1` to point at `clips/graded/`. Creating a NEW project is safe while Palmier runs.
  Never hand-write project.json for a project that is already open, it clobbers. To edit a live
  project use the MCP: `add_clips` / `insert_clips` (omit `trackIndex` to auto-create the track),
  `apply_color`, `apply_effect`.
- **@aipbi vertical compile (self-contained, both modes):** `python3 bin/compile_aipbi.py` trims
  each clip's leading and trailing dead air (keeps internal pauses, silencedetect at -30dB, run
  ffmpeg at `-v info` because `-v error` hides the detector), stacks them, drops the footage as a
  band near the top of a 1080x1920 black canvas, and overlays a persistent hook PNG. Edit `HOOK`
  and `VID_TOP` at the top of the script.

## Phase 6. Finish (the canonical layer)

- **VHS / tube grade.** `bin/grade-clip.sh <in> <out>` per clip (hardware-encoded, about 8s
  each): SD-softness downscale, oversaturated warm eq, chroma-registration fringing (rgbashift),
  highlight bloom, scanline overlay (`bin/scanlines.png`), barrel CRT lens distortion, vignette,
  grain, milky blacks. The reference grade is the CRM "Fake-News Ad" (90s VHS newscaster), pulled
  from `content_items` into `ref/`. Still-only heavy version: `bin/vhs-grade.sh`. Palmier-native
  non-baked version: `bin/palmier_degrade.py` (warm grade, grain, warm halation glow, vignette,
  softness; Palmier has no scanline or chroma-bleed effect so it approximates).
- **Audio degrade (1970s TV speaker).** `bin/vo-degrade.sh` band-limits to about 300 to 3400 Hz,
  compresses, bit-crushes, folds to mono and adds faint hiss. Palmier's MCP has no audio EQ, so
  apply this to the FINAL EXPORT in one pass, which keeps sync perfect and touches nothing in the
  project: `ffmpeg -i export.mp4 -c:v copy -af "<degrade chain>" out.mp4`. Heavier means a
  tighter band (320 to 3050), lower acrusher bits (8 to 9), more hiss.
- **Captions (canonical rig).** `engine/tools/captions/`: one word at a time, Poppins Regular
  92px, pure white, dead centre, timed to the actual voice. `whisper_words.py <vo> <script>
  <words.json>` then `burn_captions.py <base> <words.json> <out> [--offset]`. Align to the audio
  the operator actually hears (the export), never the raw stem. The end card stays caption-free.
  Governed by `skills/content-formats/formats/ (the Faceless Reframe doctrine now lives in each video format skill)` §6.
- **Top hook.** Persistent positive statement above the footage, @aipbi style, white with one
  accent word. Never a negation-swap.
- **End card (canonical).**
  `projects/content-engine/engine/config/brand/endcard-client-9x16.png` (black, the business
  mark, "Hire a the role you place"). Place it at the end for about 3s, caption-free. Music
  resolves and cuts on the card.

---

## Hard rules and gotchas

- One paid generation at a time, never batched. Dispatched jobs bill even if you interrupt.
- Stills approved in Cursor before any motion.
- Charge-safe helpers only (create once, wait by id). Recover, never re-create.
- **Seedance and Kling add an audio track even when you ask for silence.** For any clip that is
  meant to be silent, strip it (`ffmpeg -i raw -c:v copy -an out.mp4`) and verify with `ffprobe`
  that no audio stream survives.
- Model ids drift. Re-check `higgsfield model list` before blaming a prompt for a 404.
- No em dashes, no negation-swap, banned-word clean.
- Deliver clips by `open`ing the local mp4 (inline render is unreliable for the operator). Reveal
  folders in Finder for audio.
- Higgsfield-only for house. Snapshot to `_versions/` before regenerating a named asset.

## Rig (copy `ideas/talkshow-vsl/bin/`)

`render.sh` · `seedance.sh` · `veo.sh` (motion) · `vhs-grade.sh` · `grade-clip.sh` plus
`scanlines.png` (video grade) · `vo-degrade.sh` (audio degrade) ·
`make_vo.py` / `make_lines.py` / `make_line.py` (ElevenLabs fallback voice) · `make_palmier.py` ·
`compile_aipbi.py` / `compile-vertical.sh` (compiles) · `palmier_degrade.py` (live-Palmier
degrade, project-specific media ids, adapt before use) · `motion-native-4.txt` and `prompt-*.txt`
(prompt templates).

## Related

- **Written concepts: `IDEAS.md` in this folder.** 12 guru clips, each with its persona, angle,
  offer, hook line and full line-by-line script. Start there before writing a new one.
- Canon: `skills/content-formats/references/canon/angles-and-formats.md` (F1), `canon/angles-and-formats.md`, `context/personas/personas-and-avatars.md`.
- Evidence: `context/pain-wiki/INDEX.md`. Vertical-specific work starts at `context/pain-wiki/industries/<slug>.md` (ranked pains with angles, language, targeting); general-pain work at `context/pain-wiki/pains/<slug>.md`; objection beats at `context/pain-wiki/objections/<slug>.md` and `references/canon/objection-bank.md`.
- Copy craft and the QA gate: `skills/content-formats/SKILL.md`.
- Sibling video pipelines: `skills/content-formats/formats/noir-painterly/SKILL.md` (the house animation style),
  `skills/stitch-hook/SKILL.md` (borrowed viral clip into a house body).
- Full project state: [[project_your_table_vsl_2026_07_23]].
- This pipeline's shot language and grade are the reference the VSL v2 noir refine draws from
  (`.claude/handovers/house-vsl-noir-refine.md`).


---

## The Faceless Reframe house doctrine

Migrated 2026-07-31 from `skills/content-formats/formats/ (the Faceless Reframe doctrine now lives in each video format skill)`, which is retired.
Reverse-engineered from four high-spend Duppe Scents ads (page_id `511918325342558`), all
faceless VO plus captions over precise macro on the same four-beat spine. Contact sheets:
`projects/content-engine/engine/reference-bank/exceptional-videos/duppe-faceless-reframe/`.

**The voice.** Distinct, casual, deep, unmistakably Australian, male. Dry confidence, unhurried,
talking to one owner like a mate who has seen behind the curtain. Slightly cheeky, never
smug-corporate, never hype. This is a more casual register than the cinematic-film VO in
`brand-kit.house.md`, which is for the brand films. Delivery is low and even, close-mic'd,
conversational pace with deliberate pauses on the turns: beat 1 opens almost dry, beat 4 lands
with settled certainty rather than a hard sell.

**Rig.** ElevenLabs `eleven_multilingual_v2` via `nodes/voiceover.py`. The voice ID is a gated
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
| The box reveal | The house reveal: the role landing in the org chart, the operator sitting down on day one, the end card. |

**Captions (canonical, locked 2026-07-16).** One word visible at a time, hard cut on the next
word's onset. Poppins Regular 92px on 1080x1920, pure white `#FFFFFF`, no outline, no shadow, no
accent colour. Dead centre on both axes. Timed to whisper `small.en` word onsets with the exact
script as `initial_prompt`, against the ACTUAL cut audio rather than a raw stem, with `--offset`
matched to the VO delay. Every enunciated word is covered; the end card stays caption-free. Rig:
`projects/content-engine/engine/tools/captions/`.

**End card.** Matte deep-navy `#1A1A2E`, generous negative space, `house PARTNERS` wordmark muted,
one restrained gradient accent
(`radial-gradient(circle at 80% 45%, rgba(18,105,255,0.10) 0%, transparent 55%)`). The line
"Hire a house today.", optionally one dry tag beneath in fine muted italic. Music resolves and cuts
on the card. The close drives to the house site (locked 2026-07-08).

**Format note.** F1 carries native on-camera Australian voice via Seedance, so the ElevenLabs rig above is the fallback path rather than the default. The VHS/tube grade and the persistent top hook override the palette and caption placement written here.
