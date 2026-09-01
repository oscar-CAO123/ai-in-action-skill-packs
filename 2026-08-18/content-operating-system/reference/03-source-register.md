# Phase 3. The source register

The source register is the most valuable file the build produces. It is the map of every place this
business keeps proof of what its customers actually say, how the agent reaches each one, and what
each one is good for.

Write it to `brain/source-register.md` and mirror the machine-readable half into
`engine/config.json` under `sources`.

---

## The four first-class reservoirs

These ship with working pullers in `engine/cos/sources/`. Wire whichever ones exist.

### 1. Calls

**What it is.** Sales calls, discovery calls, onboarding calls, support calls, customer interviews.
Anything where a customer talked and it was recorded.

**Why it is first.** It is the only source where the customer speaks unprompted, at length, about a
problem they are currently paying to solve. A single month of discovery calls usually contains more
usable content than a year of keyword research.

**How to reach it, easiest path first:**

| Situation | Path |
|---|---|
| Transcripts already export to a folder | Point `sources.calls.paths` at it. Done, no credentials. |
| Fathom, Granola, Fireflies, Otter, Grain, tl;dv | Each has an export or an API. Prefer a scheduled export to a folder over an API integration. Fewer things to break. |
| Gong or Chorus | API, and usually an admin has to approve the app. Note it as a gap and use manual exports until then. |
| Zoom cloud recordings | Zoom API with `recording:read`. Transcripts only exist if cloud transcription was on. |
| Recorded but never transcribed | Transcribe locally with Whisper. Slower, free, and the audio is already yours. |
| Not recorded at all | Say so plainly. Recording sales calls is the single highest-return change they can make this week, and it costs nothing. |

**What a record needs:** date, call type, who the customer was in role terms, the transcript text,
and a source id. No names, no contact details, no company names in the normalised store unless the
operator explicitly opts in.

### 2. Tickets

**What it is.** Support conversations. Helpdesk tickets, the shared inbox, chat logs, the WhatsApp
thread the customers actually use.

**Why it matters.** Calls tell you why people buy. Tickets tell you what breaks the promise
afterwards, which is where the honest content lives, and where competitors never look.

**How to reach it:** Intercom, Zendesk, Front, Help Scout, Freshdesk and Crisp all have REST APIs
with a read scope. A Gmail label is reachable through the Gmail API or an mbox export. A CSV export
from any of them works with zero credentials, and is the right first move.

**What a record needs:** date, subject or first message, the customer's own words, resolution status,
and whether it recurred.

### 3. Forums

**What it is.** Where the industry complains in public. Reddit, Hacker News, X, Facebook groups,
Stack Overflow, industry-specific boards, product review threads.

**Why it matters.** It is unfiltered, it is dated, and it is the only reservoir that tells you what
people say about your category when nobody selling anything is in the room.

**How to reach it:** Reddit's public JSON endpoints need no key for read access at low volume.
Hacker News has a free public API. X needs a paid API key or a search tool. Facebook groups cannot be
read programmatically and have to be manual. Ship what is free, register the rest as gaps.

**What a record needs:** date, platform, subreddit or board, the post or comment text, engagement
count, and a permalink so a claim can be traced.

**The rule that keeps this useful:** collect the **objection**, not the topic. A thread titled "AI
tools for trades" is noise. A comment inside it saying "we tried this and it took longer than doing
it by hand" is the content.

### 4. Reviews

**What it is.** Google reviews, industry directories, app store reviews, marketplace feedback, G2 or
Capterra if it applies.

**Why it matters.** Reviews are pre-filtered for emotion and they name the specific thing that
delighted or infuriated someone. Competitor reviews are just as useful as their own, and are often
the fastest route to a positioning line.

**How to reach it:** Google Business Profile API for their own, a places API for competitors, app
store RSS feeds for mobile, or a scrape where terms allow. Manual paste is fine to start.

**What a record needs:** date, rating, the review text, whether it is theirs or a competitor's, and
the specific thing named.

---

## Sources the register maps but does not pull automatically

Record these in `brain/source-register.md` with the same four facts (where it lives, how to reach it,
how far back, what a record looks like) and a note on why it is manual. Any of them can graduate to a
puller later.

- **CRM notes and lost reasons.** Usually the highest-value structured source in the business, and
  usually the emptiest field in the CRM. If it is empty, that is a process finding, not a data
  finding. Tell them.
- **Sales email threads.** Rich, and full of personally identifying information. Manual, redacted.
- **Community channels.** Slack, Discord, Circle, Skool. Exportable, needs owner consent.
- **Own-channel performance.** What their own posts and ads actually did. Wire it once the loop is
  running, so ideation learns from results rather than guesses.
- **Search demand.** Search Console, keyword tools. Useful for topic sizing, weak for language.
- **Competitor content and ads.** Public ad libraries. Good for what a market is being told, useless
  for what customers believe.

---

## Ranking the sources

Rank by **volume times honesty**, not by how easy the integration is. A hard-to-reach source with two
years of unfiltered customer speech beats an easy one with three hundred five-star reviews that all
say "great service".

Write the ranking into the register and use it as the ingestion order. When a run has a budget or a
time limit, the top of the list goes first.

---

## Privacy, stated once and enforced everywhere

The normalised store is the thing every future content run reads. Anything that goes in comes back
out eventually, in a script, in a review page, in a prompt sent to a model.

**The default is redaction at ingestion, not at output.**

- Strip names, email addresses, phone numbers, street addresses and company names before writing a
  record. Keep role, industry, company size band and deal stage. Those carry the meaning.
- Keep the source id and the pointer to the original, so a claim can be verified by a person who has
  the right to see it.
- Never send an unredacted record to a third-party model. If a source cannot be redacted reliably,
  mark it `manual_only` and keep it out of the automated path.
- If the operator wants named quotes for testimonials, that is a separate, deliberate, per-quote
  approval, and it never runs on a schedule.

Ask once whether their industry has a regulator or a contractual limit on this. Write the answer into
`brain/language-rules.md` as a hard rule, not as a note.

---

## The register format

`brain/source-register.md`, one section per source:

```markdown
## Calls (Fathom)

- **Rank:** 1
- **Where:** ~/Library/CloudStorage/GoogleDrive/.../Fathom Transcripts/
- **Reach:** local folder, no credentials, watched by the ingestion job
- **Depth:** March 2025 to now, roughly 340 transcripts
- **Record:** date, call type, role, transcript text, source id
- **Redaction:** names and company names stripped at ingestion
- **Good for:** objections, buying triggers, the words they use for the problem
- **Known gap:** support calls are on a different system and are not here
```

Machine-readable half in `engine/config.json`:

```json
{
  "sources": [
    {
      "id": "calls_fathom",
      "type": "calls",
      "rank": 1,
      "enabled": true,
      "paths": ["~/Drive/Fathom Transcripts"],
      "redact": true,
      "lookback_days": 30
    }
  ]
}
```

Never put a credential in `config.json`. Config holds the **name** of the environment variable, and
the engine reads the value from the environment at run time.
