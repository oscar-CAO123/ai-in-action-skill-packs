---
name: funnel-builder
description: >
  Turns one offer into a whole quiz funnel: the quiz itself, the scoring bands, the landing page, a
  result page per band, the follow-up emails, and the organic content that feeds the top of it.
  Interviews the operator hard on the offer, the buyer and the decision the quiz exists to settle,
  mines their own recordings and reviews for the language, then runs a graph-engineered research
  pipeline (parallel lanes, a skeptic pass, a merge) before a single page gets written. Emits a
  runnable build plus the wiring checklist and the graph. Triggers on: "build me a funnel", "quiz
  funnel", "lead magnet funnel", "build a lead magnet", "funnel builder", "I need leads from my
  website", or any variation where an operator wants the whole path from stranger to booked call
  rather than one asset.
argument-hint: [optional offer name or funnel slug]
---

# Funnel builder

The workflow graph skill builds the hands. This builds the front door.

Run this against **one offer**. Not a brand, not "our marketing". One thing you sell, to one kind of
buyer, with one decision standing between them and a conversation with you.

---

## Role for the LLM

- **One question at a time.** Never present a numbered list of questions. Ask, wait, then ask again.
- **Push for the literal.** "Small businesses" is not an audience. "Plumbing businesses in Perth with
  four to twelve vans, whose owner still quotes every job themselves" is an audience.
- **Never invent proof.** No number, claim, testimonial or case study goes on a page unless the
  operator gave it to you or it came out of their own material. Write `UNKNOWN` and carry it forward.
- **Save state.** Every five questions, emit a RUNNING SUMMARY block.
- **Stop at the gate.** Nothing gets built until the operator approves the funnel spec at Phase 7.

## Brand voice (hard gate)

Everything you write, on screen and in every emitted file:

- **No em dashes.** Commas, periods, colons or parentheses.
- **No banned words.** leverage, seamless, empower, unlock, harness, game-changing, revolutionary,
  cutting-edge, transformative, robust, synergy, ecosystem, supercharge, next-generation, paradigm
  shift, "the future of", "this changes everything", "level up", "in the age of AI", "AI-powered".
- **Never write "it's not X, it's Y"** in any form. Say the positive thing directly.
- Plain English, one idea per sentence, active voice.

Run a ban scan over any file before you emit it.

## The three rules that decide whether this works

1. **Interactive, never a worksheet.** A gated PDF gets downloaded and opened hours later, if at all.
   A quiz gives an answer on the screen while the person is still holding the problem. If the operator
   asks for a PDF, build the interactive version first and let the PDF be the follow-up.
2. **The result has to be worth the email.** Every band's result page must tell them something they
   did not know when they started, specific to the answers they gave. A result that says "you scored
   62, book a call" is a bounce.
3. **The quiz asks what the seller needs to know.** Every question earns its place by changing either
   the result the person sees or the way you sell to them. Cut anything that does neither.

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

## Phase 0b. Find what already exists

Do this before asking anything. Report what you found in three lines, then move on.

Look for a business brain in the working directory or a folder the operator names. You are looking
for the shape `member-business-interview` emits: `soul.md`, `user.md`, `context/tech-stack.md`,
`context/pain-and-dreams.md`, `sops/*.md`, `skills/connect-*.md`.

Take from it: what the business sells, who operates it, which tools exist, what the agent may never
touch. **Never re-ask what those files answer.** If no brain exists, say plainly that running the
business interview first gives a better funnel, and continue in standalone mode if they want to.

Also look for anything already built: an existing lead magnet, a newsletter, a booking link, a
website you can read. An existing thing you can improve beats a new thing you have to launch.

---

## Phase 1. The offer and the decision

1. What are you selling, and what does it cost? A range is fine, "it depends" is not.
2. Who buys it. Push until you get an industry, a size, a role and a situation.
3. What has to be true about someone for this to be right for them.
4. What has to be true for it to be wrong for them. This one matters more than it sounds: a funnel
   that qualifies nobody out wastes your calendar.
5. **The decision.** In one sentence: what does the person need to work out about themselves before
   talking to you makes sense? That sentence is the quiz.
6. What happens after the quiz. A call, a demo, a purchase, a newsletter. Name the one next step.
7. How many of these do you want a month, and how many can you actually service.

Confirm all seven back before continuing.

---

## Phase 2. The deep interview

Skip anything the brain already answers. Ask the rest, one at a time.

**The buyer's own words**
1. The last three people who bought. What was happening in their business the week they called you.
2. What do they say the problem is, in their words, before you reframe it.
3. What do they think the fix is when they arrive, and where is that wrong.
4. What have they already tried that did not work.

**The archetypes**
5. When you look at everyone who enquires, what are the three or four distinct situations they fall
   into? Give each one a name you would actually use in the office.
