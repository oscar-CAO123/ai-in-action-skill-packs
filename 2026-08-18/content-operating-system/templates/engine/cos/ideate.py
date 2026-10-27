"""Cron 2. Ideation.

Reads the evidence store, clusters and ranks by rule, then asks the operator's own agent to
do the judgement pass against the brain. Writes a dated queue, a self-contained review page,
and the week's refresh of the founder question bank.

Reads and writes local files. It never publishes, never sends, and never spends.

    python3 -m cos.ideate
    python3 -m cos.ideate --no-agent     # rule-based only, useful for testing
    python3 -m cos.ideate --lookback 30
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import config as config_module
from .agent import ask_json
from .cluster import shortlist
from .ingest import Lock
from .questions import Bank
from .review_page import render
from .store import Store

PROMPT_FILE = "AGENT-IDEATE.md"


def build_prompt(root: Path, clusters: list[dict], cfg: dict) -> str:
    instruction_path = root / "engine" / PROMPT_FILE
    instruction = instruction_path.read_text() if instruction_path.exists() else DEFAULT_PROMPT

    payload = []
    for index, cluster in enumerate(clusters):
        payload.append({
            "cluster": index,
            "theme": cluster["term"],
            "mentions": cluster["size"],
            "independent_sources": cluster["independent_sources"],
            "source_types": cluster["source_types"],
            "latest": cluster["latest"][:10],
            "rule_score": cluster["score"],
            "quotes": [
                {"text": q["text"], "source": q["source_type"], "date": q["date"],
                 "record_id": q["record_id"]}
                for q in cluster["quotes"][:4]
            ],
        })

    return (
        f"{instruction}\n\n"
        f"## Selected formats\n{', '.join(cfg.get('formats', [])) or 'none selected'}\n\n"
        f"## Ideas wanted\n{cfg['ideation']['ideas_per_run']} ranked, "
        f"{cfg['ideation']['written_up']} written up.\n\n"
        f"## The evidence clusters\n\n```json\n{json.dumps(payload, indent=2)}\n```\n"
    )


DEFAULT_PROMPT = """You are running the weekly ideation pass for a founder-led content system.

Read `brain/SKILL.md`, then `brain/icp.md`, `brain/brand-truths.md`, `brain/copywriting.md`,
`brain/formats/`, and `brain/founder-questions.md`. Then read the evidence clusters below.

Produce a ranked idea queue. Every idea must be traceable to at least one quote in the
clusters. An idea you cannot trace does not go in, no matter how good it is.

Return ONLY a JSON array. Each element:

{
  "rank": 1,
  "hook": "the hook, filled from a structure in brain/formats/hooks.md",
  "hook_structure": "the structure id you filled",
  "angle": "one line on what this asset argues",
  "format": "one of the selected format ids",
  "founder_question": "the question to put in front of the founder",
  "question_vector": "one of the nine vectors",
  "why_now": "what in this week's evidence makes this worth making now",
  "evidence": ["record_id", "record_id"],
  "proof_tier": "shown | quoted | held",
  "script": "for the top ones only, the full first draft. Empty string otherwise."
}

