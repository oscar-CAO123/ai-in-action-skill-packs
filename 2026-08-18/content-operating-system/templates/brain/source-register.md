# Source register

Where this business keeps proof of what its customers actually say, how the agent reaches each one,
and what each is good for. Ranked by volume times honesty, which is also the ingestion order.

The machine-readable half of this lives in `../engine/config.json`. Keep them in step.

---

## {{SOURCE_NAME}}

- **Rank:** {{RANK}}
- **Where:** {{LOCATION}}
- **Reach:** {{HOW_THE_AGENT_REACHES_IT}}
- **Depth:** {{DATE_RANGE}}, roughly {{COUNT}} records
- **Record:** {{RECORD_SHAPE}}
- **Redaction:** {{REDACTION_NOTE}}
- **Good for:** {{WHAT_IT_YIELDS}}
- **Known gap:** {{GAP}}

---

## Connections

| Platform | Status | Reached by | Variables | Expires | Verified | Unlocks | Blocked by |
|---|---|---|---|---|---|---|---|
| {{PLATFORM}} | {{STATUS}} | {{METHOD}} | {{VARS}} | {{EXPIRY}} | {{VERIFIED}} | {{UNLOCKS}} | {{BLOCKER}} |

A blocked row is a real deliverable. It says what to chase and what it would buy.

## Sources mapped but not automated

| Source | Why manual | What it would take |
|---|---|---|
| {{SOURCE}} | {{REASON}} | {{REQUIREMENT}} |

## Privacy

- Redaction happens at ingestion, never at output.
- Kept: {{KEPT_FIELDS}}. Stripped: names, emails, phone numbers, addresses, company names.
- Never send an unredacted record to a third-party model.
- Named quotes for testimonials are a separate per-quote approval and never run on a schedule.

## Changelog

- {{DATE}}: built from interview phase H and the connection setup.
