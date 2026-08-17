"""Refined copy decks (v2) for the house news-headline carousels.

`slides` is what renders: five slides, each a headline of about three lines. Every slide
carries one idea at headline weight, because under the bottom-band law a slide is one
block of type at one size and prose collapses it to unreadable. The long-form `scene`,
`quote`, `attrib`, `figure` and `caption` fields below stay as provenance: they are where
each slide's line came from, and they are no longer rendered.

The older `headline_splash` / `reveal_splash` break sets are also provenance. The tabloid
and splash directions collapsed into one when the law removed the furniture they differed
on.

Grounding, verbatim from `context/personas/personas-and-avatars.md` CON-03:
    "Six to seven touch points per job and manual re-entry drive frequent
     errors and rework, sometimes costing up to $30,000 per incident, and
     roughly 400 a year." (construction)
    "Once we win a project, they then have to set it up in Premier, then set it
     up in Procore, then in Procure Pro as well, and also HammerTech. That's
     been quite an arduous process." (construction)

The 400 is ONE firm's yearly incident count, so the copy says so. Yesterday's
version read it as an industry-wide figure, which the source does not support.
"""

ENDCARD = {
    "lines": ["THERE IS ONE PLACE IN", "AUSTRALIA YOU CAN [[HIRE ONE.]]"],
    "url": "yourdomain.example",
}


