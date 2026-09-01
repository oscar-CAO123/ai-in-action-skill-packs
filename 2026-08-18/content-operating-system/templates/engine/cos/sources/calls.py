"""Calls: transcripts from a watched folder.

The folder path is deliberately the primary route. Every call recorder can export to a
folder, a folder needs no token, it never expires, it has no rate limit, and it keeps working
when the vendor changes their API. Wire the API only when there is no export path.

Handles .txt, .md, .vtt, .srt and .json. A .json file is treated as a vendor export and the
transcript is found by looking for the longest string field.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from .base import Source, iso

EXTENSIONS = {".txt", ".md", ".vtt", ".srt", ".json"}
TIMECODE = re.compile(r"^\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->.*$")
CUE_INDEX = re.compile(r"^\d+$")
DATE_IN_NAME = re.compile(r"(20\d{2})[-_.]?(\d{2})[-_.]?(\d{2})")

CALL_TYPE_HINTS = {
    "discovery": ["discovery", "intro", "first call", "qualification"],
    "demo": ["demo", "walkthrough", "presentation"],
    "onboarding": ["onboarding", "kickoff", "kick-off", "setup"],
    "support": ["support", "issue", "bug", "help"],
    "renewal": ["renewal", "qbr", "review", "check-in", "checkin"],
}


def strip_captions(text: str) -> str:
    """Turn a .vtt or .srt into plain speech."""
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or TIMECODE.match(line) or CUE_INDEX.match(line):
            continue
        lines.append(line)
    # Caption files repeat the same line across cues. Collapse consecutive duplicates.
    out = []
    for line in lines:
        if not out or out[-1] != line:
            out.append(line)
    return "\n".join(out)


def longest_string(blob) -> str:
    best = ""
    stack = [blob]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            if len(item) > len(best):
                best = item
        elif isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return best


def guess_call_type(name: str, text: str) -> str:
    blob = f"{name} {text[:2000]}".lower()
    for call_type, hints in CALL_TYPE_HINTS.items():
        if any(hint in blob for hint in hints):
            return call_type
    return "unknown"


class CallsSource(Source):
    type = "calls"

    def fetch(self, watermark: str | None, limit: int | None = None) -> list[dict]:
        since = self.since(watermark)
        records: list[dict] = []

        for raw_path in self.spec.get("paths", []):
            root = Path(os.path.expanduser(raw_path))
            if not root.exists():
                continue
            for path in sorted(root.rglob("*"), reverse=True):
                if limit and len(records) >= limit:
                    break
                if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                    continue
                if path.stat().st_size > 5_000_000:
                    continue

                occurred = self._occurred_at(path)
                if occurred < since:
                    continue

                try:
                    raw = path.read_text(errors="replace")
                except OSError:
                    continue

                if path.suffix.lower() == ".json":
                    try:
                        text = longest_string(json.loads(raw))
                    except json.JSONDecodeError:
                        text = raw
                elif path.suffix.lower() in (".vtt", ".srt"):
                    text = strip_captions(raw)
                else:
                    text = raw

                if len(text.strip()) < 200:
                    continue

                records.append(self.record(
                    native_id=str(path.relative_to(root)),
                    occurred_at=occurred,
                    text=text.strip(),
                    title=path.stem.replace("_", " ").replace("-", " "),
                    meta={
                        "call_type": guess_call_type(path.stem, text),
                        "words": len(text.split()),
                        "file": path.name,
                    },
                ))
        return records

    @staticmethod
    def _occurred_at(path: Path) -> str:
        """Prefer a date in the filename. Recorders name files by date, and mtime lies after a sync."""
        match = DATE_IN_NAME.search(path.name)
        if match:
            year, month, day = match.groups()
            try:
                return datetime(int(year), int(month), int(day),
                                tzinfo=timezone.utc).isoformat(timespec="seconds")
            except ValueError:
                pass
        return iso(path.stat().st_mtime)
