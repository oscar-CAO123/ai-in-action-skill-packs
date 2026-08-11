#!/usr/bin/env python3
"""The Build Breakdown decks (F5, industry-targeted, tool-named).

Five six-slide pain-arc decks, one per industry, written . They render on the
same rig as `decks_noir.py`: `plates_noir.py` falls through to `BUILD_DECKS` when a slug is
not in `NOIR_DECKS`.

    python3 plates_noir.py bb-construction --recomp     # free, band only
    python3 plates_noir.py bb-construction              # PAID, generates missing plates

WHAT IS DIFFERENT FROM THE 22 GENERAL-PAIN DECKS, AND WHY

The 22 decks in `decks_noir.py` are pain-led, audience-general and deliberately tool-free,
because SKILL.md section 1c bans vendor names on a teach slide: the Hub builds were
described by candidates in interviews and their stack is their intellectual property.

These five are industry-led and DO name tools, on your instruction of ("get
super specific at the tool level for each slide"). The IP firewall is kept by changing what
a name means rather than by dropping the rule:

  - A named tool here is the READER'S buildable stack, never a report of what a candidate
    used. No slide says who built it in what.
  - A tool may only be named if it clears the gate in
    `projects/content-engine/ideas/build-breakdown-carousels/PLAN.md` section 3: counted in
    five or more of the 153 candidate call summaries, or already named by that industry's
    own pain-wiki playbook. A rare stack fingerprints one candidate, so a rare stack is out.
  - The other four tells in section 1c still bind: no build-identifying counts, no
    candidate's named method, no sector-plus-scale pairing, nothing the record flags as the
    candidate's own edge.

Everything else is unchanged: the six-slide pain arc, the teach law (name, plain
definition, mechanics, and never the result), every figure held back to slide 5 at
one-business scope, one blue accent per slide, the bottom-band law and the your display typeface 200 noir
theme.

Each deck's three builds are the first three systems of the matching F8 carousel in
`ideas/industry-build-carousels/verticals/bb-<slug>.json`, so a reader who sees both is
taught the same thing twice rather than two unrelated things.
"""
from decks_noir import STYLE, LIGHT  # the noir-painterly phase 2 blocks, verbatim


def plate(scene):
    return f"{STYLE} {scene} {LIGHT}"


VOID = ("standing entirely alone in an empty black void with no floor and no walls, and the "
        "whole lower half of the frame empty solid black")

BLANK = [[], [], [], [], [], []]


