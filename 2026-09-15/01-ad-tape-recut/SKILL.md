---
name: ad-tape-recut
description: Turn video ads you have already run (or any short to-camera footage of one person) into a bank of spoken segments and a set of new single-speaker cuts, each re-ordered from the same footage with a new text hook plated over the old headline card. Use when the user says "recut the ads", "splice the founder videos", "chop these up across the funnel", "new hooks on the old ads", "the ad export landed", or drops a folder of exported ad videos and wants variations without shooting anything. Do NOT use for footage that needs generated video, a voice-over, or lines the person never said.
---

# Ad tape recut

You have a folder of video ads that already ran. Each one is a person talking to camera, usually
with a burned-in headline card and captions. This skill turns that folder into a bank of spoken
segments, then into new cuts: the same person, the same words, in a new order, opening on the
strongest line, with a new hook plated over the old card. Nothing is generated. The whole chain is
Whisper for the words, ffmpeg for the cut, and a small amount of Python to make the cut points
land between sentences instead of inside them.

On the tape this was built on, 19 exported ads became 28 finished cuts in two days, with a second
campaign of 9 films recut the day after on the same scripts. Every cut cost nothing but minutes.

Read the whole file before you run anything. Phase 0 is mandatory.

---

## Phase 0. Establish ground truth before you cut anything

Do this every time. The point is to build for the footage and the machine in front of you.

### 0.1 Read the workspace

From the directory you were opened in, look for:

| Look for | Why it matters |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, root `README.md` | Operating rules already written. Inherit them. If they ban a word, a font or a tool, that ban wins. |
| A brand or design folder (`brand/`, `design-system/`) | The font for the hook plate and the one accent colour, if any. Default is a white plate with black text in a heavy system font. |
| An existing edit workspace (`transcripts/`, `cuts/`, a segment bank) | Extend it. Never start a second bank beside one that exists. |
| The campaign export itself (videos, statics, a copy file) | The videos are the asset. Primary text in an export is usually the same few variants on every ad and carries no per-video signal. Statics are never touched. |
| Anything that looks like a secret (`.env`, `*token*`, `*credential*`, `*.key`) | Note that it exists and do not open it. This skill needs no credentials. |

Report back in five lines: what the campaign is, how many films and who is in them, whether a
bank already exists, what the brand rules say about type, and what you looked for and could not
find. Ask the user to correct it. Then continue.

### 0.2 Detect the environment and branch on it

```
python3 --version                 # 3.10 or later
ffmpeg -version | head -1         # and ffprobe beside it
python3 -c "import whisper"       # openai-whisper, the local model
python3 -c "import PIL"           # Pillow, for the hook plate
```

| Missing | macOS | Linux | Windows |
|---|---|---|---|
| ffmpeg | `brew install ffmpeg` | `sudo apt install ffmpeg` | `winget install Gyan.FFmpeg` |
| whisper | `pip install openai-whisper` (needs ffmpeg first) | same | same, in a normal terminal |
| Pillow | `pip install pillow` | same | same |

Whisper `medium.en` is the model this was built on. It downloads about 1.5 GB on first use and
runs on CPU at roughly real time for a 90 second ad on a recent laptop. `small.en` is faster and
mishears more. `large` is slower and rarely better on clean to-camera audio. On a machine with no
GPU and under 8 GB of RAM use `small.en`.

**Branch on the runtime.**

- **Claude Code or Codex on a laptop.** The full path.
- **A headless VPS.** The full path works. Copy the footage up first. Do not stream it.
- **A chat-only agent with no shell.** Stop. This skill runs a transcriber and a video encoder.
  Say so and offer to write the segment bank and the recipes by hand from a transcript the user
  pastes, for a coding agent to render later.
- **An existing cutter in the project.** Read it. If it already snaps cut points to words, use it
  and skip section 4.

### 0.3 Decide what "done" is before you start

Write `BRIEF.md` in the workspace with three lines. If the user cannot answer one, ask.

1. **Who is on the tape and where it goes.** One speaker per finished cut. Which stages of the
   funnel each cut is for (cold, warm, ready to buy. Or your own labels).
2. **What a hook is allowed to say.** New hook lines are drafted in the speaker's own register and
   shown to the user before a single plate is rendered. The user's lines ship verbatim.
3. **Where the finished files go.** A folder, a CMS, a scheduler. This skill stops at the folder.

---

## 1. The laws

These came out of the first tape, one failed render at a time. They bind every cut.

1. **Only words on tape.** A cut is built purely from spoken segments in the footage, re-ordered
   and trimmed. No bridging line, no voice-over, no written insert. If the argument needs a beat
   the tape does not carry, that beat is a hand-off point into a different asset, never patched in.
