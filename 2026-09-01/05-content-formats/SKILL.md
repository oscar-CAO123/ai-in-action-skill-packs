---
name: content-formats
description: >
  The canonical craft skill for writing and producing content: ad scripts, ad copy, hooks, VSLs,
  posts, carousels, statics, short-form and landing copy. Holds the thinking and the writing craft,
  then routes to the format skills under formats/ for the build. Trigger on "write an ad", "write a
  script", "write copy for this", "write a hook", "make a carousel", or any request to produce copy
  or creative.
canonical: true
---

> **Read this first.** This file came out of a working content engine and its `references/` and
> `config/` paths pointed at one company's brand kit, hook bank, persona set and model routing table.
> Those were removed before publishing, because copying them would make your output look like
> somebody else's. Everywhere below that names a missing file, put your own at the same path. See
> `README.md` in this folder for what each one held and how to rebuild it.

# house Content , the canonical engine

One skill for every piece of house content. It holds the thinking and the writing craft, and it
hands off to the production skills when a locked script needs to become a finished asset.

Two jobs, in order. **Write it right, then build it right.** Most failures happen in the first
job and get expensive in the second, so the gates below sit before spend, never after.

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

## 0a. The interview, before you write a word

One question at a time. Never paste the list. Skip whatever Phase 0 already answered.

**The business**
1. What do you sell, to whom, and what does it cost.
2. What does the buyer believe before they meet you that you have to change.
3. What is the one thing you want someone to remember a week later.

**The evidence**
4. What can you prove? Numbers, named customers, screenshots, results.
5. Where did each of those come from, and is it published anywhere.
6. What may never be claimed.

**The voice**
7. Paste three pieces of your own copy you were happy with, and say what you liked about each.
8. Paste one you hated. What was wrong with it.
9. What words does your business never use.
10. Formal or blunt? Australian or American spelling? First person singular or plural?

**The look**
11. What are your brand colours and typefaces, and where is that written down.
12. Show me two pieces of creative from anyone at all that you wish were yours.
13. What visual thing would be instantly wrong for your brand.

**The job**
14. What is this piece for: attention, teaching, or a sale? Only one of the three.
15. Where will it be seen, at what size, and with sound or without.

Confirm all fifteen back before drafting. What you learn in questions 7 to 13 is what the removed
brand kit and hook bank used to hold, so write it down as files and stop re-asking.

---

## 0. Load order (do this before writing a word)

Read in this order. Stop and flag anything missing rather than guessing.

| Order | File | What it gives you |
|---|---|---|
| 0 | `references/spine.md` | **What good looks like.** The canonical entries: a piece of copy that worked, the structure underneath it, and the mechanism. Read this first, every time. |
| 1 | `the business/projects/content-engine/engine/config/brand-kit.house.md` | palette, typography, voice gate, banned tokens, aspect specs, visual do/don't |
| 2 | `the business/projects/content-engine/engine/config/content-strategy.house.md` | the barbell, the format families, the operating contract |
| 3 | `references/canon/angles-and-formats.md` | the strict angle matrix (A1-A12) and the strict format list (F1, F2, F3, F5, F7). Ideation picks from here only |
| 3a | `references/canon/model-routing.md` | **which model owns which shot type**, with every id and parameter verified off your generation platform CLI. Load before anything is generated. Retro and authentic shots go to your cinematic model, design and type-led plates to your design model, object-into-scene to your image model, multi-shot video to your video model, video edits to your video edit model |
| 4 | `references/hooks/HOOKS.md` | **the hook bank.** Every hook structure house has: the mechanics floor, the scraped template library, the house's own hooks per pain, and the cleared concepts. Fill from here, never free-write a hook |
| 5 | `../../context/personas/personas-and-avatars.md` | Part 0 the industry spine (which of the 21 report industries a persona belongs to), Part 1 the approved callout list, Part 2 the persona detail behind every code, Part 3 the census that decided the list |
| 6 | `formats/<format>/SKILL.md` | the build spec for the chosen format, including its Faceless Reframe doctrine section |
| 7 | `../../context/research-corpus/INDEX.md` | **the discovery corpus, industry first.** 21 industry playbooks in `industries/`, 13 objection pages in `objections/`, 33 pain themes in `pains/`, 297 company profiles in `companies/`. `MARKET.md` is the corpus rollup: industry distribution, weighted pain, objection resolve rates. The angle almost always starts here |
| 7a | `../../context/research-corpus/industries/<slug>.md` | **the playbook for one industry.** Ranked pains in the owner's own words with an angle for each, ranked objections with a pre-empt-in-the-ad and a rebuttal-on-the-call line, the language they use and the language to avoid, a lead magnet, three carousel concepts, targeting, and the raw evidence behind all of it. Read this whenever the work is vertical-specific |
| 7b | `references/candidate-knowledge-base.md` | **the evidence layer for builds, tools and workflows.** Load whenever the copy will name what to build, which tools to use, or how a workflow is structured. 177 validated Hub builds for the structure, 483 candidate interview summaries for the named tools |
| 8 | `references/scripts/` | the written work: archetypes, the core-pain VSL scripts, the a reference brand teardowns, the raw idea dump |
| 9 | `references/canon/CONCEPT-BANK.md` | worked examples per pain (reference, never lift lines verbatim). `references/canon/objection-bank.md` carries the 13 canonical objections with how often each is raised, how often the rep closes it on the call, and a pre-empt and rebuttal pair per industry |
| 10 | Section 8 below | the evidence layer distilled from 1,954 scraped posts |

Background, read only when the question is about the account rather than the asset:
`references/meta-ads-media-buying.md`. Everything in it that touches scripting or creative is
already folded into this skill. `references/ai-tells-banlist.md` is the sweep checklist for
section 1's banned vocabulary.

**`references/spine.md` is the single source of truth for what good looks like.** It is the
one file that outranks everything else in this list, it is house-first, and it grows
perpetually: you feeds a source, it gets extracted on the spot, and every entry needs his
approval before it is canon. Entry shape and intake rules are in `references/README.md`.
Everything above now lives inside this skill's folder (`references/`), which is the point: one folder holds the craft, the canon, the hooks, the scripts and every format skill.

If the brief names a specific format, also load that format's production skill (section 9)
before scripting, because the format constrains the script. Read that format's subdivision in
**section 7c** at the same time: it names what the format does to the words and narrows the 66
spine entries to the ones that apply to it.

---

## 1. Universal hard rules

These never bend, in any mode, for any audience.

### The citation law

**Nothing is generated without a concrete reference from the bank, and the reference is shown
with the generation.** Not a description of a reference, an ID that resolves: `arch:S6`, not
"modelled on a job ad". Every format declares what it is modelled on, the copy shape first and
then the layout or look, and the id is resolved by a gate rather than trusted because it was
typed. A format with no reference does not get generated until someone picks one.

```bash
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 refs.py                       # the banks and what is citable in each
python3 refs.py list arch             # the ids in one bank
python3 refs.py show arch:S6 --open   # the entry, and the picture where there is one
python3 refs.py check hook:S1 arch:S6 # exits 1 on a dead id
```

Seven banks, resolved live off the source files so a new bank entry is citable with no second
copy to maintain: `hook` (the copy structure the headline fills), `arch` (the archetype it
imitates), `tear` (the doctrine it obeys), `hex` (the measured corpus shape), `swipe` (a real
competitor ad that ran and kept running), `tpl` (a Figma layout extract), `local` (a reference
image a format was built on) and `style` (a locked plate look).

