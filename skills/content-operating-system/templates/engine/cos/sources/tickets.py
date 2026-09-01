"""Tickets: support conversations, from a CSV export or a helpdesk API.

Calls tell you why people buy. Tickets tell you what breaks the promise afterwards, which is
where the honest content lives and where competitors never look.

CSV first, deliberately. A CSV export works today with zero credentials, and for a first run
it is the better choice. Wire the API once the loop is proven.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path

import requests

from .base import Source, iso

TEXT_COLUMNS = ["description", "body", "message", "text", "conversation", "comment", "notes",
                "first_message", "content"]
TITLE_COLUMNS = ["subject", "title", "summary", "name"]
DATE_COLUMNS = ["created_at", "created", "date", "opened_at", "submitted_at", "timestamp"]
STATUS_COLUMNS = ["status", "state", "resolution"]

API = {
    "intercom": {
        "url": "https://api.intercom.io/conversations",
        "headers": lambda t: {"Authorization": f"Bearer {t}", "Accept": "application/json"},
        "items": lambda d: d.get("conversations", []),
        "text": lambda i: (i.get("source") or {}).get("body", ""),
        "title": lambda i: (i.get("source") or {}).get("subject", ""),
        "date": lambda i: i.get("created_at"),
        "native": lambda i: i.get("id"),
    },
    "zendesk": {
        "url": "https://{subdomain}.zendesk.com/api/v2/tickets.json",
        "headers": lambda t: {"Authorization": f"Bearer {t}"},
        "items": lambda d: d.get("tickets", []),
        "text": lambda i: i.get("description", ""),
        "title": lambda i: i.get("subject", ""),
        "date": lambda i: i.get("created_at"),
        "native": lambda i: i.get("id"),
    },
    "helpscout": {
        "url": "https://api.helpscout.net/v2/conversations",
        "headers": lambda t: {"Authorization": f"Bearer {t}"},
        "items": lambda d: (d.get("_embedded") or {}).get("conversations", []),
        "text": lambda i: i.get("preview", ""),
        "title": lambda i: i.get("subject", ""),
        "date": lambda i: i.get("createdAt"),
        "native": lambda i: i.get("id"),
    },
}


def pick(row: dict, candidates: list[str]) -> str:
    lowered = {k.lower().strip(): v for k, v in row.items() if k}
    for candidate in candidates:
        value = lowered.get(candidate)
        if value:
            return str(value)
    return ""


class TicketsSource(Source):
    type = "tickets"

    def fetch(self, watermark: str | None, limit: int | None = None) -> list[dict]:
        if self.spec.get("paths"):
            return self._from_csv(watermark, limit)
        if self.spec.get("vendor"):
            return self._from_api(watermark, limit)
        return []

    # ----------------------------------------------------------------------- csv

    def _from_csv(self, watermark: str | None, limit: int | None) -> list[dict]:
        since = self.since(watermark)
        records: list[dict] = []
        for raw_path in self.spec.get("paths", []):
            root = Path(os.path.expanduser(raw_path))
            files = [root] if root.is_file() else sorted(root.glob("*.csv"), reverse=True)
            for path in files:
                if not path.exists():
                    continue
                with path.open(newline="", errors="replace") as handle:
                    for index, row in enumerate(csv.DictReader(handle)):
                        if limit and len(records) >= limit:
                            return records
                        text = pick(row, TEXT_COLUMNS)
                        if len(text.strip()) < 40:
                            continue
                        occurred = iso(pick(row, DATE_COLUMNS))
                        if occurred < since:
                            continue
                        native = pick(row, ["id", "ticket_id", "number"]) or f"{path.name}:{index}"
                        records.append(self.record(
                            native_id=native,
                            occurred_at=occurred,
                            text=text,
                            title=pick(row, TITLE_COLUMNS),
                            meta={"resolution": pick(row, STATUS_COLUMNS), "file": path.name},
                        ))
        return records

    # ----------------------------------------------------------------------- api

    def _from_api(self, watermark: str | None, limit: int | None) -> list[dict]:
        vendor = self.spec["vendor"]
        spec = API.get(vendor)
        token = self.token()
        if not spec or not token:
            return []

        url = spec["url"].format(subdomain=self.spec.get("subdomain", ""))
        try:
            response = requests.get(url, headers=spec["headers"](token),
                                    params={"per_page": min(limit or 100, 100)}, timeout=30)
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"  {self.id}: api call failed, {error}")
            return []

        since = self.since(watermark)
        records = []
        for item in spec["items"](response.json()):
            occurred = iso(spec["date"](item))
            if occurred < since:
                continue
            text = spec["text"](item) or ""
            if len(text.strip()) < 40:
                continue
            records.append(self.record(
                native_id=spec["native"](item),
                occurred_at=occurred,
                text=text,
                title=spec["title"](item) or "",
                meta={"vendor": vendor},
            ))
            if limit and len(records) >= limit:
                break
        return records
