---
name: voice-quote
description: >
  Set up the voice quote template for the operator's own business. Interviews them for the jobs they
  quote and the facts and rates behind each one, writes price-list.json, validates it, and walks them
  through a first real voice note. Use when they say "set up voice quote", "make the voice quote mine",
  "build my price list", or open this folder and ask how to start.
---

# Voice quote: make it yours

This folder is a working quoting app. The operator talks through a job, Whisper writes it down,
an LLM reads the words into a job sheet, and `price-list.json` prices it in code. Your job is to make
`price-list.json` describe their business, with their real rates, then prove it works on their own
voice note.

Read `README.md` and `price-list.json` first, so you know the shape you are filling in.

## The one rule that matters

Prices come from the price list and nowhere else. You never invent a rate, a markup or a quantity
rule. If the operator does not know a number yet, leave that job out or ask them to look it up. A
quote built on a made-up rate is worse than no quote.

## 1. Look before you ask

Check the workspace for anything that already holds their prices: a price list, a past quote, a
spreadsheet, a notes file about the business. Tell them what you found in two or three lines, and
use it so you ask less.

## 2. Interview, one question at a time

Wait for each answer before the next question. Use their words, not yours.

1. The business name, ABN, email and phone for the top of the quote.
2. Their markup on cost, the tax that applies, any deposit on signing, how long a quote stays valid,
   and the terms line they put on quotes.
3. The three to five kinds of job they quote most often. Start with those. More can be added later.
4. For each job, one at a time:
   - What do they need to hear on site to price it? Each answer becomes a fact. Ask which ones they
     cannot price without (`needed: true`).
   - Their price lines for that job: item, unit, rate, and how the quantity is worked out from the
     facts. Turn rules of thumb into `qty` rules ("a post every 2.4 metres plus one" is
     `{ "of": "length_m", "every": 2.4, "plus": 1 }`; "add ten percent for waste" is `"times": 1.1`).
   - Lines that only apply sometimes ("only if the old one comes out") become a yes/no fact and
     `only_if`.
   - Any reminders they want printed on that job's quote (`checks`).
5. The words Whisper is likely to mishear: product names, colours, suburbs they work in. These go in
   `speech_hints`.

## 3. Write it and check it

Write `price-list.json` in the same shape as the example. Fact and job keys are lower case with
underscores. Every fact needs a plain `means` line, because that is what the model reads to know what to
listen for.

Run `node server.mjs --check` and fix anything it reports. Then read each job back to the operator as
a worked example ("a 20 metre fence with one gate comes to $X inc GST, from these lines") and let them
correct it. Change the file, not the code.

## 4. First real run

1. To read their own notes, have them copy `.env.example` to `.env` and fill in their LLM provider's
   API style, a model name and an API key made just for this app, with a spend limit. They paste it themselves. Never ask them to
   paste a key into the chat, and never print it.
2. If they want to record or upload audio, help them install Whisper using the README steps.
3. Start `node server.mjs`, open http://127.0.0.1:8787 and have them talk through a real job.
4. Go through the result with them: does every fact match what they said, is every line right, are
   the Needs a price lines things that truly are not on their list? Fix the price list from what you
   learn and run it again.

## Things you do not change

- The pricing stays in code (`priceJob` in `public/app.js`). The model only reads.
- Photos only add notes and questions. They never set a size or a price.
- The server stays on 127.0.0.1. If they want it on a phone or online, that is a separate job with
  a login in front of it. Say so and stop there.
- Nothing is sent to a client by this app. The operator sends the PDF themselves.
