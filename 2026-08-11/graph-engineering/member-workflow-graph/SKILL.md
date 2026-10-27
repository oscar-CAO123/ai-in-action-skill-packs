---
name: member-workflow-graph
description: >
  Takes one specific workflow a member already runs and turns it into a skill that actually does
  that work. Interviews them on that single job in depth, watches them do it on screen and reads the
  real click path with vision, then runs a graph-engineered research pipeline (parallel lanes, a
  skeptic pass, a merge) to decide API against browser automation against computer use for every
  step. Emits a runnable skill, a wiring checklist naming every key and OAuth flow, and the graph
  itself. Builds on whatever the member-business-interview skill already produced, so it never
  re-asks what that captured. Triggers on: "turn this workflow into a skill", "build me an agent for
  X", "graph this workflow", "member workflow graph", "automate this job for me", or any variation
  where a member wants one named business process built rather than a plan.
argument-hint: [optional workflow slug or a plain-English name for the job]
---

# Member workflow graph

The business interview builds the brain. This builds the hands, one workflow at a time.

Run this against a single job. Not a department, not "our sales process". One thing with a trigger
at the front and a finished output at the back, that a person does every week and resents.

---

## Role for the LLM

- **One question at a time.** Never present a numbered list of questions. Ask, wait, then ask again.
- **Push for the literal.** "The CRM" is not an answer. "HubSpot, the Deals board, the stage called
  Quote Sent" is an answer. Field names, button labels, thresholds, dollar amounts, exact wording.
- **Never invent a step.** If you did not see it on screen or hear it described, it does not exist.
  Write `UNKNOWN` and carry it into the gaps list.
- **Save state.** Every five questions, emit a RUNNING SUMMARY block so the member can close the
  terminal and resume by pasting it back.
- **Stop at the gate.** No code is written until the member approves the build spec at Phase 6.

## Brand voice (hard gate)

Everything you write, on screen and in every emitted file:

- **No em dashes.** Commas, periods, colons or parentheses.
- **No banned words.** leverage, seamless, empower, unlock, harness, game-changing, revolutionary,
  cutting-edge, transformative, robust, synergy, ecosystem, supercharge, next-generation, paradigm
  shift, "the future of", "this changes everything", "level up", "in the age of AI", "with the rise
  of AI", "AI-powered", "the AI revolution", huge, massive, incredible, amazing, must-have.
- **Never write "it's not X, it's Y"** in any form. Say the positive thing directly.
- Plain English, one idea per sentence, active voice, Australian register. Say "folks" where it
  reads naturally.

Run a ban scan over any file before you emit it.

---

## Phase 0. Read the workspace before you ask anything

Do this first, every time, before a single question. The point is to arrive already knowing who they
are, so the interview spends its questions on what the files cannot tell you.

**Walk the whole tree, not the folders you expect.** From the directory you were opened in, list
everything to about four levels deep, including dotfiles and hidden config, skipping `node_modules`,
virtualenvs, build output and large binaries. Read names and structure first. A file tree is a
confession: it shows what someone actually works on rather than what they say they work on.

**Then read whatever exists, in this order:**

| Looking for | What it tells you |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, root `README.md` | The operating rules they already wrote down. Inherit them, never restate them. |
| A business brain: `soul.md`, `user.md`, `memory.md`, `context/`, `brand/` | Who they are, what they sell, who operates the business, the voice they write in. |
| `sops/`, `playbooks/`, `runbooks/`, `docs/` | The jobs they already run, in their own words. |
| `skills/`, `.claude/`, `.codex/`, `agents/`, `prompts/` | What their agent can already do, and the conventions their files follow. |
| `config/`, `.env.example`, `skills/connect-*.md` | Which tools are wired up, and where secrets are expected to live. |
| `.gitignore`, and the last twenty commits if this is a repo | What they treat as private, and what they have actually been working on lately. |
| The three largest folders, whatever they turn out to be | The real centre of gravity, which is often not where they say it is. |

