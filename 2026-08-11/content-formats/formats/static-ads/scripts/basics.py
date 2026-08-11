#!/usr/bin/env python3
"""The basic type-led statics: 25 pains x 6 shapes, sentence case, top anchored.

    python3 basics.py                 # render all 150
    python3 basics.py construction    # one industry
    python3 basics.py --shape question
    python3 basics.py --sheets        # contact sheet per shape

Settled with you . This is NOT the news-carousel band:

  - **Sentence case.** All caps is the F5 news-carousel doctrine and it carries the band keepers
    only. Every card here sets sentence case, which is also what separates them from the control
    at thumbnail size.
  - **Top anchored, left aligned, ragged right.** Taken off the Figma scaffolds, which all anchor
    type to the top and let it run ragged. The band anchors to the bottom and justifies flush.
  - **The avatar comes FIRST.** you, : a line like "still running seven systems that
    do not talk" with no avatar in front of it makes no sense on a cold feed. The industry opens
    every card.
  - **Fill, never free-write.** Every shape is a named template from `references/hooks/HOOKS.md`,
    cited by id, with the slots substituted. Nothing here is an invented line.
  - **Bucketed pains at a third-grade reading level.** The pain clause is the exact bucket from
    decks_industry.py, the canonical news-carousel wording: "do the admin by hand", never "the
    admin is still done by hand". Short words, one idea, said the way the industry carries it.
  - **One blue accent**, marked [[like this]], on the clause that carries the turn.

The pains are the 25 in decks_industry.py, which are the top five ranked pains in each of the five
industry playbooks. Nothing here invents a pain and nothing here carries a figure: the subject is
plural and industry-wide, so any number riding on it would read as an industry claim.
"""
import sys
from pathlib import Path

from band_basic import render

ROOT = Path(__file__).parent
OUT = ROOT / "out-basics"

