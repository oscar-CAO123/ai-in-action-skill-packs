---
name: do-smart-things
description: Read everything the user owns in this working tree, pick the single highest-value thing to build next, get a yes, then build it through an inline gauntlet of makers and blind critics. Use when the user types "do smart things", "$do-smart-things", "/do-smart-things", or asks the agent to work out what to do next and go do it. Do NOT use when the user has already named the task (prompt it directly), when the tree has no goals or context to read, or when the work needs an external send, deploy or paid action.
---

# do smart things

Three words on top of full context. The user stops assigning tasks and starts setting the conditions
the work happens in. You find the work, propose one thing, and build it to a bar.

Grounded in Allie K. Miller's account of running a 34-agent workforce, on Greg Isenberg's podcast,
18 August 2026. Her strongest prompt is three words sitting on top of every context document she
owns. This skill is that prompt made repeatable in a working tree.

## The one rule

Context first, always. The three words are worthless on an empty tree and strong on a full one. If
the sweep comes back thin, say so and build the context instead of guessing at a task.

## Step 1: locate the world

Detect the environment at runtime. Never assume a path, a vault, a stack or a company.

Establish the root: the git top level if there is one, otherwise the working directory. Then read,
in this order, only what exists:

1. **The diary index.** Any of `diary/INDEX.md`, `.diary/INDEX.md`, `*/diary/INDEX.md`. This is the
   highest-priority source in the tree. It holds what the user decided, corrected and left open, and
   it is more current than any file. Read the index, then the three most recent entries.
2. **Routers and rules.** `CLAUDE.md`, `AGENTS.md`, `README.md`, `INDEX.md`, `.cursorrules`,
   `CONTRIBUTING.md`, `docs/README.md`, and any file the routers point at as authoritative.
3. **Goals.** Anything matching goals, roadmap, OKR, north-star, strategy, PRD, plan, TODO, backlog.
4. **Live state.** `git log -20 --oneline`, `git status --short`, branch list, and the twenty most
   recently modified tracked files. What is half-finished is usually what matters.
5. **Targeted reads.** Only now open the specific files the four sources above named.

Read routers and indexes in full. Read everything else by what the indexes point at. A tree with
good indexes should cost a few dozen reads, not a full crawl.

Never open `.env`, `.env.*`, credential files, key files, token files or anything a gitignore hides.
If a router names a secret location, record that it exists and move on.

If the tree has no routers, no goals and no diary, escalate: fan out parallel readers over the top
two directory levels, merge what they find, and tell the user their tree is unindexed.

## Step 2: the context map

Write what you learned to `.smart-context/map.md` at the root. Header carries `generated:`, `head:`
(the git sha), and `sources:` (the exact paths read). Body carries: what this project is, the stated
goals, the current state, the open loops, the constraints and rules, and the named unknowns.

On later runs, read the map first. It is fresh when the recorded sha matches `git rev-parse HEAD` and
no source file is newer than the map. When it is stale, re-read only the sources that changed and the
diary index, then rewrite the map. Say in one line whether you reused the map or re-swept.

Add `.smart-context/` to the gitignore if one exists and the entry is missing.

## Step 3: pick one task

From the map, name the single highest-value thing to build next. Rank candidates on: it moves a
stated goal, it clears something the user is currently blocked by or keeps correcting, it is
finishable in this session, and it can be checked without the user's eye.

Reject candidates that need an external send, a deploy, a payment, a production write or a decision
only the user can make. Those go in a short "needs you" list instead.

## Step 4: the gate

Put one short proposal to the user before any file changes:

- The task, in one sentence.
- Why it, over the runners-up, traced to the goal or the open loop it serves.
- What passes for done, as checks, not adjectives.
- What it will touch, and what it will not.

Wait for a yes. A different pick from the user replaces yours without argument.

## Step 5: run the gauntlet inline

Use `gauntlet-goal` when that skill is available in the environment: it is the same contract and it
carries the fuller reference. Otherwise run the graph directly in this session, using subagents:

1. **Planner.** Splits the task into the smallest independent pieces, declares dependencies, and
   assigns exactly one writer per file. Writes the answer key first: atomic checks, each naming its
   artifact, its verification command and the expected result. The answer key predates every maker.
2. **Makers, one per piece.** Each improves only its owned piece against the answer key. Parallel
   only where no two pieces write the same file. Serialise anything else.
3. **Blind critics, one per piece.** Each sees the answer key, the artifact and the evidence. Never
   the maker's commentary, never the iteration count. Returns pass or fail, the failed checks and the
   concrete defects. A critic never edits.
4. **Repair.** Failed checks go back to the same maker, at most twice. Re-run the critic after every
   change.
5. **Integrator.** Assembles passed pieces only, resolves interfaces, redesigns nothing.
6. **Final critic.** Tests the assembled result against the whole-task bar and every answer-key check.

Keep a pass log: agent, owned piece, artifact path, critic result, changed checks, next action.

Stop the run on conflicting writes, a missing reference, a permission boundary, or two consecutive
passes with no measurable improvement.

## Step 6: write back

Append one line to the diary for the day, through `/diary` when that skill is present, otherwise
straight into the diary file: what you built, why you picked it, what passed, and what is still open.
The next run reads it. That loop is the whole point.

Then report: the artifact paths, the evidence paths, the checks that passed, the checks that failed,
and the "needs you" list from step 3.

## The ceiling

Local files and local commands only. Stop at a human gate, every time, before: any push, deploy,
publish, send, post, schedule change, paid API call, production write, schema change, or anything
touching credentials. Reaching one of those is a stopping point to report, never a thing to route
around.

Do not widen the ceiling because the task would be better with it widened. Say what you would need
and let the user decide.

## When this is the wrong skill

The user already named the task: just do the task. The tree is empty or brand new: build the context
first. The work is one small edit: make the edit, a gauntlet on a typo is waste.

## House rules for anything this skill writes

No em dashes. Never "it is not X, it is Y" in any form, say the positive thing directly. Every status
claim traces to a command you ran or a file you read in this session, and anything unverified is
called unverified.
