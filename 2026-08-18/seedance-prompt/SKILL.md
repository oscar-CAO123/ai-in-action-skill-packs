---
name: seedance-prompt
description: Use when you says "seedance prompt", "seedance 2.5", "write a seedance prompt", "structured video prompt", "turn this image into a video", "fly the camera through this reference", "shot-by-shot prompt", or has one or two reference images and wants a single unbroken photoreal take out of them. A layer, not a format: it bolts onto any format that turns stills into motion, and it runs the generation on Higgsfield.
canonical: true
layer: L-SEED
---

# L-SEED, a Seedance 2.5 prompting engine

**The engine's one principle: every clause in the prompt must name something you could
photograph.** A clause that survives being pasted into a prompt about a completely different
subject is a style word, it specifies nothing, and the model fills the gap it leaves with its own
average. The average is what "looks AI" means.

Seedance 2.5 will happily accept a one-line prompt and a reference image. What comes back is
plastic, and the reason is not the model. A one-liner leaves the light, the palette, the texture,
the wear, the take structure and the camera's route all unspecified, which is six invitations to
average. This engine closes all six with named physical fact, in seven tagged blocks.

**Subject-agnostic by construction.** The blocks never change. A person, a workshop, an office, a
vehicle, a plate of food, a job board, a server rack: what changes is which nouns fill the banks
below.

**Bolts onto** any format that generates motion from a still, the same slot `path-control` occupies.
They compose, and they answer different questions: `path-control` specifies **where the camera goes**, by
drawing the route on the plate. `L-SEED` specifies **the world it flies through**, in prose. On a
shot using both, `[MOTION]` shrinks to pace and reaction while the drawn line carries the geometry.

Provenance is in `reference-ophelia-decode.md`. Read it only to check our working. It is evidence,
it is not instruction, and nothing in it binds.

---

## Part 1. The seven blocks

Write them in this order and label them with these tags. The tags do real work: they stop the model
averaging a lighting instruction into a camera instruction.

| # | Block | Job |
|---|---|---|
| 1 | `[LOOK]` | the world's physics: production context, format and glass, light, palette, artefacts, focus, wear, delivery spec |
| 2 | `[REFERENCES]` | what each supplied image is authority over, and what it is not |
| 3 | `[SHOT]` | the take's integrity: one continuous take, no teleporting, an anchor that never leaves frame |
| 4 | `[MOTION]` | three to five beats, each carrying a camera verb and a subject verb |
| 5 | `[AUDIO]` | omitted by default. Present only when a format has opted into sound |
| 6 | `[NEGATIVE]` | three to six failures this specific subject invites |
| 7 | `[END]` | the frame the take lands on |

---

## Part 2. `[LOOK]`, ten laws

Ten clauses, in this order. Each closes one gap.

### L1. Name a production context, never a style word
The model has seen real production. It has not seen "cinematic", "high quality" or "8k".

Pattern: **`<a real filmmaking discipline> for a real <kind of business>`**.

Bank: observational documentary for a real trade business · commercial cinematography for a real
campaign · a product film for a real manufacturer · an interior film for a real workplace ·
reportage stills brought into motion.

### L2. Name the format and the glass
Two facts. The glass choice sets the whole geometry, so pick it before anything else.

| Subject scale | Format and glass |
|---|---|
| Inside a small mechanism, a hand, a fitting | 35mm, macro probe lens |
| A desk, a bench, a person at arm's length | 35mm, 28mm close-focus |
| A room, a workshop, a site | 35mm, 24mm |
| A product on a surface, held still | large format, 80mm |
| Handheld, human scale, moving with someone | 16mm, 50mm |

### L3. State the take structure inside the look
"single continuous take, camera flying at all times". It gets restated in `[SHOT]`. The repetition
is deliberate and it is load-bearing.

### L4. Two light sources maximum, each with a quality and a position, then the space between, then the fill decision
Four moves in one sentence. Three sources is where a prompt starts producing mush.

- **Quality bank:** hard · soft · cold · warm · raking · bounced · diffused · stuttering · flat.
- **Position bank:** from above · from a window off frame · from a screen below · through a
  roller-door gap · from a doorway behind camera · through blinds off frame · from a single
  overhead tube.
