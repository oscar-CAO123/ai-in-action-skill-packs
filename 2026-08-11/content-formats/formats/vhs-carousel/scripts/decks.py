#!/usr/bin/env python3
"""Copy for the tape carousel. Edit here, re-run build.py.

A slide is a plate, a cast for the grade, a well and some words. The well can be `auto`,
in which case build.py finds the largest empty rectangle in the band you name and colours
the ink off whatever ground it lands on.

Fields:
    plate    file in scripts/plates/ (or a real shot dropped in the same folder)
    cast     grade arguments for this plate: sat, lift, soft, grain. Cast per plate, never
             once across the set. The reference measures 0.054 to 0.635 saturation.
    well     "auto" or [x, y, w, h] in percent of the frame
    band     which third auto should prefer: "top", "mid", "low"
    kind     hook | beat | stat | endcard, drives type scale and the contrast floor
    eyebrow  small label above the headline, optional
    head     the line that carries the message
    body     supporting sentence, optional
    align    left | center
"""

DECK = {
    "slug": "owner-bottleneck",
    "angle": "Owner Bottleneck. The owner is the constraint, and the constraint is not headcount.",
    "audience": "employer side, cross industry",
    "hook_structure": "P3, Most [avatars] [problem] because [cause] (references/hooks/HOOKS.md)",
    "sources": [
        "context/research-corpus/MARKET.md, 238 usable discovery calls across 208 businesses",
        "context/research-corpus/MARKET.md, Owner Bottleneck raised on 142 calls, weighted 335, "
        "third-ranked pain in the corpus",
    ],
}

SLIDES = [
    {
        "plate": "01-warm-low.png",
        "cast": {"sat": 1.30, "lift": 0.02, "soft": 2.2, "grain": 54},
        "well": "auto", "band": "low", "kind": "hook", "align": "left",
        "eyebrow": None,
        "head": "Most owners are still the bottleneck in their own business.",
        "body": "Every approval, every quote, every exception still lands on one desk.",
    },
    {
        "plate": "02-cool-top.png",
        "cast": {"sat": 0.85, "lift": 0.01, "soft": 2.0, "grain": 44},
        "well": "auto", "band": "top", "kind": "beat", "align": "left",
        "eyebrow": "THE SYMPTOM",
        "head": "The business stops when you do.",
        "body": "Two days away and the quotes queue up, the follow-ups go cold, the invoices wait.",
    },
    {
        "plate": "03-light-low.png",
        "cast": {"sat": 0.10, "lift": 0.06, "soft": 2.4, "grain": 48},
        "well": "auto", "band": "low", "kind": "beat", "align": "left",
        "eyebrow": "THE CAUSE",
        "head": "Nobody owns the systems full time.",
        "body": "The tools were bought. The workflows were half built. Then everyone went back "
                "to their real job.",
    },
    {
        "plate": "04-blue-top.png",
        "cast": {"sat": 1.05, "lift": 0.02, "soft": 2.2, "grain": 46},
        "well": "auto", "band": "top", "kind": "stat", "align": "left",
        "eyebrow": "238 DISCOVERY CALLS",
        "head": "142",
        "body": "owners raised the same constraint: themselves.",
    },
    {
        "plate": "05-black-mid.png",
        "cast": {"sat": 0.70, "lift": 0.00, "soft": 1.8, "grain": 40},
        "well": "auto", "band": "mid", "kind": "endcard", "align": "left",
        "eyebrow": "house PARTNERS",
        "head": "Hire the person who owns it.",
        "body": "yourdomain.example",
    },
]
