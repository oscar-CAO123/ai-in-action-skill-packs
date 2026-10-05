# Phase 2. Interview

This interview feeds a PRD, so it goes deeper than a business interview. Every answer has to be
specific enough that a developer could build from it without calling the operator. Expect two hours.

## How to run it

- **One question per message.** Wait for the answer.
- **Skip what the sweep answered.** Say "The sweep says X, is that right?" and move on.
- **Make them concrete.** Whenever an answer is general, ask for the last real example: the actual
  customer, the actual job, the actual email. Then ask what happened at each step.
- **Walk the work as a sequence.** For every job: trigger, who owns it, what information comes in,
  which tool it happens in today, the exact action, the decision point, the output, the handoff, the
  exception, how it fails, how they measure it, and what they want the CRM or an agent to do instead.
- **Use the operator's words.** Their name for a thing becomes the table, field and page name. Record
  the word they use ("job", "matter", "booking", "order") and use it everywhere.
- **Conditional follow-ups.** Services get quoting, scheduling and delivery questions. Stock gets
  inventory questions. Regulated work gets compliance questions. Do not force irrelevant ones.
- **Save after every phase.** Write `interview/<phase>.md` with the answers in the operator's words,
  and update `.crm-build.json`. After every five questions print a `RUNNING SUMMARY` block grouped by
  phase so the operator can paste it into a fresh session.
- **No leading.** Ask "what happens next?" and wait. Do not offer three options and let them pick the
  nearest one.

---

## A. The business and the users

1. In one sentence, what does the business sell, and to whom?
2. Who will use the CRM every day? List each person or role.
3. For each role: what do they do in a normal day, and which tools do they open to do it?
4. Who must never see what? (Pay rates, other teams' customers, margins, private notes.)
5. Who is the owner of the data, and who decides what the CRM records?
6. How many users on day one, and how many in a year?
7. Does anyone outside the business need access (customers, contractors, an accountant)? What can
   they see?
8. What device do people use most? Desk, phone on site, tablet?

## B. The records (what the CRM holds)

For each kind of thing the business keeps track of, run questions 1 to 6. Start with the one that
matters most.

1. What is it called in your business? (The operator's word becomes the table name.)
2. Give me a real, recent example. Read me every piece of information you hold about it.
3. Which of those pieces do you look up often, and which are only ever filed?
4. Where does each piece come from, and who types it in?
5. What are the stages or statuses it moves through, in order, and what moves it from one to the next?
6. How many do you hold now, and how many do you add in a month?
7. What links to what? (A customer has many jobs, a job has many invoices, and so on.)
8. What do you wish you could see at a glance for it?

Repeat until the operator says there is nothing else. Then ask: "What do you track in your head or in
somebody's inbox that is not on this list yet?"

## C. The workflows (what happens to the records)

Pick the five to ten jobs that eat the most time. For each one:

1. Name the job and its trigger. What makes it start?
2. Walk the last time it happened, step by step, from the trigger to the end.
3. Which steps are judgement and which are the same every time?
4. Where does it wait on a person? How long does it usually wait?
5. What goes wrong most often, and what does it cost when it does?
6. What is the exception you handle by hand?
7. How do you know it was done right?
8. If the CRM did the repeatable steps and handed you the judgement, what would you want to see on
   screen at the moment you step in?

## D. The pipeline and the board

1. Is there a sales or delivery pipeline? Name every stage, in order.
2. What exact event moves something from one stage to the next? Who or what decides?
3. What should happen automatically when something moves? (A task, a message, a reminder, a document.)
4. What should raise an alert, and who gets it?
5. What does an overdue item look like, and what is the threshold in days or hours?
6. What do you report on each week? Ask for the last report they made, by hand if need be.

## E. Communication

1. Which channels do you use with customers? (Email, phone, SMS, chat, forms.)
2. Which messages do you send repeatedly? Read me the last one of each kind.
3. Which of them could safely go out on a schedule or an event, and which need a person to read first?
4. Which messages must never send without a human yes?
5. How do inbound enquiries arrive today, and who picks them up?
6. How fast do you need to respond, and what happens when you are late?

## F. Documents

1. Which documents do you make for customers or staff? (Quotes, proposals, contracts, reports,
   invoices, certificates.)
2. Show me the last one of each. What changes between versions, and what stays the same?
3. What are the brand rules? (Fonts, colours, logo, tone.)
4. Where do they live after they are made, and who needs to find them?

These become templates printed to PDF from HTML by the app.

## G. Money

1. How do you price and invoice? (Fixed, hourly, retainer, milestone, per unit.)
2. Which accounting tool do you use, and who owns it?
3. What should the CRM know about money? (Quoted, invoiced, paid, owed.) What should stay in the
   accounting tool only?
4. What is the tax setup the CRM must respect? Ask, never assume.
5. What do you chase, and how late is late?

## H. Integrations and data in

1. List every tool the CRM must read from or write to. For each: does it have an export or an API,
   and who holds the login?
2. What data must come in on day one? From where, how many rows, how clean?
3. What is duplicated across your tools today, and which one is the truth?
4. Which integration matters most in month one, and which can wait?

## I. Agents

1. Which agents do you already use, and what do you ask them to do?
2. Which jobs from phase C would you hand to an agent if it could read and write the CRM?
3. What may an agent do on its own, what must it ask first, and what must it never do?
4. Who is allowed to approve an agent's action, and where do they see it?
5. What do you want every agent to know about the business before it touches a record?

## J. Rules, risk and scale

1. What must never be deleted?
2. What data is personal or sensitive, and where may it never appear? (Exports, logs, screenshots.)
3. Which laws or contracts apply to the data? Ask, never assume.
4. What is the worst thing that could go wrong with this system, and how would you find out?
5. Who is on the hook when it breaks, and what do they need to see to fix it?
6. How will you know in three months that the CRM worked? Ask for a number.

## K. Scope and priority

1. If you could only have three things working in the first month, which three?
2. What is nice to have and can wait for month two or three?
3. What is out of scope on purpose?
4. What is the deadline, and what happens if it slips?
5. Who has the final say when two people want different things?

---

## Close

When the operator has nothing left, print one `INTERVIEW COMPLETE` block listing:

- the records and their stages in the operator's words,
- the workflows, ranked by pain,
- every integration with its owner,
- the three month-one outcomes,
- every open question you could not close.

Ask: "What did I miss?" Fold the answer in, save `.crm-build.json` with `{"phase": 2, "done": true}`,
and move to phase 3 by reading `reference/04-prd.md`.
