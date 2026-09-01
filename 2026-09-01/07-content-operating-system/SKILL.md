---
name: content-operating-system
description: >
  Run by an operator in any agent with shell and file access (Claude Code, Codex, Cursor, OpenClaw,
  Hermes, Gemini CLI). Sweeps the workspace for what the agent already knows, finds where the
  business keeps its customer evidence, then runs a 60 to 90 minute interview covering positioning,
  brand truths, channels and data reservoirs. Ends by building a working content operating system:
  a brain, an engine, an outputs tree, a founder question bank, and two scheduled tasks that pull
  evidence and turn it into a ranked idea queue every week without being asked.
purpose: Build a founder-led content operating system from the operator's own evidence.
version: 1.0
---

# The content operating system

Most content systems fail in the same place. Somebody sits down on a Sunday night, tries to think of
what to post, and thinks of the same four things they thought of last Sunday. The system was never
short of production capacity. It was short of **evidence**, and the person who had the evidence was
on calls all week and never wrote any of it down.

This skill builds the machine that fixes that. Three parts, in this order:

1. **Ingestion.** Where the business already keeps proof of what customers actually say, and a
   scheduled job that pulls it into one normalised store on its own.
2. **Ideation.** A second scheduled job that reads the store, finds what changed, and hands over a
   ranked idea queue with the evidence attached to each idea.
3. **Production.** An engine that takes an approved idea through to a finished asset, gated so
   nothing is paid for or published without a person.

It also builds the thing most founders actually get stuck on: **a standing bank of questions worth
answering on camera**, drawn from their own customers, their own beliefs and their own industry, and
refreshed every week by the ideation run.

## Run this in a CLI agent

Any agent with a shell and file access. Claude Code, Codex, Cursor's terminal, OpenClaw, Hermes,
Gemini CLI. Nothing here is tied to one of them, and the schedules step detects which one is running
and uses its native scheduler.

A web chat window will get you through the interview and the brain, and then stall, because it cannot
write files or install a scheduled task. Use a CLI.

## How to start

Open your agent in the folder where your business context lives, and tell it:

```
Read content-operating-system/SKILL.md and follow it.
```

The agent works through the phases below in order. Pause any time. State is written to
`.cos-interview.json` after every phase, so a fresh session resumes by reading that file.

## What you need before you start

- **The business brain from `member-business-interview`, if you have it.** This skill reads it and
  skips every question it already answers. Without it, expect the interview to run longer and cover
  ground that pack covers better.
- **Python 3.9 or newer.** `python3 --version`. The engine templates are Python with a small
  dependency list.
- **At least one real source of customer evidence.** Call recordings with transcripts, a helpdesk
  export, a shared inbox, or nothing but a forum where your industry complains in public. Any one of
  those is enough to start.

---

## ROLE FOR THE AGENT (read first, obey throughout)

You are running a discovery and build session for an operator who wants their content to come out of
their own customer evidence instead of out of their head on a Sunday night.

Your job has five parts, in order, and you do not skip forward:

1. Sweep the workspace and report what you found, then let them correct it.
2. Interview them, one question at a time, on what the files could not tell you.
3. Build their brain from the answers.
4. Install the engine, wire the sources they named, and install two scheduled tasks.
5. Run ingestion once for real, run ideation once for real, and put a ranked queue on screen.

### Hard rules

- **One question at a time.** Never stack two questions in one message. If you catch yourself writing
  "and also", split it into the next question.
- **Push for specifics.** "A few" and "sometimes" are not answers. Ask for the number, the most
  recent example, the actual words the customer used. A brain built on generalities produces content
  built on generalities.
- **Everything discovery already answered comes off the list.** Re-asking something their own files
  told you burns the goodwill you need for the questions that matter.
- **Never invent a specific.** If you do not know their pricing, their customer count, a URL or a
  field name, ask. A guessed number ends up in a script and then in front of their market.
- **Save state after every phase.** Write `.cos-interview.json` with every answer collected so far,
  grouped by phase. A dropped session resumes from that file.
- **Never open anything that looks like a secret.** `.env`, `*token*`, `*credential*`, `*oauth*`,
  `*.pem`, `*.key`. Note that the file exists and where it lives, then move on.
- **Nothing paid, published or sent without a person.** See the approval boundary below. This holds
  even when the task would obviously be better if you just did it.
- **Never use em dashes.** Use a comma, a period, a colon, or parentheses.
- **Never write "it is not X, it is Y".** Say the positive thing directly.
- **Run the language gate before you write any file.** Below.

### The language gate

Nothing you write into a file or into chat may contain any of these.

**Banned words and phrases:** leverage, leveraging, seamless, seamlessly, navigate, navigating,
empower, empowering, unlock, unlocking, harness, harnessing, game-changing, game-changer,
revolutionary, revolutionise, cutting-edge, transformative, transform in the marketing sense, robust,
synergy, ecosystem unless it is literally Apple's or Google's, supercharge, next-generation, next-gen,
paradigm shift, "the future of anything", "this changes everything", level up, delve, tapestry,
testament, "in today's fast-paced".

**Banned AI clichés:** "in the age of AI", "as AI continues to", "with the rise of AI", "AI-powered"
where you could say what it does instead, "the AI revolution".

**Banned hype:** huge, massive, incredible, amazing, unbelievable, must-read, must-have, must-try,
"the only way", "the best way", "you won't believe".

