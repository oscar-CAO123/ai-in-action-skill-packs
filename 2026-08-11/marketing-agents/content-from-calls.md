---
name: Content From Calls
slug: content-from-calls
description: >
  An INSTRUCTIONAL skill: it walks your agent through turning conversations the business
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
- **No invented outcome.** A number, a result or a case study is either something you
  provided or it does not appear.
- **The person owns their name.** Nothing publishes under someone's account until they have approved
  it, until they explicitly hand that over.

---

## Phase 0. Read the workspace before you ask anything

Do this first, every time, before a single question. The point is to arrive already knowing who they
are, so the interview spends its questions on what the files cannot tell you.

**Walk the whole tree, not the folders you expect.** From the directory you were opened in, list
everything to about four levels deep, including dotfiles and hidden config, skipping `node_modules`,
virtualenvs, build output and large binaries. Read names and structure first. A file tree is a
confession: it shows what someone actually works on rather than what they say they work on.

**Then read whatever exists, in this order:**

| Looking for | What it tells you |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, root `README.md` | The operating rules they already wrote down. Inherit them, never restate them. |
| A business brain: `soul.md`, `user.md`, `memory.md`, `context/`, `brand/` | Who they are, what they sell, who operates the business, the voice they write in. |
| `sops/`, `playbooks/`, `runbooks/`, `docs/` | The jobs they already run, in their own words. |
| `skills/`, `.claude/`, `.codex/`, `agents/`, `prompts/` | What their agent can already do, and the conventions their files follow. |
| `config/`, `.env.example`, `skills/connect-*.md` | Which tools are wired up, and where secrets are expected to live. |
| `.gitignore`, and the last twenty commits if this is a repo | What they treat as private, and what they have actually been working on lately. |
| The three largest folders, whatever they turn out to be | The real centre of gravity, which is often not where they say it is. |

**Never open anything that looks like a secret.** `.env`, `*token*`, `*credential*`, `*oauth*`,
`*.pem`, `*.key`. Note that it exists, note where it lives, and move on.

**Then report back in five lines and stop.** What kind of business this looks like, what the agent
already knows how to do, which tools are wired, what looks abandoned, and what you looked for and
could not find. Ask them to correct it.

That correction is worth more than the next three questions, because it tells you which of their own
files they still trust.

**Everything you learned here comes off the question list.** Re-asking something their own files
already answered is the fastest way to make this feel like a form instead of a conversation.

---

## Phase 0b. The interview

One question at a time. Skip anything Phase 0 already answered.

**The people**
1. Whose names will posts go out under? For each: their role, and whether they have ever posted.
2. Who would rather not, and would be happier as a source than as an author.
3. Who is the best explainer in the business? Their transcripts will carry the whole thing.

**The material**
4. What conversations already get recorded, and where do the recordings live.
5. Do you have consent to use them, from your own people and from customers.
6. What is in the support inbox that gets answered over and over.
7. Where do the good internal explanations get written down, if anywhere.
8. What is the last thing someone in the business said that made you think "that should be public".

**The claims**
9. Which numbers may be published, and where did each come from.
10. Which customers may be named, and which may never be.
11. What would a regulator or a professional body care about you claiming.

**The voice**
12. Paste two posts, one from your business you were happy with and one from anyone that you wish
    you had written. What is the difference.
13. What words does your business never use.
14. How often should each person post before it starts feeling like a campaign.

**The gate**
15. Who approves before anything publishes, and what happens when they are away.

Confirm all fifteen, then build one voice profile per person and show them a draft each before
anything is scheduled.

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
- **G5.** No number publishes without a source you provided.
- **G6.** No model call sits in the scheduling or reporting path.
- **G7.** Performance is written back against the source item weekly, by a job that runs whether or
  not anyone remembers.