**It is serviced on request.** Anything shown to you carries its reference: `sheet_fmt.py`
draws a MODELLED ON strip above the cards with the referenced images thumbnailed, and
`suite_copy.py --fmt <F>` prints each id with its title and the file and line it lives at.

### The bottom-band law (layout
**Scope: every type-led frame**, meaning any frame where the type IS the design. That is the
statics (F7), every carousel slide (F5), and any title, hook or quote card set as type on black.
It does not govern type laid over motion, which has two standing treatments of its own: the
one-word Poppins captions that sit dead centre (F1, F2, F3), and the persistent top hook in the
talk-show format. Those stay where they are until you rules otherwise.

On a type-led frame, every mark lives in the **bottom 1.5/4 of the frame**. At 1080x1350 that
band is 506px tall, top edge y=844. Nothing renders above that line.

The band carries **one block of type and nothing else**: one size per frame, white, with a
single blue accent. No kicker, no standfirst, no second type tier, no rules, no logo. A grey
secondary tier is banned outright, it is what made every earlier pass read small.

The face is set per format by a `band.py` theme, not by this law. Statics run `anton`; the
news-carousel format runs `noir` (your display typeface 200 caps) as of . Everything above holds either
way.

The block is **set flush on both margins and fills the band**, top to bottom and edge to edge.
Line breaking is a fit decision the renderer makes, not an authoring one: write the copy, let the
rig break it. Justification goes into the word gaps before it ever goes into the letters.

Reference implementation, copy this mechanism into any rig:
`skills/content-formats/formats/static-ads/scripts/build.py`, and section 0 of `skills/content-formats/formats/static-ads/SKILL.md` for the traps
(the fallback-metrics font trap in particular).

**The two exemptions, and there are no others).** Both came out of the carousel
reference batch in `projects/content-engine/engine/reference-bank/carousels/`, and each one is
named to a specific layout so it cannot spread.

1. **The seam.** In the stacked photographic variant of F9 `before-after-splitscreen`, two
   full-bleed photographs meet near mid-frame, both graded down to near black where they meet, and
   the copy sits inside that shared darkness. The type IS the seam, so the frame renders outside
   this law. Nothing else may put type above y=844 on that basis.
2. **The information slide.** A slide built to be stopped on and read rather than glanced at:
   comparison boxes with a verdict column, numbered spines, two-state ladders, mounted artefacts.
   It carries more than one type size and sits outside both this law and the section 7b character
   budget, with its own scale. **A carousel may not be all information slides**: the cover and the
   close stay ordinary band cards. See section 7b.

Everything else stays inside the band, including the mounted-artefact curation layout, whose title
line folds into the band above its caption line rather than sitting at the top of the frame.

### The education law
**Every pain-led or callout asset teaches before it offers.** Naming the pain and cutting
straight to "here is how we help" is banned in every format. The pain opens a question, the
teaching is what answers it, and house arrives as the conclusion of the lesson.

What the teaching beat looks like: the five easiest automations that business can build this
week, the three that close all eight of those admin gaps, the one mistake that makes AI fail in
that industry, the ranked list, the walkthrough of the actual system. Real builds only, sourced
from your content store, never invented.

**The gap stays open.** The hook raises exactly one question, the teaching pays it off, and the
offer lands after the reader already got something they can use. If a draft goes pain, pain,
pain, then a link, it is unfinished.

**Where it lands per format.** Video and carousels carry the teaching in the runtime or the
slides. A single static card has one beat, so its card carries the hook and the teaching lives
in the primary text; the card still has to point at the lesson rather than at the booking page.

### The evidence law: builds, tools and workflows come from the knowledge base

**Never invent a build, a tool, a stack or a workflow.** Any time copy names what a business
should build, which tools it should use, or how a workflow is put together, it comes from the
the business candidate knowledge base, because that is the record of what has actually been
validated and shipped. A plausible-sounding automation invented at the desk is the same failure
as an invented number.

- **The workflow structure** comes from the Hub `builds` table (177 published builds):
  `problem`, `solution`, `replicate_steps`, `what_worked`, `what_didnt`, `pitfalls`, `outcome`,
  `time_to_deploy`, `industry`. Pull the build that matches the pain, then write from it.
- **A named tool** never comes from the Hub's `stack` field, which is abstracted to categories
  by design ("an automation platform", "a fast LLM"). It comes from your content store interview evidence
  or the Hub's vetted repos and accounts, and it carries the same discipline as a number: name
  the tool only where the evidence names it.
- **The counted stack, 483 candidate interview summaries, :** Claude 198,
  ChatGPT/GPT 102, n8n 71, your content store 37, Python 29, Gemini 26, Cursor 24, Lovable 17, Zapier 16,
  Copilot 16, LangChain 15, Notion 11, Twilio 11, HubSpot 9, Airtable 8, Salesforce 7,
  Make.com 6. Lead with the top of that list, because it is what the market actually runs.

Queries, table shapes and the refresh procedure: `references/candidate-knowledge-base.md`.

### Em dashes
Zero, ever. Replace with a comma, a period, a colon, or parentheses. This includes en dashes.

### The negation swap (banned everywhere)
Never build a line on stating what a thing is not in order to state what it is. All of these
are out: "it's not X, it's Y", "that's not X, that's Y", "not because X, but because Y",
"not by doing X, but by doing Y", "that's an X, not a Y". Say the positive thing directly,
in a full sentence with a subject and a verb. If a draft contains one, rewrite the line
before anyone sees it.

This ban has no exceptions. One was carved out for an objection pre-empt on and
reverted the same day when the clause it existed for was cut from the script.

### Other banned patterns
- Three-beat staccato used dramatically ("Build. Ship. Repeat.")
- "And the X? Y." / "The result?" / "The outcome?"
- "No X. No Y. Just Z."
- "There's a kind of X that isn't Y. It doesn't come with..."
- Two-word dramatic phrases repeated two or three times in a row

### Banned vocabulary

**house terminology is canonical.** Read `the business/context/language-rules.md` before writing.
Standing rules: never "building business", always "construction business". Never "your venue",
always "hospitality business". Name the reader's business by its industry plus the word business.
**Grift register:** leverage, leveraging, seamless, seamlessly, navigate, navigating, empower,
empowering, unlock, unlocking, harness, harnessing, game-changing, game-changer, revolutionary,
revolutionise, cutting-edge, transformative, robust, synergy, supercharge, next-generation,
paradigm shift, "this changes everything", level up, elevate, master the art of, a testament to,
significant milestone, thought leader, passionate about, dedicated to.

**AI clichés:** "in the age of AI", "as AI continues to", "with the rise of AI", "AI-powered"
(say what it actually does), "the AI revolution".

**Hype intensifiers:** huge, massive, incredible, amazing, unbelievable, stunning, remarkable,
unprecedented, world-class, must-read, must-have, "you won't believe".

**Throat-clearing:** "in this article/guide/post", "it is important to note that", indeed,
furthermore, moreover, subsequently, accordingly.

The pipeline enforces this list verbatim in `engine/nodes/common.py` BANNED_WORDS. Keep the
two in sync when either changes.

**Master banlist:** `references/ai-tells-banlist.md` is the exhaustive register behind this
section (every known AI-tell word, phrase, sentence structure, formatting habit, and
per-channel giveaway, researched from Wikipedia's Signs of AI writing, the
tropes.fyi directory, and a dozen community and industry lists). The lists above stay the
always-loaded core; run the master banlist's sweep procedure on every draft before the QA
gate in section 10.

### The removal test
If you remove a word and the sentence still works, remove it.

