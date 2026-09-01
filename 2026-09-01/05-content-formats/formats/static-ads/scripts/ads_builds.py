#!/usr/bin/env python3
"""The Build Breakdown statics (F7, industry-targeted, tool-named).

Five single cards, one per industry, written . They render on the same rig as
`ads.py`: `build.py` falls through to `BUILD_ADS` when a slug is not in `ADS`.

    python3 build.py bb-construction-static          # one card, free
    python3 build.py                                 # every card in both modules

THE JOB THESE DO

They are the top of the funnel for the Build Breakdown series. The F8 carousel shows the
whole system as a diagram and the F5 carousel teaches three of them; this card states ONE
system in one sentence, names what it is built out of, and lands the result at
one-business scope. Somebody who scrolls past it has still learned that the thing is
buildable and roughly what out of, which is the argument the corpus says this market has
never been given.

They are deliberately NOT the section 1a industry pain cards in
`formats/news-carousel/scripts/decks_industry.py`. Those 25 carry no figure and no tool by
design, because their template's subject is plural and industry-wide. These carry both,
because every sentence here names one business.

The naming gate is the one in
`projects/content-engine/ideas/build-breakdown-carousels/PLAN.md` section 3.
"""

BUILD_ADS = [
    {
        "slug": "bb-construction-static",
        "structure": "HOOKS.md A1, specificity plus proof. The stack is the hook.",
        "template": "thesis",
        "persona": "general, construction and trades",
        "angle": "A3",
        "offer": "house",
        "kicker": "Construction & Trades",
        "source": "Hub case 038, one business, ~8 weeks. Construction playbook pain 1, "
                  "59 calls, the heaviest weighted pain in the pack. Tools clear the "
                  "PLAN.md section 3 naming gate.",
        "lead": [
            "THE JOB GOES INTO HUBSPOT ONCE AND XERO, PROCORE AND",
            "THE SCHEDULE ALL READ IT. ONE BUILDER GOT THERE IN",
            "[[EIGHT WEEKS.]]",
        ],
        "lines": [
            "THE JOB GOES INTO HUBSPOT ONCE, AND XERO, PROCORE AND THE",
            "SCHEDULE ALL READ IT INSTEAD OF BEING TYPED INTO ONE BY ONE.",
            "THAT IS THE WHOLE BUILD, AND ONE AUSTRALIAN BUILDER HAD IT",
            "RUNNING IN [[EIGHT WEEKS.]]",
        ],
        "cta": "Take the Site-to-Profit Readiness Check.",
    },
    {
        "slug": "bb-real-estate-static",
        "structure": "HOOKS.md A1, specificity plus proof. The cost of the opposite is the hook.",
        "template": "thesis",
        "persona": "general, real estate and property management",
        "angle": "A3",
        "offer": "house",
        "kicker": "Real Estate",
        "source": "Real estate playbook pain 2, one agency's own figure ($150,000 a year "
                  "on the fragmented stack), raised in 26 of 27 calls. Build shape from "
                  "Hub case 070.",
        "lead": [
            "ONE PROPERTY RECORD, READ BY PROPERTYME, AGENTBOX AND",
            "THE PORTAL. ONE AGENCY PAID [[$150,000 A YEAR]] FOR THE",
            "OPPOSITE.",
        ],
        "lines": [
            "ONE PROPERTY RECORD, AND PROPERTYME, AGENTBOX AND THE PORTAL",
            "ALL READ IT. THE AGENCY THAT HAS NOT BUILT THAT YET IS PAYING",
            "A PERSON TO BE THE INTEGRATION, AND ONE OF THEM PUT THAT COST",
            "AT [[$150,000 A YEAR.]]",
        ],
        "cta": "Take the AI-Ready Agency Score.",
    },
    {
        "slug": "bb-retail-static",
        "structure": "HOOKS.md A1, specificity plus proof. The before and after is the hook.",
        "template": "thesis",
        "persona": "general, retail and e-commerce",
        "angle": "A3",
        "offer": "house",
        "kicker": "Retail & E-commerce",
        "source": "Hub case 046, one business: staff time 16 hrs/week to 16 hrs/month, "
                  "about $1,000/month of apps replaced. Retail playbook pain 1, raised in "
                  "25 examples.",
        "lead": [
            "AN ORDER LANDS IN SHOPIFY AND NOBODY TOUCHES IT AGAIN",
            "UNTIL SOMETHING IS WRONG. ONE STORE WENT TO",
            "[[16 HOURS A MONTH.]]",
        ],
        "lines": [
            "AN ORDER LANDS IN SHOPIFY AND NOBODY TOUCHES IT AGAIN UNTIL",
            "SOMETHING IS ACTUALLY WRONG WITH IT. STOCK, THE WAREHOUSE AND",
            "XERO ALL READ THE SAME RECORD. ONE STORE WENT FROM 16 HOURS A",
            "WEEK OF THAT WORK TO [[16 HOURS A MONTH.]]",
        ],
        "cta": "Take the Retail Ops AI Readiness Check.",
    },
    {
        "slug": "bb-finance-static",
        "structure": "HOOKS.md A1, specificity plus proof. The timeline collapse is the hook.",
        "template": "thesis",
        "persona": "general, financial services and insurance",
        "angle": "A3",
        "offer": "house",
        "kicker": "Financial Services",
        "source": "Hub case 026, one business: fact-finding cut from 2 to 3 weeks to days. "
                  "Financial services playbook pain 1, 19 pain examples, the highest "
                  "weighted category at 41%.",
        "lead": [
            "EVERY CALL, TEXT AND EMAIL ON ONE CLIENT TIMELINE,",
            "WRITTEN BY THE MACHINE. ONE FIRM CUT FACT-FINDING TO",
            "[[DAYS.]]",
        ],
        "lines": [
            "EVERY CALL, TEXT AND EMAIL LANDS ON ONE CLIENT TIMELINE, AND",
            "THE FILE NOTE WRITES ITSELF OFF THE CALL. THE BRIEF STOPS",
            "REPEATING THEMSELVES, AND AT ONE FIRM THE FACT-FIND WENT FROM",
            "THREE WEEKS TO [[DAYS.]]",
        ],
        "cta": "Take the Broker and Adviser AI Readiness Check.",
    },
    {
        "slug": "bb-health-static",
        "structure": "HOOKS.md A1, specificity plus proof. The named loss is the hook.",
        "template": "thesis",
        "persona": "general, health, medical and allied health",
        "angle": "A3",
        "offer": "house",
        "kicker": "Health & Allied Health",
        "source": "Hub cases 033 and 062, two independent records of the same pattern, both "
                  "one business. Health playbook pain 6, 20,000 untouched leads at one "
                  "clinic group. The health discovery pack is THIN at 6 calls, so nothing "
                  "here is stated at industry scope.",
        "lead": [
            "THE PHONE IS ANSWERED ON THE FIRST RING AND THE BOOKING",
            "WRITES ITSELF INTO THE DIARY. ONE CLINIC ENDED",
            "[[MISSED CALLS.]]",
        ],
        "lines": [
            "THE PHONE IS ANSWERED ON THE FIRST RING, THE REAL DIARY IS READ",
            "BEFORE A TIME IS OFFERED, AND THE BOOKING WRITES ITSELF IN.",
            "ANYTHING CLINICAL STILL GOES TO A PERSON. ONE CLINIC ENDED",
            "[[MISSED CALLS]] ENTIRELY.",
        ],
        "cta": "Take the Practice Pulse Check.",
    },
]
