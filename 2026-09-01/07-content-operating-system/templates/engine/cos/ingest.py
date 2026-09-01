"""Cron 1. Ingestion.

Pulls every enabled source since its watermark, redacts, deduplicates, and appends to the
evidence store. Reads and writes local files. It never publishes, never sends, and never
spends, which is what makes it safe to run unattended.

    python3 -m cos.ingest                          # everything enabled
    python3 -m cos.ingest --source calls_fathom    # one source
    python3 -m cos.ingest --dry-run --limit 5      # print what it would write, write nothing
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from . import config as config_module
from .redact import looks_unredacted, redact_record
from .sources import build
from .store import Store


class Lock:
    """A pid lock so two scheduled runs never overlap."""

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                pid = int(self.path.read_text().strip())
                os.kill(pid, 0)
            except (ValueError, ProcessLookupError, PermissionError):
                self.path.unlink(missing_ok=True)  # stale, the process is gone
            else:
                raise SystemExit(f"already running as pid {pid}. lock: {self.path}")
        self.path.write_text(str(os.getpid()))
        return self

    def __exit__(self, *_):
        self.path.unlink(missing_ok=True)


def run(cfg: dict, only: str | None, dry_run: bool, limit: int | None) -> int:
    root = Path(cfg["_root"])
    store = Store(root)
    keep = cfg["redaction"].get("keep", [])
    redaction_on = cfg["redaction"].get("enabled", True)

    started = datetime.now(timezone.utc)
    results: list[dict] = []
    exit_code = 0

    for spec in config_module.enabled_sources(cfg):
        if only and spec["id"] != only:
            continue
        began = time.time()
        try:
            source = build(spec)
        except ValueError as error:
            print(f"{spec.get('id')}: {error}")
            exit_code = 1
            continue

        print(f"{source.describe()} ...", flush=True)
        try:
            raw = source.fetch(store.watermark(spec["id"]), limit=limit)
        except Exception as error:  # a broken source must not stop the run
            print(f"  failed: {type(error).__name__}: {error}")
            results.append({"source": spec["id"], "error": str(error), "written": 0})
            exit_code = 1
            continue

        records = [redact_record(r, keep) for r in raw] if redaction_on else raw

        flagged = []
        for record in records:
            reasons = looks_unredacted(record)
            if reasons:
                flagged.append((record["id"], reasons))

        if dry_run:
            print(f"  would write {len(records)} records (fetched {len(raw)})")
            for record in records[: limit or 5]:
                preview = " ".join(record["text"].split())[:220]
                print(f"  --- {record['occurred_at'][:10]}  {record.get('title', '')[:60]}")
                print(f"      {preview}")
            written = 0
        else:
            written = store.write(records)
            print(f"  wrote {written} new of {len(records)} fetched")

        if flagged:
            print(f"  REDACTION WARNING: {len(flagged)} records still look identifying")
            for record_id, reasons in flagged[:3]:
                print(f"    {record_id}: {'; '.join(reasons)}")
            print("    this source needs a custom rule before it goes near a real run")
            exit_code = 1

        results.append({
            "source": spec["id"],
            "fetched": len(raw),
            "written": written,
            "flagged": len(flagged),
            "seconds": round(time.time() - began, 1),
        })

    total = sum(r.get("written", 0) for r in results)
    log = {
        "job": "ingest",
        "started": started.isoformat(timespec="seconds"),
        "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "results": results,
        "total_written": total,
        "store": store.stats(),
        "exit_code": exit_code,
    }
    log_dir = root / "outputs" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"ingest-{started.strftime('%Y%m%d-%H%M%S')}.json"
    log_path.write_text(json.dumps(log, indent=2))

    if dry_run:
        print(f"\ndry run, nothing written. log: {log_path}")
    else:
        print(f"\n{total} new records. log: {log_path}")
    if total == 0 and not dry_run and not results:
        print("no sources ran. check engine/config.json")
        exit_code = 1
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="pull evidence into the store")
    parser.add_argument("--source", help="only this source id")
    parser.add_argument("--dry-run", action="store_true", help="print, write nothing")
    parser.add_argument("--limit", type=int, help="cap records per source")
    args = parser.parse_args()

    config_module.load_dotenv()
    cfg = config_module.load()
    problems = config_module.check(cfg)
    if problems and not args.dry_run:
        print("config check failed:")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    with Lock(Path(cfg["_root"]) / "outputs" / "logs" / ".ingest.lock"):
        return run(cfg, args.source, args.dry_run, args.limit)


if __name__ == "__main__":
    sys.exit(main())
