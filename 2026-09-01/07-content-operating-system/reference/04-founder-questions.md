# Phase 6. The founder question bank

The bottleneck in founder-led content is never the camera. It is the thirty seconds before the camera
turns on, when the founder has nothing specific to say and says something general instead.

The question bank removes that thirty seconds. It is a standing, categorised list of questions this
specific founder can answer better than anyone else in their market, each one traceable to something
a real customer said or something the founder actually believes.

Written to `brain/founder-questions.md`. Built once at install, appended to by every ideation run,
and retired as questions get answered on camera.

---

## What makes a question belong in the bank

Four tests. A question that fails any of them does not go in.

1. **Only this person can answer it well.** If a competitor could give the same answer, it is a
   category question, and the internet already has forty versions of it.
2. **The answer is a story or a position, never a definition.** "What is X" produces a Wikipedia
   entry read aloud. "What did you get wrong about X" produces content.
3. **It traces to evidence or to a stated belief.** Every question carries a source line: a customer
   quote, a ticket, a forum thread, or an interview answer with its phase and number.
4. **It can be answered in ninety seconds without preparation.** If it needs research, it is a
   different kind of asset and belongs in the idea queue instead.

---

## The nine vectors

Build the bank with roughly even coverage across these. Aim for **150 to 200 questions at install**,
with at least twelve in every vector.

### 1. Customer pain, named exactly

Drawn from calls, tickets, reviews and forums. Each question quotes the actual language.

- A customer said "[exact phrase]". What is actually going on when someone says that?
- What is the real cost of [specific problem] over a year, in a business like theirs?
- Why does [common workaround they named] stop working at a certain size?
- What do you say to someone who has already tried [thing they all try first] and it failed?

### 2. The objection

The strongest founder-led format there is, because the objection is already in the viewer's head.

- Someone said no because [objection]. Were they right?
- What is the honest answer to "[objection in their words]", including the part that hurts?
- What would have to be true for [objection] to be a good reason to walk away?
- Which objection do you get that you secretly agree with?

### 3. Contrarian belief

From interview phase D. These are the questions that build a reputation rather than a pipeline.

- Why do you think [standard industry practice] is quietly harmful?
- Everyone says [common advice]. What is wrong with it?
- What do you believe about [industry] that would get you argued with at a conference?
- What is the most expensive piece of conventional wisdom in your industry?

### 4. Changed mind

Underused and disproportionately effective, because being wrong in public is rare.

- What did you believe five years ago that you have since abandoned, and what changed it?
- What is a decision you defended publicly and later reversed?
- Where were you overconfident, and what did it cost?

### 5. Origin and scar tissue

The reason a person is credible on a subject, told as a specific event.

- What is the actual moment that made you start this?
- What is the worst thing that has happened in this business?
- What is a mistake you made that you now design the whole business to avoid?
- What did you have to learn the expensive way?

### 6. The demonstration

The founder shows something rather than describing it. These questions produce screen recordings.

- What can you show on a screen that a prospect has never seen?
- What is the thing you built internally that customers do not know exists?
- Walk through [specific process] as it actually happens, including the ugly part.
- What does the first hour of working with you actually look like?

### 7. Proprietary data

Only available to a business that has been operating and paying attention.

- What does your data say about [industry assumption] that contradicts it?
- Across your last [N] customers, what was the pattern nobody expected?
- What do you know about [category] that only comes from having done it [N] times?
- What is the number in your business that would surprise your own industry?

### 8. The category, from the inside

Questions about how the industry works, answered by someone who is in it rather than covering it.

- How does [industry pricing model] actually work, and who does it favour?
- What happens behind the scenes when a customer asks for [common request]?
- Who makes money when [common industry situation] happens?
- What would you tell a friend to look for before signing with anyone in your category?

### 9. Values and the way they work

The slowest to pay off, the hardest to copy.

- What do you refuse to do, even when it costs you the deal?
- What kind of customer do you turn away, and why?
- What does your team do differently to the rest of the industry, and why did you choose that?
- What are you optimising for that is not revenue?

---

## Building the bank at install

1. Read every interview answer, the source register, and any evidence already ingested.
2. For each vector, generate questions **from the material, not from the vector description**. A
   question that could have been written before the interview does not go in.
3. Attach a source line to every question. Format below.
4. Deduplicate. Two questions with the same answer become one question.
5. Sort each vector by how confident you are that the answer will be specific.
6. Write the file. Do not pad to hit a count. A bank of ninety real questions beats two hundred with
   sixty generic ones in the middle.

**The file format:**

```markdown
## Vector: The objection

### Q-014
**"You say the answer is honest even when it hurts. So what is the honest answer to
'this is too expensive for a business our size'?"**

- **Source:** lost deal, 12 Aug, "we just can't justify it at our revenue" (calls_fathom / c-2291)
- **Also seen:** 3 forum threads, r/[their industry], all within 60 days
- **Format fit:** talking head, 60 to 90 seconds
- **Status:** unanswered
```

Four states: `unanswered`, `queued` (attached to an idea in the current queue), `answered` (filmed,
with a link to the asset), `retired` (no longer relevant, with the date and the reason).

---

## Refreshing it every week

The ideation run does three things to the bank, in this order.

1. **Append.** New evidence from the week produces new questions, using the same four tests and the
   same nine vectors. Typically three to eight per week from an active business.
2. **Promote.** Pick the **five to ten questions worth filming this week**, based on what the week's
   evidence actually showed. A question that three separate customers raised in the last seven days
   outranks a question that has been sitting in the bank since install. Write them to the top of the
   file under `## This week`.
3. **Retire.** Mark answered questions with a link to the asset. Retire anything the founder has
   answered twice, anything overtaken by a change in the business, and anything that has sat
   unanswered for six months without ever being promoted.

The bank only stays useful if the retire step actually runs. A bank that only grows becomes a list
nobody opens.

---

## How the founder uses it

Tell them this in one line when the build finishes, and put it at the top of the file:

> Open `brain/founder-questions.md`, read the five under **This week**, pick the one you have the
> most to say about, and talk for ninety seconds. Do not script it. The source line under each
> question is there so you know a real person actually asked.

The whole system exists to keep that file worth opening.
