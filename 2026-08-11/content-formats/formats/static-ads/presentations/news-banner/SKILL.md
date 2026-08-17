---
name: static-ads-news-banner
description: Presentation sub-skill. A white news banner laid across a full-bleed workplace plate, pure black condensed caps, with a topic chip. Use when a static should read as a report about the reader's market rather than a message to the reader. Shipped as the F5 news variant, shipped and live. Read formats/static-ads/presentations/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: local:a competitor-8-statics/06-editorial-headline-still
renderer: scripts/f5_variants.py build_news
---

# News banner

you, on seeing the four F5 shapes: **"I love the news headline one."** It is the strongest card
the suite has produced and it is the one presentation here that reports rather than argues.

**The mechanism.** A movement in the market, stated as news, with the reader's own trade in it. The
reader is not being addressed, so nothing has to be resisted, and the claim arrives already
believed because of the register it is written in.

## 1. What is taken from the reference

`local:a competitor-8-statics/06-editorial-headline-still`: **the register of the type and the choice
of plate.** Heavier type set as a report, over a still of somebody in their own workplace. Nothing
else transfers.

## 2. The layout, and why it is legal

The news carousel's geometry: plate from y=0 to 844 fading into black, a 506px band from y=844
carrying one flush sentence. Over it, **a white banner running across the frame** with picture
still showing above and below.

**This is a recorded break of the band law** (`../../SKILL.md` section 0), and it is your call,
: "make it canonical to the way it's actually being presented in the reference. It's a
banner running across the screen ... white background, pure black text, with a little sort of
marker on what it is." `../../ui-mock/SKILL.md` already establishes that a format imitating
something the reader trusts breaks the band law by design.

- **The face is Anton**, the condensed display theme `band.py` already carries.
- **Pure black on white.** The blue accent does not appear inside the banner.
- **The marker is a topic chip, never a masthead.** It names the subject ("AI") and no publication.

## 3. The gates

- **No masthead, no section strip, no standfirst, no eyebrow.** `news-carousel/SKILL.md` section 6
  already lists all four as absent from the locked layout, so dropping them costs nothing and takes
  the fabricated-endorsement problem off the card at the same time.
- **No publication name, no journalist, no dateline, no source.** A named outlet on a house card is a
  fabricated endorsement, which is the one thing that gets an account penalised.
- **`../../proof/SKILL.md` binds the headline.** A reported movement is not a statistic. No figure,
  no percentage, no "study finds".
- **The head is not the approved F5 sentence.** A news banner reporting a movement in the market
  cannot also be an instruction to the reader, so this card carries its own headline. Recorded
  exception, written into the renderer.

## 4. The head that shipped

> Business owners across Australia rushing to hire new AI role as demand surges to record highs

your dictated wording with two changes he can undo in one line: the industry noun came out
because these run agnostic, and the doubled "Aussie ... across Australia" was cut to one. Present
participle, no source named.

## 5. Known, and shipped knowingly

**The plate is a STAND-IN.** `plates-suite/F1/professional-services.png` is reused so the format
could be judged for free. The real one is a workplace still shot for this card and it is a paid
job. This is written into the card's `notes` in the card's own notes.

## 6. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 f5_variants.py news                    # agnostic, free
python3 f5_variants.py news --industry retail  # one vertical
python3 f5_review.py                           # the dossier, beside its reference
```
