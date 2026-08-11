---
name: Sending Infrastructure
slug: sending-infrastructure
description: >
  An INSTRUCTIONAL skill: it walks the operator's agent through standing up email sending
  infrastructure that does not put the main business domain at risk. Separates the four kinds of
  email a business sends, buys and authenticates dedicated domains for the cold one, warms the
  inboxes, sets the per-inbox limits, and puts a monitor on the numbers that predict a
  deliverability collapse before it happens. This is the boring layer every outbound build skips
  and then blames the copy for.
status: draft
evidence: pending_dry_run
phase_0: REQUIRED. Establish ground truth on the operator's current domain and DNS access first.
modularity: PARTIALLY MODULAR. DNS and domain purchase need a human with registrar access. Everything
  after that can run through APIs or MCPs.
triggers:
  - "set up cold email infrastructure"
  - "my emails are going to spam"
  - "buy domains for outbound"
  - "warm up inboxes"
requires:
  - Registrar access, or a named person who has it and will act this week
  - A sending platform account
  - A budget line. Expect roughly a couple of hundred a month to send at any real volume
not_industry_specific: true
---

# Sending infrastructure

Send ten thousand cold emails from the domain your invoices go out on and you will spend the next
quarter wondering why customers say they never got your quote. The damage is not to the campaign, it
is to the business.

This skill separates what you send, so a bad outbound week cannot touch anything that matters.

---

## The four kinds of email, and why they never share a domain

| Kind | What it is | Where it sends from |
|---|---|---|
| **Business** | Your team's actual mail. Quotes, replies, contracts. | Your real domain. Never anything else. |
| **Transactional** | Sent by a product to a customer. Receipts, password resets. | A subdomain of the real domain, authenticated separately. |
| **Marketing** | Newsletters and campaigns to people who opted in. | A subdomain, or its own domain. |
| **Cold** | Outbound to people who have not opted in. | Dedicated domains that are not the real one, and are never used for anything else. |

The rule is simple. Reputation attaches to the sending domain. Keep the risky sending on domains you
can throw away, and keep the domain your business depends on out of the blast radius.

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

One question at a time. Skip anything Phase 0 already answered.

**What exists now**
1. What is the real business domain, and who controls its DNS? Get a person's name, not a company.
2. What already sends mail from it? Walk every tool: CRM, booking, invoicing, newsletter, the website.
3. Has anyone ever set up SPF, DKIM or DMARC on it? "I do not know" is a real answer and is the
   usual one. It gets checked, never assumed.
4. Has this domain ever been used for cold outreach before? If so, when, how much, and what happened.
5. Do you use a shared inbox, and who else sends from it.

**The plan**
6. What daily volume are you actually planning? Per day, not per month.
7. Over what period. A one-off push and an always-on programme need different infrastructure.
8. Who answers the replies, and how many a day can they handle before it falls over?
9. What is the monthly budget for this? Say the number out loud before we buy anything.

**Risk**
10. What would it cost you if your main domain stopped reaching customers for a fortnight?
11. Which jurisdictions are you sending into? This changes what has to be in every message.
12. Do you have a suppression list already, and where does it live.
13. Has anyone ever complained about your email, and what happened.

Confirm all thirteen back, then show them the arithmetic (daily volume, inboxes, domains, cost)
before a single domain is bought.

---

## Phase 1. Ground truth before anything is bought

Ask, one question at a time:

1. What is the real business domain, and who controls DNS for it? Get a name, not a company.
2. What is already sending from it today? Check every tool: the CRM, the booking system, the
   newsletter, the accounting software.
3. Is SPF, DKIM and DMARC set up on it now? If the operator does not know, that is the answer, and it
   gets checked rather than assumed.
4. What volume are you actually planning? Per day, not per month.
5. What is the follow-up capacity on the other end? If nobody can answer twenty replies a day, do not
   build for two hundred.

**Check the real domain's authentication before buying anything.** Plenty of businesses discover here
that their ordinary mail has been half-authenticated for years. Fixing that is worth more than the
entire outbound build, and it has to happen first.

---

## Phase 2. Buy the sending domains

- Buy variants of the business name that a recipient would recognise as you and would not mistake for
  a different company. Common patterns are a hyphen, a different top-level domain, or a "get" or
  "try" prefix.
- Never impersonate another business, and never buy something confusingly close to a competitor.
- Two to three inboxes per domain. More than that on one domain concentrates the risk you just spent
  money spreading.
- Redirect each domain to the real website. A recipient who types the domain in should land somewhere
  real, and a domain that resolves to nothing looks like exactly what it is.

For each domain set up SPF, DKIM and DMARC before the first send. A domain without all three will not
reach an inbox reliably in 2026, and no amount of warmup fixes it.

---

## Phase 3. Warm the inboxes

New domains have no reputation. Sending volume from a cold one is the single most common way this
whole build fails in week one.

- Two to three weeks of warmup before any real send. There is no shortcut worth the risk.
- Ramp gradually. Start at a handful of sends a day per inbox and increase slowly.
- Cap at twenty to thirty a day per inbox in steady state. The instinct to push this is the instinct
  that kills the domain.
- Keep warmup running underneath the real sending. It is not a phase you finish.

Compute the fleet from the target: daily volume divided by the per-inbox cap gives the inbox count,
and that count divided by three gives the domains. Show the operator that arithmetic before they buy,
because it is usually the moment the plan gets realistic.

---

## Phase 4. The rules that go in the platform

- Every message carries accurate sender identification and a working unsubscribe. In Australia the
  Spam Act requires both, and the unsubscribe must keep working for at least thirty days and be
  honoured within five working days.
- Suppression list is global across every campaign and every domain. One unsubscribe means never
  again, from anywhere you send.
- Bounces are removed immediately and automatically. A rising bounce rate is the fastest route to a
  blocked domain.
- No tracking pixel on the first touch. It adds nothing you cannot infer from replies and it hurts
  placement.
- One person, one sequence, at a time. Somebody in two campaigns at once will notice.

---

## Phase 5. Monitor the numbers that predict a collapse

Check weekly, per domain and per inbox. These are the leading indicators, and they move before the
reply rate does:

| Number | Healthy | Act when |
|---|---|---|
| Bounce rate | Under 2 percent | Over 3 percent, stop that inbox and re-verify the list |
| Spam complaints | Under 0.1 percent | Over 0.3 percent, stop the campaign and reread the copy |
| Reply rate | Varies by market | It halves week on week with the same list quality |
| Inbox placement | Test monthly | Any domain landing in spam on a seed test |

When a domain goes bad, retire it. That is what the disposable structure is for, and trying to
rehabilitate one costs more than a new one.

---

## What this costs, roughly

Domains are a few dollars each a year. Hosted inboxes run a few dollars each a month. A sending
platform starts around a hundred a month. Sending at ten thousand a month lands in the low hundreds
all in. If a plan cannot carry that, the plan is a smaller volume, not a cheaper shortcut.

---

## Gates

- **G1.** The real domain's authentication was checked and fixed before anything was bought.
- **G2.** Cold sending never leaves the real domain or any subdomain of it.
- **G3.** Every sending domain has SPF, DKIM and DMARC, verified by a lookup, not by assumption.
- **G4.** Warmup ran for at least two weeks and continues underneath live sending.
- **G5.** Per-inbox daily cap is set in the platform, not left to a person's discretion.
- **G6.** Unsubscribe works, is honoured globally, and was tested end to end by a real click.
- **G7.** The weekly monitor exists and a named person reads it.
