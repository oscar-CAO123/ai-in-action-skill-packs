# 8 September 2026

Two skills. The first is the method behind the content animations shown on the call: an agent that
reads a line of script, storyboards it, writes the scene as code and renders it on your own machine.
The second is the whole machine those animations run inside: it runs the content interview from
last week's pack, writes a brain of your own avatars, pains, offers and formats out of your own
sales calls, stands up the engine and the workspace, and spins up the scheduled agents that keep
the queue full. Both are reverse engineered from working builds with every
company name, client, script and credential taken out, so they run on yours.

| | On the call | Folder |
|---|---|---|
| 1 | The Blender motion study: an agent reads a line of script, storyboards it, writes the scene as code and renders it on your CPU | [`01-blender-motion-study`](01-blender-motion-study/) |
| 2 | The content machine: the interview, the brain, the engine, the workspace and the three scheduled agents, in seven phases with a stop at every one | [`02-content-machine`](02-content-machine/) |

**Installed by the plugin** alongside the 1 September drop. Add the marketplace once and it lands
with the rest.

## What is in the Blender pack

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

## What is in the content machine pack

- `SKILL.md`, seven phases: the interview, the brain, the engine and outputs, the sources, the
  workspace, the schedule, and the rewrite that turns the pack into your own skill.
- `references/`, the interview question set, the brain spec, the seven-stage flywheel, the three
  scheduled agents, the workspace and the schema.
- `scripts/guarded.ts`, the write gate, the gap ledger, the budget meter and a model caller that
  reads `stop_reason`.
- `scripts/ingest_performance.ts`, a working agent. With no credentials and no database it stamps a
  gap per channel and writes nothing.
- `templates/schema.sql` with its reverse, and `templates/brain/`, the skeleton of every brain file.

It follows on from `07-content-operating-system` in the 1 September drop and runs that interview
itself, so it stands alone. Reverse engineered from a working build and fully de-identified: no
company, no client, no table prefix, no project id, no credential, and none of the house formats.
