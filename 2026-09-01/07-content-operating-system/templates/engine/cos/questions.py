"""The founder question bank: parse, append, promote, retire.

The bank lives in brain/founder-questions.md as markdown, because the founder has to be able
to read and edit it without a tool. This module parses that markdown, applies the weekly
changes, and writes it back. It never reorders vectors and it never touches a question's text.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

VECTORS = [
    "Customer pain, named exactly",
    "The objection",
    "Contrarian belief",
    "Changed mind",
    "Origin and scar tissue",
    "The demonstration",
    "Proprietary data",
    "The category, from the inside",
    "Values and the way they work",
]

Q_HEADER = re.compile(r"^###\s+(Q-\d+)\s*$", re.MULTILINE)
VECTOR_HEADER = re.compile(r"^##\s+Vector:\s*(.+?)\s*$", re.MULTILINE)
STATUS_LINE = re.compile(r"^-\s+\*\*Status:\*\*\s*(\w+)", re.MULTILINE)
THIS_WEEK = re.compile(r"^## This week\n.*?(?=^## )", re.MULTILINE | re.DOTALL)


class Bank:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.read_text() if path.exists() else ""

    # ------------------------------------------------------------------ reading

    def questions(self) -> list[dict]:
        """Every question in the bank, with its vector, status and body."""
        out: list[dict] = []
        vector = "unfiled"
        blocks = re.split(r"^(##\s+.*)$", self.raw, flags=re.MULTILINE)
        current_vector = vector
        for chunk in blocks:
            heading = VECTOR_HEADER.match(chunk.strip()) if chunk.startswith("##") else None
            if heading:
                current_vector = heading.group(1)
                continue
            for match in Q_HEADER.finditer(chunk):
                start = match.start()
                nxt = Q_HEADER.search(chunk, match.end())
                body = chunk[start:nxt.start() if nxt else len(chunk)]
                status = STATUS_LINE.search(body)
                out.append({
                    "id": match.group(1),
                    "vector": current_vector,
                    "body": body.rstrip(),
                    "status": status.group(1) if status else "unanswered",
                })
        return out

    def next_id(self) -> str:
        existing = [int(q["id"].split("-")[1]) for q in self.questions()]
        return f"Q-{(max(existing) + 1) if existing else 1:03d}"

    def answered_terms(self) -> set[str]:
        """Rough terms already covered, used to down-rank clusters the founder has done."""
        terms: set[str] = set()
        for question in self.questions():
            if question["status"] in ("answered", "retired"):
                words = re.findall(r"[a-z]{5,}", question["body"].lower())
                terms.update(words)
        return terms

    # ------------------------------------------------------------------ writing

    def append(self, new_questions: list[dict]) -> int:
        """Add questions under their vector heading. Returns how many were added."""
        if not new_questions:
            return 0
        text = self.raw or self._skeleton()
        next_number = int(self.next_id().split("-")[1])

        for question in new_questions:
            vector = question.get("vector") or VECTORS[0]
            block = self._render(f"Q-{next_number:03d}", question)
            next_number += 1
            heading = f"## Vector: {vector}"
            if heading in text:
                index = text.index(heading)
                following = text.find("\n## ", index + 1)
                cut = following if following != -1 else len(text)
                text = text[:cut].rstrip() + "\n\n" + block + "\n" + text[cut:]
            else:
                text = text.rstrip() + f"\n\n{heading}\n\n{block}\n"

        self.raw = text
        self.path.write_text(text)
        return len(new_questions)

    def promote(self, picks: list[dict]) -> None:
        """Rewrite the `## This week` block at the top with this run's questions."""
        lines = ["## This week", "",
                 f"Refreshed {datetime.now(timezone.utc).date().isoformat()}. "
                 "Pick the one you have the most to say about and talk for ninety seconds.", ""]
        for pick in picks:
            lines.append(f"- **{pick['question']}**")
            if pick.get("why"):
                lines.append(f"  - {pick['why']}")
            if pick.get("source"):
                lines.append(f"  - Source: {pick['source']}")
        block = "\n".join(lines) + "\n\n"

        text = self.raw or self._skeleton()
        if THIS_WEEK.search(text):
            text = THIS_WEEK.sub(block, text, count=1)
        else:
            first_vector = text.find("## Vector:")
            if first_vector == -1:
                text = text.rstrip() + "\n\n" + block
            else:
                text = text[:first_vector] + block + text[first_vector:]

        self.raw = text
        self.path.write_text(text)

    def retire_stale(self, months: int = 6) -> int:
        """Retire anything unanswered and never promoted for six months."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=months * 30)).date().isoformat()
        count = 0
        text = self.raw
        for question in self.questions():
            if question["status"] != "unanswered":
                continue
            added = re.search(r"\*\*Added:\*\*\s*(\d{4}-\d{2}-\d{2})", question["body"])
            promoted = "**Promoted:**" in question["body"]
            if added and added.group(1) < cutoff and not promoted:
                updated = question["body"].replace(
                    "**Status:** unanswered",
                    f"**Status:** retired\n- **Retired:** {datetime.now(timezone.utc).date()}, "
                    "six months unanswered and never promoted")
                text = text.replace(question["body"], updated)
                count += 1
        if count:
            self.raw = text
            self.path.write_text(text)
        return count

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _render(question_id: str, question: dict) -> str:
        lines = [f"### {question_id}", "", f"**{question['question']}**", ""]
        if question.get("source"):
            lines.append(f"- **Source:** {question['source']}")
        if question.get("also_seen"):
            lines.append(f"- **Also seen:** {question['also_seen']}")
        if question.get("format"):
            lines.append(f"- **Format fit:** {question['format']}")
        lines.append(f"- **Added:** {datetime.now(timezone.utc).date().isoformat()}")
        lines.append("- **Status:** unanswered")
        return "\n".join(lines)

    @staticmethod
    def _skeleton() -> str:
        head = ["# Founder question bank", "",
                "Open this file, read the five under **This week**, pick the one you have the most",
                "to say about, and talk for ninety seconds. Do not script it. The source line under",
                "each question is there so you know a real person actually asked.", ""]
        for vector in VECTORS:
            head.append(f"## Vector: {vector}\n")
        return "\n".join(head) + "\n"
