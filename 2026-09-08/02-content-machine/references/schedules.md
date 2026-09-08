# The three scheduled agents

Stages 1 to 3 of `flywheel.md`, running on their own. One schedule, three agents, one table. Each
runs weekly, each writes a run directory, and each can be run by hand with writes off to print
exactly what it would have done.

## Agent 1, the internal read

**What it answers:** what did your own published work actually do, on every channel, this week and
this month.

**Reads.** Every row at `published`, not archived, that carries either an `asset_code` or a pasted
platform URL, plus the week's new call transcripts from the reservoirs wired in phase 4. Then each
channel in turn, over two windows ending yesterday: the last 7 days and the last 28 days. Two
windows, because a piece can win the week and lose the month, and both facts are worth having.

**Matching.** This is the part that decides whether any of the rest is true.

- **Paid.** The ad name carries the row's `asset_code` verbatim. Mint the code when a piece reaches
  produced, lock it after, and put it in the ad name when the ad is built.
- **Organic.** The person who published pastes the post URL onto the row. The agent reduces both
  that URL and the platform's permalink to the same id and compares those.

Log the number of platform assets read and the number matched, every run, per channel per window.
A matched count that drops to zero is the alarm that something upstream changed.

**Ranking.** Rank every asset the platform reported, in that channel, in that window, on that
channel's own metric. Rank 1 means best on the channel. Comparing a video view against a link click
across channels produces a number that means nothing, so it is never computed.

**The call read, in the same run.** New transcripts since the last run are read for one thing
only: the pains named, the phrasing used, the figures quoted and the objections raised. Those land
as verbatims on the matching pain page in `brain/pains.md`, dated and attributed to the call. Names,
contact details and account identifiers never leave the transcript. A week with no calls stamps a
gap.

**Writes.** One patch per row, onto the `performance` array, merging by channel plus window so a
re-run corrects rather than duplicates. Capped at the last 48 snapshots. That column is the only
thing this agent writes: it never creates a row, never moves a stage, never touches another
table.

## Agent 2, the external read

**What it answers:** what is happening outside this business that a piece should be about.

**Reads.** The reference profiles and sources named in the interview and written into
`brain/`: forums, repositories, video platforms, news aggregators, the accounts this audience
already watches. Free sources first, and a source with no credential stamps a gap.

**The model pass is isolated.** Scraped text goes to a model to be scored, and scraped text is
input from strangers. Run that pass in a child process that holds the model key and nothing else,
have it return a fixed schema, and validate the reply field by field before anything is stored.
A model that reads untrusted text and holds your database credential is a bad afternoon waiting.

**Writes.** Rows in a separate market table, never in the content table. Deduplicate on the source
URL.

## Agent 3, ideation

**What it answers:** given all of that, what should you make next week.

**Reads.** Every coded row that carries a performance snapshot, plus the market table.

**The formula.** One idea is `avatar x pain x format`, plus the surface it runs on and the
class of asset it is. It carries the evidence that produced it: which winners it drew from, which
variables it holds fixed and which it varies.

**Which variable to hold.** When a piece won, the honest read is that one of its variables carried
it. Hold that one, vary the others, and say so on the idea. When the evidence is flat, hold the
pain first and the avatar second, and never hold the packaging, because packaging is the
cheapest thing to change and the least likely to be the cause.

**The mix.** Roughly sixty percent of a batch extends what has proven itself and forty percent is
new ground. Both numbers move with how much proof you actually have. With no proof at all the run
is a cold start: a fixed small set of new formulas, written down as new, so nobody later mistakes
a guess for a finding.

**The gate.** Validate every formula against your written vocabulary before it lands: known
avatar, known pain, known format, a code that resolves, no empty fields. A formula that fails
the gate is logged with the reason and dropped from the batch.

**Writes.** One batch row, then the idea rows, all carrying the same `batch_id`, all at stage
`ideas`, each with its evidence attached. Then a summary of the run.

## What every agent shares

**The run directory.** A timestamped folder per run holding the prompts, the checkpoints, the
would-write payloads and a `summary.json`. When somebody asks why the machine suggested something,
this is the answer.

**Gaps.** A missing credential, an empty channel, a source that returned nothing: stamped on the
run, printed, carried in the summary, never fatal.

**Checkpoints.** JSON per stage. A run that dies in stage three resumes at stage three with
`--resume <run_id>`. A run you want to study replays a fresh agent's answers by label.

**The budget.** Estimate the cost of a model call and reserve it before the request. Throw with a
resume instruction rather than starting a call the run cannot afford.

**Reading a model reply.** Join the blocks whose `type` is `text`, and read `stop_reason` on every
reply. A reasoning model can return a thinking block first, which makes `content[0].text` empty and
produces a parser error that reads like malformed JSON. Log `stop_reason` and `output_tokens` on
every call so the log can tell a truncation from a refusal from an empty block.

**Every write through the gate.** See phase 6 in `SKILL.md`.

## Scheduling, and the runtime you are in

Weekly, staggered by an hour, on the quietest morning of your week. Stagger them because the third
agent reads what the first two wrote, and an hour is cheap insurance against a slow run.

Schedule in UTC and write the local time in a comment. Twice a year one of them will move, and the
comment is how you notice.

**Use the native scheduler of whatever you are running in.** There is no wrapper worth writing
here, and a wrapper is one more thing that can be the reason a run did not happen.

| Runtime | What to install |
|---|---|
| Hermes, OpenClaw | one cron entry per agent on the runtime's own scheduler |
| Claude Code | one scheduled task per agent |
| Codex | one scheduled task per agent |
| a server or container you own | a crontab line per agent |
| CI (a scheduled workflow) | one scheduled job per agent, with the secrets on the job |

Whichever it is, the agent's command is the same: the script, with `ALLOW_PROD_WRITES` off until
that agent has run once and its log has been read.

## Arming order

1. Deploy all three with writes off. Every credential name declared, empty where you do not have
   it yet.
2. Let the schedule fire once. Read every log.
3. Arm the internal read. It writes one column onto rows that already exist, which is the smallest
   blast radius of the three.
4. A week later, arm the external read.
5. A week later, arm ideation, which is the one that creates rows.
