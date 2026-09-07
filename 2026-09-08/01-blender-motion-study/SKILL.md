---
name: blender-motion-study
description: Make a short vertical animation in Blender, rendered on the CPU of the machine you already own, where one white object becomes the next in step with a line of script. Use when the user says "blender motion study", "animate this line", "make the object become the next object", "white on black animation", "render this in Blender", or wants motion for a narrated short without a paid video model. Do NOT use for photoreal footage, character acting, lip sync, or anything that needs a GPU render farm.
---

# Blender motion study

An agent that reads a line of script, decides which object stands for it and what that object turns into, writes the scene as Blender Python, and renders it on your laptop under a resource monitor. Two films of about a minute each and a five second study were made this way in the four days after the skill was written, from one brief each, with no paid video model anywhere in the chain.

The style is deliberately narrow, because a narrow style is what makes an agent's output look like one hand made it: **white objects on pure black, vertical, a front-facing camera that never moves, one dominant subject on the centre line, and motion that dissipates after every arrival.**

Read the whole file before you run anything. Phase 0 is mandatory.

---

## Phase 0. Establish ground truth before you build

Do this every time, before any geometry. The point is to know what this machine and this project can already do, so the study is built for the reality in front of you and not for the machine this skill was written on.

### 0.1 Read the workspace

From the directory you were opened in, look for the things that change how this skill runs:

| Look for | Why it matters |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, root `README.md` | Operating rules already written. Inherit them. If they ban a word, a colour or a tool, that ban wins. |
| A brand or design folder (`brand/`, `design-system/`, `styles/`) | The font and the one accent colour, if there is one. This skill's default is white on black with no accent; a brand file can add exactly one. |
| An existing `scripts/`, `engine/` or `rigs/` folder with Blender code | Extend it. Never build a second render path beside one that already works. |
| A script, voice read or caption file for the line you are animating | The words and, if narrated, their timestamps. Pictures are timed to words, never the other way round. |
| Anything that looks like a secret (`.env`, `*token*`, `*credential*`, `*.key`) | Note that it exists and do not open it. This skill needs no credentials. |

Report back in five lines: what the project is, whether Blender code already exists, what the line of script is, whether it is narrated, and what you looked for and could not find. Ask the user to correct it. Then continue.

### 0.2 Detect the environment and branch on it

Run these and record the answers. Every later step depends on them.

```
python3 --version                # 3.10 or later
ffmpeg -version | head -1        # muxes the PNG frames into an mp4
blender --version                # or the full path, see the table
```

**Find Blender.** The scripts look in the `BLENDER` environment variable first, then the usual place for your OS, then `PATH`.

| OS | Usual location | Install if missing |
|---|---|---|
| macOS | `/Applications/Blender.app/Contents/MacOS/Blender` | `brew install --cask blender`, or the DMG from blender.org |
| Linux | `/usr/bin/blender`, `/snap/bin/blender`, or an extracted tarball | `sudo snap install blender --classic`, or the tarball from blender.org |
| Windows | `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` | The installer from blender.org, or `winget install BlenderFoundation.Blender` |

Use **Blender 5.2 LTS**. The scene code was written and tested against it. Blender 4.x will run the JSON renderer but the deformation workaround in section 5 was only verified on 5.2.

**Confirm it runs headless.** `blender -b --version` must print a version and exit. On a locked-down machine or a container with no display, Blender can still crash on startup while it probes for a graphics backend even when you only want CPU rendering. If that happens:

- macOS: run the command outside any sandbox that blocks `nice` or `ps`. The monitor checks for both before it launches Blender and refuses to start if either is denied.
- Linux headless server: install `libgl1` and `libxi6` (or `mesa-libGL` and `libXi` on Fedora). Blender needs them present even in background mode.
- Windows: run from a normal terminal, not a service account.
- No luck: this skill cannot run here. Say so. Do not try to "work around" a startup crash by removing the monitor.

**Branch on the runtime you are in.**

