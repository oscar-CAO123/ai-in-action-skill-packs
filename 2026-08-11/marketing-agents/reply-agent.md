---
name: Reply Agent
slug: reply-agent
description: >
  An INSTRUCTIONAL skill: it walks the operator's agent through putting an agent on the reply side
  of an outbound campaign. A webhook fires on every reply, the agent classifies it, drafts the next
  message against a written goal, and either stages it for a human or sends it inside a narrow
  approved lane. Handles the booking handoff, the objection, the wrong-person redirect and the
  unsubscribe. Also runs the long tail: the person who said "not now" in March gets a real follow-up
  in September rather than being lost.
status: draft
evidence: pending_dry_run
phase_0: REQUIRED. Establish ground truth on the sending platform and calendar before building.
modularity: HARDWARE-MODULAR. Needs somewhere to receive a webhook. A hosted runtime or a small
  always-on server both work. A laptop does not.
triggers:
  - "agent to manage my inbox replies"
  - "automate my outbound replies"
  - "book demos from replies automatically"
  - "follow up the leads that went cold"
requires:
  - A sending platform with reply webhooks and an API
  - A calendar or booking tool with an API
  - Somewhere always-on to receive the webhook
  - A written goal, in one sentence, for what a conversation is for
not_industry_specific: true
---

# Reply agent

Outbound dies at the reply. The list gets built, the sequence goes out, twenty people answer, and
they sit unanswered for three days because the person who was going to handle it was busy.

This skill puts something on that inbox. It is deliberately narrow: it reads, it classifies, it
drafts, and it acts only inside a lane the operator drew.

---

## The one thing to get right first

Write the goal in a single sentence before building anything. Not "engage the lead". Something like:
"get a fit prospect to a thirty minute call on the calendar, and get everyone else off the list
politely."

Every classification, every draft and every gate below is measured against that sentence. Without it
the agent optimises for sounding helpful, which produces long threads and no calls.

---

## Phase 1. The lane

Decide, explicitly, what the agent may do without a person. Write it into the config, not the prompt.

| Action | Typical setting | Why |
|---|---|---|
| Read every reply | Automatic | No risk |
| Classify and route | Automatic | No outward effect |
| Unsubscribe someone | Automatic, immediately | Delay here is a legal problem, not a service one |
| Answer a factual question already in the knowledge base | Automatic, if the answer is verbatim from the source | Bounded |
| Send a booking link | Automatic to a clear-fit positive reply | The worst case is a wasted link |
| Write anything about price, scope or a commitment | Draft only, always | This is where a machine invents things |
| Anything to an existing customer | Draft only, always | Different relationship, different stakes |
| Anything after a complaint or an angry reply | Stop, escalate, no draft | A person handles this |

Start narrower than feels necessary. Widening the lane after two weeks of watching is easy. Explaining
an autonomous message to a customer is not.

---

## Phase 2. Classify

On the webhook, classify each reply into exactly one bucket:

- **Positive, fit.** Wants to talk, matches the ideal customer.
- **Positive, not fit.** Interested, but wrong for the offer. This one gets a real answer and an
  honest no, because they refer people.
- **Question.** Wants something answered before deciding.
- **Not now.** Explicit timing objection with a date or a season attached.
- **Wrong person.** Points at a colleague, or says it is not their area.
- **No.** Clear rejection.
- **Unsubscribe.** Any form of stop, including an unpleasant one.
- **Out of office.** Not a reply. Reschedule the sequence past the return date.
- **Angry or complaint.** Stop everything on that thread and escalate.

Give the classifier the goal sentence, the original message, the reply and nothing else. When it is
unsure, the answer is unsure, and unsure routes to a person. A wrong bucket produces a wrong message,
and the cost of that is much higher than a human glance.

---

## Phase 3. Act, per bucket

- **Positive, fit.** Confirm you can help, in one short paragraph that names their situation back to
  them, then offer the booking link. Never write a paragraph of qualification questions.
- **Positive, not fit.** Say so plainly, say who it is right for, and offer the one useful thing you
  can give them for free. Then remove them from the sequence.
- **Question.** Answer only from the knowledge base. If the answer is not in there, draft it and
  escalate. The failure mode to design against is a confident invented answer about your own pricing.
- **Not now.** Extract the date. Confirm you will come back then. Schedule it. This is the single
  highest-return behaviour in the whole build and almost nobody does it.
- **Wrong person.** Ask for the right one, thank them, and stop the sequence to that address.
- **No.** One line, gracious, suppress. No save attempt.
- **Unsubscribe.** Suppress globally, immediately, then confirm in one line.
- **Out of office.** No reply. Push the sequence.
- **Angry.** Stop, escalate, notify a person now.

Every action writes a row to the audit log: the reply, the bucket, the confidence, what was drafted
or sent, and who approved it.

---

## Phase 4. The long tail

Most of the value in a mature list is here, and it is the part that gets built last or never.

- Anyone who said "not now" with a date gets a scheduled return at that date, with a message that
  refers to what they said. Not a fresh sequence.
- Anyone who went quiet after a positive reply gets one nudge, then stops.
- Everyone who ever replied and did not buy is reviewable at six months, with something new to say.
  If there is nothing new to say, do not send.

Check against the calendar rather than the inbox to close the loop: did the booking actually happen,
did they attend, did it become a deal. Without that link the agent optimises for replies, and replies
are not the goal sentence.

---

## Phase 5. Watch it for two weeks

Before widening the lane, read every draft it produced. Specifically:

- Where did it agree to something nobody authorised?
- Where did it answer a pricing or scope question from its own imagination?
- Where did it miss a "not now" date sitting in plain English?
- Where did a person have to rewrite the draft completely? That bucket's instructions are wrong.
- What did it classify as unsure, and was it right to?

Fix the config and the knowledge base. Resist fixing it by making the prompt longer.

---

## Gates

- **G1.** The goal sentence exists and every bucket's action maps to it.
- **G2.** The lane is in config, not in a prompt, and a human can read it in ten seconds.
- **G3.** Unsubscribe is automatic, global and immediate.
- **G4.** Nothing about price, scope or commitment sends without a person.
- **G5.** Every answer to a question traces to a knowledge-base source, or it escalates.
- **G6.** Every action is logged with its confidence and its approver.
- **G7.** Angry and complaint replies stop the machine rather than being handled by it.
- **G8.** The calendar is the measure of success, not the reply count.
