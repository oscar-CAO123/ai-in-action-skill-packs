# Soundbite mining brief

You are mining podcast transcripts for short-form clips of one or more named speakers. Read every
transcript file you are given, in full, then write ONE JSON file of candidate soundbites.

## Who they are

<!-- Fill from BRIEF.md. One paragraph per speaker: name, the companies they are known for, where
they are from, what they talk about. Then one paragraph on the user's business and who its
customer is, so the model can judge "core" relevance. -->

- **SPEAKER ONE**: ...
- **SPEAKER TWO**: ...
- **The business** (what the clips are for): ...

## What counts as a clip

A passage SPOKEN BY THE SPEAKER (whichever the transcript header names) that stands alone as a 15
to 90 second short-form video: a complete thought with a strong first line (the hook), a point, and
a natural end. Rants, stories with a payoff, contrarian takes, hard-won lessons, specific numbers,
one-liners, emotional moments, and anything on the themes the business cares about.

Be generous: 5 to 25 clips per hour of the speaker actually talking. Skip host intros, ad reads,
banter with no point, and anything where the speaker is only asking questions.

## Speaker attribution (important, captions have no speaker labels)

- If the speaker is the GUEST (the channel is someone else's podcast), long answers are the speaker
  and short questions are the host.
- If the speaker is the HOST (the channel is their own and the title names another guest), most of
  the talking is the guest. Only clip what is clearly the speaker: first person about their own
  companies, their own story, their own staff, their own opinion delivered as a monologue. When
  unsure, mark `speaker_confidence` "low" and only include it if the content is strong.
- The speaker's own solo videos (no guest in the title) are all the speaker.

## Output

Write valid JSON (a list) to the path you are given. One object per clip:

```
{
 "id": "<youtube id from the header>",
 "speaker": "<speaker key>",
 "start": "mm:ss",            // the transcript stamp of the line the clip starts in
 "end": "mm:ss",              // the stamp of the line it ends in (the next stamp after the last line)
 "hook": "<the first spoken sentence, cleaned up, as it would appear on screen>",
 "quote": "<the passage, lightly cleaned (punctuation added, ums removed), 40 to 220 words>",
 "themes": ["..."],           // pick 1 to 3 from the list in BRIEF.md
 "relevance": "core" | "general",
 "speaker_confidence": "high" | "medium" | "low",
 "score": 1-5,                // 5 = would stop a scroll on its own
 "why": "<one sentence on why it clips>"
}
```

Timestamps are only accurate to about 15 seconds. Give the stamps of the lines and the verifier
will pin them. Never invent quotes. Everything in "quote" must be in the transcript. Do not write
anything else to disk. When finished, reply with one line: the number of clips written and the
number of transcripts read.
