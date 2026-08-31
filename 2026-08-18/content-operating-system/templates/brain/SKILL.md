# {{BUSINESS_NAME}} content, the router

Read this before writing a word of anything customer-facing. It routes. The detail lives in the file
it belongs to.

## Load order

1. This file.
2. `language-rules.md`. The bans are absolute and they apply to chat replies too.
3. `icp.md`. Who this is for, in their own words.
4. The format file for what you are making, in `formats/`.
5. `copywriting.md` for the craft, `doctrine.md` for the laws.

Only load what the job needs. A written post does not need the video format files.

## The one number

{{THE_NUMBER}}, currently {{CURRENT_VALUE}}. Every asset either moves it or explains why it exists.

## What we sell, in one line

{{POSITIONING_ONE_LINER}}

Detail: `positioning.md`.

## The three hard rules

1. **Every claim carries its proof tier.** Shown, quoted, or held. Anything that fits none of the
   three does not go in. See `doctrine.md`.
2. **Never free-write a hook.** Fill one from `formats/hooks.md` and record the id.
3. **Nothing is published without {{OWNER_NAME}}.** Every time, including when it is obviously fine.

## Where things live

| Need | File |
|---|---|
| Who the customer is | `icp.md` |
| What we believe | `brand-truths.md` |
| Our words and our bans | `language-rules.md` |
| The craft | `copywriting.md` |
| The laws | `doctrine.md` |
| How to write format X | `formats/<x>.md` |
| Hook structures | `formats/hooks.md` |
| What to ask {{OWNER_NAME}} on camera | `founder-questions.md` |
| Where our evidence comes from | `source-register.md` |

## The production order

```
evidence -> idea -> question -> hook -> script -> HUMAN
         -> stills -> HUMAN -> motion and voice -> gate -> HUMAN -> publish
```

Three human gates, none optional. The engine at `../engine/` enforces the mechanical half.

## Changelog

- {{DATE}}: built from the content operating system interview.
