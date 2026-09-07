# 8 September 2026

The call was built around GPT-6 Astra three ways: the website rebuild, the Knowledge Hub build and
content animations. This drop is the skill behind the content animations, with every company name,
client and script taken out so it runs on yours. A second skill, from the Knowledge Hub Gauntlet run
in Astra, lands in this folder after that run finishes.

| | On the call | Folder |
|---|---|---|
| 1 | The Blender motion study: an agent reads a line of script, storyboards it, writes the scene as code and renders it on your CPU | [`01-blender-motion-study`](01-blender-motion-study/) |
| 2 | The Knowledge Hub Gauntlet run in Astra | coming after the run |

**Installed by the plugin** alongside the 1 September drop. Add the marketplace once and it lands
with the rest.

## What is in the pack

- `SKILL.md`, the doctrine: Phase 0 ground truth, the narrow style, the semantic storyboard, the two
  motion lanes, the banlist, the run protocol, what one laptop measured, and the five second brief to
  hand your agent first.
- `references/`, the long version of each lane.
- `scripts/render.py` and `scripts/bpy_scene.py`, a JSON scene contract for stills and simple moves.
- `scripts/monitor_render.py`, the low-priority CPU render wrapper that stops the job on heat,
  memory or time.
- `scripts/motion_study_example.py`, the worked five second study, the one shown on the call.
- `examples/white-on-black.json`, a two second hold with one weighted arrival to prove the path.

## What is not here

The narrated film and the five second study shown on the call were made with this skill and a
company's own script, voice and brand. The films stay with the company. The method is here in full.

The website rebuild and the Knowledge Hub build carry a company's routes, client names and locked
design system. Their prompts are not in this drop.