# One entry per pain. The fields compose into all six shapes, so the copy stays specific to the
# pain rather than six unrelated lines per card.
#
#   who     the avatar, plural, naming the vertical (language-rules.md binds these)
#   pain    the pain as a second-person clause
#   ing     the same pain as a gerund, for the question hook
#   after   the resolved state, as a claim
#   wrong   the fix that owner reaches for instead, for contrarian and us vs them
#   before  the two states, for before and after
PAINS = [
 # ---- Construction and trades -------------------------------------------------
 ("construction", "quoting", dict(
  who="Aussie construction businesses", short="construction business",
  bucket="manually quote", ing="quoting by hand",
  wrong="hiring a faster estimator", cost="One person cannot quote any faster.",
  before="Quotes go out Monday", aft="Quotes go out today")),
 ("construction", "systems", dict(
  who="Aussie construction businesses", short="construction business",
  bucket="run on disconnected systems", ing="running on disconnected systems",
  wrong="buying another system", cost="You just added an eighth thing to check.",
  before="Seven systems. None of them talk.", aft="One stack. Nothing typed twice.")),
 ("construction", "double-handling", dict(
  who="Aussie construction businesses", short="construction business",
  bucket="double-handle every job", ing="double-handling every job",
  wrong="hiring someone to do the second entry", cost="You are paying twice for the same job.",
  before="Every job entered twice", aft="Every job entered once")),
 ("construction", "bottleneck", dict(
  who="Aussie construction businesses", short="construction business",
  bucket="run every decision through the owner", ing="running every decision through you",
  wrong="working longer hours", cost="The business still stops when you do.",
  before="Everything waits on you", aft="The job moves without you")),
 ("construction", "headcount", dict(
  who="Aussie construction businesses", short="construction business",
  bucket="hire more admin to grow", ing="hiring more admin to grow",
  wrong="hiring more admin staff", cost="You are scaling the problem.",
  before="More work, more admin", aft="More work, same office")),

 # ---- Real estate and property management -------------------------------------
 ("real-estate", "admin", dict(
  who="Aussie real estate agencies", short="agency",
  bucket="drown in admin", ing="drowning in admin",
  wrong="hiring a bigger admin team", cost="You are scaling the problem.",
  before="Agents buried in paperwork", aft="Agents back on listings")),
 ("real-estate", "systems", dict(
  who="Aussie real estate agencies", short="agency",
  bucket="run on disconnected systems", ing="running on disconnected systems",
  wrong="buying another CRM", cost="You just added another login.",
  before="A stack that does not talk", aft="One stack. Nothing typed twice.")),
 ("real-estate", "bottleneck", dict(
  who="Aussie real estate agencies", short="agency",
  bucket="run every decision through the principal", ing="running every decision through the principal",
  wrong="working longer hours", cost="The agency still stops when they do.",
  before="Everything waits on the principal", aft="The agency runs without them")),
 ("real-estate", "numbers", dict(
  who="Aussie real estate agencies", short="agency",
  bucket="guess at their own numbers", ing="guessing at your own numbers",
  wrong="waiting for the monthly report", cost="By the time it lands it is old.",
  before="Last month's numbers", aft="Today's numbers, today")),
 ("real-estate", "leadgen", dict(
  who="Aussie real estate agencies", short="agency",
  bucket="let leads go cold", ing="letting leads go cold",
  wrong="buying more leads", cost="The new ones go cold too.",
  before="Leads sit until someone is free", aft="Every lead answered same day")),

 # ---- Hospitality and food service --------------------------------------------
 ("hospitality", "numbers", dict(
  who="Aussie hospitality businesses", short="hospitality business",
  bucket="run on last week's numbers", ing="running on last week's numbers",
  wrong="waiting for the weekly report", cost="You are running service blind.",
  before="Last week's numbers", aft="Yesterday's, before service")),
 ("hospitality", "hiring", dict(
  who="Aussie hospitality businesses", short="hospitality business",
  bucket="hire on gut feel", ing="hiring on gut feel",
  wrong="doing more interviews", cost="A bad hire still costs you a season.",
  before="Hiring on a gut feel", aft="Hiring on evidence")),
 ("hospitality", "admin", dict(
  who="Aussie hospitality businesses", short="hospitality business",
  bucket="do the admin by hand", ing="doing the admin by hand",
  wrong="putting a part-timer on it", cost="You just moved the job to someone else.",
  before="Sunday night on the spreadsheet", aft="Done before Sunday")),
 ("hospitality", "tribal-knowledge", dict(
  who="Aussie hospitality businesses", short="hospitality business",
  bucket="keep the playbook in one person's head", ing="keeping the playbook in one head",
  wrong="writing more training docs", cost="Nobody reads them, and one person still knows everything.",
  before="It is all in one head", aft="It is all in the business")),
 ("hospitality", "presence", dict(
  who="Aussie hospitality businesses", short="hospitality business",
  bucket="be on site for it to run", ing="being on site for it to run",
  wrong="hiring a second manager", cost="You just bought another person to check on.",
  before="You have to be there", aft="It runs the same without you")),

 # ---- Retail and e-commerce ----------------------------------------------------
 ("retail", "systems", dict(
  who="Aussie retailers", short="retail business",
  bucket="run on disconnected systems", ing="running on disconnected systems",
  wrong="buying another platform", cost="Your staff still do the joining up.",
  before="Staff are the glue", aft="One stack. Nothing typed twice.")),
 ("retail", "bottleneck", dict(
  who="Aussie retailers", short="retail business",
  bucket="run every decision through the owner", ing="running every decision through you",
  wrong="working longer hours", cost="The floor still stops when you do.",
  before="Everything waits on you", aft="The floor runs without you")),
 ("retail", "numbers", dict(
  who="Aussie retailers", short="retail business",
  bucket="run on last month's numbers", ing="running on last month's numbers",
  wrong="waiting for the monthly report", cost="You are buying stock blind.",
  before="Last month's numbers", aft="This week's, this week")),
 ("retail", "admin", dict(
  who="Aussie retailers", short="retail business",
  bucket="do the admin by hand", ing="doing the admin by hand",
  wrong="putting a casual on the back office", cost="You just moved the job to someone else.",
  before="Admin done by hand", aft="Admin done overnight")),
 ("retail", "headcount", dict(
  who="Aussie retailers", short="retail business",
  bucket="hire more people to grow", ing="hiring more people to grow",
  wrong="hiring more staff to grow", cost="You are scaling the problem.",
  before="More sales, more staff", aft="More sales, same roster")),

 # ---- Financial services and insurance -----------------------------------------
 ("financial-services", "context", dict(
  who="Aussie insurance brokers", short="brokerage",
  bucket="keep asking clients the same questions", ing="asking clients the same questions",
  wrong="writing better file notes", cost="The next person still cannot find them.",
  before="Clients repeat themselves", aft="Nobody asks twice")),
 ("financial-services", "admin", dict(
  who="Aussie insurance brokers", short="brokerage",
  bucket="drown in paperwork", ing="drowning in paperwork",
  wrong="hiring a bigger back office", cost="You are scaling the problem.",
  before="Paperwork over advice", aft="Advice over paperwork")),
 ("financial-services", "bottleneck", dict(
  who="Aussie insurance brokers", short="brokerage",
  bucket="build the automation themselves", ing="building the automation yourself",
  wrong="spending another weekend on it", cost="You have a brokerage to run.",
  before="You are the one building it", aft="Someone else owns the build")),
 ("financial-services", "dormant-book", dict(
  who="Aussie insurance brokers", short="brokerage",
  bucket="sit on a dormant client book", ing="sitting on a dormant client book",
  wrong="running another campaign", cost="The book is still sitting there.",
  before="The top of the book worked", aft="The whole book worked")),
 ("financial-services", "trust", dict(
  who="Aussie insurance brokers", short="brokerage",
  bucket="guess at who they can trust", ing="guessing who you can trust",
  wrong="booking another vendor demo", cost="Nobody in that list is accountable to you.",
  before="A list of vendors", aft="One accountable person")),
]

OFFER = "A the role you place"

# One magnet per industry, in sentence case. Every card closes on its own industry's magnet,
# which is the whole reason the set exists. Spec for each is in that industry's playbook.
MAGNETS = {
    "construction": "Take the Site-to-Profit Readiness Check",
    "real-estate": "Take the AI-Ready Agency Score",
    "hospitality": "Take the Wow Factor Audit",
    "retail": "Take the Retail Ops AI Readiness Check",
    "financial-services": "Take the Broker and Adviser AI Readiness Check",
}