- **The space between** gets its own clause: "deep shadow between", "a long falloff across the
  bench", "the middle of the room going to black".
- **The fill decision is stated**, not implied. "no fill" is the strong default.

### L5. Palette is five entries, each an adjective plus a material
Never a list of colours. "Blue and yellow" buys nothing; "oxidised brass fittings" buys a shot.

Pattern: **`Palette of <adj+material>, <adj+material>, <adj+material>, <adj+material>, <adj+material>.`**

On your work, see Part 4: the five carry the brand palette and at most one accent.

### L6. Attach every artefact to a named surface
Three artefacts, each anchored:

- **Grain**: fine, or coarse. On its own.
- **Halation**: on named edges. "gentle halation on the chrome hook and the tube ends".
- **Particulate**: suspended in named light. "dust suspended in the doorway light".

Floating artefacts ("filmic", "atmospheric") specify nothing.

### L7. Describe focus as a human operation
"Shallow depth with focus pulled continuously by hand." A hand pulling focus is the single
strongest anti-render clause available, because it implies an operator, a rig and a mistake budget.

### L8. Four objects, four specific residues
Pattern: **`Every surface has real wear: <object+residue> x4.`**

Residue bank: grease · dust · lint · scuffs · ring marks · chips · oxidation · biro dents ·
offcuts · fingerprints · sun-bleach · heat discolouration · tape residue · worn nap.

"Used and worn" is worth nothing. "A coffee ring on the top job card" is worth the shot.

### L9. Two flat absolutes
"Nothing looks rendered. Nothing looks like stock." Short, absolute, no hedging, no third sentence.

### L10. Delivery spec last
"9:16 vertical, 24fps." your brand's primary master is 1080x1920 at 9:16.

**The test for the whole block:** read each clause and ask whether it would still be true of a
completely different subject. If yes, delete it and write the specific thing.

---

## Part 3. `[REFERENCES]`, six laws

The block that decides whether the take flies or collapses back into the still.

### R1. Address each image by an index token
`#Image1`, `#Image2`, in the order they are passed to the CLI.

### R2. Declare the image's role, using the word "locked"
"#Image1 is the locked bench, colour and materials". The word does work: it tells the model this is
authority rather than suggestion.

### R3. Restate the image's contents in words
Never assume the model reads the image the way you do. **The words are the contract; the image is
the texture.** One clause naming what is in it, in the same vocabulary the palette uses.

### R4. Say which attributes to take
"Use the surface texture, the colour, the plastic sheen and the wear."

### R5. Say which attribute to ignore
**"Do not reproduce its composition."** This is the most important sentence in the entire prompt.
Without it the model treats the reference as a framing target, and the flying take collapses back
toward the input image. Omit it only when the still is genuinely meant to be frame one, and in that
case the still belongs in `--start-image`, not in `--image-references`.

### R6. Pre-empt type twice, as a fact then as an instruction
Two sentences, in this order. First a fact about the world: "All printed marks and labels are
abstract, with no lettering and no readable characters." Then an instruction: "Do not reproduce any
brand name, logo or text."

One sentence is not enough, and stating the instruction without the fact is measurably weaker,
because the model still believes the world contains readable type and then tries to hide it.

**Treat this as mandatory.** Garbled AI type belongs on your Never list.

### The two-reference rule
With two images, **give each a different job and say so.** The standard split:

| Image | Locks |
|---|---|
| `#Image1` | subject, colour, material, texture |
| `#Image2` | environment, space, light |

Two images both claiming authority over the same attribute is how a shot goes muddy. If both
references are of the subject, you have one reference and a duplicate.

---

## Part 4. The brand constraint layer

Everything above is the general engine. This part is where your own brand binds it. The entries
below are the shape of that layer, written as one worked example. Replace every value with yours.

**Faceless, if that is your house style.** No talking head. Hands, backs, shoulders,
the operator's world. `[NEGATIVE]` carries "no faces" on any shot with a person in it, and
`[MOTION]` never asks for eye contact or a piece to camera.

**The palette is your brand palette.** Fix a ground, two neutrals and **at most one accent**, then
hold that for every shot in the format. Never wash a frame in the accent: one accent per shot.
Write them as materials rather than as hex, because the model reads materials: "matte navy
powder-coat", "a single cold blue screen glow", "bone-white laminate", "grey anodised steel".

