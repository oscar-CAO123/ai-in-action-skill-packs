# The format library

Fourteen format archetypes, stripped of any one company's styling. The interview picks which ones
this operator gets, based on what they can actually produce (questions 62 to 68) and where their
buyer is (questions 53 to 56).

At build time, each selected format is copied into `brain/formats/<id>.md` and filled in with their
specifics: their aspect ratios, their duration bands, their typography or voice treatment, their
examples. An unselected format is not written at all, so the brain never carries a rig for something
they will never make.

**Select three to five.** More than five and none of them get good. Fewer than three and the feed
gets monotonous.

---

## How to read the table

**Effort** is the honest cost of the second one, not the first. **Evidence tier** is the highest
proof tier the format can carry, from `05-doctrine.md`.

| Id | Format | Channel fit | Effort | Evidence tier |
|---|---|---|---|---|
| `talking-head` | Founder to camera, one idea | Short video, LinkedIn, X | Low | Held, quoted |
| `screen-walk` | Screen recording of real work | Short and long video, YouTube | Low | Shown |
| `vo-stills` | Voice over stills or slow footage | Short video | Medium | Quoted |
| `build-breakdown` | How a specific thing was built, start to finish | Long video, article | High | Shown |
| `before-after` | The state before, the state after, side by side | Short video, static | Medium | Shown |
| `interview-cut` | Customer or expert, cut to one point per clip | Short video | High | Quoted |
| `text-post` | Written post, one argument | LinkedIn, X, Threads | Low | All three |
| `thread` | Sequenced written post, one idea per beat | X, LinkedIn | Low | All three |
| `carousel` | Text-led slides, one beat per slide | LinkedIn, Instagram | Medium | All three |
| `comparison` | Two approaches, one table, honest columns | Static, carousel, post | Low | Quoted |
| `annotated-shot` | A real screenshot with callouts | Static, post | Low | Shown |
| `newsletter` | Email, one argument plus one artifact | Email | Medium | All three |
| `long-form` | Article or documentation piece | Blog, LinkedIn article | High | All three |
| `static-ad` | Single image, paid placement | Meta, LinkedIn, display | Medium | Quoted |

---

## The specs

Each is a starting spec. The build fills in the blanks marked **fill** from the interview.

### `talking-head`

The backbone of founder-led content and the format the question bank feeds directly.

- **Ratio and duration:** 9:16 or 1:1, 45 to 100 seconds. Over 100 seconds needs a reason.
- **Beats:** hook (3 to 7s), the specific instance, the turn, the mechanism, the proof, the
  consequence, one-sentence close.
- **Production:** phone on a stable surface, window light in front of them, a lapel or the phone's
  own mic in a quiet room. Nothing else is required and most upgrades do not change performance.
- **Captions:** always, burned in, **fill** their font and placement.
- **The rule that matters:** one idea. The moment a second idea appears, it becomes a second video.
- **Fails when:** it is scripted word for word. Notes on the wall, not a teleprompter.

### `screen-walk`

The highest proof-to-effort ratio available to anyone whose work happens on a screen.

- **Ratio and duration:** 16:9 for long, 9:16 cropped to the active region for short. 60 seconds to
  12 minutes.
- **Beats:** cold open on the end state, one sentence of setup, the walk in near real time, one
  insider aside, the result on screen, an honest close on time and cost and limits.
- **Production:** any screen recorder, cursor visible, **fill** whether faces appear.
- **The rule that matters:** keep the part that goes wrong. It is the credibility.
- **Fails when:** it is a polished demo. A demo is a sales asset, a walk is content.

### `vo-stills`

Voice over stills, generated imagery, or slow footage. Works when the subject cannot be filmed.

- **Ratio and duration:** 9:16, 30 to 75 seconds.
- **Beats:** one image per idea, image changes on the sentence break, never mid-sentence.
- **Production:** voice recorded first, images cut to the voice. Never the reverse.
- **Cost note:** this is the format that spends money. Approve the stills before any motion, always.
- **The rule that matters:** the image shows the specific thing named in that sentence. A generic
  image under a specific line makes the line read as generic.