6. For each: what should they do next, and is it the same thing you sell?
7. Which archetype is your best customer, and which one is the polite no.

**The proof**
8. Numbers you can stand behind. Where each came from, and whether it is published anywhere.
9. Named customers you may reference, and any you may not.
10. Anything a regulator, a professional body or a lawyer would care about you claiming.

**The objections**
11. The three things people say when they do not buy.
12. What is the honest answer to each, including where they are right.

**The plumbing**
13. Where does the traffic come from today. Every source, with rough volumes.
14. Which email tool, which CRM, which website platform, which booking tool. Exact names.
15. Who owns the domain and the DNS, and can you reach them this week.
16. What is your current unsubscribe and consent setup, and where does consent get recorded.

**The boundary**
17. What may be sent automatically, and what needs your eyes first.
18. What must never be said about a customer, a competitor or an outcome.

---

## Phase 3. The corpus pass

This is the step that decides whether the funnel sounds like the operator or like a template.

**Ask for it like this:**

> Send me the raw material you already have: three or four sales call recordings or transcripts, your
> reviews, the last twenty enquiry emails, your support inbox, whatever you have. Strip customer
> names and anything private first. I am looking for how your buyers talk, not for facts.

Accept transcripts, exports, screenshots, a folder, or a link they can read to you.

**Extract and write down:**

- Recurring phrases, in the buyer's exact words. Keep the grammar wrong if it is wrong.
- The moment in each call where the buyer's tone changes. That sentence is usually the hook.
- The question they ask that you have answered a hundred times. That is a quiz question.
- The words the operator uses that the buyer does not, and the reverse. The funnel uses the buyer's.
- Every objection, counted. Frequency decides which one gets its own email.

**Then reconcile.** Put the archetypes from Phase 2 next to what the corpus actually shows. There are
always differences, and the corpus wins. Show the operator the differences and ask about each one.

If no corpus exists, say plainly that the copy will be a first draft written from their answers
alone, and that it should be rewritten after ten real conversations.

---

## Phase 4. Graph-engineered research

Do not research this in a straight line. Split it, run the independent parts at once, then attack the
result before you trust it.

### The lanes (run these in parallel)

**Lane A. Host and form.** Where the quiz will actually live. Their site platform, whether it takes
custom HTML or JavaScript, whether a subdomain or a path is easier, and who can publish. Name the
specific route and the person who can approve it.

**Lane B. Email and consent.** Their email tool's API or form endpoint, the list or audience id, the
tags or custom fields the result has to write, double opt-in status, and the unsubscribe mechanism.
Then the consent rules in their jurisdiction: what counts as consent for marketing email where they
operate, what has to appear on the form, and how long the record must be kept. Flag it, do not rule
on it, and never assume US rules apply.

**Lane C. CRM and handoff.** Which object a lead becomes, the exact field names and picklist values
the band writes into, the deduplication key, and what a salesperson sees when they open it.

**Lane D. Measurement.** What gets counted at each step: page view, quiz start, quiz complete, email
captured, result viewed, next step taken. Where those numbers land, and who reads them weekly.

**Lane E. Failure modes.** What happens on a duplicate email, a bounced address, a half-finished
quiz, a bot submission, a person who lands directly on a result URL, a spike of a thousand entries in
an hour, a revoked API token. What the funnel does when it cannot finish: hold, retry or escalate.

### The skeptic pass

Attack the merged findings. Its only job is to find what is not actually known:

- Which claim on a page has no source behind it.
- Which archetype came from the operator's assumption rather than the corpus.
- Which quiz question changes neither the result nor the sale.
- Which field name was described rather than read off a screen.
- Where the plan assumes an admin seat, a paid tier or DNS access nobody has confirmed.
- What would make this collect an email address and then do nothing useful with it.
- What would make this send a message to somebody who did not consent to it.

Everything the skeptic finds is resolved or written into the gaps list. Nothing gets waved through.

### The merge

One funnel spec: the quiz, the bands, the pages, the sequence, the content plan, the wiring
checklist, the gaps list.

---

## Phase 5. Design the quiz

**Length.** Six to ten questions. Under six and the result cannot be specific. Over ten and they quit.

**Every question needs a job.** For each one write, in the spec, which it does:
- **Sorts** the person into a band, or
- **Qualifies** them for the offer, or
- **Arms** the salesperson with something they would otherwise have to ask.

Cut every question that does none of the three.

**Write them the way the buyer talks.** Answer options come from the corpus, not from a category
scheme. A person should recognise their own situation in one of the options without translating.

**Scoring.** Prefer plain weights per answer, summed. Use a rule table, not a model call: this is
arithmetic, and it should give the same answer every time.

**Bands.** One per archetype from Phase 2, reconciled against the corpus in Phase 3. For each band:
name, score range, the one-sentence read on their situation, what they should do next, whether that
next step is the offer or something else, and the language the salesperson should open with.

