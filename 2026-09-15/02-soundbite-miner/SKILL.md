---
name: soundbite-miner
description: Mine every podcast, interview and talk a person has already appeared in on YouTube into a bank of verified, cut, short-form soundbites, using the captions YouTube already made instead of transcribing hours of audio. Use when the user says "clip the podcasts", "find soundbites", "what has [name] said on camera about X", "pull the best moments from the interviews", or wants short-form clips of a founder without shooting anything. Do NOT use for videos with no captions in any language, for footage the user does not have the right to reuse, or when the person is not the one speaking.
---

# Soundbite miner

Most founders have hours of themselves on other people's podcasts and none of it in a form they can
post. This skill finds every episode, pulls the auto-captions YouTube already made, has a small
model read the transcripts for passages that stand alone as a 15 to 90 second clip, verifies every
candidate quote against the caption words so nothing invented survives, then downloads only the
sections that verified. On the first run 164 episodes became 467 verified soundbites for about the
cost of a coffee in model calls, and 90 hours of audio was never transcribed.

Read the whole file before you run anything. Phase 0 is mandatory.

---

## Phase 0. Establish ground truth before you fetch anything

### 0.1 Read the workspace

| Look for | Why it matters |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, root `README.md` | Operating rules already written. Inherit them. |
| A people or brand folder with the speaker's bio, companies, themes | The mining brief is written from this. Without it the model cannot tell the speaker from the host. |
| An existing clip bank, `clips.json`, `episodes.tsv` | Extend it. Re-running the search adds new episodes. It never re-mines what is done. |
| Anything that looks like a secret (`.env`, `*token*`, `*credential*`, `*.key`) | Note it and do not open it. The YouTube side needs no credentials. The mining step needs a model call, through whatever the agent already has. |

Report back in five lines: who the speaker is and what they are known for, which channels they host
themselves, whether a bank exists, what the brand rules ban, and what you could not find. Ask the
user to correct it.

### 0.2 Detect the environment and branch on it

```
python3 --version            # 3.10 or later, stdlib only for the scripts
yt-dlp --version             # the fetcher, keep it current: pip install -U yt-dlp
ffmpeg -version | head -1    # yt-dlp needs it to merge sections
```

| Missing | macOS | Linux | Windows |
|---|---|---|---|
| yt-dlp | `brew install yt-dlp` or `pip install yt-dlp` | `pip install yt-dlp` | `winget install yt-dlp` |
| ffmpeg | `brew install ffmpeg` | `sudo apt install ffmpeg` | `winget install Gyan.FFmpeg` |

**Branch on the runtime.**

- **Claude Code or Codex on a laptop.** The full path. The mining step runs as sub-agents of the
  agent you are in (one per batch of transcripts), so it costs whatever your plan charges for a
  small model. There is no separate API key.
- **A headless VPS.** The full path. YouTube rate-limits datacentre IPs harder. Keep the sleeps in
  the scripts and expect some NOSUB results to succeed on a retry.
- **A chat-only agent with no shell.** Stop at the mining brief. Write it, hand it over, and the
  user runs the scripts in a terminal.
- **A rights question.** Podcasts the speaker was a guest on belong to the host. Clipping for the
  speaker's own channels is common practice and often welcomed, and it is the user's call, not the
  agent's. Put the question in the report and do not download until it is answered.

### 0.3 Decide what "done" is

Write `BRIEF.md` with three lines. If the user cannot answer one, ask.

1. **Who, exactly.** Name, the companies they are known for, the channels they host, three things
   they talk about. This becomes the mining brief's first section.
