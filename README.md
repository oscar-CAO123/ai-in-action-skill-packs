# AI in Action skills

**Current pack: 1 September 2026.** The beginners skills hub for the AI in Action calls. Everything
given away, in one plugin you install once and never think about again.

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

Then type `/start-here`. It looks at what you already have and names the one skill to run next.

Prefer to do it by hand? Copy any folder from `skills/` into `~/.claude/skills/` and it works the
same way. The files are the product; the plugin is only the delivery.

## Start here if it is your first one

**`member-business-interview`** builds the brain every other skill assumes exists. It talks to you
for two or three hours, one question at a time, then writes your business down as files your agent
can read. Everything in this repository gets noticeably better once it has run.

After that, `/start-here` will ask what you are trying to do and point you at the right one.

## What is in the plugin

| Skill | What it does |
|---|---|
| `member-business-interview` | The deep interview that writes your business down as files. Run this first. |
| `gauntlet-goal` | Makers and blind critics, working in parallel against an answer key you approved. |
| `share-your-skills` | Turns your own skills folder into a repo that installs as a plugin, so your team gets them with one command. |
| `computer-use` | The router for getting an agent to operate software: a CLI, a macro, driving the screen, and LinkedIn outreach as the worked example. |
| `member-workflow-graph` | Takes one workflow you already run and turns it into a skill that does that work. |
| `content-formats` | The craft skill for ad scripts, copy, hooks, VSLs, posts and carousels, routing to 30 format skills. |
| `seedance-prompt` | Structured video prompting: one reference image into one unbroken photoreal take. |
| `stop-the-slop` | Two passes that take the signs of AI writing out of anything going in front of customers. |
| `workspace-audit` | Checks every claim your routers and READMEs make against what is actually on disk. Read-only. |
| `funnel-builder` | One offer into a whole quiz funnel: quiz, scoring bands, landing page, result pages, emails. |
| `content-from-calls` | Conversations the business already has, turned into published content. |
| `engagement-signal-leads` | A lead source built on intent rather than demographics. |
| `reply-agent` | An agent on the reply side of an outbound campaign. |
| `sending-infrastructure` | Email sending that does not put the main business domain at risk. |

Plus one command, `/start-here`, which reads your working directory and points you at the right one.

Each call's run order is written down in [`drops/`](drops/). The current one is
[1 September 2026](drops/2026-09-01.md).

## How to use one without the plugin

```
1. Copy the one folder you want out of skills/.
2. Open your agent in your own project.
3. Tell it: read <skill file> and follow it.
```

The interview skills expect to talk to you for a while. That is the point of them. Answer with real
field names, real numbers and real thresholds and you get something that runs. Answer vaguely and you
get a plan.

## What changed on 1 September 2026

This pack supersedes the 18 August one. Until now the repository was organised as one folder per
call date, which is a good archive and a bad thing to install: you had to know which date held the
skill you wanted, and nothing updated by itself.

It is now a single plugin with a flat `skills/` directory. Add the marketplace once, turn auto
update on, and every later call lands on your machine without you doing anything.

Also on 1 September: `share-your-skills` and `stop-the-slop` were added, the four automation skills
were gathered under one `computer-use` router, `build-headless-cli` joined them, and `diary` and
`do-smart-things` were removed.

If you cloned the old dated layout, it is preserved in git history at the tag
`dated-drops-2026-08-18`.

## Licence

MIT. Take it, change it, ship it, sell what you build with it.
