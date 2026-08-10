#!/usr/bin/env python3
"""Hook audition rig for the F5 news carousel.

    python3 audition.py                # render every candidate into out2/audition-<set>/

Renders candidate COVER slides only, one card each, so a hook architecture can be picked
before a whole deck is written. Every candidate is a FILL of a named structure in
`references/hooks/HOOKS.md`, and `ref` records the exact entry and line number so the
provenance is checkable rather than asserted.

The carousel formula this auditions against (the operator, 2026-07-31):
    curiosity gap through pain agitation  ->  education  ->  CTA to the lead magnet
The lead magnet is the AI Readiness quiz. The cover is the only slide being auditioned.

Avatar rule (the operator, 2026-07-31): never call a prospect an "operator". Name the avatar:
"your logistics company", "a transport business", "[industry] business owner".
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "static-ads" / "scripts"))
from band import render_card  # noqa: E402

SET = "audition-log-leads"

# Persona LOG-01 (leads leak) x angle A7 x house. Pain generalised from "email leads" to
# "leads" per the operator. Every line is one sentence, one accent, avatar named.
CANDIDATES = [
    {
        "id": "h01-howto",
        "ref": "V9 educational teach opener, HOOKS.md:457 "
               "(\"Builders, here are the three jobs you should automate before anything else\")",
        "lines": ["HOW TO STOP LOSING LEADS", "IN YOUR [[LOGISTICS COMPANY.]]"],
    },
    {
        "id": "h02-negative",
        "ref": "S2 Negative / problem call-out, HOOKS.md:66 "
               "(\"Here's why [their outcome] is [slipping]\")",
        "lines": ["HERE IS WHY YOUR LOGISTICS COMPANY",
                  "LOSES [[LEADS YOU PAID FOR.]]"],
    },
    {
        "id": "h03-until",
        "ref": "A3 Curiosity gap, HOOKS.md:88 "
               "(\"Most think they have good (result) until they...\")",
        "lines": ["MOST LOGISTICS OWNERS THINK EVERY LEAD",
                  "GETS ANSWERED, [[UNTIL THEY COUNT THEM.]]"],
    },
    {
        "id": "h04-question",
        "ref": "A4 Question hook, HOOKS.md:93, asked so the honest answer is yes (E-063)",
        "lines": ["COULD YOU NAME EVERY LEAD YOUR",
                  "LOGISTICS COMPANY GOT [[LAST WEEK?]]"],
    },
    {
        "id": "h05-insider",
        "ref": "A5 The Insider, HOOKS.md:98 "
               "(\"Here's what nobody tells you about the algorithm\")",
        "lines": ["HERE IS WHAT NOBODY TELLS YOU ABOUT",
                  "LEADS IN A [[TRANSPORT BUSINESS.]]"],
    },
    {
        "id": "h06-warning",
        "ref": "List 2 #6, HOOKS.md:181 "
               "(\"What no one warns you about before you (action)\")",
        "lines": ["WHAT NOBODY WARNS YOU ABOUT BEFORE",
                  "YOU BUY MORE [[LOGISTICS LEADS.]]"],
    },
    {
        "id": "h07-measuring",
        "ref": "List 2 #17, HOOKS.md:192 (\"You're measuring the wrong thing\")",
        "lines": ["YOUR LOGISTICS COMPANY COUNTS THE LEADS",
                  "IT WINS AND [[NEVER THE ONES IT DROPS.]]"],
    },
    {
        "id": "h08-contrarian",
        "ref": "S1 The Contrarian claim, HOOKS.md:60 "
               "(\"Stop [the thing everyone tells you to do]\")",
        "lines": ["STOP BUYING LEADS FOR YOUR LOGISTICS",
                  "COMPANY, YOU ALREADY [[HAVE ENOUGH.]]"],
    },
    {
        "id": "h09-things",
        "ref": "List 1 #7, HOOKS.md:159 (\"5 things no one told me about (topic)\")",
        "lines": ["THREE THINGS NOBODY TELLS YOU",
                  "ABOUT LEADS IN [[LOGISTICS.]]"],
    },
    {
        "id": "h10-specific",
        "ref": "A1 Specificity + proof, HOOKS.md:76. Grounded in LOG-01's verbatim "
               "(\"We probably miss three or four emails a week\"), scoped to one business",
        "lines": ["ONE TRANSPORT BUSINESS MISSED [[THREE",
                  "OR FOUR LEADS]] EVERY SINGLE WEEK."],
    },
    {
        "id": "h11-fortune",
        "ref": "B1 The Fortune Teller, HOOKS.md:112 "
               "(\"This is going to change how you X forever\")",
        "lines": ["YOUR COMPETITORS WILL ANSWER EVERY",
                  "LEAD [[BEFORE YOU EVEN SEE IT.]]"],
    },
    {
        "id": "h12-consistent",
        "ref": "List 1 #19, HOOKS.md:171 "
               "(\"If you've been consistent at (topic) but not seeing results\")",
        "lines": ["IF YOU ARE PAYING FOR LEADS AND THE",
                  "PHONE STILL [[FEELS QUIET.]]"],
    },
]


if __name__ == "__main__":
    out = ROOT / "out2" / SET
    picked = [c for c in CANDIDATES if not sys.argv[1:] or c["id"] in sys.argv[1:]]
    for c in picked:
        report = render_card(c["lines"], out / f"{c['id']}.png")
        print(f"{c['id']:16} {report}")
    print("done")
