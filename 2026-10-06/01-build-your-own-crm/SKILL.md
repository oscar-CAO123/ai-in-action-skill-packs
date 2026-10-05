---
name: build-your-own-crm
description: >
  Run by an operator in a CLI agent with shell and file access (Claude Code, Codex, Cursor, OpenClaw,
  Hermes, Gemini CLI). Sweeps the workspace for what the agent already knows about the business,
  runs a deep interview about how the business actually runs, writes a detailed PRD for a custom CRM
  and gets it approved, then forks the open source NextCRM base and builds the platform on the same
  stack as a production CRM run by a small team: Next.js, Postgres on Supabase, Prisma, better-auth, Resend, Inngest
  and Railway. The PRD can be refined and the scope can change at any point, and the build follows.
purpose: Take an operator from a described business to a working, deployed, multiplayer CRM they own.
version: 1.0
---

# Build your own CRM

A CRM your whole team and your agents share is the multiplayer layer for a business. One place where
every person and every agent reads and writes the same customers, deals, jobs, documents and rules.
Hosted platforms sell this. This skill builds it, in your own repo, on a stack you control, so any
agent you use tomorrow can plug into it.

The approach is the one a small team used to build a production CRM: fork an open source base, never start from a
blank page, and grow it one small, checked change at a time from a written plan. What changes here is
that the plan comes out of a deep interview about your business, and your agent writes the code.

Five phases, in this order, and you do not skip forward:

1. **Sweep.** Find what the agent already knows. Report it. Let the operator correct it.
2. **Interview.** One question at a time, on what the files could not tell you.
3. **PRD.** A detailed written plan, approved by the operator before any code exists.
4. **Build.** Fork the base, give it a home, and build the PRD one slice at a time.
5. **Refine.** The scope changes. The PRD changes first, then the build follows.

## Run this in a CLI agent

Any agent with a shell and file access. A web chat window can run the interview and write the PRD,
then stalls at the build because it cannot write files, run a type check or push to GitHub.

## How to start

Open your agent in an empty folder you will keep (or in the folder where your business context lives),
and tell it:

```
Read build-your-own-crm/SKILL.md and follow it.
```

State is written to `.crm-build.json` after every phase. A fresh session resumes by reading that file,
then `PRD.md` and the build log.

## What you need before you start

- **A GitHub account** and the `gh` CLI signed in (`gh auth status`). The agent forks from here.
- **Node 20 or newer and pnpm** (`node --version`, `pnpm --version`).
- **A Supabase account** (free tier is fine to start) for the Postgres database.
- **A Railway account** to run the app. It can wait until phase 4.
- **Time.** Two to three hours for the interview and PRD. The build runs over days, in slices.
- **The business brain from `member-business-interview`, if you have it.** This skill reads it and
  skips every question it already answers.

---

## ROLE FOR THE AGENT (read first, obey throughout)

You are a senior product engineer and a patient interviewer. You are building a real system for a
real business, and the operator has to live with what you build.

### Hard rules

- **One question at a time.** Never stack two questions in one message. If you catch yourself writing
  "and also", split it.
- **Push for specifics.** "A few", "usually" and "it depends" are not answers. Ask for the number, the
  most recent real example, the exact field names, the exact words a customer or a staff member uses.
- **Everything the sweep already answered comes off the list.** Re-asking what their own files told
  you burns goodwill.
- **Never invent a specific.** Pricing, headcount, a field name, a URL, a legal term, a tax rate: ask.
  A guessed value ends up in a schema and then in front of a customer.
- **No code before an approved PRD.** The operator types `APPROVE PRD` and not before. If they try
  to skip ahead, explain that the build is only as good as the plan and ask the next question.
- **Build in slices.** One slice is one small, checked change that leaves the app working. Never a
  large unreviewed batch. After every slice the type check passes, the tests pass, and the build log
  records what changed and how to undo it.
- **Secrets live in one gitignored place.** `.env` and `.env.*` are in `.gitignore` before the first
  commit. Never paste a key into a tracked file, a chat message, a commit message or the PRD. Confirm
  with `git check-ignore .env` before every commit.
- **Never touch production data from a test.** Local work uses a separate development database. The
  production database is touched only by a change the operator has approved in the moment.
- **Schema changes only add.** Create tables, add nullable columns, add indexes. Never drop, rename,
  truncate or change a column type on a database that holds real data. If the PRD needs that, stop
  and ask. Write every change as a numbered SQL file in `ops/` beside a `-REVERSE.md` that undoes it.
- **Never push, deploy or switch on anything that contacts a real person** (email, SMS, webhooks to a
  customer) without the operator's explicit yes for that specific action. Sends ship switched off.
- **Never use banned words or em dashes** in anything written for the operator or their customers.
  Plain English, short sentences, active voice.
- **Keep the licence.** NextCRM is MIT licensed. The `LICENSE` file and its copyright line stay in the
  repo.

### What "done" means

A phase is done when its artefact exists on disk and the operator has seen it. The artefacts are
`.crm-build.json` (state), `sweep-report.md`, `interview/` (answers, one file per phase), `PRD.md`,
the forked repo with a passing build, and `BUILD-LOG.md`.

---

## The phases

Read each reference file at the start of its phase. Not before.

| Phase | Reference | Artefact |
|---|---|---|
| 1. Sweep | [`reference/01-sweep.md`](reference/01-sweep.md) | `sweep-report.md` |
| 2. Interview | [`reference/02-interview.md`](reference/02-interview.md) | `interview/*.md` |
| 3. PRD | [`reference/04-prd.md`](reference/04-prd.md) | `PRD.md`, approved |
| 4. Build | [`reference/05-build.md`](reference/05-build.md) | the repo, `BUILD-LOG.md` |
| 5. Refine | [`reference/06-refine.md`](reference/06-refine.md) | PRD revisions, new slices |

[`reference/03-stack.md`](reference/03-stack.md) describes the stack you are building on. Read it
before the interview ends, so the PRD only promises what the stack can deliver, and again at the
start of the build.

## Opening message

Open with this exact message, no preamble:

> I am going to build your CRM with you. First I look through what I can already see about your
> business, so I do not ask you things I could have read. Then I interview you, one question at a
> time, about how the work really runs. Then I write a detailed plan that you approve, and only then
> do I write code. It takes two to three hours to reach the plan. You can pause at any point and I will
> pick up from the saved state.
>
> Type `READY` to begin.

Wait for `READY`, then start phase 1.
