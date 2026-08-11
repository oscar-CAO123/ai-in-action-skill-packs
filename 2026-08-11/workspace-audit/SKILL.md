---
name: workspace-audit
description: >
  Audits a working environment against reality. Every router, index, README and memory file is a set
  of claims about what exists and what is current; this checks each claim against the disk and
  classifies what it finds as poisoning, bloat, confusion or clash. Read-only: it never fixes, moves,
  renames or deletes while auditing. Delivers a scorecard, the questions your agent would answer
  wrongly today, and a numbered fix list that waits for your approval. Triggers on: "audit my
  workspace", "audit my second brain", "why does my agent keep getting this wrong", "os audit",
  "is my context still true", "clean up my agent setup".
argument-hint: [optional folder to audit, defaults to the working directory]
---

# Workspace audit

Every file your agent reads is a claim. The router claims a folder exists. The index claims it holds
forty notes. The memory claims you use a tool you dropped in March. Agents do not verify claims, they
repeat them, so a workspace decays quietly and the first symptom is a confident wrong answer.

This audit checks the claims against the disk.

**It is read-only.** Nothing is fixed, moved, renamed or deleted while auditing. The deliverable is a
report plus a fix list that waits for a person. That separation is the whole discipline: an audit
that fixes as it goes cannot tell you how bad things were.

Adapted from a working audit run monthly on a real vault. The field notes at the bottom are the
expensive part.

---

## The four failure modes

Classify every finding as exactly one of these. The mode explains *why* a wrong answer would happen,
which is what turns a list of untidy files into something worth fixing.

| Mode | What it is | Fix pattern |
|---|---|---|
| **Poisoning** | A false fact sits in the context and gets repeated with total confidence. | Verify against a live source, or put a person in the loop. |
| **Bloat** | So much is loaded that the part which matters is buried. Answers get slower, dearer and vaguer at once. | Segment the knowledge, demote it to situational, archive it. |
| **Confusion** | The needed fact is missing, or the ones found are irrelevant, so the model fills the gap itself. | Add the missing fact, or remove the distractor. |
| **Clash** | Two sources disagree. March says always refund, June says never. | Pick the canonical source. Archive or rewrite the loser. |

Untagged findings get argued about. Tagged findings get fixed.

## Expertise against situational

- **Expertise** is the rulebook, loaded every single run: the root instructions file, the routers,
  the agent persona, the voice rules, the things that are never allowed.
- **Situational** is pulled at the moment of need: a transcript, last month's numbers, one client's
  history, a workspace for one job.

**Misplacement is itself a finding.** Situational material sitting in an always-loaded file is
bloat. Expertise buried three folders deep is confusion waiting to happen.

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

## Phase 0b. The interview

One question at a time. Never paste the list. Short, because the disk answers most of it.

1. What is this workspace for, in one sentence?
2. Who else reads or writes in here, and do they follow the same conventions?
3. When your agent gets something wrong, what does it usually get wrong? Ask for a real example from
   this week, not a category.
4. Which file is the source of truth when two disagree? If there is no answer, that is a finding
   already.
5. What in here is finished, and what is half-built and still open?
6. What did you reorganise most recently, and roughly when?
7. Is there anything you know is stale but have not got to?
8. What must never leave this machine?
9. Have you audited this before, and is the report still here?

Confirm the answers back in a short block before you start checking.

---

## Phase 1. Ground truth before the checks

- Look for earlier reports in `audits/`, or wherever question 9 pointed. Diff against the most recent
  one so recurring findings get flagged as **recurring**, which is a different and worse problem.
- Skim recent version history if this is a repo. Rot concentrates in whatever moved last.
- Note the size of the always-loaded set. If the root instructions file plus the routers is more than
  a few thousand words, bloat is already the headline and you have not started.

---

## Phase 2. The checks

Run all eight. On a large tree, run them one top-level folder at a time rather than across
everything at once, and merge the results. Nothing writes.

1. **Routing integrity.** Does everything the routers point at exist? Read the root instructions
   file, every index, every agent file and every skill trigger list, and verify each referenced path,
   file, skill and tool resolves. Then run it backwards: sample the disk for files no router can
   reach (orphans), and files sitting under a router that does not describe them (misroutes).
2. **Index truth.** Do the indexes match the disk? Counts, names and one-line descriptions against
   reality. A confident count is the most common poisoning in any workspace.