- **Claude Code or Codex on a laptop with a screen.** The full path. Everything below applies.
- **A headless VPS or container.** The full path still works, and it is slow: budget three to five times the laptop timings in section 7. Keep the monitor's 15 minute budget and render in proof mode first.
- **A chat-only agent with no shell.** Stop. This skill writes files and runs a renderer. Tell the user it needs a coding agent with shell access and offer to write the storyboard (section 2) for them to hand to one.
- **Existing Blender code in the project.** Read it. If it already has a scene builder, add your scene to it and use its render command. Only fall back to this skill's scripts where the project has none.

### 0.3 Decide what "done" is before you start

Write these three lines down in the study's folder as `BRIEF.md` before any geometry. If the user cannot answer one, ask.

1. **The line.** The exact words the picture is for. One line, one clause, or one sentence. Not a paragraph.
2. **The bar.** Length in seconds, frame rate, and whether it is a proof for the user's eyes or a candidate for posting.
3. **The refusals.** Anything the brand or the user has banned on screen. The default banlist is in section 4.

---

## 1. The style, and why it is this narrow

**Composition.** 1080 by 1920, pure black world, white constant-colour objects with no shading, no emission bloom, no glow. A front-facing orthographic camera that does not travel. One dominant focal subject on the central vertical axis; symmetric supporting parts may flank it. Three to five visible elements at most, one of them dominant. Count visible focal groups, not mesh parts.

**Motion.** Something meaningful happens every one to two seconds. Decorative wobble, perpetual bounce and idle drift do not count as meaning. After every arrival the motion dissipates: a brake, a small settle, then a readable hold. Transitions are short, roughly 0.2 to 0.4 seconds, and the hold is where the meaning is read.

**Why narrow.** A model given a wide style invents blandly and differently every time. Given this one, its output looks like one hand made the whole series, and a person can tell at a glance whether a frame is right. Every rule below exists because a render broke it and looked wrong.

---

## 2. The semantic storyboard, required before geometry

Map the line of script against the picture **before** you write a shape. For every meaning-bearing clause, record in a table:

| Spoken span | Input state | Visible action | Resulting state | Object | Continuity anchor | Lane |
|---|---|---|---|---|---|---|

- **A noun match is not enough.** A house on screen while the words are about pricing is the failure this table exists to catch. The picture must show the **verb and its consequence**. Ask: if this action played silently, would a stranger know it belonged to this clause and not to three unrelated ones? If not, redesign it.
- **Transformation means geometry changes.** Scaling one icon down while another scales up is a swap, not a transformation. An object becoming the next object changes its geometry or its functional arrangement: a ball opens into a house, a sheet folds into a plan, a clock's hands become a spinning gear.
- **Reuse a motif only when its state changes.** The same object may return later if its state now means something new (the delayed thing coming back as the enabled thing). Record the change in the table.
- **Narration first.** If the line is spoken, lock the read before you animate, and get word timestamps (any speech-to-text with word timing will do). Time the pictures to the words. If the read is replaced later, redo the timing; never speed the audio up to fit old pictures.

Put the table in `semantic-map.json` or `STORYBOARD.md` beside the scene. The example scene script refuses to run when its beats have no spoken span, and that is the behaviour to copy: a scene with an unmapped beat is a scene with a picture nobody asked for.

---

## 3. The two lanes of movement

Alternate these to fit the script. Neither is the default. Both are authored kinematics, not physics simulation, which keeps the render deterministic and cheap.

### Lane A. The weighted whole-object handoff

The held object exits left as one piece, and the next arrives from the right, brakes near centre, and settles. Treat each object as having a mass, an arrival speed, a braking interval and a pivot. A wide heavy plan brakes firmly with a restrained lean and strong damping. A light sheet arrives faster, overshoots a little and rocks once. A third object may stop clean with no rebound at all. Vary the response per object; a uniform spring on everything reads as a preset. Overlap the incoming object's entrance with the outgoing object's exit so there is never an empty frame.

Long version: `references/weighted-object-handoff.md`.

### Lane B. Rapid decomposition and recomposition

