---
name: Codex Computer Use
slug: codex-computer-use
description: >
  An INSTRUCTIONAL skill: how to let a coding agent drive your actual screen without wrecking
  anything. Covers the two mechanisms (look at a window, or take the mouse), the escalation order
  between them, the permission model that stands behind both, and the jobs this is genuinely the
  right tool for. Written for OpenAI Codex on macOS and Windows. The principles carry to any agent
  with screen control.
status: published
evidence: documented_against_vendor_docs_2026_08_16
phase_0: REQUIRED. Establish what you are pointing it at before you point it at anything.
triggers:
  - "let codex use my computer"
  - "agent that can click things"
  - "automate an app with no API"
  - "codex computer use"
  - "appshots"
requires:
  - Codex, in the ChatGPT desktop app or the CLI
  - macOS, or Windows on version 26.527 or later
  - Nothing else. No plugin, no API, no integration.
not_industry_specific: true
---

# Letting an agent drive your screen

Every operator hits the same wall about a week into their first real build. The agent can read your
files, call your APIs and write your code, and then it runs into the one system your business
actually depends on: the scheduling tool with no API, the supplier portal from 2011, the accounting
package where the export button is three menus deep. There is no plugin for it and there never will
be, because the vendor has forty customers and no reason to build one.

Screen control is the answer to that wall. It is also the single easiest way to have an agent do
something to your business that you cannot undo, so the whole of this file is about the order you do
things in.

The one line to remember: **look before you touch, and stay in the room for anything you cannot
reverse.**

---

## Rules that bind this skill

- **Escalate, never start at the top.** Show it the window first. Take the mouse only when looking
  was not enough.
- **Narrow the job.** Screen control changes state outside your project folder. One task, one app,
  one outcome, then stop.
- **Never paste a credential into a prompt.** Not an API key, not a database password, not a
  production login. If the agent needs to be signed in, you sign it in.
- **Clean git before you delegate anything that touches code.** You cannot review a diff you cannot
  isolate.
- **Be present for anything irreversible.** Sending, paying, deleting, submitting, publishing. The
  agent asking permission is worth nothing if nobody is at the desk to answer.
- **Region check.** Computer use is not available in the EEA, the United Kingdom or Switzerland.
  It is available in Australia. Appshots are available everywhere, including those regions.

---

## Phase 0. Know what you are pointing it at

Before the first run, write down three things. It takes four minutes and it is the difference between
a useful tool and an expensive mistake.

| Question | Why it decides the run |
|---|---|
| What state does this app hold, and who else sees it? | A shared inbox, a live CRM and a booking system are all somebody else's afternoon. A local spreadsheet is not. |
| What in this app cannot be undone? | Send, pay, submit, delete, publish. List them by name so you know which screens to sit through. |
| Is there a sandbox, a test account or a copy? | If there is, use it for the first three runs. Most operators never check and most vendors have one. |

Then decide the smallest useful version of the job. Not "keep my CRM tidy". Something like "open the
five records flagged yesterday, copy the phone number from the note field into the phone field, and
stop".

---

## The two mechanisms, and the order between them

They are different tools and most people reach for the wrong one.

### Appshots. It looks.

A hotkey (double-tap Command on macOS) that captures the front window and hands it to the agent: a
screenshot plus the structured text behind it. It does not click anything, it does not type, it
cannot change a single thing on your machine.

Use it when the agent needs to **see** something to answer well. The error dialog, the report that
will not export, the layout that looks wrong, the invoice you are reading.

**The one hazard, and almost nobody is told this.** An appshot can include text past the edge of what
you can currently see: the rest of a long email thread, the next two hundred rows of a spreadsheet,
the bottom of a customer record. Before you capture a window, know what is in the whole of that
window, not just the visible part. Never appshot a window holding somebody else's personal
information, a credential, or a client's file you have no right to share.

### Computer use. It drives.

The agent sees the screen, moves the cursor, clicks and types, in any app you have. It can operate
software with no API, no plugin and no integration.

On macOS it works alongside you and you can keep using other apps. **On Windows it runs in the
foreground and takes over the active desktop session for the duration of the task**, so plan for the
machine to be busy, and do not start a twenty minute job on the laptop you are about to present
from.

### The escalation order

1. **Can the agent answer from your files?** Then no screen tool is needed. This covers more than
   people expect.
2. **Can it answer if it sees the window?** Appshot. Stop here whenever you can.
3. **Does it genuinely need to click?** Computer use, on the narrowest possible task, with you
   watching.

The way to feel this: showing somebody your screen is a normal thing to do at work. Handing them
your keyboard and walking out is not. Same instinct, same order.

---

## The permission model, in plain terms

Two separate layers, and confusing them is why people either get blocked constantly or hand over far
too much.

