---
description: The AI in Action skills hub. Shows what is installed and works out which skill to run next.
---

## Your task

The user has just installed the `ai-in-action` plugin and typed `/start-here`. They are most likely
new to running skills. Do not lecture them. Work out where they actually are and give them one next
step.

1. Look at the current working directory. Check whether an intelligence layer already exists: a
   folder tree holding identity, people, customers, SOPs and a tech stack.

2. Then say, in a few short lines:

   - **No intelligence layer yet:** the next step is `member-business-interview`, which lives in the
     repository at `2026-08-11/graph-engineering/member-business-interview` rather than in this
     plugin. Tell them plainly that it talks to them for two or three hours, one question at a time,
     and writes their business down as files every other skill reads. Ask if they want to start it.
   - **It exists:** ask what they are actually trying to do next, then route:
     build something ambitious and verifiable, `gauntlet-goal`. Turn a job they already do by hand
     into a skill, `member-workflow-graph`. Get an agent operating software, `computer-use`. Make
     content, `content-formats`. Share what they have built with their team, `share-your-skills`.

3. Only if they ask, list the rest of the current drop in one line each: `seedance-prompt` for video
   prompting, `stop-the-slop` for anything going in front of customers, and
   `content-operating-system` for the whole content pipeline.

4. Everything from earlier calls is still in the repository by date, and it is not installed with
   this plugin. `2026-08-11/` holds the business interview, the workspace audit, the funnel builder
   and four marketing agents. `2026-08-18/` holds the diary and do-smart-things. Point them at the
   folder rather than pretending the skill is available.

Never run a skill without the user saying yes first.
