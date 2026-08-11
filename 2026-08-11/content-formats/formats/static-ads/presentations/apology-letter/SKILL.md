---
name: static-ads-apology-letter
description: Presentation sub-skill. A brand apology set as a letter on warm paper, where the apology is for not having said the useful thing sooner. Use when a card needs to promise information rather than persuasion. Shipped as the F5 apology variant, LIVE on the CRM. Read formats/static-ads/presentations/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: local:a competitor-8-statics/03-apology-letter
renderer: scripts/f5_variants.py build_apology
---

# Apology letter

**The mechanism.** The frame swap. An apology promises information rather than persuasion, so the
body argues while the reader is still reading the apology.

## 1. What is taken from the reference

`local:a competitor-8-statics/03-apology-letter`: **the frame swap and the copy structure, beat for
beat.** you, : "model the copy structure and the way copy is presented within the
Gruns reference."

**The reference does not apologise for a failure at all, and that is the thing that makes it
work:**

1. who we are and what we have been busy doing
2. we were so busy we FORGOT TO TELL YOU the one specific benefit, then the benefit, stated
   concretely
3. the amends, which is the offer

So the apology is for **not having said the useful thing sooner**, which house can make truthfully
and which needs no invented service failure.

## 2. The gate that cannot move

**Apologise for something TRUE.** Never invent a service failure, a complaint, a delay, a figure or
a named client. `../../proof/SKILL.md` binds this card hard, because an apology is a claim about
the house's own conduct and a false one is the worst kind.

**Beat two names the JOB, never an outcome.** The first draft answered "what does the role do" with
a result, and a result is exactly what `../../proof/` bans. your replacement is the job said in
fragments: one person, an employee, on payroll, and the three things they actually do (find the
bottlenecks, create the agents and automations, run them full time). A job description is not a
result, so the gate never gets near it.

## 3. The head is avatar-specific

> Construction business owners. We owe you an apology.

your instruction, . It is derived from the industry's own `short`, so all seven read
as their own reader rather than one card with the noun swapped. Agnostic renders "Aussie business
owners."

## 4. The bed is a recorded exception

**Warm off-white paper, not black.** The format needs it: a letter on void is a statement, not a
letter. `news-carousel/SKILL.md` permits a warm paper canvas on the Hub-build curation carousel
"and nowhere else", so this card is a live exception and it is flagged as one rather than quietly
taken. It is written into the card's `notes` on the CRM row.

**The fallback exists.** If the bed is ever refused, the same layout renders on black with the
headline in blue and the body in white. Nothing else in the card changes.

## 5. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 f5_variants.py apology                    # agnostic, free
python3 f5_variants.py apology --industry retail  # one vertical
python3 f5_review.py                              # the dossier, beside its reference
```
