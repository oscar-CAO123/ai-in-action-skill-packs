---
name: Engagement Signal Leads
slug: engagement-signal-leads
description: >
  An INSTRUCTIONAL skill: it walks your agent through building a lead source out of
  intent rather than demographics. Pick the ten to twenty accounts your buyers actually read, watch
  their posts daily, pull the people who liked and commented, score each one against your ideal
  customer, then waterfall through enrichment providers to find a verified email or mobile. Hands
  back a clean, deduped, consent-checked list. It never sends anything by itself.
status: draft
evidence: pending_dry_run
phase_0: REQUIRED. Establish ground truth on your stack before any build step.
modularity: HARDWARE-MODULAR. Cloud APIs do the heavy work. The only branch that matters is whether
  the agent has a shell (scripts plus files) or is a locked-down runtime (drive the MCPs and a
  spreadsheet instead). Never assume a shell.
triggers:
  - "find leads who are already interested"
  - "scrape the people engaging with X"
  - "intent based lead list"
  - "build me an SDR pipeline"
requires:
  - A scraping API account with a maintained social actor (free tiers are enough to pilot)
  - At least one enrichment provider, ideally two so the waterfall has somewhere to fall
  - An email verification account
  - The operator's one-line offer and ideal-customer definition
not_industry_specific: true
---

# Engagement signal leads

Cold outbound off a demographic list is a red ocean, and reply rates show it. The people worth
contacting this week are the ones who just raised a hand at something. A like on a post about the
problem you solve is a smaller signal than a demo request and a much larger one than a job title.

This skill turns that signal into a list. It stops at the list on purpose.

---

## Rules that bind this skill

- **Never bulk-harvest addresses.** Enrichment is per-person, against a person you have a reason to
  contact. Address harvesting is illegal in Australia under the Spam Act 2003 regardless of intent.
- **Consent is checked before anything is drafted, not after.** Every record carries the basis you
  are relying on and the date you established it. No basis, no send, no exception.
- **The agent never sends.** It drafts and it stages. A person presses send until you
  explicitly changes that, and that change is a separate decision with its own gate.
- **Deduplicate against everyone you have ever contacted**, not just this run's list. The ledger is
  the point. Contacting the same person twice from two campaigns is how a domain gets burned.
- **No secret in a tracked file.** Keys live in your gitignored secrets location.

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

One question at a time. Never paste the list. Skip anything Phase 0 already answered, and say which
ones you are skipping and why.

**The offer and the buyer**
1. What are you selling, and what does it cost? A range is fine, "it depends" is not.
2. Describe the last three people who bought. Industry, size, role, and what was happening in their
   business the week they called you.
3. What has to be true about someone for this to be right for them.
4. What disqualifies someone instantly. Country, size, a competitor, an existing customer.
5. How many new conversations a month can you actually service? This sets the whole volume plan.

**The signal**
6. Who do your buyers read? Name accounts, not categories.
7. Which of those post at least weekly.
8. Show me a post that pulled in your buyers, and one that only pulled in your peers. What is the
   difference between them, in your words.
9. Is a comment worth more than a like in your market, and why.
10. Is there a second signal you already trust? A job ad, a funding round, a tender, a hire.

**The reality check**
11. What have you tried before that did not work, and what did you conclude from it.
12. What is your current reply rate, if you have ever measured one.
13. Who handles a reply when it comes in, and how fast can they realistically answer.
14. What would you never say in a first message, even if it worked.

**The boundary**
15. What may be sent automatically, and what needs your eyes first.
16. Which lists, tools or accounts must this never touch.

Confirm all sixteen back in a short block before you build anything.

---

## Phase 1. Pick the signal, not the audience

Ask you, one question at a time:

1. Who are the ten to twenty accounts your buyers actually read? Creators, competitors, industry
   press, and business accounts all count.
2. Which of those post at least weekly? Cut the rest, a dormant account produces nothing.
3. What does a post look like when it attracts your buyer rather than your peers? Have them point at
   two real examples, one of each.
