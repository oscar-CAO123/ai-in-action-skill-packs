---
name: win-back
description: Find customers who have gone quiet and draft a short personal text for each. Draft only.
---

# Win back the quiet ones

## When it runs
Every Tuesday at 9 am. Also when I ask "who has gone quiet".

## What it reads
- The customer export from the booking system: name, mobile, last visit,
  and whether they agreed to marketing texts. No opt-in column: stop and
  tell me, do not draft anything.
- offers/offer-sheet.md: the only prices and offers we may quote.
- context/brand-voice.md.
- ledger/contacted.csv: who was contacted and when.

## Steps
1. Keep active customers with no visit for 21 days or more.
2. Skip anyone contacted in the last 30 days.
3. Amber is 21 to 34 days quiet. Red is 35 days or more.
4. Amber: draft a two-line text with their first name and one offer
   from the offer sheet.
5. Red: write three talking points for a phone call instead.
6. Check every draft: any price or offer not on the offer sheet is removed.

## Rules
- Plain English. No em dashes. Never use: delve, leverage, unlock, seamless, game-changer, robust, elevate.
- If a file listed under What it reads is missing, stop and tell me which. Do not guess.
- Draft only. Nothing goes out until I say yes to that person.
- Only draft for customers who agreed to marketing texts. Never text
  anyone who has opted out.
- Log every approved send in contacted.csv.

## What it sends me
The amber texts to approve, and the red call list, longest quiet first.