BUILD_DECKS = [
    # ===================================================================================
    {
        "slug": "bb-construction",
        "slug_line": "Construction & Trades, the build breakdown",
        "board": None,
        "magnet": "The Site-to-Profit Readiness Check",
        "source": "F8 vertical bb-construction-and-trades. Hub cases 038, 109, 149. "
                  "Pain: construction playbook pain 1, 59 calls, the heaviest weighted "
                  "pain in the pack.",
        "slides": [
            ["TYPING THE SAME JOB INTO FOUR DIFFERENT SYSTEMS?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE ONE-JOB RECORD. ONE PLACE A JOB EXISTS, AND EVERYTHING",
             "ELSE READS IT. A WON QUOTE IN HUBSPOT STARTS AN N8N RUN THAT READS",
             "XERO AND PROCORE FIRST, LANDS ONE RECORD IN POSTGRES, AND SYNCS",
             "BACK OUT ONLY AFTER YOUR [[CONFIRMATION.]]"],
            ["TWO. THE TENDER ENGINE. THE TAKEOFF RUNS ITSELF AND YOU STILL SET",
             "THE PRICE. CLAUDE READS THE SCOPE AND THE DRAWINGS, EACH TAKEOFF",
             "IS ITS OWN RESUMABLE STEP, EVERY RATE COMES FROM YOUR LIBRARY,",
             "AND YOUR ESTIMATOR SIGNS THE [[NUMBER.]]"],
            ["THREE. THE STANDARDS DESK. THE SPEC ANSWERS ITSELF, WITH THE",
             "DRAWING. YOUR DOCUMENTS SIT IN SUPABASE AS VECTORS, A QUESTION",
             "FROM SITE SEARCHES THEM AND NEVER THE INTERNET, AND EVERY ANSWER",
             "IS [[LOGGED]] AGAINST THE JOB."],
            ["THE RESULT, ONE BUSINESS EACH: A FULL OPERATING SYSTEM ROLLED OUT",
             "IN EIGHT WEEKS, ABOUT TEN TIMES THE TENDER THROUGHPUT, AND FIFTY",
             "FOUR THOUSAND STANDARDS DOCUMENTS MADE [[ANSWERABLE.]]"],
            ["TAKE THE SITE-TO-PROFIT READINESS CHECK AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": BLANK,
        "plates": [
            plate(f"Wide shot of four separate filing cabinets arranged in a row, each one "
                  f"with its drawers half open and the same glowing white job docket "
                  f"duplicated inside every one of them, {VOID}."),
            plate(f"Medium shot of a single heavy steel spine running vertically through the "
                  f"frame with one glowing white docket clamped at its centre and four thin "
                  f"pneumatic tubes branching away from it into the dark, {VOID}."),
            plate(f"Medium shot of a tall mechanical press with a thick roll of drawings "
                  f"feeding through it and a single glowing white priced schedule emerging "
                  f"from the bottom, a faceless silhouette resting one hand on the lever, "
                  f"{VOID}."),
            plate(f"Wide shot of a wall of card-index drawers curving around a small "
                  f"lectern, one drawer sliding open on its own and a single glowing white "
                  f"card rising out of it toward the lectern, {VOID}."),
            plate(f"Wide shot of three machine stations lit together in a row, a spine, a "
                  f"press and an index wall, all connected by pneumatic tubes carrying "
                  f"glowing white parcels between them, {VOID}."),
            plate(f"Medium shot of a faceless silhouette in work clothes lowering a single "
                  f"glowing white core into a socket at the centre of a dark machine "
                  f"housing, {VOID}."),
        ],
    },
    # ===================================================================================
    {
        "slug": "bb-real-estate",
        "slug_line": "Real Estate & Property Management, the build breakdown",
        "board": None,
        "magnet": "The AI-Ready Agency Score",
        "source": "F8 vertical bb-real-estate-and-property-management. Hub cases 070, 059, "
                  "040. Pain: real estate playbook pain 2, raised in 26 of 27 calls.",
        "slides": [
            ["IS YOUR AGENCY PAYING SIX FIGURES A YEAR FOR A TECH STACK",
             "THAT STILL DOES NOT TALK TO ITSELF? YOU NEED THESE",
             "[[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE RENT ROLL SPINE. ONE PROPERTY RECORD THAT EVERY SYSTEM",
             "READS. A CHANGE IN PROPERTYME STARTS A RUN THAT READS AGENTBOX AND",
             "THE TRUST FILE, STRIPS THE NAMES BEFORE A MODEL SEES THEM, AND",
             "DRIVES WHATEVER HAS NO API THROUGH [[PLAYWRIGHT.]]"],
            ["TWO. THE FOLLOW-UP DESK. NOBODY WHO WALKED THROUGH GOES UNCALLED.",
             "THE ATTENDEE LIST LEAVES THE OPEN HOME, TWILIO MESSAGES INSIDE THE",
             "HOUR, EVERY REPLY IS MATCHED TO LIVE STOCK AND RANKED, AND YOUR",
             "AGENT WORKS THE [[TOP OF THE LIST.]]"],
            ["THREE. THE INSPECTION READ. THE ROUTINE INSPECTION WRITES ITSELF.",
             "THE TENANT UPLOADS THE PHOTOS, A VISION MODEL READS EACH ROOM",
             "AGAINST LAST QUARTER'S, ANYTHING UNCERTAIN IS FLAGGED RATHER THAN",
             "GUESSED, AND YOUR MANAGER [[SIGNS]] IT."],
            ["THE RESULT, ONE BUSINESS EACH: A HUNDRED AND FIFTY THOUSAND A",
             "YEAR OF FRAGMENTED STACK, FOUR HUNDRED HOURS A MONTH HANDED BACK",
             "ACROSS TWO AGENCIES, AND SIXTY TO SEVENTY PERCENT OF THE ADMIN",
             "[[GONE.]]"],
            ["TAKE THE AI-READY AGENCY SCORE AND SEE",
             "WHERE [[YOUR AGENCY STANDS.]]"],
        ],
        "annotations": BLANK,
        "plates": [
            plate(f"Wide shot of a tall stack of mismatched machine housings balanced on "
                  f"top of one another, each one humming separately with no belt or tube "
                  f"joining any of them, {VOID}."),
            plate(f"Medium shot of a single vertical spine with a glowing white property "
                  f"docket clamped at its centre, a small sealed vault at its base and four "
                  f"tubes branching away into the dark, {VOID}."),
            plate(f"Medium shot of a rotating carousel of glowing white cards, a mechanical "
                  f"arm lifting the topmost card clear while the rest continue to turn "
                  f"below it, {VOID}."),
            plate(f"Medium shot of a wide lens barrel mounted on a stand looking down at a "
                  f"small glowing white floor plan, a faceless silhouette standing beside "
                  f"it with one hand raised to a lever, {VOID}."),
            plate(f"Wide shot of a spine, a carousel and a lens barrel all lit together and "
                  f"joined by pneumatic tubes carrying glowing white parcels between them, "
                  f"{VOID}."),
            plate(f"Medium shot of a faceless silhouette lowering a single glowing white "
                  f"core into a socket at the centre of a dark machine housing, {VOID}."),
        ],
    },
    # ===================================================================================
    {
        "slug": "bb-retail",
        "slug_line": "Retail & E-commerce, the build breakdown",
        "board": None,
        "magnet": "The Retail Ops AI Readiness Check",
        "source": "F8 vertical bb-retail-and-ecommerce. Hub cases 046, 067, 073. Pain: "
                  "retail playbook pain 1, raised in 25 examples across the calls.",
        "slides": [
            ["IS YOUR TEAM THE GLUE HOLDING SIX DIFFERENT SYSTEMS TOGETHER,",
             "RE-KEYING THE SAME ORDER INTO EVERY ONE OF THEM?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE ORDER SPINE. THE ORDER MOVES AND NOBODY RE-KEYS IT. AN",
             "ORDER IN SHOPIFY STARTS AN N8N RUN THAT READS STOCK, THE WAREHOUSE",
             "AND XERO AT ONCE, LANDS ONE RECORD IN POSTGRES, BUYS THE LABEL,",
             "AND SENDS ONLY THE [[EXCEPTIONS]] TO A PERSON."],
            ["TWO. THE SUPPORT HUB. HALF THE QUEUE NEVER REACHES A HUMAN. EVERY",
             "MESSAGE IS READ AGAINST THAT CUSTOMER'S ORDER HISTORY FIRST,",
             "ROUTINE QUESTIONS RESOLVE OUTRIGHT, AND ANYTHING TOUCHING MONEY",
             "GOES STRAIGHT TO [[YOUR TEAM.]]"],
            ["THREE. THE BUYING RUN. YOU APPROVE THE BUY AND IT DOES THE BUYING.",
             "IT REORDERS OFF SELL-THROUGH RATHER THAN OFF A STOCK LEVEL, DRAFTS",
             "EACH ORDER AGAINST THAT SUPPLIER'S TERMS, AND PUTS THE LANDED COST",
             "INTO XERO THE [[SAME DAY.]]"],
            ["THE RESULT, ONE BUSINESS EACH: SIXTEEN HOURS A WEEK OF STAFF TIME",
             "DOWN TO SIXTEEN HOURS A MONTH, FIFTY THREE PERCENT OF A SUPPORT",
             "WORKLOAD AUTOMATED, AND FOUR HUNDRED AND FIFTY HOURS A MONTH",
             "[[SAVED.]]"],
            ["TAKE THE RETAIL OPS AI READINESS CHECK AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": BLANK,
        "plates": [
            plate(f"Wide shot of a broken conveyor line with a gap in the middle, a faceless "
                  f"silhouette standing in the gap lifting a glowing white parcel from one "
                  f"belt across to the next by hand, {VOID}."),
            plate(f"Medium shot of a single unbroken conveyor spine running the width of the "
                  f"frame, one glowing white parcel travelling along it and three sealed "
                  f"chutes feeding into it from above, {VOID}."),
            plate(f"Medium shot of a sorting machine with a wide funnel mouth, dozens of "
                  f"glowing white envelopes pouring in and a single one dropping out of a "
                  f"side chute into a tray, {VOID}."),
            plate(f"Medium shot of a tall shelving rig with one empty slot, a mechanical arm "
                  f"lowering a glowing white carton into the gap, {VOID}."),
            plate(f"Wide shot of a conveyor spine, a sorting funnel and a shelving rig all "
                  f"lit together and joined by pneumatic tubes carrying glowing white "
                  f"parcels between them, {VOID}."),
            plate(f"Medium shot of a faceless silhouette lowering a single glowing white "
                  f"core into a socket at the centre of a dark machine housing, {VOID}."),
        ],
    },
    # ===================================================================================
    {
        "slug": "bb-finance",
        "slug_line": "Financial Services & Insurance, the build breakdown",
        "board": None,
        "magnet": "The Broker and Adviser AI Readiness Check",
        "source": "F8 vertical bb-financial-services-and-insurance. Hub cases 002, 026, "
                  "129. Pain: financial services playbook pain 1, 19 pain examples, the "
                  "highest weighted category at 41%.",
        "slides": [
            ["DO YOUR CLIENTS HAVE TO REPEAT THEMSELVES EVERY TIME?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE CONTEXT HANDOVER. THE BRIEF SAYS IT ONCE AND EVERYONE",
             "HAS IT. WHISPER TRANSCRIBES THE CALL AS IT ENDS, THE FILE NOTE",
             "WRITES ITSELF IN YOUR FORMAT, AND EVERY CALL, TEXT AND EMAIL LANDS",
             "ON ONE CLIENT [[TIMELINE.]]"],
            ["TWO. THE FACT-FIND READER. WEEKS OF FACT-FINDING DONE IN DAYS.",
             "EVERY PAGE IS READ INTO STRUCTURED FIELDS, DUPLICATE PAGES ARE",
             "COLLAPSED BEFORE ANY MODEL RUNS, FIGURES ARE CROSS-CHECKED, AND",
             "YOUR ADVISER READS ONLY THE [[EXCEPTIONS.]]"],
            ["THREE. THE COMPLIANCE TRAIL. THE TRAIL IS BUILT WHILE THE WORK",
             "HAPPENS. EVERYTHING RUNS INSIDE YOUR OWN NETWORK BOUNDARY, EVERY",
             "STEP WRITES A LOG LINE NOBODY CAN EDIT, AND A PERSON STILL SIGNS",
             "ANYTHING THAT [[COSTS MONEY.]]"],
            ["THE RESULT, ONE BUSINESS EACH: A MULTI-THOUSAND DOLLAR CRM",
             "SUBSCRIPTION RETIRED, FACT-FINDING CUT FROM THREE WEEKS TO DAYS,",
             "AND CLAIMS PROCESSING COST DOWN [[NINETY FIVE PERCENT.]]"],
            ["TAKE THE BROKER AND ADVISER AI READINESS CHECK AND SEE",
             "WHERE [[YOUR BOOK STANDS.]]"],
        ],
        "annotations": BLANK,
        "plates": [
            plate(f"Medium shot of three sealed pneumatic tubes ending abruptly in mid air "
                  f"with a gap between each one, a single glowing white parcel falling "
                  f"through the gap into the dark, {VOID}."),
            plate(f"Medium shot of one continuous glowing white ribbon running the width of "
                  f"the frame through three sealed reading heads mounted in a row, {VOID}."),
            plate(f"Medium shot of a heavy document press with a thick stack of pages "
                  f"feeding in at one end and a single thin glowing white sheet leaving at "
                  f"the other, {VOID}."),
            plate(f"Medium shot of a locked strongroom door standing alone with a narrow "
                  f"glowing white ledger tape spooling out through a slot at its base and "
                  f"pooling on the ground, {VOID}."),
            plate(f"Wide shot of a ribbon line, a document press and a strongroom door all "
                  f"lit together and joined by pneumatic tubes carrying glowing white "
                  f"parcels between them, {VOID}."),
            plate(f"Medium shot of a faceless silhouette lowering a single glowing white "
                  f"core into a socket at the centre of a dark machine housing, {VOID}."),
        ],
    },
    # ===================================================================================
    {
        "slug": "bb-health",
        "slug_line": "Health, Medical & Allied Health, the build breakdown",
        "board": None,
        "magnet": "The Practice Pulse Check",
        "source": "F8 vertical bb-health-medical-and-allied-health. Hub cases 033 and 062, "
                  "096, 143. Pain: health playbook pain 2, 5 calls in a THIN six-call pack, "
                  "so every figure on slide 5 is build-sourced and scoped to one business.",
        "slides": [
            ["IS YOUR CLINIC DATA SCATTERED ACROSS FIVE DIFFERENT TOOLS",
             "THAT NEVER TALK? YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE FRONT DESK. THE PHONE STOPS BEING THE THING YOU LOSE",
             "MONEY ON. A VOICE AGENT ANSWERS ON THE FIRST RING, READS THE REAL",
             "DIARY BEFORE IT OFFERS A TIME, WRITES THE BOOKING IN, AND HANDS",
             "ANYTHING CLINICAL TO A [[PERSON.]]"],
            ["TWO. THE NOTES PASS. THE NOTE IS WRITTEN BEFORE YOU STAND UP.",
             "WHISPER TRANSCRIBES THE CONSULT ON A MACHINE INSIDE THE CLINIC,",
             "THE NOTE IS STRUCTURED TO YOUR OWN TEMPLATE, AND THE PRACTITIONER",
             "[[SIGNS]] IT."],
            ["THREE. THE INBOX ROUTER. THE INBOX SORTS ITSELF, SITE BY SITE.",
             "EVERY MESSAGE IS CLASSIFIED BEFORE A HUMAN OPENS IT, EACH BRANCH",
             "RUNS ON ITS OWN SO ONE BREAK IS ONE BREAK, AND YOUR PRACTICE",
             "MANAGER CLEARS ONLY THE [[UNKNOWNS.]]"],
            ["THE RESULT, ONE BUSINESS EACH: MISSED CALLS ELIMINATED AND",
             "RECEPTION HEADCOUNT CUT, A FULL-TIME JOB COVERED BY ONE OPERATOR'S",
             "BUILDS, AND FIVE HUNDRED EMAILS A MONTH HANDLED ACROSS [[SIX",
             "CLINICS.]]"],
            ["TAKE THE PRACTICE PULSE CHECK AND SEE WHERE",
             "YOUR [[PRACTICE ACTUALLY STANDS.]]"],
        ],
        "annotations": BLANK,
        "plates": [
            plate(f"Wide shot of five small separate cabinets standing apart from one "
                  f"another, each holding one glowing white card behind glass with no "
                  f"connection between any of them, {VOID}."),
            plate(f"Medium shot of an old switchboard panel with a single cable already "
                  f"plugged into the first socket and a glowing white parcel travelling "
                  f"along it, no operator present, {VOID}."),
            plate(f"Medium shot of a sealed glass writing chamber with a pen suspended "
                  f"inside it, a single glowing white sheet resting under the nib, {VOID}."),
            plate(f"Medium shot of a sorting funnel with a wide mouth, glowing white "
                  f"envelopes pouring in and dividing cleanly into three separate chutes "
                  f"below, {VOID}."),
            plate(f"Wide shot of a switchboard, a writing chamber and a sorting funnel all "
                  f"lit together and joined by pneumatic tubes carrying glowing white "
                  f"parcels between them, {VOID}."),
            plate(f"Medium shot of a faceless silhouette lowering a single glowing white "
                  f"core into a socket at the centre of a dark machine housing, {VOID}."),
        ],
    },
]
