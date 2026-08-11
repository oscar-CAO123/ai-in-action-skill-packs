#!/usr/bin/env python3
"""Candidate-facing F7.1 type-led statics (audience A, the entry-level role entry tier).

Copy of record: `projects/content-engine/candidate-angles/BATCH-1-COPY.md`, units U1 and U4.
Free to render: no plate, no paid generation, ever (type-led/SKILL.md section 1).

Theme is `noir` (your display typeface 200 caps), matching every static the house currently ships and the
locked design system's display weight. Anton is legacy on this rig.

U1 IS RENDERED IN TWO VARIANTS. The authored hook claimed "MOST COMP SCI STUDENTS ARE
SCARED", and no source supports it: EVIDENCE.md section 14 records "no student-specific
research of any kind", and the only measured Australian figures come from "Young
Australians and the AI Workforce Transition" (Microsoft + KPMG + Anyway, n=1,029,
Australians aged 15 to 24, May 2026): 63 per cent think AI will be used to eliminate jobs,
47 per cent are worried about AI automating early-career tasks. Neither is comp-sci
students, and 47 per cent is not "most". So:

  u1a  keeps a quantity claim but moves it onto the sourced cohort and the sourced number.
  u1b  keeps the comp-sci avatar and drops the quantity claim entirely, refilling from
       HOOKS.md P1 (straight conditional call-out) instead of P3.

you picks one. The other gets deleted rather than kept as an alternate.

    python3 build_candidate.py            # renders all three to ../candidate/
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from band import render_card  # noqa: E402

OUT = Path(__file__).parent.parent / "candidate"

CARDS = [
    {
        "slug": "u1a-two-in-three",
        "unit": "U1",
        "structure": "HOOKS.md P3, most [avatars] + problem + cause",
        "audience": "comp sci and software students (avatar carried by targeting, not copy)",
        "source": ("Young Australians and the AI Workforce Transition, Microsoft + KPMG + "
                   "Anyway, n=1,029, Australians aged 15 to 24, May 2026. 63 per cent "
                   "believed AI would mostly eliminate jobs."),
        "lines": [
            "ALMOST TWO IN THREE YOUNG AUSTRALIANS THINK",
            "AI IS GOING TO WIPE OUT JOBS.",
            "IF YOU KNOW HOW TO USE IT PROPERLY,",
            "[[WE WANT TO HIRE YOU.]]",
        ],
    },
    {
        "slug": "u1b-no-stat",
        "unit": "U1",
        "structure": "HOOKS.md P1, straight conditional call-out",
        "audience": "comp sci and software students",
        "source": "No external figure. Nothing to verify.",
        "lines": [
            "ABOUT TO FINISH A COMP SCI DEGREE AND SCARED",
            "THERE IS NO JOB AT THE END OF IT?",
            "IF YOU KNOW HOW TO USE AI PROPERLY,",
            "[[WE WANT TO HIRE YOU.]]",
        ],
    },
    {
        "slug": "u4-until-you-realise",
        "unit": "U4",
        "structure": "HOOKS.md P2, cause and symptom",
        "audience": "students who think the job is gone",
        "source": ("the house's own entry band, $80,000 to $100,000. FIRM scope, EVIDENCE.md "
                   "section 7."),
        "lines": [
            "YOU THINK AI IS GOING TO REPLACE YOUR JOB, UNTIL YOU",
            "REALISE COMPANIES NEED SOMEONE TO",
            "[[HELP THEM USE IT PROPERLY.]]",
            "THAT PERSON GETS EIGHTY TO ONE HUNDRED THOUSAND TO START.",
        ],
    },
]


def main:
    OUT.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        png = OUT / f"{card['slug']}.png"
        fit = render_card(card["lines"], png, theme="noir")
        print(f"{card['unit']:<4} {card['slug']:<24} {fit}")


if __name__ == "__main__":
    main