3. **Freshness.** For every data feed and living document, classify it: fresh, drifting, frozen,
   retired, or on-demand. A frozen feed presented as live is poisoning, not untidiness.
4. **Memory truth.** The memory index against the memory files. Memories pointing at files, flags or
   systems that no longer exist. Memories that contradict a current document. Memory usually lives
   outside the repo, so sweep it separately or it drifts away from everything else.
5. **Bloat and duplication.** Near-duplicate documents, superseded versions living beside their
   replacement, one-off workspaces that should be archived, oversized always-loaded files.
6. **Contradictions.** Any two documents asserting different values for the same fact: a price, a
   name, a status, a rule, a threshold. Name both files and say which should win.
7. **Hygiene.** Junk files, empty stubs, "Untitled" files, broken symlinks. Then the serious one:
   any secret or token outside the sanctioned secrets location. Check whether it is ignored by
   version control, and check whether it was ever committed, because those are different questions.
8. **Context placement.** Expertise material in situational folders and the reverse, per the
   definitions above.

---

## Phase 3. The report

One markdown file: `audits/YYYY-MM-DD-<scope>.md`.

- **Scorecard.** One line per check: red, yellow or green. No prose.
- **What would wrong-answer you today.** Three to five concrete questions the owner could ask right
  now that would get a confident wrong answer, each traced to a specific finding. **This is the
  section that makes the audit real.** Write it first if it helps; everything else supports it.
- **Findings.** Grouped by check. Each one tagged with its failure mode and the exact paths. No
  finding without a path.
- **Fix list.** Numbered, and grouped in this order: finish what is already in flight, then routing
  and index truth, then data catch-up, then the durability change that stops it recurring. Each item
  small enough to approve on its own.

End the file with **awaiting approval**, and stop. Do nothing until they pick numbers.

---

## Phase 4. After approval

- Execute only the approved numbers. Nothing outside the list, however tempting.
- Re-run whatever generates your indexes after any file moves, then repair internal links across the
  tree so nothing breaks.
- Log what was actually done at the bottom of the same report file, with the date.

## The backtrack habit, between audits

When the agent fails to find something that exists, or answers from stale data, do not just correct
it. Make it retrace where it searched, say where it should have looked, then fix the routing it just
proved broken.

One backtrack fixes more rot than a month of guessing.

---

## Field notes

Hard-won on real runs. These cost hours to learn.

- **Scan per folder, never across everything at once.** A single tree-wide search can stall silently
  on a full disk or one giant stray file. Per-folder scans finish in seconds and tell you which
  folder is the problem when one does not.
- **Before any large commit, check free disk and repository size.** A commit that times out can
  leave multi-gigabyte temporary objects behind, fill the disk, and wedge everything downstream.
- **An ignore-rule check matches rules, not files.** It will happily print a path for a file that
  does not exist, so it is never proof that a move landed. Verify landings by checking the file is
  actually there.
- **Path sweeps are two jobs, not one.** Files that moved together keep their relative references
  and must not be rewritten. Files outside the moved set do need rewriting. Split the sweep by
  region, then hand-fix the leftovers.
- **Never hand-edit a generated block.** Re-run the generator. It regenerates every block including
  the cross-links you would otherwise chase one at a time.
- **Self-locating scripts break when folders move.** Anything that walks up a fixed number of parent
  directories to find its root needs re-checking after any reorganisation.
- **Link audits need a filter for things that only look like links.** Placeholders, shell syntax and
  internal reference ids are not broken links. Without the filter the broken-link count is
  meaningless and you will chase it for an hour.
- **Config flags lie. The running system is the truth.** A scheduled job marked enabled in a config
  file meant nothing; the scheduler had booted it out weeks earlier. Check live wiring against the
  live system, in both directions.
- **Memory is its own audit surface.** It usually lives outside the repository and gets missed
  entirely.

---

## Gates

- **G1.** Nothing was written, moved, renamed or deleted during the audit.
- **G2.** Every finding carries a failure mode and at least one exact path.
- **G3.** The wrong-answer section has at least three real questions, each traced to a finding.
- **G4.** Every fix-list item is small enough to approve on its own.
- **G5.** No secret was opened, and any secret found is reported by location only, never by content.
- **G6.** Recurring findings are marked as recurring, with the date they were first raised.
- **G7.** The report ends with "awaiting approval" and nothing was executed.
