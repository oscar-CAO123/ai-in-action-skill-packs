# Phases 5, 7 and 9. The build

Only start once the operator has typed `READY TO BUILD`.

Three parts. Write the brain, install the engine, then run the whole loop once for real. The build is
not finished when the files exist. It is finished when a ranked idea queue built from their own
evidence is on their screen.

---

## Phase 5. The brain

Instructions only. No code, no media, ever. Write each file from the interview answers, with the
language gate run over every payload before it is written.

| File | Built from | The test it has to pass |
|---|---|---|
| `brain/SKILL.md` | Everything. This is the router their agent reads before writing a word. | A fresh agent that reads only this file knows what to do next. |
| `brain/positioning.md` | Interview A and B | Names the competitor, the trigger event, and the thing that is hard to copy. |
| `brain/icp.md` | Interview C, plus real quotes from ingested evidence | Every claim about the customer carries a source id. |
| `brain/brand-truths.md` | Interview D | At least six positions someone in their industry would argue with. |
| `brain/language-rules.md` | Interview 44, 50, 51, and phase D | The three reference sentences in their own writing are quoted verbatim. |
| `brain/source-register.md` | Phase 3 and phase 4 | Every source has where, reach, depth, record shape, and status. |
| `brain/doctrine.md` | `05-doctrine.md`, re-grounded | Every law has their example under it. A law with no example did not get the pass. |
| `brain/copywriting.md` | `06-copywriting.md`, filled | The ban list includes their words, not only the generic ones. |
| `brain/formats/<id>.md` | `07-format-library.md`, only the selected formats | Ratios, durations and beats are concrete numbers, not ranges copied across. |
| `brain/formats/hooks.md` | The structures in `06-copywriting.md`, plus their own | Every structure has one real example. |
| `brain/founder-questions.md` | `04-founder-questions.md` | Every question carries a source line. Nine vectors, twelve minimum each. |

`brain/SKILL.md` is the one that matters most, and it should be short. A router, a load order, the
hard rules, and pointers. Everything else lives in the file it belongs to.

**Before writing each file:** run the language gate. **After writing all of them:** read
`brain/SKILL.md` back as if you had never seen the project, and check that it actually routes.

---

## Phase 7. The engine

Copy `templates/engine/` into the project as `engine/`, then configure it. The templates are working
code. Do not rewrite them from scratch, and do not "improve" them during the build.

```bash
cp -R content-operating-system/templates/engine ./engine
mkdir -p outputs/{evidence,queue,drafts,finished,archive,logs}
python3 -m venv engine/.venv && engine/.venv/bin/pip install -r engine/requirements.txt
```

### Writing `engine/config.json`

Generated from the interview. Never holds a secret, only variable names.

```json
{
  "project": { "name": "", "root": ".", "timezone": "" },
  "sources": [],
  "channels": [],
  "formats": [],
  "providers": { "llm": "agent_cli", "image": null, "video": null, "voice": null },
  "ideation": { "ideas_per_run": 15, "written_up": 5, "lookback_days": 7 },
  "caps": { "weekly_generation_spend": 0, "per_asset_spend": 0 },
  "approval": {
    "ingest": "unattended",
    "ideate": "unattended",
    "paid_generation": "human",
    "publish": "human",
    "system_of_record_write": "human"
  },
  "redaction": { "enabled": true, "keep": ["role", "industry", "size_band", "stage"] }
}
```

Validate it before continuing: `python3 -m cos.config --check`. It exits non-zero and names the
problem if a source has no reachable path, a variable is missing from the environment, or a selected
format has no file in `brain/formats/`.

### Wiring each source

One at a time, ranked order from the register. For each one:

1. Add it to `config.json`.
2. Run `python3 -m cos.ingest --source <id> --dry-run --limit 5`. It prints what it would write and
   writes nothing.
3. Read the five records out loud to the operator. Ask one question: does this look like your
   customers.
4. Check the redaction actually worked on all five. A name that got through means the source needs a
   custom rule before it goes near a real run.
5. Only then run it for real.

Never wire all the sources and run them together the first time. One source, verified, then the next.

### Writing the agent instruction files

Two markdown files the headless runs read, in `engine/`:

- `AGENT-INGEST.md`: only needed if a source requires judgement to parse. Most do not.
- `AGENT-IDEATE.md`: the ideation prompt. It tells the agent to read `brain/`, read the week's new
  evidence, cluster it, rank it, write the queue, and refresh the question bank. It is a file rather
  than a string in the code so the operator can edit how their system thinks without touching Python.

---

## Phase 8

`09-schedules.md`. Both tasks, installed, triggered once, logs read.

---

## Phase 9. The first real run

This is the phase that decides whether any of this gets used.

### 1. Ingest for real

```bash
./engine/run-ingest.sh
```

Read the log. Report the per-source counts in one line each. If a source returned zero, say which and
why, and fix it now rather than noting it for later.

### 2. Ideate for real

```bash
./engine/run-ideate.sh
```

This produces:

- `outputs/queue/<date>/queue.json`, every idea with its evidence, rank and score.
- `outputs/queue/<date>/review.html`, the page they actually read.
- An updated `brain/founder-questions.md` with a `## This week` block at the top.

### 3. Open the review page

```bash
open outputs/queue/<date>/review.html      # macOS
xdg-open outputs/queue/<date>/review.html  # Linux
start outputs\queue\<date>\review.html     # Windows
```

The page is self-contained. One HTML file, no network calls, no build step, works from a file URL.

**What is on it, and nothing else:**

- Each idea, in rank order, in a single column.
- Under each: the hook, the angle in one line, the format it is proposed for, and the founder
  question attached to it.
- Beside each, in a muted rail: the evidence. The quotes, the source ids, the dates, the count of
  independent sources that said it.
- Keep and cut, which writes back to the queue file.

No dashboards, no charts, no metadata blocks, no buttons that do anything else. An idea with an empty
evidence rail does not appear on the page at all, because it did not come from evidence.

### 4. Walk them through it

Read the top three ideas out loud with their evidence. Then ask which one they would film today. That
answer tells you whether the ranking is any good, and it is the only measure of this build that
matters.

If they pick something from position eleven, the ranking is wrong. Ask why they picked it, and adjust
the weights in `config.json` under `ideation`. Do that now, while they are still in the room.

---

## Handing over

Four lines to the operator, no more:

1. Open `outputs/queue/<date>/review.html` and pick one. Film it this week.
2. `brain/founder-questions.md` has five questions under **This week**, refreshed every run.
3. Ingestion runs [when]. Ideation runs [when]. Logs in `outputs/logs/`.
4. To change how it thinks, edit `brain/`. To change what it pulls, edit `engine/config.json`. To
   change how it ideates, edit `engine/AGENT-IDEATE.md`.

Then write `.cos-interview.json` one last time with `"status": "built"`, the paths of everything
created, and the date. A later session reads that file and knows exactly what it is looking at.

---

## What counts as finished

A ranked queue built from their own evidence, on their screen, with the founder questions attached,
and two scheduled tasks that will do it again without being asked.

If you did not get there, say which phase you stopped at and what blocked it. Do not describe a
system as running when the first real ingestion has not happened.
