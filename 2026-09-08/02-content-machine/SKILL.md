---
name: content-machine
description: >
  The full content pipeline, built for one business, in seven phases with a stop at every one.
  Runs the content interview, writes a brain of that business's own avatars, pains, offers,
  formats and laws, stands up the engine and outputs folders, wires the external references and
  the internal call recordings that feed it, builds the workspace where work is decided, and
  spins up the scheduled agents (crons in Hermes or OpenClaw, scheduled tasks in Claude Code or
  Codex) that keep the queue full. Ends by rewriting itself around the brain it just wrote, so
  the skill they run next week is theirs.
purpose: Turn an interview into a running content machine with its own brain and its own schedule.
version: 1.0
---

# The content machine

Last week's pack ran an interview and left a business with a brain and two scheduled tasks. This
one is the whole machine, and it runs that interview itself as its first phase, so it stands alone.

At the end the business has four things it did not have before:

1. **A brain.** Its avatars, its pains, its offers, its formats, its hooks and its laws, written
   down in files, in its own words, from its own calls.
2. **An engine and an outputs tree.** The place work is produced and the place it lands, separated
   on purpose, so knowledge and media never live in the same folder.
3. **A workspace.** One table and one board where a piece moves from idea to published, filed by
   the batch that proposed it.
4. **A schedule.** Agents that read the outside world, read the business's own results and its own
   calls, and write next week's ranked ideas into stage one while nobody is watching.

## The cadence it leaves behind

Seven stages, running weekly, each feeding the next, the last feeding the first.

```
  1 internal read  ->  2 external read  ->  3 ideation  ->  4 authoring
        ^                                                        |
        |                                                        v
  7 publishing  <-  6 post-production  <-  5 production  <--------+
```

| Stage | What happens | Who does it |
|---|---|---|
| 1 | **Internal read.** Own channels, own call recordings, own past work, ranked. | agent, scheduled |
| 2 | **External read.** The reference profiles and sources they named, scored by engagement. | agent, scheduled |
| 3 | **Ideation.** Both reads become formulas: `avatar x pain x format`, ranked, gated. | agent, scheduled |
| 4 | **Authoring.** An approved formula becomes a skeleton, then filled copy. | the director, with the agent |
| 5 | **Production.** The authored batch becomes assets through the engine. | the agent, gated before spend |
| 6 | **Post-production.** Human review, the cover, the quality gate. | the director |
| 7 | **Publishing.** Scheduled, published, the post URL pasted back on the row. | the director |

Stage 7 hands the post URL to stage 1, which is the whole point: what published last month decides
what gets proposed next week.

**Nothing in stages 3 to 7 happens without a person.** The agent proposes. The director approves,
authors and publishes.

## Run this in a CLI agent

Claude Code, Codex, Cursor's terminal, OpenClaw, Hermes, Gemini CLI. Open it in the folder where
the business's context lives and say:

```
Read content-machine/SKILL.md and follow it.
```

A web chat window gets through phase 1 and then stalls, because it cannot write files or install a
schedule.

## The phase gate

**Every phase ends with a stop.** The agent shows what it built, says what the next phase will do
and what it will touch, and waits. State is written to `.machine-build.json` after each phase, so a
fresh session resumes by reading that file and nothing else.

This is not ceremony. Phase 4 reads call recordings, phase 6 installs something that runs on its
own, and both are things a person should look at before they happen.

---

## Phase 1, the interview

The full content interview, 60 to 90 minutes, in one sitting or four. If last week's
`content-operating-system` pack was already run, the agent reads its `.cos-interview.json` and asks
only what it does not already answer.

`references/interview.md` carries the whole question set. Six blocks:

1. **The business.** What is sold, to whom, at what price, and what happens after they buy.
2. **The offers.** Every offer, its promise, its proof and its objection. An offer with no proof is
   recorded as such, because it decides what content can honestly claim.
3. **The avatars.** Who buys, in their language, not in demographics. Job, situation, what their
   week looks like, what they have already tried.
4. **The pains.** What those people actually say is wrong, in their own words, with figures where
   they said figures.
5. **The channels and the references.** Where they publish, what is measured on each, and the
   accounts and sources whose work they want the machine reading.
6. **The reservoirs.** Where evidence already exists: call recordings, transcripts, support
   tickets, reviews, the CRM, the inbox.

