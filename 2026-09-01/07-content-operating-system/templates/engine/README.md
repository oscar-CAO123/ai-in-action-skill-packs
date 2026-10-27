# The engine

All the code, none of the thinking. The thinking lives in `brain/`.

## Layout

```
cos/
  config.py       load and validate config.json. `python3 -m cos.config --check`
  redact.py       identity stripping, applied at ingestion
  store.py        the evidence store: JSONL, watermarks, dedupe
  sources/        one module per source type, all implementing sources/base.py
  ingest.py       cron 1
  cluster.py      rule-based clustering and scoring, no model calls
  agent.py        headless invocation of whatever agent CLI is installed
  questions.py    the founder question bank: parse, append, promote, retire
  ideate.py       cron 2
  review_page.py  the self-contained HTML review page
  adapters/       provider adapters for image, video and voice, behind one interface
  produce.py      one approved idea, stepwise, with a human gate between every step
  gate.py         the batch gate
config.json       yours. Never holds a secret, only variable names
run-ingest.sh     what the scheduler calls
run-ideate.sh     what the scheduler calls
AGENT-IDEATE.md   how your system thinks. Edit this, not the Python
```

## The commands

```bash
python3 -m cos.config --check                      # validate config before anything else
python3 -m cos.ingest --dry-run --limit 5          # print what it would write, write nothing
python3 -m cos.ingest --source calls_export        # one source
./run-ingest.sh                                    # everything, the way the scheduler calls it
python3 -m cos.ideate --no-agent                   # rule-based ranking, no model call
./run-ideate.sh                                    # the full weekly run
python3 -m cos.produce --queue 2026-09-01 --idea 3 --step script
python3 -m cos.gate outputs/drafts/2026-09-01-i3/batch.json
```

## Three things that hold everywhere in this package

**A model call is for judgement.** Deduplication, recency windows, cost arithmetic and file naming
are rules, and they are written as rules. The only model call in the scheduled path is the ideation
judgement pass.

**Every paid call goes through one guard.** `adapters/base.py:spend_guard`. It refuses without an
approved batch id in `COS_APPROVED_BATCH`, and refuses again if the weekly cap would be exceeded. A
guard that only covers the paths somebody remembered is not a guard, so it sits above every provider
rather than inside each one.

**The two scheduled jobs read and write local files.** They never publish, never send, and never
spend. That is what makes them safe to run unattended, and it is the property to protect if you
extend them.

## Adding a source

Write a class in `cos/sources/` implementing the contract in `base.py`, register it in
`cos/sources/__init__.py`, add a spec to `config.json`, and run with `--dry-run --limit 5` before it
ever writes. Read the five records out loud and check the redaction actually worked.

## Adding a provider

Write a class in `cos/adapters/` implementing the contract in `base.py`, including a real `estimate`
from the vendor's rate card, and register it in `cos/adapters/__init__.py`. Call `self._guarded`
rather than the vendor API directly, or the spend guard does not apply to you.
