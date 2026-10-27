# Phase 1. Sweep

Do this before a single question. The point is to arrive already knowing the business, so the
interview spends its time on what the files cannot tell you.

Two sweeps. The first finds **context**: what the agent already knows. The second finds **systems**:
where the business already keeps its customers, deals, jobs and documents today, because a CRM that
ignores the current systems becomes a second place to type everything.

---

## Sweep 1. Context

From the directory you were opened in, list everything about four levels deep, including dotfiles,
skipping `node_modules`, virtualenvs, build output and files over a few megabytes. Read names and
structure first. A file tree shows what someone works on rather than what they say they work on.

Then read whatever exists, in this order.

| Looking for | What it tells you |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, root `README.md` | Operating rules they already wrote down. Inherit them. |
| A business brain: `soul.md`, `user.md`, `identity/`, `context/`, `brand/`, `memory.md` | Who they are, what they sell, who runs it, the voice they write in. |
| Anything from `member-business-interview` | The positioning layer. Read it in full. It answers most of interview phases 1 to 3. |
| `sops/`, `playbooks/`, `runbooks/`, `docs/` | The jobs they run, in their own words. Each one is a candidate CRM workflow. |
| `skills/`, `.claude/`, `.codex/`, `agents/` | What their agent can already do, and the conventions to match. |
| `config/`, `.env.example`, `docker-compose.yml` | Which tools are wired and where secrets are expected. |
| Spreadsheets, CSV exports, `data/` | The real shape of their records. Read the header rows. These become tables. |

**Never open a secret.** `.env`, `*token*`, `*credential*`, `*oauth*`, `*.pem`, `*.key`, anything under
a `secrets/` path. Note that it exists, note variable names from an `.env.example`, move on.

## Sweep 2. Systems

Find every place the business keeps records today. Look for:

- Spreadsheet exports (customers, quotes, jobs, invoices, rosters, stock).
- Connected tools named in config or notes: an accounting tool, a booking tool, a phone system, a
  helpdesk, an inbox, a form builder, a document store, a payment processor.
- Existing CRM or project tools, and any export from them.
- Email and calendar: which accounts exist, which labels or folders carry work.
- Anything that sends messages to customers on a schedule.

For each system, record: its name, what records live in it, roughly how many, who touches it, and
whether it can export or has an API. This list drives the integration and import sections of the PRD.

---

## The report

Write `sweep-report.md` with these headings and nothing else:

1. **The business in your words.** Three to six sentences, only what the files support.
2. **Where the records live today.** The systems table from Sweep 2.
3. **Jobs I found.** Each repeatable job named in a SOP, skill or note, one line each.
4. **What I could not find.** The gaps the interview must fill.
5. **Files I did not open.** Secrets noted by path only.

Print the report. Then ask:

> That is what I could see. What did I get wrong?

Correct the report from the answer, save `.crm-build.json` with `{"phase": 1, "done": true}`, and
move to phase 2.
