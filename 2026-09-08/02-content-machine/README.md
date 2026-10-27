# The content machine

The whole pipeline for one business, built in seven phases with a stop at every one.

It runs the content interview from last week's pack itself, so it stands alone. If that pack was
already run it reads those answers and asks only what is missing.

## What the business has at the end

- **A brain**: its avatars, pains, offers, formats, hooks and laws, in files, in its own words,
  grown weekly from its own calls.
- **An engine and an outputs tree**, separated on purpose, so what the machine knows never shares a
  folder with what it made.
- **A workspace**: five stages, batches, and a board where a piece moves from idea to published.
- **A schedule**: three agents reading the outside world, its own results and its own calls, and
  writing next week's ranked ideas into stage one while nobody is watching.
- **Its own skill**, rewritten around that brain in the last phase.

## The cadence it leaves behind

```
  1 internal read  ->  2 external read  ->  3 ideation  ->  4 authoring
        ^                                                        |
        |                                                        v
  7 publishing  <-  6 post-production  <-  5 production  <--------+
```

Stages 1 to 3 are scheduled. Stages 4 to 7 are a person's. Stage 7 hands the post URL back to
stage 1, which is what makes it a loop rather than a list.

| File | What it is |
|---|---|
| `SKILL.md` | the seven phases, each with its stop |
| `references/interview.md` | the full question set, six blocks |
| `references/brain.md` | what each brain file holds, and why everything carries a code |
| `references/flywheel.md` | the seven stages: what each reads, writes and gates |
| `references/schedules.md` | the three agents, the runtimes, matching, ranking, budget, gaps |
| `references/workspace.md` | the board, the batch rule, the editor window |
| `references/schema.md` | the columns, the indexes, the additive discipline |
| `scripts/guarded.ts` | the write gate, the gap ledger, the budget meter, the model caller |
| `scripts/ingest_performance.ts` | a working agent, runnable with no credentials |
| `templates/schema.sql`, `templates/001-REVERSE.md` | the schema and its reverse |
| `templates/brain/` | the skeleton of every brain file |

## Try the agent in thirty seconds

```
cd scripts
env -i PATH="$PATH" HOME="$HOME" npx tsx ingest_performance.ts
```

With no credentials and no database it reads nothing, stamps a gap per channel, writes nothing and
leaves a summary on disk. That is the contract: **a run on your laptop can never touch production.**
Writes need `ALLOW_PROD_WRITES=1`, set on one deployed agent at a time, after its log has been read.

## The two rules worth taking even if you build none of this

**Every write in a scheduled job goes through one function that sits directly above `fetch`.** A
flag you check in the code you remember writing has no reach into a helper somebody else imported.

**The ideas come from your own calls.** Everything else in this pack is plumbing around that one
fact. A business sitting on a year of recorded discovery calls already has next quarter's content
and has never read it back.

This is reverse engineered from a working build. Every company name, client, table prefix, project
id, credential and house format has been taken out.
