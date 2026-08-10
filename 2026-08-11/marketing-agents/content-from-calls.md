---
name: Content From Calls
slug: content-from-calls
description: >
  An INSTRUCTIONAL skill: it walks the operator's agent through turning conversations the business
  already has into published content. Source material comes from sales calls, a weekly ten minute
  interview with each person, support threads and internal channels. The agent extracts the
  insights, drafts in each person's own voice, schedules across multiple accounts, then reads the
  performance data back in so the next round is built on what worked. One person can run content for
  a whole team this way.
status: draft
evidence: pending_dry_run
phase_0: REQUIRED. Establish ground truth on what recordings exist and who has consented.
modularity: HARDWARE-MODULAR. Transcription and scheduling are cloud APIs. A locked-down runtime can
  drive them through MCPs and a spreadsheet.
triggers:
  - "turn our calls into content"
  - "content for my whole sales team"
  - "post on LinkedIn for my team"
  - "we have nothing to post about"
requires:
  - Recordings or transcripts of real conversations, with consent to use them
  - A scheduling tool that holds multiple accounts and exposes an API
  - Each person's agreement to publish under their own name
not_industry_specific: true
---

# Content from calls

Asking a model to "write a good post about our industry" produces the most average paragraph on the
internet, and everyone can tell. The business already generates original material every day. It is
sitting in call recordings, in the support inbox and in the internal channel where somebody explains
something well.

This skill mines that and publishes it. The source material is the whole trick.

---

## Rules that bind this skill

- **Consent first, twice.** Once from the person being recorded, once from the customer if any of
  their words or situation appear. No customer name, logo or identifying detail is published without
  written permission.
- **Never publish a paraphrase as a quote.** If it is in quotation marks it is verbatim from the
  transcript. If it is tidied, it is not a quote any more.
- **No invented outcome.** A number, a result or a case study is either something the operator
  provided or it does not appear.
- **The person owns their name.** Nothing publishes under someone's account until they have approved
  it, until they explicitly hand that over.

---

## Phase 1. Set up the source

Pick the streams that already exist before creating new ones:

| Stream | What it gives you | Cost to set up |
|---|---|---|
| Sales calls | Objections in the buyer's words, the moment they get it | Already recorded, usually |
| A weekly ten minute interview per person | Opinions and stories nothing else surfaces | Ten minutes each |
| Support and the shared inbox | The questions that repeat, which are the best posts | Free |
| Internal channels and docs | Explanations written well the first time | Free |

The weekly interview is the one that pays. It needs no agenda: ask what came up this week, what
surprised them, what they had to explain twice, what they changed their mind about. Ten minutes of
this beats an hour of trying to write.

---

## Phase 2. Extract, do not generate

Per transcript, pull structured items rather than prose:

- **Claims.** Something the person asserts, with the reasoning attached.
- **Stories.** A specific situation with a before, a turn and an after.
- **Objections.** What a customer pushed back on, and the answer given.
- **Contrarian moments.** Where they disagree with the common advice in their field.
- **Explanations.** Something complicated said simply.

Each item carries: who said it, which recording, the timestamp, the verbatim line, and whether it
needs a fact check. Items missing a source do not exist.

**Mechanism note.** Extraction is judgement, so it earns a model call. Everything downstream of the
approved post (formatting, scheduling, fetching stats, writing the report) is deterministic. Do not
pay for inference to move a string into a calendar.

---

## Phase 3. Draft in their voice, not a house voice

For each person, build a voice profile from their own transcripts: sentence length, the words they
actually use, what they never say, how they open, whether they swear. Feed that profile plus one
extracted item, and produce one post.

Rules for the draft:
- One idea per post. An item that contains three ideas is three posts.
- Open with the specific thing, not the category. The story, the number, the sentence the customer
  said.
- No em dashes, no "it's not X, it's Y", none of the banned words.
- Whatever length that person actually writes at. A short poster does not suddenly write essays.

Then the person reads it. First few weeks, every post. Later, a sample. If they rewrite it
completely, the voice profile is wrong and that is the thing to fix.

---

## Phase 4. Schedule across accounts

Use a scheduling tool that holds every account and exposes an API. What matters:

- A queue per person with their own cadence. Daily is not right for everyone.
- Never the same post on two accounts. Same idea, different angle, different week.
- Space team members out. Five near-identical posts on the same morning reads as a campaign.
- Hold a review buffer of two days so a person can pull something after the news changes.

---

## Phase 5. Read the results back in

This is the loop most content builds skip, and skipping it is why they produce the same post forever.

Weekly, pull per-post performance and write it back against the extracted item that produced it. Then:

- Find the outliers, top and bottom. The middle teaches nothing.
- For each top performer, name why in one line: the format, the topic, or the specific opening.
- Feed those reasons into the next round as instructions, not as examples to copy.
- Keep a winners file. Anything that performed twice goes in it.

**Remix on a cycle.** A post that worked is worth publishing again in ninety days, rewritten, to a
mostly different audience. This is not a trick, it is how every consistent account works. Track the
last-published date so nothing repeats too soon.

**Fight the sameness.** An agent left in a loop converges on its own average within a fortnight. The
fix is not a better prompt, it is new input: watch ten human accounts in the niche, pull their
outliers, and use those as structural prompts. Take the shape, never the words.

---

## What to check after a month

- Posts published per person against the target, and who is quietly not approving.
- Proportion published verbatim from the draft. Very high means nobody is reading them.
- Which stream produced the winners. Usually the weekly interview, sometimes support.
- Whether anything published contained a number nobody checked.

---

## Gates

- **G1.** Consent exists for every recording and every customer detail used.
- **G2.** Every extracted item has a person, a source and a timestamp.
- **G3.** Every quotation mark contains verbatim text.
- **G4.** Every post is approved by the person whose name is on it.
- **G5.** No number publishes without a source the operator provided.
- **G6.** No model call sits in the scheduling or reporting path.
- **G7.** Performance is written back against the source item weekly, by a job that runs whether or
  not anyone remembers.