The output of this phase is answers on disk. No files are generated yet.

**Stop. Show the answers. Ask what is wrong before writing a brain on top of them.**

---

## Phase 2, the brain

The interview becomes files. `references/brain.md` has the full spec and `templates/brain/` has the
skeletons.

```
brain/
  SKILL.md          the entry point, rewritten in phase 7
  avatars.md        one block per avatar, with its code
  pains.md          one page per pain theme, with the verbatims and the figures
  offers.md         each offer, its promise, its proof, its objection
  formats.md        the formats this business publishes in, each with an id
  hooks.md          hook structures, cited, never filled lines
  laws.md           the rules copy obeys here: banned words, claims, tone
  language.md       the words this business uses and the words it never uses
```

Three rules that decide whether this brain stays useful:

- **A pain page carries verbatims.** The sentence a customer actually said, with the figure they
  said, attributed to the call it came from. Paraphrase rots into marketing copy within a month.
- **Every entry has a code.** `CLINIC`, `NOSHOWS`, `SHORT-VIDEO`. Codes are how a formula, a row
  in the database and a person in a meeting all name the same thing.
- **Instruction only.** No media, no generated assets, no drafts in this folder, ever. The brain is
  what the machine knows, and outputs are what it made.

**Stop. The director reads the brain and corrects it. This one hour decides the quality of every
idea the machine ever proposes.**

---

## Phase 3, the engine and the outputs

Three folders, separated on purpose:

```
brain/     instruction only. What the machine knows.
engine/    code only. The pipeline, the per-format rigs, the gates.
outputs/   media only. drafts/ backlog/ finished/ archive/
```

The engine gets the parts that do not depend on the format:

- **The pipeline**, which walks an approved formula to a finished asset.
- **A rig per format**, one folder each, holding that format's build script and its own rules.
- **The gates.** A copy gate (the banned words, the claim rules, the tone laws from `brain/laws.md`)
  and a batch gate that has to exit zero before a batch is called done. A gate that only warns gets
  ignored by week three, so the copy gate fails the batch.

The skill scaffolds the pipeline, one worked rig and both gates. It does not invent formats: the
formats come from the interview, and each one gets its own rig folder as the business builds it.

**Stop. Run the gates against three pieces of the business's existing content. If nothing fails,
the gates are too loose.**

---

## Phase 4, the sources

Where the machine's evidence comes from. Two halves, and the internal half is the one that matters.

**External references.** The accounts, subreddits, channels, repositories and publications named in
the interview. Each becomes a source entry with its handle, why it is being read, and whether it is
read for format, for angle or for both. Scored by engagement, never by taste. A reference supplies
structure and never language: quote it to make the shape legible, then the line comes from
`brain/hooks.md`.

**Internal evidence, which is where the ideas actually come from.** Sales calls, discovery calls,
onboarding calls, support conversations, reviews. This is the reservoir most businesses are sitting
on and never read. The wiring:

1. Point the machine at where recordings or transcripts already land.
2. A weekly job pulls the new ones and extracts, per call, only what content needs: the pains named,
   the words used, the figures quoted, the objections raised.
3. Those land as pain pages and verbatims in the brain, dated, attributed to the call.
4. The ideation stage reads them ahead of anything external, because a business's own calls
   outrank the internet on what its buyers have.

**Three rules on the internal half, and they are not negotiable:**

- **Consent and law first.** Recording and reading calls is governed where the business operates.
  The agent asks whether recordings are consented, and does nothing until that is answered.
- **Extract, never store.** What lands in the brain is the pain, the phrasing and the figure.
  Names, contact details and account identifiers stay out.
- **Untrusted text goes in a scrubbed process.** Anything scraped or transcribed that a model then
  reads runs in a child process holding the model key and nothing else, returning a fixed schema
  that is validated field by field.

**Stop. Show the sources and the first extraction from a single call, and let the director read it
before the job is scheduled.**

---

## Phase 5, the workspace

One table and one board, so the machine has somewhere to write and a person has somewhere to
decide. `references/schema.md` and `references/workspace.md` carry the detail, and `templates/schema.sql`
is the additive schema with its reverse.

The shape:

- **Five stages** as plain text: `ideas`, `ready_to_produce`, `produced`, `scheduled`, `published`.
- **Batches.** Every idea from one run shares a `batch_id`, and the board files cards under it.
  One card per piece becomes an unusable wall within three weeks.
