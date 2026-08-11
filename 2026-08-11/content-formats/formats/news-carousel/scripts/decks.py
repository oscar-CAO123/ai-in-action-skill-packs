"""Copy decks for the house news-headline carousels.

Every headline, number and quoted phrase is grounded in `skills/content-formats/references/canon/CONCEPT-BANK.md`
(18 ranked pains, each from real discovery calls), `context/pain-wiki/` and
`context/personas/personas-and-avatars.md`. Nothing invented, no real company or person names.

The CONCEPT-BANK's 18-pain numbering predates the Discovery Intelligence Report and its
15 weighted pain labels. The pain numbers below still resolve inside CONCEPT-BANK; for anything new,
rank off `context/pain-wiki/MARKET.md` and pull vertical copy from
`context/pain-wiki/industries/<slug>.md`.

Each deck is tagged with its CONCEPT-BANK pain number, its persona code, and its headline
template from `ideas/news-carousels/IDEATION.md`. Build order follows the CONCEPT-BANK
production ranking: 0, 12, 4, 1, 5, 8, 6, then the rest.

`[[double brackets]]` mark the one blue accent phrase per slide, never two. Headline lines are
hand-broken and each renders on a single line, so hold them near 20 characters. The longest line
sets the size for the whole headline.
"""

ENDCARD = {
    "lines": ["THERE IS ONE PLACE", "IN AUSTRALIA YOU", "CAN [[HIRE ONE.]]"],
    "url": "yourdomain.example",
}


