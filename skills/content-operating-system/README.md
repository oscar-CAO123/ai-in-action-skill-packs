# The content operating system

Most content systems fail in the same place. Somebody sits down on a Sunday night, tries to think of
what to post, and thinks of the same four things they thought of last Sunday.

The system was never short of production capacity. It was short of **evidence**, and the person who
had the evidence was on calls all week and never wrote any of it down.

This pack builds the machine that fixes that, for your business, out of your own customer data.

## What it does

1. **Sweeps your workspace** for what your agent already knows, and for where customer evidence is
   sitting right now. Most operators have far more of it than they realise and none of it anywhere
   near their content.
2. **Interviews you for 60 to 90 minutes**, one question at a time, on positioning, brand truths,
   proof, channels and data reservoirs. Everything the sweep already answered comes off the list.
3. **Builds three directories:** `brain/` (the thinking), `engine/` (the code), `outputs/`
   (everything generated). The split is enforced, because instructions living with code is how a
   system becomes unmaintainable in six months.
4. **Wires your evidence sources** and installs **two scheduled tasks**: one that pulls evidence
   nightly, one that turns it into a ranked idea queue weekly.
5. **Generates a founder question bank**, 150 or so questions only you can answer well, each one
   traced to a real customer saying a real thing, refreshed every week.
6. **Runs the whole loop once, for real**, and puts a ranked queue on your screen before it stops.

## What you end up with

```
brain/
  SKILL.md              the router your agent reads before writing a word
  positioning.md        what you sell, to whom, against whom
  icp.md                the customer, in their own words, with sources cited
  brand-truths.md       what you actually believe, and what you will argue with
  language-rules.md     your words, your bans, your register
  source-register.md    every place your customers said something, and how to reach it
  doctrine.md           the craft laws, grounded in your business
  copywriting.md        how to actually write it
  formats/              one file per format you selected
  founder-questions.md  the standing bank. Open it, pick one, film it

engine/
  cos/                  sources, adapters, ingest, ideate, produce, gate
  config.json           your config. Never holds a secret, only variable names
  run-ingest.sh         cron 1
  run-ideate.sh         cron 2
  AGENT-IDEATE.md       how your system thinks. Edit this, not the Python

outputs/
  evidence/             the normalised store, redacted at ingestion
  queue/<date>/         queue.json and review.html, the page you actually read
  drafts/ finished/ archive/ logs/
```

## Running it

Open your agent in the folder where your business context lives, and tell it:

```
Read content-operating-system/SKILL.md and follow it.
```

Any agent with a shell and file access. Claude Code, Codex, Cursor, OpenClaw, Hermes, Gemini CLI.
Nothing here is tied to one of them. The schedules step detects which one is running and prefers its
native scheduler, falling back to launchd, cron or Task Scheduler.

Pause any time. State goes to `.cos-interview.json` after every phase and a fresh session resumes
from it.

## What you need

- **Python 3.9 or newer.** The engine is Python with one dependency, `requests`.
- **At least one real source of customer evidence.** Call transcripts, a helpdesk export, a shared
  inbox, or nothing but a public forum where your industry complains. Any one is enough to start.
- **Ideally, the business brain from `2026-08-11/graph-engineering/member-business-interview`.** This
  pack reads it and skips every question it already answered. Without it the interview runs longer.

## The four sources that ship with working pullers

| Source | Why it matters | Easiest route |
|---|---|---|
| **Calls** | The only place a customer speaks unprompted, at length, about a problem they pay to solve | Point your recorder's export at a folder. No token, no expiry |
| **Tickets** | Calls tell you why people buy. Tickets tell you what breaks the promise afterwards | A CSV export works today with zero credentials |
| **Forums** | Unfiltered, dated, and the only place people talk with nobody selling in the room | Reddit and Hacker News read without a key |
| **Reviews** | Pre-filtered for emotion, and competitor reviews are as useful as your own | A pasted file, an app store feed, or Google Places |

Everything else (CRM notes, community channels, own-channel performance, search demand, competitor
ads) gets mapped into the source register with a route and a status, and can graduate to a puller
later.

## The rules it holds to

**Nothing paid, published or sent without you.** The two scheduled jobs read and write local files.
That is their whole scope. Every paid call passes one guard that refuses without an approved batch id
and refuses again if your weekly cap would be exceeded.

**Redaction happens at ingestion, not at output.** Names, emails, phone numbers and company names are
stripped before a record is written, because everything in the store gets read back by a model
eventually. Role, industry, size band and stage survive, and those carry the meaning.

**A model call is for judgement.** Deduplication, recency windows, ranking arithmetic and file naming
are rules, so they are written as rules. The only model call in the scheduled path is the weekly
judgement pass, and it runs through the agent CLI you already pay for rather than a second API bill.

**Every idea carries its evidence.** An idea with an empty evidence rail never reaches the review
page. The system drops it rather than showing you a guess in a costume.

**Nothing gets rewritten in place.** Superseded work moves to `outputs/archive/` with the date, and
every brain file carries a changelog.

## The files in this pack

| File | What it is |
|---|---|
| `SKILL.md` | The entry point. Point your agent here |
| `reference/01-discovery.md` | The two sweeps: context, then evidence |
| `reference/02-interview.md` | The question script, ten phases, ~70 questions |
| `reference/03-source-register.md` | The reservoir taxonomy, and the privacy rules |
| `reference/04-founder-questions.md` | The nine vectors and how the bank refreshes |
| `reference/05-doctrine.md` | The craft laws, universal, personalised at build |
| `reference/06-copywriting.md` | Hooks, structure, sentence craft, the bans |
| `reference/07-format-library.md` | Fourteen format archetypes with specs |
| `reference/08-connections.md` | Per-platform credential setup, read scopes only |
| `reference/09-schedules.md` | Installing the two tasks, and what breaks them |
| `reference/10-build.md` | The build sequence and what counts as finished |
| `templates/brain/` | The brain scaffolds the interview fills |
| `templates/engine/` | Working Python. Copied in, then configured |

## Honest limits

- **The queue is only as good as the evidence.** If your calls are not recorded, the first month
  leans on public forums and your own beliefs, and it shows. Recording sales calls is the highest
  return change most operators can make this week, and it costs nothing.
- **The rule-based fallback is thin.** With no agent CLI reachable, ideation still ranks and still
  writes the page, but it hands you themes rather than written ideas, and it says so on the page.
- **Redaction over-redacts.** It will occasionally eat a product name that looks like a person. That
  is the intended direction of the error, and the dry run shows you exactly what it removed.
- **Nothing here posts anything.** Publishing access is a separate decision on a separate day.