One readable object breaks into meaningful groups and reforms as the next object through a shared centre, fast. Accelerate into the change, reform clearly, dissipate the remaining motion in a brief settle. Keep a visible core bridging the two constructions so attention never has to jump. The busy intermediate should last 0.2 to 0.4 seconds with small timing offsets between the groups. Do not force every old stroke into a particular new stroke; a group can simply be replaced behind the core.

Long version: `references/rapid-recomposition.md`.

### What neither lane is

Slow shredded intermediates, random particles, a long invisible gap between objects, uniform bouncing, a hard cut with no motion bridging it, and a slow morph of one icon into another where the halfway shape reads as nothing.

---

## 4. The banlist (a hard fail on the render)

Anything on this list in a rendered frame means the frame is rejected, whatever else is right about it.

- Glow, bloom, luminous trails, neon, gradients, coloured shadows, lens flares.
- Captions burned into the render. Type is a separate layer added afterwards, so it can be changed without a re-render.
- Random particles, debris, dust, sparkles.
- Camera movement of any kind in this style. The subject moves, the camera watches.
- A frame with more than one dominant subject, or with nothing dominant.
- Any object the script did not ask for. If it is decorative, it is out.
- Receipts, invoices, dashboards, floating glass cards, disconnected grids of tiles, invented UI. These are the props an agent reaches for when it has not understood the clause. Redesign the clause instead.

---

## 5. Building the scene

Two paths. Pick by how much control the shot needs.

### Path 1. JSON scene through `scripts/render.py` (stills and simple moves)

For a held picture, a single travel, or a proof of a composition. Write one JSON file describing `output`, `world`, `materials`, `lights`, `camera` and `objects`, and render it:

```
python3 scripts/render.py examples/white-on-black.json --still --scale 0.35 --out out/proof
python3 scripts/render.py examples/white-on-black.json --out out/full
```

The full contract is documented at the top of `scripts/bpy_scene.py`. Object types are `plane cube sphere cylinder cone torus text image import`; each takes `loc`, `rot` (degrees), `scale`, `material`, `bevel`, `smooth` and optional `keys` (keyframes). Materials carry colour, roughness and metallic and **have no emission field by design**. Relative file paths resolve against the JSON. `--scale 0.35` is the proof size; look at the PNG before rendering full size. A clean exit code is not a reviewed picture.

### Path 2. A bpy script through `scripts/monitor_render.py` (the motion lanes)

For anything with the two lanes in it. Write a Python script that runs inside Blender, builds the objects, keys their motion frame by frame, and renders a chosen frame range. `scripts/motion_study_example.py` is the worked example: 300 frames at 60 fps, a compression that becomes a machine that hands off to a growing tree. Copy its structure and replace its objects with yours.

```
python3 scripts/monitor_render.py scripts/motion_study_example.py out/study proof       # 10 frames at half size
python3 scripts/monitor_render.py scripts/motion_study_example.py out/study animation   # all 300 frames
ffmpeg -framerate 60 -i out/study/frames/%04d.png -c:v libx264 -pix_fmt yuv420p out/study/study.mp4
```

Things the example does that you should keep:

- **Constant-colour white material.** An emission shader at strength one on a pure black world with the `Standard` view transform. This is a flat colour, not a glow; there is no bloom pass anywhere.
- **Orthographic front camera**, fixed, `ortho_scale` around 6.3 for a 9:16 frame.
- **Curves with `bevel_factor_end` keyed** for draw-on growth, and non-cyclic curves closed with an explicit final point, because a cyclic curve at zero bevel factor can stay visible.
- **A child branch begins only after its parent tip reaches the junction.** Overlapping draw-on intervals produce detached tips.
- **A tiny 2D physics loop for the one thing that needs it** (the ball) and authored kinematics for everything else.
- **Save the `.blend` beside the frames** so a person can open and edit the scene.

**Deformation crash workaround (verified on Blender 5.2).** For an object whose mesh vertices change shape over time, use absolute shape keys and animate the evaluation time. Keying raw vertex coordinates through F-curves caused heap corruption on a full-length scene, and it did not always show up on the first save. Verify by reopening the saved file fresh and scrubbing the timeline before you trust it.

