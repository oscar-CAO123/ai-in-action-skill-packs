#!/usr/bin/env python3
"""The B&W noir-painterly carousel line: painted machine plates under a quiet your display typeface band.

Locked with the operator 2026-08-01, replacing the photoreal stock plates on the pain decks:

  - Plates are fully generated stills in the locked noir-painterly house style (F2),
    black and white, no colour anywhere in the frame.
  - Nothing is baked into the plate. Every plate comes back wordless, so the STYLE and
    LIGHT blocks carry an explicit no-lettering clause and the de-text pass is the fallback.
  - The painted scenes come straight from that pain's noir VSL board, so one plate serves
    the carousel and the film. Slide 1 is the board's opening motif, slides 2 to 4 are its
    three teach beats, slide 5 its solution wide, slide 6 its glowing core.
  - Annotations are your display typeface labels on hairline leaders, composited over the raw plate as SVG
    in `plates_noir.py`. They name the station, using the board's own station names.
  - The band is thin your display typeface as of 2026-08-06: the `noir` theme in `band.py`, your display typeface weight 200,
    all caps, justified, one blue accent, the bottom-band law exactly as `decks_pains.py`
    sets it. Weight 200 is the locked design system's display weight. Anton is retired here.
    Only the face changed; the geometry, caps, justification and accent are untouched. The
    sentence-case your display typeface 500 band tried on 2026-08-01 was a different thing and stays rejected.

Copy is the approved deck copy from `decks_pains.py`, verbatim.
"""

# The STYLE and LIGHT blocks from noir-painterly/SKILL.md phase 2, verbatim, with two
# documented overrides:
#   1. The LIGHT block's final clause hard-codes "wide 16:9". These plates are 5:4 to fill
#      the 1080x844 area above the band. Finding U1 in the VSL review is the standing
#      request to give the skill a proper per-aspect variant instead of an override here.
#   2. An explicit no-lettering clause, because the operator ruled the plates stay raw and
#      wordless and Nano Banana bakes gibberish signage unless told not to.
STYLE = ("A moody black-and-white oil painting in high-contrast film-noir style, thick "
         "visible brushstrokes, painterly chiaroscuro, hand-painted animation still, not a "
         "photograph. Any human figure is a neutral faceless silhouette with no face, no "
         "hat, no gender cues.")

LIGHT = ("A single hard key light rakes from high on one side, catching the glowing white "
         "work and the edges of the machinery with brilliant specular highlights while the "
         "rest falls into deep crushed black. Inky tenebrist shadows, luminous white to "
         "solid black, thick oil-paint texture, vintage noir cinema mood. Subject centred "
         "in the frame with balanced negative space, symmetrical composition, 5:4. Purely "
         "black and white with no colour of any kind. The lower quarter of the frame falls "
         "away into solid black. Absolutely no text, no lettering, no signage, no labels, "
         "no logos and no numbers anywhere in the image. The painted scene bleeds to all four "
         "edges and fills the frame completely: this is the artwork itself, never a "
         "photograph of a canvas, so there is no canvas edge, no border, no mount, no frame "
         "and no wall or surface behind or around it anywhere.")


def plate(scene):
    return f"{STYLE} {scene} {LIGHT}"


