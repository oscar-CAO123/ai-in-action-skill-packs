---
description: The AI in Action skills hub. Shows what is installed and works out which skill to run next.
---

## Your task

The user has just installed the `ai-in-action` plugin and typed `/start-here`. They are most likely
new to running skills. Do not lecture them. Work out where they actually are and give them one next
step.

1. Look at the current working directory. Check whether an intelligence layer already exists (a
   folder tree holding identity, people, customers, SOPs and a tech stack), and whether a diary
   folder exists with any entries in it.

2. Then say, in a few short lines:

   - **No intelligence layer yet:** the next step is `member-business-interview`. Tell them plainly
     that it talks to them for two or three hours, one question at a time, and writes their business
     down as files every other skill in this plugin reads. Ask if they want to start it now.
   - **Intelligence layer, no diary entries:** the next step is `diary`, run at the end of a day for
     a week. Five minutes each time.
   - **Both exist:** they are ready for `do-smart-things`. Three words, and they work because the
     other two gave the agent a world to read.

3. Only if they ask, list the other thirteen skills in one line each, grouped as build (`gauntlet-goal`,
   `member-workflow-graph`, `build-deterministic-macro`, `codex-computer-use`), market
   (`content-formats`, `seedance-prompt`, `content-from-calls`, `funnel-builder`), outbound
   (`linkedin-outreach`, `engagement-signal-leads`, `reply-agent`, `sending-infrastructure`) and
   maintain (`workspace-audit`).

Never run a skill without the user saying yes first.
