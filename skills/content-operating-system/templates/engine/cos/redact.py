"""Redaction at ingestion, not at output.

Everything written to the evidence store gets read back later by a model, so anything that
goes in comes out eventually. Strip identity on the way in, keep the meaning.

This is deliberately conservative. It over-redacts rather than under-redacts, and it reports
what it removed so a source that needs a custom rule is obvious on the dry run.
"""

from __future__ import annotations

import re

EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")
# At least nine digits, so a date like "2026 08 20" in a filename is not read as a phone number.
PHONE = re.compile(r"(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)")
URL = re.compile(r"https?://\S+")
CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")
HANDLE = re.compile(r"(?<![\w/])@[A-Za-z0-9_]{2,}")
# A speaker label at the start of a line. Transcripts put the name here, every time.
SPEAKER = re.compile(r"^[ \t]*([A-Z][\w'-]+(?:\s+[A-Z][\w'-]+){0,2})\s*:", re.MULTILINE)
# Capitalised runs of two or three words anywhere. Over-redacts on purpose.
NAME_RUN = re.compile(r"\b[A-Z][a-z]{1,15}(?:\s+[A-Z][a-z]{1,15}){1,2}\b")
COMPANY_SUFFIX = re.compile(
    r"\b[A-Z][\w&'-]*(?:\s+[A-Z][\w&'-]*)*\s+"
    r"(?:Pty\s+Ltd|Ltd|LLC|Inc\.?|GmbH|Limited|Corporation|Corp\.?|Group|Holdings)\b"
)

# Words that look like names to the regex and are not. Extend per source, not globally.
SAFE_RUNS = {
    "Google Sheets", "Microsoft Excel", "Google Drive", "Google Analytics", "Search Console",
    "Claude Code", "Open AI", "New South Wales", "United States", "United Kingdom",
    "Monday Morning", "Friday Afternoon", "Black Friday",
}

# Words that appear inside a capitalised run and prove it is not a person. Days and months
# matter: "Every Thursday night" is often the whole point of what a customer said.
NOT_A_NAME = {
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
    "every", "last", "next", "this", "the", "our", "their", "his", "her", "your",
}

# Speaker labels that are a role rather than a person. These carry meaning, so they stay.
SAFE_SPEAKERS = {
    "interviewer", "support", "agent", "customer", "client", "host", "caller", "rep",
    "sales", "me", "them", "speaker", "unknown", "note", "notes", "summary", "action items",
    "attendees", "transcript", "recording", "q", "a",
}


def redact(text: str) -> tuple[str, dict[str, int]]:
    """Return the redacted text and a count of what was removed, by kind."""
    counts = {"email": 0, "phone": 0, "url": 0, "card": 0, "handle": 0, "name": 0, "company": 0}
    if not text:
        return "", counts

    def sub(pattern, token, kind, value):
        def repl(match):
            counts[kind] += 1
            return token
        return pattern.sub(repl, value)

    out = text
    out = sub(CARD, "[card]", "card", out)
    out = sub(EMAIL, "[email]", "email", out)
    out = sub(URL, "[link]", "url", out)

    def phone_repl(match):
        if sum(c.isdigit() for c in match.group(0)) < 9:
            return match.group(0)
        counts["phone"] += 1
        return "[phone]"

    out = PHONE.sub(phone_repl, out)
    out = sub(HANDLE, "[handle]", "handle", out)

    def speaker_repl(match):
        if match.group(1).lower() in SAFE_SPEAKERS:
            return match.group(0)
        counts["name"] += 1
        return "[speaker]:"

    out = SPEAKER.sub(speaker_repl, out)

    def company_repl(match):
        counts["company"] += 1
        return "[company]"

    out = COMPANY_SUFFIX.sub(company_repl, out)

    def name_repl(match):
        run = match.group(0)
        if run in SAFE_RUNS:
            return run
        if any(word.lower() in NOT_A_NAME for word in run.split()):
            return run
        counts["name"] += 1
        return "[name]"

    out = NAME_RUN.sub(name_repl, out)
    return out, counts


def redact_record(record: dict, keep: list[str]) -> dict:
    """Redact the free text of an evidence record, keeping only the allowed meta fields."""
    text, counts = redact(record.get("text", ""))
    title, title_counts = redact(record.get("title", ""))
    for kind, count in title_counts.items():
        counts[kind] += count

    meta = {k: v for k, v in (record.get("meta") or {}).items() if k in keep or k in
            ("permalink", "rating", "engagement", "platform", "board", "resolution", "recurred")}

    out = dict(record)
    out["text"] = text
    out["title"] = title
    out["meta"] = meta
    out["redacted"] = True
    out["redaction_counts"] = {k: v for k, v in counts.items() if v}
    return out


def looks_unredacted(record: dict) -> list[str]:
    """Post-check for the dry run. Returns reasons a record still looks identifying."""
    reasons = []
    blob = f"{record.get('title', '')} {record.get('text', '')}"
    if EMAIL.search(blob):
        reasons.append("an email address survived")
    if any(sum(c.isdigit() for c in m.group(0)) >= 9 for m in PHONE.finditer(blob)):
        reasons.append("a phone number survived")
    if CARD.search(blob):
        reasons.append("a long digit run survived")
    for key, value in (record.get("meta") or {}).items():
        if key in ("name", "email", "phone", "company", "contact", "customer_name"):
            reasons.append(f"meta.{key} is an identifying field")
    return reasons
