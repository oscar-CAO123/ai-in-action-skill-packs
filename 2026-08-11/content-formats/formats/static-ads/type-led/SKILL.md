---
name: static-ads-type-led
description: F7 sub-skill. Words on black, nothing else. Owns the band, the fit solver, the one justified block and the single blue accent. Use for band, us vs them, problem/solution split, question hook, don't hire this person, PSA comparison split, numbered listicle and tick rows, and the founder statement card. Read formats/static-ads/SKILL.md first for the shared law.
parent: static-ads
format: F7.1
---

# F7.1 Type-led statics

The cheapest card house makes and the one the whole format rests on. No photograph, no interface, no
drawing. The argument is carried entirely by the words and the way they are set.

**Cost: free.** Every card in this sub-skill renders from `scripts/band.py` through headless Chrome
in about 2.5 seconds. Nothing here needs a paid generation, ever.

**Read `../SKILL.md` first.** Section 0 is the band law, section 2 is the copy rules, section 4 is
the funnel label. This file only covers what is specific to type.

---

## 1. The eight formats

| Format | Archetype | The argument | Funnel |
|---|---|---|---|
| **Band** | house | One statement, the control format for the whole test | TOF |
| **Us vs them** | S11 | Category education by contrast: the full-time problem against the part-time fix | MOF |
| **Problem / solution split** | S2 | Stacked pains resolving into one answer | MOF |
| **Question hook** | S12 | Curiosity and confrontation. Needs the strongest single line of the eight | TOF |
| **Don't hire this person** | S6 | A reverse command the reader is already inside | TOF |
| **PSA comparison split** | house | Two states of the same business set against each other | MOF |
| **Numbered listicle / tick rows** | S14 | Pain stacking into one answer | BOF |
| **Founder statement card** | house | a founder's own words, first person, signed | MOF |

Cell assignments, industries and pains: `../FORMAT-GRID.md` section 2.

## 2. Two tiers of band, and which one a format gets

**Tier A, the pure band.** One justified block in the bottom 506px, one size, white, one blue
accent. This is the law untouched and `render_card` renders it today with no new template.

Tier A formats: band, problem/solution split, question hook, don't hire this person, stop trying
to use AI, founder statement.

**Tier B, the structured band.** Rows or columns inside the same 506px, for the shapes that cannot
compress to one sentence. Recorded as a deviation in `../SKILL.md` section 0.

Tier B formats: PSA comparison split, numbered listicle and tick rows, the checklist static,
us vs them, consultant vs house, quote-card grid (rendered here, gated by `../proof/`).

What a Tier B card may contain:

- **The 506px band and nothing above it.** The geometry does not bend. Top edge stays at y=844.
- **One face, one size for the body rows.** A row label or a number may sit one step smaller, and
  that is the only second size on the card.
- **One blue accent on the whole card**, not one per row. On a listicle it goes on the answer row.
- **Flush margins.** Rows run x64 to x1016 like every other line.
- **No grey.** White at full strength, or blue. Grey is what made earlier passes read small.
- **Five rows maximum.** See the amendment below.

The renderer is `scripts/band_rows.py`, written . It solves the size the same way Tier A
does, by binary search against the well, and it carries the two traps this rig has already paid
for: the column is given an explicit 952px width because `clientWidth` counts padding, and the
well uses `justify-content:flex-end` rather than an auto margin, because an auto margin absorbs
overflow and the fit then passes at every size.

### The two amendments of (you, measured before ruling)

**The four-row ceiling is lifted to five.** The old text read "Four rows maximum. Five rows at this
width takes the type under thumbnail legibility," and it had never been measured against short
rows. Measured on the checklist static at full size: **five rows solves to 38.4px and fills 100% of
the well; four rows solves to 42.7px and also fills it.** 38.4px on a 1080px card reads at
thumbnail. Six rows has not been measured and stays out until it is.

**Us vs them renders as two columns.** The old text said the contrast is "argued in the words,
never in the layout," that columns "are historical and no longer render," and that a card needing a
column "has a copy problem rather than a layout problem." That was written when no column template
existed. One does now. Measured: the consultant-vs-house card solves to **66.5px at 95% fill** as two
columns, which is larger type than most Tier A cards in the set. Us vs them and consultant vs house
both move to Tier B.

**The rule that survives both:** one blue accent for the whole card, one face, flush margins, and
the 506px well. Structure gained a column and a row; the band did not move.

## 3. Writing the copy

**Every card names the avatar, agitates that avatar's specific pain, and lands a question or a
declarative statement.** All three, on every card, no exceptions. Parent `SKILL.md` section 2 is the
rule and it is the thing type-led gets wrong most, because a bare pain row reads like a headline and
feels finished while naming nobody.

- **Avatar in the frame.** Retailers, construction businesses, real estate agencies, hospitality
  businesses, insurance brokers. On a multi-row card it goes in the opening row or the panel label,
  so it is read before the rows.
- **Pain from that industry's playbook**, in the words the owner used on the call.
- **A question or a claim.** The format decides which: question hook and don't-hire ask; band, us vs
  them, PSA split, listicle and founder statement declare.

**Case belongs to the format.** All caps is the news-carousel doctrine and it carries the band
keepers only. The other type-led cells set sentence case, which is also what separates them from the
control at thumbnail size. Set it on the theme rather than pre-casing the copy string.

The `lines` field is copy, never a layout instruction. Hand-break it as a reading hint and the
renderer re-breaks it to fit. Length is the real control: a card that comes back small is a card
whose copy is too long for the shape.

Per-format notes worth having before writing:

- **Band.** The industry set's band is fixed:
  `AUSSIE <BUSINESS TYPE> ARE FINALLY REALISING THEY DON'T HAVE TO <PAIN> ANYMORE.` The "using AI"
  tail was cut on and does not go back. Spec of record: `news-carousel/SKILL.md` 1a.
- **Question hook.** A question mark does not make a hook. The line has to be one the owner has
  actually asked themselves, which is what the playbook's verbatim call quotes are for.
- **Don't hire this person.** The joke only lands when the reader is inside it, so it sits on a
  hiring pain. The reverse command has to describe a hire the reader is about to make.
- **Us vs them.** The contrast is full-time headcount against the part-time fix. Never name a
  competitor and never characterise one.
- **Founder statement.** First person, a founder, and every word has to be something he has
  actually said or would sign. Gated by `../proof/`.
- **Listicle and tick rows.** Rows are pains in the reader's own language from the playbook, and the
  answer row is the only blue. S14's canonical line is "Eight problems. One hire."

## 4. QA before it goes in front of you

- **The avatar is named on the card.** Read the card as a stranger: does it say who this is for.
- **The pain is that avatar's, from the playbook**, rather than a category noun.
- **The card is a question or a claim**, not a fragment.
- **Case matches the format**, caps only where the news-carousel doctrine applies.
- One blue accent per card, never two.
- Ink bbox inside the band, flush to both margins, fill above 85%.
- Funnel label recorded on the ad.
- Every number carries the scope its source supports, and the source is in the record.
- Em dash scan, negation-swap scan, banned vocabulary, house terminology.
- Read it at thumbnail size on the contact sheet, which is where the auction sees it.

## 5. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 build.py <slug>          # one card
python3 build.py                 # every card in ads.py + ads_builds.py
```

Copy lives in `scripts/ads.py`. The engine is `scripts/band.py`; do not fork it, add a theme or a
template function instead. The traps already paid for are in `../SKILL.md` section 0 and they are
expensive to rediscover.