2. **One speaker per cut.** A cut is one person from start to finish. The first cross-speaker
   render read as two ads stitched together, and it was.
3. **Never cross a lighting setting.** Before any cross-film splice, pull a frame at 6 seconds and
   mid-film from every source and group the films by room and light (`SETTINGS.md`). A recipe that
   cuts to a film shot in a different room is removed outright, even when only the closing line
   crosses. A walk-and-talk film the original editor already cut across rooms is its own setting:
   re-order inside it freely, never splice it into another film.
4. **Every cut point is sentence-safe and every join is faded.** The start snaps to the caption
   change that brings the first word up. The end runs to the end of the spoken sentence (Whisper
   punctuation and word timings) and then to the caption change that takes it down, never into the
   next word. 30 ms audio fade at every join. Contiguous segments from one film stay as one take.
   A segment that ends on a run-on with no full stop is a WARNING in the cut list. Check those
   first.
5. **The text hook covers the old card exactly.** The old ad carries a burned-in headline. The new
   hook is a plate sized to that card's exact box with the new line inside it. Blur was tried and
   rejected. A film with no card gets the hook as a pill pair at the top.
6. **Hook lines are the user's, verbatim.** Generic hook banks read flat on real people. Draft in
   the speaker's register (direct address, "the real reason", "don't X before Y", "stop trying
   to", "no clue how to X? watch this"), show the lines, take the user's edits word for word.
7. **Isolate a noisy speaker's audio, leave the clean one alone.** Run a speech enhancer over the
   cut's audio only when the room needed it, keep the raw copy, copy the video stream untouched.
8. **Nothing goes over the tape.** No animation inserts, no split screen, no B-roll windows. All
   three were built and then cut on the first tape. The person carries the ad.
9. **Never render before the user asks.** The recipes on a review page are the deliverable of the
   analysis. Media is cut when the user says render.
10. **The edit loop is dictation.** The user reads the review page and dictates per cut id: new
    opening line, cut to this line, loop that line back in, delete this one, make me alternates.
    Apply verbatim, delete what they cut, rebuild the page, re-render only the ids that changed.

---

## 2. The steps

1. **Land the export.** Source videos stay where the user put them, read-only. Make a workspace.
   Hash the files first (`md5` or `sha1sum`): exports often carry byte-identical duplicates under
   different names. Give every film a short prefix (`D`, `H`, `SIX`) and record which prefix is
   which speaker in `tape.json`. Every id downstream hangs off that map.
2. **Transcribe with timecodes, then words.** `scripts/transcribe.py` writes
   `transcripts/<stem>.json` and `.txt` per film (segments with start and end) and
   `transcripts/ALL.md`. `scripts/words.py` writes `transcripts/<stem>.words.json`, one entry per
   word. Get all of them before the first render. The user's cut points fall mid-sentence and the
   cutter needs the words. `scripts/analyse.py` writes `analysis/<stem>.json`: silence gaps and
   caption-change frames.
3. **Segment bank.** Cut every film into spliceable segments with start, end, stage and beat in
   `bank.json` (the shape is in `examples/bank.json`). Beats that worked: HOOK, PAIN, EDU, CRED,
   TURN, ROLE, DIFF, PROOF, TEACH, OFFER, CTA. Flag a third voice on tape, a third-party clip with
   unclear rights, and any line whose shape your brand rules ban.
4. **Settings map, before any recipe.** `scripts/settings.py` pulls a frame at 6 seconds and
   mid-film from every source into `settings/`, and a strip every 12 seconds. Group them by room
   and light into `SETTINGS.md` by eye. Law 3.
5. **Recipes.** `recipes.json`: one speaker per recipe, the film that carries the hook first, then
   that speaker's other films inside the same setting. Open on the strongest stat or line. Aim for
   a first pass across every stage plus the standalone cuts hiding inside any long film.
6. **Review page.** `scripts/build_review.py` writes `review.html`: each recipe as the spoken
   script, with a rail carrying stage, runtime, every segment's timecodes and source, and flags.
   This is the analysis deliverable. Nothing is rendered yet.
7. **The user's edit round.** Dictation (law 10). Then `scripts/cut.py --all` renders every
   approved recipe into `cuts/`. Each render writes `cuts/<id>.mp4`, `cuts/<id>.cutlist.txt` (in
   and out points with the words at each end, WARNING on a run-on) and `cuts/<id>.timeline.json`
   (the parts and every word re-timed onto the cut, read by the hook step).
8. **The user's media round.** They watch the folder and rule per cut. Re-render only the ids that
   carry a changed segment. If they cull by deleting files, re-list `cuts/` before anything else
   and treat a missing mp4 as a cut.