NOIR_DECKS = [
    {
        "slug": "noir-pain-admin",
        "slug_line": "Back-office admin",
        "board": "noir-vsl-admin",
        # Slide -> board beat: 1->b1, 2->b5, 3->b6, 4->b7, 5->solution wide, 6->b8.
        "slides": [
            ["STILL DOING THE BOOKS AFTER EVERYONE HAS GONE HOME?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE RECEIPT READER. A VISION MODEL LIFTS THE FIELDS OFF EVERY",
             "RECEIPT, SEVERAL PIPELINES RUN SIDE BY SIDE SO ONE BAD SCAN CANNOT",
             "STOP THE LOT, AND THE CODED RESULT LANDS IN YOUR [[BOOKS]] BEFORE",
             "IT REACHES YOU."],
            ["TWO. THE INVOICE CHECK. EVERY BILL IS READ INTO STRUCTURED FIELDS,",
             "CHECKED LINE BY LINE AGAINST THE RATE YOU AGREED, AND ANYTHING",
             "THAT DOES NOT MATCH IS [[FLAGGED]] AND SENT TO A PERSON."],
            ["THREE. THE PAYROLL RUN. IT READS YOUR HOURS WITHOUT BEING ABLE TO",
             "CHANGE THEM, APPLIES EVERY PAY RULE AS CODE RATHER THAN FROM",
             "MEMORY, AND PRINTS THE [[DAILY]] BILLINGS REPORT ON THE WAY",
             "THROUGH."],
            ["THE RESULT, ONE BUSINESS EACH: HOUR LONG JOBS DONE IN SECONDS,",
             "THIRTY FIVE THOUSAND DOLLARS OF OVERBILLING CAUGHT, AND SIX HOURS",
             "OF PAYROLL DONE IN [[TEN SECONDS.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        # Annotations: (label, logo, dot_x, dot_y, anchor_x, anchor). Each renders as a
        # small white tool logo, the label beside it, and a hairline leader rising to the
        # painted object. `logo` resolves to
        # `museum-gallery-carousels/assets/logos/<name>.svg`, or None for no mark.
        # Coordinates are card space (1080x1350); the plate is y 0..844, band top 844.
        #
        # EVIDENCE: the admin board records no tool against its three Hub builds, so the
        # logos carry the counted stack from the CRM interviews (Claude 198, n8n 71 of 483)
        # rather than a per-build claim. Slide 1 is the pain, so it stays logo-free.
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a modest multi-room business sliced open like a dollhouse "
                  "standing in an empty black void, its rooms stacked and adjacent and "
                  "connected by conveyor belts and pneumatic tubes, every room unlit and "
                  "dark, and one small table lit outside the building where a lone faceless "
                  "silhouette bends over a tall stack of glowing white parcels of work."),
            plate("Medium shot inside the machine of a large painted lens on an armature "
                  "lowered over a conveyor belt, each glowing white parcel of work passing "
                  "underneath it, coming out stamped, and dropping into its own slot in a "
                  "tall rack of empty pigeonholes beside the belt."),
            plate("Close shot of two glowing white parcels of work resting on the pans of a "
                  "heavy iron beam balance, one pan hanging visibly lower than the other, "
                  "and the hand of a faceless silhouette lifting the heavier parcel clear "
                  "of the line and setting it aside."),
            plate("Medium shot of a tall bank of iron levers throwing themselves in "
                  "sequence with nobody standing at them, and behind them a wall of thin "
                  "cards feeding down through the mechanism and emerging at the bottom as "
                  "one clean sheet."),
            plate("Wide shot of three separate working stations inside the sliced-open "
                  "building lit together for the first time, their conveyor belts joining "
                  "into one continuous line, glowing white parcels of work running the "
                  "whole length of it, and no figure anywhere in the frame."),
            plate("Wide shot of a calm upright faceless silhouette kneeling at the centre "
                  "of the sliced-open building and seating a brilliant glowing core into "
                  "its housing, the light from the core re-threading every room of the "
                  "building from the inside, and the small table outside folded and dark."),
        ],
    },
    {
        "slug": "noir-pain-inbox",
        "slug_line": "Inbox and customer service volume",
        "board": "noir-vsl-inbox",
        "slides": [
            ["DROWNING IN AN INBOX NOBODY CAN KEEP UP WITH?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE CLASSIFIER. YOU MAP EVERY TYPE OF EMAIL AND WHERE IT",
             "SHOULD GO, A FIRST PASS SORTS THE ARRIVALS AND SPECIALISTS SORT",
             "THEM AGAIN, AND EACH BRANCH IS [[WALLED OFF]] SO ONE FAILURE",
             "CANNOT TAKE THE REST DOWN."],
            ["TWO. THE TRIAGE AGENT. IT SITS RIGHT AT THE INTAKE POINT, TURNS",
             "EACH INCOMING MESSAGE INTO A JOB ON THE BOARD, AND KEEPS AN",
             "[[AUDIT TRAIL]] THROUGH EVERY STEP IT TOUCHES."],
            ["THREE. THE SUPPORT HUB. YOU MEASURE WHERE THE SUPPORT HOURS",
             "ACTUALLY GO, HAND THE REPEATING MAJORITY TO A MODEL, AND MOVE YOUR",
             "PEOPLE ONTO THE [[VIP WORK]] THAT KEEPS CUSTOMERS."],
            ["THE RESULT, ONE BUSINESS EACH: FIVE HUNDRED EMAILS A MONTH SORTED",
             "AND ROUTED WITHOUT A PERSON, FIFTY THREE PERCENT OF A SUPPORT",
             "TEAM'S WORKLOAD ABSORBED, AND VOLUME UP [[NEARLY FIVE TIMES]] WITH",
             "NO NEW HIRES."],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a single faceless silhouette standing at the centre of a "
                  "sliced-open multi-room machine with far too many arms, each arm working a "
                  "different lever, and glowing white parcels of work arriving toward it from "
                  "every direction at once."),
            plate("Medium shot of a heavy sorting head lowered over a small landing at the "
                  "left of frame, each glowing white parcel of work read as it passes beneath "
                  "it and dropped down its own chute, the row of chutes fanning out to the "
                  "right across the frame."),
            plate("Medium shot of one glowing white parcel of work running along a single "
                  "unbroken track from the left of frame to one station at the right, with a "
                  "long printed paper tag paying out behind it and trailing back down the "
                  "track it came along."),
            plate("Medium shot of a closed hatch set into the flat face of the machine at the "
                  "centre of frame, a row of identical glowing white parcels of work turning "
                  "back at the hatch and returning the way they came, none of them passing "
                  "through into the rooms beyond."),
            plate("Wide shot of a sorting head, a single running track and a hatch in the "
                  "machine face, all three lit together for the first time across one "
                  "continuous machine floor, glowing white parcels of work moving through all "
                  "three, and no figure anywhere in the frame."),
            plate("Wide shot of a calm upright faceless silhouette seating a brilliant glowing "
                  "core into a housing at the centre of the sliced-open building, and beside "
                  "it the formerly many-armed figure now standing straight with only two arms "
                  "and its hands at rest."),
        ],
    },
    {
        "slug": "noir-pain-quoting",
        "slug_line": "Quoting and estimating",
        "board": "noir-vsl-quoting",
        "slides": [
            ["LOSING JOBS BECAUSE THE QUOTE TAKES A WEEK?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE QUALIFIER. YOU MAP THE PATH FROM ENQUIRY TO QUOTE WITH",
             "THE PEOPLE WHO WALK IT AND AGREE WHAT YOU ARE MEASURING FIRST,",
             "THEN AN AGENT SCORES EVERY ENQUIRY AND WRITES THE [[QUOTE]]",
             "WITHOUT WAITING."],
            ["TWO. THE CALCULATION ENGINE. THE SUMS THAT HAVE ONE RIGHT ANSWER",
             "ARE AUTOMATED FIRST, THE QUOTE AND THE PROPOSAL ARE BUILT FROM",
             "THOSE RESULTS, AND AN [[ENGINEER]] STILL SIGNS IT OFF."],
            ["THREE. THE PROPOSAL BUILDER. EACH TENDER WORKFLOW GETS A REUSABLE",
             "AGENT SETUP RUNNING ON AN ENGINE THAT SURVIVES A CRASH MID JOB,",
             "AND YOU CHOOSE WHETHER IT RUNS [[ON YOUR OWN SERVERS.]]"],
            ["THE RESULT, ONE BUSINESS EACH: A FOUR DAY REPLY TIME DOWN TO FIVE",
             "MINUTES, AND TENDER THROUGHPUT UP [[TEN TIMES.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a long line of glowing white parcels of work stalled nose to "
                  "tail at one station, a single faceless silhouette at that station measuring "
                  "one parcel by hand with a pair of callipers, and the rest of the line "
                  "stretching back into black behind it."),
            plate("Medium shot of a narrow gate standing at the head of a conveyor belt at the "
                  "left of frame, each arriving glowing white parcel of work weighed and "
                  "tagged as it passes through the gate and continues on to the right."),
            plate("Medium shot of a tall bank of iron gears turning by itself in the centre of "
                  "frame, doing the measuring work with nobody at it, and a pair of callipers "
                  "lying abandoned on the empty wooden bench beneath it."),
            plate("Medium shot of a heavy press at the end of a conveyor belt, stamping each "
                  "measured glowing white parcel of work into a bound sheet and setting it "
                  "down on an outbound belt that runs away to the right of frame, already "
                  "filling with finished sheets."),
            plate("Wide shot of a single faceless silhouette standing at a measuring bench "
                  "holding one glowing white parcel of work and studying it, while behind and "
                  "around it a continuous line of other parcels flows past on the belts "
                  "without stopping."),
            plate("Wide shot of a calm upright faceless silhouette seating a brilliant glowing "
                  "core into a housing at the centre of the sliced-open building, the light "
                  "re-threading every room, and one clean unbroken line running the full width "
                  "of the machine from end to end."),
        ],
    },
    {
        "slug": "noir-pain-leads",
        "slug_line": "Leads leaking",
        "board": "noir-vsl-leads",
        "slides": [
            ["LEADS GOING COLD BEFORE ANYONE CALLS THEM BACK?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE LEAD CATCHER. IT SCRAPES AND ENRICHES A TARGETED LIST,",
             "PASSES EACH PROSPECT THROUGH AN AGENT THAT WRITES TO THEM",
             "PERSONALLY, AND CHECKS FOR AN EXISTING THREAD SO NOBODY IS",
             "CONTACTED [[TWICE.]]"],
            ["TWO. THE QUALIFIER. A MANAGER AGENT HANDS EACH LEAD TO A WORKER",
             "AGENT, WITH GUARDRAILS AND A DEBUGGING AGENT BUILT IN FROM DAY",
             "ONE, AND THE FUNNEL IS [[INSTRUMENTED]] SO THE LIFT CAN BE PROVEN."],
            ["THREE. THE FOLLOW UP. SCHEDULING RUNS ACROSS EVERY OFFICE, THE",
             "DRIP SEQUENCE SENDS ITSELF, AND THE SIMPLE STEPS ARE GIVEN A",
             "[[CHEAPER MODEL]] SO THE WHOLE THING COSTS LITTLE TO LEAVE",
             "RUNNING."],
            ["THE RESULT, ONE BUSINESS EACH: A PAYING CLIENT WON WITHIN A WEEK",
             "OF GOING LIVE, SALES AT TRADE SHOW EVENTS [[DOUBLED]], AND",
             "SCHEDULING RUNNING ITSELF ACROSS EVERY OFFICE."],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Close shot of a single glowing white parcel of work running off the end of "
                  "a conveyor belt at the centre of frame and falling away into black beneath "
                  "it, its light going out on the way down, with nobody anywhere near it."),
            plate("Medium shot of a solid catcher plate closing the gap at the end of a "
                  "conveyor belt, each glowing white parcel of work caught on the plate, "
                  "marked, and set back onto the belt still brightly lit, running away to the "
                  "right of frame."),
            plate("Medium shot of a heavy iron beam balance standing at the head of a conveyor "
                  "belt at the centre of frame, the heavier glowing white parcels of work "
                  "being lifted off it onto a fast upper track that runs up and away to the "
                  "right of frame."),
            plate("Medium shot of a jointed clockwork arm above a conveyor belt, returning "
                  "toward the same glowing white parcel of work at set intervals, reading the "
                  "paper tag on the parcel, and drawing back without touching it."),
            plate("Wide shot of a catcher plate, a beam balance and a clockwork arm all lit "
                  "together for the first time along one continuous conveyor belt, every "
                  "glowing white parcel of work on it still brightly lit, and no figure "
                  "anywhere in the frame."),
            plate("Wide shot of a calm upright faceless silhouette seating a brilliant glowing "
                  "core into a housing at the centre of the sliced-open building, the light "
                  "re-threading every room, and the conveyor belt now running with no gap at "
                  "the end of it."),
        ],
    },
    {
        "slug": "noir-pain-numbers",
        "slug_line": "Nobody trusts the numbers",
        "board": "noir-vsl-numbers",
        "slides": [
            ["CANNOT TRUST A SINGLE NUMBER YOUR BUSINESS PRODUCES?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE DATA PULL. THE AUTOMATION IS GIVEN READ ONLY ACCESS SO IT",
             "CAN NEVER ALTER YOUR SOURCE, THE RULES ARE WRITTEN OUT EXPLICITLY",
             "RATHER THAN CARRIED IN SOMEBODY'S HEAD, AND A [[DAILY]] ECONOMICS",
             "REPORT COMES OUT THE END."],
            ["TWO. THE KPI PACK. EVERY INBOUND MESSAGE IS CLASSIFIED AND SENT TO",
             "THE SITE THAT OWNS IT, AND THE HAND KEPT TRACKING SHEET IS",
             "REPLACED BY [[DASHBOARDS]] THAT FILL THEMSELVES."],
            ["THREE. THE BOARD PACK. YOUR DATA IS MODELLED INTO ONE AGREED SHAPE",
             "FIRST, EVERY OUTPUT IS STAMPED SO ANY FIGURE TRACES BACK TO ITS",
             "SOURCE, AND THE HIGH STAKES NUMBERS ARE [[FIXED]] RATHER THAN",
             "GENERATED FRESH EACH TIME."],
            ["THE RESULT, ONE BUSINESS EACH: PAYROLL THAT USED TO BE MANUAL",
             "RUNNING ITSELF, FIVE HUNDRED EMAILS A MONTH SORTED ACROSS THE",
             "WHOLE GROUP, AND A TWO AND A HALF WEEK BOARD PACK DOWN TO [[ONE",
             "CLICK.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Close shot of two identical round pressure gauges mounted side by side on "
                  "the same pipe at the centre of frame, both lit by the same key light, their "
                  "needles resting at two clearly different positions on the dial."),
            plate("Medium shot of a bank of four heavy one-way valves fitted along four pipes "
                  "running across the frame, glowing white work flowing outward through them "
                  "toward the right, and nothing at all flowing back the other way."),
            plate("Medium shot of a single heavy measuring drum turning at a steady rate in "
                  "the centre of frame, stamping an identical mark onto every glowing white "
                  "parcel of work that passes beneath it, the stamped parcels filing away in "
                  "one long even row."),
            plate("Medium shot of a mechanism drawing a scatter of loose glowing white sheets "
                  "together and binding them into one finished pack in a single stroke, each "
                  "sheet still carrying a visible stamp of the room it came from."),
            plate("Wide shot of a valve bank, a measuring drum and a binding mechanism all lit "
                  "together across one machine floor, and one faceless silhouette at a board "
                  "table lifting a single bound pack and turning it toward the light."),
            plate("Wide shot of a calm upright faceless silhouette seating a brilliant glowing "
                  "core into a housing at the centre of the sliced-open building, and above it "
                  "a single round dial with one steady needle, fed by four pipes converging on "
                  "it from four rooms."),
        ],
    },
    {
        "slug": "noir-pain-margin",
        "slug_line": "Margin bleeding",
        "board": "noir-vsl-margin",
        "slides": [
            ["MARGIN LEAKING SOMEWHERE AND NOBODY CAN FIND WHERE?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE INVOICE CHECK. EVERY BILL IS READ INTO STRUCTURED FIELDS,",
             "CHECKED AGAINST THE RATE YOU AGREED, AND ANYTHING THAT DOES NOT",
             "MATCH IS [[FLAGGED]] AND ROUTED TO A PERSON RATHER THAN PAID."],
            ["TWO. THE DOCUMENT SWEEP. THE PAPERWORK IS READ INTO TEXT, THE",
             "REPEATED CONTENT IS STRIPPED OUT BEFORE ANYTHING IS SENT TO A",
             "MODEL SO THE RUN COSTS ALMOST NOTHING, AND THE [[FACTS]] COME BACK",
             "SYNTHESISED."],
            ["THREE. THE SCHEDULE REVIEW. YOUR PROGRAMME IS EXPORTED AS",
             "STRUCTURED DATA, A FRONTIER MODEL READS IT FOR RISK AND WASTE, AND",
             "EVERY FINDING IS PUT IN FRONT OF SOMEONE WHO [[KNOWS THE JOB]]",
             "BEFORE IT COUNTS."],
            ["THE RESULT, ONE BUSINESS EACH: THIRTY FIVE THOUSAND DOLLARS OF",
             "OVERBILLING CAUGHT, THREE WEEKS OF FACT FINDING DONE IN DAYS, AND",
             "ONE POINT TWO MILLION FOUND IN [[THE SCHEDULE.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Close shot of a thin bright stream of light escaping from a single pipe "
                  "joint high in the machine at the centre of frame and falling steadily away "
                  "into black beneath it, with no figure anywhere in the frame at all."),
            plate("Medium shot of a single round gauge fitted at a pipe joint in the centre of "
                  "frame, comparing what enters the pipe from the left against what leaves it "
                  "to the right, its needle jumped high and holding there."),
            plate("Medium shot of a thick stack of glowing white sheets being drawn through a "
                  "set of heavy rollers in the centre of frame, emerging thin and clean on the "
                  "far side, with the discarded duplicate sheets falling away into black "
                  "below."),
            plate("Medium shot of a long flat programme board mounted across the machine wall "
                  "and filled with a grid of small glowing white cards, with a single bar of "
                  "light travelling along its full length and stopping at each weak join in "
                  "the grid."),
            plate("Wide shot of a comparison gauge, a set of rollers and a long programme board "
                  "all lit together across one machine floor, every pipe joint in the frame "
                  "completely dry, and no figure anywhere in the frame."),
            plate("Wide shot of a calm upright faceless silhouette seating a brilliant glowing "
                  "core into a housing at the centre of the sliced-open building, and the "
                  "light now travelling brightly along the inside of the pipes instead of "
                  "escaping from them."),
        ],
    },
    {
        "slug": "noir-pain-headcount",
        "slug_line": "Growth capped by headcount",
        "board": "noir-vsl-headcount",
        "slides": [
            ["BOOKED OUT AND STILL CANNOT HIRE FAST ENOUGH?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE SUPPORT HUB. YOU MEASURE WHERE THE SUPPORT HOURS ACTUALLY",
             "GO, HAND THE REPEATING MAJORITY TO A MODEL, AND MOVE YOUR PEOPLE",
             "ONTO THE [[VIP WORK]] THAT KEEPS CUSTOMERS."],
            ["TWO. THE ROUTING LAYER. EVERY INBOUND TYPE IS CATEGORISED AND SENT",
             "TO THE QUEUE THAT OWNS IT, WITH A [[FALLBACK]] FOR ANYTHING IT",
             "CANNOT PLACE, AND THE HOURS RECOVERED ARE MEASURED."],
            ["THREE. THE SALES DESK. SEVERAL MODELS WEIGH THE SAME CALL AND",
             "SETTLE ON ONE ANSWER, WIRED INTO THE PHONE AND THE CALENDAR, AND",
             "YOU MAP WHERE THE WASTE IS [[BEFORE]] YOU BUILD ANYTHING."],
            ["THE RESULT, ONE BUSINESS EACH: FIFTY THREE PERCENT OF A SUPPORT",
             "TEAM'S WORKLOAD ABSORBED, FOUR FULL TIME ROLES OF SORTING GONE,",
             "AND FIFTY APPOINTMENTS A DAY FROM [[THREE ROLES HANDED BACK.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a sliced-open multi-room business standing in an empty black "
                  "void with a brand new room bolted onto the side of it, the new room dark "
                  "and bare, and a single faceless silhouette walking into it and taking up "
                  "the identical posture to the figure in the room next door."),
            plate("Medium shot of a hatch opening in the flat face of the machine at the centre "
                  "of frame and swallowing a stream of identical glowing white parcels of work "
                  "as they arrive, so that none of them reach the rooms above and behind it."),
            plate("Medium shot of a set of railway points on a conveyor belt throwing itself "
                  "over with nobody at it, sending each glowing white parcel of work away down "
                  "its own separate track, and the junction where a figure once stood now "
                  "completely empty."),
            plate("Medium shot of three small identical mechanisms arranged in a ring, passing "
                  "one glowing white parcel of work between them and setting it down finished, "
                  "with three empty chairs standing beside the ring."),
            plate("Wide shot of the sliced-open building with no new rooms bolted onto it at "
                  "all, a hatch, a set of points and a ring of three mechanisms all lit "
                  "together inside it, and every conveyor belt running heavily loaded with "
                  "glowing white parcels of work."),
            plate("Wide shot of a calm upright faceless silhouette seating a brilliant glowing "
                  "core into a housing at the centre of the sliced-open building, the light "
                  "re-threading every room, and the building holding exactly the same "
                  "footprint it started with."),
        ],
    },
    {
        "slug": "noir-pain-systems",
        "slug_line": "Disconnected systems",
        "board": "noir-vsl-systems",
        "slides": [
            ["TYPING THE SAME JOB INTO FOUR DIFFERENT SYSTEMS?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE PARALLEL RUN. THE AI IS GIVEN READ ONLY ACCESS SO IT CAN",
             "NEVER CHANGE YOUR SOURCE SYSTEMS, AND IT RUNS ALONGSIDE WHAT YOU",
             "ALREADY HAVE UNTIL YOU [[TRUST IT.]]"],
            ["TWO. THE COMPUTER USE AGENT. FOR THE SYSTEM WITH NO WAY IN, AN",
             "AGENT ON A MACHINE YOU CONTROL LOGS IN AND TYPES LIKE A PERSON",
             "WOULD, AND [[CHECKS]] EVERY ACTION LANDED BEFORE IT MOVES ON."],
            ["THREE. THE MORNING SYNC. THE CRM IS BUILT AROUND THE WORKFLOW YOU",
             "ACTUALLY RUN, EVENTS AND OUTREACH FIRE THEMSELVES, AND A BROWSER",
             "EXTENSION [[BRIDGES]] THE TOOLS THAT OFFER NO WAY IN."],
            ["THE RESULT, ONE BUSINESS EACH: A FULL OPERATING SYSTEM ROLLED OUT",
             "IN EIGHT WEEKS, THE API LESS SYSTEM DRIVEN WITHOUT ONE, AND A CRM",
             "RUNNING A PORTFOLIO PAST [[A HUNDRED THOUSAND A MONTH.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of one glowing white parcel of work entering four identical "
                  "intake slots in sequence across four separate machines standing side by "
                  "side, and the parcel that emerges from the fourth machine noticeably dimmer "
                  "than the one that went into the first."),
            plate("Wide shot of a broad receiving floor opening beneath four separate machines, "
                  "every conveyor belt above it feeding a copy of its glowing white work down "
                  "into the floor, and every arrow and chute running one way only, downward."),
            plate("Close shot of the flat face of a single machine with no pipe fitting or "
                  "connection anywhere on it, and a jointed mechanical hand raised to the row "
                  "of keys on its front, pressing them itself."),
            plate("Wide shot of the top of the sliced-open building with the first dawn light "
                  "raking along it, and every round dial across all four machines rolling over "
                  "to rest at exactly the same reading at the same moment."),
            plate("Medium shot of the seam between two machine halves now completely closed, "
                  "with one single unbroken conveyor belt running straight across the place "
                  "where the gap used to be, and no figure anywhere in the frame."),
            plate("Wide shot of a calm upright faceless silhouette seating a brilliant glowing "
                  "core into a housing at the centre of the sliced-open building, and one "
                  "glowing white parcel of work entering once and appearing brightly lit in "
                  "all four rooms of the building at the same moment."),
        ],
    },
    # ---------------------------------------------------------------------------------
    # QUEUE DECKS. Ideated in `projects/content-engine/ideas/news-carousels/NOIR-QUEUE.md`,
    # 38 decks across three waves. Copy is first-pass and NOT approved; the operator is refining
    # after the plates land.
    #
    # NO BOARD EXISTS for these pains. SKILL.md section 2 asks every painted scene to be
    # lifted from a matching `noir-vsl-<pain>/SHOTS.md`, and those boards cover the eight
    # canonical pains only. the operator's go on 2026-08-01 was to generate anyway, so these scenes
    # are composed directly from the noir motif vocabulary (phase 3 of the noir-painterly
    # skill) and keep the same slide-to-beat shape the boards would have given: slide 1 the
    # opening motif, slides 2 to 4 the three teach beats, slide 5 the solution wide, slide 6
    # the installer seating the core.
    # ---------------------------------------------------------------------------------
    {
        "slug": "noir-pain-bottleneck",
        "slug_line": "The owner bottleneck",
        "board": None,  # composed from the motif vocabulary, see the note above
        "slides": [
            ["EVERY DECISION IN THE BUSINESS STILL WAITING ON YOU?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE STANDING ASSISTANT. IT READS YOUR MAIL BEFORE YOU DO,",
             "GIVES YOU ONE RUNDOWN EACH MORNING, ARCHIVES THE NOISE, AND FLAGS",
             "ONLY WHAT NEEDS YOU. IT LIVES ON A SERVER SO IT IS [[AWAKE]] WHEN",
             "YOU ARE NOT."],
            ["TWO. THE MAIL FLEET. YOU PICK THE ONE EMAIL JOB THAT EATS THE MOST",
             "HOURS, HAND IT TO A GROUP OF AGENTS WITH A COORDINATOR OVER THEM,",
             "AND ADD A [[CHECKING LAYER]] SO NOTHING GOES OUT WRONG."],
            ["THREE. THE HANDS. FOR THE OLD SYSTEM WITH NO WAY IN, AN AGENT",
             "DRIVES THE SCREEN ITSELF, CLICKING THROUGH THE STEPS LIKE A PERSON",
             "WOULD, AND [[CONFIRMS]] EVERY ACTION LANDED BEFORE IT MOVES ON."],
            ["THE RESULT, ONE BUSINESS EACH: THREE HOUR JOBS DONE IN THIRTY",
             "MINUTES, TEN HOURS A WEEK DOWN TO ONE, AND AN OPERATOR WHO",
             "AUTOMATED [[THEIR OWN FULL TIME JOB.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        # NO ANNOTATIONS. Cut by the operator on 2026-08-01 after seeing them on the first built
        # queue deck. The labels, leaders and tool marks are gone: the plate carries the
        # painting and the band carries the argument, with clean black between them.
        # An empty row makes `overlay_for` return None, so nothing is drawn.
        #
        # This also drops the tool-logo evidence claim, which is a simplification rather than
        # a loss: the three Hub builds behind this deck (the always-on executive-assistant
        # agent, the owners-corporation email fleet, and the computer-use inspection workflow)
        # record no tool against them, so the marks were only ever standing for the counted
        # CRM stack, never for these builds.
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a sliced-open multi-room business standing in an empty black "
                  "void, every conveyor belt and pneumatic tube in every room curving inward "
                  "and terminating at the hands of one faceless silhouette standing alone at "
                  "the centre of the building, with tall stacks of glowing white parcels of "
                  "work waiting at its feet."),
            # Regenerated 2026-08-01. The first version painted a lit floor plane straight
            # through the plate's lower fade zone, so its hard horizontal edge survived the
            # 180px gradient and the join to the band read as a truncation. The scene now
            # floats the desk in void the way slide 1 floats the building, and states the
            # empty lower half explicitly.
            plate("Medium shot of a small roll-top desk standing entirely alone in an empty "
                  "black void with no floor, no walls and no room around it, raised into the "
                  "upper half of the frame, a single lamp burning above it, a neat prepared "
                  "stack of glowing white parcels of work squared up and waiting on the desk, "
                  "no figure anywhere in the frame, and the whole lower half of the frame "
                  "empty solid black falling away into nothing."),
            plate("Medium shot of a wide bank of chutes fanning out across the frame above a "
                  "single small desk, a heavy stream of glowing white parcels of work pouring "
                  "into the chutes and away to either side, and one parcel only continuing "
                  "down to the desk below."),
            plate("Wide shot of a full workstation built into the machine wall, its bank of "
                  "keys and levers worked by two jointed mechanical arms moving on their own, "
                  "and an empty wooden chair pushed back from the station beside them."),
            plate("Wide shot of the sliced-open building with a lit desk, a bank of chutes and "
                  "a mechanical workstation all running together across one continuous machine "
                  "floor, every conveyor belt now flowing past the centre of the building "
                  "instead of into it, and no figure anywhere in the frame."),
            plate("Wide shot of a calm upright faceless silhouette kneeling at the centre of "
                  "the sliced-open building and seating a brilliant glowing core into its "
                  "housing, the light from the core re-threading every room of the building "
                  "from the inside, and the belts running on past it without stopping."),
        ],
    },
    {
        "slug": "noir-pain-staff",
        "slug_line": "Staff overload",
        "board": None,
        "slides": [
            ["YOUR TEAM AT ONE HUNDRED AND TEN AND STILL BEHIND?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE ROUTER. EVERY MESSAGE THAT ARRIVES IS READ, SORTED INTO A",
             "TYPE, AND SENT STRAIGHT TO THE QUEUE THAT OWNS IT. ANYTHING IT",
             "CANNOT PLACE GOES TO A [[FALLBACK]] SO NOTHING SITS UNREAD."],
            ["TWO. THE DOCUMENT ANALYST. IT TAKES IN THE PAPERWORK, TRANSCRIBES",
             "IT, AND MATCHES EVERY PIECE OF EVIDENCE TO WHAT IT PROVES.",
             "ANYTHING IT IS UNSURE OF GOES TO A [[PERSON]] TO CONFIRM."],
            ["THREE. THE PAYROLL RUN. IT READS YOUR HOURS WITHOUT BEING ABLE TO",
             "CHANGE THEM, APPLIES EVERY PAY RULE AS CODE RATHER THAN FROM",
             "MEMORY, AND PRINTS THE [[DAILY]] BILLINGS REPORT ON THE WAY",
             "THROUGH."],
            ["THE RESULT, ONE BUSINESS EACH: FOUR FULL TIME ROLES OF SORTING",
             "GONE, A FOUR PERSON JOB NOW RUNNING WITH ONE, AND SIX HOURS OF",
             "PAYROLL DONE IN [[TEN SECONDS.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            # v1 painted a lit floor under the benches and terminated in a hard horizontal edge
            # at y644. v2 borrowed the void phrasing from noir-pain-shelfware slide 1 and, with
            # figures in frame, floated the row onto a girder above a city. v3 keeps the ground
            # and loses it to darkness instead of denying it, per the figures rule.
            plate("Wide shot of a long row of identical faceless silhouettes seated at identical "
                  "benches, each figure behind a stack of glowing white parcels of work taller "
                  "than itself, the row receding into darkness at both sides, the unlit floor "
                  "beneath the benches falling away into deep shadow with no far wall and no "
                  "horizon visible anywhere, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Medium shot of a heavy sorting head lowered over a small landing floating in "
                  "an empty black void, each arriving glowing white parcel of work read as it "
                  "passes beneath it and dropped down its own chute, the row of chutes fanning "
                  "out across the frame, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Medium shot of a thick stack of glowing white sheets being drawn through a "
                  "set of heavy rollers suspended alone in an empty black void, emerging thin "
                  "and clean on the far side, and the discarded duplicate sheets falling away "
                  "and vanishing into the solid black lower half of the frame."),
            plate("Medium shot of a tall bank of iron levers throwing themselves in sequence "
                  "with nobody standing at them, the bank floating in an empty black void with "
                  "no floor, thin cards feeding down through the mechanism and emerging at the "
                  "bottom as one clean sheet, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Wide shot of a sorting head, a set of rollers and a bank of levers all lit "
                  "together along one continuous conveyor belt floating in an empty black void, "
                  "glowing white parcels of work running the whole length of it, no figure "
                  "anywhere in the frame, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room "
                  "from the inside, and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-delivery",
        "slug_line": "Operations and delivery drag",
        "board": None,
        "slides": [
            ["WINNING THE WORK AND THEN BLEEDING ON DELIVERY?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE WORKFLOW ENGINE. AN ASSISTANT THAT RUNS A WHOLE PROCESS.",
             "YOU ASK IN PLAIN ENGLISH, IT WORKS OUT THE NEXT STEP, OPENS YOUR",
             "CRM, EMAIL AND CALENDAR ITSELF, AND WAITS FOR YOUR [[APPROVAL]]",
             "BEFORE ANYTHING THAT COSTS YOU."],
            ["TWO. THE PROCESS RUNNER. A TEAM OF SMALL AGENTS WITH ONE",
             "COORDINATOR OVER THE TOP. YOU MAP THE SLOW PROCESS ONCE, EVERY",
             "STEP GOES TO THE AGENT THAT OWNS IT, AND THE [[JOB FILE]] IS",
             "WRITTEN BACK AT EVERY HANDOVER."],
            ["THREE. THE BILLING RUN. IT WIRES YOUR SEPARATE SYSTEMS INTO ONE.",
             "ORDERS SYNC BETWEEN SITES AS THEY LAND, A VOICE AGENT TAKES THE",
             "CALLS THAT FEED IT, AND THE SUMS RUN ON [[FIXED RULES]] SO THE",
             "NUMBERS ARE NEVER A GUESS."],
            ["THE RESULT, ONE BUSINESS EACH: SIXTY PERCENT OF THE MANUAL",
             "OVERHEAD GONE, A TWENTY ONE DAY PROCESS CLOSING IN FOUR, AND",
             "FOUR WEEKS OF BILLING DONE IN [[FOUR DAYS.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of one glowing white parcel of work travelling left to right along "
                  "a conveyor belt floating in an empty black void, passing through six "
                  "separate stations in a row, entering the first brilliantly lit and leaving "
                  "the last visibly dim and guttering, and the whole lower half of the frame "
                  "empty solid black."),
            plate("Medium shot of a long conveyor belt floating in an empty black void with the "
                  "wide idle gaps between its stations closing up and the stations drawing "
                  "together into one tight continuous run, glowing white parcels of work moving "
                  "without pause, and the whole lower half of the frame empty solid black."),
            plate("Medium shot of a tall wall of small glowing white cards arranged in a long "
                  "calendar grid suspended in an empty black void, most of the cards going dark "
                  "and folding away so only a small handful remain lit at the left end, and the "
                  "whole lower half of the frame empty solid black."),
            plate("Medium shot of a heavy press at the end of a conveyor belt floating in an "
                  "empty black void, stamping each arriving glowing white parcel of work into a "
                  "bound sheet and setting it down on an outbound belt already filling with "
                  "finished sheets, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a tightened conveyor run, a collapsed calendar wall and a "
                  "stamping press all lit together across one continuous machine floor floating "
                  "in an empty black void, every parcel still brightly lit as it leaves, no "
                  "figure anywhere in the frame, and the whole lower half of the frame empty "
                  "solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-leadgen",
        "slug_line": "The lead generation ceiling",
        "board": None,
        "slides": [
            ["SPENDING MORE ON ADS AND GETTING THE SAME LEADS BACK?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE MATCHER. IT SCORES EVERY LEAD AGAINST WHAT YOU ACTUALLY",
             "SELL RATHER THAN AGAINST WHEN IT CAME IN, SO THE LIST IN FRONT OF",
             "YOU IS RANKED BY [[FIT.]]"],
            ["TWO. THE SHARED MEMORY. SEVERAL AGENTS WRITE INTO ONE RECORD OF",
             "YOUR BUSINESS, SO THE ONE THAT RECOMMENDS YOUR NEXT MOVE IS",
             "READING EVERYTHING THE OTHERS [[LEARNED.]]"],
            ["THREE. THE OUTREACH ENGINE. IT SCRAPES AND CROSS CHECKS PROSPECT",
             "DATA, THEN SENDS OUT SMALL FAST AGENTS THAT EACH BUILD AND PUBLISH",
             "A SITE FOR ONE PROSPECT, SO EVERY CALLER OPENS WITH A [[LIVE",
             "LINK.]]"],
            ["THE RESULT, ONE BUSINESS EACH: THIRTY THOUSAND UNUSED LEADS FOUND,",
             "ENQUIRIES UP FORTY THREE PERCENT, AND THREE HUNDRED AND EIGHT",
             "SITES SHIPPED IN [[UNDER A DAY.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of an enormous wide funnel mouth floating in an empty black void "
                  "swallowing a heavy pouring stream of coins at its top, and only three small "
                  "glowing white parcels of work emerging from its narrow spout below, with the "
                  "whole lower half of the frame empty solid black."),
            plate("Wide shot of a dark storeroom suddenly lighting up inside an empty black "
                  "void to reveal tall racks packed with dormant glowing white parcels of work "
                  "stretching back into the frame, every one of them already there and unlit "
                  "until now, and the whole lower half of the frame empty solid black."),
            plate("Medium shot of a sorting head lowered over a conveyor belt floating in an "
                  "empty black void, addressing each passing glowing white parcel of work "
                  "differently and pressing a distinct individual mark into each one, and the "
                  "whole lower half of the frame empty solid black."),
            plate("Wide shot of a long conveyor belt floating in an empty black void carrying a "
                  "row of small identical buildings that assemble themselves piece by piece as "
                  "they travel, finished and lit by the right of frame, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Wide shot of a lit storeroom of dormant parcels, a marking sorting head and a "
                  "line of self-assembling buildings all running together across one continuous "
                  "machine floor floating in an empty black void, no figure anywhere in the "
                  "frame, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-shelfware",
        "slug_line": "Software paid for and unused",
        "board": None,
        "slides": [
            ["PAYING FOR SOFTWARE NOBODY IN THE BUSINESS OPENS?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE OPERATIONS FLEET. IT TAKES THE JOBS SPREAD ACROSS YOUR",
             "PAID APPS, RUNS THEM FROM ONE SERVER YOU OWN, AND BOOKS THE",
             "FREIGHT ITSELF THROUGH THE CARRIER, WITH THE DATA STAYING [[ON",
             "YOUR SIDE.]]"],
            ["TWO. THE ENQUIRY DESK. IT HANDLES THE HIGH VOLUME QUESTIONS COMING",
             "AT YOU EVERY DAY AND FILLS OUT THE FINANCIAL MODELS UNDERNEATH",
             "THEM, ALL ON A [[SECURED SERVER]] THAT YOU CONTROL."],
            ["THREE. THE ACTIVATOR. IT PULLS YOUR SYSTEMS INTO ONE PLACE, STRIPS",
             "THE PERSONAL DETAILS OUT, THEN WATCHES FOR A LINE BEING CROSSED",
             "AND SENDS SOMEBODY THE [[ACTION]] RATHER THAN ANOTHER CHART."],
            ["THE RESULT, ONE BUSINESS EACH: A THOUSAND DOLLARS A MONTH OF APPS",
             "GONE, SIXTEEN HOURS A WEEK DOWN TO SIXTEEN A MONTH, AND SEVEN",
             "THOUSAND A MONTH OF [[SOFTWARE SAVED.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a long row of handsome polished machines suspended side by side "
                  "in an empty black void with no floor and no ground plane anywhere, every one "
                  "of them lit and humming and connected to no conveyor belt at all, their "
                  "intake slots empty, nothing beneath them but empty black, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Medium shot of one polished machine in an empty black void being coupled for "
                  "the first time to a main conveyor line, a heavy connector seating home into "
                  "its side and glowing white parcels of work beginning to run through it, and "
                  "the whole lower half of the frame empty solid black."),
            plate("Close shot of a large round subscription meter mounted alone in an empty "
                  "black void, its needle sweeping firmly backwards down the dial toward zero, "
                  "and the whole lower half of the frame empty solid black."),
            plate("Medium shot of a large round dial floating in an empty black void that stops "
                  "displaying a reading and instead extends a mechanical arm to throw a heavy "
                  "lever beside it, the lever visibly travelling, and the whole lower half of "
                  "the frame empty solid black."),
            plate("Wide shot of a coupled machine, a backward-running meter and a dial throwing "
                  "its own lever all lit together across one continuous machine floor floating "
                  "in an empty black void, every machine now fed by a belt, no figure anywhere "
                  "in the frame, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-compliance",
        "slug_line": "Compliance and reporting load",
        "board": None,
        "slides": [
            ["HALF YOUR WEEK GOING INTO PROVING YOU DID THE WORK?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE AUDIT AGENT. THE AUDIT IS BROKEN INTO CHECKS AND EACH",
             "CHECK IS GIVEN TO AN AGENT THAT OWNS IT. THE DATA IS STRIPPED OF",
             "NAMES FIRST, AND A [[MANAGER AGENT]] KEEPS THE WHOLE RUN IN ORDER."],
            ["TWO. THE CONTRACT READER. IT READS THE AGREEMENTS AND MAPS THE",
             "PROCESS BURIED IN THEM, SO A DISPUTE STARTS WITH THE FACTS ALREADY",
             "PULLED. IT CAN RUN [[ON YOUR OWN HARDWARE]] WHEN THE DATA CANNOT",
             "LEAVE."],
            ["THREE. THE EVIDENCE PACK. THE RECURRING REPORT IS BUILT ONCE AS A",
             "PRODUCT, THEN THE COMPLIANCE STEPS RUN THEMSELVES AND THE",
             "SCORECARD [[REBUILDS]] WHENEVER YOU ASK FOR IT."],
            ["THE RESULT, ONE BUSINESS EACH: A SIX MONTH AUDIT DONE IN TWO DAYS,",
             "DAYS OF MANUAL WORK SAVED ON ONE DISPUTE, AND A LEADERSHIP",
             "SCORECARD REBUILT IN [[TWELVE MINUTES.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of one small faceless silhouette dwarfed by an enormous filing "
                  "wall of identical drawers rising the full height of the frame in an empty "
                  "black void with no floor and no ground plane anywhere, the wall stretching "
                  "away beyond the light on both sides, both the figure and the wall cut off "
                  "below by deep shadow with nothing beneath them but empty black, and the whole "
                  "lower half of the frame empty solid black."),
            plate("Medium shot of a heavy measuring drum turning at a steady rate in an empty "
                  "black void, stamping an identical mark onto every glowing white parcel of "
                  "work that passes beneath it, the stamped parcels filing away in one long "
                  "even row, and the whole lower half of the frame empty solid black."),
            plate("Medium shot of a large painted lens on a long armature lowered over a single "
                  "unrolled document that runs the full width of the frame in an empty black "
                  "void, the lens travelling along it and lighting each clause as it passes, "
                  "and the whole lower half of the frame empty solid black."),
            plate("Medium shot of a mechanism floating in an empty black void drawing a wide "
                  "scatter of loose glowing white sheets together and binding them into one "
                  "finished pack in a single stroke, each sheet still carrying a visible stamp "
                  "of where it came from, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Wide shot of a stamping drum, a travelling lens on its armature and a binding "
                  "mechanism all lit together across one continuous machine floor floating in "
                  "an empty black void, the enormous filing wall behind them now dark and "
                  "closed, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-hiring",
        "slug_line": "The hiring and talent gap",
        "board": None,
        "slides": [
            ["CANNOT HIRE FOR A ROLE YOU CANNOT ASSESS YOURSELF?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE SCREENING AGENT. YOU WRITE THE QUESTIONS AND THE SCORING",
             "ONCE, A VOICE AGENT RUNS EVERY FIRST CALL TO THAT SAME SCRIPT, AND",
             "EACH CANDIDATE COMES BACK [[SCORED]] THE SAME WAY."],
            ["TWO. THE ASSESSMENT ROOM. THE ROLE IS TURNED INTO REAL SCENARIOS",
             "AND PUT TO CANDIDATES BY A SPEAKING AVATAR, SO YOU CAN RUN [[A",
             "HUNDRED AT ONCE]] AND STILL SEE HOW EACH ONE THINKS."],
            ["THREE. THE ELIGIBILITY CHECK. EVERY RULE YOU HIRE AGAINST IS",
             "MAPPED AS A GRAPH THE MACHINE CAN WALK, AND EACH APPLICANT IS",
             "CHECKED AGAINST ALL OF IT BEFORE IT IS TRUSTED, IT IS [[TESTED]]",
             "AGAINST YOUR PAST DECISIONS."],
            ["THE RESULT, ONE BUSINESS EACH: A SCREENING AGENT RUNNING LIVE WITH",
             "REAL CANDIDATES, A HUNDRED ASSESSMENTS AT ONCE FOR A TWENTY FIVE",
             "THOUSAND PERSON EMPLOYER, AND A SIX MONTH ELIGIBILITY CHECK DONE",
             "IN [[UNDER A SECOND.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a long row of empty wooden chairs at empty workbenches suspended "
                  "in an empty black void with no floor and no ground plane anywhere, every "
                  "machine behind them running at full speed with nobody attending it, the "
                  "chair legs and bench legs receding into deep shadow, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Medium shot of a narrow gate standing at the head of a conveyor belt floating "
                  "in an empty black void, each arriving glowing white parcel of work weighed "
                  "and tagged as it passes through the gate and continues on, and the whole "
                  "lower half of the frame empty solid black."),
            plate("Wide shot of a tall bank of a hundred identical small painted lenses arranged "
                  "in a grid in an empty black void, every single one of them lit and focused "
                  "at the same moment, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Close shot of one large round dial alone in an empty black void with its "
                  "needle swinging instantly across the full face and coming to rest dead "
                  "steady, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a weighing gate, a grid of a hundred lit lenses and a single "
                  "steady dial all lit together across one continuous machine floor floating in "
                  "an empty black void, the row of chairs behind them now filled with working "
                  "faceless silhouettes, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-marketing",
        "slug_line": "Marketing complexity",
        "board": None,
        "slides": [
            ["MARKETING SPREAD ACROSS SIX TOOLS AND ONE AGENCY?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE CAMPAIGN FLEET. PLANNING, CREATIVE AND PUBLISHING EACH",
             "GET THEIR OWN AGENT, AND A SEPARATE [[CHECKER]] READS EVERYTHING",
             "BEFORE IT GOES OUT, SO NOTHING PUBLISHES UNREVIEWED."],
            ["TWO. THE REPORTING LAYER. THE REPORT EACH CLIENT ASKS FOR IS",
             "ASSEMBLED STRAIGHT FROM THE AD PLATFORMS, AND THE REVIEW DASHBOARD",
             "SITS ON A [[REAL DATABASE]] RATHER THAN A PILE OF SPREADSHEETS."],
            ["THREE. THE SEARCH ENGINE. IT SCRAPES WHAT PEOPLE ACTUALLY SEARCH",
             "FOR AND WHAT COMPETITORS RANK ON, WRITES THE PAGES GROUNDED IN",
             "THAT, AND PUBLISHES THEM STRAIGHT TO YOUR [[STOREFRONT.]]"],
            ["THE RESULT, ONE BUSINESS EACH: PLANNING TO PUBLISHED IN UNDER",
             "THREE DAYS, FOUR HOURS A WEEK BACK FOR EVERY MEDIA BUYER, AND",
             "CONVERSION RATES [[DOUBLED.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of six separate small machines suspended well apart from one "
                  "another in an empty black void with no floor and no ground plane anywhere, "
                  "each producing its own single dim parcel of work, no conveyor belt joining "
                  "any of them, nothing beneath them but empty black, and the whole lower half "
                  "of the frame empty solid black."),
            plate("Medium shot of three small identical mechanisms arranged in a tight ring in "
                  "an empty black void, passing one glowing white parcel of work between them "
                  "and setting it down finished and brilliantly lit, and the whole lower half "
                  "of the frame empty solid black."),
            plate("Medium shot of a heavy press floating in an empty black void producing one "
                  "bound report and setting it onto an outbound belt, a row of identical bound "
                  "reports already running away behind it at even intervals, and the whole "
                  "lower half of the frame empty solid black."),
            plate("Wide shot of a single conveyor belt in an empty black void starting narrow at "
                  "the left of frame and widening steadily as it runs toward a hard shaft of "
                  "key light at the right, carrying more glowing white parcels of work the "
                  "wider it gets, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a ring of three mechanisms, a report press and one widening belt "
                  "all lit together across a continuous machine floor floating in an empty black "
                  "void, the six scattered machines now joined into one line, and the whole "
                  "lower half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-security",
        "slug_line": "Data security fear",
        "board": None,
        "slides": [
            ["WANT THE AI AND CANNOT LET THE DATA LEAVE THE BUILDING?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE CLOSED ROOM. THE MODELS RUN ON HARDWARE INSIDE YOUR WALLS",
             "WITH NO LINE OUT, THE WORK IS SPLIT ACROSS SPECIALIST AGENTS, AND",
             "EVERY LAYER IS [[LOCKED]] WITH ITS OWN CRYPTOGRAPHY."],
            ["TWO. THE BID WRITER. THE SUBMISSION IS DRAFTED BY COORDINATED",
             "AGENTS READING YOUR OWN LIBRARY, RUNNING ON [[YOUR OWN]] INFERENCE",
             "HARDWARE, SO THE EXECUTIVE MEETINGS THAT USED TO WRITE IT STOP."],
            ["THREE. THE CLINICAL ASSISTANT. EVERY PATIENT DETAIL IS STRIPPED",
             "BEFORE ANYTHING IS PROCESSED, ACCESS IS LAYERED AND LOGGED, AND",
             "THE WHOLE THING IS PROVEN TO [[TRIAL STANDARD]] BEFORE IT GOES",
             "LIVE."],
            ["THE RESULT, ONE BUSINESS EACH: A PLATFORM PAST TEN MILLION IN",
             "RECURRING REVENUE, EXECUTIVE MEETING OVERHEAD ON BIDS GONE, AND A",
             "CLINICAL DEPLOYMENT CLEARED TO [[TRIAL READINESS.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of an enormous sealed strongroom door set into a heavy machine wall "
                  "floating in an empty black void, one single pipe running into it and no pipe "
                  "of any kind running out, and the whole lower half of the frame empty solid "
                  "black."),
            plate("Wide shot of an entire busy machine floor completely enclosed within a heavy "
                  "riveted outer shell in an empty black void, glowing white parcels of work "
                  "moving briskly along every belt inside it, and no opening anywhere in the "
                  "shell, with the whole lower half of the frame empty solid black."),
            plate("Medium shot of a bank of four heavy one-way valves fitted along four pipes "
                  "running across an empty black void, glowing white work flowing inward through "
                  "them only, nothing at all flowing back the other way, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Close shot of a large painted lens lowered over a single glowing white parcel "
                  "of work in an empty black void, blanking the markings from the parcel's face "
                  "before reading it so the surface passes beneath the lens clean, and the whole "
                  "lower half of the frame empty solid black."),
            plate("Wide shot of a sealed shell, a one-way valve bank and a blanking lens all lit "
                  "together across one continuous enclosed machine floor floating in an empty "
                  "black void, no figure anywhere in the frame, and the whole lower half of the "
                  "frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-lockin",
        "slug_line": "Vendor lock-in fear",
        "board": None,
        "slides": [
            ["CANNOT CHANGE YOUR OWN SYSTEM WITHOUT RINGING SOMEBODY?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE ESCAPE HATCH. YOU CHECK YOUR CURRENT TOOL EXPOSES A WAY",
             "IN, STAND UP A CHEAP SERVER THAT CALLS IT, AND REBUILD ONLY THE",
             "WORKFLOWS PEOPLE ACTUALLY USE ON TOP OF THE [[DATA YOU ALREADY",
             "HAVE.]]"],
            ["TWO. THE INVOICE RUN. REPORTS LAND IN AN INBOX, EACH PDF IS TURNED",
             "INTO STRUCTURED DATA, A MODEL ON YOUR OWN HARDWARE APPLIES YOUR",
             "BILLING RULES, AND THE INVOICE IS RAISED AGAINST THE RATE IN",
             "[[YOUR SYSTEM OF RECORD.]]"],
            ["THREE. THE INTERNAL BUILD. WHERE THE LICENCE IS THE COST, THE TOOL",
             "IS REBUILT IN HOUSE AND EACH AGENT IS GIVEN THE [[SMALLEST MODEL]]",
             "THAT CAN DO ITS JOB, SO THE RUNNING COST STAYS LOW."],
            ["THE RESULT, ONE BUSINESS EACH: A PAID CRM SUBSCRIPTION GONE, A",
             "NINETY THOUSAND DOLLAR A YEAR MANUAL PROCESS REPLACED FOR A FEW",
             "HUNDRED A MONTH IN COMPUTE, AND FIVE MILLION SAVED IN",
             "[[LICENSING.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a large machine floating in an empty black void with its control "
                  "panel shut away behind a heavy locked iron grille, and a single key hanging "
                  "on a hook far out in the black well beyond the machine's reach, with the "
                  "whole lower half of the frame empty solid black."),
            plate("Medium shot of a heavy iron grille lifted clear and set aside in an empty "
                  "black void, the control panel behind it standing fully open and lit, and the "
                  "bare hand of a faceless silhouette resting on its levers, with the whole "
                  "lower half of the frame empty solid black."),
            plate("Medium shot of a compact self-contained machine floating alone in an empty "
                  "black void with its own small glowing power core seated inside it, no cable "
                  "and no pipe running away from it in any direction, and the whole lower half "
                  "of the frame empty solid black."),
            plate("Medium shot of a long row of heavy padlocks fitted along a machine seam in an "
                  "empty black void, every one of them springing open at the same moment and "
                  "the seam parting to show the mechanism inside, and the whole lower half of "
                  "the frame empty solid black."),
            plate("Wide shot of an opened control panel, a self-powered machine and a row of "
                  "sprung padlocks all lit together across one continuous machine floor floating "
                  "in an empty black void, the key hook out in the black now empty, and the "
                  "whole lower half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-governance",
        "slug_line": "The AI governance gap",
        "board": None,
        "slides": [
            ["EVERY DEPARTMENT RUNNING ITS OWN AI AND NOBODY COUNTING?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE CONTROL LAYER. EVERY AGENT AND EVERY TEAM IS WALLED OFF",
             "FROM THE OTHERS, AND THE PROOF THAT YOUR SECURITY RULES ARE BEING",
             "FOLLOWED IS [[COLLECTED]] BY THE SYSTEM RATHER THAN BY YOU."],
            ["TWO. THE PROVENANCE TRAIL. ONE AGREED SHAPE FOR YOUR DATA IS SET",
             "FIRST, THEN EVERY INPUT AND EVERY OUTPUT IS STAMPED WITH WHERE IT",
             "CAME FROM, SO ANY ANSWER CAN BE [[CHECKED]] LONG AFTER IT WAS",
             "GIVEN."],
            ["THREE. THE ASSISTANT WITH LIMITS. IT PLUGS INTO THE TOOLS THE ROLE",
             "ACTUALLY USES AND CHECKS FOR NEW WORK ON A TIMER, AND ANYTHING",
             "RISKY SITS BEHIND A [[TRUST LEVEL]] IT CANNOT CROSS ALONE."],
            ["THE RESULT, ONE BUSINESS EACH: A GOVERNANCE PLATFORM LIVE WITH",
             "FIVE DESIGN PARTNERS, A PRODUCTION SYSTEM RUNNING FOR A GOVERNMENT",
             "LINKED RESEARCH CLIENT, AND AN ASSISTANT TAKEN [[TO THE",
             "EXECUTIVE.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of four separate rooms of a sliced-open building floating in an "
                  "empty black void, each room running a completely different unconnected "
                  "mechanism at a different angle, no two conveyor belts aligned, and one empty "
                  "control lectern standing unattended at the centre, with the whole lower half "
                  "of the frame empty solid black."),
            plate("Wide shot of one faceless silhouette standing at a raised control lectern at "
                  "the centre of a sliced-open building in an empty black void, every conveyor "
                  "belt in every room now visible and squared to the same axis from where it "
                  "stands, and the whole lower half of the frame empty solid black."),
            plate("Medium shot of a stamping mechanism in an empty black void pressing a "
                  "distinct room-of-origin mark into each glowing white parcel of work as it "
                  "passes, the marked parcels filing away in one long traceable row, and the "
                  "whole lower half of the frame empty solid black."),
            plate("Medium shot of a heavy gate set across a conveyor belt in an empty black "
                  "void, admitting some glowing white parcels of work straight through and "
                  "turning others firmly back the way they came, and the whole lower half of "
                  "the frame empty solid black."),
            plate("Wide shot of a manned control lectern, an origin-stamping mechanism and an "
                  "admitting gate all lit together across one continuous machine floor floating "
                  "in an empty black void, every belt running to the same axis, and the whole "
                  "lower half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-execution-gap",
        "slug_line": "The execution gap",
        "board": None,
        "slides": [
            ["KNOW AI MATTERS AND STILL HAVE NOTHING RUNNING?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE RECEIPT READER. A VISION MODEL PULLS THE FIELDS OFF EVERY",
             "RECEIPT, SEVERAL PIPELINES RUN SO ONE BAD SCAN CANNOT STOP IT, AND",
             "THE RESULT DROPS STRAIGHT INTO THE [[WORKFLOW.]] START HERE."],
            ["TWO. THE ROUTER. EVERY INBOUND MESSAGE IS SORTED INTO A TYPE AND",
             "SENT TO THE QUEUE THAT OWNS IT, WITH A [[FALLBACK]] FOR ANYTHING",
             "IT CANNOT PLACE, SO NOTHING WAITS ON A PERSON TO TRIAGE IT."],
            ["THREE. THE LEAD RESPONSE. YOU MAP THE PATH FROM ENQUIRY TO QUOTE",
             "AND AGREE WHAT YOU ARE MEASURING FIRST, THEN AN AGENT QUALIFIES",
             "EVERY LEAD AND WRITES THE [[QUOTE]] WITHOUT WAITING FOR ANYONE."],
            ["THE RESULT, ONE BUSINESS EACH: FIFTEEN MINUTE JOBS FINISHING IN",
             "SECONDS, FOUR FULL TIME ROLES OF SORTING GONE, AND A FOUR DAY",
             "REPLY TIME DOWN TO [[FIVE MINUTES.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of one faceless silhouette before an enormous wall of hundreds of "
                  "identical unlabelled iron levers in an empty black void with no floor and no "
                  "ground plane anywhere, its hand raised and touching none of them, the wall "
                  "running past the edges of the frame, nothing beneath either of them but empty "
                  "black, and the whole lower half of the frame empty solid black."),
            plate("Medium shot of a large painted lens on an armature lowered over a conveyor "
                  "belt in an empty black void, each glowing white parcel of work passing "
                  "underneath it, coming out stamped, and dropping into its own slot in a tall "
                  "rack beside the belt, with the whole lower half of the frame empty solid "
                  "black."),
            plate("Medium shot of a heavy sorting head over a small landing in an empty black "
                  "void, reading each arriving glowing white parcel of work and dropping it "
                  "down its own chute, the chutes fanning out across the frame, and the whole "
                  "lower half of the frame empty solid black."),
            plate("Medium shot of a solid catcher plate closing the gap at the end of a conveyor "
                  "belt in an empty black void, each glowing white parcel of work caught, "
                  "marked, and set back onto the belt still brightly lit, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Wide shot of the enormous lever wall now dark and closed, and three levers "
                  "only picked out of it by a single hard shaft of key light, each one wired "
                  "down to a small running mechanism below it in an empty black void, with the "
                  "whole lower half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-cx",
        "slug_line": "Customer experience risk",
        "board": None,
        "slides": [
            ["GROWING FAST, BUT SERVICE QUALITY SLIPPING?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE SUPPORT AGENT. THE SERVICE IS SPLIT INTO SPECIALIST",
             "AGENTS, EVERY ANSWER IS PULLED FROM YOUR OWN DOCUMENTS RATHER THAN",
             "GUESSED, AND THE REGULATED DATA SITS IN A [[SEALED NETWORK]] OF",
             "ITS OWN."],
            ["TWO. THE PRE PURCHASE AGENT. THE CUSTOMER SEES THE PRODUCT ON",
             "THEMSELVES BEFORE THEY BUY, A TRAINED BOT ANSWERS THE QUESTION",
             "THAT WAS STOPPING THEM, AND THE [[EMAIL FLOWS]] BEHIND IT ARE",
             "TUNED ON WHAT ACTUALLY CONVERTED."],
            ["THREE. THE COMPLIANCE CHECK. THE AGENTS ARE ARRANGED LIKE A",
             "COMPANY WITH ROLES AND A CHAIN OF COMMAND, AND ONE AGENT SITS OVER",
             "THE OUTPUT AND [[MARKS]] EVERY CALL AGAINST THE RULES."],
            ["THE RESULT, ONE BUSINESS EACH: FOURTEEN THOUSAND PEOPLE SERVED A",
             "DAY, ADD TO CART UP FIFTY PERCENT, AND CALL COMPLIANCE FROM SIXTY",
             "PERCENT TO [[NINETY EIGHT.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of a long queue of glowing white parcels of work backed up nose to "
                  "tail at one small service window in an empty black void, while the enormous "
                  "machine behind the window runs at full speed untouched, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Medium shot of a wide hatch open in the flat face of a machine in an empty "
                  "black void, absorbing a heavy stream of identical repeat glowing white "
                  "parcels of work as they arrive so that none of them reach the rooms beyond, "
                  "and the whole lower half of the frame empty solid black."),
            plate("Close shot of a large painted lens lowered over one glowing white parcel of "
                  "work in an empty black void, reading it and leaving it visibly brighter than "
                  "when it arrived as it continues along the belt, and the whole lower half of "
                  "the frame empty solid black."),
            plate("Medium shot of a heavy measuring drum in an empty black void pressing a "
                  "compliance mark onto every outgoing glowing white parcel of work, the marked "
                  "parcels leaving in one long even row, and the whole lower half of the frame "
                  "empty solid black."),
            plate("Wide shot of an absorbing hatch, a brightening lens and a compliance drum all "
                  "lit together across one continuous machine floor floating in an empty black "
                  "void, the service window queue completely gone, and the whole lower half of "
                  "the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
    {
        "slug": "noir-pain-roster",
        "slug_line": "Rostering and HR load",
        "board": None,
        "slides": [
            ["SEVENTY PERCENT OF YOUR OPS MANAGER GOING INTO THE ROSTER?",
             "YOU NEED THESE [[THREE AUTOMATIONS]] ASAP."],
            ["ONE. THE SOP WRITER. THE REPEATING HR JOBS ARE MAPPED ONCE, THEN",
             "AN AGENT DRAFTS THE PROCEDURE DOCUMENTS ITSELF, RUNNING ON [[YOUR",
             "OWN SERVERS]] SO THE STAFF DATA NEVER LEAVES THE SITES."],
            ["TWO. THE PAYROLL RUN. IT READS YOUR HOURS WITHOUT BEING ABLE TO",
             "CHANGE THEM, APPLIES EVERY PAY RULE AS CODE RATHER THAN FROM",
             "MEMORY, AND PRINTS THE [[DAILY]] BILLINGS REPORT ON THE WAY",
             "THROUGH."],
            ["THREE. THE SCREENING AGENT. YOU WRITE THE QUESTIONS AND THE",
             "SCORING ONCE, A VOICE AGENT RUNS EVERY FIRST CALL TO THAT SAME",
             "SCRIPT, AND EACH CANDIDATE COMES BACK [[SCORED]] THE SAME WAY."],
            ["THE RESULT, ONE BUSINESS EACH: HR RUNNING LIVE ACROSS A HUNDRED",
             "AND THIRTY PEOPLE, SIX HOURS OF PAYROLL DONE IN TEN SECONDS, AND",
             "SCREENING RUNNING LIVE WITH [[REAL CANDIDATES.]]"],
            ["TAKE THE AI READINESS QUIZ AND SEE",
             "WHERE [[YOUR BUSINESS STANDS.]]"],
        ],
        "annotations": [[], [], [], [], [], []],
        "plates": [
            plate("Wide shot of one faceless silhouette working alone at an enormous wall-sized "
                  "rota board of small glowing white cards in an empty black void with no floor "
                  "and no ground plane anywhere, moving the cards by hand while every other "
                  "machine in the frame sits dark and idle, nothing beneath either of them but "
                  "empty black, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a wall-sized rota board in an empty black void filling itself, "
                  "its small glowing white cards sliding into their slots on their own across "
                  "three separate identical boards standing side by side, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Medium shot of a tall bank of iron levers throwing themselves in sequence "
                  "with nobody at them in an empty black void, thin cards feeding down through "
                  "the mechanism and emerging as one clean sheet, and the whole lower half of "
                  "the frame empty solid black."),
            plate("Medium shot of a narrow gate at the head of a conveyor belt in an empty black "
                  "void, weighing and tagging each arriving glowing white parcel of work as it "
                  "passes through, and the whole lower half of the frame empty solid black."),
            plate("Wide shot of a self-filling rota board, a bank of self-throwing levers and a "
                  "weighing gate all lit together across one continuous machine floor floating "
                  "in an empty black void, no figure anywhere in the frame, and the whole lower "
                  "half of the frame empty solid black."),
            plate("Wide shot of a calm upright faceless silhouette kneeling and seating a "
                  "brilliant glowing core into its housing at the centre of a sliced-open "
                  "building floating in an empty black void, the light re-threading every room, "
                  "and the whole lower half of the frame empty solid black."),
        ],
    },
]