2. **What counts as a clip.** Themes that matter to the user, and themes that do not. A relevance
   split (core to the user's business, or general) keeps the review page usable.
3. **Where the clips go.** A folder for a later edit is the default. This skill stops at raw
   sections with under a second of padding. A separate edit tightens and cleans them.

---

## 1. The steps

1. **Find every episode.** `scripts/search.sh` runs a set of YouTube searches for the speaker's
   name plus their companies, podcast, interview, and the themes, twice each (by relevance and by
   date), 40 results a search, flat, no downloads. Merge and dedupe into `inv/episodes.tsv`
   (speaker, id, duration, channel, title, source). Read the titles by eye and cut the obvious
   misses (a namesake, a news clip, a 30 second promo). Keep the ones where the speaker is the host
   of someone else's interview: they still talk.
2. **Pull the captions.** `scripts/pull_subs.sh <id>` fetches the auto-captions as json3 plus the
   upload metadata for one video, trying four player clients in turn. Loop it over the inventory
   with a pause. About 90 percent of episodes have captions. The rest are logged as NOSUB and are
   the only ones worth transcribing with Whisper, later, if the speaker is on them a lot.
3. **Transcripts a model can read.** `scripts/to_txt.py` turns each json3 into
   `transcripts/<id>.txt`: a header (title, who, channel, date, views, duration) then the words
   with a `[mm:ss]` stamp every 15 seconds of speech. No speaker labels exist in auto-captions.
   The mining brief handles that.
4. **The mining brief.** Copy `references/mining-brief.md`, fill the speaker section from
   `BRIEF.md`, and keep the rules: what counts as a clip, how to attribute a speaker with no
   labels (guest mode versus host mode), the JSON shape, and "never invent quotes". Save it in the
   workspace.
5. **Mine in batches.** Hand a sub-agent on the smallest model you have the brief plus 8 to 12
   transcripts and one output path, `mined/<batch>.json`. Run the batches in parallel. On the
   first run 17 batches over 147 transcripts produced 584 candidates. The model will paraphrase
   quotes and it will call guest speech "high confidence" on host-mode episodes. Both are why the
   next two steps exist.
6. **Verify every candidate.** `scripts/verify.py` reads every mined file, finds the candidate's
   quote in the caption words by trigram anchors (the first 14 tokens and the last 14), pins the
   exact start and end from the caption timings, rejects anything under 45 percent word coverage,
   under 8 seconds, over 170 seconds, or overlapping a better clip from the same episode by more
   than half. Writes `clips.json` (kept, ranked by score) and `rejected.json` (with reasons).
   Never match a quote exactly. The model cleaned it up. Anchors, not equality.
7. **The speaker check.** On host-mode episodes (the speaker's own channel, another person's name
   in the title) the model cannot reliably tell who is talking. `verify.py` marks those
   `host_mode`. Read them yourself, or hand the user a `speaker_check.md` of the hook lines and let
   them strike the ones that are the guest. On the first run 53 of 520 were the guest.
8. **Download the sections.** `scripts/cut.py` groups the kept clips by video and makes one
   yt-dlp call per video with every section, 1080p at most, keyframes forced at the cut points,
   under a second of padding each side, then files each as
   `clips/<speaker>/n###_<id>_<slug>.mp4`. Rerunnable, skips what exists. Order is by rank, so the
   best clips land first if the run is stopped. Read-only on YouTube.
9. **The review page.** `scripts/build_review.py` writes `review.html` (filters by speaker, theme,
   relevance, score. Each card is the clip, the hook, the quote, and a rail with the source link at
   the exact second) and `CLIPS.md`, the index. The user picks from the page.
10. **Hand-off.** The clip files, `clips.json` and `CLIPS.md`. Tightening the edges, captions,
    audio clean-up and a hook plate are an edit step with its own skill.

---

## 2. What to know before the first run

- **Timestamps in auto-captions are only good to about 15 seconds** at the line level. The verify
  step pins them to the word from the json3 events, which is why it exists and why the model is
  asked only for the stamp of the line a clip starts in.
- **YouTube is the bottleneck, not the model.** One video at a time, a few seconds between calls,
  four player clients in rotation. A burst of parallel downloads gets the IP throttled for an hour.
- **The model paraphrases.** Every quote is verified by anchors against the caption words. A
  candidate with no anchors and low coverage was invented, and it goes in `rejected.json`.
- **Host-mode episodes need a human.** The speaker's own channel with a guest in the title is where
  the model over-attributes. Budget the speaker check. It is ten minutes and it is the difference
  between a bank and a liability.
- **Disk.** Sections at 1080p run 5 to 25 MB each. 467 clips was about 6 GB on the first run. Check
  free space before `cut.py` and stop it when the user says they have enough. It resumes.
- **The first clips downloaded are the best ones**, because `cut.py` orders by rank. If the user
  wants to look before the whole bank lands, stop after the first fifty.

---

## 3. Files in this skill

- `scripts/search.sh`: the YouTube searches, flat, no downloads.
- `scripts/pull_subs.sh`: captions plus metadata for one id, four clients.
- `scripts/to_txt.py`: json3 to stamped transcripts with a header.
- `scripts/verify.py`: trigram anchors, exact timings, dedupe, ranking.
- `scripts/cut.py`: one yt-dlp call per video, every section, filed by rank.
- `scripts/build_review.py`: the review page and the index.
- `references/mining-brief.md`: the brief to hand each mining sub-agent, with the speaker section
  left as a template.
- `examples/episodes.tsv`, `examples/mined.json`: the shapes, with invented ids.

The scripts read `speakers.json` in the workspace (the speaker keys, their names, and the channels
they host). Lines marked `# ENV` change per machine.
