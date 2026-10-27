# Phase 5. Refine

The scope will change. A new customer type shows up, a workflow turns out wrong, a tool gets replaced.
The PRD is a living document and it changes first. The build follows.

## The change loop

For any change the operator asks for, in this order:

1. **Restate it** in one sentence and ask if that is right.
2. **Find the impact.** List the PRD sections, requirement ids, tables, screens, jobs and templates it
   touches. List the slices already built that it affects.
3. **Ask what the interview did not cover.** Run the relevant questions from `reference/02-interview.md`
   for just this change, one at a time.
4. **Classify it.**
   - *Small:* a new field, a label, a filter, a template tweak.
   - *Medium:* a new screen, a new automation, a new integration.
   - *Large:* a new record type, a change to the pipeline, a change to permissions.
5. **Revise the PRD.** Edit the sections, give new requirements new ids, never reuse an id, and add a
   change log line: date, what, why, who approved. Bump the version (`v1.1`, `v2`).
6. **Get the yes.** Show the operator the PRD diff in plain English. Large changes also get the blind
   check from `reference/04-prd.md`. The operator types `APPROVE CHANGE` before any code.
7. **Add slices** to PRD section 15 and build them with the loop in `reference/05-build.md`.
8. **Record** it in `BUILD-LOG.md` with the new PRD version.

## Rules

- **The PRD and the code agree.** If the code does something the PRD does not say, either the PRD gets
  the line or the code gets reverted. Check at the end of every change.
- **Existing data is sacred.** A change that needs a drop, a rename or a type change stops and asks.
  The usual answer is to add a new column or table, migrate the data on purpose, and retire the old
  one later by hand.
- **Say what gets rebuilt.** If a change invalidates built slices, list them and get a yes first.
- **Reversible by default.** Every change has a way back written down before it ships.
- **Re-run acceptance.** After a medium or large change, re-run the acceptance scripts the change
  could affect.

## A standing review

Every month, with the operator:

1. Re-read the three month-one outcomes and the number the operator set. Did it move?
2. Which screens are unused? Which workflows are done by hand again? Ask why.
3. What do people still keep in a spreadsheet or an inbox that should be in the CRM?
4. Update the PRD and the build plan. Archive what was dropped, with the reason.

## When the agent changes

Any agent can carry on the build. A new session reads, in this order: `CLAUDE.md`, `.crm-build.json`,
`PRD.md` (latest version and change log), `BUILD-LOG.md` (last ten entries), `docs/BASE-NOTES.md`.
That is the whole context. If something a new agent needs is missing from those, add it there and not
in a chat.
