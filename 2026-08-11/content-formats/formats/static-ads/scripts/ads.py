"""Single-image static ads for the business.

One entry per ad. Every entry records persona / angle / offer so the ad traces back to
canon, and `source` records where its numbers and language came from.

The card carries ONE block of type at ONE size, white, with a single blue accent.
`lines` is the full copy, hand-broken. `lead` is the same copy cut to the headline only.
The older `template` / `kicker` / `standfirst` / list fields are kept as provenance for
where each line came from; the renderer no longer reads them.

`structure` names the hook structure from `references/hooks/HOOKS.md` that the card is a
FILL of. Hooks are filled, never free-written (SKILL.md section 0, load order 4).

`primary` is the ad's primary text, which is where the education law lands for a static:
the card carries the hook and points at the lesson, the teach beat lives here
(SKILL.md section 1, and section 7c F7 "load on the primary text").

Accent: wrap the ONE accented span in [[double brackets]]. One per card, never two.
Scope: a figure from one discovery call says one business. See SKILL.md section 3.
"""

ADS = [
    {
        "slug": "s1-costly-typo",
        "structure": "HOOKS.md A1, Specificity + proof (the number is the hook)",
        "lead": ["ONE RE-ENTERED NUMBER COSTS THIS CONSTRUCTION BUSINESS [[REAL MONEY]],",
                 "AND IT LANDS AGAIN AND AGAIN."],
        "lines": ["ONE RE-ENTERED NUMBER COSTS THIS CONSTRUCTION BUSINESS [[REAL MONEY]],",
                  "AND IT LANDS AGAIN AND AGAIN."],
        "primary": """Win a project at an Australian building firm and the same job gets set up
again in every platform it touches. Premier, then Procore, then Procure Pro, then
HammerTech. Six or seven touch points a job, each one a person typing what another person
already typed.

Here is what closes it, in the order a good operator builds it:

1. One job record that everything else reads from, so there is one place a number can be
   right or wrong.
2. A sync that pushes the job into every platform the moment it is won, so nobody re-enters
   anything.
3. A variation log that reaches the crew on site the same hour the spec changes.
4. A weekly exception report listing every field that disagreed across the four systems.

Four builds, and the first two close most of it. The reason none of them exist yet is that
the seam between your systems belongs to nobody, and owning that seam is a full-time job.
It has a title now. the role you place.

Find the right person for the job. Link below.""",
        "template": "news",              # S1 news headline
        "persona": "construction", "angle": "A3", "offer": "house",
        "source": "canon/personas-and-avatars.md (construction persona): a costly rework incident, many times a year, at one firm",
        "kicker": "Construction",
        "headline": ["THE [[EXPENSIVE TYPO]]", "HIDING IN ONE", "AUSSIE BUILDER"],
        "standfirst": "Six or seven handoffs a job, and the seam between the systems "
                      "belongs to nobody.",
        "cta": "Hire a the role you place.",
    },
    {
        "slug": "s9-own-it",
        "structure": "HOOKS.md S1, The Contrarian claim (Stop [the thing everyone tells you to do])",
        "lead": ["STOP BUYING AI SUBSCRIPTIONS THAT BECOME",
                 "ANOTHER SYSTEM [[NOBODY OWNS.]]"],
        "lines": ["STOP BUYING AI SUBSCRIPTIONS THAT BECOME",
                  "ANOTHER SYSTEM [[NOBODY OWNS.]]"],
        "primary": """One business we spoke to had bought the whole team licences. Months later
nobody had opened them, and one staff member resigned rather than learn the software.

Before you buy another one, this is the order that actually works:

1. Write down the process first. A tool cannot automate something that only lives in
   somebody's head, which is why most rollouts die in week two.
2. Pick the one job that eats the most hours, and build for that alone. Quoting, receipts,
   lead follow-up, whichever it is in your business.
3. Give it an owner by name before it ships, because a system nobody owns stops working
   the first week somebody is on leave.
4. Only then buy the licence, and buy it for the people who will use it that week.

Most owners have the tools and no owner. The businesses pulling ahead did the opposite:
they hired one person to own the whole stack, on their payroll, full time. The role has a
name now. the role you place.

Find the right person for the job. Link below.""",
        "template": "thesis",            # S9 stop trying to use AI
        "persona": "general", "angle": "A4", "offer": "house",
        "source": "canon/CONCEPT-BANK.md pain 17 (staff resist the tooling): "
                  "licences bought and never opened; one business had a "
                  "staff member resign rather than learn the software",
        "line": ["STOP TRYING TO", "USE AI IN YOUR", "BUSINESS."],
        "sub": "Hire someone to [[own it]].",
        "cta": "yourdomain.example",
    },
    {
        "slug": "s11-us-vs-them",
        "structure": "HOOKS.md A5, The Insider (Here's what nobody tells you about X)",
        "lead": ["HERE IS WHAT NOBODY TELLS YOU ABOUT [[THE",
                 "CONTRACTOR]] WHO BUILT YOUR AUTOMATIONS."],
        "lines": ["HERE IS WHAT NOBODY TELLS YOU ABOUT [[THE",
                  "CONTRACTOR]] WHO BUILT YOUR AUTOMATIONS."],
        "primary": """He has a full book of other clients. He built it the way he builds everything, he
handed over a Loom and an invoice, and he is the only person alive who understands it. What
you have there is a rental, and the rent is his phone being answered.

Here is the handover checklist that makes a build survive the person who built it. Ask for
all five before the final payment leaves:

1. A written map of every automation, what triggers it, and what breaks if it stops.
2. Every credential in your accounts, in your password manager, never his.
3. The build itself in a workspace your business owns.
4. A one-page runbook for the three failures most likely to happen, written for whoever is
   in the office on the day.
5. A named person inside your business who can open it, read it and change it.

Number five is the one that decides whether you own the thing or depend on him. An AI
operator is that fifth item as a full-time hire: one business, five days a week, on
the hook at two in the morning, and still there after it ships.

Find the right person for the job. Link below.""",
        "template": "versus",            # S11 us vs them
        "persona": "general", "angle": "A5", "offer": "house",
        "source": "canon/personas-and-avatars.md (contractor and agency builds "
                  "that fell over); CONCEPT-BANK pain 15 (key-person dependence)",
        "headline": ["WANT AI IN YOUR", "BUSINESS?"],
        "them_label": "A CONTRACTOR",
        "them": ["A full book of other clients", "Gone when the invoice clears",
                 "Nobody left who can open it"],
        "us_label": "A YOUR OFFER",
        "us": ["One business, five days a week", "Owns it after it ships",
               "On the hook at two in the morning"],
        "cta": "Hire a the role you place.",
    },
    {
        "slug": "s14-checklist",
        # The eight items moved off the card and belong in the ad's primary text
        # (SKILL.md 7c, F7: E-005 and E-050 are a primary-text move). The card carries
        # the hook and points at the lesson, per the education law.
        "structure": "HOOKS.md appendix List 1 #7, \"N things no one told me about (topic)\"",
        "lead": ["[[EIGHT THINGS]] NOBODY TELLS YOU ABOUT",
                 "ADMIN IN A GROWING BUSINESS."],
        "lines": ["[[EIGHT THINGS]] NOBODY TELLS YOU ABOUT",
                  "ADMIN IN A GROWING BUSINESS."],
        "primary": """Eight jobs run every week in a growing Australian business, and not one
of them has a name on it:

1. Receipts reconciled by hand, at night.
2. Timesheets chased every morning.
3. The same job number typed into four systems.
4. Quotes waiting on the one person who can price them.
5. Leads sitting unread while somebody is on site.
6. Reports that nobody can read side by side.
7. The owner answering questions only the owner can answer.
8. Admin that starts when the site shuts.

Every one of them is somebody's second job, which is why they never get fixed. They are
also the same problem eight times over: work that falls between two systems and belongs to
nobody.

Three builds close most of the list. A job record everything else reads from, kills 3 and
6. A quoting assistant that drafts off your own price book, kills 4 and takes the pressure
off 7. A capture that answers every lead within the minute, kills 5. The rest follow once
somebody owns the stack.

That someone is a full-time hire on your payroll, and the role has a name now. An AI
operator.

Find the right person for the job. Link below.""",
        "template": "checklist",         # S14 the checklist static
        "persona": "general", "angle": "A1", "offer": "house",
        "source": "canon/personas-and-avatars.md (construction, trades and logistics personas: admin and bottleneck pains)",
        "headline": ["EIGHT PROBLEMS.", "[[ONE HIRE.]]"],
        "items": ["Receipts reconciled by hand", "Timesheets chased every morning",
                  "The same job typed into four systems", "Quotes waiting on one estimator",
                  "Leads sitting unread", "Reports nobody can read together",
                  "The owner answering everything", "Admin starting when the site shuts"],
        "answer": "YOUR OFFER",
        "cta": "yourdomain.example",
    },
    {
        "slug": "s2-second-job",
        "structure": "HOOKS.md S2, The Negative / problem call-out (Here's why [their outcome] is slipping)",
        "lead": ["HERE IS WHY ONE BUILDING OFFICE WORKS",
                 "[[THE NIGHT SHIFT]] AFTER EVERYBODY LEAVES."],
        "lines": ["HERE IS WHY ONE BUILDING OFFICE WORKS",
                  "[[THE NIGHT SHIFT]] AFTER EVERYBODY LEAVES."],
        "primary": """The foreman writes the day in a book that lives on the dashboard of the
ute. At six it comes into the office, and somebody types it in. Hundreds of transactions a
day, receipts reconciled by hand, timesheets chased on a Sunday. Hours every week, after
everybody has already gone home. A real wage bill spent on typing.

The five easiest builds for a building office, in the order they pay off:

1. Photograph the receipt on site and have it coded and filed before the ute leaves.
2. Timesheets that submit from the phone at knock-off, with the chase automated.
3. The day's site notes captured once, at the source, then pushed everywhere else.
4. A weekly report that assembles itself on Friday afternoon.
5. Purchase orders raised against the job without anyone opening a spreadsheet.

Every one of those is ordinary work that plenty of businesses already run. Yours has not
built them yet because building the five is a full-time job, and everyone in your office
already has one. That is the hire, and it has a title now. the role you place.

Find the right person for the job. Link below.""",
        "template": "split",             # S2 problem / solution split
        "persona": "construction", "angle": "A1", "offer": "house",
        "source": "canon/personas-and-avatars.md (construction persona): hundreds of transactions a day, hours a week of typing, a real wage bill",
        "kicker": "The second job",
        "problems": ["200 receipts a day", "Timesheets on a Sunday",
                     "A book on the dashboard"],
        "solution": ["ONE PERSON", "[[OWNS IT]]"],
        "cta": "Hire a the role you place.",
    },
    {
        "slug": "s9-cant-test",
        "structure": "HOOKS.md A4, The Question hook (asked so the honest answer is yes, per E-063)",
        "lead": ["HAVE YOU EVER HIRED SOMEBODY FOR A",
                 "SKILL YOU COULD NOT [[ASSESS?]]"],
        "lines": ["HAVE YOU EVER HIRED SOMEBODY FOR A",
                  "SKILL YOU COULD NOT [[ASSESS?]]"],
        "primary": """One agency director put the risk plainly: you can end up hiring people you
cannot check. He could cross-check a media buyer against people he knew were good. For
an AI hire he had nobody to check against, and no idea who teaches a person to do this.

Four questions that separate the people who have built something from the people who have
read about it:

1. Walk me through a system you built that is still running today. Who uses it, and what
   happens when it breaks?
2. What did you build that failed, and what did you do the day it failed?
3. Here is a real process from my business. What would you build first, and what would you
   deliberately leave alone?
4. Whose job changes if this works, and how would you handle that conversation?

Answer one and three well and they have been in the room. The rest is reference checking.

Two honest things about this hire. The salary is real money, because the market for people
who can actually do this is thin. And the role is genuinely new, so there is no fifteen
year track record to look at. That is the whole reason we assess them first, and it is
what we sell.

Find the right person for the job. Link below.""",
        "template": "thesis",            # S9 shape, A12 argument
        "persona": "agency", "angle": "A12", "offer": "house",
        "source": "canon/personas-and-avatars.md (agency persona): a director who cannot check an AI hire against people he trusts, and no clear idea who teaches the skill",
        "line": ["YOU'RE HIRING", "FOR A SKILL", "YOU [[CAN'T TEST.]]"],
        "sub": ["We assess them first.", "That's the whole product."],
        "cta": "Hire a the role you place.",
    },
    {
        "slug": "s12-question-bunker",
        "structure": "HOOKS.md A3, Curiosity gap (Most think they have good X until they...)",
        "lead": ["MOST OWNERS CALL IT A SIDE PROJECT",
                 "AT [[MANY HOURS A WEEK.]]"],
        "lines": ["MOST OWNERS CALL IT A SIDE PROJECT",
                  "AT [[MANY HOURS A WEEK.]]"],
        "primary": """One owner told us he was putting many hours a week into building
AI instead of scaling the business. Another had a list of applications that would genuinely
move the numbers and no time to implement any of them. Both were right about the
opportunity. Both were the most expensive junior AI engineer in the country.

If you are the one building it, hand over these three first, in this order:

1. The actual build work, handed to somebody whose whole week is this. Your version takes
   four months of nights. Theirs takes weeks.
2. The maintenance. Every automation breaks eventually, and right now the person it falls
   back to is you at nine at night.
3. The decision about what gets built next. That is the one most owners hold longest, and
   it is the one that keeps them in the bunker.

Keep the direction. You already know what the business needs, which is more than most
people who will ever work on it. You built the car. Somebody else should be driving it,
full time, on your payroll. The role has a name now. the role you place.

Find the right person for the job. Link below.""",
        "template": "question",          # S12 question hook
        "persona": "general", "angle": "A6", "offer": "house",
        "source": "canon/personas-and-avatars.md (general persona): many hours a week building AI instead of "
                  "scaling the business (compliance); a list of projects and no time to build them (e-commerce)",
        "line": ["MANY HOURS A WEEK", "BUILDING AI.", "[[WHO'S RUNNING", "THE COMPANY?]]"],
        "sub": "You built the car. Somebody else should be driving it.",
        "cta": "Hire a the role you place.",
    },
    {
        # The directed F7 build, . One new ad per format, written to refine the
        # format skill against a real asset. The construction persona is the best warm lead in the market
        # and is uncovered by the seven above.
        "slug": "s13-already-tried",
        "structure": "HOOKS.md appendix List 2 #3, \"Almost everyone starts (action) the wrong way\"",
        "lead": ["MOST OWNERS BUILD THEIR FIRST",
                 "SYSTEM [[ALONE, AFTER HOURS.]]"],
        "lines": ["MOST OWNERS BUILD THEIR FIRST",
                  "SYSTEM [[ALONE, AFTER HOURS.]]"],
        "primary": """You bought the tools, or you hired somebody, or you sat down and built
it yourself. It half works. One owner told us his build was fine on the good days, and he
needed someone who knew a bit more than he did.

You were right about the opportunity. Here are the three places a self-built system falls
over, and they are the same three every time:

1. One agent carrying every job. Load enough context into a single agent and it starts
   hallucinating. Every department needs its own, with its own instructions and its own
   data.
2. The integrations nobody warned you about. The API points on your platform are rarely as
   good as the sales page implied, so half the build turns into plumbing.
3. Nobody owns it on Monday. It worked the day it shipped, and there is no one whose job
   it is to notice when it stops.

Fixing one and two is a weekend of reading. Fixing three is a hire, because it is the only
one that keeps happening every week for the life of the business.

That hire has a title now. the role you place.

Find the right person for the job. Link below.""",
        "persona": "construction", "angle": "A11", "offer": "house",
        "source": "canon/personas-and-avatars.md (construction persona): a self-built setup that half works and needs more know-how; "
                  "one overloaded agent that starts to hallucinate; a platform API that is clunky to work with",
        "cta": "Hire a the role you place.",
    },
]
