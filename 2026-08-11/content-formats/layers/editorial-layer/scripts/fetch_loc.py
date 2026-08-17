#!/usr/bin/env python3
"""
Fetch public-domain newspaper pages from the Library of Congress for the editorial layer.

Chronicling America is the first stop for any US period between 1770 and 1963: full-page scans,
an open API, and no licence question. Everything downloaded here is recorded in sources.json next
to the images, because the layer skill requires a source per asset.

Two things that cost time if you do not know them:
  - The old chroniclingamerica.loc.gov/search API 308-redirects now. Use www.loc.gov/collections.
  - The response is large and gzipped; without --compressed / Accept-Encoding the body arrives
    truncated and json.load fails on an unterminated string.

./fetch_loc.py --q "electric motor factory" --dates 1886/1895 --n 6 --out arch/
"""
import argparse
import json
import os
import urllib.parse
import urllib.request

API = "https://www.loc.gov/collections/chronicling-america/"
UA = "house-research/1.0 (you@yourdomain.example)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        import gzip
        raw = gzip.decompress(raw)
    return raw


def search(q, dates, n):
    url = API + "?" + urllib.parse.urlencode({"q": q, "dates": dates, "fo": "json", "c": max(n, 10)})
    return json.loads(get(url).decode("utf-8", "replace")).get("results", [])


def page_jpg(image_urls, pct):
    """Pick the IIIF image service entry and ask it for a sane size. The list also carries an
    ALTO XML text-services link, which is not an image."""
    for u in image_urls or []:
        if "image-services/iiif" in u:
            base = u.split("/full/")[0]
            return f"{base}/full/pct:{pct}/0/default.jpg"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--dates", required=True, help="YYYY/YYYY")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--pct", type=int, default=25, help="IIIF percent size; 25 is ~1500px wide")
    ap.add_argument("--out", default="arch")
    ap.add_argument("--tag", default=None, help="filename prefix, defaults to a slug of --q")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    tag = a.tag or "-".join(a.q.lower().split())[:24]
    src_path = os.path.join(a.out, "sources.json")
    sources = json.load(open(src_path)) if os.path.exists(src_path) else []

    got = 0
    for r in search(a.q, a.dates, a.n):
        if got >= a.n:
            break
        url = page_jpg(r.get("image_url"), a.pct)
        if not url:
            continue
        name = f"{tag}-{got + 1:02d}.jpg"
        path = os.path.join(a.out, name)
        try:
            data = get(url)
        except Exception as e:
            print(f"[skip] {name}  {e}")
            continue
        open(path, "wb").write(data)
        sources.append({
            "file": name, "date": r.get("date"), "title": r.get("title"),
            "item": r.get("id"), "image": url, "query": a.q, "dates": a.dates,
            "rights": "Public domain, Library of Congress Chronicling America (NDNP)",
        })
        print(f"[arch] {name}  {r.get('date')}  {len(data) // 1024}kB  {str(r.get('title'))[:48]}")
        got += 1

    json.dump(sources, open(src_path, "w"), indent=1)
    print(f"[arch] {got} pages, sources recorded in {src_path}")


if __name__ == "__main__":
    main()
