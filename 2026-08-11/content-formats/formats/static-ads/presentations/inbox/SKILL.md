---
name: static-ads-inbox
description: Presentation sub-skill. A cropped email screenshot, mail chrome in the platform's system font, the argument spoken by an invented sender to somebody else. Use when the card should read as trespass rather than as an ad. Shipped as the F5 inbox variant, LIVE on the CRM. Read formats/static-ads/presentations/SKILL.md, formats/static-ads/ui-mock/SKILL.md and formats/static-ads/SKILL.md first.
parent: static-ads-presentations
cites: local:a competitor-8-statics/04-inbox-screenshot
renderer: scripts/f5_variants.py build_inbox
---

# Inbox screenshot

**The mechanism.** Trespass. The reader is looking at mail addressed to somebody else, and the
chrome does the authenticating. Nothing is being claimed at the reader, so nothing is defended
against.

## 1. What is taken from the reference

`local:a competitor-8-statics/04-inbox-screenshot`: **the trespass, and the crop.** The reference is
cropped so the subject and the body run off both edges, which is what a real screenshot of a
phone-width thread looks like and what stops the card reading as a designed layout.

## 2. The chrome

Subject row, inbox chip, sender line, timestamp. That is what authenticates it.

- **No interface branding**, per `../../ui-mock/SKILL.md` section 3. No mail client logo, no
  platform name. A logo here is a competitor mark on a house ad and reads as a platform endorsement.
- **The face is the platform's system stack, never your display typeface.** A mail client set in your display typeface stops reading
  as a screenshot and the format's whole mechanism is that it reads as one. your display typeface returns on the
  foot strip, which is the ad speaking rather than the mail.

## 3. The gate that cannot move

**Every name on the card is invented and unidentifiable.** No real client, candidate or contact
appears, ever. This is the F18 gate and `../../proof/SKILL.md` binds it: a real person's name on a
fabricated email is the worst version of the fabrication problem.

The card that shipped uses `Dave Corrigan`, subject "the AI stuff is not working", stamp
"9:14 AM (2 hours ago)". All invented.

## 4. Two recorded exceptions, both your

1. **This card does not carry the approved sentence word for word.** The sender says the argument
   in his own voice instead. The paragraph it replaced quoted the approved sentence as something a
   third party had said, which you read as verbose and unnatural: a sender does not announce that
   a line has stuck with him, he just says the thing. The argument is unchanged.
2. **There is a negation swap in the body** ("We're a business, not a tech company"). It is your
   dictated wording and it is flagged rather than silently rewritten. The house ban is on the house's own
   voice doing it; this is a character speaking. **Ruling pending**, and it is written into the
   card's `notes` on the CRM row.

## 5. Writing the body

Five short paragraphs, a person typing at speed, no marketing register anywhere in it. The shipped
agnostic version runs: a meeting coming up, the stack named by what each tool does, the admin now
sitting with the owner, the argument, then the ask.

**The specifics move up a level rather than disappearing when the card runs agnostic.** The
construction-flavoured draft ("site meeting", "the quoting software") was the best-reading version
and it is exactly what the agnostic instruction removes, so it became a meeting, a stack of tools
named by what they do, and two people carrying it.

## 6. Running it

```
cd "the business/skills/content-formats/formats/static-ads/scripts"
python3 f5_variants.py inbox                    # agnostic, free
python3 f5_variants.py inbox --industry retail  # one vertical
python3 f5_review.py                            # the dossier, beside its reference
```
