# 11 August 2026

Five packs of agent skills, given away on the AI in Action call, Tuesday 11 August 2026.

Root of the repo: [../README.md](../README.md). Licence: MIT, see [../LICENSE](../LICENSE).

Every one of these is a **skill file**: plain markdown your coding agent reads before it does the
work. Claude Code, Codex, OpenClaw, Hermes, whatever you run. There is nothing to install, no account
to make, and no service in the middle. Point your agent at a folder and tell it to follow the file.

That is deliberate. The tools churn every few months. Anything written as a file survives the churn.

## The packs

### `graph-engineering/`
The flagship. Two skills that build the thing everything else stands on.

- **`member-business-interview`** builds the brain. It interviews you about the business until it has
  your rules, your tools, your numbers, your people and the boundaries an agent may never cross, then
  writes that out as a set of files your agent reads first, every time.
- **`member-workflow-graph`** builds the hands. Point it at one job you already run every week. It
  interviews you on that job, watches you do it on screen and reads the real click path, researches
  the APIs and the auth in parallel lanes, runs a skeptic pass over its own findings, then hands back
  a working skill, a wiring checklist and the graph.

Start here. The other three packs assume a brain exists and get much better when it does.

### `workspace-audit/`
Point it at a working environment and it checks every claim your files make against the disk, then
classifies what it finds as poisoning, bloat, confusion or clash. Read-only: it never fixes anything
while auditing. You get a scorecard, three to five questions your agent would answer wrongly today
with each one traced to a finding, and a numbered fix list that waits for you to pick.

Run it monthly. A workspace decays quietly and the first symptom is a confident wrong answer.

### `funnel-builder/`
One offer in, a whole funnel out: the quiz, the scoring bands, the landing page, a result page per
band, the follow-up emails per band, and the organic content that feeds the top of it. It runs a long
interview, then a corpus pass over your own call recordings and reviews so the copy sounds like your
buyers rather than like a template, then the same graph-engineered research and skeptic pass before a
single page is written.

### `content-formats/`
Twelve production formats for carousels, statics and video, lifted out of a working content engine
and stripped of one company's brand. Layout law, prompts, quality gates and the build scripts. See
`content-formats/README.md` for what came out and how to put your own version back.

### `marketing-agents/`
Four agents for the top of the funnel, written up the same way.

- **`engagement-signal-leads`** finds people by what they just engaged with rather than by job title,
  gates them against your ideal customer, then waterfalls through enrichment providers.
- **`sending-infrastructure`** stands up the sending layer so a bad outbound week cannot touch the
  domain your invoices go out on. The boring pack. Skip it and the other three do not matter.
- **`reply-agent`** puts an agent on the reply side: classify, draft, book, and chase the "not now"
  in six months, all inside a lane you drew.
- **`content-from-calls`** turns conversations the business already has into published content across
  a whole team's accounts, with the performance data feeding the next round.

## How to use one

```
1. Clone this repo, or copy the folder you want into your own project.
2. Open your agent in that folder.
3. Tell it: read <skill file> and follow it.
```

The interview skills expect to talk to you for a while. That is the point of them. Answer with real
field names, real numbers and real thresholds, and you get something that runs. Answer vaguely and
you get a plan.

## Things that hold across all of them

- **A model call is for judgement.** If a step has a right answer a rule can produce, write the rule.
  Paying for inference to do arithmetic is the single most common way these builds get expensive.
- **Nothing irreversible without a person.** Every pack has an explicit approval boundary, and the
  default is narrower than you will want. Widen it after you have watched it for a fortnight.
- **The thing that writes the answer never grades it.** Every research pipeline in here runs a
  separate skeptic pass, and what it cannot resolve goes into a gaps list rather than getting waved
  through.
- **No secrets in tracked files, ever.** Keys live in a gitignored location the skills read from.
- **Plain English.** No em dashes, no "it's not X, it's Y", and a banned-words list in each file.

## Licence

MIT. Use them commercially, change them, ship them, sell what you build with them.