Hard rules: no em dashes. No "it is not X, it is Y". No banned words from
brain/copywriting.md. Every claim carries its proof tier. One idea per element.
"""


def rule_based_ideas(clusters: list[dict], count: int) -> list[dict]:
    """The fallback when no agent is reachable. Honest, thin, and clearly labelled."""
    ideas = []
    for index, cluster in enumerate(clusters[:count], start=1):
        quote = cluster["quotes"][0]["text"] if cluster["quotes"] else ""
        ideas.append({
            "rank": index,
            "hook": "",
            "hook_structure": "",
            "angle": f"Theme: {cluster['term']}",
            "format": "",
            "founder_question": f'A customer said "{quote[:160]}". What is actually going on '
                                f"when someone says that?" if quote else "",
            "question_vector": "Customer pain, named exactly",
            "why_now": f"{cluster['size']} mentions across {cluster['independent_sources']} "
                       f"sources, most recent {cluster['latest'][:10]}",
            "evidence": [q["record_id"] for q in cluster["quotes"]],
            "proof_tier": "quoted",
            "script": "",
            "_rule_based": True,
        })
    return ideas


def run(cfg: dict, use_agent: bool, lookback: int | None) -> int:
    root = Path(cfg["_root"])
    store = Store(root)
    ideation = cfg["ideation"]
    days = lookback or ideation["lookback_days"]
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")

    records = list(store.read_all(since=since))
    print(f"{len(records)} records in the last {days} days")
    if not records:
        print("nothing new. run ingestion first, or widen --lookback")
        return 1

    bank_path = root / "brain" / "founder-questions.md"
    bank = Bank(bank_path)
    clusters = shortlist(records, ideation.get("weights", {}), bank.answered_terms(), take=30)
    print(f"{len(clusters)} clusters after ranking")
    if not clusters:
        print("no cluster reached the minimum size. widen --lookback or add a source")
        return 1

    ideas: list[dict] = []
    agent_note = ""
    if use_agent:
        prompt = build_prompt(root, clusters, cfg)
        cache = root / "outputs" / "logs" / ".agent-cache.json"
        parsed, detail = ask_json(prompt, cwd=root, cache_path=cache)
        if isinstance(parsed, list) and parsed:
            ideas = parsed
            agent_note = f"judgement pass ran via {detail}"
            print(f"  {agent_note}, {len(ideas)} ideas")
        else:
            agent_note = (f"JUDGEMENT PASS DID NOT RUN: {detail}. "
                          "These are rule-based clusters, not written ideas. "
                          "Run `python3 -m cos.ideate` by hand inside your agent.")
            print(f"  {agent_note}")

    if not ideas:
        ideas = rule_based_ideas(clusters, ideation["ideas_per_run"])

    # Attach the evidence back onto each idea, by record id. Prefer the sentence the clustering
    # actually matched: a whole transcript in the rail is not evidence, it is a haystack.
    by_record = {r["id"]: r for r in records}
    best_sentence: dict[str, str] = {}
    for cluster in clusters:
        for quote in cluster["quotes"]:
            best_sentence.setdefault(quote["record_id"], quote["text"])

    for idea in ideas:
        attached = []
        for record_id in idea.get("evidence", []):
            record = by_record.get(record_id)
            if not record:
                continue
            text = best_sentence.get(record_id) or " ".join(record.get("text", "").split())[:400]
            attached.append({
                "record_id": record_id,
                "source_id": record["source_id"],
                "source_type": record["source_type"],
                "date": (record.get("occurred_at") or "")[:10],
                "text": text,
                "permalink": (record.get("meta") or {}).get("permalink", ""),
            })
        idea["evidence_detail"] = attached

    # The explicit-reference law: an idea with an empty evidence rail does not appear.
    dropped = [i for i in ideas if not i.get("evidence_detail")]
    ideas = [i for i in ideas if i.get("evidence_detail")]
    if dropped:
        print(f"  dropped {len(dropped)} ideas with no traceable evidence")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = root / "outputs" / "queue" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    queue = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lookback_days": days,
        "records_considered": len(records),
        "clusters": len(clusters),
        "agent_note": agent_note,
        "dropped_no_evidence": len(dropped),
        "ideas": ideas,
    }
    (out_dir / "queue.json").write_text(json.dumps(queue, indent=2, ensure_ascii=False))

    page = out_dir / "review.html"
    page.write_text(render(queue, cfg))

    # The question bank: append, then promote this week's picks.
    new_questions = [
        {"question": i["founder_question"], "vector": i.get("question_vector"),
         "source": _source_line(i), "format": i.get("format", "")}
        for i in ideas if i.get("founder_question")
    ]
    added = bank.append(new_questions[: ideation["written_up"] * 2])
    bank.promote([
        {"question": i["founder_question"], "why": i.get("why_now", ""),
         "source": _source_line(i)}
        for i in ideas[: ideation["written_up"]] if i.get("founder_question")
    ])
    retired = bank.retire_stale()

    log_dir = root / "outputs" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"ideate-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json").write_text(
        json.dumps({"job": "ideate", "queue": str(out_dir), "ideas": len(ideas),
                    "questions_added": added, "questions_retired": retired,
                    "agent_note": agent_note}, indent=2))

    print(f"\n{len(ideas)} ideas. {added} questions added, {retired} retired.")
    print(f"open {page}")
    return 0


def _source_line(idea: dict) -> str:
    detail = idea.get("evidence_detail") or []
    if not detail:
        return ""
    first = detail[0]
    extra = f", plus {len(detail) - 1} more" if len(detail) > 1 else ""
    return f"{first['source_type']} {first['date']} ({first['record_id']}){extra}"


def main() -> int:
    parser = argparse.ArgumentParser(description="turn evidence into a ranked idea queue")
    parser.add_argument("--no-agent", action="store_true", help="rule-based ranking only")
    parser.add_argument("--lookback", type=int, help="days of evidence to consider")
    args = parser.parse_args()

    config_module.load_dotenv()
    cfg = config_module.load()
    with Lock(Path(cfg["_root"]) / "outputs" / "logs" / ".ideate.lock"):
        return run(cfg, not args.no_agent, args.lookback)


if __name__ == "__main__":
    sys.exit(main())
