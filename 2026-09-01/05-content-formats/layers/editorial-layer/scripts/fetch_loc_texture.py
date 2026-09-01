#!/usr/bin/env python3
"""Fetch public-domain TEXTURE material from the Library of Congress, beyond newspapers.

`fetch_loc.py` is hardcoded to the Chronicling America collection, so every bed it feeds is
newsprint. A bed built from one material reads as one material however you arrange it. This
reaches the other LoC endpoints that answer `?fo=json` the same way, so a bed can be layered
out of genuinely different surfaces: map hatching, engraved plates, technical line art,
catalogue pages.

./fetch_loc_texture.py --endpoint maps --q "city plan" --dates 1880/1929 --n 4 --out t/maps
./fetch_loc_texture.py --endpoint photos --q "steel mill" --dates 1900/1929 --n 4 --out t/prints

Endpoints that work: maps, photos, collections/<name>. Everything downloaded is recorded in
sources.json next to the images, because the layer skill requires a source per asset.
"""
import argparse
import gzip
import json
import os
import urllib.parse
import urllib.request

UA = "house-research/1.0 (you@yourdomain.example)"

ENDPOINTS = {
    "maps": ("https://www.loc.gov/maps/", "Public domain, Library of Congress Geography & Map Division"),
    "photos": ("https://www.loc.gov/photos/", "Public domain, Library of Congress Prints & Photographs"),
    "prints": ("https://www.loc.gov/pictures/", "Public domain, Library of Congress Prints & Photographs"),
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
        enc = r.headers.get("Content-Encoding")
    return gzip.decompress(raw) if enc == "gzip" else raw


def page_jpg(image_urls, pct):
    """Prefer the IIIF service so we can ask for a size; fall back to the largest plain jpg."""
    for u in image_urls or []:
        if "image-services/iiif" in u:
            return f"{u.split('/full/')[0]}/full/pct:{pct}/0/default.jpg"
    for u in reversed(image_urls or []):
        if str(u).lower().endswith((".jpg", ".jpeg")):
            return u if str(u).startswith("http") else "https:" + u
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", required=True, help="maps | photos | prints | collections/<name>")
    ap.add_argument("--q", required=True)
    ap.add_argument("--dates", default=None, help="YYYY/YYYY, omitted for undated material")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--pct", type=int, default=25)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()

    base, rights = ENDPOINTS.get(
        a.endpoint, (f"https://www.loc.gov/{a.endpoint.strip('/')}/", "Public domain, Library of Congress"))

    params = {"q": a.q, "fo": "json", "c": max(a.n, 10)}
    if a.dates:
        params["dates"] = a.dates
    results = json.loads(get(base + "?" + urllib.parse.urlencode(params)).decode("utf-8", "replace"))
    results = results.get("results", [])

    os.makedirs(a.out, exist_ok=True)
    tag = a.tag or "-".join(a.q.lower().split())[:24]
    src_path = os.path.join(a.out, "sources.json")
    sources = json.load(open(src_path)) if os.path.exists(src_path) else []

    got = 0
    for r in results:
        if got >= a.n:
            break
        url = page_jpg(r.get("image_url"), a.pct)
        if not url:
            continue
        name = f"{tag}-{got + 1:02d}.jpg"
        try:
            data = get(url)
        except Exception as e:
            print(f"[skip] {name}  {e}")
            continue
        if len(data) < 40_000:          # thumbnails are useless as a bed
            continue
        open(os.path.join(a.out, name), "wb").write(data)
        sources.append({
            "file": name, "date": r.get("date"), "title": r.get("title"),
            "item": r.get("id"), "image": url, "query": a.q,
            "endpoint": a.endpoint, "rights": rights,
        })
        print(f"[tex] {name}  {len(data) // 1024}kB  {str(r.get('title'))[:52]}")
        got += 1

    json.dump(sources, open(src_path, "w"), indent=1)
    print(f"[tex] {got} items -> {a.out}")


if __name__ == "__main__":
    main()