### Specificity
Every vague claim costs trust and every specific detail buys it. "Sixteen years" beats "many
years". "$5-6k a month" beats "expensive". "Turning over $5M or more" beats "established".
When you cannot be specific, ask you for the specific. Never invent a number.

### Register floor
- **Contractions always.** Write to ONE owner, one human to one human, never "business owners".
- **Australian register:** measured, dry, credible, slightly skeptical of hype.
- **No overclaim.** Trust is existential for this brand. Underpromise.

### The conversational modulation pass (mandatory second pass on anything spoken)
Draft for structure and truth first, then modulate for the ear as a deliberate second pass
(full rules and before/after pairs: `.claude/skills-library/conversational-modulation.md`). The load-bearing
five: make a human the subject (automations never sound self-building), specificity at the level
of the mechanism (name the actual thing), compress as readily as you expand, keep the spoken
connectives (and, but, so, because, see, now), unpack an abstraction in the same breath.

### Write for the ear
Anything spoken (VO, UGC, VSL, ad script) gets a second pass for naturalness after the
structural draft is right. Keep the spoken connectives (and, but, so, because, see, now).
Give every contrast a subject. Unpack an abstraction in the same breath you use it. Close
relational rather than mechanical.

---

## 3. Voice registers (pick one, never mix)

**Register 1 , cinematic.** For the futuristic-Australia brand films. Short, declarative,
built for VO. Measured, credible, future-facing. The rhythm to mirror: "Australia is not
waiting for the future." / "A new role is being written into the org chart. Chief Agent
Officer." / "We find the people who build what comes next."

**Register 2 , faceless performance.** For the canonical performance ads. A distinct, casual,
deep Australian voice. Dry and unhurried, talking to one owner like a mate who has seen behind
the curtain. Slightly cheeky, never smug, never hype.

Both are Australian, both are banned-word clean, both run one idea per line. Register 1 lands
on a brand beat. Register 2 lands on a decision.

---

## 4. Mode dispatch

| Mode | Trigger | Structure |
|---|---|---|
| **Ad script (short-form)** | "ad script", "video ad", "reel script" | Pick a spine (section 5). Five hook variants, body, CTA. Stage directions in parens. |
| **Ad copy (static / Meta)** | "ad copy", "static ad", "Meta copy" | Opening line (pain or hook), benefits as short dashes, CTA. Every line earns its place. |
| **VSL / long-form** | "VSL", "sales letter", "long-form" | Full awareness ladder (section 6). 1,500 to 3,500 words. |
| **Hooks only** | "hooks for", "give me hooks" | Ten minimum, graded against 4.3, spread across the archetypes in section 7. |
| **Carousel** | "carousel", "swipe" | One idea per slide, slide 1 does the whole job alone, last slide carries the action. |
| **LinkedIn post** | "LinkedIn post" | One thought per line, blank line between every line, hard cut at peak curiosity before "see more". |
| **Organic short-form** | "reel", "TikTok", "organic script" | Hook, buildup, payoff. Conversational and opinionated. |
| **Landing / page copy** | "landing page", "pain page" | Route to `pain-page` skill for structure, write the copy here. |

Ask the mode-specific questions before writing. Context first, copy second. If the brief
already answered something, do not re-ask it.

**Always confirm:** audience (A or B), the one pain or angle, the CTA, the length or runtime,
and which spine or archetype. Guessing any of these produces work that gets thrown away.

### The production table (the locked schema for any video script)

Every video script is written as this five-column table. Folded in from `ad-scripting` .

| Section | Script | Shot List | Filming Location | Music/Tone |
|---|---|---|---|---|

- **Sections in order:** Hook, Context/Problem, Difficulty, Teach, Solution, Payoff. Each gets
  several rows, and a 45 to 60 second video runs 12 to 20 rows. The Teach row is the education
  law's beat and it is not optional.
- **Script column:** spoken voiceover only. Read end to end it has to sound like one coherent
  voiceover rather than caption fragments. Captions belong in the Shot List column, written as
  `Caption: "TEXT"`.
- **Shot List column:** camera angle, framing, movement, what is in frame, props, captions.
- **Filming Location:** real locations, aiming for four or more for visual variety.
- **Music/Tone:** a tonal shift at each section boundary, where the music builds (usually Teach
  into Payoff), where silence lands, and the overall mood.

---

## 4b. The ad-script workflow

The order that produces a script worth rendering.

1. **Start from the mined pains.** They are already mined. `context/research-corpus/MARKET.md` ranks the
   15 pain labels by weighted severity across 238 discovery calls; `industries/<slug>.md` gives that
   industry's pains in the owner's own words with an angle already written for each; `pains/<slug>.md`
   holds the record-level evidence and `context/personas/personas-and-avatars.md` the verbatims behind
   them. Pull the phrases you will build hooks from. Never invent a pain and never re-mine.
   **Rank on the report weighting, not on wiki record counts.** Record counts measure how often a pain
   was extracted; the weighting measures how badly owners said it hurt, which is what should drive the
   draw.
2. **Pick the concept: persona x angle x offer.** One avatar, the belief you attack, the
   destination. One concept per script. If the same angle writes three ways, that is one concept
   with the wrong persona count.
3. **Choose the format last** (section 9 and angles-and-formats.md). Default to short-form VO video or
   the pain stack.
4. **Write five or more hooks** for that concept (section 7). Index the first half on proven
   shapes, tag each by type and angle, vary visual against copy against audio, run the scroll
   test on every one.
5. **Draft the body as the production table** (section 4). Agitate before the solution, apply
   the voiceover rhythm rules, walk the awareness stages, cut any line the footage already shows.
6. **Place the teach beat** before the offer. Section 1's education law, and V9 in
   `references/scripts/archetypes.md` is the menu it draws from.
7. **Land the offer and close.** Frame it on the employer's live objection, keep it soft and
   direct, put the proof in the reframe.
8. **Check retention:** four to five mechanics present.
9. **Run the QA gate** (section 10), then present for review in Cursor.

**Produce in volume.** Many concepts across avatars, and spend decides the winners. Nobody picks
the winner before launch.

---

## 5. The two canonical ad spines

**Before the spine, the concept.** A concept = persona x angle x offer, built in that order,
format last. Persona from personas-and-avatars.md (general-pain default, callout only from the approved
list). Angle from angles-and-formats.md (A1-A12, rotation pool per its rules). Offer: house flagship,
AI Officer, or the entry-level role. Diversity means new persona x angle concepts, never three
thumbnails on one line; and the portfolio model applies: many concepts clearing the quality bar,
spend decides the winner, nobody predicts it.

Both spines run through identical production. Picking a spine is a scripting decision.

### Spine A , the Reframe
Use when the job is to expose a con and reframe the smart move. The anti-consultant,
anti-guru, ownership scripts.

1. **The provocative claim.** The agitation-led hook. The felt problem or the truth bomb.
2. **Expose the con.** You pay a consultant for a discovery call and a slide deck. A contractor
   juggling ten clients. A guru's course. You do not get an owner.
3. **Prove the real substance.** The embedded operator, the systems running, the week that
   becomes minutes, the work actually getting owned.
4. **Reframe and name the move.** house arrives here and only here.

Name house as late as the runtime allows. Beats 1 and 2 are all problem and con.

### Spine B , the Direct Callout
Use when the pain is already conscious and the job is to be found fast by the right avatar.

1. **Callout.** "If you run an Australian construction business turning over $5M or more"
2. **Problem.** One ranked pain, in their words, fused into the same opening line. A naked
   callout on its own fails the hook grade.
