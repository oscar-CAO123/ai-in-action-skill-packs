# Language rules

Binding on every word this system produces, in every format, including chat replies from the agent.

## The reference cadence

Three sentences {{OWNER_NAME}} actually wrote, quoted verbatim. Sit every draft next to these.

1. "{{REFERENCE_SENTENCE_1}}"
2. "{{REFERENCE_SENTENCE_2}}"
3. "{{REFERENCE_SENTENCE_3}}"

If a sentence would not sit comfortably beside those, rewrite it.

## Decisions, not adjectives

| Decision | Ours |
|---|---|
| Contractions | {{CONTRACTIONS}} |
| Person | {{PERSON}} |
| Swearing | {{SWEARING}} |
| Humour | {{HUMOUR}} |
| Sentence length | {{SENTENCE_LENGTH}} |
| Regional register | {{REGISTER}} |
| Units and spelling | {{UNITS}} |

## Terminology

Words we always use, and the words they replace.

| Never say | Always say | Why |
|---|---|---|
| {{NEVER}} | {{ALWAYS}} | {{REASON}} |

## Structural bans

Absolute, no exceptions, enforced by `../engine/cos/gate.py`.

- Em dashes. Use a comma, a period, a colon, or parentheses.
- The negation swap: "it is not X, it is Y", in every variation.
- Rhetorical question stacks. One per asset, maximum.
- Opening on a definition.
- Closing on "the choice is yours" or any relative of it.

## Lexical bans

The generic list is in `copywriting.md`. Ours, on top of it:

- banned: {{OUR_BANNED_WORDS}}

## Claims we cannot back up

These are never stated as fact, in any format. From interview question 50.

- {{UNSUPPORTED_CLAIM}}

## Compliance

Regulator or body: {{REGULATOR}}

Rules that bind our claims: {{COMPLIANCE_RULES}}

## Changelog

- {{DATE}}: written from interview questions 44, 50 and 51.