- **The full window** where a piece is worked: the copy, the hook, the shot list, the references,
  the performance snapshots, the stage.
- **Concepts**, one ranked podium of formulas by how their pieces actually performed. A hand-set
  rank is stored as a performance snapshot marked `manual`, so a human judgement and a measured
  result travel the same code path.

If the business has no database, the same five stages work in the tool it already uses. The stages,
the batch and the codes are what matter, and the storage is negotiable.

**Stop. A person moves one real piece from idea to published before anything is scheduled.**

---

## Phase 6, the schedule

Now the machine runs itself. Three agents, weekly, staggered by an hour:

| Agent | Reads | Writes |
|---|---|---|
| internal read | own channels over two windows, plus the week's new call transcripts | a performance snapshot per channel per window, plus new verbatims into the brain |
| external read | the reference profiles and sources from phase 4 | rows in a market table |
| ideation | every coded row with a snapshot, plus the market table and the brain | one batch of ranked formulas as `ideas` rows |

**The skill detects the runtime and uses its native scheduler.**

| Runtime | What it installs |
|---|---|
| Hermes, OpenClaw | a cron entry per agent, on the runtime's own scheduler |
| Claude Code | a scheduled task per agent |
| Codex | a scheduled task per agent |
| a server, a container, CI | a crontab line or a scheduled workflow |

`references/schedules.md` carries the three agents in full: the matching rules, the ranking rules,
the gaps, the budget and the checkpoints. `scripts/ingest_performance.ts` is a working one to copy.

### The gate, which is the part not to skip

Every write and every send in every agent goes through one function sitting directly above `fetch`:

```ts
if (process.env.ALLOW_PROD_WRITES !== "1") {
  console.log(`  WOULD ${what}`);   // the payload lands in the run directory
  return null;
}
```

- **One function, not a boolean read in four places.** A flag guarding the code you remember
  writing has no reach into a helper somebody else imported, and alerting helpers are the usual way
  a dry run writes a real row into production.
- **A local run passes only the variables that run needs.** Sourcing a whole environment file into
  a test is the other way it happens.
- **Writes are armed one agent at a time**, on a person's word, after that agent has run once with
  writes off and its log has been read.

**Stop. Nothing is armed in this phase. The schedules exist, writes are off.**

---

## Phase 7, the rewrite

The skill rewrites itself around the brain it just built.

- `brain/SKILL.md` becomes the business's own entry point: its avatars, its pains, its offers, its
  formats, its laws, its channels and its sources, with the generic examples gone.
- The seven-stage cadence at the top of this file is rewritten with their stage names, their
  schedule and their runtime.
- This pack's `SKILL.md` is left in place, unchanged, as the record of how the machine was built.

Two files, two jobs: the pack explains the build, the brain runs the business.

**Stop. The director reads their own SKILL.md. If it reads like a generic marketing document,
phase 2 was too thin and the fix is in the brain, never in the prompt.**

---

## The first month

1. Every agent runs on its schedule with writes off. Read every log.
2. Arm the internal read first: it writes one column onto rows that already exist, which is the
   smallest blast radius of the three.
3. A week later, arm the external read.
4. A week later, arm ideation, the one that creates rows.
5. Watch the first batch land in the workspace and judge the ideas against the brain, not against
   whether the job exited zero.

A run that proposes something the director would not have thought of is working. A run that
proposes what they already had is telling them the brain is thin, and that is a phase 2 problem.

## Files in this pack

- `references/interview.md`, the full question set, six blocks.
- `references/brain.md`, what each brain file holds and how it is coded.
- `references/flywheel.md`, the seven stages in full: what each reads, writes and gates.
- `references/schedules.md`, the three scheduled agents, the runtimes, matching, ranking, budget.
- `references/workspace.md`, the board, the batch rule, the editor window.
- `references/schema.md`, the columns, the indexes, the additive discipline.
- `scripts/guarded.ts`, the write gate, the gap ledger, the budget meter, the model caller.
- `scripts/ingest_performance.ts`, a working agent that runs with no credentials and writes nothing.
- `templates/schema.sql` and `templates/001-REVERSE.md`, the schema and its reverse.
- `templates/brain/`, the skeleton of every brain file.
