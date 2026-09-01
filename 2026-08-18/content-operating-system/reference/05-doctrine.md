# The doctrine

These are craft laws that came out of a working content engine. They are written universally here.
The build step copies them into `brain/doctrine.md` and **re-grounds every one of them in the
operator's own business**, with their examples, their evidence and their constraints substituted in.

A law copied across without that pass is decoration. Do the pass.

---

## 1. The citation law

**Never free-write a hook.**

Every hook is filled from a structure that has been shown to work, and the finished asset records
which structure it used. A hook written from scratch on a Tuesday afternoon is a guess, and there is
no way to learn from a guess because there is nothing to compare it against.

In practice:

- Keep a hook bank in `brain/formats/hooks.md`. Every entry has an id, the structural shape with
  slots, and at least one real example the operator has seen work.
- When writing, pick a structure by id, fill its slots, and write the id beside the hook.
- When a hook performs, the structure gets a note. When a structure never performs across ten uses,
  it comes out.

The bank starts from the operator's own best-performing content and from what actually works in their
market. It does not start from a list of viral hook templates, because those templates were tuned on
an audience that is not theirs.

**Personalisation pass:** seed their bank from the answers to interview questions 60 and 61, plus
anything the discovery sweep found in their existing content.

---

## 2. The evidence law

**Every claim in a finished asset traces to something a real person said or something the operator
can show.**

Three tiers, and the tier goes in the asset's metadata:

| Tier | Means | Allowed to say |
|---|---|---|
| **Shown** | A screen recording, a document, a number from their own data | Anything the artifact supports |
| **Quoted** | A customer, a ticket, a review, a forum post, with a source id | The claim, attributed, in the source's words |
| **Held** | The operator believes it and can argue it | Framed as a position, never as a fact |

Anything that fits none of the three does not go in the asset. This is the rule that stops a content
system from slowly drifting into confident nonsense, and it is the first rule people quietly drop.

**Personalisation pass:** interview questions 45 to 51 define what tier they can actually reach.
Question 50 becomes a written do-not-say list.

---

## 3. The demonstration law

**Show the thing being done, at the moment it is being done.**

Description is cheap and everybody has it. A market that has heard the claim a hundred times has
never watched the claim happen. The single most reliable content upgrade available to any operator is
replacing an explanation with a recording of the work.

- If it happens on a screen, record the screen.
- If it happens in the physical world, record the physical world.
- If it happens over weeks, record the artifact at the start and at the end.
- If it genuinely cannot be shown, say what stopped it from being shown. That is often the more
  interesting content.

**Personalisation pass:** interview questions 45, 48 and 64 define what they can demonstrate. If the
answer to all three is nothing, that is the finding, and the first month of content should be built
around creating something demonstrable.

---

## 4. The canonical format law

**One canonical specification per format, and nothing produces outside it.**

A format is a named thing with a fixed spec: aspect ratio, duration band, structure, typography or
voice treatment, and the rules for what goes in each beat. When somebody produces a variant, either
it becomes a new named format with its own spec, or it does not ship.

Without this, drift is guaranteed. Three months of small improvisations produce a feed where nothing
looks related to anything else, and no result can be attributed to a format because no two assets
were the same format.

- Formats live in `brain/formats/`, one file each, selected in interview question 55.
- A format file is the only authority for that format. A production script never carries a rule.
- Changing a format is an edit to its file with a dated changelog line, applied to everything made
  after that date, never retroactively.

---

## 5. The three craft laws

**Specificity.** Every clause names something a person could point at. A number, a brand, a place, a
time, an object. "Small businesses waste time on admin" names nothing. "A three-person plumbing
business spends Thursday night doing quotes" names four things.

**Consequence.** Every claim carries what happens as a result, for a named person. Not the feature,
not even the benefit in the abstract, the actual downstream event in someone's week.

**Compression.** Say it in the fewest words that keep the specificity and the consequence intact.
Compression happens last, after the other two are true. Compressing first produces a slogan.

---

## 6. The hook laws

The hook is the only part of an asset that most of the audience will ever see, so it gets
disproportionate attention.

- **The gap sits at the audience's pain, not at the operator's product.** The reason to keep watching
  is that something unresolved in the viewer's own week is about to be resolved.
- **Foreshadow the mechanism inside the hook.** Name the shape of the answer without giving it. A
  hook that only creates curiosity gets the view and loses the person at second four, because the
  payoff was never specified and the body cannot match an unspecified promise.
- **Open on an avatar or a question.** Either name who this is for in concrete terms, or ask the
  thing they are already asking. Both give the right person a reason to stay and the wrong person a
  reason to leave, which is the correct outcome.
- **Flow conjunctively.** Each line follows from the one before. When a line could be moved without
  the piece noticing, cut it.
- **Never withhold as a technique.** Deliberate vagueness to force a click reads as cheap and trains
  an audience to stop trusting the account.

Two patterns are banned outright, everywhere, in every format:

- **The negation swap.** "It is not X, it is Y." Say the positive thing directly. It is the single
  most recognisable tell of generated copy.
- **The em dash.** Use a comma, a period, a colon, or parentheses.

**Personalisation pass:** add whatever the operator's own language rules require, from interview
questions 44 and 51.

---

## 7. The volume model

Volume without a quality floor produces a feed nobody follows. A quality floor without volume
produces four excellent posts a year that nobody sees.

The model that works: **fix the floor, then take the volume the floor allows.**

1. Define the floor as a checkable gate, not as a feeling. See `brain/doctrine.md` gate section and
   `engine/cos/gate.py`.
2. Measure how many assets per week actually clear the floor with the time and money available.
3. That number is the volume. Publishing below the floor to hit a number costs more than posting
   less.
4. Raise volume by making the floor cheaper to clear, through formats and templates, rather than by
   lowering it.

**Personalisation pass:** interview questions 56, 67 and 68 set the real ceiling. Use their worst
week, not their best.

---

## 8. The production order

The order is the whole point, because every gate sits before the spend it protects.

```
evidence  ->  idea  ->  question or angle  ->  hook  ->  script  ->  human approval
          ->  stills or storyboard  ->  human approval  ->  motion, voice, render
          ->  gate  ->  human approval  ->  publish
```

Three human gates, and none of them are optional:

- **After the script.** Cheapest place to kill a bad idea. Most assets that fail should fail here.
- **Before any paid generation.** A still costs cents, a video costs dollars, and a bad still becomes
  a bad video every single time. Approve the still.
- **Before publish.** Always. Every time. Including when it is obviously fine.

---

## 9. The gate

A batch is not finished because it looks finished. It is finished because a check ran and exited
clean. `engine/cos/gate.py` enforces the mechanical half:

- Every asset has an idea id, and that idea exists in a queue file.
- Every claim tier is recorded, and no `held` claim is phrased as a fact.
- Every hook records the structure id it was filled from.
- No banned word, no em dash, no negation swap, anywhere in the copy.
- Every asset names its format, and its dimensions match that format's spec.
- Nothing references a file that does not exist.

The judgement half stays with a person. The gate exists so that the person spends their attention on
judgement instead of on catching typos.

---

## 10. What to do when a law fights the work

Say so, out loud, to the operator. Do not silently deviate, and do not follow a law off a cliff
because it is written down.

These laws came out of one business. Some of them will not survive contact with another one. The
useful move is to name which law is fighting, what it is costing, and what the replacement rule
should be, then edit `brain/doctrine.md` with a dated changelog line.

A doctrine file that has never been edited is a doctrine file nobody is using.
