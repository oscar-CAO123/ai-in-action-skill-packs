#!/usr/bin/env bash
# Every YouTube appearance of the speakers: flat searches, by relevance and by date, no downloads.
# Reads speakers.json for the names and companies; writes inv/s_*.tsv and inv/d_*.tsv, then
# merge and dedupe them into inv/episodes.tsv by hand (or with a five-line python).
# Usage: scripts/search.sh   (from the workspace)
set -u
mkdir -p inv; cd inv
mapfile -t Q < <(python3 -c '
import json
s = json.load(open("../speakers.json"))
for k, v in s.items():
    for c in [v["name"]] + v.get("companies", []):
        for t in ("podcast", "interview"):
            print(f"{v[\"name\"]} {t}" if c == v["name"] else f"{v[\"name\"]} {c}")
    for th in v.get("themes", []):
        print(f"{v[\"name\"]} {th}")
' | sort -u)
for s in "${Q[@]}"; do
  f="${s// /_}"
  yt-dlp "ytsearch40:$s" --flat-playlist --no-warnings --print "%(id)s\t%(duration)s\t%(channel)s\t%(title)s" > "s_$f.tsv" 2>/dev/null &
  yt-dlp "ytsearchdate40:$s" --flat-playlist --no-warnings --print "%(id)s\t%(duration)s\t%(channel)s\t%(title)s" > "d_$f.tsv" 2>/dev/null &
done
wait
cat s_*.tsv d_*.tsv | sort -u -t$'\t' -k1,1 > fresh_all.tsv
echo "$(wc -l < fresh_all.tsv) unique videos in inv/fresh_all.tsv; read the titles, then write inv/episodes.tsv as: speaker<TAB>id<TAB>duration<TAB>channel<TAB>title<TAB>source"
