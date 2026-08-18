---
name: linkedin-outreach
description: Preflight and send an explicitly approved batch of personalised LinkedIn connection invitations through supervised Codex Computer Use, using a canonical template, recipient verification, mapped profile variants, a daily cap, and a durable contacted ledger. Use when you need to send an approved LinkedIn connection batch. Do NOT use for sourcing, cold email, unapproved recipients, scraping private data, login automation, or messages outside the approved template.
---

# LinkedIn outreach

Send only a reviewed target set through your signed-in LinkedIn session. Auto-send is permitted only after one preflight explicitly approves the ordered recipients, canonical note, and cap.

## Load

Read:

- The current Computer Use skill.
- Your own profile-schema map for the platform's current top-card structure.
- The target run file with original-case LinkedIn URLs.
- The canonical template.
- Your contacted ledger, keyed by normalized profile URL.

Drive it through your Computer Use runtime. Never automate login. Never use the lowercased ledger URL for navigation because obfuscated LinkedIn URLs are case-sensitive.

## Preflight gate

Resolve only targets that are evidence-backed and clear of your anti-signal rules. Remove the skip list and every ledger hit. Default cap is 15.

Present the exact ordered names, count, state, original-case URLs, canonical template path, rendered note, already-contacted skips, and cap. Wait for explicit approval of all three: targets, template, and cap. Any change requires a fresh preflight.

## Fast profile procedure

Process one profile at a time:

1. Navigate directly to the original-case URL.
2. Fetch one fresh app state. Verify the visible owner name and URL against the approved row.
3. Classify the owner top card: direct Connect, owner More with Connect, Follow with no Connect, bare More, connected, or ambiguous.
4. Anchor every action to the top-card section containing the profile heading. Ignore recommendation-rail controls even when they appear higher on the page.
5. Use direct Connect when owner-scoped. Otherwise open the owner-scoped More menu and choose the exact visible `Connect` item.
6. Choose Add a note. Verify the recipient and exact rendered note, then enter it.
7. Click Send under the approved batch authority.
8. Fetch fresh state once. Accept explicit invitation confirmation, modal closure plus changed owner action, or a confirmation toast. LinkedIn may show no Pending marker.
9. Write the confirmed result to the ledger immediately using the normalized URL key while preserving the original URL in the run evidence.

Use accessibility elements before coordinates. Fetch new state after navigation, menu opening, modal opening, and Send. Reuse no stale element index. Use screenshots only when accessibility text cannot resolve the owner-scoped action.

## Variant order

1. Ledger hit: skip before navigation when possible.
2. Direct owner Connect in the top card.
3. Owner-scoped More, then exact menu text `Connect`.
4. Follow or bare More with no Connect: record `no-connect` and continue.
5. Already connected: record `already-connected` and continue.
6. Ambiguous owner or control: stop that profile without sending.

Never select the page's first, top-most, or nearest Connect or More control. Geometry does not prove ownership.

## Stop conditions

Stop the batch on name or URL mismatch, CAPTCHA, checkpoint, login redirect, invitation limit, missing note control, over-limit note, unexpected permission, unverified send, or the same unmapped drift on two profiles. Never retry Send blindly.

## Report

Return confirmed sent names and count, skips by reason, stopped profile and evidence, cap status, and exact external writes. A request counts only after explicit confirmation and immediate ledger recording.

Read `references/profile-variants.md` only when LinkedIn's top-card structure drifts or the detection order needs explanation.
