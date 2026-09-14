---
name: agent-context-transfer
description: Move one business's core documentation and skill files into a single repository every agent can read, then have any agent (Grok Bot, Hermes, Claude Code, Codex, a voice session) discover it, inventory it, build the skills natively in that tool, map the context, then train itself into the orchestrator with three named sub-agents in one group chat and the delegation rules. Use when the user says "put my context in one repo", "share my brain with all my agents", "ingest the repo", "build my skills in Grok Bot", "set up the orchestrator", or is starting a new agent tool and wants it to know the business on day one. Do NOT use for moving secrets, customer records or client files; those never go in the repository.
---

# Agent context transfer

Two halves. The first builds the repository from the folder where the business already keeps its
files (the brain: context, skills, routers), text only, scanned for secrets and personal data. The
second is what an agent does the first time it is pointed at that repository: discover, inventory,
build the skills natively, map the context, plan the orchestrator, verify. If the business has no
brain folder yet, run `member-business-interview` first
(`2026-08-11/graph-engineering/member-business-interview` in this repository); this skill assumes
the files exist.

## Half one: build the repository (the operator, once, then on every refresh)

1. Create a private repository (GitHub is fine) and clone it. This is the transfer repository.
2. Copy `examples/transfer.json` to `transfer.json` in the folder you will run the script from,
   and fill it in: the root of
   the brain folder, the repository clone path, the include globs (routers, context, skills, code
   the skills call), the exclude patterns (customers, candidates, proposals, meetings, outputs,
   data dumps, vendored libraries, anything binary), the email domains that are allowed to stay.
3. Run `python3 scripts/build_transfer.py transfer.json` (the manifest path is relative to where
   you run it). It checks the manifest, prints what it is about to clear and asks once before it
   wipes the clone's working tree (never `.git`; pass `--yes` to skip the prompt on a refresh),
   copies what the manifest includes, redacts phone numbers and personal email addresses
   in the copies, refuses to continue if anything that looks like a key or token is found, writes
   `README.md`, `CLAUDE.md` and `AGENTS.md` (the router) and `INGEST.md` (the first file an agent
   reads), and prints what it did.
4. Read the printout. Open any file it flagged. Review `git diff`. Commit. Push only when you have
   looked.
5. Refresh by running step 3 again. The manifest is the contract; edit it, never the copies.
6. If the printout shows a redaction you did not expect (a year, a price, an order number caught
   as a phone), tighten `phone_pattern` in the manifest; the default only matches numbers that
   start with a country code or a leading zero.

Laws for half one:

- Text only. Markdown, scripts, small configs. No PDFs, images, archives, exports.
- No secrets, ever. Keys live in a gitignored folder on the machine, never in a repository, not
  even a private one. The script stops on anything that looks like one.
- No records. Customers, candidates, clients, proposals, meetings, transcripts stay out by path.
  The agent that needs one asks; it never finds one here.
- One business per repository. Mixing two businesses gives every agent two sets of rules.

## Half two: ingest and build (any agent, first session in the repository)

Read `INGEST.md`, then work in order. Write everything under `_native/` and nowhere else. Ask
before you assume.

### Phase 0: ground truth (no writing yet)

1. Read `INGEST.md`, then `CLAUDE.md`. Say back, in three lines, what the business does, who the
   agent reports to, and the three rules you will be held to.
2. List the tree to two levels. Count the skill files: every `*.md` directly inside a skills
   folder, every `SKILL.md`. Report the count before you go on. Zero means the wrong folder was
   transferred or the manifest excluded the skills: stop, say which, and ask.

### Phase 1: discovery

For every file except this skill and `_native/`, decide its kind: `context` (knowledge about the
business), `skill` (an instruction set with a trigger and steps; the frontmatter `description`
carries the triggers), `code` (a script a skill calls), `reference` (material a skill reads while
it runs), `template` (a fill-in), `router` (`CLAUDE.md`, `AGENTS.md`, any `INDEX.md`). Read the
first forty lines of each to decide its kind. For a `skill`, read the WHOLE file: the dependencies
live in the step text (a path outside the repository, a token, a service, a CLI, another skill),
never only in the frontmatter. Do not read scripts end to end; note what they import and what
they call out to (a URL, a CLI, an environment variable): that is the dependency.

### Phase 2: the inventory

Write `_native/inventory.md`: one row per file with `path`, `kind`, `purpose` (one sentence, your
words), `triggers`, `depends on` (files, scripts, tools, tokens, local paths, connections),
`runnable here` (yes / with a connection / with a file / no, and why; "with a file" is a path
outside the repository, "with a connection" is a token, a sign-in or a service). Then a summary: counts per kind, the ten
skills with the fewest dependencies, and every dependency that names something outside the
repository, grouped: local path, CLI tool, credential, external service, other agent. Show the
summary. Wait for a go.

### Phase 3: build the native skills

For each `skill` row, fewest dependencies first, create one native skill in this tool. Use the
tool's own skill format if it has one; otherwise write `_native/skills/<name>/SKILL.md` with
frontmatter `name`, `description` (every trigger phrase from the source kept), `source` (the
repository path), then: **What it does** (two lines); **Context it reads first** (repository
paths, in order, every context file the source names or clearly needs, an INDEX resolved to its
files); **Steps** (the source's steps in order and in substance, rewritten only where they name a
tool you do not have: a local script becomes "run `<path>`" or "needs: code runner", a token or a
system becomes "needs: <connection>" and the step waits there); **Gates** (everything the source
says never to do, verbatim, a hard stop here); **Output** (what it produces and where, under
`_native/out/<name>/` unless the source names a place). Append to `_native/manifest.json`: `name`,
`source`, `native_path`, `triggers`, `needs` (each prefixed `connection:`, `file:`, `tool:` or
`skill:`), `status` (`ready` / `needs-connection` / `needs-file` / `needs-code-runner`). Never merge two skills. Never invent a step. Never drop a skill that cannot
run yet; build it and mark its status.

