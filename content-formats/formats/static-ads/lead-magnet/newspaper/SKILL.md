---
name: lead-magnet-newspaper
description: F7.6.3. The newspaper front page for a lead-magnet static. Built on the downloaded newspaper template, Didone masthead, VHS coverage photo, two columns and a reversed CTA box. Use when building F-M3 for a new industry. Read formats/static-ads/SKILL.md and lead-magnet/SKILL.md first.
parent: static-ads-lead-magnet
format: F7.6.3
---

# F-M3, the newspaper front page

**Hook 3:** `The truth about using AI in your [avatar] business. It's a lot easier than you think.`
HOOKS.md: **A3** curiosity gap, **C9** the uncomfortable truth.

## Build

```
python3 plates_magnet.py <industry> editorial --go    # ONE paid job, the coverage photo
python3 build_editorial.py <industry>
```

**1 paid job per industry**, at 3:2, `vhs-camcorder` graded like the rest of the set.

## The law

**Built on the template, not referenced by it.** `../../references/newspaper-template.webp`, the
one the operator downloaded. The furniture is what does the work, so it is followed in order:

```
rule, issue line and date, rule
full-width Didone masthead
rule
hero photograph
lead headline
two body columns plus a reversed sidebar box
rule, footer line
```

**The first version was digital-article chrome and was rejected** for reading as our own authored
page, which is the one thing this format cannot do.

**The masthead is the industry's own word**, from `magnet_copy.INDUSTRIES[...]["paper"]`. Not an
invented publication: a made-up trade title close to a real Australian one is what gets a creative
pulled, and one word does the same job.

**The headline IS the hook, and it appears once.** An earlier pass ran it twice, as the headline
and again as an overlay on the photo. Saying it twice on one card reads as a template with a slot
left filled in.

**This card is the one deliberate break from your display typeface-only.** A newspaper set in your display typeface is not a
newspaper, and the borrow is the whole format. Didone for the masthead and headline, Georgia for
the body, both off the system font stack. Flagged, never silent: the lock covers house-branded
surfaces, and this card is dressed as somebody else's paper on purpose.

**The columns carry real copy.** Every claim in them is checkable against the built report: nine
areas at ten points each is what the report itself prints.

## Traps already paid for

- **`clientWidth` counts padding.** The masthead was solved 92px too wide off
  `parentElement.clientWidth` and ran its last letter off the page. Pass the measured width in.
- **An `<img>` carries its intrinsic height as its flex basis.** `flex:1 1 auto` let the coverage
  plate push the share row and the CTA clean off the bottom of the card. Use `flex:1 1 0` with
  `min-height:0`.
