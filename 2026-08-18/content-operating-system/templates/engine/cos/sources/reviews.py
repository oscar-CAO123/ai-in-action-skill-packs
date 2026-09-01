"""Reviews: their own and their competitors'.

Reviews are pre-filtered for emotion and they name the specific thing that delighted or
infuriated someone. Competitor reviews are as useful as their own, and are often the fastest
route to a positioning line.

Three routes, in order of how little setup they need: a pasted or exported file, an app store
RSS feed, or the Google Places API.
"""

from __future__ import annotations

import csv
import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from .base import Source, iso

ATOM = "{http://www.w3.org/2005/Atom}"
RATING_COLUMNS = ["rating", "stars", "score"]
TEXT_COLUMNS = ["review", "text", "comment", "body", "content", "review_text"]
DATE_COLUMNS = ["date", "created_at", "published", "time", "review_date"]


def pick(row: dict, candidates: list[str]) -> str:
    lowered = {k.lower().strip(): v for k, v in row.items() if k}
    for candidate in candidates:
        value = lowered.get(candidate)
        if value not in (None, ""):
            return str(value)
    return ""


class ReviewsSource(Source):
    type = "reviews"

    def fetch(self, watermark: str | None, limit: int | None = None) -> list[dict]:
        route = self.spec.get("route", "file")
        if route == "file":
            return self._from_file(watermark, limit)
        if route == "appstore":
            return self._appstore(watermark, limit)
        if route == "google_places":
            return self._google_places(watermark, limit)
        return []

    # ------------------------------------------------------------------ file

    def _from_file(self, watermark: str | None, limit: int | None) -> list[dict]:
        since = self.since(watermark)
        records: list[dict] = []
        for raw_path in self.spec.get("paths", []):
            root = Path(os.path.expanduser(raw_path))
            files = [root] if root.is_file() else sorted(root.glob("*"))
            for path in files:
                if not path.is_file():
                    continue
                if path.suffix.lower() == ".csv":
                    with path.open(newline="", errors="replace") as handle:
                        for index, row in enumerate(csv.DictReader(handle)):
                            text = pick(row, TEXT_COLUMNS)
                            if len(text.strip()) < 30:
                                continue
                            occurred = iso(pick(row, DATE_COLUMNS))
                            if occurred < since:
                                continue
                            records.append(self._record(
                                f"{path.name}:{index}", occurred, text,
                                pick(row, RATING_COLUMNS)))
                            if limit and len(records) >= limit:
                                return records
                elif path.suffix.lower() == ".json":
                    try:
                        blob = json.loads(path.read_text(errors="replace"))
                    except json.JSONDecodeError:
                        continue
                    items = blob if isinstance(blob, list) else blob.get("reviews", [])
                    for index, item in enumerate(items):
                        if not isinstance(item, dict):
                            continue
                        text = pick(item, TEXT_COLUMNS)
                        if len(text.strip()) < 30:
                            continue
                        occurred = iso(pick(item, DATE_COLUMNS))
                        if occurred < since:
                            continue
                        records.append(self._record(
                            f"{path.name}:{index}", occurred, text, pick(item, RATING_COLUMNS)))
                        if limit and len(records) >= limit:
                            return records
        return records

    # -------------------------------------------------------------- app store

    def _appstore(self, watermark: str | None, limit: int | None) -> list[dict]:
        app_id = self.spec.get("app_id")
        country = self.spec.get("country", "au")
        if not app_id:
            return []
        url = (f"https://itunes.apple.com/{country}/rss/customerreviews/"
               f"id={app_id}/sortby=mostrecent/xml")
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            tree = ET.fromstring(response.content)
        except (requests.RequestException, ET.ParseError) as error:
            print(f"  {self.id}: app store feed failed, {error}")
            return []

        since = self.since(watermark)
        records = []
        for entry in tree.findall(f"{ATOM}entry"):
            content = entry.find(f"{ATOM}content")
            updated = entry.find(f"{ATOM}updated")
            entry_id = entry.find(f"{ATOM}id")
            rating = entry.find("{http://itunes.apple.com/rss}rating")
            if content is None or updated is None:
                continue
            occurred = iso(updated.text)
            if occurred < since:
                continue
            text = (content.text or "").strip()
            if len(text) < 30:
                continue
            records.append(self._record(
                entry_id.text if entry_id is not None else text[:32],
                occurred, text, rating.text if rating is not None else ""))
            if limit and len(records) >= limit:
                break
        return records

    # ---------------------------------------------------------- google places

    def _google_places(self, watermark: str | None, limit: int | None) -> list[dict]:
        key = self.token()
        place_id = self.spec.get("place_id")
        if not key or not place_id:
            return []
        try:
            response = requests.get(
                "https://maps.googleapis.com/maps/api/place/details/json",
                params={"place_id": place_id, "fields": "reviews,name", "key": key},
                timeout=20,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"  {self.id}: places call failed, {error}")
            return []

        since = self.since(watermark)
        records = []
        for review in (response.json().get("result") or {}).get("reviews", []):
            occurred = iso(review.get("time"))
            if occurred < since:
                continue
            text = (review.get("text") or "").strip()
            if len(text) < 30:
                continue
            records.append(self._record(
                f"{place_id}:{review.get('time')}", occurred, text, review.get("rating")))
            if limit and len(records) >= limit:
                break
        return records

    # ----------------------------------------------------------------- shared

    def _record(self, native_id: str, occurred_at: str, text: str, rating) -> dict:
        try:
            rating_value = int(float(re.sub(r"[^\d.]", "", str(rating)))) if rating else None
        except ValueError:
            rating_value = None
        return self.record(
            native_id=native_id,
            occurred_at=occurred_at,
            text=text,
            title="",
            meta={
                "platform": self.spec.get("route", "file"),
                "rating": rating_value,
                "whose": self.spec.get("whose", "own"),
                "subject": self.spec.get("subject", ""),
            },
        )