3. **Teach.** The education beat, and it is mandatory (section 1). The five automations that
   fix this, the three mistakes that make it worse, the ranked list, the walkthrough. They get
   something usable here whether or not they ever call.
4. **Solution.** The full-time embedded operator who owns the systems. Name the mechanism.
5. **CTA.** Restate callout and problem, then one action.

Spine B names house early, which suspends the late-naming rule. One avatar and one pain per ad.
Swapping industry and pain against a locked skeleton is how spine B batches into volume.

**Beat 3 is what separates this from the version that failed.** The old canonical spine B ran
callout, pain, "here's exactly how we help", CTA, and it was cut on for exactly that
reason. A callout that arrives at the offer without teaching is a brochure with a name on it.

### Spine C , the Story
Use when one real, specific incident carries the argument better than any claim about it. It is
format-agnostic: it runs as a LinkedIn post, a VSL open, a talk-show monologue, or the spine of
a still-frame film. Folded in from the LinkedIn storytelling engine .

1. **Hook.** Drop into the scene, no preamble. "Three in the afternoon on a Friday and the
   quote still wasn't out."
2. **Setup.** One or two lines. What the situation was.
3. **Tension.** What went wrong, with numbers, times and physical details.
4. **Action.** What was actually done, first person, active verbs.
5. **Resolution.** How it ended. Tight.
6. **The lesson.** One line the reader can use tomorrow. **This is the education beat**, so it
   has to be genuinely usable rather than a moral.
7. **CTA, optional.** A question, or a soft mention.

**The chaos is the content.** Do not soften it. Specificity creates credibility, credibility
earns trust, and trust is what moves the decision. A story told at low resolution persuades
nobody, because the detail is the only part that proves you were in the room.

**Five openers for beat 1.** Result or chaos (lead with what happened). Giveaway (lead with the
value of the thing being handed over). Stakes (what is changing and why now). Contrast (before
against after, then against now). Direct statement (name the thought the reader has and never
says out loud).

**The house constraint on this spine:** the incident has to be real and it comes from a discovery
call or a placement, attributed by role and never by name. An invented anecdote fails the same
test as an invented statistic.

---

## 6. VSL awareness ladder

For long-form only. Do not skip a stage.

| Stage | Reader state | Job |
|---|---|---|
| 1. Unaware | Does not know they have a problem | Open on a person experiencing the problem in vivid specific detail. No product. |
| 2. Problem-aware | Recognises it | Three-point preview escalating in severity. Name the villain as a system. |
| 3. Solution-aware | Wants a fix | Introduce the mechanism with specificity. Plain language. |
| 4. Product-aware | Understands the fix | house as the natural extension. Lead with the standard, call out the fakes. |
| 5. Conversion | Ready | Risk reversal, two-path close, callback to the opening, one CTA. |

Deploy when the brief warrants: misconception hook, root-cause deepening (go one level past
the obvious, your answer lives on the third level), anti-category education (why most options
in the category fail, before yours arrives), relationship stakes, peer social proof over formal
testimonials, supply-based urgency that is actually plausible.

---

## 7. Hook craft (the full doctrine

Hooks carry roughly 80% of view-through. For the same hour of work, 15 hooks x 2 bodies beats
2 hooks x 5 bodies nearly always. Grade every hook before the script is written.

### Hard rules
- 1-3 seconds. Leads with payoff or provocation, never context.
- Creates exactly ONE question that only watching can answer; the body closes the loop, the
  hook never resolves it.
- Always has voiceover (the silent text-on-screen static is the one tested exception).
- Three independently changeable layers: visual, on-screen copy, audio. Change one and
  performance swings; Meta reads a different hook as a different creative, so hook rotation is
  near-free volume (fatigued bodies revive on fresh hooks).

### The six mechanical TYPES
Incomplete Sentence · Curiosity Gap · Action Drop · Visual Provocation · Stakes/Counter ·
Self-Aware Comedy (sparingly for house: credible, never crass).

### The ten ANGLE labels (tag every hook with one)
[Discovery] · [Authority] · [Problem Agitation] · [Guilt/Empathy] · [Us vs Them] · [Founder] ·
[Callout] · [Data/Stat] · [Contrarian] · [Curiosity].

### The nine hook types that scale (Meta canon)
Problem agitation (problem-aware only) · contrarian truth (all awareness levels) · specific
proof · curiosity gap · truth bomb (exceptional where price is the objection, which it is for
house: confront the salary up front) · psychological confrontation · sensory/ASMR (weak house fit) ·
founder's letter (must be true) · social proof.

### Grading (five criteria; a couple done well beats 10/10 on all)
1. **Clarity**: a stranger understands it inside 3 seconds.
2. **Relevance**: the problem, never a naked persona callout; nobody wants to hear themselves
   called out, they want their problem named (spine B resolves this by fusing callout into pain).
3. **Novelty**: purple ocean, novel but adjacent to proven demand.
4. **Specificity**: unrounded numbers, names, quantified outcomes out of the gate.
5. **Credibility**: usually carried by the visual, not the copy.

### Generation principles
Index on winners first (40-50% of hooks vary proven angles before new territory) · education-first
dominates (expose a problem they did not know they had; best performer across every you client) ·
the 7am scroll test · first-person means a real founder or operator, never an actor · label every
hook by type and angle · ten minimum per brief across at least four types before one gets picked.

### Bridges (the part everyone botches)
Two bridges exist: hook to body, and body to CTA. The failure mode is the step change: great hook
straight to product. Walk the viewer through awareness inside the ad (unaware, problem-aware,
solution-aware, product-aware) and introduce house as late as the runtime allows (spine A; spine B
suspends this). A wide hook jumped straight to "book a call" has never been seen to convert.

### Voiceover rhythm (scripts are spoken, not read)
Narrative logic end to end (read the script column aloud) · "but" as the problem pivot · "and so"
as the consequence connector · plant a re-hook question before the payoff so it lands as an
answer · cut any line the footage already proves.

### Retention mechanics (aim for 4-5 per script)
Word-per-second captions · physical props for text · match cuts · hand-drawn diagrams · reaction
shots · archival/screen B-roll · branded outro card · clean-loop ending.

### Educational conventions (house is education-first, never UGC or testimonial)
Every hook teaches the owner something genuinely useful, then the body reframes to the hire.
The proven shapes: the N-things checklist ("The 5 AI systems every construction company should
be running in 2026") · the capability reveal · problem-first teaching (root cause, then the right
way) · myth-bust category education · the build walkthrough (name real builds, real specifics) ·
the direct educational callout ("Construction business owners, here are the three jobs you should automate first").

### Hook shapes that have actually won (adapt the shape, never the words)
- "For the love of God, whatever you do in an interview process, do not forget to ask the high
  performer question." (517k)
- "Hear me out. There's something I've learned about the most successful people, and that is
  that they're very good at staying private." (88k)
- "The biggest gold rush in the past 25 years is right now, but you're getting left behind." (54k)

The house adaptations already written: "Whatever you do this year, do not make the hire that every
growing business gets wrong." · "There's something I've learned about the businesses pulling
ahead right now, and it's more than more staff." · "The biggest shift in how businesses run in
25 years is happening now, and most owners are getting left behind."

### Hook rotation is near-free volume (post-Andromeda)
Meta reads a changed hook as a different creative, gives it its own creative ID, and reaches a
novel audience with it. Record six hooks in one session and you have six variants. Ads that had
spent $50k to $100k and fatigued have been revived with fifty new hooks for another $100k of
spend at the same efficiency, off roughly an hour of work. Two uses: keep a winner alive, and
resurrect an ad whose body was good and whose hook rate was not.

