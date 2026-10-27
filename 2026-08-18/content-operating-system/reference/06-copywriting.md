# The copywriting reference

The craft layer. `05-doctrine.md` says what is allowed. This says how to actually write it.

Copied into `brain/copywriting.md` at build, with the operator's own language, bans and examples
substituted into every section marked **fill**.

---

## The order of operations

Writing in the wrong order is why most copy takes three times as long and lands flat.

1. **Pick the evidence.** One specific thing a real person said or did. Never start from a topic.
2. **Pick the audience.** One person, named by their situation. Never "business owners".
3. **Pick the claim.** The one thing this asset is arguing. If there are two, there are two assets.
4. **Pick the proof tier.** Shown, quoted, or held. This determines what you are allowed to say.
5. **Write the body.** All of it, badly, without stopping.
6. **Write the hook.** Filled from a structure, after the body exists, because a hook written first
   writes a promise the body then has to chase.
7. **Cut.** Compression happens last.

Steps 5 and 6 are in that order deliberately, and it is the step people reverse.

---

## The audience line

Before writing anything, write one sentence in this shape and keep it visible:

> This is for a [role] at a [size and type of business] who is currently [specific situation], and
> who has already tried [the thing they all try first].

If that sentence contains "anyone", "businesses", or "people who want to grow", the asset will be
generic no matter how well it is written. Go back to the evidence and find the actual person.

**Fill:** their ICP from interview phase C, in the customer's own words.

---

## Hooks

A hook has three jobs, in three to twelve words each: name who this is for, open a gap at their pain,
and foreshadow the shape of the answer.

**Structures that carry across markets.** Keep the operator's own bank in `brain/formats/hooks.md`,
seeded from these and from what already worked for them.

| Id | Shape | Example slot fill |
|---|---|---|
| `avatar-cost` | [Role] are losing [specific measure] to [specific cause] | Plumbers are losing four hours a week to quoting |
| `objection-honest` | "[Objection in their words]" is fair. Here is what it misses | "Too expensive for us" is fair. Here is what it misses |
| `wrong-first-move` | Most [role] start with [common first attempt]. That is why [failure] | Most agencies start with a tool. That is why nothing sticks |
| `changed-mind` | I was wrong about [thing] for [duration]. What changed it was [event] | |
| `number-surprise` | We looked at [N] [things]. [Counterintuitive finding] | |
| `demonstration` | This is [process] as it actually happens, including [ugly part] | |
| `insider` | Here is what happens on our side when you ask for [common request] | |
| `refusal` | We turn down [type of work]. The reason is [specific] | |
| `overheard` | A customer said "[exact quote]". Here is what that actually means | |
| `two-paths` | You can [option A] or [option B]. Most pick A and [consequence] | |

**Rules for filling one:**

- Every slot gets a specific. A slot filled with an abstraction produces an abstract hook regardless
  of how good the structure is.
- The foreshadow is not optional. "Here is what it misses" is a foreshadow. "Watch this" is not.
- Say it out loud. If it does not survive being spoken, it will not survive being spoken on camera.
- Record the id beside the hook. This is the citation law and it is what makes learning possible.

---

## Structure, by asset length

### Ninety seconds of talking head

```
hook           3 to 7 seconds, filled from a structure
the specific   the actual instance, named. Who, when, what they said
the turn       why the obvious reading of that instance is incomplete
the mechanism  what is actually going on, in one idea
the proof      shown, quoted, or explicitly framed as a position
the consequence what this means for the viewer's next week
close          one sentence. A position, or a single next step. Never both
```

### A written post

```
line 1     the hook, standing alone, readable before the fold
line 2     the specific instance
the middle one idea per line, conjunctive, no line reorderable
the turn   the part they did not expect
close      the position. No call to action unless there is a real one
```

### A demonstration or screen walkthrough

```
cold open  the end state, three seconds, before any explanation
the setup  what we are doing and for whom, one sentence
the walk   real time or lightly cut, including the part that goes wrong
the aside  the thing only somebody who does this would know
the result the artifact, on screen
close      what it took, honestly. Time, cost, what it cannot do
```

The part that goes wrong is not a flaw in the recording. It is the reason the recording is credible.

---

## Sentence craft

- **One idea per sentence.** Two ideas joined by "and" are two sentences.
- **Active, present tense.** "We rebuilt it" beats "it was rebuilt".
- **Concrete nouns.** Name the tool, the number, the day, the object.
- **No softeners.** Cut "potentially", "arguably", "in some sense", "essentially", "really".
- **No stacked adjectives.** One is a choice, three is padding.
- **Vary the length.** Three short, one long, three short. Uniform sentence length reads as generated
  even when every sentence is fine.
- **End on the strong word.** The last word of a sentence carries the weight, so do not spend it on
  "though" or "as well".

---

## Bans

Enforced by `engine/cos/gate.py`, so a violation fails the batch rather than getting an opinion.

**Structural:**

- The negation swap. "It is not X, it is Y", in every variation, including "less X, more Y" and "X?
  No. Y." Say the positive thing.
- Em dashes. Comma, period, colon, parentheses.
- Rhetorical question stacks. One rhetorical question in an asset, maximum.
- The tricolon on everything. Three-part lists are fine occasionally and exhausting as a default.
- Opening on a definition.
- Closing on "the choice is yours" or any of its relatives.

**Lexical**, and this list gets extended with the operator's own during the build:

leverage, seamless, navigate, empower, unlock, harness, game-changing, revolutionary, cutting-edge,
transformative, robust, synergy, supercharge, next-generation, paradigm shift, delve, tapestry,
testament, "in today's fast-paced", "in the age of AI", "as AI continues to", "the AI revolution",
"AI-powered" where you could say what it does, huge, massive, incredible, amazing, unbelievable,
must-have, "the only way", "the best way", "you won't believe", "let's dive in", "buckle up".

**Fill:** add every word the operator said they hate, every phrase their industry has worn out, and
every claim from interview question 50 that they cannot back up.

---

## Voice

Write down the operator's register in `brain/language-rules.md` as decisions, not adjectives.
"Professional but approachable" is not a decision. These are:

- Contractions: yes or no.
- First person singular, first person plural, or second person led.
- Swearing: never, rarely, or as they actually speak.
- Humour: dry, none, or self-deprecating.
- Sentence length: short and clipped, or longer and conversational.
- Jargon: which industry terms are used plainly, and which are always translated.
- Regional register: the spellings, the idiom, the units.
- The three sentences from their own writing that sound most like them, quoted verbatim as the
  reference cadence.

That last one does more work than the other eight combined. Take them from something they actually
wrote, not from their website, which was probably written by somebody else.

---

## The self-check before anything goes to a person

Six questions. If any answer is no, it goes back.

1. Could a competitor have published this word for word? If yes, it has no specificity.
2. Does every claim have its proof tier recorded?
3. Does the hook name an audience and foreshadow a mechanism?
4. Is there a banned word, an em dash, or a negation swap anywhere in it?
5. Does the close say one thing?
6. Does it sound like the three reference sentences?