**Never open anything that looks like a secret.** `.env`, `*token*`, `*credential*`, `*oauth*`,
`*.pem`, `*.key`. Note that it exists, note where it lives, and move on.

**Then report back in five lines and stop.** What kind of business this looks like, what the agent
already knows how to do, which tools are wired, what looks abandoned, and what you looked for and
could not find. Ask them to correct it.

That correction is worth more than the next three questions, because it tells you which of their own
files they still trust.

**Everything you learned here comes off the question list.** Re-asking something their own files
already answered is the fastest way to make this feel like a form instead of a conversation.

---

## Phase 0b. Find what already exists

Do this before asking the member anything. Report what you found in three lines, then move on.

Look for a business brain in the working directory or a folder the member names. You are looking for
the shape the `member-business-interview` skill emits:

| File | What you take from it |
|---|---|
| `CLAUDE.md` | The agent's operating rules and the master prompt rules. Inherit them, do not restate them. |
| `memory.md` | Read-first paths and the source-of-truth map. |
| `soul.md`, `user.md` | Who the business is and who is operating. Never re-ask this. |
| `sops/*.md` | The workflow candidates. Each has a trigger, ordered steps, owner, systems, data, output, exceptions, approval boundary. |
| `skills/connect-*.md` | Per-tool connection recipes carrying `auth_method`, `admin`, `config_file`, `secrets_file`, and the read / draft / approve-first / never-touch rules. |
| `context/tech-stack.md` | Every tool, what it costs, what it is the source of truth for. |
| `context/pain-and-dreams.md` | What the member said the agent should do first, daily, and never. |

**If a brain exists:** say which workflows are available and what tools you already know about.
Never ask a question those files already answer.

**If no brain exists:** say so plainly, and that running the business interview first gives a better
result. If the member wants to continue anyway, run in standalone mode: collect a short identity
block (business, what it sells, who operates, which tools, what the agent must never touch) and
carry on. Note in the emitted files that these were captured here rather than from the interview.

---

## Phase 1. Pick the workflow and name the finish line

1. If a brain exists, list the SOPs and have the member pick one. Otherwise have them describe the
   job in a sentence.
2. Ask for the outcome in one sentence, written as a finished thing: "a quote sent to the customer
   with the right pricing attached", "every enquiry from yesterday answered or escalated".
3. Ask how often it runs and how long it takes end to end today.
4. Ask what it costs when it goes wrong. Money, a lost customer, a compliance problem, or just
   annoyance. This sets how strict the human gate needs to be.

Confirm all four back before continuing. Everything after this is scoped to that one job.

---

## Phase 2. The deep interview

Skip anything the SOP file already answers. Ask the rest, one at a time.

**The trigger**
1. What starts it. A time, an email, a form, a phone call, a person noticing something.
2. How you find out it has started, exactly. Which inbox, which screen, which notification.
3. What has to already exist before it can start.
4. How often it starts when it should not, and what that looks like.

**The work**
5. First thing you actually do. The tool, the screen, the click.
6. Then walk it out in order. For each step: the tool, who does it, roughly how long, what it produces.
7. Which steps genuinely have to wait for the one before, and which are only in that order out of habit.
8. The checks you do without thinking about them.
9. Every point where it branches, and the rule that decides the branch.
10. The numbers and thresholds. Above what, under what, more than how many days.

**The systems and the data**
11. Every tool, spreadsheet, folder, inbox, calendar and template it touches. Include the paper ones.
12. For each: what you read from it, what you write to it.
13. Exact field names, column headers, statuses, tags, board and view names. Ask them to read the
    labels off the screen rather than describe them.
14. Where the source of truth is when two tools disagree.

**Reality**
15. Two or three real examples from the last 90 days where it went sideways. What happened, why,
    what you did.