**Trial reels test hooks for free.** Post them on a business or personal page before spending a
cent. You get comparative virality and a retention graph showing exactly where viewers left, so
you learn whether the hook, the bridge or the body is broken, inside 24 hours. Post twenty hook
variants, load the best five into Ads Manager. (Current as of April 2026, algorithm-dependent.)

### Hook failures to catch
A naked capability line is not a hook. A question mark does not make a hook. A callout with no
pain attached does not make a hook. Anything a competitor could run unchanged is not a hook.

---

## 7b. Writing for the band (every silent card: statics, carousel slides, title cards)

Section 7 is written for copy that is spoken. A band card is silent, has no voiceover to carry
it, and gets one block of type at one size. The constraints below are not style preferences,
they are what the renderer does to the words.

### The character budget (measured off the rendered cards, Type size falls off as the square root of the character count. Across seventeen rendered cards
the relationship holds to about 20%:

    size in px  ~=  887 / sqrt(characters)

| Want the card to read at | Write no more than |
|---|---|
| 140px, the hardest-hitting cards | 40 characters |
| 120px | 55 characters |
| 100px | 79 characters |
| 90px, the floor for headline weight | 97 characters |

**Under 90px a card stops being a headline and becomes a paragraph.** The 8-item checklist static
runs 274 characters and lands at 52px. That is the diagnosis, not the rendering: cut the copy.

Two cards came in under their predicted size because their words were uneven in length. The
renderer sets every line flush to both margins, so lines that want very different sizes cost the
whole card. **Words of similar length buy you type size for free.**

### The rules

**One idea per card, one blue accent, on the surprise.** The accent goes on the number or the
role, whichever the reader did not see coming, never on both.

**Write whole sentences, never lines.** The renderer re-breaks everything to fill the band, so
any construction that depends on where a line lands is lost. The hand breaks in `ads.py` and
`decks2.py` are a reading hint for whoever edits the copy, nothing more.

**One sentence per card.** Two sentences on a single card run together into one wall, because
nothing separates them: no leading change, no colour change, no rule. "Six or seven handoffs a
job. The seam belongs to nobody." reads as one confused sentence at 92px. If the second sentence
earns its place, it is a second card.

**Every card carries a number, a name or a comparison.** A card that is pure assertion has
nothing for the reader to check, and at this size there is no voiceover and no footage to carry
credibility. Section 7's specificity criterion is the whole game here rather than one of five.

**Numbers keep the scope their source supports.** A figure from one discovery call says one
business, on the card, in the same sentence. See section 8.

### The information slide (new class

Everything above governs a **band card**: one block of type, one size, in the bottom band. The
information slide is the second class, and it is governed by none of it.

**What it is.** A slide built to be stopped on and read rather than glanced at. It carries several
type sizes and a drawn structure, and its job is to hand the reader something usable. The four
structures evidenced in the reference bank, in order of strength:

| Structure | What it is | Reference |
|---|---|---|
| The artefact slide | A real document photographed at a slight tilt, floating with its paper edge and shadow visible, carrying a template and a filled-in worked example at once | `carousels/DaN90DTAMjQ` |
| The comparison box | Caps label, bold statement, grey support line, right-hand verdict in caps, one row per side | `carousels/DZ8Fv-LgH9z` |
| The numbered spine | Filled accent discs joined by a thin accent line, caps step name plus one line of instruction each | `carousels/DZ8Fv-LgH9z` |
| The two-state ladder | A hairline box of quotes, a large accent arrow, an accent-bordered box of quotes, border colour changing with the state | `carousels/DaN90DTAMjQ` |

**What still binds it.**

- **The cover and the close stay band cards.** A carousel may not be all information slides, or the
  reader never gets a slide they can read at a glance.
- **One accent per slide, on the payoff.** Same rule as a band card. The measured references hold to
  this even at 550 characters a slide.
- **One quotable closing line at the foot of a dense slide**, so the reader carries something out.
- **Everything in section 8.** Every number keeps the scope its source supports, and every structure
  it names comes from `context/research-corpus/` or a named Hub build.

**What is not settled.** The information slide's own type scale has not been measured. The band
budget above was measured off seventeen rendered cards on and this class needs the same
treatment before anything is shot. Until then, `527` to `578` characters a slide is the observed
working range on the references, at four type sizes, on pure black.

### The five-slide carousel arc

One job per slide, one line of argument each, about 45 to 60 characters:
hook, then the scene said once, then the cost with its scope, then the reveal that names the
the role you place, then the endcard.

Canonical references for the layout and the density are
`skills/content-formats/formats/news-carousel/scripts/out2/con-03-v2/slide-01..05.png`. **The copy in those renders is
not canonical** and is pending a refinement pass.

---

## 7c. The format subdivisions

The spine holds 66 entries and no single piece uses all of them. Pick the concept first
(persona x angle x offer), pick the format second, then load that format's shortlist here.
Entries outside a shortlist are still true; they are aimed at a different job, and pulling one
into the wrong format is the most common way a good move produces bad copy.

Each subdivision names what the format physically does to the words, then the entries to load,
then the entries to leave out and why.

### The universal floor (every format, every time)

| Entry | What it holds |
|---|---|
| E-001, E-002, E-003 | concept equals persona x angle x offer; a batch that only changed the visual is one ad; ship for the winners |
| E-007 | grade the script before anything is rendered, shot or painted |
| E-013 | the offer outranks the copy, so settle it before writing |
| E-018 | write to one person, never to a category |
| E-025 | research before writing: personas, pain wiki, discovery transcripts |
| E-034 | every bold claim gets its proof in the next beat, before the doubt arrives |
| E-040 | cold traffic kills the pure persona callout, the brand-name open and the pattern interrupt |
| E-048 | the contrast negation is banned outright |
| E-053 | write from their words, attributed by role, never by identity |
| E-054 | a number carries the scope its source supports |
| E-060 | the house category is level one to two sophistication, so the plain claim and the pain still carry it |
| E-062 | write to be consumed, sixth to eighth grade, nothing needing a second pass |
| E-064 | every element exists to buy the next one |
| E-066 | the draft comes back cut, and the cut gets written into the spine |

On top of that, the three video formats share a floor of their own: E-004 (visual, on-screen
copy and audio are three separately changeable layers, so hook rotation is near-free volume)
and E-006 (the wider the hook, the longer the walk before the product appears).

Portfolio-level rather than per-piece, so they govern the week rather than the asset:
E-009 (judge top-of-funnel on the audience it builds), E-010 and E-011 (read the number, name
the cause; platform ROAS is directional), E-012 and E-045 (build against the live objection,
one asset per objection), E-044 (60/40 pain-led), E-065 (the plus/minus grid, used at ideation
to find the angle).

---

### F1 · Guru clip, talk-show (`talkshow-vsl`)

**What the format does to the copy.** Twenty to forty seconds of one man talking to camera,
which is roughly 55 to 110 spoken words and nothing else. No cutaways, no second scene, no
props. The persistent top hook sits on screen for the whole clip, so it has to stay true from
the first second to the last and read in about six words. Kinetic captions mean every word is
read as well as heard, so a line that only works out loud gets caught on screen.

**The register.** Elder statesman. Certainty, no hedging, mild contempt for the con. He is the
credible third party in E-017 speaking in his own voice, so the authority claim never gets
handed to anyone else here.

**The teach beat: one build, plus its outcome.** The education law in
section 1 binds here like everywhere else, and this is how it lands inside the word budget. One
line names a real Hub build, the next line gives its recorded outcome scoped to one business.
The three-build trio belongs to F5, where three separate slides carry it: inside thirty-eight
seconds of one man talking, three builds eat the pain arc and land nothing, and they push every
script past the 110-word ceiling. Keep the two lines in one clip chunk so the mechanism and the
result land in a single breath.