**Sandbox mode** is what the agent is technically able to reach. Which folders it can read, which it
can write, whether it has network at all.

**Approval policy** is when it has to stop and ask you.

The default preset lets it edit inside your working folder and run commands there, and makes it ask
before it edits anything outside that folder or touches the network. **Network is off by default.**
You turn it on deliberately, and you can restrict it to an allowlist of hosts rather than opening it
entirely.

`/permissions` switches between modes mid-session. The one worth knowing is **read-only**: the agent
can look at everything and change nothing. That is the correct mode for the first half of most jobs,
and for every conversation where you are still working out what you want.

The rule that holds across every setup: **tight by default, loosened one notch at a time for a
specific job you have already watched work.** Nobody has ever regretted this order. Plenty of people
have regretted the other one.

---

## Making it good rather than merely working

### Write the rules down once, in `AGENTS.md`

Put a plain markdown file called `AGENTS.md` in the folder you work in. Think of it as a README
written for the agent instead of for a new hire: how this project is laid out, the commands that
build and test it, the conventions you hold to, the things it must never do, and how it is supposed
to check its own work.

Every rule you put in that file is a rule you stop typing into prompts. This is the single highest
return thing in this document and it takes twenty minutes. It is also, per OpenAI's own numbers from
13 August, the measurable difference between the firms pulling ahead and everyone else: the top ten
percent of enterprises use skills six times as often as typical ones.

### Ask in four parts

Every request that matters carries the same four:

- **Goal.** What are you trying to change or build?
- **Context.** Which files, folders, apps, examples or errors matter?
- **Constraints.** What conventions, standards or boundaries apply?
- **Done when.** What has to be true before this is finished?

The fourth is the one everybody skips and the one that decides whether you get an answer or a
conversation. "Done when the five flagged records have a phone number in the phone field and nothing
else has changed" ends a task. "Tidy up the CRM" does not.

### Plan before it acts

For anything complex or vaguely specified, start in plan mode (`/plan`, or Shift and Tab). You get
the intended sequence before anything happens, and you can approve it, rewrite a step, or throw it
out. If your idea is still rough, ask the agent to interview you instead of guessing.

Plan mode matters more with screen control than anywhere else, because a plan is the only chance you
get to catch "and then it clicks Send" before it clicks Send.

### Keep sessions clean

One conversation per unit of work. `/fork` to branch off without losing where you were. `/compact`
when a session has run long. Hand bounded side jobs to subagents rather than piling them into the
main thread.

### Review it like a colleague's work

Clean `git status` before you delegate, then read the diff. Screen work needs the equivalent: know
what the app looked like before, and check it afterwards. An agent reporting success is a claim, not
a result. Verify the thing it says it did.

---

## What this is actually good for

Worth doing:

- **The software with no API.** The industry portal, the old accounting package, the supplier
  system. This is the case that justifies the whole feature.
- **Reproducing a fault.** Something breaks only when clicked in a certain order. Have the agent
  reproduce it and write down what it did.
- **Settings work across many screens.** Long, dull configuration passes where every step is
  obvious and there are two hundred of them.
- **Reading something complicated.** Appshot the window and ask. No control needed.
- **Checking a flow end to end.** Walk a booking, a checkout or a form the way a customer would, and
  report where it broke.

Not worth doing:

- **Anything with a decent API.** The API is faster, cheaper and more reliable every single time.
- **High volume repetition.** If it is running the same click path five hundred times, that job
  wants a script, and the agent should be writing the script rather than doing the clicking.
- **Anything irreversible while you are away from the desk.** Sending, paying, submitting,
  publishing, deleting.
- **Anything holding somebody else's personal information** unless you have a clear basis to be
  looking at it and have thought about where the capture goes.

---

## Gates

- **G1.** The escalation order was followed. Nobody reached for control before looking.
- **G2.** The job is one task, one app, one stated finish condition.
- **G3.** No credential appears in any prompt. Sign-ins are done by a person.
- **G4.** Network stayed off, or was opened to a named allowlist for a stated reason.
- **G5.** A person was present for every irreversible action.
- **G6.** The result was verified against the app, not accepted from the agent's report.
- **G7.** Every durable rule that came up during the run was written into `AGENTS.md` afterwards,
  rather than re-typed next time.

---

## Sources

Documented against OpenAI's own materials on 16 August 2026: the Codex best practices guide, the
agent approvals and security documentation, the appshots documentation, and the ChatGPT and Codex
changelog. Computer use shipped on macOS on 16 April 2026 and on Windows in version 26.527 on
29 May 2026. Appshots shipped on macOS on 21 May 2026. Regional restrictions were current at the
time of writing and vendors change them, so check before you rely on one.
