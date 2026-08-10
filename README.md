# AI in Action skill packs

Everything given away on the AI in Action calls, one folder per call date.

Each drop is a set of **skill files**: plain markdown your coding agent reads before it does the
work. Claude Code, Codex, OpenClaw, Hermes, whatever you run. There is nothing to install, no account
to make, and no service in the middle. Point your agent at a folder and tell it to follow the file.

That is deliberate. The tools churn every few months. Anything written as a file survives the churn.

## The drops

| Date | What landed | Folder |
|---|---|---|
| **11 August 2026** | Graph engineering, funnel builder, content formats, four marketing agents | [`2026-08-11/`](2026-08-11/) |

Nothing gets rewritten in place. A later drop that improves an earlier pack ships as its own dated
folder and says what it supersedes, so anything you cloned keeps working.

## How to use one

```
1. Clone this repo, or copy the one folder you want into your own project.
2. Open your agent in that folder.
3. Tell it: read <skill file> and follow it.
```

The interview skills expect to talk to you for a while. That is the point of them. Answer with real
field names, real numbers and real thresholds, and you get something that runs. Answer vaguely and
you get a plan.

## Start here if it is your first one

`2026-08-11/graph-engineering/member-business-interview`. It builds the brain every other pack in
this repo assumes exists, and all of them get noticeably better once it has run.

## Things that hold across every pack

- **A model call is for judgement.** If a step has a right answer a rule can produce, write the rule.
  Paying for inference to do arithmetic is the single most common way these builds get expensive.
- **Nothing irreversible without a person.** Every pack has an explicit approval boundary, and the
  default is narrower than you will want. Widen it after you have watched it for a fortnight.
- **The thing that writes the answer never grades it.** Every research pipeline in here runs a
  separate skeptic pass, and what it cannot resolve goes into a gaps list rather than getting waved
  through.
- **No secrets in tracked files, ever.** Keys live in a gitignored location the skills read from.
- **Plain English.** No em dashes, no "it's not X, it's Y", and a banned-words list in each file.

## Licence

MIT. Use them commercially, change them, ship them, sell what you build with them.
