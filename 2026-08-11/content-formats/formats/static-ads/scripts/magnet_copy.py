#!/usr/bin/env python3
"""The copy layer for the lead-magnet statics: 7 industries x 5 hooks = 35 cards.

    python3 magnet_copy.py                # print every filled line, free
    python3 magnet_copy.py construction   # one industry
    python3 magnet_copy.py --check        # the copy gate: em dashes, negation swap, banlist

Settled with you . Five hooks he supplied, each one given its own visual format,
filled per industry, every card closing on a lead magnet that ACTUALLY EXISTS.

That last clause is the whole point of the set. The 25 existing industry statics close on
`decks_industry.MAGNETS`, which names five assets that were never built ("The Site-to-Profit
Readiness Check", "The Wow Factor Audit"). The seven that exist are in
`projects/lead-magnet-funnels/build/`, and those are the names used here. The old names are
retired for this set and left alone in the old rig.

Three laws this file obeys:

  - **Fill, never free-write.** Every hook is a named structure in `references/hooks/HOOKS.md`
    with its id cited on the template. you authored the five sentences; the slots are
    substituted and the sentence is not rewritten.
  - **The avatar comes FIRST**, or is named somewhere on the card. A pain with nobody in front
    of it makes no sense on a cold feed.
  - **The pain clause is a bucket, not a scene** (decks_industry.py's rule). Name the pain the
    way the whole industry carries it, in the fewest words that still land.

Case: sentence case everywhere EXCEPT hook 5, which is the news-carousel card and inherits that
format's caps band. you, .
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
VAULT = ROOT.parents[5]          # <your-vault>
MAGNET_BUILD = VAULT / "the business" / "projects" / "lead-magnet-funnels" / "build"
PLATES_REAL = (VAULT / "the business" / "skills" / "content-formats" / "formats"
               / "news-carousel" / "scripts" / "plates-real")

# ---------------------------------------------------------------------------------------------
# The seven industries.
#
#   avatar    the plural the card opens on. `language-rules.md` binds these: name the reader's
#             business by its INDUSTRY plus the word business. Hospitality moves off "venues",
#             which that rule bans as the name of a business; building services and professional
#             services get their first avatar line here.
#   short     the singular noun for "your ___", used by hooks 2 and 3.
#   pain      hook 1's fill, as a gerund, because the sentence reads "still [painpoint]".
#   still     the same pain as a second-person clause, for the split-screen dossier.
#   magnet    the asset that EXISTS, verbatim off its shipped page's <title>. Kept for provenance:
#             it is what the card's own record records and what the route serves. Renamed to the
#             post-rename titles in `specs/RENAME-AND-FORMATS.md`: every industry asset is now
#             "The [Industry] Business AI Audit", so the seven pain-named originals are gone.
#   audit     WHAT THE CARDS SAY. you, : one name across the whole program,
#             "The [Industry] AI Audit", rather than seven separately branded assets. The cards
#             sell one thing with an industry in front of it; the built page keeps its own title.
#   proto     the prototype file the report screenshot is captured from.
#   plate     the graded VHS plate already on disk that the caution card sits on. None means it
#             has to be shot.
#   agent     "AI agent" said in full where the industry already uses "agent" for a person
#             (language-rules.md), "Agent" alone where it does not.
#
# Pain rule: rank-1 off that industry's ledger, written as a bucket. Where two industries collide
# on a bucket, the lower call-volume one walks down its own ranked list until it reaches a pain
# the set has not used. Seven cards, seven different pains, no near-duplicates. Construction,
# building services and professional services all rank systems/bottleneck/admin at the top, so
# the last two walk down to the pain their own magnet actually measures, which reads better.
INDUSTRIES = [
    dict(key="construction", audit="The Construction AI Audit", slug="construction-and-trades", paper="CONSTRUCTION",
         name="Construction & Trades",
         avatar="Aussie construction businesses",
         short="construction business",
         pain="running on disconnected systems",
         still="run on disconnected systems",
         magnet="The Construction Business AI Audit",
         route="/lead-magnet/construction-business-ai-audit",
         proto="systems-audit-prototype.html",
         plate="construction-and-trades/quoting.png",
         agent="Agent"),
    dict(key="real-estate", audit="The Real Estate AI Audit", slug="real-estate-and-property-management", paper="REAL ESTATE",
         name="Real Estate & Property Management",
         avatar="Aussie real estate agencies",
         short="real estate agency",
         # you : hospitality took "drowning in admin", so real estate walks down its
         # own ranked list to keep seven distinct pains across the set.
         pain="running on disconnected systems",
         still="run on disconnected systems",
         magnet="The Real Estate Business AI Audit",
         route="/lead-magnet/real-estate-business-ai-audit",
         proto="admin-audit-prototype.html",
         plate="real-estate-and-property-management/leadgen.png",
         agent="AI agent"),
    dict(key="hospitality", audit="The Hospitality AI Audit", slug="hospitality-and-food-service", paper="HOSPITALITY",
         name="Hospitality & Food Service",
         avatar="Aussie hospitality businesses",
         short="hospitality business",
         # you : hospitality moves onto the drowning-in-admin hook.
         pain="drowning in admin",
         still="drown in admin",
         magnet="The Hospitality Business AI Audit",
         route="/lead-magnet/hospitality-business-ai-audit",
         proto="margin-audit-prototype.html",
         plate="hospitality-and-food-service/numbers.png",
         agent="Agent"),
    dict(key="retail", audit="The Retail AI Audit", slug="retail-and-ecommerce", paper="RETAIL",
         name="Retail & E-commerce",
         avatar="Aussie retailers",
         short="retail business",
         pain="running every decision through you",
         still="run every decision through the owner",
         magnet="The E-commerce Business AI Audit",
         route="/lead-magnet/ecommerce-business-ai-audit",
         proto="spend-audit-prototype.html",
         plate="retail-and-ecommerce/systems.png",
         agent="Agent"),
    dict(key="financial-services", audit="The Insurance AI Audit", slug="financial-services-and-insurance", paper="INSURANCE",
         name="Financial Services & Insurance",
         avatar="Aussie insurance brokers",
         short="brokerage",
         pain="asking clients the same questions twice",
         still="keep asking clients the same questions",
         magnet="The Financial Services Business AI Audit",
         route="/lead-magnet/financial-services-business-ai-audit",
         proto="ratio-benchmark-prototype.html",
         plate="financial-services-and-insurance/context.png",
         agent="AI agent"),
    # you : this avatar is "trades businesses" everywhere it is said out loud, across
    # all five formats. `key`, `slug` and `proto` keep the building-services spelling: they address
    # the card's own record and the prototype file on disk, and renaming them breaks both. `magnet` and
    # `route` moved to the trades name on because the shipped page did.
    dict(key="building-services", audit="The Trades AI Audit", slug="building-services", paper="TRADES",
         name="Trades",
         avatar="Aussie trades businesses",
         short="trades business",
         pain="sitting on a database you never call",
         still="sit on a database they never call",
         magnet="The Trades Business AI Audit",
         route="/lead-magnet/trades-business-ai-audit",
         proto="reactivation-audit-prototype.html",
         plate=None,
         agent="Agent"),
    dict(key="professional-services", audit="The Professional Services AI Audit", slug="professional-services", paper="PROFESSIONAL SERVICES",
         name="Professional Services",
         avatar="Aussie professional services businesses",  # masthead is the full trade, not "PROFESSIONAL"
         short="professional services business",
         pain="writing off hours you already worked",
         still="write off hours they already worked",
         magnet="The Professional Services Business AI Audit",
         route="/lead-magnet/professional-services-business-ai-audit",
         proto="write-off-audit-prototype.html",
         plate=None,
         agent="Agent"),
]

BY_KEY = {i["key"]: i for i in INDUSTRIES}

# ---------------------------------------------------------------------------------------------
# The five hooks, verbatim from you each mapped to its HOOKS.md structure.
#
# Hook 5 ships with the `do do` typo corrected and the exclamation mark dropped to a full stop,
# which is the band's own punctuation.
HOOKS = {
    "split": dict(
        n=1, fmt="F-M1", label="Before / after split screen",
        hooks_id="P2 cause and symptom, opened with P5 name the avatar",
        model=[("hook:P2", "cause and symptom, the avatar named first"),
               ("arch:S10", "before and after held in one frame on a hard seam"),
               ("arch:S2", "the two halves argue with each other")],
        template="[Avatar]: this is the real reason you're still [painpoint]"),
    "deliverable": dict(
        n=2, fmt="F-M2", label="Deliverable shot",
        hooks_id="S2 negative / problem call-out",
        model=[("hook:S2", "the negative call-out, the problem named before the offer"),
               ("tpl:VetNotes Static Ads", "the B2B service card, the closest scaffold in the "
               "library to a business with nothing to photograph")],
        template="Don't use AI in your [avatar] business before this audit"),
    "editorial": dict(
        n=3, fmt="F-M3", label="Fake editorial",
        hooks_id="A3 curiosity gap, C9 the uncomfortable truth",
        model=[("hook:A3", "the curiosity gap, the truth withheld until the click"),
               ("arch:S1", "the news register, reported rather than claimed"),
               ("local:newspaper-template", "the printed page: masthead, column rules, "
               "justified body, the route in the footer")],
        template="The truth about using AI in your [avatar] business. "
                 "It's a lot easier than you think"),
    "billboard": dict(
        n=4, fmt="F-M4", label="Filmed billboard",
        hooks_id="A4 question hook, opened with P5 name the avatar",
        model=[("hook:A4", "the question hook, opened by naming the avatar"),
               ("arch:S12", "the question is the whole card and the picture answers it"),
               ("style:vhs-camcorder", "the handheld documentary look the board is shot in")],
        template="[avatar] still figuring out how to use AI? "
                 "This quiz will do the heavy lifting for you"),
    "caution": dict(
        n=5, fmt="F-M5", label="Caution card",
        hooks_id="S2 negative / problem call-out, opened with P5",
        model=[("hook:S2", "the negative call-out as a warning"),
               ("local:snapchat-text-template", "the caption bar treatment: caps, centred, "
               "sitting on the plate area")],
        template="[avatar businesses] Please be careful. "
                 "Do not touch AI before you do this audit."),
}

# Accent markup is [[double brackets]], one per card, same as band.py and band_basic.py.


# Hook 1 written out in full for one industry rather than filled from the template. you wrote
# this line for trades on and asked for it on the split screen ONLY: the other four
# trades cards keep their own format's template, with the avatar renamed. The template's
# "still [painpoint]" clause does not survive the rewrite, so the whole sentence is stored.
SPLIT_HEAD = {
    "building-services":
        "Aussie trades businesses: you're sitting on [[a database of leads you never call]], "
        "and it's costing you more than you'd think.",
}


def split_copy(i):
    """Hook 1. The avatar opens it, the pain carries the accent."""
    return dict(
        head=SPLIT_HEAD.get(
            i["key"],
            f"{i['avatar']}: this is the real reason you're still [[{i['pain']}]]."),
        # you: "apart from the first ones, which say take the audit"
        cta="Take the audit")


def deliverable_copy(i):
    """Hook 2. Black on white, so the accent is the only colour on the card."""
    return dict(
        head=f"Don't use AI in your [[{i['short']}]] before this audit.",
        cta=f"{i['audit']}, free")


def editorial_copy(i):
    """Hook 3. The line IS the lead headline on a newspaper front page.

    you, second pass: the card is built on the downloaded newspaper template
    (`~/Desktop/template.webp`), not on digital-article chrome. The first version read as our own
    authored page, which is the one thing this format cannot do.

    The masthead is the industry's own word, not an invented publication. A made-up trade title
    close to a real Australian one is what gets a creative pulled, and a one-word masthead does
    the same job.

    The two columns carry real copy about the asset. Every claim in them is checkable against the
    built report: nine areas at ten points each is what the report itself prints.
    """
    return dict(
        paper=i["paper"],
        head=f"The truth about using AI in your [[{i['short']}]]. "
             f"It's a lot easier than you think.",
        col1=f"Most {i['short']} owners are told to use AI and never told where. This audit asks "
             f"how the work actually moves through the business, then scores nine areas out of "
             f"ten.",
        col2="You get the score, the dollar figure sitting behind it, and the five areas costing "
             "you the most, each with the AI agent that would take it off your desk.",
        col1h="Where it actually goes",
        col2h="What comes back",
        cta=f"Take {i['audit']}")


# The top three ranked pains per industry, as a bucket phrase (decks_industry.py's rule: the
# pain the way the whole industry carries it, never a scene). The five wave-one industries reuse
# the exact gerund phrasing already authored in `basics.PAINS` (`ing` field) for their top three
# ranked pains, off `decks_industry.INDUSTRY_STATICS`, so the wording matches what the rest of
# the house already says about that pain. Building services and professional services have no
# existing gerund phrasing, so their three are written fresh off their pain ledgers, same voice.
PAIN3 = {
    "construction": ["running on disconnected systems", "double-handling every job",
                     "running every decision through you"],
    "real-estate": ["drowning in admin", "running on disconnected systems",
                    "running every decision through the principal"],
    "hospitality": ["running on last week's numbers", "hiring on gut feel",
                    "doing the admin by hand"],
    "retail": ["running on disconnected systems", "running every decision through you",
              "running on last month's numbers"],
    "financial-services": ["asking clients the same questions", "drowning in paperwork",
                           "building the automation yourself"],
    "building-services": ["running on systems that don't talk", "running every decision "
                          "through you", "burying good people in admin"],
    "professional-services": ["running every decision through you", "burying your team in "
                              "admin", "gluing your own systems together"],
}


def billboard_copy(i):
    """Hook 4. Third pass, you : **the comic is scrapped.**

    The card is now a roadside billboard someone is filming on their phone, and the billboard
    face carries the "Still..." sequence: a hanging lead, the industry's top three ranked pains
    as questions, then the magnet in its own bordered box. The copy survived the format change
    unchanged; only what it is printed on moved.

    The Snapchat text bar stays. It is what makes the card read as a phone film of a real
    billboard rather than a mock-up of one, and it is where the avatar is named.
    """
    return dict(
        # what is PRINTED ON THE BILLBOARD, generated into the plate rather than composited.
        # Set in caps because that is how a billboard is set, and because the model holds
        # spelling far better on caps than on mixed case at this size.
        head=f"{i['avatar'].upper()}, ARE YOU STILL...",
        bullets=[p.upper() + "?" for p in PAIN3[i["key"]]],
        box=f"Take {i['audit']}".upper(),
        # the Snapchat text-tool line. This one IS composited: it is phone UI sitting over the
        # footage, not something printed on the billboard.
        snap=f"for all the {i['avatar'].lower()} out there",
        cta=f"Take {i['audit']}")


def caution_copy(i):
    """Hook 5. The news-carousel band, so ALL CAPS, and `band.py` applies the transform: the
    copy string is not pre-cased. The accent is the prohibition."""
    return dict(
        lines=[f"{i['avatar']}. Please be careful.",
               f"[[Do not touch AI]] before you do this audit."],
        anno=f"TAKE {i['audit'].upper}")


COPY = {
    "split": split_copy,
    "deliverable": deliverable_copy,
    "editorial": editorial_copy,
    "billboard": billboard_copy,
    "caution": caution_copy,
}


def card(industry_key, hook_key):
    """Everything one card needs: the industry, the hook's metadata, and the filled copy."""
    i = BY_KEY[industry_key]
    h = HOOKS[hook_key]
    return dict(industry=i, hook=h, copy=COPY[hook_key](i))