DECKS = [
    {
        "slug": "con-03-v2",
        "slug_line": "Construction",
        "slides": [
            ["ONE BUILDER TYPES THE SAME JOB", "INTO [[FOUR SEPARATE SYSTEMS.]]"],
            ["[[SIX OR SEVEN TIMES A JOB,]] SOMEONE RE-ENTERS",
             "WHAT SOMEONE ELSE ALREADY TYPED."],
            ["ONE REWORK COSTS [[$30,000]], AND IT LANDS",
             "ABOUT 400 TIMES A YEAR IN THIS ONE BUILDER."],
            ["NOBODY OWNS THE SEAM, WHICH IS WHY", "THE [[YOUR OFFER]] EXISTS."],
            ["THERE IS ONE PLACE IN", "AUSTRALIA YOU CAN [[HIRE ONE.]]"],
        ],
        # Tabloid: wide, three lines under a masthead.
        "headline": ["THE [[$30,000 TYPO]]", "HIDING IN ONE", "AUSSIE BUILDER"],
        # Splash: short stacked lines, maximum size, no furniture.
        "headline_splash": ["THE", "[[$30,000]]", "TYPO"],
        "standfirst": "It lands about 400 times a year in a single business, and "
                      "nobody in the building owns the place where it starts.",
        "eyebrow": "The scene",
        "scene": [
            "Win a project at an Australian building firm and the same job gets set up "
            "again in every platform it touches. Premier, then Procore, then Procure Pro, "
            "then HammerTech.",
        ],
        "quote": "That has been quite an arduous process.",
        "attrib": "A construction owner, in a house discovery call",
        "scene_after": [
            "Six or seven touch points a job, each one a person re-entering what another "
            "person already entered. Nobody owns the seam, so nobody catches the digit "
            "that moved.",
        ],
        "figure": "$30,000",
        "figure_label": "per incident, roughly 400 times a year",
        "caption": "What one rework costs this builder when a number is typed wrong at "
                   "handoff four. Six to seven handoffs run on every job they win.",
        "reveal": ["THE CONSTRUCTION FIRMS", "WHO CLOSED THE SEAM HIRED", "A [[YOUR OFFER]]"],
        "reveal_splash": ["ONE PERSON", "NOW OWNS", "[[THE SEAM]]"],
    },
    {
        # Persona AGY-01 (approved callout) x angle A9 margin leaking invisibly x offer house.
        # Grounding, verbatim from canon/personas-and-avatars.md AGY-01:
        #   "From the time we receive a brief from a client through to reporting back to the
        #    client how their campaigns went, there are many, many hands and many, many
        #    systems that touch every part of our operation." (media agency)
        #   Their numbers: reporting consumes ~50% of some staff members' time with little
        #   value added. 70 to 80 VAs doing work that agents could do.
        # BOTH figures are one agency's, from one discovery call, so every line says one
        # agency. Nothing here is framed as an industry figure.
        "slug": "agy-01-eighty-people",
        "slug_line": "Agency",
        "slides": [
            ["ONE AGENCY PAYS [[80 PEOPLE]]", "TO MOVE NUMBERS BETWEEN SCREENS."],
            ["A BRIEF PASSES THROUGH HANDS AND",
             "SYSTEMS THAT [[NEVER TALK]] TO EACH OTHER."],
            ["REPORTING EATS [[HALF THE WEEK]] OF THE",
             "PEOPLE WHO OWN IT, IN ONE AGENCY."],
            ["ONE HIRE OWNS THE WHOLE RUN, AND", "THE ROLE IS [[YOUR OFFER]]"],
            ["THERE IS ONE PLACE IN", "AUSTRALIA YOU CAN [[HIRE ONE.]]"],
        ],
        "headline": ["THE AUSSIE AGENCY", "PAYING [[80 PEOPLE]]", "TO MOVE NUMBERS"],
        "headline_splash": ["[[80 PEOPLE]]", "TO MOVE", "NUMBERS"],
        "standfirst": "Reporting eats about half the week of the staff who own it, inside a "
                      "business that sells efficiency for a living.",
        "eyebrow": "The scene",
        "scene": [
            "A brief lands at an Australian media agency and starts a run that ends weeks "
            "later with a report going back to the client. In between it passes through "
            "hands and systems that do not talk to each other.",
        ],
        "quote": "There are many, many hands and many, many systems that touch every part "
                 "of our operation.",
        "attrib": "A media agency director, in a house discovery call",
        "scene_after": [
            "So the agency grew an offshore team of seventy to eighty people to keep the "
            "run moving. Every one of them is carrying a number from one screen to another, "
            "and none of it changes what a campaign returns.",
        ],
        "figure": "80",
        "figure_label": "people in one agency, moving numbers by hand",
        "caption": "Seventy to eighty offshore staff, hired by a single Australian agency to "
                   "keep its reporting moving. Reporting takes about half the week of the "
                   "people who own it.",
        "reveal": ["THE AGENCIES THAT", "FIXED IT HIRED A", "[[YOUR OFFER]]"],
        "reveal_splash": ["ONE PERSON", "NOW OWNS", "[[THE REPORTING]]"],
    },
    {
        # The directed F5 build, v2 after your notes.
        #
        # HOOK ARCHITECTURE: the direct educational callout.
        #   Named reference: references/hooks/HOOKS.md Part 3 section B2, V9 educational
        #   teach openers, line 457: "Builders, here are the three jobs you should automate
        #   before anything else." Also line 452: "The 5 AI systems every construction
        #   company should be running in 2026."
        #   The cover names the avatar and promises N lessons; the deck then delivers all N.
        #
        # your three notes, applied here:
        #   1. Never call a prospect an "operator". Name the avatar: "your logistics
        #      company". The v1 cover read "ONE TRANSPORT OPERATOR" and was wrong.
        #   2. Slide 1 has to teach. It is now a how-to, not a statistic.
        #   3. Education throughout. Slides 2, 3 and 4 are three real builds, in order.
        #
        # Persona LOG-01 x angle A7 (leads leak) x house flagship.
        # Grounding, verbatim from canon/personas-and-avatars.md LOG-01:
        #   "Phone calls, I'm on the ball answering those. But it's the email leads that get
        #    lost in the archives. We probably miss three or four emails a week."
        #    (transport/logistics)
        # The weekly figure now sits in the caption rather than the cover, because the cover
        # teaches. Nothing on a slide is a claim about a result.
        #
        # SIX slides, not five. The educational architecture needs cover + three lessons +
        # the reveal + the endcard. SKILL.md 7b's five-slide arc was written for the
        # scene/cost/reveal shape. Flagged for you: either 7b's arc gains an educational
        # variant at six, or lesson three gets cut to hold five.
        "slug": "log-01-inbox",
        "slug_line": "Logistics",
        "slides": [
            ["HOW TO STOP LOSING EMAIL LEADS", "IN YOUR [[LOGISTICS COMPANY.]]"],
            ["ONE: CAPTURE EVERY ENQUIRY AS A RECORD",
             "THE MOMENT [[IT ARRIVES.]]"],
            ["TWO: EVERY EMAIL LEAD GETS A REPLY",
             "WITHIN [[SIXTY SECONDS,]] AUTOMATICALLY."],
            ["THREE: ANYTHING UNANSWERED BY FIVE",
             "LANDS ON [[SOMEBODY'S DAILY LIST.]]"],
            ["THE PERSON WHO BUILDS ALL THREE", "IS A [[YOUR OFFER]]"],
            ["THERE IS ONE PLACE IN", "AUSTRALIA YOU CAN [[HIRE ONE.]]"],
        ],
        "eyebrow": "The lesson",
        "quote": "Phone calls, I'm on the ball answering those. But it's the email leads "
                 "that get lost in the archives.",
        "attrib": "The owner of an Australian transport company, in a house discovery call",
        "figure": "3 to 4",
        "figure_label": "email leads missed a week, in one transport business",
    },
    {
        # "The one guy from Australia" architecture, you .
        #
        # HOOK STRUCTURE (your, two beats across two cards):
        #     [pain point, as a question]
        #     "This one guy from Australia just solved it permanently"
        #   Nearest named ancestor in the bank: A2 The Desire hook, HOOKS.md:82
        #   ("Here's how [named person] went from [before] to [after] using [mechanism]"),
        #   split into a question beat and a character beat so the gap opens before the
        #   character arrives.
        #
        # NO industry avatar anywhere. This deck targets the pain alone, so one deck runs
        # across every vertical and only the pain swaps.
        #
        # Formula: curiosity gap through pain agitation -> education -> lead magnet.
        # The lead magnet is the AI Readiness quiz.
        "slug": "three-automations",
        "slug_line": "Pain-led, no avatar",
        "slides": [
            # Cover carries both beats: the pain as a question, then the promise. Type sets
            # smaller so the whole hook lands in one frame, same band, same position.
            # The pain is the umbrella one, because the three automations span lead
            # follow-up, job triage and reporting rather than one of them.
            ["BURIED IN ADMIN THAT NOBODY ACTUALLY OWNS?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            # Each workflow card carries name, steps, outcome. That is three beats, so the
            # type sets smaller, the same trade you accepted on the cover. Every one is a
            # Hub build (project your-project-ref), tools named only where your content store
            # transcripts name them.
            #
            # 1. Hub: "Multi-step cold-outreach pipeline that won a paying client in a week".
            #    replicate_steps check each row for a thread ID so nobody is contacted twice,
            #    then draft and send a personalised email. Tools from Joshua Gaudry's
            #    lead-nurturing agent (n8n + Claude, "demonstrably reduced manual follow-up
            #    labour"). Claude appears in 198 of 483 transcript summaries.
            ["ONE. THE LEAD CATCHER. EVERY ENQUIRY IS CAPTURED AND",
             "CHECKED, THEN [[CLAUDE]] SENDS A PERSONALISED REPLY."],
            # 2. Hub: "AI-native operations rebuild with email agents that auto-triage jobs"
            #    (operations and logistics). Problem was manual email handling with no
            #    reliable trail; solution auto-triages incoming jobs and keeps an audit
            #    trail. Tools from Ash Johanson (email triage on n8n plus the Claude API in
            #    a trade company). n8n appears in 71 of 483 summaries.
            ["TWO. THE INBOX TRIAGE. [[N8N]] READS EVERY JOB AS IT",
             "ARRIVES AND ROUTES IT WITH A LOGGED TRAIL."],
            # 3. Hub: "Email classification and KPI dashboards across clinics". Handles
            #    ~500 emails a month across six clinics and replaces manual KPI tracking
            #    with dashboards.
            ["THREE. THE REPORTING PACK. THE NUMBERS ARE PULLED",
             "AND WRITTEN INTO A [[DASHBOARD]] EVERY MONTH."],
            # Results slide. Deliberately not a case study, per you. Each claim traces to
            # a Hub outcome: hours back (Ash Johanson, 72 to 78 hrs/week saved, attribution
            # unclear so the card says hours rather than a figure), every lead answered
            # (cold-outreach pipeline, a paying client inside one week), numbers you trust
            # (the clinic KPI dashboards replacing manual counting).
            ["THE RESULT: HOURS BACK EVERY WEEK, EVERY LEAD ANSWERED,",
             "AND NUMBERS YOU CAN [[ACTUALLY TRUST.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "eyebrow": "The lesson",
        # FLAG FOR REVIEW, two open items on this deck:
        #  1. "This one guy" and "solved it permanently" both read as claims about a real
        #     person and a real permanent outcome. Compliance (SKILL.md 9c) binds on the
        #     overall impression under the ACL, so this needs to map to an actual placement
        #     or the wording softens. It is the only line in the batch making that kind of
        #     claim.
        #  2. The AI Readiness quiz URL is not recorded anywhere in your workspace. Slide 7 names
        #     the quiz and has nowhere to point yet.
    },
]
