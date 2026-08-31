"""The source contract.

A source turns some place customers said things into a list of evidence records. It does not
redact, it does not deduplicate, and it does not write. Those happen once, in ingest.py, so
every source gets the same treatment.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from ..store import make_id


class Source:
    type = "unset"

    def __init__(self, spec: dict):
        self.spec = spec
        self.id = spec["id"]

    # ------------------------------------------------------------------ helpers

    def token(self) -> str | None:
        name = self.spec.get("token_env")
        return os.environ.get(name) if name else None

    def since(self, watermark: str | None) -> str:
        """The datetime to pull from: the watermark if there is one, else the lookback window."""
        if watermark:
            return watermark
        days = int(self.spec.get("lookback_days", 30))
        return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")

    def record(self, native_id: str, occurred_at: str, text: str,
               title: str = "", meta: dict | None = None) -> dict:
        return {
            "id": make_id(self.id, str(native_id)),
            "source_id": self.id,
            "source_type": self.type,
            "occurred_at": occurred_at,
            "title": title or "",
            "text": text or "",
            "meta": meta or {},
        }

    # --------------------------------------------------------------- the contract

    def fetch(self, watermark: str | None, limit: int | None = None) -> list[dict]:
        """Return evidence records newer than the watermark. Never raises for an empty source."""
        raise NotImplementedError

    def describe(self) -> str:
        """One line for the run log."""
        return f"{self.id} ({self.type})"


def iso(value) -> str:
    """Coerce whatever a vendor returned into an ISO string, or now if it is unreadable."""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat(timespec="seconds")
    if isinstance(value, str) and value:
        cleaned = value.replace("Z", "+00:00")
        for parse in (datetime.fromisoformat,):
            try:
                return parse(cleaned).isoformat(timespec="seconds")
            except ValueError:
                pass
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(value[:19], fmt).replace(
                    tzinfo=timezone.utc).isoformat(timespec="seconds")
            except ValueError:
                pass
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