9. **Audio, only where needed.** A/B a 20 second excerpt first. If a room is noisy, run a local
   speech enhancer over `cuts/<id>.mp4`'s audio to a wav, then `scripts/swap_audio.py` muxes it on
   with the video copied and the raw file kept in `cuts/raw-audio/`. Any enhancer works. Pick one
   your security review clears, pin the version, and never run one on a clean room.
10. **Text hooks.** `hooks.json`: per id, `text_hook` (two lines, `\n`), and an optional `y`.
    Draft the lines, show them, take the user's verbatim. `scripts/cardbox.py` finds the burned-in
    card's box once per film (`analysis/_cardbox.json`). `scripts/hook_plate.py [ids]` writes
    `hooked/<id>.mp4`: the cut, a white plate over the card's exact box with the hook inside it,
    or the pill pair at the top for a film with no card, or at the user's `y`.
11. **The user's hook round.** They rewrite, move, delete. Re-render the keepers. On the first
    tape this took 26 to 16.
12. **Hand-off.** The finished files in `hooked/`, a `CUTS.md` index (id, speaker, stage, seconds,
    hook, script), and nothing else. Uploading is a different skill with its own approval.

---

## 3. What the user dictates, and how it maps

| They say | Do |
|---|---|
| "start with [line]", "make T4 open on the 238 line" | move that segment to position 1, trim the film's own hook out |
| "it should cut to [line]", "then it goes into [line]" | append that segment, same speaker, same setting |
| "loop that line back in to give context" | repeat a segment already used, at the point named |
| "that line all the way through / down to [word]" | run the film natively from that word to its end or to the named word |
| "the rest can read the same" | keep the remainder of the recipe as it stands |
| "make another variant that starts with [line]" | new id `T5b`, same body, new opening |
| "you're limiting yourself, look at the other videos" | widen the pull to every film of that speaker inside the setting |
| "get rid of that one" | delete the id from the recipes, the page and the folder |
| "it goes too quickly into the sell, bridge it" | write alternates that add an EDU or PAIN segment before the OFFER |
| "finish the sentence", "it cuts too quickly" | move the segment end past the full stop on the word timing |
| "same hooks, vary them" | distinct openers from the speaker's other films, one per id |

---

## 4. The cutter, in one paragraph

For each segment the start snaps to the caption change that brings the first word's caption up
(never inside the previous word). The end runs to the end of the sentence (Whisper punctuation, up
to 0.8 s past the requested end), else trims back up to 2.5 s to the last full stop, else warns. Then it runs
to the caption change that takes that caption down, never into the next word. Silence gaps
corroborate. One ffmpeg pass: trim, 30 ms audio fade in and out on every part, concat, encode at
720x1280 30 fps, the source's burned-in captions travelling with each part. Contiguous parts from
one film merge into one take. The first cutter did hard cuts on segment timecodes, and it is why
the user heard clicks, cold starts and clipped sentences on the first batch. Read
`references/cut-points.md` for the reasoning.

---

## 5. Lessons that cost time

- Get every film's word timings before the first render, and read the cutter for what it does at a
  join before rendering 35 cuts. The first batch was re-rendered twice.
- Pull the settings frames before writing recipes. Nine recipes and a whole stage column were
  written and rendered before the lighting rule surfaced.
- A cut of 31 recipes on a laptop is about 40 s each. Run it in the background and count the mp4s.
- When the user asks for progress mid-render, answer with the count done and the minutes left, in
  one line.
- Whisper mishears stay on the display text and are named once at the top of the review page. The
  tape is the tape.
- The user approved a whole second tape unedited, so the edit round can be skipped when they say
  so. The media round then does the culling.

---

## 6. Files in this skill

- `scripts/transcribe.py`, `scripts/words.py`, `scripts/analyse.py`: the words and the joins.
- `scripts/settings.py`: the frames for the settings map.
- `scripts/build_review.py`: the review page from `bank.json` and `recipes.json`.
- `scripts/cut.py`: the sentence-safe cutter. `--all`, ids, or `--timelines`.
- `scripts/cardbox.py`, `scripts/hook_plate.py`, `scripts/swap_audio.py`: the hook and the audio.
- `examples/tape.json`, `examples/bank.json`, `examples/recipes.json`, `examples/hooks.json`: the
  shapes, with invented ids.
- `references/cut-points.md`: why the cut points land where they do.
- `references/hook-register.md`: the shapes a hook line takes, with placeholder examples.

Every script reads `tape.json` in the workspace for the source folder, the file glob and the
prefix map. Lines marked `# ENV` are the ones that change per machine.
