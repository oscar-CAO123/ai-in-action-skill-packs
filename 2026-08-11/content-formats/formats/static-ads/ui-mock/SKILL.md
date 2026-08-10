---
name: static-ads-ui-mock
description: F7 sub-skill. The card imitates an interface the reader already trusts. Owns message-thread, post-card and comment-row chrome, and the fidelity rules that keep a mock honest. Use for the iMessage chat, the organic post screenshot, and the comment reply ad. Read formats/static-ads/SKILL.md first for the shared law.
parent: static-ads
format: F7.3
---

# F7.3 UI-mock statics

A card that looks like something the reader received rather than something a brand paid for. The
whole value is the half-second before the reader classifies it as an ad, so fidelity is the format.

**Read `../SKILL.md` first.** This sub-skill breaks the band law by design: an interface cannot live
inside a bottom type band, and the operator recorded that deviation on 2026-08-06 for this test.

**Cost: free.** Chrome renders HTML and CSS, which is what an interface is made of. The comment
reply is the one exception, because it sits over a phone-snapshot plate that is authorised and
unshot.

---

## 1. The three formats

| Format | Archetype | What it imitates | Funnel |
|---|---|---|---|
| **iMessage / WhatsApp chat** | S3 | A thread between the owner and someone in their business | TOF |
| **Organic post screenshot** | S15 | A personal LinkedIn post, not a company post | TOF |
| **Comment reply ad** | house | A comment row and the brand's reply beneath it | TOF |

Cell assignments: `../FORMAT-GRID.md` section 2. All three are TOF, which is the point: these are
the native shapes that scale cold, and they are what the long-running accounts in the swipe bank
actually run.

## 2. Fidelity is the format

A mock that is nearly right is worse than no mock, because the reader notices the wrongness before
they read the words. Match the real interface exactly:

- **Real chrome.** Correct bubble radii, correct tail, correct read receipt, correct timestamp
  format, correct system font for that platform. Screenshot the real thing and match it rather than
  approximating from memory.
- **Real proportions.** A thread on a 4:5 canvas is a crop of a phone screen, so the status bar,
  the safe area and the keyboard either belong in frame or are cropped cleanly out. Half a keyboard
  is the tell.
- **Plausible content.** Names, handles, avatars and timestamps have to be internally consistent.
  A reply that arrives before the message it answers is the second most common tell.
- **The blue accent stays a house decision.** iMessage blue is the interface's own colour, not the
  card's accent. A card whose interface is already blue takes no separate accent.

## 3. What may not go on a mock

- **No real person's name, handle, avatar or profile photo** unless it is a founder's own and
  the operator has signed it. Everyone else is invented and unidentifiable.
- **No fabricated testimonial, reaction or comment attributed to a real client.** A mocked comment
  praising house is a fabricated testimonial wearing an interface. `../proof/` governs the moment a
  real client's words appear, and the fabrication ban is absolute.
- **No competitor logo, name or interface branding.**
- **Nothing that reads as a platform endorsement**, which is a policy problem as well as a trust
  problem.

The organic post screenshot is a **personal profile post from Simon**, which is exactly why it sits
on financial services / owner-bottleneck: the pain is the owner personally building the automation,
and a personal post is how that gets said. It is first person, it is his, and it is gated by
`../proof/`.

## 4. Writing the copy

The copy is dialogue rather than headline. It has to read like a message someone actually sent,
which means contractions, lower case where a person would use it, and no marketing cadence.

- **The avatar is named inside the interface**, which is the one place it can go: the contact name,
  the group title, the poster's headline, the commenter's own words. A thread between two unnamed
  people is a thread about nobody. Parent `SKILL.md` section 2.
- **Sentence case, always.** Nobody types in caps. This is the sub-skill where the news-carousel caps
  doctrine is most obviously wrong, and caps here destroy the format outright.
- **One exchange, one idea.** A thread that carries two points carries neither.
- **The pain arrives in the reader's own words**, taken from the playbook's verbatim call quotes,
  which is the whole reason those quotes are kept verbatim.
- **The turn lands in the last bubble.** Everything before it is setup.
- House floor still applies: no em dashes, no negation swap, house terminology.

## 5. Building it

No template exists yet. The route is HTML and CSS rendered by the same headless Chrome path
`band.py` already uses, with the interface built as real markup rather than an image. Write each
mock as its own template function so the chrome is reusable across cells and one fix corrects every
card using it.

The comment reply is the only one of the three needing a plate: a phone snapshot with on-camera
flash, authorised as one of the two paid jobs in `../FORMAT-GRID.md` section 4 and not yet shot.
Approve it on its own, one job, before anything renders on top of it.

## 6. QA

- Put it beside a real screenshot of the same interface at the same zoom. Anything that differs is
  a defect.
- Read it at thumbnail size, where an ad-classified card dies.
- Funnel label recorded, sources recorded, no real name that is not Simon's.
- Em dash scan, negation-swap scan, banned vocabulary, house terminology.
