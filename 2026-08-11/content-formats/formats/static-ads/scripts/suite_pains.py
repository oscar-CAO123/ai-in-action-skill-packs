#!/usr/bin/env python3
"""The pain bank for all SEVEN industries.

`basics.PAINS` carries 25 entries, five pains across five industries, and it stops there because
trades and professional services were added as avatars on after it was written. This
module re-exports those 25 and adds the missing 10 in the identical shape, so the suite has a
complete 7 x 5 grid to fill from.

Field shape, unchanged from `basics.py`:

    who      the plural the card opens on, bound by `context/language-rules.md`
    short    the singular, for "your ___"
    bucket   the pain as a third-person clause: "[they] run on disconnected systems"
    ing      the same pain as a gerund, for "still [painpoint]"
    wrong    the move they make instead, which is the one that does not work
    cost     what that move actually costs, one flat sentence
    before   the left half of a before / after, four or five words
    aft      the right half, same length, same grammar

The two new avatars follow the same ranking law the other five do: rank 1 is the pain that
industry owns most distinctly, and no two industries lead on the same bucket.
"""
from basics import PAINS as _BASE

# ---- Trades ------------------------------------------------------------------------------
# `key` stays "building-services" everywhere it addresses a built page or a CRM row. Every word
# said out loud is "trades". you, .
TRADES = [
    ("building-services", "database", dict(
        who="Aussie trades businesses", short="trades business",
        bucket="sit on a database they never call", ing="sitting on a database you never call",
        wrong="buying more leads", cost="You already paid for the ones sitting there.",
        before="Past customers, never called", aft="Every past customer called")),
    ("building-services", "quoting", dict(
        who="Aussie trades businesses", short="trades business",
        bucket="quote from the ute at night", ing="quoting from the ute at night",
        wrong="quoting later, after tea", cost="The other bloke quoted at four.",
        before="Quotes go out at nine at night", aft="Quotes go out from the driveway")),
    ("building-services", "scheduling", dict(
        who="Aussie trades businesses", short="trades business",
        bucket="rebuild the run sheet by phone", ing="rebuilding the run sheet by phone",
        wrong="calling everyone again", cost="Half a day gone before a tool comes out.",
        before="An hour of calls before eight", aft="The run sheet rebuilds itself")),
    ("building-services", "bottleneck", dict(
        who="Aussie trades businesses", short="trades business",
        bucket="run every decision through the owner", ing="running every decision through you",
        wrong="working longer hours", cost="The work still stops when you do.",
        before="Everything waits on you", aft="The job moves without you")),
    ("building-services", "followup", dict(
        who="Aussie trades businesses", short="trades business",
        bucket="lose the follow-up after the job", ing="losing the follow-up after the job",
        wrong="meaning to call them back", cost="The quote goes cold in four days.",
        before="Quotes sent, never chased", aft="Every quote chased on time")),
]

# ---- Professional services ---------------------------------------------------------------
PROFESSIONAL = [
    ("professional-services", "write-off", dict(
        who="Aussie professional services businesses", short="professional services business",
        bucket="write off hours they already worked", ing="writing off hours you already worked",
        wrong="pushing the team to bill harder", cost="The hours were already gone by then.",
        before="Hours worked, never billed", aft="Every hour on the invoice")),
    ("professional-services", "admin", dict(
        who="Aussie professional services businesses", short="professional services business",
        bucket="put senior people on admin", ing="putting senior people on admin",
        wrong="hiring another junior", cost="You are paying partner rates for data entry.",
        before="Partners doing paperwork", aft="Partners back on the work")),
    ("professional-services", "knowledge", dict(
        who="Aussie professional services businesses", short="professional services business",
        bucket="keep the method in one partner's head",
        ing="keeping the method in one partner's head",
        wrong="writing it up when there is time", cost="There is never time, and then they leave.",
        before="One partner knows how", aft="The method is written down")),
    ("professional-services", "bottleneck", dict(
        who="Aussie professional services businesses", short="professional services business",
        bucket="run every file past the principal", ing="running every file past the principal",
        wrong="reviewing faster", cost="The file still waits for one diary.",
        before="Every file waits on review", aft="The file moves on its own")),
    ("professional-services", "capacity", dict(
        who="Aussie professional services businesses", short="professional services business",
        bucket="turn work away at capacity", ing="turning work away at capacity",
        wrong="hiring another fee earner", cost="You just raised the break-even too.",
        before="Good work turned away", aft="Same team, more files")),
]

PAINS = list(_BASE) + TRADES + PROFESSIONAL

BY_INDUSTRY = {}
for _ind, _slug, _p in PAINS:
    BY_INDUSTRY.setdefault(_ind, {})[_slug] = _p

# Rank 1 per industry: the pain that industry owns most distinctly, and the one every
# single-pain format fills from. No two industries lead on the same bucket.
RANK1 = {
    "construction": "systems",
    "real-estate": "systems",
    "hospitality": "admin",
    "retail": "bottleneck",
    "financial-services": "context",
    "building-services": "database",
    "professional-services": "write-off",
}


if __name__ == "__main__":
    for ind, slugs in BY_INDUSTRY.items:
        print(f"\n{ind}  ({len(slugs)} pains, rank 1 = {RANK1[ind]})")
        for slug, p in slugs.items:
            print(f"  {slug:16} {p['bucket']}")
    print(f"\n{len(PAINS)} pains across {len(BY_INDUSTRY)} industries")
