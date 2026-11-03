# Voice quote

The bonus demo from the 3 November call. You talk through a job on site, add a few photos, and a
priced quote is waiting for your OK before you are back in the van.

It runs on your own computer, in three parts:

1. **Whisper**, a free speech to text program, writes the voice note down on your computer. The
   audio never leaves it.
2. **Your LLM** reads the words (and any site photos) into a fixed job sheet. This is the one step that
   goes over the internet, to the provider you pick. Every fact it records carries the exact words it
   came from, and the app flags any quote that is missing or not in the voice note word for word. The
   model never sets a price.
3. **Your price list** (`price-list.json`) prices the job sheet in plain code. If a fact you need to
   price the job was not said, the app asks you for it. It never guesses. Anything asked for that is
   not on your price list comes back as a **Needs a price** line at $0, for you to price by hand.

The example price list is a building business (fences, decks, bathrooms) with made-up rates. Swap it
for your own trade. `SKILL.md` has your agent interview you and write your price list for you.

## Try it in two minutes, no key needed

You need [Node](https://nodejs.org) 20 or newer, and nothing else. Open Terminal in this folder and run:

```
node server.mjs
```

Open http://127.0.0.1:8787, press **Use the example**, then **Build the quote**. With no API key, the
example uses a saved reading of its words (`example/job-sheet.json`), so you can watch the pricing work
first. It should land on $11,833.14 including GST, with two Needs a price lines.

## Make it read your own voice notes

**1. Connect an LLM.** Copy `.env.example` to `.env` and fill in your provider's API style, your key
and the model you want. It works with any provider that offers an Anthropic or OpenAI style API. Make
a key just for this app and set a monthly spend limit on it at your provider. `.env` is ignored by
git, so it never gets committed. The server reads it on every call, sends the key only to your
provider, and never prints it. Pick a model that reads images if you want it to look at photos.

**2. Whisper, for recorded and uploaded voice notes.** On a Mac:

```
brew install whisper-cpp ffmpeg
mkdir -p ~/.cache/whisper-cpp
curl -L -o ~/.cache/whisper-cpp/ggml-large-v3-turbo-q5_0.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
```

On Windows or Linux, build whisper.cpp from [its repository](https://github.com/ggml-org/whisper.cpp)
and set `WHISPER_CLI` and `WHISPER_MODEL` in `.env`. Without Whisper you can still type or paste the
words into the box.

Restart `node server.mjs`. The line under **New quote** goes green when both are ready.

## Make it yours

Everything about your business lives in `price-list.json`:

| Field | What it does |
|---|---|
| `business` | Your name, ABN, email and phone, printed on the quote |
| `markup_percent`, `tax`, `deposit_percent`, `valid_days`, `terms` | How the totals and the terms are worked out |
| `speech_hints` | Words Whisper should expect: your products, colours, suburbs |
| `jobs` | One entry per kind of job you quote |
| `jobs.<job>.facts` | What you need to hear to price that job. Each has a `type` (`number`, `count`, `yes_no`, `text`), a `means` line the model reads, and `needed: true` when you cannot price without it |
| `jobs.<job>.lines` | Your price lines. `qty` is a fixed number, a fact name, or a rule like `{ "of": "length_m", "every": 2.4, "plus": 1 }` (one post every 2.4 m, plus one). `times` covers waste, for example `1.1`. `only_if` adds a line only when a yes/no fact is yes |
| `jobs.<job>.checks` | Plain reminders printed on that job's quote |

After any change, run `node server.mjs --check`. It names the job and the item that is wrong.

The fastest way to fill it in is to let your agent do it. Open your agent in this folder and say:

```
Read SKILL.md and follow it.
```

## What it will not do

- Send anything. The quote opens as a page you save as a PDF. You send it.
- Guess. No size, no count and no price comes from the model or from a photo.
- Talk to the internet, apart from the one call to your LLM provider with the words and photos you chose
  (and, if you run the setup above, the one Whisper download).
  The server listens on 127.0.0.1 only, so nothing else on your network can reach it.

## Files

| File | What it is |
|---|---|
| `server.mjs` | The local engine: serves the page, runs Whisper, makes the one LLM call. No dependencies |
| `price-list.json` | Your business, your jobs, your rates |
| `public/` | The page: `index.html`, `app.js` (the pricing is `priceJob` in here), `style.css` |
| `example/` | The example words, a saved reading of them, and a script to read aloud |
| `SKILL.md` | For your agent: interviews you and writes your price list |
| `.env.example` | Copy to `.env` for your key and settings |