**Semi-premium, one notch below luxury, on purpose.** Precise macro, controlled lighting, shallow
depth, real-material texture. The subject is the operator's world: hands at a keyboard, a dashboard
resolving, an inbox clearing, a job board filling.

**Silent.** Every run sets `--generate-audio false` and every return is verified with `ffprobe`
before it is called done. `[AUDIO]` is omitted entirely unless a format has explicitly opted into
sound and changed its own spec to say so.

**No type in the frame, ever.** R6 is mandatory. Text is added in post, never generated.

**Terminology binds the nouns.** Your own word list governs the words inside a model prompt,
because the noun you write is the world the model builds. Keep one list and make it binding.

**Aspect.** `9:16` for the 1080x1920 primary master. Seedance offers no `4:5`, so when a format
needs 1080x1350, generate `3:4` and let the rig crop.

**House prompt rules still bind:** detailed positive prose, camera distance led, never JSON, never
a wall of negatives.

---

## Part 5. `[SHOT]`, three laws

### S1. State the one rule four ways
"One single unbroken take. There are no cuts, no edits, no transitions, no dissolves and no jumps
at any point." The redundancy is the point: each synonym closes a different failure the model
already knows how to produce.

### S2. Ban teleporting by name
"The camera flies through one continuous physical path and never teleports." A model will
cheerfully satisfy "no cuts" with a smooth impossible jump through a wall.

### S3. Give the frame an anchor
One named thing that may never leave frame. "The handset or the job cards stay visible in frame at
all times."

**Pick the anchor before writing `[MOTION]`**, because the route has to be flyable while holding
it. The right anchor is the object the ad's argument is about, which means this line quietly
enforces the demonstration doctrine: if you cannot name one object the shot is about, the shot has
no argument yet.

---

## Part 6. `[MOTION]`, seven laws

### M1. Open in medias res
The action pre-exists the shot. "a handset **already** ringing", "a printer **already** halfway
through a run". Nothing starts when the camera starts.

### M2. Every beat carries a camera verb and a subject verb
Beat grammar: **`<camera verb> + <what enters or changes> + <subject verb>`**. A beat with only a
camera verb produces a dead world with a moving lens, which reads as a video game.

### M3. Chain the beats explicitly
"then", "immediately", "as". Ordering is stated, never implied.

### M4. Physical move vocabulary, never cinema jargon
Bank: opens tight and low on · pulls back and up · banks hard · dives back down along · skims ·
drifts · settles with · rides · cranes over · tracks beside · pushes through · lifts clear of.

No "dolly", no "crane shot", no "epic sweeping". Those name a piece of equipment, not a movement.

### M5. Give the camera a rail
A boundary in the material to travel along. This is the strongest single move in the block and the
one most people skip.

Rail bank: the boundary between done and not-done · a seam · the edge of a pool of light · a cable
run · a row of desks · a fence line · a conveyor · a queue · a stack's torn edge · a wire.

Most subjects have a done / not-done line, and it is almost always the best rail available, because
travelling along it makes the shot argue for itself.

### M6. Let the camera react to the subject's physics
"It settles with the hand as the card is pulled." The subject moves, so the camera moves with it.
This one detail is what reads as a real operator on a real rig.

### M7. Land on a detail, not a wide
Finish riding something small and specific.

### The beat ceiling
**Three to five beats for a ten second take.** Past five the model starts cutting, which
contradicts `[SHOT]` and wastes the generation.

---

## Part 7. `[AUDIO]`, `[NEGATIVE]`, `[END]`

**`[AUDIO]`.** Omitted by default, see Part 4. When a format has opted in, write it to `[LOOK]`
standard: named sources, in the room, no music bed unless the format asks for one.

**`[NEGATIVE]`.** Three to six items, and **only failures this subject invites**: extra fingers on
a hands shot, readable signage in an office, a logo on a vehicle, a second machine where there is
one, a face entering frame. The general ones already live in L9. If this list is getting long, the
fix is a more specific `[LOOK]`, not a longer `[NEGATIVE]`.

