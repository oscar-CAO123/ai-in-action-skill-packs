# AI in Action skill packs

Everything given away on the AI in Action calls, one folder per call date.

Each drop is a set of **skill files**: plain markdown your coding agent reads before it does the
work. Claude Code, Codex, OpenClaw, Hermes, whatever you run.

Nothing gets rewritten in place. A later drop that improves an earlier pack ships as its own dated
folder and says what it supersedes, so anything you cloned keeps working.

## The drops

| Date | What landed | Folder |
|---|---|---|
| **11 August 2026** | Graph engineering, workspace audit, funnel builder, content formats, four marketing agents | [`2026-08-11/`](2026-08-11/) |
| **18 August 2026** | The diary, the three-word prompt, the gauntlet, and a content operating system that feeds itself | [`2026-08-18/`](2026-08-18/) |
| **1 September 2026** | The gauntlet, sharing your skills as a plugin, computer use, Seedance prompting, content formats, stop the slop, the content operating system | [`2026-09-01/`](2026-09-01/) |

## Install the current drop as a plugin

New on 1 September: the repository is also a Claude Code plugin marketplace, so you can install the
current drop instead of copying folders around. In Claude Code or Codex, type `/plugin`, then:

```
/plugin marketplace add oscar-CAO123/ai-in-action-skill-packs
/plugin install ai-in-action
```

**Turn on auto update** in the plugin menu. Every later call lands on your machine by itself.

The plugin serves the **current drop**, which is [`2026-09-01/`](2026-09-01/). The older folders stay
where they are and stay readable. `02-share-your-skills` in that drop shows you how to do this with
your own skills.

Then type `/start-here`. It looks at what you already have and names the one skill to run next.

## Or use one by hand, with no plugin at all

```
1. Clone this repo, or copy the one folder you want into your own project.
2. Open your agent in that folder.
3. Tell it: read <skill file> and follow it.
```

The interview skills expect to talk to you for a while. That is the point of them. Answer with real
field names, real numbers and real thresholds and you get something that runs. Answer vaguely and you
get a plan.

## Start here if it is your first one

`2026-08-11/graph-engineering/member-business-interview`. It builds the brain every other pack in
this repo assumes exists, and all of them get noticeably better once it has run.

Then `2026-08-18/diary`. Run it for a week, and the rest of the repo starts reading your actual
situation instead of guessing at it.

## Licence

MIT. Take it, change it, ship it, sell what you build with it.
