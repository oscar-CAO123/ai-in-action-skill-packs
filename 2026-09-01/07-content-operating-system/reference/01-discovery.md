# Phase 0 and 1. Discovery

Do this before a single question. The point is to arrive already knowing who they are, so the
interview spends its budget on what the files cannot tell you.

There are two sweeps here and they look for different things. The first finds **context**: what the
agent already knows about this business. The second finds **evidence**: where the customer's actual
words are kept. Most operators have far more of the second than they realise, and almost none of it
is anywhere near their content.

---

## Sweep 1. Context

From the directory you were opened in, list everything about four levels deep, including dotfiles,
skipping `node_modules`, virtualenvs, build output, and anything over a few megabytes. Read names and
structure first. A file tree shows what someone works on rather than what they say they work on.

Then read whatever exists, in this order.

| Looking for | What it tells you |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, root `README.md` | The operating rules they already wrote down. Inherit them. Never restate them back at them. |
| A business brain: `soul.md`, `user.md`, `identity/`, `context/`, `brand/`, `memory.md` | Who they are, what they sell, who runs the business, the voice they write in. |
| Anything from `member-business-interview` | The whole positioning layer. Read it in full. It is the single highest-value file in the sweep. |
| `sops/`, `playbooks/`, `runbooks/`, `docs/` | The jobs they already run, in their own words. |
| `skills/`, `.claude/`, `.codex/`, `agents/`, `prompts/` | What their agent can already do, and the file conventions to match. |
| `config/`, `.env.example`, `docker-compose.yml`, `Makefile` | Which tools are wired, and where secrets are expected to live. |
| `.gitignore`, and the last thirty commits if this is a repo | What they treat as private, and what they have actually been doing lately. |
| The three largest folders, whatever they are | The real centre of gravity, which is often not where they say it is. |

**Never open a secret.** `.env`, `*token*`, `*credential*`, `*oauth*`, `*.pem`, `*.key`, anything
under a `secrets/` path. Note that it exists, note the variable names if there is an `.env.example`
beside it, move on.

---

## Sweep 2. Evidence

This is the sweep that makes the difference, and it is the one nobody runs. You are looking for
places where a customer said something in their own words.

Search the workspace, and then ask permission before going wider. Say exactly which locations you
want to look in and why, and sweep only what they name. Do not walk their home directory uninvited.

**File patterns worth finding:**

| Pattern | Usually is |
|---|---|
| `*transcript*`, `*.vtt`, `*.srt`, `*recording*`, `*meeting*` | Call transcripts. The richest source there is. |
| `*.md` or `*.txt` under `notes/`, `calls/`, `discovery/` | Hand-written call notes. Sparser, still gold. |
| `*export*.csv`, `*tickets*`, `*conversations*` | A helpdesk export somebody pulled once and forgot. |
| `*survey*`, `*nps*`, `*feedback*` | Structured voice of customer, usually with scores attached. |
| `*testimonial*`, `*review*`, `*case-study*` | Copy that already passed a customer's approval. |
| `*.eml`, `*mbox*`, `inbox/` | Mail exports. Check the size before reading anything. |
| Anything under a Drive, Dropbox or iCloud mount | Where the transcripts usually actually are. |

**Tools worth detecting**, by config file, installed CLI, MCP server entry, or an environment
variable name found in an `.env.example`:

- Call recording: Fathom, Granola, Fireflies, Otter, Gong, Grain, tl;dv, Zoom cloud recording, Read.
- Helpdesk: Intercom, Zendesk, Front, Help Scout, Freshdesk, Crisp, a shared Gmail label.
- CRM: HubSpot, Pipedrive, Attio, Close, Salesforce, Airtable, Notion, a Supabase or Postgres table.
- Community: a Slack or Discord workspace, a Circle or Skool community, a private forum.
- Analytics and channels: Meta, TikTok, LinkedIn, YouTube, Google Analytics, Search Console, Ahrefs.

**MCP and connector config to check**, since a wired connector means the agent can already read a
source without any new credentials: `.mcp.json`, `.cursor/mcp.json`, `~/.codex/config.toml`, the
Claude Code settings file, and any `mcpServers` block in a project config.

---

## Phase 1. Report and correct

Report back in **five lines and stop**. Not a document, not a table, five lines.

1. What kind of business this looks like, and what you think it sells.
2. What the agent already knows how to do, and which of its files you will inherit.
3. Where customer evidence is sitting right now, and roughly how much of it there is.
4. What looks abandoned or stale, so they can tell you to ignore it.
5. What you looked for and could not find.

Then ask them to correct it.

That correction is worth more than the next three questions, because it tells you which of their own
files they still trust. A file they wrote eight months ago and have not opened since is not context,
it is archaeology, and building a brain on it produces content that argues for a position they have
already moved off.

**Write the sweep result to `.cos-interview.json` under `discovery` before you ask the first
interview question.** Include the paths you found, what you inferred, and what they corrected.

---

## The one thing not to do here

Do not present a findings report. No multi-section wall, no stacked tables, no numbered list of
twenty observations. Five lines, then a question. The thinking happened in the sweep. What reaches
them is the conclusion.