**Positives to mirror:** plain English, one idea per sentence, active voice, present tense, no
softeners, specifics over abstractions, names and numbers and tool names.

Scan every file payload before you write it. If a banned token appears, rewrite, then scan again.

### The approval boundary

Written into the built system's config, and enforced by the engine, not by your good intentions.

| Action | Who decides |
|---|---|
| Reading and pulling evidence from a configured source | The scheduled job, unattended |
| Clustering, ranking, writing the idea queue and refreshing the question bank | The scheduled job, unattended |
| Any paid generation (image, video, voice, a metered API) | The operator, per batch |
| Any post, send, publish or schedule to a live channel | The operator, per asset |
| Any write to a system of record (CRM, helpdesk, database) | The operator, per write |
| Installing or changing a scheduled task | The operator, once, at install |

Widen it after they have watched it run for a fortnight. Start here.

---

## The phases

Work through these in order. Each one has a reference file with the detail. Read the reference file
at the start of its phase, not before.

| Phase | What happens | Reference |
|---|---|---|
| **0** | Sweep the workspace and the machine for context and evidence | `reference/01-discovery.md` |
| **1** | Report the sweep in five lines, take their corrections | `reference/01-discovery.md` |
| **2** | The interview, one question at a time | `reference/02-interview.md` |
| **3** | Build the source register from what they named | `reference/03-source-register.md` |
| **4** | Set up the connections that need credentials | `reference/08-connections.md` |
| **5** | Write the brain | `reference/10-build.md`, `reference/05-doctrine.md`, `reference/06-copywriting.md` |
| **6** | Generate the founder question bank | `reference/04-founder-questions.md` |
| **7** | Install the engine and wire the sources | `reference/10-build.md` |
| **8** | Install the two scheduled tasks | `reference/09-schedules.md` |
| **9** | Run ingestion for real, run ideation for real, open the review page | `reference/10-build.md` |

Do not start phase 5 until the interview is complete and the operator has typed `READY TO BUILD`. If
they try to jump ahead, tell them which phase they are in and ask the next question.

---

## What gets built

Three directories, at the root of wherever they opened you, unless discovery found a convention they
already use and you should match it instead.

```
brain/            instructions only, no code, no media
  SKILL.md            the router their agent reads before writing anything
  positioning.md      what the business sells, to whom, and what it is competing against
  icp.md              the customer, in their own words, with the evidence cited
  brand-truths.md     what this founder actually believes, and what they will argue with
  language-rules.md   their words, their bans, their register
  founder-questions.md the standing question bank
  formats/            one file per format they selected, with the rules for writing it
  doctrine.md         the craft laws, personalised to their business

engine/           all the code, none of the thinking
  cos/                the package: sources, adapters, ingest, ideate, produce, gate
  config.json         their config: sources, channels, formats, providers, caps
  run-ingest.sh       the ingestion entrypoint the scheduler calls
  run-ideate.sh       the ideation entrypoint the scheduler calls
  requirements.txt

outputs/          everything generated, nothing instructional
  evidence/           the normalised store the ingestion job writes to
  queue/              the dated idea queues and review pages
  drafts/             work in progress
  finished/           shipped assets
  archive/            everything superseded
```

The split is the point. **Instructions never live with code, and neither ever lives with media.** A
brain file that carries a script, or an engine file that carries a rule about hooks, is the start of
a system nobody can update six months later.

---

## Rules that hold across the whole build

**A model call is for judgement.** If a step has a right answer a rule can produce, write the rule.
Deduplication, recency windows, word counts, file naming and cost arithmetic are all rules. Paying
for inference to do arithmetic is the most common way these systems get expensive.

**Evidence beats opinion, and every idea carries its evidence.** An idea in the queue with no source
line attached is a guess wearing a costume. The ranking cares about how many independent sources said
the same thing, how recently, and how much money sat behind the person saying it.

**The founder is the format.** This is founder-led content. The engine's job is to hand a person a
question worth answering and a reason it is worth answering this week. Everything else is production.

**Nothing gets rewritten in place.** Superseded work moves to `outputs/archive/` with the date. The
brain keeps a changelog at the bottom of each file.

**One home for secrets.** Whatever discovery found. If they have no convention, create a gitignored
`.env` at the project root and confirm with `git check-ignore .env` before anything is committed.
Never paste a key into a tracked file, a config file, or a script.

---

## If they already have some of this

Common, and it changes the job. Read what exists before you propose replacing it.

- **They have a business brain from `member-business-interview`.** Read it in full. Every question it
  answered comes off the interview. Your brain files link to theirs rather than duplicating.
- **They have content already running.** Do not rebuild it. Point the ingestion at what they have,
  and make the first ideation run explain what their existing content is missing.
- **They have a CRM or a helpdesk with an API.** That is the best reservoir in the building. Wire it
  first, before anything public.
- **They have nothing but a website and a personal opinion.** Say so plainly. Run the interview
  longer, lean the question bank on brand truths and industry, wire the public sources, and set the
  expectation that the queue gets sharper once real calls start landing in it.

## When you are done

The operator should have, on screen, a ranked idea queue built from evidence that came out of their
own business, with the founder questions attached, and two scheduled tasks that will do it again next
week without being asked.

If you cannot get that far, say which phase you stopped at and why, and write the state file. Do not
report a system as running when the first real ingestion has not happened.
