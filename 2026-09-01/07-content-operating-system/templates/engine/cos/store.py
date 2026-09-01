"""The evidence store.

Flat JSONL under outputs/evidence/, one file per source type per month, plus a small index
holding seen ids and per-source watermarks. No database, no service, greppable by hand and
readable by an agent.

If a source ever outgrows this (roughly past a few hundred thousand records), the migration
is to SQLite with the same record shape. Nothing above this module needs to change.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_id(source_id: str, native_id: str) -> str:
    return hashlib.sha1(f"{source_id}:{native_id}".encode()).hexdigest()[:16]


class Store:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.dir = self.root / "outputs" / "evidence"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.dir / "index.json"
        self.index = self._load_index()

    def _load_index(self) -> dict:
        if self.index_path.exists():
            with self.index_path.open() as handle:
                return json.load(handle)
        return {"seen": {}, "watermarks": {}, "counts": {}}

    def save_index(self) -> None:
        tmp = self.index_path.with_suffix(".json.tmp")
        with tmp.open("w") as handle:
            json.dump(self.index, handle, indent=2, sort_keys=True)
        tmp.replace(self.index_path)

    # ------------------------------------------------------------------ writes

    def has(self, record_id: str) -> bool:
        return record_id in self.index["seen"]

    def watermark(self, source_id: str) -> str | None:
        return self.index["watermarks"].get(source_id)

    def set_watermark(self, source_id: str, value: str) -> None:
        current = self.index["watermarks"].get(source_id)
        if current is None or value > current:
            self.index["watermarks"][source_id] = value

    def write(self, records: list[dict]) -> int:
        """Append records, skipping ones already seen. Returns how many were actually written."""
        written = 0
        handles: dict[Path, object] = {}
        try:
            for record in records:
                if self.has(record["id"]):
                    continue
                month = (record.get("occurred_at") or _now())[:7]
                path = self.dir / record["source_type"] / f"{month}.jsonl"
                path.parent.mkdir(parents=True, exist_ok=True)
                if path not in handles:
                    handles[path] = path.open("a")
                record.setdefault("ingested_at", _now())
                handles[path].write(json.dumps(record, ensure_ascii=False) + "\n")
                self.index["seen"][record["id"]] = record["source_id"]
                source_counts = self.index["counts"].setdefault(record["source_id"], 0)
                self.index["counts"][record["source_id"]] = source_counts + 1
                if record.get("occurred_at"):
                    self.set_watermark(record["source_id"], record["occurred_at"])
                written += 1
        finally:
            for handle in handles.values():
                handle.close()
        self.save_index()
        return written

    # ------------------------------------------------------------------- reads

    def read_all(self, since: str | None = None, source_types: list[str] | None = None):
        """Yield records, newest month first, optionally filtered by date and source type."""
        types = source_types or [p.name for p in self.dir.iterdir() if p.is_dir()]
        for source_type in types:
            type_dir = self.dir / source_type
            if not type_dir.exists():
                continue
            for path in sorted(type_dir.glob("*.jsonl"), reverse=True):
                for line in path.read_text().splitlines():
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if since and (record.get("occurred_at") or "") < since:
                        continue
                    yield record

    def stats(self) -> dict:
        return {
            "total": len(self.index["seen"]),
            "by_source": dict(self.index["counts"]),
            "watermarks": dict(self.index["watermarks"]),
        }
