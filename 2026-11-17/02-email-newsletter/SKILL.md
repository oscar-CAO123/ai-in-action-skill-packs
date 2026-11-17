---
name: email-newsletter
allowed-tools: Read, Write, Bash(node check.mjs:*)
description: Author a designed HTML email newsletter on your own computer, check it against the rules email clients enforce, and hand the file over for sending. Use when someone asks for a newsletter, a campaign email or a designed HTML email. The agent drafts and checks only. It never sends, schedules or uploads anything, and the person sends the email from their own email or mailing tool.
---

# Email newsletter

Write one HTML email that renders the same in Gmail, Outlook and Apple Mail, check it, and hand the file to the person. You draft and check. The person sends it.

## Hard limits

- Never send, schedule, upload or publish the email. Never call a send, reply or forward tool.
- Never invent a figure, testimonial, price or claim. Use only facts the person gives you. Ask when one is missing.
- Do not call the email ready until `check.mjs` exits 0 and every warning has been read.

## Before you write

Get these from the person. Ask for anything missing, one question at a time.

1. Audience: who receives it and why they signed up.
2. One action: the single thing you want the reader to do, such as a click, a reply or a booking.
3. Brand kit: colours, typeface, logo (as a hosted https:// image) and the business name.
4. Footer details: business name and postal address. Most countries require both.
5. Pictures: the files, and where they are hosted.
6. Subject line and preheader (the short line shown after the subject in the inbox).

## Method

1. Write the copy first as plain text: subject, preheader and every line. Get it approved before you build any layout.
2. Build on one 600px container table. Delete any section the email does not use.
3. Put every style inline on each element. The one `<style>` block in the head holds only media queries for phone width.
4. Add `role="presentation"` to every layout table.
5. Host each picture on an https:// address. Give each one alt text that says what it shows. Add `display:block` to each picture's style.
6. Keep the file under 100KB. Gmail cuts off anything past about 102KB, and the unsubscribe link goes with it.
7. Put a plain text unsubscribe link in the footer: `<a href="{{unsubscribeUrl}}">Unsubscribe</a>`. If the person's mailing tool uses another tag, change `UNSUB_TOKEN` at the top of `check.mjs` to match.
8. Write no em dashes. Use a comma, a full stop, a colon or brackets.
9. Save it as `newsletter-<date>.html` in the project folder. Run `node check.mjs <file.html>`. Fix every ERROR. Read every warning and decide.
10. Open the file in a browser. Narrow the window to phone width and confirm the columns stack and nothing overlaps.
11. Go through `deliverability.md` with the person. Whoever runs their domain sets the DNS records.
12. Hand off. Give the file path, the subject, the preheader and the checks that passed. Tell the person to send a test to themselves first, then send from their own tool.

## Design rules

- Write like a person. Short sentences, plain words, the positive thing said directly.
- Use the brand kit only. Keep to one typeface with a web-safe fallback stack, and two or three colours at most.
- One button, one action. Button text is a short verb phrase.
- Keep most of the email as real text. A single large picture with little text reads as spam to filters.
- Do not use flexbox, grid, fixed or absolute positioning, scripts, forms or background images for key content. Email clients ignore or strip them.
- Dark designs can change in some phone mail apps, so look at a dark email on a phone before it goes out.

## What check.mjs checks

- Size under 100KB.
- A 600px container table, and `role="presentation"` on every table.
- No scripts, frames, forms, outside stylesheets or event handlers.
- Styles inline, with the `<style>` block holding only media queries.
- Alt text on every picture, and an absolute https:// address for each.
- A plain text unsubscribe link.
- No em dashes, as the character or as an HTML entity.
- Doctype, charset and a hidden preheader (warnings).

It checks the rules, not the look. Read the render yourself.

## Commands

```
node check.mjs path/to/email.html
```

Exit 0: no errors. Exit 1: at least one error. Exit 2: bad usage. Needs Node 14 or newer and nothing else.

## Writing rules

Plain English, short sentences. No em dashes. Never write "it's not X, it's Y". 
Never use: delve, leverage, unlock, seamless, game-changer, robust, elevate.
