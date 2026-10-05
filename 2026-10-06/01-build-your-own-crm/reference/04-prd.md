# Phase 3. The PRD

The PRD is the contract between the interview and the code. Write it so a developer who has never met
the operator could build the system from it, and so the operator can read it in plain English and say
"yes, that is my business" or "no, that part is wrong".

It lives in `PRD.md` at the repo root, is versioned in git, and every build slice cites the section it
implements. A slice with no section is scope creep and gets challenged.

## Rules for writing it

- **Plain English first, then the precise form.** Every requirement has a sentence the operator can
  read, followed by the detail the build needs.
- **The operator's words.** Use their names for things.
- **Testable.** Each requirement has an acceptance check that a person or a test can run.
- **Numbered.** Every requirement gets an id (`R-014`) so slices, tests and changes can point at it.
- **Honest about the stack.** Check each requirement against `reference/03-stack.md`. Mark what the
  base already does, what is new, and what needs a third party.
- **Nothing invented.** Anything the interview did not answer is listed under Open questions, not
  filled in.
- **No em dashes, no banned words.**

## Sections, in this order

### 1. Summary
Three to six sentences: the business, who uses the system, what it replaces, the outcome in three
months with the number the operator gave.

### 2. Goals and non-goals
Goals as measurable outcomes. Non-goals as things deliberately left out, with the reason.

### 3. Users and permissions
A table: role, who holds it, what they can see, what they can change, what they can never see. Include
any outside users. State how a new person is added and removed.

### 4. The records
One subsection per record type, in the operator's word:
- purpose in one sentence,
- every field: name, type, required or optional, example value, where it comes from,
- the stages or statuses and the exact event that moves it between them,
- relationships to other records,
- volumes now and in a year,
- what is shown on the list page, the detail page and the board.

### 5. Data model
Every new table and every added column, with types, keys and indexes. Mark what is new against the base
and name tables with a prefix so they never collide with inherited ones. Include an entity diagram in
text. Every change is additive. State how existing base tables are touched, if at all.

### 6. Workflows
One subsection per job from the interview. For each: trigger, steps in order, which are automatic and
which need a person, the decision points, the exceptions, the failure handling, the alert and who gets
it, and the metric. Say what the human sees on screen at the moment they step in.

### 7. Screens
Every page: its purpose, who sees it, what it shows, the filters, the actions, and what happens on
empty, loading and error states. Include navigation.

### 8. Automations and schedules
Every scheduled job and event trigger: what it does, how often, what it reads, what it writes, its
safety switch, and what a dry run prints.

### 9. Communications
Every message template: channel, trigger, audience, the text, the variables, whether a human approves
it, and the switch that turns it on. All start off.

### 10. Documents
Every generated document: template name, data it needs, the brand rules, and how it is stored.

### 11. Integrations
Every external tool: direction (read, write, both), what moves, how often, auth method, who owns the
account, the first sync, the failure mode, and what happens when the tool is down.

### 12. Agents
What agents may read, what they may write, what needs approval, where approvals appear, the audit
trail, and the context file every agent loads first.

### 13. Security and privacy
Roles, row-level rules, sensitive fields and where they are masked, secrets handling, backups, the
audit log, retention, and what must never be exported or logged.

### 14. Non-functional requirements
Expected load, response targets, uptime expectation, device support, accessibility, backup and restore
time.

### 15. Build plan
The slices, in order, each small enough to review in minutes:

| Slice | What it adds | Requirement ids | Needs from the operator | Done when |
|---|---|---|---|---|

Order by: the foundation (fork, database, sign-in, deploy), then the records that everything else
points at, then the month-one workflows, then integrations, then communications, then agents, then the
rest. The three month-one outcomes decide the order.

### 16. Acceptance
For each month-one outcome, a short script a person can follow to see that it works.

### 17. Risks and open questions
Each risk with its likelihood, its cost and what reduces it. Each open question with an owner and the
slice it blocks.

### 18. Change log
Date, what changed, why, who approved it. Starts with "v1, approved".

---

## Review and approval

1. Print a one page plain English summary and the build plan table. Ask what is wrong.
2. Walk the operator through sections 3, 4, 6 and 15 in full. These are where mistakes cost most.
3. Run the **blind check**: start a fresh sub-agent or a fresh session with only `PRD.md` and the stack
   file, and ask it to list every requirement it could not build from the text alone. Fix those.
4. Resolve open questions that block month one. Others stay open with an owner.
5. When the operator types `APPROVE PRD`, tag the commit `prd-v1`, write `{"phase": 3, "done": true,
   "prd": "v1"}` to `.crm-build.json`, and move to phase 4 by reading `reference/05-build.md`.

No code is written before `APPROVE PRD`.