### `build-breakdown`

Something specific was built. This is how, including the wrong turns.

- **Duration:** 4 to 15 minutes video, or 800 to 1500 words written.
- **Beats:** the problem in one paragraph, the constraint, the first attempt, why it failed, the
  approach that worked, the artifact, what it cost, what it still cannot do.
- **The rule that matters:** the failed attempt is mandatory. A breakdown with no failure is a
  brochure.

### `before-after`

- **Ratio and duration:** 9:16 or 1:1, 15 to 40 seconds, or a single static.
- **Beats:** the before, held long enough to be read, the transition, the after, the measure.
- **The rule that matters:** the measure is a number and it is real. Without a number this format is
  a claim with a nice transition on it.

### `interview-cut`

- **Duration:** 30 to 90 seconds per cut, many cuts per recording.
- **Beats:** the question on screen as text, the answer, nothing else.
- **The rule that matters:** one point per clip. A five-minute interview is eight clips, not one.
- **Consent:** written, before recording, covering the platforms it will appear on.

### `text-post`

- **Length:** 80 to 250 words. The first line is the hook and stands alone.
- **Beats:** hook, the specific instance, one idea per line, the turn, the position.
- **The rule that matters:** conjunctive flow. If a line can move without the post noticing, cut it.
- **Fails when:** it ends with an engagement-bait question. One real question or none.

### `thread`

- **Length:** 5 to 12 beats. Each beat stands alone and earns the next.
- **The rule that matters:** the last beat is a position, not a summary of the thread.

### `carousel`

- **Ratio:** 4:5 or 1:1. 6 to 10 slides.
- **Beats:** slide 1 is the hook and does one job. Slides 2 to n are one idea each. The last slide is
  the position or the single next step, never both.
- **Typography:** **fill** their type scale, colours, and grid. This is where drift starts, so the
  spec is exact.
- **The rule that matters:** the deck reads without the caption. The caption is a bonus.

### `comparison`

- **Form:** two columns, three to six rows, one honest disadvantage in their own column.
- **The rule that matters:** the honest disadvantage. A comparison where one side wins every row is
  read as an ad and dismissed.

### `annotated-shot`

- **Form:** a real screenshot, two to five callouts, nothing decorative.
- **The rule that matters:** it must be a real screenshot from real work, with redaction where
  needed. A mockup fails the shown tier.

### `newsletter`

- **Length:** 300 to 700 words, one argument, one artifact, one next step.
- **Beats:** subject line as the hook, the instance, the argument, the artifact, the step.
- **The rule that matters:** one artifact per send. A newsletter with four links gets none of them
  clicked.

### `long-form`

- **Length:** 1000 to 2500 words.
- **Beats:** the question, why the obvious answer is incomplete, the evidence, the position, the
  limits of the position.
- **The rule that matters:** the limits section. It is the part that gets it shared by people who
  disagree.

### `static-ad`

- **Ratio:** 1:1 and 4:5 at minimum, 9:16 if placements need it.
- **Beats:** one claim, one proof element, one identity mark. Three elements, no more.
- **The rule that matters:** it is legible at thumbnail size on a phone. Check it at 25 percent
  before approving anything.
- **Compliance:** **fill** whatever their regulator or the platform requires.

---

## Adding a format that is not here

Allowed, and expected eventually. The requirements are the same as any format file:

1. A name and an id.
2. What it is, and the one situation where it beats every other format in the library.
3. The spec: ratio, duration or length, and the named beats.
4. The production requirements, honestly stated.
5. The one rule that makes it work and the one thing that kills it.
6. Two real examples, at least one of them the operator's own.

Without all six it stays a variant, not a format, and variants drift. That is the canonical format
law in `05-doctrine.md`.
