#!/usr/bin/env python3
"""Push the 11 ready-to-go noir pain carousels to Supabase Storage, in place.

    python3 push_noir_ready.py --dry-run     # list what would move, write nothing
    python3 push_noir_ready.py               # upload

Each slide overwrites its existing `content-media/<slug>/slide-NN.png` object with x-upsert.
The paths do not move, so `content_items.media_urls` and `thumbnail_url` stay valid and no
database row is touched. Storage serves these objects `cache-control: no-cache`, so the CRM
content page picks the new slides up on the next request.

Source of truth is `out-noir/<slug>/`, the thin-your display typeface 200 canon. The retired Anton renders that
these replace are parked at `out-noir/_superseded/<slug>/`; to roll back, point SRC at that
directory and re-run.

Credentials come from the vault's single merged env at `.secrets/.env`: SUPABASE_URL and
SUPABASE_SERVICE_ROLE_KEY.
"""
import hashlib
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "out-noir"
SECRETS = Path.home / "AIOS" / ".secrets" / ".env"
BUCKET = "content-media"

SLUGS = [
    "noir-pain-admin", "noir-pain-cx", "noir-pain-systems", "noir-pain-inbox",
    "noir-pain-leads", "noir-pain-numbers", "noir-pain-delivery", "noir-pain-quoting",
    "noir-pain-execution-gap", "noir-pain-leadgen", "noir-pain-bottleneck",
]


def load_env:
    """Read the two keys we need. The merged .env has shell-hostile lines, so parse, never source."""
    env = {}
    for line in SECRETS.read_text.splitlines:
        line = line.strip
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip] = v.strip.strip('"').strip("'")
    url = env.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    key = env.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        sys.exit("missing SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY in .secrets/.env")
    return url.rstrip("/"), key


def put(url, key, obj_key, body):
    req = urllib.request.Request(
        f"{url}/storage/v1/object/{BUCKET}/{obj_key}",
        data=body, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "image/png",
                 "x-upsert": "true", "Cache-Control": "no-cache"},)
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.status


def main:
    dry = "--dry-run" in sys.argv
    url, key = load_env
    ok = fail = 0
    for slug in SLUGS:
        for i in range(1, 7):
            p = SRC / slug / f"slide-{i:02d}.png"
            if not p.exists:
                print(f"MISSING {p}")
                fail += 1
                continue
            body = p.read_bytes
            obj = f"{slug}/slide-{i:02d}.png"
            digest = hashlib.sha256(body).hexdigest[:12]
            if dry:
                print(f"would push {obj:<44} {len(body)/1e6:5.2f} MB  {digest}")
                ok += 1
                continue
            try:
                put(url, key, obj, body)
                print(f"pushed {obj:<44} {len(body)/1e6:5.2f} MB  {digest}")
                ok += 1
            except Exception as e:
                print(f"FAILED {obj}: {e}")
                fail += 1
    print(f"\n{'would push' if dry else 'pushed'} {ok}, failed {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main)
