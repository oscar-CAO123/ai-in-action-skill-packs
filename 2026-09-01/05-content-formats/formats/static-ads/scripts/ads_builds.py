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
        "source": "A construction build case, one business. Construction playbook pain 1, "
                  "the heaviest weighted pain in the pack. Tools clear the "
                  "PLAN.md section 3 naming gate.",
        "lead": [
            "THE JOB GOES INTO HUBSPOT ONCE AND XERO, PROCORE AND",
            "THE SCHEDULE ALL READ IT. ONE BUILDER GOT THERE IN",
            "[[A FEW WEEKS.]]",
        ],
        "lines": [
            "THE JOB GOES INTO HUBSPOT ONCE, AND XERO, PROCORE AND THE",
            "SCHEDULE ALL READ IT INSTEAD OF BEING TYPED INTO ONE BY ONE.",
            "THAT IS THE WHOLE BUILD, AND ONE AUSTRALIAN BUILDER HAD IT",
            "RUNNING IN [[A FEW WEEKS.]]",
        ],
        "cta": "Take the Construction AI Check.",
    },
    {
        "slug": "bb-real-estate-static",
        "structure": "HOOKS.md A1, specificity plus proof. The cost of the opposite is the hook.",
        "template": "thesis",
        "persona": "general, real estate and property management",
        "angle": "A3",
        "offer": "house",
        "kicker": "Real Estate",
        "source": "Real estate playbook pain 2, one agency's own cost on the fragmented stack, "
                  "raised across the calls. Build shape from a real estate build case.",
        "lead": [
            "ONE PROPERTY RECORD, READ BY PROPERTYME, AGENTBOX AND",
            "THE PORTAL. ONE AGENCY PAID [[A HUGE BILL]] FOR THE",
            "OPPOSITE.",
        ],
        "lines": [
            "ONE PROPERTY RECORD, AND PROPERTYME, AGENTBOX AND THE PORTAL",
            "ALL READ IT. THE AGENCY THAT HAS NOT BUILT THAT YET IS PAYING",
            "A PERSON TO BE THE INTEGRATION, AND ONE OF THEM PUT THAT COST",
            "AT [[A HUGE BILL.]]",
        ],
        "cta": "Take the Real Estate AI Check.",
    },
    {
        "slug": "bb-retail-static",
        "structure": "HOOKS.md A1, specificity plus proof. The before and after is the hook.",
        "template": "thesis",
        "persona": "general, retail and e-commerce",
        "angle": "A3",
        "offer": "house",
        "kicker": "Retail & E-commerce",
        "source": "A retail build case, one business: staff time cut to a fraction, "
                  "and a monthly app bill replaced. Retail playbook pain 1, raised across the examples.",
        "lead": [
            "AN ORDER LANDS IN SHOPIFY AND NOBODY TOUCHES IT AGAIN",
            "UNTIL SOMETHING IS WRONG. ONE STORE WENT TO",
            "[[A FRACTION OF IT.]]",
        ],
        "lines": [
            "AN ORDER LANDS IN SHOPIFY AND NOBODY TOUCHES IT AGAIN UNTIL",
            "SOMETHING IS ACTUALLY WRONG WITH IT. STOCK, THE WAREHOUSE AND",
            "XERO ALL READ THE SAME RECORD. ONE STORE WENT FROM A FULL WEEK",
            "OF THAT WORK TO [[A FRACTION OF IT.]]",
        ],
        "cta": "Take the Retail AI Check.",
    },
    {
        "slug": "bb-finance-static",
        "structure": "HOOKS.md A1, specificity plus proof. The timeline collapse is the hook.",
        "template": "thesis",
        "persona": "general, financial services and insurance",
        "angle": "A3",
        "offer": "house",
        "kicker": "Financial Services",
        "source": "A financial services build case, one business: fact-finding cut from weeks to days. "
                  "Financial services playbook pain 1, the highest weighted category.",
        "lead": [
            "EVERY CALL, TEXT AND EMAIL ON ONE CLIENT TIMELINE,",
            "WRITTEN BY THE MACHINE. ONE FIRM CUT FACT-FINDING TO",
            "[[DAYS.]]",
        ],
        "lines": [
            "EVERY CALL, TEXT AND EMAIL LANDS ON ONE CLIENT TIMELINE, AND",
            "THE FILE NOTE WRITES ITSELF OFF THE CALL. THE BRIEF STOPS",
            "REPEATING THEMSELVES, AND AT ONE FIRM THE FACT-FIND WENT FROM",
            "WEEKS TO [[DAYS.]]",
        ],
        "cta": "Take the Broker and Adviser AI Check.",
    },
    {
        "slug": "bb-health-static",
        "structure": "HOOKS.md A1, specificity plus proof. The named loss is the hook.",
        "template": "thesis",
        "persona": "general, health, medical and allied health",
        "angle": "A3",
        "offer": "house",
        "kicker": "Health & Allied Health",
        "source": "Two health build cases, one business each, the same pattern. Health playbook "
                  "pain 6, untouched leads at one clinic group. The health discovery pack is "
                  "thin, so nothing here is stated at industry scope.",
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
        "cta": "Take the Health Practice AI Check.",
    },
]