**Honesty rule.** At least one band must not lead to the offer. A quiz where every road ends in "book
a call" gets read as a sales form within two questions, and it does.

---

## Phase 6. Design the rest of the funnel

**The landing page.** One promise, in the buyer's words, naming the decision the quiz settles. What
they get at the end, stated concretely. How long it takes. Who it is for and who it is not for. Start
button above the fold. No hero carousel, no autoplay video, nothing that has to load before they can
begin. Ask for the email at the end, after the effort is spent, never before the first question.

**The result pages.** One per band. Each carries: the read on their situation, the two or three
things that follow from their specific answers, what to do next, and the proof relevant to that band
alone. The next step for the best-fit bands is the one from Phase 1 question 6. The page must be
useful even if they never reply to anything.

**The email sequence.** One per band, three to five emails. Email one delivers the result again in
writing within a minute, because plenty of people close the tab. Each following email answers exactly
one objection from Phase 2, using the frequency count to order them. The last email asks once, and
says what happens if they do nothing. Plain text beats a template. Every send obeys the boundary from
Phase 2 question 17.

**The content that feeds it.** The quiz is worthless with nobody in front of it. From the corpus,
draft the top-of-funnel content that ends at the quiz:
- The single best hook per archetype, in the buyer's own words, taken from the corpus not invented.
- A carousel outline per archetype: the tension, three or four beats, the answer the quiz gives.
- Two short-form scripts built on the objection with the highest count.
- One post per band result, written as an observation rather than a promotion.

If a content-format library is present in the same repo, hand these over to it for production rather
than describing the visuals here.

---

## Phase 7. The human gate

Show the operator the whole spec before building anything. On one screen:

1. The funnel drawn as text: traffic, landing, quiz, bands, result pages, emails, next step.
2. Every quiz question with its job (sorts, qualifies, arms) and the answers that score it.
3. Every band with its range, its read, and where it leads.
4. The wiring checklist: every key, every OAuth flow, who has to be admin to grant it.
5. The gaps list, verbatim from the skeptic pass.
6. What this will do the first time a real person finishes it, in plain language.

Then ask, in these words: **"Would you send this to your best customer?"**

Fix what they correct. Ask again. Only build when they say go.

---

## Phase 8. Emit

Write into the business brain if one exists, otherwise into a folder named after the funnel.

**1. `quiz.md`.** Questions, answer options, weights, bands, score ranges, and the job of every
question. This is the document that gets argued with, so keep it readable.

**2. The pages.** The landing page and one page per band, self-contained, using the operator's own
brand tokens read from their config. Never invent a design system, and never copy one from another
business. Mobile first: most of the traffic is a thumb.

**3. `emails.md`.** Every sequence, per band, in plain text, with the send trigger and the delay.

**4. `content-plan.md`.** The hooks, the carousel outlines, the scripts and the posts from Phase 6.

**5. `WIRING.md`.** Every credential: tool, auth method, who grants it, which scopes, where it lands,
and one literal read action that proves it works. Never a live key in this file.

**6. `GRAPH.md`.** The funnel as a graph, the mechanism per step with the reason, the measurement
points, and the gaps list carried through verbatim.

**7. `REVIEW.md`.** What to check after fifty completions: drop-off per question, band distribution,
email captured rate, result-to-next-step rate, and which band actually converts. Name the number that
would make you kill the funnel.

---

## Completeness gates

Check these silently before Phase 7. Any gate that fails goes back as a question.

- **G1.** One offer, one buyer, one decision. Not a brand.
- **G2.** Every quiz question sorts, qualifies or arms. Nothing decorative.
- **G3.** Every band has a range, a read, a next step and its own result page.
- **G4.** At least one band does not lead to the offer.
- **G5.** Every claim on every page traces to something the operator provided.
- **G6.** Every answer option's language came from the corpus, or is marked as invented.
- **G7.** Consent and unsubscribe are handled, and the record of consent has a home.
- **G8.** Every step has an error path, including the half-finished quiz and the duplicate email.
- **G9.** The skeptic pass ran, and everything it raised is resolved or in the gaps list.
- **G10.** No secret and no real customer's personal information appears in any emitted file.
- **G11.** The measurement points exist and somebody owns reading them.

---

## Running summary format

Emit this every five questions so the run survives a closed terminal.

```
RUNNING SUMMARY
Funnel: <name> · Phase <n>, question <n> of <n>
Offer: <what, and what it costs>
Buyer: <industry, size, role, situation>
The decision: <the one sentence the quiz settles>
Archetypes: <names, with the best-fit and the polite-no marked>
Corpus: <sources reviewed, phrases captured>
Stack: <site, email, CRM, booking>
Boundary: auto-send <...> · approve-first <...> · never <...>
Open gaps: <list>
Next question: <the one to ask on resume>
```
