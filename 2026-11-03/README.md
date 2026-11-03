# 3 November 2026

AI video editing, then a construction build live: a priced quote from a voice note.

| | On the call | Folder |
|---|---|---|
| 1 | The tools for AI video editing and animation, with links | [`01-the-stack`](01-the-stack/) |
| 2 | Voice quote: talk through a job, get a priced quote back. A working template you can run today | [`02-voice-quote`](02-voice-quote/) |

## Voice quote

The bonus demo, as software you can run. Whisper writes the voice note down on your own computer,
an LLM of your choice reads it into a job sheet that quotes your exact words, and your own price list
prices it in code. Nothing is guessed, and nothing goes to a client until you send it.

```
cd 2026-11-03/02-voice-quote
node server.mjs
```

Open http://127.0.0.1:8787 and press **Use the example**. It works with no key, so you can see it
price a job first. Then tell your agent:

```
Read 2026-11-03/02-voice-quote/SKILL.md and follow it.
```

It interviews you for the jobs you quote and your real rates, and writes your price list.