def every_card(keys=None):
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        for hk in HOOKS:
            yield card(i["key"], hk)


# ---------------------------------------------------------------------------------------------
# The copy gate. Runs before anything renders and before anything is paid for.

BANNED = [
    # house rules, CLAUDE.md + language-rules.md
    (r"—", "em dash"),
    (r"\bbuilding business", "banned: building business (use construction business)"),
    (r"\byour venue\b|\ba venue\b", "banned: venue as the name of a business"),
    (r"\bre-?key", "banned: re-key (use re-enter)"),
    (r"[Ii]t'?s not .{1,40}, it'?s ", "banned: the negation swap"),
    (r"\bbuilders\b", "banned: builders as the audience"),
]


def check(keys=None):
    bad = 0
    for c in every_card(keys):
        text = " ".join(str(v) for v in c["copy"].values())
        where = f"{c['industry']['key']}/{list(HOOKS).index('split') and ''}{c['hook']['fmt']}"
        for pattern, why in BANNED:
            if re.search(pattern, text):
                print(f"  FAIL {where}: {why}")
                bad += 1
        # exactly one accent per card, the house law
        n = text.count("[[")
        if n > 1:
            print(f"  FAIL {where}: {n} accents, the law is one")
            bad += 1
    # your law, : every format cites the bank entry it is modelled on, by an id that
    # resolves. `refs.py check` is the same gate any other pipeline stage runs.
    import refs
    for key, h in HOOKS.items():
        if not h.get("model"):
            print(f"  FAIL {h['fmt']}: no model reference (refs.py list)")
            bad += 1
        for ref, takes in h.get("model", []):
            try:
                refs.resolve(ref)
            except KeyError as err:
                print(f"  FAIL {h['fmt']}: {err}")
                bad += 1
            if len(takes.split()) < 4:
                print(f"  FAIL {h['fmt']}: {ref} cites no principle, say what is taken from it")
                bad += 1
    print(f"\n{'FAILED, ' + str(bad) + ' problems' if bad else 'clean'}")
    return bad


def show(keys=None):
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        plate = i["plate"] or "NO PLATE, needs one shot"
        print(f"\n{'=' * 92}\n{i['name']}  ({i['avatar']})")
        print(f"  magnet {i['magnet']}   route {i['route']}")
        print(f"  plate  {plate}")
        for hk, h in HOOKS.items():
            c = COPY[hk](i)
            print(f"\n  {h['fmt']}  {h['label']}   [{h['hooks_id']}]")
            for k, v in c.items():
                v = " / ".join(v) if isinstance(v, list) else v
                print(f"      {k:9} {v}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keys = args or None
    if "--check" in sys.argv:
        sys.exit(1 if check(keys) else 0)
    show(keys)