DECKS = [
    {
        # Pain 0, the pain stack. Persona-plural by design. Template 8, contrarian report.
        "slug": "p00-eight-hats",
        "headline": ["THE EIGHT PROBLEMS", "IN YOUR BUSINESS", "ARE [[ONE PROBLEM]]",
                     "WEARING EIGHT HATS"],
        "scene": [
            "Across Australian businesses turning over five million and up, the same eight "
            "complaints come up on every discovery call. Quotes that take a week. Receipts at "
            "nine at night. The same job number typed into four systems. Leads paid for and "
            "never called.",
            "Owners treat them as eight separate fires. Every one of them is work that nobody "
            "in the building owns, because until about a year ago the job did not exist.",
        ],
        "figure": "EIGHT",
        "caption": "Separate problems on the surface. One job description underneath, and it "
                   "has sat vacant in most Australian businesses since the day it was invented.",
        "reveal": ["THE OWNERS WHO", "STOPPED FIREFIGHTING", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 12, X-01, the owner in the bunker. The flagship. Template 8.
        "slug": "p12-most-expensive-junior",
        "headline": ["AUSTRALIA'S MOST", "EXPENSIVE JUNIOR AI", "ENGINEER IS",
                     "[[THE BUSINESS OWNER]]", "BUILDING IT HIMSELF"],
        "scene": [
            "In Australian businesses turning over five million and up, the person with the "
            "most valuable hours in the company is spending them watching an agent fail in a "
            "terminal window.",
            "One owner goes down into a bunker for a fortnight at a time to get a build off "
            "the ground. Then he comes back up and firefights, and the build sits there.",
        ],
        "figure": "30 HRS",
        "caption": "A week the owner puts into building the system instead of scaling the "
                   "company. Priced at what his hour is actually worth, that is the most "
                   "expensive engineering in the building.",
        "reveal": ["THE OWNERS WHO GOT", "THEIR WEEK BACK", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 4, X-02, already burned. The strongest message we have. Template 8.
        "slug": "p04-right-all-along",
        "headline": ["THE AUSSIE OWNERS", "WHOSE AI BUILD FELL", "OVER WERE",
                     "[[RIGHT ALL ALONG]]"],
        "scene": [
            "There are half-finished agents sitting on laptops across Australia that have not "
            "been opened in five weeks. The owner got sixty percent of the way there on a "
            "Sunday, and then the business needed him.",
            "Others paid an agency, took the discovery call and the slide deck, and got a "
            "contractor juggling nine other clients. When one automation broke there was "
            "nobody to call.",
        ],
        "figure": "22%",
        "caption": "Of the Australian market has already tried AI and watched it stall. They "
                   "need no convincing about the tools. They were never given anybody "
                   "accountable for them.",
        "reveal": ["THE ONES WHO GOT IT", "WORKING HIRED A", "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 1, CON-01, back-office admin. Biggest pain in the dataset. Template 7.
        "slug": "p01-second-job",
        "headline": ["AUSSIE CONSTRUCTION", "FIRMS WHOSE [[SECOND JOB]]", "STARTS WHEN THE",
                     "SITE SHUTS"],
        "scene": [
            "Across Australian building firms the day finishes at four on site and starts "
            "again at nine at night at the kitchen table. Receipts, timesheets, subbie "
            "invoices, the reconciliation that doubles if it waits until tomorrow.",
            "One builder keeps a book on the dashboard of the ute, because writing the figures "
            "down is faster than typing them in. Then he types them in anyway.",
        ],
        "figure": "$60,000",
        "caption": "A year in evenings, at eight to ten hours a week on timesheets alone, paid "
                   "in the only currency an owner cannot invoice for.",
        "reveal": ["THE FIRMS THAT GOT", "THEIR EVENINGS BACK", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 5, CON-02, quoting caps revenue. Prospects price this one themselves. Template 4.
        "slug": "p05-eight-seconds",
        "headline": ["THREE WEEKS TO", "[[EIGHT SECONDS]]:", "THE AUSSIE FIRMS",
                     "WINNING TENDERS", "BEFORE RIVALS FILE"],
        "scene": [
            "Across Australian construction and civil, a quote means reading the plans, doing "
            "the takeoff, counting it out, and typing all of it into a spreadsheet. Two to four "
            "hours on a small job, two weeks on a real one.",
            "One civil firm named estimating as the single thing blocking its expansion. The "
            "quotes that never got sent are the biggest number in the business and they appear "
            "on no report.",
        ],
        "figure": "8 SECONDS",
        "caption": "What a twenty-five million dollar quoting pipeline now takes, down from "
                   "three weeks, after one operator rebuilt it from inside the business.",
        "reveal": ["THE FIRMS QUOTING", "IN A DAY HIRED A", "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 8, TRD-03, the octopus. Owner as bottleneck. Template 7.
        "slug": "p08-octopus",
        "headline": ["'I FEEL LIKE AN", "[[OCTOPUS]]': THE AUSSIE", "OWNERS WHO CANNOT",
                     "PUT AN ARM DOWN"],
        "scene": [
            "Across Australian businesses every real decision still routes through one person. "
            "Quotes, invoices, hiring, site calls, payroll, complaints, scheduling, the bank.",
            "One owner described himself as an octopus, all these arms, and every one of them a "
            "decision only he can make. A concrete supplier runs fifty thousand phone calls a "
            "year through a single man.",
        ],
        "figure": "50,000",
        "caption": "Phone calls a year through one person, allocations and drivers and all of "
                   "it. He works harder than anyone in the building, and the building cannot "
                   "run a day without him.",
        "reveal": ["THE OWNERS WHO GOT", "A BUSINESS BACK", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 6, TRD-02, leads leak. Most urgent once named, the money is already spent.
        "slug": "p06-two-thousand-customers",
        "headline": ["AUSSIE TRADIES ARE", "BUYING STRANGERS", "WHILE [[2,000 LOYAL]]",
                     "CUSTOMERS SIT IDLE"],
        "scene": [
            "Across Australian trades and field services, owners are paying for new leads today "
            "while thousands of past customers sit in a database nobody has opened in a year.",
            "One residential builder follows up fifteen percent of the leads he pays for. A "
            "transport operator loses three or four email enquiries a week to the archive. He "
            "is all over the phone calls.",
        ],
        "figure": "15%",
        "caption": "The share of paid leads that get followed up, purely from capacity. The "
                   "other eighty-five percent were bought, billed, and left to go cold.",
        "reveal": ["THE OWNERS WHO", "PLUGGED THE LEAK", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 2, CON-03, systems don't talk. Template 2, expose.
        "slug": "p02-thirty-thousand-typo",
        "headline": ["REVEALED: THE", "[[$30,000 TYPO]]", "HIDING IN AUSTRALIAN",
                     "CONSTRUCTION, 400", "TIMES A YEAR"],
        "scene": [
            "Across Australian building firms, the same job number gets typed into six or seven "
            "different systems before the work is finished. Estimating, procurement, "
            "scheduling, accounts, payroll.",
            "Every handoff is a person re-entering what another person already entered. Nobody "
            "owns the seam between the systems, so nobody catches the digit that moved.",
        ],
        "figure": "$30,000",
        "caption": "The cost of one rework on a major job, traced back to a single number typed "
                   "wrong at handoff four. Six to seven handoffs run on every job.",
        "reveal": ["THE FIRMS THAT", "FIXED IT HIRED A", "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 7, ECOM-02, margin bleeding into unmeasured spend. Template 2.
        "slug": "p07-no-attribution",
        "headline": ["REVEALED: THE AUSSIE", "BRANDS SPENDING", "[[$1.5 MILLION]] ON ADS",
                     "WITH NO IDEA WHAT", "IT RETURNS"],
        "scene": [
            "Across Australian e-commerce, seven-figure media budgets run through platforms "
            "that each claim the same sale. Meta counts it, Google counts it, the email tool "
            "counts it.",
            "The founder opens three dashboards, gets three answers, and scales the channel "
            "that feels right that week. One of them is on two million a year and wants to "
            "halve it without shrinking.",
        ],
        "figure": "$1.5M",
        "caption": "Spent on paid media in a year, with no attribution anybody in the business "
                   "trusts. Every scaling decision after that is a guess with a seven-figure "
                   "price on it.",
        "reveal": ["THE BRANDS THAT", "FIXED IT HIRED A", "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 9, the headcount trap. Growth capped by people. Template 1.
        "slug": "p09-headcount-trap",
        "headline": ["THE AUSSIE FIRMS", "BOOKED OUT TEN", "MONTHS THAT STOPPED",
                     "[[HIRING TO GROW]]"],
        "scene": [
            "Across Australian manufacturing and construction, demand has never been the "
            "problem. Firms are booked nine to ten months out and turning work away, because "
            "the only growth lever they have ever had is people.",
            "So they hire, then train, then manage, then carry the overhead through the quiet "
            "month, and the margin the growth was meant to deliver goes to the cost of "
            "delivering it.",
        ],
        "figure": "150%",
        "caption": "The revenue growth one Australian manufacturer needs inside two years with "
                   "no proportional headcount. A builder on half a billion in projects simply "
                   "cannot hire fast enough.",
        "reveal": ["THE FIRMS THAT GREW", "WITHOUT HEADCOUNT", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 11, ECOM-06, inbox volume. Template 2.
        "slug": "p11-three-thousand-unread",
        "headline": ["[[3,000 UNREAD]]: THE", "AUSSIE INBOXES", "WHERE CUSTOMERS",
                     "QUIETLY GIVE UP"],
        "scene": [
            "An operator who walked into an Australian electrical business inherited six "
            "separate email accounts with no labels and no triage. A wholesaler takes hundreds "
            "of emails a day and the good ones drown with the rest.",
            "Every message that sits for four days is a customer deciding the business is not "
            "fussed. They never complain. They go somewhere else, and nobody finds out why.",
        ],
        "figure": "3,000",
        "caption": "Unread messages in one account, the oldest of them four months old. "
                   "Somebody in there was ready to buy.",
        "reveal": ["THE BRANDS ANSWERING", "BEFORE A HUMAN WAKES", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
    {
        # Pain 13, AGY-03, cannot vet AI talent. This one goes direct to site. Template 5.
        "slug": "p13-eighteen-months",
        "headline": ["[[EIGHTEEN MONTHS]]:", "HOW LONG ONE AUSSIE", "BUSINESS SEARCHED",
                     "FOR AN AI OPERATOR", "BEFORE GIVING UP"],
        "scene": [
            "There is no degree for this work and no ten-year CV to check it against. The "
            "market is full of people who can talk fluently about AI for forty-five minutes and "
            "have never shipped a thing that runs on a Monday without them.",
            "Owners keep asking the same two questions. Where do you find these people, and who "
            "teaches a person that.",
        ],
        "figure": "18 MONTHS",
        "caption": "One Australian business searched that long for an AI operator and came up "
                   "empty. Nobody can hire for a skill they have no way to assess.",
        "reveal": ["THERE IS ONE FIRM", "IN AUSTRALIA THAT", "VETS AND PLACES",
                   "[[CHIEF AGENT OFFICERS]]"],
    },
    {
        # Pain 16, HOSP-02, nobody trusts the numbers. Small count, enormous deal size.
        "slug": "p16-three-hundred-grand",
        "headline": ["[[$300,000]] A YEAR", "FOR A SYSTEM THIS", "AUSSIE VENUE GROUP",
                     "DOES NOT BELIEVE"],
        "scene": [
            "Across Australian hospitality groups the reporting comes out of a booking system "
            "costing close to three hundred thousand dollars a year, and nobody in the business "
            "trusts a number it produces.",
            "So the call on the next site never gets made. The whole expansion sits frozen "
            "while everyone waits for a figure they can believe.",
        ],
        "figure": "35 VENUES",
        "caption": "An expansion held up by data nobody trusts. Money is not the thing blocking "
                   "it, and hiring another analyst pulls the same numbers out of the same "
                   "system.",
        "reveal": ["THE GROUPS THAT", "TRUST THEIR NUMBERS", "HIRED A",
                   "[[CHIEF AGENT OFFICER]]"],
    },
]
