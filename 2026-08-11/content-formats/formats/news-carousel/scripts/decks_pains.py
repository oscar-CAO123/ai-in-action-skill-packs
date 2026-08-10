"""The "three automations" carousel, one deck per canonical pain point.

Same exact structure as `three-automations` in decks2.py, which the operator locked 2026-07-31:

    1  cover        [pain, as a question] + "YOU NEED THESE THREE AUTOMATIONS ASAP."
    2  automation 1 name, then what it does
    3  automation 2 name, then what it does
    4  automation 3 name, then what it does
    5  results      the primary results a business gets, no case study
    6  CTA          the AI Readiness quiz

**Every automation on every slide is a real published build in the Candidate Knowledge Hub**
(Supabase `aksmtvpubuinqhhmkzxd`, `builds` table, 170 published rows), per the evidence law in
`content-formats/SKILL.md` section 1. The build behind each slide is named in the comment above it,
with its recorded `outcome` where the slide leans on one. Nothing here is invented.

Named tools appear only where the CRM interview evidence names them
(`your_table.transcript_summary`, 483 rows: Claude 198, n8n 71, Supabase 37).

`plates` carries the Higgsfield prompt for each slide, consumed by plates.py.
"""

QUIZ = ["TAKE THE AI READINESS QUIZ AND SEE", "WHERE [[YOUR BUSINESS STANDS.]]"]

LOOK = ("Deep near-black navy palette, one restrained electric blue accent, shallow depth "
        "of field, real material texture, fine film grain, controlled lighting, precise and "
        "understated, semi-premium editorial photography. No people, no text, no lettering, "
        "no signage, no logos, no numbers. The lower third of the frame falls away into "
        "near black.")

QUIZ_PLATE = ("Macro photograph of an open laptop on a dark desk, screen glowing an even soft "
              "blue with no readable content, inviting and calm, a notebook and pen resting "
              "beside it. " + LOOK)


