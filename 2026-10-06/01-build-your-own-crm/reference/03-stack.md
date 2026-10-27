# The stack you are building on

This is the stack a production CRM runs on, and the stack your fork inherits. The PRD must only
promise what this stack can deliver. Read it before the interview ends and again at the start of the
build.

## The base

**NextCRM**, an open source CRM at `github.com/pdovhomilja/nextcrm-app`, MIT licence. It already
brings sign-in, accounts, contacts, leads, opportunities, campaigns, projects, tasks, an email client,
documents, invoices, reports and an MCP server. You fork it and build on top. You do not rewrite what
it already does well. Keep the `LICENSE` file.

## The layers

| Layer | What it is | What you use it for |
|---|---|---|
| App | Next.js (App Router), React, TypeScript, pnpm | Every page and every API route. |
| UI | shadcn/ui components, Tailwind | Tables, forms, dialogs. Reuse the existing components. |
| Data | Postgres on Supabase, Prisma as the ORM | Every table. Optionally pgvector for search by meaning. |
| Sign-in | better-auth | Accounts, sessions, roles. |
| Email | Resend | Outgoing email from the app. |
| Background work | Inngest, or a scheduled script run as its own service | Anything that happens on a schedule or after an event. |
| Hosting | Railway | Runs the app and each scheduled job. A push to `main` deploys. |
| Agents | The MCP server, plus plain API routes | How Claude, ChatGPT, Hermes or any agent reads and writes the CRM. |

## How a production CRM grew on it

Use these as proof of the pattern, never as a template to copy line for line.

- An industry pipeline (its own records, stages and a board that advances on its own) was
  added as new tables and pages beside the inherited ones. Tables added by the team are prefixed so
  they never collide with the base.
- Scheduled jobs (scoring, email sequences, syncs with an accounting tool and a phone system)
  run as separate Railway services, each with its own schedule and watch paths.
- Branded PDFs (client-facing documents and reports) come from an HTML template printed to PDF by
  headless Chromium, inside the app.
- The same data is read by agents over MCP, so any agent can ask the CRM a question.

## Rules that kept it alive

Write these into the new repo's `CLAUDE.md` or `AGENTS.md` in phase 4, adapted to the business.

1. **Fork, never blank.** Start from the base and add.
2. **Schema changes only add.** Never `prisma db push` or `prisma migrate` against a database that
   holds real data. A schema sync can silently drop live columns and break a scheduled job for days. Changes are numbered SQL files in `ops/` with a `-REVERSE.md`, applied on purpose.
3. **Type check and tests pass before every commit.** `pnpm tsc --noEmit` and `pnpm test`.
4. **One slice per commit.** A slice you can review in a few minutes and undo in one command.
5. **Poll the deploy until it says success** before saying "deployed". A push is not a deploy.
6. **Anything that contacts a real person ships switched off**, with a config flag the operator turns
   on, after being told exactly who will be contacted and when.
7. **Secrets in one gitignored file.** Never in tracked files, never in chat.
8. **Scheduled jobs write to the database only when a flag says so.** A local test prints what it
   would do.

## Limits to say out loud in the PRD

- The base is a general CRM. Industry workflows (quoting, rostering, compliance) are built as new
  tables, pages and jobs on top. Say which are new.
- Free tiers have limits on database size, row counts and job time. Name the ones that matter.
- Anything that needs a third party (accounting, phone, SMS) needs that account and its API access.
  List each one as a dependency with an owner.