### Phase 4: the context map

Write `_native/context-map.md`: for each kind of question an operator or a sub-agent will ask
(who is the business, what is the offer, how do we talk, who is the customer, what hurts them, how
is a sales call run, how is the core process run, which template goes out when, what is live now),
the one to three files to read, in order, and one line on what each gives. Every sub-agent gets
this file before its first task.

### Phase 5: become the orchestrator, stand up the department

You, the agent reading this, become the orchestrator: the head of department. You never do the
work yourself; you delegate it to a small number of sub-agents, keep them in one group chat, and
report to the operator. Write `_native/orchestrator.md`, then do what it says in this tool.

**Train yourself first.** Read the company overview, the agent identity file if there is one,
`_native/context-map.md` and `_native/manifest.json`. Write your identity block at the top of
`_native/orchestrator.md`: who the business is, who you serve, what you own (delegation, the chat,
the daily report, the backup, the spend) and what you never do (send, post, deploy, spend, write
to production, invent a record, do a sub-agent's job). Give yourself a random human first name;
the title is Head of Department.

**The sub-agents.** Start with three, never more on day one; the department grows on the
operator's word. Derive the three from the business's own functions as the context describes
them (for a service business the usual split is client fulfilment, the core operational process,
and marketing and content; use the business's words). Each gets a random human first name and a
fixed title, its own section in `_native/orchestrator.md` with its remit, the context files it
reads before any task (from the context map), and the native skills it owns from the manifest
(matched by what the skill produces). A skill that fits none stays with you, listed as held.

**The group chat.** Create one chat with the sub-agents and yourself, named for the department.
Post the rules as its first message and write them into `_native/orchestrator.md`: every
delegated task is posted there by you (sub-agent, skill, context files, gate); every result comes
back there as a path plus a three-line summary; nothing is decided in a private message;
sub-agents talk to each other in the chat when a task crosses remits, and ask rather than assume;
one topic per thread; every message costs tokens, so no acknowledgements or status for its own
sake; the operator reads the chat and anything meant for them is addressed by name.

**Delegation rules.** Written into `_native/orchestrator.md` and held to:

1. Chief of staff first, specialists second. You were stood up first and designed the department
   from the business's functions; a new function is proposed (remit, skills) before it is created.
2. Same org chart as humans. Human names, real titles, one remit each, sections by function.
3. Match by trigger: request to skill by the manifest's trigger phrases, skill to owner. No match
   means ask, never improvise.
4. Pass down the whole brief: the request in the operator's words, the context map, the skill
   name, the gates verbatim, where the output goes.
5. Routines ask before they fire: a scheduled routine wakes, looks, says what it would do and
   what it would cost, and runs on a yes. You are not the first domino by default.
6. The approval line: anything that leaves this tool (email, post, deploy, purchase, a write to
   another system, a message to a customer) is drafted by the sub-agent, posted in the chat, and
   shown to the operator by you. Nothing leaves without a yes.
7. Spend governor: you track usage; ahead of budget means you pause routines and say which,
   before the cap. A paid tool unused for a month goes on the chopping block in your report.
8. The daily backup: once a day, everything that changed in this tool (identity, sub-agents,
   skills, chat rules, routines, connections) is written back to `_native/` in the repository and
   committed, so the department can be rebuilt anywhere. The file outlives the tool.
9. The daily roundup: once a day, at an off-hour the operator sets, one message: what shipped,
   what is waiting on them, what it cost, what is next.
10. Quality gates travel: every word a sub-agent writes for the business passes the business's
    own copy rules before it is posted.

If this tool cannot create sub-agents or a group chat, `_native/orchestrator.md` is the plan, you
say so, and you name the one thing the operator has to click. Log what you created (names,
titles, chat, routines) in `_native/orchestrator-log.md`.

### Phase 6: verify

Every skill row has exactly one manifest entry (print both counts). Open three native skills at
random and trace each step to its source. Search every file under `_native/` with your tool's
text search for `api_key`, `secret`, `token=`, `sk-`, `gho_`, `ghp_`, and for email addresses
outside the allowed domains; there must be none, and if there are, stop and say where. Run one `ready` skill end to end on a harmless input and show the
output, or name the connection that would unlock the first one. Report in five lines: built, ready
now, waiting on which connections, the sub-agents by name and title plus the chat, the one thing
to do next.

## What is in this pack

- `scripts/build_transfer.py`: the manifest-driven exporter with the secret and PII scan.
- `examples/inventory-row.md` and `examples/manifest-entry.json`: the shape of one inventory row
  and one manifest entry, so every run writes the same columns.
- `examples/transfer.json`: a filled manifest for a brain folder laid out as
  `context/`, `skills/`, `agent/`, with the usual excludes.
- `templates/INGEST.md`: the first file an agent reads; the exporter writes it from the manifest.

## Lessons carried in

- The inventory before the build. Building from a half-read repository produced skills that
  pointed at files that did not exist.
- A skill that cannot run yet is still worth building. The gap it names is the next connection to
  make, and it is usually a sign-in away.
- The gates travel verbatim. A softened "never send" became a send in one earlier run.
- "Fewest dependencies" is only true after the whole skill is read. The test run ranked by
  frontmatter, built three, and found the hidden ones in the step text afterwards.
- Two contact-list files nearly went in on the first build because they lived under `context/`.
  The scan caught them. Read the printout every time.
