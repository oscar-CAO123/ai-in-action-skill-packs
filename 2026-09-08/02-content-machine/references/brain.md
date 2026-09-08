# The brain

Instruction only. What the machine knows about this business. No media, no drafts, no generated
assets, ever: those live in `outputs/`.

```
brain/
  SKILL.md      the entry point, written in phase 7
  avatars.md    who is being written for
  pains.md      what those people say is wrong
  offers.md     what is being sold, with its proof
  formats.md    the shapes content is published in
  hooks.md      hook structures, cited, never filled lines
  laws.md       the rules copy obeys here
  language.md   the words this business uses, and the ones it never uses
```

## Codes, and why everything has one

Every avatar, pain and format carries a short code. A formula is three codes, a row in the database
carries the same three, and a person in a meeting says the same three out loud. Pick codes that read
out loud in your own business, and keep them short. Without codes a
concept is a paragraph, and paragraphs cannot be counted, ranked or searched.

```
CLINIC x NOSHOWS x SHORT-VIDEO
```

## avatars.md

One block per avatar: the code, the job and the situation, the week they are having when they come
looking, what they have already tried, what they fear, who else is in the decision, and the words
they use for the problem. Written in their language, never in demographics.

## pains.md

One page per pain theme. The slug, the home angle, then:

- **The verbatims.** Sentences customers actually said, dated, attributed to the call.
- **The figures.** Whatever numbers they quoted, with who quoted them.
- **The cost of inaction**, in their terms.
- **The proof this business has** that it fixes this, or an honest note that it has none yet.

Pain pages grow every week from the call read. This is the file the machine's ideas actually come
out of, and it is the difference between content that sounds like the business and content that
sounds like everybody.

## offers.md

Each offer: the promise in one sentence, the proof, the objection that always comes, who it is for,
who it is not for, and the free thing that leads into it. Proof is named specifically, and an offer
with no proof says so.

## formats.md

Each format: its id, what it looks like, its length or slide count, what it is good at, what it is
bad at, and one link to a piece that proves it works here. Name the ids after the format itself
(`SHORT-VIDEO`, `CAROUSEL`, `LONG-POST`) so a code is readable without a lookup. The register starts
short and earns its entries.

## hooks.md

Hook structures with ids, and their slots. Structures, never filled lines. A filled line in this
file gets reused verbatim within a fortnight and the whole channel starts to sound the same.

## laws.md

The rules every piece of copy obeys here, and each one should be checkable by a script:

- the banned words and phrases, with what to say instead,
- the claim rule: what may be asserted and what needs a named proof,
- the structures that are refused,
- the punctuation and formatting conventions,
- the tone, stated as things to do rather than adjectives.

`engine/gates/copy.py` reads this file. A law that cannot be checked belongs in `language.md`.

## language.md

The words this business uses for its own things, and the words it never uses. One line each, with
the reason. Industry terms that mean something specific belong here, and so does every word the
founder hates.
