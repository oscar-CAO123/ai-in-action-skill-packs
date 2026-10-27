"""Forums: where the industry complains in public.

Reddit and Hacker News read without a key at these volumes. X needs a paid bearer token, and
if the operator does not already have one, this source skips it and says so rather than
pretending it ran.

The rule that keeps this useful: collect the OBJECTION, not the topic. A thread titled
"AI tools for trades" is noise. A comment inside it saying "we tried this and it took longer
than doing it by hand" is the content. That is why comments are pulled, not only posts.
"""

from __future__ import annotations

import time

import requests

from .base import Source, iso

USER_AGENT = "content-operating-system/1.0 (evidence ingestion, low volume)"

# A comment with one of these is somebody describing a real experience rather than speculating.
OBJECTION_MARKERS = [
    "we tried", "i tried", "we switched", "we ended up", "waste of", "took longer",
    "does not work", "doesn't work", "didn't work", "gave up", "cancelled", "canceled",
    "regret", "the problem is", "the issue is", "in my experience", "we used to",
    "nobody tells you", "turned out", "cost us", "wish i had known", "wish we had",
    "the hard part", "what actually happened",
]


def has_objection(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in OBJECTION_MARKERS)


class ForumsSource(Source):
    type = "forums"

    def fetch(self, watermark: str | None, limit: int | None = None) -> list[dict]:
        platform = self.spec.get("platform", "reddit")
        if platform == "reddit":
            return self._reddit(watermark, limit)
        if platform == "hackernews":
            return self._hackernews(watermark, limit)
        if platform == "x":
            return self._x(watermark, limit)
        return []

    # -------------------------------------------------------------------- reddit

    def _reddit(self, watermark: str | None, limit: int | None) -> list[dict]:
        since = self.since(watermark)
        records: list[dict] = []
        headers = {"User-Agent": USER_AGENT}

        for board in self.spec.get("boards", []):
            for listing in self.spec.get("listings", ["new", "top"]):
                url = f"https://www.reddit.com/r/{board}/{listing}.json"
                params = {"limit": 50}
                if listing == "top":
                    params["t"] = "month"
                try:
                    response = requests.get(url, headers=headers, params=params, timeout=20)
                    response.raise_for_status()
                except requests.RequestException as error:
                    print(f"  {self.id}: r/{board} {listing} failed, {error}")
                    continue

                for child in response.json().get("data", {}).get("children", []):
                    post = child.get("data", {})
                    occurred = iso(post.get("created_utc"))
                    if occurred < since:
                        continue
                    body = (post.get("selftext") or "").strip()
                    title = (post.get("title") or "").strip()
                    if len(body) < 80 and not has_objection(title):
                        continue
                    records.append(self.record(
                        native_id=post.get("id", ""),
                        occurred_at=occurred,
                        text=body or title,
                        title=title,
                        meta={
                            "platform": "reddit",
                            "board": board,
                            "engagement": post.get("score", 0),
                            "comments": post.get("num_comments", 0),
                            "permalink": f"https://reddit.com{post.get('permalink', '')}",
                            "objection": has_objection(f"{title} {body}"),
                        },
                    ))
                    if limit and len(records) >= limit:
                        return records
                time.sleep(2)  # stay well under the unauthenticated rate limit
        return records

    # --------------------------------------------------------------- hacker news

    def _hackernews(self, watermark: str | None, limit: int | None) -> list[dict]:
        since = self.since(watermark)
        records: list[dict] = []
        for query in self.spec.get("queries", []):
            try:
                response = requests.get(
                    "https://hn.algolia.com/api/v1/search_by_date",
                    params={"query": query, "tags": "comment", "hitsPerPage": 50},
                    timeout=20,
                )
                response.raise_for_status()
            except requests.RequestException as error:
                print(f"  {self.id}: hn '{query}' failed, {error}")
                continue

            for hit in response.json().get("hits", []):
                occurred = iso(hit.get("created_at"))
                if occurred < since:
                    continue
                text = (hit.get("comment_text") or "").strip()
                if len(text) < 120:
                    continue
                records.append(self.record(
                    native_id=hit.get("objectID", ""),
                    occurred_at=occurred,
                    text=text,
                    title=hit.get("story_title", "") or query,
                    meta={
                        "platform": "hackernews",
                        "board": query,
                        "engagement": hit.get("points") or 0,
                        "permalink": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                        "objection": has_objection(text),
                    },
                ))
                if limit and len(records) >= limit:
                    return records
            time.sleep(1)
        return records

    # ------------------------------------------------------------------------- x

    def _x(self, watermark: str | None, limit: int | None) -> list[dict]:
        token = self.token()
        if not token:
            print(f"  {self.id}: skipped, no bearer token. X has no usable free read tier.")
            return []

        since = self.since(watermark)
        records: list[dict] = []
        for query in self.spec.get("queries", []):
            try:
                response = requests.get(
                    "https://api.x.com/2/tweets/search/recent",
                    headers={"Authorization": f"Bearer {token}"},
                    params={
                        "query": f"{query} -is:retweet lang:en",
                        "max_results": 100,
                        "tweet.fields": "created_at,public_metrics",
                    },
                    timeout=20,
                )
                response.raise_for_status()
            except requests.RequestException as error:
                print(f"  {self.id}: x '{query}' failed, {error}")
                continue

            for item in response.json().get("data", []):
                occurred = iso(item.get("created_at"))
                if occurred < since:
                    continue
                text = item.get("text", "")
                if len(text) < 80:
                    continue
                metrics = item.get("public_metrics") or {}
                records.append(self.record(
                    native_id=item.get("id", ""),
                    occurred_at=occurred,
                    text=text,
                    title="",
                    meta={
                        "platform": "x",
                        "board": query,
                        "engagement": metrics.get("like_count", 0),
                        "permalink": f"https://x.com/i/status/{item.get('id')}",
                        "objection": has_objection(text),
                    },
                ))
                if limit and len(records) >= limit:
                    return records
        return records
