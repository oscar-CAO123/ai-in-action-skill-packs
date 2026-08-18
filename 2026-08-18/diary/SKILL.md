---
name: diary
description: Capture the context that never lands in a meeting, an email or a commit, and file it so agents can query it. Use when the user types "/diary", "diary entry", "log my day", "brain dump", or wants what they know written somewhere their agents will read. Do NOT use for meeting notes an existing transcript already covers, or for task tracking that belongs in an issue.
---

# diary

Most of what a person knows about their own work is not written anywhere. It is not in the meeting
transcript, the inbox or the commit log. That gap is why agents get things confidently wrong.

This skill closes it. A short prompted entry, dictated or typed, filed dated, then read back into a
queryable index that other skills use as their highest-priority context.

Grounded in Allie K. Miller's daily AI diary, on Greg Isenberg's podcast, 18 August 2026. Her rule:
dictate, because it is four times faster than typing, and bank it into a wiki the whole workforce
reads. `do-smart-things` reads this index first.

## Step 1: find or make the diary

Detect at runtime. Look for `diary/`, `.diary/` or a directory a router names as the wiki. If none
exists, create `diary/` at the git top level, or at the working directory when there is no repo, and
say where you put it.

## Step 2: prompt, then get out of the way

Ask these three, together, in one short block:

1. What changed today that is not in a meeting, an email or a commit?
2. What did you decide, or correct, or change your mind about?
3. What is still open, and what is blocked on someone else?

Tell the user to dictate rather than type. Take whatever comes back, including fragments, half
sentences and dictation artifacts. Never send the entry back for tidying and never ask a follow-up
before filing. A diary that interrogates its author stops getting used.

If the user opens with the entry already written, skip the prompts and file it.

## Step 3: file the entry

Write `diary/YYYY-MM-DD.md`. Append to it when the file already exists, under a time heading, so a
day can hold several entries.

Keep the user's own words. Fix only what makes it unreadable later: a name spelled out, an acronym
expanded on first use, an obvious dictation mangle corrected. Do not summarise, compress, tidy, or
turn speech into prose. The value is in the specifics that a summary would strip out.

## Step 4: extract into the index

Rewrite `diary/INDEX.md` after every entry. It is the file agents read, so it stays small and
factual, newest first, every line pointing at the dated entry it came from.

Four sections:

- **Decisions.** What was settled, with the date and the reason if one was given. A decision that
  reverses an earlier one supersedes it in place, with the old line kept and marked superseded.
- **Corrections.** Where the user corrected something, an agent, a document, an assumption. These
  are the highest-value lines in the file: each one is a wrong belief someone is about to repeat.
- **People and relationships.** Who is involved in what, what state each thread is actually in.
  The point is the detail the systems of record miss.
- **Open loops.** What is unfinished, what it is waiting on, and who owns the next move. Close a
  loop in place when a later entry resolves it, with the closing date.

Also carry a **Friction** section when entries name it: where the same correction keeps recurring,
what access or context an agent was missing. That list is what to fix next.

Every extracted line cites its source entry. Never write a line into the index that no entry supports.

## Step 5: hand back

Report the entry path, the index path, and what changed in the index: new decisions, new corrections,
loops opened, loops closed. Two or three lines, no more.

## The ceiling

Local files only. This skill never sends, posts, syncs, publishes or uploads an entry anywhere. A
diary that leaves the machine stops being honest.

Never write secrets, keys, tokens or credentials into an entry or the index. If the user dictates
one, file the entry with the value replaced by a note of what it was and where it lives.

## House rules

No em dashes. Never "it is not X, it is Y" in any form. The user's voice survives into the entry
unedited, and the index stays plain and short.
