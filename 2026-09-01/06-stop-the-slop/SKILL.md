---
name: stop-the-slop
description: Strip the signs of AI writing out of anything going in front of customers, using a surface pass over words and phrasing and a structural pass over the shape of the piece. Use when the user says "stop the slop", "this reads like AI", "humanize this", "de-slop this", or is about to publish a post, email, page or script and wants it to read like a person wrote it. Do NOT use to evade an AI-detection requirement somebody has a right to enforce.
---

# Stop the slop

Most humanising fixes words. That is the easy half, and it is the half that stops working fastest.
The durable tell is structural.

## The finding this rests on

The StoryScope study (Russell et al., 2026, `github.com/jenna-russell/storyscope`) classified 61,608
stories from humans and five language models using **discourse-level features only**, with every
stylistic feature withheld. It picked the machine at 93.2 percent F1.

The authors then ran the AI text through a professional span-level rewriting system that strips
cliche, purple prose and redundant exposition, which is functionally a very good surface humaniser.

Detection fell **1.6 points**.

So run the words pass, because it is cheap and it removes the obvious. Then run the structure pass,
because that is where the fingerprint actually lives.

## Pass one, the words

Vocabulary, punctuation and phrasing. Inflated symbolism, promotional language, superficial "-ing"
analyses, vague attributions, em dash overuse, the rule of three, and negative parallelism, which is
the "it's not X, it's Y" construction. Say the positive thing directly instead.

## Pass two, the structure

Six audits, run **one at a time**. Aspect-by-aspect checking caught 95 percent of issues in the
study's own pipeline against 68 percent for a single combined pass, so resist doing them together.

1. **Theme explicitness.** AI states its own lesson. The narrator explains the theme 77 percent of
   the time, against 52 percent for humans. Cut the sentence that tells the reader what to think.
2. **Structural tidiness.** One track, everything resolved. People digress and leave threads open.
3. **Emotion mode.** The largest gap in the study. AI performs a feeling through the body 81 percent
   of the time (the chest tightens, the hands shake). Humans just name it, 38 percent.
4. **Reference specificity.** Humans name real things, 47 percent against 24. AI stays at vague
   allusion. Name the actual tool, town, number or person.
5. **Reader engagement.** Humans acknowledge that somebody is reading. AI writes as though nobody is
   watching.
6. **Shape convergence.** Does this piece have the same skeleton as the last three you published.

## The trap, and it is the important part

Do not trade one default for another. The study's deepest finding is convergence: all five models
occupy one tight region of structural space while humans are dispersed. **Rarity is the human
signal.**

If every piece now opens mid-scene, names three feelings and ends unresolved, you have built a new
detectable cluster. Pick one or two interventions per piece, vary them across pieces, and be able to
say why this piece got this shape.

## The honest limit

StoryScope studied roughly 5,000-word fiction. Applying it to short nonfiction is an inference, not
a result the paper establishes. Audits 1, 3, 4 and 6 transfer most cleanly.

And nothing here makes text undetectable. That is not the goal. The goal is writing that reads as
though a person with a specific point of view wrote it, because one did.

## The full implementation

This page is the doctrine. The working version, with both passes as installable skills plus two
deterministic scanners you can run over a draft, is at:

**`github.com/NulightJens/humanizer-stack`**

```
python3 scripts/copy_scan.py draft.md
python3 skills/structural-humanizer/scripts/structural_scan.py draft.md
```

The scanners catch the pattern-matchable slice, which is maybe half. Cadence, formulaic shape and
polished-but-empty paragraphs are still yours to judge.