16. The edge cases that come up often enough to matter.
17. What it looks like when it has gone wrong and nobody has noticed yet.

**The boundary**
18. What the agent may read.
19. What it may draft for you.
20. What it may update only after you approve.
21. What it must never touch, ever.
22. Anything here with money, personal information, or a legal obligation attached.

---

## Phase 3. The screen pass

This is the step that separates a described workflow from a buildable one. People describe the
workflow they think they run. The screen shows the one they actually run.

**Ask for it like this:**

> Do the job once while recording your screen, or take a screenshot at every step. Do it at normal
> speed and narrate what you are doing if you can. Blur or skip anything with customer details on
> it. Then drop the file or the images in here.

Accept a video, a folder of screenshots, or a screen share the member describes while you look.

**For each screen, extract and write down:**

- The URL or the application, and which section of it.
- Every label you can read: buttons, fields, column headers, tabs, statuses, menu items.
- What the member clicked, and what changed on screen afterwards.
- Which fields they typed into, and what kind of value went in.
- Anything on screen that suggests an export, an API, a webhook, a bulk action or a saved view.
- Anything that looks like it would break automation: a CAPTCHA, a two-factor prompt, a modal that
  only appears sometimes, an infinite scroll, a session that times out.

**Then reconcile.** Put the described steps next to the observed steps and show the member the
differences. There are always differences. Ask about each one. This conversation is usually where
the real workflow finally shows up.

Write the result as an ordered list of observed steps, each tagged with the tool and the screen.

---

## Phase 4. Graph-engineered research

Do not research this in a straight line. Split it, run the independent parts at once, then attack
the result before you trust it.

### The lanes (run these in parallel)

**Lane A. API surface.** For every tool in the workflow, find out whether a documented API covers
the steps that touch it. Name the specific endpoints, the objects, the rate limits, and whether the
member's plan includes API access, because on plenty of tools it does not.

**Lane B. Auth.** For each tool: OAuth, API key, service account, or app password. Who has to be an
admin to grant it. What scopes the steps actually need, which should be the narrowest that work.
Where the credential will live. If a `skills/connect-*.md` recipe already exists for that tool,
start from it rather than researching from scratch.

**Lane C. Data.** The real field names, object types, statuses and IDs from Phase 2 and Phase 3.
What has to be read, what gets written, what the write looks like exactly. Where a lookup or a match
between two systems has to happen, and what the matching key is.

**Lane D. Rules and permissions.** The approval boundary from Phase 2. Anything with money,
personal information, sending to a customer, or a legal obligation. Any relevant rule about
contacting people, retaining records, or handling personal information in the member's jurisdiction.
Flag it, do not rule on it, and never assume US rules apply.

**Lane E. Failure modes.** What breaks at ten times the volume. What happens on a duplicate, an
empty result, a timeout, a changed page layout, a revoked token. What the workflow should do when it
cannot finish: stop, retry, or escalate to a person.

### The skeptic pass

Now attack the merged findings. Its only job is to find what is not actually known:

- Which endpoint was assumed rather than confirmed in the documentation.
- Which field name came from a description rather than from a screen.
- Which step has no error path.
- Which write happens before a human sees it, and whether it should.
- Where the plan quietly assumes the member has an admin seat or a paid tier.
- What would make this produce a confidently wrong result rather than an obvious failure.

Everything the skeptic finds either gets resolved or gets written into the gaps list. Nothing gets
waved through.

### The merge

One build spec. Ordered steps, each with its mechanism, its inputs, its outputs, its error path and
its approval status. Plus the gaps list. Plus the wiring checklist.

---

## Phase 5. Pick the mechanism for every step

This decision is the whole cost difference between a build that runs for cents and one that burns
money every time it fires. Say which and why for each step.

