# Phase 4. Build

You build from the approved PRD, one slice at a time. Read `reference/03-stack.md` first if you have
not read it this session.

## Step 0. Preconditions

Check, and stop to ask if any fails:

- `PRD.md` exists and `.crm-build.json` says `"phase": 3, "done": true`.
- `gh auth status`, `node --version` (20 or newer), `pnpm --version` all pass.
- The operator has a Supabase project for development. Create a separate one for production later.

## Step 1. Fork and clone

```
gh repo fork pdovhomilja/nextcrm-app --clone --fork-name <their-crm-name>
```

Then, in the clone:

1. Make the repo **private**: `gh repo edit --visibility private --accept-visibility-change-consequences`.
2. Keep `LICENSE` and its copyright line.
3. Create a branch `build/foundation`.
4. Put `.env`, `.env.*` and any key files in `.gitignore` and run `git check-ignore .env` to confirm.
5. Copy `.env.example` to `.env` and fill it from the operator, one variable at a time. Never print a
   secret back. Never write one into a tracked file.
6. Install: `pnpm install`.
7. Read the base. Open `README`, `package.json`, `prisma/schema.prisma` and the folder layout of
   `app/`, `lib/` and `components/`. Write what you learned into `docs/BASE-NOTES.md`. This is the map
   every later slice uses.

## Step 2. Write the rules file

Create `CLAUDE.md` and a copy named `AGENTS.md` at the repo root from the rules in
`reference/03-stack.md`, adapted to this business, plus the operator's own rules from interview
phase J. Every agent that opens the repo reads these first. Commit.

## Step 3. Database, development first

1. Point `DATABASE_URL` and `DIRECT_URL` at the **development** Supabase project.
2. Apply the base schema to the development database only: `pnpm prisma db push` is acceptable here
   because the database is empty and disposable. This is the one place it is allowed. Write in
   `BUILD-LOG.md` that it was development only.
3. Generate the client: `pnpm prisma generate`.
4. Run the type check: `pnpm tsc --noEmit`. It must pass before you go on.

If the base needs a placeholder `DATABASE_URL` only to generate the client, use a placeholder.

## Step 4. First run, local and contained

1. `pnpm dev` against the development database only.
2. Sign up the first user, make them the admin, and confirm the base screens load.
3. Stop the server. Record the result in `BUILD-LOG.md`.

A local run uses the development database and never the production one. Never put production keys in
a local `.env`.

## Step 5. Deploy the foundation

1. Create the Railway project, connect the repo, set the production environment variables in Railway,
   not in the repo.
2. Create the production Supabase project, then apply the schema to it as numbered SQL files in `ops/`
   (not `prisma db push`). Generate the SQL from the Prisma schema with `prisma migrate diff`, review
   it, and keep a `-REVERSE.md` for each file.
3. Push `build/foundation`, open a pull request, merge to `main` on the operator's yes.
4. Poll the deploy until it says SUCCESS. Open the live URL and sign in. Only then say "deployed".

## Step 6. The slice loop

Take the first unfinished slice in PRD section 15, then repeat for each:

1. **Read** the slice's requirement ids in the PRD. Quote them in the log entry.
2. **Branch** off the latest `main`: `build/<slice-name>`.
3. **Plan** the change in a few lines: files to add, files to touch, tables to add. Show it to the
   operator if it touches data or permissions.
4. **Schema first, if any.** Write `ops/NNN-<name>.sql` (additive only) and `ops/NNN-<name>-REVERSE.md`.
   Apply to development. Confirm the app still runs before applying anywhere else.
5. **Build** the change, reusing the base's components and patterns. Match the code around it.
6. **Check.** `pnpm tsc --noEmit`, `pnpm lint`, `pnpm test`. Add tests for the acceptance check in the
   PRD. All must pass.
7. **Review.** Start a fresh sub-agent with only the diff, the slice's requirements and `CLAUDE.md`,
   and ask it to find bugs, missing validation, permission gaps and anything outside the slice. Fix
   what it finds.
8. **Show the files.** Print `git diff --stat` and confirm the set is only the intended files.
9. **Operator's go.** Wait for a yes before pushing.
10. **Ship.** Apply the SQL to production if there is any, push, merge, and poll the deploy to SUCCESS.
11. **Log.** Append to `BUILD-LOG.md`: date, slice, requirement ids, files, the SQL applied, how to
    undo it, and the acceptance check result.
12. **Tick** the slice in PRD section 15.

Never combine slices. Never start the next slice with a failing check.

## Rules inside the loop

- **Anything that contacts a real person ships switched off.** Add a config row or environment flag
  that defaults to off. When the operator wants it on, say exactly who will be contacted and at what
  time, and wait for a separate yes.
- **Scheduled jobs write only when a flag says so.** The default run prints what it would do.
- **Permissions are built with the screen, never after it.** Every page and every API route checks the
  user's role as part of the same slice.
- **Sensitive fields are masked in lists, logs and exports** as the PRD's section 13 says.
- **Imports are dry runs first.** Print counts, a sample and the rows that would be skipped. Write
  only after the operator has seen the numbers.
- **When the PRD is wrong or silent, stop.** Do not guess. Ask the operator, then change the PRD first
  (phase 5) and build after.

## Wiring agents

Do this once the records exist, as its own slice:

1. Enable the MCP server the base ships with, behind sign-in.
2. Give agents the least access the PRD allows: read by default, write only on the tables PRD section
   12 names, and every write logged with the agent's name.
3. Write `docs/AGENT-CONTEXT.md`: the business in a page, the record types in the operator's words,
   the stages, the rules and the never-do list. Every agent loads it first.
4. Test with the operator's own agent: ask it three questions only the CRM can answer.

## Documents

When the PRD asks for branded documents, build each as an HTML template and print it to PDF with
headless Chromium on the server (`puppeteer-core` with the system Chromium in the Docker image). One
template per document, the brand rules in one stylesheet, the data in one function. Open the PDF and
check it against the operator's last real example before shipping.

## Finishing

When every month-one slice is done, run the acceptance scripts from PRD section 16 with the
operator watching. Write the result into `BUILD-LOG.md`, tag `v1`, and move to phase 5.
