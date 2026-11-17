# 17 November 2026

Four packs, given away on the AI in Action call, Tuesday 17 November 2026. The theme was loops that
check their own work.

Root of the repo: [../README.md](../README.md). Three of these (01, 02, 04) install with the
`ai-in-action` plugin; the Grok Bot routines are files you copy into your bot's repository. Licence: MIT, see [../LICENSE](../LICENSE).

Every one of these is a **skill file**: plain markdown your agent reads before it does the work.
Nothing to install, no account, no service in the middle.

## The packs

### `01-agent-loops/`
Turns any task into a loop that checks its own work, and hands back one prompt any agent can run.
It asks what done means and turns it into a check, picks the smallest shape (solo, maker and checker,
or a gauntlet), and always sets a hard stop. Includes how Boris Cherny, who built Claude Code, and a
colleague run loops, and `release-gate.py`: the gate this drop itself passed before it was shared. Copy it for
your own releases: `python3 release-gate.py <folder> [<repo root>] [<private word list>]`.

### `02-email-newsletter/`
Builds a designed HTML email newsletter on your computer, checks it with `check.mjs` (layout, alt
text on images, size, an unsubscribe line), and hands you the file. It never sends: you press send in your own
email tool. `deliverability.md` is the checklist for landing in the inbox.

### `03-grok-bot-routines/`
Grok Bot is xAI's always-on agent that runs jobs on a schedule; any agent that can read a file and
run on a timer works the same way. Four routines for it: inbox sort, after-hours call follow-through, find
the money (overcharges on supplier invoices) and win-back. Each says when it runs, what it reads, its
steps and its gate. All are drafts only, and the money one never pays or disputes anything. Each lists the files it reads: create
those first (brand voice, FAQ, services list, booking diary, agreed prices, offer sheet, and empty
ledgers). Put the
file in the repository your bot reads, run it once by hand and watch it, then schedule it.

### `04-content-operating-system-update/`
What we added to the 18 August content operating system since: the pipeline edits, the animation
philosophy, and a shared library of moves. It extends `2026-09-01/07-content-operating-system/` (first shipped as
`2026-08-18/content-operating-system/`) and
replaces nothing.

## How this drop was checked

Every file passed `01-agent-loops/release-gate.py` and NVIDIA SkillSpector (see `2026-10-27/`) (no keys, no private names or paths, no em dashes,
no banned words, every skill complete), then four agents attacked it from four angles before a
person merged it.
