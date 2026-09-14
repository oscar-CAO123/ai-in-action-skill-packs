# 15 September 2026

Three skills. Two are about footage that already exists. The first turns the video ads a business has
already run into new single-speaker cuts: the same person, the same words, re-ordered from the same
footage, a new hook plated over the old headline card, cut points that land between sentences.
The second mines every podcast and interview a person has appeared in on YouTube into a bank of
verified short-form soundbites, from the captions YouTube already made, so hours of audio are never
transcribed. The third is the one the call is built around: put a business's core documentation and
skill files in one repository, then let any agent (Grok Bot, Hermes, Claude Code, Codex, a voice
session) ingest it, build the skills natively, map the context and plan an orchestrator over
sub-agents. All three are reverse engineered from working builds with every company, client,
script and credential taken out.

| | On the call | Folder |
|---|---|---|
| 1 | The ad tape recut: transcribe, bank, recipe, sentence-safe cut, hook plate | [`01-ad-tape-recut`](01-ad-tape-recut/) |
| 2 | The soundbite miner: find every episode, pull the captions, mine, verify by anchors, download the sections | [`02-soundbite-miner`](02-soundbite-miner/) |
| 3 | The agent context transfer: one repository every agent reads, then ingest, build native skills, map, orchestrate | [`03-agent-context-transfer`](03-agent-context-transfer/) |

**Installed by the plugin** alongside the 1 and 8 September drops. Add the marketplace once and it
lands with the rest.

## What is in the ad tape recut

- `SKILL.md`: Phase 0 ground truth, the ten laws, the twelve steps, what the user dictates and how
  it maps, the cutter in one paragraph, the lessons.
- `scripts/`: `transcribe.py`, `words.py`, `analyse.py` (the words and the joins), `settings.py`
  (frames for the lighting map), `build_review.py` (the recipes as a review page), `cut.py` (the
  sentence-safe cutter), `cardbox.py`, `hook_plate.py`, `swap_audio.py`.
- `examples/`: `tape.json`, `bank.json`, `recipes.json`, `hooks.json`, the shapes with invented ids.
- `references/cut-points.md` and `references/hook-register.md`.

## What is in the soundbite miner

- `SKILL.md`: Phase 0, the ten steps, what to know before the first run.
- `scripts/`: `search.sh`, `pull_subs.sh`, `to_txt.py`, `verify.py`, `cut.py`, `build_review.py`.
- `references/mining-brief.md`: the brief each mining sub-agent gets, speaker section as a template.
- `examples/`: `speakers.json`, `episodes.tsv`, `mined.json`.

## What is in the agent context transfer

- `SKILL.md`: half one (build the repository from the brain folder, the laws), half two (the six
  phases an agent walks the first time it is pointed at the repository).
- `scripts/build_transfer.py`: the manifest-driven exporter with the secret stop and the phone
  and email redaction.
- `examples/transfer.json`: a filled manifest for a `context/`, `skills/`, `agent/` brain folder.
- `templates/INGEST.md`: the first file an agent reads in the repository; the exporter writes it.

## What is not here

The cuts and clips shown on the call were made from a company's own ads and its founders' own
podcast appearances. The films stay with the company. The method is here in full. Any speech
enhancer for a noisy room is your choice, after your own security review. None is bundled.