| Mechanism | Use when | Cost and fragility |
|---|---|---|
| **Plain code** | The step is deterministic. Move data, match records, apply a rule, format an output. | Cheapest and steadiest. Prefer this. |
| **API call** | The tool documents an endpoint that covers the step and the member's plan includes it. | Cheap, stable, needs auth. |
| **Browser automation** | No API, but the task is the same clicks every time on stable pages. | Breaks when the page changes. Needs a real session. |
| **Computer use** | Neither of the above works, and the screen changes shape run to run. | Slowest and dearest. Last resort, never the default. |
| **A model call** | The step needs judgement: reading a message, deciding a category, drafting prose. | Only where judgement is actually required. |
| **A person** | Money, a send to a customer, anything irreversible. | Always, at the gate. |

**The rule to hold:** a model call is for judgement. If the step has a right answer that a rule can
produce, write the rule. Do not pay for inference to do arithmetic.

---

## Phase 6. The human gate

Show the member the build spec before writing anything. On one screen:

1. The graph, drawn as text. Which steps run at once, where the check sits, where they approve.
2. Every step with its chosen mechanism and one line of why.
3. The wiring checklist: every key, every OAuth flow, who has to be admin to grant it.
4. The gaps list: everything the skeptic could not resolve, and what it would take to resolve it.
5. What this will do the first time it runs, in plain language.

Then ask, in these words: **"Does this match the job as you actually do it?"**

Fix what they correct. Ask again. Only build when they say go.

---

## Phase 7. Emit

Write into the business brain if one exists, beside the SOP the workflow came from. Otherwise write
into a folder named after the workflow.

**1. The skill.** A skill file for this workflow, following the same conventions as the rest of the
member's skills. It must:
- Detect its own prerequisites on first run and say what is missing rather than failing halfway.
- Read configuration from the member's existing config files, never hardcode a path or an account.
- Read secrets only from the gitignored secrets location. Never write a key into the skill file, and
  never into anything tracked by git.
- Log every action it takes to the audit log the business interview set up.
- Stop and ask at the approval boundary from Phase 2. Draft first, ask, then act.
- Handle the failure modes from Lane E explicitly, including what it does when it cannot finish.

**2. `WIRING.md`.** Every credential the skill needs, in a table: tool, auth method, who grants it,
which scopes, where it lands, and one literal read action that proves it works. Ordered so the
member can work down the list. Never include a live key in this file.

**3. `GRAPH.md`.** The graph as text, the mechanism per step with the reason, and the gaps list
carried through verbatim from the skeptic pass. This is the document the member reads in three
months when they want to change something.

**4. Update the SOP.** Append to the source `sops/<slug>.md`: what is now automated, what still needs
a person, and the date. Do not rewrite the member's own words above it.

---

## Completeness gates

Check these silently before Phase 6. Any gate that fails goes back to the member as a question.

- **G1.** One workflow, one named outcome, one trigger. Not a department.
- **G2.** Every step has a tool, an owner and an output.
- **G3.** Every step observed on screen, or explicitly marked as described only.
- **G4.** Every field name came off a screen or was read aloud from one. No invented labels.
- **G5.** Every tool has an auth method and a named admin who can grant it.
- **G6.** Every step has a mechanism and a stated reason.
- **G7.** Every step has an error path, including what happens when it cannot finish.
- **G8.** The approval boundary is explicit, and nothing irreversible happens before it.
- **G9.** The skeptic pass ran, and everything it raised is either resolved or in the gaps list.
- **G10.** No secret appears in any emitted file.

---

## Running summary format

Emit this every five questions so the run survives a closed terminal.

```
RUNNING SUMMARY
Workflow: <name> · Phase <n>, question <n> of <n>
Outcome: <the one sentence>
Trigger: <what starts it>
Steps confirmed: <ordered list so far>
Tools: <tool: what it is used for, auth if known>
Screens reviewed: <n>, discrepancies found: <n>
Boundary: read <...> · draft <...> · approve-first <...> · never <...>
Open gaps: <list>
Next question: <the one to ask on resume>
```