# THE ASSIGNMENT. 25 cells, five industries by five ranked pains. Five already exist as the
# band keepers (FORMAT-GRID.md section 2), so **20 cards are the whole remaining demand**:
# one static per pain point per industry, never six formats per pain.
#
# Two rules set the assignment:
#   1. No industry repeats a shape, so each industry's four cards look like four different ads.
#   2. The shape is cast to the pain. Contrarian goes where there is an obvious wrong fix,
#      versus goes where the category needs explaining, before and after goes where the pain
#      is a time lag, question goes where confrontation lands, callout where the pain is
#      blunt enough to just say, declarative where house can make a flat claim.
KEEPERS = {  # these five are the existing band cards, not rebuilt here
    "construction": "quoting", "real-estate": "leadgen", "hospitality": "numbers",
    "retail": "systems", "financial-services": "context",
}

GRID = {
    ("construction", "systems"): "question",
    ("construction", "double-handling"): "callout",
    ("construction", "bottleneck"): "versus",
    ("construction", "headcount"): "contrarian",

    ("real-estate", "admin"): "contrarian",
    ("real-estate", "systems"): "before-after",
    ("real-estate", "bottleneck"): "versus",
    ("real-estate", "numbers"): "question",

    ("hospitality", "hiring"): "contrarian",
    ("hospitality", "admin"): "before-after",
    ("hospitality", "tribal-knowledge"): "declarative",
    ("hospitality", "presence"): "question",

    ("retail", "bottleneck"): "declarative",
    ("retail", "numbers"): "before-after",
    ("retail", "admin"): "callout",
    ("retail", "headcount"): "contrarian",

    ("financial-services", "admin"): "callout",
    ("financial-services", "bottleneck"): "declarative",
    ("financial-services", "dormant-book"): "before-after",
    ("financial-services", "trust"): "versus",
}


def cap(s):
    return s[0].upper + s[1:] if s else s


# Each shape is a FILL of a named template in references/hooks/HOOKS.md, cited by id.
# The avatar opens every one of them. Slots are substituted, never rewritten.

def shape_callout(p):
    """HOOKS A1/S1, the news headline, in the canonical news-carousel band wording:
    `Aussie [avatar] ... don't have to [pain] anymore.`"""
    return dict(kind="stack",
                head=f"{p['who']} don't have to [[{p['bucket']}]] anymore.",
                sub="One hire. That is the whole change.")


def shape_question(p):
    """HOOKS A1/S12, the question hook. Avatar first, then the question."""
    return dict(kind="stack",
                head=f"{p['who']}. Still [[{p['ing']}]]?",
                sub="You don't have to be.")


def shape_declarative(p):
    """HOOKS A1/S8, did you know: `you don't need to use AI in your [avatar] business`."""
    return dict(kind="stack",
                head=f"{p['who']} don't need to use AI.",
                sub=f"They need [[one person who owns it]]. That person stops you having to "
                    f"{p['bucket']}.")


def shape_contrarian(p):
    """HOOKS S1 contrarian engine: `Stop [common move]. [The cost, said plainly].`"""
    return dict(kind="stack",
                head=f"{p['who']}: stop [[{p['wrong']}]].",
                sub=p["cost"])


def shape_before_after(p):
    """HOOKS A1/S10, before and after."""
    return dict(kind="rows",
                label=p["who"],
                rows=[("Before", p["before"], False), ("After", p["aft"], True)])


def shape_versus(p):
    """HOOKS A1/S11, us vs them: `Want AI in your [avatar] business?`
    Them: consultants and their pains. Us: a house and the benefits."""
    return dict(kind="cols",
                label=f"Want AI in your {p['short']}?",
                cols=[("A consultant", ["Costs you a fee", "Leaves when the job ends",
                                        "You still run it"], False),
                      (OFFER, ["Costs you a salary", "Stays on the team",
                               "They run it"], True)])


SHAPES = {
    "callout": shape_callout,
    "question": shape_question,
    "declarative": shape_declarative,
    "contrarian": shape_contrarian,
    "before-after": shape_before_after,
    "versus": shape_versus,
}


def build(industries=None):
    n = skipped = 0
    for industry, slug, p in PAINS:
        if industries and industry not in industries:
            continue
        if KEEPERS.get(industry) == slug:
            skipped += 1
            continue                       # the band keeper already exists, do not rebuild
        name = GRID.get((industry, slug))
        if not name:
            print(f"  no shape assigned for {industry}/{slug}")
            continue
        spec = SHAPES[name](p)
        spec["cta"] = MAGNETS[industry]
        out = OUT / industry / f"{slug}--{name}.png"
        report = render(spec, out)
        print(f"{industry:19} {slug:17} {name:13} {report}")
        n += 1
    print(f"\n{n} cards rendered, {skipped} band keepers left alone -> {OUT}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--sheets" in sys.argv:
        from sheets_basic import sheets
        sheets(OUT)
    else:
        build(args or None)