4. What disqualifies someone instantly? Wrong country, too small, too big, a competitor, an existing
   customer.

**Why a handful is enough.** Within any niche a small number of posts are the outliers everyone
engages with. Monitoring those gets most of the reachable surface. Chasing the long tail costs more
than it returns.

Write the result as `sources.md`: account, why it qualifies, posting cadence, last checked.

---

## Phase 2. Pull the engagers

Daily, per source:

1. Fetch the account's new posts since the last run. Store the post id and the URL.
2. For each new post, pull the reactions and the comments. Commenters are a stronger signal than
   likers, so keep the distinction on the record.
3. Write one row per person: profile URL, name, headline, employer, which post, which action, date.

**Mechanism note.** All of this is deterministic. It is an API call, a loop and a write. Do not put a
model in this path. Inference belongs at the judgement step in Phase 3 and nowhere else in this
pipeline.

Deduplicate on the profile URL against the ledger before anything leaves this phase.

---

## Phase 3. The fit gate

This is the one step that earns a model call, because it is judgement against a written standard.

For each new person, give the model the ideal-customer definition from Phase 1 and the person's
public profile fields, and ask for three things: a fit verdict, a one-line reason, and a confidence.
Nothing else. Then:

- **Clear fit.** Continue to enrichment.
- **Clear miss.** Write to the ledger as excluded, with the reason. Never look at them again.
- **Unsure.** Hold in a review queue for you. Unsure is a real answer and it is cheaper than
  a wrong one.

Keep the prompt and the definition in a file you can edit. When the gate is wrong, the fix
is an edit to that file, not a longer prompt.

---

## Phase 4. Waterfall enrichment

Never pay the expensive provider for a record the cheap one already has.

1. Send the batch to the cheapest provider that covers your geography. Keep the hits.
2. Send only the misses to the next provider. Keep the hits.
3. Send only the remaining misses to the third, if you have one.
4. Stop when the cost per found record exceeds what a lead is worth to you. Write that number down
   before you start, or you will not stop.

Record per person: which provider found them, the field found, and the date. When a provider's hit
rate drops, that record is how you notice.

**Then verify every email.** Enrichment providers return addresses that no longer exist. Sending to
them is the fastest way to wreck deliverability. Classify each as valid, risky or invalid, keep the
valid, and hold the risky separately rather than deleting them.

Expect roughly two thirds to three quarters of a good list to end up with a verified address. A
provider claiming much better than that on cold profiles is measuring something else.

---

## Phase 5. Consent and the handoff

For each surviving record, write the consent basis explicitly. In Australia the practical bases for a
business-to-business email are an inferred one, where the address is publicly listed in a work
capacity and your message relates directly to that role, or an express one. Record which, and record
where you found the address.

Every message the pipeline eventually feeds must carry accurate sender identification and a working
unsubscribe. That belongs to the sending skill, and it is not optional there either.

Then hand off: a CSV or a sheet, one row per person, with the profile, the verified contact, the
source post, the fit reason, the consent basis and the date. Plus a ledger update covering everyone
seen this run, including the excluded, so tomorrow's run does not rediscover them.

---

## What to check after the first week

- How many people per source per day, and which sources produce nothing. Cut those.
- The fit gate's disagreement rate with you on the review queue. Over about one in five,
  the definition file is wrong, not the model.
- Verified-email rate by provider, and cost per verified record.
- How many were already in the ledger. A high number early is normal and it should fall.

---

## Gates

- **G1.** Every source is named, with a reason and a cadence.
- **G2.** Deduplication runs against the full ledger before enrichment, not after.
- **G3.** No model call sits in the fetch or the enrichment path.
- **G4.** Every record has a provider, a verification result and a date.
- **G5.** Every record has a written consent basis, or it does not leave the pipeline.
- **G6.** The stop-spending threshold was written down before the first paid call.
- **G7.** Nothing sends. The output is a list and a set of drafts.