---

## 6. Run protocol

1. Phase 0, written down.
2. The storyboard table (section 2), written down, spans covered end to end.
3. Proof render. Look at the frames. Check the first pose, the transition midpoint and the last pose at phone size. A silhouette that reads at 300 pixels wide reads everywhere.
4. Fix what the proof shows. The usual finds: an object facing the wrong way for its travel (the nose must lead), a previous object flashing back for a frame or two after its exit, two focal groups fighting, a transition that is a swap and not a transformation.
5. Full render under the monitor. Never remove the monitor to get a render to finish.
6. Mux with ffmpeg. Add captions and any type as a separate layer in your video tool, timed to the same word timestamps.
7. Watch the whole thing once at full speed and once at quarter speed. Then hand it over as a **candidate**, never as done. A person calls it done.

---

## 7. What to expect from the machine

Observed on one Apple laptop, CPU only, three render threads, low priority. These are what that machine did, not budgets you are owed.

| Render | Frames | Wall time | Peak memory | Peak CPU |
|---|---|---|---|---|
| Five second study, 1080 x 1920, 60 fps, 8 samples | 300 | about 4 minutes | about 0.5 GB | about 3 cores |
| Six second handoff study, same settings | 360 | about 3 minutes | about 0.5 GB | about 2.6 cores |
| Two second deformation test, 640 x 640, 16 samples | 48 | about 2.5 minutes | about 0.9 GB | 3 cores |
| One still, 800 x 1000, 48 samples | 1 | about 40 seconds | about 0.7 GB | 3 cores |

A minute of film is a few thousand frames and renders in the background over an hour or so at these settings. Nobody sat and watched it. The monitor's 15 minute budget is per invocation, so render a long film in ranges (the example script takes a frame range through its mode argument) and mux the ranges together.

**The monitor stops the render** above 4 GiB resident memory, on an OS thermal warning (macOS), after two samples above 350 percent CPU, or at 15 minutes. It samples every five seconds and writes `<mode>-usage.json` and `<mode>-summary.json`. Read the summary before you read the frames.

---

## 8. What this skill does not prove

Say these plainly when you hand over, so nobody promises a client something the method cannot do.

- Continuous deformation of one solid into another is proven for simple shapes with the same vertex count. Holes, splits and merges need different construction and are not covered.
- Character animation, facial acting, lip sync, cloth and fluid are not part of this style and have not been made reliable with it.
- Photoreal output is out of scope. This is flat graphic motion.
- A reference render handed to a video model as motion guidance does not guarantee the model keeps the physics. Check the generated take again.

---

## The five second brief (start here)

Hand your agent this, with your own line in it, before you ask for a minute of film.

```
GOAL
Make a five second silent motion study, 1080 by 1920, for one line of script: "<your line>".
Original objects and an original sequence for this line. The compression, the pinball machine and
the tree belong to the example and stay out.

THE STYLE
White objects on pure black. A front-facing camera that does not travel. One dominant subject on the
central axis; symmetric supporting parts may flank it. Readable holds, and motion that dissipates
after every arrival.

THE STORYBOARD FIRST
Write the semantic storyboard before touching geometry: the object the line is about, the
transformation that carries its meaning, and the object it becomes. A transformation changes the
object's geometry or functional arrangement; scaling one icon down and another up is not one.

THE LANES
Alternate the two lanes. Weighted whole-object handoffs with varied braking and settling. Rapid
decomposition and recomposition around the centred focal position, with a visible core bridging the
constructions. Something meaningful happens every one to two seconds.

THE RULES
No bloom, no glow, no luminous trails, no captions, no random particles, no camera movement, no
forced slow morphs. Contacts reverse a moving part's velocity; travel between contacts uses gravity.
Authored kinematics for exits and arrivals, never simulated mass.

THE BAR
Proof first, then the full render on the CPU under the monitor: 60 frames a second, 300 frames.
Hand back the MP4, the .blend and the storyboard table. Every render is a candidate for my review;
nothing is finished, nothing is posted, and no paid model is called.
```