**Load:** E-026 and E-027 (spine A, and house named at the reframe only), E-037 (the contrarian
claim, which is the natural opening for this face), E-046 (chain the takes and hold the gap
open, compressed to the runtime), E-036 (discomfort in the first three seconds), E-032 and
E-033 (context in line one, ten to fifteen words a sentence), E-035 (a second loop before the
fifteen-second mark), E-031 (keep the conjunctions, read it aloud before it locks), E-063 (a
question only where the honest answer is yes), E-061 (write against what the feed already
showed them), E-006 (a wide hook walks the awareness stages before the product appears).

**Optional:** E-055, the ranked list scored controversially low, is a monologue structure and
this is its natural home. It needs the full forty seconds and real builds from your content store. Spine B
(E-029) is also available when the pain is already conscious, and it suspends the late-naming
rule for that clip only.

**The three-system fork (full VSL mode only, LOCKED as the canonical style .** This is
the style for the format, approved off the reference implementation at
`formats/talkshow-vsl/IDEAS.md` V01, with the production detail in that format's SKILL.md
Phase 2. Write every full VSL against it rather than composing a new arc. The 45 to 90 second mode
does not compose an arc. It **forks one script** from `references/scripts/core-pain-vsl-scripts.md`
(18 written P/S/VSL scripts, one per core pain, all on the same canonical template) and modulates
a single block. Pick the script whose pain matches, keep its hook, its machine walkthrough and its
result beat in its own words, and change only this:

1. **The hook**, from the source script. Either the dream outcome as a question or the pain
   agitated, whichever that script uses.
2. **The turn.** "Well, you can. You just need these three AI systems." One line, and it goes
   straight on. An objection pre-empt sat here until ("and no, it's not hiring another
   admin") and was cut: it slowed the turn and bought nothing the three builds do not.
3. **Straight into the systems.** Cut the source's machine walkthrough ("so here's your
   business, the work comes in here"). The job of this script is to educate, so the runtime goes
   to the builds rather than to a second lap of the pain.
4. **Three AI systems, replacing the source's hire block. Each one is taught the same way: the
   tools, what it does, the outcome.** Every build is a published row in the Hub `builds` table
   (`references/candidate-knowledge-base.md` has the query). Take the tools out of that build's
   own `replicate_steps`, never out of the `stack` column, which is abstracted on purpose.
   Pick the three that remove the owner from three different parts of the loop, and drop any
   build the owner has obviously already tried.
   **Say the tools in the owner's language.** He does not know what LangGraph or a classifier
   model is, so naming them costs the line. Answer what he is actually asking, which is what it
   plugs into and what it touches: the software he already pays for, his inbox, his team chat.
   The real stack stays in the concept metadata as the evidence trail.
   **Name the system, never the outcome.** "The auto job dispatcher" and "the auto report
   builder" are names a system could carry. "The job that runs itself" is the result, and using
   it as the name spends the payoff before the teach beat arrives. Give each one a plain
   owner-legible product name, then say what it does, then give the outcome.
5. **The bridge.** One sentence between the third outcome and the CTA: all three are already
   running somewhere, and the gap widens every month it is left. Halbert 8, the last line is
   prime real estate, and a CTA that arrives cold wastes it. Keep the scarcity honest, since the
   register floor bans overclaim and trust is the one thing this brand cannot spend.
6. **The quiz CTA**, in place of the source's "there's only one place in Australia you can hire
   them", carried in on "so" rather than starting cold.

Roughly 120 to 240 spoken words. **The role is not named in this archetype**: the video teaches and the quiz result introduces the category, which is why the close
is the quiz rather than the 7e canon. The guru-clip mode keeps the 55 to 110 word arc and the
ordinary close.

**Rebuild, do not copy, the source's two pivot beats.** Those scripts were written and
run "But the fix isn't X, it's Y" and "Not by hiring your replacement, but by hiring someone",
both banned on 07-31. They sit inside the block this fork replaces, so the fork is clean by
construction. Read the source for structure, and take its wording only from the beats you keep.

**Leave out:** E-005 and E-050 (eight "if you" lines eat the whole runtime and the collapse
arrives with nothing left to spend it on), E-047 (no long-copy surface exists), E-024 (an
objection list needs length this format does not have), E-058 (the proof is a screen share and
there is no screen), E-028 (the con prop needs a shot the format cannot cut to).

---

### F2 · Painted animation with VO, noir-painterly (`noir-painterly`)

**What the format does to the copy.** Four to eight painted beats carry a deep Australian VO,
so every line has to name something paintable in the B&W oil-noir world: a machine, a seam, a
silhouette, a light. An abstraction with no image behind it costs a beat and shows nothing.
This is the highest-cost format in the canon, which makes the script the gate: the structure
gets proven cheap before anything is painted (E-051, read as a warning here rather than a
method).

**The register.** Image-first and metaphor-led. The words say the least the picture cannot.

**Load:** E-026 and E-027 (spine A, late naming), E-028 (put the con prop in frame, handle it,
then set it aside: the glossy deck, the van pulling away, the invoice), E-058 (the mess
becoming a map, which is the one shape where the visual is the proof), E-020 and E-021 (build
to the reveal, then land the number the story earned), E-043 (agitate, educate, repeat, one
loop per painted beat), E-022 (the identity: the owner who got out of the weeds), E-016 (the
fact under every adjective, since a painted world is already atmospheric enough), E-031 (one
idea per line, written for the ear).

**Leave out:** E-005 and E-050 (eight symptoms means eight paintings, and the stack is the one
concept that works pen-and-paper cheap, so it belongs in F3 or F7), E-047, E-024 (no long-copy
surface), E-055 (a ranked list is a talking format).

---

### F3 · Still frame with VO, nighthawks-style (`still-frame-vo`)

**What the format does to the copy.** One still is held for the entire runtime, so the image
never changes and every bit of movement lives in the words. That makes this the format with
the most words per image in the canon, and the cheapest place to run a long spoken structure.
The one-word Poppins captions carry the rhythm, so the line breaks where the voice breaks.

**The register.** Story-led or quote-led. A scene the viewer is already inside, narrated.

**Load:** E-005 and E-050 (the symptom stack and its house build: eight owners' evenings, then
the collapse into one problem and one hire, which costs one still), E-042 (take the contractor,
the course, the tool subscription and the 9pm DIY off the table before offering the hire),
E-041 (widen the claim so "probably not me" fails), E-043 (agitate, educate, repeat), E-020 and
E-021 (build to the reveal, pay it off with the number), E-017 (the owner quoted and attributed
by role), E-053 (the book on the dashboard, the second job that starts when the site shuts),
E-035 (rehook inside fifteen seconds), E-063, E-031.

**Leave out:** E-028 (dethroning the con prop needs a second image), E-058 (needs a screen
share), E-008 (the native-format borrow is a static and carousel move).

---

### F5 · News-headline carousel (`news-carousel`)

**What the format does to the copy.** Five silent cards under the bottom-band law. One block
of type per card, one size, no voiceover and no footage to carry anything. Section 7b is the
binding constraint: about 45 to 60 characters a slide, one sentence, one idea, one blue accent,
and a number, a name or a comparison on every card. The arc is fixed: hook, the scene said
once, the cost with its scope, the reveal that names the the role you place, the endcard.

**The register.** Reported rather than argued. The news frame does the persuading, so the
sentences stay flat and factual and let the facts be the shock.

**Load:** E-059 (the silent bar: the whole thing lands in the text or it does not land),
E-008 (borrow the news frame, and the limit that goes with it: fabricating a source, a study or
a masthead is out, because trust is existential for a recruitment brand), E-039 and E-016 (the
unrounded number leads, every adjective replaced by the fact under it), E-054 (the scope caveat
lives on the card, in the same sentence, and it costs three words), E-019 and E-064 (slide one
buys slide two, and nothing else), E-030 (no naked callout on slide one), E-052 (industry x
pain x circumstance, never a job title), E-057 (the reveal slide treats the role as a contested
thing the reader is late to), E-023 (if capacity is the scarcity, give its exact number).

**Leave out:** E-043 and E-046 (both need runtime the deck does not have; five cards cannot
stack loops), E-047 and E-024 (no long-copy surface on a slide), E-035 (a rehook inside a
five-card deck is just the next card), E-042 (handling the default fix properly costs two
cards, and the arc has no room to spare).

---

### F7 · Single-image static ads (`static-ads`)

**What the format does to the copy.** Two surfaces, and they take opposite kinds of writing.
The **card** is one silent band under section 7b: 40 characters to read at 140px, 97 before it
drops below headline weight, one sentence, one idea, one accent. The **primary text** above the
image has no such limit, and it is the only place in the canon where the full unaware-to-ready
walk fits.

**The register.** The card is a headline. The primary text is a letter.

**Load on the card:** E-059 (silent bar), E-037 (the contrarian claim), E-038 (the negative
problem callout: here is why the outcome is slipping), E-056 (the negative command, with the
conditional doing the qualifying), E-039 and E-016 (the number leads, unrounded), E-054 (scope
on the card), E-057 (category creation reads as scarcity), E-063 (question only where the
answer is yes), E-029 and E-030 (spine B is how this format batches: the callout fused to the
pain against a locked skeleton, industry and pain swapped per variant, and never the label on
its own).

**Load on the primary text:** E-047 (long copy walks the unaware all the way, and shortening it
to look modern is the failure), E-024 (answer every objection inside the piece, then one
unambiguous next step), E-042 (the default fixes go first), E-005 and E-050 (the checklist
static, S14: eight admin pains, one hire, and the cause line that explains why nobody has fixed
it), E-014 and E-015 (explain the salary rather than soften it, and admit the role is new),
E-041 (the widening line), E-049 (if it reads as an advertorial, it lands somewhere that
teaches).

**Leave out:** E-035 and E-046 (a static has no timeline to rehook or chain across), E-058
(needs motion), E-020 (the reveal build needs a sequence, and the card has one beat), E-028.

### F10 · Slide carousel with VO, the projector film (`slide-carousel-vo`)

**What it does to the words:** the script is cut into POINTS rather than sentences, and every
point gets its own painted frame at roughly a two second hold. A line that carries three ideas
becomes three beats, so the writing has to survive being read one clause at a time. The picture
changing on the point is what does the retention work, and the projector clunk is the metronome.

**Load:** the universal floor, plus the video floor (E-004, E-006). E-007 hardest of all here,
because the voiceover is cut before a single still is generated and the whole cut is timed off it.
E-034 (proof in the next beat) lands naturally, since the next beat is two seconds away. E-064
(every element buys the next) is the format's own logic.

**Leave out:** E-035 if it assumes one long held frame; the rehook is structural here rather than
written, because the cut rate carries it.

---

## 7d. The Halbert benchmark

The eight principles the whole craft reduces to. When a draft is not working and the reason is
not obvious, walk this list.

1. **The offer is everything.** Sharpen the deal before the words. Strong copy cannot carry a
   weak offer, and a strong offer survives weak copy.
2. **Specificity beats adjectives.** "At 60mph the loudest noise is the electric clock."
3. **Get the envelope opened first.** The first line's only job is to earn the second.
4. **Research before writing.** Copy is 90% preparation. The fact sheet already exists:
   PERSONAS, the pain wiki, the discovery transcripts.
5. **Write to one person.** "Dear Friend", never "business owners".
6. **Confession builds credibility.** Name the honest tension. A house is a real hire at real
   money, and the role is new. Admitting the flaw is what makes the rest believable.
7. **Seduce before you sell.** Agitate the real cost of the status quo before the CTA arrives.
8. **The last line is prime real estate.** Never spend it on a limp CTA.

**The canon behind the benchmark**, for anyone going deeper: *Breakthrough Advertising* (Eugene
Schwartz, the five levels of market sophistication in spine entry E-060), *Scientific
Advertising* (Claude Hopkins), *Ogilvy on Advertising* (David Ogilvy, the Rolls-Royce ad in
E-016 and E-017), and *Influence* (Robert Cialdini).

---

## 8. The evidence layer

Distilled from 1,954 classified posts and 196 transcribed videos across 24 content-educator
accounts, scraped and analysed . Full corpus in your own reference store.

**Read this as craft evidence, and apply the transferability filter.** These creators sell
courses to creators. The attention mechanics transfer to house. The monetisation tactics
(comment-gated vaults, follow-for-more, course funnels) do not, and house does not run them.

### What the corpus actually demonstrates

**Openers carried the most signal by a wide margin** (80 distinct opener conventions across
638 total). The recurring winners: open on a contrarian principle, open on the common mistake,
open by naming a specific visual cliché, open on data, open with common knowledge and then
pivot off it, open with a binary contrast question.

**Proof works as a structure the reader can follow** (39 distinct). What worked: establish the
mechanism before claiming the result, use a high-performer stat as the credibility anchor,
run a split-screen case study as the proof structure, cite a cross-platform parallel, use
repetition itself as proof.

**Contrast does the persuading** (57 distinct). Generic versus specific, mechanism-led versus
reach-led, audience quality versus audience size, before versus after. Set the principle
before the rule, then show the two cases.

**Specificity separates the top decile** (62 distinct). Numbered principles, ranking by
outcome metric rather than vanity metric, separating view metrics from conversion metrics,
tying a specific example back to the abstract principle.

**Closes** (53 distinct). The best ended on a principle-driven prediction or on system-proof.
The gated-resource close dominated the corpus and stays out of house work.

### Transferability ruling
| Transfers directly | Adapt with care | Does not transfer |
|---|---|---|
| Opener architecture, contrast structure, mechanism-before-result, specificity discipline, pacing and cut rhythm, proof stacking | Listicle beats, teardown structure, tier ranking | Comment gates, resource vaults, follow CTAs, course funnels, creator-economy proof (view counts as the outcome) |

### Scraped hook bank
275 verbatim scraped hooks (237 the educators' own openers, 38 quoted by them) are distilled
into `references/hooks/HOOKS.md`, and the raw captions they came from sit in
`projects/content-formats-studio/bank-source/`. Treat the scraped lines as structural reference for
how a line is built. Do not lift them, because the voice and the domain are wrong for house.

---

## 9. Production routing

This skill stops at the locked script. The build belongs to these, and each stays the source
of truth for its own pipeline.

**Which model builds which shot: `references/canon/model-routing.md`.** It binds across every
format, it carries the verified parameter schema for each model, and it holds the two traps that
cost real money: `soul_cinematic` and `gpt_image_2` have no 4:5 ratio, and `gemini_omni` caps at
720p. A format's own locked model set outranks it, and F2 noir-painterly is the one that does.

The strict format list is `canon/angles-and-formats.md`, five formats as of . Route by format:

| Format | Route to |
|---|---|
| F1 Guru clip / talk-show | `the business/skills/content-formats/formats/talkshow-vsl/SKILL.md` |
| F2 Painted animation w/VO (house style) | `the business/skills/content-formats/formats/noir-painterly/SKILL.md` |
| F3 Still frame w/VO (nighthawks-style) | `the business/skills/content-formats/formats/still-frame-vo/SKILL.md` |
| F5 News-headline carousel | `the business/skills/content-formats/formats/news-carousel/SKILL.md` |
| F7 Single-image static ads | `the business/skills/content-formats/formats/static-ads/SKILL.md` |
| F10 Slide carousel w/VO (the projector film) | `the business/skills/content-formats/formats/slide-carousel-vo/SKILL.md` |
| F12 Tape carousel (type in the negative space) | `the business/skills/content-formats/formats/vhs-carousel/SKILL.md` , in gate, no real shot set yet |
| Faceless performance ad style spec | `the business/skills/content-formats/formats/ (the Faceless Reframe doctrine now lives in each video format skill)` + `content-engine/engine/` |
| Photoreal B&W noir character ad (non-canon variant) | `the business/skills/noir-painter-ad/SKILL.md` |
| Pain-led landing page | `the business/skills/pain-page/SKILL.md` |

**Layers** bolt onto a format without changing it, so they are never picked for a slot on their own:

| Layer | Route to |
|---|---|
| L-EDIT Editorial layer (archival bed and paper cutouts) | `the business/skills/content-formats/layers/editorial-layer/SKILL.md` |
| L-PATH Path control (draw the camera move on the plate) | `the business/skills/content-formats/layers/path-control/SKILL.md` , unproven on the house account, one test outstanding |

**Retired never pick these for a slot:** stitch-hook (was F4), best-time-carousel and
webinar-carousel (were F6). The skills still work and stay on disk for ad-hoc use; they are out of
the canonical draw. Retired numbers are never reused.

### Production gates (never skip, they sit before spend)
1. Script refined against the canon and reviewed in Cursor.
2. Shotlist mapped to the beat spine and the shot bank.
3. Storyboard board approved. Hard gate before any generation spend.
4. Stills approved one at a time in Cursor. Hard gate before any motion.
5. Motion on approved stills only. One paid job at a time, never batched.
6. VO with the ear-tested voice ID.
7. Assemble, captions, end card, review in Cursor.

**Captions (canonical):** one word visible at a time, Poppins Regular 92px on 1080x1920, pure
white, no outline or shadow, dead center, timed to whisper word onsets against the actual cut
audio. Rig at `content-engine/engine/tools/captions/`.

**End card (canonical):** matte deep navy `#1A1A2E`, `house PARTNERS` wordmark muted, one
restrained `#1269FF` radial accent, the line "Hire a house today." Music resolves and cuts on
the card.

**Moiré shimmer (optional, any asset, adopted :** a house-wide finishing layer that
adds continuous movement to a frame for zero generation spend. Rig and full spec at
`content-engine/engine/tools/moire/`. Locked look: `displace` mode, 6px carrier, 18px
displacement, 0.32 opacity, 0.25 deg/sec drift. Reach for it whenever a held still needs life
(F3 runs one image for its whole runtime and F2's L2 lane holds a still under a post graphic
layer, so both get motion here without a single credit).

Three rules bind it. **It is never prompt-baked**, because moiré is an interference artifact
rather than a texture and a model's decoder low-passes the very gratings that create it, so
your generation platform returns decorative op-art with a locked pitch and a paid regeneration per variant.
Ask the plate for the carrier instead (mesh, louvre, corrugated sheet, perforated panel, in
deep focus) and generate the beat in post. **It never runs behind the kinetic captions**, since
92px pure white type vibrates against a moving high-frequency field; the rig's caption safe
band is on by default. **It stays luma-only and monochrome**, because 4:2:0 subsampling kills
coloured moiré at twice the rate and a tint would spend the one-accent-colour budget.

### The house style (the Faceless Reframe)

A single casual, deep Australian voice running a truth-bomb monologue over semi-premium,
precise AI-generated visuals, word-by-word kinetic captions, landing on a minimalist house end
card. No talking head, roughly 90% AI-buildable, cheap to batch. Full spec:
`the format skills' Faceless Reframe section`.

| Element | Spec |
|---|---|
| **Voice** | Casual, deep, unmistakably Australian, male. Dry confidence, unhurried. Talks to one owner like a mate who has seen behind the curtain. your voice model `eleven_multilingual_v2`, voice ID is a gated ear test. |
| **Music** | Light bed, low. Near-silent open, lifts on the proof beat, resolves and cuts on the end card. Never wall to wall. |
| **Visuals** | Semi-premium and precise. Clean macro, controlled lighting, shallow depth of field, real-material texture. One notch below full luxury on purpose. The operator's world: hands at a keyboard, a dashboard resolving, an inbox clearing. |
| **Palette** | Deep navy `#1A1A2E`, one electric-blue accent `#1269FF` used with intent, text `#F4F6FB`, muted `#8A8FA3`. Never wash a frame in blue, one accent per shot. |
| **Captions** | Kinetic, word by word, hard-synced to the voice. Sora, weight 800, tight tracking. Mostly `#F4F6FB` with a single `#1269FF` accent word per phrase on the load-bearing word. |
| **Never** | Text baked into the generated plate, moiré baked into the generated plate, garbled AI type, stock cheese, rainbow gradients, more than one accent colour. |

**Refining images:** always feed the existing image plus its anchors back as i2i references.
Never regenerate fresh.

---

## Removed before publishing

Five sections came out of this file because they were one company's commercial strategy rather than
craft: the audience barbell and its ICP, the call-to-action canon, the volume and spend model, the
industry compliance rules, and the reference-bank index. Write your own at these headings. The
funnel-builder skill in this repo produces most of what the first one needs.

---

## 10. The QA gate

Run the output-qa gate against every draft before it leaves. The skill itself was archived to `Archive/old-skills/general/output-qa.md` (read-only); the six gates are restated here so the archive is reference, not a dependency. Six gates, in order,
stopping at the first failure: em dash scan, banned pattern scan, banned vocabulary scan,
voice match check, reference bank comparison, format-specific checks.

Add two house-specific checks on top:
- **Negation-swap scan.** Any line built on what a thing is not. Hard fail.
- **Barbell check.** Does the asset speak to exactly one side of the barbell, and is that the
  side the brief asked for. Hard fail on drift.

Fix and re-run. Never deliver a flagged draft.

### The script checklist (run before presenting any video script)

- The concept is a single persona x angle x offer rather than a thumbnail variation.
- The hook is 1 to 3 seconds, leads with provocation, has voiceover, passes the scroll test, and
  is tagged by type and angle.
- The problem is agitated before the solution appears, never a wide hook straight to the CTA.
- The teach beat is present and genuinely usable on its own.
- The strongest emotional beat is the final row.
- Four or more filming locations, and every line is specific and filmable.
- Read the Script column aloud: it sounds like one coherent voiceover.
- Four to five retention mechanics present.
- Zero banned words, zero em dashes, Australian operator-grade register.
- No overclaim, and every number carries the scope its source supports.
- The close is soft, direct, and points at the right destination.

---

## 12. What this skill does not do

- Blog posts and SEO articles. Use `seo-brief` plus a writer pass.
- Media plans, budget allocation, audience research.
- Email sequences, unless asked with full context.
- Brand voice document creation. Use the `brand-voice` skill.
- Anything for Open Operator. Different brand, different voice, different rules.
- Writing before the clarifying questions are answered.
- Publishing. Nothing here posts anything anywhere.