**`[END]`.** One sentence naming the frame the take lands on: what fills frame at the last moment,
and what the camera is doing as it arrives. A take with no stated ending drifts. When the format
loops, the end frame is the opening frame and `--end-image` carries it.

---

## Part 8. The template

Fill every bracket. **If a bracket cannot be filled with something photographable, the shot is not
specified yet and no generation should be bought.**

```
[LOOK] <production context> for a real <kind of business>. Shot on <format> with a <lens>, single
continuous take, camera flying at all times. Practical light only: <quality+source+position>,
<quality+source+position>, <what the space between them does>, no fill. Palette of <adj+material>,
<adj+material>, <adj+material>, <adj+material>, <adj+material>. <Fine|Coarse> film grain, gentle
halation on <named edges>, <particulate> suspended in <named light>. <Shallow|Deep> depth with
focus pulled continuously by hand. Every surface has real wear: <object+residue>, <object+residue>,
<object+residue>, <object+residue>. Nothing looks rendered. Nothing looks like stock. 9:16
vertical, 24fps.

[REFERENCES] #Image1 is the locked <thing>, colour and materials: <the image restated in words>.
Use the <attribute list>. Do not reproduce its composition. All <printed marks|labels|motifs> are
abstract, with no lettering and no readable characters. Do not reproduce any brand name, logo or
text.
[#Image2 is the locked <environment>, space and light: <restated in words>. Use <attributes>. Do
not reproduce its composition.]

[SHOT] One single unbroken take. There are no cuts, no edits, no transitions, no dissolves and no
jumps at any point. The camera flies through one continuous physical path and never teleports.
<the anchor> stays visible in frame at all times.

[MOTION] The take opens <framing> on <subject already mid-action>, <subject verb>, <second subject
verb>. The camera <camera verb>, revealing <what enters frame>, then <camera verb> along <the
rail>, <what differs on either side of the rail>. It <camera reaction to the subject's physics>,
and <final beat riding a detail>.

[NEGATIVE] <3 to 6 failures this subject invites>.

[END] <the last frame, and what the camera is doing as it arrives>.
```

---

## Part 9. Worked example

A faceless subject, a fixed brand palette, no type. One supplied still of the desk.

**The argument:** a construction business's quoting backlog sitting untouched overnight.

```
[LOOK] Observational documentary for a real construction business. Shot on 35mm with a 28mm
close-focus lens, single continuous take, camera flying at all times. Practical light only: a
single cold overhead tube stuttering on, thin blue-grey pre-dawn through a roller-door gap behind
camera, the middle of the room going to black between them, no fill. Palette of matte navy
powder-coated shelving, bone-white laminate desk, grey anodised steel trays, sun-greyed manila
folders, one cold blue monitor glow. Fine film grain, gentle halation on the tube ends and the
steel tray edges, dust suspended in the roller-door light. Shallow depth with focus pulled
continuously by hand. Every surface has real wear: biro dents along the desk edge, a coffee ring on
the top folder, tape residue on the tray lip, sun-bleach across the folder spines. Nothing looks
rendered. Nothing looks like stock. 9:16 vertical, 24fps.

[REFERENCES] #Image1 is the locked desk, colour and materials: a bone-white laminate desk with grey
steel trays, a stack of manila folders and navy shelving behind. Use the surface texture, the
colour, the laminate sheen and the wear. Do not reproduce its composition. All printed marks and
labels are abstract, with no lettering and no readable characters. Do not reproduce any brand name,
logo or text.

[SHOT] One single unbroken take. There are no cuts, no edits, no transitions, no dissolves and no
jumps at any point. The camera flies through one continuous physical path and never teleports. The
folder stack stays visible in frame at all times.

[MOTION] The take opens tight and low on the stack already leaning under its own weight, the top
folder lifting slightly as the roller door moves air across it. The camera pulls back and up,
revealing the whole desk and the empty chair behind it, then banks hard and dives back down along
the desk surface, skimming the boundary between the signed folders behind and the untouched ones
ahead as the blue monitor glow reaches the near edge. It settles with a hand entering frame and
landing on the third folder down, and rides the folder's torn corner as it lifts clear of the
stack.

[NEGATIVE] No faces, no readable text on the folders, no visible screen content, no second desk, no
duplicated hands.

[END] The take lands on the pulled folder filling the lower frame, the stack still leaning out of
focus behind it, the camera drifting a few centimetres closer as it arrives.
```

