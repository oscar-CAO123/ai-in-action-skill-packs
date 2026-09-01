"""Rule-based clustering and scoring.

A model call is for judgement. Counting how many independent sources said a thing, how
recently, and how much money sat behind the person saying it are all rules, so they are
written as rules. The judgement pass in ideate.py starts from this shortlist rather than from
the raw store, which is what keeps the ideation run cheap.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been before being below
between both but by can cannot could did do does doing down during each few for from further had
has have having he her here hers him his how i if in into is it its just me more most my no nor not
now of off on once only or other our out over own same she should so some such than that the their
them then there these they this those through to too under until up very was we were what when
where which while who whom why will with would you your yeah yes okay ok like know think going get
got really actually thing things stuff want need said says say im ive dont didnt thats theres
""".split()) | {
    # The redaction tokens from redact.py. They are in every record and mean nothing.
    "speaker", "name", "company", "email", "phone", "link", "card", "handle",
}

# How much weight a source type carries. Money behind the words is a real signal.
SOURCE_WEIGHT = {
    "calls": 1.0,
    "tickets": 0.85,
    "reviews": 0.7,
    "forums": 0.5,
}

WORD = re.compile(r"[a-z][a-z'-]{2,}")


def terms(text: str) -> list[str]:
    words = [w for w in WORD.findall(text.lower()) if w not in STOPWORDS and len(w) > 3]
    bigrams = [f"{a} {b}" for a, b in zip(words, words[1:])]
    return words + bigrams


def recency_score(occurred_at: str, half_life_days: float = 45.0) -> float:
    try:
        when = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return 0.3
    age = (datetime.now(timezone.utc) - when).days
    return math.exp(-max(age, 0) / half_life_days)


def build_clusters(records: list[dict], min_size: int = 2, max_clusters: int = 60,
                   max_memberships: int = 3) -> list[dict]:
    """Greedy clustering on shared salient terms. Deterministic, no model, no dependencies."""
    if not records:
        return []

    doc_freq: Counter = Counter()
    per_record: dict[str, set[str]] = {}
    for record in records:
        found = set(terms(f"{record.get('title', '')} {record.get('text', '')}"))
        per_record[record["id"]] = found
        doc_freq.update(found)

    total = len(records)
    # A theme is a term several records share and most do not. On a small corpus every shared
    # term qualifies, because with five calls there is no such thing as a term that is too
    # common to be interesting.
    ceiling = total if total < 10 else max(min_size, int(total * 0.6))

    by_term: dict[str, list[str]] = defaultdict(list)
    for record_id, found in per_record.items():
        for term in found:
            if min_size <= doc_freq[term] <= ceiling:
                by_term[term].append(record_id)

    index = {r["id"]: r for r in records}
    memberships: Counter = Counter()
    seen_member_sets: set[frozenset] = set()
    clusters: list[dict] = []

    # Bigrams first: "too expensive" is a theme, "expensive" on its own is a word.
    ordered = sorted(
        by_term.items(),
        key=lambda kv: (-(len(kv[1]) * (1.6 if " " in kv[0] else 1.0)), kv[0]),
    )
    for term, record_ids in ordered:
        # One call can be about quoting AND about price AND about a failed workaround. Letting a
        # record sit in a few themes is closer to the truth than forcing it into one.
        members = [rid for rid in record_ids if memberships[rid] < max_memberships]
        if len(members) < min_size:
            continue
        key = frozenset(members)
        if key in seen_member_sets:
            continue  # same records, different word for it
        seen_member_sets.add(key)
        for rid in members:
            memberships[rid] += 1
        clusters.append(_summarise(term, [index[rid] for rid in members]))
        if len(clusters) >= max_clusters:
            break

    return clusters


def _summarise(term: str, records: list[dict]) -> dict:
    sources = {r["source_id"] for r in records}
    source_types = {r["source_type"] for r in records}
    latest = max((r.get("occurred_at") or "") for r in records)
    return {
        "term": term,
        "size": len(records),
        "independent_sources": len(sources),
        "source_types": sorted(source_types),
        "latest": latest,
        "records": records,
        "quotes": _quotes(term, records),
    }


def _quotes(term: str, records: list[dict], count: int = 5) -> list[dict]:
    """The sentences that actually contain the term, which is what goes in the evidence rail."""
    head = term.split()[0]
    out = []
    for record in records:
        for sentence in re.split(r"(?<=[.!?])\s+", record.get("text", "")):
            stripped = sentence.strip()
            if head in stripped.lower() and 40 <= len(stripped) <= 320:
                out.append({
                    "text": stripped,
                    "source_id": record["source_id"],
                    "source_type": record["source_type"],
                    "record_id": record["id"],
                    "date": (record.get("occurred_at") or "")[:10],
                    "permalink": (record.get("meta") or {}).get("permalink", ""),
                })
                break
        if len(out) >= count:
            break
    return out


def score(cluster: dict, weights: dict, answered_terms: set[str]) -> float:
    independent = min(cluster["independent_sources"], 5) / 5
    recency = recency_score(cluster["latest"])
    money = max(SOURCE_WEIGHT.get(t, 0.4) for t in cluster["source_types"])
    repetition = min(cluster["size"], 20) / 20
    unanswered = 0.0 if cluster["term"] in answered_terms else 1.0

    return round(
        weights.get("independent_sources", 3.0) * independent
        + weights.get("recency", 2.0) * recency
        + weights.get("money_behind_it", 2.0) * money
        + weights.get("repetition", 1.5) * repetition
        + weights.get("unanswered", 1.0) * unanswered,
        3,
    )


def shortlist(records: list[dict], weights: dict, answered_terms: set[str],
              take: int = 30) -> list[dict]:
    clusters = build_clusters(records)
    for cluster in clusters:
        cluster["score"] = score(cluster, weights, answered_terms)
    clusters.sort(key=lambda c: c["score"], reverse=True)
    return clusters[:take]
