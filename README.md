# AI in Action skills

The beginners skills hub for the AI in Action calls. Everything given away, in one plugin you
install once and never think about again.

A **skill** is a plain markdown file your coding agent reads before it does the work. A **plugin**
is just a way for the agent to find them. This repository is both: a marketplace and the plugin
inside it.

## Install

In Claude Code or Codex, type `/plugin`, then:

```
/plugin marketplace add oscar-CAO123/ai-in-action-skill-packs
/plugin install ai-in-action
```

That is the whole setup. Nothing to clone, no account, no service in the middle.

**Turn on auto update** in the plugin menu. Every time a call adds a skill, it lands on your machine
by itself.

Prefer to do it by hand? Copy any folder from `skills/` into `~/.claude/skills/` and it works the
same way. The files are the product; the plugin is only the delivery.

## Start here if it is your first one

1. **`member-business-interview`** builds the brain every other skill assumes exists. It talks to you
   for two or three hours, one question at a time, then writes your business down as files your agent
   can read. Everything in this repository gets noticeably better once it has run.
2. **`diary`** for a week. Five minutes at the end of a day. It captures the context that never lands
   in a meeting, an email or a commit.
3. **`do-smart-things`**. Three words, and they only work because the two skills above gave the agent
   a world to read.

## What is in the plugin

| Skill | What it does |
|---|---|
| `member-business-interview` | The deep interview that writes your business down as files. Run this first. |
| `diary` | Daily context capture, filed so agents can query it. The corrections section is the valuable one. |
| `do-smart-things` | Reads everything you own, picks the highest-value thing to build next, gets a yes, builds it. |
| `gauntlet-goal` | Makers and blind critics, working in parallel against an answer key you approved. |
| `member-workflow-graph` | Takes one workflow you already run and turns it into a skill that does that work. |
| `workspace-audit` | Checks every claim your routers and READMEs make against what is actually on disk. Read-only. |
| `funnel-builder` | One offer into a whole quiz funnel: quiz, scoring bands, landing page, result pages, emails. |
| `content-formats` | The craft skill for ad scripts, copy, hooks, VSLs, posts and carousels, routing to 30 format skills. |
| `seedance-prompt` | Structured video prompting: one reference image into one unbroken photoreal take. |
| `codex-computer-use` | How to let an agent drive your actual screen without wrecking anything. |
| `linkedin-outreach` | An approved batch of connection invitations, sent through supervised Computer Use. |
| `build-deterministic-macro` | A bounded click and keyboard path for work that needs no model reasoning. |
| `content-from-calls` | Conversations the business already has, turned into published content. |
| `engagement-signal-leads` | A lead source built on intent rather than demographics. |
| `reply-agent` | An agent on the reply side of an outbound campaign. |
| `sending-infrastructure` | Email sending that does not put the main business domain at risk. |

## How to use one without the plugin

```
1. Copy the one folder you want out of skills/.
2. Open your agent in your own project.
3. Tell it: read <skill file> and follow it.
```

The interview skills expect to talk to you for a while. That is the point of them. Answer with real
field names, real numbers and real thresholds and you get something that runs. Answer vaguely and you
get a plan.

## A note on the layout

Until 1 September 2026 this repository was organised as one folder per call date. It is now a single
plugin with a flat `skills/` directory, because a dated folder is a good archive and a bad thing to
install. The old layout is preserved in git history at the tag `dated-drops-2026-08-18` if you
cloned it and want to compare.

## Licence

MIT. Take it, change it, ship it, sell what you build with it.