Every block is the template. Only the nouns moved, and every noun came from the brand constraint layer.

---

## Part 10. Failure table

Read the return, find the symptom, fix the block. Never buy a second generation before doing this.

| Symptom in the return | Cause | Fix |
|---|---|---|
| Looks plastic, looks AI | `[LOOK]` carries style words | Apply the Part 2 test to every clause and replace what survives it |
| The model cut, despite `[SHOT]` | too many beats | Cut `[MOTION]` to three beats |
| Framing collapses back toward the reference still | R5 missing, or the still was passed as `--start-image` | Add "Do not reproduce its composition" and move the still to `--image-references` |
| Camera wanders into invented geography | no anchor | Add S3 with a named object |
| Only the camera moves, the world is dead | beats carry camera verbs only | Rewrite every beat to M2 grammar |
| Garbled type or an invented logo appears | R6 written as one sentence, or as instruction only | Two sentences, fact first then instruction |
| The frame washes out in one colour | palette written as colours, or more than one accent | Rewrite L5 as five adjective-plus-material entries, one accent maximum |
| A face enters frame | faceless not stated | Add "no faces" to `[NEGATIVE]` |
| Audio came back | flag missing | `--generate-audio false`, then re-verify with `ffprobe` |

---

## Part 11. Wiring and the run protocol

Verified live off the CLI on 2026-08-16, `higgsfield model get seedance_2_5`.

| Param | What matters here |
|---|---|
| `job_type` | `seedance_2_5`. `seedance_2_0` remains the multi-shot workhorse; this layer owns the reference-driven single take |
| `mode` | **`omni_reference`.** `t2v` refuses reference media entirely, so a supplied image forces this mode |
| `image_references` | array, up to 30 images counting `start_image` and `end_image`, 50 reference items total |
| `start_image` | allowed **only** in `omni_reference`, and it is literally frame one of the render. A reference that must not open the shot does not go here |
| `end_image` | same restriction. Use it when the format needs to land on a known frame, or loops |
| `aspect_ratio` | `auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16`. Default `16:9`. **No 4:5** |
| `duration` | integer, default 5. The cost endpoint quotes 4 through 20 linearly. **The create-side cap is untested on this account** |
| `resolution` | `480p, 720p, 1080p`. Default `720p` |
| `generate_audio` | defaults **true**. Set `false` on every run |
| `bitrate_mode` | `standard` or `high` |
| `extension_mode` | valid **only** with `mode: video_extension` |

**Cost, off `higgsfield generate cost`, 2026-08-16, 9:16, audio off:** 6.5 credits per second at
720p, 9 at 1080p. So 45 credits for a 5s 1080p take, 90 for 10s.

Exact commands live in `COMMANDS.md` in this folder. Anything in chat is a preview of that file.

### The protocol

1. **Write the blocks into a file first.** Never compose a prompt inside a shell command.
2. **Run the pre-flight** (Part 12).
3. **Cost it before creating it.** `higgsfield generate cost` takes the same flags and spends
   nothing, and it also confirms the references upload cleanly.
4. **One paid generation, then stop.** Create one, wait, review the return against the failure
   table, and stop. A second only after you have seen the first. House floor, no exceptions.
5. **Verify silence** with `ffprobe` before the clip is called done.
6. **Look at frames before reporting.** A clean exit code is not a reviewed shot.

---

## Part 12. Pre-flight

Nine checks, before any spend. A no on any line is a rewrite, not a generation.

1. Does every `[LOOK]` clause name something photographable?
2. Are there exactly five palette entries, each adjective plus material, with at most one accent?
3. Are there exactly four wear items, each an object plus its own residue?
4. Does `[REFERENCES]` say "Do not reproduce its composition"?
5. Is the type pre-empt two sentences, fact then instruction?
6. With two images, does each lock a different attribute?
7. Is there a named anchor in `[SHOT]`?
8. Are there three to five beats, each carrying a camera verb and a subject verb?
9. Is `--generate-audio false` in the command?

---