PAIN_DECKS = [
    {
        "slug": "pain-admin",
        "slug_line": "Back-office admin",
        # 1 "AI receipt-reader with a multi-pipeline architecture": classifies each image by
        #   type, multi-stage cloud pipeline. outcome "Reduced 5-15 minute manual tasks to
        #   seconds."
        # 2 "OCR invoice-validation for a solar company": OCR invoices into structured fields,
        #   validate against expected rates, flag and route discrepancies. outcome "Prevented
        #   ~$35K+ in invoice fraud."
        # 3 "Medical payroll automation from hours to seconds": read source data read-only,
        #   encode payroll rules in code, emit a daily economics report. outcome "Payroll
        #   reduced from 6-7 hours to ~10 seconds."
        "slides": [
            ["STILL DOING THE BOOKS AFTER EVERYONE HAS GONE HOME?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE RECEIPT READER. EVERY RECEIPT IS SNAPPED,",
             "[[CLASSIFIED]] AND CODED BEFORE IT REACHES YOU."],
            ["TWO. THE INVOICE CHECK. EVERY BILL IS READ AND",
             "[[VALIDATED]] AGAINST THE RATE YOU AGREED."],
            ["THREE. THE PAYROLL RUN. THE HOURS ARE GATHERED",
             "AND EVERY RULE APPLIED IN [[SECONDS.]]"],
            ["THE RESULT: FIFTEEN MINUTE JOBS DONE IN SECONDS,",
             "OVERBILLING CAUGHT, AND [[YOUR NIGHTS BACK.]]"],
            QUIZ,
        ],
        "plates": [
            "A small Australian business back office late in the evening, a dense stack of "
            "paper invoices and dockets on a dark timber desk lit by an off-frame monitor "
            "glow. " + LOOK,
            "Extreme macro of a crumpled paper receipt lying on dark timber, one edge catching "
            "a thin line of blue light, the rest in deep shadow. " + LOOK,
            "Macro of a printed invoice on matte paper at an oblique angle on a dark desk, a "
            "narrow blue edge light raking across the paper grain, nothing readable. " + LOOK,
            "Macro of an old mechanical time clock and punch cards in a dark room, brushed "
            "metal catching a cool blue rim light. " + LOOK,
            "A tidy empty desk in an Australian office at the end of the day, chair pushed in, "
            "monitor dark, one shaft of late blue evening light across clean timber. " + LOOK,
            QUIZ_PLATE,
        ],
    },
    {
        "slug": "pain-inbox",
        "slug_line": "Inbox and customer service volume",
        # 1 "Multi-stage email classification and routing across a multi-site operation":
        #   map every email type, first-pass classifier then specialised classifiers, route to
        #   a dedicated sub-flow. outcome eleven-way routing at high monthly volume.
        # 2 "AI-native operations rebuild with email agents that auto-triage jobs": email
        #   agents triage incoming jobs and maintain an audit trail.
        # 3 "CX automation hub that absorbed half a support team's workload". outcome
        #   "Automated 53% of team workload (~181 hours/week); enabled 4.7x volume with no
        #   headcount growth."
        "slides": [
            ["DROWNING IN AN INBOX NOBODY CAN KEEP UP WITH?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE CLASSIFIER. EVERY MESSAGE IS READ AND",
             "SORTED INTO THE [[RIGHT QUEUE]] ON ARRIVAL."],
            ["TWO. THE TRIAGE AGENT. EACH JOB IS ROUTED",
             "STRAIGHT TO ITS OWNER, WITH AN [[AUDIT TRAIL.]]"],
            ["THREE. THE SUPPORT HUB. THE REPEAT QUESTIONS ARE",
             "ANSWERED WITHOUT [[ANYONE TOUCHING THEM.]]"],
            ["THE RESULT: HALF THE WORKLOAD ABSORBED, VOLUME UP",
             "SEVERALFOLD, AND [[NO NEW HIRES.]]"],
            QUIZ,
        ],
        "plates": [
            "A dark office at night, a single monitor glowing cool blue with an out-of-focus "
            "wall of message rows, no readable text, seen past the silhouette of a desk "
            "lamp. " + LOOK,
            "Macro of a wall of brass post-office pigeonholes in a dark room, one compartment "
            "lit from within by soft blue light. " + LOOK,
            "Macro of a stack of metal office filing trays in a dark room, papers sorted into "
            "each tier, a narrow band of blue light picking out one tray. " + LOOK,
            "Macro of a switchboard patch panel in a dark room, neat rows of cables, one "
            "connector glowing a restrained electric blue. " + LOOK,
            "A calm empty customer service desk at end of day, headset resting on the timber, "
            "screens dark, low blue evening light. " + LOOK,
            QUIZ_PLATE,
        ],
    },
    {
        "slug": "pain-quoting",
        "slug_line": "Quoting and estimating",
        # 1 "Sales agent with auto-quoting that cut speed-to-lead from days to minutes":
        #   map the lead-to-quote workflow, define the metric, auto-qualify inbound leads.
        #   outcome "Speed-to-lead reduced from ~4 days to ~5 minutes."
        # 2 "Engineering-quoting and proposal automation for construction": automate the
        #   deterministic calculations first, then generate quotes and proposals.
        # 3 "Agentic infrastructure for construction tendering". outcome "~10x tender
        #   throughput; quote-conversion uplift."
        "slides": [
            ["LOSING JOBS BECAUSE THE QUOTE TAKES A WEEK?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE QUALIFIER. EVERY ENQUIRY IS SCORED AND",
             "[[PRICED]] THE SAME DAY IT LANDS."],
            ["TWO. THE CALCULATION ENGINE. THE SUMS RUN WITHOUT",
             "ANYONE OPENING A [[SPREADSHEET.]]"],
            ["THREE. THE PROPOSAL BUILDER. EVERY QUOTE BECOMES",
             "A FINISHED [[PROPOSAL]] WITHOUT ANYBODY TYPING."],
            ["THE RESULT: SPEED TO LEAD FROM DAYS TO MINUTES,",
             "AND [[TEN TIMES]] THE TENDERS OUT THE DOOR."],
            QUIZ,
        ],
        "plates": [
            "A dark site office at dusk, rolled construction drawings and a tape measure on a "
            "timber bench, one cool blue light falling across the paper. " + LOOK,
            "Macro of a desk calendar and a pen on dark timber, one day marked, a thin blue "
            "edge light across the page, nothing readable. " + LOOK,
            "Extreme macro of an old mechanical calculator's keys in a dark room, worn metal "
            "and plastic, a restrained blue rim light. " + LOOK,
            "Macro of a crisp bound document on a dark desk, corner lifted, clean paper edges "
            "catching a narrow blue light, nothing readable. " + LOOK,
            "A tidy site office desk at the end of the day, drawings rolled and stacked "
            "neatly, hard hat resting beside them, low blue evening light. " + LOOK,
            QUIZ_PLATE,
        ],
    },
    {
        "slug": "pain-leads",
        "slug_line": "Leads leaking",
        # 1 "Multi-step cold-outreach pipeline that won a paying client in a week": daily
        #   scrape with dedup, the automation reads row by row and checks for a thread ID so
        #   nobody is contacted twice, then drafts and sends a personalised email.
        #   outcome "Produced a paying client within one week of deployment."
        # 2 "Agentic lead-qualification system that doubled event sales."
        # 3 "Cross-office scheduling and outreach automation": scheduling across locations
        #   plus email drip sequences.
        # Tools: Joshua Gaudry's lead-nurturing agent (n8n + Claude), Alana Meany's
        # lead-generation workflows (n8n). Claude 198 / n8n 71 of 483 summaries.
        "slides": [
            ["LEADS GOING COLD BEFORE ANYONE CALLS THEM BACK?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE LEAD CATCHER. EVERY ENQUIRY IS CAPTURED AND",
             "CHECKED, THEN [[CLAUDE]] SENDS A PERSONALISED REPLY."],
            ["TWO. THE QUALIFIER. EVERY ENQUIRY IS SCORED SO",
             "YOUR TEAM CALLS THE [[RIGHT ONES FIRST.]]"],
            ["THREE. THE FOLLOW UP. THE SEQUENCE RUNS ITSELF",
             "AND NOBODY EVER GETS [[CONTACTED TWICE.]]"],
            ["THE RESULT: EVERY LEAD ANSWERED IN MINUTES, AND",
             "[[NOTHING SITTING UNREAD.]]"],
            QUIZ,
        ],
        "plates": [
            "A dark office at night, a desk phone off to one side, an unopened notebook, one "
            "cold blue screen glow from off frame across empty timber. " + LOOK,
            "Macro of a phone lying face up on dark timber beside a closed laptop, its screen "
            "throwing a single soft blue notification glow across the grain. " + LOOK,
            "Macro of a row of index cards standing in a dark wooden card file, one card "
            "raised slightly and lit by a narrow blue beam. " + LOOK,
            "Macro of a line of dominoes standing on dark timber, receding into shadow, a thin "
            "blue rim light along their edges. " + LOOK,
            "A calm tidy desk at end of day, phone face down, laptop closed, one shaft of late "
            "blue evening light across clean timber. " + LOOK,
            QUIZ_PLATE,
        ],
    },
    {
        "slug": "pain-numbers",
        "slug_line": "Nobody trusts the numbers",
        # 1 "Medical-practice payroll automation": extract billing data from multiple sources
        #   weekly, with read-only data principles for the medical data.
        # 2 "Email classification and KPI dashboards across clinics": replaces manual KPI
        #   tracking with dashboards, "30+ KPIs" from two automated report downloads.
        # 3 "Adaptive AI platform that turns a quarterly board-pack process into one click",
        #   with full provenance and attestation on every output. outcome "Quarterly board-pack
        #   assembly cut from ~2.5 weeks to a button-click."
        "slides": [
            ["CANNOT TRUST A SINGLE NUMBER YOUR BUSINESS PRODUCES?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE DATA PULL. EVERY SOURCE IS READ ON A SCHEDULE,",
             "AND NOTHING IS EVER [[WRITTEN BACK TO IT.]]"],
            ["TWO. THE KPI PACK. THE MEASURES ARE CALCULATED",
             "THE SAME WAY [[EVERY SINGLE MONTH.]]"],
            ["THREE. THE BOARD PACK. THE WHOLE THING ASSEMBLES",
             "ON A [[BUTTON CLICK.]]"],
            ["THE RESULT: A BOARD PACK IN MINUTES INSTEAD OF",
             "WEEKS, AND [[NUMBERS THAT AGREE.]]"],
            QUIZ,
        ],
        "plates": [
            "A dark boardroom at night, a long empty timber table, scattered printed reports "
            "with corners curling, one cool blue light from a window. " + LOOK,
            "Extreme macro of a brass water tap over dark stone, a single drop catching blue "
            "light, everything else in shadow. " + LOOK,
            "Tight macro of a printed bar chart on matte paper on dark timber, the bars "
            "catching a thin edge of blue light, shot obliquely so nothing is readable. "
            + LOOK,
            "Macro of a neatly bound report on a dark table, crisp edges, a narrow blue light "
            "along the spine, nothing readable. " + LOOK,
            "A clean boardroom table at dusk, one closed folder squared to the edge, chairs "
            "tucked in, low blue evening light. " + LOOK,
            QUIZ_PLATE,
        ],
    },
    {
        "slug": "pain-margin",
        "slug_line": "Margin bleeding",
        # 1 "OCR invoice-validation for a solar company": validates invoices against expected
        #   values, catching overbilling. outcome "Prevented ~$35K+ in invoice fraud."
        # 2 "Document-intelligence platform that cut fact-finding from weeks to days": OCR and
        #   extraction with deduplication to slash processing cost. outcome "Fact-finding cut
        #   from 2-3 weeks to days; ~98% token-cost saving via deduplication."
        # 3 "AI-assisted schedule analysis that surfaced large cost savings": frontier models
        #   analyse complex project schedules for risk and waste.
        "slides": [
            ["MARGIN LEAKING SOMEWHERE AND NOBODY CAN FIND WHERE?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE INVOICE CHECK. EVERY SINGLE BILL IS READ",
             "AND MATCHED TO THE [[RATE YOU ACTUALLY AGREED.]]"],
            ["TWO. THE DOCUMENT SWEEP. THE PAPERWORK IS PULLED",
             "APART AND [[DEDUPLICATED]] BEFORE ANYONE READS IT."],
            ["THREE. THE SCHEDULE REVIEW. THE PROGRAMME IS",
             "ANALYSED FOR [[RISK AND WASTE]] EVERY WEEK."],
            ["THE RESULT: OVERBILLING CAUGHT, WEEKS OF FACT",
             "FINDING CUT TO DAYS, AND [[COSTS DOWN.]]"],
            QUIZ,
        ],
        "plates": [
            "Extreme macro of a hairline crack running through dark polished stone, a thin "
            "line of blue light caught in the fracture. " + LOOK,
            "Macro of a printed invoice on matte paper at an oblique angle on dark timber, a "
            "narrow blue edge light raking across the grain, nothing readable. " + LOOK,
            "Macro of a thick stack of paper documents seen edge on in a dark room, the layers "
            "razor sharp, a thin blue light along the top edge. " + LOOK,
            "Macro of a wall-mounted project schedule board in a dark room, a grid of blank "
            "cards and pins, one card catching restrained blue light. " + LOOK,
            "A clean dark desk with a single closed ledger squared to the edge, low blue "
            "evening light, everything in order. " + LOOK,
            QUIZ_PLATE,
        ],
    },
    {
        "slug": "pain-headcount",
        "slug_line": "Growth capped by headcount",
        # 1 "CX automation hub that absorbed half a support team's workload". outcome
        #   "Automated 53% of team workload (~181 hours/week); enabled 4.7x volume with no
        #   headcount growth."
        # 2 "Council email-routing automation that freed several full-time roles" (local
        #   government).
        # 3 "Multi-LLM 'council' sales system that eliminated three roles". outcome
        #   "Eliminated 3 FTE roles; generates ~50 appointments/day."
        "slides": [
            ["BOOKED OUT AND STILL CANNOT HIRE FAST ENOUGH?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE SUPPORT HUB. THE REPEAT WORK IS ABSORBED",
             "BEFORE IT REACHES [[ANYBODY'S DESK.]]"],
            ["TWO. THE ROUTING LAYER. EVERY REQUEST FINDS ITS",
             "OWNER WITHOUT A [[COORDINATOR.]]"],
            ["THREE. THE SALES COUNCIL. QUALIFYING AND BOOKING",
             "RUNS WITHOUT [[THREE SEPARATE ROLES.]]"],
            ["THE RESULT: VOLUME UP NEARLY FIVE TIMES ON THE SAME",
             "TEAM, AND WHOLE [[ROLES FREED UP AGAIN.]]"],
            QUIZ,
        ],
        "plates": [
            "A dark open plan office at night, rows of empty desks receding into shadow, one "
            "cool blue light over the nearest chair. " + LOOK,
            "Macro of a conveyor belt of plain cardboard parcels in a dark warehouse, a "
            "restrained blue light raking across the tops. " + LOOK,
            "Macro of a brass railway points lever in a dark room, polished metal, a narrow "
            "blue rim light along the shaft. " + LOOK,
            "Macro of three empty chairs in a dark room seen in a row, upholstery texture "
            "sharp, a thin blue light across the nearest backrest. " + LOOK,
            "A calm open plan office at dusk, desks clear, monitors dark, one long shaft of "
            "blue evening light down the aisle. " + LOOK,
            QUIZ_PLATE,
        ],
    },
    {
        "slug": "pain-systems",
        "slug_line": "Disconnected systems",
        # 1 "Full AI operating-system rollout using a shadow system and read-only warehouse"
        #   (construction): a read-only data warehouse so the AI never mutates source systems.
        #   outcome "A full operating-system rollout for a construction company delivered in
        #   ~8 weeks."
        # 2 "Computer-use automation for a third-party system with no API": the agent drives
        #   the UI like a human because the target system offers no API access.
        # 3 "Custom CRM with event automation for a VC portfolio": a scheduled task each
        #   morning pulls data and enriches profiles from communication history.
        "slides": [
            ["TYPING THE SAME JOB INTO FOUR DIFFERENT SYSTEMS?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE SHADOW WAREHOUSE. EVERY SYSTEM IS READ INTO",
             "ONE PLACE AND [[NEVER WRITTEN BACK.]]"],
            ["TWO. THE COMPUTER USE AGENT. THE SYSTEM WITH NO",
             "API GETS [[DRIVEN LIKE A HUMAN.]]"],
            ["THREE. THE MORNING SYNC. EVERY JOB RECORD UPDATES",
             "ITSELF [[EVERYWHERE]] ON A SCHEDULE."],
            ["THE RESULT: ONE SOURCE OF TRUTH, NO RE-ENTERING,",
             "AND A ROLLOUT IN [[ABOUT EIGHT WEEKS.]]"],
            QUIZ,
        ],
        "plates": [
            "Macro of four identical old keyboards stacked on a dark bench in a dim room, worn "
            "keys, a thin blue light raking across them. " + LOOK,
            "Macro of a single brass key lying on dark stone, one narrow blue light along its "
            "edge, deep shadow around it. " + LOOK,
            "Macro of an old computer mouse on dark timber lit by a cool blue screen glow from "
            "off frame, cable curling into shadow. " + LOOK,
            "Macro of interlocking brass clock gears in a dark room, teeth meshing precisely, "
            "a restrained blue rim light. " + LOOK,
            "A single clean monitor on an otherwise empty dark desk, screen dark, one shaft of "
            "blue evening light across the timber. " + LOOK,
            QUIZ_PLATE,
        ],
    },
]
